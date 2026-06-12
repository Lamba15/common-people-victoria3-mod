#!/usr/bin/env python3
"""Regression tests for the Egypt gameplay save audit."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "script" / "audit-egypt-gameplay-save.py"
ALWAYS_ON = ("layla", "bey", "soldier", "nour", "mina", "zaynab")
WORKPLACE = {
    "layla": "agrarian",
    "bey": "manufacturing",
    "soldier": "military",
    "nour": "public_service",
    "mina": "public_service",
    "zaynab": "public_service",
}
HOME_PLACE = {
    "layla": "mit_al_nakhla",
    "bey": "sayyid_estate",
    "soldier": "kafr_al_gindi",
    "nour": "mansoura",
    "mina": "faggala_cairo",
    "zaynab": "mit_al_nakhla",
}


def var(name: str, var_type: str = "boolean", identity: int | None = 1) -> str:
    identity_line = f"\n\t\t\tidentity={identity}" if identity is not None else ""
    return f"\t\t{{\n\t\t\tflag={name}\n\t\t\tdata={{\n\t\t\t\ttype={var_type}{identity_line}\n\t\t\t}}\n\t\t}}"


def save_text(extra_egy_vars: list[str] | None = None, extra_state_vars: list[str] | None = None) -> str:
    global_vars = [var(f"cp_person_{person}_alive") for person in ALWAYS_ON]
    state_vars = [var(f"cp_{person}_lives_here") for person in ALWAYS_ON]
    egy_vars = [
        var("cp_common_people_je_added"),
        var("cp_first_contact_chosen"),
        var("cp_active_roster_v0_cleaned"),
        var("cp_layla_met_player"),
        var("cp_layla_active_slot", "value", 100000),
    ]
    for person in ALWAYS_ON:
        egy_vars.extend(
            [
                var(f"cp_{person}_alive", "value", 100000),
                var(f"cp_{person}_state_pointer", "state", None),
                var(f"cp_{person}_home_place_{HOME_PLACE[person]}"),
                var(f"cp_{person}_workplace_{WORKPLACE[person]}", "value", 100000),
            ]
        )
    if extra_egy_vars:
        egy_vars.extend(extra_egy_vars)
    if extra_state_vars:
        state_vars.extend(extra_state_vars)

    return "\n".join(
        [
            "date=1836.1.2",
            'meta={ mods={ "Common People" } }',
            "globals={",
            *global_vars,
            "}",
            '1={',
            '\tdefinition="EGY"',
            "\tvariables={",
            *egy_vars,
            "\t}",
            "}",
            "states={",
            "\t4={",
            '\t\tregion="STATE_LOWER_EGYPT"',
            "\t\tvariables={",
            *state_vars,
            "\t\t}",
            "\t}",
            "}",
            "",
        ]
    )


def run_audit(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(AUDIT), "--save", str(path), "--min-date", "1836.1.2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        good_save = tmp_path / "good.v3"
        good_save.write_text(save_text(), encoding="utf-8")
        good = run_audit(good_save)
        if good.returncode != 0:
            print("FAIL: valid synthetic save was rejected")
            print(good.stdout)
            print(good.stderr)
            return 1

        duplicate_slot_save = tmp_path / "duplicate-slot.v3"
        duplicate_slot_save.write_text(
            save_text(
                [
                    var("cp_bey_seen_intro"),
                    var("cp_bey_active_slot", "value", 100000),
                ]
            ),
            encoding="utf-8",
        )
        duplicate = run_audit(duplicate_slot_save)
        if duplicate.returncode == 0 or "duplicate slot value" not in duplicate.stdout:
            print("FAIL: duplicate active slot was not rejected")
            print(duplicate.stdout)
            print(duplicate.stderr)
            return 1

        missing_home_save = tmp_path / "missing-home.v3"
        missing_home_save.write_text(save_text().replace("cp_mina_home_place_faggala_cairo", "cp_mina_removed_home_place"), encoding="utf-8")
        missing_home = run_audit(missing_home_save)
        if missing_home.returncode == 0 or "mina should have exactly one home-place token" not in missing_home.stdout:
            print("FAIL: missing home-place token was not rejected")
            print(missing_home.stdout)
            print(missing_home.stderr)
            return 1

        duplicate_home_marker_save = tmp_path / "duplicate-home-marker.v3"
        duplicate_home_marker_save.write_text(
            save_text(extra_state_vars=[var("cp_mina_lives_here")]),
            encoding="utf-8",
        )
        duplicate_home_marker = run_audit(duplicate_home_marker_save)
        if duplicate_home_marker.returncode == 0 or "mina should have exactly one state home marker" not in duplicate_home_marker.stdout:
            print("FAIL: duplicate state home marker was not rejected")
            print(duplicate_home_marker.stdout)
            print(duplicate_home_marker.stderr)
            return 1

        bad_state_pointer_save = tmp_path / "bad-state-pointer.v3"
        bad_state_pointer_save.write_text(
            save_text().replace("cp_mina_state_pointer\n\t\t\tdata={\n\t\t\t\ttype=state", "cp_mina_state_pointer\n\t\t\tdata={\n\t\t\t\ttype=value"),
            encoding="utf-8",
        )
        bad_state_pointer = run_audit(bad_state_pointer_save)
        if bad_state_pointer.returncode == 0 or "mina journal home-state pointer should be type=state" not in bad_state_pointer.stdout:
            print("FAIL: bad state pointer type was not rejected")
            print(bad_state_pointer.stdout)
            print(bad_state_pointer.stderr)
            return 1

    print("ok: Egypt gameplay save audit regression tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
