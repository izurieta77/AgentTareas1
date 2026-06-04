#!/usr/bin/env bash
# SessionStart hook: ensure the `graphify` CLI is available in this (ephemeral)
# environment. The skill files live in .claude/skills/graphify, but the actual
# executable is installed via `uv` and does not persist across containers.
set -euo pipefail

# Already installed? Nothing to do.
if command -v graphify >/dev/null 2>&1; then
  exit 0
fi

# Need uv to install the tool.
if ! command -v uv >/dev/null 2>&1; then
  echo "graphify hook: 'uv' not found; skipping graphifyy install" >&2
  exit 0
fi

echo "graphify hook: installing graphifyy CLI..." >&2
uv tool install graphifyy >/dev/null 2>&1 || {
  echo "graphify hook: graphifyy install failed" >&2
  exit 0
}
echo "graphify hook: graphifyy installed" >&2
exit 0
