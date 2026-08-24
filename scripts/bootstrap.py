#!/usr/bin/env python3
"""Create the project virtual environment and install pinned dependencies."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path


MINIMUM_PYTHON = (3, 12)
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def environment_python(environment: Path) -> Path:
    if os.name == "nt":
        return environment / "Scripts" / "python.exe"
    return environment / "bin" / "python"


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=REPOSITORY_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create .venv and install the FLOP Technocore dependencies."
    )
    parser.add_argument(
        "--venv",
        type=Path,
        default=REPOSITORY_ROOT / ".venv",
        help="virtual-environment directory (default: repository .venv)",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="create or validate the environment without installing packages",
    )
    args = parser.parse_args()

    if sys.version_info < MINIMUM_PYTHON:
        found = ".".join(str(part) for part in sys.version_info[:3])
        parser.error(f"Python 3.12 or newer is required; found {found}")

    environment = args.venv.expanduser().resolve()
    marker = environment / "pyvenv.cfg"
    if environment.exists() and not marker.is_file():
        parser.error(f"refusing to reuse non-virtual-environment path: {environment}")

    if not marker.exists():
        print(f"Creating virtual environment: {environment}", flush=True)
        venv.EnvBuilder(with_pip=True).create(environment)
    else:
        print(f"Using existing virtual environment: {environment}", flush=True)

    python = environment_python(environment)
    if not python.is_file():
        parser.error(f"virtual-environment Python is missing: {python}")

    if not args.skip_install:
        run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
        run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "-r",
                str(REPOSITORY_ROOT / "requirements.txt"),
            ]
        )

        run([str(python), str(REPOSITORY_ROOT / "technocore_agent.py"), "doctor"])
    else:
        print("Dependency installation and doctor check skipped.", flush=True)
    print("Bootstrap complete.")
    print(f"Next: {python} -m unittest discover -s tests -v")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
