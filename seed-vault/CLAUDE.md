# CLAUDE.md — brain (Dropbox, git-free)

This repository is the owner's **LLM-maintained knowledge brain**, stored in Dropbox. Your job is to build and
maintain it, not just answer from it.

**Before doing anything here:** read `SCHEMA.md` (your full protocol) and `wiki/_conventions.md` (the rules).

## Core rules
- **Capture is frictionless.** Anything the owner wants to save goes to `inbox/` as a timestamped note — no
  filing decisions at capture time. Use the `capture-to-inbox` skill.
- **Compilation is separate.** `inbox/` → `wiki/` happens on `/process` or the nightly scheduled task, using
  the `process-inbox` skill. Don't compile during a capture.
- **You own `wiki/`.** Concept-per-page, interlinked, with frontmatter per `_conventions.md`.
- **Sources are immutable.** Never fabricate facts — every wiki claim traces to a note in `raw/` (or an
  inbox note being processed). Processed inbox notes are moved into `raw/`, not deleted.
- **Identity is metadata, not a folder.** Use frontmatter `identity: {{IDENTITY_VALUES}}`.
- **Three classification axes, three mechanisms.** Lifecycle → folders, identity → `identity:` field, subject →
  tags + links from the controlled vocabulary in `wiki/_tags.md`. Never make folders carry subject or tags
  carry status/type/identity. Canonical rule in `wiki/_conventions.md`.
- **No git.** Dropbox handles sync and versioning. Never run git commands in this vault.

## Capture prompting (important behavior)
At the end of a session, or whenever we produce durable, reusable knowledge — a decision, a method, a spec,
a finding, a corrected fact — **proactively offer**: "This looks worth capturing — want me to drop it to the
brain inbox?" Don't capture silently and don't nag mid-flow; offer at natural stopping points and capture on
the owner's yes.

## Pull
When the owner asks something the brain might know, answer from `wiki/` and cite the page(s). If it's not
covered, say so. If the answer is durable, offer to capture it.

For humans: see `PROCESS.md`. This same protocol is followed on every surface (Claude Code, Cowork, chat).
