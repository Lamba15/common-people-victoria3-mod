#!/usr/bin/env bash
# new_loc.sh <relative_path>
#
# Create a new Victoria 3 localization .yml with the required UTF-8 BOM
# and `l_english:` header. V3 displays the raw key instead of text if the
# BOM is missing, so always create files with this script rather than by
# hand.
#
# Usage (from repo root):
#   .claude/skills/victoria3-event/scripts/new_loc.sh mod/localization/english/cp_new_l_english.yml
#
# Will refuse to overwrite an existing file.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <path-to-new-yml>" >&2
    exit 2
fi

target="$1"

if [[ -e "$target" ]]; then
    echo "error: $target already exists; refusing to overwrite" >&2
    exit 1
fi

mkdir -p "$(dirname "$target")"

# UTF-8 BOM (EF BB BF) followed by the l_english header.
# V3 requires the BOM; the leading space on entries is vanilla convention.
{
    printf '\xef\xbb\xbf'
    printf 'l_english:\n'
    printf ' # add entries below. format: key:0 "value"\n'
} > "$target"

# Verify
first_bytes=$(xxd "$target" | head -1 | awk '{print $2$3}' | cut -c1-6)
if [[ "$first_bytes" != "efbbbf" ]]; then
    echo "error: BOM missing from $target (got: $first_bytes)" >&2
    exit 1
fi

echo "created $target (UTF-8 with BOM, l_english header)"
