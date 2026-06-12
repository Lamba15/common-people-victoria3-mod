# Event firing — the rate-control protocol

**How the mod decides when to show the player an event.**

## The target

**1-2 routine visible Common People beats per in-game year as the target, with a hard cap of 2** across all persons combined, not per character.

In the first campaign year, the one-time first-contact opener counts against that same quiet lane: opener plus at most one later passive ambient, law, or world-response beat. In later years, the monthly ambient router can produce at most two passive beats, and law/technology/building/conditional-entry reactions consume that same lane. If no eligible story exists, the router may stay silent; it must not force filler just to hit a minimum. Player-click buttons, debug QA, and genuinely critical life events are separate because the player or game state caused them directly.

Law reactions and routine world responses now consume the same shared visible-story cooldown as ambient/startup beats, so reform-heavy or modernization-heavy years do not flood the player. Milestones should still stay rare, one-shot, and tied to a critical life event. Do not use them to sneak in ordinary ambient or modernization material.

Wars and revolutions use one shared target resolver before person dispatchers run. A single war-start may be Layla's Ahmed-conscripted beat, Yusuf's notice beat, or silent; a single revolution may be Layla's fear beat, Nabil's public-order aftermath, or silent. Neither hook should fan out into every eligible person's dispatcher.

## The five tiers

Every event belongs to exactly one firing tier.

### AMBIENT — gated by budget
Daily-life beats. Seasonal pulses. Conversation events. Small-victory. Imam's-visit. Mariam's letter. The neighbour's-boy-in-the-lane. The bread that didn't rise.

Fires from `cp_roll_for_event` (the monthly router) via `cp_try_fire_ambient`. Gated by:
- **`cp_global_ambient_cooldown`** — 183 days (no routine automatic popup more than twice per year, across all persons)
- **`cp_person_<name>_ambient_cooldown`** — 365 days (each person fires at most one ambient/year)
- per-event `cp_<name>_seen_<id>` flag — 365–730 days (no repeat of the same beat)

### FIRST CONTACT — one opener, budget-aware
Game start uses `cp_shared_startup.2` to pick one visible first-contact opener from the eligible roster, or to stay silent. Every visible first-contact branch calls `cp_mark_first_contact_budget` before it fires, which starts the same 183-day global cooldown and a 365-day per-person cooldown. That keeps the first year from becoming "intro now, ambient one month later."

### LAW-REACTION — budget-aware
The event is a direct reaction to a specific law enactment. Fires from `cp_on_law_enacted` via `cp_try_fire_law_reaction`.

Consumes the same `cp_global_ambient_cooldown` and `cp_person_<name>_ambient_cooldown` lane as ambient/startup. A law still gets a chance to produce one human-scale reaction, but a rapid reform sequence will not open a Common People window for every law.

One-shot per life via the event's own `cp_<name>_seen_<id>` flag (1825+ days).

### WORLD-RESPONSE — budget-aware
Routine reactions to technology, new buildings, conditional person entry, and noncritical yearly state changes. This is where "the country modernizes and a factory worker, railway porter, clerk, or dockworker becomes visible" belongs.

Fires from person-owned yearly, technology, building, revolution, or hidden setup dispatchers via `cp_try_fire_world_response`.

Consumes the same shared cooldown lane as ambient/startup/law reactions. If the budget is closed, the person remains registered and can surface later through monthly ambient routing.

### MILESTONE — bypasses budget
Critical beats: first childbirth, death, Cairo offer, suitor, first welfare envelope, Ahmed homecoming/death, the District Office, the Forty Days coda.

Fires from various dispatchers (yearly, war, revolution, mortality, family, crossroads) via `cp_try_fire_milestone`.

Bypasses budget. Dispatcher controls probability via `random_list` (e.g. 25% Cairo offer, mortality curve, etc.).

### BUTTON — bypasses budget
Player-initiated fires from scripted buttons, currently the shared QA button and any future roster-level player action. Fires via `cp_button_fire`.

Always fires (player click is a promise). Per-event seen-flags still apply so the button can't repeat the same beat within its cooldown.

## The gatekeepers and budget helper (in `cp_shared_firing.txt`)

```
cp_try_fire_ambient      # checks 183d global + 365d per-person
cp_mark_first_contact_budget # startup opener marks the same cooldown lane
cp_try_fire_law_reaction # checks/marks the same cooldown lane
cp_try_fire_world_response # checks/marks the same cooldown lane
cp_roll_war_start_response # chooses one authored war-start target
cp_roll_revolution_response # chooses one authored revolution target
cp_try_fire_milestone    # bypass, just trigger_event
cp_button_fire           # bypass, trigger_event with popup = yes
```

The firing gatekeepers take `event = <id>` and `person = <name>` parameters. `cp_mark_first_contact_budget` takes only `person = <name>` and is followed by the startup first-contact `trigger_event`.

The static audit permits raw `trigger_event` in `mod/common` only when the target event is hidden setup plumbing. Visible events fired from common script must use one of the gatekeepers above; event-local chained follow-ups inside an event's own `immediate` or `option` block remain allowed.

## The monthly router

`cp_roll_for_event` (in `cp_shared_firing.txt`) is called once per month from `cp_on_monthly`:

```
cp_roll_for_event = {
    random_list = {
        9 = {
            trigger = {
                cp_person_is_alive = { person = layla }
                cp_era_before_1850 = yes
            }
            cp_roll_ambient_layla = yes
        }
        10 = {
            trigger = {
                cp_person_is_alive = { person = samier }
                cp_person_home_has_manufacturing = { person = samier }
                cp_country_workers_unprotected = yes
            }
            cp_roll_ambient_samier = yes
        }
        # One active branch per person, with weight chosen by date/game state.
        32 = { }   # silent branch
    }
}
```

Most months, nothing fires. When a person is picked, their own `cp_roll_ambient_<name>` effect does a weighted `random_list` over that person's ambient pool and calls `cp_try_fire_ambient` — which then checks the cooldowns.
The person branch is no longer a flat `7` forever. Each registered person has mutually exclusive branches in the shared router: date (`game_date` era), laws, local home-state buildings, war state, education, property rights, and health laws decide whose life is most likely to surface in the current playthrough. For physical workplace/building beats, use the `cp_person_home_has_*` sensors so a factory in Lower Egypt reaches only people whose residence marker is in Lower Egypt. Country-wide `cp_country_has_*` sensors are still valid for conditional entry and national technologies/laws. The silent branch remains positive so the ambient budget stays quiet.

`python3 script/audit-event-pacing.py` proves the pacing contract statically: the monthly router is only called from `cp_on_monthly`, the shared global cooldown is at least 183 days, the per-person cooldown is at least 365 days, first-contact/law-reaction/world-response gatekeepers mark the cooldown lane, all ambient calls live inside person-owned `cp_roll_ambient_<name>` pools, technology/building reactions cannot use `cp_try_fire_milestone`, hidden setup first appearances cannot raw-trigger visible intros, and routine automatic fires cannot exceed two/year. `python3 script/build-event-pacing-ledger.py --check` keeps the generated proof in `documentation/event-pacing-ledger.md` current.
`script/audit-event-repeatability.py` checks that visible event windows are not loose repeaters: each must be covered by a self/upstream latch, a cooldown, a visible parent chain, a terminal state change, startup-only routing, or an explicit intentional-repeat entry.
`python3 script/build-event-firing-ledger.py --check` verifies that every visible non-debug event has at least one production route. The generated proof in `documentation/event-firing-ledger.md` separates startup first contact, ambient budget, law reaction, world response, milestone, button, hidden person router, setup first appearance, and visible-chain paths; debug wrappers do not count as proof.

## Shared-trigger resolution

When `law_homesteading` enacts and both Layla AND the Bey would react, a single `random_list` at the dispatcher picks one (or neither):

```
random_list = {
    60 = {   # Layla's share — higher, she's the peasant
        trigger = {
            cp_person_is_alive = { person = layla }
            NOT = { has_variable = cp_layla_seen_homesteading }
        }
        cp_try_fire_law_reaction = { event = cp_layla.2  person = layla }
    }
    30 = {   # Bey's share — lower, he loses tenants
        trigger = {
            cp_person_is_alive = { person = bey }
            NOT = { has_variable = cp_bey_seen_homesteading }
        }
        cp_try_fire_law_reaction = { event = cp_bey.2  person = bey }
    }
    10 = { }   # silent this playthrough
}
```

Weights express "whose life this beat belongs to most." Different playthroughs route the same law to different characters.

War and revolution hooks use the same ownership idea. `cp_on_war_started_for_egy` calls `cp_roll_war_start_response` once, and `cp_on_revolution` calls `cp_roll_revolution_response` once. Each resolver sets one short-lived `cp_shared_<hook>_target_<person>` flag. Person dispatchers still own their event logic, but only the chosen target can fire from that country rupture. When adding another authored war or revolution reaction, add a branch to the relevant resolver and make the person's dispatcher consume only its target flag.

## Writing a new event

1. **Decide the tier** — ambient (everyday beat), law-reaction (responding to a specific law), world-response (technology/building/conditional entry/noncritical yearly state), milestone (critical one-shot), or button-only.
2. **Write the event** with an `immediate =` block that sets the seen-flag via `cp_mark_event_seen = { person = <name> id = <id> days = N }` where N is the cooldown length (365 / 540 / 1825 depending on how often the beat can repeat).
3. **Wire it** into the appropriate dispatcher or pool:
   - Ambient: add to `cp_roll_ambient_<name>` in that person's memory file
   - Law-reaction: add branch to `cp_<name>_dispatch_law_enacted` with `cp_try_fire_law_reaction`; use `cp_on_law_enacted` direct fires only for multi-person shared contests
   - World-response: add branch to `cp_<name>_dispatch_tech`, `cp_<name>_dispatch_building`, the hidden setup event, or a noncritical yearly dispatcher with `cp_try_fire_world_response`
   - Milestone: add branch to `cp_<name>_dispatch_yearly` or relevant dispatcher with `cp_try_fire_milestone`
   - Button: add to the random_list in that person's button with `cp_button_fire`
4. **Regenerate debug QA selectors**. Visible popups are queued by generated debug events, then opened from the JE **Open queued QA event** button so they run in game-thread context. Run `python3 script/generate-person-debug-wrappers.py` after changing any registered person's visible events, then verify with `python3 script/generate-person-debug-wrappers.py --check` and `script/audit-person-roster.py`.
5. **Refresh the firing ledger**. Run `python3 script/build-event-firing-ledger.py` after adding or rerouting visible events, then verify with `python3 script/build-event-firing-ledger.py --check`. A new event is not production-reachable until it appears in the ledger with a non-debug route.
6. **Check pacing**. Run `python3 script/audit-event-pacing.py` and `python3 script/build-event-pacing-ledger.py --check`. The answer must remain "max ambient fires/year = 2", "max routine automatic fires/year = 2", and "max passive fires in first campaign year = 2."

## Defaults summary

| Knob | Value |
|---|---|
| `cp_global_ambient_cooldown` | **183 days** |
| `cp_person_<name>_ambient_cooldown` | **365 days** |
| First-contact opener | **marks the 183d global + 365d person cooldown lane** |
| Monthly router nothing-branch | **positive silent branch**; **32 static weight today** |
| Per-person branch in router | **context-weighted** by date, law, industry, war, education, property, and health sensors |
| Ambient seen-flag | **365–730 days** |
| Law-reaction seen-flag | **1825+ days** (effectively once per life) |
| World-response seen-flag | **540–1825+ days** depending on repeatability |
| Target routine automatic fires/year | **1–2** |

The button always fires regardless of budget.
