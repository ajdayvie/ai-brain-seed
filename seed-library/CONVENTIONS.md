# CONVENTIONS.md — the contract for the skill library

Read this file before you build a skill, install one, or package one. It is binding until the owner changes
it. It lives in the library, so it is present and current on every machine the sync reaches.

The brain holds knowledge. The library holds methods. **A skill is a verb. Knowledge is a noun.**

---

## 1. Where a master lives, and how far it reaches

**Where a master lives.** A skill that needs the brain to exist belongs in `<vault>/.claude/skills/`, so the
vault keeps installing itself. Everything else belongs in the library.

**How far it reaches.** A skill that runs a shell command, a script, or a file write works only on a surface
with disk access, which means Claude Code and Cowork. It cannot reach a chat surface, and a bundle uploaded
for one would fail there. A pure-instruction skill can reach every surface.

**Reach is a property of the skill, not a packaging choice.** Do not fight it.

This is the one place that guidance lives. Other files point here. No other file restates it.

---

## 2. The four stores, and what each one reaches

| Store | What lives there | Installed how | Reaches |
|---|---|---|---|
| **Vault `.claude/`** | The brain skills only | Copy into `~/.claude/`, per `<vault>/.claude/INSTALL.md` | Claude Code on that machine |
| **Library** | Every other master | Junction, or copy, into `~/.claude/skills/`, per `<library>/INSTALL.md` | Claude Code and Cowork on that machine |
| **Account store** | Pure-instruction skills only | Upload a `.skill` bundle through the Claude skills UI | Every Claude surface on the account: web, desktop, and mobile. No per-machine step. |
| **ChatGPT** | No skill store exists | A custom GPT built from the master, or the method pasted into an existing GPT's or Project's instructions | ChatGPT on the whole account: web and mobile |

**ChatGPT has no skill store.** The equivalent is a custom GPT, or instruction text added to an existing GPT
or Project. Either one is a copy of the master, so record the carrier and the refresh date in `registry.md`.

Only the account store syncs on its own. The vault store and the library both need a per-machine install.

### The Claude unit and the ChatGPT unit

| Claude | ChatGPT |
|---|---|
| The brain skills in `<vault>/.claude/skills/` | The **`Brain` GPT**. The main one. It is the brain client. |
| A library skill installed into `~/.claude/skills/` | A **custom GPT** built from the master, or the method added to an existing GPT |
| The account store, which syncs to every Claude chat surface | Nothing extra. **A custom GPT is already account-wide.** |

**A custom GPT needs no per-machine install and no bundle upload.** It exists on the account the moment it is
created, on web and on mobile.

**The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by
naming it. A long list of custom GPTs is hard to remember and hard to pick from, so a small method belongs
in a GPT the owner already uses.

**NOTE:** ChatGPT's features change. Check current behavior before you redesign anything around it.

### Staleness — the rule that does not soften

**The master in the library is the source of truth. A GPT's instructions are a copy.**

The copy goes stale the day the master changes, and nothing on either side reports it. This is the same
shape as the account-store upload problem in §6, with no hash to check, because a GPT's instruction text
cannot be hashed from outside.

So the record is the only control:

- **`registry.md` names every ChatGPT carrier for every skill, and the date it was last refreshed.**
- When a master changes, that table is the list of places to refresh **by hand**.
- `/brain-skill build` re-emits the artifact into `<name>.BUILD.md`, so refreshing is a paste, not a rewrite.

---

## 3. The one-store rule

**A skill lives in exactly one store.**

Four stores in the system is fine. **Two copies of one skill is the bug.** When the same name exists in two
stores, both load, and which one wins is ambiguous. Nothing anywhere reports this. There is no error, no
warning, and no log line.

`registry.md` is what makes it visible. One row per skill, one store per row. Write the row when you build
the master, not later.

---

## 4. Junction or copy

**Use a junction where the operating system allows it.** A junction makes drift structurally impossible. The
installed path and the master are the same bytes, so an edit to the master needs no reinstall.

**Copy only where a junction cannot work.** A copy is a snapshot. It drifts the moment you edit the master,
and you must redo it after every edit.

**WARNING:** junctions are **directory-only**. A lone command file is not a directory, so it must be copied,
and re-copied after every edit to the master. Keep command files thin for that reason.

The vault store copy-installs on purpose, for self-containment, and that is why the vault runbook ships a
drift check. The library prefers the junction, and needs a drift check only for the skills it copied.

---

## 5. Naming and shape of a master

A master is one folder under `<library>/skills/`.

```
<library>/skills/<name>/SKILL.md          required
<library>/skills/<name>/references/       optional
<library>/skills/<name>/scripts/          optional
<library>/skills/<name>.BUILD.md          BESIDE the folder, never inside it
```

Rules:

- **The folder name is lowercase kebab-case.** Words in lowercase, joined by single hyphens.
- **The folder name and the frontmatter `name:` must match exactly.** The packager refuses the build when
  they differ.
- **`SKILL.md` frontmatter carries `name` and `description`, and nothing else.** Both are required. Any
  other key makes the packager refuse the build. The third warning in §7 says what an extra key does on
  upload.
- **`references/` and `scripts/` are optional.** Use `references/` for material the skill reads on demand.
  Use `scripts/` for code the skill runs. A skill with a `scripts/` folder needs local execution, so it
  reaches Claude Code and Cowork only.
- **`<name>.BUILD.md` goes beside the folder, never inside it.** The packager sweeps everything under the
  skill folder into the bundle. A `BUILD.md` inside becomes context cost on every load, with no run-time
  value. The packager refuses the build when it finds one inside.

```yaml
---
name: <folder-name>
description: <one paragraph. See §9.>
---
```

The packager skips `.DS_Store`, `Thumbs.db`, and `.keep`. Everything else under the folder goes into the
bundle, so put nothing there that does not earn its place.

### What a `BUILD.md` must record

One `<name>.BUILD.md` per master. It is the operator's file, not the model's. Record all of this:

| Item | Why |
|---|---|
| **How to build** | The exact command, if the skill goes to the account store. |
| **Where it installs** | The target path on each operating system, and whether it is a junction or a copy. |
| **Which surfaces it reaches** | Written out, per §1. |
| **The ChatGPT artifact** | Only for a pure-instruction skill. The builder prompt, or the instruction block, in its own section. |
| **The SHA-256 and date of the last uploaded bundle** | Only if it goes to the account store. See §6. |
| **Any manual step** | A setting, a token, a folder to create, a permission the owner grants by hand. |

A manual step that lives only in someone's memory is a step that will be missed on the next machine.

---

## 6. Provenance — compute it, do not remember it

**The upload to the account store is the step with no safety net.** A rebuilt master that was never uploaded
leaves every chat surface serving an old version. Nothing anywhere reports the gap.

Rules:

- **Record the SHA-256 of the uploaded bundle** in that skill's `BUILD.md`, with the date.
- **Before you assume the live copy matches, rebuild and compare the hash.** The packager is deterministic.
  Two runs on an unchanged master produce byte-identical output, so the hashes agree. That makes the
  comparison a real check and not a guess.
- **Verify the published payload, not just that the upload reported success.**

---

## 7. Packaging traps — for the account store only

These apply to the account store and to nothing else. Each one is real.

**WARNING:** never build a bundle with PowerShell `Compress-Archive`. It writes backslash path separators
inside the zip. The skills UI rejects the archive with an error about characters in the path. That error
points at the file's location rather than at the bytes inside, so the wrong thing gets debugged. A Python
`zipfile` packager is immune, because `ZipInfo` rewrites the separator on write. Use
`tools/package-skill.py`.

**WARNING:** the reading tools hide the defect. Python's `zipfile.namelist()` normalizes a backslash to a
forward slash on read, and the Windows extractor accepts a backslash archive and installs it. The packager
was checked against a hand-built backslash archive. Its raw-header check returned true, while
`zipfile.namelist()` read that same archive back as `demo/SKILL.md`. **The only reliable check is the raw
local-file-header bytes, which the packager performs before it finishes.**

**WARNING:** only the frontmatter keys `name` and `description` round-trip. An extra key can make an upload
land the `SKILL.md` alone and silently drop every other file in the bundle. The packager refuses the build
when it finds any other key.

**WARNING:** watch for functional duplicates that no name collision catches. Two differently named skills
covering the same ground both load, and the model picks one. The one-line summaries in `registry.md` are how
you spot it.

### The packager

```
python tools/package-skill.py skills/<name>
```

It writes `skills/<name>.skill` beside the folder, lists the entries it packed, and prints the SHA-256.

It **refuses and exits 1** on any of these:

- a frontmatter key other than `name` or `description`
- a `name:` value that does not match the folder name
- a `BUILD.md` inside the skill folder
- a missing `SKILL.md`
- an empty folder

It skips `.DS_Store`, `Thumbs.db`, and `.keep`.

---

## 8. What is not a skill

Declining is a real outcome. **Record it as a `declined` row in `registry.md`, with the reason.** The reason
on the row stops the same candidate coming back on the next sweep.

| Decline reason | Where it belongs instead |
|---|---|
| **Three rules, not a method.** | A `CLAUDE.md`, or project instructions. |
| **Already covered by an existing skill.** | Absorb it there, where it will actually be read. |
| **A conclusion, not a method.** | That is knowledge. A wiki page. |
| **Done once, with no sign it repeats.** | Nowhere yet. Wait for the second time. |

---

## 9. Write the description for triggering

**The description is what makes the skill trigger.** The model reads it to decide whether to load the skill.
A vague description means a skill that never fires, or one that fires on the wrong work.

Write it this way:

- **Say what the skill does, in one clause.** Start with a verb.
- **List concrete trigger phrases** the owner actually types. Quote them.
- **Name the artifacts and the tools** involved: a file type, a folder, a command, a system name.
- **Say plainly when NOT to use the skill.** Name the neighbouring skill that owns that work, if there is
  one. This is the half most descriptions leave out, and it is the half that prevents a functional
  duplicate.

Keep it to one paragraph. It is the only part of the skill loaded before the decision to load the rest.
