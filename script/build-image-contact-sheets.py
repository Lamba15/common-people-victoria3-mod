#!/usr/bin/env python3
"""Build review contact sheets for generated Common People event images."""

from __future__ import annotations

import argparse
import io
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = ROOT / "image" / "generated"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def image_sets(root: Path) -> list[Path]:
    sets: list[Path] = []
    for path in sorted(root.glob("**/*.dds.png")):
        if path.parent not in sets:
            sets.append(path.parent)
    return sets


def review_folders(root: Path) -> list[Path]:
    return [root] if any(root.glob("*.dds.png")) else image_sets(root)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: str) -> None:
    # Pillow's default bitmap font cannot wrap; keep labels short and stable.
    draw.text(xy, text, font=font, fill=fill)


def render_sheet(folder: Path, columns: int, thumb_width: int, thumb_height: int, padding: int) -> Image.Image:
    paths = sorted(folder.glob("*.dds.png"))
    if not paths:
        raise ValueError(f"no *.dds.png files in {folder}")

    font = ImageFont.load_default()
    title_height = 36
    label_height = 30
    rows = math.ceil(len(paths) / columns)
    width = columns * thumb_width + (columns + 1) * padding
    height = title_height + padding + rows * (thumb_height + label_height + padding)

    sheet = Image.new("RGB", (width, height), "#f5f0e8")
    draw = ImageDraw.Draw(sheet)
    draw_text(draw, (padding, 12), rel(folder), font, "#2f2a24")

    for index, path in enumerate(paths):
        col = index % columns
        row = index // columns
        x = padding + col * (thumb_width + padding)
        y = title_height + padding + row * (thumb_height + label_height + padding)

        with Image.open(path) as src:
            thumb = ImageOps.contain(src.convert("RGB"), (thumb_width, thumb_height), Image.Resampling.LANCZOS)
        frame = Image.new("RGB", (thumb_width, thumb_height), "#1f1d1a")
        frame.paste(thumb, ((thumb_width - thumb.width) // 2, (thumb_height - thumb.height) // 2))
        sheet.paste(frame, (x, y))

        label = path.name.removesuffix(".dds.png")
        draw.rectangle((x, y + thumb_height, x + thumb_width, y + thumb_height + label_height), fill="#efe4d3")
        draw_text(draw, (x + 6, y + thumb_height + 8), label, font, "#2f2a24")

    return sheet


def image_png_bytes(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def build_sheet(folder: Path, columns: int, thumb_width: int, thumb_height: int, padding: int) -> Path:
    sheet = render_sheet(folder, columns, thumb_width, thumb_height, padding)
    output = folder / "contact-sheet.png"
    sheet.save(output)
    return output


def sheet_is_current(folder: Path, columns: int, thumb_width: int, thumb_height: int, padding: int) -> bool:
    output = folder / "contact-sheet.png"
    if not output.exists():
        return False
    expected = image_png_bytes(render_sheet(folder, columns, thumb_width, thumb_height, padding))
    return output.read_bytes() == expected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "roots",
        nargs="*",
        type=Path,
        default=[DEFAULT_ROOT],
        help="generated image roots or specific folders to scan",
    )
    parser.add_argument("--columns", type=int, default=2, help="thumbnail columns per sheet")
    parser.add_argument("--thumb-width", type=int, default=300)
    parser.add_argument("--thumb-height", type=int, default=200)
    parser.add_argument("--padding", type=int, default=18)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any contact-sheet.png is missing or stale; do not rewrite files",
    )
    args = parser.parse_args()

    folders: list[Path] = []
    for root in args.roots:
        root = root if root.is_absolute() else ROOT / root
        folders.extend(review_folders(root))

    outputs: list[Path] = []
    stale: list[Path] = []
    for folder in folders:
        if args.check:
            if not sheet_is_current(folder, args.columns, args.thumb_width, args.thumb_height, args.padding):
                stale.append(folder / "contact-sheet.png")
            continue
        output = build_sheet(folder, args.columns, args.thumb_width, args.thumb_height, args.padding)
        outputs.append(output)
        print(f"ok: {rel(output)}")

    if args.check:
        if stale:
            print("FAIL: stale or missing generated image contact sheets:")
            for path in stale:
                print(f"- {rel(path)}")
            print("Run: script/build-image-contact-sheets.py")
            return 1
        print(f"ok: {len(folders)} contact sheet(s) are current")
        return 0

    print(f"contact sheets: {len(outputs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
