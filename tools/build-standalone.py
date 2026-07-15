#!/usr/bin/env python3
"""Regenerate STANDALONE.md from the seed-vault files and docs.

Run from the repo root:  python tools/build-standalone.py
STANDALONE.md is a generated file — edit the sources, then rebuild.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VAULT_FILES = [
    "SCHEMA.md",
    "CLAUDE.md",
    "PROCESS.md",
    "README.md",
    "wiki/_conventions.md",
    "wiki/_tags.md",
    "wiki/_index.md",
    "wiki/_log.md",
    ".claude/skills/capture-to-inbox/SKILL.md",
    ".claude/skills/process-inbox/SKILL.md",
    ".claude/skills/maintenance-pass/SKILL.md",
    ".claude/commands/capture.md",
    ".claude/commands/process.md",
    ".claude/commands/pull.md",
    ".claude/commands/maintain.md",
]

DOC_PARTS = [
    ("docs/surfaces.md", "Part IV — Surfaces"),
    ("docs/scheduling.md", "Part V — Scheduling the nightly compile"),
    ("docs/chatgpt.md", "Part VI — ChatGPT (optional)"),
    ("docs/backfilling.md", "Part VII — Backfilling"),
]

# Cross-reference rewrites: repo paths -> standalone part names
XREFS = [
    (r"`?docs/background\.md`?", "Part I (Background)"),
    (r"`?docs/surfaces\.md`?", "Part IV (Surfaces)"),
    (r"`?docs/scheduling\.md`?", "Part V (Scheduling)"),
    (r"`?docs/chatgpt\.md`?", "Part VI (ChatGPT)"),
    (r"`?docs/backfilling\.md`?", "Part VII (Backfilling)"),
    (r"\[([^\]]+)\]\(Part ([IVX]+) \(([^)]+)\)\)", r"Part \2 (\3)"),  # collapse md links left over
]

PREAMBLE = """\
# STANDALONE.md — set up an LLM-maintained knowledge brain (single-file edition)

> **Human:** paste this entire document into an AI assistant — ideally Claude Code running on the machine
> where your Dropbox lives — with one of these prompts:
>
> - **"Teach me how the brain works before setup."** → the AI explains the system and answers questions;
>   nothing is written.
> - **"Set up the brain."** → the AI runs a guided interview, then builds your vault from the templates in
>   Part III.
>
> This is the self-contained edition of the `ai-brain-seed` kit
> (https://github.com/ajdayvie/ai-brain-seed) — same content, no download needed.
> Everything below is addressed to the AI.

---

You are setting up (or explaining) a **personal LLM-maintained knowledge brain**: a plain-markdown
knowledge base in a Dropbox folder, reachable from every AI surface the owner uses, in which the wiki — not
chat history or model memory — is the durable source of truth.

This document has seven parts:

- **Part I — Background**: the why. Read it first; you cannot set up or teach what you don't understand.
- **Part II — Setup procedure**: the guided interview and build steps.
- **Part III — Vault file templates**: every file the vault needs, verbatim, with `{{PLACEHOLDER}}` values.
- **Part IV — Surfaces**: connecting Claude Code, Cowork/Desktop, claude.ai chat, and phone.
- **Part V — Scheduling**: the nightly compile (recommended scheduled task + alternatives).
- **Part VI — ChatGPT** (optional): a private custom GPT as a ChatGPT-side client.
- **Part VII — Backfilling**: seeding the initial wiki from existing context and memory.

## MODE 1 — "teach me"

Explain, don't build. Walk the owner through, conversationally and in this order: the problem (knowledge
evaporates across AI surfaces) → the claim (the wiki you own is the source of truth; every tool is just a
client) → the Karpathy framing (spec / verifier / environment; the brain is the environment's knowledge
base) → the golden flow (`inbox/ → raw/ → wiki/ → outputs/`) and the three verbs (capture / process /
pull) → the three classification axes → what daily use feels like (capture freely, nightly compile, pull
with citations) → what setup will require from them (Part II, step 0). Answer questions from Part I and
the `SCHEMA.md` template in Part III. Offer to run setup when they're ready; don't write anything until
they say so.

## MODE 2 — "set up the brain" (Part II — Setup procedure)

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
5. **Scheduling** — "Do you have a machine that's on most nights?" Yes → recommend Option A in Part V
   (OS scheduler + headless Claude Code). App-always-open instead → Option B (Cowork scheduled task). No
   always-on machine → Option C (manual cadence + a recurring reminder); help them pick the reminder
   mechanism.
6. **Confirm** before writing: vault path, identity list, chosen scheduling option, surfaces to configure.

### Step 2 — build the vault

1. Create this tree at the vault path (empty folders get a `.keep` file), then write every file from
   Part III at its stated path:

   ```
   <vault>/
     SCHEMA.md  CLAUDE.md  PROCESS.md  README.md
     inbox/.keep   raw/.keep   outputs/.keep
     wiki/_conventions.md  wiki/_tags.md  wiki/_index.md  wiki/_log.md
     wiki/topics/.keep  wiki/projects/.keep  wiki/archive/.keep
     .claude/skills/capture-to-inbox/SKILL.md
     .claude/skills/process-inbox/SKILL.md
     .claude/skills/maintenance-pass/SKILL.md
     .claude/commands/capture.md  process.md  pull.md  maintain.md
   ```

   Never create a git repo in the vault — it is git-free forever (Dropbox is the sync and history layer).
2. Replace placeholders in every written file:
   - `{{IDENTITY_VALUES}}` → the pipe-separated identity list, e.g. `acme | personal | na`
   - `{{IDENTITY_VALUES_SLASH}}` → the same list slash-separated, e.g. `acme / personal / na`
   - `{{OWNER_NAME}}` → the owner's name
   - `{{TODAY}}` → today's date, `YYYY-MM-DD`
   - `{{NIGHTLY_METHOD_SUMMARY}}` (in `SCHEMA.md`) → one or two sentences naming the chosen scheduling
     option
   - `{{NIGHTLY_METHOD_DETAIL}}` (in `PROCESS.md`) → a short paragraph describing the concrete setup chosen
     in Step 4c (schedule time, script path or reminder mechanism, log location)
3. Verify: no `{{` remains anywhere in the vault.

### Step 3 — first-run verification (do not skip)

Run the loop once end-to-end from a Claude Code session inside the vault:

1. **Capture:** "capture this: the brain was initialized today from ai-brain-seed" → confirm one
   timestamped note lands in `inbox/`.
2. **Process:** run `/process` → confirm a wiki page is built with valid frontmatter, the note moved to
   `raw/`, and `_index.md` / `_log.md` updated.
3. **Pull:** ask "when was this brain initialized?" → confirm the answer cites the new page.

If any step fails, fix the cause before proceeding — this loop is the whole system.

### Step 4 — connect the surfaces (per the owner's Step-1 answers)

a. **Claude Code everywhere:** follow Part IV §1 — offer to add a brain-awareness section to the owner's
   user-level `~/.claude/CLAUDE.md` and `additionalDirectories` to the projects they name.
b. **Cowork / Claude Desktop:** walk them through creating the Project and pasting the instruction block
   from Part IV §2.
c. **Scheduling:** implement the chosen option from Part V. For Option A you may write the wrapper script
   and (on their confirmation) register the scheduled task; the owner must run `claude setup-token`
   themselves and store the token. For Option C, help them set the recurring reminder.
d. **claude.ai chat:** have the owner connect the Dropbox connector; test one pull and (if write access)
   one capture per Part IV §3.
e. **ChatGPT (optional):** hand them the builder prompt from Part VI with `<VAULT>`/`<OWNER>` filled in,
   then run its three verification tests.

### Step 5 — seed it

Offer the owner the backfill program in Part VII, starting with the **brain-dump interview** (Pass 1) right
now if they have 20 minutes. Remind them: modest seed + steady capture beats a giant import.

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
"""


def apply_xrefs(text: str) -> str:
    for pattern, repl in XREFS:
        text = re.sub(pattern, repl, text)
    return text


def main() -> None:
    parts: list[str] = [PREAMBLE]

    background = (ROOT / "docs/background.md").read_text(encoding="utf-8")
    parts.append("\n---\n\n# Part I — Background\n\n" + apply_xrefs(
        background.split("\n", 1)[1].lstrip("\n")))

    parts.append(
        "\n---\n\n# Part II — Setup procedure\n\n"
        "The full procedure is MODE 2 above; it is not repeated here.\n"
    )

    parts.append("\n---\n\n# Part III — Vault file templates\n\n"
                 "Write each file at the stated path (relative to the vault root), verbatim, then apply the\n"
                 "placeholder replacements from Step 2.\n")
    for rel in VAULT_FILES:
        content = (ROOT / "seed-vault" / rel).read_text(encoding="utf-8")
        parts.append(f"\n## File: `{rel}`\n\n````markdown\n{content}````\n")

    for rel, title in DOC_PARTS:
        content = (ROOT / rel).read_text(encoding="utf-8")
        body = apply_xrefs(content.split("\n", 1)[1].lstrip("\n"))
        parts.append(f"\n---\n\n# {title}\n\n" + body)

    out = ROOT / "STANDALONE.md"
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
