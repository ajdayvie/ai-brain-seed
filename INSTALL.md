# INSTALL.md — the guided intake for a new brain

> **Human:** you do not need to read this file. Open an AI assistant in this folder and say
> `help me install an AI brain`. The assistant reads this document and walks you through the rest. It
> teaches you the system first, asks a short set of questions, then builds your vault and verifies it.
>
> If you want the explanation and nothing written to disk, say `teach me how the brain works` instead.
>
> The core install takes about 30 minutes. Connecting extra surfaces and the first backfill pass add
> more. You can stop after any step and resume later.

---

**Everything below this line is addressed to the AI.**

You are installing a **personal LLM-maintained knowledge brain** for the owner. The brain is a
plain-markdown knowledge base in a synced folder, reachable from every AI surface the owner uses. The wiki,
not chat history and not model memory, is the durable source of truth.

This repository holds everything you need.

| Path | What it is |
|------|-----------|
| `docs/background.md` | The why: the knowledge-loss problem, the method, the design decisions |
| `seed-vault/` | The vault skeleton, with `{{PLACEHOLDER}}` values you replace |
| `seed-vault/SCHEMA.md` | The operating protocol. Binding in the vault after install. |
| `seed-vault/.claude/INSTALL.md` | The per-machine runbook for installing the Claude Code skills |
| `seed-library/` | The skill library skeleton, with `{{PLACEHOLDER}}` values you replace |
| `docs/surfaces.md` | Wiring for Claude Code, Cowork and desktop, claude.ai chat, and ChatGPT |
| `docs/skills.md` | The skill library: the stores, what each one reaches, and the offer behavior |
| `docs/scheduling.md` | The nightly compile: options A, B, and C |
| `docs/chatgpt.md` | The private custom GPT: builder prompt and preview tests |
| `docs/backfilling.md` | Seeding the wiki from existing context |

Read `docs/background.md` before you teach or build. You cannot install what you do not understand.

If you have this document but not the repository files, use `STANDALONE.md`. It embeds every template.

---

## Mode: teach only

Trigger: the owner says `teach me how the brain works`, or asks to understand the system before any setup.

Explain. Write nothing. Cover, in this order: the problem, the claim, the method behind the design, the
golden flow, the four verbs, the three classification axes, what daily use feels like, and what an install
would ask of them. Answer questions from `docs/background.md` and `seed-vault/SCHEMA.md`.

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
4. **The four verbs.** capture, process, pull, maintain. Four verbs move knowledge, and `/brain-skill` turns
   a repeated method into a skill that installs to the surfaces the owner uses.
5. **What daily use feels like.** Capture freely from any surface. The compile runs nightly, or on a cadence
   they choose. Pull answers with citations to pages.

Then offer more: "I can go deeper from `docs/background.md` before we start." Read from it only if they say
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

1. Copy the **contents** of `seed-vault/` into the vault path. Copy the hidden `.claude/` folder too.
2. Copy the **contents** of `seed-library/` into the library path from step 3. The library is a second
   folder, beside the vault, in the same synced storage.
3. **WARNING:** if this repository was cloned, make sure **no `.git` directory travels into the vault or into
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
**4 skills** (`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`) and **5 commands**
(`/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`).

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

If a step fails, fix the cause before you go on.

---

## Step 7 — connect the surfaces

Run only the parts the owner named in step 3. Each part is detailed in `docs/surfaces.md`.

a. **Claude Code, everywhere.** Offer to add a brain-awareness block to the owner's user-level
   `~/.claude/CLAUDE.md`: the vault location, capture-offer behavior, pull behavior, and the rule that no
   session runs git in the vault. Add the vault to `additionalDirectories` for the projects they name.

b. **Cowork or Claude desktop.** Walk them through creating a Project pointed at the vault and pasting the
   instruction block from `docs/surfaces.md`.

c. **claude.ai chat, web and phone.** Have the owner connect the Dropbox connector, then test one pull and
   one capture. This surface does capture and pull. It cannot process, because moving a note out of `inbox/`
   needs real disk access.

d. **ChatGPT.** Hand them the builder prompt from `docs/chatgpt.md`, with the `<VAULT>`, `<LIBRARY>`, and
   `<OWNER>` placeholders filled in. `<LIBRARY>` is the library path as Dropbox sees it. They create a
   **private custom GPT** named `Brain` with the Dropbox app enabled, and the app must reach both folders.
   Then run the preview tests in that document. **Never upload vault or library files as GPT Knowledge.** A
   second copy goes stale the day the source changes.

The rule that spans every surface: **point, don't copy.** The client instructions carry the workflow
skeleton. The rules are read from the vault at run time.

---

## Step 8 — set up processing

Processing should run nightly. Pick the option that matches the step 3 answers. Then set the two nightly
placeholders from step 4 to match. `docs/scheduling.md` holds the full recipes.

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
and prints the one artifact to paste. `docs/chatgpt.md` holds the builder prompt and the preview tests.

Point the owner at `docs/skills.md` for the full concept: the stores, and what each one reaches. State these
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

Offer the **brain-dump interview** from `docs/backfilling.md` right now, if the owner has 20 minutes. It is
the fastest route to a useful first wiki. Then point them at the other passes in that document: per-tool
memory exports, and selected high-value conversations and documents.

Every backfill pass is a series of ordinary captures into `inbox/`. Never write historical material straight
into `wiki/` or `raw/`.

Tell them the rule: a modest seed plus steady capture beats a large stale import.

---

## Step 11 — handoff

Close by telling the owner, in plain language:

- Where the vault is, and where the library is.
- The four verbs, and how to invoke each one on each surface they set up.
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
- **Do not write outside this repository** until the owner confirms the vault path in step 3.
- After setup, the vault's own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol. That holds
  for you, in every future session.
