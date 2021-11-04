"""Device Tracker platform for openhab."""
from homeassistant.components.device_tracker import SOURCE_TYPE_GPS
from homeassistant.components.device_tracker.config_entry import TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN, DEVICE_TRACKER, ITEMS_MAP
from .entity import OpenHABEntity
from .device_classes_map import SENSOR_DEVICE_CLASS_MAP


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup device_tracker platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OpenHABTracker(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ in ITEMS_MAP[DEVICE_TRACKER]
    )


class OpenHABTracker(OpenHABEntity, TrackerEntity):
    """openhab device_tracker class."""

    _attr_device_class_map = SENSOR_DEVICE_CLASS_MAP

    @property
    def location_name(self):
        """Return the latitude."""
        return self.item.label if len(self.item.label) > 0 else self.item.name

    @property
    def latitude(self):
        """Return the latitude."""
        if (
            self.item._state is not None
            and self.item._state != "NULL"
            and self.item._state != "UNDEF"
        ):
            return float(self.item._state.split(",")[0])
        return None

    @property
    def longitude(self):
        """Return the longitude."""
        if (
            self.item._state is not None
            and self.item._state != "NULL"
            and self.item._state != "UNDEF"
        ):
            return float(self.item._state.split(",")[1])
        return None

    @property
    def source_type(self) -> str:
        """Return the source type, eg gps or router, of the device."""
        return SOURCE_TYPE_GPS
