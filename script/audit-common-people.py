#!/usr/bin/env python3
"""Static audit for Common People Victoria 3 event content.

This is intentionally lightweight: it does not try to fully parse Paradox
script, but it catches the failure modes that have repeatedly shown up in
Victoria 3 logs for this project.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mod"

EVENT_DEF_RE = re.compile(r"^\s*([a-zA-Z0-9_]+\.[0-9]+)\s*=\s*\{")
TOP_LEVEL_BLOCK_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\{")
LOC_KEY_RE = re.compile(r"^\s*([A-Za-z0-9_.-]+):\d+\s+")
IMAGE_RE = re.compile(r'event_image\s*=\s*\{[^}]*?\b(texture|video)\s*=\s*"([^"]+)"', re.S)
TRIGGER_EVENT_RE = re.compile(r"trigger_event\s*=\s*\{[^}]*?\bid\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)", re.S)
GATEKEEPER_EVENT_RE = re.compile(r"\bevent\s*=\s*([a-zA-Z0-9_]+\.[0-9]+)")
LOC_FIELD_RE = re.compile(r"\b(?:title|desc|flavor)\s*=\s*([A-Za-z0-9_.-]+)")
OPTION_NAME_RE = re.compile(r"\bname\s*=\s*([A-Za-z0-9_.-]+)")
ALIVE_HAS_RE = re.compile(r"\bhas_variable\s*=\s*(cp_(?:[A-Za-z0-9_]+|\$person\$)_alive)\b")
SOUND_RE = re.compile(r'\bon_(?:created|opened)_soundeffect\s*=\s*"([^"]+)"')
GUID_EVENT_RE = re.compile(r"\b(event:/\S+)")
LAW_TYPE_RE = re.compile(r"\blaw_type:(law_[A-Za-z0-9_]+)\b")
LAW_REACTION_CALL_RE = re.compile(
    r"cp_try_fire_law_reaction\s*=\s*\{[^}]*?\bevent\s*=\s*(cp_[A-Za-z0-9_]+\.[0-9]+)[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)
SHARED_DIRECT_GATEKEEPER_RE = re.compile(r"\bcp_try_fire_(?:ambient|world_response|milestone|button)\s*=")
DIRECT_PERSON_VARIABLE_MUTATION_RE = re.compile(
    r"\b(?:set|change|add|subtract|remove|clamp)_variable\s*=\s*(cp_(?!person_)[A-Za-z0-9_]+)\b"
    r"|\b(?:set|change|add|subtract|remove|clamp)_variable\s*=\s*\{[^}\n]*?\bname\s*=\s*(cp_(?!person_)[A-Za-z0-9_]+)\b"
)
LOC_DIRECT_TAG_RE = re.compile(r"\[[a-z]:[A-Z0-9_]+\.")
LOC_RULER_GETTITLE_RE = re.compile(r"\bGetRuler\.GetTitle\b")
REGISTER_PERSON_RE = re.compile(r"cp_register_person\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bcountry\s*=\s*([A-Za-z0-9_]+)", re.S)
CP_YES_CALL_RE = re.compile(r"^\s*(cp_[A-Za-z0-9_]+)\s*=\s*yes\b")
SIGNED_POSITIVE_NUMBER_RE = re.compile(r"\b([A-Za-z0-9_]+)\s*=\s*\+[0-9]")
CP_VARIABLE_READ_RE = re.compile(r"\bhas_(?:global_)?variable\s*=\s*(cp_[A-Za-z0-9_]+)\b|\bvar:(cp_[A-Za-z0-9_]+)\b")
CP_VARIABLE_WRITE_RE = re.compile(
    r"\b(?:set|change|add|subtract)_(?:global_)?variable\s*=\s*(cp_[A-Za-z0-9_]+)\b"
    r"|\b(?:set|change|add|subtract)_(?:global_)?variable\s*=\s*\{[^}]*?\bname\s*=\s*(cp_[A-Za-z0-9_]+)\b",
    re.S,
)
MARK_EVENT_SEEN_CALL_RE = re.compile(
    r"cp_mark_event_seen\s*=\s*\{[^}]*?\bperson\s*=\s*([A-Za-z0-9_]+)[^}]*?\bid\s*=\s*([A-Za-z0-9_]+)",
    re.S,
)
CP_SCRIPTED_CALL_RE = re.compile(r"^\s*(cp_[A-Za-z0-9_]+)\s*=\s*(?:yes|\{)", re.M)

KNOWN_V3_GAME_DIRS = [
    Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3/game"),
]
KNOWN_V3_INSTALL_DIRS = [
    Path("/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3"),
]


def script_files():
    return sorted((MOD / "common").glob("**/*.txt")) + sorted((MOD / "events").glob("*.txt"))


def strip_comment(line: str) -> str:
    return line.split("#", 1)[0]


def iter_blocks(path: Path):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
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


def event_options(block: str) -> int:
    return len(re.findall(r"(?m)^\s*option\s*=", block))


def event_default_options(block: str) -> int:
    return len(re.findall(r"\bdefault_option\s*=\s*yes\b", block))


def uncommented_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


def loc_files():
    return sorted((MOD / "localization").glob("**/*.yml"))


def event_files():
    return sorted((MOD / "events").glob("*.txt"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def has_nearby_value_check(lines: list[str], index: int, variable: str) -> bool:
    window = " ".join(strip_comment(line) for line in lines[index : index + 4])
    return f"var:{variable}" in window


def find_guid_file() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("CP_V3_GAME_DIR"):
        candidates.append(Path(os.environ["CP_V3_GAME_DIR"]) / "sound" / "GUIDs.txt")
    candidates.extend(path / "sound" / "GUIDs.txt" for path in KNOWN_V3_GAME_DIRS)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def find_game_dir() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("CP_V3_GAME_DIR"):
        candidates.append(Path(os.environ["CP_V3_GAME_DIR"]))
    candidates.extend(KNOWN_V3_GAME_DIRS)
    for candidate in candidates:
        if (candidate / "common" / "on_actions").exists():
            return candidate
    return None


def find_install_dir() -> Path | None:
    candidates: list[Path] = []
    if os.environ.get("CP_V3_INSTALL_DIR"):
        candidates.append(Path(os.environ["CP_V3_INSTALL_DIR"]))
    if os.environ.get("CP_V3_GAME_DIR"):
        game_dir = Path(os.environ["CP_V3_GAME_DIR"])
        candidates.append(game_dir.parent if game_dir.name == "game" else game_dir)
    candidates.extend(KNOWN_V3_INSTALL_DIRS)
    for candidate in candidates:
        if (candidate / "caligula_branch.txt").exists():
            return candidate
    game_dir = find_game_dir()
    if game_dir and game_dir.name == "game" and (game_dir.parent / "caligula_branch.txt").exists():
        return game_dir.parent
    return None


def installed_game_version() -> str | None:
    install_dir = find_install_dir()
    if not install_dir:
        return None
    branch = (install_dir / "caligula_branch.txt").read_text(encoding="utf-8-sig", errors="replace").strip()
    match = re.search(r"(\d+\.\d+\.\d+)", branch)
    return match.group(1) if match else None


def version_pattern_matches(pattern: str, version: str) -> bool:
    regex = "^" + re.escape(pattern).replace(r"\*", r".*") + "$"
    return re.match(regex, version) is not None


def load_guid_events() -> set[str] | None:
    guid_file = find_guid_file()
    if not guid_file:
        return None
    text = guid_file.read_text(encoding="utf-8-sig", errors="replace")
    return set(GUID_EVENT_RE.findall(text))


def registered_persons() -> list[str]:
    text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    return sorted({match.group(1) for match in REGISTER_PERSON_RE.finditer(text)})


def top_level_blocks(path: Path) -> list[tuple[str, int]]:
    blocks: list[tuple[str, int]] = []
    depth = 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
        clean = strip_comment(line)
        if depth == 0:
            match = TOP_LEVEL_BLOCK_RE.match(clean)
            if match:
                blocks.append((match.group(1), line_no))
        depth += clean.count("{")
        depth -= clean.count("}")
        depth = max(depth, 0)
    return blocks


def named_top_level_block_text(path: Path, name: str) -> str:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    i = 0
    while i < len(lines):
        clean = strip_comment(lines[i])
        match = TOP_LEVEL_BLOCK_RE.match(clean)
        if not match or match.group(1) != name:
            i += 1
            continue

        start = i
        depth = 0
        seen_open = False
        while i < len(lines):
            current = strip_comment(lines[i])
            depth += current.count("{")
            depth -= current.count("}")
            if "{" in current:
                seen_open = True
            if seen_open and depth <= 0:
                break
            i += 1
        return "\n".join(lines[start : i + 1])
    return ""


def effect_body_items(block_text: str) -> list[str]:
    effect_match = re.search(r"\beffect\s*=\s*\{", block_text)
    if not effect_match:
        return []
    open_pos = block_text.index("{", effect_match.start())
    depth = 0
    effect_end = None
    for pos in range(open_pos, len(block_text)):
        char = block_text[pos]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                effect_end = pos
                break
    if effect_end is None:
        return []

    lines = block_text[open_pos + 1 : effect_end].splitlines()
    items: list[str] = []
    i = 0
    while i < len(lines):
        start = i
        while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
            i += 1
        if i >= len(lines):
            break

        item_start = start
        depth = 0
        seen_open = False
        while i < len(lines):
            clean = strip_comment(lines[i])
            depth += clean.count("{")
            depth -= clean.count("}")
            if "{" in clean:
                seen_open = True
            i += 1
            if seen_open and depth <= 0:
                break
        items.append("\n".join(lines[item_start:i]))
    return items


def vanilla_on_actions() -> set[str] | None:
    game_dir = find_game_dir()
    if not game_dir:
        return None
    on_action_dir = game_dir / "common" / "on_actions"
    hooks: set[str] = set()
    for path in sorted(on_action_dir.glob("*.txt")):
        hooks.update(name for name, _line_no in top_level_blocks(path))
    return hooks


def vanilla_laws() -> set[str] | None:
    game_dir = find_game_dir()
    if not game_dir:
        return None
    law_dir = game_dir / "common" / "laws"
    if not law_dir.exists():
        return None
    laws: set[str] = set()
    for path in sorted(law_dir.glob("*.txt")):
        laws.update(name for name, _line_no in top_level_blocks(path) if name.startswith("law_"))
    return laws


def cp_scripted_definitions() -> set[str]:
    definitions: set[str] = set()
    for folder in ("scripted_effects", "scripted_triggers"):
        for path in sorted((MOD / "common" / folder).glob("*.txt")):
            definitions.update(name for name, _line_no in top_level_blocks(path) if name.startswith("cp_"))
    return definitions


def cp_scripted_definition_texts() -> dict[str, str]:
    definitions: dict[str, str] = {}
    for folder in ("scripted_effects", "scripted_triggers"):
        for path in sorted((MOD / "common" / folder).glob("*.txt")):
            for name, _line_no in top_level_blocks(path):
                if name.startswith("cp_"):
                    definitions[name] = named_top_level_block_text(path, name)
    return definitions


def line_no_for_match(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def first_group(match: re.Match[str]) -> str:
    return next(group for group in match.groups() if group)


def image_size(path: Path) -> tuple[int, int] | None:
    try:
        with Image.open(path) as image:
            return image.size
    except (FileNotFoundError, OSError):
        return None


def known_event_videos() -> set[str]:
    videos: set[str] = set()
    search_roots = [MOD / "gfx" / "event_pictures"]
    game_dir = find_game_dir()
    if game_dir:
        search_roots.append(game_dir)

    for root in search_roots:
        if not root.exists():
            continue
        if root == MOD / "gfx" / "event_pictures":
            candidates = sorted(root.glob("*.bk2"))
        else:
            candidates = sorted(root.glob("**/gfx/event_pictures/*.bk2"))
        for path in candidates:
            videos.add(path.stem)
            videos.add(f"gfx/event_pictures/{path.name}")
    return videos


def is_hidden_event(event_texts: dict[str, str], event_id: str) -> bool:
    return bool(re.search(r"\bhidden\s*=\s*yes\b", event_texts.get(event_id, "")))


def is_orphan_event(event_texts: dict[str, str], event_id: str) -> bool:
    return bool(re.search(r"\borphan\s*=\s*yes\b", uncommented_text(event_texts.get(event_id, ""))))


def is_debug_event_id(event_id: str) -> bool:
    return event_id == "cp_debug.1" or event_id.startswith("cp_debug.") or event_id.startswith("cp_debug_")


def is_debug_event_file(path: Path) -> bool:
    return path.name.startswith("cp_debug") and path.name.endswith("_events.txt")


def is_debug_script_file(path: Path) -> bool:
    if is_debug_event_file(path):
        return True
    try:
        path.relative_to(MOD / "common")
    except ValueError:
        return False
    return path.name.startswith("cp_debug")


def calls_activation_boundary(text: str, definitions: dict[str, str], seen: set[str] | None = None) -> bool:
    clean = uncommented_text(text)
    if re.search(r"\bcp_mark_event_seen\s*=", clean) or re.search(r"\bcp_spotlight_person\s*=", clean):
        return True

    seen = set() if seen is None else seen
    for call in CP_SCRIPTED_CALL_RE.findall(clean):
        if call in seen or call not in definitions:
            continue
        seen.add(call)
        if calls_activation_boundary(definitions[call], definitions, seen):
            return True
    return False


def main() -> int:
    issues: list[tuple[str, str]] = []
    warnings: list[tuple[str, str]] = []
    guid_events = load_guid_events()
    on_action_hooks = vanilla_on_actions()
    law_types = vanilla_laws()
    game_version = installed_game_version()
    cp_definitions = cp_scripted_definitions()
    cp_definition_texts = cp_scripted_definition_texts()
    event_videos = known_event_videos()

    for path in script_files():
        if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
            issues.append(("SCRIPT_BOM", f"{rel(path)} is missing UTF-8 BOM"))

    metadata_path = MOD / ".metadata" / "metadata.json"
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        metadata = {}
        issues.append(("METADATA", f"{rel(metadata_path)} is missing"))
    except json.JSONDecodeError as exc:
        metadata = {}
        issues.append(("METADATA", f"{rel(metadata_path)} is invalid JSON: {exc}"))

    supported_game_version = metadata.get("supported_game_version")
    if not supported_game_version:
        issues.append(("METADATA_VERSION", f"{rel(metadata_path)} has no supported_game_version entry"))
    elif game_version is not None and not version_pattern_matches(str(supported_game_version), game_version):
        issues.append((
            "METADATA_VERSION",
            f"{rel(metadata_path)} supported_game_version {supported_game_version!r} does not match installed Victoria 3 {game_version}",
        ))

    picture = metadata.get("picture")
    if not picture:
        issues.append(("THUMBNAIL", f"{rel(metadata_path)} has no picture entry"))
    elif Path(str(picture)).is_absolute() or ".." in Path(str(picture)).parts:
        issues.append(("THUMBNAIL", f"{rel(metadata_path)} picture must be a local filename, got {picture!r}"))
    else:
        launcher_thumbnail = MOD / ".metadata" / str(picture)
        size = image_size(launcher_thumbnail)
        if size is None:
            issues.append(("THUMBNAIL", f"{rel(metadata_path)} picture points to missing/unreadable {rel(launcher_thumbnail)}"))
        elif size != (600, 333):
            issues.append(("THUMBNAIL", f"{rel(launcher_thumbnail)} is {size[0]}x{size[1]}, expected 600x333"))

    workshop_thumbnail = MOD / "thumbnail.png"
    size = image_size(workshop_thumbnail)
    if size is None:
        issues.append(("THUMBNAIL", f"{rel(workshop_thumbnail)} is missing or unreadable"))
    elif size != (512, 512):
        issues.append(("THUMBNAIL", f"{rel(workshop_thumbnail)} is {size[0]}x{size[1]}, expected 512x512"))

    loc_keys: Counter[str] = Counter()
    loc_locations: defaultdict[str, list[str]] = defaultdict(list)
    for path in loc_files():
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            issues.append(("LOC_BOM", f"{rel(path)} is missing UTF-8 BOM"))
        text = raw.decode("utf-8-sig", errors="replace").splitlines()
        for line_no, line in enumerate(text, 1):
            if not line.lstrip().startswith("#"):
                direct_tag = LOC_DIRECT_TAG_RE.search(line)
                if direct_tag:
                    issues.append((
                        "LOC_DIRECT_TAG_SCOPE",
                        f"{rel(path)}:{line_no} uses {direct_tag.group(0)!r}; localization cannot resolve c:TAG directly, use ROOT.GetCountry or a saved SCOPE.sCountry(...)",
                    ))
                if LOC_RULER_GETTITLE_RE.search(line):
                    issues.append((
                        "LOC_RULER_TITLE_METHOD",
                        f"{rel(path)}:{line_no} uses GetRuler.GetTitle; vanilla 1.13 localization uses GetRuler.GetPrimaryRoleTitle",
                    ))
            match = LOC_KEY_RE.match(line)
            if not match:
                continue
            key = match.group(1)
            loc_keys[key] += 1
            loc_locations[key].append(f"{rel(path)}:{line_no}")

    for key, count in loc_keys.items():
        if count > 1:
            warnings.append(("LOC_DUP", f"{key} appears {count} times at {', '.join(loc_locations[key])}"))

    events = []
    event_ids: Counter[str] = Counter()
    event_locations: defaultdict[str, list[str]] = defaultdict(list)
    event_texts: dict[str, str] = {}
    for path in event_files():
        for block in iter_blocks(path):
            events.append(block)
            event_ids[block["id"]] += 1
            event_locations[block["id"]].append(f"{rel(block['path'])}:{block['line']}")
            event_texts[block["id"]] = block["text"]

    for event_id, count in event_ids.items():
        if count > 1:
            issues.append(("EVENT_DUP", f"{event_id} appears {count} times at {', '.join(event_locations[event_id])}"))

    for block in events:
        event_id = block["id"]
        num = int(event_id.rsplit(".", 1)[1])
        location = f"{rel(block['path'])}:{block['line']}"
        text = block["text"]
        options = event_options(text)
        defaults = event_default_options(text)
        hidden = bool(re.search(r"\bhidden\s*=\s*yes\b", text))
        visible_non_debug = options and not hidden and not is_debug_event_id(event_id)

        if num > 9999:
            issues.append(("EVENT_ID_RANGE", f"{event_id} at {location} uses a 5+ digit event number"))
        if hidden and options:
            issues.append(("HIDDEN_OPTIONS", f"{event_id} at {location} is hidden but has option blocks"))
        if options and defaults != 1:
            issues.append(("DEFAULT_OPTION", f"{event_id} at {location} has {defaults} default_option entries across {options} option blocks"))
        if visible_non_debug:
            if not IMAGE_RE.search(text):
                issues.append(("EVENT_IMAGE", f"{event_id} at {location} has no event_image block"))
            if "on_created_soundeffect" not in text:
                issues.append(("EVENT_AUDIO", f"{event_id} at {location} has no on_created_soundeffect"))
            if "on_opened_soundeffect" not in text:
                issues.append(("EVENT_AUDIO", f"{event_id} at {location} has no on_opened_soundeffect"))
            if not calls_activation_boundary(text, cp_definition_texts):
                issues.append((
                    "EVENT_JE_ACTIVATION",
                    f"{event_id} at {location} does not call cp_mark_event_seen/cp_spotlight_person directly or through a scripted effect; visible Common People events must activate the shared JE roster",
                ))

        clean_text = uncommented_text(text)
        loc_refs = LOC_FIELD_RE.findall(clean_text)
        option_depth = 0
        for line in clean_text.splitlines():
            stripped = line.strip()
            if stripped.startswith("option ="):
                loc_refs.extend(OPTION_NAME_RE.findall(stripped))
                option_depth += stripped.count("{") - stripped.count("}")
                continue
            if option_depth > 0 and stripped.startswith("name ="):
                loc_refs.extend(OPTION_NAME_RE.findall(stripped))
            if option_depth > 0:
                option_depth += stripped.count("{") - stripped.count("}")

        for loc_ref in loc_refs:
            if loc_ref not in loc_keys and not loc_ref.endswith(".0001"):
                warnings.append(("LOC_MISSING", f"{event_id} at {location} references missing loc key {loc_ref}"))

        for media_type, image in IMAGE_RE.findall(text):
            if media_type == "texture":
                image_path = MOD / image
                if not image_path.exists():
                    issues.append(("IMAGE_MISSING", f"{event_id} at {location} references missing image {image}"))
            elif image not in event_videos:
                issues.append(("IMAGE_MISSING", f"{event_id} at {location} references missing video {image}"))

    production_triggered = Counter()
    debug_triggered = Counter()
    for path in sorted((MOD / "common").glob("**/*.txt")) + event_files():
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        triggered = debug_triggered if is_debug_script_file(path) else production_triggered
        for event_id in TRIGGER_EVENT_RE.findall(text):
            triggered[event_id] += 1
        for event_id in GATEKEEPER_EVENT_RE.findall(text):
            triggered[event_id] += 1

    all_triggered = production_triggered + debug_triggered
    for event_id in sorted(all_triggered):
        if event_id not in event_ids:
            issues.append((
                "TRIGGER_MISSING",
                f"{event_id} is triggered {all_triggered[event_id]} times but no event definition was found",
            ))

    for event_id in sorted(production_triggered):
        if event_id in event_texts and is_orphan_event(event_texts, event_id):
            issues.append((
                "EVENT_CALLED_ORPHAN",
                f"{event_id} is marked orphan = yes but has {production_triggered[event_id]} production caller(s)",
            ))

    for path in sorted((MOD / "events").glob("cp_debug*_events.txt")):
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for match in TRIGGER_EVENT_RE.finditer(text):
            event_id = match.group(1)
            if event_id in event_texts and not is_hidden_event(event_texts, event_id):
                issues.append((
                    "DEBUG_POPUP_THREAD",
                    f"{rel(path)}:{line_no_for_match(text, match.start())} direct-triggers visible event {event_id}; queue it and fire the popup from the JE debug button instead",
                ))

    for event_id in sorted(event_ids):
        if (
            event_id.startswith("cp_")
            and not is_debug_event_id(event_id)
            and event_id not in production_triggered
            and not event_id.endswith(".0001")
            and not is_orphan_event(event_texts, event_id)
        ):
            debug_note = " (debug-only callers exist)" if event_id in debug_triggered else ""
            warnings.append(("EVENT_UNCALLED", f"{event_id} is defined but no production trigger_event caller was found{debug_note}"))

    common_text = "\n".join(
        uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for path in script_files()
    )
    cp_variable_reads: defaultdict[str, list[str]] = defaultdict(list)
    cp_variable_writes: set[str] = set()
    for path in script_files():
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for match in CP_VARIABLE_READ_RE.finditer(text):
            variable = first_group(match)
            cp_variable_reads[variable].append(f"{rel(path)}:{line_no_for_match(text, match.start())}")
        for match in CP_VARIABLE_WRITE_RE.finditer(text):
            cp_variable_writes.add(first_group(match))

    for match in MARK_EVENT_SEEN_CALL_RE.finditer(common_text):
        cp_variable_writes.add(f"cp_{match.group(1)}_seen_{match.group(2)}")
    for match in REGISTER_PERSON_RE.finditer(common_text):
        cp_variable_writes.add(f"cp_person_{match.group(1)}_alive")
        cp_variable_writes.add(f"cp_person_{match.group(1)}_country")

    for variable in sorted(cp_variable_reads):
        if variable not in cp_variable_writes:
            locations = ", ".join(cp_variable_reads[variable][:5])
            more = f" (+{len(cp_variable_reads[variable]) - 5} more)" if len(cp_variable_reads[variable]) > 5 else ""
            issues.append((
                "CP_VARIABLE_UNSET_READ",
                f"{variable} is read at {locations}{more}, but no script writer was found",
            ))

    seen_ids_by_person: defaultdict[str, set[str]] = defaultdict(set)
    for match in MARK_EVENT_SEEN_CALL_RE.finditer(common_text):
        seen_ids_by_person[match.group(1)].add(match.group(2))
    for person, seen_ids in sorted(seen_ids_by_person.items()):
        visible_history_trigger = named_top_level_block_text(
            MOD / "common" / "scripted_triggers" / "cp_shared_sensors.txt",
            f"cp_{person}_has_visible_history",
        )
        for seen_id in sorted(seen_ids):
            expected = f"cp_{person}_seen_{seen_id}"
            if expected not in visible_history_trigger:
                issues.append((
                    "EVENT_JE_RECOVERY",
                    f"cp_{person}_has_visible_history is missing {expected}; seen events must be recoverable into the active JE roster",
                ))

    shared_firing_path = MOD / "common" / "scripted_effects" / "cp_shared_firing.txt"
    shared_firing = uncommented_text(shared_firing_path.read_text(encoding="utf-8-sig", errors="replace"))
    persons = registered_persons()
    for person in persons:
        memory = MOD / "common" / "scripted_effects" / f"cp_{person}_memory.txt"
        loc = MOD / "localization" / "english" / f"cp_{person}_l_english.yml"
        if not memory.exists():
            issues.append(("PERSON_FILE", f"registered person {person} is missing {rel(memory)}"))
        if not loc.exists():
            issues.append(("PERSON_FILE", f"registered person {person} is missing {rel(loc)}"))
        if f"cp_roll_ambient_{person} =" not in common_text:
            issues.append(("PERSON_AMBIENT", f"registered person {person} has no cp_roll_ambient_{person} definition"))
        if f"cp_roll_ambient_{person} = yes" not in shared_firing:
            issues.append(("PERSON_ROUTER", f"registered person {person} is not called from cp_roll_for_event"))
        alive_init = re.compile(rf"set_variable\s*=\s*\{{\s*name\s*=\s*cp_{re.escape(person)}_alive\s+value\s*=\s*1\s*\}}")
        if not alive_init.search(common_text):
            issues.append(("PERSON_ALIVE", f"registered person {person} has no cp_{person}_alive initialization to 1"))

    on_actions_path = MOD / "common" / "on_actions" / "cp_on_actions.txt"
    law_dispatcher = named_top_level_block_text(on_actions_path, "cp_on_law_enacted")
    for item in effect_body_items(uncommented_text(law_dispatcher)):
        law_calls = LAW_REACTION_CALL_RE.findall(item)
        if not law_calls:
            continue
        call_people = sorted({person for _event_id, person in law_calls})
        if len(call_people) < 2:
            events_list = ", ".join(event_id for event_id, _person in law_calls)
            issues.append((
                "LAW_DIRECT_SINGLE_PERSON",
                f"{rel(on_actions_path)} direct-fires single-person law reaction(s) {events_list}; put single-person law routing in cp_<person>_dispatch_law_enacted and reserve cp_on_law_enacted direct fires for shared contests",
            ))

    shared_infra_paths = [on_actions_path]
    shared_infra_paths.extend(sorted((MOD / "common" / "scripted_effects").glob("cp_shared*.txt")))
    for path in shared_infra_paths:
        if path == shared_firing_path:
            continue
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for match in SHARED_DIRECT_GATEKEEPER_RE.finditer(text):
            issues.append((
                "SHARED_DIRECT_GATEKEEPER",
                f"{rel(path)}:{line_no_for_match(text, match.start())} directly calls {match.group(0).rstrip('= ').strip()}; shared infrastructure should call cp_<person>_dispatch_* and let person-owned files fire non-law events",
            ))

    on_actions_text = uncommented_text(on_actions_path.read_text(encoding="utf-8-sig", errors="replace"))
    for match in DIRECT_PERSON_VARIABLE_MUTATION_RE.finditer(on_actions_text):
        variable = first_group(match)
        issues.append((
            "ON_ACTION_PERSON_MUTATION",
            f"{rel(on_actions_path)}:{line_no_for_match(on_actions_text, match.start())} mutates {variable}; shared on_actions should call cp_<person>_dispatch_* and let person-owned files write person variables",
        ))

    for path in script_files():
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        for line_no, line in enumerate(lines, 1):
            clean = strip_comment(line)
            signed_positive = SIGNED_POSITIVE_NUMBER_RE.search(clean)
            if signed_positive:
                issues.append((
                    "SIGNED_POSITIVE_NUMBER",
                    f"{rel(path)}:{line_no} uses {signed_positive.group(0)!r}; use an unsigned positive number because Victoria 3 logs +N as a bad script value",
                ))
            for match in ALIVE_HAS_RE.finditer(clean):
                variable = match.group(1)
                prefix = clean[: match.start()]
                if "NOT" in prefix:
                    continue
                if not has_nearby_value_check(lines, line_no - 1, variable):
                    issues.append((
                        "ALIVE_GUARD",
                        f"{rel(path)}:{line_no} checks {variable} exists without a nearby var:{variable} value check",
                    ))
            if guid_events is not None:
                for sound_path in SOUND_RE.findall(clean):
                    if sound_path.startswith("event:/") and sound_path not in guid_events:
                        issues.append((
                            "AUDIO_GUID",
                            f"{rel(path)}:{line_no} references unknown audio event {sound_path}",
                        ))
            if law_types is not None:
                for law_type in LAW_TYPE_RE.findall(clean):
                    if law_type not in law_types:
                        issues.append((
                            "LAW_TYPE_UNKNOWN",
                            f"{rel(path)}:{line_no} references unknown law_type:{law_type} for the installed Victoria 3 build",
                        ))
            call = CP_YES_CALL_RE.match(clean)
            if call and call.group(1) not in cp_definitions:
                issues.append((
                    "CP_CALL_MISSING",
                    f"{rel(path)}:{line_no} calls undefined scripted effect/trigger {call.group(1)}",
                ))

    for path in sorted((MOD / "common").glob("**/*.txt")):
        if path == shared_firing_path:
            continue
        text = uncommented_text(path.read_text(encoding="utf-8-sig", errors="replace"))
        for match in TRIGGER_EVENT_RE.finditer(text):
            event_id = match.group(1)
            if is_hidden_event(event_texts, event_id):
                continue
            issues.append((
                "RAW_TRIGGER_EVENT",
                f"{rel(path)}:{line_no_for_match(text, match.start())} directly triggers visible event {event_id}; route visible fires through cp_try_fire_ambient, cp_try_fire_law_reaction, cp_try_fire_world_response, cp_try_fire_milestone, or cp_button_fire",
            ))

    if on_action_hooks is not None:
        for path in sorted((MOD / "common" / "on_actions").glob("*.txt")):
            for name, line_no in top_level_blocks(path):
                if name.startswith("cp_"):
                    continue
                if name not in on_action_hooks:
                    issues.append((
                        "ON_ACTION_UNKNOWN",
                        f"{rel(path)}:{line_no} subscribes to unknown vanilla on_action {name}",
                    ))

    print("Common People static audit")
    print(f"Events: {len(events)}")
    print(f"Registered persons: {len(persons)}")
    print(f"Localization keys: {len(loc_keys)}")
    print(f"Audio GUID validation: {'enabled' if guid_events is not None else 'skipped'}")
    print(f"On-action validation: {'enabled' if on_action_hooks is not None else 'skipped'}")
    print(f"Law type validation: {'enabled' if law_types is not None else 'skipped'}")
    print(f"Metadata game-version validation: {'enabled: ' + game_version if game_version is not None else 'skipped'}")
    print("Thumbnail validation: enabled")
    print("Paradox script BOM validation: enabled")
    print("Localization dynamic-scope validation: enabled")
    print("Scripted call validation: enabled")
    print("CP variable read/write validation: enabled")
    print("Visible event image/audio hook validation: enabled")
    print("Visible event JE activation validation: enabled")
    print("Visible history JE recovery validation: enabled")
    print("Raw trigger_event validation: enabled")
    print("Shared law-dispatch validation: enabled")
    print("Shared non-law gatekeeper validation: enabled")
    print("On-action person-mutation validation: enabled")
    print("Production reachability validation: enabled")
    print(f"Issues: {len(issues)}")
    for code, message in issues:
        print(f"[FAIL] {code}: {message}")
    print(f"Warnings: {len(warnings)}")
    for code, message in warnings:
        print(f"[WARN] {code}: {message}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
