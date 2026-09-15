# Background — why the brain works the way it does

This is the reasoning behind the system. Read it to understand *why* before you build. Nothing here is
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
  real goal, not just the stated task. Work in small reviewable buckets. Force explicit verification of key
  decisions.
- **Verifier** — give the agent a way to *check* its own output against a defined bar. This is the
  highest-ROI layer: define "good" precisely, use a second model as critic, pull external signal (tests,
  linters, reference artifacts).
- **Environment** — the workshop that compounds: always-on rules (a `CLAUDE.md`), a **knowledge base**,
  on-demand **skills** (methods), and deterministic hooks.

The mental model is the **robot librarian**: the model is brilliant when the answer is in its library and
confidently wrong when it isn't. Pleading with it changes nothing — the only levers you actually control are
spec, verifier, and environment. And the principle underneath it all:

> **"You can outsource your thinking, but you can't outsource your understanding."**

**The brain is the knowledge-base layer of that environment.** That is its entire reason for existing. The
protocol documents (`SCHEMA.md`, `_conventions.md`) are its spec. The maintenance pass and the
cite-your-sources rule are its verifiers.

Karpathy also sketched the direct ancestor of this design: an **LLM-maintained markdown wiki** that replaces
RAG at personal scale — the model doesn't retrieve fragments from an index, it *curates* a small, coherent,
linked library it can actually read. The brain implements that idea and extends it across surfaces. The
spiritual ancestor is Vannevar Bush's **Memex** (1945) — with the LLM finally doing the curation Bush
couldn't automate.

The other direct ancestor is the **Data Garden / PlantWave implementation**, a production build of that same
wiki idea. It supplied most of the working parts this design runs on: concept-per-page, the index-versus-log
split, conventions first, immutable sources, the `outputs/` stage, frontmatter for querying, and periodic
maintenance passes. It also used cloud sync rather than git, which this design matches. What follows is an
evolution of that work, and the credit for the parts it contributed stands.

## The adaptations — what this design adds to the base idea

### 1. The inbox split: capture ≠ compile

Capture must be frictionless from anywhere. Compilation must be careful, and it needs a capable local surface.
Splitting them removes the "where does this go?" burden at capture time — nothing is lost to filing friction.
**Capture is frequent and dumb. Processing is periodic and careful. Pulling is whenever.** The trade-off
(knowledge is briefly unfiled until processed) is handled by a nightly compile.

### 2. Brain-as-library: every tool is a client

Claude Code, claude.ai chat, Cowork, even a ChatGPT custom GPT are *clients* that read from and write to the
brain — **none of them is the brain.** The portable unit across surfaces is the **protocol** (in
`SCHEMA.md`), not any tool's skill file or memory feature. Each surface carries the same behavior through
whatever mechanism it has: slash commands, project instructions, or a connector-driven launcher. Because the
binding rules live in the vault itself, every surface stays correct when the conventions change — there is
nothing to re-sync.

### 3. Skills vs knowledge: a verb is not a noun

A **skill** is a reusable *method* ("how to capture") — stateless, loaded on demand. **Knowledge** lives
in the wiki — it persists in files. The skill remembers nothing. The wiki remembers everything. This
separation is what keeps the system coherent as tools change underneath it.

### 4. Identity is metadata, not a folder

If you operate in several contexts (businesses, roles, personal), never file knowledge by context. Much of
the valuable knowledge is cross-cutting. Filing by context would wall it off inside one context's folder or
duplicate it across several. Instead, knowledge is **filed by subject**, and identity is a frontmatter
*filter*. A cross-cutting fact lives exactly once and is filterable — never walled off, never duplicated.

This generalizes to **three independent classification axes, three mechanisms**:
- **Lifecycle** (evergreen / active / done) → folders (`topics/` · `projects/<slug>/` · `archive/`)
- **Identity** (your contexts) → the `identity:` frontmatter field
- **Subject** → tags + wikilinks from a controlled vocabulary (`wiki/_tags.md`)

Keep each axis on its own mechanism and filing is mechanical. Collapse two onto one and filing becomes a
judgment call.

### 5. No git — cloud sync is the versioning layer

Versioning and backup matter, but a git repo imposes cross-surface friction (hooks, push/pull discipline,
repo paths, merge states) that isn't worth it for personal notes. Dropbox provides sync across machines and
file version history for free. **There is no git in the vault, ever.**

Why Dropbox specifically (and not, say, Google Drive): the vault must exist as **real files on local disk**
("Make available offline"), because the process step moves files and a shell/agent session must be able to
mount the folder. A virtual stream drive that materializes files on demand, as Google Drive does by default,
is not reliably mountable by an agent session. Dropbox also has a first-party Claude connector for the chat
surface. Any sync product that (a) mirrors real
files to disk and (b) has a connector your chat surface can read would work. Dropbox is the proven default.

### 6. Immutable sources: the traceability spine

Processed inbox notes are *moved* into `raw/` and never edited again. Every wiki claim traces back to a
frozen source via the `sources:` frontmatter field, so the wiki can always be audited or rebuilt, and the
LLM can never quietly launder a fabricated fact into "established knowledge." Never fabricate facts or
sources. A claim without a source does not go in the wiki.

### 7. The self-sufficient note: a note is filed from its own content

The inbox is fed from every machine and every surface. A note captured on a phone, in a browser tab, or
inside a coding project syncs to the vault, and the compile files it later, somewhere else. **That run can
see only the vault.** It cannot open the repo, the session transcript, or the URL the note came from.

Two rules follow, and they work as a pair.

**At capture time, write the substance itself.** Never write a pointer in place of the content. Cite the repo,
the branch, the transcript, or the URL as provenance **in addition to** the content, never instead of it.
When the capture came from work in another repo, say so in the `context:` line. It is the only breadcrumb
back.

**At process time, file the note from its own content.** If a note points at material the run cannot reach,
file what the note asserts, at the note's own level of confidence, and record the unreachable part as an open
item on the wiki page. That is where open questions belong. "Go fetch the rest" is never a precondition for
filing.

Without this pair, notes that point outward pile up in the inbox forever, waiting for context that will never
arrive. The system looks healthy because nothing errors, and the wiki quietly stops growing.

### 8. Skills compound beside knowledge, in their own library

Adaptation 3 draws the line: a skill is a verb, knowledge is a noun. This one follows the line to its
conclusion. **A repeated method is not a wiki page.** Writing a method into the wiki, then following it by
hand every time, is the wiki doing a job it was never built for.

Working with the brain is what makes the repetition visible. The same method gets explained again. The same
checklist gets rebuilt. The same steps get pasted into a new session. Nowhere else in the owner's tooling is
that pattern in view, so the brain is the right place to **notice it and offer**.

The offer appears where the owner is present and looking for improvement. That is **capture**, when they
have just decided something is worth keeping, and **maintain**, when they are deliberately looking for
things to fix. It never appears during the unattended nightly compile, because nobody is there to answer,
and a scheduled run must not stop to ask a question. The AI offers in one line, after the work finishes. It
never builds without a yes, and it never nags.

Saying yes builds the skill now, on the surface in use, in whatever form that surface installs a method. The
**master always lands in the library**, a folder beside the vault in the same synced storage, holding the
one master copy of each skill. That copy is what lets the method reach other surfaces later.

The honest limit is about reach, and it must not be softened. A skill does not travel the way a wiki page
travels. **Only the Claude account store reaches the chat surfaces with no per-machine step**, and only
pure-instruction skills belong there. Every other store needs an install on each machine. **ChatGPT has no
skill store at all**, so a method reaches ChatGPT as a custom GPT or as instruction text that the owner
refreshes by hand whenever the master changes. The full treatment is in `docs/skills.md`.

### 9. The digest: an interface onto the knowledge, not a record of it

The wiki is written to be **read**. Some knowledge is easier to take in while driving, walking, or away from
a screen, and reading a wiki page aloud does not work — it is dense, full of links and paths, and written
for eyes that can skim back.

So `/digest` writes a different artifact from the same material: a **spoken-word script**, 600 to 900 words,
plus a pre-rendered MP3. It sits in `digests/`, outside the golden flow.

**The line that makes this safe is that a digest is an interface, never a record.** The wiki holds what is
true. A digest holds one explanation of it, shaped for ears. Three rules follow, and each one exists because
the alternative corrupts something:

- **A digest is not a capture.** Durable knowledge still goes to `inbox/`. A spoken restatement is a
  presentation of a source, not a source.
- **Process never reads `digests/`.** Compiling lossy prose back into the wiki would put something that was
  never the source into the source of truth. That is the failure this rule exists to prevent, and it is the
  one that would be hardest to detect afterward.
- **It is never offered proactively.** An offer that fires in normal use is noise, and noise trains the
  owner to ignore the channel.

Digests age out of the root at 60 days into `heard/`, and **nothing is deleted**. That is a deliberate
choice with a real cost: `heard/` grows without bound at roughly two megabytes per digest. The alternative —
deleting after a window — was rejected because a listened-to explanation is sometimes the only place an
argument was ever phrased well, and the system should not throw that away on a timer. An owner who wants a
delete step adds it knowingly.

## Key design decisions, consolidated

| Decision | Why | Trade-off accepted |
|----------|-----|--------------------|
| No git | Cross-surface friction outweighs git's value for personal notes. Dropbox gives sync + history | Lose fine-grained diffs/branching |
| Dropbox, local/offline mode | Real files on disk, mountable by agent sessions. First-party Claude connector | A second cloud account to manage. Local disk space |
| Inbox split (capture ≠ compile) | Frictionless capture from anywhere. Careful compilation locally | Knowledge briefly unfiled until processed |
| Subject, not identity | Cross-cutting knowledge lives once, filterable. Never walled off or duplicated | Must set `identity` correctly at process time |
| Immutable `raw/` | Every wiki claim traces to a frozen source. Auditable and rebuildable | Can't tidy a source after the fact (write a new one) |
| Concept-per-page | Knowledge composes and links cleanly. Avoids document-shaped silos | More pages, more linking discipline |
| LLM owns the wiki | The whole point — the agent curates, the human reviews | Requires trust + periodic maintenance passes |
| Self-sufficient notes | The compile sees only the vault, so a note that points outward is unfileable | Capture takes a few more words than a bare link |
| Library beside the vault, not inside it | A tool is not knowledge. Methods inside a knowledge base blur what the brain is | A second folder to sync and to install on each machine |
| Digests outside the golden flow | A spoken restatement is an interface, not a source. Compiling one into the wiki would corrupt the source of truth | A second place to look, and one the compile deliberately ignores |
| Digests are never deleted | A well-phrased explanation is sometimes the only good phrasing of an argument | `heard/` grows without bound, about two megabytes per digest |
| A versioned kit with migrations | A vault built a year ago can gain new verbs without a reinstall or a rebuild | The kit must ship a tested migration per release, and it must never overwrite an edited file |

## The governance chain

The documents form a deliberate chain from thin-and-always-loaded to deep-and-on-demand:

| Doc | Role |
|-----|------|
| `CLAUDE.md` | Thin, auto-loaded entry point. Points to SCHEMA |
| `SCHEMA.md` | The full binding protocol — the law that governs all reads and writes |
| `PROCESS.md` | Plain-language human handbook |
| `wiki/_conventions.md` | The per-page contract (naming, frontmatter, linking, the three axes) |
| `wiki/_tags.md` | The controlled subject vocabulary |
| `wiki/_index.md` | Catalog — *what exists* |
| `wiki/_log.md` | Append-only journal — *what changed* |
| `digests/_catalog.md` | What there is to listen to — an index onto the wiki, not part of it |
| `.claude/INSTALL.md` | The per-machine runbook: how skills copy from the vault into `~/.claude/` |
| `.claude/VERSION.md` | Which kit version built this vault, and every update applied since |
| `<library>/CONVENTIONS.md` | The skill contract: where a master lives, how far it reaches, provenance, packaging traps, what is not a skill |

Index vs log is an easy thing to confuse: `_index.md` answers "what's in here?", `_log.md` answers "what
happened?".

One principle holds the chain together: **point, don't copy.** A skill file, a project instruction block, or
a custom GPT carries the shape of a job and nothing more. It points at `SCHEMA.md`, `wiki/_conventions.md`,
and `wiki/_tags.md` for the rules, and reads them at run time. Keeping the clients thin means a rule change
edits one file in the vault and reaches every machine and every surface through cloud sync, with no install
step. A client that copies a rule inline goes stale the day the vault changes, and it goes stale silently.

## Guardrails (always true)

- Never edit `raw/`. Sources are immutable.
- Never fabricate facts or sources. Every wiki claim traces to a source.
- Identity is metadata, not a folder. File by subject.
- No cross-domain duplication. Link the canonical page.
- No git in the vault, ever.
- A note is filed from its own content. An unreachable pointer becomes an open item on the page, never a
  reason to hold the note back.
- Never force a bad filing. A note stays in the inbox **only** for a filing-destination ambiguity, never for
  a missing-detail one, and it is flagged in `_log.md` for the human. A note carried more than twice is a
  filing bug, not a safe outcome.
- The AI offers to capture at natural stopping points. It never captures silently and never nags.
- Never compile a digest into the wiki, and never let a digest stand in for a capture. A digest is never
  offered — the owner asks for it.
- An update never costs the owner knowledge. It never overwrites a file they edited, and it never touches
  `wiki/` page content, `inbox/`, `raw/`, `outputs/`, or `digests/`.
