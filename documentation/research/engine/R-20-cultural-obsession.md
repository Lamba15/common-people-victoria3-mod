# R-20 — Cultural obsession / taboo

## Question
How does the mod read whether a culture has an obsession on a specific good? Plan §4 depends on it for narrative gating around coffee, opium, fine art, etc. Plan §4.5 constraint #8 is driven by this.

## Answer

Trigger: `has_cultural_obsession = <good_key>` — culture scope.
Effects: `add_cultural_obsession = <good_key>`, `remove_cultural_obsession = <good_key>` — culture scope.
Good-level config: `obsession_chance = <scalar>` — defined per good in `common/goods/`.

Taboos are defined per **religion** (not culture), in `common/religions/`, as a list of good tags the religion forbids. There is no "has_taboo" dynamic trigger because taboos don't change mid-game — they're a static property of the religion.

## Evidence

Trigger localization (`common/trigger_localization/00_trigger_localization.txt:2963`):

```
has_cultural_obsession = {
```

Vanilla usage patterns:

- `common/journal_entries/00_opium.txt:22` — `has_cultural_obsession = opium`
- `common/journal_entries/00_prohibition_laws.txt:19` — `has_cultural_obsession = liquor`
- `events/belle_epoque_events.txt:145` — `NOT = { has_cultural_obsession = fine_art }`
- `events/law_events/state_atheism.txt:159` — `add_cultural_obsession = opium`
- `events/opium_wars_events.txt:385` — `remove_cultural_obsession = opium`
- `common/character_traits/condition_traits.txt:45–46` — `has_cultural_obsession = liquor` / `has_cultural_obsession = wine`

`obsession_chance` values (per good, in `common/goods/00_goods.txt`):

- opium — 10.0 (spikes hard when available)
- coffee / tea / tobacco / sugar / wine / liquor — 1.5–2.0
- fine art — 1.0
- most basic goods — 0.5 or 1.0

## Scope note

`has_cultural_obsession` runs on **culture** scope, not country or pop. To test whether Layla's culture has a coffee obsession:

```
cu:misri = { has_cultural_obsession = coffee }
```

Note: `cu:misri` starts with `coffee` in its `obsessions` list (see [cultures_misri](cultures_misri.md)) — so this trigger is true from 1836.1.1. Other obsessions accrue dynamically per the obsession mechanic.

## Mod usage

- `cp_sensor_her_culture_loves_coffee = { cu:misri = { has_cultural_obsession = coffee } }` — returns true at game start; used to gate pulse events about coffee culture in Egypt.
- Opium, liquor, fine art gates follow the same pattern, each reading against `cu:misri`.
- The `obsession_chance` value on a good is a passive mechanic — no scripted access needed; obsessions develop on their own per the wiki rules (50k+ pops of culture, market supply ≥50%, market demand ≥£500).
