"""Media Player platform for openHAB."""

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MEDIA_TYPE_MUSIC,
    SUPPORT_PLAY,
    SUPPORT_PAUSE,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_NEXT_TRACK,
    SUPPORT_VOLUME_SET,
)
from homeassistant.const import STATE_IDLE, STATE_OFF, STATE_PAUSED, STATE_PLAYING
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ITEMS_MAP, MEDIA_PLAYER
from .device_classes_map import MEDIA_PLAYER_DEVICE_CLASS_MAP
from .entity import OpenHABEntity

SUPPORT_OPENHAB = (
    SUPPORT_PLAY
    | SUPPORT_PAUSE
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_NEXT_TRACK
    | SUPPORT_VOLUME_SET
)

PLAYBACK_DICT = {
    "PLAYING": STATE_PLAYING,
    "PAUSED": STATE_PAUSED,
    "STOPPED": STATE_IDLE,
    "NULL": STATE_IDLE,
    "UNDEF": STATE_IDLE,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    for item in coordinator.data.values():
        # if item.type_ == ITEMS_MAP[MEDIA_PLAYER]:
        if item.name == "Tv_MediaPlayer":
            print(item.type_)

    async_add_entities(
        OpenHABPlayer(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ == ITEMS_MAP[MEDIA_PLAYER]
    )


class OpenHABPlayer(OpenHABEntity, MediaPlayerEntity):
    """openHAB Player class."""

    _attr_device_class_map = MEDIA_PLAYER_DEVICE_CLASS_MAP

    # def __init__(
    #     self,
    #     hass: HomeAssistant,
    #     coordinator,
    #     item,
    # ):
    #     """Initialize a openHAB media player."""
    #     super().__init__(hass, coordinator, item)
    #     self._state = STATE_OFF

    async def async_update(self) -> None:
        """Update openHAB Player entity."""
        await self.coordinator.async_request_refresh()
        # self._state = PLAYBACK_DICT[self.item._state]

    @property
    def should_poll(self) -> bool:
        return True

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.item._state:
            return STATE_OFF
        return PLAYBACK_DICT[self.item._state]

    @property
    def media_content_type(self):
        """Content type of current playing media."""
        return MEDIA_TYPE_MUSIC

    @property
    def supported_features(self):
        """Return the supported features."""
        return SUPPORT_OPENHAB

    async def async_turn_on(self) -> None:
        """Turn on."""
        await self.coordinator.async_refresh()

    async def async_turn_off(self) -> None:
        """Turn off."""
        await self.coordinator.async_refresh()

    async def async_media_play(self) -> None:
        """Play."""
        await self.hass.async_add_executor_job(self.item.play)
        await self.coordinator.async_refresh()

    async def async_media_pause(self) -> None:
        """Pause."""
        await self.hass.async_add_executor_job(self.item.pause)
        await self.coordinator.async_refresh()

    async def async_media_next_track(self) -> None:
        """Send next track command."""
        await self.hass.async_add_executor_job(self.item.next)
        await self.coordinator.async_refresh()

    async def async_media_previous_track(self) -> None:
        """Send the previous track command."""
        await self.hass.async_add_executor_job(self.item.previous)
        await self.coordinator.async_refresh()

    async def async_set_volume_level(self, volume: str) -> None:
        """Set volume level, range 0..1."""
        await self.coordinator.async_refresh()