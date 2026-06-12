#!/usr/bin/env python3
"""Audit a Victoria 3 save for a real Egypt/Common People gameplay pass."""

from __future__ import annotations

import argparse
import gzip
import re
import sys
import zipfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
DEFAULT_SAVE_DIR = Path.home() / ".local/share/Paradox Interactive/Victoria 3/save games"

REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*EGY\b",
    re.S,
)
FLAG_RE = re.compile(r"\bflag=([A-Za-z0-9_]+)\b")
VAR_ENTRY_RE = re.compile(
    r"\{\s*flag=([A-Za-z0-9_]+)\b(?:(?!\}\s*\{).)*?\bdata=\{\s*type=([A-Za-z_]+)(?:\s+identity=(-?\d+))?",
    re.S,
)
MODS_RE = re.compile(r"\bmods=\{([^}]*)\}", re.S)
DATE_RE = re.compile(r"(?m)^date=(\d+)\.(\d+)\.(\d+)\b")
WORKPLACE_PROFILES = (
    "agrarian",
    "manufacturing",
    "machine",
    "rail",
    "port",
    "public_service",
    "electric",
    "urban",
    "military",
)


@dataclass(frozen=True)
class SaveVariable:
    name: str
    type: str
    identity: int | None

    @property
    def game_value(self) -> float:
        if self.identity is None:
            return 0
        if self.type == "value":
            return self.identity / 100000
        return self.identity


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def script_files() -> list[Path]:
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def registered_egypt_persons() -> list[str]:
    text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    return sorted(set(REGISTER_PERSON_RE.findall(text)))


def always_on_egypt_persons() -> list[str]:
    startup_path = MOD / "events" / "cp_shared_startup_events.txt"
    text = uncommented_text(startup_path.read_text(encoding="utf-8-sig", errors="replace"))
    always_on_text = text.split("cp_startup_conditional_scan", 1)[0]
    return sorted(set(REGISTER_PERSON_RE.findall(always_on_text)))


def latest_save(save_dir: Path) -> Path:
    saves = sorted(save_dir.glob("*.v3"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not saves:
        raise SystemExit(f"error: no .v3 saves found under {save_dir}")
    return saves[0]


def read_save_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"PK"):
        with zipfile.ZipFile(BytesIO(raw)) as archive:
            names = archive.namelist()
            preferred = [name for name in names if name.endswith("gamestate")]
            name = preferred[0] if preferred else names[0]
            raw = archive.read(name)
    elif raw.startswith(b"\x1f\x8b"):
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", errors="replace")


def parse_date(text: str) -> tuple[int, int, int] | None:
    match = DATE_RE.search(text)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def parse_date_arg(value: str) -> tuple[int, int, int]:
    parts = value.split(".")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("date must be YYYY.M.D")
    try:
        year, month, day = (int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must be YYYY.M.D") from exc
    return year, month, day


def date_str(date: tuple[int, int, int] | None) -> str:
    if date is None:
        return "unknown"
    return f"{date[0]}.{date[1]}.{date[2]}"


def find_block_start_before(text: str, index: int) -> int | None:
    matches = list(re.finditer(r"\n(\d+)=\{", text[:index]))
    if not matches:
        return None
    return matches[-1].start() + 1


def extract_balanced_block(text: str, start: int) -> str:
    open_index = text.find("{", start)
    if open_index == -1:
        raise ValueError("block has no opening brace")

    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    raise ValueError("block is not balanced")


def country_block(text: str, tag: str) -> str | None:
    definition = f'definition="{tag}"'
    index = text.find(definition)
    if index == -1:
        return None
    start = find_block_start_before(text, index)
    if start is None:
        return None
    return extract_balanced_block(text, start)


def save_mods(text: str) -> set[str]:
    match = MODS_RE.search(text[:100_000])
    if not match:
        return set()
    return set(re.findall(r'"([^"]+)"', match.group(1)))


def flags_in(text: str) -> set[str]:
    return set(FLAG_RE.findall(text))


def variables_in(text: str) -> dict[str, list[SaveVariable]]:
    variables: dict[str, list[SaveVariable]] = {}
    for match in VAR_ENTRY_RE.finditer(text):
        name = match.group(1)
        var_type = match.group(2)
        identity = int(match.group(3)) if match.group(3) is not None else None
        variables.setdefault(name, []).append(SaveVariable(name=name, type=var_type, identity=identity))
    return variables


def has_variable(variables: dict[str, list[SaveVariable]], name: str) -> bool:
    return name in variables


def variable_value(variables: dict[str, list[SaveVariable]], name: str) -> float | None:
    values = variables.get(name, [])
    if not values:
        return None
    return values[-1].game_value


def positive_variable(variables: dict[str, list[SaveVariable]], name: str) -> bool:
    value = variable_value(variables, name)
    return value is not None and value > 0


def variable_types(variables: dict[str, list[SaveVariable]], name: str) -> set[str]:
    return {value.type for value in variables.get(name, [])}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the latest or selected Victoria 3 save for a real Egypt/Common People gameplay pass."
    )
    parser.add_argument("--save", type=Path, help="specific .v3 save to audit; defaults to latest local save")
    parser.add_argument("--save-dir", type=Path, default=DEFAULT_SAVE_DIR, help="save directory for latest-save lookup")
    parser.add_argument(
        "--min-date",
        type=parse_date_arg,
        default=(1836, 1, 2),
        help="minimum accepted in-save date, default: 1836.1.2",
    )
    parser.add_argument(
        "--allow-silent-first-contact",
        action="store_true",
        help="allow startup proof with zero active people, matching the intentional silent first-contact branch",
    )
    args = parser.parse_args()

    save_path = args.save if args.save else latest_save(args.save_dir)
    text = read_save_text(save_path)
    date = parse_date(text)
    mods = save_mods(text)
    egy_block = country_block(text, "EGY")
    people = registered_egypt_persons()
    always_on_people = always_on_egypt_persons()
    issues: list[str] = []

    if "Common People" not in mods:
        issues.append("save metadata does not list the Common People mod")
    if date is None:
        issues.append("could not read save date")
    elif date < args.min_date:
        issues.append(f"save date {date_str(date)} is before required {date_str(args.min_date)}")
    if egy_block is None:
        issues.append("could not find an EGY country block")

    egy_variables = variables_in(egy_block or "")
    all_variables = variables_in(text)
    egy_flags = set(egy_variables)
    all_flags = set(all_variables)
    active_slots = {
        person: int(variable_value(egy_variables, f"cp_{person}_active_slot") or 0)
        for person in people
        if has_variable(egy_variables, f"cp_{person}_active_slot")
    }
    active_people = sorted(active_slots)
    alive_people = sorted(person for person in people if positive_variable(egy_variables, f"cp_{person}_alive"))
    seen_people = sorted(
        person
        for person in people
        if any(flag.startswith(f"cp_{person}_seen_") for flag in egy_flags)
        or f"cp_{person}_met_player" in egy_flags
    )

    required_egy_flags = [
        "cp_common_people_je_added",
        "cp_first_contact_chosen",
        "cp_active_roster_v0_cleaned",
    ]
    for flag in required_egy_flags:
        if not has_variable(egy_variables, flag):
            issues.append(f"EGY is missing required Common People flag: {flag}")

    for person in always_on_people:
        if not positive_variable(egy_variables, f"cp_{person}_alive"):
            issues.append(f"always-on person is missing EGY alive flag: cp_{person}_alive")
        if not has_variable(all_variables, f"cp_person_{person}_alive"):
            issues.append(f"global registry is missing alive flag: cp_person_{person}_alive")

    for person in alive_people:
        home_marker_count = len(all_variables.get(f"cp_{person}_lives_here", []))
        if home_marker_count == 0:
            issues.append(f"{person} is alive but has no state home marker: cp_{person}_lives_here")
        elif home_marker_count != 1:
            issues.append(f"{person} should have exactly one state home marker; found {home_marker_count}")

        state_pointer = f"cp_{person}_state_pointer"
        if not has_variable(egy_variables, state_pointer):
            issues.append(f"{person} is alive but has no journal home-state pointer: cp_{person}_state_pointer")
        elif variable_types(egy_variables, state_pointer) != {"state"}:
            found = ", ".join(sorted(variable_types(egy_variables, state_pointer)))
            issues.append(f"{person} journal home-state pointer should be type=state; found {found}")

        home_places = sorted(flag for flag in egy_flags if flag.startswith(f"cp_{person}_home_place_"))
        if len(home_places) != 1:
            issues.append(f"{person} should have exactly one home-place token; found {len(home_places)}")
        active_profiles = sorted(
            profile
            for profile in WORKPLACE_PROFILES
            if positive_variable(egy_variables, f"cp_{person}_workplace_{profile}")
        )
        if len(active_profiles) != 1:
            issues.append(f"{person} should have exactly one positive workplace profile; found {len(active_profiles)}")

    for person, slot in active_slots.items():
        if slot < 1 or slot > 3:
            issues.append(f"{person} has invalid active JE slot {slot}; expected 1, 2, or 3")
        if not positive_variable(egy_variables, f"cp_{person}_alive"):
            issues.append(f"{person} is active in the JE but is not alive in EGY variables")

    active_slot_values = list(active_slots.values())
    duplicate_slots = sorted(slot for slot in set(active_slot_values) if active_slot_values.count(slot) > 1)
    if duplicate_slots:
        issues.append(f"active JE roster has duplicate slot value(s): {', '.join(str(slot) for slot in duplicate_slots)}")
    if len(active_people) > 3:
        issues.append(f"active JE roster has more than three people: {', '.join(active_people)}")
    if not args.allow_silent_first_contact and not active_people:
        issues.append(
            "no active Common People are present; rerun after a visible first-contact/event, "
            "or pass --allow-silent-first-contact for the intentional silent startup branch"
        )
    if active_people and not set(active_people).issubset(seen_people):
        missing = sorted(set(active_people) - set(seen_people))
        issues.append(f"active people lack visible-history flags: {', '.join(missing)}")

    print("Common People Egypt gameplay save audit")
    print(f"save: {save_path}")
    print(f"date: {date_str(date)}")
    print(f"mods: {', '.join(sorted(mods)) if mods else '(none found)'}")
    print(f"registered Egypt persons: {len(people)}")
    print(f"always-on Egypt persons: {len(always_on_people)}" + (f" ({', '.join(always_on_people)})" if always_on_people else ""))
    print(f"alive Egypt persons in save: {len(alive_people)}" + (f" ({', '.join(alive_people)})" if alive_people else ""))
    if active_people:
        slot_text = ", ".join(f"{person}=slot{active_slots[person]}" for person in active_people)
        print(f"active JE people in save: {len(active_people)} ({slot_text})")
    else:
        print("active JE people in save: 0")
    print(f"people with visible history: {len(seen_people)}" + (f" ({', '.join(seen_people)})" if seen_people else ""))

    if issues:
        print("Issues:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Issues: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
