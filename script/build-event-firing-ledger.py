#!/usr/bin/env python3
"""Build and check a production firing ledger for visible Common People events."""

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
LEDGER = ROOT / "documentation" / "event-firing-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
TOP_LEVEL_BLOCK_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
LOC_FIELD_RE = re.compile(r"\btitle\s*=\s*([A-Za-z0-9_.-]+)")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+\"(.*)\"")


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


def classify_source(path: Path, source_id: str, source_text: str, match_start: int, target: str) -> str:
    window = source_text[max(0, match_start - 500) : match_start + 500]
    source_clean = uncommented_text(source_text)
    source_visible = bool(OPTION_RE.search(source_clean)) and not re.search(r"\bhidden\s*=\s*yes\b", source_clean)
    target_person = person_for_event(target)

    if "cp_try_fire_ambient" in window:
        return "ambient"
    if "cp_try_fire_law_reaction" in window:
        return "law_reaction"
    if "cp_try_fire_world_response" in window:
        return "world_response"
    if "cp_try_fire_milestone" in window:
        return "milestone"
    if "cp_button_fire" in window:
        return "button"
    if "cp_shared_startup.2" in source_id or "cp_shared_startup.2" in window:
        return "first_contact"
    if re.search(r"\bhidden\s*=\s*yes\b", source_clean):
        if source_id == f"cp_{target_person}.1":
            return "setup_first_appearance"
        if f"cp_{target_person}." in source_id or f"cp_{target_person}_" in source_id:
            return "hidden_person_router"
        return "hidden_direct"
    if source_visible:
        return "visible_chain"
    if "cp_debug" in str(path):
        return "debug"
    return "direct"


def collect_sources() -> dict[str, list[dict[str, str]]]:
    sources: dict[str, list[dict[str, str]]] = defaultdict(list)

    events = set(event_files())
    for path in common_files() + event_files():
        if is_debug_script_file(path):
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")

        if path in events:
            blocks = list(iter_blocks(path, EVENT_DEF_RE))
            for block in blocks:
                source_id = str(block["id"])
                if is_debug_event_id(source_id):
                    continue
                block_text = uncommented_text(str(block["text"]))
                for regex in (TRIGGER_EVENT_RE, GATEKEEPER_EVENT_RE):
                    for match in regex.finditer(block_text):
                        target = match.group(1)
                        route = classify_source(path, source_id, block_text, match.start(), target)
                        sources[target].append({
                            "route": route,
                            "source": source_id,
                            "location": f"{rel(path)}:{block['line']}",
                        })
            continue

        for block in iter_blocks(path, TOP_LEVEL_BLOCK_RE):
            source_id = str(block["id"])
            block_text = uncommented_text(str(block["text"]))
            for regex in (TRIGGER_EVENT_RE, GATEKEEPER_EVENT_RE):
                for match in regex.finditer(block_text):
                    target = match.group(1)
                    route = classify_source(path, source_id, block_text, match.start(), target)
                    line = int(block["line"]) + line_no_for_offset(block_text, match.start()) - 1
                    sources[target].append({
                        "route": route,
                        "source": source_id,
                        "location": f"{rel(path)}:{line}",
                    })

    return sources


def source_summary(entries: list[dict[str, str]]) -> tuple[str, str]:
    if not entries:
        return "missing", "-"
    route_counts = Counter(entry["route"] for entry in entries)
    routes = ", ".join(f"{route}={count}" if count > 1 else route for route, count in sorted(route_counts.items()))
    samples = []
    seen: set[str] = set()
    for entry in entries:
        sample = f"`{entry['source']}` ({entry['location']})"
        if sample in seen:
            continue
        samples.append(sample)
        seen.add(sample)
        if len(samples) >= 3:
            break
    return routes, "<br>".join(samples)


def build() -> tuple[str, list[str]]:
    loc = loc_keys()
    sources = collect_sources()
    issues: list[str] = []
    rows: list[dict[str, object]] = []
    route_totals: Counter[str] = Counter()

    for path in event_files():
        for block in iter_blocks(path, EVENT_DEF_RE):
            if not is_visible_non_debug(block):
                continue
            event_id = str(block["id"])
            entries = [entry for entry in sources.get(event_id, []) if entry["route"] != "debug"]
            routes, source_text = source_summary(entries)
            if not entries:
                issues.append(f"{event_id} at {rel(Path(str(block['path'])))}:{block['line']} has no production route")
            for entry in entries:
                route_totals[entry["route"]] += 1
            rows.append({
                "event": event_id,
                "person": person_for_event(event_id),
                "title": title_for(block, loc),
                "routes": routes,
                "sources": source_text,
                "location": f"{rel(Path(str(block['path'])))}:{block['line']}",
            })

    person_counts = Counter(str(row["person"]) for row in rows)
    lines = [
        "# Event Firing Ledger",
        "",
        "Generated from live Paradox script. Rebuild with `python3 script/build-event-firing-ledger.py`.",
        "",
        "This ledger maps each visible non-debug event to its production route. Debug wrappers do not count as proof here.",
        "",
        "## Summary",
        "",
        f"- Visible non-debug events: {len(rows)}",
        f"- Events without production routes: {len(issues)}",
        f"- Persons with visible events: {len(person_counts)}",
        "",
        "## Route Counts",
        "",
    ]
    for route, count in sorted(route_totals.items()):
        lines.append(f"- `{route}`: {count}")

    lines.extend([
        "",
        "## Route Glossary",
        "",
        "- `first_contact`: visible event selected by the startup first-contact roll.",
        "- `ambient`: visible event selected by a person ambient pool through `cp_try_fire_ambient`.",
        "- `law_reaction`: visible event selected by a law dispatcher through `cp_try_fire_law_reaction`.",
        "- `world_response`: visible event selected by routine technology, building, conditional-entry, yearly, or public-order routing through `cp_try_fire_world_response`.",
        "- `milestone`: visible event selected by a critical yearly, war, mortality, family, crossroads, revolution, or other life-event dispatcher through `cp_try_fire_milestone`.",
        "- `button`: visible event selected by a player or QA button through `cp_button_fire`.",
        "- `setup_first_appearance`: visible event opened by that person's hidden setup event after a conditional entry roll.",
        "- `hidden_person_router`: visible event opened by a same-person hidden router, such as a conversation chooser.",
        "- `visible_chain`: visible event opened by another visible event in the same beat.",
        "",
        "",
        "## Person Event Counts",
        "",
    ])
    for person, count in sorted(person_counts.items()):
        lines.append(f"- `{person}`: {count}")

    lines.extend([
        "",
        "## Visible Event Routes",
        "",
        "| Event | Person | Title | Routes | Production Sources | Definition |",
        "|---|---|---|---|---|---|",
    ])
    for row in sorted(rows, key=lambda item: (str(item["person"]), str(item["event"]))):
        lines.append(
            f"| `{row['event']}` | {row['person']} | {row['title']} | {row['routes']} | {row['sources']} | `{row['location']}` |"
        )

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the generated ledger is stale or has route issues")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("event firing route issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-event-firing-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
