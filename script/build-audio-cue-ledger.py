#!/usr/bin/env python3
"""Build a review ledger of visible event audio cues."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
LOC = MOD / "localization" / "english"
DEFAULT_OUTPUT = ROOT / "documentation" / "audio-cue-ledger.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
TITLE_RE = re.compile(r"\btitle\s*=\s*([A-Za-z0-9_.-]+)")
OPENED_RE = re.compile(r'\bon_opened_soundeffect\s*=\s*"([^"]+)"')
LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.-]+):\d+\s+"(.*)"\s*$')
CUE_PREFIX = "event:/MUSIC/Stingers/events/"


@dataclass(frozen=True)
class Cue:
    event_id: str
    title_key: str
    title: str
    cue: str
    path: Path
    line: int


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def event_sort_key(event_id: str) -> tuple[str, int]:
    namespace, number = event_id.rsplit(".", 1)
    return namespace, int(number)


def unescape_loc(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\n", " ")


def load_localization() -> dict[str, str]:
    loc: dict[str, str] = {}
    for path in sorted(LOC.glob("*.yml")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for line in text.splitlines():
            match = LOC_RE.match(line)
            if match:
                loc[match.group(1)] = unescape_loc(match.group(2))
    return loc


def iter_event_blocks():
    for path in sorted(EVENTS.glob("*.txt")):
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

            yield match.group(1), path, start + 1, "\n".join(lines[start : i + 1])
            i += 1


def is_debug_event(event_id: str) -> bool:
    return event_id == "cp_debug.1" or event_id.startswith("cp_debug.") or event_id.startswith("cp_debug_")


def is_visible_non_debug(event_id: str, text: str) -> bool:
    if is_debug_event(event_id):
        return False
    if re.search(r"\bhidden\s*=\s*yes\b", text):
        return False
    return bool(OPTION_RE.search(text))


def collect_cues() -> list[Cue]:
    loc = load_localization()
    cues: list[Cue] = []
    for event_id, path, line, raw_text in iter_event_blocks():
        text = uncommented_text(raw_text)
        if not is_visible_non_debug(event_id, text):
            continue
        title_match = TITLE_RE.search(text)
        title_key = title_match.group(1) if title_match else "<missing>"
        opened = OPENED_RE.findall(text)
        sound = opened[0] if opened else "<missing>"
        cue = sound.removeprefix(CUE_PREFIX)
        cues.append(Cue(event_id, title_key, loc.get(title_key, title_key), cue, path, line))
    return sorted(cues, key=lambda cue: event_sort_key(cue.event_id))


def markdown_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_ledger(cues: list[Cue]) -> str:
    counts = Counter(cue.cue for cue in cues)
    lines = [
        "# Common People audio cue ledger",
        "",
        "Generated from visible non-debug event blocks. Regenerate with:",
        "",
        "```bash",
        "script/build-audio-cue-ledger.py",
        "script/build-audio-cue-ledger.py --check",
        "```",
        "",
        "## Palette Counts",
        "",
    ]
    for stinger, count in sorted(counts.items()):
        lines.append(f"- `{stinger}`: {count}")

    lines.extend([
        "",
        "## Event Cues",
        "",
        "| Event | Title | Cue | Source |",
        "|---|---|---|---|",
    ])
    for cue in cues:
        lines.append(
            f"| `{cue.event_id}` | {markdown_escape(cue.title)} | "
            f"`{cue.cue}` | `{rel(cue.path)}:{cue.line}` |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if the ledger is missing or stale")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else ROOT / args.output
    ledger = render_ledger(collect_cues())

    if args.check:
        if not output.exists():
            print(f"FAIL: {rel(output)} is missing")
            print("Run: script/build-audio-cue-ledger.py")
            return 1
        if output.read_text(encoding="utf-8") != ledger:
            print(f"FAIL: {rel(output)} is stale")
            print("Run: script/build-audio-cue-ledger.py")
            return 1
        print(f"ok: {rel(output)} is current")
        return 0

    output.write_text(ledger, encoding="utf-8")
    print(f"wrote {rel(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
