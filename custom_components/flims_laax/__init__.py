"""
Custom integration to integrate flims_laax with Home Assistant.

For more details about this integration, please refer to:
https://github.com/n3utrino/ha_flims-laax
"""

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import FlimsLaaxApiClient
from .const import CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES, DOMAIN, LOGGER
from .coordinator import FlimsLaaxDataUpdateCoordinator
from .data import FlimsLaaxData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import FlimsLaaxConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the integration domain."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
) -> bool:
    """
    Set up a config entry.

    Returns:
        True once the coordinator has data and every platform is forwarded.

    """
    client = FlimsLaaxApiClient(session=async_get_clientsession(hass))

    interval_minutes = float(entry.options.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES))
    coordinator = FlimsLaaxDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=timedelta(minutes=interval_minutes),
        always_update=False,
    )

    entry.runtime_data = FlimsLaaxData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
) -> bool:
    """
    Unload a config entry.

    Returns:
        True if every platform unloaded cleanly.

    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: FlimsLaaxConfigEntry,
) -> None:
    """Reload the config entry after its data or options changed."""
    await hass.config_entries.async_reload(entry.entry_id)
