# Flims Laax

Home Assistant integration for the public Flims Laax live feed.

## Features

The integration polls `https://api.laax.com/laax-inside/live-feed` and exposes:

- Status sensors for every lift, including opening-soon and not-in-operation states
- Open, total, preparing, closed, and non-operational lift counts
- Temperature and snow-depth sensors for the locations provided by the feed
- Avalanche danger level
- Caumasee visitor count and visitor capacity
- Gate-count sensors for Flims, Laax, Falera, other entrances, and Caumasee

The feed is public and read-only. Trails are intentionally not exposed in this initial version.

## Setup

1. Install the integration through HACS or copy `custom_components/flims_laax` into Home Assistant's
   `custom_components` directory.
2. Restart Home Assistant.
3. Add **Flims Laax** from **Settings → Devices & services → Add integration**.
4. Adjust the polling interval from the integration options if needed.

The default polling interval is five minutes.
