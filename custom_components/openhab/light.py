"""Light platform for openhab."""
from typing import Any, cast

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.color import (
    color_temperature_kelvin_to_mired as kelvin_to_mired,
    color_temperature_mired_to_kelvin as mired_to_kelvin,
)

from .const import DOMAIN, ITEMS_MAP, LIGHT
from .device_classes_map import COVER_DEVICE_CLASS_MAP
from .entity import OpenHABEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        OpenHABLight(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ in ITEMS_MAP[LIGHT]
    )


class OpenHABLight(OpenHABEntity, LightEntity):
    """openhab Light class."""
