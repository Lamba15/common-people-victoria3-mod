# Victoria 3 scripting — language notes

A running log of hard-won facts about Paradox's V3 scripting dialect. Every
entry cites a vanilla file that proves the pattern or a session where the
fact was established empirically. Read this before inventing syntax; append
new entries whenever a gotcha costs more than 10 minutes.

Source of truth: installed vanilla at
`/media/aboelsoud/97889587-.../SteamLibrary/steamapps/common/Victoria 3/game/`.


## 1. Scope reference cheat-sheet

`root` — the event's root scope (country_event → country, character_event → character).
Persists through nested blocks; does NOT change when you scope-jump.

`this` — the current scope. Changes every time you enter a `{}` that redirects scope.

`prev` — the scope one level up the chain. Useful inside `random_scope_state`,
`ordered_scope_pop`, etc., to refer back to the parent scope.

`scope:<name>` — a named scope saved with `save_scope_as` (persists for the
event's lifetime) or `save_temporary_scope_as` (same lifetime, no save-file
footprint).

**Cross-scope trigger reads must use the nested block form, not the dot form:**

```
# WRONG (silently fails)
limit = { root.has_variable = cp_foo }

# RIGHT
limit = { root = { has_variable = cp_foo } }
```

Vanilla source: `common/character_interactions/01_additional_interactions.txt:164`.
Empirical: the wrong form caused a scripted effect to silently no-op, leaving
a variable at its startup value. No parse error was logged.

The dot form IS valid in localization substitutions
(`[ROOT.GetCountry.GetRuler.GetFullName]`) and in script_values as a value
chain (`value = c:EGY.average_sol`) — but NOT in trigger blocks.


## 2. State geography — states vs region_states vs city hubs

V3 has three nested concepts that are easy to conflate:

- **State region** (`s:STATE_LOWER_EGYPT`) — the geographic polygon on the
  map. Persistent across the game. There are 673 of them.
- **Region state** (`region_state:EGY` inside a state region) — one per
  owning country. A state region shared between two countries has two
  region_states. This is where `average_sol`, `state_urbanization_rate`,
  pops, and buildings actually live.
- **City hub** — the urban centre tile of a state region. City hubs have
  names (Cairo, Alexandria, Damascus) but are NOT state regions. Accessed
  via `.GetStateRegion.GetCityHubName`.

**Navigation patterns:**

```
# Enter a state region → random_scope_state → region_state
s:STATE_LOWER_EGYPT ?= {
    random_scope_state = {
        limit = { owner = c:EGY }
        # scope here = region_state, readable: average_sol, pops, etc.
    }
}

# From country scope → every_scope_state iterates its region_states
c:EGY = {
    every_scope_state = {
        limit = { has_variable = cp_foo }
        # scope here = region_state
    }
}
```

Vanilla sources:
- `common/journal_entries/00_belle_epoque.txt` (state-region nav)
- `common/scripted_progress_bars/00_ip4_morocco_progress_bars.txt` (`region_state:MOR ?= { value = average_sol }`)
- `common/laws/00_slavery.txt` (`every_scope_state + limit = { has_variable }`)


## 3. Pop iteration — what works, what doesn't

**Effect iterators** (run in immediate/option effects):
- `every_scope_pop` — iterates all pops in the current scope.
- `random_scope_pop` — picks one at random from matches.
- `ordered_scope_pop` — picks by `order_by = <value>` / `position = 0`.

**Trigger iterators** (run in limit/trigger blocks):
- `any_scope_pop` — returns true if ANY pop matches.
- `every_scope_pop` does NOT work as a trigger. It silently evaluates to
  true. Do not use it as a "for all pops" check.

**The canonical read-one-pop-value pattern:**

```
s:STATE_LOWER_EGYPT ?= {
    random_scope_state = {
        limit = { owner = c:EGY }
        ordered_scope_pop = {
            limit = {
                culture = cu:misri
                religion = rel:sunni
                is_pop_type = peasants
            }
            order_by = total_pops
            position = 0
            check_range_bounds = no
            save_temporary_scope_value_as = {
                name = tmp_sol
                value = standard_of_living
            }
        }
    }
}
# scope:tmp_sol now holds the largest matching pop's SoL, or is unset
# if no pop matched.
```

Vanilla source: `events/india_events/india_misc_events.txt:1565` (ordered_scope_state
with order_by + position + check_range_bounds).

**Key filters on `any_scope_pop` / `ordered_scope_pop` limit blocks:**
- `culture = cu:<name>`
- `religion = rel:<name>`
- `is_pop_type = <name>` (NOT `pop_type` — that's for other contexts)
- `standard_of_living >= N` / `< N` — numeric; both directions work.

**What does NOT work:** using `NOT = { any_scope_pop = { ... SoL < N } }` as
a "min SoL in group" bisection. Empirically returns "no match" too often —
likely because the engine short-circuits the filter chain differently than
an equivalent direct check. Use `ordered_scope_pop order_by = total_pops`
and accept the largest-pop proxy instead.


## 4. Reading simulation values into variables

**What's readable as a value** (grep-verified):

| Attribute              | Scope           | Context                        |
|------------------------|-----------------|--------------------------------|
| `average_sol`          | country         | `set_variable value = average_sol` works |
| `average_sol`          | region_state    | Only inside `random_scope_state` / `every_scope_state` body |
| `standard_of_living`   | pop             | Inside pop scope, via `save_temporary_scope_value_as` |

**What's NOT directly readable** (returned 0 in testing):
- `state_average_sol` as a read-value (trigger-only — comparisons work, but
  `save_temporary_scope_value_as = { value = state_average_sol }` returns 0).

**The idiom to extract a value from a non-current scope:**

```
<target_scope> = {
    save_temporary_scope_value_as = {
        name = tmp_x
        value = <attribute>
    }
}
# scope:tmp_x is now readable from outside
set_variable = { name = cp_x value = scope:tmp_x }
```

`save_temporary_scope_value_as` is event-lifetime; it persists across scope
exits within the same event/effect chain.


## 5. Script values — math-only computations

Files in `common/script_values/` can be referenced by name as numeric values.
They support:

- `value = <number or scope.attribute>`
- `add`, `subtract`, `multiply`, `divide`, `min`, `max`, `round`
- Scope blocks: `s:STATE_X ?= { add = average_sol }`
- Condition blocks: `if = { limit = { X } value = Y } else = { value = Z }`

They do NOT support:
- Effects (no `set_variable`, no `trigger_event`).
- Triggers as statements (only as `limit = { }` gating).
- Iteration (`every_scope_*` / `random_scope_*` don't produce aggregated math).

Empirical: tried to expose state-region avg SoL via script_value with
`s:STATE_X.region_state:EGY ?= { add = average_sol }`. Returned 0. The
scope-chain-dot form works in progress bars but not in script_values.
Workaround: do the math in a scripted_effect using `save_temporary_scope_value_as`.


## 6. Variables — country, state, global

**Country variables** — `c:EGY` has `var:cp_X`, `has_variable = cp_X`,
`set_variable`, `change_variable`, `remove_variable`. Persists through save/load.

**State-scope variables** — region_states can carry their own variables.
Used by vanilla for state-specific JE flags (e.g. `cult_center`,
`former_slave_state`). Access via `every_scope_state / any_scope_state`
with `has_variable` in the limit.

**Global variables** — `set_global_variable = { name = X value = Y }`,
`has_global_variable`, `global_var:X`.

**Scope pointers as variables** — a variable can hold a scope reference:

```
s:STATE_X ?= {
    ROOT = { set_variable = { name = my_ptr value = prev } }
}
# Later:
var:my_ptr = { ... }  # scope becomes the state pointed to
```

Render in localization: `[Country.Var('my_ptr').GetState.GetStateRegion.GetName]`.
Vanilla source: `common/scripted_effects/00_expedition_effects.txt:911`.


## 7. Macro substitution in scripted effects

Scripted effects take parameters via `$name$`:

```
cp_do_thing = {
    set_variable = { name = cp_x value = $delta$ }
}
# Call:
cp_do_thing = { delta = 5 }
```

Substitution happens at compile time, so `$state$` can be a V3 identifier
like `STATE_LOWER_EGYPT` and expands to valid syntax. You cannot pass a
variable as the macro argument — it must be a literal.

To dispatch on a runtime state, branch with `if/else_if` on flags OR use
a state-scope marker + `every_scope_state` to iterate.


## 8. Save-migration guards (self-heal)

V3 mods should tolerate old saves that predate new variables. Pattern:

```
# In cp_on_start (wired to on_game_started)
if = {
    limit = { has_variable = cp_X_alive  NOT = { has_variable = cp_new_var } }
    set_variable = { name = cp_new_var value = <sensible default> }
}
```

Guard with `has_variable = <life flag>` so NEW games (where the life flag
isn't set yet) skip the backfill and go through normal startup.


## 9. Color + icon markup in localization

V3 uses `#` for markup, not `§`:

- `#G green text #!`
- `#R red text #!`
- `#b bold #!`
- `#v value #!`
- `#italic italicized #!`

Inline icons use `@name!` — e.g. `@clock!`, `@paper!`, `@peasants!`,
`@state!`, `@destitute!`, `@struggling!`, `@impoverished!`, `@middling!`,
`@secure!`, `@prosperous!`, `@affluent!`, `@wealthy!`, `@lavish!`,
`@opulent!`, `@popularity!`, `@activism!`, `@pinned_star!`,
`@movement_royalist_absolutist!`.


## 10. Known silent-failure modes

Gotchas that cost hours and produced no error log entry:

1. **Wrong scope access syntax** (`root.has_variable`) — silent no-op.
2. **Wrong trigger context for value reads** — `state_average_sol` as a
   read-value in `save_temporary_scope_value_as` returned 0.
3. **Non-existent state identifier** in `s:STATE_X ?=` — the `?=` guard
   silently skips. (STATE_NUBIA does not exist; use STATE_BLUE_NILE for Sudan.)
4. **`every_scope_pop` as trigger** — silently evaluates to `true`.
5. **Variance masking bugs** — a ±1 random on top of a silent no-op looks
   like "the variable didn't move" rather than "the write failed". Suppress
   variance in debug probes.
6. **`change_variable = { subtract = var:X }`** — silently no-ops in some
   contexts. Use `multiply_variable = -1` + `change_variable = { add = var:X }`
   as a safe pattern.


## 11. Debug workflow

When a scripted effect silently fails:

1. Add a marker write at the TOP of the effect (`set_variable = cp_sol = 99`).
   If `cp_sol` stays at its prior value, the effect never ran.
2. Add marker writes between each stage (11, 22, 33, …) and observe where
   the marker stops updating in the JE readout.
3. Strip variance / random elements from debug probes; they mask which
   stage failed.
4. Test in an in-game debug event with `hidden = yes, orphan = yes`, fired
   via `event <namespace>.<id>` in the console.


## Appendix — confirmed-working patterns

### Cohort read (largest pop of a culture/religion/pop_type in a state)

```
s:STATE_LOWER_EGYPT ?= {
    random_scope_state = {
        limit = { owner = c:EGY }
        ordered_scope_pop = {
            limit = {
                culture = cu:misri
                religion = rel:sunni
                is_pop_type = peasants
            }
            order_by = total_pops
            position = 0
            check_range_bounds = no
            save_temporary_scope_value_as = {
                name = tmp_cohort_sol
                value = standard_of_living
            }
        }
    }
}
```

### State-region avg SoL read

```
s:STATE_LOWER_EGYPT ?= {
    random_scope_state = {
        limit = { owner = c:EGY }
        save_temporary_scope_value_as = {
            name = tmp_state_sol
            value = average_sol
        }
    }
}
```

### Country avg SoL — simpler, works anywhere

```
set_variable = { name = cp_sol value = average_sol }
# where scope = the country you want to read
```

### Data-driven home-state (location as state-scope variable)

```
# Set marker + pointer
cp_move_to_state = {
    cp_clear_home_state = yes          # clears marker globally
    s:$state$ ?= {
        random_scope_state = {
            limit = { owner = c:EGY }
            set_variable = cp_layla_lives_here
            root = {
                set_variable = { name = cp_layla_state_pointer value = prev }
            }
        }
    }
}

# Clear everywhere
cp_clear_home_state = {
    every_country = {
        every_scope_state = {
            limit = { has_variable = cp_layla_lives_here }
            remove_variable = cp_layla_lives_here
        }
    }
}

# Read her state's cohort
every_scope_state = {
    limit = { has_variable = cp_layla_lives_here }
    # scope here = her region_state; do pop / state reads
}

# Render state name in loc
[Country.MakeScope.Var('cp_layla_state_pointer').GetState.GetStateRegion.GetName]
```
