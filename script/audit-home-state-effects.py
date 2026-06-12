#!/usr/bin/env python3
"""Audit that Common People local building effects respect person home places."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
COMMON = MOD / "common"
EVENTS = MOD / "events"
LOCALIZATION = MOD / "localization"
ON_ACTIONS = COMMON / "on_actions" / "cp_on_actions.txt"

REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)",
    re.DOTALL,
)
DISPATCH_RE = re.compile(r"^(cp_([A-Za-z0-9_]+)_dispatch_building)\s*=\s*\{", re.MULTILINE)
TRY_SPAWN_RE = re.compile(r"\bcp_([A-Za-z0-9_]+)_try_spawn\s*=\s*yes\b")
TRY_SPAWN_DEF_RE = re.compile(r"^(cp_([A-Za-z0-9_]+)_try_spawn)\s*=\s*\{", re.MULTILINE)
TOP_LEVEL_EFFECT_RE = re.compile(r"^(cp_[A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
HOME_PLACE_CALL_RE = re.compile(r"cp_set_person_home_place\s*=\s*\{\s*person\s*=\s*([A-Za-z0-9_]+)\s+place\s*=\s*([A-Za-z0-9_]+)")
BUILDING_SENSITIVE_SPAWN_MARKERS = (
    "cp_country_has_manufacturing",
    "cp_country_has_factory_migration",
    "cp_country_has_machine_industry",
    "cp_country_has_rail_infrastructure",
    "cp_country_has_port",
    "cp_country_has_government_office",
    "cp_country_has_electric_service",
    "cp_country_has_telephone_network",
    "cp_country_has_urban_growth",
)
SPAWN_GATE_TO_HOME_MARKER = {
    "cp_country_has_manufacturing": "cp_mark_person_spawn_home_from_manufacturing",
    "cp_country_has_factory_migration": "cp_mark_person_spawn_home_from_manufacturing",
    "cp_country_has_machine_industry": "cp_mark_person_spawn_home_from_machine_industry",
    "cp_country_has_rail_infrastructure": "cp_mark_person_spawn_home_from_rail_infrastructure",
    "cp_country_has_port": "cp_mark_person_spawn_home_from_port",
    "cp_country_has_government_office": "cp_mark_person_spawn_home_from_government_office",
    "cp_country_has_electric_service": "cp_mark_person_spawn_home_from_electric_service",
    "cp_country_has_telephone_network": "cp_mark_person_spawn_home_from_electric_service",
    "cp_country_has_urban_growth": "cp_mark_person_spawn_home_from_urban_growth",
}
HOME_SENSOR_PROFILE_VARS = {
    "cp_person_home_has_manufacturing": (
        "var:cp_$person$_workplace_manufacturing > 0",
        "var:cp_$person$_workplace_machine > 0",
    ),
    "cp_person_home_has_machine_industry": (
        "var:cp_$person$_workplace_manufacturing > 0",
        "var:cp_$person$_workplace_machine > 0",
    ),
    "cp_person_home_has_rail_infrastructure": ("var:cp_$person$_workplace_rail > 0",),
    "cp_person_home_has_port": ("var:cp_$person$_workplace_port > 0",),
    "cp_person_home_has_government_office": ("var:cp_$person$_workplace_public_service > 0",),
    "cp_person_home_has_electric_service": ("var:cp_$person$_workplace_electric > 0",),
    "cp_person_home_has_telephone_network": ("var:cp_$person$_workplace_electric > 0",),
    "cp_person_home_has_urban_growth": ("var:cp_$person$_workplace_urban > 0",),
    "cp_person_home_has_military_industry": ("var:cp_$person$_workplace_military > 0",),
}
WORKPLACE_PROFILE_VARS = (
    "var:cp_$person$_workplace_agrarian > 0",
    "var:cp_$person$_workplace_manufacturing > 0",
    "var:cp_$person$_workplace_machine > 0",
    "var:cp_$person$_workplace_rail > 0",
    "var:cp_$person$_workplace_port > 0",
    "var:cp_$person$_workplace_public_service > 0",
    "var:cp_$person$_workplace_electric > 0",
    "var:cp_$person$_workplace_urban > 0",
    "var:cp_$person$_workplace_military > 0",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def uncommented(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def script_files() -> list[Path]:
    return sorted(COMMON.glob("**/cp_*.txt")) + sorted(EVENTS.glob("cp_*.txt"))


def localization_files() -> list[Path]:
    return sorted(LOCALIZATION.glob("**/cp_*.yml"))


def registered_persons() -> set[str]:
    text = "\n".join(uncommented(read(path)) for path in script_files())
    return set(REGISTER_PERSON_RE.findall(text))


def extract_block(text: str, start: int) -> str:
    depth = 0
    opened = False
    for index in range(start, len(text)):
        char = text[index]
        if char == "{":
            depth += 1
            opened = True
        elif char == "}":
            depth -= 1
            if opened and depth == 0:
                return text[start : index + 1]
    return text[start:]


def collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def named_block(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}\s*=\s*\{{", text, re.MULTILINE)
    if not match:
        return None
    return extract_block(text, match.start())


def require_contains(failures: list[str], context: str, block: str, needle: str, message: str) -> None:
    if needle not in collapse_ws(block):
        failures.append(f"{context}: {message}")


def require_assignment_pointer_pairs(failures: list[str], context: str, block: str) -> None:
    marker_write = "set_variable = cp_$person$_lives_here"
    pointer_write = "set_variable = { name = cp_$person$_state_pointer value = prev }"
    cursor = 0
    count = 0
    while True:
        index = block.find(marker_write, cursor)
        if index == -1:
            break
        count += 1
        next_index = block.find(marker_write, index + len(marker_write))
        segment_end = next_index if next_index != -1 else len(block)
        if pointer_write not in block[index:segment_end]:
            failures.append(f"{context}: home marker write lacks matching state-pointer write")
        cursor = index + len(marker_write)
    if count == 0:
        failures.append(f"{context}: no cp_<person>_lives_here assignment found")


def audit_shared_home_state_contract(shared_memory_text: str, failures: list[str]) -> None:
    home_block = named_block(shared_memory_text, "cp_set_person_home_state")
    if not home_block:
        failures.append("cp_shared_memory: cp_set_person_home_state block not found")
    else:
        require_contains(
            failures,
            "cp_set_person_home_state",
            home_block,
            "cp_clear_person_home_state = { person = $person$ }",
            "must clear existing home markers before assigning a new home",
        )
        require_contains(
            failures,
            "cp_set_person_home_state",
            home_block,
            "s:$state$ ?=",
            "must enter the requested state-region scope",
        )
        require_contains(
            failures,
            "cp_set_person_home_state",
            home_block,
            "any_scope_state = { owner = c:$country$ }",
            "must prefer a state owned by the person's country",
        )
        require_contains(
            failures,
            "cp_set_person_home_state",
            home_block,
            "limit = { owner = c:$country$ }",
            "owned-state branch must limit random_scope_state to the person's country",
        )
        require_assignment_pointer_pairs(failures, "cp_set_person_home_state", home_block)

    from_marker_block = named_block(shared_memory_text, "cp_set_person_home_state_from_spawn_marker_or_default")
    if not from_marker_block:
        failures.append("cp_shared_memory: cp_set_person_home_state_from_spawn_marker_or_default block not found")
    else:
        require_contains(
            failures,
            "cp_set_person_home_state_from_spawn_marker_or_default",
            from_marker_block,
            "cp_clear_person_home_state = { person = $person$ }",
            "must clear existing home markers before using a spawn candidate",
        )
        require_contains(
            failures,
            "cp_set_person_home_state_from_spawn_marker_or_default",
            from_marker_block,
            "any_scope_state = { has_variable = cp_$person$_spawn_home_candidate }",
            "must look for a marked spawn-state candidate",
        )
        require_contains(
            failures,
            "cp_set_person_home_state_from_spawn_marker_or_default",
            from_marker_block,
            "limit = { has_variable = cp_$person$_spawn_home_candidate }",
            "must assign the state that carries the spawn-state candidate marker",
        )
        require_contains(
            failures,
            "cp_set_person_home_state_from_spawn_marker_or_default",
            from_marker_block,
            "cp_clear_person_spawn_home_candidate = { person = $person$ }",
            "must clear temporary spawn-state markers after assignment",
        )
        require_contains(
            failures,
            "cp_set_person_home_state_from_spawn_marker_or_default",
            from_marker_block,
            "cp_set_person_home_state = { person = $person$ country = $country$ state = $state$ }",
            "must fall back to authored default home state when no spawn candidate exists",
        )
        require_assignment_pointer_pairs(failures, "cp_set_person_home_state_from_spawn_marker_or_default", from_marker_block)

    clear_place_block = named_block(shared_memory_text, "cp_clear_person_home_place")
    if not clear_place_block:
        failures.append("cp_shared_memory: cp_clear_person_home_place block not found")

    set_place_block = named_block(shared_memory_text, "cp_set_person_home_place")
    if not set_place_block:
        failures.append("cp_shared_memory: cp_set_person_home_place block not found")
    else:
        require_contains(
            failures,
            "cp_set_person_home_place",
            set_place_block,
            "cp_clear_person_home_place = { person = $person$ }",
            "must clear existing home-place tokens before assigning a new one",
        )


def audit_home_sensor_contract(shared_sensor_text: str, failures: list[str]) -> None:
    building_home_block = named_block(shared_sensor_text, "cp_building_is_in_person_home_state")
    if not building_home_block:
        failures.append("cp_shared_sensors: cp_building_is_in_person_home_state block not found")
    else:
        require_contains(
            failures,
            "cp_building_is_in_person_home_state",
            building_home_block,
            "state = { has_variable = cp_$person$_lives_here }",
            "must check the current building's state against the person's home marker",
        )

    workplace_block = named_block(shared_sensor_text, "cp_building_affects_person_workplace")
    if not workplace_block:
        failures.append("cp_shared_sensors: cp_building_affects_person_workplace block not found")
    else:
        require_contains(
            failures,
            "cp_building_affects_person_workplace",
            workplace_block,
            "cp_building_is_in_person_home_state = { person = $person$ }",
            "must reject buildings outside the person's home state",
        )
        collapsed = collapse_ws(workplace_block)
        for profile_var in WORKPLACE_PROFILE_VARS:
            if profile_var not in collapsed:
                failures.append(
                    f"cp_building_affects_person_workplace: missing workplace profile gate {profile_var}"
                )

    for sensor, profile_vars in HOME_SENSOR_PROFILE_VARS.items():
        block = named_block(shared_sensor_text, sensor)
        if not block:
            failures.append(f"cp_shared_sensors: {sensor} block not found")
            continue
        require_contains(
            failures,
            sensor,
            block,
            "has_variable = cp_$person$_lives_here",
            "must inspect only the person's marked home state",
        )
        require_contains(
            failures,
            sensor,
            block,
            "any_scope_building = {",
            "must require a matching local building in the person's home state",
        )
        collapsed = collapse_ws(block)
        if not any(profile_var in collapsed for profile_var in profile_vars):
            failures.append(
                f"{sensor}: missing matching workplace profile gate ({', '.join(profile_vars)})"
            )


def main() -> int:
    failures: list[str] = []
    people = registered_persons()
    files = script_files()
    all_text = "\n".join(read(path) for path in files)
    all_user_visible_text = all_text + "\n" + "\n".join(read(path) for path in localization_files())
    shared_memory_text = read(COMMON / "scripted_effects" / "cp_shared_memory.txt")
    audit_shared_home_state_contract(shared_memory_text, failures)
    clear_place_block = named_block(shared_memory_text, "cp_clear_person_home_place") or ""
    for _person, place in sorted(set(HOME_PLACE_CALL_RE.findall(all_text))):
        expected_clear = f"remove_variable = cp_$person$_home_place_{place}"
        if expected_clear not in clear_place_block:
            failures.append(
                f"cp_clear_person_home_place: missing clear for home-place token cp_<person>_home_place_{place}"
            )
    shared_sensor_text = read(COMMON / "scripted_triggers" / "cp_shared_sensors.txt")
    audit_home_sensor_contract(shared_sensor_text, failures)
    shared_pointer_write = "set_variable = { name = cp_$person$_state_pointer value = prev }"
    if shared_memory_text.count(shared_pointer_write) < 2:
        failures.append(
            "cp_shared_memory: shared home-state assignment must store cp_<person>_state_pointer for journal/save audits"
        )

    for person in sorted(people):
        marker = f"cp_{person}_lives_here"
        pointer = f"cp_{person}_state_pointer"
        setup_call = f"cp_set_person_home_state = {{ person = {person} "
        setup_from_marker_call = f"cp_set_person_home_state_from_spawn_marker_or_default = {{ person = {person} "
        place_call = f"cp_set_person_home_place = {{ person = {person} "
        profile_call = f"cp_set_person_workplace_profile = {{ person = {person} "
        layla_move_call = "cp_move_to_state = { state = "
        if marker not in all_text and setup_call not in all_text and setup_from_marker_call not in all_text:
            failures.append(f"{person}: no home-state marker or shared setup call for {marker}")
        if setup_call not in all_text and setup_from_marker_call not in all_text and not (person == "layla" and layla_move_call in all_text):
            failures.append(f"{person}: setup does not use shared home-state assignment")
        if pointer not in all_user_visible_text:
            failures.append(f"{person}: journal/save state pointer {pointer} is not referenced")
        if place_call not in all_text:
            failures.append(f"{person}: setup does not set a home-place token")
        if profile_call not in all_text:
            failures.append(f"{person}: setup does not set a workplace-profile token")

    manual_marker_re = re.compile(r"\bset_variable\s*=\s*cp_([A-Za-z0-9_]+)_lives_here\b")
    allowed_manual_paths = {
        Path("mod/common/scripted_effects/cp_layla_memory.txt"),
        Path("mod/common/scripted_effects/cp_shared_memory.txt"),
        Path("mod/events/cp_debug_events.txt"),
    }
    for path in files:
        relative = path.relative_to(ROOT)
        if relative in allowed_manual_paths:
            continue
        for match in manual_marker_re.finditer(read(path)):
            failures.append(f"{relative}: manual home marker write for {match.group(1)}; use shared home-state effects")

    found_dispatches: set[str] = set()
    for path in sorted((COMMON / "scripted_effects").glob("cp_*_memory.txt")):
        text = read(path)
        for match in DISPATCH_RE.finditer(text):
            name, person = match.group(1), match.group(2)
            found_dispatches.add(person)
            block = extract_block(text, match.start())
            if "cp_person_hook_noop" in block and "is_building_" not in block:
                continue
            local_trigger = f"cp_building_affects_person_workplace = {{ person = {person} }}"
            raw_local_check = f"state = {{ has_variable = cp_{person}_lives_here }}"
            if local_trigger not in block and raw_local_check not in block:
                failures.append(f"{path.relative_to(ROOT)}::{name} lacks a home/workplace building check")

    for person in sorted(people - found_dispatches):
        failures.append(f"{person}: missing cp_{person}_dispatch_building hook")

    for path in sorted((COMMON / "scripted_effects").glob("cp_*_memory.txt")):
        text = read(path)
        for match in TRY_SPAWN_DEF_RE.finditer(text):
            name, person = match.group(1), match.group(2)
            block = extract_block(text, match.start())
            uses_building_sensitive_gate = any(marker in block for marker in BUILDING_SENSITIVE_SPAWN_MARKERS) or (
                "any_scope_state" in block and "any_scope_building" in block
            )
            if not uses_building_sensitive_gate:
                continue

            if f"cp_mark_building_spawn_home = {{ person = {person} }}" in block:
                continue

            missing_markers = sorted(
                expected
                for gate, expected in SPAWN_GATE_TO_HOME_MARKER.items()
                if gate in block and f"{expected} = {{ person = {person} }}" not in block
            )
            if missing_markers:
                failures.append(
                    f"{path.relative_to(ROOT)}::{name} has building-sensitive spawn gates but lacks matching home-state marker(s): "
                    + ", ".join(missing_markers)
                )
            elif "any_scope_state" in block and "any_scope_building" in block and "cp_mark_person_spawn_home_from_" not in block:
                failures.append(
                    f"{path.relative_to(ROOT)}::{name} has building-sensitive spawn gates but no matching home-state candidate marker"
                )

    for path in sorted((COMMON / "scripted_effects").glob("cp_*_memory.txt")):
        text = uncommented(read(path))
        for match in TOP_LEVEL_EFFECT_RE.finditer(text):
            name = match.group(1)
            if name.endswith("_try_spawn"):
                continue
            block = extract_block(text, match.start())
            for marker in BUILDING_SENSITIVE_SPAWN_MARKERS:
                if marker in block:
                    failures.append(
                        f"{path.relative_to(ROOT)}::{name} uses country-wide {marker}; local physical beats should use cp_person_home_has_* sensors"
                    )

    on_actions_text = read(ON_ACTIONS)
    building_match = re.search(r"^cp_on_building_built\s*=\s*\{", on_actions_text, re.MULTILINE)
    if building_match:
        building_block = extract_block(on_actions_text, building_match.start())
        for person in sorted(set(TRY_SPAWN_RE.findall(building_block))):
            marker_call = f"cp_mark_building_spawn_home = {{ person = {person} }}"
            if marker_call not in building_block:
                failures.append(f"cp_on_building_built: {person} spawn lacks building-state home marker")
    else:
        failures.append("cp_on_building_built block not found")

    if failures:
        print("FAIL: Common People home-state effects audit")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Common People home-state effects audit")
    print(f"registered persons: {len(people)}")
    print("home markers/state pointers: present")
    print("home-place/workplace profiles: present")
    print("shared home/workplace sensors: local-state and profile gated")
    print("building dispatches/spawns: local home/workplace checks and matching spawn markers present")
    print("Issues: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
