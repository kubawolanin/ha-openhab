"""Adds config flow for openHAB."""
from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .api import OpenHABApiClient
from .const import (
    AUTH_TYPES,
    CONF_BASE_URL,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_AUTH_TOKEN,
    CONF_AUTH_TYPE_BASIC,
    CONF_AUTH_TYPE,
    CONF_AUTH_TYPE_TOKEN,
    DOMAIN,
    PLATFORMS,
    LOGGER,
)
from .utils import strip_ip


class OpenHABFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for openHAB."""

    VERSION = 1
    data = None

    async def async_step_user(
        self,
        user_input: dict[str, str] | None = None,
    ):
        """Handle a flow initialized by the user."""
        errors = {}

        LOGGER.info(user_input)

        if user_input is not None:
            self.data = user_input
            return await self.async_step_credentials(user_input)

        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_BASE_URL,
                        default=user_input.get(CONF_BASE_URL, "http://"),
                    ): str,
                    vol.Required(
                        CONF_AUTH_TYPE,
                        default=user_input.get(CONF_AUTH_TYPE, CONF_AUTH_TYPE_TOKEN),
                    ): vol.In(AUTH_TYPES),
                }
            ),
            errors=errors,
        )

    async def async_step_credentials(
        self,
        user_input: dict[str, str] | None = None,
    ):
        """Handle a flow initialized by the user."""
        errors = {}

        user_input[CONF_BASE_URL] = self.data[CONF_BASE_URL]
        user_input[CONF_AUTH_TYPE] = self.data[CONF_AUTH_TYPE]

        if user_input is not None and (
            CONF_AUTH_TOKEN in user_input or CONF_USERNAME in user_input
        ):
            if await self._test_credentials(
                user_input[CONF_BASE_URL],
                user_input[CONF_AUTH_TYPE],
                user_input.get(CONF_AUTH_TOKEN, ""),
                user_input.get(CONF_USERNAME, ""),
                user_input.get(CONF_PASSWORD, ""),
            ):
                return self.async_create_entry(
                    title=strip_ip(user_input[CONF_BASE_URL]), data=user_input
                )
            else:
                errors["base"] = "auth"

        if user_input is None:
            user_input = {}

        if user_input[CONF_AUTH_TYPE] == CONF_AUTH_TYPE_BASIC:
            schema = {
                vol.Optional(
                    CONF_USERNAME, default=user_input.get(CONF_USERNAME, "")
                ): cv.string,
                vol.Optional(
                    CONF_PASSWORD, default=user_input.get(CONF_PASSWORD, "")
                ): cv.string,
            }
        elif user_input[CONF_AUTH_TYPE] == CONF_AUTH_TYPE_TOKEN:
            schema = {
                vol.Required(
                    CONF_AUTH_TOKEN, default=user_input.get(CONF_AUTH_TOKEN, "")
                ): cv.string,  # cv.matches_regex(r"^(oh)\.(.+)\.(.+)$"),
            }

        return self.async_show_form(
            step_id="credentials",
            data_schema=vol.Schema(schema),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return OpenHABOptionsFlowHandler(config_entry)

    async def _test_credentials(
        self,
        base_url: str,
        auth_type: str,
        auth_token: str,
        username: str,
        password: str,
    ):
        """Return true if credentials is valid."""
        try:
            client = OpenHABApiClient(
                self.hass, base_url, auth_type, auth_token, username, password
            )  # pylint: disable=broad-except
            await client.async_get_version()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class OpenHABOptionsFlowHandler(config_entries.OptionsFlow):
    """openHAB config flow options handler."""

    def __init__(self, config_entry: config_entries.ConfigEntry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return self.async_create_entry(
                title=strip_ip(self.config_entry.data.get(CONF_BASE_URL)),
                data=self.options,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )
