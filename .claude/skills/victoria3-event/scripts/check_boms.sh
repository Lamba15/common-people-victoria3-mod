#!/usr/bin/env bash
# check_boms.sh
#
# Verify every .yml file under mod/localization/ starts with the UTF-8 BOM
# (EF BB BF). Files without the BOM cause V3 to display localization keys
# instead of the localized strings in-game, often silently.
#
# Usage (from repo root):
#   .claude/skills/victoria3-event/scripts/check_boms.sh
#
# Exits 0 if all files are OK; exits 1 and prints a list if any are missing
# the BOM. Intended for pre-commit or CI.

set -uo pipefail

scan_dir="mod/localization"
missing=()
checked=0

if [[ ! -d "$scan_dir" ]]; then
    echo "error: $scan_dir not found (run from repo root)" >&2
    exit 2
fi

while IFS= read -r -d '' file; do
    checked=$((checked + 1))
    # Read first 3 bytes and hex-encode them
    first=$(head -c 3 "$file" | xxd -p)
    if [[ "$first" != "efbbbf" ]]; then
        missing+=("$file (got: ${first:-empty})")
    fi
done < <(find "$scan_dir" -name '*.yml' -type f -print0)

if [[ ${#missing[@]} -eq 0 ]]; then
    echo "ok: all $checked localization file(s) have BOM"
    exit 0
fi

echo "MISSING BOM (${#missing[@]}/$checked files):"
printf '  %s\n' "${missing[@]}"
echo ""
echo "To fix a file, prepend the BOM:"
echo "  tmpfile=\$(mktemp) && printf '\\xef\\xbb\\xbf' > \"\$tmpfile\" && cat <file> >> \"\$tmpfile\" && mv \"\$tmpfile\" <file>"
exit 1
