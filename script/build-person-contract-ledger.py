#!/usr/bin/env python3
"""Build and check Common People's live person-contract ledger."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
LEDGER = ROOT / "documentation" / "person-contract-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
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
BASELINE_ATTRS = ("age", "hope", "exhaustion", "sol", "literacy", "radical", "loyalist")


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


def person_owns_event(person: str, event_id: str) -> bool:
    prefix = f"cp_{person}"
    return event_id.startswith(f"{prefix}.") or event_id.startswith(f"{prefix}_")


def visible_event(text: str) -> bool:
    return not re.search(r"\bhidden\s*=\s*yes\b", text) and bool(re.search(r"(?m)^\s*option\s*=", text))


def event_image_kind(text: str) -> str:
    if re.search(r"event_image\s*=\s*\{[^}]*\bvideo\s*=", text, re.S):
        return "video"
    if re.search(r"event_image\s*=\s*\{[^}]*\btexture\s*=", text, re.S):
        return "texture"
    return "missing"


def setup_event_for(
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
        if alive_init_re.search(text) and block_or_called_effect_mentions(text, home_marker, definitions):
            candidates.append(block)
    return sorted(candidates, key=lambda block: str(block["id"]))[0] if candidates else None


def startup_registers_person(startup_text: str, person: str) -> bool:
    return bool(re.search(rf"cp_register_person\s*=\s*\{{[^}}]*?\bperson\s*=\s*{re.escape(person)}\b", startup_text, re.S))


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


def yes_no(value: bool) -> str:
    return "yes" if value else "NO"


def ok_join(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def build() -> tuple[str, list[str]]:
    issues: list[str] = []
    persons = registered_persons()
    definitions = all_top_level_block_texts()
    shared_firing = MOD / "common" / "scripted_effects" / "cp_shared_firing.txt"
    on_actions = MOD / "common" / "on_actions" / "cp_on_actions.txt"
    shared_war = MOD / "common" / "scripted_effects" / "cp_shared_war.txt"
    startup_events = MOD / "events" / "cp_shared_startup_events.txt"
    monthly_router = named_top_level_block(shared_firing, "cp_roll_for_event")
    startup_text = startup_events.read_text(encoding="utf-8-sig", errors="replace")
    events_by_id = {str(block["id"]): block for block in iter_event_blocks()}
    debugged = debug_triggers()

    hook_blocks = {
        "startup": startup_text,
        "monthly": named_top_level_block(on_actions, "cp_on_monthly"),
        "law_enacted": named_top_level_block(on_actions, "cp_on_law_enacted"),
        "yearly": named_top_level_block(on_actions, "cp_on_yearly"),
        "war_started": named_top_level_block(shared_war, "cp_on_war_started_for_egy"),
        "war_end": named_top_level_block(on_actions, "cp_on_war_end"),
        "tech": named_top_level_block(on_actions, "cp_on_tech"),
        "building": named_top_level_block(on_actions, "cp_on_building_built"),
        "revolution": named_top_level_block(on_actions, "cp_on_revolution"),
    }

    rows: list[dict[str, object]] = []
    for person in persons:
        setup = setup_event_for(person, events_by_id, definitions)
        setup_id = str(setup["id"]) if setup else ""
        setup_text = str(setup["text"]) if setup else ""
        setup_path = Path(str(setup["path"])) if setup else Path()
        memory_path = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        memory_text = memory_path.read_text(encoding="utf-8-sig", errors="replace") if memory_path.exists() else ""
        memory_defs = top_level_block_texts(memory_path) if memory_path.exists() else {}

        entry = "startup" if startup_registers_person(startup_text, person) else "conditional"
        try_spawn = f"cp_{person}_try_spawn"
        try_spawn_hooks = [
            hook
            for hook in CONDITIONAL_ENTRY_HOOKS
            if block_or_called_effect_mentions(hook_blocks.get(hook, ""), try_spawn, definitions)
        ]

        person_events = [block for block in events_by_id.values() if person_owns_event(person, str(block["id"]))]
        visible = [block for block in person_events if visible_event(str(block["text"]))]
        motion = [block for block in visible if event_image_kind(str(block["text"])) == "video"]
        stills = [block for block in visible if event_image_kind(str(block["text"])) == "texture"]
        missing_images = [block for block in visible if event_image_kind(str(block["text"])) == "missing"]
        audio_ready = [
            block
            for block in visible
            if "on_created_soundeffect" in str(block["text"]) and "on_opened_soundeffect" in str(block["text"])
        ]
        debug_ready = [block for block in visible if str(block["id"]) in debugged]

        baseline_missing = [
            attr
            for attr in BASELINE_ATTRS
            if f"cp_{person}_{attr}" not in uncommented_text(setup_text)
        ]
        profession = bool(re.search(rf"\bcp_{re.escape(person)}_profession_[A-Za-z0-9_]+\b", setup_text))
        home = block_or_called_effect_mentions(setup_text, f"cp_{person}_lives_here", definitions)
        setup_contract = not baseline_missing and profession and home

        hook_defs = [hook for hook in PERSON_HOOKS if f"cp_{person}_dispatch_{hook}" in memory_defs]
        hook_calls = [
            hook
            for hook in PERSON_HOOKS
            if block_or_called_effect_mentions(hook_blocks.get(hook, ""), f"cp_{person}_dispatch_{hook}", definitions)
        ]
        yearly_text = memory_defs.get(f"cp_{person}_dispatch_yearly", "")
        yearly_lifecycle = (
            f"cp_age_increment = {{ person = {person} }}" in uncommented_text(yearly_text)
            and f"cp_{person}_refresh_sol = yes" in uncommented_text(yearly_text)
        )
        refresh = f"cp_{person}_refresh_sol" in memory_defs
        ambient = f"cp_roll_ambient_{person}" in memory_defs
        router_branches = len(re.findall(rf"\bcp_roll_ambient_{re.escape(person)}\s*=\s*yes\b", monthly_router))
        first_visible_weight = 0
        first_silent_weight = 0
        for weight, body in weighted_random_list_entries(setup_text):
            targets = event_targets(body)
            if any(person_owns_event(person, event_id) for event_id in targets):
                first_visible_weight += weight
            elif not targets:
                first_silent_weight += weight

        if not setup:
            issues.append(f"{person}: missing hidden setup event")
        if not setup_contract:
            issues.append(f"{person}: setup contract missing {ok_join(baseline_missing)} profession={profession} home={home}")
        missing_hook_defs = sorted(set(PERSON_HOOKS) - set(hook_defs))
        missing_hook_calls = sorted(set(PERSON_HOOKS) - set(hook_calls))
        if missing_hook_defs:
            issues.append(f"{person}: missing hook definitions {ok_join(missing_hook_defs)}")
        if missing_hook_calls:
            issues.append(f"{person}: missing shared hook calls {ok_join(missing_hook_calls)}")
        if not yearly_lifecycle:
            issues.append(f"{person}: yearly dispatch does not age and refresh SoL")
        if not refresh or not ambient or router_branches <= 0:
            issues.append(f"{person}: missing refresh/ambient/router coverage")
        if visible and len(audio_ready) != len(visible):
            issues.append(f"{person}: not all visible events have audio hooks")
        if visible and len(debug_ready) != len(visible):
            issues.append(f"{person}: not all visible events have generated debug coverage")
        if missing_images:
            issues.append(f"{person}: visible events without event_image")
        if entry == "conditional" and (not try_spawn_hooks or first_visible_weight <= 0 or first_silent_weight <= 0):
            issues.append(f"{person}: conditional entry lacks hooks or visible/silent first-appearance weights")

        rows.append({
            "person": person,
            "entry": entry,
            "try_spawn_hooks": try_spawn_hooks,
            "setup": f"`{setup_id}` ({rel(setup_path)}:{setup['line']})" if setup else "missing",
            "setup_contract": setup_contract,
            "baseline_missing": baseline_missing,
            "hook_defs": len(hook_defs),
            "hook_calls": len(hook_calls),
            "yearly_lifecycle": yearly_lifecycle,
            "router_branches": router_branches,
            "events": len(person_events),
            "visible": len(visible),
            "audio": len(audio_ready),
            "motion": len(motion),
            "stills": len(stills),
            "debug": len(debug_ready),
            "first_visible_weight": first_visible_weight,
            "first_silent_weight": first_silent_weight,
        })

    total_visible = sum(int(row["visible"]) for row in rows)
    total_motion = sum(int(row["motion"]) for row in rows)
    conditional = [row for row in rows if row["entry"] == "conditional"]
    always_on = [row for row in rows if row["entry"] == "startup"]

    lines = [
        "# Person Contract Ledger",
        "",
        "Generated from live Paradox script. Rebuild with `python3 script/build-person-contract-ledger.py`.",
        "",
        "This ledger proves that Layla is not on a special infrastructure lane: every registered person has the same setup, hook, yearly lifecycle, ambient routing, audio/art, and generated QA surfaces.",
        "",
        "## Summary",
        "",
        f"- Registered persons: {len(rows)}",
        f"- Always-on startup persons: {len(always_on)}",
        f"- Conditional entrants: {len(conditional)}",
        f"- Visible person-owned events: {total_visible}",
        f"- Moving event-window scenes: {total_motion}",
        f"- Contract issues: {len(issues)}",
        "",
        "## Life Contract Matrix",
        "",
        "| Person | Entry | Setup | Setup Vars | Hooks | Yearly Life | Router | Events | Audio | Art | Debug |",
        "|---|---|---|---|---:|---|---:|---:|---:|---|---:|",
    ]

    for row in rows:
        art = f"{row['motion']} video / {row['stills']} still"
        lines.append(
            "| {person} | {entry} | {setup} | {setup_vars} | {hooks}/9 | {yearly} | {router} | {visible} | {audio}/{visible} | {art} | {debug}/{visible} |".format(
                person=row["person"],
                entry=row["entry"],
                setup=row["setup"],
                setup_vars=yes_no(bool(row["setup_contract"])),
                hooks=min(int(row["hook_defs"]), int(row["hook_calls"])),
                yearly=yes_no(bool(row["yearly_lifecycle"])),
                router=row["router_branches"],
                visible=row["visible"],
                audio=row["audio"],
                art=art,
                debug=row["debug"],
            )
        )

    lines.extend([
        "",
        "## Conditional Entry Chances",
        "",
        "| Person | Entry Hooks | Immediate Visible Weight | Silent Weight |",
        "|---|---|---:|---:|",
    ])
    for row in conditional:
        lines.append(
            f"| {row['person']} | {ok_join(list(row['try_spawn_hooks']))} | {row['first_visible_weight']} | {row['first_silent_weight']} |"
        )

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the generated ledger is stale or contract issues exist")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("person contract issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-person-contract-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
