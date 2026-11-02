"""Resort overview sensors."""

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import SensorStateClass
from homeassistant.helpers.typing import StateType

from .entity import FlimsLaaxSensorEntityDescription


def _overview_value(key: str) -> Callable[[dict[str, Any]], StateType]:
    """Return a value from the overview section."""
    return lambda data: data.get("overview", {}).get(key)


ENTITY_DESCRIPTIONS: tuple[FlimsLaaxSensorEntityDescription, ...] = (
    FlimsLaaxSensorEntityDescription(
        key="lifts_open",
        translation_key="lifts_open",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_overview_value("liftsOpen"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="lifts_total",
        translation_key="lifts_total",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_overview_value("liftsTotal"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="lifts_preparing",
        translation_key="lifts_preparing",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_overview_value("liftsPreparing"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="lifts_closed",
        translation_key="lifts_closed",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_overview_value("liftsClosed"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="lifts_non_operational",
        translation_key="lifts_non_operational",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=_overview_value("liftsNonOperational"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="avalanche_danger",
        translation_key="avalanche_danger",
        device_group="overview",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("avalanche", {}).get("dangerLevel"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="caumasee_visitors",
        translation_key="caumasee_visitors",
        device_group="visitors",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("visitors", {}).get("caumasee"),
    ),
    FlimsLaaxSensorEntityDescription(
        key="caumasee_capacity",
        translation_key="caumasee_capacity",
        device_group="visitors",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("visitors", {}).get("caumaseeAllowed"),
    ),
)
