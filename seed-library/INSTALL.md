# Installing and updating the skill library on a machine

Point a Claude Code session at this file and say **"install the skill library on this machine"**. Everything
needed is here.

This file lives in the library, so it is present and current on every machine the sync reaches.

**This is a second install.** The vault installs its own skills separately, per `<vault>/.claude/INSTALL.md`.
The two stores do not overlap, and neither install covers the other.

---

## The one rule

```
<library>/skills/     SOURCE OF TRUTH. Edit here. Cloud sync carries it to every machine.
      |  junction, or copy
      v
~/.claude/skills/     INSTALLED. A junction IS the master. A copy is a snapshot that drifts.
```

**Never edit a copied skill in `~/.claude/skills/`.** An edit there is invisible to every other machine, and
the next install destroys it. Change the master in the library and reinstall.

A junction has no second copy to edit. The installed path and the master are the same bytes, so an edit to
the master needs no reinstall. That is why the junction is the default.

The library path on this machine is `{{SKILLS_PATH}}`.

---

## Install by junction (preferred)

Install one skill at a time. There is no bulk step, because each skill is a separate junction.

### Windows (PowerShell)

```powershell
$s = "{{SKILLS_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
New-Item -ItemType Junction `
  -Path   "$env:USERPROFILE\.claude\skills\<name>" `
  -Target "$s\skills\<name>"
```

The `cmd.exe` form does the same thing:

```
mklink /J "%USERPROFILE%\.claude\skills\<name>" "<library>\skills\<name>"
```

**A junction needs no administrator rights. A symbolic link does.** That is the whole reason this runbook
uses a junction. Do not substitute `New-Item -ItemType SymbolicLink`, and do not substitute `mklink /D`.
Both ask for rights you should not need for this.

**NOTE:** a junction points at a directory on a local volume. The library must be a real folder on local
disk, which it already is, because the sync folder is set to Local / "Make available offline".

To remove a junction, delete the junction itself with `Remove-Item`. Deleting the junction does not touch
the master.

### macOS and Linux

```bash
s="{{SKILLS_PATH}}"
mkdir -p "$HOME/.claude/skills"
ln -s "$s/skills/<name>" "$HOME/.claude/skills/<name>"
```

`ln -s` writes a symbolic link. It needs no elevated rights on macOS or Linux.

---

## Install by copy (the fallback)

Use a copy only where a junction or a symbolic link cannot work.

**WARNING:** a copy drifts. It is a snapshot taken at one moment. The moment you edit the master, the
installed copy is stale, and nothing reports it. **Redo the copy after every edit to the master.**

**WARNING:** junctions are directory-only. A lone command file is not a directory, so it must be copied, and
re-copied after every edit. Keep command files thin for that reason.

### Windows (PowerShell)

```powershell
$s = "{{SKILLS_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item "$s\skills\<name>" "$env:USERPROFILE\.claude\skills\" -Recurse -Force
```

### macOS and Linux

```bash
s="{{SKILLS_PATH}}"
mkdir -p "$HOME/.claude/skills"
cp -R "$s/skills/<name>" "$HOME/.claude/skills/"
```

The copy overwrites files of the same name inside that one skill folder. It does not delete anything else in
`~/.claude/skills/`.

---

## One optional per-machine setting: `SKILLS_DIR`

It goes in `~/.claude/settings.json`, **not** in the library, because the library path differs per machine.

```json
{
  "env": {
    "BRAIN_DIR":  "{{VAULT_PATH}}",
    "SKILLS_DIR": "{{SKILLS_PATH}}"
  }
}
```

**NOTE:** on Windows, JSON needs each backslash doubled, like
`"C:\\Users\\<you>\\Dropbox\\AI-Skills"`.

`SKILLS_DIR` is optional. **When it is unset, the skills resolve the library as the sibling of `BRAIN_DIR`
named `{{SKILLS_DIRNAME}}`.** Set `SKILLS_DIR` when the library is not a sibling of the vault, or when the
folder carries a different name on this machine.

If `~/.claude/settings.json` already exists, merge the `env` block into it. Do not replace the file.

---

## Verify

Open a **new** Claude Code session and confirm the installed skill is offered. A session started before the
install does not see it.

Then run the skill on real work and confirm it does what the master says. A junction that points at a folder
with no `SKILL.md` installs cleanly and does nothing.

---

## Optional: check for drift

A stale copy fails quietly. The check below makes it announce itself instead. Run it after you edit a master,
or whenever an installed skill behaves in a way the master does not explain.

A junction-installed skill always agrees, because both sides are the same bytes. **This check exists for the
skills you copied.** It also names any master with no install at all.

### Windows (PowerShell)

Paste this in whole. It prints a line per mismatch and **nothing when the two sides agree**.

```powershell
$s = "{{SKILLS_PATH}}"
$dst = "$env:USERPROFILE\.claude\skills"
Get-ChildItem -Recurse -File "$s\skills" | ForEach-Object {
  $rel  = $_.FullName.Substring("$s\skills\".Length)
  $copy = Join-Path $dst $rel
  if (-not (Test-Path $copy)) { "NOT INSTALLED: $rel" }
  elseif ((Get-FileHash $_.FullName).Hash -ne (Get-FileHash $copy).Hash) { "DIFFERS: $rel" }
}
```

`NOT INSTALLED` on every file of one skill means that master is not installed on this machine. That is a
normal state, not an error. Install it if you want it here.

`fc.exe` compares a single pair of files if you want to see the differing lines:
`fc.exe "%USERPROFILE%\.claude\skills\<name>\SKILL.md" "<library>\skills\<name>\SKILL.md"`

### macOS and Linux

```bash
diff -rq "{{SKILLS_PATH}}/skills/<name>" "$HOME/.claude/skills/<name>"
```

**NOTE:** `diff -rq` also reports files that exist only on the installed side, as `Only in ...`. Those are
fine if they come from somewhere other than the library. The PowerShell check walks the library side only,
so it ignores them.

To fix any drift, redo the copy. The master always wins. Better: replace the copy with a junction or a
symbolic link, and the drift cannot come back.

---

## The account store

The account store syncs to every Claude surface on the account: web, desktop, and mobile. **There is no
per-machine step.** It is the only store that reaches the chat surfaces.

**Only pure-instruction skills belong here.** See `CONVENTIONS.md` §1. A skill that needs a shell command, a
script, or a file write reaches Claude Code and Cowork only. A bundle uploaded to the account store would
reach the chat surfaces and fail on every one of them.

Three steps:

1. **Build the bundle.**

   ```
   python tools/package-skill.py skills/<name>
   ```

   It writes `skills/<name>.skill` beside the folder, lists the entries it packed, and prints the SHA-256.
   It refuses and exits 1 on a frontmatter key other than `name` or `description`, on a `name:` value that
   does not match the folder name, on a `BUILD.md` inside the skill folder, on a missing `SKILL.md`, and on
   an empty folder.

2. **Upload it** through the Claude skills UI.

   **WARNING:** never build the bundle with PowerShell `Compress-Archive`. It writes backslash path
   separators inside the zip, and the skills UI rejects the archive with an error about characters in the
   path. That error points at the file's location rather than at the bytes inside, so the wrong thing gets
   debugged. Use the packager. It checks the raw local-file-header bytes before it finishes.

3. **Record the SHA-256 and the date** in `skills/<name>.BUILD.md`.

   The build is deterministic, so two runs on an unchanged master produce byte-identical output and the same
   SHA-256. That turns "is the uploaded copy current?" into a hash comparison instead of a memory test.
   Rebuild, compare, and verify the published payload. Do not settle for an upload that reported success.

**A master rebuilt and never uploaded leaves every chat surface serving an old version, and nothing anywhere
reports the gap.** This is the step with no safety net.

---

## ChatGPT

**ChatGPT has no skill store.** There is nothing to install and nothing to upload.

The equivalent is a **custom GPT**, or **instruction text added to an existing GPT or Project**. Only a
pure-instruction skill reaches ChatGPT at all. See `CONVENTIONS.md` §1.

**A custom GPT is account-wide.** It needs no per-machine install and no bundle upload. It exists on the
account the moment it is created, on web and on mobile.

**The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by
naming it.

**Two branches. The AI chooses, and says which it chose and why, in one sentence.** A method worth its own
GPT gets one. Everything else goes into a GPT or Project the owner already uses.

**NOTE:** ChatGPT's features change. Check current behavior before you redesign anything around it.

### Branch A — its own custom GPT

1. **Open the ChatGPT GPT builder.**
2. **Paste the builder prompt** that `/brain-skill build <name>` generated. It is in the ChatGPT section of
   `skills/<name>.BUILD.md`.
3. **Keep the GPT private.** Do not publish it to the GPT Store.
4. **Enable the Dropbox app only when the method needs the brain.** A method that never reads the
   vault needs no app and no Step 0 protocol-loading block.
5. **Add no custom Actions.**

**WARNING:** do not upload library files or vault files as GPT Knowledge. A copy in Knowledge is a second
brain that goes stale, and it breaks the point-don't-copy rule. The GPT reads the vault at run time through
the Dropbox app.

### Branch B — added to an existing GPT or Project

1. **Open the target GPT or Project.** It is usually the `Brain` GPT.
2. **Paste the instruction block** that `/brain-skill build <name>` generated, from the ChatGPT section of
   `skills/<name>.BUILD.md`, into that GPT's or Project's instructions.

### Both branches

**The generated artifact lives in `skills/<name>.BUILD.md`.** `/brain-skill build <name>` writes it there,
and re-emits it on every rebuild. **Refreshing a ChatGPT copy is a paste, never a rewrite.**

`BUILD.md` sits beside the skill folder and never inside it, so the artifact adds no weight to a bundle.

**Record the carrier and the date in `registry.md`.** The carrier is the GPT or Project that holds the text.
The text is a copy, so it goes stale the day the master changes, and nothing on either side reports it. When
you edit a master, that table is the list of places to refresh by hand.

---

## What an install does and does not cover

| Covered | Not covered |
|---|---|
| One skill folder in `~/.claude/skills/`, per junction or per copy | `CONVENTIONS.md` and `registry.md`. Sync carries those, and no install is involved. |
| Nothing else. Each skill is installed on its own. | `SKILLS_DIR` in `~/.claude/settings.json`. Set once per machine, by hand. |
| | The account store. Build and upload a bundle instead. |
| | ChatGPT. Build the custom GPT, or paste the instruction block into the existing GPT, by hand. |

**WARNING:** installing a library skill does not install the brain skills. Those live in the vault and use
their own runbook at `<vault>/.claude/INSTALL.md`.
