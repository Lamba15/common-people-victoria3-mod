#!/usr/bin/env python3
"""Build and check a ledger of game-world routes into visible person events."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
COMMON = MOD / "common"
LEDGER = ROOT / "documentation" / "world-response-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
TOP_LEVEL_BLOCK_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
LOC_FIELD_RE = re.compile(r"\btitle\s*=\s*([A-Za-z0-9_.-]+)")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+\"(.*)\"")
CONTEXT_BLOCK_START_RE = re.compile(r"(?m)^\s*(?:if|else_if)\s*=\s*\{")

SIGNAL_PATTERNS = (
    (re.compile(r"ROOT\.currently_enacting_law\.type\s*\?=\s*law_type:([A-Za-z0-9_]+)"), "law"),
    (re.compile(r"has_law\s*=\s*law_type:([A-Za-z0-9_]+)"), "has_law"),
    (re.compile(r"has_technology_researched\s*=\s*([A-Za-z0-9_]+)"), "tech"),
    (re.compile(r"is_building_type\s*=\s*([A-Za-z0-9_]+)"), "building"),
    (re.compile(r"is_building_group\s*=\s*([A-Za-z0-9_]+)"), "building_group"),
    (re.compile(r"\b(cp_country_[A-Za-z0-9_]+)\s*=\s*yes"), "sensor"),
    (re.compile(r"\b(cp_era_[A-Za-z0-9_]+)\s*=\s*yes"), "era"),
    (re.compile(r"\bgame_date\s*([<>=.]+)\s*([0-9.]+)"), "date"),
    (re.compile(r"\bhas_variable\s*=\s*(cp_[A-Za-z0-9_]+)"), "var"),
    (re.compile(r"\bNOT\s*=\s*\{\s*has_variable\s*=\s*(cp_[A-Za-z0-9_]+)\s*\}"), "not_var"),
)

NOISE_VARIABLE_FRAGMENTS = (
    "_alive",
    "_button_cooldown",
    "_met_player",
    "_seen_",
    "cp_debug_",
    "cp_first_contact_",
    "cp_global_ambient_cooldown",
    "cp_person_",
    "cp_startup_conditional_scan",
)

WORLD_STATE_HOOKS = {
    "building_built",
    "conditional_setup",
    "law_enacted",
    "revolution",
    "technology",
    "war_end",
    "war_started",
    "yearly_or_date",
}


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def event_files() -> list[Path]:
    return sorted(EVENTS.glob("*.txt"))


def common_files() -> list[Path]:
    return sorted(COMMON.glob("**/*.txt"))


def iter_blocks(path: Path, pattern: re.Pattern[str]):
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        match = pattern.match(lines[i])
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


def line_no_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def is_debug_event_id(event_id: str) -> bool:
    return event_id == "cp_debug.1" or event_id.startswith("cp_debug.") or event_id.startswith("cp_debug_")


def is_debug_script_file(path: Path) -> bool:
    return path.name.startswith("cp_debug")


def is_visible_non_debug(block: dict[str, object]) -> bool:
    event_id = str(block["id"])
    text = str(block["text"])
    return not is_debug_event_id(event_id) and not re.search(r"\bhidden\s*=\s*yes\b", text) and bool(OPTION_RE.search(text))


def loc_keys() -> dict[str, str]:
    keys: dict[str, str] = {}
    for path in sorted((MOD / "localization").glob("**/*.yml")):
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            match = LOC_KEY_RE.match(line)
            if match:
                keys[match.group(1)] = match.group(2)
    return keys


def title_for(block: dict[str, object], loc: dict[str, str]) -> str:
    match = LOC_FIELD_RE.search(uncommented_text(str(block["text"])))
    if not match:
        return "-"
    return loc.get(match.group(1), match.group(1)).replace("|", "\\|")


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if namespace.startswith("cp_"):
        namespace = namespace[3:]
    return namespace.split("_", 1)[0]


def hook_for_source(source_id: str, source_text: str, target: str) -> str:
    person = person_for_event(target)
    if source_id == "cp_shared_startup.2":
        return "startup_first_contact"
    if source_id == f"cp_{person}.1":
        return "conditional_setup"
    if source_id == f"cp_roll_ambient_{person}" or "cp_try_fire_ambient" in source_text:
        return "monthly_ambient"
    if source_id in {"cp_on_law_enacted", "cp_roll_public_order_law_reaction"} or source_id.endswith("_dispatch_law_enacted"):
        return "law_enacted"
    if source_id.endswith("_dispatch_tech") or source_id == "cp_on_tech":
        return "technology"
    if source_id.endswith("_dispatch_building") or source_id == "cp_on_building_built":
        return "building_built"
    if source_id.endswith("_dispatch_war_started") or source_id == "cp_on_war_started_for_egy":
        return "war_started"
    if source_id.endswith("_dispatch_war_end") or source_id == "cp_on_war_end":
        return "war_end"
    if source_id.endswith("_dispatch_revolution") or source_id == "cp_on_revolution":
        return "revolution"
    if source_id.endswith("_dispatch_yearly") or source_id == "cp_on_yearly":
        return "yearly_or_date"
    if source_id.endswith("_check_button") or "cp_button_fire" in source_text:
        return "button"
    if re.search(r"\bhidden\s*=\s*yes\b", source_text):
        return "hidden_person_router"
    if bool(OPTION_RE.search(source_text)) and not re.search(r"\bhidden\s*=\s*yes\b", source_text):
        return "visible_chain"
    return "direct_or_unknown"


def signal_summary(source_text: str, match_start: int) -> str:
    starts = [match.start() for match in CONTEXT_BLOCK_START_RE.finditer(source_text, 0, match_start)]
    start = starts[-1] if starts else max(0, match_start - 2500)
    window = source_text[start:match_start]
    signals: list[str] = []
    seen: set[str] = set()
    for regex, label in SIGNAL_PATTERNS:
        for match in regex.finditer(window):
            if label == "date":
                value = f"date {match.group(1)} {match.group(2)}"
            else:
                value = f"{label}:{match.group(1)}"
                if value.endswith("_"):
                    continue
                if label in {"var", "not_var"} and any(fragment in value for fragment in NOISE_VARIABLE_FRAGMENTS):
                    continue
            if value in seen:
                continue
            signals.append(value)
            seen.add(value)
            if len(signals) >= 8:
                return ", ".join(signals)
    return ", ".join(signals) if signals else "-"


def collect_routes() -> dict[str, list[dict[str, str]]]:
    routes: dict[str, list[dict[str, str]]] = defaultdict(list)
    events = set(event_files())
    for path in common_files() + event_files():
        if is_debug_script_file(path):
            continue

        if path in events:
            for block in iter_blocks(path, EVENT_DEF_RE):
                source_id = str(block["id"])
                if is_debug_event_id(source_id):
                    continue
                block_text = uncommented_text(str(block["text"]))
                for regex in (TRIGGER_EVENT_RE, GATEKEEPER_EVENT_RE):
                    for match in regex.finditer(block_text):
                        target = match.group(1)
                        routes[target].append({
                            "hook": hook_for_source(source_id, block_text, target),
                            "source": source_id,
                            "signals": signal_summary(block_text, match.start()),
                            "location": f"{rel(path)}:{block['line']}",
                        })
            continue

        for block in iter_blocks(path, TOP_LEVEL_BLOCK_RE):
            source_id = str(block["id"])
            block_text = uncommented_text(str(block["text"]))
            for regex in (TRIGGER_EVENT_RE, GATEKEEPER_EVENT_RE):
                for match in regex.finditer(block_text):
                    target = match.group(1)
                    line = int(block["line"]) + line_no_for_offset(block_text, match.start()) - 1
                    routes[target].append({
                        "hook": hook_for_source(source_id, block_text, target),
                        "source": source_id,
                        "signals": signal_summary(block_text, match.start()),
                        "location": f"{rel(path)}:{line}",
                    })
    return routes


def format_sources(entries: list[dict[str, str]]) -> str:
    samples: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        sample = f"`{entry['source']}` ({entry['location']})"
        if sample in seen:
            continue
        samples.append(sample)
        seen.add(sample)
        if len(samples) >= 3:
            break
    return "<br>".join(samples) if samples else "-"


def build() -> tuple[str, list[str]]:
    loc = loc_keys()
    routes = collect_routes()
    issues: list[str] = []
    rows: list[dict[str, str]] = []
    hook_counts: Counter[str] = Counter()
    person_counts: Counter[str] = Counter()
    person_hooks: dict[str, set[str]] = defaultdict(set)

    for path in event_files():
        for block in iter_blocks(path, EVENT_DEF_RE):
            if not is_visible_non_debug(block):
                continue
            event_id = str(block["id"])
            entries = routes.get(event_id, [])
            if not entries:
                issues.append(f"{event_id} at {rel(Path(str(block['path'])))}:{block['line']} has no world-response route")
                entries = []
            unknown = [entry for entry in entries if entry["hook"] == "direct_or_unknown"]
            if unknown:
                issues.append(f"{event_id} has unclassified route(s): {format_sources(unknown)}")

            hook_counter = Counter(entry["hook"] for entry in entries)
            hooks = ", ".join(f"{hook}={count}" if count > 1 else hook for hook, count in sorted(hook_counter.items())) or "missing"
            signals = []
            seen_signals: set[str] = set()
            for entry in entries:
                if entry["signals"] == "-" or entry["signals"] in seen_signals:
                    continue
                signals.append(entry["signals"])
                seen_signals.add(entry["signals"])
                if len(signals) >= 3:
                    break
            person = person_for_event(event_id)
            person_counts[person] += 1
            hook_counts.update(entry["hook"] for entry in entries)
            person_hooks[person].update(entry["hook"] for entry in entries)
            rows.append({
                "event": event_id,
                "person": person,
                "title": title_for(block, loc),
                "hooks": hooks,
                "signals": "<br>".join(signals) if signals else "-",
                "sources": format_sources(entries),
                "location": f"{rel(Path(str(block['path'])))}:{block['line']}",
            })

    startup_people = {person for person, hooks in person_hooks.items() if "startup_first_contact" in hooks}
    non_layla_startup_people = startup_people - {"layla"}
    world_people = {person for person, hooks in person_hooks.items() if hooks & WORLD_STATE_HOOKS}
    non_layla_world_people = world_people - {"layla"}
    for person in sorted(person_counts):
        if "startup_first_contact" not in person_hooks[person]:
            issues.append(f"{person} has visible events but no startup first-contact route")
        if not person_hooks[person] & WORLD_STATE_HOOKS:
            issues.append(f"{person} has visible events but no world-state response hook")
    if len(non_layla_startup_people) < 5:
        issues.append(f"first-contact roster has only {len(non_layla_startup_people)} non-Layla candidate(s)")
    if len(non_layla_world_people) < 5:
        issues.append(f"world-response roster has only {len(non_layla_world_people)} non-Layla participant(s)")

    lines = [
        "# World Response Ledger",
        "",
        "Generated from live Paradox script. Rebuild with `python3 script/build-world-response-ledger.py`.",
        "",
        "This ledger maps visible non-debug events to the game-world hooks and signals that can surface them. Debug wrappers do not count.",
        "",
        "## Summary",
        "",
        f"- Visible non-debug events: {len(rows)}",
        f"- Events with unclassified or missing routes: {len(issues)}",
        f"- Persons with visible events: {len(person_counts)}",
        "",
        "## Design Coverage",
        "",
        f"- Startup first-contact persons: {len(startup_people)} ({len(non_layla_startup_people)} non-Layla)",
        f"- Persons with world-state response hooks: {len(world_people)} ({len(non_layla_world_people)} non-Layla)",
        f"- Active world-state hook classes: {', '.join(f'`{hook}`' for hook in sorted(hook_counts.keys() & WORLD_STATE_HOOKS))}",
        "",
        "## Hook Counts",
        "",
    ]
    for hook, count in sorted(hook_counts.items()):
        lines.append(f"- `{hook}`: {count}")

    lines.extend([
        "",
        "## Person Event Counts",
        "",
    ])
    for person, count in sorted(person_counts.items()):
        lines.append(f"- `{person}`: {count}")

    lines.extend([
        "",
        "## Visible Event World Routes",
        "",
        "| Event | Person | Title | Hooks | Signals | Sources | Definition |",
        "|---|---|---|---|---|---|---|",
    ])
    for row in sorted(rows, key=lambda item: (item["person"], item["event"])):
        lines.append(
            f"| `{row['event']}` | {row['person']} | {row['title']} | {row['hooks']} | {row['signals']} | {row['sources']} | `{row['location']}` |"
        )

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the ledger is stale or has route issues")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("world-response route issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-world-response-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
