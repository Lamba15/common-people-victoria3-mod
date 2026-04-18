# R-17 — Food security

## Question
What trigger name reads food security on a state? Plan §4 depends on it for `cp_sensor_her_family_is_hungry`.

## Answer

Trigger: `food_security` — a numeric read in `[0, 1]` range (0.0 = none, 1.0 = full).
Modifier: `state_food_security_add` — used by laws, institutions, decrees, buildings.

## Evidence

Trigger localization (`common/trigger_localization/00_trigger_localization.txt:814`):

```
food_security = {
    global = TRIGGER_FOOD_SECURITY
    global_not = TRIGGER_FOOD_SECURITY_NOT
}
```

Modifier definition (`common/modifier_type_definitions/00_modifier_types.txt:1651`):

```
state_food_security_add={
```

Vanilla usage of the modifier:

- `common/laws/00_welfare.txt:142` — `state_food_security_add = 0.01`
- `common/laws/00_health_system.txt:44` — `state_food_security_add = 0.02`
- `common/decrees/00_decree.txt:154` — `state_food_security_add = 0.05` (the Emergency Relief decree)
- `common/institutions/00_institutions.txt:14` — `state_food_security_add = 0.02`

## Scale clarification

The wiki shows food security as a 0–100% concept, but the script value is 0.0–1.0. So the mild-starvation threshold (<40%) in script is `food_security < 0.4`; severe (<20%) is `food_security < 0.2`.

## Mod usage

`cp_sensor_her_family_is_hungry` reads `food_security < 0.4` in her home state. `cp_sensor_her_family_is_starving` reads `food_security < 0.2`. These are state-scope reads; usage pattern:

```
s:STATE_LOWER_EGYPT = { food_security < 0.4 }
```

Emergency Relief decree bumps `state_food_security_add` by 0.05 — narrative: if the player decreed Emergency Relief, Layla's family's sensor output changes.
