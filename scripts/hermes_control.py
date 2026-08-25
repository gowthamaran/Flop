#!/usr/bin/env python3
"""Safe JSON bridge between Hermes (or any agent) and the local FLOP toolkit.

This module intentionally never accepts a seed/private key/passphrase as an argument.
Secrets remain inside the existing local identity implementation. Public writes are
explicit subcommands so an agent can propose first and execute only after approval.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLKIT = ROOT / "flop-airdrop-skill-advanced" / "scripts" / "agent_toolkit.py"


def emit(ok: bool, **data: object) -> None:
    print(json.dumps({"ok": ok, **data}, ensure_ascii=False))


def run_toolkit(args: list[str]) -> int:
    if not TOOLKIT.exists():
        emit(False, error="advanced toolkit not found", path=str(TOOLKIT))
        return 2
    p = subprocess.run(
        [sys.executable, str(TOOLKIT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if p.returncode:
        emit(False, exit_code=p.returncode, error=(p.stderr or p.stdout).strip())
        return p.returncode
    out = p.stdout.strip()
    try:
        payload = json.loads(out)
        emit(True, result=payload)
    except json.JSONDecodeError:
        emit(True, output=out)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Hermes-safe JSON bridge for FLOP/Technocore")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("status")
    sub.add_parser("did")

    say = sub.add_parser("say")
    say.add_argument("--room", required=True)
    say.add_argument("--message", required=True)

    con = sub.add_parser("contribute")
    con.add_argument("--url", required=True)
    con.add_argument("--room", default="technocore")

    ver = sub.add_parser("verify")
    ver.add_argument("--sequence", required=True, type=int)
    ver.add_argument("--room", default="technocore")

    a = ap.parse_args()
    if a.cmd == "doctor": return run_toolkit(["doctor"])
    if a.cmd == "status": return run_toolkit(["status"])
    if a.cmd == "did": return run_toolkit(["export-public"])
    if a.cmd == "say": return run_toolkit(["say", a.room, a.message])
    if a.cmd == "contribute": return run_toolkit(["contribute", a.url, "--room", a.room])
    if a.cmd == "verify": return run_toolkit(["verify", str(a.sequence), "--room", a.room])
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
