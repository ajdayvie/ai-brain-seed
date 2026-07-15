# SCHEMA.md — Operating Manual for the Brain (Dropbox, git-free)

Read this fully at the start of every session, with `wiki/_conventions.md`. Binding unless the owner changes
it — and when they do, update this file + `_conventions.md` + `PROCESS.md` together.

## 1. What this is
A personal LLM-maintained knowledge base in plain markdown, stored in Dropbox so every surface can reach it.
The wiki — not chat history or model memory — is the durable source of truth.

## 2. Store & sync
Lives in a Dropbox folder, mirrored to local disk. Set the vault folder (ideally the whole Dropbox account
dedicated to it) to **Local / "Make available offline"**, not online-only, so files are real on disk and a
shell session can mount them. Dropbox handles all sync (across machines) and version history. There is
**no git**. Do not create or use a git repo here.

## 3. Structure & the golden flow
`inbox/` (frictionless capture) → `raw/` (immutable sources) → `wiki/` (you build knowledge) → `outputs/` (deliverables).
- `inbox/` — timestamped capture notes from any surface, awaiting compilation.
- `raw/` — immutable source material, organized loosely by topic. Processed inbox notes are moved here.
- `wiki/topics/` — evergreen knowledge by subject (flat; nest only when a cluster grows).
- `wiki/projects/<slug>/` — active efforts; pull from topics; graduate learnings back to topics when done.
- `wiki/archive/` — finished/dormant projects.
- `outputs/<project>/drafts/` then `outputs/<project>/` — deliverables (code outputs go in their own project repo, not here).

## 4. Identity is metadata
Never file by identity (business, role, or context). Use frontmatter `identity: {{IDENTITY_VALUES}}`.
A cross-cutting fact lives once (usually in `topics/`) and is filtered by tags/identity, never duplicated
per identity.

## 5. Frontmatter (required on every wiki page)
```yaml
---
title: <Human-readable title>
type: concept | reference | source-summary | canonical | process | log
identity: {{IDENTITY_VALUES}}
tags: [tag1, tag2]            # subject axis only; from the controlled list in wiki/_tags.md (not free-form)
status: draft | stable | needs-review
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/<path>, ...]   # what this derives from; [] if synthesized
---
```
Classification runs on three independent axes — **lifecycle** (folders: topics/projects/archive),
**identity** (the `identity:` field), and **subject** (`tags:` + wikilinks from `wiki/_tags.md`). Each axis
uses one mechanism; never make folders carry subject or tags carry status/type/identity. See
`wiki/_conventions.md` for the full rule.

## 6. Workflows

### 6a. CAPTURE (anything → inbox)  [skill: capture-to-inbox]
Triggered by "capture this", "/capture", or by you offering at a natural stopping point.
1. Take the content (provided text, or the durable knowledge from the current session).
2. Write ONE note to `inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md` with a 1-line `context:` header and the content.
3. Do NOT file it into the wiki, do NOT make filing decisions. That's the whole point — capture is dumb and fast.
4. Confirm what you captured.

### 6b. PROCESS (inbox → wiki)  [skill: process-inbox]
Triggered by "/process", "process the inbox", or the nightly scheduled task. Run it on a surface with native
disk access to the vault (local Claude Code / Cowork), so the move-into-`raw/` step can actually delete from `inbox/`.
1. Read each note in `inbox/`.
2. Compile it into the wiki: concept-per-page (a note may yield several pages), correct topic/project, full
   frontmatter (set `identity`), wikilinks to existing pages, no cross-domain duplication.
3. Move the source note from `inbox/` into `raw/<topic>/` (it becomes the immutable source); set the wiki
   page's `sources:` to that path.
4. Update `wiki/_index.md` (catalog) and append to `wiki/_log.md`.
5. If a note is ambiguous or you're unsure where it belongs, LEAVE it in `inbox/` and add a line to `_log.md`
   flagging it for the owner — never force a bad filing.
6. Report what you filed and what you left.

### 6c. PULL (query the brain)  [command: /pull]
Answer from the wiki with citations to specific pages. If not covered, say so. If the answer is durable,
offer to capture it.

### 6d. MAINTENANCE (lint)  [skill: maintenance-pass]
Triggered by "/maintain" or "run a maintenance pass". Scan for broken wikilinks, orphan pages, contradictions,
stale pages, and invalid frontmatter. Report, apply safe fixes, list contradictions for the owner's decision,
update `_log.md`.

## 7. Index vs Log
- `wiki/_index.md` — catalog: every page, link, one-line summary. What exists.
- `wiki/_log.md` — append-only journal: `## [YYYY-MM-DD] <type> | <description>` (types: capture, process,
  wiki, draft, final, conventions, maintenance, flag). What changed.

## 8. The nightly compile
{{NIGHTLY_METHOD_SUMMARY}}
Treat scheduled runs exactly like a manual `/process`, including leaving ambiguous notes for the owner.
See `PROCESS.md` for the concrete setup on this machine.

## 9. Capture-prompting behavior
Proactively offer to capture at the end of sessions and when durable knowledge appears (decision, method,
spec, finding, corrected fact). Offer, don't nag; capture on the owner's yes.

## 10. Cross-surface
- Claude Code: reads `CLAUDE.md` → this file automatically; capture/process/pull via skills/commands; attach
  the brain to a project session with `--add-dir <brain path>` or `additionalDirectories` in the project's settings.
- Cowork / Claude Desktop: a Project pointed at this folder; can run a scheduled task; can write files directly.
- claude.ai chat (web/phone): reaches the brain via the Dropbox connector — read to pull, and (if the
  connector has write access) append to `inbox/`; otherwise capture via a dispatch to the always-on machine.
- ChatGPT (optional): a private custom GPT acting as a pull-and-capture client via the Dropbox app; it never
  processes or edits `wiki/`/`raw/`.

## 11. Guardrails
- Never edit `raw/`. Never fabricate facts or sources.
- Never duplicate a cross-cutting fact across topics/projects — link the canonical page.
- Never run git here.
