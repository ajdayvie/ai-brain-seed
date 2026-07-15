# Surfaces — connecting each Claude client to the brain

The same protocol runs on every surface; only the mechanics of reaching the files differ. The portable unit
is the **protocol in `SCHEMA.md`**, not any skill file — each surface just needs (a) access to the vault
files and (b) an instruction to read `SCHEMA.md` + `wiki/_conventions.md` and follow them.

## 1. Claude Code (the primary surface)

Nothing to install — the seed vault ships with everything:

- `CLAUDE.md` is auto-loaded whenever Claude Code runs inside the vault folder, and points to `SCHEMA.md`.
- Skills live in `.claude/skills/` (`capture-to-inbox`, `process-inbox`, `maintenance-pass`).
- Slash commands live in `.claude/commands/` (`/capture`, `/process`, `/pull`, `/maintain`).

**Use it two ways:**

1. **Inside the vault** — `cd` into the vault folder and run `claude`. Everything loads automatically. This
   is where you run `/process` and `/maintain`.
2. **Attached to other projects** — make every coding session brain-aware by attaching the vault:
   - Per session: `claude --add-dir "<path-to-vault>"`
   - Per project: add to the project's `.claude/settings.json`:
     ```json
     { "additionalDirectories": ["<path-to-vault>"] }
     ```
   - Globally: add a section to your user-level `~/.claude/CLAUDE.md` telling Claude the brain exists, where
     it lives, and to be "brain-aware": offer to capture durable knowledge at natural stopping points, pull
     from the wiki when a question might be covered, and never run git in the vault. (The SETUP.md interview
     writes this for you.)

## 2. Cowork / Claude Desktop

Cowork has no skill files of its own; it carries the protocol in **Project instructions**.

1. Create a Project pointed at the vault folder.
2. Paste this into the Project's Instructions field:

> This project IS my LLM-maintained knowledge brain (plain markdown in Dropbox). Your job is to build and
> maintain it, not just answer from it.
>
> At the start of any work here, read these vault files and treat them as your binding instructions:
> - `SCHEMA.md` — the full operating protocol (structure, the capture / process / pull / maintain
>   workflows, frontmatter, guardrails). This is authoritative; everything defers to it.
> - `wiki/_conventions.md` — the per-page rules.
> - `CLAUDE.md` — the short summary that points to the above.
>
> Follow whatever those files currently say (they may have changed since you last read them — re-read, don't
> rely on memory). In particular: capture freely to `inbox/` on request or proactively at stopping points;
> compile only on "process"; answer pulls from `wiki/` with citations; never fabricate facts or sources; and
> no git, ever.

The paste block carries no protocol of its own — it just tells Claude to read the spec files in the vault
and follow them. That's deliberate: when the conventions change, every surface stays correct with nothing to
re-sync.

## 3. claude.ai chat (web and phone)

Chat reaches the brain through the **Dropbox connector**:

1. In claude.ai → Settings → Connectors, connect Dropbox (the account that holds the vault).
2. **Pull:** ask "what does my brain say about X?" — Claude reads `wiki/` pages through the connector and
   cites them.
3. **Capture:** if the connector has write access, "capture this to the brain" creates a note in `inbox/`
   directly. Confirm the exact file before it writes; report the created path after.
4. For consistent behavior, create a claude.ai **Project** for brain interactions and put the same
   instruction block from the Cowork section above into its project instructions (with paths as Dropbox
   paths, e.g. `/AI-Brain/SCHEMA.md`).

Chat never runs the process step — moving notes out of `inbox/` needs local disk access. Capture and pull
only.

## 4. Phone

Two options, in order of preference:

- **claude.ai mobile app** with the Dropbox connector (same as web chat): capture and pull from anywhere.
- **Dispatch to the always-on machine**: if you run one (see `docs/scheduling.md`), send capture requests to
  a session running there (e.g., Cowork mobile dispatch).

## 5. ChatGPT (optional)

If you also work in ChatGPT, set it up as a *client* of the same brain — see `docs/chatgpt.md`. It pulls and
captures through the Dropbox app; it never processes or edits `wiki/`/`raw/`.

## The one rule that spans all surfaces

Every surface re-reads `SCHEMA.md` and `wiki/_conventions.md` before acting on the brain, and treats them as
binding. Memory of the protocol is always stale; the files are always current.
