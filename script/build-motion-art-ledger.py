#!/usr/bin/env python3
"""Build and check a generated ledger of moving event art."""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
PICTURES = MOD / "gfx" / "event_pictures"
LEDGER = ROOT / "documentation" / "motion-art-ledger.md"
AUDIT_SCRIPT = ROOT / "script" / "audit-event-motion.py"
sys.dont_write_bytecode = True

LOC_FIELD_RE = re.compile(r"\btitle\s*=\s*([A-Za-z0-9_.-]+)")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+\"(.*)\"")


def load_motion_audit():
    spec = importlib.util.spec_from_file_location("audit_event_motion", AUDIT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {AUDIT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def loc_keys() -> dict[str, str]:
    keys: dict[str, str] = {}
    for path in sorted((MOD / "localization").glob("**/*.yml")):
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
            match = LOC_KEY_RE.match(line)
            if match:
                keys[match.group(1)] = match.group(2)
    return keys


def title_for(text: str, loc: dict[str, str]) -> str:
    match = LOC_FIELD_RE.search(text)
    if not match:
        return "-"
    return loc.get(match.group(1), match.group(1)).replace("|", "\\|")


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if namespace.startswith("cp_"):
        namespace = namespace[3:]
    return namespace.split("_", 1)[0]


def mod_video_keys() -> set[str]:
    keys: set[str] = set()
    if not PICTURES.exists():
        return keys
    for path in sorted(PICTURES.glob("*.bk2")):
        keys.add(path.stem)
        keys.add(f"gfx/event_pictures/{path.name}")
    return keys


def build() -> tuple[str, list[str]]:
    motion = load_motion_audit()
    loc = loc_keys()
    game_dir = motion.find_game_dir()
    known_videos = motion.known_event_videos(game_dir)
    custom_videos = mod_video_keys()
    video_supported = motion.event_window_supports_video(game_dir)

    rows: list[dict[str, str]] = []
    issues: list[str] = []
    video_counts: Counter[str] = Counter()
    custom_video_counts: Counter[str] = Counter()
    vanilla_video_counts: Counter[str] = Counter()
    person_counts: Counter[str] = Counter()
    vanilla_person_counts: Counter[str] = Counter()
    visible_count = 0

    for block in motion.iter_event_blocks():
        if not motion.visible_non_debug(block):
            continue
        visible_count += 1
        event_id = str(block["id"])
        text = motion.uncommented_text(str(block["text"]))
        fields = motion.image_fields(text)
        videos = [value for kind, value in fields if kind == "video"]
        textures = [value for kind, value in fields if kind == "texture"]
        location = f"{rel(Path(block['path']))}:{block['line']}"

        if textures and videos:
            issues.append(f"{event_id} at {location} mixes texture and video event art")
        if len(videos) > 1:
            issues.append(f"{event_id} at {location} has {len(videos)} video fields")

        for video in videos:
            if video not in known_videos:
                issues.append(f"{event_id} at {location} references missing video {video}")
            person = person_for_event(event_id)
            status = "custom" if video in custom_videos else "vanilla-debt"
            person_counts[person] += 1
            video_counts[video] += 1
            if status == "custom":
                custom_video_counts[video] += 1
            else:
                vanilla_video_counts[video] += 1
                vanilla_person_counts[person] += 1
            rows.append({
                "event": event_id,
                "person": person,
                "title": title_for(text, loc),
                "video": video,
                "status": status,
                "source": location,
            })

    custom_motion_count = sum(custom_video_counts.values())
    vanilla_motion_count = sum(vanilla_video_counts.values())

    if video_supported is False:
        issues.append("installed eventwindow.gui does not reference Event.HasVideo and Event.GetVideo")

    lines = [
        "# Motion Art Ledger",
        "",
        "Generated from live event script. Rebuild with `python3 script/build-motion-art-ledger.py`.",
        "",
        "This ledger records visible non-debug events that use Victoria 3 `.bk2` event videos. Still-image events remain covered by the image inventory and art provenance audits.",
        "",
        "## Summary",
        "",
        f"- Visible non-debug events: {visible_count}",
        f"- Motion events: {len(rows)}",
        f"- Custom/mod motion events: {custom_motion_count}",
        f"- Vanilla video placeholder debt: {vanilla_motion_count}",
        f"- Persons with motion events: {len(person_counts)}",
        f"- Persons with vanilla video debt: {len(vanilla_person_counts)}",
        f"- Known event videos: {len(known_videos)}",
        f"- Mod-shipped custom videos: {len(custom_videos) // 2}",
        f"- Event window video support: {'yes' if video_supported else 'not checked' if video_supported is None else 'no'}",
        f"- Issues: {len(issues)}",
        "",
        "## Person Counts",
        "",
    ]
    for person, count in sorted(person_counts.items()):
        lines.append(f"- `{person}`: {count}")

    lines.extend([
        "",
        "## Vanilla Video Debt by Person",
        "",
    ])
    if vanilla_person_counts:
        for person, count in sorted(vanilla_person_counts.items()):
            lines.append(f"- `{person}`: {count}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Video Reuse",
        "",
    ])
    for video, count in sorted(video_counts.items()):
        lines.append(f"- `{video}`: {count}")

    lines.extend([
        "",
        "## Vanilla Video Reuse",
        "",
    ])
    if vanilla_video_counts:
        for video, count in sorted(vanilla_video_counts.items()):
            lines.append(f"- `{video}`: {count}")
    else:
        lines.append("- none")

    lines.extend([
        "",
        "## Motion Events",
        "",
        "| Event | Person | Title | Video | Status | Source |",
        "|---|---|---|---|---|---|",
    ])
    for row in sorted(rows, key=lambda item: (item["person"], item["event"])):
        lines.append(f"| `{row['event']}` | {row['person']} | {row['title']} | `{row['video']}` | {row['status']} | `{row['source']}` |")

    lines.extend([
        "",
        "## Rules",
        "",
        "- Use `event_image = { video = \"<vanilla_or_mod_bk2>\" }` only for known `.bk2` assets that resolve in `script/audit-event-motion.py`.",
        "- Treat vanilla videos as temporary development placeholders. Release builds must pass `script/audit-generic-video-art.py --strict-no-vanilla-video`.",
        "- Do not mix `texture` and `video` inside one `event_image` block.",
        "- Use motion for public, institutional, technological, or crowd-scale beats. Use reviewed GPT stills for intimate person scenes.",
        "- Custom moving GPT images need a real `.bk2` export path before they can be promoted into `mod/gfx/event_pictures/`.",
        "",
        "## Checks",
        "",
        "```bash",
        "python3 script/build-motion-art-ledger.py --check",
        "script/audit-event-motion.py",
        "script/audit-generic-video-art.py --strict-no-vanilla-video",
        "script/audit-event-images.py --strict-size --strict-unused",
        "```",
    ])

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the ledger is stale or has motion-art issues")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("motion-art ledger issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-motion-art-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
