# STANDALONE.md — set up an LLM-maintained knowledge brain (single-file edition)

> **Human:** paste this entire document into an AI assistant — ideally Claude Code running on the machine
> where your Dropbox lives — with one of these prompts:
>
> - **"Teach me how the brain works before setup."** → the AI explains the system and answers questions;
>   nothing is written.
> - **"Set up the brain."** → the AI runs a guided interview, then builds your vault from the templates in
>   Part III.
>
> This is the self-contained edition of the `ai-brain-seed` kit
> (https://github.com/ajdayvie/ai-brain-seed) — same content, no download needed.
> Everything below is addressed to the AI.

---

You are setting up (or explaining) a **personal LLM-maintained knowledge brain**: a plain-markdown
knowledge base in a Dropbox folder, reachable from every AI surface the owner uses, in which the wiki — not
chat history or model memory — is the durable source of truth.

This document has seven parts:

- **Part I — Background**: the why. Read it first; you cannot set up or teach what you don't understand.
- **Part II — Setup procedure**: the guided interview and build steps.
- **Part III — Vault file templates**: every file the vault needs, verbatim, with `{{PLACEHOLDER}}` values.
- **Part IV — Surfaces**: connecting Claude Code, Cowork/Desktop, claude.ai chat, and phone.
- **Part V — Scheduling**: the nightly compile (recommended scheduled task + alternatives).
- **Part VI — ChatGPT** (optional): a private custom GPT as a ChatGPT-side client.
- **Part VII — Backfilling**: seeding the initial wiki from existing context and memory.

## MODE 1 — "teach me"

Explain, don't build. Walk the owner through, conversationally and in this order: the problem (knowledge
evaporates across AI surfaces) → the claim (the wiki you own is the source of truth; every tool is just a
client) → the Karpathy framing (spec / verifier / environment; the brain is the environment's knowledge
base) → the golden flow (`inbox/ → raw/ → wiki/ → outputs/`) and the three verbs (capture / process /
pull) → the three classification axes → what daily use feels like (capture freely, nightly compile, pull
with citations) → what setup will require from them (Part II, step 0). Answer questions from Part I and
the `SCHEMA.md` template in Part III. Offer to run setup when they're ready; don't write anything until
they say so.

## MODE 2 — "set up the brain" (Part II — Setup procedure)

### Step 0 — human prerequisites (tell the owner; wait until done)

The owner must do these themselves — you cannot and must not do account signups or grant permissions for
them:

1. **A Dropbox account** — ideally a *dedicated* account for the brain (avoids contention with existing
   sync usage and keeps connector permissions clean), but a dedicated folder in an existing account works.
2. **Dropbox for desktop installed** on the machine you're running on (and on any always-on machine that
   will run the nightly compile), signed in to that account.
3. **The vault folder set to Local / "Make available offline"** — NOT online-only. The files must be real
   on disk; the process step moves files and cannot work through a virtual stream drive.
4. Decide the vault location, e.g. `~/Dropbox/AI-Brain` (default name: `AI-Brain`).
5. Optional, for the chat surface later: the **Dropbox connector** available in claude.ai settings.

### Step 1 — the interview

Ask, one block at a time (skip anything already answered):

1. **Name** — what name should appear as the approver in the vault's conventions and log?
2. **Vault path** — confirm the exact local path (verify it exists and is writable; verify it looks like a
   real synced folder, not a placeholder stream).
3. **Identities** — "What distinct contexts do you operate in — businesses, employers, roles, personal?"
   Build the identity vocabulary: short lowercase slugs (e.g. `acme | consulting | personal | na`). Always
   include `na` (for knowledge that belongs to no identity, like the brain's own pages). Recommend
   `personal` plus one slug per business/role. Two to five values is the sweet spot; a single-context owner
   can use just `personal | na`.
4. **Surfaces** — which do they use? Claude Code / Cowork or Claude Desktop / claude.ai chat / phone /
   ChatGPT. (Only affects which setup steps you run in Step 4.)
5. **Scheduling** — "Do you have a machine that's on most nights?" Yes → recommend Option A in Part V
   (OS scheduler + headless Claude Code). App-always-open instead → Option B (Cowork scheduled task). No
   always-on machine → Option C (manual cadence + a recurring reminder); help them pick the reminder
   mechanism.
6. **Confirm** before writing: vault path, identity list, chosen scheduling option, surfaces to configure.

### Step 2 — build the vault

1. Create this tree at the vault path (empty folders get a `.keep` file), then write every file from
   Part III at its stated path:

   ```
   <vault>/
     SCHEMA.md  CLAUDE.md  PROCESS.md  README.md
     inbox/.keep   raw/.keep   outputs/.keep
     wiki/_conventions.md  wiki/_tags.md  wiki/_index.md  wiki/_log.md
     wiki/topics/.keep  wiki/projects/.keep  wiki/archive/.keep
     .claude/skills/capture-to-inbox/SKILL.md
     .claude/skills/process-inbox/SKILL.md
     .claude/skills/maintenance-pass/SKILL.md
     .claude/commands/capture.md  process.md  pull.md  maintain.md
   ```

   Never create a git repo in the vault — it is git-free forever (Dropbox is the sync and history layer).
2. Replace placeholders in every written file:
   - `{{IDENTITY_VALUES}}` → the pipe-separated identity list, e.g. `acme | personal | na`
   - `{{IDENTITY_VALUES_SLASH}}` → the same list slash-separated, e.g. `acme / personal / na`
   - `{{OWNER_NAME}}` → the owner's name
   - `{{TODAY}}` → today's date, `YYYY-MM-DD`
   - `{{NIGHTLY_METHOD_SUMMARY}}` (in `SCHEMA.md`) → one or two sentences naming the chosen scheduling
     option
   - `{{NIGHTLY_METHOD_DETAIL}}` (in `PROCESS.md`) → a short paragraph describing the concrete setup chosen
     in Step 4c (schedule time, script path or reminder mechanism, log location)
3. Verify: no `{{` remains anywhere in the vault.

### Step 3 — first-run verification (do not skip)

Run the loop once end-to-end from a Claude Code session inside the vault:

1. **Capture:** "capture this: the brain was initialized today from ai-brain-seed" → confirm one
   timestamped note lands in `inbox/`.
2. **Process:** run `/process` → confirm a wiki page is built with valid frontmatter, the note moved to
   `raw/`, and `_index.md` / `_log.md` updated.
3. **Pull:** ask "when was this brain initialized?" → confirm the answer cites the new page.

If any step fails, fix the cause before proceeding — this loop is the whole system.

### Step 4 — connect the surfaces (per the owner's Step-1 answers)

a. **Claude Code everywhere:** follow Part IV §1 — offer to add a brain-awareness section to the owner's
   user-level `~/.claude/CLAUDE.md` and `additionalDirectories` to the projects they name.
b. **Cowork / Claude Desktop:** walk them through creating the Project and pasting the instruction block
   from Part IV §2.
c. **Scheduling:** implement the chosen option from Part V. For Option A you may write the wrapper script
   and (on their confirmation) register the scheduled task; the owner must run `claude setup-token`
   themselves and store the token. For Option C, help them set the recurring reminder.
d. **claude.ai chat:** have the owner connect the Dropbox connector; test one pull and (if write access)
   one capture per Part IV §3.
e. **ChatGPT (optional):** hand them the builder prompt from Part VI with `<VAULT>`/`<OWNER>` filled in,
   then run its three verification tests.

### Step 5 — seed it

Offer the owner the backfill program in Part VII, starting with the **brain-dump interview** (Pass 1) right
now if they have 20 minutes. Remind them: modest seed + steady capture beats a giant import.

### Step 6 — handoff

Close by telling the owner, in plain language: where the vault is; the three verbs and how to invoke them
from each of their surfaces; when the compile runs (or when their reminder fires); to check `wiki/_log.md`
occasionally for `flag` entries awaiting their judgment; and to read `PROCESS.md` (their handbook) and
optionally open the vault in Obsidian to browse it.

## Rules that bind YOU during setup

- Never run git inside the vault; never leave a `.git` folder there.
- Never fabricate facts or sources anywhere in the vault; the log's first entry records only what actually
  happened.
- Don't perform account signups, permission grants, or token generation for the owner — instruct, verify,
  proceed.
- Confirm before overwriting anything that already exists at the vault path.
- After setup, the vault's own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol — including
  for you, in every future session.

---

# Part I — Background

This is the reasoning behind the system. Read it to understand *why* before you build; nothing here is
operational protocol (that lives in the seed vault's `SCHEMA.md` and `wiki/_conventions.md`).

## The problem: knowledge evaporates

Working with AI across many surfaces — a CLI coding agent, a desktop app, a web chat, a phone — creates a
knowledge-loss problem. Useful decisions, methods, specs, and findings get produced inside a chat or a coding
session and then **evaporate** when that session ends. Per-surface memory features (chat memory, project
memory, session memory) don't travel between surfaces, so leaning on them quietly breaks the promise that
knowledge *accumulates*.

The brain fixes this by making the knowledge an **artifact you own** — markdown files in your own storage —
and giving the AI a disciplined, repeatable way to write into it and read out of it. Because durable
learnings get promoted *up* into a wiki, the system **compounds over time** instead of resetting every
session.

The defining claim of the whole system:

> **The wiki — not chat history, not model memory, not any one tool's built-in memory — is the durable
> source of truth.** Everything else (the tools, the connectors, the skills) is interchangeable plumbing
> around one durable, owned set of files.

## The Karpathy method

The architecture is a direct expression of a working method for getting high-quality output from AI agents,
articulated by Andrej Karpathy (talks and interviews, 2026). It has three layers that stack:

- **Spec** — get your understanding of the goal into a precise, scoped plan *before* building. Uncover the
  real goal, not just the stated task; work in small reviewable buckets; force explicit verification of key
  decisions.
- **Verifier** — give the agent a way to *check* its own output against a defined bar. This is the
  highest-ROI layer: define "good" precisely, use a second model as critic, pull external signal (tests,
  linters, reference artifacts).
- **Environment** — the workshop that compounds: always-on rules (a `CLAUDE.md`), a **knowledge base**,
  on-demand **skills** (procedures), and deterministic hooks.

The mental model is the **robot librarian**: the model is brilliant when the answer is in its library and
confidently wrong when it isn't. Pleading with it changes nothing — the only levers you actually control are
spec, verifier, and environment. And the principle underneath it all:

> **"You can outsource your thinking, but you can't outsource your understanding."**

**The brain is the knowledge-base layer of that environment.** That is its entire reason for existing. The
protocol documents (`SCHEMA.md`, `_conventions.md`) are its spec; the maintenance pass and the
cite-your-sources rule are its verifiers.

Karpathy also sketched the direct ancestor of this design: an **LLM-maintained markdown wiki** that replaces
RAG at personal scale — the model doesn't retrieve fragments from an index, it *curates* a small, coherent,
linked library it can actually read. The brain implements that idea and extends it across surfaces. The
spiritual ancestor is Vannevar Bush's **Memex** (1945) — with the LLM finally doing the curation Bush
couldn't automate.

## The adaptations — what this design adds to the base idea

### 1. The inbox split: capture ≠ compile

Capture must be frictionless from anywhere; compilation must be careful and needs a capable local surface.
Splitting them removes the "where does this go?" burden at capture time — nothing is lost to filing friction.
**Capture is frequent and dumb; processing is periodic and careful; pulling is whenever.** The trade-off
(knowledge is briefly unfiled until processed) is handled by a nightly compile.

### 2. Brain-as-library: every tool is a client

Claude Code, claude.ai chat, Cowork, even a ChatGPT custom GPT are *clients* that read from and write to the
brain — **none of them is the brain.** The portable unit across surfaces is the **protocol** (in
`SCHEMA.md`), not any tool's skill file or memory feature. Each surface carries the same behavior through
whatever mechanism it has: slash commands, project instructions, or a connector-driven launcher. Because the
binding rules live in the vault itself, every surface stays correct when the conventions change — there is
nothing to re-sync.

### 3. Skills vs knowledge: a verb is not a noun

A **skill** is a reusable *procedure* ("how to capture") — stateless, loaded on demand. **Knowledge** lives
in the wiki — it persists in files. The skill remembers nothing; the wiki remembers everything. This
separation is what keeps the system coherent as tools change underneath it.

### 4. Identity is metadata, not a folder

If you operate in several contexts (businesses, roles, personal), never file knowledge by context. Much of
the valuable knowledge is cross-cutting; filing by context would wall it off inside one context's folder or
duplicate it across several. Instead, knowledge is **filed by subject**, and identity is a frontmatter
*filter*. A cross-cutting fact lives exactly once and is filterable — never walled off, never duplicated.

This generalizes to **three independent classification axes, three mechanisms**:
- **Lifecycle** (evergreen / active / done) → folders (`topics/` · `projects/<slug>/` · `archive/`)
- **Identity** (your contexts) → the `identity:` frontmatter field
- **Subject** → tags + wikilinks from a controlled vocabulary (`wiki/_tags.md`)

Keep each axis on its own mechanism and filing is mechanical; collapse two onto one and filing becomes a
judgment call.

### 5. No git — cloud sync is the versioning layer

Versioning and backup matter, but a git repo imposes cross-surface friction (hooks, push/pull discipline,
repo paths, merge states) that isn't worth it for personal notes. Dropbox provides sync across machines and
file version history for free. **There is no git in the vault, ever.**

Why Dropbox specifically (and not, say, Google Drive): the vault must exist as **real files on local disk**
("Make available offline"), because the process step moves files and a shell/agent session must be able to
mount the folder. Google Drive's virtual stream drive could not be mounted by agent sandboxes in testing,
and Dropbox has a first-party Claude connector for the chat surface. Any sync product that (a) mirrors real
files to disk and (b) has a connector your chat surface can read would work; Dropbox is the proven default.

### 6. Immutable sources: the traceability spine

Processed inbox notes are *moved* into `raw/` and never edited again. Every wiki claim traces back to a
frozen source via the `sources:` frontmatter field, so the wiki can always be audited or rebuilt, and the
LLM can never quietly launder a fabricated fact into "established knowledge." Never fabricate facts or
sources; a claim without a source doesn't go in the wiki.

## Key design decisions, consolidated

| Decision | Why | Trade-off accepted |
|----------|-----|--------------------|
| No git | Cross-surface friction outweighs git's value for personal notes; Dropbox gives sync + history | Lose fine-grained diffs/branching |
| Dropbox, local/offline mode | Real files on disk, mountable by agent sessions; first-party Claude connector | A second cloud account to manage; local disk space |
| Inbox split (capture ≠ compile) | Frictionless capture from anywhere; careful compilation locally | Knowledge briefly unfiled until processed |
| Subject, not identity | Cross-cutting knowledge lives once, filterable; never walled off or duplicated | Must set `identity` correctly at process time |
| Immutable `raw/` | Every wiki claim traces to a frozen source; auditable, rebuildable | Can't tidy a source after the fact (write a new one) |
| Concept-per-page | Knowledge composes and links cleanly; avoids document-shaped silos | More pages, more linking discipline |
| LLM owns the wiki | The whole point — the agent curates, the human reviews | Requires trust + periodic maintenance passes |

## The governance chain

The documents form a deliberate chain from thin-and-always-loaded to deep-and-on-demand:

| Doc | Role |
|-----|------|
| `CLAUDE.md` | Thin, auto-loaded entry point; points to SCHEMA |
| `SCHEMA.md` | The full binding protocol — the law that governs all reads and writes |
| `PROCESS.md` | Plain-language human handbook |
| `wiki/_conventions.md` | The per-page contract (naming, frontmatter, linking, the three axes) |
| `wiki/_tags.md` | The controlled subject vocabulary |
| `wiki/_index.md` | Catalog — *what exists* |
| `wiki/_log.md` | Append-only journal — *what changed* |

Index vs log is an easy thing to confuse: `_index.md` answers "what's in here?", `_log.md` answers "what
happened?".

## Guardrails (always true)

- Never edit `raw/`; sources are immutable.
- Never fabricate facts or sources; every wiki claim traces to a source.
- Identity is metadata, not a folder; file by subject.
- No cross-domain duplication; link the canonical page.
- No git in the vault, ever.
- Never force a bad filing — ambiguous notes stay in the inbox, flagged for the human.
- The AI offers to capture at natural stopping points; it never captures silently and never nags.

---

# Part II — Setup procedure

The full procedure is MODE 2 above; it is not repeated here.

---

# Part III — Vault file templates

Write each file at the stated path (relative to the vault root), verbatim, then apply the
placeholder replacements from Step 2.

## File: `SCHEMA.md`

````markdown
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
````

## File: `CLAUDE.md`

````markdown
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
````

## File: `PROCESS.md`

````markdown
# PROCESS.md — human handbook

How to actually use the brain day to day. The machine-facing protocol lives in `SCHEMA.md`; this is the
plain-language companion.

## The daily loop
Capture freely as you work — any decision, method, spec, finding, or corrected fact goes to `inbox/` with no
filing. Don't stop to organize. Once a day (or on the nightly schedule) the inbox is **processed**: each note
is compiled into the wiki, its source moved into `raw/`, and the index and log updated. When you need to know
something, **pull** from the wiki and it answers with citations. Capture is frequent and dumb; processing is
periodic and careful; pulling is whenever.

## Capturing from each surface
- **Claude Code / Cowork (local):** the vault folder is on disk. Say "capture this" or run `/capture`; Claude
  writes a timestamped note to `inbox/`.
- **claude.ai chat (web/phone):** with the Dropbox connector connected (and write access), say "capture this
  to the brain" and Claude appends a note to `inbox/` directly.
- **Either way** the note is just dropped in the inbox — filing happens later at process time.

## The nightly compile
{{NIGHTLY_METHOD_DETAIL}}

Ambiguous notes are intentionally left in the inbox and flagged in `_log.md` for you to file by hand.

## Run process where the files are local
The "move note out of inbox" step deletes from `inbox/`, so run `/process` on a surface with native disk
access to the vault (local Cowork or Claude Code with the Dropbox folder set to Local/available offline).
That's also where any scheduled task should run.

## Pulling from any surface
Ask a question; Claude answers from `wiki/` and cites the pages it used. From claude.ai chat (web or phone),
add the **Dropbox connector** so chat can read the wiki. If the answer is durable, accept the offer to
capture it back into the inbox.

## Backfilling existing context
Don't try to file everything at once. As topics come up in real work, capture what you know into the inbox and
let processing build the pages. The brain compounds over time; old material graduates in as it becomes relevant.

## Tools
- **Obsidian** to read and navigate (`[[wikilinks]]`, graph view).
- **Dropbox for desktop** with the vault folder set to **Local / "Make available offline"** (not online-only)
  so files are local and fast — and mountable by a shell session.
- No git, ever — Dropbox is the sync and history layer.
````

## File: `README.md`

````markdown
# Brain

A personal, LLM-maintained knowledge base in plain markdown, stored in Dropbox so every Claude surface
(Claude Code, Cowork, claude.ai chat on web/phone) can reach it. The wiki — not chat history or model memory —
is the durable source of truth.

## The golden flow
`inbox/` → `raw/` → `wiki/` → `outputs/`

Capture anything worth keeping into `inbox/` (fast, no filing). Compilation moves notes into `raw/` (immutable
sources) and builds them into `wiki/` (concept-per-page, interlinked). Deliverables come out in `outputs/`.

## Three verbs
- **capture** — drop something to `inbox/` with zero filing decisions.
- **process** — compile the inbox into the wiki (on demand, or nightly).
- **pull** — ask the brain; answers cite wiki pages.

## No git
Dropbox handles sync and version history. There is no git repo here — don't create one.

## Read it
Open this folder as an [Obsidian](https://obsidian.md) vault to browse pages and follow `[[wikilinks]]`.
Keep Dropbox for desktop with this folder set to **Local / "Make available offline"** (not online-only) so
files are real on local disk.

See `SCHEMA.md` for the full protocol and `PROCESS.md` for the human handbook.
````

## File: `wiki/_conventions.md`

````markdown
---
title: Conventions
type: reference
identity: na
status: stable
created: {{TODAY}}
updated: {{TODAY}}
sources: []
---

# Conventions — how this wiki thinks

> Approved by {{OWNER_NAME}} ({{TODAY}}). The contract for every page.

## Naming
- Lowercase kebab-case filenames (`my-first-concept.md`). One **concept per page**, not one page per source.
- Inbox notes: `YYYY-MM-DD-HHMM-<slug>.md`.

## Folders
- `wiki/topics/` evergreen knowledge by subject (flat; nest only when big).
- `wiki/projects/<slug>/` active efforts; `wiki/archive/` finished/dormant.
- A cross-cutting fact lives once (usually in `topics/`); filter by tags/identity, never duplicate.

## The three axes
Every page is classified on three independent axes, each with its own mechanism. Keep them separate and
filing is mechanical; collapse two onto one mechanism and filing becomes a judgment call.
- **Lifecycle** (evergreen / active / done) → **folders**: `topics/` · `projects/<slug>/` · `archive/`. Folders encode *only* lifecycle, never subject.
- **Identity** ({{IDENTITY_VALUES_SLASH}}) → **frontmatter** `identity:`. A filter, never a folder.
- **Subject** (whatever the brain grows to cover) → **tags + wikilinks**, drawn from the controlled list in [[_tags]]. Subject never rides on folders — that's what lets a cross-cutting fact live once and still be findable.

So at process time: pick the folder by lifecycle, set `identity`, then tag by subject from [[_tags]] and link the canonical page. No single decision carries more than one axis.

## Identity (metadata, not folders)
`identity: {{IDENTITY_VALUES}}` in frontmatter. Knowledge is filed by subject; identity is a filter.

## Linking
- Obsidian wikilinks `[[slug]]` / `[[slug|text]]`. Every page links to >=1 other and is linked from >=1 (no orphans).
- Prefer linking the canonical page over restating it.

## Frontmatter (every page)
```yaml
---
title:
type: concept | reference | source-summary | canonical | process | log
identity: {{IDENTITY_VALUES}}
tags: []
status: draft | stable | needs-review
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
---
```
`tags:` are the subject axis, drawn from the controlled vocabulary in [[_tags]] — not free-form. Status, type,
and identity have their own fields and must never be expressed as tags.

## Outputs
Drafts -> `outputs/<project>/drafts/`. Finals -> `outputs/<project>/`. Code outputs go in their own repo.

## Log entry types
`capture | process | wiki | draft | final | conventions | maintenance | flag`

## Hard rules
- `raw/` and processed source notes are immutable. No fabricated facts; every claim traces to a source.
- No cross-domain duplication. No git in this vault.
````

## File: `wiki/_tags.md`

````markdown
---
title: Tag Vocabulary
type: reference
identity: na
tags: [brain, knowledge-management]
status: stable
created: {{TODAY}}
updated: {{TODAY}}
sources: []
---

# Tag Vocabulary — the controlled list

Tags are the **subject** axis only (see the three axes in [[_conventions#The three axes]]). This is the
canonical list: every `tags:` value on a wiki page must come from here. Adding a tag means **adding it here
first**, then using it — never the reverse. `maintenance-pass` lints pages against this file.

**Tags are not the place for:**
- **status** — `draft | stable | needs-review` go in the `status:` field, never as tags.
- **type** — `concept | reference | source-summary | …` go in the `type:` field (so no `talk`/`source` tags).
- **identity** — `{{IDENTITY_VALUES}}` go in the `identity:` field.

Keep the list small. Prefer an existing tag over a near-synonym; reach for a new one only when a real subject
has no home here. New tags are added at process time by proposing them here first.

## Canonical tags

### The brain / knowledge system
- `brain` — this knowledge base itself, its architecture and storage.
- `knowledge-management` — PKM concepts, methods, the library/Karpathy framing.
- `workflow` — capture / process / pull and other procedures.

### Starter subjects
<!-- The vocabulary grows with the brain. As real subjects appear during processing, add a tag here with a
     one-line definition, then use it. Group related tags under a heading. Delete this comment once the list
     has real entries. -->

## Retired / redirected (do not use)
<!-- When a tag is replaced or absorbed, move it here with an arrow to its canonical replacement, e.g.:
- `meta`, `system` → use `brain`. -->
````

## File: `wiki/_index.md`

````markdown
---
title: Brain Index
type: log
identity: na
updated: {{TODAY}}
sources: []
---

# Index — what exists in the brain

> Note: cross-cutting knowledge lives in `topics/`; identity-specific applied work lives in
> `projects/<slug>/`. Use the `identity:` field, not folders, to filter by identity.

---

*(empty — pages are added here as the inbox is processed)*
````

## File: `wiki/_log.md`

````markdown
---
title: Brain Change Log
type: log
identity: na
updated: {{TODAY}}
sources: []
---

# Log — append-only journal

Format: `## [YYYY-MM-DD] <type> | <description>`

---

## [{{TODAY}}] conventions | Brain initialized from ai-brain-seed; conventions and tag vocabulary approved by {{OWNER_NAME}}.
````

## File: `.claude/skills/capture-to-inbox/SKILL.md`

````markdown
---
name: capture-to-inbox
description: >
  This skill should be used when the user wants to quickly save something to the knowledge brain without
  filing it. Triggers include "capture this", "save this to the brain", "add to inbox", the /capture command,
  or when you proactively offer to capture durable knowledge. It writes ONE timestamped note to inbox/ and
  does no filing or wiki editing — capture is intentionally fast and dumb.
---

# Capture → inbox

1. Read `SCHEMA.md` §6a if not loaded.
2. Gather the content: either the text the user gives, or the durable knowledge from the current session
   (decisions, methods, specs, findings, corrected facts — skip transient chatter).
3. Write ONE file to `inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md`. Start it with a single `context:` line
   (where it came from / what it's about), then the content as clean markdown.
4. Do NOT create or edit wiki pages. Do NOT decide a topic/project/identity. That happens at process time.
5. Confirm what was captured and where.
````

## File: `.claude/skills/process-inbox/SKILL.md`

````markdown
---
name: process-inbox
description: >
  This skill should be used to compile the brain inbox into the wiki. Triggers include "/process", "process
  the inbox", or a scheduled nightly run. It reads each note in inbox/, builds concept-per-page wiki pages
  with frontmatter and links, moves the source note into raw/, updates _index.md and _log.md, and leaves
  ambiguous notes in the inbox flagged for the user.
---

# Process inbox → wiki

Run on a surface with native disk access to the vault (local Cowork/Claude Code with the Dropbox folder set
to Local/available offline), so step 3's move can actually remove the note from `inbox/`.

For each note in `inbox/`:
1. Read and understand it.
2. Compile into the wiki per `wiki/_conventions.md`, classifying on the three axes: pick the folder by
   lifecycle (`topics/` evergreen vs `projects/<slug>/` active), set `identity`, and tag the subject from the
   controlled vocabulary in `wiki/_tags.md` (don't invent tags — if a subject has no tag, propose adding one
   to `_tags.md`). Concept-per-page (a note may yield several), wikilinks to existing pages, no cross-domain
   duplication.
3. Move the source note from `inbox/` into `raw/<topic>/` (it becomes the immutable source). Set each new
   wiki page's `sources:` to that path.
4. Update `wiki/_index.md` and append to `wiki/_log.md` (`process` entries).
5. If a note is ambiguous or you're unsure where it belongs, LEAVE it in `inbox/` and add a `flag` line to
   `_log.md` describing the uncertainty — never force a bad filing.
6. Report: what you filed (and where), and what you left in the inbox and why.
````

## File: `.claude/skills/maintenance-pass/SKILL.md`

````markdown
---
name: maintenance-pass
description: >
  This skill should be used to clean, audit, or lint the brain. Triggers include "/maintain", "run a
  maintenance pass", "check for broken links", or "find contradictions". It scans the wiki for broken
  wikilinks, orphan pages, contradictions, stale pages, and invalid frontmatter, reports findings, applies
  safe fixes, and logs the pass.
---

# Maintenance pass (lint)

1. Scan `wiki/` for: broken `[[links]]`, orphan pages, contradictions between pages on the same topic, stale
   pages (whose `sources:` changed), missing/invalid frontmatter vs `_conventions.md`, and **off-vocabulary
   tags** — any `tags:` value not in `wiki/_tags.md`, plus tags that encode status/type/identity (which
   belong in their own fields). Map retired tags to their canonical replacement per `_tags.md`.
2. Report findings grouped by category with page paths.
3. Apply safe fixes (broken links, missing frontmatter fields, relink orphans into `_index.md`, remap retired
   tags to their canonical form). Do NOT silently resolve contradictions, and do NOT invent new canonical
   tags — propose vocabulary additions to `_tags.md` for the user. List both for the user.
4. Update `_index.md` if needed; append a `maintenance` entry to `_log.md`.
````

## File: `.claude/commands/capture.md`

````markdown
---
description: Capture something to the brain inbox (no filing)
---
Apply the **capture-to-inbox** skill for: $ARGUMENTS
If no argument is given, capture the durable knowledge from our current conversation. Write one timestamped
note to `inbox/` and confirm — do not file it into the wiki.
````

## File: `.claude/commands/process.md`

````markdown
---
description: Compile the inbox into the wiki
---
Apply the **process-inbox** skill across everything in `inbox/`. Build wiki pages, move sources into `raw/`,
update `_index.md` and `_log.md`, and leave ambiguous notes flagged. Report what you filed and what you left.
````

## File: `.claude/commands/pull.md`

````markdown
---
description: Answer from the brain wiki with citations
---
Answer this from the brain wiki, citing the specific pages you used: $ARGUMENTS
If the wiki doesn't cover it, say so plainly. If the answer is durable and worth keeping, offer to capture it.
````

## File: `.claude/commands/maintain.md`

````markdown
---
description: Run a maintenance / lint pass
---
Apply the **maintenance-pass** skill across the entire `wiki/`. Report by category, apply safe fixes, list
contradictions for me, and log the pass.
````

---

# Part IV — Surfaces

The same protocol runs on every surface; only the mechanics of reaching the files differ. The portable unit
is the **protocol in `SCHEMA.md`**, not any skill file — each surface just needs (a) access to the vault
files and (b) an instruction to read `SCHEMA.md` + `wiki/_conventions.md` and follow them.

## 1. Claude Code (the primary surface)

Nothing to install — the seed vault ships with everything:

- `CLAUDE.md` is auto-loaded whenever Claude Code runs inside the vault folder, and points to `SCHEMA.md`.
- Skills live in `.claude/skills/` (`capture-to-inbox`, `process-inbox`, `maintenance-pass`).
- Slash commands live in `.claude/commands/` (`/capture`, `/process`, `/pull`, `/maintain`).

**Use it two ways:**

1. **Inside the vault** — `cd` into the vault folder and run `claude`. Everything loads automatically. This
   is where you run `/process` and `/maintain`.
2. **Attached to other projects** — make every coding session brain-aware by attaching the vault:
   - Per session: `claude --add-dir "<path-to-vault>"`
   - Per project: add to the project's `.claude/settings.json`:
     ```json
     { "additionalDirectories": ["<path-to-vault>"] }
     ```
   - Globally: add a section to your user-level `~/.claude/CLAUDE.md` telling Claude the brain exists, where
     it lives, and to be "brain-aware": offer to capture durable knowledge at natural stopping points, pull
     from the wiki when a question might be covered, and never run git in the vault. (The SETUP.md interview
     writes this for you.)

## 2. Cowork / Claude Desktop

Cowork has no skill files of its own; it carries the protocol in **Project instructions**.

1. Create a Project pointed at the vault folder.
2. Paste this into the Project's Instructions field:

> This project IS my LLM-maintained knowledge brain (plain markdown in Dropbox). Your job is to build and
> maintain it, not just answer from it.
>
> At the start of any work here, read these vault files and treat them as your binding instructions:
> - `SCHEMA.md` — the full operating protocol (structure, the capture / process / pull / maintain
>   workflows, frontmatter, guardrails). This is authoritative; everything defers to it.
> - `wiki/_conventions.md` — the per-page rules.
> - `CLAUDE.md` — the short summary that points to the above.
>
> Follow whatever those files currently say (they may have changed since you last read them — re-read, don't
> rely on memory). In particular: capture freely to `inbox/` on request or proactively at stopping points;
> compile only on "process"; answer pulls from `wiki/` with citations; never fabricate facts or sources; and
> no git, ever.

The paste block carries no protocol of its own — it just tells Claude to read the spec files in the vault
and follow them. That's deliberate: when the conventions change, every surface stays correct with nothing to
re-sync.

## 3. claude.ai chat (web and phone)

Chat reaches the brain through the **Dropbox connector**:

1. In claude.ai → Settings → Connectors, connect Dropbox (the account that holds the vault).
2. **Pull:** ask "what does my brain say about X?" — Claude reads `wiki/` pages through the connector and
   cites them.
3. **Capture:** if the connector has write access, "capture this to the brain" creates a note in `inbox/`
   directly. Confirm the exact file before it writes; report the created path after.
4. For consistent behavior, create a claude.ai **Project** for brain interactions and put the same
   instruction block from the Cowork section above into its project instructions (with paths as Dropbox
   paths, e.g. `/AI-Brain/SCHEMA.md`).

Chat never runs the process step — moving notes out of `inbox/` needs local disk access. Capture and pull
only.

## 4. Phone

Two options, in order of preference:

- **claude.ai mobile app** with the Dropbox connector (same as web chat): capture and pull from anywhere.
- **Dispatch to the always-on machine**: if you run one (see Part V (Scheduling)), send capture requests to
  a session running there (e.g., Cowork mobile dispatch).

## 5. ChatGPT (optional)

If you also work in ChatGPT, set it up as a *client* of the same brain — see Part VI (ChatGPT). It pulls and
captures through the Dropbox app; it never processes or edits `wiki/`/`raw/`.

## The one rule that spans all surfaces

Every surface re-reads `SCHEMA.md` and `wiki/_conventions.md` before acting on the brain, and treats them as
binding. Memory of the protocol is always stale; the files are always current.

---

# Part V — Scheduling the nightly compile

The brain maintains itself only if the inbox is regularly processed. The recommended setup is a **scheduled
task on an always-on local machine running headless Claude Code**; alternatives follow for other situations.

**The binding constraint:** the process step *moves* notes from `inbox/` into `raw/` — it deletes files from
the local Dropbox vault. So the job must run somewhere with **native disk access to the vault** (Dropbox
folder set to Local / "Make available offline"). Cloud-hosted schedulers cannot see the vault; don't use
them for this.

## Option A (recommended) — OS scheduler + headless Claude Code

An always-on machine (a desktop that stays on, a home server, a mini PC) runs the compile nightly with no
GUI and no app window. This is the most robust option: it survives reboots and needs nothing open.

### The pieces (any OS)

1. **Auth token.** A bare headless `claude -p` subprocess does not inherit the interactive app's login. Run
   `claude setup-token` once — it generates a long-lived OAuth token on your existing Claude subscription
   (no extra billing). Store it in the environment variable `CLAUDE_CODE_OAUTH_TOKEN` for the account the
   task runs as. Note: stored as an env var it sits in plaintext within your OS account's trust boundary.
2. **Wrapper script** that: changes to the vault directory, runs the compile prompt, and appends to a log
   file. The core command:
   ```
   claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions
   ```
   `--permission-mode bypassPermissions` is required — unattended file moves/edits would otherwise stall on
   approval prompts. It is scoped to a vault of your own notes; keep the prompt narrow.
3. **Scheduler entry** that runs the wrapper nightly (2:00 AM is a good default — after your workday, before
   the next).

Failure is non-destructive: if a run errors before doing work, no notes are moved and the inbox is intact —
the next night catches up.

### Windows — Task Scheduler

Wrapper `process-inbox.ps1` (adjust paths):

```powershell
Set-Location "C:\Users\<you>\Dropbox\AI-Brain"
$log = "C:\Users\<you>\.claude\brain\logs\process-$(Get-Date -Format yyyy-MM).log"
"`n===== $(Get-Date -Format s) =====" | Out-File $log -Append -Encoding utf8
& "$env:USERPROFILE\.local\bin\claude.exe" -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions *>> $log
```

Task settings that matter: Daily at 2:00 AM · Action:
`powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "<path>\process-inbox.ps1"`
· **Run only when user is logged on** (Interactive logon, so the user env var with the token is picked up) ·
**Run task as soon as possible after a scheduled start is missed** (`StartWhenAvailable`) · optionally **Wake
the computer to run this task** · stop after 1 hour · do not start a new instance if already running. Set the
token once with `setx CLAUDE_CODE_OAUTH_TOKEN "<token>"`.

### macOS — launchd (or cron)

Wrapper `process-inbox.sh` (make executable, adjust paths):

```bash
#!/bin/bash
export CLAUDE_CODE_OAUTH_TOKEN="<token>"   # or source it from a protected file
cd "$HOME/Dropbox/AI-Brain" || exit 1
LOG="$HOME/.claude/brain/logs/process-$(date +%Y-%m).log"
mkdir -p "$(dirname "$LOG")"
echo -e "\n===== $(date -Iseconds) =====" >> "$LOG"
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions >> "$LOG" 2>&1
```

Schedule with a launchd user agent (`~/Library/LaunchAgents/com.brain.process.plist`) using
`StartCalendarInterval` at Hour 2, Minute 0 — launchd runs missed jobs on wake, which cron does not. Plain
cron (`0 2 * * * /path/to/process-inbox.sh`) also works on any Unix if the machine is reliably awake.

## Option B — Cowork / Claude Desktop scheduled task

If you'd rather stay inside the app: in a Cowork project pointed at the vault, create a scheduled task
("every night at 2:00 AM, process the brain inbox per SCHEMA.md…"). Simpler to set up, but it requires the
desktop app to be open and the machine awake at run time — fine for a desktop you never close, fragile
otherwise.

## Option C — manual cadence (no always-on machine)

The compile doesn't have to be nightly; it has to be *regular*. If you work from a laptop that sleeps:

- **End-of-day habit:** run `/process` in Claude Code (in the vault) at the end of any day you captured
  something. It takes a minute or two for a handful of notes.
- **Reminder-driven:** set a recurring reminder (calendar, todo app) — "process the brain inbox" — daily or
  every few days. When it fires, open the vault in Claude Code and run `/process`.
- **Opportunistic:** whenever a session's Claude notices a non-empty inbox in the vault, it may offer to
  process; accept when convenient.

The inbox is designed to tolerate lag — notes just wait, nothing is lost. What breaks the system is *never*
processing: the wiki stops compounding and pulls go stale. Pick the cadence you'll actually keep.

## Whichever option: verify the loop monthly

Check `wiki/_log.md` occasionally — you should see `process` entries at your expected cadence, and any
`flag` entries are ambiguous notes waiting for your judgment. Silence in the log means the schedule broke
(commonly: expired token, moved vault path, renamed task).

---

# Part VI — ChatGPT (optional)

If you also work in ChatGPT, wire it up as a **client** of the same brain. ChatGPT is not another brain:
ChatGPT saved memory, chat history, project memory, uploaded files, and custom GPT configuration are
convenience only. The durable source of truth remains the markdown files in Dropbox.

The recommended integration is a **private custom GPT named `Brain`** that pulls and captures through the
Dropbox app. It never compiles the inbox and never edits `wiki/` or `raw/` — processing stays with your
local Claude Code / scheduled workflow.

## One-time setup

1. In ChatGPT, connect the **Dropbox app** (Settings → Apps/Connectors) using the account that holds the
   vault.
2. Create a new custom GPT and paste the builder prompt below. Replace `<VAULT>` with your Dropbox vault
   path (e.g. `/AI-Brain`) and `<OWNER>` with your name.
3. Keep the GPT **private**. Do not upload the vault as GPT Knowledge — the live Dropbox files are the
   source of truth, and a Knowledge copy would silently go stale.
4. Invoke it from any conversation with `@Brain` (where supported), or start a chat with it directly.

## Builder prompt

```text
Create a private custom GPT with the following configuration.

NAME
Brain

DESCRIPTION
Pulls trusted context from <OWNER>'s Dropbox brain and captures durable knowledge from ChatGPT
conversations into its inbox without changing the brain's existing rules or compilation workflow.

PRIVACY
Keep this GPT private. Do not publish it to the GPT Store.

TOOLS
Enable Apps and select Dropbox when available.
Do not configure custom Actions.
Do not upload files as GPT Knowledge because the live Dropbox files are the source of truth.
Web search may be enabled, but external research must be clearly distinguished from brain content.
Tell me about any setting that must be completed manually in Configure.

INSTRUCTIONS
You are the ChatGPT client for <OWNER>'s personal Dropbox knowledge brain at `<VAULT>`.

The brain is the markdown file system in Dropbox. You are a client of it, not the brain itself. ChatGPT
memory, project memory, chat history, uploaded knowledge, and earlier model outputs are not durable
sources of truth.

Before any brain operation, use Dropbox to read the current versions of:

1. `<VAULT>/SCHEMA.md`
2. `<VAULT>/wiki/_conventions.md`

Treat those files as binding. Re-read them instead of relying on memory. Use these additional files when
relevant:

- `<VAULT>/PROCESS.md`
- `<VAULT>/wiki/_index.md`
- `<VAULT>/wiki/_log.md`

The current `SCHEMA.md` and `wiki/_conventions.md` override these GPT instructions if they differ.

CORE ROLE
Support two primary operations:

1. Pull trusted context from the brain.
2. Capture durable knowledge from the current conversation into the brain inbox.

Do not take over the existing local compilation or maintenance workflow.

PULL WORKFLOW
Use pull behavior when the user asks to pull from the brain, ask the brain, use existing context, or
review relevant brain context.

For a pull:

1. Read the authoritative rules.
2. Read `<VAULT>/wiki/_index.md` to orient.
3. Search for relevant pages under `<VAULT>/wiki/`.
4. Fetch and read the actual relevant pages, not only search snippets.
5. Answer using the brain's content.
6. Cite the specific Dropbox pages or paths used.
7. State plainly when the brain does not contain enough information.
8. Distinguish brain knowledge, external research, and your own inference.
9. Prefer canonical current pages over duplicated or outdated material.
10. At a natural stopping point, offer once to capture durable new decisions, methods, specifications,
    findings, corrected facts, or rationale.

Do not say something is in the brain merely because it appears in the current chat or ChatGPT memory.

CAPTURE WORKFLOW
Capture only after the user explicitly asks or accepts an offer.

Include durable material such as decisions, methods, specifications, findings, corrected facts, important
rationale, consequential unresolved questions, and exact final wording when requested.

Normally omit greetings, repeated discussion, temporary troubleshooting, abandoned wording, unadopted
speculation, and material already represented accurately in the brain.

For a capture:

1. Read the current capture rules in `SCHEMA.md`.
2. Create exactly one markdown file under `<VAULT>/inbox/`.
3. Name it `YYYY-MM-DD-HHMM-<short-slug>.md`, using the user's current local time.
4. Start with `context: <where this came from and what it concerns>`.
5. Put the durable content below as clean markdown.
6. Preserve exact text when requested.
7. Do not add wiki frontmatter.
8. Do not decide topic, project, identity, tags, lifecycle folder, or final wiki page.
9. Do not edit or create files in `<VAULT>/wiki/`, `<VAULT>/raw/`, or `<VAULT>/outputs/`.
10. Do not update `_index.md` or `_log.md`.
11. Keep capture separate from processing.
12. Request Dropbox approval when required.
13. Claim success only after Dropbox confirms the file was created.
14. Report the exact created path and summarize what was captured.
15. When a write fails, provide the intended filename and complete markdown note so the user can save it
    by hand.

PROCESS AND MAINTENANCE BOUNDARY
The existing local Claude Code / scheduled workflows remain responsible for processing `inbox/`, moving
immutable sources into `raw/`, creating and updating wiki pages, updating `_index.md`, appending to
`_log.md`, and maintenance. A read-only review is allowed. Do not perform modifying process or
maintenance work.

GUARDRAILS
- Do not edit `<VAULT>/raw/`.
- Do not fabricate facts, file contents, citations, or successful writes.
- Do not use git inside `<VAULT>`.
- Do not capture silently.
- Do not maintain a duplicate brain in GPT Knowledge.
- Do not treat ChatGPT memory as more authoritative than Dropbox.
- Do not weaken or rewrite the existing brain rules.
- Use current brain files rather than remembered versions.

RESPONSE STYLE
Be direct and practical. For a pull, lead with the answer and identify the pages used. For a capture,
identify the durable material selected, perform the approved write, and report the exact path. Do not
repeatedly explain the brain architecture unless relevant.

CONVERSATION STARTERS

1. Pull from the brain: what context do I already have on this topic?
2. Review the relevant brain pages before we continue this project.
3. Capture the durable decisions and open questions from this conversation.
4. Compare this new idea against what is already in the brain.

FINAL SETUP CHECK
After configuring the GPT:

1. Confirm that no Knowledge files were uploaded.
2. Confirm that custom Actions are disabled.
3. Confirm that Dropbox is selected under Apps, or give the exact manual step needed.
4. Confirm that the GPT is private.
5. Show the final name, description, conversation starters, and remaining manual settings.
```

## Verify it with three tests

1. **Pull:** `Pull from the brain: summarize what the wiki currently covers and cite the specific pages
   used.` — expect an answer with real Dropbox paths.
2. **Capture:** `Capture this decision to the brain inbox: ChatGPT is a client of the brain, not its source
   of truth.` — expect exactly one new file in `<VAULT>/inbox/` and the exact path reported.
3. **Boundary:** `Process the entire brain inbox and update the wiki now.` — expect a refusal that
   compilation stays with the local/scheduled workflow.

## Day-to-day use

- `@Brain Pull the existing context on <topic> and compare it with what we're discussing here.`
- `@Brain Capture the durable decisions, specifications, rationale, and unresolved questions from this
  conversation.`
- Backfilling old ChatGPT history into the brain is covered in Part VII (Backfilling).

---

# Part VII — Backfilling

A new brain starts empty, but you don't. Backfill is the controlled import of durable knowledge from what
already exists: old AI conversations, exported chat histories, per-tool memory features, project documents,
and your own head.

**Backfill does not introduce a new knowledge path.** It is a coordinated series of ordinary captures:

```
Past conversations / documents / memory
        ↓ review and triage
Approved capture manifest
        ↓ individual captures
      inbox/
        ↓ the normal process step (manual or nightly)
       raw/  →  wiki/
```

Never write historical material directly into `wiki/` or `raw/` — everything enters through the inbox so the
normal process step makes the filing decisions with full conventions in force.

## The golden rule: don't file everything at once

The tempting failure mode is a giant week-one import of everything you've ever discussed with an AI. Resist
it. The brain compounds by ingesting knowledge *as it becomes relevant*: when a topic comes up in real work,
capture what you know, and let processing build the pages. A modest seed plus steady capture beats a huge
stale import every time.

That said, three deliberate backfill passes are worth doing early:

## Pass 1 — the brain-dump interview (recommended first seed)

The fastest way to a useful initial wiki. In a Claude session attached to the vault:

> Interview me to seed my brain. Ask me one domain at a time: what I work on, the projects currently in
> flight, the key decisions already made and why, the methods and specs I reuse, and the facts I keep
> re-explaining to AIs. After each domain, capture what I told you as one or more inbox notes (normal
> capture rules — no filing). Stop when I say done.

Do 20–60 minutes, let the nightly (or a manual `/process`) compile it, then review `wiki/_index.md`. You'll
have a real, cited starter wiki within a day.

## Pass 2 — per-tool memory exports

Your AI tools have been quietly accumulating memory. Harvest it once:

- **claude.ai memory / ChatGPT saved memory:** ask the tool to display everything it remembers about you
  ("show me everything in your memory about me"), paste the output into a backfill conversation, and capture
  the durable parts as inbox notes (source: "ChatGPT saved memory, exported YYYY-MM-DD").
- **Claude Code auto-memory / project memories:** review `~/.claude/projects/*/memory/` files and capture
  the durable, non-code facts.
- Treat these as *claims to verify*, not gospel — memory features accumulate errors. Mark anything doubtful
  as such in the capture note.

## Pass 3 — selected high-value conversations and documents

For the handful of conversations or documents that contain real decisions and specs:

### Mode A — selected-conversation backfill (highest quality)

Open the original conversation (in Claude or ChatGPT with its Brain GPT) and ask:

> Review this conversation for backfill. Identify durable decisions, methods, specifications, findings,
> corrected facts, important rationale, and unresolved questions. Compare against the existing brain, show
> me the proposed capture before writing anything, and capture only what is not already in the brain.

### Mode B — exported-history backfill (bulk review)

For large histories, export first (ChatGPT: Settings → Data Controls → Export Data →
`conversations.json`; Claude: Settings → Privacy → export). Then, in a dedicated backfill session, begin
with a **read-only inventory**:

> Review this exported conversation history for a brain backfill. First produce an inventory only: identify
> conversations likely to contain durable decisions, methods, specifications, findings, corrected facts, or
> consequential unresolved questions. Compare candidates with the current brain. Do not write any files yet.

Split oversized exports by project, date range, or subject before review.

### Mode C — documents and cross-platform material

The same workflow covers project context files, design records, master-context documents, notes from other
LLMs, and collections of markdown. Provide the files, request a read-only inventory, then approve captures.

## The capture manifest (for any sizeable pass)

Before writing anything, have the AI produce a manifest — temporary workflow state, not brain knowledge —
listing per candidate source: title, original date, platform, the durable content spotted, existing brain
coverage (none / partial / covered / conflicting), proposed disposition (capture / skip / merge / review),
proposed note slug, and confidence.

Favor **net-new knowledge**. Skip sources that contain only casual questions, temporary troubleshooting,
repeated explanations, superseded plans with no reusable rationale, material already in the brain, or
AI-generated claims that were never accepted or used. But don't skip a superseded decision whose reversal
contains a reusable lesson — capture it as a corrected/historical decision.

Work in **reviewable batches** (roughly 5–20 related sources), approve each batch explicitly, and have the
AI report at the end of each: sources reviewed, skipped, notes created with exact paths, conflicts left for
you, and the next unreviewed range — so a backfill can pause and resume across sessions.

## Writing backfill notes

Backfill notes are ordinary inbox notes with one extra habit — record the historical source *inside* the
note, and use the **current capture time** in the filename:

```markdown
context: Backfill from ChatGPT conversation "<title>", originally dated YYYY-MM-DD; reviewed and captured YYYY-MM-DD.

<clean durable knowledge — synthesis, not a transcript dump>

## Source reference
- Platform: ChatGPT
- Original title: <conversation title>
- Original date: YYYY-MM-DD
```

Preserve exact wording only when it matters (approved copy, contract language, prompts, naming decisions,
canonical definitions). Otherwise synthesize into concise factual markdown. One conversation usually yields
one note; split only when a source contains clearly independent durable subjects. Backfill never makes final
wiki filing decisions — the normal process step decides whether one capture becomes one page, several, or
updates to existing pages.
