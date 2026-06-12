# Event Pacing Ledger

Generated from `script/audit-event-pacing.py`. Rebuild with:

```bash
python3 script/build-event-pacing-ledger.py
python3 script/build-event-pacing-ledger.py --check
python3 script/audit-event-pacing.py
```

## Contract

- Routine automatic Common People events should land in a reasonable range: 1-2 per in-game year across the whole roster, never 1-2 per person.
- Ordinary monthly ambient routing has a hard cap of 2 visible fires per calendar year by a 183-day global cooldown.
- The first campaign year is also capped at 2 passive fires because the startup first-contact opener marks the same global/person cooldown lane before it opens an event.
- Law reactions and routine world responses consume the same shared visible-story cooldown, so rapid reform, technology, or building sequences cannot open a Common People window for every trigger.
- War-start and revolution-start use shared resolver targets, so a single war or rupture belongs to one authored person response instead of fanning out across every eligible dispatcher.
- The router may stay silent when no eligible story exists; it should never force filler just to hit a minimum.
- Person-specific cooldowns stay at 365 days, so one person cannot dominate the ambient budget even when the global budget is open.
- Critical milestones and player-clicked QA/buttons use separate gatekeepers and are not part of the routine yearly popup budget.

## Current Static Proof

| Measure | Value |
|---|---:|
| Ambient global cooldown days | 183 |
| Ambient per-person cooldown days | 365 |
| First-contact global cooldown days | 183 |
| First-contact per-person cooldown days | 365 |
| Law-reaction global cooldown days | 183 |
| Law-reaction per-person cooldown days | 365 |
| World-response global cooldown days | 183 |
| World-response per-person cooldown days | 365 |
| Monthly router calls | 1 |
| Monthly silent branch weights | 32 |
| Ambient pool calls | 84 |
| Persons with ambient pools | 16 |
| World-response calls | 97 |
| War-start resolver targets | layla, soldier |
| Revolution resolver targets | layla, nabil |
| Startup first-contact visible branches | 16 |
| Max ambient fires/year from monthly cadence | 2 |
| Max routine automatic fires/year from shared cooldown | 2 |
| Max passive fires in first campaign year | 2 |
| Audit issues | 0 |

## Source Surfaces

- `mod/common/scripted_effects/cp_shared_firing.txt`: `cp_try_fire_ambient`, `cp_mark_first_contact_budget`, `cp_try_fire_law_reaction`, `cp_try_fire_world_response`, and `cp_roll_for_event`.
- `mod/common/scripted_effects/cp_shared_war.txt`: `cp_roll_war_start_response` chooses the single authored war-start target.
- `mod/common/scripted_effects/cp_shared_firing.txt`: `cp_roll_revolution_response` chooses the single authored revolution target.
- `mod/common/on_actions/cp_on_actions.txt`: the monthly country pulse calls the shared monthly router once, and the revolution hook calls the shared revolution resolver once.
- `mod/events/cp_shared_startup_events.txt`: every visible first-contact branch marks the shared cooldown budget before `trigger_event`.

## Raw Audit Output

```text
Common People event pacing audit
Ambient global cooldown days: 183
Ambient per-person cooldown days: 365
First-contact global cooldown days: 183
First-contact per-person cooldown days: 365
Law-reaction global cooldown days: 183
Law-reaction per-person cooldown days: 365
World-response global cooldown days: 183
World-response per-person cooldown days: 365
Monthly router calls: 1
Monthly silent branch weights: 32
Ambient pool calls: 84
Persons with ambient pools: 16
World-response calls: 97
War-start resolver targets: layla, soldier
Revolution resolver targets: layla, nabil
Startup first-contact visible branches: 16
Max ambient fires/year from monthly cadence: 2
Max routine automatic fires/year from shared cooldown: 2
Max passive fires in first campaign year: 2
Issues: 0
```
