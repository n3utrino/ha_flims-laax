"""Sensor platform for Flims Laax."""

from typing import Any

from custom_components.flims_laax.data import FlimsLaaxConfigEntry
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import FlimsLaaxSensor, FlimsLaaxSensorEntityDescription
from .overview import ENTITY_DESCRIPTIONS as OVERVIEW_DESCRIPTIONS
from .weather import build_gate_descriptions, build_weather_descriptions

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up aggregate, weather, gate, and lift sensors."""
    data: dict[str, Any] = entry.runtime_data.coordinator.data
    descriptions = [*OVERVIEW_DESCRIPTIONS, *build_weather_descriptions(data), *build_gate_descriptions(data)]

    for lift in data.get("lifts", []):
        if not isinstance(lift, dict) or not lift.get("id"):
            continue
        lift_id = str(lift["id"])
        lift_name = str(lift.get("name") or lift.get("id")).replace("-", " ").title()
        descriptions.append(
            FlimsLaaxSensorEntityDescription(
                key=f"lift_{lift_id}",
                translation_key="lift_status",
                device_group="lifts",
                device_class=SensorDeviceClass.ENUM,
                options=["open", "soon", "closed", "not-in-operation"],
                value_fn=lambda payload, lift_id=lift_id: next(
                    (item.get("status") for item in payload.get("lifts", []) if str(item.get("id")) == lift_id),
                    None,
                ),
                attributes_fn=lambda payload, lift_id=lift_id: next(
                    (
                        {
                            "lift_id": item.get("id"),
                            "information": item.get("text"),
                            "last_ride": item.get("lastRide"),
                        }
                        for item in payload.get("lifts", [])
                        if str(item.get("id")) == lift_id
                    ),
                    {},
                ),
                translation_placeholders={"lift": lift_name},
            ),
        )

    async_add_entities(FlimsLaaxSensor(entry.runtime_data.coordinator, description) for description in descriptions)
