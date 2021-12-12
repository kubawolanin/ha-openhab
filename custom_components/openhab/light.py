"""Light platform for openHAB."""

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    COLOR_MODE_BRIGHTNESS,
    COLOR_MODE_HS,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ITEMS_MAP, LIGHT
from .entity import OpenHABEntity
from .utils import hsv_to_str


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_devices(
        OpenHABLightColor(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ == ITEMS_MAP[LIGHT][0]  # Color
    )
    async_add_devices(
        OpenHABLightDimmer(hass, coordinator, item)
        for item in coordinator.data.values()
        if item.type_ == ITEMS_MAP[LIGHT][1]  # Dimmer
    )


class OpenHABLightColor(OpenHABEntity, LightEntity):
    """openHAB Color Light class."""

    _attr_device_class_map = []
    _attr_color_mode = COLOR_MODE_BRIGHTNESS
    _attr_supported_color_modes = {COLOR_MODE_BRIGHTNESS, COLOR_MODE_HS}

    @property
    def is_on(self):
        """Return true if light is on."""
        return self.item._state[2] > 0

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        if not self.item:
            return
        if ATTR_HS_COLOR in kwargs:
            return print(kwargs[ATTR_HS_COLOR])
        hsv = self.item._state
        await self.hass.async_add_executor_job(
            self.coordinator.api.openhab.req_post,
            f"/items/{self._id}",
            data=hsv_to_str([hsv[0], hsv[1], 100]),
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        if not self.item:
            return
        hsv = self.item._state
        await self.hass.async_add_executor_job(
            self.coordinator.api.openhab.req_post,
            f"/items/{self._id}",
            data=hsv_to_str([hsv[0], hsv[1], 0]),
        )
        await self.coordinator.async_request_refresh()

    # @property
    # def color_mode(self) -> str | None:
    #     """Return the color mode of the light."""
    #     return COLOR_MODE_HS

    @property
    def hs_color(self) -> tuple[float, float]:
        """Return the hs color value."""
        hsv = self.item._state
        return [hsv[0], hsv[1]]


class OpenHABLightDimmer(OpenHABEntity, LightEntity):
    """openHAB Dimmer Light class."""

    _attr_device_class_map = []
    _attr_color_mode = COLOR_MODE_BRIGHTNESS
    _attr_supported_color_modes = {COLOR_MODE_BRIGHTNESS}

    @property
    def is_on(self):
        """Return true if light is on."""
        if self.item._state is None:
            return False
        return self.item._state > 0

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return int((self.item._state / 100) * 255)

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        if not self.item:
            return
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 255) * 100
            await self.hass.async_add_executor_job(
                self.coordinator.api.openhab.req_post,
                f"/items/{self._id}",
                str(brightness),
            )
            return await self.coordinator.async_request_refresh()
        await self.hass.async_add_executor_job(
            self.coordinator.api.openhab.req_post, f"/items/{self._id}", "ON"
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        if not self.item:
            return
        await self.hass.async_add_executor_job(
            self.coordinator.api.openhab.req_post, f"/items/{self._id}", "OFF"
        )
        await self.coordinator.async_request_refresh()
