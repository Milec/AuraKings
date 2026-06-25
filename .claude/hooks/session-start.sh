#!/bin/bash
set -euo pipefail

# Aura Kings — SessionStart hook.
#
# A CK3 mod has no build/dependency step, so this just runs the offline mod
# validator (scripts/validate_mod.py, Python stdlib only) at the start of every
# session. That surfaces scripting mistakes — unbalanced braces, missing loc
# BOMs, undefined aura_* effect/trigger/value/event/trait references — before
# the mod is ever loaded in the game.
#
# It never fails the session: validation problems are reported, not fatal.

cd "${CLAUDE_PROJECT_DIR:-.}"

if command -v python3 >/dev/null 2>&1; then
    python3 scripts/validate_mod.py || true
else
    echo "session-start: python3 not found; skipping Aura Kings mod validation"
fi
