#!/usr/bin/env python3
"""Build a readable ledger for Common People's person-selection weights."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
LEDGER = ROOT / "documentation" / "person-selection-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
REGISTER_PERSON_RE = re.compile(r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*([A-Za-z0-9_]+)", re.S)
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
EFFECT_CALL_RE = re.compile(r"\b(cp_[A-Za-z0-9_]+)\s*=\s*(?:yes|\{)")

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

SENSOR_LABELS = {
    "cp_era_before_1850 = yes": "before 1850",
    "cp_era_1850_to_1880 = yes": "1850-1880",
    "cp_era_after_1880 = yes": "after 1880",
    "cp_country_has_manufacturing = yes": "manufacturing exists",
    "cp_country_has_factory_migration = yes": "factory migration pressure",
    "cp_country_has_machine_industry = yes": "machine industry exists",
    "cp_country_has_rail_infrastructure = yes": "rail infrastructure exists",
    "cp_country_has_telegraph = yes": "telegraph exists",
    "cp_country_has_port = yes": "port exists",
    "cp_country_has_steam_trade = yes": "steam trade exists",
    "cp_country_has_government_office = yes": "government office exists",
    "cp_country_has_modern_records = yes": "modern records exist",
    "cp_country_has_electric_service = yes": "electric service exists",
    "cp_country_has_telephone_network = yes": "telephone network exists",
    "cp_country_has_urban_growth = yes": "urban growth pressure",
    "cp_country_has_public_order_pressure = yes": "public-order pressure",
    "cp_country_old_land_order = yes": "old land order",
    "cp_country_workers_unprotected = yes": "workers unprotected",
    "cp_country_women_property_rights = yes": "women have property rights",
    "cp_country_public_schools = yes": "public schools",
    "cp_country_public_health = yes": "public health",
}


def label_condition(line: str) -> str:
    negated = re.match(r"NOT\s*=\s*\{\s*(.+?)\s*\}", line)
    if negated:
        inner = negated.group(1)
        return f"not {SENSOR_LABELS.get(inner, inner)}"
    return SENSOR_LABELS.get(line, line)


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


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


def named_top_level_block(path: Path, name: str) -> str:
    return top_level_block_texts(path).get(name, "")


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


def registered_persons() -> list[str]:
    text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    return sorted({match.group(1) for match in REGISTER_PERSON_RE.finditer(text)})


def startup_registers_person(startup_text: str, person: str) -> bool:
    return bool(re.search(rf"cp_register_person\s*=\s*\{{[^}}]*?\bperson\s*=\s*{re.escape(person)}\b", startup_text, re.S))


def person_owns_event(person: str, event_id: str) -> bool:
    prefix = f"cp_{person}"
    return event_id.startswith(f"{prefix}.") or event_id.startswith(f"{prefix}_")


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


def first_named_block(text: str, name: str) -> str:
    clean = uncommented_text(text)
    match = re.search(rf"\b{re.escape(name)}\s*=\s*\{{", clean)
    if not match:
        return ""
    pos = clean.find("{", match.start()) + 1
    start = pos
    depth = 1
    while pos < len(clean) and depth > 0:
        if clean[pos] == "{":
            depth += 1
        elif clean[pos] == "}":
            depth -= 1
        pos += 1
    return clean[start : pos - 1]


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def condition_summary(body: str, person: str | None = None) -> str:
    trigger = first_named_block(body, "trigger")
    if not trigger:
        return "always"

    lines: list[str] = []
    for raw_line in trigger.splitlines():
        line = " ".join(raw_line.split())
        if not line or line in {"{", "}"}:
            continue
        if person and f"cp_person_is_alive = {{ person = {person} }}" in line:
            continue
        if "cp_person_is_alive = {" in line:
            continue
        if line == "OR = {":
            lines.append("any of")
            continue
        if line == "AND = {":
            lines.append("all of")
            continue
        if line == "NOT = {":
            lines.append("not")
            continue
        if line == "}":
            continue
        lines.append(label_condition(line))

    summary = "; ".join(line for line in lines if line)
    summary = summary.replace("not; any of; ", "not any of: ")
    summary = summary.replace("not; all of; ", "not all of: ")
    summary = summary.replace("any of; ", "any of: ")
    summary = summary.replace("all of; ", "all of: ")
    return summary or "alive"


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
        clean = uncommented_text(text)
        calls = set(EFFECT_CALL_RE.findall(clean))
        if not block_or_called_effect_mentions(clean, home_marker, definitions):
            continue
        candidates.append(block)
    return sorted(candidates, key=lambda block: str(block["id"]))[0] if candidates else None


def event_link(block: dict[str, object] | None) -> str:
    if not block:
        return ""
    path = Path(block["path"]).relative_to(ROOT)
    return f"{path}:{block['line']}"


def event_targets(text: str) -> list[str]:
    clean = uncommented_text(text)
    return TRIGGER_EVENT_RE.findall(clean) + GATEKEEPER_EVENT_RE.findall(clean)


def build_markdown() -> str:
    persons = registered_persons()
    definitions_by_name = all_top_level_block_texts()
    events_by_id = {str(block["id"]): block for block in iter_event_blocks()}

    shared_firing = MOD / "common" / "scripted_effects" / "cp_shared_firing.txt"
    on_actions = MOD / "common" / "on_actions" / "cp_on_actions.txt"
    shared_war = MOD / "common" / "scripted_effects" / "cp_shared_war.txt"
    startup_text = str(events_by_id.get("cp_shared_startup.1", {}).get("text", ""))
    first_contact_text = str(events_by_id.get("cp_shared_startup.2", {}).get("text", ""))
    monthly_router = named_top_level_block(shared_firing, "cp_roll_for_event")
    hook_call_blocks = {
        "startup": startup_text,
        "yearly": named_top_level_block(on_actions, "cp_on_yearly"),
        "law_enacted": named_top_level_block(on_actions, "cp_on_law_enacted"),
        "war_started": named_top_level_block(shared_war, "cp_on_war_started_for_egy"),
        "war_end": named_top_level_block(on_actions, "cp_on_war_end"),
        "tech": named_top_level_block(on_actions, "cp_on_tech"),
        "building": named_top_level_block(on_actions, "cp_on_building_built"),
        "revolution": named_top_level_block(on_actions, "cp_on_revolution"),
    }

    out: list[str] = [
        "# Person Selection Ledger",
        "",
        "Generated from live Paradox script. Rebuild with `python3 script/build-person-selection-ledger.py`.",
        "",
        "## First Contact",
        "",
    ]

    first_entries = weighted_random_list_entries(first_contact_text)
    first_total = sum(weight for weight, _body in first_entries)
    first_silent_weight = 0
    first_person_weights: dict[str, int] = {}
    always_on_people = {person for person in persons if startup_registers_person(startup_text, person)}
    for weight, body in first_entries:
        targets = TRIGGER_EVENT_RE.findall(body)
        if not targets:
            first_silent_weight += weight
            continue
        for event_id in targets:
            owner = next((person for person in persons if person_owns_event(person, event_id)), "unknown")
            if owner != "unknown":
                first_person_weights[owner] = first_person_weights.get(owner, 0) + weight

    first_visible_weight = sum(first_person_weights.values())
    first_top = max(first_person_weights.items(), key=lambda item: item[1]) if first_person_weights else None
    always_on_weights = {
        person: weight for person, weight in first_person_weights.items() if person in always_on_people
    }
    always_on_visible_weight = sum(always_on_weights.values())
    always_on_total = always_on_visible_weight + first_silent_weight
    always_on_top = max(always_on_weights.items(), key=lambda item: item[1]) if always_on_weights else None
    first_top_text = (
        f"`{first_top[0]}` at {first_top[1] / first_total * 100:.1f}%"
        if first_top and first_total
        else "none"
    )
    always_on_top_text = (
        f"`{always_on_top[0]}` at {always_on_top[1] / always_on_total * 100:.1f}%"
        if always_on_top and always_on_total
        else "none"
    )
    out.extend([
        f"All-candidate roll: {len(first_person_weights)} visible candidates, visible weight {first_visible_weight}, silent weight {first_silent_weight}, top share {first_top_text}.",
        f"Always-on baseline if no conditional startup scan succeeds: {len(always_on_weights)} visible candidates, visible weight {always_on_visible_weight}, silent weight {first_silent_weight}, top share {always_on_top_text}.",
        "",
        "| Person | Event | Weight | Share | Gate |",
        "|---|---|---:|---:|---|",
    ])

    for weight, body in first_entries:
        targets = TRIGGER_EVENT_RE.findall(body)
        if not targets:
            share = f"{(weight / first_total * 100):.1f}%" if first_total else "0.0%"
            out.append(f"| silent | - | {weight} | {share} | no visible first contact |")
            continue
        for event_id in targets:
            owner = next((person for person in persons if person_owns_event(person, event_id)), "unknown")
            share = f"{(weight / first_total * 100):.1f}%" if first_total else "0.0%"
            out.append(
                f"| {owner} | `{event_id}` | {weight} | {share} | {md_escape(condition_summary(body, owner))} |"
            )

    out.extend([
        "",
        "## Monthly Ambient Router",
        "",
        "These weights pick whose ambient pool gets a chance each month. The actual event still passes through the shared ambient cooldowns, so most eligible months remain quiet.",
        "",
        "| Person | Weight | Conditions | Pool |",
        "|---|---:|---|---|",
    ])

    for weight, body in weighted_random_list_entries(monthly_router):
        match = re.search(r"\bcp_roll_ambient_([A-Za-z0-9_]+)\s*=\s*yes\b", body)
        if not match:
            out.append(f"| silent | {weight} | always | no event |")
            continue
        person = match.group(1)
        out.append(
            f"| {person} | {weight} | {md_escape(condition_summary(body, person))} | `cp_roll_ambient_{person}` |"
        )

    out.extend([
        "",
        "## Conditional Entrants",
        "",
        "Conditional people are not always present in 1836. Their spawn effects are called from the startup scan and later hooks below, and their hidden setup events randomize whether a visible first appearance fires immediately or stays silent.",
        "",
        "| Person | Hooks | Setup Event | First Appearance Weight | Silent Weight | Immediate Visible Chance | Targets |",
        "|---|---|---|---:|---:|---:|---|",
    ])

    for person in persons:
        if startup_registers_person(startup_text, person):
            continue
        memory = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        definitions = top_level_definitions(memory) if memory.exists() else set()
        try_spawn = f"cp_{person}_try_spawn"
        if try_spawn not in definitions:
            continue
        hooks = [
            hook
            for hook in CONDITIONAL_ENTRY_HOOKS
            if block_or_called_effect_mentions(hook_call_blocks.get(hook, ""), try_spawn, definitions_by_name)
        ]
        setup = find_person_setup_event(person, events_by_id, definitions_by_name)
        setup_text = str(setup["text"]) if setup else ""
        visible_weight = 0
        silent_weight = 0
        targets: list[str] = []
        for weight, body in weighted_random_list_entries(setup_text):
            body_targets = event_targets(body)
            owned_targets = [target for target in body_targets if person_owns_event(person, target)]
            if owned_targets:
                visible_weight += weight
                targets.extend(owned_targets)
            elif not body_targets:
                silent_weight += weight
        total = visible_weight + silent_weight
        chance = f"{(visible_weight / total * 100):.1f}%" if total else "0.0%"
        target_text = ", ".join(f"`{target}`" for target in sorted(set(targets))) or "-"
        setup_id = str(setup["id"]) if setup else "-"
        setup_ref = event_link(setup)
        setup_text_md = f"`{setup_id}` ({setup_ref})" if setup_ref else f"`{setup_id}`"
        out.append(
            f"| {person} | {', '.join(hooks) or '-'} | {setup_text_md} | {visible_weight} | {silent_weight} | {chance} | {target_text} |"
        )

    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the ledger file is stale")
    args = parser.parse_args()

    markdown = build_markdown()
    if args.check:
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != markdown:
            print(f"stale: {LEDGER.relative_to(ROOT)}; run python3 script/build-person-selection-ledger.py")
            return 1
        print(f"ok: {LEDGER.relative_to(ROOT)} is current")
        return 0

    LEDGER.write_text(markdown, encoding="utf-8")
    print(f"wrote {LEDGER.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
