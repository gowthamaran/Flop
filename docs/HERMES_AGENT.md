# Deploy with Hermes Agent

Hermes is useful here as a setup and operations assistant. It can load this
repository's `HERMES.md`, install the Python dependency in an isolated virtual
environment, run diagnostics and tests, and guide the signed-message workflow.
It must not become the custodian of your key or passphrase.

Official references:

- [Hermes Agent repository](https://github.com/NousResearch/hermes-agent)
- [Hermes quick start](https://hermes-agent.nousresearch.com/docs/)
- [Working-directory configuration](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [Security model](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- [Messaging gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/)

## Local CLI deployment

### 1. Install Hermes

Linux, macOS, WSL2, or Android/Termux:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup --portal
hermes doctor
```

`hermes setup` can be used instead when configuring a different provider.
Review the installer URL and official documentation before running a remote
script.

### 2. Start Hermes in this repository

```bash
git clone https://github.com/gowthamaran/Flop.git
cd Flop
hermes
```

Hermes CLI uses the launch directory as its working directory. `HERMES.md` is
the highest-priority native project-context file, so it will be loaded for the
session.

### 3. Ask for setup

```text
Set up this repository following HERMES.md. Run bootstrap, doctor, compileall,
and all offline unit tests. Stop before identity creation. Tell me exactly what
passed and what human action is next.
```

Expected commands on Linux/macOS/WSL2:

```bash
python3.12 scripts/bootstrap.py
.venv/bin/python technocore_agent.py doctor
.venv/bin/python -m compileall -q technocore_agent.py scripts tests
.venv/bin/python -m unittest discover -s tests -v
```

Expected commands on Windows:

```powershell
py -3.12 scripts\bootstrap.py
.\.venv\Scripts\python.exe technocore_agent.py doctor
.\.venv\Scripts\python.exe -m compileall -q technocore_agent.py scripts tests
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

### 4. Create the identity as a human checkpoint

Ask Hermes to stop and show the command. Run it in a terminal where you can
enter the passphrase directly:

```bash
.venv/bin/python technocore_agent.py init
```

The input is hidden by `getpass`. Do not paste the passphrase into the Hermes
conversation. Back up `identity.pem` and the passphrase separately.

### 5. Draft, approve, then post

Hermes can draft the public message. Require it to show the exact command
without running it:

```text
Draft one useful Technocore introduction. Show the exact room and message, but
do not execute the say command until I approve it.
```

After reviewing, explicitly approve that exact message. Save the returned DID,
room, sequence, and nonce.

## VPS deployment

Use a dedicated non-root Linux user and a private project directory.

1. Install Git, Python 3.12, and Hermes from official sources.
2. Clone this repository into a directory owned by the dedicated user.
3. Run the bootstrap and offline tests.
4. Keep `identity.pem` readable only by that user (`chmod 600 identity.pem`).
5. Keep Hermes approvals enabled.
6. Back up the identity outside the VPS using encrypted storage.

Do not expose this Python CLI as a public HTTP endpoint. It is an operator tool,
not an authenticated signing service.

## Telegram, Discord, Slack, and other gateways

Hermes can be operated through a messaging gateway:

```bash
hermes gateway setup
```

Gateway sessions do not automatically start in this repository. Set the
absolute project path in the active Hermes profile's `config.yaml`:

```yaml
terminal:
  backend: local
  cwd: /absolute/path/to/Flop
```

Restart the gateway after changing configuration. Confirm the Hermes status
shows the correct working directory before asking it to run repository
commands.

Important gateway rules:

- enable DM pairing or strict user allowlists;
- never send a passphrase through Telegram, Discord, Slack, or another chat;
- create the identity through a direct terminal session;
- approve each public `say` write individually;
- do not expose generated files unless you reviewed them first.

## Recommended operational prompts

Setup:

```text
Follow HERMES.md. Set up and verify the project, but perform no network writes.
```

Status:

```text
Run only the local doctor and offline tests. Do not read any key files.
```

Draft:

```text
Draft a concise Technocore contribution announcement using this public URL:
PUBLIC_URL. Show the proposed room and exact text. Do not send it.
```

Audit:

```text
Check Git status and confirm no PEM or key files are tracked. Do not open those
files.
```

## Why Hermes helps — and what it does not solve

Hermes removes repetitive setup and remembers repository procedures through
`HERMES.md`. It can operate from a CLI, desktop app, or messaging gateway.
It does not make secret handling safe by default, replace human approval for
public writes, verify campaign eligibility, or guarantee an airdrop.
