# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

This is **Common People**, a Victoria 3 mod targeting the 1.13 line (metadata supports `1.13.*`; the installed local game reports `release/1.13.8`, checksum suffix `ce22`; current logs are for 1.13.8 but may predate the latest no-launch mod edits) built from the [common-people template](https://github.com/common-people). It adds personal, human-scale stories about ordinary citizens of the nations the player governs. The design document is `documentation/the-holy-grail.md`. Characters and their events live in `documentation/characters/<name>/`. The mod code itself lives in `mod/`.

The mod abbreviation is `cp`. All mod-owned identifiers are prefixed `cp_`.

Current version: **v0.4.0** — multi-person scaffolding + event-firing budget landed in the r5 refactor, first in-game test passed. Layla is Person 1 of N. Adding new persons is purely additive. See `documentation/audit-v0.3.md` for the pre-test audit snapshot and known limitations (dated; v0.3 filename retained as a historical marker).

## Architecture (r5)

The mod is designed around **persons** — narrative objects owned by the mod, not V3 `character` entities. Each person is a cluster of country variables with the name token baked into every identifier.

**Three reference documents are the ground truth — read them before editing:**

- `documentation/characters/_shared/registry.md` — how a person joins the mod, what variables they own, how they die.
- `documentation/characters/_shared/firing.md` — the five-tier event firing protocol and the 1–2 routine automatic events/year target with a hard cap of two.
- `documentation/characters/_shared/adding-a-new-person.md` — mechanical 7-step recipe with copy-paste templates for Person 2/3/N. **This is the most important file in the repo when onboarding a new character.**

### File prefix rule

Every file under `mod/common/` and `mod/events/` classifies cleanly as one of:

- `cp_shared_*` — cross-person infrastructure (registry, firing gatekeepers, parameterised primitives, monthly router).
- `cp_<name>_*` — a single person's events, memory, sensors, buttons, custom_loc, JE, loc (e.g. `cp_layla_*`).
- `cp_debug_*` — console-fireable probes.
- `cp_on_actions.txt` — the thin dispatcher router.

**When adding Person 2, do not edit any `cp_layla_*` file.** The only shared files that gain new content are `cp_shared_startup_events.txt` (one `cp_register_person` call), `cp_shared_firing.txt` (one branch in `cp_roll_for_event`), and `cp_on_actions.txt` (one guarded `if`-block per hook). Everything else is new `cp_<name>_*` files.

### Variable naming

Every person-specific variable carries the name token: `cp_<name>_<attr>`. Examples: `cp_layla_hope`, `cp_layla_sol`, `cp_layla_seen_homesteading`, `cp_layla_w_revolution`, `cp_layla_profession_peasants`, `cp_layla_ahmed_alive` (household-furniture prefixed by owner). Never use an unprefixed `cp_<attr>` — that's a pre-r5 pattern and will fail the rename audit.

Globals (cross-person): `cp_person_<name>_alive`, `cp_person_<name>_country`, `cp_global_ambient_cooldown`, `cp_person_<name>_ambient_cooldown`, `cp_is_loaded`.

### Firing gatekeepers

Every `trigger_event` in shared code or buttons flows through one of five gatekeepers in `cp_shared_firing.txt`:

- `cp_try_fire_ambient` — small life beats. Gated by 183-day global cooldown + 365-day per-person cooldown. Target: **1–2 routine automatic fires per in-game year across all persons combined, with a hard cap of two.**
- `cp_try_fire_law_reaction` — law-reform beats. Uses the same 183-day global + 365-day per-person cooldown lane so rapid law passing cannot flood the player. Per-event seen-flag enforces one-shot.
- `cp_try_fire_world_response` — routine technology, building, conditional-entry, and noncritical yearly state beats. Uses the same shared cooldown lane.
- `cp_try_fire_milestone` — bypasses budget. Death, Cairo offer, suitor, first welfare, revolution.
- `cp_button_fire` — player-initiated; always fires (player click is a promise). Per-event seen-flags still apply.

Raw `trigger_event` inside an event's `immediate` or option block is allowed for chained follow-ups (the next scene in the same beat) — not for dispatcher-initiated fires.

## Reference skill

When editing Paradox script files (`.txt` under `mod/events/` or `mod/common/`, or `.yml` localization under `mod/localization/`), the project-level skill `.Codex/skills/victoria3-event/` auto-loads. It contains:

- `SKILL.md` — fast reference: conventions, checklists, quick trait list
- `reference.md` — deep reference: verbatim vanilla examples for events, templates, on_actions, variables, scopes, localization; full 25 personality + 17 condition trait lists; debug workflow; common gotchas

Always consult the skill's `reference.md` before inventing V3 syntax. The vanilla source of truth is the GitHub mirror `settintotrieste/V3-Vanilla-Extract`; WebFetch the relevant raw file when unsure.

## Repository Structure

- **`mod/`** — The actual mod directory (this is what gets symlinked into the game's mod folder and uploaded to Steam Workshop)
  - `common/` — Game data definitions (buildings, laws, ideologies, interest groups, on_actions, etc.)
  - `events/` — Event scripts
  - `gfx/` — Game graphics (DDS textures)
  - `gui/` — UI layout files
  - `localization/english/` — Localization YAML files (`l_english` header). Subdirectory `replace/` overrides base game strings.
  - `.metadata/metadata.json` — Mod metadata (name, id, version, tags, supported game version)
- **`image/`** — Source artwork (GIMP `.xcf` files) and icon templates; not shipped with the mod
- **`documentation/`** — Project documentation and guides; not shipped with the mod
- **`script/`** — Automation scripts (bash)

## Key Conventions

- **Paradox script syntax:** Files in `mod/common/` and `mod/events/` use Paradox's declarative scripting format (block-based with `=`, `{ }`, indentation by tabs). This is NOT JSON, YAML, or any standard format.
- **Localization files** must start with a BOM (`\xEF\xBB\xBF`) and use the header format `l_english:` (or other language code). Entries are `key:0 "value"` format. Verify with `xxd <file> | head -1` — first three bytes must be `ef bb bf`.
- **File naming:** Mod files are prefixed `cp_` (e.g., `cp_layla_events.txt`) to avoid conflicts with other mods and the base game. Per-person files add the name token: `cp_<name>_*`.
- **Global variable pattern:** `cp_is_loaded` is set on game start via `on_actions`, with a corresponding error-suppression event (`cp_error_suppression.0001`). This is a compatibility mechanism for inter-mod detection.
- **V3 macro substitution is load-time, not runtime.** `$param$` is substituted when a scripted effect is parsed, so `cp_$person$_hope` becomes literal `cp_layla_hope` at each callsite. This means `cu:$culture$`, `rel:$religion$`, `c:$country$` do not work at runtime — use per-person wrappers that bake the literals in (see `cp_layla_refresh_sol` in `cp_layla_memory.txt` for the pattern).
- **V3 rejects scripted_effects with unused macro parameters.** If a scripted_effect's callsites pass `person = layla` but the effect body never references `$person$`, V3 silently rejects compilation — every call becomes a no-op. Either reference every declared param in the body (e.g. `limit = { has_variable = cp_$person$_alive }` satisfies the check while adding a sanity gate) or strip the unused param from the callsite.
- **Routine event budget.** The mod targets 1–2 routine automatic events per in-game year across all persons, with a hard cap of two. Ambient, first-contact, law-reaction, and world-response events share the same visible-story cooldown lane. Milestones add 0–1 only when a critical life/world state demands it. Do not write new event sources that bypass this — use the five gatekeepers.
- **Writing style:** Every event text is written as a paragraph of a novel (tone reference: Naguib Mahfouz's *Cairo Trilogy*). Specific, sensory, subtext. Never narration ("you see X") — write what a witness would feel.
- **No dead code in-tree.** When a system is replaced, do not leave the old files sitting with a "retired" header comment. Two acceptable paths: either **salvage** the old content (port the good prose, route the unused images, lift the reusable effects) into the new system, or **delete** the old files in the same commit as the new system. Never both retired-and-kept — orphaned files confuse future work, complicate bug-hunts, and rot. If a short grace period is genuinely needed for playtest comparison, that is an explicit TODO with an expiry, not a permanent condition.

## Useful Scripts

### Generate localization for all languages
```bash
cd script/
./generate-localization.sh [base_language] [path_to_mod/]
```
Copies English localization to all other languages listed in `script/languages.txt` (braz_por, french, japanese, polish, russian, turkish), replacing the language header accordingly.

### Initialize mod template (GitHub Actions)
Run the "Initialize Mod Template" workflow from the Actions tab. It replaces `ABBREVIATION_PLACEHOLDER` and `MODNAME_PLACEHOLDER` throughout the repo and updates `metadata.json`. Alternatively, do this manually with find/sed.

## Git Notes

- `.gitattributes` marks all files as binary — this avoids line-ending normalization issues with Paradox game files and DDS textures. Be aware that `git diff` won't show text diffs by default.
