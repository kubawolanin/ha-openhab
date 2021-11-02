"""Sensor platform for openhab."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .entity import OpenHABEntity
from .device_classes_map import SENSOR_DEVICE_CLASS_MAP


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OpenHABSensor(hass=hass, coordinator=coordinator, item=item)
        for item in coordinator.data.values()
        if item.type_ == "String" or item.type_ == "Number" or item.type_ == "DateTime"
    )


class OpenHABSensor(OpenHABEntity, SensorEntity):
    """openhab Sensor class."""

    _attr_device_class_map = SENSOR_DEVICE_CLASS_MAP

    @property
    def state(self) -> StateType:
        """Return the state of the sensor."""
        return self.item._state
