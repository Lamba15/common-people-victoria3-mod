#!/usr/bin/env python3
"""Audit Common People's multi-person roster scaffolding."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
IMAGE_RE = re.compile(r'event_image\s*=\s*\{[^}]*?(?:texture|video)\s*=\s*"([^"]+)"', re.S)
REGISTER_PERSON_RE = re.compile(r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*([A-Za-z0-9_]+)", re.S)
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
EFFECT_CALL_RE = re.compile(r"\b(cp_[A-Za-z0-9_]+)\s*=\s*(?:yes|\{)")

PERSON_HOOKS = (
    "startup",
    "monthly",
    "law_enacted",
    "yearly",
    "war_started",
    "war_end",
    "tech",
    "building",
    "revolution",
)
CONDITIONAL_ENTRY_HOOKS = (
    "startup",
    "yearly",
    "law_enacted",
    "war_started",
    "war_end",
    "tech",
    "building",
    "revolution",
)
SITUATION_ENTRY_HOOKS = tuple(hook for hook in CONDITIONAL_ENTRY_HOOKS if hook not in {"startup", "yearly"})
MODERNIZATION_ENTRY_HOOKS = ("tech", "building")
MODERNIZATION_SPAWN_MARKERS = (
    "bg_manufacturing",
    "has_technology_researched",
    "law_no_workers_rights",
    "law_regulatory_bodies",
    "law_worker_protections",
    "law_serfdom",
    "law_tenant_farmers",
)


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def script_files() -> list[Path]:
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def event_files() -> list[Path]:
    return sorted((MOD / "events").glob("*.txt"))


def iter_event_blocks():
    for path in event_files():
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        i = 0
        while i < len(lines):
            match = EVENT_DEF_RE.match(lines[i])
            if not match:
                i += 1
                continue

            start = i
            depth = 0
            seen_open = False
            while i < len(lines):
                clean = strip_comment(lines[i])
                depth += clean.count("{")
                depth -= clean.count("}")
                if "{" in clean:
                    seen_open = True
                if seen_open and depth <= 0:
                    break
                i += 1

            yield {
                "id": match.group(1),
                "path": path,
                "line": start + 1,
                "text": "\n".join(lines[start : i + 1]),
            }
            i += 1


def top_level_definitions(path: Path) -> set[str]:
    definitions: set[str] = set()
    depth = 0
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        clean = strip_comment(line)
        if depth == 0:
            match = TOP_LEVEL_BLOCK_RE.match(clean)
            if match:
                definitions.add(match.group(1))
        depth += clean.count("{")
        depth -= clean.count("}")
        depth = max(depth, 0)
    return definitions


def top_level_block_texts(path: Path) -> dict[str, str]:
    blocks: dict[str, str] = {}
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
        blocks[name] = "\n".join(lines[start : i + 1])
        i += 1
    return blocks


def all_top_level_block_texts() -> dict[str, str]:
    blocks: dict[str, str] = {}
    for path in script_files():
        blocks.update(top_level_block_texts(path))
    return blocks


def block_or_called_effect_mentions(block_text: str, marker: str, definitions: dict[str, str]) -> bool:
    clean_block = uncommented_text(block_text)
    if marker in clean_block:
        return True
    home_match = re.fullmatch(r"cp_([A-Za-z0-9_]+)_lives_here", marker)
    if home_match:
        person = home_match.group(1)
        if re.search(
            rf"\bcp_set_person_home_state(?:_from_spawn_marker_or_default)?\s*=\s*\{{[^}}]*?\bperson\s*=\s*{re.escape(person)}\b",
            clean_block,
            re.S,
        ):
            return True
    calls = set(EFFECT_CALL_RE.findall(clean_block))
    return any(marker in definitions.get(call, "") for call in calls)


def spawn_definition_uses_modernization(text: str) -> bool:
    return any(marker in text for marker in MODERNIZATION_SPAWN_MARKERS)


def find_person_setup_event(
    person: str,
    events_by_id: dict[str, dict[str, object]],
    definitions: dict[str, str],
) -> dict[str, object] | None:
    alive_marker = f"cp_{person}_alive"
    home_marker = f"cp_{person}_lives_here"
    alive_init_re = re.compile(
        rf"set_variable\s*=\s*(?:\{{\s*name\s*=\s*{re.escape(alive_marker)}\s+value\s*=\s*1\b|{re.escape(alive_marker)}\b)"
    )
    candidates: list[dict[str, object]] = []
    for block in events_by_id.values():
        text = str(block["text"])
        if not re.search(r"\bhidden\s*=\s*yes\b", text):
            continue
        if not alive_init_re.search(text):
            continue
        if not block_or_called_effect_mentions(text, home_marker, definitions):
            continue
        candidates.append(block)
    return sorted(candidates, key=lambda block: str(block["id"]))[0] if candidates else None


def registered_persons() -> list[str]:
    text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    return sorted({match.group(1) for match in REGISTER_PERSON_RE.finditer(text)})


def loc_keys() -> set[str]:
    keys: set[str] = set()
    for path in sorted((MOD / "localization").glob("**/*.yml")):
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            match = LOC_KEY_RE.match(line)
            if match:
                keys.add(match.group(1))
    return keys


def visible_event(block: dict[str, object]) -> bool:
    text = str(block["text"])
    return not re.search(r"\bhidden\s*=\s*yes\b", text) and bool(OPTION_RE.search(text))


def person_owns_event(person: str, event_id: str) -> bool:
    """Return true for cp_layla.10 and subnamespaces like cp_layla_vox.10."""
    prefix = f"cp_{person}"
    return event_id.startswith(f"{prefix}.") or event_id.startswith(f"{prefix}_")


def person_owns_loc_key(person: str, loc_key: str) -> bool:
    prefix = f"cp_{person}"
    return loc_key.startswith(f"{prefix}.") or loc_key.startswith(f"{prefix}_")


def describe_event_ids(event_ids: list[str], full: bool) -> str:
    if full or len(event_ids) <= 40:
        return ", ".join(event_ids)
    namespace_counts = Counter(event_id.split(".", 1)[0] for event_id in event_ids)
    counts = ", ".join(f"{namespace}={count}" for namespace, count in sorted(namespace_counts.items()))
    sample = ", ".join(event_ids[:30])
    return f"{len(event_ids)} missing ({counts}); first 30: {sample}; pass --list-missing-debug for the full list"


def named_top_level_block(path: Path, name: str) -> str:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        clean = strip_comment(lines[i])
        match = TOP_LEVEL_BLOCK_RE.match(clean)
        if not match or match.group(1) != name:
            i += 1
            continue

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
        return "\n".join(lines[start : i + 1])
    return ""


def debug_triggers() -> set[str]:
    triggers: set[str] = set()
    paths = sorted((MOD / "events").glob("cp_debug*_events.txt"))
    paths.extend(sorted((MOD / "common").glob("**/cp_debug*.txt")))
    for path in paths:
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        triggers.update(TRIGGER_EVENT_RE.findall(text))
        triggers.update(GATEKEEPER_EVENT_RE.findall(text))
    return triggers


def event_targets(text: str) -> list[str]:
    clean = uncommented_text(text)
    return TRIGGER_EVENT_RE.findall(clean) + GATEKEEPER_EVENT_RE.findall(clean)


def startup_registers_person(startup_text: str, person: str) -> bool:
    return bool(re.search(rf"cp_register_person\s*=\s*\{{[^}}]*?\bperson\s*=\s*{re.escape(person)}\b", startup_text, re.S))


def block_triggers_event(block_text: str, event_id: str) -> bool:
    return event_id in set(TRIGGER_EVENT_RE.findall(uncommented_text(block_text)))


def effect_call_has_params(block_text: str, effect: str, params: dict[str, str]) -> bool:
    clean = uncommented_text(block_text)
    pattern = rf"\b{re.escape(effect)}\s*=\s*\{{(?P<body>[^}}]*)\}}"
    for match in re.finditer(pattern, clean, re.S):
        body = match.group("body")
        if all(re.search(rf"\b{re.escape(key)}\s*=\s*{re.escape(value)}\b", body) for key, value in params.items()):
            return True
    return False


def weighted_random_list_entries(text: str) -> list[tuple[int, str]]:
    clean = uncommented_text(text)
    match = re.search(r"\brandom_list\s*=\s*\{", clean)
    if not match:
        return []

    pos = clean.find("{", match.start()) + 1
    depth = 1
    entries: list[tuple[int, str]] = []
    while pos < len(clean) and depth > 0:
        if depth == 1:
            entry = re.match(r"\s*(\d+)\s*=\s*\{", clean[pos:])
            if entry:
                weight = int(entry.group(1))
                pos += entry.end()
                body_start = pos
                entry_depth = 1
                while pos < len(clean) and entry_depth > 0:
                    if clean[pos] == "{":
                        entry_depth += 1
                    elif clean[pos] == "}":
                        entry_depth -= 1
                    pos += 1
                entries.append((weight, clean[body_start : pos - 1]))
                continue

        if clean[pos] == "{":
            depth += 1
        elif clean[pos] == "}":
            depth -= 1
        pos += 1
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-debug",
        action="store_true",
        help=(
            "deprecated; debug QA coverage is always required for every visible "
            "person-owned event"
        ),
    )
    parser.add_argument(
        "--show-missing-debug",
        action="store_true",
        help="deprecated; missing debug QA coverage is always printed and fails",
    )
    parser.add_argument(
        "--list-missing-debug",
        action="store_true",
        help="print every missing event id instead of compacting long debug-wrapper reports",
    )
    parser.add_argument(
        "--min-visible-events",
        type=int,
        default=0,
        help="require every registered person to have at least this many visible events",
    )
    parser.add_argument(
        "--min-first-contact-candidates",
        type=int,
        default=0,
        help="require the shared first-contact roll to include at least this many visible event candidates",
    )
    parser.add_argument(
        "--min-always-on-first-contact-candidates",
        type=int,
        default=0,
        help=(
            "require the no-conditional-startup baseline to include at least this "
            "many visible first-contact event candidates"
        ),
    )
    parser.add_argument(
        "--max-first-contact-person-share",
        type=float,
        default=0.0,
        help=(
            "fail if any one person has more than this share of first-contact "
            "weight, checked both with and without conditional entrants"
        ),
    )
    args = parser.parse_args()

    issues: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []
    persons = registered_persons()
    all_loc_keys = loc_keys()
    debug_event_ids = debug_triggers()
    definitions_by_name = all_top_level_block_texts()
    common_text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    shared_firing_path = MOD / "common" / "scripted_effects" / "cp_shared_firing.txt"
    on_actions_path = MOD / "common" / "on_actions" / "cp_on_actions.txt"
    shared_war_path = MOD / "common" / "scripted_effects" / "cp_shared_war.txt"
    monthly_router = named_top_level_block(shared_firing_path, "cp_roll_for_event")
    yearly_dispatcher = named_top_level_block(on_actions_path, "cp_on_yearly")
    hook_call_blocks = {
        "startup": common_text,
        "monthly": named_top_level_block(on_actions_path, "cp_on_monthly"),
        "law_enacted": named_top_level_block(on_actions_path, "cp_on_law_enacted"),
        "yearly": yearly_dispatcher,
        "war_started": named_top_level_block(shared_war_path, "cp_on_war_started_for_egy"),
        "war_end": named_top_level_block(on_actions_path, "cp_on_war_end"),
        "tech": named_top_level_block(on_actions_path, "cp_on_tech"),
        "building": named_top_level_block(on_actions_path, "cp_on_building_built"),
        "revolution": named_top_level_block(on_actions_path, "cp_on_revolution"),
    }
    router_people = re.findall(r"\bcp_roll_ambient_([A-Za-z0-9_]+)\s*=\s*yes\b", monthly_router)
    silent_weights = [
        int(match.group(1))
        for match in re.finditer(r"(?m)^\s*(\d+)\s*=\s*\{\s*\}\s*(?:#.*)?$", monthly_router)
    ]

    person_events: dict[str, list[dict[str, object]]] = {person: [] for person in persons}
    events_by_id: dict[str, dict[str, object]] = {}
    for block in iter_event_blocks():
        event_id = str(block["id"])
        events_by_id[event_id] = block
        for person in persons:
            if person_owns_event(person, event_id):
                person_events[person].append(block)
    startup_text = str(events_by_id["cp_shared_startup.1"]["text"]) if "cp_shared_startup.1" in events_by_id else ""
    first_contact_text = str(events_by_id["cp_shared_startup.2"]["text"]) if "cp_shared_startup.2" in events_by_id else ""
    always_on_people = sorted(person for person in persons if startup_registers_person(startup_text, person))
    conditional_hook_call_blocks = dict(hook_call_blocks)
    conditional_hook_call_blocks["startup"] = startup_text
    first_contact_targets = sorted(set(TRIGGER_EVENT_RE.findall(uncommented_text(first_contact_text))))
    non_layla_first_contacts = sorted(
        event_id
        for event_id in first_contact_targets
        if event_id != "cp_layla.1" and re.match(r"cp_[A-Za-z0-9_]+\.[0-9]+$", event_id)
    )
    first_contact_person_weights: Counter[str] = Counter()
    first_contact_silent_weight = 0
    for weight, body in weighted_random_list_entries(first_contact_text):
        targets = TRIGGER_EVENT_RE.findall(body)
        if not targets:
            first_contact_silent_weight += weight
            continue
        for event_id in targets:
            for person in persons:
                if person_owns_event(person, event_id):
                    first_contact_person_weights[person] += weight
                    break
    always_on_first_contact_targets = sorted(
        event_id
        for event_id in first_contact_targets
        if any(person_owns_event(person, event_id) for person in always_on_people)
    )
    always_on_first_contact_person_weights = Counter(
        {
            person: weight
            for person, weight in first_contact_person_weights.items()
            if person in always_on_people
        }
    )
    memory_definitions_by_person: dict[str, set[str]] = {}
    conditional_entry_hooks: dict[str, list[str]] = {}
    for person in persons:
        memory = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        definitions = top_level_definitions(memory) if memory.exists() else set()
        memory_definitions_by_person[person] = definitions
        try_spawn = f"cp_{person}_try_spawn"
        if try_spawn not in definitions:
            continue
        hooks = [
            hook
            for hook in CONDITIONAL_ENTRY_HOOKS
            if block_or_called_effect_mentions(conditional_hook_call_blocks.get(hook, ""), try_spawn, definitions_by_name)
        ]
        if hooks:
            conditional_entry_hooks[person] = hooks

    print("Common People person roster audit")
    print(f"Registered persons: {len(persons)}")
    print(
        f"Monthly router branches: {len(router_people)} weighted person entries "
        f"({len(set(router_people))} persons) + {sum(silent_weights)} silent weight"
    )
    print(
        f"First-contact candidates: {len(first_contact_targets)} "
        f"({len(non_layla_first_contacts)} non-Layla)"
    )
    first_contact_visible_weight = sum(first_contact_person_weights.values())
    top_first_contact = first_contact_person_weights.most_common(1)
    top_first_contact_text = f"{top_first_contact[0][0]}={top_first_contact[0][1]}" if top_first_contact else "none"
    print(
        f"First-contact weights: visible={first_contact_visible_weight} "
        f"silent={first_contact_silent_weight} top={top_first_contact_text}"
    )
    always_on_first_contact_visible_weight = sum(always_on_first_contact_person_weights.values())
    top_always_on_first_contact = always_on_first_contact_person_weights.most_common(1)
    top_always_on_text = (
        f"{top_always_on_first_contact[0][0]}={top_always_on_first_contact[0][1]}"
        if top_always_on_first_contact
        else "none"
    )
    print(
        "First-contact always-on baseline: "
        f"candidates={len(always_on_first_contact_targets)} "
        f"visible={always_on_first_contact_visible_weight} "
        f"silent={first_contact_silent_weight} top={top_always_on_text}"
    )
    if args.min_first_contact_candidates > 0:
        print(f"Minimum first-contact candidates: {args.min_first_contact_candidates}")
    if args.min_always_on_first_contact_candidates > 0:
        print(
            "Minimum always-on first-contact candidates: "
            f"{args.min_always_on_first_contact_candidates}"
        )
    if args.max_first_contact_person_share > 0:
        print(f"Maximum first-contact person share: {args.max_first_contact_person_share:.0%}")
    conditional_summary = ", ".join(
        f"{person}:{'/'.join(hooks)}" for person, hooks in sorted(conditional_entry_hooks.items())
    )
    print(f"Conditional entrants: {len(conditional_entry_hooks)} ({conditional_summary or 'none'})")
    print("Shared yearly lifecycle: required for non-Layla persons")
    print("Setup entry validation: enabled")
    if args.min_visible_events > 0:
        print(f"Minimum visible events per person: {args.min_visible_events}")

    for definition in ("cp_refresh_person_mortality_pressure", "cp_person_yearly_lifecycle"):
        if definition not in definitions_by_name:
            issues.append((
                "SHARED_LIFECYCLE_DEF",
                f"{definition} is missing; non-Layla persons need the shared yearly progression/death-pressure path",
            ))

    if not startup_text:
        issues.append(("STARTUP_EVENT", "cp_shared_startup.1 is missing"))
    elif not block_triggers_event(startup_text, "cp_shared_startup.2"):
        issues.append((
            "FIRST_CONTACT_ENTRY",
            "cp_shared_startup.1 does not call cp_shared_startup.2 after always-on setup",
        ))

    legacy_startup_ids = sorted(event_id for event_id in events_by_id if event_id.startswith("cp_startup."))
    if legacy_startup_ids:
        issues.append((
            "LEGACY_STARTUP_NAMESPACE",
            f"legacy startup namespace still defines {', '.join(legacy_startup_ids)}; person setup must live in cp_<name> or cp_<name>_setup namespaces",
        ))

    layla_setup = find_person_setup_event("layla", events_by_id, definitions_by_name)
    layla_setup_id = str(layla_setup["id"]) if layla_setup else ""
    layla_setup_text = str(layla_setup["text"]) if layla_setup else ""
    if layla_setup and not person_owns_event("layla", layla_setup_id):
        issues.append((
            "LAYLA_SETUP_NAMESPACE",
            f"Layla's hidden setup event is {layla_setup_id}; it should live in a Layla-owned namespace like cp_layla_setup.*",
        ))
    if block_triggers_event(layla_setup_text, "cp_layla.1"):
        issues.append((
            "LAYLA_DIRECT_STARTUP",
            f"{layla_setup_id or 'Layla setup'} still direct-fires cp_layla.1; the first visible contact must be randomized in cp_shared_startup.2",
        ))

    if not first_contact_text:
        issues.append(("FIRST_CONTACT_EVENT", "cp_shared_startup.2 randomized first-contact event is missing"))
    else:
        if "cp_layla.1" not in first_contact_targets:
            issues.append(("FIRST_CONTACT_LAYLA", "cp_shared_startup.2 does not include Layla as one normal candidate"))
        if args.min_first_contact_candidates > 0 and len(first_contact_targets) < args.min_first_contact_candidates:
            issues.append((
                "FIRST_CONTACT_CANDIDATES",
                f"cp_shared_startup.2 has {len(first_contact_targets)} visible candidates; expected at least {args.min_first_contact_candidates}",
            ))
        if (
            args.min_always_on_first_contact_candidates > 0
            and len(always_on_first_contact_targets) < args.min_always_on_first_contact_candidates
        ):
            issues.append((
                "FIRST_CONTACT_ALWAYS_ON_CANDIDATES",
                f"the no-conditional-startup baseline has {len(always_on_first_contact_targets)} visible candidates; expected at least {args.min_always_on_first_contact_candidates}",
            ))
        if len(non_layla_first_contacts) < 5:
            issues.append((
                "FIRST_CONTACT_DIVERSITY",
                "cp_shared_startup.2 needs at least five non-Layla starting candidates",
            ))
        if first_contact_silent_weight <= 0:
            issues.append(("FIRST_CONTACT_SILENT", "cp_shared_startup.2 has no positive silent branch"))
        total_first_contact_weight = first_contact_visible_weight + first_contact_silent_weight
        layla_first_contact_weight = first_contact_person_weights.get("layla", 0)
        if total_first_contact_weight and layla_first_contact_weight / total_first_contact_weight > 0.25:
            issues.append((
                "FIRST_CONTACT_LAYLA_WEIGHT",
                f"Layla has {layla_first_contact_weight}/{total_first_contact_weight} first-contact weight; she should be one candidate, not the default face",
            ))
        if total_first_contact_weight and top_first_contact and top_first_contact[0][1] / total_first_contact_weight > 0.35:
            issues.append((
                "FIRST_CONTACT_TOP_WEIGHT",
                f"{top_first_contact[0][0]} has {top_first_contact[0][1]}/{total_first_contact_weight} first-contact weight; opener should stay broadly randomized",
            ))
        if args.max_first_contact_person_share > 0 and total_first_contact_weight and top_first_contact:
            top_share = top_first_contact[0][1] / total_first_contact_weight
            if top_share > args.max_first_contact_person_share:
                issues.append((
                    "FIRST_CONTACT_TOP_SHARE",
                    f"{top_first_contact[0][0]} has {top_first_contact[0][1]}/{total_first_contact_weight} first-contact weight ({top_share:.1%}); expected at most {args.max_first_contact_person_share:.1%}",
                ))
        always_on_first_contact_total = always_on_first_contact_visible_weight + first_contact_silent_weight
        if (
            args.max_first_contact_person_share > 0
            and always_on_first_contact_total
            and top_always_on_first_contact
        ):
            top_always_on_share = top_always_on_first_contact[0][1] / always_on_first_contact_total
            if top_always_on_share > args.max_first_contact_person_share:
                issues.append((
                    "FIRST_CONTACT_ALWAYS_ON_TOP_SHARE",
                    f"{top_always_on_first_contact[0][0]} has {top_always_on_first_contact[0][1]}/{always_on_first_contact_total} baseline first-contact weight ({top_always_on_share:.1%}); expected at most {args.max_first_contact_person_share:.1%}",
                ))

    if set(router_people) != set(persons):
        issues.append((
            "ROUTER_PERSONS",
            f"cp_roll_for_event routes {sorted(router_people)}, but registered persons are {persons}",
        ))
    if sum(silent_weights) <= 0:
        issues.append((
            "ROUTER_SILENT",
            "cp_roll_for_event has no positive silent branch; ambient pacing needs a no-event branch",
        ))
    if len(conditional_entry_hooks) < 10:
        issues.append((
            "CONDITIONAL_ROSTER_SIZE",
            "the conditional roster needs at least ten entrants so Layla cannot remain the default lens",
        ))
    public_order_resolver = definitions_by_name.get("cp_roll_public_order_law_reaction", "")
    if not public_order_resolver:
        issues.append((
            "PUBLIC_ORDER_RESOLVER",
            "cp_roll_public_order_law_reaction is missing; Layla/Nabil public-order laws need one shared weighted resolver",
        ))
    else:
        for event_id in ("cp_layla.116", "cp_layla.117", "cp_layla.119", "cp_layla.120", "cp_nabil.20", "cp_nabil.30", "cp_nabil.40"):
            if event_id not in public_order_resolver:
                issues.append((
                    "PUBLIC_ORDER_RESOLVER_EVENT",
                    f"cp_roll_public_order_law_reaction does not route {event_id}",
                ))
        if "cp_shared_public_order_law_handled" not in public_order_resolver:
            issues.append((
                "PUBLIC_ORDER_RESOLVER_MARKER",
                "cp_roll_public_order_law_reaction does not set cp_shared_public_order_law_handled",
            ))
    if "cp_roll_public_order_law_reaction = yes" not in hook_call_blocks.get("law_enacted", ""):
        issues.append((
            "PUBLIC_ORDER_RESOLVER_CALL",
            "cp_on_law_enacted does not call cp_roll_public_order_law_reaction",
        ))
    for dispatcher in ("cp_layla_dispatch_law_enacted", "cp_nabil_dispatch_law_enacted"):
        if "cp_shared_public_order_law_handled" not in definitions_by_name.get(dispatcher, ""):
            issues.append((
                "PUBLIC_ORDER_DIRECT_GUARD",
                f"{dispatcher} does not guard public-order law reactions with cp_shared_public_order_law_handled",
            ))
    for person in persons:
        alive_guard = f"cp_person_is_alive = {{ person = {person} }}"
        if alive_guard not in monthly_router:
            issues.append(("ROUTER_ALIVE_GUARD", f"cp_roll_for_event does not use {alive_guard}"))

    for person in persons:
        memory = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        events_file = MOD / "events" / f"cp_{person}_events.txt"
        loc = MOD / "localization" / "english" / f"cp_{person}_l_english.yml"
        definitions = memory_definitions_by_person.get(person, set())
        blocks = person_events[person]
        visible = [block for block in blocks if visible_event(block)]
        images = [block for block in visible if IMAGE_RE.search(str(block["text"]))]
        loc_count = len([key for key in all_loc_keys if person_owns_loc_key(person, key)])
        visible_ids = sorted(str(block["id"]) for block in visible)
        debugged_visible = sorted(event_id for event_id in visible_ids if event_id in debug_event_ids)

        print(
            f"- {person}: events={len(blocks)} visible={len(visible)} images={len(images)} "
            f"loc_keys={loc_count} debug_visible={len(debugged_visible)}"
        )

        for path in (memory, events_file, loc):
            if not path.exists():
                issues.append(("PERSON_FILE", f"{person} is missing {rel(path)}"))

        if events_file.exists():
            event_text = uncommented_text(events_file.read_text(encoding="utf-8-sig", errors="replace"))
            if f"namespace = cp_{person}" not in event_text:
                issues.append(("PERSON_NAMESPACE", f"{rel(events_file)} does not declare namespace = cp_{person}"))

        required_defs = {f"cp_{person}_refresh_sol", f"cp_roll_ambient_{person}"}
        required_defs.update(f"cp_{person}_dispatch_{hook}" for hook in PERSON_HOOKS)
        for definition in sorted(required_defs - definitions):
            issues.append(("PERSON_MEMORY_DEF", f"{person} is missing {definition} in {rel(memory)}"))

        yearly_definition = definitions_by_name.get(f"cp_{person}_dispatch_yearly", "")
        if person != "layla" and not effect_call_has_params(
            yearly_definition,
            "cp_person_yearly_lifecycle",
            {"person": person, "country": "EGY"},
        ):
            issues.append((
                "PERSON_YEARLY_LIFECYCLE",
                f"{person}'s yearly dispatcher does not call cp_person_yearly_lifecycle with person = {person} and country = EGY",
            ))

        try_spawn = f"cp_{person}_try_spawn"
        has_startup_entry = startup_registers_person(startup_text, person)
        has_try_spawn_definition = try_spawn in definitions
        try_spawn_hooks = conditional_entry_hooks.get(person, [])
        has_conditional_entry = has_try_spawn_definition and bool(try_spawn_hooks)
        if not has_startup_entry and not has_conditional_entry:
            issues.append((
                "PERSON_ENTRY",
                f"{person} has no shared-startup registration and no called {try_spawn} conditional entry path",
            ))
        if not has_startup_entry and has_try_spawn_definition:
            if "startup" not in try_spawn_hooks:
                issues.append((
                    "CONDITIONAL_STARTUP_SCAN",
                    f"{person}'s {try_spawn} is not called from the startup conditional scan; eligible start dates should be able to meet them before the first-contact roll",
                ))
            if not any(person_owns_event(person, event_id) for event_id in first_contact_targets):
                issues.append((
                    "CONDITIONAL_FIRST_CONTACT",
                    f"{person} has no first-contact branch in cp_shared_startup.2; startup-eligible conditional persons should be able to become the campaign opener",
                ))
            if "yearly" not in try_spawn_hooks:
                issues.append((
                    "CONDITIONAL_YEARLY_ENTRY",
                    f"{person}'s {try_spawn} is not called from cp_on_yearly; date/state entrants need annual polling",
                ))
            if not any(hook in try_spawn_hooks for hook in SITUATION_ENTRY_HOOKS):
                issues.append((
                    "CONDITIONAL_SITUATION_ENTRY",
                    f"{person}'s {try_spawn} is only annual; conditional entrants also need a law/war/tech/building/revolution hook",
                ))
            spawn_definition = definitions_by_name.get(try_spawn, "")
            if spawn_definition_uses_modernization(spawn_definition) and not any(
                hook in try_spawn_hooks for hook in MODERNIZATION_ENTRY_HOOKS
            ):
                issues.append((
                    "CONDITIONAL_MODERNIZATION_ENTRY",
                    f"{person}'s {try_spawn} depends on modernization markers but is not called from cp_on_tech or cp_on_building_built",
                ))
            setup = find_person_setup_event(person, events_by_id, definitions_by_name)
            setup_text = str(setup["text"]) if setup else ""
            visible_chance_weight = 0
            silent_chance_weight = 0
            for weight, body in weighted_random_list_entries(setup_text):
                targets = event_targets(body)
                if not targets:
                    silent_chance_weight += weight
                    continue
                if any(person_owns_event(person, event_id) for event_id in targets):
                    visible_chance_weight += weight
            if visible_chance_weight <= 0 or silent_chance_weight <= 0:
                issues.append((
                    "CONDITIONAL_FIRST_APPEARANCE_CHANCE",
                    f"{person}'s setup event should randomize its first visible appearance with a positive silent branch",
                ))

        setup = find_person_setup_event(person, events_by_id, definitions_by_name)
        if not setup:
            issues.append((
                "PERSON_SETUP",
                f"{person} has no hidden setup event that initializes cp_{person}_alive and establishes cp_{person}_lives_here",
            ))
        else:
            setup_id = str(setup["id"])
            if has_startup_entry and not block_triggers_event(startup_text, setup_id):
                issues.append((
                    "PERSON_SETUP_ENTRY",
                    f"{person} is registered in cp_shared_startup.1 but that startup path does not trigger setup event {setup_id}",
                ))
            if has_conditional_entry and not block_triggers_event(definitions_by_name.get(try_spawn, ""), setup_id):
                issues.append((
                    "PERSON_SETUP_ENTRY",
                    f"{person} enters through {try_spawn} but that conditional path does not trigger setup event {setup_id}",
                ))
        for hook, block_text in hook_call_blocks.items():
            call = f"cp_{person}_dispatch_{hook} = yes"
            if call not in block_text:
                issues.append(("PERSON_HOOK_CALL", f"{person} is not called from the shared {hook} dispatcher"))
            if hook != "startup" and f"cp_person_is_alive = {{ person = {person} }}" not in block_text:
                issues.append(("PERSON_HOOK_GUARD", f"{person}'s {hook} dispatcher is not guarded by cp_person_is_alive"))

        missing_debug = sorted(set(visible_ids) - debug_event_ids)
        if missing_debug:
            issues.append((
                "PERSON_DEBUG",
                f"{person} visible events lack debug QA coverage: {describe_event_ids(missing_debug, args.list_missing_debug)}",
            ))

        if not visible:
            issues.append(("PERSON_VISIBLE", f"{person} has no visible events"))
        if len(visible) < args.min_visible_events:
            issues.append((
                "PERSON_VISIBLE_BASELINE",
                f"{person} has {len(visible)} visible events; expected at least {args.min_visible_events}",
            ))
        if visible and len(images) != len(visible):
            warnings.append(("PERSON_IMAGE", f"{person} has {len(visible) - len(images)} visible events without event_image"))
        if loc_count == 0:
            issues.append(("PERSON_LOC", f"{person} has no localization keys with prefix cp_{person}."))

    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    print(f"Warnings: {len(warnings)}")
    for code, message in warnings:
        print(f"[WARN] {code}: {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
