"""OpenHABEntity class"""
from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import OpenHABDataUpdateCoordinator
from .icons_map import ICONS_MAP, ITEM_TYPE_MAP
from .utils import strip_ip


class OpenHABEntity(CoordinatorEntity):
    """Base openHAB entity."""

    coordinator: OpenHABDataUpdateCoordinator

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: OpenHABDataUpdateCoordinator,
        item: Any,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.hass = hass
        self.item = item

        if not self.coordinator.api:
            self._base_url = ""
        self._base_url = self.coordinator.api._base_url
        self._ip = strip_ip(self._base_url)

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self.item.label if len(self.item.label) > 0 else self.item.name

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        name = self.item.name
        if not name:
            return None
        return f"{DOMAIN}_{self._ip}_{name}"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._ip)},
            name=f"{NAME} - {self._ip}",
            model=VERSION,
            manufacturer=NAME,
            configuration_url=self._base_url,
            entry_type="service",
        )

    @property
    def icon(self) -> str:
        """Return the icon of the switch."""
        category = self.item.category
        item_type = self.item.type_
        if category in ICONS_MAP:
            return ICONS_MAP[category]
        if item_type in ITEM_TYPE_MAP:
            return ITEM_TYPE_MAP[item_type]
        return ""

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        name = self.item.name
        link = f"{self._base_url}/rest/items/{name}"
        return {
            "attribution": ATTRIBUTION,
            "id": f"{DOMAIN}_{name}",
            "integration": DOMAIN,
            "link": link,
            "editable": self.item.editable,
            "type": self.item.type_,
            "name": self.item.name,
            "label": self.item.label,
            "category": self.item.category,
            "tags": self.item.tags,
            "group_names": self.item.groupNames,
            "members": self.item.members,
            "ip": self._ip,
        }
