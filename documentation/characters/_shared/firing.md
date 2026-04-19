# Event firing — the rate-control protocol

**How the mod decides when to show the player an event.**

## The target

**0–2 ambient events per in-game year** across all persons combined. Laws add 0–3 more when they enact. Milestones (death, Cairo offer, suitor, first envelope, revolution) add 0–1.

Quiet year: 0–4 events total. Law-heavy year: 4–8. The player reads each one.

## The four tiers

Every event belongs to exactly one firing tier.

### AMBIENT — gated by budget
Daily-life beats. Seasonal pulses. Conversation events. Small-victory. Imam's-visit. Mariam's letter. The neighbour's-boy-in-the-lane. The bread that didn't rise.

Fires from `cp_roll_for_event` (the monthly router) via `cp_try_fire_ambient`. Gated by:
- **`cp_global_ambient_cooldown`** — 180 days (no ambient fire within 6 months of another, across all persons)
- **`cp_person_<name>_ambient_cooldown`** — 365 days (each person fires at most one ambient/year)
- per-event `cp_<name>_seen_<id>` flag — 365–730 days (no repeat of the same beat)

### LAW-REACTION — bypasses budget
The event is a direct reaction to a specific law enactment. Fires from `cp_on_law_enacted` via `cp_try_fire_law_reaction`.

Bypasses the ambient cooldown because laws set their own pacing: a year with two law enactments should produce two law events.

One-shot per life via the event's own `cp_<name>_seen_<id>` flag (1825+ days).

### MILESTONE — bypasses budget
Critical beats: death, Cairo offer, suitor, first welfare envelope, revolution, first textile mill, Ahmed homecoming/death, the District Office, the Forty Days coda.

Fires from various dispatchers (yearly, war, tech, building, revolution) via `cp_try_fire_milestone`.

Bypasses budget. Dispatcher controls probability via `random_list` (e.g. 25% Cairo offer, mortality curve, etc.).

### BUTTON — bypasses budget
Player-initiated fires from the "Check on Layla" scripted button. Fires via `cp_button_fire`.

Always fires (player click is a promise). Per-event seen-flags still apply so the button can't repeat the same beat within its cooldown.

## The gatekeepers (in `cp_shared_firing.txt`)

```
cp_try_fire_ambient      # checks 180d global + 365d per-person
cp_try_fire_law_reaction # bypass, just trigger_event
cp_try_fire_milestone    # bypass, just trigger_event
cp_button_fire           # bypass, trigger_event with popup = yes
```

All take `event = <id>` and `person = <name>` parameters.

## The monthly router

`cp_roll_for_event` (in `cp_shared_firing.txt`) is called once per month from `cp_on_monthly`:

```
cp_roll_for_event = {
    random_list = {
        7 = { trigger = { has_variable = cp_layla_alive } cp_roll_ambient_layla = yes }
        # 7 per additional registered person
        93 = { }   # silent month
    }
}
```

Most months, nothing fires. When a person is picked, their own `cp_roll_ambient_<name>` effect does a weighted `random_list` over that person's ambient pool and calls `cp_try_fire_ambient` — which then checks the cooldowns.

## Shared-trigger resolution

When `law_homesteading` enacts and both Layla AND the Bey would react, a single `random_list` at the dispatcher picks one (or neither):

```
random_list = {
    60 = {   # Layla's share — higher, she's the peasant
        trigger = { has_variable = cp_layla_alive  NOT = { has_variable = cp_layla_seen_homesteading } }
        cp_try_fire_law_reaction = { event = cp_layla.2  person = layla }
    }
    30 = {   # Bey's share — lower, he loses tenants
        trigger = { has_variable = cp_bey_alive  NOT = { has_variable = cp_bey_seen_homesteading } }
        cp_try_fire_law_reaction = { event = cp_bey.2  person = bey }
    }
    10 = { }   # silent this playthrough
}
```

Weights express "whose life this beat belongs to most." Different playthroughs route the same law to different characters.

## Writing a new event

1. **Decide the tier** — ambient (everyday beat), law-reaction (responding to a specific law), milestone (critical one-shot), or button-only.
2. **Write the event** with an `immediate =` block that sets the seen-flag via `cp_mark_event_seen = { person = <name> id = <id> days = N }` where N is the cooldown length (365 / 540 / 1825 depending on how often the beat can repeat).
3. **Wire it** into the appropriate dispatcher or pool:
   - Ambient: add to `cp_roll_ambient_<name>` in that person's memory file
   - Law-reaction: add branch to `cp_on_law_enacted` with `cp_try_fire_law_reaction`
   - Milestone: add branch to `cp_on_yearly` or relevant dispatcher with `cp_try_fire_milestone`
   - Button: add to the random_list in that person's button with `cp_button_fire`
4. **Write a debug event** (`cp_debug.X`) that fires your event directly, for QA.

## Defaults summary

| Knob | Value |
|---|---|
| `cp_global_ambient_cooldown` | **180 days** |
| `cp_person_<name>_ambient_cooldown` | **365 days** |
| Monthly router nothing-branch | **93/100** |
| Per-person branch in router | **7/100** |
| Ambient seen-flag | **365–730 days** |
| Law-reaction seen-flag | **1825+ days** (effectively once per life) |
| Target ambient fires/year | **1–2** |

The button always fires regardless of budget.
