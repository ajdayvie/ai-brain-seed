# UPDATES.md — bring an existing brain up to the current kit

> **Human:** you do not need to read this file. Open a Claude Code session on a machine that can reach your
> vault folder and say:
>
> ```
> check my brain for updates
> ```
>
> If your vault is already at version 0.3.0 or later, `/brain-update` does the same thing and finds the kit
> for you.
>
> The assistant works out which version your vault is on, tells you what changed since, and asks before it
> writes anything. **Nothing expires.** A vault that stays where it is keeps working. An update is a choice.
>
> Most updates take 5 to 15 minutes. The 0.1.0 to 0.2.0 step is larger — budget an hour.

---

**Everything below this line is addressed to the AI.**

You are updating an **existing** brain vault to a newer version of the ai-brain-seed kit. The vault already
holds the owner's real knowledge. Treat it that way.

**The governing rule of this whole document: an update adds capability. It never costs the owner
knowledge, and it never silently overwrites something they wrote.** When those two goals conflict with
"match the current templates exactly", the owner's content wins and you report the difference.

---

## Step 0 — get the kit, and keep it out of the vault

You need the kit's files: `VERSION`, `CHANGELOG.md`, `migrations/`, and `seed-vault/`.

**If this session is already running in a clone of the kit**, you have them. Run `git pull` to make sure it
is current, then go to Step 1.

**If it is not**, get the kit one of two ways.

1. **Clone it** to a scratch directory. The OS temp directory is fine, or any folder outside the vault.

   ```bash
   git clone --depth 1 https://github.com/ajdayvie/ai-brain-seed.git <scratch>/ai-brain-seed
   ```

2. **No git, or the clone is blocked** — fetch the raw files you need over HTTPS from
   `https://raw.githubusercontent.com/ajdayvie/ai-brain-seed/main/<path>`. Fetch `VERSION` and
   `CHANGELOG.md` first, then only the migration documents Step 4 selects, then only the seed files those
   migrations name. Do not try to mirror the whole repository this way.

**WARNING: the clone must never land inside the vault, and you must never run git inside the vault.** The
vault is git-free forever — cloud sync is its versioning layer. A `.git` folder in a synced vault is a sync
conflict generator, and the seed's own rules forbid it. If the owner asks you to clone into the vault, say
no and clone elsewhere.

Delete the scratch clone when you are done, or tell the owner where you left it.

---

## Step 1 — resolve the vault, the library, and the machine

**Assume nothing about paths.** This vault belongs to someone whose setup you have not seen. It may sit
anywhere, on any OS, under any folder name.

1. **The vault.** Read `BRAIN_DIR` from the environment (`echo "$BRAIN_DIR"`). If it is unset or does not
   exist, look at the session's working and additional directories for one holding both `SCHEMA.md` and a
   `wiki/` folder. If that finds nothing, or finds more than one, **ask the owner for the absolute path and
   wait.** Do not guess `~/Dropbox/AI-Brain`.
2. **Confirm it is really the vault** before you write a single byte. It must hold `SCHEMA.md` and `wiki/`.
   Say the resolved path back to the owner and get a yes.
3. **The library**, if the vault is at 0.2.0 or later. Read `SKILLS_DIR`. If unset, look for a sibling of
   the vault named `AI-Skills` — **or whatever name this vault's own files use.** Grep the vault for the
   folder name it expects rather than assuming the default. If there is no library and the migration needs
   one, say so and ask.
4. **The machine.** Note the OS and the shell. The copy commands, the path separators, and the JSON escaping
   in `settings.json` all differ between Windows and macOS/Linux. Use the form that matches this machine.
5. **Check the vault is real on disk, not an online-only placeholder.** Read one existing file and confirm
   you get content. A cloud-stream drive can list names it cannot open.

---

## Step 2 — work out the vault's current version

**First, look for the marker.** Read `<vault>/.claude/VERSION.md` and take `seed-version:`. If it is there,
that is the answer. Go to Step 3.

**If there is no marker**, the vault predates version tracking. Probe for features, in this order, and take
the **highest** version whose markers are all present.

| Version | Present when |
|---|---|
| 0.3.0 | `digests/` exists, **and** `.claude/skills/audio-digest/SKILL.md` exists |
| 0.2.0 | `.claude/skills/skill-library/SKILL.md` exists, **and** `SCHEMA.md` contains a `§6e` or `6e.` heading |
| 0.1.0 | `SCHEMA.md` and `wiki/` exist, and neither row above matches |

**A partial match means a partial or hand-built install, not a version.** If some markers of a version are
present and others are not, treat the vault as the **lower** version, say exactly which markers you found
and which you did not, and let the migration's own preconditions sort it out. Do not average.

**If nothing matches at all**, this is not a vault built from this kit. It may be a hand-built brain, or a
much older one. Say so plainly, and offer two honest choices: apply the migrations as *additive only*,
skipping every edit whose anchor text is missing, or run the fresh-install intake in `INSTALL.md` into a new
folder and let the owner move content across. **Do not force a migration onto a vault it does not fit.**

State the version you concluded and the evidence for it, and get the owner's yes before Step 3.

---

## Step 3 — read the vault's own values back out

A migration writes new files. Those files must carry **this owner's** values, not the seed's defaults.
Recover each value from the vault itself. Never invent one and never carry one over from a different
install.

| Value | Where to read it from |
|---|---|
| `{{VAULT_PATH}}` | The path you resolved in Step 1 |
| `{{OWNER_NAME}}` | `wiki/_conventions.md`, and the first entry in `wiki/_log.md` |
| `{{IDENTITY_VALUES}}` | The `identity:` line in `SCHEMA.md` §5, verbatim |
| `{{IDENTITY_VALUES_SLASH}}` | The same list, slash-separated |
| `{{SKILLS_PATH}}` | The library path from Step 1 |
| `{{SKILLS_DIRNAME}}` | The library folder's actual name on this machine |
| `{{TODAY}}` | Today's date, `YYYY-MM-DD` |
| `{{NIGHTLY_METHOD_SUMMARY}}` / `{{NIGHTLY_METHOD_DETAIL}}` | `SCHEMA.md` §8 and `PROCESS.md`, as this vault already words them |

**Then check for drift.** Grep the vault for `{{`. A leftover placeholder means the original install did not
finish. Report each one. Offer to fill it from the values above, and fix it only on a yes.

**Respect renames.** If the owner renamed a folder, a command, or a skill, the new file you write must match
what their vault already uses. Their naming is not a defect.

---

## Step 4 — choose the migrations

Read `<kit>/VERSION` for the kit's current version, and `<kit>/CHANGELOG.md` for what each release changed.

Every migration lives at `<kit>/migrations/<version>-<slug>.md`. Apply every migration **above** the vault's
version, **in ascending order, one at a time.** Never skip one to reach a later feature. A later migration
assumes the earlier ones ran.

Before you touch anything, tell the owner:

- the version their vault is on, and the version the kit is on;
- one line per migration, saying what it adds — from `CHANGELOG.md`, not from memory;
- roughly how long it will take;
- that they can stop after any migration and resume later, because each one records itself.

**Then ask which ones to apply, and wait.** They may take one and decline another. An update they did not
ask for is the same defect as an offer that fires too often.

---

## Step 5 — the safety contract

This binds you for every migration, and a migration cannot relax it.

**Never touch these, for any reason:**

- `wiki/` page content — except an anchored `_index.md` or `_log.md` entry a migration explicitly names
- `inbox/`, `raw/`, `outputs/`, `digests/` — the owner's notes, sources, deliverables, and digests
- Anything under the library's `skills/` — those are the owner's built skills

**Before editing any existing file:**

1. **Back it up** beside itself as `<file>.pre-<version>` — for example `SCHEMA.md.pre-0.3.0`. Cloud sync
   has version history too, but a local copy is what the owner can actually see and diff.
2. **Edit by anchor, never by overwrite.** A migration names the text to find and the text to insert or
   replace. Find it, and make that one change. **Do not copy the seed template over the owner's file.**
   Their file is edited. Yours is not.
3. **If an anchor is missing**, do not improvise a location. Report it, show the owner the surrounding
   lines, and let them decide. A missing anchor usually means they rewrote that section, and their wording
   is the one that stays.
4. **Show the diff and get a yes** for every existing file you change. New files you may create after a
   single yes covering them all.

**Never:**

- Run git in the vault.
- Delete anything the owner created.
- Overwrite a file at `~/.claude/` without the owner's yes — they may have unrelated skills there.
- Fabricate a fact, a date, or a source in any file you write.
- Report a step as done when it errored or you skipped it.

---

## Step 6 — run each migration

Open the migration document and follow it exactly. Each one carries its own preconditions, file list,
anchored edits, and verification. **The migration document is authoritative for its own step.** This file
carries only the frame around it.

Run them one at a time. Verify each before you start the next. If one fails partway, stop, report what
landed and what did not, and leave the rest for a later run. **Do not roll forward past a failure.**

---

## Step 7 — reinstall the Claude Code copies

A migration that adds or changes a file under `<vault>/.claude/skills/` or `<vault>/.claude/commands/` does
not take effect until each machine reinstalls.

Follow `<vault>/.claude/INSTALL.md`, which is the vault's own runbook and knows this owner's paths. It
carries the copy commands for both platforms, the `BRAIN_DIR` setting, the drift check, and the verify step.

Two things to say out loud when you finish:

- **A protocol change needs no install.** Edits to `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md`
  reach every machine and every surface through cloud sync.
- **Every other machine still needs the copy-install re-run.** The vault files sync. The `~/.claude/` copies
  do not. Name that as a to-do for each of the owner's other machines.

Check whether the migration adds a new dependency — a Python package, a command-line tool. If it does, state
what to install and let the owner run it. **Do not install software on their machine without asking.**

---

## Step 8 — verify

Run the migration's own verification steps. Then run the loop once, end to end, to prove nothing broke:

1. **Capture.** `/capture test note from the 0.x.y update` must write one file into `<vault>/inbox/` and
   echo the full path.
2. **Pull.** Ask something the wiki already covers. The answer must cite real pages.
3. **Grep for `{{`** across the vault and the library. It must return nothing.

If a step fails, fix the cause before you report success. **Do not report a partial update as a finished
one.**

---

## Step 9 — record it

1. **Update the marker.** Write `<vault>/.claude/VERSION.md` if it does not exist — use the template at
   `<kit>/seed-vault/.claude/VERSION.md` and fill it from Step 3. Set `seed-version:` to the version you
   reached, and append one row per migration applied: version, date, how, and any part you skipped.
2. **Append one line to `wiki/_log.md`**, as a `maintenance` entry. It is the owner's journal of what
   changed in their brain, and a kit update belongs in it.

   ```
   ## [YYYY-MM-DD] maintenance | Updated the brain from seed 0.2.0 to 0.3.0: added the digest verb.
   ```

3. **Record what you skipped**, in both places, with the reason. A skipped step that is not written down is
   a step the next update assumes ran.

---

## Step 10 — report

Tell the owner, in plain language:

- The version they were on, and the version they are on now.
- What is new and how to use it — the command, and one sentence of what it does.
- What still needs a human: reinstalling on other machines, installing a dependency, refreshing a Cowork,
  chat, or ChatGPT instruction block.
- Anything you skipped, and why.
- Where the backups are, and that they can be deleted once the owner is happy.

---

## Rules that bind YOU during an update

- **The owner's content always wins.** Their knowledge, their wording, their names.
- **Never run git in the vault. Never leave a `.git` folder there.**
- **Confirm the vault path before the first write**, and show a diff before every edit to an existing file.
- **Ask before each migration.** Declining one is a valid answer.
- **Never fabricate a fact, a date, or a source.** The log records only what actually happened.
- **Report failures plainly**, with the error. A quiet failure in a knowledge base is worse than a loud one.
- After the update, the vault's own `SCHEMA.md` and `wiki/_conventions.md` are the binding protocol again —
  including the parts you just changed.
