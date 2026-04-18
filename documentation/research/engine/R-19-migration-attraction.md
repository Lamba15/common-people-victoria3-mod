# R-19 — Migration attraction

## Question
Is there a script-readable value for migration attraction per state/country? Plan §4 depends on it for `cp_sensor_migration_to_city_plausible`.

## Answer

State scope — full comparison family:
- `state_migration_pull_greater_than`
- `state_migration_pull_less_than`
- `state_migration_pull_greater_or_equal`
- `state_migration_pull_less_or_equal`
- `state_migration_pull_equal`
- `state_migration_pull_not_equal`

Country scope — parallel family: `country_migration_pull_greater_than` etc.

Modifiers: `state_migration_pull_mult`, `country_mass_migration_attraction_mult`.

## Evidence

Trigger localization (`common/trigger_localization/00_trigger_localization.txt:1112–1165`):

```
state_migration_pull_greater_than = {
    global = TRIGGER_STATE_MIGRATION_PULL_GREATER_THAN
    third = TRIGGER_STATE_MIGRATION_PULL_GREATER_THAN_THIRD
}
...
country_migration_pull_greater_than = {
    global = TRIGGER_COUNTRY_MIGRATION_PULL_GREATER_THAN
    first = TRIGGER_COUNTRY_MIGRATION_PULL_GREATER_THAN_FIRST
    third = TRIGGER_COUNTRY_MIGRATION_PULL_GREATER_THAN_THIRD
}
```

Modifier usage:

- `common/country_ranks/00_country_ranks.txt:44` — `state_migration_pull_mult = 0.25` (applied per rank tier)
- `common/static_modifiers/content_304_modifiers.txt:512` — `country_mass_migration_attraction_mult = 0.5`

## Syntax pattern

These are third-value comparisons (they take a target scope and a value). Usage:

```
s:STATE_CAIRO = {
    state_migration_pull_greater_than = s:STATE_LOWER_EGYPT
}
```

For a numeric read against a constant, use the modifier family (`state_migration_pull_mult`) on an artificial modifier and read back, or use the iterator pattern to compute deltas.

## Mod usage

`cp_sensor_migration_to_city_plausible` compares Cairo's pull to Lower Egypt's pull:

```
cp_sensor_migration_to_city_plausible = {
    c:EGY = { NOT = { has_law = law_type:law_serfdom } }
    s:STATE_CAIRO = {
        state_migration_pull_greater_than = s:STATE_LOWER_EGYPT
    }
}
```

This is still a boolean. For the crossroads "Cairo offers work" event, the value of the gradient is approximated via the state_population YoY delta polled in `cp_on_yearly` (plan §2b, R-11). Direct numeric read of the pull isn't needed for narrative gating.
