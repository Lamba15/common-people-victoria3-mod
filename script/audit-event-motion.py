#!/usr/bin/env python3
"""Audit Common People's moving event-picture coverage."""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
PICTURES = MOD / "gfx" / "event_pictures"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
EVENT_IMAGE_RE = re.compile(r"event_image\s*=\s*\{([^}]*)\}", re.S)
IMAGE_FIELD_RE = re.compile(r'\b(texture|video)\s*=\s*"([^"]+)"')
KNOWN_V3_GAME_DIRS = [
    Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game"),
]


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def find_game_dir() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("CP_V3_GAME_DIR"):
        candidates.append(Path(os.environ["CP_V3_GAME_DIR"]))
    candidates.extend(KNOWN_V3_GAME_DIRS)
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def known_event_videos(game_dir: Path | None) -> set[str]:
    videos: set[str] = set()
    search_roots = [PICTURES]
    if game_dir:
        search_roots.append(game_dir)

    for root in search_roots:
        if not root.exists():
            continue
        candidates = sorted(root.glob("*.bk2")) if root == PICTURES else sorted(root.glob("**/gfx/event_pictures/*.bk2"))
        for path in candidates:
            videos.add(path.stem)
            videos.add(f"gfx/event_pictures/{path.name}")
    return videos


def mod_event_videos() -> set[str]:
    videos: set[str] = set()
    if not PICTURES.exists():
        return videos
    for path in sorted(PICTURES.glob("*.bk2")):
        videos.add(path.stem)
        videos.add(f"gfx/event_pictures/{path.name}")
    return videos


def event_window_supports_video(game_dir: Path | None) -> bool | None:
    if not game_dir:
        return None
    event_window = game_dir / "gui" / "eventwindow.gui"
    if not event_window.exists():
        return None
    text = event_window.read_text(encoding="utf-8-sig", errors="replace")
    return "Event.HasVideo" in text and "Event.GetVideo" in text


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

            yield {
                "id": match.group(1),
                "path": path,
                "line": start + 1,
                "text": "\n".join(lines[start : i + 1]),
            }
            i += 1


def visible_non_debug(block: dict[str, object]) -> bool:
    event_id = str(block["id"])
    text = str(block["text"])
    return (
        bool(OPTION_RE.search(text))
        and not re.search(r"\bhidden\s*=\s*yes\b", text)
        and not event_id.startswith("cp_debug.")
        and not event_id.startswith("cp_debug_")
    )


def image_fields(text: str) -> list[tuple[str, str]]:
    fields: list[tuple[str, str]] = []
    for image_block in EVENT_IMAGE_RE.findall(uncommented_text(text)):
        fields.extend(IMAGE_FIELD_RE.findall(image_block))
    return fields


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--min-motion-events",
        type=int,
        default=0,
        help="minimum visible non-debug events that must use event_image video, default 0",
    )
    args = parser.parse_args()

    issues: list[tuple[str, str]] = []
    game_dir = find_game_dir()
    known_videos = known_event_videos(game_dir)
    custom_videos = mod_event_videos()
    video_supported = event_window_supports_video(game_dir)
    motion_events: list[tuple[str, str, int, str]] = []
    video_counts: Counter[str] = Counter()
    custom_count = 0
    vanilla_placeholder_count = 0

    for block in iter_event_blocks():
        if not visible_non_debug(block):
            continue
        event_id = str(block["id"])
        path = Path(block["path"])
        line = int(block["line"])
        fields = image_fields(str(block["text"]))
        textures = [value for kind, value in fields if kind == "texture"]
        videos = [value for kind, value in fields if kind == "video"]
        location = f"{rel(path)}:{line}"

        if textures and videos:
            issues.append(("MOTION_MIXED_MEDIA", f"{event_id} at {location} has both texture and video in event_image"))
        if len(videos) > 1:
            issues.append(("MOTION_MULTI_VIDEO", f"{event_id} at {location} has {len(videos)} video fields"))
        for video in videos:
            motion_events.append((event_id, rel(path), line, video))
            video_counts[video] += 1
            if video in custom_videos:
                custom_count += 1
            else:
                vanilla_placeholder_count += 1
            if video not in known_videos:
                issues.append(("MOTION_MISSING_VIDEO", f"{event_id} at {location} references missing video {video}"))

    if len(motion_events) < args.min_motion_events:
        issues.append((
            "MOTION_COVERAGE",
            f"{len(motion_events)} visible non-debug events use video; expected at least {args.min_motion_events}",
        ))
    if video_supported is False:
        issues.append(("MOTION_GUI", "installed eventwindow.gui does not reference Event.HasVideo and Event.GetVideo"))

    print("Common People event motion audit")
    print(f"Game dir:       {game_dir if game_dir else '<not found>'}")
    if video_supported is None:
        print("Event window:   <not checked>")
    else:
        print(f"Event window:   {'video-enabled' if video_supported else 'missing video hooks'}")
    print(f"Known videos:   {len(known_videos)}")
    print(f"Motion events:  {len(motion_events)}")
    print(f"Custom motion:  {custom_count}")
    print(f"Vanilla debt:   {vanilla_placeholder_count}")
    for event_id, path, line, video in motion_events:
        print(f"  {event_id:18} {video:32} {path}:{line}")
    print("Video reuse:")
    for video, count in sorted(video_counts.items()):
        print(f"  {count:3}  {video}")

    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
