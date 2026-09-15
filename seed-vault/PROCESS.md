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
