"""Tests for the Flims Laax live-feed sensors."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.flims_laax.api import FlimsLaaxApiClientError
from custom_components.flims_laax.const import DOMAIN
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant, State
from homeassistant.helpers import entity_registry as er


def _sensor_state(hass: HomeAssistant, unique_id: str) -> State:
    """Return a sensor state using its integration-stable unique ID."""
    entity_id = er.async_get(hass).async_get_entity_id("sensor", DOMAIN, unique_id)
    assert entity_id is not None
    state = hass.states.get(entity_id)
    assert state is not None
    return state


async def test_entities_read_the_coordinator_payload(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
) -> None:
    """Every sensor takes its state from the live-feed payload."""
    prefix = f"{init_integration.entry_id}_flims-laax_"
    assert _sensor_state(hass, f"{prefix}lifts_open").state == "2"
    assert _sensor_state(hass, f"{prefix}weather_laax_temperature").state == "3.5"
    assert _sensor_state(hass, f"{prefix}weather_laax_snow_depth").state == "42"
    assert _sensor_state(hass, f"{prefix}weather_laax_snow_24h").state == "8"
    assert _sensor_state(hass, f"{prefix}weather_laax_wind_speed").state == "12.5"
    assert _sensor_state(hass, f"{prefix}gate_count_flims").state == "7"


async def test_entities_go_unavailable_when_the_poll_fails(
    init_integration: MockConfigEntry,
    hass: HomeAssistant,
    mock_api: AsyncMock,
) -> None:
    """A failed refresh makes the entities unavailable rather than stale."""
    mock_api.side_effect = FlimsLaaxApiClientError("boom")

    await init_integration.runtime_data.coordinator.async_refresh()
    await hass.async_block_till_done()

    assert _sensor_state(hass, f"{init_integration.entry_id}_flims-laax_lifts_open").state == STATE_UNAVAILABLE
