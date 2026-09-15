---
name: process-inbox
description: >
  This skill should be used to compile the brain inbox into the wiki. Triggers include "/process", "process
  the inbox", or a scheduled nightly run. It reads each note in the vault's inbox/, builds concept-per-page
  wiki pages with frontmatter and links, moves the source note into raw/, and updates _index.md and _log.md.
---

# Process inbox -> wiki

Run this on a surface with native disk access to the vault: local Claude Code or Cowork, with the Dropbox
folder set to Local / available offline. Step 3 removes the note from `inbox/`, and that needs real disk
access.

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `inbox/` or `wiki/`.** This skill runs from any
project directory, and a relative path resolves against that project instead of the brain. Every path below
is relative to `<brain>`.

## Step 0 — load the binding protocol, every run, before anything else

Read these three files and follow them. They are authoritative, they may have changed since the last run, and
this skill **deliberately does not copy their rules**. Do not work from memory.

- **`SCHEMA.md` §6b** — governs this job: what gets filed, what may be left, and how.
- **`wiki/_conventions.md`** — the page contract: the three axes, frontmatter, linking.
- **`wiki/_tags.md`** — the controlled subject vocabulary.

Where this skill and those files disagree, **they win**. Say so in the report, so the skill gets fixed.

## The job

For each note in `<brain>/inbox/`:

1. Read the note and understand it.
2. **Compile it into the wiki** per `wiki/_conventions.md`: concept-per-page (one note may yield several
   pages), folder chosen by lifecycle, `identity` set, subject tagged from `wiki/_tags.md`, wikilinks to
   existing pages, no cross-domain duplication.
3. **Move the source note** from `inbox/` into `raw/<topic>/`. It becomes the immutable source. Set each new
   page's `sources:` to that path.
4. **Update the catalog and the journal:** `wiki/_index.md`, and a `process` entry appended to `wiki/_log.md`.
5. **Decide file-versus-leave by SCHEMA §6b steps 5 and 6**, not from memory. That is the rule most likely to
   have changed. Anything left in `inbox/` also gets a `flag` line in `_log.md` saying exactly what was
   uncertain.
6. **Report** what you filed and where, what you moved into `raw/`, and what you left in the inbox and why.

## Hard rules (SCHEMA §11 — restated because a mistake here is expensive)

- Never edit `raw/`. Never fabricate a fact or a source.
- Never invent a tag. Propose an addition to `wiki/_tags.md` instead.
- Never duplicate a cross-cutting fact across pages. Link the canonical page.
- **Never read `digests/`.** It is not part of the inbox and it is not a source. A digest is a lossy spoken
  restatement written for ears, and compiling one into the wiki puts prose that was never the source into
  the source of truth. If a digest holds something durable that was never captured, the fix is a real
  capture note, not a filing of the digest. See `SCHEMA.md` §6b step 8.
- Never run git in this vault.
