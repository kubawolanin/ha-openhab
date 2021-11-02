"""Sensor platform for openhab."""
from homeassistant.components.cover import ATTR_POSITION, CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .entity import OpenHABEntity
from .device_classes_map import COVER_DEVICE_CLASS_MAP

from typing import Any, cast


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OpenHABCover(hass=hass, coordinator=coordinator, item=item)
        for item in coordinator.data.values()
        if item.type_ == "Rollershutter"
    )


class OpenHABCover(OpenHABEntity, CoverEntity):
    """openhab Cover class."""

    _attr_device_class_map = COVER_DEVICE_CLASS_MAP

    @property
    def current_cover_position(self) -> int:
        """Return current position of cover.
        None is unknown, 0 is closed, 100 is fully open.
        """
        if not self.item._state:
            return None
        return 100 - cast(int, self.item._state)

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""
        if not self.item:
            return
        await self.hass.async_add_executor_job(
            self.item.command, int(kwargs[ATTR_POSITION])
        )

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        if not self.item:
            return
        await self.hass.async_add_executor_job(self.item.up)

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close cover."""
        if not self.item:
            return
        await self.hass.async_add_executor_job(self.item.down)

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Close cover."""
        if not self.item:
            return
        await self.hass.async_add_executor_job(self.item.stop)

    @property
    def is_closed(self) -> bool:
        """Return if the cover is closed or not."""
        return self.current_cover_position == 0
