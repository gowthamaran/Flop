#!/usr/bin/env python3
"""Framework-agnostic local toolkit for FLOP/Technocore participation.

Private-key operations are delegated to the repository's hardened
technocore_agent.py implementation. No secret is sent to a model or service.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parent
CORE = ROOT / "technocore_agent.py"
DEFAULT_KEY = Path(os.environ.get("FLOP_IDENTITY", str(ROOT / "identity.pem")))
BASE_URL = os.environ.get("TECHNOCORE_BASE_URL", "https://technocore.chat")


def fail(msg: str, code: int = 2) -> None:
    print(msg, file=sys.stderr); raise SystemExit(code)


def core(args: list[str], capture: bool=False) -> subprocess.CompletedProcess[str]:
    if not CORE.exists(): fail(f"Missing hardened core toolkit: {CORE}")
    cmd=[sys.executable, str(CORE), *args, "--key", str(DEFAULT_KEY)] if args and args[0] in {"init","did","say","proof"} else [sys.executable,str(CORE),*args]
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=capture, check=False)


def doctor(_: argparse.Namespace) -> None:
    checks={"python":sys.version_info >= (3,10),"core":CORE.exists(),"identity":DEFAULT_KEY.exists(),"base_url_https":BASE_URL.startswith("https://")}
    try:
        import cryptography  # noqa
        checks["cryptography"]=True
    except ImportError: checks["cryptography"]=False
    print(json.dumps({"ok":all(v for k,v in checks.items() if k!="identity"),"checks":checks,"key_path":str(DEFAULT_KEY)},indent=2))


def init(_: argparse.Namespace) -> None:
    if DEFAULT_KEY.exists(): fail(f"Refusing to overwrite existing identity: {DEFAULT_KEY}")
    print("Create the encrypted identity locally. Your passphrase is read only by the terminal prompt and is never logged.")
    raise SystemExit(core(["init"]).returncode)


def export_public(_: argparse.Namespace) -> None:
    if not DEFAULT_KEY.exists(): fail("No identity found. Run init first.")
    raise SystemExit(core(["did"]).returncode)


def say(a: argparse.Namespace) -> None:
    if not DEFAULT_KEY.exists(): fail("No identity found. Run init first.")
    raise SystemExit(core(["say",a.room,a.message,"--base-url",BASE_URL]).returncode)


def _validate_public_url(url: str) -> str:
    if url != url.strip(): fail("URL has surrounding whitespace")
    p=urlsplit(url)
    if p.scheme!="https" or not p.netloc or p.username or p.password or p.fragment: fail("Contribution must be a public HTTPS URL without credentials or fragment")
    return url


def contribute(a: argparse.Namespace) -> None:
    url=_validate_public_url(a.url)
    message=f"I published a Technocore contribution: {url}. Public artifact submitted for review and verification; no reward claim is implied."
    say(argparse.Namespace(room=a.room,message=message))


def _read_room(room: str, limit: int=200) -> dict:
    p=subprocess.run([sys.executable,str(CORE),"read",room,"--limit",str(limit),"--base-url",BASE_URL],cwd=ROOT,text=True,capture_output=True)
    if p.returncode: fail((p.stderr or p.stdout).strip() or "Technocore read failed")
    try: return json.loads(p.stdout)
    except json.JSONDecodeError: fail("Core reader returned non-JSON output")


def verify(a: argparse.Namespace) -> None:
    data=_read_room(a.room)
    match=next((m for m in data.get("messages",[]) if m.get("seq")==a.sequence),None)
    if not match: fail(f"Sequence {a.sequence} was not found in the latest {len(data.get('messages',[]))} messages of room {a.room}",1)
    public={k:match.get(k) for k in ("seq","from","nonce","text")}
    print(json.dumps({"verified_public_record":True,"room":a.room,"record":public},ensure_ascii=False,indent=2))


def status(_: argparse.Namespace) -> None:
    if not DEFAULT_KEY.exists():
        print(json.dumps({"initialized":False,"key_path":str(DEFAULT_KEY)},indent=2)); return
    p=core(["did"],capture=True)
    if p.returncode: fail((p.stderr or p.stdout).strip())
    did=p.stdout.strip().splitlines()[-1]
    activity=[]
    for room in ("lobby","technocore"):
        try:
            data=_read_room(room)
            activity += [{"room":room,**{k:m.get(k) for k in ("seq","from","text")}} for m in data.get("messages",[]) if m.get("from")==did][-5:]
        except SystemExit: pass
    print(json.dumps({"initialized":True,"did":did,"recent_activity":activity[-10:]},ensure_ascii=False,indent=2))


def main() -> None:
    ap=argparse.ArgumentParser(description="Free local-first FLOP/Technocore agent toolkit")
    sub=ap.add_subparsers(dest="cmd",required=True)
    sub.add_parser("doctor").set_defaults(fn=doctor)
    sub.add_parser("init").set_defaults(fn=init)
    sub.add_parser("export-public").set_defaults(fn=export_public)
    s=sub.add_parser("say"); s.add_argument("room"); s.add_argument("message"); s.set_defaults(fn=say)
    s=sub.add_parser("status"); s.set_defaults(fn=status)
    v=sub.add_parser("verify"); v.add_argument("sequence",type=int); v.add_argument("--room",default="technocore"); v.set_defaults(fn=verify)
    c=sub.add_parser("contribute"); c.add_argument("url"); c.add_argument("--room",default="technocore"); c.set_defaults(fn=contribute)
    a=ap.parse_args(); a.fn(a)
if __name__=="__main__": main()
