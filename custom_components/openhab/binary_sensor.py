"""Binary sensor platform for openhab."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_SENSOR, DOMAIN, ITEMS_MAP
from .device_classes_map import BINARY_SENSOR_DEVICE_CLASS_MAP
from .entity import OpenHABEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        OpenHABBinarySensor(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ in ITEMS_MAP[BINARY_SENSOR]
    )


class OpenHABBinarySensor(OpenHABEntity, BinarySensorEntity):
    """openhab binary_sensor class."""

    _attr_device_class_map = BINARY_SENSOR_DEVICE_CLASS_MAP

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.item._state == "OPEN"
