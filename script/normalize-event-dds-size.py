#!/usr/bin/env python3
"""Resize referenced Common People event DDS assets to the event-window size."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
PICTURES = MOD / "gfx" / "event_pictures"

TEXTURE_RE = re.compile(r'texture\s*=\s*"gfx/event_pictures/([^"]+\.dds)"')


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def referenced_images() -> set[str]:
    refs: set[str] = set()
    for path in sorted(EVENTS.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        refs.update(TEXTURE_RE.findall(text))
    return refs


def image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return image.size


def normalize(path: Path, size: tuple[int, int], nvcompress: str) -> None:
    with tempfile.TemporaryDirectory(prefix="cp-dds-resize-") as tmp:
        png = Path(tmp) / f"{path.stem}.png"
        out = Path(tmp) / path.name
        with Image.open(path) as image:
            resized = image.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            resized.save(png)
        subprocess.run(
            [nvcompress, "-bc3", "-nomips", "-silent", str(png), str(out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        shutil.move(str(out), path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="rewrite oversized referenced DDS files; default is dry-run",
    )
    parser.add_argument("--width", type=int, default=600)
    parser.add_argument("--height", type=int, default=400)
    args = parser.parse_args()

    nvcompress = shutil.which("nvcompress")
    if not nvcompress:
        raise SystemExit("error: nvcompress is required (install libnvtt-bin)")

    expected = (args.width, args.height)
    changed = 0
    oversized = []
    missing = []
    for name in sorted(referenced_images()):
        path = PICTURES / name
        if not path.exists():
            missing.append(name)
            continue
        size = image_size(path)
        if size == expected:
            continue
        oversized.append((path, size))

    for path, size in oversized:
        print(f"{'resize' if args.apply else 'would resize'}: {rel(path)} {size[0]}x{size[1]} -> {expected[0]}x{expected[1]}")
        if args.apply:
            normalize(path, expected, nvcompress)
            changed += 1

    for name in missing:
        print(f"missing: gfx/event_pictures/{name}")

    print(f"referenced oversized DDS: {len(oversized)}")
    print(f"rewritten: {changed}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
