# Getting Started

Flims Laax reads the public LAAX live feed and does not require an account, host, or API key.

## Installation

Install the integration through HACS, or copy `custom_components/flims_laax` into Home Assistant's

## Setup

1. Open **Settings → Devices & services**.
2. Select **Add integration**.
3. Search for **Flims Laax**.

Setup creates one Flims Laax service device. The default refresh interval is five minutes and can be changed from the
integration's options.

## Entities

The integration creates:

- One status sensor for every lift in the live feed
- Aggregate lift count sensors
- Temperature and snow-depth sensors for available locations
- Avalanche danger level
- Caumasee visitor count and capacity
- Gate-count sensors

Trails are not exposed in this initial version.

## Troubleshooting

If entities are unavailable, verify that Home Assistant can reach
`https://api.laax.com/laax-inside/live-feed` and review the Home Assistant logs. Reload the integration after restoring
network access.
