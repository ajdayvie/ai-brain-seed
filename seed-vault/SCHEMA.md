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
