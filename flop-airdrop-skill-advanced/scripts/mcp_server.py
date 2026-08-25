#!/usr/bin/env python3
"""Optional local MCP facade. Secrets remain in terminal/local core process."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    raise SystemExit("Install free dependencies first: pip install -r scripts/requirements.txt")

HERE=Path(__file__).resolve().parent
TOOL=HERE/"agent_toolkit.py"
mcp=FastMCP("flop-technocore-local")

def run(*args: str) -> str:
    p=subprocess.run([sys.executable,str(TOOL),*args],cwd=HERE.parent,text=True,capture_output=True,timeout=45)
    if p.returncode: raise RuntimeError((p.stderr or p.stdout).strip() or "tool failed")
    return p.stdout.strip()

@mcp.tool()
def doctor() -> str:
    """Check local readiness without reading private key material."""
    return run("doctor")

@mcp.tool()
def export_public() -> str:
    """Return only the public DID. Encrypted-key passphrase may require local terminal interaction."""
    return run("export-public")

@mcp.tool()
def status() -> str:
    """Return public DID and recent public Technocore activity."""
    return run("status")

@mcp.tool()
def verify(sequence: int, room: str="technocore") -> str:
    """Verify a public sequence in a Technocore room."""
    return run("verify",str(sequence),"--room",room)

@mcp.tool()
def publish(room: str, message: str) -> str:
    """Publish one signed message. Use only after explicit user approval; passphrase stays in local prompt."""
    return run("say",room,message)

@mcp.tool()
def contribute(url: str, room: str="technocore") -> str:
    """Record a user-published public HTTPS contribution URL after explicit approval."""
    return run("contribute",url,"--room",room)

if __name__=="__main__":
    mcp.run()
