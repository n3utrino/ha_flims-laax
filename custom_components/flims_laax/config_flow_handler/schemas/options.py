"""Options flow schemas."""

from collections.abc import Mapping
from typing import Any

import probatio

from custom_components.flims_laax.const import CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES
from homeassistant.helpers import selector


def get_options_schema(defaults: Mapping[str, Any] | None = None) -> probatio.Schema:
    """
    Build the options form schema.

    Args:
        defaults: The entry's current options, used to pre-fill the form.

    Returns:
        The voluptuous schema for the options form.

    """
    defaults = defaults or {}
    return probatio.Schema(
        {
            probatio.Optional(
                CONF_UPDATE_INTERVAL_MINUTES,
                default=defaults.get(CONF_UPDATE_INTERVAL_MINUTES, DEFAULT_UPDATE_INTERVAL_MINUTES),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1,
                    max=60,
                    step=1,
                    unit_of_measurement="min",
                    mode=selector.NumberSelectorMode.BOX,
                ),
            ),
        },
    )


__all__ = ["get_options_schema"]
