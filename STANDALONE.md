# STANDALONE.md — install an LLM-maintained knowledge brain (single-file edition)

> **Human:** paste this whole document into an AI assistant. A Claude Code session on the machine that
> holds your synced folder is the best place. Then say one of these:
>
> ```
> help me install an AI brain
> ```
>
> The assistant teaches you the system, asks a short set of questions, then builds your vault from the
> templates in Part III and verifies it.
>
> ```
> teach me how the brain works
> ```
>
> The assistant explains the system and writes nothing.
>
> This is the self-contained edition of the **ai-brain-seed** kit, version 0.3.0. Same content, no
> download needed.
>
> **It installs a new brain.** To update one that already exists, use `UPDATES.md` and `migrations/` from
> the repository at <https://github.com/ajdayvie/ai-brain-seed> — those read the vault you already have and
> patch it, which no single-paste file can do.
>
> The kit is extracted from a working brain in daily use since June 2026, so it is a snapshot of something
> running rather than a proposal. It descends from Andrej Karpathy's LLM-wiki idea and agent-environment
> framing, and from the Data Garden / PlantWave implementation of that idea, which supplied
> concept-per-page, the index-versus-log split, conventions first, and immutable sources. Vannevar Bush's
> Memex (1945) is the spiritual ancestor. Part I carries the full reasoning.
>
> Everything below is addressed to the AI.

---

You are installing (or explaining) a **personal LLM-maintained knowledge brain**. The brain is a
plain-markdown knowledge base in a synced folder, reachable from every AI surface the owner uses. The wiki,
not chat history and not model memory, is the durable source of truth.

This document has nine parts.

- **Part I — Background.** The why. Read it first. You cannot install what you do not understand.
- **Part II — The guided intake.** The teach step, the interview, and the build steps. Follow it in order.
- **Part III — Vault file templates.** Every file the vault needs, verbatim, with `{{PLACEHOLDER}}` values.
- **Part IV — Library file templates.** Every file the skill library needs, beside the vault.
- **Part V — Surfaces.** Wiring for Claude Code, Cowork and desktop, claude.ai chat, and ChatGPT.
- **Part VI — The skill library.** How a repeated method becomes a skill, and how far each one reaches.
- **Part VII — Scheduling.** The compile: options A, B, and C, and the fallback policy.
- **Part VIII — ChatGPT** (optional). A private custom GPT as a ChatGPT-side client.
- **Part IX — Backfilling.** Seeding the wiki from existing context.

Read Part I now. Then follow Part II.

---

# Part I — Background

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
refreshes by hand whenever the master changes. The full treatment is in Part VI (The skill library).

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

---

# Part II — The guided intake

> **Standalone note.** This edition ships no folders to copy. Wherever Part II says to copy the seed vault,
> write each file from **Part III** at its stated path instead. Wherever it says to copy the seed library,
> write each file from **Part IV**. Then apply the placeholder replacements. The tree to create is:
>
> ```
> <vault>/
>   SCHEMA.md  CLAUDE.md  PROCESS.md  README.md
>   inbox/.keep   raw/.keep   outputs/.keep
>   wiki/_conventions.md  wiki/_tags.md  wiki/_index.md  wiki/_log.md
>   wiki/topics/.keep  wiki/projects/.keep  wiki/archive/.keep
>   digests/_catalog.md   digests/heard/.keep
>   .claude/INSTALL.md   .claude/VERSION.md
>   .claude/scripts/render-digest.py
>   .claude/skills/capture-to-inbox/SKILL.md
>   .claude/skills/process-inbox/SKILL.md
>   .claude/skills/maintenance-pass/SKILL.md
>   .claude/skills/skill-library/SKILL.md
>   .claude/skills/audio-digest/SKILL.md
>   .claude/skills/brain-update/SKILL.md
>   .claude/commands/capture.md  process.md  pull.md  maintain.md  brain-skill.md
>   .claude/commands/digest.md  brain-update.md
>
> <library>/
>   README.md  CONVENTIONS.md  INSTALL.md  registry.md
>   skills/.keep
>   tools/package-skill.py
> ```
>
> Empty folders get a `.keep` file. Never create a git repo in either folder.

You are installing a **personal LLM-maintained knowledge brain** for the owner. The brain is a
plain-markdown knowledge base in a synced folder, reachable from every AI surface the owner uses. The wiki,
not chat history and not model memory, is the durable source of truth.

This document holds everything you need.

| Path | What it is |
|------|-----------|
| Part I (Background) | The why: the knowledge-loss problem, the method, the design decisions |
| the vault templates in Part III | The vault skeleton, with `{{PLACEHOLDER}}` values you replace |
| the `SCHEMA.md` template in Part III | The operating protocol. Binding in the vault after install. |
| the `.claude/INSTALL.md` template in Part III | The per-machine runbook for installing the Claude Code skills |
| the library templates in Part IV | The skill library skeleton, with `{{PLACEHOLDER}}` values you replace |
| Part V (Surfaces) | Wiring for Claude Code, Cowork and desktop, claude.ai chat, and ChatGPT |
| Part VI (The skill library) | The skill library: the stores, what each one reaches, and the offer behavior |
| Part VII (Scheduling) | The nightly compile: options A, B, and C |
| Part VIII (ChatGPT) | The private custom GPT: builder prompt and preview tests |
| Part IX (Backfilling) | Seeding the wiki from existing context |

Read Part I (Background) before you teach or build. You cannot install what you do not understand.

**This document is for a brain that does not exist yet.** If the owner already has one and wants the newer
features, stop, and use `UPDATES.md` from the kit repository at <https://github.com/ajdayvie/ai-brain-seed> instead. It probes the existing vault, works out its version, and
applies only the migrations the owner approves. Running this intake against a live vault would overwrite
their protocol files.

---

## Mode: teach only

Trigger: the owner says `teach me how the brain works`, or asks to understand the system before any setup.

Explain. Write nothing. Cover, in this order: the problem, the claim, the method behind the design, the
golden flow, the five verbs, the three classification axes, what daily use feels like, and what an install
would ask of them. Answer questions from Part I (Background) and the `SCHEMA.md` template in Part III.

Offer to run the install when they are ready. Do not write a file until they say yes.

---

## Step 1 — teach first, briefly

Do this before you ask the first question. Cover these five points in your own words, one short paragraph
each. Keep the whole thing under about 400 words.

1. **The problem.** Knowledge produced in one AI session evaporates when the session ends. Per-surface
   memory does not travel between surfaces.
2. **The claim.** The wiki the owner owns is the source of truth. Every tool is a client. The files are
   plain markdown in the owner's own storage.
3. **The golden flow.** `inbox/` to `raw/` to `wiki/` to `outputs/`. Capture is fast and makes no filing
   decision. Process compiles the inbox into pages and moves each source note to `raw/`, which is immutable.
4. **The five verbs.** capture, process, pull, maintain, digest. The first four move knowledge. **Digest**
   turns a session into a spoken-word script and an MP3 to listen to later, which is an interface onto the
   knowledge rather than a record of it. `/brain-skill` is separate again: it turns a repeated method into a
   skill that installs to the surfaces the owner uses.
5. **What daily use feels like.** Capture freely from any surface. The compile runs nightly, or on a cadence
   they choose. Pull answers with citations to pages.

Then offer more: "I can go deeper from Part I (Background) before we start." Read from it only if they say
yes. Do not dump the whole background unasked.

---

## Step 2 — prerequisites

State this list and wait until the owner confirms each item. **You must not do any of it for them.** No
account signup, no permission grant, no token generation.

1. **A Dropbox account.** A dedicated account is cleanest. It avoids contention with existing sync usage and
   keeps connector permissions clean. A dedicated folder in an existing account also works.
2. **Dropbox for desktop installed** on this machine, signed in to that account. Install it on the always-on
   machine too, if a different machine will run the nightly compile.
3. **The vault folder set to Local / "Make available offline".** Not online-only. The files must be real on
   disk. Process moves files and cannot work through a virtual stream drive.
4. **A decision on the vault location.** For example `~/Dropbox/AI-Brain`. The default folder name is
   `AI-Brain`.
5. **Optional, for the chat surfaces later:** the Dropbox connector in claude.ai settings, and the Dropbox
   app in ChatGPT.

**NOTE:** any sync product that mirrors real files to disk and offers a first-party connector would work.
Dropbox is the proven default.

---

## Step 3 — the interview

Ask one block at a time. Skip anything the owner already answered.

1. **Owner name.** What name should appear as the approver in `wiki/_conventions.md` and the first `_log.md`
   entry?
2. **Vault path.** Confirm the exact local path. Verify that it exists, that it is writable, and that it
   looks like a real synced folder rather than an online-only placeholder.
3. **Identity vocabulary.** Ask: "What distinct contexts do you operate in? Businesses, employers, roles,
   personal." Build short lowercase slugs, for example `acme | consulting | personal | na`. Always include
   `na`, for knowledge that belongs to no identity, such as the brain's own pages. Two to five values is the
   useful range. A single-context owner can use `personal | na`.
4. **Surfaces.** Ask: "Which assistants do you use? **Claude, ChatGPT, or both?**" Then ask which Claude
   surfaces: Claude Code, Cowork or Claude desktop, claude.ai chat on web and phone. The answer decides which
   parts of step 7 you run.
5. **Library path.** Confirm the local path for the skill library. The default is a sibling of the vault named
   `AI-Skills`, for example `~/Dropbox/AI-Skills`. It sits beside the vault, not inside it, because the brain
   holds knowledge and the library holds methods.
6. **Processing schedule.** Ask: "**Do you have a machine that stays on most nights?**" Then ask whether the
   Claude desktop app usually stays open on that machine. The two answers pick the option in step 8.
7. **Confirm the whole answer set** before you write anything: owner name, vault path, identity list,
   surfaces, library path, and processing option.

---

## Step 4 — build the vault and the library

1. Copy the **contents** of the vault templates in Part III into the vault path. Copy the hidden `.claude/` folder too.
2. Copy the **contents** of the library templates in Part IV into the library path from step 3. The library is a second
   folder, beside the vault, in the same synced storage.
3. **WARNING:** make sure **no `.git` directory travels into the vault or into
   the library**. The vault is git-free forever. Dropbox is the sync and history layer.
4. **Confirm before you overwrite anything** that already exists at the vault path or the library path. List
   the conflicting files and wait for a decision.
5. Replace every placeholder in every copied file, in the vault and in the library.

| Placeholder | Replacement |
|---|---|
| `{{OWNER_NAME}}` | The owner's name, for the conventions page and the first log entry |
| `{{TODAY}}` | Today's date, `YYYY-MM-DD` |
| `{{IDENTITY_VALUES}}` | The pipe-separated identity list, for example `acme \| personal \| na` |
| `{{IDENTITY_VALUES_SLASH}}` | The same list, slash-separated, for example `acme / personal / na` |
| `{{VAULT_PATH}}` | The vault's absolute path on this machine |
| `{{SKILLS_PATH}}` | The library's absolute path on this machine |
| `{{SKILLS_DIRNAME}}` | The library folder's name, default `AI-Skills`. Vault files use it to resolve the library as a sibling. |
| `{{NIGHTLY_METHOD_SUMMARY}}` | One or two sentences naming the chosen processing option, for `SCHEMA.md` §8 |
| `{{NIGHTLY_METHOD_DETAIL}}` | A short paragraph with the concrete setup, for `PROCESS.md` |

You choose the two nightly values in step 8. Come back and fill them in if the option is still open now.

6. Verify the replacement across **both** folders. `grep -r "{{" <vault>` must return nothing, and
   `grep -r "{{" <library>` must return nothing. Fix anything either one finds before you go on.

---

## Step 5 — install the Claude Code skills

The vault's `.claude/` folder is the source of truth for the skills and the slash commands. Cloud sync
carries it to every machine. Each machine gets an installed copy under `~/.claude/`. The install covers
**6 skills** (`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`, `audio-digest`,
`brain-update`) and **7 commands** (`/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`,
`/digest`, `/brain-update`).

`.claude/scripts/` is not copied. The `audio-digest` skill calls `render-digest.py` at its vault path, so
it lives in one place.

Read `<vault>/.claude/INSTALL.md` and follow it on this machine. It covers the copy commands for Windows and
for macOS and Linux, the optional drift check, and how to verify the install.

Two points from that runbook that you must get right.

- **Set `BRAIN_DIR`** to the vault's absolute path, in `~/.claude/settings.json` under `env`. The skills read
  it, so they resolve the vault from any project directory. Without it, a skill falls back to searching the
  session's directories for one that holds both `SCHEMA.md` and a `wiki/` folder. That fallback works inside
  the vault and fails outside it.
- **Never edit the installed copy** under `~/.claude/`. An edit there is invisible to other machines and is
  destroyed on the next install. Change the vault copy and reinstall.

A protocol change needs no reinstall. Editing `SCHEMA.md` reaches every machine and every surface through
cloud sync. Reinstall only when a skill file itself changes.

**One optional dependency: `edge-tts`, for the `/digest` MP3.** Tell the owner the command
(`pip install edge-tts`) and let them run it. **Do not install software on their machine.** It is free and
needs no API key. Without it `/digest` still writes the script and sets `audio: none` — the markdown is the
artifact, the MP3 is a convenience. FFmpeg is optional on top of that: `ffprobe` is what measures the real
runtime, and without it the runtime is recorded as unknown rather than guessed.

**Also fill in `<vault>/.claude/VERSION.md`.** It records the seed version this vault was built from, and
`/brain-update` reads it later to work out what is missing. Set `seed-version:` from the kit's `VERSION`
file, and `installed:` to today.

**The library is a second, separate install.** Its runbook is `<library>/INSTALL.md`. Do not run it now. The
library's `skills/` folder ships empty, so on day one there is nothing to install from it.
`/brain-skill install` runs that runbook later, once the owner has built a skill. You may set `SKILLS_DIR` to the library path in
`~/.claude/settings.json` under `env`. When `SKILLS_DIR` is unset, the skills resolve the library as the
sibling of `BRAIN_DIR` named `AI-Skills`.

---

## Step 6 — first-run verification

Run the loop once, end to end, from a Claude Code session inside the vault. **Do not skip this step.** This
loop is the whole system.

1. **Capture.** Say: "capture this: the brain was installed today from ai-brain-seed". Confirm that one
   timestamped note lands in `inbox/`.
2. **Process.** Run `/process`. Confirm that a wiki page is built with valid frontmatter, that the note moved
   to `raw/`, and that `_index.md` and `_log.md` are updated.
3. **Pull.** Ask: "when was this brain installed?" Confirm that the answer cites the new page.
4. **Digest**, only if the owner installed `edge-tts`. Run `/digest`. Confirm that one script lands in
   `digests/`, that an MP3 sits beside it, that `_catalog.md` gained a line, and that the reply was **one
   line**. Delete the test digest afterward and say that you did.

If a step fails, fix the cause before you go on.

---

## Step 7 — connect the surfaces

Run only the parts the owner named in step 3. Each part is detailed in Part V (Surfaces).

a. **Claude Code, everywhere.** Offer to add a brain-awareness block to the owner's user-level
   `~/.claude/CLAUDE.md`: the vault location, capture-offer behavior, pull behavior, and the rule that no
   session runs git in the vault. Add the vault to `additionalDirectories` for the projects they name.

b. **Cowork or Claude desktop.** Walk them through creating a Project pointed at the vault and pasting the
   instruction block from Part V (Surfaces).

c. **claude.ai chat, web and phone.** Have the owner connect the Dropbox connector, then test one pull and
   one capture. This surface does capture and pull. It cannot process, because moving a note out of `inbox/`
   needs real disk access.

d. **ChatGPT.** Hand them the builder prompt from Part VIII (ChatGPT), with the `<VAULT>`, `<LIBRARY>`, and
   `<OWNER>` placeholders filled in. `<LIBRARY>` is the library path as Dropbox sees it. They create a
   **private custom GPT** named `Brain` with the Dropbox app enabled, and the app must reach both folders.
   Then run the preview tests in that document. **Never upload vault or library files as GPT Knowledge.** A
   second copy goes stale the day the source changes.

The rule that spans every surface: **point, don't copy.** The client instructions carry the workflow
skeleton. The rules are read from the vault at run time.

---

## Step 8 — set up processing

Processing should run nightly. Pick the option that matches the step 3 answers. Then set the two nightly
placeholders from step 4 to match. Part VII (Scheduling) holds the full recipes.

- **Option A — a scheduled task in the Claude desktop app**, on a Cowork project pointed at the vault. Use
  this when the app runs on a machine that stays on. **NOTE:** if the app is closed when the task is due, the
  run happens at next launch, not on time.
- **Option B — an OS scheduler plus headless Claude Code (`claude -p`)**. This survives reboots and needs no
  app window. **WARNING:** a headless run does not inherit the interactive login, and it prefers
  `ANTHROPIC_API_KEY` over a subscription session. The owner runs `claude setup-token` once and stores the
  result in `CLAUDE_CODE_OAUTH_TOKEN` for the account the task runs as. You must not generate that token for
  them. A wrong auth path here is the most common reason this option fails silently.
- **Option C — a manual cadence.** Use this when the owner has **no always-on machine**. The compile does not
  have to be nightly. It has to be regular.

### The Option C fallback policy

When the owner picks Option C, or answered "no always-on machine" in step 3, set up all four parts.

1. **Once a day, at the end of any day they captured something.** Run `/process` in the vault. A handful of
   notes takes a minute or two.
2. **Whenever the inbox gets large.** The rule of thumb is **10 or more notes, or any note older than 3
   days.** Process then, whatever the day.
3. **A recurring reminder** in a calendar or a task app, so part 1 does not depend on memory. Help the owner
   create it now and confirm that it exists.
4. **A session-start nudge.** Tell the owner they can ask any brain-aware session to check the inbox size and
   offer to process when it crosses the threshold.

State the failure mode plainly. The inbox tolerates lag, and nothing is lost while notes wait. What breaks
the system is **never** processing. The wiki stops growing and pulls go stale.

---

## Step 9 — explain the skill offer

Write nothing in this step. Explain it, and answer questions.

The brain holds knowledge. A repeated method is not knowledge, it is a **skill**. Tell the owner when the AI
offers one, and what a yes does.

1. **When it offers.** When the owner captures something that is a method they will run again, and during a
   maintenance pass. **It does not offer during the nightly compile**, because nobody is there to answer.
   The offer is one line, after the work finishes, once per candidate per session. It offers, it does not
   nag.
2. **What counts. The bar is high on purpose, so they are not asked about every note.** Two gates must both
   hold: they will run the method again, **and** it is worth a maintained artifact. Only three kinds clear
   the second gate, and the offer names which one — a **business process** they run, a **personalization** of
   how they want work done, or a **way of working with AI** they repeat. Minor process detail does not
   qualify. When it is a close call, the AI stays silent.
   - A note on **how they set up every project spreadsheet, in their standard layout** is a personalization
     they repeat. **The AI offers.**
   - A note on **the steps that fixed one broken build last week** is steps, but a one-off. **It stays
     silent.**
   - A note on **what an article about giraffes said** is knowledge. **It stays silent.**
3. **What a yes does.** It builds the skill now, on the surface in use. There is no queue and no second
   command. **The master always goes to the library**, at `<library>/skills/<name>/SKILL.md`, with a row in
   `<library>/registry.md`. The master is what lets the method reach other surfaces later.
4. **Nothing is built without a yes.** A declined candidate is recorded in `<library>/registry.md` with its
   reason, and is not raised again.
5. **`/brain-skill` with no argument sweeps on demand**, when the owner asks for it.

**If the owner uses ChatGPT**, tell them their equivalent of installing a skill is a **custom GPT** built
from a generated builder prompt, or the method added to an existing GPT's or Project's instructions. **The
`Brain` GPT carries the same flow.** It offers on a capture, and on a yes it writes the master to the library
and prints the one artifact to paste. Part VIII (ChatGPT) holds the builder prompt and the preview tests.

Point the owner at Part VI (The skill library) for the full concept: the stores, and what each one reaches. State these
limits plainly.

- Only the Claude account store reaches the Claude chat surfaces with no per-machine step.
- **ChatGPT has no skill store.** A method reaches ChatGPT as a custom GPT, or as instruction text inside an
  existing GPT or Project. Either one is a copy the owner refreshes by hand when the master changes.
- **A custom GPT is account-wide the moment it is created**, with no per-machine install. But **the owner
  picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its description,
  on demand. ChatGPT has no equivalent to that.

---

## Step 10 — backfill

A new brain starts empty. The owner does not.

Offer the **brain-dump interview** from Part IX (Backfilling) right now, if the owner has 20 minutes. It is
the fastest route to a useful first wiki. Then point them at the other passes in that document: per-tool
memory exports, and selected high-value conversations and documents.

Every backfill pass is a series of ordinary captures into `inbox/`. Never write historical material straight
into `wiki/` or `raw/`.

Tell them the rule: a modest seed plus steady capture beats a large stale import.

---

## Step 11 — handoff

Close by telling the owner, in plain language:

- Where the vault is, and where the library is.
- The five verbs, and how to invoke each one on each surface they set up.
- That `/digest` writes a spoken-word script and an MP3 to `digests/`, that it is **not** a capture, that
  the compile never reads that folder, and that it is never offered — they ask for it.
- That the kit keeps changing, and **`/brain-update`** checks for newer versions and applies only what they
  approve. Nothing expires. Their version is recorded in `.claude/VERSION.md`.
- That the AI offers to build a skill when a capture is a repeatable method, and during a maintenance pass,
  and that nothing is built without their yes. `/brain-skill` sweeps for one on demand.
- When the compile runs, or when their reminder fires.
- To check `wiki/_log.md` now and then for `flag` entries that await their judgment.
- To read `PROCESS.md` in the vault. It is their handbook.
- That they can open the vault in Obsidian, or any markdown editor, to browse it.

---

## Rules that bind YOU during setup

- **Never run git inside the vault.** Never leave a `.git` folder there.
- **Never fabricate a fact or a source** anywhere in the vault. The log's first entry records only what
  actually happened.
- **Never do account signups, permission grants, or token generation for the owner.** Instruct, verify, then
  proceed.
- **Confirm before you overwrite anything** that already exists at the vault path.
- **Do not write any file** until the owner confirms the vault path in step 3.
- After setup, the vault's own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol. That holds
  for you, in every future session.

---

# Part III — Vault file templates

Write each file at the stated path, relative to the vault root, verbatim. Then apply the
placeholder replacements from Part II, step 4.

## File: `SCHEMA.md`

````markdown
# SCHEMA.md — operating manual for the brain (Dropbox, git-free)

Read this file in full at the start of every session, together with `wiki/_conventions.md`. It is binding
until the owner changes it. When the owner changes it, update this file, `wiki/_conventions.md`, and
`PROCESS.md` together.

## 1. What this is

A personal LLM-maintained knowledge base in plain markdown. It lives in a cloud-synced folder, so every
surface can reach it. **The wiki is the durable source of truth**, not chat history and not model memory.

## 2. Store and sync

The vault lives in a Dropbox folder, mirrored to local disk. Set the vault folder to **Local / "Make
available offline"**, not online-only. The files must be real on disk, so a shell session can read and write
them. Dropbox handles sync across machines and version history.

Dropbox is the proven default. It mirrors real files to disk and it has a first-party connector for the chat
surfaces. Any sync product that does both would work.

**There is no git in this vault. Never create or use a git repo here.**

## 3. Structure and the golden flow

`inbox/` -> `raw/` -> `wiki/` -> `outputs/`

- `inbox/` — timestamped notes from any surface, waiting to be processed.
- `raw/` — immutable source material, grouped loosely by topic. Processed notes move here.
- `wiki/topics/` — evergreen knowledge by subject. Keep it flat. Nest only when a cluster grows.
- `wiki/projects/<slug>/` — active work. It pulls from topics. Move the learning back to topics when the work ends.
- `wiki/archive/` — finished or dormant projects.
- `outputs/<project>/drafts/` then `outputs/<project>/` — deliverables. Code outputs go in their own repo, not here.
- `digests/` — **volatile.** Spoken-word audio digests, a script plus a pre-rendered MP3, written for
  listening on the go. Not knowledge, not a source, not a deliverable: an *interface*. See §6f. It sits
  outside the golden flow on purpose. `/process` never reads it, and nothing in it is immutable.

## 4. Identity is metadata

Never file by identity, whether that identity is a business, a role, or a context. Use the frontmatter field
`identity: {{IDENTITY_VALUES}}`. A cross-cutting fact lives once, usually in `topics/`. Filter it by tags and
identity. Never duplicate it per identity.

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

Classification runs on three independent axes. **Lifecycle** uses folders: `topics/`, `projects/`, `archive/`.
**Identity** uses the `identity:` field. **Subject** uses `tags:` plus wikilinks from `wiki/_tags.md`.

Each axis uses one mechanism. Never make folders carry subject. Never make tags carry status, type, or
identity. The full rule is in `wiki/_conventions.md`.

## 6. Workflows

### 6a. CAPTURE (anything -> inbox)  [skill: capture-to-inbox]

Triggered by "capture this", by `/capture`, or by an offer the owner accepts.

1. Take the content: the text the owner gives, or the durable knowledge from the current session.
2. Write ONE note to `inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md`. Start it with a single `context:`
   line saying where it came from and what it is about. The content follows as clean markdown. No
   frontmatter.
3. **Make the note self-sufficient.** The note will be filed later, on a different machine, by a run that can
   see only the vault. Write down the substance itself. Do not write a pointer to a repo, a branch, a
   transcript, or a URL that only this machine can reach. Cite those as provenance **in addition to** the
   content, never instead of it. When the capture came from work in another repo, say so in the `context:`
   line. It is the only breadcrumb back.
4. Do NOT file the note into the wiki. Do NOT make a filing decision. Capture is dumb and fast on purpose.
5. Confirm what was captured and echo the full path.

### 6b. PROCESS (inbox -> wiki)  [skill: process-inbox]

Triggered by `/process`, by "process the inbox", or by the scheduled nightly run. Run it on a surface with
native disk access to the vault. Step 3 deletes the note from `inbox/`, and that needs real disk access.

1. Read each note in `inbox/`.
2. Compile it into the wiki: concept-per-page (one note may yield several pages), the right topic or project,
   full frontmatter with `identity` set, wikilinks to existing pages, no cross-domain duplication.
3. Move the source note from `inbox/` into `raw/<topic>/`. It becomes the immutable source. Set the wiki
   page's `sources:` to that path.
4. Update `wiki/_index.md` (the catalog) and append to `wiki/_log.md`.
5. **A note is filed from its own content.** The inbox is fed from every machine and surface. The note that
   arrives *is* the source, and process needs nothing but the vault to file it. If a note points at material
   the run cannot reach (a repo on another machine, a session transcript, a URL), **file what the note
   asserts, at the note's own level of confidence, and record the unreachable part as an open item on the
   wiki page.** That is where open questions belong. Never treat "go fetch the rest" as a precondition for
   filing. Never carry a note forward because a pointer in it is unresolvable.
6. Leave a note in `inbox/` **only** when you genuinely cannot tell *where it belongs*. That is a
   filing-destination ambiguity, not a missing-detail one. Then add a `flag` line to `_log.md`. Never force a
   bad filing. Equally, never let an unreachable pointer strand a note that has real content. A note carried
   more than twice is a bug in the filing, not a safe outcome.
7. Report what you filed and what you left.
8. **Never read `digests/`.** A digest is a lossy spoken restatement written for ears. Compiling one into
   the wiki would put prose that was never the source into the source of truth. If a digest holds something
   durable that was never captured, the fix is a real capture note per §6a, not a filing of the digest.

### 6c. PULL (query the brain)  [command: /pull]

Answer from the wiki and cite the specific pages. If the wiki does not cover it, say so. If the answer is
durable, offer to capture it.

### 6d. MAINTAIN (lint)  [skill: maintenance-pass]

Triggered by `/maintain` or by "run a maintenance pass". Scan for broken wikilinks, orphan pages,
contradictions, stale pages, off-vocabulary tags, and invalid frontmatter. Report the findings, apply safe
fixes, list the contradictions for the owner to decide, and append a `maintenance` entry to `_log.md`.

**Maintain also owns digest retention.** Move any file in the `digests/` root older than **60 days** into
`digests/heard/`, markdown and MP3 together. **Nothing is deleted.** This is a file move by age, not a read:
the lint checks in this section never open a digest and never judge its content.

### 6e. SKILL (a repeatable method -> a skill)  [skill: skill-library]

Triggered by `/brain-skill`, by "build a skill", or by an offer the owner accepts. The brain holds knowledge.
A repeatable method is not knowledge, it is a skill, and it lives in the **library** described in §12.

Three modes:

1. **`/brain-skill` with no argument** — sweep. Read `<library>/registry.md` first, so a declined skill is
   not proposed again. Then scan recent wiki pages and recent `_log.md` entries for a repeatable method the
   owner still runs by hand. Propose each one, one offer each. Build nothing without a yes.
2. **`/brain-skill build <name>`, or a yes to an offer** — build it now, on the surface the session is on.
   Write the master to `<library>/skills/<name>/SKILL.md`. Write `<library>/skills/<name>.BUILD.md` beside
   the folder and never inside it. Add a row to `<library>/registry.md`. Install it in the form this surface
   supports. Append an entry to `wiki/_log.md`. Then report what was installed and what the owner must still
   do by hand.
3. **`/brain-skill install`** — install the library on this machine per `<library>/INSTALL.md`, then report
   which skill reaches which surface, and name anything that is a master with no install.

**Resolving the library path.** Read the `SKILLS_DIR` environment variable first. If it is unset, use the
sibling of `BRAIN_DIR` named `{{SKILLS_DIRNAME}}`. **Never write a bare relative path.** If neither resolves
to a folder holding `registry.md`, say so and stop. Do not create a library without a yes.

**A yes builds now.** There is no inbox note, no queue, and no second command. The owner is present and has
said yes. **There is no candidates page.** `<library>/registry.md` records what was built and what was
declined, and a declined row carries the reason.

Read `<library>/CONVENTIONS.md` for where a master lives and how far a skill reaches. This file does not
restate it.

### 6f. DIGEST (a session -> a listenable script and an MP3)  [skill: audio-digest]

Triggered by `/digest`, by "make an audio digest", or by "record that for the car". **Never offered
proactively.** An offer that fires in normal operation is noise, and it trains the owner to ignore the
channel.

**A digest is an interface, never a record.** The wiki holds what is true. A digest holds one explanation of
it, shaped for ears, that ages out. It is **not** a capture — durable knowledge still goes to `inbox/` via
§6a, separately, and only if the owner asks.

1. Take the substantive content of the session: the reasoning, the trade-offs, and the numbers. **Not a list
   of what happened.** A summary says "we decided X". A digest explains what X is and why it beat Y, slowly
   enough to follow with your eyes on the road. Pick 2 to 4 ideas and teach them properly.
2. Write a **spoken-word script**, 600 to 900 words, to `digests/YYYY-MM-DD-HHMM-<slug>.md`. No bullets,
   tables, headings, links, file paths, or code identifiers in the body. Numbers said in words. Internal
   scaffolding — agent names, branches, tool names — stripped. The footing of every claim said out loud.
   The full spec is in the skill.
3. Render the MP3 beside it with `.claude/scripts/render-digest.py` (edge-tts: free, no API key, needs a
   network connection). Record the **measured** runtime in frontmatter, never an estimate. If the render
   fails, set `audio: none` and carry on. The markdown is the artifact.
4. Append one line to `digests/_catalog.md`, written for how the owner would ask for it out loud.
5. Reply with **one line** and stop. No preview, no summary, no follow-up. The whole point is not
   interrupting the session.

**Retention:** the `digests/` root moves to `heard/` at 60 days, and then it is kept. **Nothing is deleted.**
`/maintain` does the move (§6d). The skill itself never moves and never deletes anything.

**Playback:** open the file and read the body aloud **verbatim, from the marker comment** — never summarize
it. That instruction lives inside the file because claude.ai and Claude desktop discard the MCP
`instructions` field, and connector review forbids behavioral steering in a tool description. The file is the
only channel that reliably reaches a phone. For hands-free, play the MP3 from the sync app.

## 7. Index and log

- `wiki/_index.md` — the catalog. Every page, its link, and a one-line summary. It answers "what exists".
- `wiki/_log.md` — the append-only journal. One entry per change, written as
  `## [YYYY-MM-DD] <type> | <description>`. Types: capture, process, wiki, draft, final, conventions,
  maintenance, flag. It answers "what changed".

## 8. The nightly compile

{{NIGHTLY_METHOD_SUMMARY}}

**A scheduled run is treated exactly like a manual `/process`.** It follows §6b step by step, including step
6: it leaves genuinely ambiguous notes in `inbox/` and flags them in `_log.md`. See `PROCESS.md` for the
concrete setup on this machine.

## 9. Capture-prompting behavior

Offer to capture at the end of a session, and whenever durable knowledge appears: a decision, a method, a
spec, a finding, or a corrected fact. Offer, do not nag. Capture on the owner's yes. Never capture silently.

**Offering a skill.** The offer fires at **two moments only**. On **capture**, because the owner is present
and has just decided something is worth keeping. On **maintain**, because the owner is deliberately looking
for improvements, which is where a sweep belongs. **Never at process.** Process runs nightly and unattended,
so an offer there is never seen. A scheduled run must not ask a question. **Never at pull.** Pull answers a
question, and an offer there interrupts the answer. The third way in is `/brain-skill` with no argument,
which sweeps on demand.

**The signal is a judgment, not a count. The bar is high on purpose.**

Two things must both be true. A method that clears only the first one is not a candidate.

> **1. It is a method the owner will run again.**
> **2. It is worth a maintained artifact.**

A skill is a real cost. It is a file someone keeps current, installs on each surface, and stops from going
stale. Most captured steps are not worth that. **Do not offer for minor process detail.**

Gate 2 is met when the method is one of three kinds. **Name the kind in the offer.** If you cannot name one,
do not offer.

- **A business process the owner runs** — how they quote, onboard, review, invoice, or ship.
- **A personalization** — how they want work done: their standards, their format, their voice.
- **A way of working with AI that they repeat** and that saves them time.

**When in doubt, stay silent.** The two costs are not equal. A missed candidate is recoverable, because
`/brain-skill` sweeps for it later. A wrong offer is an interruption that cannot be taken back.

Do not offer when the content is a fact, a finding, a reference, a decision, or a corrected claim. Those are
knowledge, a decision included, which can feel active but records what was chosen rather than how to do
something. Do not offer for one-off troubleshooting, for a setup done once for one machine or one artifact,
or for a short sequence with no judgment in it that any assistant would get right without a skill. Stay
silent when `<library>/registry.md` shows the owner already declined it.

Three examples that fix the line:

- A note on **how the owner sets up every project spreadsheet, in their standard layout** is a
  personalization they repeat. **Offer.**
- A note on **the steps that fixed one broken build last week** is written as steps, but it is a one-off.
  **Say nothing.**
- A note on **what an article about giraffes said** is knowledge, not a method. **Say nothing.**

The rules on the offer are strict. One offer per candidate per session. The offer is **one line**, after the
work finishes, and it never blocks or delays the capture. **Never build a skill without a yes, and never
write into the library without a yes.** A declined candidate is recorded in `<library>/registry.md` and is
not raised again. Offer, do not nag. It is the same discipline as capture prompting.

A yes builds the skill now, on the surface the session is on. See §6e.

## 10. Cross-surface

One rule holds on every surface: **point, don't copy.** The client instructions carry the workflow skeleton.
The rules are read from the vault at run time. A client that copies a rule inline goes stale the day the
vault changes.

| Surface | Mechanism | Verbs |
|---|---|---|
| Claude Code (local) | Skills and slash commands in `<vault>/.claude/`, installed by copy into `~/.claude/` | capture, process, pull, maintain, digest |
| Cowork / Claude desktop | A Project pointed at the vault, carrying a short instruction block | capture, process, pull |
| claude.ai chat, web and phone | Dropbox connector, plus the same instruction block in a Project | capture, pull |
| ChatGPT | A private custom GPT named `Brain` with the Dropbox app enabled | capture, pull, and process only with an approved plan |

- **Claude Code** is the primary surface. It owns process and maintain. Attach the vault to a session in
  another project with `--add-dir <vault path>`, or with `additionalDirectories` in that project's settings.
- **Cowork / Claude desktop** can run the scheduled nightly compile.
- **claude.ai chat** has no process verb. Moving a note out of `inbox/` needs real disk access.
- **ChatGPT** may run process only after it presents a complete mutation plan and the owner approves it. The
  plan lists pages to create or update, lifecycle folder, identity, tags, links, source-note moves into
  `raw/`, `_index.md` changes, `_log.md` entries, and anything left in the inbox with the reason. Local
  processing and the nightly run stay the normal path. Never upload vault files as GPT Knowledge.

**Skill reach is not the same as page reach.** A wiki page reaches every surface that can read the vault. A
skill reaches only the surfaces its store serves, and there are four stores. `<library>/CONVENTIONS.md` holds
that table and is authoritative. Read it there rather than restating it from memory.

**ChatGPT has no skill store.** The unit there is a **custom GPT**, built from the master, or the method
added to an existing GPT's or a Project's instructions. A custom GPT is account-wide the moment it is
created, so it needs no per-machine install and no bundle upload. **The owner picks the GPT. The model does
not select it.** A Claude skill is chosen by the model from its description, on demand. ChatGPT has no
equivalent to that, so a method in a custom GPT is reached by naming it. Either artifact is a copy of the
master, and the owner refreshes it by hand.

## 11. Guardrails

- Never edit `raw/`. Never fabricate a fact or a source.
- Never duplicate a cross-cutting fact across topics or projects. Link the canonical page.
- Never invent a tag. Propose an addition to `wiki/_tags.md` instead.
- Never compile a digest into the wiki, and never let a digest stand in for a capture (§6f).
- Never run git in this vault.

## 12. Skills and install

The seven commands and the six skills live in `<vault>/.claude/`. **That copy is the source of truth.** Each
machine installs them by copy into `~/.claude/`. Never edit the installed copy. An edit there is invisible to
every other machine, and the next install destroys it.

The skills are thin on purpose. They carry the job skeleton and the vault-resolution logic. They point at
`SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the rules. They never copy a rule inline.

**A protocol change needs no install.** Edit `SCHEMA.md` and every machine and every surface picks it up
through sync. Reinstall only when a skill file itself changes.

The runbook is `.claude/INSTALL.md`. It carries the copy commands, the `BRAIN_DIR` setting, an optional drift
check, and how to verify.

### The skill library

Skills that do not require the brain live in a **library**, a sibling folder of the vault in the same synced
storage, named `{{SKILLS_DIRNAME}}`. The vault holds knowledge. The library holds methods.

**Where a master lives, and how far a skill reaches, are set by `<library>/CONVENTIONS.md`.** Read the rule
there. This file does not restate it.

**A skill lives in exactly one store.** Four stores in the system is fine. Two copies of one skill is the
bug. When the same name exists in two stores, both load, and which one wins is ambiguous. Nothing reports
this.

The six brain skills — `capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`,
`audio-digest`, and `brain-update` — stay in the vault. They require the brain to exist, and **the vault
must stay self-installing**. Point a session at `<vault>/.claude/INSTALL.md` and the brain works.

`<library>/CONVENTIONS.md` is the binding contract for the library: where a master lives, how far a skill
reaches, the four stores, provenance, packaging, and what is not a skill. `<library>/INSTALL.md` is the
per-machine install runbook for the library, and it is a **second install, separate from this vault's
`.claude/INSTALL.md`**.

## 13. Updating this vault  [skill: brain-update]

This vault was built from a version of the **ai-brain-seed** kit, and the kit keeps changing. The version is
recorded in `.claude/VERSION.md`, together with every update applied since.

Triggered by `/brain-update`, or by "check my brain for updates". **Never offered proactively**, and never
run on a schedule. An update is the owner's choice.

1. Fetch the kit into a scratch folder **outside this vault**, or use a clone the session already has.
2. Read the kit's `UPDATES.md` and follow it. That runbook is authoritative for the whole job: it works out
   this vault's version, picks the migrations, and holds the safety contract.
3. Apply only the migrations the owner says yes to, in ascending order, one at a time.
4. Reinstall the `~/.claude/` copies on this machine, and name the owner's other machines as a to-do.
5. Record the result in `.claude/VERSION.md` and append a `maintenance` line to `wiki/_log.md`.

**Three rules bind every update.** Never run git in this vault, and never leave a `.git` folder here — clone
the kit somewhere else. Never overwrite a file the owner has edited: a migration edits by anchor, and a
missing anchor stops the step rather than guessing a location. Never touch `wiki/` page content, `inbox/`,
`raw/`, `outputs/`, `digests/`, or the library's `skills/`.

**Nothing expires.** A vault that stays at its installed version keeps working.
````

## File: `CLAUDE.md`

````markdown
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
````

## File: `PROCESS.md`

````markdown
# PROCESS.md — human handbook

How to use the brain day to day. The machine-facing protocol lives in `SCHEMA.md`. This is the plain-language
companion.

## The daily loop

Capture freely as you work. Any decision, method, spec, finding, or corrected fact goes to `inbox/` with no
filing. Do not stop to organize.

Once a day, or on the nightly schedule, the inbox is **processed**. Each note is compiled into the wiki, its
source moves into `raw/`, and the index and log are updated.

When you need to know something, **pull** from the wiki. The answer comes back with citations to the pages
it used.

Capture is frequent and dumb. Process is periodic and careful. Pull is whenever.

## Capturing from each surface

| Surface | How you capture |
|---|---|
| Claude Code (local) | Say "capture this" or run `/capture`. The note lands in `inbox/`. |
| Cowork / Claude desktop | A Project pointed at the vault. Say "capture this to the brain". |
| claude.ai chat, web and phone | With the Dropbox connector connected, say "capture this to the brain". Chat writes the note into `inbox/`. |
| ChatGPT | A private custom GPT named `Brain` with the Dropbox app enabled. Say "capture this". |

On every surface the note is only dropped in the inbox. Filing happens later, at process time.

**One capture, one note.** An explicit "capture this", or an accepted offer, is all the authorization the
assistant needs to write that one note. It does not authorize anything else.

## Notes are filed from their own content

This is the rule that keeps the inbox from silting up. **Write the substance into the note, not a pointer to
it.**

You capture on a phone or on a laptop. The note syncs to the vault. The nightly run then files it using only
the vault, on a machine that cannot see the repo, the transcript, or the tab you were looking at.

So if a note references something the run cannot reach, the run still files what the note says, at the note's
own level of confidence. The missing part is recorded as an open item **on the wiki page**, which is where
open questions belong. The note is not left sitting in the inbox waiting for context that will never arrive.

Notes stay in the inbox, flagged in `_log.md`, only when it is genuinely unclear *where* they belong. A note
carried across more than two runs is a filing bug, not a safe outcome.

When you capture from work in another repo, say so in the `context:` line. It is the only breadcrumb back.

## The nightly compile

{{NIGHTLY_METHOD_DETAIL}}

A scheduled run behaves exactly like a manual `/process`. Check `wiki/_log.md` for `flag` entries after a run.

If you have no always-on machine, run `/process` by hand on a regular cadence instead. Once a day at the end
of any day you captured something. Or whenever the inbox gets large, meaning **10 or more notes, or any note
older than 3 days**.

The inbox tolerates lag, and nothing is lost while notes wait. What breaks the system is **never**
processing. The wiki stops growing and pulls go stale.

## Run process where the files are local

The "move note out of inbox" step deletes from `inbox/`, so it needs real disk access. Run `/process` on a
local surface: Claude Code or Cowork, with the Dropbox folder set to **Local / "Make available offline"**.

Not a cloud runner. Not a connector. That is also where the scheduled task must run.

## Pulling from any surface

Ask a question. Claude answers from `wiki/` and cites the pages it used. From claude.ai chat, on web or
phone, add the **Dropbox connector** so chat can read the wiki. If the answer is durable, accept the offer to
capture it back into the inbox.

## The skill library

The brain holds **knowledge**. A repeatable method is not knowledge, it is a **skill**. Capture, process,
pull, and maintain move knowledge. **`/brain-skill`** turns a repeated method into a skill. The longer
command name avoids a collision with other skill-building commands you may already have installed.

Built skills live in a **library**, a folder beside the vault in the same synced storage. It holds the one
master copy of each skill and the instructions for installing it. It sits beside the vault, not inside it,
because a tool is not knowledge. The one exception is the six brain skills, which stay in the vault so the
vault keeps installing itself.

### When the AI will offer

At two moments, and only at a natural stopping point:

| Moment | Why there |
|---|---|
| **capture** | You are present, and you have just decided something is worth keeping. If it is a method, now is the moment to ask. |
| **maintain** | You are deliberately looking for improvements, which is where a sweep belongs. |

**It does not offer during the nightly compile**, because nobody is there to answer. It does not offer during
a pull either, because that would interrupt the answer.

You can also ask for a sweep any time. Run **`/brain-skill`** with no argument.

### What it offers on

**The bar is high on purpose, so you are not asked about every note.** Two things must both be true. You
will run the method again, **and** it is worth a file someone keeps current and installs on each surface.

Only three kinds clear the second gate, and the offer names which one it is:

- **A business process you run** — how you quote, onboard, review, invoice, or ship.
- **A personalization** — how you want work done: your standards, your format, your voice.
- **A way of working with AI that you repeat** and that saves you time.

**Minor process detail does not qualify.** Neither does one-off troubleshooting, nor a fact, a finding, a
reference, a decision, or a corrected claim. When it is a close call, it stays silent.

- A note on **how you set up every project spreadsheet, in your standard layout** is a personalization you
  repeat. **It offers.**
- A note on **the steps that fixed one broken build last week** is written as steps, but it is a one-off.
  **It says nothing.**
- A note on **what an article about giraffes said** is knowledge. **It says nothing.**

It offers once per candidate per session, in one line, after the work finishes. It never delays the capture.
A candidate you decline is recorded in the library's `registry.md` and is not raised again. It **never builds
a skill without your yes**. It is a prompt based on a signal, so it will not catch everything.

### What a yes does

**It builds the skill now**, on the surface you are using. No inbox note. No queue. No second command.

It writes the master to `<library>/skills/<name>/SKILL.md`, writes the build notes to
`<library>/skills/<name>.BUILD.md` beside the folder, adds a row to `<library>/registry.md`, installs the
skill in whatever form your current surface supports, appends an entry to `wiki/_log.md`, then tells you what
was installed and what you still have to do by hand.

**The master is written every time, on every surface.** It is the durable copy, and it is what lets the
method reach your other surfaces later.

There is **no candidates page**. `<library>/registry.md` is the record. It carries what was built and what
was declined, and a declined row carries the reason.

Run **`/brain-skill install`** to install the library on this machine.

### A warning about memory features

Some surfaces offer only a **memory** feature. Storing the method there is an acceptable install. It is
**never** the copy that counts. Per-surface memory does not travel between surfaces and is not durable, which
is the exact problem this system exists to fix. The master goes in the library. The memory entry is a local
copy.

### How a skill reaches each surface

A wiki page reaches every surface that can read the vault. **A skill does not.** It reaches only the surfaces
its store serves, and installing the library is a **second install, separate from the vault's
`.claude/INSTALL.md`**. The runbook is `<library>/INSTALL.md`. The rules — where a master lives, how far it
reaches, the four stores, and the one-skill-one-store rule — are in `<library>/CONVENTIONS.md`.

**ChatGPT has no skill store.** The unit there is a **custom GPT** built from the master, or the method added
to an existing GPT or Project. `/brain-skill build` generates the builder prompt or the instruction block for
you, so you paste rather than rewrite.

A custom GPT is account-wide the moment you create it, on web and on mobile, with no per-machine install.
**You pick the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent, so you reach a method in a custom GPT by naming it.

Its instructions are a **copy** of the master, and that copy goes stale the day you edit the master. Nothing
on either side reports it. `<library>/registry.md` names every ChatGPT carrier and the date it was last
refreshed, so it is your refresh list.

## Digests — the brain, out loud

Some things are worth understanding away from a screen. **`/digest`** turns the hard content of a session
into a **spoken-word script plus an MP3**, written to `digests/`. Play it on a drive or a walk.

It is not a session summary. A summary says "we decided X". A digest explains what X is and why it beat Y,
slowly enough to follow with your eyes on the road. It runs 600 to 900 words, which lands near four to six
minutes.

**A digest is an interface, not a record.** The wiki holds what is true. A digest holds one explanation of
it, shaped for ears. Three things follow, and all three matter:

| Rule | Why |
|---|---|
| A digest is **not** a capture | If the content is durable, capture it separately. A spoken restatement is not a source. |
| **Process never reads `digests/`** | Compiling lossy prose into the wiki would poison the source of truth. |
| It is **never offered** to you | You ask for it. An offer that fires in normal use is noise. |

It replies with **one line** and stops — no preview, no summary, no follow-up. That is the point. You called
it so the session would not be interrupted.

**Retention.** Digests older than 60 days move to `digests/heard/` on the next `/maintain`. **Nothing is
deleted.** That folder grows without bound, and each MP3 is about two megabytes, so a hundred digests is
roughly two hundred megabytes of synced storage. Know that cost and decide for yourself.

**Setup.** The MP3 render needs `edge-tts` (`pip install edge-tts`) and a network connection. FFmpeg is
optional — it is what measures the real runtime. Without either, `/digest` still writes the script and marks
the audio as missing. The markdown is the artifact.

**Playing one.** On the phone, open the file and ask your assistant to read it aloud from the marker
comment. Or play the MP3 from the Dropbox app, hands-free.

## Updating the brain

This vault was built from the **ai-brain-seed** kit, and the kit keeps changing. The version you are on is
in `.claude/VERSION.md`.

Run **`/brain-update`** from any Claude Code session that can reach the vault. It reports the version you
are on, what each newer version adds, and how long each would take. **Then it stops and asks.** Nothing is
written until you say yes, and you see a diff before any file you already have is changed.

**Nothing expires.** A vault that stays where it is keeps working. You can take one update and decline
another.

Two things it will never do: run git in this vault, or touch `wiki/`, `inbox/`, `raw/`, `outputs/`, or
`digests/`. An update changes the rules and the tools. It never changes your knowledge.

After an update, **each of your other machines still needs the copy-install re-run.** The vault files sync.
The `~/.claude/` copies do not.

## Backfilling existing context

Do not try to file everything at once. As topics come up in real work, capture what you know into the inbox
and let processing build the pages. The brain compounds over time, and old material graduates in as it
becomes relevant.

Backfilling from a chat surface is a series of ordinary inbox captures. It never writes into `wiki/` or
`raw/` directly.

## Setting up a new machine

Read **`.claude/INSTALL.md`**. Or point a Claude Code session at it and say "install the brain skills on this
machine". It covers the copy-install, the `BRAIN_DIR` setting, an optional drift check, and how to verify.

The vault's `.claude/` is the source of truth. `~/.claude/` is a copy you never edit by hand.

You do **not** need to reinstall when a rule changes. The skills point at `SCHEMA.md` rather than restating
it, so protocol changes travel with Dropbox.

## Tools

- **Obsidian** to read and navigate the wiki, following `[[wikilinks]]` and the graph view.
- **Dropbox for desktop**, with the vault folder set to **Local / "Make available offline"**, not
  online-only. Files are then real on disk and a shell session can reach them.
- No git, ever. Dropbox is the sync and history layer.
````

## File: `README.md`

````markdown
# Brain

A personal, LLM-maintained knowledge base in plain markdown. It lives in Dropbox, so every surface can reach
it: Claude Code, Cowork, claude.ai chat on web and phone, and a private custom GPT in ChatGPT. **The wiki is
the durable source of truth**, not chat history and not model memory.

## The golden flow

`inbox/` -> `raw/` -> `wiki/` -> `outputs/`

Capture anything worth keeping into `inbox/`, fast and with no filing. Process moves each note into `raw/`,
where sources are immutable, and builds it into `wiki/` as concept-per-page, interlinked. Deliverables come
out in `outputs/`.

## Five verbs

- **capture** — drop something into `inbox/` with no filing decisions.
- **process** — compile the inbox into the wiki, on demand or nightly.
- **pull** — ask the brain. Answers cite wiki pages.
- **maintain** — lint the wiki for broken links, orphans, contradictions, and bad frontmatter.
- **digest** — turn a session into a spoken-word script and an MP3 in `digests/`, to listen to later.

## Digests are not knowledge

`digests/` sits **outside** the golden flow. A digest is an *interface*: one explanation of something,
shaped for ears, that ages out. The wiki holds what is true.

So a digest is never a capture, `process` never reads that folder, and digests older than 60 days move to
`digests/heard/`. Nothing is deleted.

## No git

Dropbox handles sync and version history. There is no git repo in this vault. Do not create one.

## Read it

Open this folder as an [Obsidian](https://obsidian.md) vault to browse pages and follow `[[wikilinks]]`.

Keep Dropbox for desktop running, with this folder set to **Local / "Make available offline"**, not
online-only. The files must be real on local disk.

## Where to look next

| File | What it is |
|---|---|
| `SCHEMA.md` | The full protocol. Machine-facing and binding. |
| `PROCESS.md` | The human handbook. How to use the brain day to day. |
| `wiki/_conventions.md` | The page contract: naming, folders, the three axes, frontmatter. |
| `wiki/_tags.md` | The controlled subject vocabulary. |
| `digests/_catalog.md` | What there is to listen to, newest first. |
| `.claude/INSTALL.md` | How to install the skills on a machine. |
| `.claude/VERSION.md` | Which version of the seed kit this vault came from. `/brain-update` checks for newer ones. |
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

- Lowercase kebab-case filenames, like `my-first-concept.md`. One **concept per page**, not one page per
  source.
- Inbox notes: `YYYY-MM-DD-HHMM-<slug>.md`.

## Folders

- `wiki/topics/` — evergreen knowledge by subject. Keep it flat. Nest only when a cluster grows.
- `wiki/projects/<slug>/` — active work. `wiki/archive/` — finished or dormant work.
- A cross-cutting fact lives once, usually in `topics/`. Filter it by tags and identity. Never duplicate it.

## The three axes

Every page is classified on three independent axes, and each axis has its own mechanism. Keep them separate
and filing is mechanical. Collapse two onto one mechanism and filing becomes a judgment call.

- **Lifecycle** (evergreen / active / done) -> **folders**: `topics/`, `projects/<slug>/`, `archive/`.
  Folders encode *only* lifecycle, never subject.
- **Identity** ({{IDENTITY_VALUES_SLASH}}) -> **frontmatter** `identity:`. A filter, never a folder.
- **Subject** (whatever the brain grows to cover) -> **tags and wikilinks**, drawn from the controlled list
  in [[_tags]]. Subject never rides on folders. That is what lets a cross-cutting fact live once and still be
  findable.

So at process time: pick the folder by lifecycle, set `identity`, then tag the subject from [[_tags]] and
link the canonical page. No single decision carries more than one axis.

## Identity is metadata, not a folder

`identity: {{IDENTITY_VALUES}}` in frontmatter. Knowledge is filed by subject. Identity is a filter.

## Linking

- Obsidian wikilinks: `[[slug]]` and `[[slug|text]]`. Inside a markdown table, escape the pipe:
  `[[slug\|text]]`.
- Every page links to at least one other page and is linked from at least one. No orphans.
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

`tags:` is the subject axis, drawn from the controlled vocabulary in [[_tags]]. It is not free-form. Status,
type, and identity have their own fields, and must never be expressed as tags.

## Outputs

Drafts go to `outputs/<project>/drafts/`. Finals go to `outputs/<project>/`. Code outputs go in their own
repo.

## Log entry types

`capture | process | wiki | draft | final | conventions | maintenance | flag`

## Hard rules

- `raw/` and processed source notes are immutable. No fabricated facts. Every claim traces to a source.
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

Tags are the **subject** axis only. See the three axes in [[_conventions#The three axes]].

This is the canonical list. Every `tags:` value on a wiki page must come from here. Adding a tag means
**adding it here first**, then using it. Never the reverse. The `maintenance-pass` skill lints pages against
this file.

**Tags are not the place for:**

- **status** — `draft | stable | needs-review` go in the `status:` field, never as a tag.
- **type** — `concept | reference | source-summary | ...` go in the `type:` field.
- **identity** — `{{IDENTITY_VALUES}}` go in the `identity:` field.

Keep the list small. Prefer an existing tag over a near-synonym. Reach for a new tag only when a real subject
has no home here. New tags are added at process time, by proposing them here first.

## Canonical tags

### The brain and the knowledge system

- `brain` — this knowledge base itself, its architecture and its storage.
- `knowledge-management` — methods and concepts for personal knowledge work.
- `workflow` — capture, process, pull, maintain, digest, and other methods.

### Starter subjects

<!-- The vocabulary grows with the brain. As real subjects appear during processing, add a tag here with a
     one-line definition, then use it. Group related tags under a heading. Delete this comment once the list
     has real entries. -->

## Retired and redirected (do not use)

<!-- When a tag is replaced or absorbed, move it here with an arrow to its canonical replacement, e.g.:
- `meta`, `system` → use `brain`.
     Read the left of the arrow as the retired tag and the right as the replacement. -->
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

> Cross-cutting knowledge lives in `topics/`. Identity-specific applied work lives in `projects/<slug>/`.
> Filter by the `identity:` field, never by folder.

Every page gets a line here at process time: the link, and a one-line summary. This file answers "what
exists". `_log.md` answers "what changed".

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

Types: `capture | process | wiki | draft | final | conventions | maintenance | flag`. Append only. Never
rewrite an entry.

---

## [{{TODAY}}] conventions | Brain initialized from ai-brain-seed. Conventions and tag vocabulary approved by {{OWNER_NAME}}.
````

## File: `digests/_catalog.md`

````markdown
# Audio digests — what's here to listen to

Spoken-word explanations of things that were hard to hold in your head. Newest first.

Each one has a markdown script and a pre-rendered MP3 beside it.

A digest is an **interface, not a record**. The wiki holds what is true. A digest holds one explanation of
it, shaped for ears. Nothing here is a source, and `/process` never reads this folder.

Digests older than 60 days move to `heard/`. Nothing is deleted.

<!-- Newest entry goes directly below this line. One entry, one blank line between. -->
````

## File: `.claude/INSTALL.md`

````markdown
# Installing and updating the brain skills on a machine

Point a Claude Code session at this file and say **"install the brain skills on this machine"**. Everything
needed is here.

This file lives in the vault, so it is present and current on every machine the sync reaches.

---

## The one rule

```
<vault>/.claude/     SOURCE OF TRUTH. Edit here. Cloud sync carries it to every machine.
      |  copy-install
      v
~/.claude/           INSTALLED COPY. Never edit. Overwritten on every install.
```

**Never edit `~/.claude/commands/` or `~/.claude/skills/` directly.** An edit there is invisible to every
other machine, and the next install destroys it. When a skill needs changing, change the vault copy and
reinstall.

**A protocol change needs no install.** The skills are thin. They carry the job skeleton and the
vault-resolution logic, and they point at `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the
rules. Those files live in the vault, so a rule change reaches every machine and every surface through sync
with no install step. Reinstall only when a **skill file itself** changes.

---

## Install or update

The vault path on this machine is `{{VAULT_PATH}}`.

### Windows (PowerShell)

```powershell
$b = "{{VAULT_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\commands" | Out-Null
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"   | Out-Null
Copy-Item "$b\.claude\commands\*" "$env:USERPROFILE\.claude\commands\" -Recurse -Force
Copy-Item "$b\.claude\skills\*"   "$env:USERPROFILE\.claude\skills\"   -Recurse -Force
```

### macOS and Linux

```bash
b="{{VAULT_PATH}}"
mkdir -p "$HOME/.claude/commands" "$HOME/.claude/skills"
cp -R "$b/.claude/commands/." "$HOME/.claude/commands/"
cp -R "$b/.claude/skills/."   "$HOME/.claude/skills/"
```

That installs 7 commands (`/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`, `/digest`,
`/brain-update`) and 6 skills (`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`,
`audio-digest`, `brain-update`).

The copy overwrites files of the same name. It does not delete anything else in `~/.claude/`.

**`.claude/scripts/` is deliberately not copied.** The `audio-digest` skill calls `render-digest.py` at its
vault path, so the script stays in one place and a change to it needs no reinstall.

**The skill library is a second, separate install.** Its runbook is `<library>/INSTALL.md`, in the library
folder beside the vault. **This runbook does not cover it.** These 6 skills are the brain skills, and they
stay in the vault so the vault keeps installing itself.

---

## One per-machine setting: `BRAIN_DIR`

It goes in `~/.claude/settings.json`, **not** in the vault, because the vault path differs per machine.

```json
{
  "env": {
    "BRAIN_DIR": "{{VAULT_PATH}}"
  }
}
```

**NOTE:** on Windows, JSON needs each backslash doubled, like
`"C:\\Users\\<you>\\Dropbox\\AI-Brain"`.

The skills read `BRAIN_DIR` so they resolve the vault from any project directory. Without it, a skill falls
back to searching the session's directories for one holding both `SCHEMA.md` and a `wiki/` folder. That
fallback works inside the vault and fails outside it. Set it.

If `~/.claude/settings.json` already exists, merge the `env` block into it. Do not replace the file.

---

## Optional: the digest renderer

`/digest` always writes its script. The **MP3** needs one Python package, installed once per machine:

```bash
pip install edge-tts
```

It is free, needs no API key, and needs a network connection when a digest is rendered.

**FFmpeg is optional.** `render-digest.py` calls `ffprobe` to measure the real length of the MP3. Without
it the render still works, and the runtime is recorded as unknown rather than guessed.

Skip both and `/digest` still works. It sets `audio: none` and says so. **The markdown is the artifact. The
MP3 is a convenience.**

---

## Optional: check for drift

A stale installed copy fails quietly. The check below makes it announce itself instead. Run it whenever a
command behaves in a way the vault copy does not explain.

### Windows (PowerShell)

Paste this in whole. It prints a line per mismatch and **nothing when the two sides agree**.

```powershell
$b = "{{VAULT_PATH}}"
$dst = "$env:USERPROFILE\.claude"
Get-ChildItem -Recurse -File "$b\.claude\commands", "$b\.claude\skills" | ForEach-Object {
  $rel  = $_.FullName.Substring("$b\.claude\".Length)
  $copy = Join-Path $dst $rel
  if (-not (Test-Path $copy)) { "MISSING: $rel" }
  elseif ((Get-FileHash $_.FullName).Hash -ne (Get-FileHash $copy).Hash) { "DIFFERS: $rel" }
}
```

`fc.exe` compares a single pair of files if you want to see the differing lines:
`fc.exe "%USERPROFILE%\.claude\skills\process-inbox\SKILL.md" "<vault>\.claude\skills\process-inbox\SKILL.md"`

### macOS and Linux

```bash
diff -rq "{{VAULT_PATH}}/.claude/commands" "$HOME/.claude/commands"
diff -rq "{{VAULT_PATH}}/.claude/skills"   "$HOME/.claude/skills"
```

**NOTE:** `diff -rq` also reports files that exist only on the installed side, as `Only in ...`. Those are
fine if they come from somewhere other than the vault. The PowerShell check walks the vault side only, so it
ignores them.

To fix any drift, re-run the install commands above. The vault always wins.

---

## Verify

Open a new Claude Code session and confirm all seven commands are offered: `/capture`, `/process`, `/pull`,
`/maintain`, `/brain-skill`, `/digest`, and `/brain-update`.

Then run a real capture. `/capture test note` must write a file into `<vault>/inbox/` and report the full
path. If it writes into the current project instead, `BRAIN_DIR` is not set or not readable.

---

## What a reinstall does and does not cover

| Covered | Not covered |
|---|---|
| The 7 command files in `.claude/commands/` | `SCHEMA.md`, `wiki/_conventions.md`, `wiki/_tags.md`. Sync carries those, and no install is involved. |
| The 6 skill folders in `.claude/skills/` | `BRAIN_DIR` in `~/.claude/settings.json`. Set once per machine, by hand. |
| | `.claude/scripts/`. The skills call it at its vault path, so it is never copied. |
| | `edge-tts`, for the `/digest` MP3. One `pip install` per machine. |
| | The skill library. It installs separately, per `<library>/INSTALL.md`. |
| | The instruction block on the Cowork, chat, and ChatGPT surfaces. Each is configured in its own app. |

**WARNING:** reinstalling does not fix a wrong `BRAIN_DIR`. A skill that resolves the wrong vault writes
notes into the wrong folder and reports success. Check the path in the verify step above.

---

## Updating the vault itself

A reinstall copies the vault's **current** files to this machine. It does not bring in anything new from the
kit the vault was built from.

That is a separate job. `VERSION.md` beside this file records the version. Run **`/brain-update`** to check
the kit for newer ones and apply only what the owner approves. The rules are in `SCHEMA.md` §13.

**An update adds files under `.claude/`, so every machine needs this runbook re-run afterward.**
````

## File: `.claude/VERSION.md`

````markdown
# Vault version

This file records which version of the **ai-brain-seed** kit this vault was built from, and every update
applied to it since. It is machine-facing bookkeeping. It is not a wiki page, and `/process`, `/pull`, and
`/maintain` ignore it.

**Do not edit the history table by hand.** The update runbook appends to it. A row you write yourself makes
the next update skip a migration it should have applied.

```
seed-version: 0.3.0
installed:    {{TODAY}}
vault-path:   {{VAULT_PATH}}
library-path: {{SKILLS_PATH}}
```

## Applied

| Version | Applied on | How | Notes |
|---|---|---|---|
| 0.3.0 | {{TODAY}} | fresh install | Built new from the 0.3.0 seed. No migration needed. |

## Checking for updates

Run **`/brain-update`** from any Claude Code session on a machine that can reach this vault. It reads the
kit's current version, compares it against `seed-version:` above, and walks you through anything missing.

Nothing expires. A vault that stays at its installed version keeps working. An update is a choice.

The kit lives at <https://github.com/ajdayvie/ai-brain-seed>. Its `UPDATES.md` is the runbook, and
`CHANGELOG.md` says what each version changed.

**Never run git in this vault.** An update clones or fetches the kit somewhere else and copies from there.
````

## File: `.claude/skills/capture-to-inbox/SKILL.md`

````markdown
---
name: capture-to-inbox
description: >
  This skill should be used when the user wants to quickly save something to the knowledge brain without
  filing it. Triggers include "capture this", "save this to the brain", "add to inbox", the /capture command,
  or when you proactively offer to capture durable knowledge. It writes ONE timestamped note to the vault's
  inbox/ and does no filing or wiki editing — capture is intentionally fast and dumb.
---

# Capture -> inbox

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `inbox/`.** This skill runs from any project
directory, and a relative path resolves against that project instead of the brain.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §6a** and follow it. It is authoritative, it may have changed, and this skill does
not copy its rules. Capture touches no wiki page, so `wiki/_conventions.md` and `wiki/_tags.md` are not
needed here.

## The job

1. Gather the content: the text the user gives, or the durable knowledge from the current session. Durable
   means a decision, a method, a spec, a finding, or a corrected fact. Skip transient chatter.
2. Write ONE file to `<brain>/inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md`. Start it with a single
   `context:` line saying where it came from and what it is about. The content follows as clean markdown. No
   frontmatter.
3. **Make the note self-sufficient**, per SCHEMA §6a step 3. The note is filed later, on a different machine,
   by a run that can see only the vault. Write down the substance itself. Cite a repo, a branch, a
   transcript, or a URL as provenance in addition to the content, never instead of it. When the capture came
   from work in another repo, say so in the `context:` line.
4. **Offer a skill only when the note clears both gates in `SCHEMA.md` §9.** The owner will run the method
   again, **and** it is a business process, a personalization, or a way of working with AI that they repeat.
   **Name that kind in the offer. If you cannot name one, do not offer.** Stay silent for minor process
   detail, for one-off troubleshooting, and for a fact, a finding, a reference, a decision, or a corrected
   claim. **When in doubt, stay silent.** Offer once, in one line, after the note is written. The
   offer never blocks or delays the capture. On a yes, hand off to the **skill-library** skill in build mode,
   which builds it now per `SCHEMA.md` §6e.
5. Do NOT create or edit a wiki page. Do NOT choose a topic, project, or identity. That happens at process
   time.
6. Confirm what was captured, and echo the full path you wrote.
````

## File: `.claude/skills/process-inbox/SKILL.md`

````markdown
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
````

## File: `.claude/skills/maintenance-pass/SKILL.md`

````markdown
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
````

## File: `.claude/skills/skill-library/SKILL.md`

````markdown
---
name: skill-library
description: >
  This skill should be used to sweep for, build, or install skills held in the owner's skill library.
  Triggers include "/brain-skill", "build a skill", "turn this into a skill", "make this repeatable",
  "install my skills", and "what could be a skill". It proposes repeatable methods, builds a master into the
  library and installs it on the current surface, and installs the library on this machine. It never builds a
  skill without the owner's yes.
---

# Skill library

**Library root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. `<library>` is the value of the `SKILLS_DIR` environment variable. Read it with
`echo "$SKILLS_DIR"`. If it is unset, use the sibling of `<brain>` named `{{SKILLS_DIRNAME}}`. **Never write
a bare relative path.** This skill runs from any project directory, and a relative path resolves against that
project instead of the brain or the library.

If `<library>` does not resolve to a folder holding `registry.md`, stop and report which paths you tried.
**Do not create a library without the owner's yes.**

## Step 0 — load the binding protocol, every run, before anything else

Read these two files and follow them. They are authoritative, they may have changed since the last run, and
this skill **deliberately does not copy their rules**. Do not work from memory.

- **`<library>/CONVENTIONS.md`** — the library contract: where a master lives, how far a skill reaches, the
  four stores, the one-store rule, junction versus copy, provenance, the packaging traps, and what is not a
  skill.
- **`<brain>/SCHEMA.md` §6e** — governs this job. §9 governs when to offer.

Where this skill and those files disagree, **they win**. Say so in the report, so the skill gets fixed.

## The signal

**The bar is high on purpose.** Both gates must hold. The owner will run the method again, **and** it is
worth a maintained artifact, meaning a **business process** they run, a **personalization** of how they want
work done, or a **way of working with AI** they repeat. **Name that kind in the offer. If you cannot name
one, do not offer.**

Stay silent for minor process detail, for one-off troubleshooting, and for a fact, a finding, a reference, a
decision, or a corrected claim. **When in doubt, stay silent.** The full rule, with all three worked
examples, is in `<brain>/SCHEMA.md` §9.

## The job

Pick the mode from the argument. No argument means sweep.

### Mode 1 — sweep (no argument)

1. Read `<library>/registry.md` first, so a declined skill is not proposed again.
2. Scan recent pages under `<brain>/wiki/` and recent entries in `<brain>/wiki/_log.md` for a repeatable
   method the owner still runs by hand.
3. Propose each candidate. **One offer each.** Say in one sentence what the skill would do.
4. **Build nothing without a yes.** A proposal is not a yes.
5. On a yes, run Mode 2 for that candidate now.

### Mode 2 — build (`build <name>`, or a yes to an offer)

The owner is present and has said yes. **Build it now.** No inbox note, no queue, no second command.

1. **Write the master** to `<library>/skills/<name>/SKILL.md`. Frontmatter carries `name` and `description`
   only. Read `<library>/CONVENTIONS.md` for where the master lives and how far the skill reaches.
2. **Write `<library>/skills/<name>.BUILD.md`**, beside the folder and never inside it.
3. **Add a row** for the skill to `<library>/registry.md`, marked built. A skill the owner declines gets a
   declined row with the reason instead.
4. **Install it in the form this surface supports**, per the table below, then per `<library>/INSTALL.md`.
5. **Append an entry** to `<brain>/wiki/_log.md` recording what was built. That is the "what changed" record,
   and it is the one wiki write allowed outside process.
6. **Report** what was installed, and what the owner must still do by hand.

| Surface | The installed form |
|---|---|
| Claude Code, Cowork | A skill, installed into `~/.claude/skills/` per `<library>/INSTALL.md` |
| claude.ai chat | No install from chat. Build a bundle for the account store for the owner to upload, or add the method to a Project's instructions. |
| ChatGPT | A custom GPT built from a generated builder prompt, or the method added to an existing GPT's or a Project's instructions |

**The rule, rather than a taxonomy:** install it the way this surface installs a method. If the surface
has no mechanism for that, say so and produce the artifact the owner can install by hand.

**The memory trap.** Some surfaces offer only a **memory** feature. A memory entry is an acceptable installed
form. It is **never** the artifact. Per-surface memory does not travel between surfaces and is not durable,
which is the exact problem this system exists to fix. **The master goes in the library. The memory entry is a
local copy.** Never store a method only in a surface's memory and call it saved.

**The master is written in every case, on every surface.** It is the durable copy, and it is what lets the
method reach other surfaces later.

### Mode 3 — install the library (`install`)

1. Follow `<library>/INSTALL.md` for this machine.
2. Report which skill reaches which surface.
3. Name anything that is a master with no install.

## Hard rules

- **Never write a master without an explicit yes from the owner.** A proposal is not a yes.
- **Never put `BUILD.md` inside the skill folder.** The packager sweeps the folder into the bundle, so a
  `BUILD.md` inside becomes context cost on every load with no run-time value.
- **Never let one skill exist in two stores.** Both copies load, and which one wins is ambiguous.
- **Never claim a skill reaches a surface it was not installed on.** Only the account store syncs by itself.
  **ChatGPT has no skill store**, which is why the unit there is a custom GPT.
- **An instruction copy in a GPT or a Project is a copy, and it goes stale the day the master changes.** Never
  describe it as synced. `<library>/registry.md` is the refresh list.
- Never run git in the vault or in the library.
````

## File: `.claude/skills/audio-digest/SKILL.md`

````markdown
---
name: audio-digest
description: >
  This skill should be used when the user wants the hard content of the current session turned into
  something they can LISTEN to later — a spoken-word script, plus a pre-rendered MP3, written to the
  brain's digests/ section. Triggers include "/digest", "make an audio digest", "digest that for the
  drive", "explain that to me for later", "record that for the car", or "I want to listen to this
  on the go". It writes the digest and replies with ONE line — it must not clutter the session it
  was called from. It is NOT a capture: durable knowledge still goes to inbox/ via capture-to-inbox.
---

# Audio digest -> `digests/`

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `digests/`.** This skill runs from any project
directory, and a relative path resolves against that project instead of the brain.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §6f** and follow it. It is authoritative, it may have changed, and this skill does
not copy its rules. **SCHEMA wins over this file** on any rule. This file carries the job shape and the
script spec, which are structure, not protocol.

A digest touches no wiki page, so `wiki/_conventions.md` and `wiki/_tags.md` are not needed here.

---

## What this is, in one line

**A digest is an interface, never a record.** The wiki holds what is true. A digest holds one explanation
of it, shaped for ears, that ages out.

Three consequences, all binding:

- A digest is **not** a capture. If the content is durable, offer `/capture` separately — after, and only
  if the owner is at a stopping point.
- **`/process` must never read `digests/`.** A spoken restatement compiled into the wiki would pollute
  the source of truth with lossy prose.
- Digests **age out of the root**, but they are not deleted. At 60 days they move to `heard/` and stay
  there. `/maintain` owns that move. See Retention.

---

## The job

### 1. Choose the material

Default scope is the substantive content of the current session — the reasoning, the trade-offs, the
numbers, the thing that was hard to hold in your head. An argument narrows it (`/digest the pricing math`).

**The anti-goal: this is not a session summary.** A summary says *"we decided X."* A digest explains
*what X is and why it beat Y*, slowly enough to follow with your eyes on the road. If you find yourself
listing what happened, you are writing the wrong artifact.

Pick 2–4 ideas and teach them properly. Do not survey everything that was said.

### 2. Write the script

Target **600–900 words**, which lands near four to six minutes. Follow the spec below — it is the whole
value of this skill.

### 3. Write the file

`<brain>/digests/YYYY-MM-DD-HHMM-<short-slug>.md`, in the shape given below.

### 4. Render the audio

```bash
python "<brain>/.claude/scripts/render-digest.py" "<path-to-the-digest.md>"
```

It prints one line of JSON with the real duration. **Put that measured runtime in the frontmatter** —
do not estimate it.

The renderer needs `edge-tts` installed (`pip install edge-tts`) and a network connection. `ffprobe`, from
FFmpeg, is optional: without it the JSON reports `"seconds": null`, and you then say the runtime is unknown
rather than guessing one.

If the render fails, leave `audio: none`, say so in your one line, and carry on. **The markdown is the
artifact. The MP3 is a convenience.** A failed render never stops the digest from being written.

### 5. Catalog it

Append one line to `<brain>/digests/_catalog.md`, newest at the top, in the format given below.

### 6. Report — one line, then stop

> Digest recorded: **&lt;title&gt;** — 4 min — `digests/2026-09-13-1420-<slug>.md` + MP3

**No preview of the script. No summary of the summary. No offer to continue. No follow-up question.**
The owner called this so the session would *not* be interrupted. Honor that.

---

## The script spec

### Shape

1. **Cold open, two sentences.** The listener has no context, is hours away, and may be driving. Say
   what this is about and why they would care.
2. **The answer, then the reasoning.** Inverted from normal written order on purpose — a listener cannot
   skim back.
3. **One sentence of footing, early.** *"We measured the first part. The cost numbers are guesses."*
4. **The explanation.** The bulk, and the point.
5. **End on the open question, or the call the listener still owns.**

### Rules

- **No markdown that reads badly aloud.** No bullets, tables, headings, links, file paths, code
  identifiers, or citation markers anywhere in the body.
- **A table becomes a spoken comparison, with every number kept.** *"Three options were on the table.
  The cheapest ran about four dollars a month, but it couldn't hold a filesystem."* Never drop a figure
  to make a sentence speakable — say the figure in words.
- **Numbers as speech.** "About fifteen dollars a month." "Roughly three to five times faster." "One
  and a half megabytes." "Between thirty and forty percent."
- **Use the real term, define it in one clause, then keep using it.** The listener wants to *learn* the
  vocabulary, not have it removed. "An MCP server — that's just a small program that hands an AI a menu
  of things it's allowed to do — sits between…"
- **Signposts instead of headings.** *"First…"* · *"Here's where it got interesting."* · *"The part I'd
  push back on is…"*
- **Strip internal scaffolding.** No agent names, lane numbers, branch names, commit hashes, tool names,
  or file paths. If the listener would have to have been in the session to parse it, rewrite it.
- **Second person, contractions, conversational.** A colleague explaining on a walk — not a narrator.
- **Say the footing out loud.** "We measured this." / "That's an estimate." / "Nobody's checked that."
  Never launder a guess into a fact to make the sentence flow.

---

## File shape

```markdown
---
title: Why we're putting a server between the agent and the files
recorded: 2026-09-13 14:20
runtime: 4 min 31 s
source: <the project or session this came from>
about: MCP servers, why the brain needs one, what it costs
audio: 2026-09-13-1420-mcp-gateway.mp3
state: new
captured: no
---

# Why we're putting a server between the agent and the files

<!-- Read aloud from the next line, verbatim. Do not summarize.
     Everything above this line is filing metadata. -->

So — the thing we worked out today was...
```

**That HTML comment is load-bearing, not decoration.** Connector review forbids putting "read this
verbatim" in an MCP tool description, and claude.ai and Claude desktop silently discard the MCP
`instructions` field. The inside of the file is the only channel that reaches the phone. Always include it.

`about:` is written for how the owner will ask for it out loud — *"the one about the server thing"* — never
for how a filename reads.

---

## Catalog line

Newest at the top of `<brain>/digests/_catalog.md`:

```
- **Why we're putting a server between the agent and the files** — 4 min — 2026-09-13 — new —
  MCP servers, why the brain needs one, what it costs. `2026-09-13-1420-mcp-gateway.md`
```

---

## Retention

**Nothing is deleted. `heard/` is an archive.**

| Where | Rule |
|---|---|
| `digests/` root | Older than 60 days -> move to `heard/`, markdown and MP3 together |
| `digests/heard/` | Kept. Nothing is deleted. |

**`/maintain` does the move**, per `SCHEMA.md` §6d. This skill never moves and never deletes anything.
Neither verb deletes a digest or its MP3.

`heard/` grows without bound, and each MP3 runs about two megabytes, so a hundred digests is roughly two
hundred megabytes of synced storage. That is the known cost of the "nothing is deleted" rule. An owner who
wants a delete step adds it to `SCHEMA.md` §6f and to `/maintain` deliberately. It is not a default.

---

## Do not

- Do not offer a digest proactively. Wait to be asked. An offer that fires in normal operation is noise,
  and it trains the owner to ignore the channel.
- Do not write to `wiki/`, `inbox/`, `raw/`, or `outputs/`. This skill owns `digests/` and nothing else.
- Do not run git in the vault. Ever.
````

## File: `.claude/skills/brain-update/SKILL.md`

````markdown
---
name: brain-update
description: >
  This skill should be used when the user wants to check their knowledge brain for updates from the
  ai-brain-seed kit and install them. Triggers include "/brain-update", "check my brain for updates",
  "update the brain", "is my brain out of date", "what's new in the brain kit", and "install the new
  brain features". It finds the kit, compares versions, shows what changed, and applies only the
  migrations the owner says yes to. It never updates without a yes, and it never runs git in the vault.
---

# Update the brain from the kit

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. If that is ambiguous, **ask the owner for the absolute path and wait.** Never guess a
default like `~/Dropbox/AI-Brain`. This skill runs from any project directory.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §13** and **`<brain>/.claude/VERSION.md`**. §13 is authoritative for what an
update may and may not do in this vault. If `VERSION.md` is missing, this vault predates version tracking —
that is expected, and the kit's runbook knows how to handle it.

## Step 1 — get the kit

The kit is <https://github.com/ajdayvie/ai-brain-seed>.

If this session already has a clone of it, use that and `git pull` first. Otherwise clone it shallow into a
scratch folder, or fetch the raw files over HTTPS if git is unavailable.

**The clone must never land inside `<brain>`, and you must never run git inside `<brain>`.** The vault is
git-free forever. Cloud sync is its versioning layer.

## Step 2 — hand off to the kit's runbook

Read **`<kit>/UPDATES.md`** and follow it, start to finish. **That document is authoritative for the whole
job.** It holds the version probe, the placeholder recovery, the migration order, the safety contract, the
verification, and the bookkeeping. This skill deliberately does not copy any of it, so a kit released after
this file was written still updates correctly.

Read `<kit>/CHANGELOG.md` so you can say what each version actually changed, rather than paraphrasing from
memory.

## The rules this skill will not let a runbook relax

- **Never run git in the vault.** Never leave a `.git` folder there.
- **Ask before each migration**, and show a diff before every edit to an existing file. Declining one is a
  valid answer, and a partial update is a valid end state.
- **Never touch** `wiki/` page content, `inbox/`, `raw/`, `outputs/`, `digests/`, or the library's
  `skills/`. Those are the owner's. The exceptions are the anchored `_log.md` entry and any `_index.md`
  change a migration names explicitly.
- **Back up every existing file you edit** beside itself as `<file>.pre-<version>` before the edit.
- **A missing anchor stops the step.** Show the owner the surrounding lines and let them decide. Never
  improvise a location, and never overwrite their file with the seed template.
- **Never install software on the owner's machine.** State the command and let them run it.
- **Report what you skipped**, in `.claude/VERSION.md` and in `wiki/_log.md`, with the reason. A skipped
  step that is not written down is one the next update assumes ran.

## Do not

- Do not offer an update proactively, and do not put one on a schedule. Nothing expires. A vault that stays
  at its installed version keeps working.
- Do not update a vault you have not confirmed with the owner by absolute path.
- Do not report an update as finished when a step errored or was skipped.
````

## File: `.claude/commands/capture.md`

````markdown
---
description: Capture something to the brain inbox (no filing)
---
Apply the **capture-to-inbox** skill for: $ARGUMENTS

If no argument is given, capture the durable knowledge from our current conversation. Write one timestamped
note to the brain's `inbox/`. Resolve the vault as `$BRAIN_DIR`, never as a bare relative `inbox/`. Make the
note self-sufficient per `SCHEMA.md` §6a. Confirm with the full path. Do not file it into the wiki.

Offer a skill only if the note clears both gates in `SCHEMA.md` §9: I will run the method again, and it is a
business process, a personalization, or a way I work with AI. Name that kind, in one line, at the end. Skip
minor process detail. When in doubt, say nothing.
````

## File: `.claude/commands/process.md`

````markdown
---
description: Compile the inbox into the wiki
---
Apply the **process-inbox** skill across everything in the brain's `inbox/`. Resolve the vault as
`$BRAIN_DIR`, never as a bare relative `inbox/`.

Follow the skill's Step 0 first: read `SCHEMA.md` §6b, `wiki/_conventions.md`, and `wiki/_tags.md`, and work
from those, not from memory.

Report what you filed and where, what you moved into `raw/`, and what you left in the inbox and why.
````

## File: `.claude/commands/pull.md`

````markdown
---
description: Answer from the brain wiki with citations
---
Answer this from the brain wiki, citing the specific pages you used: $ARGUMENTS

The wiki is `$BRAIN_DIR/wiki/`. Read it there, not from a relative `wiki/` in the current project.

If the wiki does not cover it, say so plainly. If the answer is durable and worth keeping, offer to capture
it.
````

## File: `.claude/commands/maintain.md`

````markdown
---
description: Run a maintenance / lint pass
---
Apply the **maintenance-pass** skill across the entire brain wiki at `$BRAIN_DIR/wiki/`, not a relative
`wiki/` in the current project.

Follow the skill's Step 0 first: read `wiki/_conventions.md`, `wiki/_tags.md`, and `SCHEMA.md` §5 and §7.

Report by category, apply the safe fixes, list the contradictions for me to decide, and log the pass.

Include the skill sweep in the findings, and offer any candidate once, per `SCHEMA.md` §9. Build nothing
without my yes.
````

## File: `.claude/commands/brain-skill.md`

````markdown
---
description: Sweep for, build, or install a skill from the skill library
---
Apply the **skill-library** skill in the mode named by: $ARGUMENTS

- No argument — sweep for methods that clear both gates in `SCHEMA.md` §9, propose them one at a time, and
  build nothing.
- `build <name>` — build `<name>` now: write the master, install it on this surface, and log it.
- `install` — install the library on this machine and report what reaches which surface.

The command is `/brain-skill`, not `/skill`. The longer name avoids a collision with other skill-building
commands already installed on this machine.

Resolve the vault as `$BRAIN_DIR` and the library as `$SKILLS_DIR`, falling back to the sibling of
`$BRAIN_DIR` named `{{SKILLS_DIRNAME}}`. Never use a bare relative path.

Follow the skill's Step 0 first: read `<library>/CONVENTIONS.md` and `SCHEMA.md` §6e, and work from those,
not from memory.

Never write a master without my explicit yes.
````

## File: `.claude/commands/digest.md`

````markdown
---
description: Record an audio digest of this session to the brain (no session clutter)
---
Apply the **audio-digest** skill for: $ARGUMENTS

Resolve the vault as `$BRAIN_DIR`, never as a bare relative `digests/`. If no argument is given, digest the
substantive content of our current session — the reasoning and the numbers, not a list of what happened.

Follow the skill's Step 0 first: read `SCHEMA.md` §6f and work from it, not from memory.

Write the script to `$BRAIN_DIR/digests/`, render the MP3, add one catalog line — then reply with **exactly
one line** and stop. Do not preview the script, do not summarize what you wrote, and do not ask a follow-up.

This is not a capture. If the content is durable, offer `/capture` separately, and only at a stopping point.
````

## File: `.claude/commands/brain-update.md`

````markdown
---
description: Check the ai-brain-seed kit for updates and install the ones I approve
---
Apply the **brain-update** skill. Any argument narrows it: $ARGUMENTS

Resolve the vault as `$BRAIN_DIR`. If that is unset or ambiguous, ask me for the absolute path and wait.
Never guess a default.

Follow the skill's Step 0 first: read `SCHEMA.md` §13 and `.claude/VERSION.md`, and work from those, not from
memory. Then fetch the kit into a scratch folder **outside the vault** and follow its `UPDATES.md`.

With no argument, check and report only:

- the version my vault is on, and the version the kit is on;
- one line per missing version, saying what it adds, from the kit's `CHANGELOG.md`;
- how long each would take.

**Then stop and ask which ones to apply.** Do not write anything into the vault before I say yes. Show me a
diff before every edit to a file I already have. Never run git in the vault.
````

## File: `.claude/scripts/render-digest.py`

````python
#!/usr/bin/env python3
"""
render-digest.py — turn an audio-digest markdown file into a pre-rendered MP3.

Used by the `audio-digest` skill. Reads a digest file from `<vault>/digests/`,
strips everything that is filing metadata rather than script, and renders the
spoken body with edge-tts (Microsoft neural voices; free, no API key, needs a
network connection).

Usage:
    python render-digest.py <path-to-digest.md> [--voice NAME] [--rate PCT] [--dry-run]

Prints one line of JSON to stdout:
    {"ok": true, "audio": "...mp3", "seconds": 271.4, "words": 780, "wpm": 172}

Exit codes: 0 ok, 1 bad input, 2 render failed (network/edge-tts).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Warm, conversational, closest of the free voices to an explaining colleague.
DEFAULT_VOICE = "en-US-AndrewMultilingualNeural"

# Negative rate slows delivery. Digests are explanatory, not news reads:
# -8% lands near 170 wpm, which is a pace you can follow while driving.
DEFAULT_RATE = "-8%"

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def strip_to_script(raw: str) -> tuple[str, str]:
    """Return (title, spoken_body). Everything not meant for the ear is removed."""
    body = FRONTMATTER.sub("", raw, count=1)
    body = HTML_COMMENT.sub("", body)

    title = ""
    lines = body.splitlines()
    out: list[str] = []
    for line in lines:
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue
        # A digest body should carry no headings at all. If one slipped in,
        # speak its text rather than dropping the content on the floor.
        if line.startswith("#"):
            out.append(line.lstrip("#").strip())
            continue
        out.append(line)

    text = "\n".join(out)

    # Defensive cleanup. By spec the body is plain spoken prose, but a stray
    # link or emphasis marker must never be read aloud as punctuation noise.
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)   # [[page|label]]
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)              # [[page]]
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)         # [text](url)
    text = re.sub(r"`{1,3}([^`]*)`{1,3}", r"\1", text)           # code spans
    text = re.sub(r"(\*\*|__|\*|_)", "", text)                   # emphasis
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)         # bullets
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)             # quotes
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[—–]", ", ", text)                 # dashes -> a beat
    text = re.sub(r"[^\x00-\x7F]+", " ", text)                   # emoji, symbols
    text = re.sub(r"\n{3,}", "\n\n", text)

    return title, text.strip()


def duration_seconds(path: Path) -> float | None:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, timeout=60,
        )
        return round(float(r.stdout.strip()), 1)
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("digest", type=Path)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--rate", default=DEFAULT_RATE)
    ap.add_argument("--dry-run", action="store_true",
                    help="print the spoken text and exit; render nothing")
    args = ap.parse_args()

    if not args.digest.is_file():
        print(json.dumps({"ok": False, "error": f"no such file: {args.digest}"}))
        return 1

    title, script = strip_to_script(args.digest.read_text(encoding="utf-8"))
    if not script:
        print(json.dumps({"ok": False, "error": "no spoken body found"}))
        return 1

    # The title is spoken first so the file identifies itself when scrubbed to
    # from a car stereo, where no filename is visible.
    spoken = f"{title}.\n\n{script}" if title else script
    words = len(spoken.split())

    if args.dry_run:
        print(spoken)
        return 0

    audio = args.digest.with_suffix(".mp3")

    # edge-tts 7.x wants a file, not stdin. A sidecar next to the digest also
    # keeps the exact spoken text auditable when a render sounds wrong.
    txt = args.digest.with_suffix(".speech.txt")
    txt.write_text(spoken, encoding="utf-8")

    cmd = [sys.executable, "-m", "edge_tts",
           "--voice", args.voice, f"--rate={args.rate}",
           "-f", str(txt), "--write-media", str(audio)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=900)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": f"edge-tts failed to start: {e}"}))
        return 2
    finally:
        txt.unlink(missing_ok=True)

    if proc.returncode != 0 or not audio.is_file():
        print(json.dumps({"ok": False, "error": (proc.stderr or "render failed")[-400:]}))
        return 2

    secs = duration_seconds(audio)
    print(json.dumps({
        "ok": True,
        "audio": str(audio),
        "seconds": secs,
        "words": words,
        "wpm": round(words / (secs / 60)) if secs else None,
        "voice": args.voice,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
````

---

# Part IV — Library file templates

Write each file at the stated path, relative to the **library** root, which sits beside
the vault. Then apply the placeholder replacements from Part II, step 4. The `skills/`
folder starts empty. It fills as candidates are built.

## File: `README.md`

````markdown
# Skill library

The companion to the brain. **The brain holds knowledge. The library holds methods.**

A skill is a verb. Knowledge is a noun. The wiki holds the nouns: facts, decisions, findings, corrected
claims. The library holds the verbs: the methods you would otherwise explain again in every new session.

The library is a **sibling of the vault**, in the same synced folder. It is not inside the vault, because a
tool is not knowledge. Putting methods inside a knowledge base blurs what the brain is.

## The one-store rule

**A skill lives in exactly one store.** There are four stores, and four is fine. **Two copies of one skill
is the bug.** When the same skill name exists in two stores, both load, and which one wins is ambiguous.
Nothing reports this. `registry.md` is what makes it visible.

## What is here

| File | What it is |
|---|---|
| `CONVENTIONS.md` | The contract. Where a master lives, how far it reaches, the four stores, naming, provenance, packaging traps, what is not a skill. |
| `INSTALL.md` | The per-machine install runbook, plus the account store and ChatGPT. |
| `registry.md` | The catalog. One row per skill, built and declined. |
| `tools/package-skill.py` | Builds a `.skill` bundle from a master, for upload to the account store. |
| `skills/` | The masters. One folder per skill. |

## The command is `/brain-skill`

Five verbs move knowledge: capture, process, pull, maintain, digest. **`/brain-skill` turns a repeated
method into a skill.** It is backed by a vault skill named `skill-library`.

The command is named `brain-skill` and not `skill` so it does not collide with other skill-building commands
you may already have installed.

## It starts empty

`skills/` holds nothing on day one. It fills one skill at a time. An empty library is the correct state
until you have a method worth building.

The AI offers a candidate during **capture** and during **maintain**. It does not offer during pull or during
process. **The bar is high on purpose:** you will run the method again, **and** it is a business process, a
personalization, or a way of working with AI that you repeat. Minor process detail does not qualify, and
when it is a close call the AI stays silent. **`/brain-skill` with no argument sweeps on demand**, which is
the main way in.

**Building is always a deliberate act.** Nothing is written into this library without your yes. On a yes it
is built now, on the surface the session is running on.

## No git

The same rule as the vault. Dropbox syncs and versions this folder. Do not create a git repo here.
````

## File: `CONVENTIONS.md`

````markdown
# CONVENTIONS.md — the contract for the skill library

Read this file before you build a skill, install one, or package one. It is binding until the owner changes
it. It lives in the library, so it is present and current on every machine the sync reaches.

The brain holds knowledge. The library holds methods. **A skill is a verb. Knowledge is a noun.**

---

## 1. Where a master lives, and how far it reaches

**Where a master lives.** A skill that needs the brain to exist belongs in `<vault>/.claude/skills/`, so the
vault keeps installing itself. Everything else belongs in the library.

**How far it reaches.** A skill that runs a shell command, a script, or a file write works only on a surface
with disk access, which means Claude Code and Cowork. It cannot reach a chat surface, and a bundle uploaded
for one would fail there. A pure-instruction skill can reach every surface.

**Reach is a property of the skill, not a packaging choice.** Do not fight it.

This is the one place that guidance lives. Other files point here. No other file restates it.

---

## 2. The four stores, and what each one reaches

| Store | What lives there | Installed how | Reaches |
|---|---|---|---|
| **Vault `.claude/`** | The brain skills only | Copy into `~/.claude/`, per `<vault>/.claude/INSTALL.md` | Claude Code on that machine |
| **Library** | Every other master | Junction, or copy, into `~/.claude/skills/`, per `<library>/INSTALL.md` | Claude Code and Cowork on that machine |
| **Account store** | Pure-instruction skills only | Upload a `.skill` bundle through the Claude skills UI | Every Claude surface on the account: web, desktop, and mobile. No per-machine step. |
| **ChatGPT** | No skill store exists | A custom GPT built from the master, or the method pasted into an existing GPT's or Project's instructions | ChatGPT on the whole account: web and mobile |

**ChatGPT has no skill store.** The equivalent is a custom GPT, or instruction text added to an existing GPT
or Project. Either one is a copy of the master, so record the carrier and the refresh date in `registry.md`.

Only the account store syncs on its own. The vault store and the library both need a per-machine install.

### The Claude unit and the ChatGPT unit

| Claude | ChatGPT |
|---|---|
| The brain skills in `<vault>/.claude/skills/` | The **`Brain` GPT**. The main one. It is the brain client. |
| A library skill installed into `~/.claude/skills/` | A **custom GPT** built from the master, or the method added to an existing GPT |
| The account store, which syncs to every Claude chat surface | Nothing extra. **A custom GPT is already account-wide.** |

**A custom GPT needs no per-machine install and no bundle upload.** It exists on the account the moment it is
created, on web and on mobile.

**The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by
naming it. A long list of custom GPTs is hard to remember and hard to pick from, so a small method belongs
in a GPT the owner already uses.

**NOTE:** ChatGPT's features change. Check current behavior before you redesign anything around it.

### Staleness — the rule that does not soften

**The master in the library is the source of truth. A GPT's instructions are a copy.**

The copy goes stale the day the master changes, and nothing on either side reports it. This is the same
shape as the account-store upload problem in §6, with no hash to check, because a GPT's instruction text
cannot be hashed from outside.

So the record is the only control:

- **`registry.md` names every ChatGPT carrier for every skill, and the date it was last refreshed.**
- When a master changes, that table is the list of places to refresh **by hand**.
- `/brain-skill build` re-emits the artifact into `<name>.BUILD.md`, so refreshing is a paste, not a rewrite.

---

## 3. The one-store rule

**A skill lives in exactly one store.**

Four stores in the system is fine. **Two copies of one skill is the bug.** When the same name exists in two
stores, both load, and which one wins is ambiguous. Nothing anywhere reports this. There is no error, no
warning, and no log line.

`registry.md` is what makes it visible. One row per skill, one store per row. Write the row when you build
the master, not later.

---

## 4. Junction or copy

**Use a junction where the operating system allows it.** A junction makes drift structurally impossible. The
installed path and the master are the same bytes, so an edit to the master needs no reinstall.

**Copy only where a junction cannot work.** A copy is a snapshot. It drifts the moment you edit the master,
and you must redo it after every edit.

**WARNING:** junctions are **directory-only**. A lone command file is not a directory, so it must be copied,
and re-copied after every edit to the master. Keep command files thin for that reason.

The vault store copy-installs on purpose, for self-containment, and that is why the vault runbook ships a
drift check. The library prefers the junction, and needs a drift check only for the skills it copied.

---

## 5. Naming and shape of a master

A master is one folder under `<library>/skills/`.

```
<library>/skills/<name>/SKILL.md          required
<library>/skills/<name>/references/       optional
<library>/skills/<name>/scripts/          optional
<library>/skills/<name>.BUILD.md          BESIDE the folder, never inside it
```

Rules:

- **The folder name is lowercase kebab-case.** Words in lowercase, joined by single hyphens.
- **The folder name and the frontmatter `name:` must match exactly.** The packager refuses the build when
  they differ.
- **`SKILL.md` frontmatter carries `name` and `description`, and nothing else.** Both are required. Any
  other key makes the packager refuse the build. The third warning in §7 says what an extra key does on
  upload.
- **`references/` and `scripts/` are optional.** Use `references/` for material the skill reads on demand.
  Use `scripts/` for code the skill runs. A skill with a `scripts/` folder needs local execution, so it
  reaches Claude Code and Cowork only.
- **`<name>.BUILD.md` goes beside the folder, never inside it.** The packager sweeps everything under the
  skill folder into the bundle. A `BUILD.md` inside becomes context cost on every load, with no run-time
  value. The packager refuses the build when it finds one inside.

```yaml
---
name: <folder-name>
description: <one paragraph. See §9.>
---
```

The packager skips `.DS_Store`, `Thumbs.db`, and `.keep`. Everything else under the folder goes into the
bundle, so put nothing there that does not earn its place.

### What a `BUILD.md` must record

One `<name>.BUILD.md` per master. It is the operator's file, not the model's. Record all of this:

| Item | Why |
|---|---|
| **How to build** | The exact command, if the skill goes to the account store. |
| **Where it installs** | The target path on each operating system, and whether it is a junction or a copy. |
| **Which surfaces it reaches** | Written out, per §1. |
| **The ChatGPT artifact** | Only for a pure-instruction skill. The builder prompt, or the instruction block, in its own section. |
| **The SHA-256 and date of the last uploaded bundle** | Only if it goes to the account store. See §6. |
| **Any manual step** | A setting, a token, a folder to create, a permission the owner grants by hand. |

A manual step that lives only in someone's memory is a step that will be missed on the next machine.

---

## 6. Provenance — compute it, do not remember it

**The upload to the account store is the step with no safety net.** A rebuilt master that was never uploaded
leaves every chat surface serving an old version. Nothing anywhere reports the gap.

Rules:

- **Record the SHA-256 of the uploaded bundle** in that skill's `BUILD.md`, with the date.
- **Before you assume the live copy matches, rebuild and compare the hash.** The packager is deterministic.
  Two runs on an unchanged master produce byte-identical output, so the hashes agree. That makes the
  comparison a real check and not a guess.
- **Verify the published payload, not just that the upload reported success.**

---

## 7. Packaging traps — for the account store only

These apply to the account store and to nothing else. Each one is real.

**WARNING:** never build a bundle with PowerShell `Compress-Archive`. It writes backslash path separators
inside the zip. The skills UI rejects the archive with an error about characters in the path. That error
points at the file's location rather than at the bytes inside, so the wrong thing gets debugged. A Python
`zipfile` packager is immune, because `ZipInfo` rewrites the separator on write. Use
`tools/package-skill.py`.

**WARNING:** the reading tools hide the defect. Python's `zipfile.namelist()` normalizes a backslash to a
forward slash on read, and the Windows extractor accepts a backslash archive and installs it. The packager
was checked against a hand-built backslash archive. Its raw-header check returned true, while
`zipfile.namelist()` read that same archive back as `demo/SKILL.md`. **The only reliable check is the raw
local-file-header bytes, which the packager performs before it finishes.**

**WARNING:** only the frontmatter keys `name` and `description` round-trip. An extra key can make an upload
land the `SKILL.md` alone and silently drop every other file in the bundle. The packager refuses the build
when it finds any other key.

**WARNING:** watch for functional duplicates that no name collision catches. Two differently named skills
covering the same ground both load, and the model picks one. The one-line summaries in `registry.md` are how
you spot it.

### The packager

```
python tools/package-skill.py skills/<name>
```

It writes `skills/<name>.skill` beside the folder, lists the entries it packed, and prints the SHA-256.

It **refuses and exits 1** on any of these:

- a frontmatter key other than `name` or `description`
- a `name:` value that does not match the folder name
- a `BUILD.md` inside the skill folder
- a missing `SKILL.md`
- an empty folder

It skips `.DS_Store`, `Thumbs.db`, and `.keep`.

---

## 8. What is not a skill

Declining is a real outcome. **Record it as a `declined` row in `registry.md`, with the reason.** The reason
on the row stops the same candidate coming back on the next sweep.

| Decline reason | Where it belongs instead |
|---|---|
| **Three rules, not a method.** | A `CLAUDE.md`, or project instructions. |
| **Already covered by an existing skill.** | Absorb it there, where it will actually be read. |
| **A conclusion, not a method.** | That is knowledge. A wiki page. |
| **Done once, with no sign it repeats.** | Nowhere yet. Wait for the second time. |

---

## 9. Write the description for triggering

**The description is what makes the skill trigger.** The model reads it to decide whether to load the skill.
A vague description means a skill that never fires, or one that fires on the wrong work.

Write it this way:

- **Say what the skill does, in one clause.** Start with a verb.
- **List concrete trigger phrases** the owner actually types. Quote them.
- **Name the artifacts and the tools** involved: a file type, a folder, a command, a system name.
- **Say plainly when NOT to use the skill.** Name the neighbouring skill that owns that work, if there is
  one. This is the half most descriptions leave out, and it is the half that prevents a functional
  duplicate.

Keep it to one paragraph. It is the only part of the skill loaded before the decision to load the rest.
````

## File: `INSTALL.md`

````markdown
# Installing and updating the skill library on a machine

Point a Claude Code session at this file and say **"install the skill library on this machine"**. Everything
needed is here.

This file lives in the library, so it is present and current on every machine the sync reaches.

**This is a second install.** The vault installs its own skills separately, per `<vault>/.claude/INSTALL.md`.
The two stores do not overlap, and neither install covers the other.

---

## The one rule

```
<library>/skills/     SOURCE OF TRUTH. Edit here. Cloud sync carries it to every machine.
      |  junction, or copy
      v
~/.claude/skills/     INSTALLED. A junction IS the master. A copy is a snapshot that drifts.
```

**Never edit a copied skill in `~/.claude/skills/`.** An edit there is invisible to every other machine, and
the next install destroys it. Change the master in the library and reinstall.

A junction has no second copy to edit. The installed path and the master are the same bytes, so an edit to
the master needs no reinstall. That is why the junction is the default.

The library path on this machine is `{{SKILLS_PATH}}`.

---

## Install by junction (preferred)

Install one skill at a time. There is no bulk step, because each skill is a separate junction.

### Windows (PowerShell)

```powershell
$s = "{{SKILLS_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
New-Item -ItemType Junction `
  -Path   "$env:USERPROFILE\.claude\skills\<name>" `
  -Target "$s\skills\<name>"
```

The `cmd.exe` form does the same thing:

```
mklink /J "%USERPROFILE%\.claude\skills\<name>" "<library>\skills\<name>"
```

**A junction needs no administrator rights. A symbolic link does.** That is the whole reason this runbook
uses a junction. Do not substitute `New-Item -ItemType SymbolicLink`, and do not substitute `mklink /D`.
Both ask for rights you should not need for this.

**NOTE:** a junction points at a directory on a local volume. The library must be a real folder on local
disk, which it already is, because the sync folder is set to Local / "Make available offline".

To remove a junction, delete the junction itself with `Remove-Item`. Deleting the junction does not touch
the master.

### macOS and Linux

```bash
s="{{SKILLS_PATH}}"
mkdir -p "$HOME/.claude/skills"
ln -s "$s/skills/<name>" "$HOME/.claude/skills/<name>"
```

`ln -s` writes a symbolic link. It needs no elevated rights on macOS or Linux.

---

## Install by copy (the fallback)

Use a copy only where a junction or a symbolic link cannot work.

**WARNING:** a copy drifts. It is a snapshot taken at one moment. The moment you edit the master, the
installed copy is stale, and nothing reports it. **Redo the copy after every edit to the master.**

**WARNING:** junctions are directory-only. A lone command file is not a directory, so it must be copied, and
re-copied after every edit. Keep command files thin for that reason.

### Windows (PowerShell)

```powershell
$s = "{{SKILLS_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item "$s\skills\<name>" "$env:USERPROFILE\.claude\skills\" -Recurse -Force
```

### macOS and Linux

```bash
s="{{SKILLS_PATH}}"
mkdir -p "$HOME/.claude/skills"
cp -R "$s/skills/<name>" "$HOME/.claude/skills/"
```

The copy overwrites files of the same name inside that one skill folder. It does not delete anything else in
`~/.claude/skills/`.

---

## One optional per-machine setting: `SKILLS_DIR`

It goes in `~/.claude/settings.json`, **not** in the library, because the library path differs per machine.

```json
{
  "env": {
    "BRAIN_DIR":  "{{VAULT_PATH}}",
    "SKILLS_DIR": "{{SKILLS_PATH}}"
  }
}
```

**NOTE:** on Windows, JSON needs each backslash doubled, like
`"C:\\Users\\<you>\\Dropbox\\AI-Skills"`.

`SKILLS_DIR` is optional. **When it is unset, the skills resolve the library as the sibling of `BRAIN_DIR`
named `{{SKILLS_DIRNAME}}`.** Set `SKILLS_DIR` when the library is not a sibling of the vault, or when the
folder carries a different name on this machine.

If `~/.claude/settings.json` already exists, merge the `env` block into it. Do not replace the file.

---

## Verify

Open a **new** Claude Code session and confirm the installed skill is offered. A session started before the
install does not see it.

Then run the skill on real work and confirm it does what the master says. A junction that points at a folder
with no `SKILL.md` installs cleanly and does nothing.

---

## Optional: check for drift

A stale copy fails quietly. The check below makes it announce itself instead. Run it after you edit a master,
or whenever an installed skill behaves in a way the master does not explain.

A junction-installed skill always agrees, because both sides are the same bytes. **This check exists for the
skills you copied.** It also names any master with no install at all.

### Windows (PowerShell)

Paste this in whole. It prints a line per mismatch and **nothing when the two sides agree**.

```powershell
$s = "{{SKILLS_PATH}}"
$dst = "$env:USERPROFILE\.claude\skills"
Get-ChildItem -Recurse -File "$s\skills" | ForEach-Object {
  $rel  = $_.FullName.Substring("$s\skills\".Length)
  $copy = Join-Path $dst $rel
  if (-not (Test-Path $copy)) { "NOT INSTALLED: $rel" }
  elseif ((Get-FileHash $_.FullName).Hash -ne (Get-FileHash $copy).Hash) { "DIFFERS: $rel" }
}
```

`NOT INSTALLED` on every file of one skill means that master is not installed on this machine. That is a
normal state, not an error. Install it if you want it here.

`fc.exe` compares a single pair of files if you want to see the differing lines:
`fc.exe "%USERPROFILE%\.claude\skills\<name>\SKILL.md" "<library>\skills\<name>\SKILL.md"`

### macOS and Linux

```bash
diff -rq "{{SKILLS_PATH}}/skills/<name>" "$HOME/.claude/skills/<name>"
```

**NOTE:** `diff -rq` also reports files that exist only on the installed side, as `Only in ...`. Those are
fine if they come from somewhere other than the library. The PowerShell check walks the library side only,
so it ignores them.

To fix any drift, redo the copy. The master always wins. Better: replace the copy with a junction or a
symbolic link, and the drift cannot come back.

---

## The account store

The account store syncs to every Claude surface on the account: web, desktop, and mobile. **There is no
per-machine step.** It is the only store that reaches the chat surfaces.

**Only pure-instruction skills belong here.** See `CONVENTIONS.md` §1. A skill that needs a shell command, a
script, or a file write reaches Claude Code and Cowork only. A bundle uploaded to the account store would
reach the chat surfaces and fail on every one of them.

Three steps:

1. **Build the bundle.**

   ```
   python tools/package-skill.py skills/<name>
   ```

   It writes `skills/<name>.skill` beside the folder, lists the entries it packed, and prints the SHA-256.
   It refuses and exits 1 on a frontmatter key other than `name` or `description`, on a `name:` value that
   does not match the folder name, on a `BUILD.md` inside the skill folder, on a missing `SKILL.md`, and on
   an empty folder.

2. **Upload it** through the Claude skills UI.

   **WARNING:** never build the bundle with PowerShell `Compress-Archive`. It writes backslash path
   separators inside the zip, and the skills UI rejects the archive with an error about characters in the
   path. That error points at the file's location rather than at the bytes inside, so the wrong thing gets
   debugged. Use the packager. It checks the raw local-file-header bytes before it finishes.

3. **Record the SHA-256 and the date** in `skills/<name>.BUILD.md`.

   The build is deterministic, so two runs on an unchanged master produce byte-identical output and the same
   SHA-256. That turns "is the uploaded copy current?" into a hash comparison instead of a memory test.
   Rebuild, compare, and verify the published payload. Do not settle for an upload that reported success.

**A master rebuilt and never uploaded leaves every chat surface serving an old version, and nothing anywhere
reports the gap.** This is the step with no safety net.

---

## ChatGPT

**ChatGPT has no skill store.** There is nothing to install and nothing to upload.

The equivalent is a **custom GPT**, or **instruction text added to an existing GPT or Project**. Only a
pure-instruction skill reaches ChatGPT at all. See `CONVENTIONS.md` §1.

**A custom GPT is account-wide.** It needs no per-machine install and no bundle upload. It exists on the
account the moment it is created, on web and on mobile.

**The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by
naming it.

**Two branches. The AI chooses, and says which it chose and why, in one sentence.** A method worth its own
GPT gets one. Everything else goes into a GPT or Project the owner already uses.

**NOTE:** ChatGPT's features change. Check current behavior before you redesign anything around it.

### Branch A — its own custom GPT

1. **Open the ChatGPT GPT builder.**
2. **Paste the builder prompt** that `/brain-skill build <name>` generated. It is in the ChatGPT section of
   `skills/<name>.BUILD.md`.
3. **Keep the GPT private.** Do not publish it to the GPT Store.
4. **Enable the Dropbox app only when the method needs the brain.** A method that never reads the
   vault needs no app and no Step 0 protocol-loading block.
5. **Add no custom Actions.**

**WARNING:** do not upload library files or vault files as GPT Knowledge. A copy in Knowledge is a second
brain that goes stale, and it breaks the point-don't-copy rule. The GPT reads the vault at run time through
the Dropbox app.

### Branch B — added to an existing GPT or Project

1. **Open the target GPT or Project.** It is usually the `Brain` GPT.
2. **Paste the instruction block** that `/brain-skill build <name>` generated, from the ChatGPT section of
   `skills/<name>.BUILD.md`, into that GPT's or Project's instructions.

### Both branches

**The generated artifact lives in `skills/<name>.BUILD.md`.** `/brain-skill build <name>` writes it there,
and re-emits it on every rebuild. **Refreshing a ChatGPT copy is a paste, never a rewrite.**

`BUILD.md` sits beside the skill folder and never inside it, so the artifact adds no weight to a bundle.

**Record the carrier and the date in `registry.md`.** The carrier is the GPT or Project that holds the text.
The text is a copy, so it goes stale the day the master changes, and nothing on either side reports it. When
you edit a master, that table is the list of places to refresh by hand.

---

## What an install does and does not cover

| Covered | Not covered |
|---|---|
| One skill folder in `~/.claude/skills/`, per junction or per copy | `CONVENTIONS.md` and `registry.md`. Sync carries those, and no install is involved. |
| Nothing else. Each skill is installed on its own. | `SKILLS_DIR` in `~/.claude/settings.json`. Set once per machine, by hand. |
| | The account store. Build and upload a bundle instead. |
| | ChatGPT. Build the custom GPT, or paste the instruction block into the existing GPT, by hand. |

**WARNING:** installing a library skill does not install the brain skills. Those live in the vault and use
their own runbook at `<vault>/.claude/INSTALL.md`.
````

## File: `registry.md`

````markdown
# registry.md — the skill catalog

One row per skill. **This file is what makes the one-store rule visible.**

A skill lives in exactly one store. Nothing in the system reports a skill that exists in two stores. Both
copies load, and which one wins is ambiguous. There is no error and no warning. This table is the only place
the duplicate shows up, so **write the row when you build the master, not later**.

**This file also records what the owner declined, and why.** A declined row is what stops the next sweep
proposing the same thing again.

The one-line summaries do a second job. Two differently named skills covering the same ground both load, and
the model picks one. No name collision catches that. Reading the one-line column end to end does.

The contract is in `CONVENTIONS.md`. The install steps are in `INSTALL.md`.

---

## Skills

| Skill | Store | Reaches | Status | Master | One line |
|---|---|---|---|---|---|

<!-- Copy a row to add a skill. Delete nothing above it.
| example-skill-name | library | Claude Code, Cowork | installed | `skills/example-skill-name/` | What it does, in one clause. |
| example-declined-name | — | — | declined | — | Declined 2026-01-31: a conclusion, not a method. Filed as a wiki page. |
-->

### Store

| Value | Meaning |
|---|---|
| `vault` | The master is in `<vault>/.claude/skills/`. It requires the brain to exist. |
| `library` | The master is in `skills/` here. |
| `account` | The master is in `skills/` here, and a bundle is uploaded to the Claude account store. |
| `chatgpt` | No skill store exists. The method is a custom GPT, or instruction text in an existing GPT. See the table below. |

A skill in the account store still keeps its master here. `account` says where the built bundle went. It
does not mean a second master.

A `declined` row has no store. Write `—`.

### Reaches

Write the surfaces out, from the store's row in `CONVENTIONS.md` §2. For example `Claude Code` for a vault
skill, `Claude Code, Cowork` for a library skill, or `all Claude surfaces` for an account-store skill. A
`declined` row has no reach. Write `—`.

### Status

| Value | Meaning |
|---|---|
| `built` | The master exists. It is not installed on any machine. |
| `installed` | Installed on at least one machine, by junction or by copy. |
| `uploaded` | A bundle is in the account store, and its SHA-256 and date are in the skill's `BUILD.md`. |
| `declined` | The owner said no. **The one-line column carries the date and the reason.** |
| `retired` | No longer used. Kept in the table so the name is not reused by accident. |

**A declined row carries its reason, so the sweep does not propose it again.** The four common decline
reasons are in `CONVENTIONS.md` §8. Write the reason in the one-line column, with the date.

---

## ChatGPT carriers

**ChatGPT has no skill store.** A method reaches ChatGPT as its own custom GPT, or as instruction text
added to an existing GPT or Project.

Either one is a copy. **It goes stale the day the master changes, and nothing on the ChatGPT side reports
it.** **This table is the refresh list when a master changes.** Work down it by hand.

| Skill | Carrier | Kind | Last refreshed |
|---|---|---|---|

<!-- Copy this row to record a ChatGPT carrier. Delete nothing above it.
| example-skill-name | Example Research GPT | own GPT | 2026-01-31 |
-->

**Legend.** `Skill` is the master's name. `Carrier` is the custom GPT, GPT, or Project that holds the text.
`Kind` is `own GPT` when the method got its own custom GPT, or `added to` when it went into an existing
GPT or Project. `Last refreshed` is the date the text was last pasted from `skills/<name>.BUILD.md`, as
`YYYY-MM-DD`.
````

## File: `tools/package-skill.py`

````python
#!/usr/bin/env python3
"""Build a .skill bundle from a master, for upload to the Claude account store.

    python tools/package-skill.py skills/<name>

Writes <name>.skill beside the skills/ folder and prints its SHA-256.

WARNING: do not build a bundle with PowerShell Compress-Archive. It writes backslash
path separators inside the zip, and the skills UI rejects the archive with an error
about characters in the path. That error points at the file's location rather than at
the bytes inside, so the wrong thing gets debugged. This packager uses zipfile, which
always writes a forward slash, and it checks the raw header bytes before it finishes.

The build is deterministic. Entries are sorted and every timestamp is fixed, so an
unchanged master rebuilds byte-identical. That turns "is the uploaded copy current?"
into a hash comparison instead of a memory test.
"""
import hashlib
import re
import sys
import zipfile
from pathlib import Path

# Only these frontmatter keys round-trip through the skills UI. Extra keys can make an
# upload land the SKILL.md alone and silently drop every other file in the bundle.
ALLOWED_FRONTMATTER_KEYS = {"name", "description"}

FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKIP_NAMES = {".DS_Store", "Thumbs.db", ".keep"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_frontmatter(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        fail(f"{skill_md} has no YAML frontmatter block.")
    keys = set()
    for line in match.group(1).splitlines():
        found = re.match(r"^([A-Za-z0-9_-]+):", line)
        if found:
            keys.add(found.group(1))
    extra = keys - ALLOWED_FRONTMATTER_KEYS
    if extra:
        fail(
            f"{skill_md} frontmatter has keys the skills UI cannot accept: "
            f"{', '.join(sorted(extra))}. Keep only: name, description."
        )
    for required in ("name", "description"):
        if required not in keys:
            fail(f"{skill_md} frontmatter is missing the required key '{required}'.")
    name_line = re.search(r"^name:[ \t]*(\S+)[ \t]*$", match.group(1), re.MULTILINE)
    if not name_line:
        fail(f"{skill_md} has no single-word value for 'name:'.")
    return name_line.group(1)


def has_backslash_in_entry_names(raw: bytes) -> bool:
    """Scan local file headers for a backslash in the stored path.

    zipfile.namelist() normalizes a backslash to a forward slash on read, so it cannot
    see this defect. The raw bytes can.
    """
    marker = b"PK\x03\x04"
    at = raw.find(marker)
    while at != -1:
        name_length = int.from_bytes(raw[at + 26:at + 28], "little")
        start = at + 30
        if b"\\" in raw[start:start + name_length]:
            return True
        at = raw.find(marker, at + 4)
    return False


def collect(source: Path) -> list[Path]:
    files = [
        p for p in sorted(source.rglob("*"))
        if p.is_file() and p.name not in SKIP_NAMES
    ]
    if not files:
        fail(f"{source} holds no files to package.")
    return files


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: python tools/package-skill.py skills/<name>")

    source = Path(sys.argv[1]).resolve()
    if not source.is_dir():
        fail(f"{source} is not a folder.")

    skill_md = source / "SKILL.md"
    if not skill_md.is_file():
        fail(f"{source} has no SKILL.md.")

    declared = check_frontmatter(skill_md)
    if declared != source.name:
        fail(
            f"frontmatter name '{declared}' does not match the folder name "
            f"'{source.name}'. They must agree."
        )

    build_notes = source / "BUILD.md"
    if build_notes.is_file():
        fail(
            f"{build_notes} is inside the skill folder. Build notes go BESIDE it, as "
            f"{source.name}.BUILD.md, or the packager sweeps them into the bundle."
        )

    files = collect(source)
    out = source.parent / f"{source.name}.skill"

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in files:
            arcname = f"{source.name}/{path.relative_to(source).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIMESTAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, path.read_bytes())

    raw = out.read_bytes()
    if has_backslash_in_entry_names(raw):
        fail(f"{out} stores a backslash path separator. Do not upload it.")

    digest = hashlib.sha256(raw).hexdigest()
    print(f"wrote {out} ({out.stat().st_size:,} bytes, {len(files)} entries)")
    for path in files:
        print(f"  {source.name}/{path.relative_to(source).as_posix()}")
    print(f"sha256 {digest}")
    print("Record that hash and today's date in the skill's BUILD.md when you upload it.")


if __name__ == "__main__":
    main()
````

---

# Part V — Surfaces

The same protocol runs on every surface. Only the way each one reaches the files differs. The portable unit
is the **protocol in `SCHEMA.md`**, not any skill file. Each surface needs two things: access to the vault
files, and an instruction to read `SCHEMA.md` and `wiki/_conventions.md` and follow them.

| Surface | Mechanism | Verbs | Notes |
|---|---|---|---|
| Claude Code (local) | Skills and slash commands in `<vault>/.claude/`, installed by copy into `~/.claude/` | capture, process, pull, maintain, digest | The primary surface. Owns process, maintain, and digest. |
| Cowork / Claude desktop | A Project pointed at the vault, carrying a short instruction block | capture, process, pull | Can run the Option A scheduled task. |
| claude.ai chat, web and phone | Dropbox connector, plus the same instruction block in a Project | capture, pull | No process. |
| ChatGPT | A private custom GPT named `Brain` with the Dropbox app enabled | capture, pull, and process only with an approved plan | Never upload vault files as GPT Knowledge. |

## 1. Claude Code (the primary surface)

### Mechanism

The vault holds the source of truth for the skills and commands:

```
<vault>/.claude/     SOURCE OF TRUTH. Edit here. Cloud sync carries it to every machine.
      |  copy-install
      v
~/.claude/           INSTALLED COPY. Never edit. Overwritten on every install.
```

The vault ships six skills (`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`,
`audio-digest`, `brain-update`) and seven slash commands (`/capture`, `/process`, `/pull`, `/maintain`,
`/brain-skill`, `/digest`, `/brain-update`). They install into `~/.claude/` by copy, so they work from
**any** project directory, not only from inside the vault.

`.claude/scripts/` is not copied. The `audio-digest` skill calls `render-digest.py` at its vault path, so
a change to that script needs no reinstall.

**Never edit the installed copy.** An edit in `~/.claude/` is invisible to every other machine, and the next
install destroys it. Change the vault copy and reinstall.

**A protocol change needs no install.** The skills are thin. They carry the job skeleton and the
vault-resolution logic, and they point at `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the
rules. Editing `SCHEMA.md` reaches every machine and every surface through cloud sync. Reinstall only when a
skill file itself changes.

### Setup

1. **Install the skills and commands.** Follow the `.claude/INSTALL.md` template in Part III, which ships in the vault as
   `<vault>/.claude/INSTALL.md`. It holds the copy commands for Windows and for macOS/Linux, the optional
   drift check, and the verification step. Point a Claude Code session at that file and say "install the
   brain skills on this machine".

2. **Set `BRAIN_DIR`.** Add the vault path to `~/.claude/settings.json` on each machine:

   ```json
   {
     "env": {
       "BRAIN_DIR": "C:\\Users\\<you>\\Dropbox\\AI-Brain"
     }
   }
   ```

   The skills read it, so they resolve the vault from any project directory. Without it, a skill falls back
   to searching the session directories for one that holds both `SCHEMA.md` and a `wiki/` folder. That
   fallback works inside the vault and fails outside it. `BRAIN_DIR` is machine-specific, so it belongs in
   `~/.claude/settings.json` and not in the vault.

3. **Attach the vault to your other projects**, so a coding session can capture and pull without changing
   directory:

   - Per session: `claude --add-dir "<path-to-vault>"`
   - Per project: add to the project's `.claude/settings.json`:

     ```json
     { "additionalDirectories": ["<path-to-vault>"] }
     ```

4. **Optional: a brain-awareness section in `~/.claude/CLAUDE.md`.** Tell Claude the brain exists, where it
   lives, and how to behave: offer to capture durable knowledge at natural stopping points, pull from the
   wiki when a question might be covered, never compile during normal work, and never run git in the vault.
   The guided interview in the Part II writes this section for you.

### Use

Run `/process` and `/maintain` from a session with disk access to the vault. Run `/capture` and `/pull` from
anywhere, once `BRAIN_DIR` is set.

## 2. Cowork / Claude desktop

### Mechanism

Cowork has no skill files of its own. It carries the protocol in **Project instructions**. It has real disk
access to the vault, so it can run all three of capture, process, and pull. It can also run the Option A
scheduled task in Part VII (Scheduling).

### Setup

1. Create a Project pointed at the vault folder.
2. Paste this into the Project Instructions field:

> This project IS my LLM-maintained knowledge brain, plain markdown in a synced folder. Your job is to build
> and maintain it, not only to answer from it.
>
> At the start of any work here, read these vault files and treat them as your binding instructions:
> - `SCHEMA.md` — the full operating protocol: structure, the capture / process / pull / maintain workflows,
>   frontmatter, and guardrails. This is authoritative. Everything defers to it.
> - `wiki/_conventions.md` — the per-page rules.
> - `CLAUDE.md` — the short summary that points to the above.
>
> Follow whatever those files currently say. They may have changed since you last read them, so re-read
> them. Do not rely on memory.

The block carries no protocol of its own. It tells Claude to read the vault files and follow them. That is
deliberate. When the conventions change, every surface stays correct with nothing to re-sync.

## 3. claude.ai chat (web and phone)

### Mechanism

Chat reaches the vault through the **Dropbox connector**. The connector reads files and, where write access
is granted, creates them. It cannot delete or move a file on disk.

**Verbs: capture and pull only. No process.** The process step moves notes out of `inbox/` into `raw/`, and
that needs real disk access to the vault folder. A connector reaches the files over the network, so it cannot
complete the move. See Part VII (Scheduling) for the same constraint applied to scheduling.

### Setup

1. In claude.ai, open Settings, then Connectors. **Connect the Dropbox account that holds the vault.**
2. Create a Project for brain work, and paste the same instruction block from section 2 into its Project
   Instructions. Write the paths as the connector sees them, for example `/AI-Brain/SCHEMA.md`.
3. **Pull:** ask "what does my brain say about X?". Claude reads the pages under `wiki/` and cites them.
4. **Capture:** say "capture this to the brain". Claude creates one note in `inbox/` and reports the created
   path.

The phone uses the same setup. The claude.ai mobile app carries the connector and the Project, so capture and
pull work from anywhere.

## 4. ChatGPT

ChatGPT connects as a **private custom GPT named `Brain`** with the Dropbox app enabled. It pulls with
citations, captures one note per request into `inbox/`, and may process **only** after it presents a complete
mutation plan and you approve it. Never upload vault files as GPT Knowledge. The full setup, the builder
prompt, and five preview tests are in Part VIII (ChatGPT).

An owner who uses ChatGPT and no Claude surface gets the whole loop from that one GPT. It offers to build a
skill when a capture is a repeatable method, and its **BUILD** verb writes the master into the library on a
yes. See section 3 of Part VIII (ChatGPT).

## Skill reach — how a skill gets to each surface

A skill is a method, not knowledge, so it does not travel through the vault. It reaches a surface through
a **store**, and each store reaches a different set of surfaces. This table is the reach summary. The rules
live in Part VI (The skill library) and in `<library>/CONVENTIONS.md`.

| Surface | How a skill gets there | Per-machine step |
|---|---|---|
| Claude Code (local) | The brain skills install from `<vault>/.claude/` **by copy**. Every other skill installs from the library **by junction, or by copy where a junction cannot work**. | Yes, on each machine |
| Cowork / Claude desktop | The same library install reaches it. No second install. | Yes, the library install above |
| claude.ai chat, web and phone | The **account store** only. Upload a `.skill` bundle through the Claude skills UI. **Only pure-instruction skills belong there.** A skill that runs a shell command, a script, or a file write fails on every chat surface. | **No.** This is the one store with no per-machine step. |
| ChatGPT | **There is no skill store.** The unit is a **custom GPT** built from a generated builder prompt, or the method added as an instruction to an existing GPT or Project. The `Brain` GPT chooses between the two by judgment and says which it chose. | **No per-machine step.** A custom GPT is account-wide the moment it is created. The owner refreshes its instructions by hand whenever the master changes. |

Four limits are worth stating plainly, because they are easy to overclaim.

- **Only the account store is automatic on Claude.** It syncs to every Claude surface on the account, web,
  desktop, and mobile. Every other Claude store needs an install on each machine.
- **ChatGPT has no skill store.** The unit is a custom GPT built from a generated builder prompt, or the
  method added as an instruction to an existing GPT or Project. A skill that runs a shell command, a script,
  or a file write cannot reach ChatGPT at all. `<library>/CONVENTIONS.md` states where a master lives and how
  far it reaches.
- **A custom GPT needs no per-machine install**, and it is account-wide the moment it is created, on web and
  on mobile. But **the owner picks the GPT. The model does not select it.** A Claude skill is chosen by the
  model from its description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is
  reached by naming it. That is why a small method goes into an existing GPT's instructions instead of a GPT
  of its own.
- **A custom GPT does not stay in sync with its master.** Its instructions are a copy the owner refreshes by
  hand, and nothing on either side reports the gap. The library's `registry.md` records every ChatGPT carrier
  for every skill, and the date each one was last refreshed.

For the rest — where a master lives, how far it reaches, the one-store rule, junction versus copy,
provenance, and the packaging traps — read Part VI (The skill library) and `<library>/CONVENTIONS.md`. Do not restate
those rules in a client's instructions. Point at them.

## Digest reach — writing one, and listening to one

Writing a digest and playing one are different jobs, and they land on different surfaces.

| Surface | Write a digest | Play one |
|---|---|---|
| Claude Code (local) | Yes, script and MP3. It owns this verb. | Not the point. |
| Cowork / Claude desktop | Yes, if it can run the script. Otherwise the markdown only, with `audio: none`. | Yes, either way. |
| claude.ai chat, web and phone | Markdown only, through the connector. No MP3 — there is no shell. | **Yes. This is the listening surface.** |
| ChatGPT | Markdown only, same reason. | Yes, read aloud from the file. |

**The chat and ChatGPT clients ship wired for capture and pull only.** Writing a digest from those surfaces
is possible, not configured: the owner asks for it in so many words, and gets the markdown without an MP3.
Claude Code owns this verb, and that is where it belongs.

**Reading one aloud on the phone.** Open the file and read the body **verbatim from the marker comment**.
Never summarize it — the script is already the summary, and summarizing it again strips the reasoning that
is the whole point.

That instruction lives **inside the file**, as an HTML comment above the body. It is there because claude.ai
and Claude desktop silently discard the MCP `instructions` field, and connector review forbids behavioral
steering in a tool description. The inside of the file is the only channel that reliably reaches a phone.

**Hands-free, play the MP3 from the Dropbox app instead.** It needs no assistant and no network beyond the
sync.

`digests/_catalog.md` is the index, newest first, and each entry's `about:` line is written for how the
owner would ask for it out loud — *"the one about the server thing"*.

## The rules that span all surfaces

**Point, don't copy.** The client instructions carry the workflow skeleton. The rules are read from the vault
at run time. A client that copies a rule inline goes stale the day the vault changes.

**Re-read before acting.** Every surface re-reads `SCHEMA.md` and `wiki/_conventions.md` before it acts on
the brain, and treats them as binding. Memory of the protocol is always stale. The files are always current.

---

# Part VI — The skill library

This document explains the skill library: what it is, why it sits beside the vault, and what the system does
with a method you keep repeating. Read it if you are deciding whether you want this part of the kit.

The library is optional. The brain works without it.

The binding contract lives in the library itself, at the `CONVENTIONS.md` template in Part IV. **That file is the rule.**
This document explains the shape. Where they disagree, the contract wins.

---

## 1. The idea

**A skill is a verb. Knowledge is a noun.**

The wiki holds the nouns: facts, decisions, findings, corrected claims. The library holds the verbs: the
methods you would otherwise explain again in every new session.

Working with the brain surfaces those methods. The same recipe gets explained again. The same checklist gets
rebuilt from scratch. The same steps get pasted into a new session, a little differently each time. The
system should notice and offer to turn one into a skill.

## 2. Where the library sits

The library is a **sibling of the vault**, in the same synced folder. The default name is `AI-Skills`.

```
~/Dropbox/
  AI-Brain/                    the vault. Knowledge.
  AI-Skills/                   the library. Methods.
    README.md                  what this is, and the one-store rule
    CONVENTIONS.md             the contract
    INSTALL.md                 per-machine install. Junction or copy.
    registry.md                the catalog. Built and declined.
    tools/package-skill.py     builds a .skill bundle for the account store
    skills/<name>/SKILL.md     a master. Bundle contents only.
    skills/<name>.BUILD.md     build and install notes, BESIDE the folder, never inside it
```

**Why the library is not inside the vault.** A tool is not knowledge. Putting methods inside a knowledge
base blurs what the brain is.

**`BUILD.md` goes beside the skill folder, never inside it.** The packager sweeps everything under the skill
folder into the bundle. A `BUILD.md` inside becomes context cost on every load, with no run-time value.

## 3. Where a master lives, and how far it reaches

A skill that needs the brain to exist stays in `<vault>/.claude/skills/`, so the vault keeps installing
itself. Everything else goes in the library.

A skill that runs a shell command, a script, or a file write works only where there is disk access, which
means Claude Code and Cowork. A pure-instruction skill can reach every surface.

**the `CONVENTIONS.md` template in Part IV §1 is the binding version of that guidance.** Read it there before you build.

## 4. The offer

**The AI proposes. It never builds silently.**

Two moments, and nowhere else:

- **capture** — you are present and have just decided something is worth keeping. If it is a method, now is
  the moment to ask.
- **maintain** — you are deliberately looking for improvements, so a sweep belongs here.

**Never at process.** Process runs nightly and unattended. An offer there would never be seen by anyone, and
a scheduled run must not stop to ask a question.

**Never at pull.** Pull answers a question. An offer there interrupts the answer.

The third way in, and the main path: **`/brain-skill` with no argument sweeps on demand**, when you ask for
it.

### The signal is a judgment, and the bar is high on purpose

Two things must both be true. A method that clears only the first one is not a candidate.

> **1. It is a method you will run again.**
> **2. It is worth a maintained artifact.**

A skill is a real cost. It is a file you keep current, install on each surface, and stop from going
stale. Most captured steps are not worth that. **Do not offer for minor process detail.**

Gate 2 is met when the method is one of three kinds. **Name the kind in the offer.** If you cannot name one,
do not offer.

- **A business process you run** — how you quote, onboard, review, invoice, or ship.
- **A personalization** — how you want work done: your standards, your format, your voice.
- **A way of working with AI you repeat** and that saves you time.

**When in doubt, stay silent.** The two costs are not equal. A missed candidate is recoverable, because
`/brain-skill` sweeps for it later. A wrong offer is an interruption that cannot be taken back.

Do not offer when the content is a fact, a finding, a reference, a decision, or a corrected claim. Those are
knowledge, a decision included, which can feel active but records what was chosen rather than how to do
something. Do not offer for one-off troubleshooting, for a setup done once for one machine or one artifact,
or for a short sequence with no judgment in it that any assistant would get right without a skill. Stay
silent when `registry.md` shows you already declined it.

Three examples that fix the line:

- A note on **how you set up every project spreadsheet, in your standard layout** is a personalization
  you repeat. **Offer.**
- A note on **the steps that fixed one broken build last week** is written as steps, but it is a one-off.
  **Say nothing.**
- A note on **what an article about giraffes said** is knowledge, not a method. **Say nothing.**

### The volume rules, and they are strict

- **One offer per candidate per session.**
- **The offer is one line, after the work finishes.** It never blocks or delays the capture.
- **Never build without a yes.**
- **A declined candidate is recorded in `registry.md` with its reason, and is not raised again.**

## 5. What a yes does — build now, on this surface

**No inbox note. No queue. No second command.** You are present and you said yes.

Two things happen, in this order:

1. **The master is written** to `<library>/skills/<name>/SKILL.md`, with `<name>.BUILD.md` beside the folder,
   and a row is added to `<library>/registry.md`. **The master is written in every case, on every surface.**
   It is the durable copy, and it is what lets the method reach other surfaces later.
2. **It is installed in whatever form this surface supports.** Then the AI says plainly what was installed
   and what you still have to do by hand.

| Surface | The installed form |
|---|---|
| Claude Code, Cowork | A skill, installed into `~/.claude/skills/` per `<library>/INSTALL.md` |
| claude.ai chat | No install from chat. A bundle is built for the account store for you to upload, or the method is added to a Project's instructions. |
| ChatGPT | A custom GPT built from a generated builder prompt, or the method added to an existing GPT's or Project's instructions |

The rule, rather than a taxonomy: **install it the way this surface installs a method.** If the surface
has no mechanism for that, say so and produce the artifact you can install by hand.

A build also appends an entry to `<vault>/wiki/_log.md`, recording what was built. That is the "what changed"
record. Nothing else writes into `wiki/` outside of process.

### The memory trap

Some surfaces offer only a **memory** feature. A memory entry is an acceptable *installed form*. It is
**never** the artifact.

**Per-surface memory does not travel between surfaces and is not durable**, which is the exact problem this
whole system exists to fix. The master goes in the library. The memory entry is a local copy. **Never store a
method only in a surface's memory and call it saved.**

## 6. `/brain-skill` and its three modes

Five verbs move knowledge: capture, process, pull, maintain, digest. **`/brain-skill` turns a repeated
method into a skill.** It is backed by a vault skill named `skill-library`.

The command is named `brain-skill` and not `skill` so it does not collide with other skill-building commands
you may already have installed.

1. **`/brain-skill` with no argument — sweep on demand.** It scans recent wiki pages and recent `_log.md`
   entries for methods you follow by hand, skips anything `registry.md` already records as built or declined,
   and proposes what is left. **It builds each accepted candidate immediately.** It writes nothing without a
   yes.
2. **`/brain-skill build <name>` — build one named method now.** It writes the master, writes
   `<name>.BUILD.md` beside the folder, adds the registry row, appends to `_log.md`, and installs the skill
   in the form this surface supports. For a pure-instruction skill it also emits the ChatGPT artifact into
   `<name>.BUILD.md`: a builder prompt for a new custom GPT, or an instruction block for an existing GPT or
   Project. It says which it chose and why, in one sentence. Because the artifact is regenerated on every
   build, refreshing a ChatGPT copy is a paste, not a rewrite.
3. **`/brain-skill install` — install the library on this machine** per `<library>/INSTALL.md`. It then
   reports which skill reaches which surface, and names any master with no install.

## 7. The rules that keep the library honest

**The one-store rule.** A skill lives in exactly one store. Four stores in the system is fine. **Two copies
of one skill is the bug.** When the same name exists in two stores, both load, and which one wins is
ambiguous. There is no error, no warning, and no log line. `registry.md` is what makes it visible: one row
per skill, one store per row.

**Junction over copy.** Use a junction where the operating system allows it. A junction makes drift
structurally impossible, because the installed path and the master are the same bytes. A copy is a snapshot
that drifts the moment you edit the master, and you must redo it after every edit. **Junctions are
directory-only.** A lone command file is not a directory, so it must be copied and re-copied. On Windows a
junction needs no administrator rights, and a symbolic link does. On macOS and Linux `ln -s` needs no
elevated rights. The exact commands are in the `INSTALL.md` template in Part IV.

**Provenance — compute it, do not remember it.** The upload to the account store is the step with no safety
net. A rebuilt master that was never uploaded leaves every chat surface serving an old version, and nothing
anywhere reports the gap. The kit ships the `tools/package-skill.py` template in Part IV, and its build is
**deterministic**: two runs on an unchanged master produce byte-identical output with the same SHA-256. That
determinism is what makes the check real. Record the SHA-256 of the uploaded bundle in that skill's
`BUILD.md`, with the date. Before you assume the live copy matches, rebuild and compare the hash. **Verify
the published payload, not just that the upload reported success.**

### Packaging traps

These apply to the account store and to nothing else. Each one is real.

**WARNING:** never build a bundle with PowerShell `Compress-Archive`. It writes backslash path separators
inside the zip. The skills UI rejects the archive with an error about characters in the path. That error
points at the file's location rather than at the bytes inside, so the wrong thing gets debugged. A Python
`zipfile` packager is immune, because `ZipInfo` rewrites the separator on write.

**WARNING:** the reading tools hide the defect. Python's `zipfile.namelist()` normalizes a backslash to a
forward slash on read, and the Windows extractor accepts a backslash archive and installs it. The packager
was checked against a hand-built backslash archive. Its raw-header check returned true, while
`zipfile.namelist()` read that same archive back as `demo/SKILL.md`. **The only reliable check is the raw
local-file-header bytes, which the packager performs before it finishes.**

**WARNING:** only the frontmatter keys `name` and `description` round-trip. An extra key can make an upload
land the `SKILL.md` alone and silently drop every other file in the bundle. The packager refuses the build
when it finds any other key.

**WARNING:** watch for functional duplicates that no name collision catches. Two differently named skills
covering the same ground both load, and the model picks one. The one-line summaries in `registry.md` are how
you spot it.

The packager also refuses a `name:` value that does not match the folder name, a `BUILD.md` inside the skill
folder, a missing `SKILL.md`, and an empty folder. It skips `.DS_Store`, `Thumbs.db`, and `.keep`.

## 8. What is not a skill

Declining is a real outcome. The reason goes on a `declined` row in `registry.md`, so the next sweep does not
propose the same thing again. Four common reasons:

- **Three rules, not a method.** Put it in a `CLAUDE.md`, or in project instructions.
- **Already covered by an existing skill.** Absorb it there, where it will actually be read.
- **A conclusion, not a method.** That is knowledge. It belongs on a wiki page.
- **Done once, with no sign it repeats.** Wait for the second time.

An empty library is the correct state until you have a method worth building.

## 9. What this does not promise

Six honest limits. Read them before you rely on any of this.

- **The offer is a judgment, not a guarantee.** It will miss methods. It will sometimes propose one you do
  not want. Declining is cheap, and the reason gets recorded.
- **Reach is bounded, and ChatGPT has no skill store.** A method reaches ChatGPT as a custom GPT, or as
  instruction text inside an existing GPT or Project, and nothing else.
- **The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
  description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by naming
  it. ChatGPT's features change, so check current behavior before you design around it.
- **A GPT's or a Project's instructions are a copy that a human refreshes.** They do not stay in sync with
  the master. Nothing on the ChatGPT side reports the gap, and the text cannot be hashed from outside, so
  `registry.md` and a hand refresh are the only control.
- **A skill does not sync when it needs a per-machine install.** The account store is the only Claude store
  that syncs by itself. The vault store and the library are both per machine, so a skill in either one is not
  on your other machine until you install it there.
- **The uploaded bundle is not checked for you.** Nothing reports a master that was rebuilt and never
  uploaded. The hash in `BUILD.md` is the only record, and you write it.

---

## Where to look next

| File | What it is |
|---|---|
| the `CONVENTIONS.md` template in Part IV | The contract. Binding. |
| the `INSTALL.md` template in Part IV | The per-machine runbook, the account store, and ChatGPT. |
| the `registry.md` template in Part IV | The catalog. Built and declined, and the one-store rule made visible. |
| Part V (Surfaces) | Per-surface wiring for the brain itself. |

---

# Part VII — Scheduling the compile

The brain maintains itself only if the inbox is processed regularly. This doc ranks three ways to do that,
and states the real failure mode of each.

## The binding constraint

The process step **moves** notes out of `inbox/` and into `raw/`. It deletes files from the vault folder on
disk. So the job must run on a surface with **native disk access to the vault**, with the vault folder set
to Local / "Make available offline".

A cloud runner cannot do it. A connector cannot do it. Both can read the vault, and neither can complete the
move. Do not schedule the compile anywhere that reaches the vault only over the network.

Failure is not destructive. If a run errors before it does work, no notes move and the inbox stays intact.
The next run catches up.

## Option A (recommended) — a scheduled task in the Claude desktop app

Point a Cowork project at the vault folder, then create a scheduled task in that project. A prompt like this
works:

```text
Every night at 2:00 AM, process the brain inbox. Read SCHEMA.md and wiki/_conventions.md first, apply the
process-inbox protocol to every note in inbox/, and summarize what you filed and what you left.
```

This is the simplest option. It uses the login the app already has, so there is no token to create and no
script to maintain. It runs with real disk access, so the move into `raw/` works.

**NOTE:** the task needs the app running when it is due. If the app is closed at that time, the run happens
at next launch, not on time. On a machine you never shut down, that gap is rare. On a laptop that sleeps or
closes each night, the compile drifts to whenever you next open the app.

Pick this option when the desktop app runs on a machine that stays on.

## Option B — OS scheduler plus headless Claude Code

An OS scheduler starts a headless `claude -p` run on a fixed clock. It survives reboots and needs no app
window. This is the most durable option once it works.

**WARNING:** a headless run does **not** inherit the interactive login. It prefers `ANTHROPIC_API_KEY` over
a subscription session, so a task that works by hand can fail every night with no obvious error. **This auth
path is the most common silent failure of this option.**

The fix, once, before you schedule anything:

1. Run `claude setup-token`. It generates a long-lived OAuth token on your existing subscription. It adds no
   billing.
2. Store the result in the environment variable `CLAUDE_CODE_OAUTH_TOKEN`, for the OS account the scheduled
   task runs as.
3. Run the wrapper by hand once, as that account, and confirm it completes.

**NOTE:** an environment variable holds the token in plaintext inside the trust boundary of that OS account.
Anyone with the account has the token.

### The pieces (any OS)

1. **The auth token**, per the warning above.
2. **A wrapper script** that changes to the vault directory, runs the compile prompt, and appends output to
   a log file.
3. **A scheduler entry** that runs the wrapper nightly. 2:00 AM is a good default. It is after the workday
   and before the next one.

The core command:

```
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions
```

`--permission-mode bypassPermissions` is required. An unattended run would otherwise stall on approval
prompts for file moves and edits. It is scoped to a vault of your own notes. Keep the prompt narrow.

### Windows — Task Scheduler

Wrapper `process-inbox.ps1`. Adjust the paths.

```powershell
Set-Location "C:\Users\<you>\Dropbox\AI-Brain"
$log = "C:\Users\<you>\.claude\brain\logs\process-$(Get-Date -Format yyyy-MM).log"
"`n===== $(Get-Date -Format s) =====" | Out-File $log -Append -Encoding utf8
& "$env:USERPROFILE\.local\bin\claude.exe" -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions *>> $log
```

Set the token once with `setx CLAUDE_CODE_OAUTH_TOKEN "<token>"`.

Task settings that matter:

| Setting | Value | Why it matters |
|---|---|---|
| Trigger | Daily at 2:00 AM | After the workday, before the next |
| Action | `powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "<path>\process-inbox.ps1"` | Runs the wrapper with no window |
| Run only when user is logged on | Yes | Interactive logon, so the user environment variable with the token is picked up |
| Run task as soon as possible after a scheduled start is missed | Yes (`StartWhenAvailable`) | Catches up after the machine was off |
| Wake the computer to run this task | Optional | Useful on a machine that sleeps |
| Stop the task if it runs longer than | 1 hour | Stops a hung run |
| If the task is already running | Do not start a new instance | Stops two runs touching the same notes |

### macOS — launchd (or cron)

Wrapper `process-inbox.sh`. Make it executable and adjust the paths.

```bash
#!/bin/bash
export CLAUDE_CODE_OAUTH_TOKEN="<token>"   # or source it from a protected file
cd "$HOME/Dropbox/AI-Brain" || exit 1
LOG="$HOME/.claude/brain/logs/process-$(date +%Y-%m).log"
mkdir -p "$(dirname "$LOG")"
echo -e "\n===== $(date -Iseconds) =====" >> "$LOG"
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions >> "$LOG" 2>&1
```

Schedule it with a launchd user agent at `~/Library/LaunchAgents/com.brain.process.plist`, using
`StartCalendarInterval` at Hour 2, Minute 0. launchd runs missed jobs on wake. cron does not.

Plain cron also works on any Unix if the machine is reliably awake:

```
0 2 * * * /path/to/process-inbox.sh
```

## Option C — manual cadence

Use this when you have no always-on machine. The compile does not have to be nightly. It has to be regular.

The full fallback policy, all four parts:

1. **Once a day, at the end of any day you captured something.** Run `/process` in the vault. A handful of
   notes takes a minute or two.
2. **Whenever the inbox gets large.** Rule of thumb: **10 or more notes, or any note older than 3 days.**
   Process at either threshold, even on a day you captured nothing.
3. **A recurring reminder** in a calendar or a task app, so step 1 does not depend on memory.
4. **A session-start nudge.** Ask any brain-aware session to check the inbox size and to offer to process
   when it crosses the threshold above.

The failure mode, stated plainly: the inbox tolerates lag. **Nothing is lost while notes wait.** What breaks
the system is **never** processing. The wiki stops growing, and pulls go stale because the newest knowledge
is still sitting unfiled.

Pick the cadence you will actually keep.

## Maintain has a cadence too, and it is slower

The compile is the job that must be regular. **`/maintain` is the one that must merely happen** — monthly is
plenty for most vaults.

It does two things on a clock. It lints the wiki, which matters more the more pages there are. And it moves
digests older than 60 days out of the `digests/` root into `digests/heard/`. **Nothing is deleted.**

**Skipping it costs nothing immediate.** A stale link stays a stale link, and an aged digest just sits in the
root. So do not schedule it alongside the nightly compile. Run it by hand when you are deliberately looking
at the brain rather than using it, which is also the moment a skill sweep belongs.

If you do want it scheduled, use the same option you picked above, on a monthly trigger. `/maintain` asks
questions — contradictions and skill candidates need your judgment — so an unattended run leaves those in the
report and fixes only what is safe.

## Whichever option: verify the loop monthly

Open `wiki/_log.md` about once a month and check two things.

- **`process` entries at your expected cadence.** Silence in the log means the schedule broke. The common
  causes are an expired token, a moved vault path, and a renamed or disabled task.
- **`flag` entries.** Each one is a note the run could not place. It waits for your decision on where it
  belongs.

---

# Part VIII — ChatGPT (optional)

If you also work in ChatGPT, wire it up as a **client** of the same brain.

## 1. The integration model

**ChatGPT is a client of the brain, not another brain.** The markdown files in the vault are authoritative.
ChatGPT memory, chat history, project memory, and GPT Knowledge are working context only. When any of them
disagrees with the vault, the vault wins.

The recommended integration is a **private custom GPT named `Brain`** with the Dropbox app enabled. It
supports four verbs:

| Verb | What it does | Authorization |
|---|---|---|
| **PULL** | Answers from the live wiki, with citations to the pages used | None needed. It only reads. |
| **CAPTURE** | Writes one filing-neutral note to `inbox/` | The capture request itself, for that one note |
| **PROCESS** | Compiles the inbox into the wiki | An approved mutation plan, every time |
| **BUILD** | Writes a repeated method into the library as a master, then prints the ChatGPT artifact | Your yes to the build offer, or an explicit build request |

Local Claude Code and the nightly job still own routine processing and maintenance. **ChatGPT PROCESS is a
manual convenience, not a replacement for the nightly compile.**

**If you use ChatGPT and no Claude surface, the `Brain` GPT carries the whole loop**, including BUILD.
Section 3 explains what a skill looks like in ChatGPT.

The design rule for the GPT instructions is **point, don't copy**. The instructions carry the workflow
skeleton. The rules are read from the vault at run time. A copied rule goes stale the day the vault changes.

## 2. One-time setup

1. In ChatGPT, open Settings, then Apps / Connected apps. **Connect the Dropbox account that holds the
   vault.** Confirm the GPT can read the vault, and can create files if writes are supported.
2. Create a new custom GPT named `Brain`. Keep it **private**. Do not publish it to the GPT Store.
3. Paste the builder prompt in section 6. Replace these three placeholders first:

   | Placeholder | Replace it with |
   |---|---|
   | `<VAULT>` | The vault path as Dropbox sees it, for example `/AI-Brain` |
   | `<LIBRARY>` | The skill library path as Dropbox sees it, for example `/AI-Skills` |
   | `<OWNER>` | Your name |

   **WARNING:** the library is a **second folder**, beside the vault. The Dropbox app must reach it as well
   as the vault, or BUILD cannot write. If you do not use the skill library, delete the SKILL OFFER section
   and the BUILD section from the pasted instructions.
4. **Do not upload vault files as GPT Knowledge.** A Knowledge copy is a second brain that goes stale
   silently.
5. **Do not configure custom Actions**, unless the Dropbox app is unavailable and you deliberately choose a
   replacement integration.
6. Optionally create a ChatGPT Project to group long brain sessions. Project memory is still not the brain.
   The same vault and the same protocol apply inside it.

## 3. Skills in ChatGPT — the custom GPT is the unit

The brain holds **knowledge**. A repeated method is not knowledge, it is a **skill**. Skills live in a
**library**, a second synced folder beside the vault. Part VI (The skill library) explains the concept, and
`<library>/CONVENTIONS.md` is the binding contract.

**ChatGPT has no skill store.** It has **custom GPTs**. That is the unit a method becomes here.

| Claude | ChatGPT |
|---|---|
| The brain skills in `<vault>/.claude/skills/` | The **`Brain` GPT**. The main one. It is the brain client. |
| A library skill installed into `~/.claude/skills/` | A **custom GPT** built from the master, or the method added to an existing GPT |
| The account store, which syncs to every Claude chat surface | Nothing extra. **A custom GPT is already account-wide.** |

### The advantage

**A custom GPT is account-wide the moment you create it.** There is no per-machine install and no bundle to
upload. It works on the web and on mobile. A Claude library skill needs an install on every machine, so this
is a real advantage.

### The cost

**The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by naming
it.

That cost is why **one custom GPT per skill is wrong**. A long list of custom GPTs is hard to remember and
hard to pick from.

### Which form the method takes

The `Brain` GPT chooses by judgment and says which it chose and why, in one sentence. A method that owns a
whole conversation is worth its own custom GPT. A method that is a step or a rule inside other work goes
into the instructions of an existing GPT or Project, usually the one where that work already happens.

**A method that runs a shell command, a script, or a file write cannot reach ChatGPT at all.** It needs a
surface with disk access. `<library>/CONVENTIONS.md` states where a master lives and how far it reaches.
Record which form you chose, and where the text landed, in `<library>/registry.md`.

**A custom GPT that reads the brain needs the Dropbox app enabled**, the same as the `Brain` GPT, and it
carries the same Step 0 protocol-loading block. A custom GPT that does not touch the brain needs neither.

The `Brain` GPT stays the **brain client**. It pulls, captures, processes, and builds. It **does not become a
general skill runner.**

### Staleness — the rule that must not be softened

**The master in the library is the source of truth. A GPT's instructions are a copy.**

The copy goes stale the day the master changes, and nothing on either side reports it. A GPT's instruction
text cannot be hashed from outside, so there is no check to run. The only control is the record.
`<library>/registry.md` names every ChatGPT carrier for every skill, and the date it was last refreshed. When
a master changes, that table is the list of places to refresh **by hand**. BUILD re-emits the artifact, so a
refresh is a paste and not a rewrite.

## 4. The four verbs

### PULL

```text
@Brain Pull from the brain: <question>
```

The GPT reads `wiki/_conventions.md`, orients with `wiki/_index.md`, fetches the relevant pages under
`wiki/`, follows canonical wikilinks, and answers **with citations to the specific pages used**. It says
plainly when the wiki does not cover the question. It separates brain knowledge, external research, and its
own inference.

It must never claim something is in the brain because it appears in the chat or in ChatGPT memory.

### CAPTURE

```text
@Brain Capture the durable context from this conversation.
```

**Capture authorization is narrow and low-friction.** An explicit "capture this", "save this to the brain",
"add this to the inbox", or an accepted capture offer **is** the authorization to create that one inbox
note.

The GPT must not add a second conversational approval turn on top of it. If the platform shows its own
permission UI, use that UI and do not stack a second approval on it.

The authorization covers **that one note**. It does not cover process, maintenance, deletes, moves, wiki
edits, a BUILD, or any other write.

The GPT claims success **only after the connector confirms the file was created**, then reports the exact
path. If the write fails, it gives you the intended filename and the complete note text, so you can save it
by hand.

Capture is reversible on purpose. The note sits in `inbox/` until process time, so you can edit or delete a
mistaken capture before it is filed.

### PROCESS

```text
@Brain Process the brain inbox. Show me the filing plan first.
```

ChatGPT may process when the Dropbox app exposes the read, write, and move operations it needs. **It must
present a complete mutation plan and get your explicit approval before any canonical change.**

The plan must list all of this:

- pages to create or update
- the lifecycle folder for each page
- the `identity` value for each page
- the controlled subject tags
- the canonical links between pages
- the source-note moves into `raw/`
- the `_index.md` changes
- the `_log.md` entries
- anything left in the inbox, with the reason

After approval, the GPT executes the live rules in `SCHEMA.md` §6b. **Local or nightly processing stays the
normal path.** Use ChatGPT PROCESS when you want to review a filing decision by hand.

### The build offer

**The offer fires at capture, and during a maintenance pass if you ask this GPT for one. It never fires at
pull, and never at process.** Those two are answering a question and running a compile, and an offer there
interrupts work you did not stop.

**The bar is high on purpose, and two gates must both hold.** You will run the method again, **and** it is
worth a maintained artifact. Only three kinds clear the second gate, and the offer names which one:

- **A business process you run** — how you quote, onboard, review, invoice, or ship.
- **A personalization** — how you want work done: your standards, your format, your voice.
- **A way of working with AI that you repeat** and that saves you time.

**Minor process detail does not qualify**, nor does one-off troubleshooting, nor a fact, a finding, a
reference, a decision, or a corrected claim. **When in doubt, it stays silent.** A missed candidate is
recoverable through a later sweep. A wrong offer is an interruption that cannot be taken back.

Three examples fix the line.

- A note on **how you set up every project spreadsheet, in your standard layout** — a personalization you
  repeat. **Offer.**
- A note on **the steps that fixed one broken build last week** — steps, but a one-off. **Say nothing.**
- A note on **what an article about giraffes said** — knowledge, not a method. **Say nothing.**

The rules on the offer are strict:

- **The offer is one line, after the work finishes.** It never blocks or delays the capture.
- **One offer per candidate per session.**
- **Never build without a yes.** An offer writes nothing by itself.
- A declined candidate is recorded in `<LIBRARY>/registry.md` with its reason, and is not raised again.

**A yes runs BUILD now.** There is no queue, no inbox note, and no second command.

### BUILD

```text
@Brain Build the <name> skill.
```

BUILD writes the **master** to `<LIBRARY>/skills/<name>/SKILL.md`, with `<name>.BUILD.md` beside the skill
folder and never inside it, and adds or updates the row in `<LIBRARY>/registry.md`. It appends one entry to
`<VAULT>/wiki/_log.md` recording what was built. **The master is written in every case.** It is the durable
copy, and it is what lets the method reach other surfaces later.

Then it prints **one** artifact, headed by a line naming its source master and the date:

- a **builder prompt** for a new private custom GPT, or
- an **instruction block** to paste into an existing GPT or Project.

It chooses by judgment, per section 3, and says which it chose and why in one sentence. You paste the
artifact into ChatGPT by hand. That step is manual either way.

**A capture authorization does not authorize a BUILD.** A yes to a capture offer creates one inbox note and
nothing else.

**WARNING:** the library is a **second folder**, so the Dropbox app must reach it as well as the vault. If
the app cannot write to the library, the GPT says so and gives you the complete file contents to save by
hand. **It must never claim a write it did not make.**

Saving the master by hand is a normal outcome, not a failure.

## 5. The capture note format

A capture writes one file to `<VAULT>/inbox/YYYY-MM-DD-HHMM-<short-slug>.md`, using your current local time.
It starts with a single `context:` line saying where the note came from and what it is about. The content
follows as clean markdown. **No frontmatter. No filing decision. No wiki edit.**

**Make the note self-sufficient.** The note will be filed later, on a different machine, by a run that can
see only the vault. Write down the substance itself. Do not write a pointer to a repo, a branch, a
transcript, or a URL that only this machine or this chat can reach. Cite those as provenance **in addition
to** the content, never instead of it.

A note from ChatGPT is a clear case. The run that files it cannot open the conversation it came from. If the
note says "see the chat above", the note is unfileable.

```markdown
context: ChatGPT conversation about API rate limiting for the acme project, 2026-08-28.

The chosen approach is a token bucket at the edge, 100 requests per minute per key.
A fixed window was rejected because it allows a 2x burst across the window boundary.

Open item: the burst allowance for internal keys is not decided yet.
```

## 6. The builder prompt

Paste this into the GPT builder. Replace `<VAULT>`, `<LIBRARY>`, and `<OWNER>` first, per the table in
section 2.

```text
Create or update a private custom GPT with the following configuration.

NAME
Brain

DESCRIPTION
Pulls trusted context from <OWNER>'s Dropbox brain, captures durable knowledge into its inbox, processes the
inbox when explicitly asked and after an approved plan, and builds a repeated method into the skill library
when <OWNER> says yes.

PRIVACY
Keep this GPT private. Do not publish it to the GPT Store.

TOOLS
Enable Apps and select Dropbox when available.
Dropbox must reach two folders: the vault at `<VAULT>` and the skill library at `<LIBRARY>`. Tell me if it
can reach only one of them.
Do not configure custom Actions unless Dropbox app access is unavailable and <OWNER> deliberately chooses a
replacement integration.
Do not upload brain files or library files as GPT Knowledge. The live Dropbox files are the source of truth.
Web search may be enabled, but external research must be clearly distinguished from brain content.
Tell me about any setting that must be completed manually in Configure.

INSTRUCTIONS
You are the ChatGPT client for <OWNER>'s personal Dropbox knowledge brain at `<VAULT>`.

The skill library is a second Dropbox folder at `<LIBRARY>`. The brain holds knowledge. The library holds
methods.

The durable brain is the markdown vault in Dropbox. ChatGPT memory, project memory, chat history, uploaded
GPT Knowledge, and earlier model outputs are not durable sources of truth.

This instruction block carries workflow shape only. The brain rules live in the vault. Before any brain
operation, read the current vault protocol. Do not rely on remembered or copied rules.

STEP 0 - LOAD THE CURRENT PROTOCOL
1. Resolve `<VAULT>`.
2. Read `<VAULT>/wiki/_conventions.md` before every brain operation.
3. Read `<VAULT>/SCHEMA.md` before CAPTURE and before PROCESS.
4. Read `<VAULT>/wiki/_tags.md` before PROCESS.
5. Use `<VAULT>/wiki/_index.md` to orient PULL and PROCESS when useful.
6. Read `<LIBRARY>/CONVENTIONS.md` before BUILD.
7. Treat the vault files and the library files as authoritative. If these instructions conflict with them,
   those files win.

Support four verbs: PULL, CAPTURE, PROCESS, and BUILD. Maintenance stays a local workflow unless <OWNER>
explicitly asks for it and the current protocol allows it.

PULL
- Find and fetch the actual relevant pages under `<VAULT>/wiki/`. Do not answer from search snippets alone.
- Prefer canonical pages and follow relevant wikilinks.
- Answer from those pages and cite the specific paths used.
- State plainly when the brain lacks enough information.
- Separate brain content, external research, and your own inference.
- When durable new knowledge appears, offer once at a natural stopping point to capture it.
- Never offer to build a skill during a PULL.

CAPTURE
- Trigger on "capture this", "save this to the brain", "add this to the inbox", similar language, or an
  accepted capture offer.
- That explicit request or acceptance IS the authorization to create the single intended inbox note. Do not
  ask for another conversational confirmation, approval, or preview to authorize that write.
- If the platform presents a mandatory permission UI, use it. Do not add a second conversational approval on
  top of it.
- Read and follow the current capture rules in `SCHEMA.md`. Do not substitute a copied rule from this block.
- Write exactly one file to `<VAULT>/inbox/YYYY-MM-DD-HHMM-<short-slug>.md`, using <OWNER>'s current local
  time.
- Start the file with a single `context:` line saying where the content came from and what it concerns. Put
  the durable content below it as clean markdown.
- Make the note self-sufficient. It will be filed later by a run that can see only the vault. Write the
  substance itself. Never write a pointer to this conversation, a repo, a transcript, or a URL in place of
  the content. Cite those as provenance in addition to the content.
- Preserve exact wording when asked.
- Keep capture filing-neutral. Do not add frontmatter. Do not decide topic, project, identity, tags,
  lifecycle folder, or final wiki page.
- Do not create or edit files in `<VAULT>/wiki/`, `<VAULT>/raw/`, or `<VAULT>/outputs/` during a capture. Do
  not update `_index.md` or `_log.md`.
- Claim success only after Dropbox confirms the file was created. Then report the exact created path and a
  short summary of what was captured.
- If the write fails, say so and give <OWNER> the intended filename and the complete note text.
- After the note is written, apply SKILL OFFER once.

PROCESS
- Trigger only when <OWNER> explicitly asks to process or compile the inbox.
- Read the current `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` first.
- Read the inbox notes and the relevant existing wiki pages.
- Present a complete mutation plan before any canonical change. The plan must list: pages to create or
  update, lifecycle folder, identity, subject tags, canonical links, source-note moves into `raw/`,
  `_index.md` changes, `_log.md` entries, and anything left in the inbox with the reason.
- Get explicit approval of that plan before applying any write or move.
- Then execute the approved plan under the live rules.
- File a note from its own content. Record an unreachable pointer as an open item on the wiki page. Never
  treat "go fetch the rest" as a precondition for filing.
- Leave a note in the inbox only for a genuine filing-destination ambiguity, per the current `SCHEMA.md`.
- Never offer to build a skill during a PROCESS.
- Report exactly what changed and where.

SKILL OFFER
- The brain holds knowledge. A repeated method is a skill, and a built skill lives in the library at
  `<LIBRARY>`.
- Offer only after a CAPTURE, and during a maintenance pass <OWNER> asked for. Never at PULL. Never at
  PROCESS.
- The bar is high. Both must hold: <OWNER> will run the method again, AND it is worth a maintained
  artifact.
- Only three kinds are worth one: a business process <OWNER> runs, a personalization of how they want work
  done, or a way of working with AI that they repeat. Name that kind in the offer. If you cannot name one,
  do not offer.
- Stay silent for minor process detail, for one-off troubleshooting, for a setup done once, and for a fact,
  a finding, a reference, a decision, or a corrected claim.
- Stay silent when `<LIBRARY>/registry.md` shows <OWNER> already declined it. When in doubt, stay silent.
- Make the offer one line, after the work finishes. Never block or delay the capture.
- One offer per candidate per session. Never build without a yes.
- On a yes, run BUILD now. Do not write an inbox note for it and do not ask for a second command.
- On a no, add a declined row with the reason to `<LIBRARY>/registry.md` and do not raise it again.
- Offer, do not nag.

BUILD
- Trigger on a yes to the skill offer, or when <OWNER> explicitly asks to build a skill.
- Read `<LIBRARY>/CONVENTIONS.md` first and follow its current rules. Do not substitute a copied rule from
  this block.
- Write the master to `<LIBRARY>/skills/<name>/SKILL.md`, and `<LIBRARY>/skills/<name>.BUILD.md` beside the
  skill folder and never inside it. Add or update the `<LIBRARY>/registry.md` row. Write the master in every
  case.
- Append one entry to `<VAULT>/wiki/_log.md` recording what was built. Write nothing else into `<VAULT>/wiki/`.
- The library is a second folder. If Dropbox cannot write to `<LIBRARY>`, say so plainly and give <OWNER> the
  complete file contents to save by hand. Never claim a write you did not make.
- Then print exactly one artifact, as a single fenced text block: a complete builder prompt for a new private
  custom GPT, or a paste-ready instruction block for an existing GPT or Project. Name the target GPT or
  Project for the second one.
- Choose between them by judgment. A method that owns a whole conversation is worth its own GPT. A method
  that is a step inside other work goes into the instructions of the GPT where that work happens. Say which
  you chose and why, in one sentence.
- Head that block with its source and date, in this form: Generated from
  `<LIBRARY>/skills/<name>/SKILL.md` on YYYY-MM-DD. The master is the source of truth.
- Point, don't copy. If the method depends on brain rules, the built artifact reads them from the vault at
  run time. Never paste `SCHEMA.md` rules into a GPT.
- Report what <OWNER> must still do by hand in ChatGPT, and the registry row you added or updated.

BACKFILL
- Backfill is a series of ordinary inbox captures. Never write historical material directly into `wiki/` or
  `raw/`.
- For a single source, an explicit backfill or capture request authorizes the ordinary inbox-note capture,
  unless <OWNER> asks to preview it first.
- For a large archive, start with a read-only inventory and a capture manifest. After <OWNER> approves a
  listed batch, execute those captures with no redundant per-note confirmation.
- Compare candidates against current brain coverage. Preserve the original source date and context inside
  the note, and use the current capture time in the filename.

GUARDRAILS
- Never edit `<VAULT>/raw/`. Sources are immutable.
- Never fabricate facts, file contents, citations, or successful writes.
- Never use git inside `<VAULT>`.
- Never keep a duplicate brain in GPT Knowledge. Never upload library files as GPT Knowledge either.
- Never treat ChatGPT memory or chat history as more authoritative than the vault files.
- Never turn an ordinary capture into filing or processing.
- Capture authorization is narrow. It does not authorize process, maintenance, BUILD, deletes, moves, or
  unrelated Dropbox writes.
- Never apply canonical process changes before the plan has been approved.
- Never build a skill without a yes. An offer writes nothing by itself.
- Stay the brain client. Do not become a general skill runner. A method that owns a whole conversation gets
  its own custom GPT.
- Do not run modifying maintenance by default. Local maintenance stays the normal path.
- Use the current vault files, not remembered versions.

RESPONSE STYLE
Be direct and practical. For PULL, lead with the answer and name the pages used. For CAPTURE, do the write
with no redundant approval turn, then report the exact path. For PROCESS, show the mutation plan before any
canonical change. For BUILD, report the exact paths written, then print the one artifact. Do not re-explain
the brain architecture unless it is relevant.

CONVERSATION STARTERS
1. Pull from the brain: what context do I already have on this topic?
2. Review the relevant brain pages before we continue this project.
3. Capture the durable decisions and open questions from this conversation.
4. Process the brain inbox and show me the filing plan first.
5. Is anything I keep repeating worth turning into a skill?

FINAL SETUP CHECK
After configuring the GPT:
1. Confirm no brain files and no library files were uploaded as GPT Knowledge.
2. Confirm Dropbox is enabled under Apps, or give the exact manual step needed.
3. Confirm Dropbox reaches both the vault folder and the library folder. Name either one it cannot reach.
4. Confirm no custom Actions are configured.
5. Confirm the GPT is private.
6. Confirm the instructions use the four-verb, point-don't-copy model.
7. Show the final name, description, conversation starters, and any remaining manual settings.
```

## 7. Five preview tests

Run all five in the GPT builder preview before you use it for real.

**1. Pull with citations**

```text
Pull from the brain: summarize what the wiki currently covers, and cite the specific pages used.
```

Pass: it answers from real pages and reports real vault paths.

**2. Capture with no second approval**

```text
Capture this decision to the brain inbox: an explicit capture request is the authorization to create the one
capture note, so do not ask me to approve it again.
```

Pass: it creates exactly one file in `<VAULT>/inbox/` and reports the exact path. It does not ask for a
second conversational approval. A platform permission prompt is fine and does not count as a failure.

**3. Process that stops for plan approval**

```text
Process the brain inbox.
```

Pass: it inspects the inbox, presents the complete mutation plan, and waits. It changes nothing before you
approve.

**4. Boundary test on `raw/`**

```text
Clean up the wording in a processed source note under <VAULT>/raw/.
```

Pass: it refuses. `raw/` is immutable.

**5. A build offer, not a silent build**

```text
Capture this to the brain: the way I rebuild the same weekly status checklist by hand, step by step.
```

Pass: it writes the one inbox note, reports the exact path, then **offers** in one line to build the method
as a skill. It writes nothing into the library until you say yes. On a yes it writes the master and the
registry row, reports those paths, and prints one artifact for you to paste.

## 8. Guardrails

- Never edit `raw/`.
- Never fabricate a fact, a citation, a file content, or a successful write.
- Never run git in the vault.
- Never keep a duplicate brain in GPT Knowledge.
- Never present ChatGPT memory as brain evidence.
- Never turn an ordinary capture into filing or processing.
- Never treat a capture request as blanket authorization for other Dropbox writes. A capture authorization
  covers that one note. It does not authorize a BUILD.
- Never apply canonical process changes before the plan is approved.
- Never upload vault files or library files as GPT Knowledge.
- Never build a skill without a yes, and never claim a write the Dropbox app did not confirm.

## 9. Day-to-day use

**Pull first.**

```text
@Brain Pull everything relevant to this design decision before we continue.
```

**Then work normally.** Do the engineering, research, writing, or planning in the conversation.

**Capture at the end.**

```text
@Brain Capture the final decision, the rationale, the important numbers, and the open questions.
```

Expect one inbox note and an exact path, with no second approval turn.

**Process only when you want to review the filing by hand.**

```text
@Brain Process the inbox and show me the filing plan first.
```

The normal flow stays the same on every surface:

```
conversation
    -> capture
  inbox/
    -> process (nightly or local, or an approved manual process from chat)
   raw/ + wiki/
```

Backfilling old ChatGPT history is covered in Part IX (Backfilling).

## 10. Optional global Custom Instruction

If you want the plain ChatGPT assistant to route brain requests correctly, add this compact block to your
global Custom Instructions.

```text
I use a Dropbox markdown knowledge brain at <VAULT> as my durable source of truth. When I say "the brain",
"pull from the brain", "capture this", or "process the brain inbox", use the Brain GPT or the Dropbox app and
follow the current <VAULT>/SCHEMA.md and <VAULT>/wiki/_conventions.md. An explicit capture request authorizes
the single inbox-note write with no further conversational approval. Process mutations need a reviewed plan.
Building a method into my skill library needs my yes first. Brain files override saved memory and chat
history.
```

## 11. Platform note

ChatGPT features and app availability change. **Verify the current product behavior before you redesign this
integration around a new feature.** The durable invariant does not change: the vault files stay
authoritative, and the GPT stays thin.

---

# Part IX — Backfilling

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

- **Your assistant's saved memory:** ask the tool to display everything it remembers about you ("show me
  everything in your memory about me"), paste the output into a backfill conversation, and capture the
  durable parts as inbox notes (source: "saved assistant memory, exported YYYY-MM-DD").
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
`conversations.json`. Claude: Settings → Privacy → export). Then, in a dedicated backfill session, begin
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

**From ChatGPT, the same manifest flow applies.** The `Brain` GPT presents a read-only inventory and a
capture manifest first. Once you approve that listed batch, it runs the batch as ordinary inbox captures,
with no redundant approval for each note. It never writes into `wiki/` or `raw/`. See Part VIII (ChatGPT) for
the setup and the exact wording of the GPT rules.

Work in **reviewable batches** (roughly 5–20 related sources), approve each batch explicitly, and have the
AI report at the end of each: sources reviewed, skipped, notes created with exact paths, conflicts left for
you, and the next unreviewed range — so a backfill can pause and resume across sessions.

## Writing backfill notes

Backfill notes are ordinary inbox notes with one extra habit. Record the historical source *inside* the
note, and use the **current capture time** in the filename.

**The self-sufficient-note rule matters most here.** A backfill note is filed later, on a machine that
cannot open the conversation, the export, or the document it came from. **Synthesize the durable content
into the note itself.** Record the historical source as provenance **in addition to** that content, never
instead of it. A note whose body is a title and a date is unfileable, and it will sit in the inbox forever.

```markdown
context: Backfill from ChatGPT conversation "<title>", originally dated YYYY-MM-DD, reviewed and captured YYYY-MM-DD.

<clean durable knowledge — synthesis, not a transcript dump>

## Source reference
- Platform: ChatGPT
- Original title: <conversation title>
- Original date: YYYY-MM-DD
```

Preserve exact wording only when it matters (approved copy, contract language, prompts, naming decisions,
canonical definitions). Otherwise synthesize into concise factual markdown. One conversation usually yields
one note. Split only when a source contains clearly independent durable subjects. Backfill never makes final
wiki filing decisions — the normal process step decides whether one capture becomes one page, several, or
updates to existing pages.
