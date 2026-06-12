#!/usr/bin/env python3
"""Track vanilla video art debt in Common People event windows."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "mod" / "events"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
VIDEO_RE = re.compile(r'\bvideo\s*=\s*"([^"]+)"')
TITLE_RE = re.compile(r"\btitle\s*=\s*([A-Za-z0-9_.-]+)")


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if not namespace.startswith("cp_"):
        return "<unknown>"
    token = namespace.removeprefix("cp_")
    return token.split("_", 1)[0]


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


def visible_non_debug(event_id: str, text: str) -> bool:
    if event_id.startswith("cp_debug."):
        return False
    if "_debug" in event_id:
        return False
    if re.search(r"\bhidden\s*=\s*yes\b", text):
        return False
    return bool(OPTION_RE.search(text))


def vanilla_video_rows() -> list[tuple[str, str, str, int, str, str]]:
    rows: list[tuple[str, str, str, int, str, str]] = []
    for event_id, path, line, text in iter_event_blocks():
        clean = uncommented_text(text)
        if not visible_non_debug(event_id, clean):
            continue
        title_match = TITLE_RE.search(clean)
        title = title_match.group(1) if title_match else "-"
        for video in VIDEO_RE.findall(clean):
            rows.append((event_id, person_for_event(event_id), video, line, rel(path), title))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-no-vanilla-video",
        action="store_true",
        help="fail unless no visible non-debug event uses a vanilla video plate",
    )
    parser.add_argument("--list", action="store_true", help="print every remaining vanilla-video event")
    parser.add_argument("--limit", type=int, default=40, help="maximum rows to print without --list")
    args = parser.parse_args()

    rows = vanilla_video_rows()
    by_person = Counter(row[1] for row in rows)
    by_video = Counter(row[2] for row in rows)

    print("Common People generic video art audit")
    print(f"Visible non-debug events using vanilla video plates: {len(rows)}")
    print("By person:")
    for person, count in sorted(by_person.items()):
        print(f"  {person}: {count}")
    print("Most reused vanilla videos:")
    for video, count in by_video.most_common(12):
        print(f"  {count:3}  {video}")

    listed = rows if args.list else rows[: args.limit]
    if listed:
        print("Remaining vanilla-video events:")
        for event_id, person, video, line, path, title in listed:
            print(f"  {event_id:18} {person:10} {video:32} {path}:{line} title={title}")
        if not args.list and len(rows) > len(listed):
            print(f"  ... {len(rows) - len(listed)} more; pass --list for all")

    if args.strict_no_vanilla_video and rows:
        print("[FAIL] visible event art still uses generic vanilla video plates")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
