"""Button platform for flims_laax."""

from typing import TYPE_CHECKING

from .reset_filter import ENTITY_DESCRIPTIONS, FlimsLaaxButton

# Acts on the device: the coordinator does not limit outbound calls.
PARALLEL_UPDATES = 1

if TYPE_CHECKING:
    from custom_components.flims_laax.data import FlimsLaaxConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the button platform."""
    async_add_entities(
        FlimsLaaxButton(entry.runtime_data.coordinator, description) for description in ENTITY_DESCRIPTIONS
    )
