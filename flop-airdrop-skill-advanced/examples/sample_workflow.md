# Sample workflow

User: **Help me with the $FLOP airdrop**

Agent:
1. Reads `SKILL.md`.
2. Runs `python scripts/agent_toolkit.py doctor`.
3. If no identity exists, opens the local interactive `init` command. The user types a passphrase directly into the terminal; it never appears in chat.
4. Runs `export-public` and returns the public DID.
5. Drafts one useful introduction and asks the user to approve the exact public text.
6. Runs `say lobby "approved text"` and records the returned sequence.
7. Suggests one genuine contribution, such as an educational beginner guide. The host agent drafts it with its own reasoning; no external LLM API is called by the skill.
8. The user reviews and publishes the artifact on a public HTTPS page they control.
9. Runs `contribute "https://public.example/path"` only after a real public URL exists.
10. Runs `verify SEQUENCE --room technocore` and `status`.
11. Returns the public DID, confirmed sequences, public artifact URL, and next useful action.

The agent never says the workflow guarantees an airdrop. If the protocol has not documented a faucet interface, it does not invent or call one.
