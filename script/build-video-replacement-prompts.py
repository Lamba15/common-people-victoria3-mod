#!/usr/bin/env python3
"""Build GPT-image-2 prompt exports for vanilla video placeholder replacement."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
LOC = MOD / "localization"
LEDGER = ROOT / "documentation" / "video-replacement-prompt-ledger.md"
VERSION = "v0.1"
OUTPUT_ROOT = ROOT / "image" / "generated" / "video-replacements" / VERSION
PROMPT_DIR = OUTPUT_ROOT / "prompts"
JSONL = OUTPUT_ROOT / "gpt-image-2-batch.jsonl"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
FIELD_RE = re.compile(r"\b(title|desc|flavor)\s*=\s*([A-Za-z0-9_.-]+)")
VIDEO_RE = re.compile(r'\bvideo\s*=\s*"([^"]+)"')
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+\"(.*)\"")


@dataclass(frozen=True)
class VideoEvent:
    event_id: str
    person: str
    line: int
    path: Path
    title_key: str
    desc_key: str
    flavor_key: str
    title: str
    desc: str
    flavor: str
    video: str

    @property
    def target_asset(self) -> str:
        event_token = self.event_id.replace(".", "_")
        return f"{event_token}_{slug(self.title)}_v01.dds"

    @property
    def prompt_filename(self) -> str:
        return f"{self.target_asset.removesuffix('.dds')}.prompt.txt"

    @property
    def output_png(self) -> str:
        return f"{self.target_asset}.png"

    @property
    def source(self) -> str:
        return f"{rel(self.path)}:{self.line}"


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def slug(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"[^a-z0-9]+", "_", lowered)
    return lowered.strip("_")[:72] or "event"


def md(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def loc_value(text: str) -> str:
    return text.replace(r"\"", '"').replace(r"\n", " ").strip()


def loc_keys() -> dict[str, str]:
    keys: dict[str, str] = {}
    for path in sorted(LOC.glob("**/*.yml")):
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            match = LOC_KEY_RE.match(line)
            if match:
                keys[match.group(1)] = loc_value(match.group(2))
    return keys


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if namespace.startswith("cp_"):
        namespace = namespace[3:]
    return namespace.split("_", 1)[0]


def visible_non_debug(event_id: str, text: str) -> bool:
    return (
        bool(OPTION_RE.search(text))
        and not re.search(r"\bhidden\s*=\s*yes\b", text)
        and not event_id.startswith("cp_debug.")
        and not event_id.startswith("cp_debug_")
    )


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


def discover_video_events() -> list[VideoEvent]:
    loc = loc_keys()
    rows: list[VideoEvent] = []
    for event_id, path, line, raw_text in iter_event_blocks():
        text = uncommented_text(raw_text)
        if not visible_non_debug(event_id, text):
            continue
        videos = VIDEO_RE.findall(text)
        if not videos:
            continue
        fields = {match.group(1): match.group(2) for match in FIELD_RE.finditer(text)}
        title_key = fields.get("title", "-")
        desc_key = fields.get("desc", "-")
        flavor_key = fields.get("flavor", "-")
        title = loc.get(title_key, title_key)
        desc = loc.get(desc_key, desc_key)
        flavor = loc.get(flavor_key, flavor_key)
        for video in videos:
            rows.append(
                VideoEvent(
                    event_id=event_id,
                    person=person_for_event(event_id),
                    line=line,
                    path=path,
                    title_key=title_key,
                    desc_key=desc_key,
                    flavor_key=flavor_key,
                    title=title,
                    desc=desc,
                    flavor=flavor,
                    video=video,
                )
            )
    return sorted(rows, key=lambda row: (row.person, row.event_id))


def prompt_text(row: VideoEvent) -> str:
    return "\n".join(
        [
            f"Common People video replacement prompt {VERSION}",
            f"Source event: {row.event_id} at {row.source}",
            f"Previous vanilla video placeholder: {row.video}",
            f"Target DDS: mod/gfx/event_pictures/{row.target_asset}",
            f"Source PNG: image/generated/video-replacements/{VERSION}/{row.output_png}",
            "",
            "Generation target:",
            "Use case: historical-scene",
            "Asset type: Victoria 3 event image, 3:2 landscape, final crop must read at 600x400",
            "Model: gpt-image-2",
            "Size: 1536x1024",
            "Quality: high",
            "",
            "Global Common People constraints:",
            "Painted historical realism, textured oil-paint surface, grounded 19th-century materials, natural anatomy.",
            "No text, no UI, no border, no watermark, no modern clothing, no fantasy costume, no heroic propaganda pose.",
            "The image must be human-scale and must include the essential person, action, object, or workplace named by the event.",
            "Victoria 3 event-window safety: place the essential face, action, and required object in the left half or center-left; the game's right-side text panel covers much of the right half, so reserve that area for atmosphere and background only.",
            "",
            "Specific event:",
            f"Event id: {row.event_id}",
            f"Person token: {row.person}",
            f"Title: {row.title}",
            f"Short description: {row.desc}",
            f"Flavor text: {row.flavor}",
            "",
            "Scene instruction:",
            "Render one specific moment from the event text. Favor ordinary labor, domestic detail, and social consequence over spectacle. Keep the subject and the event's most important object readable on the left side. Use the right side for background depth, architecture, smoke, crowd edge, or empty space that can be covered by Victoria 3's text panel.",
            "",
        ]
    )


def jsonl_text(rows: list[VideoEvent]) -> str:
    lines = []
    for row in rows:
        lines.append(
            json.dumps(
                {
                    "model": "gpt-image-2",
                    "out": row.output_png,
                    "output_format": "png",
                    "prompt": prompt_text(row),
                    "quality": "high",
                    "size": "1536x1024",
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return "\n".join(lines) + "\n"


def ledger_text(rows: list[VideoEvent]) -> str:
    person_counts = Counter(row.person for row in rows)
    video_counts = Counter(row.video for row in rows)
    lines = [
        "# Video Replacement Prompt Ledger",
        "",
        "Generated from visible non-debug events that still use vanilla `.bk2` video placeholders.",
        "Rebuild with `python3 script/build-video-replacement-prompts.py`.",
        "",
        "These prompts do not promote art into the mod. They create the review queue for replacing vanilla motion placeholders with custom GPT-image-2 stills or later custom motion exports.",
        "",
        "## Summary",
        "",
        f"- Version: {VERSION}",
        f"- Vanilla video placeholder events: {len(rows)}",
        f"- Persons affected: {len(person_counts)}",
        f"- Prompt exports: {len(rows)}",
        f"- Prompt directory: `{rel(PROMPT_DIR)}`",
        f"- Batch manifest: `{rel(JSONL)}`",
        "",
        "## Person Counts",
        "",
    ]
    for person, count in sorted(person_counts.items()):
        lines.append(f"- `{person}`: {count}")

    lines.extend(["", "## Previous Vanilla Video Reuse", ""])
    for video, count in sorted(video_counts.items()):
        lines.append(f"- `{video}`: {count}")

    lines.extend(
        [
            "",
            "## Replacement Targets",
            "",
            "| Event | Person | Title | Old Video | Target DDS | Prompt | Source |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        prompt_path = PROMPT_DIR / row.prompt_filename
        lines.append(
            f"| `{row.event_id}` | {row.person} | {md(row.title)} | `{row.video}` | "
            f"`{row.target_asset}` | `{rel(prompt_path)}` | `{row.source}` |"
        )

    lines.extend(
        [
            "",
            "## Checks",
            "",
            "```bash",
            "python3 script/build-video-replacement-prompts.py --check",
            "script/audit-generic-video-art.py --strict-no-vanilla-video",
            "```",
            "",
        ]
    )
    if rows:
        lines.append(
            "`--strict-no-vanilla-video` is expected to fail until generated replacements are reviewed, converted to DDS or custom BK2, and wired into events."
        )
    else:
        lines.append(
            "`--strict-no-vanilla-video` is expected to pass; there are no active vanilla `.bk2` event-video placeholders."
        )
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(rows: list[VideoEvent]) -> None:
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    JSONL.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    for row in rows:
        (PROMPT_DIR / row.prompt_filename).write_text(prompt_text(row), encoding="utf-8")
    JSONL.write_text(jsonl_text(rows), encoding="utf-8")
    LEDGER.write_text(ledger_text(rows), encoding="utf-8")


def check_outputs(rows: list[VideoEvent]) -> list[str]:
    stale: list[str] = []
    for row in rows:
        path = PROMPT_DIR / row.prompt_filename
        expected = prompt_text(row)
        if not path.exists():
            stale.append(f"{rel(path)} is missing")
        elif path.read_text(encoding="utf-8") != expected:
            stale.append(f"{rel(path)} is stale")

    expected_jsonl = jsonl_text(rows)
    if not JSONL.exists():
        stale.append(f"{rel(JSONL)} is missing")
    elif JSONL.read_text(encoding="utf-8") != expected_jsonl:
        stale.append(f"{rel(JSONL)} is stale")

    expected_ledger = ledger_text(rows)
    if not LEDGER.exists():
        stale.append(f"{rel(LEDGER)} is missing")
    elif LEDGER.read_text(encoding="utf-8") != expected_ledger:
        stale.append(f"{rel(LEDGER)} is stale")
    return stale


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if prompt exports or ledger are missing or stale")
    args = parser.parse_args()

    rows = discover_video_events()
    if args.check:
        stale = check_outputs(rows)
        if stale:
            print("FAIL: video replacement prompt exports are stale:")
            for item in stale:
                print(f"- {item}")
            print("Run: python3 script/build-video-replacement-prompts.py")
            return 1
        print(f"ok: {len(rows)} video replacement prompt export(s) and ledger are current")
        return 0

    write_outputs(rows)
    print(f"wrote {len(rows)} video replacement prompt export(s)")
    print(f"wrote {rel(JSONL)}")
    print(f"wrote {rel(LEDGER)}")
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
