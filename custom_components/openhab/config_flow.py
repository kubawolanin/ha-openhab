"""Adds config flow for openHAB."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import OpenHABApiClient
from .const import CONF_BASE_URL, CONF_PASSWORD, CONF_USERNAME, DOMAIN, PLATFORMS
from .utils import strip_ip


class OpenHABFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for openHAB."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, str] | None = None,
    ):
        """Handle a flow initialized by the user."""
        errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # if await self._test_credentials(
            #     user_input[CONF_BASE_URL],
            #     user_input[CONF_USERNAME],
            #     user_input[CONF_PASSWORD],
            # ):
            return self.async_create_entry(
                title=strip_ip(user_input[CONF_BASE_URL]), data=user_input
            )
            # else:
            #     errors["base"] = "auth"

        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_BASE_URL, default=user_input.get(CONF_BASE_URL, "http://")
                    ): str,
                    vol.Optional(
                        CONF_USERNAME, default=user_input.get(CONF_USERNAME, "")
                    ): str,
                    vol.Optional(
                        CONF_PASSWORD, default=user_input.get(CONF_PASSWORD, "")
                    ): str,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return OpenHABOptionsFlowHandler(config_entry)

    async def _test_credentials(self, base_url: str, username: str, password: str):
        """Return true if credentials is valid."""
        try:
            # session = async_create_clientsession(self.hass)
            client = OpenHABApiClient(self.hass, base_url, username, password)
            await self.hass.async_add_executor_job(client.async_get_version())
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
                title=self.config_entry.data.get(CONF_USERNAME),
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
