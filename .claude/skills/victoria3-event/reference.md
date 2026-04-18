# Victoria 3 Modding Reference (v1.12, verified against vanilla)

This is the deep reference. Every pattern here has been verified against vanilla game files (via the `settintotrieste/V3-Vanilla-Extract` GitHub mirror) rather than inferred from the wiki. When you find a disagreement with vanilla, trust vanilla and update this file.

## Table of Contents

1. [Authoritative sources](#authoritative-sources)
2. [File structure](#file-structure)
3. [Paradox script basics](#paradox-script-basics)
4. [Character templates](#character-templates)
5. [create_character in events](#create_character-in-events)
6. [Events](#events)
7. [on_actions](#on_actions)
8. [Variables](#variables)
9. [Scopes](#scopes)
10. [Scripted triggers and effects](#scripted-triggers-and-effects)
11. [Localization](#localization)
12. [Traits (full list)](#traits-full-list)
13. [Debug workflow](#debug-workflow)
14. [Common gotchas](#common-gotchas)

---

## Authoritative sources

- **GitHub mirror of vanilla**: https://github.com/settintotrieste/V3-Vanilla-Extract (browse the `game/` tree)
- **Raw vanilla file URL pattern**: `https://raw.githubusercontent.com/settintotrieste/V3-Vanilla-Extract/main/game/<path>`
- **Wiki** (JS-heavy, unreliable for agents): https://vic3.paradoxwikis.com
- **Paradox forum dev diaries** (good for 1.12 / 1.13 context): search "Victoria 3 Dev Diary #<N>" on paradoxplaza.com

When unsure, WebFetch the raw vanilla URL first.

## File structure

```
mod/
├── .metadata/metadata.json     # required; name, id, version, supported_game_version
├── thumbnail.png               # optional but launcher-friendly
├── common/
│   ├── character_templates/    # templates instantiated by events
│   ├── character_traits/       # custom traits (rare; usually reuse vanilla)
│   ├── on_actions/             # subscriptions to game hooks
│   ├── scripted_triggers/      # reusable boolean conditions
│   ├── scripted_effects/       # reusable actions
│   └── journal_entries/        # persistent UI narrative trackers
├── events/                     # country/state/character events
├── localization/english/       # l_english:-headed .yml files with UTF-8 BOM
│   └── replace/                # files that override base-game localization
├── gfx/                        # .dds textures, event icons
└── gui/                        # .gui window definitions (rarely touched)
```

All text files use LF line endings. `.gitattributes` in this repo marks files as binary to avoid line-ending churn across platforms.

## Paradox script basics

- **Assignment**: `key = value`. No colons, no semicolons.
- **Blocks**: `{ }`. Indentation is stylistic (vanilla uses tabs).
- **Comments**: `# to end of line`.
- **Booleans**: `yes` / `no` (not `true` / `false`).
- **Numbers**: bare (`42`, `0.5`). No quotes unless string.
- **Strings**: quoted only when they contain spaces or special chars.
- **References**: typed prefixes:
  - `c:EGY` country, `s:STATE_LOWER_EGYPT` state, `cu:misri` culture, `rel:sunni` religion
  - `ig:ig_rural_folk` interest group, `law_type:law_serfdom` law
  - `scope:<name>` previously saved scope

## Character templates

Templates DEFINE characters; events INSTANTIATE them. Put templates in `common/character_templates/<file>.txt`.

### Verbatim vanilla example

From `game/common/character_templates/country_egy.txt` -- a 22-year-old Egyptian woman, the closest real-world parallel to Layla:

```
egy_aisha_taymur = {
    first_name = "Aisha"
    last_name = "Taymur"
    historical = yes
    female = yes
    birth_date = 1840.1.6
    culture = cu:misri
    religion = rel:sunni
    interest_group = ig_intelligentsia
    ideology = ideology_feminist
    traits = {
        persistent
        tactful
        aesthete
        literary
    }
    agitator_usage = {
        country_trigger = { c:EGY ?= this }
        interest_group_trigger = { is_interest_group_type = ig_intelligentsia }
        earliest_usage_date = 1885.1.1
        latest_usage_date = 1895.1.1
        chance = 50
    }
}
```

### Fields

- `first_name`, `last_name`: string literals OR localization keys (if the key exists in an .yml file, the game uses the localized value).
- `historical`: `yes` if this is a known historical figure; affects trait generation.
- `female`: `yes` for women. Omit for men (vanilla convention).
- `culture`, `religion`: use the `cu:` / `rel:` prefixes.
- `birth_date` OR `age`: pick one. `age = 47` is an integer; `birth_date = 1814.1.1` is yyyy.m.d.
- `interest_group`: bare IG id. Omit for unaffiliated characters.
- `ideology`: bare ideology id. Optional.
- `traits`: brace-delimited list of bare trait names. See [Traits](#traits-full-list).
- `dna`: portrait DNA string (from in-game `portrait_editor` console command). Locks her face; omit to let the game roll.
- `commander_rank`, `ruler`, `heir`, `ig_leader`, `is_general`, `is_admiral`, `is_agitator`: role flags for template-based spawns.
- `hq`: strategic region for commanders.
- `on_created`: an effect block that runs when this template is instantiated.
- `agitator_usage` / `executive_usage`: control automatic spawning. Omit if you want manual-only spawns.

## create_character in events

Two idiomatic patterns.

### Pattern A: instantiate a template (preferred)

```
create_character = {
    template = cp_layla
    on_created = {
        save_scope_as = cp_layla
        set_variable = { name = cp_hope value = 5 }
    }
}
```

The `on_created` block runs in the new character's scope. Use it to save the scope and set all variables in one place.

### Pattern B: inline creation (when a template doesn't exist)

```
create_character = {
    first_name = cp_name_layla
    last_name = cp_name_alsharif
    female = yes
    culture = cu:misri
    religion = rel:sunni
    birth_date = 1814.1.1
    traits = { persistent pious reserved compliant }
    save_scope_as = cp_layla
}
```

Inline is fine, but the template pattern is cleaner for characters instantiated from multiple events or re-used later.

### The country the character belongs to

`create_character` runs in a country scope and the character is attached to that country. Run the effect from a `country_event` and the character becomes a member of that country.

## Events

### Types

- `country_event` (root is a country)
- `state_event` (root is a state)
- `character_event` (root is a character)

Vanilla's convention, even for character-focused events, is `country_event` with the character reached via saved scope. Follow this.

### Verbatim vanilla example

From `game/events/ig_leaders.txt` (lightly truncated):

```
ig_leaders.20 = {
    type = country_event
    placement = ROOT

    title = ig_leaders.20.t
    desc = ig_leaders.20.d
    flavor = ig_leaders.20.f

    gui_window = event_window_1char_tabloid
    left_icon = scope:reckless_ig.leader

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    on_opened_soundeffect = "event:/SFX/Events/misc/1Character_Banner"

    icon = "gfx/interface/icons/event_icons/event_default.dds"

    duration = 3
    cooldown = { days = stupidly_long_modifier_time }

    trigger = {
        has_ruling_interest_group_count >= 2
        any_interest_group = {
            is_in_government = yes
            leader ?= { has_trait = reckless }
        }
        NOT = { has_variable = the_gamble_var }
    }

    immediate = {
        random_interest_group = {
            limit = {
                is_in_government = yes
                leader = { has_trait = reckless }
            }
            save_scope_as = reckless_ig
            leader = { save_scope_as = reckless_leader }
        }
        set_variable = { name = the_gamble_var days = normal_modifier_time }
    }

    option = {
        name = ig_leaders.20.a
        random_list = {
            50 = { trigger_event = { id = ig_leaders.1 days = 10 } }
            50 = { trigger_event = { id = ig_leaders.2 days = 10 } }
        }
    }

    option = {
        name = ig_leaders.20.b
        default_option = yes
        scope:reckless_leader = {
            add_modifier = { name = gamble_denied_modifier days = normal_modifier_time }
        }
    }
}
```

### Field reference

- `type`: one of the three types above.
- `placement`: where the event's 3D marker appears. `ROOT`, `scope:<saved>`, or a state. Optional.
- `title`, `desc`, `flavor`: localization keys. `flavor` is the italic italics subtitle shown below the description.
- `gui_window`: event window template. Common values:
  - `event_window_1char_tabloid` -- single-character tabloid
  - `event_window_2char_tabloid` -- two-character
  - `event_window_background_only` -- no portraits
- `left_icon`, `right_icon`, `center_icon`: portrait slots. Accept scope references (e.g. `scope:cp_layla`).
- `icon`: path to a `.dds` texture used as the event's card icon.
- `duration`: how long the event stays visible in the queue (game days).
- `cooldown`: minimum time between re-fires. `{ days = N }` or a named define like `normal_modifier_time` / `stupidly_long_modifier_time`.
- `hidden = yes`: fires silently, no UI, no player interaction. Use for dispatch/routing events.
- `orphan = yes`: silences "unused event" errors for events triggered only from code paths the validator can't see.
- `trigger`: conditions that must be true for the event to be eligible when triggered.
- `immediate`: effects that run *before* the player sees the event (useful for saving scopes).
- `option`: at least one; player choice. Each option has `name = <loc_key>` and an effect body. Exactly one option should have `default_option = yes` (used when the event auto-resolves on timeout).
- `on_created_soundeffect`, `on_opened_soundeffect`: audio hooks.

### trigger_event

```
trigger_event = { id = cp_layla.intro days = 1 }
```

- `id`: namespaced event id.
- `days`, `months`, `years`: optional delay.

## on_actions

Custom dispatch: subscribe to a vanilla hook by nesting a custom action inside it.

```
# common/on_actions/cp_on_actions.txt
on_law_enacted = {
    on_actions = {
        cp_on_law_enacted_dispatch
    }
}

cp_on_law_enacted_dispatch = {
    effect = {
        if = {
            limit = { has_law = law_type:law_homesteading }
            c:EGY ?= {
                trigger_event = { id = cp_layla.homesteading }
            }
        }
    }
}
```

### Common hooks (verified)

Country-scope:
- `on_game_started`
- `on_monthly_pulse_country`
- `on_yearly_pulse_country`
- `on_law_enacted`
- `on_war_started`, `on_war_ended`
- `on_revolution_start`, `on_revolution_end`
- `on_election_campaign_start`, `on_election_campaign_end`
- `on_diplomatic_play_started`, `on_diplomatic_play_ended`

State-scope:
- `on_monthly_pulse_state`, `on_yearly_pulse_state`

Character-scope:
- `on_character_death` (scope is the character who died)
- `on_ruler_change`

Battle/war:
- `on_battle_won`, `on_battle_lost`

When unsure about a hook name or scope, grep vanilla `game/common/on_actions/00_on_actions.txt`.

### Never override vanilla

Don't write `on_law_enacted = { effect = { ... } }` at top level -- that replaces the vanilla one. Always nest via the `on_actions = { ... }` subscription pattern so every subscriber runs.

## Variables

Stored on any scoped object (country, state, pop, character, even global).

### Effects

```
# Numeric set
set_variable = { name = cp_hope value = 5 }

# Boolean-style flag (no value = effectively "exists")
set_variable = cp_layla_seeded

# Arithmetic change
change_variable = { name = cp_hope add = 1 }        # also: subtract, multiply, divide, modulo, min, max

# Clamp to range
clamp_variable = { name = cp_hope min = 0 max = 10 }

# Remove
remove_variable = cp_hope

# Timed variable (auto-expires after duration)
set_variable = { name = cp_shock_var days = 30 }
```

### Triggers

```
has_variable = cp_hope              # variable exists on this scope

# Comparison (requires block form)
scope:cp_layla = {
    var:cp_hope >= 7
}
```

### What variables can hold

- Integers and floats: yes
- Boolean-like "exists" flags: yes (set_variable without a value)
- Scope references: **not reliably.** If you need to "remember a state," prefer:
  - A scripted trigger that computes it fresh each time, OR
  - Storing the state by convention (character is always in `s:STATE_LOWER_EGYPT` until a specific event moves them), OR
  - Saving the state as a named scope on game start (but saved scopes have their own lifecycle concerns).

### Global variables

```
set_global_variable = { name = cp_is_loaded value = yes }
has_global_variable = cp_is_loaded
global_var:cp_is_loaded
```

Use for inter-mod detection and game-wide counters.

## Scopes

Scopes are the "current object." Scope changes with nesting.

### Saving a scope

```
save_scope_as = cp_layla
```

Saves the current scope under a name. Accessible anywhere afterward as `scope:cp_layla`.

### Accessing saved scopes

```
scope:cp_layla = { ... }
scope:cp_layla.leader             # property-chain access
```

### Scope change keywords

- `root` -- the event's root scope (type-defined)
- `this` (or `THIS`) -- the current scope
- `prev` -- the scope just before the current block

### Existence check

```
trigger = {
    exists = scope:cp_layla
}
```

Skips the event silently if the scope isn't valid (e.g. character died). Use in every event that references a saved character.

## Scripted triggers and effects

Reusable condition and action blocks.

### Trigger file

```
# common/scripted_triggers/cp_triggers.txt
cp_hears_foreign_news = {
    OR = {
        scope:cp_layla = { has_character_flag = cousin_in_alexandria }
        AND = {
            scope:cp_layla = { var:cp_literate = 1 }
            has_law = law_type:law_free_press
        }
    }
}
```

Use in any event's `trigger` block: `cp_hears_foreign_news = yes`.

### Effect file

```
# common/scripted_effects/cp_effects.txt
cp_increase_hope = {
    scope:cp_layla = {
        change_variable = { name = cp_hope add = 1 }
        clamp_variable = { name = cp_hope min = 0 max = 10 }
    }
}
```

Invoke: `cp_increase_hope = yes` inside any effect block.

## Localization

### File requirements

- **UTF-8 with BOM.** The first three bytes MUST be `EF BB BF`. Verify with `xxd <file> | head -1`.
- **Filename ends with `_l_<language>.yml`**: e.g. `cp_layla_l_english.yml`. Lowercase "L", not numeral "1".
- **First line**: `l_english:` (or `l_french:`, etc.).
- **Entries**: indented one space, format `key:0 "value"`:

```
l_english:
 cp_layla.intro.t:0 "The Farmer's Daughter"
 cp_layla.intro.d:0 "The call to fajr comes before the light does..."
 cp_layla.intro.a:0 "Watch her."
```

### String features

- `\n` inside double-quoted strings produces a line break.
- `[root.GetName]` embeds the current root scope's localized name. Other scopes: `[scope:cp_layla.GetName]`.
- `§R...§!` colors text red, `§Y...§!` yellow, etc.
- `$var$` substitutes variable values (context-dependent).

### Common error: missing localization

If an event shows `CP_LAYLA.INTRO.T` as the title in-game instead of the real string, the localization key is missing or the file doesn't have the BOM. Fix with `xxd <file> | head -1`; re-prepend `EF BB BF` if missing.

## Traits (full list)

Trait names are used bare in `traits = { }` blocks and `has_trait = X` checks. **Do not include the `trait_` prefix**, even though the wiki lists traits with that prefix.

### Personality (25)

Pick 3-4 per character. These are pure-flavor in most cases, though the game uses them to influence AI and a few specific mechanics.

```
child, direct, persistent, cautious, arrogant, bigoted, reckless,
tactful, ambitious, imperious, wrathful, reserved, cruel, meticulous,
charismatic, romantic, brave, innovative, hedonist, pious, imposing,
honorable, ruthless, compliant, aesthete
```

### Condition (17)

Negative/circumstantial. Use sparingly and in context (disease outbreak, war wound, etc.).

```
alcoholic, opium_addiction, cocaine_addiction, cancer, tuberculosis,
grifter, scarred, senile, syphilis, shell_shock, wounded,
psychological_affliction, expensive_tastes, kidney_stones, beetle_eared,
war_criminal, sickly
```

### Skill (partial, commander/politician)

Most don't fit common people. Listed for completeness:

Commander: `supply_requisitions_expert, pillager, surveyor, woodland_combat_expert, open_terrain_commander, mountain_combat_expert, artillery_commander` (and `_experienced` / `_expert` variants), `stalwart_defender, trench_rat, defense_in_depth_specialist, offensive_planner, defensive_strategist, naval_commander, convoy_raider, dockyard_organizer, traditionalist_commander, popular_commander, celebrity_commander`

Politician: `diplomat, colonial_administrator, political_operator, inspirational_orator, demagogue, firebrand`

Other: `explorer, bandit, social_bandit, erudite, literary, engineer, master_bureaucrat, political_appointee, inept, inexperienced, elder, basic_entrepreneur`

### Modifying traits in events

```
scope:cp_layla = {
    add_trait = wounded
    remove_trait = persistent
}
```

Characters can have multiple traits. No hard limit documented.

## Debug workflow

### Enable debug mode

- **Steam launch options** (right-click Victoria 3 in Steam -> Properties -> Launch Options): `-debug_mode`
- **Paradox launcher**: Game Settings -> toggle Debug Mode.

### Console (in-game)

- **Open**: tilde key (`~`). On some Linux keyboards: `Shift+2` or `Alt+2+1`.
- **Fire an event**: `event cp_layla.intro EGY` (event id, then country tag).
- **Test without effects**: `testevent cp_layla.intro EGY`.
- **Speed time**: `time_speed 5` (max).
- **Force law**: `set_law law_homesteading EGY`.
- **Print debug**: `print.eventdebug`.

### Error logs

On Linux:
```
~/.local/share/Paradox Interactive/Victoria 3/logs/error.log
~/.local/share/Paradox Interactive/Victoria 3/logs/debug.log
```

Tail in real time:
```bash
tail -f ~/.local/share/Paradox\ Interactive/Victoria\ 3/logs/error.log
```

### Hot reload

In debug mode, the game's file watcher auto-reloads changed `.yml` and most `.txt` files without restart. Heavy structural changes (new on_actions, new character_templates) may require a return to main menu.

### Make saves human-readable

Edit `~/.local/share/Paradox Interactive/Victoria 3/pdx_settings.json` and set:
```json
"save_file_format": "text"
```

Saves become zip archives containing plaintext `gamestate` and `meta` files -- grep them to confirm variables persist.

## Common gotchas

1. **`trait_` prefix** -- wiki lists traits as `trait_pious`; vanilla script uses `pious`. Drop the prefix.
2. **`save_scope_as` scope lifetime** -- saved scopes survive save/reload *if the referenced object survives*. A dead character invalidates the scope; always `exists = scope:X` guard.
3. **Scope in a variable** -- `set_variable = { name = x value = scope:y }` does not work. Use scripted triggers or conventions instead.
4. **Localization key misspelling** -- if your event shows the raw key (e.g. `CP_LAYLA.INTRO.T`) in-game, either the key is missing from the `.yml` or the BOM is missing from the file. Check `xxd <file> | head -1` for `EF BB BF`.
5. **`gui_window` name** -- must be an existing window in `gui/eventwindow.gui`. Typos fail silently (no portrait shown).
6. **`default_option = yes`** -- exactly one option per event must have it; otherwise the event can't auto-resolve on timeout.
7. **`on_character_death` cleanup** -- if you rely on a saved scope (`scope:cp_layla`) in other events, always guard them with `exists = scope:cp_layla` so her death doesn't crash subsequent events.
8. **`every_country` with `limit`** -- works but is slower than direct `c:EGY ?= { ... }`. Use the direct form when you know the target country.
9. **`?= ` vs `= `** -- `?=` is optional assignment (doesn't error if the scope is missing). Use `?=` when accessing country tags that may not exist in the current playthrough.
10. **`should_popup_when_expiring = no`** (1.12 feature) -- use for hidden-ish events that should silently time out with the default option rather than forcing a popup.
