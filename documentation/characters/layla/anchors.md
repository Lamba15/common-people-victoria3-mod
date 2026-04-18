# Layla's State Model

> The novel is a state machine. At any moment Layla is in one *anchor* (life phase), has zero or more *branch letters* set (the world she lives in), and carries a handful of *flags, weights, and opinions*. Monthly pulse draws a vignette from a pool matching that state. Reactions move her between anchors and set branch letters.
>
> This file is the spec. Reactions live in `reactions.md`; pulse events live in `pulse.md`. Both depend on the definitions here.

---

## Table of contents

1. [Branch letters (three binary hinges)](#1-branch-letters)
2. [Anchors (the twelve life phases)](#2-anchors)
3. [Anchor transition table](#3-anchor-transition-table)
4. [Character variables reference](#4-character-variables-reference)
5. [Monthly pulse dispatcher](#5-monthly-pulse-dispatcher)
6. [Scripted triggers to create (for the eventify pass)](#6-scripted-triggers-to-create)

---

## 1. Branch letters

Branch letters record which world she lives in. Each hinge is binary. Letters are set by **reactions** when a game-state threshold is crossed; once set, they don't unset unless an explicit rollback reaction fires. Pulse events **read** letters to pick variant prose; they never **write** them.

### H1 -- The Land

Does serfdom give way in her lifetime?

| Letter | Set when | Sub-letter |
|---|---|---|
| `A` | Egypt enacts any non-serfdom land law while she lives. The specific law is stored in a sub-letter so prose can differ. | `A.T` = `law_tenant_farmers`, `A.H` = `law_homesteading`, `A.C` = `law_commercialized_agriculture`, `A.K` = `law_collectivized_agriculture` |
| `B` | Serfdom persists. Default letter while `cp_h1` is unset and EGY has `law_serfdom`. Formalized as `B` at age ~40 (no reform came in her young adulthood). | none |

Rollback: if she's on `A.*` and the country slides back to `law_serfdom` (the darkest event in the mod), `cp_h1` is re-set to `B` and `cp_h1_rolled_back = 1` is flagged. Prose treats this as the worst rupture of her life.

### H2 -- The Throne

Is Egypt still an Ottoman subject, or sovereign?

| Letter | Set when |
|---|---|
| `α` (alpha) | Egypt remains a subject/vassal of OTT per V3 diplomacy. Default letter while EGY's overlord is OTT. Formalized as `α` at age ~45 (no break came in her middle adulthood). |
| `β` (beta) | Egypt breaks free -- independence declared, war of independence won, inherited independence from OTT collapse, any path. Set on the first event that makes EGY's overlord non-OTT. |

Rollback: if Egypt is reconquered/vassalized back under OTT, `cp_h2` is re-set to `α` and `cp_h2_rolled_back = 1`. Prose treats this as a mocking of the generation that had dared to hope.

### H3 -- The World

Has the modern world arrived at her village door?

| Letter | Set when |
|---|---|
| `X` | Egypt stayed agrarian. No industry laws above `law_no_labor_rights` + urbanization low + no foreign concessions of note. Default letter. Formalized as `X` at age ~55 (the world came not). |
| `Y` | The world came. Any of: industrialization laws enacted, urbanization in any EGY state above threshold, foreign capital concession granted, major railway constructed, capitulations signed. First of any of these sets `cp_h3 = "Y"`. |

H3 does not roll back -- once the factory whistle has been heard, the memory remains.

### Scripted-trigger wrappers (eventify pass)

```
cp_is_branch_A          -> cp_h1 == "A"
cp_is_branch_B          -> cp_h1 == "B"
cp_is_land_homesteading -> cp_h1_sub == "H"
cp_is_sultanate         -> cp_h2 == "alpha"
cp_is_sovereign_egypt   -> cp_h2 == "beta"
cp_world_came           -> cp_h3 == "Y"
cp_world_stayed         -> cp_h3 == "X"
```

Reactions and pulse events use these triggers, not raw variable reads. Keeps the eventify pass consistent and one-line changes easy.

---

## 2. Anchors

An anchor is her current life phase. She is in exactly one at a time. Each anchor has entry conditions (set by a reaction or automatic on spawn), exit conditions (what reactions can move her out), and a rough age band. Anchors are **orthogonal** to branch letters: a `widow` in `A.β.Y` state is a different novel from a `widow` in `B.α.X`. Anchor says *what she is doing now*; branch letters say *what world she is doing it in*.

Stored as `cp_anchor = "<id>"` (string variable on her character).

### Marital / family anchors

#### `bride`
- **Entry:** spawn (age 22, newlywed to Ahmed, no children). Default at game start.
- **Exit:** first pregnancy reaction (-> `young_mother`); age 28 with no pregnancy (-> flag `cp_barren_wife = 1`, anchor stays `bride` but pulse pool shifts).
- **Typical duration:** 1-5 years.

#### `young_mother`
- **Entry:** first child born (childbirth reaction).
- **Exit:** youngest surviving child turns 10 (automatic anchor check) -> `mother`. Also: Ahmed conscripted -> `soldiers_wife` (returns here when war ends).
- **Typical duration:** 8-12 years.

#### `mother`
- **Entry:** youngest surviving child turns 10.
- **Exit:** youngest surviving child turns 18 -> `matriarch`. Ahmed dies -> `widow`. Ahmed conscripted -> `soldiers_wife`.
- **Typical duration:** 8-10 years.

#### `soldiers_wife`
- **Entry:** "Ahmed conscripted" reaction (any war, any branch). Stores `cp_prev_anchor = <old_anchor>` so she can return.
- **Exit:** war ends with Ahmed alive -> `cp_prev_anchor`. Ahmed dies in war -> `widow`.
- **Typical duration:** months to years, bounded by war.

#### `widow`
- **Entry:** Ahmed-dies reaction (war or natural).
- **Exit:** natural progression through age -- `widow` is marital-state terminal, but she still ages into `matriarch` / `elder` with the widow flag retained. So `cp_anchor` may become `matriarch_widow` or `elder_widow` (composite), OR we keep `cp_anchor = "widow"` and carry `cp_age_band` separately. **Decision:** keep it simple -- `cp_anchor = "widow"` persists; `cp_age_band` is set separately and pulse events use both.
- **Typical duration:** years to decades.

#### `matriarch`
- **Entry:** youngest surviving child turns 18 and Ahmed alive.
- **Exit:** age 55 -> `elder`. Ahmed dies -> `widow`.
- **Typical duration:** ~10 years.

#### `elder`
- **Entry:** age 55 with Ahmed alive. Or `widow` persists and she crosses 55 (anchor stays `widow`, age band shifts -- see widow note).
- **Exit:** death roll succeeds -> `dying`.
- **Typical duration:** 5-15 years.

#### `dying`
- **Entry:** natural-death reaction fires (age 60+ yearly roll), or disaster-death reaction (cholera/famine/childbirth).
- **Exit:** closure reaction -> END (character flagged dead, legacy reaction fires, arc concludes).
- **Typical duration:** a single event.

### Landholding anchors (overlay on marital anchors)

Landholding is a **second axis**: she's always in one of these in parallel with her marital anchor. Stored as `cp_land_anchor = "<id>"`. Pulse events can require both (e.g. anchors=`young_mother` + land_anchor=`serf_wife`).

| `cp_land_anchor` | Entry | Exit |
|---|---|---|
| `serf_wife` | default at spawn while `cp_h1` unset and EGY has `law_serfdom`; also re-entry on H1 rollback | H1 resolves to `A.*` -> matching land_anchor below |
| `landowner_wife` | `A.H` (homesteading) enacted | debt reaction -> `tenant_wife`; land-lost reaction -> `laborer_wife`; H1 rollback -> `serf_wife` |
| `tenant_wife` | `A.T` (tenant_farmers) enacted, or `landowner_wife` loses the deed to debt | land-lost reaction -> `laborer_wife`; rollback -> `serf_wife` |
| `wage_laborer_wife` | `A.C` (commercialized) enacted while rural, or `tenant_wife` loses tenancy | migration reaction -> `city_laborer`; rollback -> `serf_wife` |
| `collective_member` | `A.K` (collectivized) enacted | H1 rollback -> `serf_wife`; migration -> `city_laborer` |
| `city_laborer` | migration reaction from any rural land_anchor. Separately sets `cp_in_city = 1` and updates her home state. | return-to-village reaction (rare) -> previous rural land_anchor; husband's death + son calls her home -> widow + rural |

Rationale for two-axis anchors: marital state and landholding state move on different clocks. Conflating them would give us 6 x 8 = 48 anchors; keeping them orthogonal gives us 8 + 6 = 14 and the same coverage.

### Summary: the anchor pair

At any time Layla's anchor pair is `(cp_anchor, cp_land_anchor)`. Pulse events can require just one or both. Reactions move either or both in a single fire.

Total anchors: 8 marital + 6 landholding = 14 distinct. Well within the 10-anchor floor.

---

## 3. Anchor transition table

Which reactions move her between which anchors. Every non-terminal anchor has at least one documented exit. Reaction IDs (`R<n>`) are forward references to `reactions.md`.

### Marital axis

```
bride ─── R_first_pregnancy ──────────► young_mother
bride ─── age_check: 28 + no child ───► (bride, cp_barren_wife = 1)
young_mother ─── R_all_children_10 ───► mother
young_mother ─── R_ahmed_conscripted ─► soldiers_wife (prev: young_mother)
mother ─── R_all_children_18 ─────────► matriarch
mother ─── R_ahmed_conscripted ───────► soldiers_wife (prev: mother)
mother ─── R_ahmed_dies ──────────────► widow
soldiers_wife ─── R_ahmed_returns ────► cp_prev_anchor
soldiers_wife ─── R_ahmed_dies ───────► widow
matriarch ─── age_check: 55 ──────────► elder
matriarch ─── R_ahmed_dies ───────────► widow
widow ─── age_check: 55 ──────────────► (widow, cp_age_band = elder)
elder ─── R_natural_death_roll ───────► dying
widow ─── R_natural_death_roll ───────► dying
widow ─── R_cholera_death ────────────► dying
(any) ─── R_cholera_death ────────────► dying
dying ─── R_closure ──────────────────► END
```

### Landholding axis

```
serf_wife ─── R_h1_tenant_farmers ─────► tenant_wife       (sets cp_h1=A, cp_h1_sub=T)
serf_wife ─── R_h1_homesteading ───────► landowner_wife    (sets cp_h1=A, cp_h1_sub=H)
serf_wife ─── R_h1_commercialized ─────► wage_laborer_wife (sets cp_h1=A, cp_h1_sub=C)
serf_wife ─── R_h1_collectivized ──────► collective_member (sets cp_h1=A, cp_h1_sub=K)
serf_wife ─── R_serfdom_endures ───────► (serf_wife, cp_h1=B)
landowner_wife ─── R_debt_forecloses ──► tenant_wife
landowner_wife ─── R_h1_rollback ──────► serf_wife         (sets cp_h1=B, cp_h1_rolled_back=1)
tenant_wife ─── R_tenancy_lost ────────► wage_laborer_wife
tenant_wife ─── R_h1_rollback ─────────► serf_wife         (and rolled_back flag)
wage_laborer_wife ─── R_migrates ──────► city_laborer
any_rural ─── R_family_migrates ───────► city_laborer
city_laborer ─── R_returns_to_village ─► wage_laborer_wife (rare)
```

### Common combinations (reference, not exhaustive)

| Marital | Land | Typical age | Example prose anchor |
|---|---|---|---|
| `bride` | `serf_wife` | 22-26 | "The dawn rises on another year of the bey's fields." |
| `young_mother` | `landowner_wife` | 28-38 | "Her son sleeps in the room she owns." |
| `mother` | `tenant_wife` | 36-46 | "The rent is due and the harvest is not in yet." |
| `soldiers_wife` | `wage_laborer_wife` | 40s | "Ahmed's wage stopped when his name was read out." |
| `widow` | `city_laborer` | 50s | "She scrubs the floor of a house she has never seen in daylight." |
| `elder` | `serf_wife` (B, never reformed) | 65+ | "She has outlived three beys and buried two children." |

---

## 4. Character variables reference

Everything Layla's state machine needs, stored on her character via `save_scope_as = cp_layla`.

### Branch letters (set by reactions, read by pulse + reactions)

| Variable | Values | Notes |
|---|---|---|
| `cp_h1` | unset / `"A"` / `"B"` | H1 state |
| `cp_h1_sub` | unset / `"T"` / `"H"` / `"C"` / `"K"` | valid only when `cp_h1 = "A"` |
| `cp_h1_rolled_back` | 0 / 1 | set if she ever saw A and was pushed back to B |
| `cp_h2` | unset / `"alpha"` / `"beta"` | H2 state |
| `cp_h2_rolled_back` | 0 / 1 | sovereign Egypt reconquered |
| `cp_h3` | unset / `"X"` / `"Y"` | H3 state; no rollback |

### Anchors (set by reactions, read by pulse)

| Variable | Values |
|---|---|
| `cp_anchor` | `"bride"` / `"young_mother"` / `"mother"` / `"soldiers_wife"` / `"widow"` / `"matriarch"` / `"elder"` / `"dying"` |
| `cp_land_anchor` | `"serf_wife"` / `"landowner_wife"` / `"tenant_wife"` / `"wage_laborer_wife"` / `"collective_member"` / `"city_laborer"` |
| `cp_prev_anchor` | any marital value | saved when she enters `soldiers_wife`, used to return |
| `cp_age_band` | `"young"` (<35) / `"middle"` (35-54) / `"elder"` (55+) | updated by yearly tick; overlay on anchor |

### Personal flags (set by reactions, read by pulse)

| Flag | Meaning |
|---|---|
| `cp_pregnant` | 1 while expecting |
| `cp_barren_wife` | 1 if passed 28 childless |
| `cp_ahmed_at_war` | 1 while Ahmed is conscripted |
| `cp_widow` | 1 after Ahmed's death |
| `cp_bereaved_mother` | counter: how many children she has lost |
| `cp_children_alive` | counter: how many children currently living |
| `cp_in_city` | 1 if she has migrated |
| `cp_literacy` | 0 (illiterate) / 1 (reads minimally) / 2 (reads well) -- reflects state literacy + personal events |
| `cp_recent_hardship` | sliding window flag: 1 for 12 months after any hardship reaction |
| `cp_recent_joy` | sliding window flag: 1 for 6 months after any joy reaction |
| `cp_hears_foreign_news` | 1 if state allows foreign news to reach her (info-flow gate) |

### Personality weights (0-10, clamped)

Already documented in `README.md`. Key ones: `cp_w_land_reform`, `cp_w_war`, `cp_w_revolution`, `cp_w_religion`, `cp_w_womens_rights`, `cp_w_economy`, `cp_w_france`, `cp_w_education`, `cp_w_labor_laws`, `cp_w_diplomacy`. Plus `cp_hope` (0-10), which is its own scalar.

### Opinions (-100 to +100)

`cp_opinion_ott`, `cp_opinion_fra`, `cp_opinion_gbr`, `cp_opinion_egy`, `cp_opinion_gre`, `cp_opinion_ita`. Others stay 0.

---

## 5. Monthly pulse dispatcher

The core loop. Fires monthly on EGY while Layla is alive.

### Pseudocode

```
on_monthly_pulse_country {
    effect = {
        if = {
            limit = { exists = scope:cp_layla  scope:cp_layla = { is_alive = yes } }
            scope:cp_layla = {
                random_list = {
                    90 = { }                       # 90% silent, as per design
                    10 = {
                        trigger_event = {
                            # A dispatcher event whose options are all the pulse
                            # events, each guarded by an AI chance of 0 unless its
                            # anchor / branch / flag requirements match.
                            id = cp_layla_pulse.dispatch
                        }
                    }
                }
            }
        }
    }
}
```

### Why a dispatcher event instead of random_events on the on_action

- The pulse events are plural and varied; encoding 100 of them as weighted branches in an `on_action` is worse to maintain than one dispatcher event with 100 options.
- We get to apply cooldowns and recency weights inside the dispatcher using scripted effects.
- Future pulse events drop in by adding one option -- no on_action edits.

### Dispatcher event (cp_layla_pulse.dispatch) skeleton

```
cp_layla_pulse.dispatch = {
    type = country_event
    hidden = yes
    trigger = { exists = scope:cp_layla  scope:cp_layla = { is_alive = yes } }
    immediate = {
        # Dispatcher picks exactly one pulse event to fire by trying each in
        # priority order; first one whose guards pass fires and the rest short-circuit.
        # Alternative: use random_list weighted by pool tuning. Eventify pass decides.
        scope:cp_layla = {
            ordered_list_of_pulse_ids = { ... }   # generated from pulse.md
        }
    }
}
```

Exact mechanism (random_list vs. ordered probe vs. scripted effect) is an eventify-pass decision. `anchors.md` just names the contract: the dispatcher fires exactly one pulse event whose requirements match, or none if the pool is empty for her state.

### Cooldowns and recency

Each pulse event declares a cooldown (months). The dispatcher records `cp_last_pulse_<id>` as a months-since value and refuses to fire an event whose cooldown has not elapsed. Cooldowns stop the same vignette from ringing back-to-back.

### Weighting

Each pulse event declares a base weight (default 1.0) and optional modifiers keyed to flags (`cp_recent_hardship` +0.5, `cp_recent_joy` -0.3, season, age band). Final weight feeds `random_list` if the dispatcher uses weighted selection.

---

## 6. Scripted triggers to create

For the eventify pass. These wrap the raw variable reads so reactions and pulse events stay terse and single-line-editable.

### Branch-letter triggers

```
cp_is_branch_A             # land reformed (any)
cp_is_branch_B             # serfdom endures
cp_is_land_tenant          # cp_h1_sub == "T"
cp_is_land_homesteading    # cp_h1_sub == "H"
cp_is_land_commercial      # cp_h1_sub == "C"
cp_is_land_collective      # cp_h1_sub == "K"
cp_h1_ever_rolled_back     # cp_h1_rolled_back == 1

cp_is_sultanate            # H2 alpha
cp_is_sovereign_egypt      # H2 beta
cp_h2_ever_rolled_back

cp_world_came              # H3 Y
cp_world_stayed            # H3 X
```

### Anchor triggers

```
cp_anchor_is_bride
cp_anchor_is_young_mother
cp_anchor_is_mother
cp_anchor_is_soldiers_wife
cp_anchor_is_widow
cp_anchor_is_matriarch
cp_anchor_is_elder

cp_land_anchor_is_serf
cp_land_anchor_is_landowner
cp_land_anchor_is_tenant
cp_land_anchor_is_wage_laborer
cp_land_anchor_is_collective
cp_land_anchor_is_city_laborer

cp_in_marital_family_life  # any of young_mother, mother, matriarch
cp_in_rural_anchor         # any land_anchor != city_laborer
```

### State triggers

```
cp_hears_foreign_news      # info-flow gate
cp_has_children_alive      # cp_children_alive > 0
cp_had_hardship_recently   # cp_recent_hardship == 1
cp_had_joy_recently        # cp_recent_joy == 1
cp_is_literate             # cp_literacy > 0
```

### Scripted effects to create

```
cp_set_anchor = <name>     # sets cp_anchor, stores previous, handles age-band side effects
cp_set_land_anchor = <name>
cp_resolve_h1 = <letter>   # sets cp_h1, optionally cp_h1_sub, logs via debug if -debug_mode
cp_resolve_h2 = <letter>
cp_resolve_h3 = <letter>
cp_mark_hardship          # sets cp_recent_hardship = 1 with a 12-month timer
cp_mark_joy               # sets cp_recent_joy = 1 with a 6-month timer
cp_shift_opinion = { tag delta }
cp_shift_weight = { name delta }
cp_roll_death = { cause }  # death check with a cause-tagged probability
```

The eventify pass creates these in `mod/common/scripted_triggers/` and `mod/common/scripted_effects/`. Reactions and pulse events call them exclusively -- no raw `set_variable` outside the scripted-effect library. Keeps state changes auditable and refactor-safe.

---

*Next: `reactions.md` -- the ~50 reaction events that move Layla through this state machine. Then `pulse.md` -- the ~100 vignettes that paint each state.*