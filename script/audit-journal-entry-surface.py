#!/usr/bin/env python3
"""Audit Common People's journal-entry surface.

The shipped persistent journal UI is roster-level, not Layla-owned. Version 0
cleanup means there is no save-migration Layla JE shell: new games and test
games should see only cp_je_common_people plus one shared action button per
registered person. Character buttons are still declared statically, but their
visibility must be gated to the active three-person roster.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMON = ROOT / "mod" / "common"
EVENTS = ROOT / "mod" / "events"
LOCALIZATION = ROOT / "mod" / "localization"

JE_DIR = COMMON / "journal_entries"
BUTTON_DIR = COMMON / "scripted_buttons"

JE_DEF_RE = re.compile(r"^\s*(cp_je_[A-Za-z0-9_]+)\s*=", re.MULTILINE)
ADD_JE_RE = re.compile(r"add_journal_entry\s*=\s*\{[^{}]*\btype\s*=\s*(cp_je_[A-Za-z0-9_]+)", re.DOTALL)
SCRIPTED_BUTTON_RE = re.compile(r"scripted_button\s*=\s*(cp_[A-Za-z0-9_]+)")
REGISTER_PERSON_RE = re.compile(r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)", re.DOTALL)
BUTTON_DEF_RE = re.compile(r"^\s*(cp_shared_action_([A-Za-z0-9_]+)_button)\s*=", re.MULTILINE)
ACTION_EFFECT_DEF_RE = re.compile(r"^\s*(cp_shared_action_([A-Za-z0-9_]+))\s*=", re.MULTILINE)
ACTION_TRIGGER_DEF_RE = re.compile(r"^\s*(cp_shared_action_([A-Za-z0-9_]+)_available)\s*=", re.MULTILINE)
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+", re.MULTILINE)
MARK_EVENT_SEEN_RE = re.compile(
    r"cp_mark_event_seen\s*=\s*\{[^{}]*?\bperson\s*=\s*([A-Za-z0-9_]+)"
    r"[^{}]*?\bid\s*=\s*([A-Za-z0-9_]+)",
    re.DOTALL,
)
CURRENT_LOC_KEY_RE = re.compile(r"localization_key\s*=\s*(cp_roster_[A-Za-z0-9_]+_current_[A-Za-z0-9_]+)")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def uncommented(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def script_files() -> list[Path]:
    return sorted(COMMON.glob("**/cp_*.txt")) + sorted(EVENTS.glob("cp_*.txt"))


def registered_persons() -> list[str]:
    text = "\n".join(uncommented(read(path)) for path in script_files())
    return sorted(set(REGISTER_PERSON_RE.findall(text)))


def localization_keys() -> set[str]:
    keys: set[str] = set()
    for path in sorted(LOCALIZATION.glob("**/*.yml")):
        keys.update(LOC_KEY_RE.findall(read(path)))
    return keys


def extract_named_block(text: str, name: str) -> str:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*\{{", text, re.MULTILINE)
    if not match:
        return ""

    start = match.end() - 1
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return text[start:]


def seen_history_ids_by_person() -> dict[str, set[str]]:
    marks: dict[str, set[str]] = {}
    text = "\n".join(uncommented(read(path)) for path in script_files())
    for person, seen_id in MARK_EVENT_SEEN_RE.findall(text):
        if seen_id == "intro":
            continue
        marks.setdefault(person, set()).add(seen_id)
    return marks


def main() -> int:
    failures: list[str] = []

    je_defs: dict[str, Path] = {}
    for path in sorted(JE_DIR.glob("cp_*.txt")):
        text = read(path)
        for match in JE_DEF_RE.finditer(text):
            je_defs[match.group(1)] = path

        for button in SCRIPTED_BUTTON_RE.findall(text):
            if button.startswith("cp_layla_"):
                failures.append(f"{rel(path)} still exposes person-owned journal button {button}")

    if "cp_je_common_people" not in je_defs:
        failures.append("cp_je_common_people is not defined")

    allowed_defs = {"cp_je_common_people"}
    unexpected = sorted(set(je_defs) - allowed_defs)
    for je in unexpected:
        failures.append(f"unexpected person/special journal entry remains defined: {je} in {rel(je_defs[je])}")

    active_adds: list[tuple[str, Path]] = []
    for root in (EVENTS, COMMON):
        for path in sorted(root.rglob("cp_*.txt")):
            text = read(path)
            for match in ADD_JE_RE.finditer(text):
                active_adds.append((match.group(1), path))

    for je, path in active_adds:
        if je != "cp_je_common_people":
            failures.append(f"{rel(path)} adds {je}; new games must only add cp_je_common_people")

    layla_button_file = BUTTON_DIR / "cp_layla_buttons.txt"
    if layla_button_file.exists():
        failures.append(f"{rel(layla_button_file)} still exists; Layla journal buttons should not ship")

    retired_files = [
        COMMON / "journal_entries" / "cp_layla_journal_entries.txt",
        COMMON / "customizable_localization" / "cp_layla_custom_loc.txt",
        COMMON / "scripted_progress_bars" / "cp_scripted_progress_bars.txt",
    ]
    for path in retired_files:
        if path.exists():
            failures.append(f"{rel(path)} still exists; retired Layla dashboard surface should be deleted")

    roster = registered_persons()
    je_text = read(JE_DIR / "cp_shared_journal_entries.txt") if (JE_DIR / "cp_shared_journal_entries.txt").exists() else ""
    button_text = read(BUTTON_DIR / "cp_shared_buttons.txt") if (BUTTON_DIR / "cp_shared_buttons.txt").exists() else ""
    effect_path = COMMON / "scripted_effects" / "cp_shared_action_buttons.txt"
    trigger_path = COMMON / "scripted_triggers" / "cp_shared_action_buttons.txt"
    sensor_path = COMMON / "scripted_triggers" / "cp_shared_sensors.txt"
    active_roster_path = COMMON / "scripted_effects" / "cp_shared_active_roster.txt"
    custom_loc_path = COMMON / "customizable_localization" / "cp_shared_custom_loc.txt"
    effect_text = read(effect_path) if effect_path.exists() else ""
    trigger_text = read(trigger_path) if trigger_path.exists() else ""
    sensor_text = read(sensor_path) if sensor_path.exists() else ""
    active_roster_text = read(active_roster_path) if active_roster_path.exists() else ""
    custom_loc_text = read(custom_loc_path) if custom_loc_path.exists() else ""
    locs = localization_keys()

    button_defs = {match.group(2): match.group(1) for match in BUTTON_DEF_RE.finditer(button_text)}
    effect_defs = {match.group(2): match.group(1) for match in ACTION_EFFECT_DEF_RE.finditer(effect_text)}
    trigger_defs = {match.group(2): match.group(1) for match in ACTION_TRIGGER_DEF_RE.finditer(trigger_text)}

    if "cp_shared_roster_" in je_text:
        failures.append("cp_je_common_people still exposes roster page selector buttons")
    if "cp_common_people_roster_page" in je_text:
        failures.append("cp_je_common_people still branches on the retired roster page variable")
    if "cp_common_people_roster_page" in button_text:
        failures.append("shared buttons still branch on the retired roster page variable")
    if "cp_active_roster_has_any_person" not in sensor_text:
        failures.append("missing cp_active_roster_has_any_person; JE empty-state checks must use valid active slots")
    if "var:cp_$person$_active_slot <= 3" not in sensor_text:
        failures.append("cp_active_roster_has_person must reject slots above the three visible JE slots")
    if "cp_active_roster_has_slot" not in sensor_text:
        failures.append("missing cp_active_roster_has_slot; active roster compaction needs target-slot guards")
    if "cp_clear_all_active_people" not in active_roster_text:
        failures.append("missing active-roster clear effect for v0 cleanup/test reset")
    if "cp_compact_active_roster" not in active_roster_text:
        failures.append("missing active-roster compaction; cleared/dead people should not leave blank JE slots")
    if "cp_compact_active_roster = yes" not in active_roster_text:
        failures.append("cp_refresh_active_roster does not compact slots after clearing invalid/dead people")
    if "cp_active_roster_v0_cleaned" not in "\n".join(read(path) for path in sorted(EVENTS.glob("cp_*.txt"))):
        failures.append("startup does not run the one-time v0 active-roster cleanup")

    for person in roster:
        button = f"cp_shared_action_{person}_button"
        effect = f"cp_shared_action_{person}"
        trigger = f"cp_shared_action_{person}_available"
        if person not in button_defs:
            failures.append(f"missing shared action scripted button for {person}: {button}")
        if f"scripted_button = {button}" not in je_text:
            failures.append(f"cp_je_common_people does not expose {button}")
        if f"cp_active_roster_has_person = {{ person = {person} }}" not in button_text:
            failures.append(f"{button} is not visibility-gated by active roster membership")
        if person not in effect_defs:
            failures.append(f"missing shared action effect for {person}: {effect}")
        if person not in trigger_defs:
            failures.append(f"missing shared action availability trigger for {person}: {trigger}")
        if f"{button}_name" not in locs:
            failures.append(f"missing localization key {button}_name")
        if f"{button}_desc" not in locs:
            failures.append(f"missing localization key {button}_desc")

    seen_by_person = seen_history_ids_by_person()
    for person in roster:
        if person == "layla":
            continue
        current_block_name = f"cp_roster_{person}_current"
        current_block = extract_named_block(custom_loc_text, current_block_name)
        if not current_block:
            failures.append(f"missing shared JE current-life custom localization block: {current_block_name}")
            continue

        for seen_id in sorted(seen_by_person.get(person, set())):
            seen_flag = f"cp_{person}_seen_{seen_id}"
            if seen_flag not in current_block:
                failures.append(f"{current_block_name} does not react to visible history flag {seen_flag}")

        for loc_key in CURRENT_LOC_KEY_RE.findall(current_block):
            if loc_key not in locs:
                failures.append(f"{current_block_name} references missing localization key {loc_key}")

    for path in script_files():
        text = uncommented(read(path))
        if "cp_layla_life_bar" in text:
            failures.append(f"{rel(path)} still references cp_layla_life_bar")
        if "cp_layla_button_cooldown" in text:
            failures.append(f"{rel(path)} still references retired cp_layla_button_cooldown")

    if failures:
        print("FAIL: journal-entry surface is still person-owned")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("ok: shared Common People JE is the only active journal-entry surface")
    print(f"journal entries: {', '.join(sorted(je_defs))}")
    print(f"registered action buttons: {len(roster)}")
    print("visible JE character buttons are capped by cp_*_active_slot membership")
    print("active add_journal_entry targets:")
    for je, path in active_adds:
        print(f"- {je} from {rel(path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
