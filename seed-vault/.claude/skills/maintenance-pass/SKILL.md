---
name: maintenance-pass
description: >
  This skill should be used to clean, audit, or lint the brain. Triggers include "/maintain", "run a
  maintenance pass", "check for broken links", or "find contradictions". It scans the vault's wiki for broken
  wikilinks, orphan pages, contradictions, stale pages, and invalid frontmatter, reports findings, applies
  safe fixes, and logs the pass.
---

# Maintenance pass (lint)

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `wiki/`.** This skill runs from any project
directory, and a relative path resolves against that project instead of the brain. Every path below is
relative to `<brain>`.

## Step 0 — load the binding protocol, every run, before anything else

You are linting *against* these files, so read them first. Do not lint from memory. They are authoritative
and they may have changed since the last pass.

- **`wiki/_conventions.md`** — the page contract you are checking pages against.
- **`wiki/_tags.md`** — the controlled vocabulary, including the retired-tag redirects.
- **`SCHEMA.md` §5 and §7** — the required frontmatter, and what `_index.md` and `_log.md` are each for.

## The job

1. Scan `wiki/` for broken `[[links]]`, orphan pages, contradictions between pages on the same subject, stale
   pages whose `sources:` changed, missing or invalid frontmatter, and **off-vocabulary tags**. An
   off-vocabulary tag is any `tags:` value not in `wiki/_tags.md`, or a tag that encodes status, type, or
   identity, which belong in their own fields. Map a retired tag to its canonical replacement per
   `wiki/_tags.md`.

   - **Resolve wikilinks the way the vault writes them.** There are five forms: a bare `[[slug]]`, a
     folder-relative `[[<project>/<page>]]`, an aliased `[[slug|text]]`, a section link `[[slug#Heading]]`,
     and an **escaped-pipe alias `[[slug\|text]]`**, which is required inside a markdown table. A checker
     that misses any of the five reports false positives.
   - **Exclude `_log.md` from the broken-link check and the orphan check.** It is an append-only journal. It
     records pages that were later deleted, it quotes broken links it just fixed, and it holds literal syntax
     examples. All of that is correct content. Flagging it means every logged repair poisons the next pass.
     For the orphan check, a mention in `_log.md` is **not** an inbound link. A page whose only reference is
     the journal is an orphan.
   - **Parse the retired list in `wiki/_tags.md` from the left of the arrow only.** The right side names the
     *replacement* tag. Sweeping it up condemns every correctly-tagged page that uses it.
   - **Sweep for methods in the wiki the owner still runs by hand and could be a skill.** Apply both gates
     in `SCHEMA.md` §9: the owner will run the method again, **and** it is a business process, a
     personalization, or a way of working with AI that they repeat. Minor process detail does not qualify,
     and neither does a fact, a finding, or a reference. Name the kind for each candidate you raise. Read the
     library's `registry.md` first, so a declined skill is not proposed again. Resolve the library as
     `$SKILLS_DIR`, else the sibling of `<brain>` named `{{SKILLS_DIRNAME}}`. Report the candidates as
     proposals in the findings, per `SCHEMA.md` §6e and §9. **Never act on one without the owner's yes.** On
     a yes, hand off to the **skill-library** skill in build mode.

2. **Move aged digests.** Any file in the `digests/` root older than **60 days** moves into
   `digests/heard/`, the markdown and its MP3 together. **Nothing is deleted, ever.** This is a file move by
   age: do not open a digest, do not judge its content, and do not lint it. `digests/` is not part of the
   wiki, and nothing in it is a source. Report how many moved. See `SCHEMA.md` §6d and §6f.

3. Report the findings grouped by category, with page paths.
4. Apply the safe fixes: broken links, missing frontmatter fields, orphans relinked into `_index.md`, and
   retired tags remapped to their canonical form. Do NOT silently resolve a contradiction. Do NOT invent a
   new canonical tag. Propose vocabulary additions to `wiki/_tags.md` and list both for the owner.
5. Update `wiki/_index.md` if needed. Append a `maintenance` entry to `wiki/_log.md`.

## Hard rules

- Never edit `raw/`. It is immutable, and a stale source is not a defect to fix.
- Never delete a page to resolve a finding. Propose it and let the owner decide.
- Never delete a digest or its MP3. `heard/` is an archive, not a staging area for deletion.
- Never lint, edit, or compile anything in `digests/`. The retention move is the only thing you do there.
- Never run git in this vault.
