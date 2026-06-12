# Adding a new person — the manual

**The mechanical recipe for landing Person 2, 3, 4, N.** Everything here is copy-paste plus substitution. If you find yourself editing an existing Layla file, you're doing it wrong — adding a person is purely additive.

This is the most important document in the mod. If it ever drifts out of date, fix it first.

Read `registry.md` and `firing.md` alongside this file. They explain the *why*. This file is the *how*.

---

## Pre-flight — pick the person

Decide before you start:

| Field | Example | Notes |
|---|---|---|
| **name token** | `bey` | lowercase, snake-case, unique, short. Becomes the `$person$` macro parameter everywhere. Never changes. |
| **country** | `EGY` | the 3-letter V3 tag where their life plays out. They don't follow the player's game; they follow *this* country. |
| **culture** | `misri` | literal V3 culture id. Not a variable. |
| **religion** | `sunni` | literal V3 religion id. |
| **home state** | `STATE_LOWER_EGYPT` | literal V3 state. Used for the pop-cohort SoL read. |
| **starting profession** | `peasants` | literal V3 pop_type. The profession for the SoL cohort read; can change over their life. |
| **starting age** | `42` | integer. Ages one tick per in-game year via `cp_on_yearly`. |

Also decide whether they share a country with another person (the Bey and Layla both on EGY — so shared-trigger resolution applies for laws affecting both) or live alone (a Russian serf on RUS — no shared triggers ever).

---

## The file manifest — what you create

Three required new files, all prefixed `cp_<name>_*`. Add optional files only when the person actually needs sensors or a full conversation tree. The persistent journal entry is shared by the roster, not copied per person.

```
mod/events/
  cp_<name>_events.txt                     # their life events

mod/common/scripted_effects/
  cp_<name>_memory.txt                     # their dispatchers + ambient pool + refresh wrapper

mod/localization/english/
  cp_<name>_l_english.yml                  # all their strings
```

Optional files (skip unless the person genuinely needs the surface):

```
mod/events/
  cp_<name>_vox_events.txt                 # their conversation tree

mod/common/scripted_triggers/
  cp_<name>_sensors.txt                    # their compound sensors

mod/common/customizable_localization/
  cp_<name>_custom_loc.txt                 # person-specific loc helpers, if needed outside the shared JE
```

Images go under `mod/gfx/event_pictures/cp_<name>_*.dds`.

The roster audit treats both `cp_<name>.*` and `cp_<name>_*.*` event namespaces as owned by the person. Optional conversation trees like `cp_<name>_vox.*` still count toward the person's visible-event, image, localization, and debugability surface; the global audio audit covers them too.

After the first pass compiles, the generated person contract ledger becomes the
mechanical source of truth for parity with the rest of the roster:

```bash
python3 script/build-person-contract-ledger.py
python3 script/build-person-contract-ledger.py --check
python3 script/build-person-hook-ledger.py
python3 script/build-person-hook-ledger.py --check
python3 script/audit-event-pacing.py
python3 script/build-event-firing-ledger.py
python3 script/build-event-firing-ledger.py --check
python3 script/build-world-response-ledger.py
python3 script/build-world-response-ledger.py --check
```

That check fails if the new person lacks baseline setup variables, a profession
flag, a home-state marker, any of the nine dispatcher hooks, yearly age/SoL
maintenance, ambient router coverage, visible-event audio/art, generated debug
coverage, or chance-based visible/silent setup when they are conditional.
The hook ledger fails if a dispatcher hook direct-fires a visible event instead
of using a shared gatekeeper, and it keeps each person's active/no-op hook
surface visible so scaffolds cannot quietly drift into Layla-only infrastructure.
The firing ledger fails separately if any new visible event is reachable only
from debug wrappers or is not reachable from production script at all.
The world-response ledger fails if a visible event has no classified production
source through startup, monthly, law, technology, building, war, revolution,
yearly/date, button, or visible-chain routing.
The pacing audit fails if the new person can push routine automatic Common
People events above 1-2 per year across the whole roster, if first-contact or
law-reaction/world-response routing stops marking the shared cooldown lane, if
technology/building reactions use milestone routing, if conditional first
appearances raw-trigger their visible intro, or if ambient fires bypass the
person-owned `cp_roll_ambient_<name>` pool.

---

## The seven-step recipe

### Step 1 — Create the person's memory file

`mod/common/scripted_effects/cp_<name>_memory.txt`. This one file holds:
- their refresh-SoL wrapper (bakes culture + religion + profession into literals),
- their dispatcher branches (one per on-action hook),
- their ambient-event pool.

**Template** (substitute `<name>`, `<culture>`, `<religion>`, `<poptype>`):

```
###############################################################################
# Common People -- <name>'s memory
###############################################################################


# --- Refresh SoL from pop cohort -------------------------------------------
cp_<name>_refresh_sol = {
    cp_refresh_sol_from_pop = {
        person   = <name>
        culture  = <culture>
        religion = <religion>
        poptype  = <poptype>
    }
}


# --- Dispatcher branches ----------------------------------------------------
# One per on-action hook. Keep them lean; each just routes to their own
# events via the appropriate cp_try_fire_* gatekeeper.

cp_<name>_dispatch_startup = {
    cp_person_hook_noop = yes
    # Replace the no-op with optional save-migration/backfill logic
    # for cp_<name>_* variables when needed.
}

cp_<name>_dispatch_monthly = {
    cp_person_hook_noop = yes
    # Replace the no-op with a JE/display-state pulse if this person has one.
}

cp_<name>_dispatch_law_enacted = {
    cp_person_hook_noop = yes
    # if = { limit = { ROOT.currently_enacting_law.type ?= law_type:law_homesteading
    #                  NOT = { has_variable = cp_<name>_seen_homesteading } }
    #        cp_try_fire_law_reaction = { event = cp_<name>.2  person = <name> } }
}

cp_<name>_dispatch_yearly = {
    cp_age_increment = { person = <name> }
    cp_<name>_refresh_sol = yes
    cp_person_yearly_lifecycle = { person = <name> country = EGY }
    # any yearly milestone rolls go here
}

cp_<name>_dispatch_war_started = {
    cp_person_hook_noop = yes
}

cp_<name>_dispatch_war_end = {
    cp_person_hook_noop = yes
}

cp_<name>_dispatch_tech = {
    cp_person_hook_noop = yes
}

cp_<name>_dispatch_building = {
    cp_person_hook_noop = yes
}

cp_<name>_dispatch_revolution = {
    cp_person_hook_noop = yes
}


# --- Event effects ---------------------------------------------------------
cp_<name>_mark_intro = {
    cp_mark_event_seen = { person = <name> id = intro days = 3650 }
}


# --- Ambient pool ----------------------------------------------------------
# Called from cp_roll_for_event in cp_shared_firing.txt. Each option gates
# on per-event seen flags. cp_try_fire_ambient applies the 183d global /
# 365d per-person cooldown.

cp_roll_ambient_<name> = {
    random_list = {
        10 = { trigger = { NOT = { has_variable = cp_<name>_seen_intro } }
               cp_try_fire_ambient = { event = cp_<name>.10  person = <name> } }
        # ... add more beats as you write them
    }
}
```

### Step 2 — Register the person

Add one death-safe registration block to `mod/events/cp_shared_startup_events.txt` inside `cp_shared_startup.1`'s `immediate =` block:

```
if = {
    limit = {
        OR = {
            NOT = { has_variable = cp_<name>_alive }
            AND = {
                has_variable = cp_<name>_alive
                var:cp_<name>_alive > 0
            }
        }
    }
    cp_register_person = {
        person  = <name>
        country = <TAG>
    }
}
trigger_event = { id = cp_<name>.1 }
```

This sets the two global registry flags (`cp_person_<name>_alive`, `cp_person_<name>_country`), then triggers the person's hidden setup event if their local variable block does not exist yet. Country-variable init (culture, religion, home_state, profession, starting age) all happens in the person's own startup event (Step 3). The roster audit fails a registered person whose startup/spawn path does not trigger its setup event.

If the person is always-on and should be able to introduce the mod at game
start, add their visible intro to the randomized `cp_shared_startup.2`
first-contact table. Do not direct-fire their intro from their hidden setup
event; no person gets to own every new campaign.

**Why only two args?** V3's script compiler rejects scripted_effects that declare parameters the body doesn't reference. `cp_register_person` only touches `$person$` and `$country$` — extra args break compilation silently.

### Step 3 — Write the person's setup and first visible event

`mod/events/cp_<name>_events.txt`, first namespace. This initialises every `cp_<name>_<attr>` variable on their country.

```
namespace = cp_<name>

# cp_<name>.1 -- hidden setup
cp_<name>.1 = {
    type = country_event
    hidden = yes
    orphan = yes

    trigger = {
        c:<TAG> ?= this
        has_global_variable = cp_person_<name>_alive
        NOT = { has_variable = cp_<name>_alive }
    }

    immediate = {
        # Initialise every country variable this person needs
        set_variable = { name = cp_<name>_alive         value = 1 }
        set_variable = { name = cp_<name>_age           value = <age> }
        set_variable = { name = cp_<name>_hope          value = 5 }
        set_variable = { name = cp_<name>_exhaustion    value = 3 }
        set_variable = { name = cp_<name>_sol           value = 5 }
        set_variable = { name = cp_<name>_literacy      value = 0 }
        set_variable = { name = cp_<name>_radical       value = 0 }
        set_variable = { name = cp_<name>_loyalist      value = 0 }
        set_variable = { name = cp_<name>_profession_<poptype> value = 1 }

        # Plant exactly one state marker so local buildings and SoL reads
        # affect only people who live in that state, store the state pointer
        # rendered by the shared JE, then add one home-place token and one
        # workplace profile for local building routing.
        # Always-on persons can call cp_set_person_home_state directly.
        # Building-triggered conditional persons should use the marker-aware
        # form below so they inherit the triggering building's state.
        cp_set_person_home_state_from_spawn_marker_or_default = { person = <name> country = <TAG> state = <STATE> }
        cp_set_person_home_place = { person = <name> place = <place_token> }
        cp_set_person_workplace_profile = { person = <name> profile = <profile_token> }
        cp_<name>_refresh_sol = yes
    }
}


# cp_<name>.10 -- visible intro
cp_<name>.10 = {
    type = country_event

    title = cp_<name>.10.t
    desc  = cp_<name>.10.d
    flavor = cp_<name>.10.f

    icon = "gfx/interface/icons/event_icons/event_default.dds"

    event_image = {
        texture = "gfx/event_pictures/cp_<name>_intro.dds"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    on_opened_soundeffect = "event:/MUSIC/Stingers/events/tranquil"

    duration = 3

    trigger = {
        has_variable = cp_<name>_alive
        var:cp_<name>_alive > 0
        NOT = { has_variable = cp_<name>_seen_intro }
    }

    immediate = {
        cp_<name>_mark_intro = yes
    }

    option = {
        name = cp_<name>.10.a
        default_option = yes
    }
}
```

Trigger the hidden setup from `cp_shared_startup.1` immediately after `cp_register_person`, or (if conditional — e.g. only after a factory, law, or date condition) from the person's `cp_<name>_try_spawn` effect immediately after `cp_register_person`. Wire setup with a raw `trigger_event` (startup events bypass gatekeepers — they run once, and the static audit permits hidden setup plumbing). If a conditional person's world gates can already be true at game start, call their `cp_<name>_try_spawn` during the startup conditional scan and add their intro to `cp_shared_startup.2`; their setup event should suppress its own immediate visible intro while `cp_startup_conditional_scan` is set. Visible first appearances should be routed through `cp_shared_startup.2`, `cp_roll_for_event`, or the person-owned conditional spawn chance.

Conditional persons may roll a person-owned immediate first appearance inside
their setup event after non-startup spawn, because the game state that created
them is already the reason the player might meet them. Always-on persons
should instead rely on `cp_shared_startup.2` at game start and
`cp_roll_for_event` after that. Wire conditional spawn checks from startup and
every shared hook that can make them newly eligible. For example, factory-gated
persons should be checked from startup, yearly, technology, and building hooks;
the shared hook only calls `cp_<name>_try_spawn`, while the person file owns
the conditions, registration, setup, and non-startup immediate first-appearance
chance.

If the conditional gate depends on local buildings, mark the intended home
state before registration. Use `cp_mark_building_spawn_home = { person =
<name> }` in building scope for the exact just-built building. Inside
`cp_<name>_try_spawn`, call the matching shared fallback before
`cp_register_person` so startup/yearly/technology checks can select an existing
matching state instead of blindly using the default:

```
cp_mark_person_spawn_home_from_manufacturing = { person = <name> }
cp_mark_person_spawn_home_from_machine_industry = { person = <name> }
cp_mark_person_spawn_home_from_rail_infrastructure = { person = <name> }
cp_mark_person_spawn_home_from_port = { person = <name> }
cp_mark_person_spawn_home_from_government_office = { person = <name> }
cp_mark_person_spawn_home_from_electric_service = { person = <name> }
cp_mark_person_spawn_home_from_urban_growth = { person = <name> }
```

These effects do not override an exact building marker already planted by
`cp_on_building_built`. `script/audit-home-state-effects.py` fails
building-sensitive spawn gates that do not mark a matching home-state
candidate.

### Step 4 — Wire dispatchers in `cp_on_actions.txt`

For each internal dispatcher hook (`cp_on_monthly`, `cp_on_yearly`, `cp_on_law_enacted`, `cp_on_war_started`, `cp_on_war_end`, `cp_on_tech`, `cp_on_building_built`, `cp_on_revolution`), add one `if` block guarded on `cp_person_is_alive = { person = <name> }`. Keep the hook even if the person's dispatcher is still a no-op. Note that `cp_on_war_started` is reached from vanilla `on_diplo_play_war_start` after entering the relevant country scope via `scope:actor` / `scope:target`.

```
if = {
    limit = {
        c:<TAG> ?= this
        cp_person_is_alive = { person = <name> }
    }
    cp_<name>_dispatch_<hook> = yes
}
```

Do this per hook. Keep blocks lean — just the guard + the dispatch call. All the real routing lives in `cp_<name>_dispatch_<hook>` in the memory file.

### Step 5 — Add to the monthly router

Edit `cp_roll_for_event` in `mod/common/scripted_effects/cp_shared_firing.txt`:

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
        8 = {                                               # ← new context block
            trigger = {
                cp_person_is_alive = { person = <name> }
                # Example: use shared sensors first.
                cp_era_1850_to_1880 = yes
            }
            cp_roll_ambient_<name> = yes
        }
        32 = { }                                            # keep a positive silent branch
    }
}
```

Rule: each person gets one active context branch, not one permanent flat branch. Use shared sensors like `cp_era_before_1850`, `cp_person_home_has_manufacturing = { person = <name> }`, `cp_country_old_land_order`, `cp_country_public_schools`, or add a new shared sensor when the same game-state idea will matter to more than one person. For physical workplace/building beats, prefer `cp_person_home_has_*` so a building affects only characters who live in that state and have the matching workplace profile; reserve `cp_country_has_*` for national eligibility, technologies, laws, and spawn discovery. The silent branch must stay positive; the 183-day global cooldown still does the real annual pacing, so the full roster stays at 1-2 routine automatic beats/year instead of 1-2 per person.

### Step 6 — Handle shared triggers (only if they share a country)

If Person 2 shares a country with Person 1 and both would react to the same law enactment, resolve ownership with a weighted `random_list` in the **shared** dispatcher (`cp_on_law_enacted` in `cp_on_actions.txt`), placed *before* the per-person if-blocks:

```
if = {
    limit = {
        c:<TAG> ?= this
        ROOT.currently_enacting_law.type ?= law_type:law_homesteading
    }
    random_list = {
        60 = {
            trigger = {
                cp_person_is_alive = { person = layla }
                NOT = { has_variable = cp_layla_seen_homesteading }
            }
            cp_try_fire_law_reaction = { event = cp_layla.2  person = layla }
        }
        30 = {
            trigger = {
                cp_person_is_alive = { person = <name> }
                NOT = { has_variable = cp_<name>_seen_homesteading }
            }
            cp_try_fire_law_reaction = { event = cp_<name>.2  person = <name> }
        }
        10 = { }
    }
}
```

Weights express "whose life this beat belongs to most." Different playthroughs route the same law to different characters. That's the replayability mechanism.

If they don't share a country, skip this — `c:<TAG>` gating in per-person dispatchers is enough.

Shared `cp_on_law_enacted` direct fires are only for contests with two or more eligible registered persons. A single-person reaction belongs in `cp_<name>_dispatch_law_enacted`; `script/audit-common-people.py` fails new one-person direct law fires in the shared dispatcher.

### Step 7 — Write events, loc, images, sensors, buttons, JE

With the skeleton in place, content is purely additive:

**Events** — write into `cp_<name>_events.txt`. Every event's `immediate` block should include:

```
cp_mark_event_seen = { person = <name> id = <event_short_id> days = 540 }
```

This prevents repeat firing of the same beat inside the seen-flag window (use 365 for beats that can recur seasonally, 540 for one-per-life). Wrap every fire through a gatekeeper:

- Ambient fires from `cp_roll_ambient_<name>` → `cp_try_fire_ambient`.
- Law reactions from `cp_<name>_dispatch_law_enacted` → `cp_try_fire_law_reaction`.
- Routine world responses from `cp_<name>_dispatch_tech`, `cp_<name>_dispatch_building`, hidden conditional setup, or noncritical yearly/date routing → `cp_try_fire_world_response`.
- Critical milestones from yearly, war, mortality, family, crossroads, or revolution routing → `cp_try_fire_milestone`.
- Buttons (if a future shared roster-level button fires a story) → `cp_button_fire`.

If the person gets an authored war-start or revolution scene, do not simply
fire it from `cp_<name>_dispatch_war_started` or
`cp_<name>_dispatch_revolution`. Add the person to
`cp_roll_war_start_response` in `cp_shared_war.txt` or
`cp_roll_revolution_response` in `cp_shared_firing.txt`, have the resolver set
a `cp_shared_<hook>_target_<name>` flag, and make the person's dispatcher
consume that target flag before firing. That keeps one country rupture from
opening a stack of Common People windows.

Shared infrastructure (`cp_on_actions.txt`, `cp_shared_*`) should not directly call non-law gatekeepers for person events. It should enter the right scope, guard `cp_person_is_alive`, and call `cp_<name>_dispatch_*`. The static audit enforces this so new content does not rebuild a Layla-only lane.

Shared on-actions also must not directly mutate `cp_<name>_*` variables. Put startup migrations, monthly JE/display state, and hook-specific state changes inside the person's memory file, then call the relevant dispatcher. The static audit's `ON_ACTION_PERSON_MUTATION` rule catches direct person-variable writes from `cp_on_actions.txt`.

**Localization** — write `mod/localization/english/cp_<name>_l_english.yml`. First three bytes must be `ef bb bf` (BOM). Second line: `l_english:`. Every key you reference in events must be defined here.

**Images** — `cp_<name>_<beat>.dds`, DXT5 (BC3), 600x400 for event-window readability. Put in `mod/gfx/event_pictures/`.

**Sensors** — only if you need compound sensors (e.g. `cp_<name>_in_crisis` = SoL < 5 and age > 50). Otherwise skip. The shared sensors in `cp_shared_sensors.txt` are already parameterised.

**Shared JE policy** — do not create a per-person JE or "Check on <name>" button by default. The shipped persistent surface is `cp_je_common_people`, with a hidden-when-idle shared QA button. A per-person JE/button is a design exception, not the normal way to add a major person.

**Debug probes** — visible popups are covered by generated queue selectors so QA can review them without waiting for the right game state or opening popup windows from the console thread. All registered persons, including Layla, are generated by `script/generate-person-debug-wrappers.py`. After adding or renumbering visible events, run that generator and verify with `python3 script/generate-person-debug-wrappers.py --check` plus `script/audit-person-roster.py`. Hand-written `cp_debug.*` events are still useful for setup/state shortcuts, but they are no longer the source of truth for visible-event coverage.

---

## Death

When they die (from a milestone event's option, a mortality crossroads, or a war casualty):

```
cp_person_dies = {
    person  = <name>
    country = <TAG>
}
```

This clears `cp_<name>_alive` on the country and removes the global registry flag. Their other variables stay — post-death prose ("The Forty Days") can still read `cp_<name>_age`, `cp_<name>_sol` etc.

Their ambient pool stops firing because `cp_person_is_alive = { person = <name> }` fails in `cp_roll_for_event` and the gatekeepers. Their dispatcher blocks stop firing for the same reason. JE closes. Clean.

---

## What NOT to do

### Don't register household furniture

Ahmed (Layla's husband), the Bey's secretary, a neighbour's child — these are *not* persons. They're variables on the primary person's block: `cp_layla_ahmed_alive`, `cp_layla_ahmed_at_war`, `cp_layla_ahmed_profession_laborer`. A real person has:
- their own events (not just mentions in another person's events),
- their own ambient pool, and only an exceptional per-person JE if the shared surface is not enough,
- their own dispatcher branches,
- their own name token.

If they don't have these, they're furniture. Model them as variables on someone who does.

### Don't edit a Layla file

Adding Person 2 must not touch:
- `cp_layla_events.txt`
- `cp_layla_vox_events.txt`
- `cp_layla_memory.txt`
- `cp_layla_sensors.txt`
- `cp_layla_buttons.txt`
- `cp_layla_custom_loc.txt`
- `cp_layla_l_english.yml`

The only shared files you edit are:
- `cp_shared_startup_events.txt` (one new `cp_register_person` call plus one hidden setup trigger),
- `cp_shared_firing.txt` (one new branch in `cp_roll_for_event`),
- `cp_on_actions.txt` (one new `if` block per hook),
- (optional) shared-trigger resolver blocks in `cp_on_actions.txt` for laws both persons react to.

Everything else is new files prefixed `cp_<name>_*`.

### Don't use `cu:$culture$` at runtime

V3 does macro substitution at load time, not runtime. `cu:$culture$` only works if `$culture$` is a literal passed in at the callsite. The idiomatic pattern is a per-person wrapper that bakes the literal:

```
cp_<name>_refresh_sol = {
    cp_refresh_sol_from_pop = {
        person   = <name>
        culture  = <culture-literal>
        religion = <religion-literal>
        poptype  = <poptype-literal>
    }
}
```

Same for `c:$country$` and `rel:$religion$`. Look at `cp_layla_refresh_sol` (`cp_layla_memory.txt:24`) for the working example.

### Don't bypass the gatekeepers

Every visible event fire in a person's files must flow through one of the five gatekeepers. Raw `trigger_event` is allowed only inside another event's `immediate` or option block for chained follow-ups (the next scene in the same beat).

### Don't skip the seen-flag

Ambient events that don't set their own `cp_<name>_seen_<id>` in the event body can fire twice per playthrough (bounded by the 183-day global cooldown). That's fine for small beats but wrong for one-per-life events. Always plant `cp_mark_event_seen` in the `immediate` block.

---

## Completion checklist

After wiring, verify:

```bash
# 1. Variable rename is complete (no leftover cp_<attr> without prefix)
grep -RE '\bcp_(hope|age|sol|literacy|radical|loyalist|exhaustion)\b' mod/ --include='*.txt' | grep -v cp_<name>_

# 2. All trigger_event calls in person's files flow through gatekeepers
grep -E 'trigger_event' mod/events/cp_<name>_events.txt | grep -v '^[[:space:]]*#' \
    | grep -v cp_try_fire_ | grep -v cp_button_fire

# 3. Registry flag is both set and checked
grep cp_person_<name>_alive mod/

# 4. Monthly router has a branch for this person
grep cp_roll_ambient_<name> mod/common/scripted_effects/cp_shared_firing.txt

# 5. Loc file has correct BOM
xxd mod/localization/english/cp_<name>_l_english.yml | head -1  # must start ef bb bf

# 6. Every referenced event image exists
grep -oE 'cp_<name>_[a-z_0-9]+\.dds' mod/events/cp_<name>_events.txt | sort -u \
    | while read f; do test -f "mod/gfx/event_pictures/$f" || echo "MISSING: $f"; done

# 7. Roster scaffold stays scalable
script/audit-person-roster.py
```

All clean → boot V3. First monthly ticks should route the new person only through the shared ambient budget, and debug QA paths should be able to force their setup/intro/law beats. Follow the current rebuild plan in `documentation/test-plan-v0.5-rebuild.md` for multi-person readiness validation.

---

## Reference — Layla as the worked example

Everything Layla has is what Person 2 should have. Read these in order:

| Role | File | Read for |
|---|---|---|
| Registration | `mod/events/cp_shared_startup_events.txt:39-47` | How `cp_register_person` is called |
| Country-var init | `mod/events/cp_<name>_events.txt` or `mod/events/cp_<name>_setup_events.txt` | The intro event's `immediate` block |
| Refresh wrapper | `mod/common/scripted_effects/cp_layla_memory.txt:24-31` | The per-person literals-baked wrapper |
| Dispatcher branches | `mod/common/scripted_effects/cp_layla_memory.txt` (search `cp_layla_dispatch_`) | One per hook |
| Ambient pool | `mod/common/scripted_effects/cp_layla_memory.txt:1115-1177` | The `random_list` over her beats |
| Monthly routing | `mod/common/scripted_effects/cp_shared_firing.txt:129-139` | How Layla plugs into the router |
| Dispatcher wiring | `mod/common/on_actions/cp_on_actions.txt` (search `cp_person_is_alive = { person = layla }`) | Guarded dispatcher calls |
| Shared-trigger pattern | `documentation/characters/_shared/firing.md` §Shared-trigger resolution | Weight-driven person routing |

If your Person N files match the required person shape one-to-one, you're done. If anything differs structurally, the refactor either drifted or your person is genuinely different (e.g. a minor person with no JE, no button, no conversation tree) — in which case you omit the optional files rather than restructuring the required ones.
