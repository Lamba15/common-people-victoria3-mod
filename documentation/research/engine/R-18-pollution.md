# R-18 — Pollution

## Question
What trigger reads pollution on a state? Plan §4 depends on it for `cp_sensor_her_air_is_polluted`.

## Answer

Trigger: `pollution_generation` — numeric read of the total pollution generated in a state (sum of production methods active there).
Modifiers: `state_pollution_generation_add` (adds to the generation total), `state_pollution_reduction_health_mult` (reduces the SoL/mortality impact of existing pollution).

## Evidence

Trigger localization (`common/trigger_localization/00_trigger_localization.txt:2701`):

```
pollution_generation = {
    global = TRIGGER_POLLUTION_GENERATION
    global_not = TRIGGER_POLLUTION_GENERATION_NOT
}
```

Modifier definitions (`common/modifier_type_definitions/00_modifier_types.txt:1660,1668`):

```
state_pollution_generation_add={
state_pollution_reduction_health_mult={
```

Vanilla usage in production methods — all values are per-PM integers added to the state's total:

- `common/production_methods/06_urban_center.txt:452` — `state_pollution_generation_add = 50` (heaviest urban PM)
- `common/production_methods/09_misc_resource.txt:158` — `state_pollution_generation_add = 15`
- `common/production_methods/04_plantations.txt:51` — `state_pollution_generation_add = 5`

Health reduction — laws and health techs reduce the SoL/mortality penalty per unit of generated pollution:

- `common/laws/00_health_system.txt:43` — `state_pollution_reduction_health_mult = -0.1`
- `common/laws/00_health_system.txt:110` — `state_pollution_reduction_health_mult = -0.15`

## Scale clarification

`pollution_generation` values are integers (typical range 0–200+ in heavily industrialized states). The wiki's "pollution impact %" is a derived UI concept; the script works in raw generation units.

## Mod usage

`cp_sensor_her_air_is_polluted = { s:STATE_LOWER_EGYPT = { pollution_generation >= 50 } }`
`cp_sensor_her_air_is_choking = { s:STATE_LOWER_EGYPT = { pollution_generation >= 150 } }`

Thresholds will be retuned in Phase D after observing actual values on a Lower Egypt playthrough. The comparison is against the pollution present in Layla's `var:cp_home_state`, not always Lower Egypt — migrating her to Cairo changes what she breathes.
