#!/usr/bin/env python3
"""Audit repeat-control coverage for visible Common People events."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
COMMON = MOD / "common"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
CP_YES_CALL_RE = re.compile(r"^\s*(cp_[A-Za-z0-9_]+)\s*=\s*yes\b", re.M)
MARK_SEEN_RE = re.compile(r"\bcp_mark_event_seen\b")
HAS_NOT_VAR_RE = re.compile(r"\bNOT\s*=\s*\{\s*has_variable\s*=\s*(cp_[A-Za-z0-9_]+)\s*\}", re.S)
SET_VAR_RE = re.compile(
    r"\bset_variable\s*=\s*(cp_[A-Za-z0-9_]+)\b"
    r"|\bset_variable\s*=\s*\{[^}]*?\bname\s*=\s*(cp_[A-Za-z0-9_]+)\b",
    re.S,
)
COOLDOWN_RE = re.compile(r"\bcp_[A-Za-z0-9_]+_(?:button|audience)_cooldown\b")
TERMINAL_RE = re.compile(
    r"\bcp_(?:[A-Za-z0-9_]+_dies|person_dies|ahmed_killed|child_dies|ahmed_homecoming)\b"
    r"|\bset_variable\s*=\s*\{[^}]*?\bname\s*=\s*cp_[A-Za-z0-9_]+_alive\s+value\s*=\s*0\b",
    re.S,
)

INTENTIONAL_REPEATABLE = {
    "cp_layla.40": "war-end homecoming can recur after a later conscription",
    "cp_layla.91": "welfare-up reaction follows each welfare ladder increase",
    "cp_layla.92": "welfare-down reaction follows each welfare ladder decrease",
}


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def first_group(match: re.Match[str]) -> str:
    return next(group for group in match.groups() if group)


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


def event_files() -> list[Path]:
    return sorted(EVENTS.glob("*.txt"))


def common_files() -> list[Path]:
    return sorted(COMMON.glob("**/*.txt"))


def is_debug_event_id(event_id: str) -> bool:
    return event_id == "cp_debug.1" or event_id.startswith("cp_debug.") or event_id.startswith("cp_debug_")


def is_debug_script_file(path: Path) -> bool:
    return path.name.startswith("cp_debug")


def is_visible_non_debug(block: dict[str, object]) -> bool:
    event_id = str(block["id"])
    text = str(block["text"])
    return not is_debug_event_id(event_id) and not re.search(r"\bhidden\s*=\s*yes\b", text) and bool(OPTION_RE.search(text))


def effect_definitions() -> dict[str, str]:
    definitions: dict[str, str] = {}
    for folder in ("scripted_effects", "scripted_triggers"):
        for path in sorted((COMMON / folder).glob("*.txt")):
            for block in iter_blocks(path, TOP_LEVEL_BLOCK_RE):
                definitions[str(block["id"])] = uncommented_text(str(block["text"]))
    return definitions


def expanded_text(text: str, definitions: dict[str, str], seen: set[str] | None = None) -> str:
    clean = uncommented_text(text)
    seen = set() if seen is None else set(seen)
    chunks = [clean]
    for call in CP_YES_CALL_RE.findall(clean):
        if call in seen or call not in definitions:
            continue
        seen.add(call)
        chunks.append(expanded_text(definitions[call], definitions, seen))
    return "\n".join(chunks)


def set_vars(text: str) -> set[str]:
    return {first_group(match) for match in SET_VAR_RE.finditer(text)}


def guarded_vars(text: str) -> set[str]:
    return set(HAS_NOT_VAR_RE.findall(text))


def source_windows(event_id: str) -> list[tuple[str, bool, str]]:
    windows: list[tuple[str, bool, str]] = []
    for path in common_files():
        if is_debug_script_file(path):
            continue
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for match in list(TRIGGER_EVENT_RE.finditer(text)) + list(GATEKEEPER_EVENT_RE.finditer(text)):
            if match.group(1) != event_id:
                continue
            windows.append((text[max(0, match.start() - 1200) : match.end() + 1200], False, rel(path)))

    for path in event_files():
        if is_debug_script_file(path):
            continue
        for block in iter_blocks(path, EVENT_DEF_RE):
            source_id = str(block["id"])
            if is_debug_event_id(source_id):
                continue
            text = uncommented_text(str(block["text"]))
            source_is_visible = is_visible_non_debug(block)
            for match in list(TRIGGER_EVENT_RE.finditer(text)) + list(GATEKEEPER_EVENT_RE.finditer(text)):
                if match.group(1) != event_id:
                    continue
                windows.append((text[max(0, match.start() - 1200) : match.end() + 1200], source_is_visible, source_id))
    return windows


def classify_event(block: dict[str, object], definitions: dict[str, str]) -> tuple[str, str]:
    event_id = str(block["id"])
    expanded = expanded_text(str(block["text"]), definitions)
    event_set_vars = set_vars(expanded)
    if MARK_SEEN_RE.search(expanded):
        return "self_seen_marker", "cp_mark_event_seen"
    self_latches = guarded_vars(expanded) & set_vars(expanded)
    if self_latches:
        return "self_latch", ", ".join(sorted(self_latches)[:3])
    if COOLDOWN_RE.search(expanded):
        return "self_cooldown", COOLDOWN_RE.search(expanded).group(0)
    if TERMINAL_RE.search(expanded):
        return "terminal_or_state_change", TERMINAL_RE.search(expanded).group(0)
    if event_id in INTENTIONAL_REPEATABLE:
        return "intentional_repeatable", INTENTIONAL_REPEATABLE[event_id]

    visible_sources = False
    for window, source_is_visible, source in source_windows(event_id):
        if source_is_visible:
            visible_sources = True
            continue
        window_latches = guarded_vars(window) & set_vars(window)
        if window_latches:
            return "upstream_latch", f"{source}: {', '.join(sorted(window_latches)[:3])}"
        upstream_guard_event_sets = guarded_vars(window) & event_set_vars
        if upstream_guard_event_sets:
            return "upstream_guard_event_sets", f"{source}: {', '.join(sorted(upstream_guard_event_sets)[:3])}"
        if COOLDOWN_RE.search(window):
            return "upstream_cooldown", f"{source}: {COOLDOWN_RE.search(window).group(0)}"
        if "cp_shared_startup" in source:
            return "startup_once", source

    if visible_sources:
        return "visible_chain_followup", "opened from a visible parent event option"
    return "uncontrolled_entry", "no self/upstream latch, cooldown, terminal state, or visible parent chain found"


def main() -> int:
    definitions = effect_definitions()
    issues: list[tuple[str, str]] = []
    counts: Counter[str] = Counter()
    examples: defaultdict[str, list[str]] = defaultdict(list)

    for path in event_files():
        for block in iter_blocks(path, EVENT_DEF_RE):
            if not is_visible_non_debug(block):
                continue
            category, detail = classify_event(block, definitions)
            counts[category] += 1
            if len(examples[category]) < 8:
                examples[category].append(f"{str(block['id'])} at {rel(path)}:{block['line']} ({detail})")
            if category == "uncontrolled_entry":
                issues.append((category, f"{str(block['id'])} at {rel(path)}:{block['line']}: {detail}"))

    print("Common People event repeatability audit")
    print(f"Visible non-debug events: {sum(counts.values())}")
    for category, count in sorted(counts.items()):
        print(f"{category}: {count}")
        for example in examples[category]:
            print(f"  - {example}")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
