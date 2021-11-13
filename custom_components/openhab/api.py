"""Sample API Client."""
from __future__ import annotations

from typing import Any

import aiohttp
from openhab import OpenHAB

from .const import CONF_AUTH_TYPE_BASIC, CONF_AUTH_TYPE_TOKEN

API_HEADERS = {aiohttp.hdrs.CONTENT_TYPE: "application/json; charset=UTF-8"}


class ApiClientException(Exception):
    """Api Client Exception."""


class OpenHABApiClient:
    """API Client"""

    # pylint: disable=R0913
    def __init__(
        self,
        hass,
        base_url: str,
        auth_type: str,
        auth_token: str | None,
        username: str | None,
        password: str | None,
    ) -> None:
        """openHAB API Client."""
        self.hass = hass
        self._base_url = base_url
        self._rest_url = f"{base_url}/rest"
        self._username = username
        self._password = password

        if auth_type == CONF_AUTH_TYPE_TOKEN and auth_token is not None:
            API_HEADERS["X-OPENHAB-TOKEN"] = auth_token
            self.openhab = OpenHAB(self._rest_url)

        if auth_type == CONF_AUTH_TYPE_BASIC:
            if username is not None and len(username) > 0:
                self.openhab = OpenHAB(self._rest_url, self._username, self._password)
            else:
                self.openhab = OpenHAB(self._rest_url)

    async def async_get_version(self) -> str:
        """Get all items from the API."""
        info = await self.hass.async_add_executor_job(self.openhab.req_get, "/")
        runtime_info = info["runtimeInfo"]
        return f"{runtime_info['version']} {runtime_info['buildString']}"

    async def async_get_items(self) -> dict[str, Any]:
        """Get all items from the API."""
        return await self.hass.async_add_executor_job(self.openhab.fetch_all_items)

    async def async_get_item(self, item_name: str) -> dict[str, Any]:
        """Get item from the API."""
        return await self.hass.async_add_executor_job(self.openhab.get_item, item_name)

    async def async_send_command(self, item_name: str, command: str) -> None:
        """Set Item state"""
        item = await self.hass.async_add_executor_job(self.async_get_item, item_name)
        await item.command(command)

    async def async_update_item(self, item_name: str, command: str) -> None:
        """Set Item state"""
        item = await self.hass.async_add_executor_job(self.async_get_item, item_name)
        await item.update(command)
