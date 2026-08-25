# Framework installation

The canonical interface is `SKILL.md` + `scripts/agent_toolkit.py`. Any coding agent that can read files and run local shell commands can use it.

## Universal
Clone the repository, then run `./flop-airdrop-skill-advanced/install.sh` on macOS/Linux/WSL or `./flop-airdrop-skill-advanced/install.ps1` in PowerShell. The installer creates a local virtual environment and copies the skill into `~/.agents/skills/flop-airdrop-advanced` together with the audited protocol core it delegates to.

If your agent supports the open skills CLI, from a terminal use:

```bash
npx skills add https://github.com/gowthamaran/Flop
```

Then select/enable `flop-airdrop-advanced` if the client asks which skill to install. Client behavior varies; the universal clone/install path remains the source of truth.

## Codex / Cursor / Windsurf / Antigravity / OpenCode
Open the cloned `Flop` repository as the workspace. Tell the agent: `Read flop-airdrop-skill-advanced/SKILL.md and follow it for this task.` The agent should run the toolkit, not reimplement cryptography.

## Claude Code
Start Claude Code from the repository root and point it to `flop-airdrop-skill-advanced/SKILL.md`. Keep identity creation/passphrase entry in the human terminal prompt.

## Hermes
Start Hermes from the repository root. The repository's `HERMES.md` provides project-wide safety context; this skill adds the autonomous airdrop/contribution workflow. Prompt: `Help me with the $FLOP airdrop. Follow flop-airdrop-skill-advanced/SKILL.md.`

## OpenClaw and MCP-capable hosts
Use the CLI directly, or configure a local stdio MCP process with the skill virtual-environment Python and `scripts/mcp_server.py`. Do not expose the MCP process publicly.

## Important compatibility rule
An agent is compatible if it can (1) read SKILL.md, (2) execute local Python/shell commands, and (3) allow a human to complete secure terminal prompts. No vendor SDK is required.
