# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Common People**, a Victoria 3 mod (target version 1.12, forward-compatible with 1.13's National Cast shipping April 28, 2026) built from the [common-people template](https://github.com/common-people). It adds personal, human-scale stories about ordinary citizens of the nations the player governs. The design document is `documentation/the-holy-grail.md`. Characters and their events live in `documentation/characters/<name>/`. The mod code itself lives in `mod/`.

The mod abbreviation is `cp`. All mod-owned identifiers are prefixed `cp_`.

## Reference skill

When editing Paradox script files (`.txt` under `mod/events/` or `mod/common/`, or `.yml` localization under `mod/localization/`), the project-level skill `.claude/skills/victoria3-event/` auto-loads. It contains:

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
- **File naming:** Mod files are prefixed `cp_` (e.g., `cp_layla_events.txt`) to avoid conflicts with other mods and the base game.
- **Global variable pattern:** `cp_is_loaded` is set on game start via `on_actions`, with a corresponding error-suppression event (`cp_error_suppression.0001`). This is a compatibility mechanism for inter-mod detection.
- **Writing style:** Every event text is written as a paragraph of a novel (tone reference: Naguib Mahfouz's *Cairo Trilogy*). Specific, sensory, subtext. Never narration ("you see X") — write what a witness would feel.

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
