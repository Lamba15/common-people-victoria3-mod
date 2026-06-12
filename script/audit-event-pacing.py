#!/usr/bin/env python3
"""Audit Common People's routine automatic event pacing budget.

This deliberately checks structure instead of runtime logs: the mod should stay
near 1-2 routine visible story events per in-game year even as more persons,
ambient pools, law reactions, and routine world responses are added.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
SHARED_FIRING = MOD / "common" / "scripted_effects" / "cp_shared_firing.txt"
SHARED_WAR = MOD / "common" / "scripted_effects" / "cp_shared_war.txt"
ON_ACTIONS = MOD / "common" / "on_actions" / "cp_on_actions.txt"
STARTUP_EVENTS = MOD / "events" / "cp_shared_startup_events.txt"

TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_.]+)\s*=\s*\{")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*(cp_[A-Za-z0-9_]+\.[0-9]+)", re.S)
ROLL_FOR_EVENT_CALL_RE = re.compile(r"\bcp_roll_for_event\s*=\s*yes\b")
REVOLUTION_RESOLVER_CALL_RE = re.compile(r"\bcp_roll_revolution_response\s*=\s*yes\b")
WAR_START_RESOLVER_CALL_RE = re.compile(r"\bcp_roll_war_start_response\s*=\s*yes\b")
TRY_AMBIENT_CALL_RE = re.compile(r"\bcp_try_fire_ambient\s*=")
TRY_WORLD_RESPONSE_CALL_RE = re.compile(r"\bcp_try_fire_world_response\s*=")
TRY_MILESTONE_CALL_RE = re.compile(r"\bcp_try_fire_milestone\s*=")
WEIGHTED_BRANCH_RE = re.compile(r"(?m)^\s*(\d+)\s*=\s*\{\s*\}\s*$")
REVOLUTION_RESOLVER_TARGETS = ("layla", "nabil")
WAR_START_RESOLVER_TARGETS = ("layla", "soldier")

MONTH_START_DAYS = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def script_files() -> list[Path]:
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def iter_top_level_blocks(path: Path):
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        clean = strip_comment(lines[i])
        match = TOP_LEVEL_BLOCK_RE.match(clean)
        if not match:
            i += 1
            continue

        name = match.group(1)
        start = i
        depth = 0
        seen_open = False
        while i < len(lines):
            current = strip_comment(lines[i])
            depth += current.count("{")
            depth -= current.count("}")
            if "{" in current:
                seen_open = True
            if seen_open and depth <= 0:
                break
            i += 1

        yield {
            "name": name,
            "path": path,
            "line": start + 1,
            "text": "\n".join(lines[start : i + 1]),
        }
        i += 1


def top_level_block(path: Path, name: str) -> dict[str, object] | None:
    for block in iter_top_level_blocks(path):
        if block["name"] == name:
            return block
    return None


def line_no_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def variable_name_pattern(variable: str) -> str:
    return rf"\bname\s*=\s*{re.escape(variable)}(?=\s|$)"


def extract_global_variable_days(block_text: str, variable: str) -> list[int]:
    days: list[int] = []
    set_var_re = re.compile(
        r"set_global_variable\s*=\s*\{(?P<body>[^{}]*"
        + variable_name_pattern(variable)
        + r"[^{}]*)\}",
        re.S,
    )
    for match in set_var_re.finditer(block_text):
        day_match = re.search(r"\bdays\s*=\s*([0-9]+)\b", match.group("body"))
        if day_match:
            days.append(int(day_match.group(1)))
    return days


def has_cooldown_guard(block_text: str, variable: str) -> bool:
    return bool(
        re.search(
            r"NOT\s*=\s*\{\s*has_global_variable\s*=\s*"
            + re.escape(variable)
            + r"(?=\s|\})\s*\}",
            block_text,
            re.S,
        )
    )


def max_monthly_fires_per_calendar_year(cooldown_days: int) -> int:
    fires = 0
    next_allowed_day = 0
    for month_start in MONTH_START_DAYS:
        if month_start >= next_allowed_day:
            fires += 1
            next_allowed_day = month_start + cooldown_days
    return fires


def max_arbitrary_fires_per_calendar_year(cooldown_days: int) -> int:
    fires = 0
    next_allowed_day = 0
    while next_allowed_day < 365:
        fires += 1
        next_allowed_day += cooldown_days
    return fires


def max_first_year_passive_events(cooldown_days: int) -> int:
    # One visible startup opener happens on day 0, then the ambient router is
    # blocked until the same cooldown expires.
    fires_after_opener = 0
    next_allowed_day = cooldown_days
    for month_start in MONTH_START_DAYS:
        if month_start >= next_allowed_day:
            fires_after_opener += 1
            next_allowed_day = month_start + cooldown_days
    return 1 + fires_after_opener


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if namespace.startswith("cp_"):
        namespace = namespace[3:]
    return namespace.split("_", 1)[0]


def enclosing_weight_branch(text: str, offset: int) -> str:
    starts = list(re.finditer(r"(?m)^\s*\d+\s*=\s*\{", text[:offset]))
    if not starts:
        return text[max(0, offset - 400) : offset + 200]

    start = starts[-1].start()
    open_pos = text.find("{", start)
    if open_pos < 0:
        return text[start : offset + 200]

    depth = 0
    for idx in range(open_pos, len(text)):
        if text[idx] == "{":
            depth += 1
        elif text[idx] == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]
    return text[start:]


def first_contact_budget_precedes_event(branch_text: str, person: str, event_id: str) -> bool:
    budget_match = re.search(
        r"cp_mark_first_contact_budget\s*=\s*\{[^}]*\bperson\s*=\s*"
        + re.escape(person)
        + r"(?=\s|\})[^}]*\}",
        branch_text,
        re.S,
    )
    event_match = re.search(
        r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*"
        + re.escape(event_id)
        + r"(?=\s|\})",
        branch_text,
        re.S,
    )
    return bool(budget_match and event_match and budget_match.start() < event_match.start())


def check_budget_gate(
    issues: list[tuple[str, str]],
    gate_label: str,
    gate_text: str,
    global_days: list[int],
    person_days: list[int],
) -> None:
    code = gate_label.upper().replace("-", "_")
    if not has_cooldown_guard(gate_text, "cp_global_ambient_cooldown"):
        issues.append((f"{code}_GLOBAL_GUARD", f"cp_try_fire_{gate_label} does not check cp_global_ambient_cooldown"))
    if not has_cooldown_guard(gate_text, "cp_person_$person$_ambient_cooldown"):
        issues.append((f"{code}_PERSON_GUARD", f"cp_try_fire_{gate_label} does not check cp_person_$person$_ambient_cooldown"))

    if not global_days:
        issues.append((f"{code}_GLOBAL_SET", f"cp_try_fire_{gate_label} does not set cp_global_ambient_cooldown with days"))
    elif min(global_days) < 183:
        issues.append((f"{code}_GLOBAL_TOO_SHORT", f"{gate_label} global cooldown is {min(global_days)} days; expected at least 183"))

    if not person_days:
        issues.append((f"{code}_PERSON_SET", f"cp_try_fire_{gate_label} does not set cp_person_$person$_ambient_cooldown with days"))
    elif min(person_days) < 365:
        issues.append((f"{code}_PERSON_TOO_SHORT", f"{gate_label} person cooldown is {min(person_days)} days; expected at least 365"))


def main() -> int:
    issues: list[tuple[str, str]] = []

    shared_firing_block = top_level_block(SHARED_FIRING, "cp_try_fire_ambient")
    first_contact_budget = top_level_block(SHARED_FIRING, "cp_mark_first_contact_budget")
    law_reaction_block = top_level_block(SHARED_FIRING, "cp_try_fire_law_reaction")
    world_response_block = top_level_block(SHARED_FIRING, "cp_try_fire_world_response")
    revolution_resolver = top_level_block(SHARED_FIRING, "cp_roll_revolution_response")
    war_start_resolver = top_level_block(SHARED_WAR, "cp_roll_war_start_response")
    war_start_dispatch = top_level_block(SHARED_WAR, "cp_on_war_started_for_egy")
    monthly_router = top_level_block(SHARED_FIRING, "cp_roll_for_event")
    monthly_hook = top_level_block(ON_ACTIONS, "cp_on_monthly")
    revolution_hook = top_level_block(ON_ACTIONS, "cp_on_revolution")
    monthly_subscription = top_level_block(ON_ACTIONS, "on_monthly_pulse_country")
    startup_first_contact = top_level_block(STARTUP_EVENTS, "cp_shared_startup.2")

    if shared_firing_block is None:
        issues.append(("AMBIENT_GATE_MISSING", f"{rel(SHARED_FIRING)} is missing cp_try_fire_ambient"))
        ambient_text = ""
    else:
        ambient_text = uncommented_text(str(shared_firing_block["text"]))

    if first_contact_budget is None:
        issues.append(("FIRST_CONTACT_BUDGET_MISSING", f"{rel(SHARED_FIRING)} is missing cp_mark_first_contact_budget"))
        first_contact_budget_text = ""
    else:
        first_contact_budget_text = uncommented_text(str(first_contact_budget["text"]))

    if law_reaction_block is None:
        issues.append(("LAW_REACTION_GATE_MISSING", f"{rel(SHARED_FIRING)} is missing cp_try_fire_law_reaction"))
        law_reaction_text = ""
    else:
        law_reaction_text = uncommented_text(str(law_reaction_block["text"]))

    if world_response_block is None:
        issues.append(("WORLD_RESPONSE_GATE_MISSING", f"{rel(SHARED_FIRING)} is missing cp_try_fire_world_response"))
        world_response_text = ""
    else:
        world_response_text = uncommented_text(str(world_response_block["text"]))

    if revolution_resolver is None:
        issues.append(("REVOLUTION_RESOLVER_MISSING", f"{rel(SHARED_FIRING)} is missing cp_roll_revolution_response"))
        revolution_resolver_text = ""
    else:
        revolution_resolver_text = uncommented_text(str(revolution_resolver["text"]))

    if war_start_resolver is None:
        issues.append(("WAR_START_RESOLVER_MISSING", f"{rel(SHARED_WAR)} is missing cp_roll_war_start_response"))
        war_start_resolver_text = ""
    else:
        war_start_resolver_text = uncommented_text(str(war_start_resolver["text"]))

    if war_start_dispatch is None:
        issues.append(("WAR_START_DISPATCH_MISSING", f"{rel(SHARED_WAR)} is missing cp_on_war_started_for_egy"))
        war_start_dispatch_text = ""
    else:
        war_start_dispatch_text = uncommented_text(str(war_start_dispatch["text"]))

    if monthly_router is None:
        issues.append(("MONTHLY_ROUTER_MISSING", f"{rel(SHARED_FIRING)} is missing cp_roll_for_event"))
        router_text = ""
    else:
        router_text = uncommented_text(str(monthly_router["text"]))

    if monthly_hook is None:
        issues.append(("MONTHLY_HOOK_MISSING", f"{rel(ON_ACTIONS)} is missing cp_on_monthly"))
        monthly_hook_text = ""
    else:
        monthly_hook_text = uncommented_text(str(monthly_hook["text"]))

    if revolution_hook is None:
        issues.append(("REVOLUTION_HOOK_MISSING", f"{rel(ON_ACTIONS)} is missing cp_on_revolution"))
        revolution_hook_text = ""
    else:
        revolution_hook_text = uncommented_text(str(revolution_hook["text"]))

    if monthly_subscription is None:
        issues.append(("MONTHLY_SUBSCRIPTION_MISSING", f"{rel(ON_ACTIONS)} is missing on_monthly_pulse_country"))
        monthly_subscription_text = ""
    else:
        monthly_subscription_text = uncommented_text(str(monthly_subscription["text"]))

    if startup_first_contact is None:
        issues.append(("FIRST_CONTACT_MISSING", f"{rel(STARTUP_EVENTS)} is missing cp_shared_startup.2"))
        startup_text = ""
    else:
        startup_text = uncommented_text(str(startup_first_contact["text"]))

    global_cooldown_days = extract_global_variable_days(ambient_text, "cp_global_ambient_cooldown")
    person_cooldown_days = extract_global_variable_days(ambient_text, "cp_person_$person$_ambient_cooldown")
    first_contact_global_days = extract_global_variable_days(first_contact_budget_text, "cp_global_ambient_cooldown")
    first_contact_person_days = extract_global_variable_days(first_contact_budget_text, "cp_person_$person$_ambient_cooldown")
    law_reaction_global_days = extract_global_variable_days(law_reaction_text, "cp_global_ambient_cooldown")
    law_reaction_person_days = extract_global_variable_days(law_reaction_text, "cp_person_$person$_ambient_cooldown")
    world_response_global_days = extract_global_variable_days(world_response_text, "cp_global_ambient_cooldown")
    world_response_person_days = extract_global_variable_days(world_response_text, "cp_person_$person$_ambient_cooldown")

    if not has_cooldown_guard(ambient_text, "cp_global_ambient_cooldown"):
        issues.append(("AMBIENT_GLOBAL_GUARD", "cp_try_fire_ambient does not check cp_global_ambient_cooldown"))
    if not has_cooldown_guard(ambient_text, "cp_person_$person$_ambient_cooldown"):
        issues.append(("AMBIENT_PERSON_GUARD", "cp_try_fire_ambient does not check cp_person_$person$_ambient_cooldown"))

    if not global_cooldown_days:
        issues.append(("AMBIENT_GLOBAL_SET", "cp_try_fire_ambient does not set cp_global_ambient_cooldown with days"))
    elif min(global_cooldown_days) < 183:
        issues.append(("AMBIENT_GLOBAL_TOO_SHORT", f"cp_global_ambient_cooldown is {min(global_cooldown_days)} days; expected at least 183"))

    if not person_cooldown_days:
        issues.append(("AMBIENT_PERSON_SET", "cp_try_fire_ambient does not set cp_person_$person$_ambient_cooldown with days"))
    elif min(person_cooldown_days) < 365:
        issues.append(("AMBIENT_PERSON_TOO_SHORT", f"cp_person_$person$_ambient_cooldown is {min(person_cooldown_days)} days; expected at least 365"))

    if not first_contact_global_days:
        issues.append(("FIRST_CONTACT_GLOBAL_SET", "cp_mark_first_contact_budget does not set cp_global_ambient_cooldown with days"))
    elif min(first_contact_global_days) < 183:
        issues.append(("FIRST_CONTACT_GLOBAL_TOO_SHORT", f"first-contact global cooldown is {min(first_contact_global_days)} days; expected at least 183"))

    if not first_contact_person_days:
        issues.append(("FIRST_CONTACT_PERSON_SET", "cp_mark_first_contact_budget does not set cp_person_$person$_ambient_cooldown with days"))
    elif min(first_contact_person_days) < 365:
        issues.append(("FIRST_CONTACT_PERSON_TOO_SHORT", f"first-contact person cooldown is {min(first_contact_person_days)} days; expected at least 365"))

    if not has_cooldown_guard(law_reaction_text, "cp_global_ambient_cooldown"):
        issues.append(("LAW_REACTION_GLOBAL_GUARD", "cp_try_fire_law_reaction does not check cp_global_ambient_cooldown"))
    if not has_cooldown_guard(law_reaction_text, "cp_person_$person$_ambient_cooldown"):
        issues.append(("LAW_REACTION_PERSON_GUARD", "cp_try_fire_law_reaction does not check cp_person_$person$_ambient_cooldown"))

    if not law_reaction_global_days:
        issues.append(("LAW_REACTION_GLOBAL_SET", "cp_try_fire_law_reaction does not set cp_global_ambient_cooldown with days"))
    elif min(law_reaction_global_days) < 183:
        issues.append(("LAW_REACTION_GLOBAL_TOO_SHORT", f"law-reaction global cooldown is {min(law_reaction_global_days)} days; expected at least 183"))

    if not law_reaction_person_days:
        issues.append(("LAW_REACTION_PERSON_SET", "cp_try_fire_law_reaction does not set cp_person_$person$_ambient_cooldown with days"))
    elif min(law_reaction_person_days) < 365:
        issues.append(("LAW_REACTION_PERSON_TOO_SHORT", f"law-reaction person cooldown is {min(law_reaction_person_days)} days; expected at least 365"))

    check_budget_gate(
        issues,
        "world_response",
        world_response_text,
        world_response_global_days,
        world_response_person_days,
    )

    silent_weights = [int(match.group(1)) for match in WEIGHTED_BRANCH_RE.finditer(router_text)]
    if not silent_weights or max(silent_weights) <= 0:
        issues.append(("MONTHLY_SILENT_BRANCH", "cp_roll_for_event has no positive empty silent branch"))

    if "cp_on_monthly" not in monthly_subscription_text:
        issues.append(("MONTHLY_SUBSCRIPTION_TARGET", "on_monthly_pulse_country does not subscribe cp_on_monthly"))
    if not ROLL_FOR_EVENT_CALL_RE.search(monthly_hook_text):
        issues.append(("MONTHLY_ROUTER_CALL", "cp_on_monthly does not call cp_roll_for_event = yes"))
    if not REVOLUTION_RESOLVER_CALL_RE.search(revolution_hook_text):
        issues.append(("REVOLUTION_RESOLVER_CALL", "cp_on_revolution does not call cp_roll_revolution_response = yes"))

    if not WAR_START_RESOLVER_CALL_RE.search(war_start_dispatch_text):
        issues.append(("WAR_START_RESOLVER_CALL", "cp_on_war_started_for_egy does not call cp_roll_war_start_response = yes before person dispatchers"))

    revolution_targets: list[str] = []
    for person in REVOLUTION_RESOLVER_TARGETS:
        target_var = f"cp_shared_revolution_target_{person}"
        if target_var not in revolution_resolver_text:
            issues.append(("REVOLUTION_TARGET_MISSING", f"cp_roll_revolution_response does not target {person} with {target_var}"))
            continue

        memory_path = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        dispatch_block = top_level_block(memory_path, f"cp_{person}_dispatch_revolution") if memory_path.exists() else None
        dispatch_text = uncommented_text(str(dispatch_block["text"])) if dispatch_block else ""
        if not dispatch_block:
            issues.append(("REVOLUTION_DISPATCH_MISSING", f"{rel(memory_path)} is missing cp_{person}_dispatch_revolution"))
        elif target_var not in dispatch_text:
            issues.append(("REVOLUTION_TARGET_GUARD", f"cp_{person}_dispatch_revolution does not guard on {target_var}"))
        elif f"remove_variable = {target_var}" not in dispatch_text:
            issues.append(("REVOLUTION_TARGET_CLEAR", f"cp_{person}_dispatch_revolution does not clear {target_var} after consuming it"))
        else:
            revolution_targets.append(person)

    war_start_targets: list[str] = []
    for person in WAR_START_RESOLVER_TARGETS:
        target_var = f"cp_shared_war_start_target_{person}"
        if target_var not in war_start_resolver_text:
            issues.append(("WAR_START_TARGET_MISSING", f"cp_roll_war_start_response does not target {person} with {target_var}"))
            continue

        memory_path = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        dispatch_block = top_level_block(memory_path, f"cp_{person}_dispatch_war_started") if memory_path.exists() else None
        dispatch_text = uncommented_text(str(dispatch_block["text"])) if dispatch_block else ""
        if not dispatch_block:
            issues.append(("WAR_START_DISPATCH_PERSON_MISSING", f"{rel(memory_path)} is missing cp_{person}_dispatch_war_started"))
        elif target_var not in dispatch_text:
            issues.append(("WAR_START_TARGET_GUARD", f"cp_{person}_dispatch_war_started does not guard on {target_var}"))
        elif f"remove_variable = {target_var}" not in dispatch_text:
            issues.append(("WAR_START_TARGET_CLEAR", f"cp_{person}_dispatch_war_started does not clear {target_var} after consuming it"))
        else:
            war_start_targets.append(person)

    roll_call_locations: list[str] = []
    for path in script_files():
        for block in iter_top_level_blocks(path):
            clean = uncommented_text(str(block["text"]))
            for match in ROLL_FOR_EVENT_CALL_RE.finditer(clean):
                location = f"{rel(path)}:{int(block['line']) + line_no_for_offset(clean, match.start()) - 1}"
                roll_call_locations.append(f"{block['name']} at {location}")
                if block["name"] != "cp_on_monthly":
                    issues.append(("ROUTER_CALL_SITE", f"cp_roll_for_event is called outside cp_on_monthly: {block['name']} at {location}"))

    ambient_pool_calls = 0
    ambient_pool_people: set[str] = set()
    world_response_calls = 0
    for path in script_files():
        for block in iter_top_level_blocks(path):
            name = str(block["name"])
            clean = uncommented_text(str(block["text"]))
            if name != "cp_try_fire_world_response" and TRY_WORLD_RESPONSE_CALL_RE.search(clean):
                world_response_calls += len(TRY_WORLD_RESPONSE_CALL_RE.findall(clean))
            if name.endswith("_dispatch_tech") or name.endswith("_dispatch_building"):
                if TRY_MILESTONE_CALL_RE.search(clean):
                    issues.append((
                        "ROUTINE_WORLD_RESPONSE_BYPASS",
                        f"{name} at {rel(path)}:{block['line']} uses cp_try_fire_milestone; technology/building reactions should use cp_try_fire_world_response",
                    ))
            if re.fullmatch(r"cp_[A-Za-z0-9_]+\.1", name):
                person = name.removeprefix("cp_").split(".", 1)[0]
                for match in TRIGGER_EVENT_RE.finditer(clean):
                    if match.group(1) == f"cp_{person}.10":
                        issues.append((
                            "SETUP_FIRST_APPEARANCE_BYPASS",
                            f"{name} at {rel(path)}:{block['line']} directly triggers {match.group(1)}; conditional first appearances should use cp_try_fire_world_response",
                        ))
            if not TRY_AMBIENT_CALL_RE.search(clean):
                continue
            if name != "cp_try_fire_ambient":
                if not re.fullmatch(r"cp_roll_ambient_[A-Za-z0-9_]+", name):
                    issues.append(("AMBIENT_CALL_SITE", f"cp_try_fire_ambient is called outside a person ambient pool: {name} at {rel(path)}:{block['line']}"))
                    continue
                ambient_pool_calls += len(TRY_AMBIENT_CALL_RE.findall(clean))
                ambient_pool_people.add(name.removeprefix("cp_roll_ambient_"))

    first_contact_events = 0
    for match in TRIGGER_EVENT_RE.finditer(startup_text):
        first_contact_events += 1
        event_id = match.group(1)
        person = person_for_event(event_id)
        branch = enclosing_weight_branch(startup_text, match.start())
        if not first_contact_budget_precedes_event(branch, person, event_id):
            line_no = int(startup_first_contact["line"]) + line_no_for_offset(startup_text, match.start()) - 1 if startup_first_contact else line_no_for_offset(startup_text, match.start())
            issues.append((
                "FIRST_CONTACT_BRANCH_BUDGET",
                f"{rel(STARTUP_EVENTS)}:{line_no} fires {event_id} without a preceding cp_mark_first_contact_budget call for {person}",
            ))

    effective_global = min(global_cooldown_days) if global_cooldown_days else 0
    first_year_cooldown_days = global_cooldown_days + first_contact_global_days
    effective_first_year_global = min(first_year_cooldown_days) if first_year_cooldown_days else 0
    routine_cooldown_days = global_cooldown_days + first_contact_global_days + law_reaction_global_days + world_response_global_days
    effective_routine_global = min(routine_cooldown_days) if routine_cooldown_days else 0
    normal_year_cap = max_monthly_fires_per_calendar_year(effective_global) if effective_global else 0
    routine_year_cap = max_arbitrary_fires_per_calendar_year(effective_routine_global) if effective_routine_global else 0
    first_year_cap = max_first_year_passive_events(effective_first_year_global) if effective_first_year_global else 0
    if effective_global and normal_year_cap > 2:
        issues.append(("AMBIENT_YEAR_CAP", f"monthly cadence plus {effective_global}-day cooldown permits {normal_year_cap} ambient fires/year; expected at most 2"))
    if effective_routine_global and routine_year_cap > 2:
        issues.append(("ROUTINE_YEAR_CAP", f"shared visible-story cooldown of {effective_routine_global} days permits {routine_year_cap} routine automatic fires/year; expected at most 2"))
    if effective_first_year_global and first_year_cap > 2:
        issues.append(("FIRST_YEAR_CAP", f"startup first contact plus ambient cadence permits {first_year_cap} passive fires in year one; expected at most 2"))

    print("Common People event pacing audit")
    print(f"Ambient global cooldown days: {min(global_cooldown_days) if global_cooldown_days else 'missing'}")
    print(f"Ambient per-person cooldown days: {min(person_cooldown_days) if person_cooldown_days else 'missing'}")
    print(f"First-contact global cooldown days: {min(first_contact_global_days) if first_contact_global_days else 'missing'}")
    print(f"First-contact per-person cooldown days: {min(first_contact_person_days) if first_contact_person_days else 'missing'}")
    print(f"Law-reaction global cooldown days: {min(law_reaction_global_days) if law_reaction_global_days else 'missing'}")
    print(f"Law-reaction per-person cooldown days: {min(law_reaction_person_days) if law_reaction_person_days else 'missing'}")
    print(f"World-response global cooldown days: {min(world_response_global_days) if world_response_global_days else 'missing'}")
    print(f"World-response per-person cooldown days: {min(world_response_person_days) if world_response_person_days else 'missing'}")
    print(f"Monthly router calls: {len(roll_call_locations)}")
    print(f"Monthly silent branch weights: {', '.join(str(weight) for weight in silent_weights) if silent_weights else 'missing'}")
    print(f"Ambient pool calls: {ambient_pool_calls}")
    print(f"Persons with ambient pools: {len(ambient_pool_people)}")
    print(f"World-response calls: {world_response_calls}")
    print(f"War-start resolver targets: {', '.join(war_start_targets) if war_start_targets else 'missing'}")
    print(f"Revolution resolver targets: {', '.join(revolution_targets) if revolution_targets else 'missing'}")
    print(f"Startup first-contact visible branches: {first_contact_events}")
    print(f"Max ambient fires/year from monthly cadence: {normal_year_cap if effective_global else 'unknown'}")
    print(f"Max routine automatic fires/year from shared cooldown: {routine_year_cap if effective_routine_global else 'unknown'}")
    print(f"Max passive fires in first campaign year: {first_year_cap if effective_global else 'unknown'}")
    print(f"Issues: {len(issues)}")

    for code, message in issues:
        print(f"- [{code}] {message}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
