# CLAUDE.md — brain (Dropbox, git-free)

This folder is the owner's **LLM-maintained knowledge brain**, stored in Dropbox. Your job is to build and
maintain it, not only to answer from it.

**Before you do anything here, read `SCHEMA.md` (the full protocol) and `wiki/_conventions.md` (the page
rules).** They are binding, they may have changed, and this file deliberately does not copy them.

## Core rules

- **Capture is frictionless.** Anything the owner wants to save goes to `inbox/` as one timestamped note. No
  filing decisions at capture time. Use the `capture-to-inbox` skill.
- **Process is separate.** `inbox/` -> `wiki/` happens on `/process` or on the scheduled nightly run, using
  the `process-inbox` skill. Never process during a capture.
- **You own `wiki/`.** Concept-per-page, interlinked, with the frontmatter in `wiki/_conventions.md`.
- **Sources are immutable.** Never fabricate a fact. Every wiki claim traces to a note in `raw/`, or to the
  inbox note being processed. Processed notes move into `raw/`, they are not deleted.
- **Identity is metadata, not a folder.** Use frontmatter `identity: {{IDENTITY_VALUES}}`.
- **Three axes, three mechanisms.** Lifecycle goes to folders. Identity goes to the `identity:` field.
  Subject goes to tags and links from the controlled vocabulary in `wiki/_tags.md`. Never make folders carry
  subject. Never make tags carry status, type, or identity. The canonical rule is in `wiki/_conventions.md`.
- **Digests are an interface, not a record.** `/digest` writes a spoken-word script and an MP3 to
  `digests/`. It is **not** a capture, `/process` never reads that folder, and it is never offered
  proactively. See the Digests section below.
- **No git.** Dropbox handles sync and version history. Never run git commands in this vault.

## Capture prompting

At the end of a session, or whenever you and the owner produce durable knowledge, **offer to capture it**:
"This looks worth capturing. Want me to drop it to the brain inbox?" Durable knowledge means a decision, a
method, a spec, a finding, or a corrected fact.

Offer at natural stopping points. Do not capture silently and do not nag mid-flow. Capture on the owner's yes.

## Offering a skill

A repeatable method is not knowledge, it is a **skill**. **The bar is high on purpose.** Two things must
both be true: the owner will run the method again, **and** it is worth a maintained artifact. Gate 2 is met
only by a **business process** they run, a **personalization** of how they want work done, or a **way of
working with AI** they repeat. **Name the kind in the offer. If you cannot name one, do not offer.**

**Do not offer for minor process detail**, for one-off troubleshooting, or for a fact, a finding, a
reference, a decision, or a corrected claim. **When in doubt, stay silent.** A missed candidate is
recoverable through a `/brain-skill` sweep. A wrong offer is an interruption that cannot be taken back.

**Offer at capture and at maintain only.** Never at process, which runs unattended, so an offer there is
never seen. Never at pull, which would interrupt the answer. One offer per candidate per session, one line,
after the work finishes.

A yes **builds the skill now**, on the surface this session is on. The rules are in `SCHEMA.md` §6e and §9.
Read them there.

## Pull

When the owner asks something the brain might know, answer from `wiki/` and cite the pages you used. If the
wiki does not cover it, say so. If the answer is durable, offer to capture it.

## Digests

`/digest` turns the substantive content of a session into a **spoken-word script plus an MP3**, written to
`digests/`, for listening to later. The rules are in `SCHEMA.md` §6f. Read them there.

Four things that are easy to get wrong:

- **It is not a session summary.** A summary says "we decided X". A digest explains what X is and why it
  beat Y, slowly enough to follow while driving.
- **It is not a capture.** Durable knowledge still goes to `inbox/`. Offer that separately, after, and only
  at a stopping point.
- **`/process` never reads `digests/`.** A lossy spoken restatement must never reach the source of truth.
- **Never offer a digest proactively.** Wait to be asked. Reply with one line and stop.

## Updating this vault

This vault was built from the **ai-brain-seed** kit. Its version is in `.claude/VERSION.md`. `/brain-update`
checks the kit for newer versions and applies only what the owner approves. The rules are in `SCHEMA.md`
§13.

Never run git in this vault as part of an update. The kit gets cloned somewhere else.

## Skills — the vault is the source

The `/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`, `/digest`, and `/brain-update` commands
and their skills live in **`.claude/` in this vault**. Each machine installs them by copy into `~/.claude/`. **Never edit the
installed copy.** Edit the vault copy and reinstall.

The skills are thin. They carry the job skeleton and the vault-resolution logic, and they point at
`SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the rules. So **a protocol change needs no
install**. Edit `SCHEMA.md` and every machine and surface picks it up through Dropbox. Reinstall only when a
skill file itself changes.

**To install or update the skills on any machine, read `.claude/INSTALL.md`.** It carries the copy commands,
the `BRAIN_DIR` setting, an optional drift check, and how to verify.

For humans, see `PROCESS.md`. The same protocol is followed on every surface.
