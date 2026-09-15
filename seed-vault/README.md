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
