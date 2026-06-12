#!/usr/bin/env python3
"""Audit visible Common People event audio hooks and cue palette."""

from __future__ import annotations

import os
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"
EVENTS = MOD / "events"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
OPTION_RE = re.compile(r"(?m)^\s*option\s*=")
CREATED_RE = re.compile(r'\bon_created_soundeffect\s*=\s*"([^"]+)"')
OPENED_RE = re.compile(r'\bon_opened_soundeffect\s*=\s*"([^"]+)"')
GUID_EVENT_RE = re.compile(r"\b(event:/\S+)")

EXPECTED_CREATED = "event:/SFX/UI/Alerts/event_appear"
EXPECTED_OPENED_PREFIX = "event:/MUSIC/Stingers/events/"
EXPECTED_EVENT_STINGERS = {
    "event:/MUSIC/Stingers/events/civil",
    "event:/MUSIC/Stingers/events/dramatic",
    "event:/MUSIC/Stingers/events/enthusiastic",
    "event:/MUSIC/Stingers/events/political",
    "event:/MUSIC/Stingers/events/sadness",
    "event:/MUSIC/Stingers/events/spiritual",
    "event:/MUSIC/Stingers/events/tranquil",
}
KNOWN_V3_GAME_DIRS = [
    Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game"),
]


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


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

            yield {
                "id": match.group(1),
                "path": path,
                "line": start + 1,
                "text": "\n".join(lines[start : i + 1]),
            }
            i += 1


def find_game_dir() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("CP_V3_GAME_DIR"):
        candidates.append(Path(os.environ["CP_V3_GAME_DIR"]))
    candidates.extend(KNOWN_V3_GAME_DIRS)
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def find_guid_file(game_dir: Path | None) -> Path | None:
    if not game_dir:
        return None
    candidate = game_dir / "sound" / "GUIDs.txt"
    return candidate if candidate.exists() else None


def load_guid_events() -> set[str] | None:
    guid_file = find_guid_file(find_game_dir())
    if not guid_file:
        return None
    return set(GUID_EVENT_RE.findall(guid_file.read_text(encoding="utf-8-sig", errors="replace")))


def event_window_uses_opened_sound(game_dir: Path | None) -> bool | None:
    if not game_dir:
        return None
    event_window = game_dir / "gui" / "eventwindow.gui"
    if not event_window.exists():
        return None
    text = event_window.read_text(encoding="utf-8-sig", errors="replace")
    return "Event.GetOnOpenedSoundEvent" in text


def music_definition_files(game_dir: Path | None) -> list[Path]:
    if not game_dir:
        return []
    return [
        path
        for path in (game_dir / "music").glob("**/*.txt")
        if path.is_file()
    ]


def is_visible_non_debug(block: dict[str, object]) -> bool:
    event_id = str(block["id"])
    text = str(block["text"])
    if event_id == "cp_debug.1" or event_id.startswith("cp_debug.") or event_id.startswith("cp_debug_"):
        return False
    if re.search(r"\bhidden\s*=\s*yes\b", text):
        return False
    return bool(OPTION_RE.search(text))


def main() -> int:
    issues: list[tuple[str, str]] = []
    visible_events = []
    created_counts: Counter[str] = Counter()
    opened_counts: Counter[str] = Counter()
    game_dir = find_game_dir()
    guid_file = find_guid_file(game_dir)
    guid_events = load_guid_events()
    opened_hook = event_window_uses_opened_sound(game_dir)
    music_files = music_definition_files(game_dir)

    if opened_hook is False:
        issues.append(("AUDIO_EVENT_WINDOW", "installed gui/eventwindow.gui does not reference Event.GetOnOpenedSoundEvent"))
    if guid_events is not None:
        for stinger in sorted(EXPECTED_EVENT_STINGERS - guid_events):
            issues.append(("AUDIO_STINGER_GUID", f"installed sound/GUIDs.txt lacks expected event stinger {stinger}"))

    for block in iter_event_blocks():
        location = f"{rel(Path(block['path']))}:{block['line']}"
        text = uncommented_text(str(block["text"]))

        if guid_events is not None:
            for sound in CREATED_RE.findall(text) + OPENED_RE.findall(text):
                if sound.startswith("event:/") and sound not in guid_events:
                    issues.append(("AUDIO_GUID", f"{location} references unknown audio event {sound}"))

        if not is_visible_non_debug(block):
            continue

        visible_events.append(block)
        event_id = str(block["id"])
        created = CREATED_RE.findall(text)
        opened = OPENED_RE.findall(text)

        if len(created) != 1:
            issues.append(("AUDIO_CREATED", f"{event_id} at {location} has {len(created)} on_created_soundeffect entries"))
        elif created[0] != EXPECTED_CREATED:
            issues.append(("AUDIO_CREATED", f"{event_id} at {location} uses {created[0]} instead of {EXPECTED_CREATED}"))
        else:
            created_counts[created[0]] += 1

        if len(opened) != 1:
            issues.append(("AUDIO_OPENED", f"{event_id} at {location} has {len(opened)} on_opened_soundeffect entries"))
            continue

        opened_counts[opened[0]] += 1
        if opened[0] not in EXPECTED_EVENT_STINGERS:
            issues.append((
                "AUDIO_OPENED",
                f"{event_id} at {location} uses opened sound outside the reviewed music-stinger palette: {opened[0]}",
            ))

    print("Common People event audio audit")
    print(f"Visible non-debug events: {len(visible_events)}")
    print(f"Game dir: {game_dir if game_dir else '<not found>'}")
    print(f"Audio GUID validation: {'enabled: ' + str(guid_file) if guid_events is not None else 'skipped'}")
    print(f"Event window opened hook: {'enabled' if opened_hook else 'skipped' if opened_hook is None else 'missing'}")
    print(f"Music definition files: {len(music_files)}")
    print("Created sounds:")
    for sound, count in sorted(created_counts.items()):
        print(f"  {count:3}  {sound}")
    print("Opened cues:")
    for sound, count in sorted(opened_counts.items()):
        label = sound.removeprefix(EXPECTED_OPENED_PREFIX)
        print(f"  {count:3}  {label}")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
