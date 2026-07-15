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
