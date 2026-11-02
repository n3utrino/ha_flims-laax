"""Config flow for the public Flims Laax live feed."""

from typing import Any

from custom_components.flims_laax.const import DOMAIN
from homeassistant import config_entries

from .options_flow import FlimsLaaxOptionsFlow


class FlimsLaaxConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle setup of the public Flims Laax service."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> FlimsLaaxOptionsFlow:
        """Return the options flow."""
        return FlimsLaaxOptionsFlow()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Create the single public resort entry."""
        await self.async_set_unique_id("flims-laax")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title="Flims Laax", data={})


__all__ = ["FlimsLaaxConfigFlowHandler"]
