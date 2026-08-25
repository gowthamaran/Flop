#!/usr/bin/env sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PY=${PYTHON:-python3}
VENV="$ROOT/.venv"
command -v "$PY" >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
"$PY" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$ROOT/scripts/requirements.txt"
mkdir -p "$HOME/.agents/skills"
DEST="$HOME/.agents/skills/flop-airdrop-advanced"
rm -rf "$DEST"
cp -R "$ROOT" "$DEST"
printf '\nInstalled local skill at %s\n' "$DEST"
printf 'Run: %s/scripts/agent_toolkit.py doctor\n' "$DEST"
printf 'Keys are NOT created by the installer. Run init interactively when ready.\n'
