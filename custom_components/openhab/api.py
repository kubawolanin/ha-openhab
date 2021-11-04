"""Sample API Client."""
from __future__ import annotations

from typing import Any

import aiohttp
from openhab import OpenHAB

API_HEADERS = {aiohttp.hdrs.CONTENT_TYPE: "application/json; charset=UTF-8"}


class ApiClientException(Exception):
    """Api Client Exception."""


class OpenHABApiClient:
    def __init__(
        self,
        hass,
        base_url: str,
        username: str | None,
        password: str | None,
    ) -> None:
        """openHAB API Client."""
        self.hass = hass
        self._base_url = base_url
        self._rest_url = f"{base_url}/rest"
        self._username = username
        self._password = password
        if len(username) > 0:
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

    async def async_set_state(self, item_name: str, command: str) -> None:
        """Set Item state"""
        item = await self.hass.async_add_executor_job(self.async_get_item, item_name)
        await item.command(command)
