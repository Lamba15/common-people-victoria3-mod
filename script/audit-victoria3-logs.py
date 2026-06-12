#!/usr/bin/env python3
"""Summarize Victoria 3 launcher state and Common People log findings."""

from __future__ import annotations

import json
import os
import re
import sys
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path


DEFAULT_USER_DIR = Path.home() / ".local/share/Paradox Interactive/Victoria 3"
USER_DIR = Path(os.environ.get("V3_USER_DIR", DEFAULT_USER_DIR))
LOG_DIR = USER_DIR / "logs"
CONTENT_LOAD = USER_DIR / "content_load.json"
ROOT = Path(__file__).resolve().parents[1]
REPO_MOD = ROOT / "mod"
LOCAL_MOD_LINK = USER_DIR / "mod" / "Common People"

DEFAULT_GAME_DIR = Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3")
GAME_DIR = Path(os.environ.get("CP_V3_INSTALL_DIR", DEFAULT_GAME_DIR))
DEFAULT_APP_MANIFEST = Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/appmanifest_529340.acf")
APP_MANIFEST = Path(os.environ.get("CP_V3_APP_MANIFEST", DEFAULT_APP_MANIFEST))


PATTERNS = [
    ("VERSION_MISMATCH", re.compile(r"Common People .*does not match game version", re.I)),
    ("NO_DEFAULT_OPTION", re.compile(r"No default option in event (cp_[\w.]+)", re.I)),
    ("HIDDEN_WITH_OPTIONS", re.compile(r"hidden event with options.*(cp_[\w.]+)", re.I)),
    ("DUPLICATE_EVENT_ID", re.compile(r"Duplicated event ID|Duplicate event id", re.I)),
    ("DUPLICATE_IMMEDIATE", re.compile(r"There is more than one '_Immediate' defined:.*(?:events|common)/cp_", re.I)),
    ("UNEXPECTED_TOKEN", re.compile(r"Unexpected token.*|Error: .*Unexpected", re.I)),
    ("SCRIPT_SYSTEM_ERROR", re.compile(r"Script system error:.*|Wrong scope for trigger:.*", re.I)),
    ("MISSING_LOCALIZATION", re.compile(r"(cp_[\w.]+).*Missing localization|Missing localization.*(cp_[\w.]+)", re.I)),
    ("SCRIPT_BOM_WARNING", re.compile(r"File '.*(?:common|events)/.*cp_.*\.txt' should be in utf8-bom encoding", re.I)),
    ("BAD_SCRIPT_VALUE", re.compile(r"Badly read script value .*(?:common|events)/.*cp_.*\.txt", re.I)),
    ("CP_VARIABLE_USED_NEVER_SET", re.compile(r"Variable 'cp_[^']+' is used but is never set", re.I)),
    ("COMMON_PEOPLE", re.compile(r"Common People|cp_layla|cp_shared|cp_debug|cp_person", re.I)),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def normalize_enabled_mod(entry: object) -> str:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        for key in ("name", "displayName", "id"):
            if key in entry:
                return str(entry[key])
        if "path" in entry:
            path = Path(str(entry["path"]))
            return path.name or str(entry["path"])
        return json.dumps(entry, sort_keys=True)
    return str(entry)


def load_enabled_mods() -> list[str]:
    try:
        data = json.loads(CONTENT_LOAD.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return ["<content_load.json is invalid json>"]
    mods = data.get("enabledMods", [])
    return [normalize_enabled_mod(mod) for mod in mods] if isinstance(mods, list) else ["<enabledMods is not a list>"]


def newest_system_version() -> str:
    system_log = LOG_DIR / "system.log"
    text = read_text(system_log)
    for line in text.splitlines():
        if "Exe Git Version:" in line:
            return line.strip()
    return "<no system.log version line found>"


def installed_branch() -> str:
    return read_text(GAME_DIR / "caligula_branch.txt").strip()


def newest_system_branch() -> str:
    line = newest_system_version()
    match = re.search(r"Exe Git Version:\s*([^:]+?)\s*:", line)
    return match.group(1).strip() if match else ""


def parse_steam_acf(path: Path) -> dict[str, str]:
    text = read_text(path)
    pairs = re.findall(r'"([^"]+)"\s+"([^"]*)"', text)
    return dict(pairs)


def iso_from_unix(value: str) -> str:
    try:
        return datetime.fromtimestamp(int(value)).isoformat()
    except (TypeError, ValueError, OSError):
        return value or "<unknown>"


def installed_game_summary() -> str:
    parts: list[str] = []

    branch = installed_branch()
    checksum = read_text(GAME_DIR / "binaries" / "checksum.txt").strip()
    if branch:
        parts.append(branch)
    if checksum:
        parts.append(f"checksum={checksum[-4:]}")

    manifest = parse_steam_acf(APP_MANIFEST)
    if manifest.get("buildid"):
        parts.append(f"buildid={manifest['buildid']}")
    if manifest.get("LastUpdated"):
        parts.append(f"updated={iso_from_unix(manifest['LastUpdated'])}")

    if not parts:
        return f"<no installed-game metadata found at {GAME_DIR}>"
    return " ".join(parts)


def common_people_install_summary() -> str:
    if not LOCAL_MOD_LINK.exists() and not LOCAL_MOD_LINK.is_symlink():
        return f"missing: expected {LOCAL_MOD_LINK}"

    try:
        resolved = LOCAL_MOD_LINK.resolve(strict=True)
    except FileNotFoundError:
        return f"broken symlink: {LOCAL_MOD_LINK} -> {os.readlink(LOCAL_MOD_LINK)}"

    marker = "ok" if resolved == REPO_MOD.resolve() else "different-target"
    link_type = "symlink" if LOCAL_MOD_LINK.is_symlink() else "directory"
    return f"{marker}: {link_type} {LOCAL_MOD_LINK} -> {resolved}"


def common_people_install_ok() -> bool:
    return common_people_install_summary().startswith("ok:")


def file_mtime(path: Path) -> float | None:
    try:
        return path.stat().st_mtime
    except FileNotFoundError:
        return None


def format_mtime(value: float | None) -> str:
    if value is None:
        return "<missing>"
    return datetime.fromtimestamp(value).isoformat(timespec="seconds")


def repo_relative(path: Path | None) -> str:
    if path is None:
        return "<none>"
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def newest_shipped_mod_file() -> tuple[Path | None, float | None]:
    if not REPO_MOD.is_dir():
        return None, None

    newest_path: Path | None = None
    newest_mtime = -1.0
    for path in REPO_MOD.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime > newest_mtime:
            newest_path = path
            newest_mtime = mtime

    if newest_path is None:
        return None, None
    return newest_path, newest_mtime


def log_files(include_history: bool) -> list[Path]:
    if not LOG_DIR.is_dir():
        return []
    if include_history:
        return sorted(LOG_DIR.glob("*.log"))
    names = [
        "debug.log",
        "dedicated_server.log",
        "error.log",
        "game.log",
        "system.log",
        "warning.log",
    ]
    return [LOG_DIR / name for name in names if (LOG_DIR / name).is_file()]


def scan_logs(paths: list[Path]) -> dict[str, list[tuple[str, int, str]]]:
    hits: dict[str, list[tuple[str, int, str]]] = {name: [] for name, _ in PATTERNS}

    for path in paths:
        text = read_text(path)
        for line_no, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS:
                if pattern.search(line):
                    hits[name].append((path.name, line_no, line.strip()))
    return hits


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--history",
        action="store_true",
        help="scan rotated numbered logs as well as the current log files",
    )
    parser.add_argument(
        "--require-current-build",
        action="store_true",
        help="fail unless current logs prove Common People was run on the installed Victoria 3 build",
    )
    args = parser.parse_args()

    enabled_mods = load_enabled_mods()
    scanned_files = log_files(args.history)
    hits = scan_logs(scanned_files)
    installed = installed_branch()
    last_run = newest_system_branch()
    newest_mod_path, newest_mod_mtime = newest_shipped_mod_file()
    system_log_mtime = file_mtime(LOG_DIR / "system.log")
    runtime_status = "unknown"
    if installed and last_run:
        runtime_status = "current-build" if installed == last_run else "stale-run"

    mod_runtime_status = "unknown"
    if newest_mod_mtime is not None and system_log_mtime is not None:
        mod_runtime_status = (
            "logs-after-latest-mod-file"
            if system_log_mtime + 1 >= newest_mod_mtime
            else "logs-predate-latest-mod-file"
        )

    print("Victoria 3 log audit")
    print(f"user_dir: {USER_DIR}")
    print(f"installed:{installed_game_summary()}")
    print(f"mod_link: {common_people_install_summary()}")
    print(f"system:   {newest_system_version()}")
    print(f"runtime:  {runtime_status}")
    print(f"mod_time: {format_mtime(newest_mod_mtime)} {repo_relative(newest_mod_path)}")
    print(f"log_time: {format_mtime(system_log_mtime)} system.log")
    print(f"mod_run:  {mod_runtime_status}")
    print(f"enabled:  {enabled_mods}")
    print(f"scope:    {'current + history' if args.history else 'current logs only'}")
    print(f"logs:     {', '.join(path.name for path in scanned_files) if scanned_files else '<none>'}")
    print("")

    if "Common People" not in enabled_mods:
        print("WARNING: Common People is not enabled in content_load.json.")

    proof_failures: list[str] = []
    if args.require_current_build:
        if "Common People" not in enabled_mods:
            proof_failures.append("Common People is not enabled in content_load.json")
        if not common_people_install_ok():
            proof_failures.append(f"Common People local mod link is not correct: {common_people_install_summary()}")
        if not installed:
            proof_failures.append(f"installed Victoria 3 branch was not found at {GAME_DIR / 'caligula_branch.txt'}")
        if not last_run:
            proof_failures.append("current system.log does not contain an Exe Git Version line")
        if installed and last_run and installed != last_run:
            proof_failures.append(f"current system.log is {last_run}, but installed game is {installed}")
        if newest_mod_mtime is None:
            proof_failures.append(f"no shipped mod files were found under {REPO_MOD}")
        if system_log_mtime is None:
            proof_failures.append(f"current system.log was not found at {LOG_DIR / 'system.log'}")
        if (
            newest_mod_mtime is not None
            and system_log_mtime is not None
            and system_log_mtime + 1 < newest_mod_mtime
        ):
            proof_failures.append(
                "current system.log predates latest shipped mod file "
                f"({repo_relative(newest_mod_path)} at {format_mtime(newest_mod_mtime)}); "
                "relaunch Victoria 3 before claiming this tree was loaded"
            )
        if not hits["COMMON_PEOPLE"]:
            proof_failures.append(
                "current logs contain no Common People evidence; wait for script compilation or relaunch with the mod enabled"
            )

    important = [
        "VERSION_MISMATCH",
        "NO_DEFAULT_OPTION",
        "HIDDEN_WITH_OPTIONS",
        "DUPLICATE_EVENT_ID",
        "DUPLICATE_IMMEDIATE",
        "UNEXPECTED_TOKEN",
        "SCRIPT_SYSTEM_ERROR",
        "MISSING_LOCALIZATION",
        "SCRIPT_BOM_WARNING",
        "BAD_SCRIPT_VALUE",
        "CP_VARIABLE_USED_NEVER_SET",
    ]

    total_important = 0
    for name in important:
        rows = hits[name]
        total_important += len(rows)
        print(f"{name}: {len(rows)}")
        for file_name, line_no, line in rows[:20]:
            print(f"  {file_name}:{line_no}: {line}")
        if len(rows) > 20:
            print(f"  ... {len(rows) - 20} more")

    common_people_rows = hits["COMMON_PEOPLE"]
    print(f"COMMON_PEOPLE_LINES: {len(common_people_rows)}")
    for file_name, line_no, line in common_people_rows[:20]:
        print(f"  {file_name}:{line_no}: {line}")
    if len(common_people_rows) > 20:
        print(f"  ... {len(common_people_rows) - 20} more")

    if args.require_current_build:
        print(f"RUNTIME_PROOF_FAILURES: {len(proof_failures)}")
        for failure in proof_failures:
            print(f"  {failure}")

    return 1 if total_important or proof_failures else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        sys.exit(1)
