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
