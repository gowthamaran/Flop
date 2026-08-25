#!/usr/bin/env sh
set -eu
SKILL=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH= cd -- "$SKILL/.." && pwd)
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
"$PY" -m venv "$SKILL/.venv"
"$SKILL/.venv/bin/python" -m pip install --upgrade pip
"$SKILL/.venv/bin/python" -m pip install -r "$SKILL/scripts/requirements.txt"
BASE="$HOME/.agents/skills"
DEST="$BASE/flop-airdrop-advanced"
mkdir -p "$BASE"
rm -rf "$DEST"
cp -R "$SKILL" "$DEST"
# The advanced toolkit deliberately reuses the repository's audited protocol core.
cp "$REPO/technocore_agent.py" "$BASE/technocore_agent.py"
printf '\nInstalled at %s\n' "$DEST"
printf 'Run: %s/.venv/bin/python %s/scripts/agent_toolkit.py doctor\n' "$DEST" "$DEST"
printf 'No key was created. Run init interactively when ready.\n'
