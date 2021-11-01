"""Binary sensor platform for openhab."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import BINARY_SENSOR, BINARY_SENSOR_DEVICE_CLASS, DEFAULT_NAME, DOMAIN
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
        if item.type_ == "Contact"
    )


class OpenHABBinarySensor(OpenHABEntity, BinarySensorEntity):
    """openhab binary_sensor class."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.item._state == "OPEN"
