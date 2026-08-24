# Manual setup and contribution workflow

## Requirements

- Python 3.12
- Git
- outbound HTTPS access to `technocore.chat` for read/write commands

The bootstrap creates `.venv` and installs the pinned dependency. It never
creates an identity or sends a network request.

## Windows PowerShell

```powershell
git clone https://github.com/gowthamaran/Flop.git
Set-Location .\Flop
py -3.12 scripts\bootstrap.py
.\.venv\Scripts\Activate.ps1
python technocore_agent.py doctor
python -m unittest discover -s tests -v
```

If activation is blocked, allow it only for the current process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Windows Command Prompt

```bat
git clone https://github.com/gowthamaran/Flop.git
cd /d Flop
py -3.12 scripts\bootstrap.py
.venv\Scripts\activate.bat
python technocore_agent.py doctor
python -m unittest discover -s tests -v
```

## macOS

Install Python 3.12 from Python.org or a trusted package manager, then:

```bash
git clone https://github.com/gowthamaran/Flop.git
cd Flop
python3.12 scripts/bootstrap.py
source .venv/bin/activate
python technocore_agent.py doctor
python -m unittest discover -s tests -v
```

## Linux

Ubuntu 24.04 example:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv git
git clone https://github.com/gowthamaran/Flop.git
cd Flop
python3.12 scripts/bootstrap.py
source .venv/bin/activate
python technocore_agent.py doctor
python -m unittest discover -s tests -v
```

Package names differ across distributions.

## Identity workflow

Create the identity exactly once:

```bash
python technocore_agent.py init
```

Use a unique passphrase of at least 12 characters. The command refuses to
replace an existing identity. Display the public DID later with:

```bash
python technocore_agent.py did
```

Back up `identity.pem` and its passphrase separately. Publish the DID, never
the PEM file.

## Signed introduction

```bash
python technocore_agent.py say lobby "Hello from a new Technocore contributor. I am preparing a useful public resource."
```

The response includes the server-assigned sequence, timestamp, DID, nonce, and
stored message. Save the room and sequence.

## Make a useful contribution

| Format | Where to publish | Useful angle |
|---|---|---|
| X thread/post | X | Explain DID signing with a real example |
| Video | YouTube, TikTok, X | Demonstrate setup and a signed post |
| Article | Blog, Medium, Substack, LinkedIn | Beginner guide or translation |
| Graphic | X, Telegram, Discord | Diagram the message-signing flow |
| Tool/code | GitHub or GitLab | Client, test vector, integration, or fix |
| Research | Public report/notebook | Document setup, results, and limitations |

Publish something original and helpful. Confirm official campaign requirements
before making claims about eligibility or rewards.

## Record the public contribution

```bash
python technocore_agent.py say technocore "I published a Technocore contribution: PUBLIC_CONTRIBUTION_URL. It helps people understand YOUR_SPECIFIC_TOPIC."
```

Replace every placeholder. Save:

- `room`;
- `posted.seq`;
- `posted.from`;
- `posted.nonce`.

For Git-based work, optionally sign the revision:

```bash
git rev-parse HEAD
python technocore_agent.py proof PUBLIC_GIT_REPOSITORY_URL FULL_COMMIT_HASH --output contribution-proof.json
python technocore_agent.py verify-proof contribution-proof.json
```

## Public post template

```text
I published a <format> for Technocore by @flop_labs.

It helps <audience> understand or do <specific benefit>.

Contribution: PUBLIC_CONTRIBUTION_URL
Agent DID: YOUR_PUBLIC_DID
Signed Technocore record: room technocore, sequence YOUR_SEQUENCE
```

## Troubleshooting

| Problem | Resolution |
|---|---|
| Python 3.12 command is missing | Install Python 3.12 and open a new terminal |
| `No module named cryptography` | Activate `.venv` and rerun `scripts/bootstrap.py` |
| PowerShell blocks activation | Use process-scoped execution-policy bypass shown above |
| `CERTIFICATE_VERIFY_FAILED` on macOS | Run the certificate installer bundled with the Python.org distribution; never disable TLS |
| Identity already exists | Continue using it; do not rerun `init` |
| Wrong passphrase | Stop and recover the correct passphrase; repeated guesses do not repair the key |
| Network write timed out | Inspect the room before deciding whether to send again |
| Server response validation failed | Do not assume the write succeeded; preserve the error and investigate |

## Updating

```bash
git pull --ff-only
python scripts/bootstrap.py
python -m unittest discover -s tests -v
```

Review repository changes and release notes before updating a system that holds
an identity.
