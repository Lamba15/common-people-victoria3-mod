#!/usr/bin/env python3
"""Promote generated replacement-batch art into active event references."""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"
PICTURES = MOD / "gfx" / "event_pictures"
GENERATED = ROOT / "image" / "generated"
ARCHIVE = ROOT / "image" / "archive" / "legacy-event-pictures"
MOTION_ARCHIVE = ROOT / "image" / "archive" / "motion-replaced-event-pictures"
DEFAULT_PLAN = ROOT / "documentation" / "characters" / "layla" / "prompts" / "replacement-batch-v0.7.md"

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

    @property
    def archive_dir(self) -> Path:
        return ARCHIVE / f"{self.version}-superseded"


@dataclass(frozen=True)
class TargetStatus:
    target: Target
    source_png: Path
    target_dds: Path
    legacy_dds: Path
    archive_dds: Path
    motion_archive_dds: Path | None
    legacy_refs: int
    target_refs: int

    @property
    def source_ready(self) -> bool:
        return self.source_png.exists()

    @property
    def dds_ready(self) -> bool:
        return self.target_dds.exists()

    @property
    def already_promoted(self) -> bool:
        return self.legacy_refs == 0 and self.target_refs == self.target.expected_windows

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
    def ready_to_promote(self) -> bool:
        return self.source_ready and self.dds_ready and self.legacy_refs > 0


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
    count = 0
    for path in event_files():
        count += path.read_text(encoding="utf-8-sig", errors="replace").count(needle)
    return count


def status_for_target(batch: Batch, target: Target) -> TargetStatus:
    motion_archives = sorted(MOTION_ARCHIVE.glob(f"*/{target.asset}"))
    return TargetStatus(
        target=target,
        source_png=batch.generated_dir / f"{target.asset}.png",
        target_dds=PICTURES / target.asset,
        legacy_dds=PICTURES / target.legacy_asset,
        archive_dds=batch.archive_dir / target.legacy_asset,
        motion_archive_dds=motion_archives[0] if motion_archives else None,
        legacy_refs=count_event_refs(target.legacy_asset),
        target_refs=count_event_refs(target.asset),
    )


def statuses_for_batch(batch: Batch) -> list[TargetStatus]:
    return [status_for_target(batch, target) for target in batch.targets]


def replacement_issues(status: TargetStatus) -> list[str]:
    issues: list[str] = []
    if not status.source_ready:
        issues.append(f"missing generated source {rel(status.source_png)}")
    if status.motion_replaced:
        return issues
    if not status.dds_ready:
        issues.append(f"missing shipped DDS {rel(status.target_dds)}")
    if status.legacy_refs and status.legacy_refs != status.target.expected_windows:
        issues.append(
            f"{status.target.legacy_asset} has {status.legacy_refs} active refs; "
            f"expected {status.target.expected_windows}"
        )
    if not status.legacy_refs and not status.already_promoted:
        issues.append(
            f"{status.target.legacy_asset} has no active refs, but "
            f"{status.target.asset} has {status.target_refs}; expected {status.target.expected_windows}"
        )
    if status.archive_dds.exists() and status.legacy_dds.exists():
        try:
            same = status.archive_dds.read_bytes() == status.legacy_dds.read_bytes()
        except OSError:
            same = False
        if not same:
            issues.append(f"archive collision at {rel(status.archive_dds)}")
    return issues


def print_batch_status(batch: Batch, statuses: list[TargetStatus]) -> None:
    promoted = sum(1 for status in statuses if status.already_promoted)
    motion = sum(1 for status in statuses if status.motion_replaced)
    ready = sum(1 for status in statuses if status.ready_to_promote)
    waiting = len(statuses) - promoted - motion - ready
    legacy_refs = sum(status.legacy_refs for status in statuses)

    print("Common People art batch promotion status")
    print(f"Plan: {rel(batch.plan)}")
    print(f"Generated dir: {rel(batch.generated_dir)}")
    print(f"Archive dir: {rel(batch.archive_dir)}")
    print(f"Targets: {len(statuses)}")
    print(f"Promoted: {promoted}")
    print(f"Motion replaced: {motion}")
    print(f"Ready: {ready}")
    print(f"Waiting: {waiting}")
    print(f"Legacy event-window references queued for replacement: {legacy_refs}")
    for status in statuses:
        if status.already_promoted:
            state = "promoted"
        elif status.motion_replaced:
            state = "motion"
        elif status.ready_to_promote:
            state = "ready"
        else:
            state = "waiting"
        print(
            f"- {status.target.priority:02d} {status.target.asset}: {state} "
            f"legacy_refs={status.legacy_refs} target_refs={status.target_refs} "
            f"source={'yes' if status.source_ready else 'no'} "
            f"dds={'yes' if status.dds_ready else 'no'}"
        )
        for issue in replacement_issues(status):
            print(f"  [INFO] {issue}")


def promote_status(status: TargetStatus, batch: Batch) -> None:
    old_ref = f"gfx/event_pictures/{status.target.legacy_asset}"
    new_ref = f"gfx/event_pictures/{status.target.asset}"

    for path in event_files():
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        if old_ref not in text:
            continue
        path.write_text(text.replace(old_ref, new_ref), encoding="utf-8-sig")
        print(f"rewired {rel(path)}: {status.target.legacy_asset} -> {status.target.asset}")

    if status.legacy_dds.exists():
        batch.archive_dir.mkdir(parents=True, exist_ok=True)
        if status.archive_dds.exists():
            status.legacy_dds.unlink()
            print(f"removed duplicate archived legacy DDS {rel(status.legacy_dds)}")
        else:
            shutil.move(str(status.legacy_dds), str(status.archive_dds))
            print(f"archived {rel(status.archive_dds)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", nargs="?", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--all", action="store_true", help="process every replacement-batch-vNN.md ledger")
    parser.add_argument("--apply", action="store_true", help="rewrite event refs and archive superseded DDS files")
    parser.add_argument("--check", action="store_true", help="fail unless all targets are already promoted")
    parser.add_argument("--allow-partial", action="store_true", help="with --apply, promote ready targets and leave waiting targets alone")
    args = parser.parse_args()

    if args.all and args.plan != DEFAULT_PLAN:
        parser.error("pass either a plan path or --all, not both")
    if args.apply and args.check:
        parser.error("--apply and --check are mutually exclusive")

    plans = discover_plans() if args.all else [args.plan if args.plan.is_absolute() else ROOT / args.plan]
    total_blockers = 0
    total_promoted = 0
    total_unpromoted = 0

    for index, plan in enumerate(plans):
        if index:
            print()
        batch = load_batch(plan)
        statuses = statuses_for_batch(batch)
        print_batch_status(batch, statuses)

        promoted = [status for status in statuses if status.already_promoted]
        motion = [status for status in statuses if status.motion_replaced]
        ready = [status for status in statuses if status.ready_to_promote]
        waiting = [
            status
            for status in statuses
            if not status.already_promoted and not status.motion_replaced and not status.ready_to_promote
        ]
        blockers = [issue for status in statuses for issue in replacement_issues(status)]
        if args.check:
            total_unpromoted += len(waiting) + len(ready)
            total_blockers += len(waiting) + len(ready)
            continue

        if args.apply:
            if waiting and not args.allow_partial:
                print(f"[FAIL] {len(waiting)} target(s) are not ready; rerun with --allow-partial to promote only ready assets")
                total_blockers += len(waiting)
                continue
            if blockers and not args.allow_partial:
                print(f"[FAIL] {len(blockers)} promotion issue(s) must be fixed before applying")
                total_blockers += len(blockers)
                continue
            for status in ready:
                if replacement_issues(status):
                    continue
                promote_status(status, batch)
                total_promoted += 1

    if args.check and total_unpromoted:
        print(f"[FAIL] {total_unpromoted} target(s) are not fully promoted")
        return 1
    if total_blockers:
        return 1
    if args.apply:
        print(f"promoted targets: {total_promoted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
