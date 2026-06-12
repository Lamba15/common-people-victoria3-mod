#!/usr/bin/env python3
"""Run Common People's development, runtime, or release readiness gates."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Check:
    label: str
    command: list[str]


DEV_CHECKS = [
    Check("Egypt gameplay save audit regression", ["python3", "script/test-egypt-gameplay-save.py"]),
    Check("generated person debug QA files are current", ["python3", "script/generate-person-debug-wrappers.py", "--check"]),
    Check("static event/script audit", ["script/audit-common-people.py"]),
    Check("event repeatability audit", ["script/audit-event-repeatability.py"]),
    Check("event pacing budget audit", ["python3", "script/audit-event-pacing.py"]),
    Check("event pacing ledger is current", ["python3", "script/build-event-pacing-ledger.py", "--check"]),
    Check("event firing ledger is current", ["python3", "script/build-event-firing-ledger.py", "--check"]),
    Check("world response ledger is current", ["python3", "script/build-world-response-ledger.py", "--check"]),
    Check(
        "person roster audit + shared debug visibility",
        [
            "script/audit-person-roster.py",
            "--show-missing-debug",
            "--min-visible-events",
            "6",
            "--min-first-contact-candidates",
            "16",
            "--min-always-on-first-contact-candidates",
            "6",
            "--max-first-contact-person-share",
            "0.20",
        ],
    ),
    Check("person selection ledger is current", ["python3", "script/build-person-selection-ledger.py", "--check"]),
    Check("person contract ledger is current", ["python3", "script/build-person-contract-ledger.py", "--check"]),
    Check("person hook surface ledger is current", ["python3", "script/build-person-hook-ledger.py", "--check"]),
    Check("person home-state effects", ["python3", "script/audit-home-state-effects.py"]),
    Check("journal entry surface is shared", ["python3", "script/audit-journal-entry-surface.py"]),
    Check("journal entry identity text", ["python3", "script/audit-journal-entry-identity.py"]),
    Check("production debug UI leak audit", ["script/audit-production-debug-leaks.py"]),
    Check("dynamic localization scope audit", ["python3", "script/audit-localization-dynamic-scope.py"]),
    Check("dynamic localization scope ledger is current", ["python3", "script/build-localization-dynamic-scope-ledger.py", "--check"]),
    Check("event audio audit", ["script/audit-event-audio.py"]),
    Check("event audio cue ledger is current", ["script/build-audio-cue-ledger.py", "--check"]),
    Check("event audio palette audit", ["python3", "script/audit-audio-palette.py"]),
    Check("event audio palette ledger is current", ["python3", "script/build-audio-palette-ledger.py", "--check"]),
    Check("event image inventory", ["script/audit-event-images.py"]),
    Check("generic vanilla video art debt report", ["script/audit-generic-video-art.py", "--limit", "20"]),
    Check("event video reference audit", ["script/audit-event-motion.py"]),
    Check("event motion art ledger is current", ["python3", "script/build-motion-art-ledger.py", "--check"]),
    Check("video replacement prompt exports are current", ["python3", "script/build-video-replacement-prompts.py", "--check"]),
    Check("event art provenance coverage", ["script/audit-art-provenance.py"]),
    Check("character README contracts", ["python3", "script/audit-character-doc-contract.py"]),
    Check("character art prompt contracts", ["python3", "script/audit-character-art-contract.py"]),
    Check("character seed prompt ledger is current", ["python3", "script/build-character-seed-prompt-ledger.py", "--version", "v0.1", "--check"]),
    Check("character seed prompt exports are current", ["python3", "script/export-character-seed-prompts.py", "--version", "v0.1", "--check"]),
    Check("art prompt exports are current", ["python3", "script/export-art-batch-prompts.py", "--all", "--check"]),
    Check("art prompt safety contract", ["script/audit-art-prompt-safety.py"]),
    Check("planned art replacement batches", ["script/audit-art-batch-plan.py", "--all"]),
    Check("art acceptance ledger is current", ["script/build-art-acceptance-ledger.py", "--check"]),
    Check("generated image contact sheets are current", ["script/build-image-contact-sheets.py", "--check"]),
    Check("localization BOM audit", [".agents/skills/victoria3-event/scripts/check_boms.sh"]),
]

RUNTIME_CHECKS = [
    Check("Victoria 3 current log scan", ["script/audit-victoria3-logs.py"]),
    Check("Victoria 3 current-build runtime proof", ["script/audit-victoria3-logs.py", "--require-current-build"]),
]

RELEASE_CHECKS = [
    Check(
        "release art provenance coverage",
        ["script/audit-art-provenance.py", "--strict-generated"],
    ),
    Check(
        "release planned art batch readiness",
        ["script/audit-art-batch-plan.py", "--all", "--strict-ready"],
    ),
    Check(
        "release planned art promotion",
        ["script/promote-art-batch.py", "--all", "--check"],
    ),
    Check(
        "release image size/unused audit",
        ["script/audit-event-images.py", "--strict-size", "--strict-unused"],
    ),
    Check(
        "release generic video art removal",
        ["script/audit-generic-video-art.py", "--strict-no-vanilla-video", "--limit", "80"],
    ),
]


def run_check(check: Check) -> bool:
    print(f"\n== {check.label} ==")
    print("$ " + " ".join(check.command))
    result = subprocess.run(check.command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())
    status = "PASS" if result.returncode == 0 else f"FAIL ({result.returncode})"
    print(f"-- {status}: {check.label}")
    return result.returncode == 0


def checks_for_mode(mode: str, egypt_save: Path | None, allow_silent_first_contact: bool) -> list[Check]:
    checks = list(DEV_CHECKS)
    if mode in {"runtime", "release"}:
        checks.extend(RUNTIME_CHECKS)
    if egypt_save is not None:
        command = ["script/audit-egypt-gameplay-save.py", "--save", str(egypt_save)]
        if allow_silent_first_contact:
            command.append("--allow-silent-first-contact")
        checks.append(Check("Egypt gameplay save proof", command))
    if mode == "release":
        checks.extend(RELEASE_CHECKS)
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("dev", "runtime", "release"),
        default="dev",
        help="dev = static/local checks; runtime = dev + current-build log proof; release = runtime + strict image cleanup + Egypt gameplay save proof",
    )
    parser.add_argument(
        "--egypt-save",
        type=Path,
        help="real Egypt gameplay .v3 save to audit; required in release mode",
    )
    parser.add_argument(
        "--skip-egypt-save",
        action="store_true",
        help="release mode only: run strict script/art/runtime gates without claiming full gameplay acceptance",
    )
    parser.add_argument(
        "--allow-silent-first-contact",
        action="store_true",
        help="pass through to the Egypt save audit when intentionally accepting the startup silent branch",
    )
    args = parser.parse_args()

    print("Common People release readiness audit")
    print(f"mode: {args.mode}")
    if args.skip_egypt_save:
        print("skip_egypt_save: yes")

    if args.skip_egypt_save and args.mode != "release":
        parser.error("--skip-egypt-save is only valid with --mode release")
    if args.skip_egypt_save and args.egypt_save is not None:
        parser.error("--skip-egypt-save cannot be combined with --egypt-save; choose dry-run or gameplay acceptance")
    if args.mode == "release" and args.egypt_save is None and not args.skip_egypt_save:
        print("error: --mode release requires --egypt-save <tested-save>.v3")
        print("       Use --skip-egypt-save only for script/art/runtime dry-runs that are not full release acceptance.")
        return 2

    failed = 0
    checks = checks_for_mode(args.mode, args.egypt_save, args.allow_silent_first_contact)
    for check in checks:
        if not run_check(check):
            failed += 1

    passed = len(checks) - failed
    print("\nSummary")
    print(f"passed: {passed}")
    print(f"failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
