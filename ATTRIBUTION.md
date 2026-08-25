# Attribution

This repository is a modified distribution of
[`zunmax/technocore-did-starter`](https://github.com/zunmax/technocore-did-starter),
original commit `3cc03a6e908e8776de9fdd465c53d23d31db2e9f`.

The upstream project is licensed under the MIT License. Its original copyright
notice remains in [LICENSE](LICENSE), as required by that license.

## Additional design reference

The Hermes local-control revision was informed by the public MIT-licensed
[`Nerevarine22/technocore`](https://github.com/Nerevarine22/technocore) project,
particularly its local-only browser UX, safe identity bootstrap concept,
machine-readable agent mode, loopback binding, and receipt verification model.

This repository does not replace Flop's encrypted `identity.pem` architecture
with that project's `.env` seed storage. The integration added here is an
independently written orchestration bridge around Flop's existing signer.

## Changes in this repository

- restructured the README around a faster quick start;
- added Hermes Agent project context and a detailed deployment workflow;
- added a Hermes-safe one-JSON command bridge (`scripts/hermes_control.py`);
- documented a loopback-only Hermes Mission Control architecture;
- added human checkpoints for identity creation and network writes;
- added a cross-platform Python bootstrap script;
- added a machine-readable local `doctor` command;
- added offline cryptographic, identity, validation, and proof tests;
- added Python 3.12 CI for Linux, macOS, and Windows;
- added expanded manual setup and security documentation;
- changed the HTTP user-agent string to identify this distribution.

Hermes Agent is maintained separately by Nous Research. No affiliation or
endorsement by Nous Research, Flop Labs, or any upstream/reference author is
implied.
