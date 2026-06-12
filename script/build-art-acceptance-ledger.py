#!/usr/bin/env python3
"""Build the generated-art acceptance ledger for planned replacements."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
PICTURES = MOD / "gfx" / "event_pictures"
GENERATED = ROOT / "image" / "generated"
MOTION_ARCHIVE = ROOT / "image" / "archive" / "motion-replaced-event-pictures"
DEFAULT_OUTPUT = ROOT / "documentation" / "art-acceptance-ledger.md"

TARGET_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+\.dds)`\s*\|\s*(\d+)\s*\|")
VERSION_RE = re.compile(r"replacement-batch-(v\d+(?:\.\d+)?)\.md$")


@dataclass(frozen=True)
class Target:
    priority: int
    asset: str
    expected_windows: int

    @property
    def legacy_asset(self) -> str:
        return re.sub(r"_v\d+\.dds$", ".dds", self.asset)


@dataclass(frozen=True)
class Batch:
    plan: Path
    person: str
    version: str
    targets: list[Target]

    @property
    def generated_dir(self) -> Path:
        return GENERATED / self.person / self.version


@dataclass(frozen=True)
class TargetStatus:
    batch: Batch
    target: Target
    source_png: Path
    target_dds: Path
    motion_archive_dds: Path | None
    legacy_refs: int
    target_refs: int
    source_size: str
    dds_size: str

    @property
    def source_ready(self) -> bool:
        return self.source_png.exists()

    @property
    def dds_ready(self) -> bool:
        return self.target_dds.exists()

    @property
    def motion_replaced(self) -> bool:
        return (
            self.source_ready
            and self.motion_archive_dds is not None
            and self.motion_archive_dds.exists()
            and self.legacy_refs == 0
            and self.target_refs == 0
        )

    @property
    def counts_match(self) -> bool:
        return (
            self.motion_replaced
            or self.legacy_refs == self.target.expected_windows
            or (self.legacy_refs == 0 and self.target_refs == self.target.expected_windows)
        )

    @property
    def already_promoted(self) -> bool:
        return self.legacy_refs == 0 and self.target_refs == self.target.expected_windows and self.dds_ready

    @property
    def ready_to_promote(self) -> bool:
        return (
            self.source_ready
            and self.dds_ready
            and self.legacy_refs == self.target.expected_windows
            and self.target_refs == 0
        )

    @property
    def state(self) -> str:
        if self.motion_replaced:
            return "motion-replaced"
        if not self.counts_match or (self.legacy_refs > 0 and self.target_refs > 0):
            return "reference-conflict"
        if self.already_promoted:
            return "promoted"
        if self.ready_to_promote:
            return "ready-to-promote"
        if not self.source_ready:
            return "waiting-gpt-image-2"
        if not self.dds_ready:
            return "review-and-convert"
        return "needs-review"

    @property
    def next_gate(self) -> str:
        return {
            "reference-conflict": "fix event references",
            "motion-replaced": "in-game motion QA",
            "promoted": "in-game QA",
            "ready-to-promote": "run promote-art-batch --apply",
            "waiting-gpt-image-2": "generate source PNG",
            "review-and-convert": "contact sheet review + DDS",
            "needs-review": "review before promotion",
        }[self.state]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def discover_plans() -> list[Path]:
    return sorted((ROOT / "documentation" / "characters").glob("*/prompts/replacement-batch-v*.md"))


def parse_targets(text: str) -> list[Target]:
    targets: list[Target] = []
    for line in text.splitlines():
        match = TARGET_ROW_RE.match(line)
        if match:
            targets.append(Target(int(match.group(1)), match.group(2), int(match.group(3))))
    return targets


def load_batch(plan: Path) -> Batch:
    version_match = VERSION_RE.match(plan.name)
    if not version_match:
        raise ValueError(f"{rel(plan)} must be named replacement-batch-vNN.md")
    if plan.parent.name != "prompts":
        raise ValueError(f"{rel(plan)} must live under documentation/characters/<person>/prompts/")
    text = plan.read_text(encoding="utf-8")
    return Batch(
        plan=plan,
        person=plan.parent.parent.name,
        version=version_match.group(1),
        targets=parse_targets(text),
    )


def event_files() -> list[Path]:
    return sorted(EVENTS.glob("*.txt"))


def count_event_refs(asset: str) -> int:
    needle = f"gfx/event_pictures/{asset}"
    return sum(path.read_text(encoding="utf-8-sig", errors="replace").count(needle) for path in event_files())


def image_size(path: Path) -> str:
    if not path.exists():
        return "-"
    try:
        with Image.open(path) as image:
            return f"{image.width}x{image.height}"
    except OSError:
        return "unreadable"


def statuses_for_batch(batch: Batch) -> list[TargetStatus]:
    statuses: list[TargetStatus] = []
    for target in batch.targets:
        source_png = batch.generated_dir / f"{target.asset}.png"
        target_dds = PICTURES / target.asset
        motion_archives = sorted(MOTION_ARCHIVE.glob(f"*/{target.asset}"))
        statuses.append(
            TargetStatus(
                batch=batch,
                target=target,
                source_png=source_png,
                target_dds=target_dds,
                motion_archive_dds=motion_archives[0] if motion_archives else None,
                legacy_refs=count_event_refs(target.legacy_asset),
                target_refs=count_event_refs(target.asset),
                source_size=image_size(source_png),
                dds_size=image_size(target_dds),
            )
        )
    return statuses


def markdown_code(value: str) -> str:
    return f"`{value}`"


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def row(status: TargetStatus) -> str:
    return (
        f"| {markdown_code(status.batch.person)} | {markdown_code(status.batch.version)} | "
        f"{status.target.priority:02d} | {markdown_code(status.target.asset)} | "
        f"{markdown_code(status.target.legacy_asset)} | {status.target.expected_windows} | "
        f"{status.legacy_refs} | {status.target_refs} | {yes_no(status.source_ready)} | "
        f"{status.source_size} | {yes_no(status.dds_ready)} | {status.dds_size} | "
        f"{status.state} | {status.next_gate} |"
    )


def build_markdown(statuses: list[TargetStatus]) -> str:
    state_counts: dict[str, int] = {}
    for status in statuses:
        state_counts[status.state] = state_counts.get(status.state, 0) + 1

    legacy_refs = sum(status.legacy_refs for status in statuses)
    target_refs = sum(status.target_refs for status in statuses)
    plans = sorted({status.batch.plan for status in statuses})
    lines = [
        "# Common People art acceptance ledger",
        "",
        "Generated by `script/build-art-acceptance-ledger.py`; do not edit by hand.",
        "",
        "## Summary",
        "",
        f"- Replacement batch ledgers: {len(plans)}",
        f"- Planned replacement targets: {len(statuses)}",
        f"- Legacy event-window references queued: {legacy_refs}",
        f"- Promoted replacement references: {target_refs}",
        "",
        "State counts:",
        "",
    ]

    for state in sorted(state_counts):
        lines.append(f"- {state}: {state_counts[state]}")

    lines.extend(
        [
            "",
            "## Batch Ledgers",
            "",
        ]
    )
    for plan in plans:
        lines.append(f"- `{rel(plan)}`")

    lines.extend(
        [
            "",
            "## Acceptance Table",
            "",
            "| Person | Batch | # | Target DDS | Legacy DDS | Expected windows | Legacy refs | Target refs | Source PNG | Source size | DDS | DDS size | State | Next gate |",
            "|---|---:|---:|---|---|---:|---:|---:|---|---:|---|---:|---|---|",
        ]
    )
    lines.extend(row(status) for status in statuses)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plans", nargs="*", type=Path, help="specific replacement-batch ledgers to include")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if the generated ledger is missing or stale")
    args = parser.parse_args()

    plans = args.plans or discover_plans()
    batches = [load_batch(plan if plan.is_absolute() else ROOT / plan) for plan in plans]
    statuses = [status for batch in batches for status in statuses_for_batch(batch)]
    text = build_markdown(statuses)
    output = args.output if args.output.is_absolute() else ROOT / args.output

    if args.check:
        if not output.exists():
            print(f"FAIL: {rel(output)} is missing")
            print("Run: script/build-art-acceptance-ledger.py")
            return 1
        if output.read_text(encoding="utf-8") != text:
            print(f"FAIL: {rel(output)} is stale")
            print("Run: script/build-art-acceptance-ledger.py")
            return 1
        print(f"ok: {rel(output)} is current")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"wrote {rel(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
