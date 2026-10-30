"""Binary sensor platform for flims_laax."""

from typing import TYPE_CHECKING

from .filter import ENTITY_DESCRIPTIONS, FlimsLaaxFilterSensor

# Read-only platform: the coordinator already serializes the fetch.
PARALLEL_UPDATES = 0

if TYPE_CHECKING:
    from custom_components.flims_laax.data import FlimsLaaxConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        FlimsLaaxFilterSensor(entry.runtime_data.coordinator, description)
        for description in ENTITY_DESCRIPTIONS
    )
