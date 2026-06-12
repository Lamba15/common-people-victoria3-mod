#!/usr/bin/env python3
"""Build and check the audio palette review ledger."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "documentation" / "audio-palette-ledger.md"
AUDIT = ROOT / "script" / "audit-audio-palette.py"
sys.dont_write_bytecode = True


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_audio_palette", AUDIT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {AUDIT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def build() -> tuple[str, list[tuple[str, str]]]:
    audit = load_audit()
    cues, global_counts, person_counts, issues = audit.build_summary()
    total = sum(global_counts.values())
    tranquil = global_counts.get("tranquil", 0)
    non_tranquil = total - tranquil

    lines = [
        "# Audio Palette Ledger",
        "",
        "Generated from visible non-debug event audio hooks. Rebuild with:",
        "",
        "```bash",
        "python3 script/build-audio-palette-ledger.py",
        "python3 script/build-audio-palette-ledger.py --check",
        "python3 script/audit-audio-palette.py",
        "```",
        "",
        "This ledger is the review surface for whether Common People's event music still feels deliberate as the roster expands. `documentation/audio-cue-ledger.md` records every individual event cue; this file summarizes palette balance and per-person variety.",
        "",
        "## Contract",
        "",
        "- Every visible event already has one creation cue and one opened cue, enforced by `script/audit-event-audio.py`.",
        "- The seven reviewed Victoria 3 event stingers should all remain in use: civil, dramatic, enthusiastic, political, sadness, spiritual, tranquil.",
        "- Tranquil can dominate quiet conversation scenes, but it must not exceed 70% of visible event cues overall.",
        "- At least 25% of visible events should use a non-tranquil cue so laws, war, death, reforms, protest, spirituality, and breakthroughs do not feel flat.",
        "- Non-Layla people with two or more visible events need at least two cue types; non-Layla people with four or more visible events need at least three cue types.",
        "",
        "## Summary",
        "",
        f"- Visible non-debug events: {len(cues)}",
        f"- Music cue categories used: {len(set(global_counts) & audit.MUSIC_CUES)}/{len(audit.MUSIC_CUES)}",
        f"- Tranquil share: {tranquil}/{total} ({tranquil / total:.1%})" if total else "- Tranquil share: n/a",
        f"- Non-tranquil share: {non_tranquil}/{total} ({non_tranquil / total:.1%})" if total else "- Non-tranquil share: n/a",
        f"- Issues: {len(issues)}",
        "",
        "## Palette Counts",
        "",
        "| Cue | Events | Share |",
        "|---|---:|---:|",
    ]
    for cue, count in sorted(global_counts.items()):
        share = count / total if total else 0
        lines.append(f"| `{cue}` | {count} | {share:.1%} |")

    lines.extend([
        "",
        "## Person Variety",
        "",
        "| Person | Events | Cue Types | Cue Mix |",
        "|---|---:|---:|---|",
    ])
    for person, counts in sorted(person_counts.items()):
        event_count = sum(counts.values())
        labels = ", ".join(f"`{cue}` {count}" for cue, count in sorted(counts.items()))
        lines.append(f"| `{person}` | {event_count} | {len(counts)} | {labels} |")

    lines.extend([
        "",
        "## Checks",
        "",
        "```bash",
        "script/audit-event-audio.py",
        "script/build-audio-cue-ledger.py --check",
        "python3 script/audit-audio-palette.py",
        "python3 script/build-audio-palette-ledger.py --check",
        "```",
    ])

    if issues:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- `{code}`: {message}" for code, message in issues)

    return "\n".join(lines).rstrip() + "\n", issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the ledger is stale or palette issues exist")
    args = parser.parse_args()

    text, issues = build()
    if args.check:
        if issues:
            print("audio palette ledger issues:", file=sys.stderr)
            for code, message in issues:
                print(f"- [{code}] {message}", file=sys.stderr)
            return 1
        current = LEDGER.read_text(encoding="utf-8") if LEDGER.exists() else ""
        if current != text:
            print(f"{rel(LEDGER)} is stale; run python3 script/build-audio-palette-ledger.py", file=sys.stderr)
            return 1
        print(f"ok: {rel(LEDGER)} is current")
        return 0

    LEDGER.write_text(text, encoding="utf-8")
    print(f"wrote {rel(LEDGER)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
