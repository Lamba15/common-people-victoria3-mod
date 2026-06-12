#!/usr/bin/env bash
# convert-images-to-dds.sh
#
# Convert event PNGs from the generated source library into DDS textures
# inside the mod. Walks image/generated/ for files named *.dds.png and
# produces siblings at mod/gfx/event_pictures/<name>.dds.
#
# Idempotent: skips any DDS that is newer than its source PNG.
# Naming convention: only *.dds.png are converted -- portraits (layla.png)
# and archives (_1536.png) are ignored.
#
# Requires nvcompress (preferred) or ImageMagick's `magick`.
# Install:
#   sudo apt install libnvtt-bin     # gives nvcompress (recommended)
#   sudo apt install imagemagick     # fallback
#
# Usage (from repo root):
#   ./script/convert-images-to-dds.sh
#
# Environment overrides:
#   CP_IMAGES_SRC   source PNG root     (default: image/generated)
#   CP_IMAGES_DST   destination root    (default: mod/gfx/event_pictures)
#   CP_IMAGES_CONVERT_ALL=1             convert every source PNG, including retired art

set -euo pipefail

src_root="${CP_IMAGES_SRC:-image/generated}"
dst_root="${CP_IMAGES_DST:-mod/gfx/event_pictures}"
convert_all="${CP_IMAGES_CONVERT_ALL:-0}"

if [[ ! -d "$src_root" ]]; then
    echo "error: source directory $src_root does not exist" >&2
    echo "hint: set CP_IMAGES_SRC or populate the default location" >&2
    exit 2
fi

mkdir -p "$dst_root"

# Pick a converter. nvcompress is purpose-built for DDS and faster;
# magick works but emits DXT5 via a plugin that isn't always present.
if command -v nvcompress >/dev/null 2>&1; then
    converter=nvcompress
elif command -v magick >/dev/null 2>&1; then
    converter=magick
else
    cat >&2 <<EOF
error: no DDS converter found

Install one of:
  sudo apt install libnvtt-bin   # recommended -- provides nvcompress
  sudo apt install imagemagick   # fallback

EOF
    exit 1
fi

echo "converter: $converter"
echo "src:       $src_root"
echo "dst:       $dst_root"
echo ""

allowed_targets="$(mktemp)"
trap 'rm -f "$allowed_targets"' EXIT
if [[ "$convert_all" != "1" ]]; then
    if command -v rg >/dev/null 2>&1; then
        rg --no-filename -o 'gfx/event_pictures/[^"]+\.dds' mod/events 2>/dev/null \
            | sed 's#gfx/event_pictures/##' >>"$allowed_targets" || true
        rg --no-filename -o 'cp_[A-Za-z0-9_]+_v[0-9]+\.dds' documentation/characters/*/prompts/replacement-batch-v*.md 2>/dev/null \
            >>"$allowed_targets" || true
    else
        grep -RhoE 'gfx/event_pictures/[^"]+\.dds' mod/events 2>/dev/null \
            | sed 's#gfx/event_pictures/##' >>"$allowed_targets" || true
        grep -RhoE 'cp_[A-Za-z0-9_]+_v[0-9]+\.dds' documentation/characters/*/prompts/replacement-batch-v*.md 2>/dev/null \
            >>"$allowed_targets" || true
    fi
    sort -u "$allowed_targets" -o "$allowed_targets"
fi

converted=0
skipped=0
failed=0

while IFS= read -r -d '' png; do
    base=$(basename "$png" .dds.png)
    target_base="$base"

    if [[ "$base" == cp_conversation_* ]]; then
        printf '  FAIL: %s uses retired cp_conversation_* source naming; rename it to cp_layla_conversation_*_vNN.dds.png\n' "$base.dds.png" >&2
        failed=$((failed + 1))
        continue
    fi

    dst="$dst_root/$target_base.dds"

    if [[ "$convert_all" != "1" ]] && ! grep -Fxq "$target_base.dds" "$allowed_targets"; then
        printf '  skip: %s (not active or planned)\n' "$target_base.dds"
        skipped=$((skipped + 1))
        continue
    fi

    # Skip if destination is fresh
    if [[ -f "$dst" && "$dst" -nt "$png" ]]; then
        printf '  skip: %s (dds newer than png)\n' "$target_base.dds"
        skipped=$((skipped + 1))
        continue
    fi

    case "$converter" in
        nvcompress)
            # -bc3 = DXT5-compatible, with alpha
            # -nomips = V3 event pictures don't need mipmaps
            # -silent = suppress progress chatter
            if nvcompress -bc3 -nomips -silent "$png" "$dst" >/dev/null 2>&1; then
                printf '  ok:   %s\n' "$target_base.dds"
                converted=$((converted + 1))
            else
                printf '  FAIL: %s\n' "$target_base.dds" >&2
                failed=$((failed + 1))
            fi
            ;;
        magick)
            if magick "$png" \
                -define dds:compression=dxt5 \
                -define dds:mipmaps=0 \
                "$dst" 2>/dev/null; then
                printf '  ok:   %s\n' "$target_base.dds"
                converted=$((converted + 1))
            else
                printf '  FAIL: %s\n' "$target_base.dds" >&2
                failed=$((failed + 1))
            fi
            ;;
    esac
done < <(find "$src_root" -name '*.dds.png' -type f -print0)

echo ""
echo "converted: $converted  skipped: $skipped  failed: $failed"
[[ $failed -eq 0 ]]
