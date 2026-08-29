# ai-brain-seed — instructions for AI assistants

This repository is a **starter kit** for a personal LLM-maintained knowledge brain. It is not itself a
brain. It holds the templates, the docs, and the install flow that stand one up.

## Routing

- The user asks for help installing a brain, for example `help me install an AI brain`, "set up the brain",
  or "install the brain". **Read `INSTALL.md` and follow it.** It is the single guided intake.
- The user asks to be taught first, for example `teach me how the brain works`. **Read `docs/background.md`
  and explain it. Write nothing.** Offer the install when they are ready.
- The user asks about one part only, such as scheduling, a surface, or backfill. Read the matching file
  under `docs/` and answer from it.

`INSTALL.md` holds the actual instructions. Do not restate them here and do not act from memory of them.

## Rules

- **Do not write anything outside this repository** until `INSTALL.md` says to, and the user has confirmed
  the vault path.
- **The vault is git-free, forever.** Never run git inside a vault. Never leave a `.git` folder in a vault
  you create.
- **Never fabricate a fact or a source** in a vault you build.
- **Never do account signups, permission grants, or token generation** for the user. Instruct and verify.
- After a vault exists, its own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol.
- If you have this file but not the repository files, `STANDALONE.md` embeds every template in one paste.
