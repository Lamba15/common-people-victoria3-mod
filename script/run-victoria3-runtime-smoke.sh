#!/usr/bin/env bash
# Launch a controlled Victoria 3 compile/log smoke for Common People, then audit logs.
#
# This is intentionally direct-binary, not launcher-driven:
# - enables the workspace mod through script/enable-common-people-local.sh
# - starts the installed Victoria 3 binary with SteamAppId set
# - waits long enough for the game to compile scripts and write fresh logs
# - runs script/audit-victoria3-logs.py --require-current-build
# - closes the direct-launched process after the audit unless --keep-running is set
#
# With --keep-running, the game is launched through nohup+setsid so the audit
# timeout does not keep ownership of the game process and cannot close it when
# this wrapper exits.
#
# It does not start a campaign, select Egypt, unpause, inspect event windows,
# verify JE state in-game, or prove audio/art behavior in the player UI.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
game_dir="${CP_V3_INSTALL_DIR:-/media/aboelsoud/97889587-0454-426f-b9ae-89456f462ace/SteamLibrary/steamapps/common/Victoria 3}"
user_dir="${V3_USER_DIR:-$HOME/.local/share/Paradox Interactive/Victoria 3}"
binary="$game_dir/binaries/victoria3"
wait_seconds=45
keep_running=0

usage() {
    printf 'usage: %s [--wait-seconds N] [--keep-running]\n' "$(basename "$0")"
    printf 'note: this is a compile/log smoke only; it is not an Egypt gameplay test\n'
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --wait-seconds)
            [[ $# -ge 2 ]] || { usage >&2; exit 2; }
            wait_seconds="$2"
            shift 2
            ;;
        --keep-running)
            keep_running=1
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

if [[ ! "$wait_seconds" =~ ^[0-9]+$ ]] || [[ "$wait_seconds" -lt 10 ]]; then
    echo "error: --wait-seconds must be an integer >= 10" >&2
    exit 2
fi

if [[ ! -x "$binary" ]]; then
    echo "error: Victoria 3 binary not found or not executable: $binary" >&2
    exit 2
fi

if pgrep -f "$binary" >/dev/null; then
    echo "error: Victoria 3 already appears to be running; close it before smoke testing" >&2
    exit 2
fi

"$repo_root/script/enable-common-people-local.sh"

log_dir="$user_dir/logs"
system_log="$log_dir/system.log"
before_mtime=0
if [[ -f "$system_log" ]]; then
    before_mtime="$(stat -c %Y "$system_log")"
fi

echo "launching: $binary"
echo "wait_seconds: $wait_seconds"
if [[ "$keep_running" -eq 1 ]]; then
    live_log="$log_dir/common_people_live_launch.log"
    (
        cd "$game_dir"
        exec nohup setsid env SteamAppId=529340 "$binary" >"$live_log" 2>&1
    ) &
    game_pid="$!"
    echo "keep_running: true"
    echo "detached_launch_log: $live_log"
else
    (
        cd "$game_dir"
        exec env SteamAppId=529340 "$binary"
    ) &
    game_pid="$!"
fi
echo "game_pid: $game_pid"

cleanup() {
    local status=$?
    if [[ "$keep_running" -eq 0 ]] && kill -0 "$game_pid" 2>/dev/null; then
        echo "closing Victoria 3 smoke process: $game_pid"
        kill -TERM "$game_pid" 2>/dev/null || true
        for _ in {1..20}; do
            kill -0 "$game_pid" 2>/dev/null || return "$status"
            sleep 0.5
        done
        kill -KILL "$game_pid" 2>/dev/null || true
    fi
    return "$status"
}
trap cleanup EXIT

deadline=$((SECONDS + wait_seconds))
while [[ "$SECONDS" -lt "$deadline" ]]; do
    if [[ -f "$system_log" ]]; then
        current_mtime="$(stat -c %Y "$system_log")"
        if [[ "$current_mtime" -gt "$before_mtime" ]]; then
            break
        fi
    fi
    if ! kill -0 "$game_pid" 2>/dev/null; then
        echo "error: Victoria 3 exited before writing fresh system.log" >&2
        exit 1
    fi
    sleep 1
done

remaining=$((deadline - SECONDS))
if [[ "$remaining" -gt 0 ]]; then
    sleep "$remaining"
fi

"$repo_root/script/audit-victoria3-logs.py" --require-current-build

if [[ "$keep_running" -eq 1 ]]; then
    if kill -0 "$game_pid" 2>/dev/null; then
        echo "Victoria 3 left running by request: $game_pid"
    else
        echo "error: Victoria 3 was not running after the keep-running audit window" >&2
        exit 1
    fi
fi
