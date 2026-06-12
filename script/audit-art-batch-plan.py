#!/usr/bin/env python3
"""Audit a generated-art replacement batch prompt ledger."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
GENERATED = ROOT / "image" / "generated"
MOTION_ARCHIVE = ROOT / "image" / "archive" / "motion-replaced-event-pictures"
DEFAULT_PLAN = ROOT / "documentation" / "characters" / "layla" / "prompts" / "replacement-batch-v0.7.md"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
TEXTURE_RE = re.compile(r'texture\s*=\s*"gfx/event_pictures/([^"]+\.dds)"')
TARGET_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+\.dds)`\s*\|\s*(\d+)\s*\|")
PROMPT_HEADING_RE = re.compile(r"^## Prompt\s+(\d+)\s+-\s+(.+)$")


@dataclass(frozen=True)
class Target:
    priority: int
    asset: str
    expected_windows: int


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
    return {path.name.removesuffix(".png") for path in GENERATED.glob("**/*.dds.png")}


def legacy_workflow_issues() -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    old_generator = ROOT / "script" / "gen-layla-event-images.sh"
    if old_generator.exists():
        issues.append((
            "LEGACY_GENERATOR",
            f"{rel(old_generator)} exists; use versioned batch ledgers plus script/export-art-batch-prompts.py instead",
        ))

    for path in sorted(GENERATED.glob("**/cp_conversation_*.dds.png")):
        issues.append((
            "LEGACY_SOURCE_NAME",
            f"{rel(path)} uses retired cp_conversation_* source naming; use cp_layla_conversation_*_vNN.dds.png",
        ))

    converter = ROOT / "script" / "convert-images-to-dds.sh"
    if converter.exists() and 'target_base="cp_layla_${base#cp_}"' in converter.read_text(encoding="utf-8", errors="replace"):
        issues.append((
            "LEGACY_CONVERTER_MAPPING",
            f"{rel(converter)} still silently maps cp_conversation_* sources into Layla DDS names",
        ))
    return issues


def parse_targets(text: str) -> list[Target]:
    targets: list[Target] = []
    for line in text.splitlines():
        match = TARGET_ROW_RE.match(line)
        if match:
            targets.append(Target(int(match.group(1)), match.group(2), int(match.group(3))))
    return targets


def parse_prompt_numbers(text: str) -> set[int]:
    return {int(match.group(1)) for match in map(PROMPT_HEADING_RE.match, text.splitlines()) if match}


def legacy_asset_name(planned_asset: str) -> str:
    return re.sub(r"_v\d+\.dds$", ".dds", planned_asset)


def motion_archived(planned_asset: str) -> bool:
    return any(MOTION_ARCHIVE.glob(f"*/{planned_asset}"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def discover_plans() -> list[Path]:
    return sorted((ROOT / "documentation" / "characters").glob("*/prompts/replacement-batch-v*.md"))


def audit_plan(plan: Path, *, strict_ready: bool) -> int:
    text = plan.read_text(encoding="utf-8")
    targets = parse_targets(text)
    prompt_numbers = parse_prompt_numbers(text)
    usage = image_usage()
    generated = generated_source_images()
    issues: list[tuple[str, str]] = []
    ready = 0
    issues.extend(legacy_workflow_issues())

    expected_priorities = set(range(1, len(targets) + 1))
    target_priorities = {target.priority for target in targets}
    if target_priorities != expected_priorities:
        issues.append(("PRIORITY", f"target priorities are {sorted(target_priorities)}, expected {sorted(expected_priorities)}"))
    if prompt_numbers != expected_priorities:
        issues.append(("PROMPT", f"prompt headings are {sorted(prompt_numbers)}, expected {sorted(expected_priorities)}"))

    print("Common People art batch plan audit")
    print(f"Plan: {rel(plan)}")
    print(f"Targets: {len(targets)}")
    print(f"Prompts: {len(prompt_numbers)}")
    for target in targets:
        legacy = legacy_asset_name(target.asset)
        legacy_events = usage.get(legacy, [])
        target_events = usage.get(target.asset, [])
        source_ready = target.asset in generated
        dds_ready = (MOD / "gfx" / "event_pictures" / target.asset).exists()
        archived_motion = motion_archived(target.asset)
        promoted = not legacy_events and len(target_events) == target.expected_windows
        motion_replaced = archived_motion and not legacy_events and not target_events
        if source_ready and (dds_ready or archived_motion):
            ready += 1

        if promoted:
            pass
        elif motion_replaced:
            pass
        elif legacy_events and target_events:
            issues.append((
                "PARTIAL_PROMOTION",
                f"{target.asset} has {len(target_events)} active windows while {legacy} still has {len(legacy_events)}",
            ))
        elif legacy_events:
            if len(legacy_events) != target.expected_windows:
                issues.append((
                    "WINDOW_COUNT",
                    f"{target.asset} expects {target.expected_windows} active windows, but {legacy} is used by {len(legacy_events)}",
                ))
        elif target_events:
            issues.append((
                "WINDOW_COUNT",
                f"{target.asset} expects {target.expected_windows} active windows, but is used by {len(target_events)}",
            ))
        else:
            issues.append(("TARGET", f"{target.asset} maps to {legacy}, which is not referenced by active events"))

        print(
            f"- {target.priority:02d} {target.asset}: legacy={legacy} "
            f"legacy_windows={len(legacy_events)} target_windows={len(target_events)} "
            f"source={'yes' if source_ready else 'no'} "
            f"dds={'yes' if dds_ready else 'no'} "
            f"motion_archive={'yes' if archived_motion else 'no'}"
        )

    print(f"Ready planned assets: {ready}/{len(targets)}")
    if strict_ready and ready != len(targets):
        issues.append(("READY", f"{len(targets) - ready} planned asset(s) are not generated and shipped yet"))

    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    return len(issues)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plan",
        nargs="?",
        type=Path,
        default=DEFAULT_PLAN,
        help="markdown replacement-batch prompt ledger to audit",
    )
    parser.add_argument("--all", action="store_true", help="audit every replacement-batch-vNN.md ledger")
    parser.add_argument(
        "--strict-ready",
        action="store_true",
        help="fail unless every planned vNN asset already has generated PNG and shipped DDS coverage",
    )
    args = parser.parse_args()

    plans = discover_plans() if args.all else [args.plan if args.plan.is_absolute() else ROOT / args.plan]
    total_issues = 0
    for index, plan in enumerate(plans):
        if index:
            print()
        total_issues += audit_plan(plan, strict_ready=args.strict_ready)
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
