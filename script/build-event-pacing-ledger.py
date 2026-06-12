#!/usr/bin/env python3
"""Build and check the passive event pacing proof ledger."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "documentation" / "event-pacing-ledger.md"
AUDIT = ROOT / "script" / "audit-event-pacing.py"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def audit_fields() -> tuple[dict[str, str], str, int]:
    result = subprocess.run([sys.executable, str(AUDIT)], cwd=ROOT, text=True, capture_output=True, check=False)
    output = result.stdout.rstrip()
    fields: dict[str, str] = {}
    for line in output.splitlines():
        if ": " not in line or line.startswith("- "):
            continue
        key, value = line.split(": ", 1)
        fields[key] = value
    return fields, output, result.returncode


def field(fields: dict[str, str], key: str) -> str:
    return fields.get(key, "missing")


def build() -> tuple[str, list[str]]:
    fields, output, status = audit_fields()
    issues: list[str] = []

    if status != 0:
        issues.append("event pacing audit failed")
    if field(fields, "Issues") != "0":
        issues.append(f"event pacing audit reports {field(fields, 'Issues')} issue(s)")
    if field(fields, "Max ambient fires/year from monthly cadence") != "2":
        issues.append("ordinary ambient yearly cap is not 2")
    if field(fields, "Max routine automatic fires/year from shared cooldown") != "2":
        issues.append("routine automatic yearly cap is not 2")
    if field(fields, "Max passive fires in first campaign year") != "2":
        issues.append("first-year passive yearly cap is not 2")

    lines = [
        "# Event Pacing Ledger",
        "",
        "Generated from `script/audit-event-pacing.py`. Rebuild with:",
        "",
        "```bash",
        "python3 script/build-event-pacing-ledger.py",
        "python3 script/build-event-pacing-ledger.py --check",
        "python3 script/audit-event-pacing.py",
        "```",
        "",
        "## Contract",
        "",
        "- Routine automatic Common People events should land in a reasonable range: 1-2 per in-game year across the whole roster, never 1-2 per person.",
        "- Ordinary monthly ambient routing has a hard cap of 2 visible fires per calendar year by a 183-day global cooldown.",
        "- The first campaign year is also capped at 2 passive fires because the startup first-contact opener marks the same global/person cooldown lane before it opens an event.",
        "- Law reactions and routine world responses consume the same shared visible-story cooldown, so rapid reform, technology, or building sequences cannot open a Common People window for every trigger.",
        "- War-start and revolution-start use shared resolver targets, so a single war or rupture belongs to one authored person response instead of fanning out across every eligible dispatcher.",
        "- The router may stay silent when no eligible story exists; it should never force filler just to hit a minimum.",
        "- Person-specific cooldowns stay at 365 days, so one person cannot dominate the ambient budget even when the global budget is open.",
        "- Critical milestones and player-clicked QA/buttons use separate gatekeepers and are not part of the routine yearly popup budget.",
        "",
        "## Current Static Proof",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| Ambient global cooldown days | {field(fields, 'Ambient global cooldown days')} |",
        f"| Ambient per-person cooldown days | {field(fields, 'Ambient per-person cooldown days')} |",
        f"| First-contact global cooldown days | {field(fields, 'First-contact global cooldown days')} |",
        f"| First-contact per-person cooldown days | {field(fields, 'First-contact per-person cooldown days')} |",
        f"| Law-reaction global cooldown days | {field(fields, 'Law-reaction global cooldown days')} |",
        f"| Law-reaction per-person cooldown days | {field(fields, 'Law-reaction per-person cooldown days')} |",
        f"| World-response global cooldown days | {field(fields, 'World-response global cooldown days')} |",
        f"| World-response per-person cooldown days | {field(fields, 'World-response per-person cooldown days')} |",
        f"| Monthly router calls | {field(fields, 'Monthly router calls')} |",
        f"| Monthly silent branch weights | {field(fields, 'Monthly silent branch weights')} |",
        f"| Ambient pool calls | {field(fields, 'Ambient pool calls')} |",
        f"| Persons with ambient pools | {field(fields, 'Persons with ambient pools')} |",
        f"| World-response calls | {field(fields, 'World-response calls')} |",
        f"| War-start resolver targets | {field(fields, 'War-start resolver targets')} |",
        f"| Revolution resolver targets | {field(fields, 'Revolution resolver targets')} |",
        f"| Startup first-contact visible branches | {field(fields, 'Startup first-contact visible branches')} |",
        f"| Max ambient fires/year from monthly cadence | {field(fields, 'Max ambient fires/year from monthly cadence')} |",
        f"| Max routine automatic fires/year from shared cooldown | {field(fields, 'Max routine automatic fires/year from shared cooldown')} |",
        f"| Max passive fires in first campaign year | {field(fields, 'Max passive fires in first campaign year')} |",
        f"| Audit issues | {field(fields, 'Issues')} |",
        "",
        "## Source Surfaces",
        "",
        "- `mod/common/scripted_effects/cp_shared_firing.txt`: `cp_try_fire_ambient`, `cp_mark_first_contact_budget`, `cp_try_fire_law_reaction`, `cp_try_fire_world_response`, and `cp_roll_for_event`.",
        "- `mod/common/scripted_effects/cp_shared_war.txt`: `cp_roll_war_start_response` chooses the single authored war-start target.",
        "- `mod/common/scripted_effects/cp_shared_firing.txt`: `cp_roll_revolution_response` chooses the single authored revolution target.",
        "- `mod/common/on_actions/cp_on_actions.txt`: the monthly country pulse calls the shared monthly router once, and the revolution hook calls the shared revolution resolver once.",
        "- `mod/events/cp_shared_startup_events.txt`: every visible first-contact branch marks the shared cooldown budget before `trigger_event`.",
        "",
        "## Raw Audit Output",
        "",
        "```text",
        output,
        "```",
    ]

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the pacing ledger is stale or the pacing audit fails")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("event pacing ledger issues:", file=sys.stderr)
            for issue in issues:
                print(f"- {issue}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-event-pacing-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
