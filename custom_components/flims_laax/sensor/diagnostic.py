"""Diagnostic sensor descriptions for flims_laax."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfTime

from .entity import FlimsLaaxSensorEntityDescription

ENTITY_DESCRIPTIONS: tuple[FlimsLaaxSensorEntityDescription, ...] = (
    FlimsLaaxSensorEntityDescription(
        key="filter_life",
        translation_key="filter_life",
        entity_category=EntityCategory.DIAGNOSTIC,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda data: data.get("filter_life"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="runtime",
        translation_key="runtime",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=0,
        value_fn=lambda data: data.get("runtime"),
    ),
)
