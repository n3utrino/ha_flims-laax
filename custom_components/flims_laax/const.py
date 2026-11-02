"""Constants for flims_laax."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "flims_laax"
ATTRIBUTION = "Data provided by LAAX"

CONF_UPDATE_INTERVAL_MINUTES = "update_interval_minutes"

DEFAULT_UPDATE_INTERVAL_MINUTES = 5
LIVE_FEED_URL = "https://api.laax.com/laax-inside/live-feed"
