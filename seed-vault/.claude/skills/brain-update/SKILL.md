---
name: brain-update
description: >
  This skill should be used when the user wants to check their knowledge brain for updates from the
  ai-brain-seed kit and install them. Triggers include "/brain-update", "check my brain for updates",
  "update the brain", "is my brain out of date", "what's new in the brain kit", and "install the new
  brain features". It finds the kit, compares versions, shows what changed, and applies only the
  migrations the owner says yes to. It never updates without a yes, and it never runs git in the vault.
---

# Update the brain from the kit

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. If that is ambiguous, **ask the owner for the absolute path and wait.** Never guess a
default like `~/Dropbox/AI-Brain`. This skill runs from any project directory.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §13** and **`<brain>/.claude/VERSION.md`**. §13 is authoritative for what an
update may and may not do in this vault. If `VERSION.md` is missing, this vault predates version tracking —
that is expected, and the kit's runbook knows how to handle it.

## Step 1 — get the kit

The kit is <https://github.com/ajdayvie/ai-brain-seed>.

If this session already has a clone of it, use that and `git pull` first. Otherwise clone it shallow into a
scratch folder. **Prefer the clone** — it gets every file byte-exact and makes the next update one `git
pull`.

Without git, download the individual files with `curl -fsSL <raw url> -o <path>`, per `UPDATES.md` Step 0.
**Download the bytes.** Skill files and the renderer script are copied into the vault verbatim, so a
page-reading tool that reflows the content corrupts them silently.

**The clone must never land inside `<brain>`, and you must never run git inside `<brain>`.** The vault is
git-free forever. Cloud sync is its versioning layer.

## Step 2 — hand off to the kit's runbook

Read **`<kit>/UPDATES.md`** and follow it, start to finish. **That document is authoritative for the whole
job.** It holds the version probe, the placeholder recovery, the migration order, the safety contract, the
verification, and the bookkeeping. This skill deliberately does not copy any of it, so a kit released after
this file was written still updates correctly.

Read `<kit>/CHANGELOG.md` so you can say what each version actually changed, rather than paraphrasing from
memory.

## The rules this skill will not let a runbook relax

- **Never run git in the vault.** Never leave a `.git` folder there.
- **Ask before each migration**, and show a diff before every edit to an existing file. Declining one is a
  valid answer, and a partial update is a valid end state.
- **Never touch** `wiki/` page content, `inbox/`, `raw/`, `outputs/`, `digests/`, or the library's
  `skills/`. Those are the owner's. The exceptions are the anchored `_log.md` entry and any `_index.md`
  change a migration names explicitly.
- **Back up every existing file you edit** beside itself as `<file>.pre-<version>` before the edit.
- **A missing anchor stops the step.** Show the owner the surrounding lines and let them decide. Never
  improvise a location, and never overwrite their file with the seed template.
- **Never install software on the owner's machine.** State the command and let them run it.
- **Report what you skipped**, in `.claude/VERSION.md` and in `wiki/_log.md`, with the reason. A skipped
  step that is not written down is one the next update assumes ran.

## Do not

- Do not offer an update proactively, and do not put one on a schedule. Nothing expires. A vault that stays
  at its installed version keeps working.
- Do not update a vault you have not confirmed with the owner by absolute path.
- Do not report an update as finished when a step errored or was skipped.
