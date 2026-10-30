"""
Runtime data types for flims_laax.

Access pattern: entry.runtime_data.client / entry.runtime_data.coordinator
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import FlimsLaaxApiClient
    from .coordinator import FlimsLaaxDataUpdateCoordinator


type FlimsLaaxConfigEntry = ConfigEntry[FlimsLaaxData]


@dataclass
class FlimsLaaxData:
    """Runtime data stored on the config entry after a successful setup."""

    client: FlimsLaaxApiClient
    coordinator: FlimsLaaxDataUpdateCoordinator
    integration: Integration
