# Surfaces — connecting each client to the brain

The same protocol runs on every surface. Only the way each one reaches the files differs. The portable unit
is the **protocol in `SCHEMA.md`**, not any skill file. Each surface needs two things: access to the vault
files, and an instruction to read `SCHEMA.md` and `wiki/_conventions.md` and follow them.

| Surface | Mechanism | Verbs | Notes |
|---|---|---|---|
| Claude Code (local) | Skills and slash commands in `<vault>/.claude/`, installed by copy into `~/.claude/` | capture, process, pull, maintain | The primary surface. Owns process and maintain. |
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

The vault ships four skills (`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`) and
five slash commands (`/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`). They install into
`~/.claude/` by copy, so they work from **any** project directory, not only from inside the vault.

**Never edit the installed copy.** An edit in `~/.claude/` is invisible to every other machine, and the next
install destroys it. Change the vault copy and reinstall.

**A protocol change needs no install.** The skills are thin. They carry the job skeleton and the
vault-resolution logic, and they point at `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the
rules. Editing `SCHEMA.md` reaches every machine and every surface through cloud sync. Reinstall only when a
skill file itself changes.

### Setup

1. **Install the skills and commands.** Follow `seed-vault/.claude/INSTALL.md`, which ships in the vault as
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
   The guided interview in the repo-root `INSTALL.md` writes this section for you.

### Use

Run `/process` and `/maintain` from a session with disk access to the vault. Run `/capture` and `/pull` from
anywhere, once `BRAIN_DIR` is set.

## 2. Cowork / Claude desktop

### Mechanism

Cowork has no skill files of its own. It carries the protocol in **Project instructions**. It has real disk
access to the vault, so it can run all three of capture, process, and pull. It can also run the Option A
scheduled task in `docs/scheduling.md`.

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
complete the move. See `docs/scheduling.md` for the same constraint applied to scheduling.

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
prompt, and five preview tests are in `docs/chatgpt.md`.

An owner who uses ChatGPT and no Claude surface gets the whole loop from that one GPT. It offers to build a
skill when a capture is a repeatable method, and its **BUILD** verb writes the master into the library on a
yes. See section 3 of `docs/chatgpt.md`.

## Skill reach — how a skill gets to each surface

A skill is a method, not knowledge, so it does not travel through the vault. It reaches a surface through
a **store**, and each store reaches a different set of surfaces. This table is the reach summary. The rules
live in `docs/skills.md` and in `<library>/CONVENTIONS.md`.

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
provenance, and the packaging traps — read `docs/skills.md` and `<library>/CONVENTIONS.md`. Do not restate
those rules in a client's instructions. Point at them.

## The rules that span all surfaces

**Point, don't copy.** The client instructions carry the workflow skeleton. The rules are read from the vault
at run time. A client that copies a rule inline goes stale the day the vault changes.

**Re-read before acting.** Every surface re-reads `SCHEMA.md` and `wiki/_conventions.md` before it acts on
the brain, and treats them as binding. Memory of the protocol is always stale. The files are always current.
