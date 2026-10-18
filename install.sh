#!/usr/bin/env bash
# Install the Muse Code skill package and an exact, project-local Ruflo MCP entry.
# This script never starts Ruflo, never writes API keys, and never weakens Muse
# Code approvals. Muse starts the optional local stdio MCP process on the next
# trusted workspace session.
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$PWD"
SCOPE="user"
VERSION="${MUSE_RUFLO_VERSION:-3.56.10}"
INSTALL_PLUGIN=1

usage() {
  cat <<'USAGE'
Usage: bash install.sh [options]

Installs the Muse ↔ Ruflo skill package and adds a pinned, local Ruflo MCP
entry to a Muse Code project. No provider API key is read or written.

Options:
  --project PATH        Target Muse Code project (default: current directory)
  --scope user|project  Plugin installation scope (default: user)
  --version VERSION     Exact Ruflo npm version (default: 3.56.10)
  --skip-plugin         Add only the project MCP entry
  -h, --help            Show this help

The workspace is trusted and the MCP server is started by Muse Code on the next
session. Inspect .mcp.json before trusting a workspace.
USAGE
}

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

need_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project)
      [[ $# -ge 2 ]] || fail "--project needs a path"
      PROJECT="$2"
      shift 2
      ;;
    --scope)
      [[ $# -ge 2 ]] || fail "--scope needs user or project"
      SCOPE="$2"
      shift 2
      ;;
    --version)
      [[ $# -ge 2 ]] || fail "--version needs an exact Ruflo version"
      VERSION="$2"
      shift 2
      ;;
    --skip-plugin)
      INSTALL_PLUGIN=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Unknown option: $1"
      ;;
  esac
done

[[ "$SCOPE" == "user" || "$SCOPE" == "project" ]] || fail "--scope must be user or project"
[[ -d "$PROJECT" ]] || fail "Project directory does not exist: $PROJECT"
PROJECT="$(CDPATH= cd -- "$PROJECT" && pwd)"

need_command muse
need_command node
need_command npm
need_command npx
need_command python3

NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
[[ "$NODE_MAJOR" =~ ^[0-9]+$ ]] || fail "Could not detect Node.js version"
(( NODE_MAJOR >= 20 )) || fail "Ruflo requires Node.js 20 or newer; found Node.js $(node --version)"

if (( INSTALL_PLUGIN )); then
  # Validation only parses package metadata; it cannot execute plugin code.
  muse plugins validate "$ROOT"
  muse plugins install "$ROOT" --scope "$SCOPE"
fi

python3 "$ROOT/scripts/merge_mcp.py" --project "$PROJECT" --version "$VERSION"
python3 "$ROOT/scripts/merge_mcp.py" --project "$PROJECT" --version "$VERSION" --check

cat <<EOF

Installed safely.

  Plugin:     muse-ruflo-bridge ($SCOPE scope)
  Project:    $PROJECT
  Ruflo:      ruflo@$VERSION (pinned in .mcp.json)
  Model auth: current Muse Code session only; no provider API key was configured

Next:
  1. Inspect $PROJECT/.mcp.json.
  2. Start a NEW Muse Code session in that workspace.
  3. Trust the workspace only after reviewing its files; Muse Code will start
     the optional local Ruflo MCP server and /mcp will show its live status.
  4. Run /muse-ruflo-bridge:ruflo-health in Muse Code.
EOF
