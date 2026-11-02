# Examples

Entity IDs are based on the lift or location names. Confirm the exact IDs in **Settings → Devices & services**.

## Notify when a lift opens

```yaml
alias: Notify when Caumasee lift opens
triggers:
  - trigger: state
    entity_id: sensor.flims_laax_caumasee_status
    to: open
actions:
  - action: notify.notify
    data:
      message: Caumasee lift is open.
```

## Show resort status

```yaml
type: entities
title: Flims Laax
entities:
  - sensor.flims_laax_lifts_open
  - sensor.flims_laax_lifts_total
  - sensor.flims_laax_avalanche_danger_level
  - sensor.flims_laax_caumasee_visitors
  - sensor.flims_laax_caumasee_capacity
```

## Show mountain weather

```yaml
type: entities
title: Mountain weather
entities:
  - sensor.flims_laax_vorab_gletscher_temperature
  - sensor.flims_laax_vorab_gletscher_snow_depth
  - sensor.flims_laax_crap_sogn_gion_temperature
  - sensor.flims_laax_crap_sogn_gion_snow_depth
```
