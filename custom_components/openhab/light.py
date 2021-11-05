"""Light platform for openHAB."""
from typing import Any, cast

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    PLATFORM_SCHEMA,
    COLOR_MODE_BRIGHTNESS,
    COLOR_MODE_HS,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, ITEMS_MAP, LIGHT
from .entity import OpenHABEntity
from .utils import str_to_hsv, hsv_to_str


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
    # async_add_devices(
    #     OpenHABLightDimmer(hass, coordinator, item)
    #     for item in coordinator.data.values()
    #     if item.type_ == ITEMS_MAP[LIGHT][1]  # Dimmer
    # )


class OpenHABLightColor(OpenHABEntity, LightEntity):
    """openHAB Color Light class."""

    @property
    def is_on(self):
        """Return true if light is on."""
        return self.item._state[2] > 0

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        if not self.item:
            return
        hsv = self.item._state
        self.coordinator.api.openhab.req_post(
            f"/items/{self._id}", data=hsv_to_str([hsv[0], hsv[1], 100])
        )

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        if not self.item:
            return
        hsv = self.item._state
        self.coordinator.api.openhab.req_post(
            f"/items/{self._id}", data=hsv_to_str([hsv[0], hsv[1], 0])
        )

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
