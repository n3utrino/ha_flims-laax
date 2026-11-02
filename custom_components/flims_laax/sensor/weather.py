"""Weather and gate-count sensor description builders."""

from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfLength, UnitOfSpeed, UnitOfTemperature
from homeassistant.util import slugify

from .entity import FlimsLaaxSensorEntityDescription


def build_weather_descriptions(data: dict[str, Any]) -> list[FlimsLaaxSensorEntityDescription]:
    """Build sensors for every weather location in the feed."""
    descriptions: list[FlimsLaaxSensorEntityDescription] = []
    for location, weather in data.get("weather", {}).items():
        if not isinstance(weather, dict):
            continue
        location_name = location.replace("-", " ").title()
        location_slug = slugify(location)
        descriptions.append(
            FlimsLaaxSensorEntityDescription(
                key=f"weather_{location_slug}_temperature",
                translation_key="weather_temperature",
                device_group="weather",
                device_class=SensorDeviceClass.TEMPERATURE,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=UnitOfTemperature.CELSIUS,
                value_fn=lambda payload, location=location: payload["weather"].get(location, {}).get("temp"),
                translation_placeholders={"location": location_name},
            ),
        )
        snow = weather.get("snow")
        if isinstance(snow, dict) and "height" in snow:
            descriptions.append(
                FlimsLaaxSensorEntityDescription(
                    key=f"weather_{location_slug}_snow_depth",
                    translation_key="snow_depth",
                    device_group="weather",
                    native_unit_of_measurement=UnitOfLength.CENTIMETERS,
                    state_class=SensorStateClass.MEASUREMENT,
                    value_fn=lambda payload, location=location: (
                        payload["weather"]
                        .get(location, {})
                        .get("snow", {})
                        .get(
                            "height",
                        )
                    ),
                    translation_placeholders={"location": location_name},
                ),
            )
        if isinstance(snow, dict) and "new24h" in snow:
            descriptions.append(
                FlimsLaaxSensorEntityDescription(
                    key=f"weather_{location_slug}_snow_24h",
                    translation_key="snow_24h",
                    device_group="weather",
                    native_unit_of_measurement=UnitOfLength.CENTIMETERS,
                    state_class=SensorStateClass.MEASUREMENT,
                    value_fn=lambda payload, location=location: (
                        payload["weather"].get(location, {}).get("snow", {}).get("new24h")
                    ),
                    translation_placeholders={"location": location_name},
                ),
            )
        wind = weather.get("wind")
        if isinstance(wind, dict) and "max" in wind:
            descriptions.append(
                FlimsLaaxSensorEntityDescription(
                    key=f"weather_{location_slug}_wind_speed",
                    translation_key="wind_speed",
                    device_group="weather",
                    device_class=SensorDeviceClass.WIND_SPEED,
                    native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
                    state_class=SensorStateClass.MEASUREMENT,
                    value_fn=lambda payload, location=location: (
                        payload["weather"].get(location, {}).get("wind", {}).get("max")
                    ),
                    translation_placeholders={"location": location_name},
                ),
            )
    return descriptions


def build_gate_descriptions(data: dict[str, Any]) -> list[FlimsLaaxSensorEntityDescription]:
    """Build sensors for the resort gate counters."""
    return [
        FlimsLaaxSensorEntityDescription(
            key=f"gate_count_{gate}",
            translation_key="gate_count",
            device_group="gates",
            state_class=SensorStateClass.MEASUREMENT,
            value_fn=lambda payload, gate=gate: payload["gate_counts"].get(gate),
            translation_placeholders={"gate": gate.replace("-", " ").title()},
        )
        for gate in data.get("gate_counts", {})
    ]
