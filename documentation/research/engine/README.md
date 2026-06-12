# Engine research notes

Audit trail for Victoria 3 1.12 capabilities referenced by the mod plan at `/home/aboelsoud/.claude/plans/the-noughbour-s-boy-in-proud-spring.md`.

Every R-N question in plan §2c either has a file here or is consolidated below.

## Method

Primary source: installed vanilla at `/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game/`. Triggers, effects, and modifier names are taken from `common/trigger_localization/00_trigger_localization.txt` and `common/modifier_type_definitions/00_modifier_types.txt`, then cross-checked against vanilla usage in `events/` and `common/`.

## Closed research — dedicated files

- [R-17 food security](R-17-food-security.md)
- [R-18 pollution](R-18-pollution.md)
- [R-19 migration attraction](R-19-migration-attraction.md)
- [R-20 cultural obsession / taboo](R-20-cultural-obsession.md)

## Reference data

- [buy_packages](buy_packages.md) — 99 wealth tiers, one per SoL point; goods categories and weights
- [cultures_misri](cultures_misri.md) — default religion, obsessions, heritage

## Closed research — inline

The following were confirmed earlier and are documented in the plan's §2a capability matrix. No separate file needed; evidence is cited inline in the plan.

- **R-1**: `common/on_actions/00_code_on_actions.txt` — ~197 hooks; subscriptions used: `on_game_started`, `on_monthly_pulse_country`, `on_yearly_pulse_country`, `on_law_enactment_pass`, `on_diplo_play_war_start`, `on_war_end`, `on_revolution_start`, `on_acquired_technology`, `on_building_built`, `on_production_method_changed`.
- **R-5**: JE `on_monthly_pulse` fires automatically; 115 vanilla JEs prove the pattern.
- **R-11**: No `on_pop_migrated` hook. Effect `create_mass_migration` exists. Polling pattern: yearly pulse stores state_population delta in a country variable.
- **R-13**: 24 `market_goods_*` triggers (list in plan §2a).
- **R-14**: Pop consumption — 99 wealth tiers in `buy_packages/`, 14 `popneed_*` categories, culture obsessions ×2, religion taboos ×0.5. See [buy_packages](buy_packages.md).
- **R-15**: Pops carry numeric `radicalism` and `loyalism` (0–100). "A pop cannot be both a loyalist and a radical at the same time" — engine-managed mutual exclusion.
- **R-16**: Pop iterators (`any_scope_pop`, `every_scope_pop`) with `limit` blocks are how we aggregate culture/religion/pop_type subsets.

## Still open (empirical — will close in-game)

- **R-6 confirmation**: Pop-level triggers for radicalism/loyalism thresholds. Confirmed numeric; the test-event confirmation is deferred to P6/P8.
- **R-8**: Custom topbar / map tint UI modding — not a Phase A blocker.
- **R-9**: DDS format audit — deferred to Phase D asset regeneration.

## Conventions

- One file per R-N, named `R-<num>-<slug>.md`.
- Each file has: question, trigger/effect names, exact vanilla file citations, at least one verbatim usage example, and a one-paragraph conclusion on how the mod uses the capability.
