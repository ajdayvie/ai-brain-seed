# ai-brain-seed — instructions for Claude Code

This repository is a **starter kit** for a personal LLM-maintained knowledge brain. It is not itself a
brain. It holds the templates, the docs, and the install flow that stand one up.

## Routing

- The owner asks for help installing a brain, for example `help me install an AI brain`, "set up the
  brain", or "install the brain". **Read `INSTALL.md` and follow it.** It is the single guided intake.
- The owner asks to be taught first, for example `teach me how the brain works`. **Read
  `docs/background.md` and explain it. Write nothing.** Offer the install when they are ready.
- The owner **already has a brain** and asks to update it, for example `check my brain for updates`, "update
  the brain", or "install the new digest feature". **Read `UPDATES.md` and follow it.** It probes the
  existing vault, works out its version, and applies only the migrations the owner approves. Do not run
  `INSTALL.md` against a vault that already exists.
- The owner asks what changed in a version. Read `CHANGELOG.md` and answer from it.
- The owner asks about one part only, such as scheduling, a surface, or backfill. Read the matching file
  under `docs/` and answer from it.

`INSTALL.md` holds the actual install instructions, and `UPDATES.md` the update ones. Do not restate either
here and do not act from memory of them.

## Rules

- **Do not write anything outside this repository** until `INSTALL.md` says to, and the owner has confirmed
  the vault path.
- **The vault is git-free, forever.** Never run git inside a vault. Never leave a `.git` folder in a vault
  you create.
- **Never fabricate a fact or a source** in a vault you build.
- **Never do account signups, permission grants, or token generation** for the owner. Instruct and verify.
- **An update never costs the owner knowledge.** Never overwrite a file they edited, never touch `wiki/`
  page content, `inbox/`, `raw/`, `outputs/`, or `digests/`, and always show a diff before an edit.
- After a vault exists, its own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol.
