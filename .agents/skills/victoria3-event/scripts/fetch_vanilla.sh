#!/usr/bin/env bash
# fetch_vanilla.sh <game/relative/path>
#
# Fetch a vanilla Victoria 3 file from the GitHub mirror of extracted game
# files. The mirror at settintotrieste/V3-Vanilla-Extract is the most
# reliable source of V3 script truth -- the official wiki requires
# JavaScript and often returns empty content to agents/curl.
#
# Usage (from repo root):
#   .claude/skills/victoria3-event/scripts/fetch_vanilla.sh common/character_templates/country_egy.txt
#   .claude/skills/victoria3-event/scripts/fetch_vanilla.sh events/ig_leaders.txt > /tmp/ig_leaders.txt
#
# Prints the file to stdout. Exit 0 on success, non-zero if HTTP != 200.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    cat >&2 <<EOF
usage: $0 <game/relative/path>

examples:
  $0 common/character_templates/country_egy.txt
  $0 common/character_traits/00_traits.txt
  $0 common/on_actions/00_on_actions.txt
  $0 events/ig_leaders.txt
  $0 events/character_events.txt

The path is relative to the game/ directory in the vanilla mirror.
EOF
    exit 2
fi

path="$1"
url="https://raw.githubusercontent.com/settintotrieste/V3-Vanilla-Extract/main/game/$path"

# Use curl with fail-on-error so non-200 responses return non-zero
if ! curl -fsSL "$url"; then
    echo "" >&2
    echo "error: could not fetch $url" >&2
    echo "hint: verify the path exists at https://github.com/settintotrieste/V3-Vanilla-Extract/tree/main/game" >&2
    exit 1
fi
