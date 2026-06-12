#!/usr/bin/env python3
"""Build and check Common People's live person hook-surface ledger."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
LEDGER = ROOT / "documentation" / "person-hook-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")

PERSON_HOOKS = (
    "startup",
    "monthly",
    "yearly",
    "law_enacted",
    "war_started",
    "war_end",
    "tech",
    "building",
    "revolution",
)
HOOK_LABELS = {
    "startup": "Startup",
    "monthly": "Monthly",
    "yearly": "Yearly",
    "law_enacted": "Law",
    "war_started": "War Start",
    "war_end": "War End",
    "tech": "Tech",
    "building": "Building",
    "revolution": "Revolution",
}
GATEKEEPERS = {
    "amb": "cp_try_fire_ambient",
    "law": "cp_try_fire_law_reaction",
    "world": "cp_try_fire_world_response",
    "mile": "cp_try_fire_milestone",
    "button": "cp_button_fire",
}


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
    if not path.exists():
        return blocks
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


def registered_persons() -> list[str]:
    text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    return sorted({match.group(1) for match in REGISTER_PERSON_RE.finditer(text)})


def visible_event(text: str) -> bool:
    return not re.search(r"\bhidden\s*=\s*yes\b", text) and bool(OPTION_RE.search(text))


def person_owns_event(person: str, event_id: str) -> bool:
    prefix = f"cp_{person}"
    return event_id.startswith(f"{prefix}.") or event_id.startswith(f"{prefix}_")


def gatekeeper_targets(text: str, gatekeeper: str) -> set[str]:
    clean = uncommented_text(text)
    pattern = re.compile(
        rf"\b{re.escape(gatekeeper)}\s*=\s*\{{[^}}]*?\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)",
        re.S,
    )
    return set(pattern.findall(clean))


def classify_block(text: str, event_visibility: dict[str, bool]) -> tuple[str, list[str], bool, int]:
    clean = uncommented_text(text)
    if not clean.strip():
        return "missing", ["missing hook block"], False, 0

    parts: list[str] = []
    issues: list[str] = []
    active_score = 0

    targets_by_kind = {
        kind: gatekeeper_targets(clean, gatekeeper)
        for kind, gatekeeper in GATEKEEPERS.items()
    }
    raw_targets = set(TRIGGER_EVENT_RE.findall(clean))
    gated_targets = set().union(*targets_by_kind.values())
    raw_targets -= gated_targets
    raw_visible = sorted(target for target in raw_targets if event_visibility.get(target, False))
    raw_hidden = sorted(target for target in raw_targets if not event_visibility.get(target, False))

    has_life = "cp_age_increment" in clean or re.search(r"\bcp_[A-Za-z0-9_]+_refresh_sol\s*=", clean)
    has_state = bool(
        re.search(
            r"\b(set_variable|change_variable|remove_variable|clamp_variable|cp_shift_|cp_refresh_|cp_move_to_state|cp_debug_tick_increment)\b",
            clean,
        )
    )
    noop = "cp_person_hook_noop = yes" in clean

    if noop and not any(targets_by_kind.values()) and not raw_targets and not has_life and not has_state:
        parts.append("noop")
    else:
        if noop:
            issues.append("active hook still contains cp_person_hook_noop")
        if has_life:
            parts.append("life")
            active_score += 1
        elif has_state:
            parts.append("state")
            active_score += 1
        for kind in ("amb", "law", "world", "mile", "button"):
            count = len(targets_by_kind[kind])
            if count:
                parts.append(f"{kind}:{count}")
                active_score += count
        if raw_hidden:
            parts.append(f"raw-hidden:{len(raw_hidden)}")
            active_score += len(raw_hidden)
        if raw_visible:
            parts.append(f"raw-visible:{len(raw_visible)}")
            issues.append("raw visible trigger_event bypasses gatekeepers")
            active_score += len(raw_visible)
        if not parts:
            parts.append("empty")
            issues.append("hook has no noop marker and no classified action")

    return "+".join(parts), issues, parts != ["noop"], active_score


def build() -> tuple[str, list[str]]:
    issues: list[str] = []
    persons = registered_persons()
    event_blocks = {str(block["id"]): block for block in iter_event_blocks()}
    event_visibility = {
        event_id: visible_event(str(block["text"]))
        for event_id, block in event_blocks.items()
    }

    rows: list[dict[str, object]] = []
    total_noop_hooks = 0
    total_active_hooks = 0
    total_raw_visible = 0
    layla_visible = 0
    non_layla_visible = 0

    for person in persons:
        memory_path = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        blocks = top_level_block_texts(memory_path)
        person_visible = sum(
            1
            for event_id, block in event_blocks.items()
            if person_owns_event(person, event_id) and visible_event(str(block["text"]))
        )
        if person == "layla":
            layla_visible += person_visible
        else:
            non_layla_visible += person_visible

        hook_cells: dict[str, str] = {}
        active_hooks = 0
        noop_hooks = 0
        active_score = 0

        if not memory_path.exists():
            issues.append(f"{person}: missing memory file {rel(memory_path)}")

        for hook in PERSON_HOOKS:
            block_name = f"cp_{person}_dispatch_{hook}"
            cell, block_issues, active, score = classify_block(blocks.get(block_name, ""), event_visibility)
            hook_cells[hook] = cell
            if active:
                active_hooks += 1
            elif cell == "noop":
                noop_hooks += 1
            active_score += score
            total_raw_visible += cell.count("raw-visible")
            for issue in block_issues:
                issues.append(f"{person}.{hook}: {issue}")

        ambient_name = f"cp_roll_ambient_{person}"
        ambient_cell, ambient_issues, _active, ambient_score = classify_block(
            blocks.get(ambient_name, ""), event_visibility
        )
        if "amb:" not in ambient_cell:
            issues.append(f"{person}: ambient pool has no cp_try_fire_ambient target")
        for issue in ambient_issues:
            issues.append(f"{person}.ambient: {issue}")

        try_spawn_name = f"cp_{person}_try_spawn"
        try_spawn_cell = "-"
        if try_spawn_name in blocks:
            try_spawn_cell, try_spawn_issues, _active, try_spawn_score = classify_block(
                blocks[try_spawn_name], event_visibility
            )
            active_score += try_spawn_score
            for issue in try_spawn_issues:
                # Hidden setup trigger_event is expected here; visible raw triggers are not.
                if "raw visible" in issue or "noop" in issue or "missing" in issue:
                    issues.append(f"{person}.try_spawn: {issue}")

        total_active_hooks += active_hooks
        total_noop_hooks += noop_hooks
        rows.append(
            {
                "person": person,
                "visible": person_visible,
                "active_hooks": active_hooks,
                "noop_hooks": noop_hooks,
                "active_score": active_score + ambient_score,
                "ambient": ambient_cell,
                "try_spawn": try_spawn_cell,
                "hooks": hook_cells,
            }
        )

    total_visible = layla_visible + non_layla_visible
    lines = [
        "# Person Hook Surface Ledger",
        "",
        "Generated from live Paradox script. Rebuild with `python3 script/build-person-hook-ledger.py`.",
        "",
        "This ledger shows what each registered person's standard hook surface actually does. The person contract ledger proves every hook exists; this file makes no-op hooks, maintenance hooks, world responses, law reactions, milestones, and raw triggers reviewable so Layla cannot quietly become a special infrastructure lane again.",
        "",
        "Cell key: `noop` means an intentional placeholder, `life` means yearly age/SoL maintenance, `state` means non-popup variable work, `amb:N`, `law:N`, `world:N`, `mile:N`, and `button:N` count unique events fired through the shared gatekeepers, and `raw-hidden:N` is allowed hidden setup plumbing. `raw-visible:N` is a failure because visible event windows must use a gatekeeper.",
        "",
        "## Summary",
        "",
        f"- Registered persons: {len(rows)}",
        f"- Dispatcher hooks inspected: {len(rows) * len(PERSON_HOOKS)}",
        f"- Active dispatcher hooks: {total_active_hooks}",
        f"- Intentional no-op dispatcher hooks: {total_noop_hooks}",
        f"- Visible person-owned events: {total_visible}",
        f"- Layla visible events: {layla_visible}",
        f"- Non-Layla visible events: {non_layla_visible}",
        f"- Raw visible hook triggers: {total_raw_visible}",
        f"- Ledger issues: {len(issues)}",
        "",
        "## Hook Matrix",
        "",
        "| Person | Startup | Monthly | Yearly | Law | War Start | War End | Tech | Building | Revolution | Ambient Pool | Try Spawn |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    for row in rows:
        hooks = row["hooks"]
        assert isinstance(hooks, dict)
        lines.append(
            "| {person} | {startup} | {monthly} | {yearly} | {law_enacted} | {war_started} | {war_end} | {tech} | {building} | {revolution} | {ambient} | {try_spawn} |".format(
                person=row["person"],
                startup=hooks["startup"],
                monthly=hooks["monthly"],
                yearly=hooks["yearly"],
                law_enacted=hooks["law_enacted"],
                war_started=hooks["war_started"],
                war_end=hooks["war_end"],
                tech=hooks["tech"],
                building=hooks["building"],
                revolution=hooks["revolution"],
                ambient=row["ambient"],
                try_spawn=row["try_spawn"],
            )
        )

    lines.extend(
        [
            "",
            "## Content Depth Backlog",
            "",
            "This table is deliberately descriptive, not a failing gate: a new person can land with a small scaffold, but the imbalance stays visible until the roster has enough authored beats to feel as grand as Layla's branch.",
            "",
            "| Person | Visible Events | Active Hooks | No-op Hooks | Hook Action Score |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['person']} | {row['visible']} | {row['active_hooks']} | {row['noop_hooks']} | {row['active_score']} |"
        )

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the generated ledger is stale or has hook issues")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("person hook ledger issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-person-hook-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
