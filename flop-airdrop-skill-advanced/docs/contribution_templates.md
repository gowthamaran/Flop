# Contribution templates

These are quality frameworks, not copy-paste spam. Replace the structure with original, accurate work.

## Educational X thread
1. Hook: one concrete beginner problem.
2. Explain what Technocore is in plain language.
3. Explain `did:key` and why the public identifier is safe to share.
4. Explain local Ed25519 signing without exposing a key.
5. Show one real, verified interaction or public sequence.
6. Explain what is known versus unknown about current testnet/airdrop mechanics.
7. End with a security warning and useful next step.

## Short tutorial
**Goal** — what the reader will accomplish.
**Prerequisites** — Python/Git and local terminal.
**Steps** — minimal reproducible commands.
**Verification** — how to independently confirm the public record.
**Safety** — never share PEM/passphrase.
**Unknowns** — explicitly list protocol behavior that is not documented.

## Translation/localization
Translate meaning rather than marketing hype. Keep code, DID strings, command names, and URLs unchanged. Preserve warnings. Add a short glossary only when it improves comprehension.

## Code contribution
State the bug/problem, why it matters, the smallest change, tests performed, and immutable public revision. Never label a local/unpublished file as a public contribution.

## Quality checklist
- Is it useful without an airdrop incentive?
- Is every factual protocol claim verifiable?
- Is it materially different from the user's recent work?
- Does it avoid reward guarantees and hidden-scoring speculation?
- Is there a real public artifact URL before `contribute` is run?
