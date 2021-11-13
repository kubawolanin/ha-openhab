"""Light platform for openHAB."""

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ITEMS_MAP, MEDIA_PLAYER
from .device_classes_map import MEDIA_PLAYER_DEVICE_CLASS_MAP
from .entity import OpenHABEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        OpenHABPlayer(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ == ITEMS_MAP[MEDIA_PLAYER]
    )


class OpenHABPlayer(OpenHABEntity, MediaPlayerEntity):
    """openHAB Player class."""

    _attr_device_class_map = MEDIA_PLAYER_DEVICE_CLASS_MAP
