#!/usr/bin/env python3
"""Audit narrative variety in Common People's event audio palette."""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIO_LEDGER_SCRIPT = ROOT / "script" / "build-audio-cue-ledger.py"
sys.dont_write_bytecode = True

MUSIC_CUES = {
    "civil",
    "dramatic",
    "enthusiastic",
    "political",
    "sadness",
    "spiritual",
    "tranquil",
}
STRONG_CUES = {"civil", "dramatic", "enthusiastic", "political", "sadness", "spiritual"}
QUIET_CUES = {"tranquil", "civil", "spiritual"}
NON_LAYLA_MIN_VARIETY_FOR_FOUR_EVENTS = 3
NON_LAYLA_MIN_VARIETY_FOR_TWO_EVENTS = 2
MAX_GLOBAL_TRANQUIL_SHARE = 0.70
MIN_GLOBAL_NON_TRANQUIL_SHARE = 0.25


def load_audio_ledger():
    spec = importlib.util.spec_from_file_location("build_audio_cue_ledger", AUDIO_LEDGER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {AUDIO_LEDGER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def person_for_event(event_id: str) -> str:
    namespace = event_id.split(".", 1)[0]
    if namespace.startswith("cp_"):
        namespace = namespace[3:]
    return namespace.split("_", 1)[0]


def build_summary() -> tuple[list[object], Counter[str], dict[str, Counter[str]], list[tuple[str, str]]]:
    audio = load_audio_ledger()
    cues = audio.collect_cues()
    global_counts: Counter[str] = Counter(cue.cue for cue in cues)
    person_counts: dict[str, Counter[str]] = defaultdict(Counter)
    issues: list[tuple[str, str]] = []

    for cue in cues:
        person_counts[person_for_event(cue.event_id)][cue.cue] += 1

    missing_palette = sorted(MUSIC_CUES - set(global_counts))
    for cue in missing_palette:
        issues.append(("AUDIO_PALETTE_UNUSED", f"music cue `{cue}` is unused across visible events"))

    unknown_music = sorted(cue for cue in global_counts if cue not in MUSIC_CUES)
    for cue in unknown_music:
        issues.append(("AUDIO_PALETTE_UNKNOWN", f"cue `{cue}` is not in the reviewed music-stinger palette"))

    total = sum(global_counts.values())
    tranquil = global_counts.get("tranquil", 0)
    non_tranquil = total - tranquil
    if total:
        tranquil_share = tranquil / total
        non_tranquil_share = non_tranquil / total
        if tranquil_share > MAX_GLOBAL_TRANQUIL_SHARE:
            issues.append((
                "AUDIO_PALETTE_TOO_TRANQUIL",
                f"tranquil cue share is {tranquil_share:.1%}; expected at most {MAX_GLOBAL_TRANQUIL_SHARE:.0%}",
            ))
        if non_tranquil_share < MIN_GLOBAL_NON_TRANQUIL_SHARE:
            issues.append((
                "AUDIO_PALETTE_TOO_FLAT",
                f"non-tranquil cue share is {non_tranquil_share:.1%}; expected at least {MIN_GLOBAL_NON_TRANQUIL_SHARE:.0%}",
            ))

    for person, counts in sorted(person_counts.items()):
        if person == "layla":
            continue
        event_count = sum(counts.values())
        varieties = set(counts)
        if event_count >= 4 and len(varieties) < NON_LAYLA_MIN_VARIETY_FOR_FOUR_EVENTS:
            issues.append((
                "AUDIO_PERSON_VARIETY",
                f"{person} has {event_count} visible event(s) but only {len(varieties)} cue type(s)",
            ))
        if 2 <= event_count < 4 and len(varieties) < NON_LAYLA_MIN_VARIETY_FOR_TWO_EVENTS:
            issues.append((
                "AUDIO_PERSON_VARIETY",
                f"{person} has {event_count} visible event(s) but only {len(varieties)} cue type(s)",
            ))
        if event_count >= 4 and not (varieties & STRONG_CUES):
            issues.append(("AUDIO_PERSON_NO_STRONG_CUE", f"{person} has no non-tranquil narrative cue"))
        if event_count >= 4 and not (varieties & QUIET_CUES):
            issues.append(("AUDIO_PERSON_NO_QUIET_CUE", f"{person} has no quiet/civil/spiritual cue"))

    return cues, global_counts, person_counts, issues


def main() -> int:
    cues, global_counts, person_counts, issues = build_summary()
    total = sum(global_counts.values())
    tranquil = global_counts.get("tranquil", 0)
    non_tranquil = total - tranquil

    print("Common People audio palette audit")
    print(f"Visible non-debug events: {len(cues)}")
    print(f"Music cue categories used: {len(set(global_counts) & MUSIC_CUES)}/{len(MUSIC_CUES)}")
    print(f"Tranquil share: {tranquil}/{total} ({tranquil / total:.1%})" if total else "Tranquil share: n/a")
    print(f"Non-tranquil share: {non_tranquil}/{total} ({non_tranquil / total:.1%})" if total else "Non-tranquil share: n/a")
    print("Palette counts:")
    for cue in sorted(global_counts):
        print(f"  {global_counts[cue]:3}  {cue}")
    print("Person cue variety:")
    for person, counts in sorted(person_counts.items()):
        total_for_person = sum(counts.values())
        labels = ", ".join(f"{cue}={count}" for cue, count in sorted(counts.items()))
        print(f"  {person:8} {len(counts):2} cue type(s), {total_for_person:3} event(s): {labels}")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
