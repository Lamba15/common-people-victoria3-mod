---
name: victoria3-event
description: "Verified Victoria 3 modding knowledge for this Common People mod project, currently targeting the 1.13 line -- event syntax, character templates, on_actions, scripted triggers/effects, variables, scopes, traits, localization BOM rules. Load any time the work touches Paradox script -- writing or editing .txt files in mod/events/ or mod/common/, editing .yml localization, reviewing a pull request that touches the mod, debugging an event that isn't firing, answering questions about V3 traits or scope syntax, or planning new event content. Load it even if the user didn't explicitly ask -- guessing V3 syntax silently breaks events, and the online wiki needs JavaScript and often returns empty to fetches. Bundled resources include checklists, the verified 25 personality + 17 condition trait lists, scripts for creating BOM-prefixed localization files, and a pointer to reference.md with verbatim vanilla examples."
paths:
  - mod/**/*.txt
  - mod/**/*.yml
  - mod/**/*.yaml
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch
---

# Victoria 3 Event Skill

You are editing Paradox script for the Victoria 3 1.13 line. Prefer patterns verified in this mod or in the installed 1.13 vanilla files, and keep variable names/data shapes compatible with the r5 person architecture.

## First principles, in order of preference

When you need to figure out how something works in V3 script, try sources in this order -- each is faster and more reliable than the next:

1. **Grep this mod first.** The mod already contains working, verified script (Layla's character template, cp_startup.1, cp_layla.intro, cp_on_start). If you need a pattern similar to something already in the mod, copy that pattern. It's been shaped to the project's conventions and any rough edges have already been filed. Search `mod/events/`, `mod/common/`, and `mod/localization/english/`.
2. **Read reference.md.** Full structured reference with verbatim vanilla examples, the full trait list, the debug workflow, and a table of the common gotchas. Re-read the relevant section before writing anything non-trivial. Don't try to hold the whole reference in your head; load the section you need.
3. **Fetch vanilla from the mirror.** The GitHub mirror [settintotrieste/V3-Vanilla-Extract](https://github.com/settintotrieste/V3-Vanilla-Extract) has the entire `game/` tree of vanilla V3 as text files. WebFetch the raw URL pattern:
   ```
   https://raw.githubusercontent.com/settintotrieste/V3-Vanilla-Extract/main/game/<path>
   ```
   Good starting points: `common/character_templates/country_egy.txt` (the Aisha Taymur template), `common/character_traits/00_traits.txt`, `common/on_actions/00_on_actions.txt`, `events/ig_leaders.txt`, `events/character_events.txt`, `events/agitators_events/`. Quote the relevant block in the response so the user can audit the source.
4. **Avoid the wiki.** `vic3.paradoxwikis.com` requires JavaScript and often returns empty content to WebFetch. Use it only as a last resort, and treat any answer as unverified until a vanilla file confirms it.

## Top gotchas you will hit first

Most V3 script errors in this project come from a handful of recurring mistakes. Pattern-match against these before you debug anything else:

1. **Localization BOM missing.** If an event displays its key (`CP_LAYLA.INTRO.T`) instead of the localized string, the .yml either lacks the UTF-8 BOM or the file uses the wrong header. Verify with `xxd <file> | head -1` -- the first three bytes must be `ef bb bf`. Fix with `scripts/new_loc.sh` (creates new) or by prepending bytes.
2. **Trait prefix.** Vanilla wiki lists traits as `trait_pious`, but script uses the bare name: `pious`. Drop the prefix in `traits = { ... }` blocks and in `has_trait = X` checks.
3. **Scope in a variable.** `set_variable = { name = x value = scope:y }` does not reliably store scope references. If you need to "remember a state or character," use a scripted trigger that computes it fresh, or save the object as a named scope (`save_scope_as = X`) and guard every use with `exists = scope:X`.
4. **Overriding vanilla on_actions.** Writing a vanilla hook such as `on_law_enactment_pass = { effect = { ... } }` at the top level *replaces* that on_action and breaks base-game events. Always subscribe by nesting inside `on_actions = { ... }` (pattern in reference.md §on_actions).
5. **Missing `default_option = yes`.** If no option has this, an event that auto-resolves on timeout has nothing to resolve to and fails silently. Exactly one option per event should be the default.

## Where to read next

[reference.md](reference.md) holds the deep reference -- 14 sections, table of contents, verbatim vanilla examples for every subsystem. Load it when you're about to write or edit a non-trivial event, character template, on_action, or scripted trigger. Sections (skim the ToC in reference.md for line numbers):

- File structure, Paradox script basics
- Character templates (with vanilla Aisha Taymur), `create_character` patterns
- Events (verbatim `ig_leaders.20`), full field reference, `trigger_event`
- on_actions (subscription pattern, verified hook list with scopes)
- Variables (set/change/clamp/remove, boolean shorthand, `has_variable`, timed vars)
- Scopes (save, access, chain, existence check)
- Scripted triggers and effects
- Localization (BOM, format, `\n`, `[scope:X.GetName]` interpolation)
- Full 25 personality + 17 condition trait lists (bare names)
- Debug workflow (launch flag, console, error log paths)
- 10 common gotchas with explanations

## Writing style for this mod specifically

Every event in this project is written as a paragraph of a novel, not a line of game text. Reference for tone: Naguib Mahfouz's *Cairo Trilogy*. Specifics, sensory language, subtext. Avoid narration ("you see X"); write what a witness would feel. The design document in `documentation/the-holy-grail.md` spells out the full philosophy (living characters, monthly life pulse, information flow, game-rule integrity, silent personality drift, Egypt-first). Read or skim it before writing new event content so the tone stays consistent.

## Naming conventions for this mod

- Everything mod-owned is prefixed `cp_` (for Common People). Apply to event namespaces, event IDs, variable names, flag names, scripted triggers, scripted effects, on_actions, localization keys, global variables, GUI windows.
- Characters: `cp_<firstname>` as saved-scope name (e.g. `cp_layla`).
- Variables on a character: `cp_w_<topic>` for personality weights (0-10), `cp_opinion_<TAG>` for per-nation opinions (-100..+100), `cp_<topic>` for general state/flags/counters.
- Event IDs: `cp_<character>.<beat>` (e.g. `cp_layla.intro`) or `cp_<character>_life.<bucket>` for pulse events.
- Files: `cp_<character>_events.txt`, `cp_<topic>_events.txt`.

## Checklist: saving a new event

Before saving, verify each item and fix before moving on. The "why" is included because items usually fail silently -- knowing the symptom helps you catch it in-game faster.

1. **Confirmed `type`** -- usually `country_event`, even for character-focused ones. Vanilla convention: reach the character via saved scope, not root scope. Using `character_event` can work but isn't vanilla's norm and wires scopes differently.
2. **`trigger` guards the saved scope** -- `exists = scope:cp_layla` at minimum. Why: a dead or unspawned character invalidates the scope, and referencing an invalid scope crashes the event silently.
3. **`gui_window` matches portrait count** -- `event_window_1char_tabloid` (one), `event_window_2char_tabloid` (two). Why: a mismatched window leaves empty portrait frames or no portrait at all.
4. **`left_icon` (and `right_icon`) takes a scope** -- `left_icon = scope:cp_layla`. Not `root`, not `this`. Why: portrait slots only resolve scope references correctly when the scope is saved; `root` in a `country_event` is the country, not the character.
5. **`icon`** points to a `.dds` file, typically `"gfx/interface/icons/event_icons/event_default.dds"` until you have custom art.
6. **Every option has a `name`** (localization key) and exactly one option has `default_option = yes`. Why: without a default, auto-resolve on timeout has no fallback.
7. **Localization file has UTF-8 BOM** -- verify with `xxd <file> | head -1`. First three bytes must be `ef bb bf`. Header line: `l_english:`. Entries: ` key:0 "value"` (leading space, colon-zero).
8. **Every localization key exists in the .yml** -- title, desc, flavor, all option names, any custom name keys used by `create_character`. Why: a missing key displays the raw key in-game (e.g. `CP_LAYLA.INTRO.T`), not the text.
9. **Mechanical effects inside options use explicit scope** -- `scope:cp_layla = { set_character_flag = X }`, not bare `set_character_flag = X`. Why: option root in a `country_event` is the country, and bare effects run in that scope.

## Checklist: saving a new on_action hook

1. **Never override base-game on_actions.** Always subscribe via the nesting pattern. Writing `on_law_enactment_pass = { effect = { ... } }` at top level replaces vanilla's entire on_action handler -- every base-game event tied to law enactment stops firing.
   ```
   on_law_enactment_pass = {
       on_actions = {
           cp_on_law_enacted_dispatch
       }
   }
   cp_on_law_enacted_dispatch = {
       effect = { ... }
   }
   ```
2. **Confirm the hook exists in vanilla.** Grep the installed `common/on_actions/00_code_on_actions.txt`, or use `script/audit-common-people.py` which validates subscribed vanilla hook names against the local install.
3. **Know the scope the hook gives you.** `on_law_enactment_pass` -- country scope. `on_diplo_play_war_start` -- diplomatic-play scope; enter `scope:actor` / `scope:target` for countries. `on_monthly_pulse_country` -- country scope. `on_character_death` -- character scope. Using the wrong scope reference inside the effect is a common silent failure.

## Traits quick reference

Drop the `trait_` prefix in `traits = { ... }` blocks and `has_trait = X` checks.

**25 personality traits** (pick 3-4 per character):

`child, direct, persistent, cautious, arrogant, bigoted, reckless, tactful, ambitious, imperious, wrathful, reserved, cruel, meticulous, charismatic, romantic, brave, innovative, hedonist, pious, imposing, honorable, ruthless, compliant, aesthete`

**17 condition traits** (negative/circumstantial; use in context like disease outbreaks, war wounds, etc.):

`alcoholic, opium_addiction, cocaine_addiction, cancer, tuberculosis, grifter, scarred, senile, syphilis, shell_shock, wounded, psychological_affliction, expensive_tastes, kidney_stones, beetle_eared, war_criminal, sickly`

Skill traits (commander/politician/etc.) exist but rarely fit common-people characters. Full list in reference.md §"Skill (partial, commander/politician)".

## Bundled scripts

Under `scripts/` in this skill folder:

- **`scripts/new_loc.sh <relative_path>`** -- create a new .yml localization file with the UTF-8 BOM and `l_english:` header, ready to edit. Use this every time you need a new localization file. It removes the BOM-missing failure mode at source.
- **`scripts/check_boms.sh`** -- verify every .yml under `mod/localization/` starts with the BOM bytes. Run before a commit that touches localization.
- **`scripts/fetch_vanilla.sh <game/relative/path>`** -- WebFetch wrapper for the GitHub vanilla mirror. Prints the file to stdout; redirect to save locally. Saves typing the full raw URL.

Run them from the repository root.

## When this skill is wrong

If vanilla disagrees with something stated here or in `reference.md`, vanilla wins. Update the skill in the same edit. The goal is to never re-derive the same fact twice.
