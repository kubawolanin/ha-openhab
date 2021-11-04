"""Data update coordinator for integration openHAB."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiClientException, OpenHABApiClient
from .const import DATA_COORDINATOR_UPDATE_INTERVAL, DOMAIN, LOGGER


class OpenHABDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, api: OpenHABApiClient) -> None:
        """Initialize."""
        self.api = api
        self.platforms: list[str] = []
        self.version: str = ""
        self.is_online = False

        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=DATA_COORDINATOR_UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            if self.version is None or len(self.version) == 0:
                self.version = await self.api.async_get_version()

            items = await self.api.async_get_items()
            self.is_online = bool(items)
            return items

        except ApiClientException as exception:
            raise UpdateFailed(exception) from exception
