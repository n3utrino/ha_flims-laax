"""Sensor entities for the Flims Laax live feed."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.flims_laax.coordinator import FlimsLaaxDataUpdateCoordinator
from custom_components.flims_laax.entity import FlimsLaaxEntity
from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class FlimsLaaxSensorEntityDescription(SensorEntityDescription):
    """Describe a live-feed sensor and its value lookup."""

    device_group: str
    value_fn: Callable[[dict[str, Any]], StateType]
    attributes_fn: Callable[[dict[str, Any]], dict[str, Any]] | None = None
    translation_placeholders: dict[str, str] | None = None


class FlimsLaaxSensor(SensorEntity, FlimsLaaxEntity):
    """Sensor backed by the coordinator's live-feed payload."""

    entity_description: FlimsLaaxSensorEntityDescription

    def __init__(
        self,
        coordinator: FlimsLaaxDataUpdateCoordinator,
        entity_description: FlimsLaaxSensorEntityDescription,
    ) -> None:
        """Initialize a live-feed sensor."""
        super().__init__(coordinator, entity_description)
        if entity_description.translation_placeholders:
            self._attr_translation_placeholders = entity_description.translation_placeholders

    @property
    def native_value(self) -> StateType:
        """Return the current value."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return optional details supplied by the feed."""
        if self.entity_description.attributes_fn is None:
            return None
        return self.entity_description.attributes_fn(self.coordinator.data)
