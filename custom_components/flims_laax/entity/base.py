"""Base entity class for flims_laax."""

from typing import TYPE_CHECKING

from custom_components.flims_laax.const import ATTRIBUTION
from custom_components.flims_laax.coordinator import FlimsLaaxDataUpdateCoordinator
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class FlimsLaaxEntity(CoordinatorEntity[FlimsLaaxDataUpdateCoordinator]):
    """
    Base entity providing device info, unique ID and attribution.

    The stable resort identifier is used as the service device identifier.
    """

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: FlimsLaaxDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_flims-laax_{entity_description.key}"
        device_group = getattr(entity_description, "device_group", "overview")
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.domain, f"{coordinator.config_entry.entry_id}_{device_group}")},
            name=f"{coordinator.config_entry.title} {device_group.title()}",
            manufacturer="LAAX",
            model=coordinator.data["model"],
            serial_number=coordinator.data["serial_number"],
            sw_version=coordinator.data["sw_version"],
            entry_type=DeviceEntryType.SERVICE,
        )
