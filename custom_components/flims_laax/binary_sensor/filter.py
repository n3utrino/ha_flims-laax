"""Filter maintenance binary sensor for flims_laax."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from custom_components.flims_laax.entity import FlimsLaaxEntity
from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.components.binary_sensor.const import BinarySensorDeviceClass


@dataclass(frozen=True, kw_only=True)
class FlimsLaaxBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a binary sensor and how to read it from coordinator data."""

    value_fn: Callable[[dict[str, Any]], bool | None]


ENTITY_DESCRIPTIONS: tuple[FlimsLaaxBinarySensorEntityDescription, ...] = (
    FlimsLaaxBinarySensorEntityDescription(
        key="filter_replacement",
        translation_key="filter_replacement",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda data: data.get("filter_replacement"),
    ),
)


class FlimsLaaxFilterSensor(BinarySensorEntity, FlimsLaaxEntity):
    """Binary sensor reporting whether the filter needs replacing."""

    entity_description: FlimsLaaxBinarySensorEntityDescription

    @property
    def is_on(self) -> bool | None:
        """Return the value read from coordinator data."""
        return self.entity_description.value_fn(self.coordinator.data)
