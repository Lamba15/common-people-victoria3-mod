#!/usr/bin/env python3
"""Inventory Common People event image/video assets.

This deliberately stays separate from audit-common-people.py. Missing event
images are hard failures there; this script is for production cleanup: shipped
but unused DDS files, inconsistent dimensions, oversized event art, and motion
event-picture readiness.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
PICTURES = MOD / "gfx" / "event_pictures"

TEXTURE_RE = re.compile(r'texture\s*=\s*"gfx/event_pictures/([^"]+\.dds)"')
VIDEO_RE = re.compile(r'\bvideo\s*=\s*"([^"]+)"')
KNOWN_V3_GAME_DIRS = [
    Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game"),
]


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


def referenced_images() -> Counter[str]:
    refs: Counter[str] = Counter()
    for path in sorted(EVENTS.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        refs.update(TEXTURE_RE.findall(text))
    return refs


def referenced_videos() -> Counter[str]:
    refs: Counter[str] = Counter()
    for path in sorted(EVENTS.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        refs.update(VIDEO_RE.findall(text))
    return refs


def shipped_videos(game_dir: Path | None) -> dict[str, Path]:
    videos: dict[str, Path] = {}
    search_roots = [PICTURES]
    if game_dir:
        search_roots.append(game_dir)
    for root in search_roots:
        if not root.exists():
            continue
        for path in sorted(root.glob("**/gfx/event_pictures/*.bk2")):
            videos.setdefault(path.stem, path)
            try:
                rel_name = str(path.relative_to(path.parents[len(path.parts) - len(root.parts) - 1])).replace("\\", "/")
            except ValueError:
                rel_name = str(path).replace("\\", "/")
            if "gfx/event_pictures/" in rel_name:
                videos.setdefault(rel_name[rel_name.index("gfx/event_pictures/") :], path)
        if root == PICTURES:
            for path in sorted(root.glob("*.bk2")):
                videos.setdefault(path.stem, path)
                videos.setdefault(f"gfx/event_pictures/{path.name}", path)
    return videos


def image_dimensions(path: Path) -> str:
    try:
        result = subprocess.run(["file", str(path)], check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return "unknown: file command missing"
    match = re.search(r"(\d+) x (\d+)", result.stdout)
    return match.group(0) if match else "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-size",
        action="store_true",
        help="return failure when referenced event images are not the expected size",
    )
    parser.add_argument(
        "--strict-unused",
        action="store_true",
        help="return failure when shipped DDS files are not referenced by any event",
    )
    parser.add_argument(
        "--expected-size",
        default=os.environ.get("CP_EVENT_IMAGE_SIZE", "600 x 400"),
        help='expected event image dimensions as reported by file, default "600 x 400"',
    )
    args = parser.parse_args()

    refs = referenced_images()
    video_refs = referenced_videos()
    shipped = {path.name: path for path in sorted(PICTURES.glob("*.dds"))}
    game_dir = find_game_dir()
    videos = shipped_videos(game_dir)
    missing = sorted(set(refs) - set(shipped))
    missing_videos = sorted(ref for ref in video_refs if ref not in videos)
    unused = sorted(set(shipped) - set(refs))

    dimensions = {name: image_dimensions(path) for name, path in shipped.items()}
    dim_counts = Counter(dimensions.values())
    nonstandard = sorted(
        name for name in refs if name in dimensions and dimensions[name] != args.expected_size
    )

    print("Common People event image audit")
    print(f"Game dir:       {game_dir if game_dir else '<not found>'}")
    print(f"Referenced DDS: {len(refs)}")
    print(f"Referenced BK2: {len(video_refs)}")
    print(f"Known BK2:      {len(videos)}")
    print(f"Shipped DDS:    {len(shipped)}")
    print(f"Missing:        {len(missing)}")
    for name in missing:
        print(f"[FAIL] missing referenced image: gfx/event_pictures/{name}")
    print(f"Missing videos: {len(missing_videos)}")
    for name in missing_videos:
        print(f"[FAIL] missing referenced video: {name}")

    print(f"Unused shipped: {len(unused)}")
    for name in unused:
        print(f"[WARN] unused shipped image: {rel(shipped[name])}")

    print("Dimensions:")
    for size, count in sorted(dim_counts.items()):
        print(f"  {count:3}  {size}")

    print(f"Non-standard referenced images ({args.expected_size} expected): {len(nonstandard)}")
    for name in nonstandard:
        print(f"[INFO] {name}: {dimensions[name]}")

    if missing or missing_videos:
        return 1
    if args.strict_size and nonstandard:
        return 1
    if args.strict_unused and unused:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
