#!/usr/bin/env python3
"""Report generated-source coverage for active Common People event art."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
GENERATED = ROOT / "image" / "generated"

TEXTURE_RE = re.compile(r'texture\s*=\s*"gfx/event_pictures/([^"]+\.dds)"')
EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def active_event_images() -> set[str]:
    refs: set[str] = set()
    for path in sorted(EVENTS.glob("*.txt")):
        refs.update(TEXTURE_RE.findall(path.read_text(encoding="utf-8-sig", errors="replace")))
    return refs


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


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

            yield match.group(1), "\n".join(lines[start : i + 1])
            i += 1


def image_usage() -> dict[str, list[str]]:
    usage: dict[str, list[str]] = {}
    for event_id, text in iter_event_blocks():
        for image in TEXTURE_RE.findall(text):
            usage.setdefault(image, []).append(event_id)
    return usage


def generated_source_images() -> set[str]:
    return {
        path.name.removesuffix(".png")
        for path in GENERATED.glob("**/*.dds.png")
    }


def person_token(image_name: str) -> str:
    if image_name.startswith("cp_layla_"):
        return "layla"
    if image_name.startswith("cp_bey_"):
        return "bey"
    if image_name.startswith("cp_soldier_"):
        return "soldier"
    if image_name.startswith("cp_samier_"):
        return "samier"
    if image_name.startswith("cp_tarek_"):
        return "tarek"
    if image_name.startswith("cp_nour_"):
        return "nour"
    if image_name.startswith("cp_mina_"):
        return "mina"
    if image_name.startswith("cp_zaynab_"):
        return "zaynab"
    match = re.match(r"cp_([A-Za-z0-9]+)_", image_name)
    return match.group(1) if match else "<unknown>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--list-missing",
        action="store_true",
        help="print every active event image that lacks a generated source PNG",
    )
    parser.add_argument(
        "--rank-missing",
        action="store_true",
        help="print missing generated-source images sorted by active event usage count",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="limit --rank-missing output; 0 means print every ranked image",
    )
    parser.add_argument(
        "--strict-generated",
        action="store_true",
        help="return failure unless every active event DDS has generated source coverage",
    )
    args = parser.parse_args()

    active = active_event_images()
    generated = generated_source_images()
    usage = image_usage()
    covered = active & generated
    missing = sorted(active - generated)
    covered_by_person = Counter(person_token(name) for name in covered)
    missing_by_person = Counter(person_token(name) for name in missing)

    print("Common People art provenance audit")
    print(f"Active event DDS references: {len(active)}")
    print(f"Generated source coverage:  {len(covered)}")
    print(f"Legacy/no generated source: {len(missing)}")
    print("Coverage by person:")
    for person in sorted(set(covered_by_person) | set(missing_by_person)):
        print(
            f"  {person}: generated={covered_by_person[person]} "
            f"legacy_or_missing_source={missing_by_person[person]}"
        )

    if args.list_missing and missing:
        print("Legacy/no generated source images:")
        for name in missing:
            print(f"- mod/gfx/event_pictures/{name}")

    if args.rank_missing and missing:
        ranked = sorted(missing, key=lambda name: (-len(usage.get(name, [])), name))
        if args.limit > 0:
            ranked = ranked[: args.limit]
        print("Ranked legacy/no generated source images:")
        for name in ranked:
            events = usage.get(name, [])
            sample = ", ".join(events[:10])
            suffix = " ..." if len(events) > 10 else ""
            print(f"{len(events):3}  mod/gfx/event_pictures/{name}  {sample}{suffix}")

    if args.strict_generated and missing:
        print("[FAIL] active event art is not fully regenerated/source-covered")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
