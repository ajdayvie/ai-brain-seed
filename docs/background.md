# Background — why the brain works the way it does

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
