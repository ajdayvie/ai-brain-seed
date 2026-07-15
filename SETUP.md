# SETUP.md — prompt document for standing up a new brain

> **Human:** give this document (or this whole repo) to an AI assistant — ideally Claude Code running on
> the machine where your Dropbox lives — with one of these prompts:
>
> - **"Teach me how the brain works before setup."** → the AI explains the system and answers questions;
>   nothing is written.
> - **"Set up the brain."** → the AI runs the guided interview below, then builds your vault.
>
> Everything below this line is addressed to the AI.

---

You are setting up (or explaining) a **personal LLM-maintained knowledge brain**: a plain-markdown knowledge
base in a Dropbox folder, reachable from every AI surface the owner uses, in which the wiki — not chat
history or model memory — is the durable source of truth. This repo contains everything you need:

| Path | What it is |
|------|-----------|
| `docs/background.md` | The why: the knowledge-loss problem, the Karpathy method, the design decisions |
| `seed-vault/` | A complete, ready-to-copy vault skeleton with `{{PLACEHOLDER}}` values |
| `docs/surfaces.md` | Connecting Claude Code, Cowork/Desktop, claude.ai chat, and phone |
| `docs/chatgpt.md` | Optional ChatGPT client (private custom GPT builder prompt) |
| `docs/scheduling.md` | The nightly compile: recommended scheduled task + alternatives |
| `docs/backfilling.md` | Seeding the initial wiki from existing context and memory |

Read `docs/background.md` before either mode — you cannot set up or teach what you don't understand.

## MODE 1 — "teach me"

Explain, don't build. Walk the owner through, conversationally and in this order: the problem (knowledge
evaporates across AI surfaces) → the claim (the wiki you own is the source of truth; every tool is just a
client) → the Karpathy framing (spec / verifier / environment; the brain is the environment's knowledge
base) → the golden flow (`inbox/ → raw/ → wiki/ → outputs/`) and the three verbs (capture / process /
pull) → the three classification axes → what daily use feels like (capture freely, nightly compile, pull
with citations) → what setup will require from them (the checklist in Mode 2, step 0). Answer questions
from `docs/background.md` and the seed vault's `SCHEMA.md`. Offer to run setup when they're ready; don't
write anything until they say so.

## MODE 2 — "set up the brain"

### Step 0 — human prerequisites (tell the owner; wait until done)

The owner must do these themselves — you cannot and must not do account signups or grant permissions for
them:

1. **A Dropbox account** — ideally a *dedicated* account for the brain (avoids contention with existing
   sync usage and keeps connector permissions clean), but a dedicated folder in an existing account works.
2. **Dropbox for desktop installed** on the machine you're running on (and on any always-on machine that
   will run the nightly compile), signed in to that account.
3. **The vault folder set to Local / "Make available offline"** — NOT online-only. The files must be real
   on disk; the process step moves files and cannot work through a virtual stream drive.
4. Decide the vault location, e.g. `~/Dropbox/AI-Brain` (default name: `AI-Brain`).
5. Optional, for the chat surface later: the **Dropbox connector** available in claude.ai settings.

### Step 1 — the interview

Ask, one block at a time (skip anything already answered):

1. **Name** — what name should appear as the approver in the vault's conventions and log?
2. **Vault path** — confirm the exact local path (verify it exists and is writable; verify it looks like a
   real synced folder, not a placeholder stream).
3. **Identities** — "What distinct contexts do you operate in — businesses, employers, roles, personal?"
   Build the identity vocabulary: short lowercase slugs (e.g. `acme | consulting | personal | na`). Always
   include `na` (for knowledge that belongs to no identity, like the brain's own pages). Recommend
   `personal` plus one slug per business/role. Two to five values is the sweet spot; a single-context owner
   can use just `personal | na`.
4. **Surfaces** — which do they use? Claude Code / Cowork or Claude Desktop / claude.ai chat / phone /
   ChatGPT. (Only affects which setup steps you run in Step 4.)
5. **Scheduling** — "Do you have a machine that's on most nights?" Yes → recommend Option A in
   `docs/scheduling.md` (OS scheduler + headless Claude Code). App-always-open instead → Option B (Cowork
   scheduled task). No always-on machine → Option C (manual cadence + a recurring reminder); help them pick
   the reminder mechanism.
6. **Confirm** before writing: vault path, identity list, chosen scheduling option, surfaces to configure.

### Step 2 — build the vault

1. Copy the **contents** of `seed-vault/` into the vault path. If the repo was cloned, ensure **no `.git`
   directory travels with it** — the vault is git-free forever (Dropbox is the sync and history layer).
   If you only have this document and not the repo files, use `STANDALONE.md`, which embeds every template.
2. Replace placeholders in every copied file:
   - `{{IDENTITY_VALUES}}` → the pipe-separated identity list, e.g. `acme | personal | na`
   - `{{IDENTITY_VALUES_SLASH}}` → the same list slash-separated, e.g. `acme / personal / na`
   - `{{OWNER_NAME}}` → the owner's name
   - `{{TODAY}}` → today's date, `YYYY-MM-DD`
   - `{{NIGHTLY_METHOD_SUMMARY}}` (in `SCHEMA.md`) → one or two sentences naming the chosen scheduling
     option (e.g. "An always-on machine runs a nightly Windows Task Scheduler job launching headless Claude
     Code (`claude -p --permission-mode bypassPermissions`).")
   - `{{NIGHTLY_METHOD_DETAIL}}` (in `PROCESS.md`) → a short paragraph describing the concrete setup chosen
     in Step 4c (schedule time, script path or reminder mechanism, log location).
3. Verify: no `{{` remains anywhere in the vault (`grep -r "{{" <vault>` must come back empty).

### Step 3 — first-run verification (do not skip)

Run the loop once end-to-end from a Claude Code session inside the vault:

1. **Capture:** "capture this: the brain was initialized today from ai-brain-seed" → confirm one
   timestamped note lands in `inbox/`.
2. **Process:** run `/process` → confirm a wiki page is built with valid frontmatter, the note moved to
   `raw/`, and `_index.md` / `_log.md` updated.
3. **Pull:** ask "when was this brain initialized?" → confirm the answer cites the new page.

If any step fails, fix the cause before proceeding — this loop is the whole system.

### Step 4 — connect the surfaces (per the owner's Step-1 answers)

a. **Claude Code everywhere:** follow `docs/surfaces.md` §1 — offer to add a brain-awareness section to the
   owner's user-level `~/.claude/CLAUDE.md` (brain location, capture-offer behavior, pull behavior, never
   run git in the vault) and `additionalDirectories` to the projects they name.
b. **Cowork / Claude Desktop:** walk them through creating the Project and pasting the instruction block
   from `docs/surfaces.md` §2.
c. **Scheduling:** implement the chosen option from `docs/scheduling.md`. For Option A you may write the
   wrapper script and (on their confirmation) register the scheduled task; the owner must run
   `claude setup-token` themselves and store the token. For Option C, help them set the recurring reminder.
d. **claude.ai chat:** have the owner connect the Dropbox connector; test one pull and (if write access)
   one capture per `docs/surfaces.md` §3.
e. **ChatGPT (optional):** hand them the builder prompt from `docs/chatgpt.md` with `<VAULT>`/`<OWNER>`
   filled in, then run its three verification tests.

### Step 5 — seed it

Offer the owner the backfill program in `docs/backfilling.md`, starting with the **brain-dump interview**
(Pass 1) right now if they have 20 minutes. Remind them: modest seed + steady capture beats a giant import.

### Step 6 — handoff

Close by telling the owner, in plain language: where the vault is; the three verbs and how to invoke them
from each of their surfaces; when the compile runs (or when their reminder fires); to check `wiki/_log.md`
occasionally for `flag` entries awaiting their judgment; and to read `PROCESS.md` (their handbook) and
optionally open the vault in Obsidian to browse it.

## Rules that bind YOU during setup

- Never run git inside the vault; never leave a `.git` folder there.
- Never fabricate facts or sources anywhere in the vault; the log's first entry records only what actually
  happened.
- Don't perform account signups, permission grants, or token generation for the owner — instruct, verify,
  proceed.
- Confirm before overwriting anything that already exists at the vault path.
- After setup, the vault's own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol — including
  for you, in every future session.
