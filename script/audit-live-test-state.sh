#!/usr/bin/env bash
# Inspect a manual Victoria 3 live test without launching or closing the game.
#
# This is the safe companion for user-driven playtests:
# - reports whether Victoria 3 is currently running
# - audits the current logs against the installed game build
# - identifies the latest save
# - optionally requires a passing Egypt/Common People save proof
# - optionally runs the full release gate against that tested save

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
game_dir="${CP_V3_INSTALL_DIR:-/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3}"
user_dir="${V3_USER_DIR:-$HOME/.local/share/Paradox Interactive/Victoria 3}"
binary="$game_dir/binaries/victoria3"
save_dir="$user_dir/save games"
save_path=""
require_egypt_save=0
allow_silent_first_contact=0
release_gate=0
failures=0

usage() {
    printf 'usage: %s [--save PATH] [--require-egypt-save] [--release-gate] [--allow-silent-first-contact]\n' "$(basename "$0")"
    printf 'note: this script never launches or closes Victoria 3\n'
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --save)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            save_path="$2"
            shift 2
            ;;
        --require-egypt-save)
            require_egypt_save=1
            shift
            ;;
        --release-gate)
            require_egypt_save=1
            release_gate=1
            shift
            ;;
        --allow-silent-first-contact)
            allow_silent_first_contact=1
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            usage >&2
            exit 2
            ;;
    esac
done

echo "Victoria 3 live-test state"
echo "user_dir: $user_dir"
echo "game_binary: $binary"

if pgrep -af "$binary" >/tmp/cp_victoria3_pids.$$; then
    echo "running: yes"
    sed 's/^/  /' /tmp/cp_victoria3_pids.$$
else
    echo "running: no"
fi
rm -f /tmp/cp_victoria3_pids.$$

if ! "$repo_root/script/audit-victoria3-logs.py" --require-current-build; then
    failures=1
fi

if [[ -z "$save_path" ]]; then
    save_path="$(
        find "$save_dir" -maxdepth 1 -type f -name '*.v3' -printf '%T@ %p\n' 2>/dev/null \
            | sort -nr \
            | awk 'NR == 1 { $1 = ""; sub(/^ /, ""); print }'
    )"
fi

if [[ -z "$save_path" ]]; then
    echo "latest_save: none"
    if [[ "$require_egypt_save" -eq 1 ]]; then
        echo "error: --require-egypt-save was set, but no save exists" >&2
        failures=1
    fi
    exit "$failures"
fi

echo "latest_save: $save_path"
if [[ -e "$save_path" ]]; then
    echo "latest_save_mtime: $(date -r "$save_path" '+%Y-%m-%d %H:%M:%S %z')"
fi

egypt_args=(--save "$save_path")
if [[ "$allow_silent_first_contact" -eq 1 ]]; then
    egypt_args+=(--allow-silent-first-contact)
fi

if [[ "$require_egypt_save" -eq 1 ]]; then
    if ! "$repo_root/script/audit-egypt-gameplay-save.py" "${egypt_args[@]}"; then
        failures=1
    fi
    if [[ "$release_gate" -eq 1 ]]; then
        release_args=(--mode release --egypt-save "$save_path")
        if [[ "$allow_silent_first_contact" -eq 1 ]]; then
            release_args+=(--allow-silent-first-contact)
        fi
        if ! "$repo_root/script/audit-release-readiness.py" "${release_args[@]}"; then
            failures=1
        fi
    else
        printf 'release_command: %q --mode release --egypt-save %q' "$repo_root/script/audit-release-readiness.py" "$save_path"
        if [[ "$allow_silent_first_contact" -eq 1 ]]; then
            printf ' --allow-silent-first-contact'
        fi
        printf '\n'
    fi
else
    if ! "$repo_root/script/audit-egypt-gameplay-save.py" "${egypt_args[@]}"; then
        echo "note: Egypt gameplay save proof is not passing yet; this is non-blocking without --require-egypt-save"
        echo "note: rerun with --require-egypt-save after a real Egypt first-contact save"
    fi
fi

exit "$failures"
