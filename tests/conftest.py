"""Shared fixtures for the flims_laax tests."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.flims_laax.const import DOMAIN
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

# The response the public live feed returns; the client turns it into the device payload.
API_RESPONSE: dict[str, Any] = {
    "status": "success",
    "data": {
        "overview": {
            "liftsOpen": 2,
            "liftsTotal": 4,
            "liftsPreparing": 1,
            "liftsClosed": 1,
            "liftsNonOperational": 0,
        },
        "lifts": [
            {"id": "l1", "name": "Test Lift", "status": "open", "text": "", "lastRide": "17:00"},
        ],
        "weather": {
            "laax": {
                "temp": 3.5,
                "snow": {"height": 42, "new24h": 8},
                "wind": {"min": 4.2, "max": 12.5, "dir": "W"},
            },
        },
        "avalanche": {"dangerLevel": 2},
        "visitors": {"caumasee": 120, "caumaseeAllowed": 500},
        "gateCounts": {"flims": 7},
    },
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Load custom integrations in every test."""


@pytest.fixture
def mock_api() -> Generator[AsyncMock]:
    """Replace the client's HTTP layer, keeping its payload logic under test."""
    with patch(
        "custom_components.flims_laax.api.client.FlimsLaaxApiClient._api_wrapper",
        new_callable=AsyncMock,
        return_value=API_RESPONSE,
    ) as api_wrapper:
        yield api_wrapper


@pytest.fixture
def config_entry() -> MockConfigEntry:
    """Return a config entry for this integration."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="demo",
        unique_id="demo",
        data={CONF_USERNAME: "demo", CONF_PASSWORD: "secret"},
    )


@pytest.fixture
async def init_integration(
    hass: HomeAssistant,
    mock_api: AsyncMock,
    config_entry: MockConfigEntry,
) -> MockConfigEntry:
    """
    Set up the integration from a config entry.

    Returns:
        The config entry, now loaded.

    """
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return config_entry
