"""Tests for Home Assistant 2026.8 config-entry-scoped device ownership."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.flims_laax.const import DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr


async def test_entry_owns_its_own_device(init_integration: MockConfigEntry, hass: HomeAssistant) -> None:
    """A loaded entry registers one device for each sensor group."""
    assert init_integration.state is ConfigEntryState.LOADED

    devices = dr.async_entries_for_config_entry(dr.async_get(hass), init_integration.entry_id)

    assert len(devices) == 5
    assert {device.config_entry_id for device in devices} == {init_integration.entry_id}
    assert {device.name for device in devices} == {
        "demo Overview",
        "demo Weather",
        "demo Lifts",
        "demo Visitors",
        "demo Gates",
    }


async def test_two_entries_get_separate_devices(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    init_integration: MockConfigEntry,
) -> None:
    """Two entries never share a device, and entry-scoped lookups keep them apart."""
    second_entry = MockConfigEntry(
        domain=DOMAIN,
        title="second",
        unique_id="second",
        data={CONF_USERNAME: "second", CONF_PASSWORD: "secret"},
    )
    second_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(second_entry.entry_id)
    await hass.async_block_till_done()

    device_registry = dr.async_get(hass)
    first_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{init_integration.entry_id}_overview"),
        init_integration.entry_id,
    )
    second_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{second_entry.entry_id}_overview"),
        second_entry.entry_id,
    )

    assert first_device is not None
    assert second_device is not None
    assert first_device.id != second_device.id
