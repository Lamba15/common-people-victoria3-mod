#!/usr/bin/env python3
"""Audit the Common People journal text for personal identity context."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
COMMON = MOD / "common"
EVENTS = MOD / "events"
LOC = MOD / "localization" / "english" / "cp_shared_l_english.yml"

REGISTER_PERSON_RE = re.compile(
    r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)",
    re.DOTALL,
)
LOC_RE = re.compile(r'^\s*([A-Za-z0-9_.-]+):\d+\s+"((?:[^"\\]|\\.)*)"', re.MULTILINE)
EXPECTED_HOME = {
    "bey": "al-Sayyid estate outside Mīt al-Nakhla",
    "dawud": "Alexandria port quarter",
    "farid": "Tanta station road, Lower Egypt",
    "huda": "al-Matariya upstairs room, Cairo",
    "karim": "Bulaq workshop quarter, Cairo",
    "layla": "Mīt al-Nakhla, Lower Egypt",
    "mansur": "al-Mahalla al-Kubra rented bed",
    "mina": "Faggala church courtyard, Cairo",
    "nabil": "Bab al-Khalq police quarter, Cairo",
    "nour": "Mansoura market rooms, Lower Egypt",
    "rashid": "Abdeen office quarter, Cairo",
    "salma": "Ataba exchange rooms, Cairo",
    "samier": "Bulaq workers' lodging, Cairo",
    "soldier": "Kafr al-Gindi family house, Lower Egypt",
    "zaynab": "Mīt al-Nakhla women's courtyards, Lower Egypt",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def uncommented(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def script_files() -> list[Path]:
    return sorted(COMMON.glob("**/cp_*.txt")) + sorted(EVENTS.glob("cp_*.txt"))


def registered_persons() -> list[str]:
    text = "\n".join(uncommented(read(path)) for path in script_files())
    return sorted(set(REGISTER_PERSON_RE.findall(text)))


def loc_entries() -> dict[str, str]:
    return {key: value for key, value in LOC_RE.findall(read(LOC))}


def main() -> int:
    failures: list[str] = []
    people = registered_persons()
    locs = loc_entries()

    active_body = locs.get("cp_common_people_active_body", "")
    personal_status = locs.get("cp_je_common_people_status_personal", "")
    if "Use the name buttons below for personal check-ins" not in personal_status:
        failures.append("cp_je_common_people_status_personal does not explain the action buttons above the body text")
    if "Personal check-ins" in active_body or "Click a name" in active_body:
        failures.append("cp_common_people_active_body still places button guidance below the character body")

    for person in people:
        line_key = f"cp_roster_{person}_line_alive"
        line = locs.get(line_key)
        if line is None:
            failures.append(f"missing active JE row localization: {line_key}")
            continue

        for label in ("#v Occupation#!", "#v Home#!", "#v State#!", "#v Work#!"):
            if label not in line:
                failures.append(f"{line_key} lacks identity subtitle {label}")
        if "\\n#v Home#!" not in line:
            failures.append(f"{line_key} does not put Home on its own line")
        if "\\n#v State#!" not in line:
            failures.append(f"{line_key} does not put State on its own line")
        if "\\n#v Work#!" not in line:
            failures.append(f"{line_key} does not put Work on its own line")
        expected_home = EXPECTED_HOME.get(person)
        if expected_home and f"#v Home#! {expected_home}" not in line:
            failures.append(f"{line_key} does not name its expected home place: {expected_home}")
        state_expr = f"[Country.MakeScope.Var('cp_{person}_state_pointer').GetState.GetStateRegion.GetName]"
        if state_expr not in line:
            failures.append(f"{line_key} does not render the actual home-state pointer")

        for metric in ("@clock! age", "SoL", "@popularity! hope", "@paper! literacy"):
            if metric not in line:
                failures.append(f"{line_key} lacks metric text: {metric}")

        if f"cp_roster_{person}_current" not in line:
            failures.append(f"{line_key} does not include the current-life sentence custom loc")

        # The row should be more than a label and stats. Require at least one
        # full prose sentence after the current-life line.
        sentence_count = line.count(".")
        if sentence_count < 2:
            failures.append(f"{line_key} is too terse; expected biographical prose after the subtitles")

        button_desc = locs.get(f"cp_shared_action_{person}_button_desc", "")
        if "Open a current check-in scene" not in button_desc:
            failures.append(f"cp_shared_action_{person}_button_desc does not explain the check-in action")

    stale_button_descs = sorted(
        key
        for key, value in locs.items()
        if key.startswith("cp_shared_action_")
        and key.endswith("_button_desc")
        and value.startswith("Check in on ")
    )
    for key in stale_button_descs:
        failures.append(f"{key} still uses terse pre-identity tooltip text")

    if failures:
        print("FAIL: Common People JE identity audit")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Common People JE identity audit")
    print(f"registered persons: {len(people)}")
    print("active rows: occupation/home/state/work subtitles present, line-broken, place-specific, and state-aware")
    print("button guidance: status line and action tooltips present")
    print("Issues: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
