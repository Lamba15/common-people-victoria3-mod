#!/usr/bin/env bash
# Enable the workspace Common People mod in the local Victoria 3 runtime config.
#
# This is for smoke testing only. It preserves the existing content_load.json
# as a timestamped backup, creates/repairs the local mod symlink when safe, and
# adds "Common People" to enabledMods without disturbing DLC settings.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
user_dir="${V3_USER_DIR:-$HOME/.local/share/Paradox Interactive/Victoria 3}"
mod_dir="$user_dir/mod"
mod_link="$mod_dir/Common People"
repo_mod="$repo_root/mod"
content_load="$user_dir/content_load.json"

mkdir -p "$mod_dir"

if [[ -L "$mod_link" ]]; then
    current_target="$(readlink -f "$mod_link")"
    if [[ "$current_target" != "$repo_mod" ]]; then
        echo "error: $mod_link points to $current_target, not $repo_mod" >&2
        exit 2
    fi
elif [[ -e "$mod_link" ]]; then
    echo "error: $mod_link exists and is not a symlink; refusing to replace it" >&2
    exit 2
else
    ln -s "$repo_mod" "$mod_link"
    echo "created symlink: $mod_link -> $repo_mod"
fi

if [[ -f "$content_load" ]]; then
    backup="$content_load.cp-backup-$(date +%Y%m%d-%H%M%S)"
    cp "$content_load" "$backup"
    echo "backup: $backup"
fi

CONTENT_LOAD="$content_load" python3 - <<'PY'
from __future__ import annotations

import json
import os
from pathlib import Path

path = Path(os.environ["CONTENT_LOAD"])
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except FileNotFoundError:
    data = {}

enabled = data.get("enabledMods")
if not isinstance(enabled, list):
    enabled = []

def mod_name(entry):
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict):
        if "name" in entry:
            return str(entry["name"])
        if "displayName" in entry:
            return str(entry["displayName"])
        if "id" in entry:
            return str(entry["id"])
        if "path" in entry:
            return Path(str(entry["path"])).name
    return str(entry)

deduped = []
seen = set()
for entry in enabled:
    name = mod_name(entry)
    if name in seen:
        continue
    seen.add(name)
    deduped.append(entry)

enabled = deduped
if "Common People" not in {mod_name(entry) for entry in enabled}:
    enabled.append("Common People")

data["enabledMods"] = enabled
data.setdefault("disabledDLC", [])
data.setdefault("enabledUGC", [])
path.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
print(f"enabledMods: {enabled}")
PY
