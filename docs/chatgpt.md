# ChatGPT — using the brain from ChatGPT (optional)

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
**library**, a second synced folder beside the vault. `docs/skills.md` explains the concept, and
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

Backfilling old ChatGPT history is covered in `docs/backfilling.md`.

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
