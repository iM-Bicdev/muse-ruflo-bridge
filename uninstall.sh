#!/usr/bin/env bash
# Remove only the exact MCP entry installed by this bridge, then remove its
# Muse Code content package. It never touches a different user-managed Ruflo
# configuration.
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$PWD"
VERSION="${MUSE_RUFLO_VERSION:-3.56.10}"
KEEP_PLUGIN=0

usage() {
  cat <<'USAGE'
Usage: bash uninstall.sh [options]

Options:
  --project PATH     Target Muse Code project (default: current directory)
  --version VERSION  Exact Ruflo version used at installation (default: 3.56.10)
  --keep-plugin      Keep the Muse skill/command package installed
  -h, --help         Show this help
USAGE
}

fail() { printf 'error: %s\n' "$*" >&2; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) [[ $# -ge 2 ]] || fail "--project needs a path"; PROJECT="$2"; shift 2 ;;
    --version) [[ $# -ge 2 ]] || fail "--version needs a value"; VERSION="$2"; shift 2 ;;
    --keep-plugin) KEEP_PLUGIN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) fail "Unknown option: $1" ;;
  esac
done

command -v python3 >/dev/null 2>&1 || fail "Missing required command: python3"
[[ -d "$PROJECT" ]] || fail "Project directory does not exist: $PROJECT"
PROJECT="$(CDPATH= cd -- "$PROJECT" && pwd)"

python3 "$ROOT/scripts/merge_mcp.py" --project "$PROJECT" --version "$VERSION" --remove

if (( ! KEEP_PLUGIN )); then
  command -v muse >/dev/null 2>&1 || fail "Muse Code is required to remove the plugin; rerun with --keep-plugin to remove only MCP config"
  muse plugins remove muse-ruflo-bridge
fi

printf 'Removed Muse ↔ Ruflo Bridge configuration from %s\n' "$PROJECT"
