"""Tests for the Flims Laax config flow."""

from custom_components.flims_laax.const import DOMAIN
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_creates_public_feed_entry(hass: HomeAssistant) -> None:
    """The user flow creates the public feed entry without credentials."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": SOURCE_USER})

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Flims Laax"
    assert result["data"] == {}
    assert result["result"].unique_id == "flims-laax"
