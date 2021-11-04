"""OpenHABEntity class"""
from __future__ import annotations

from typing import Any, List

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from openhab import items

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import OpenHABDataUpdateCoordinator
from .icons_map import ICONS_MAP, ITEM_TYPE_MAP
from .utils import strip_ip


class OpenHABEntity(CoordinatorEntity):
    """Base openHAB entity."""

    coordinator: OpenHABDataUpdateCoordinator
    _attr_device_class_map: List | None

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: OpenHABDataUpdateCoordinator,
        item: items.Item,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.hass = hass
        self.item = item
        self._id = item.name

        if not self.coordinator.api:
            self._base_url = ""
        self._base_url = self.coordinator.api._base_url
        self._host = strip_ip(self._base_url)

        self.entity_id = f"{DOMAIN}_{self._host}_{self.item.name}"

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.is_online

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self.item.label if len(self.item.label) > 0 else self.item.name

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        return f"{DOMAIN}_{self._host}_{self.item.name}"

    @property
    def device_info(self) -> DeviceInfo:
        version = VERSION
        oh_version = self.coordinator.version
        if oh_version is not None:
            version = oh_version
        return DeviceInfo(
            identifiers={(DOMAIN, self._host)},
            name=f"{NAME} - {self._host}",
            model=version,
            manufacturer=NAME,
            configuration_url=self._base_url,
            entry_type="service",
        )

    @property
    def device_class(self):
        """Return the device class"""
        name = self.item.name.lower()
        label = self.item.label.lower()
        device_classes = self._attr_device_class_map

        if device_classes is not None:
            for device_class in device_classes:
                if device_class in name or device_class in label:
                    return device_class

        return ""

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
        label = self.item.label
        link = f"{self._base_url}/rest/items/{name}"
        is_group = bool(self.item.group)
        attributes = {
            "attribution": ATTRIBUTION,
            "category": self.item.category,
            "editable": self.item.editable,
            "group_names": self.item.groupNames,
            "hostname": self._host,
            "id": f"{DOMAIN}_{name}",
            "integration": DOMAIN,
            "is_group": self.item.group,
            "label": label,
            "link": link,
            "name": self.item.name,
            "tags": self.item.tags,
            "type": self.item.type_,
            "raw_state": self.item._raw_state,
        }

        if is_group and len(self.item.members):
            attributes["members"] = self.item.members.keys()

        if self.item.quantityType is not None:
            attributes["quantity_type"] = self.item.quantityType

        return attributes

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.item = self.coordinator.data.get(self._id)
        self.async_write_ha_state()
