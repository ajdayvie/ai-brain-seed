# Installing and updating the brain skills on a machine

Point a Claude Code session at this file and say **"install the brain skills on this machine"**. Everything
needed is here.

This file lives in the vault, so it is present and current on every machine the sync reaches.

---

## The one rule

```
<vault>/.claude/     SOURCE OF TRUTH. Edit here. Cloud sync carries it to every machine.
      |  copy-install
      v
~/.claude/           INSTALLED COPY. Never edit. Overwritten on every install.
```

**Never edit `~/.claude/commands/` or `~/.claude/skills/` directly.** An edit there is invisible to every
other machine, and the next install destroys it. When a skill needs changing, change the vault copy and
reinstall.

**A protocol change needs no install.** The skills are thin. They carry the job skeleton and the
vault-resolution logic, and they point at `SCHEMA.md`, `wiki/_conventions.md`, and `wiki/_tags.md` for the
rules. Those files live in the vault, so a rule change reaches every machine and every surface through sync
with no install step. Reinstall only when a **skill file itself** changes.

---

## Install or update

The vault path on this machine is `{{VAULT_PATH}}`.

### Windows (PowerShell)

```powershell
$b = "{{VAULT_PATH}}"
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\commands" | Out-Null
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills"   | Out-Null
Copy-Item "$b\.claude\commands\*" "$env:USERPROFILE\.claude\commands\" -Recurse -Force
Copy-Item "$b\.claude\skills\*"   "$env:USERPROFILE\.claude\skills\"   -Recurse -Force
```

### macOS and Linux

```bash
b="{{VAULT_PATH}}"
mkdir -p "$HOME/.claude/commands" "$HOME/.claude/skills"
cp -R "$b/.claude/commands/." "$HOME/.claude/commands/"
cp -R "$b/.claude/skills/."   "$HOME/.claude/skills/"
```

That installs 5 commands (`/capture`, `/process`, `/pull`, `/maintain`, `/brain-skill`) and 4 skills
(`capture-to-inbox`, `process-inbox`, `maintenance-pass`, `skill-library`).

The copy overwrites files of the same name. It does not delete anything else in `~/.claude/`.

**The skill library is a second, separate install.** Its runbook is `<library>/INSTALL.md`, in the library
folder beside the vault. **This runbook does not cover it.** These 4 skills are the brain skills, and they
stay in the vault so the vault keeps installing itself.

---

## One per-machine setting: `BRAIN_DIR`

It goes in `~/.claude/settings.json`, **not** in the vault, because the vault path differs per machine.

```json
{
  "env": {
    "BRAIN_DIR": "{{VAULT_PATH}}"
  }
}
```

**NOTE:** on Windows, JSON needs each backslash doubled, like
`"C:\\Users\\<you>\\Dropbox\\AI-Brain"`.

The skills read `BRAIN_DIR` so they resolve the vault from any project directory. Without it, a skill falls
back to searching the session's directories for one holding both `SCHEMA.md` and a `wiki/` folder. That
fallback works inside the vault and fails outside it. Set it.

If `~/.claude/settings.json` already exists, merge the `env` block into it. Do not replace the file.

---

## Optional: check for drift

A stale installed copy fails quietly. The check below makes it announce itself instead. Run it whenever a
command behaves in a way the vault copy does not explain.

### Windows (PowerShell)

Paste this in whole. It prints a line per mismatch and **nothing when the two sides agree**.

```powershell
$b = "{{VAULT_PATH}}"
$dst = "$env:USERPROFILE\.claude"
Get-ChildItem -Recurse -File "$b\.claude\commands", "$b\.claude\skills" | ForEach-Object {
  $rel  = $_.FullName.Substring("$b\.claude\".Length)
  $copy = Join-Path $dst $rel
  if (-not (Test-Path $copy)) { "MISSING: $rel" }
  elseif ((Get-FileHash $_.FullName).Hash -ne (Get-FileHash $copy).Hash) { "DIFFERS: $rel" }
}
```

`fc.exe` compares a single pair of files if you want to see the differing lines:
`fc.exe "%USERPROFILE%\.claude\skills\process-inbox\SKILL.md" "<vault>\.claude\skills\process-inbox\SKILL.md"`

### macOS and Linux

```bash
diff -rq "{{VAULT_PATH}}/.claude/commands" "$HOME/.claude/commands"
diff -rq "{{VAULT_PATH}}/.claude/skills"   "$HOME/.claude/skills"
```

**NOTE:** `diff -rq` also reports files that exist only on the installed side, as `Only in ...`. Those are
fine if they come from somewhere other than the vault. The PowerShell check walks the vault side only, so it
ignores them.

To fix any drift, re-run the install commands above. The vault always wins.

---

## Verify

Open a new Claude Code session and confirm all five commands are offered: `/capture`, `/process`, `/pull`,
`/maintain`, and `/brain-skill`.

Then run a real capture. `/capture test note` must write a file into `<vault>/inbox/` and report the full
path. If it writes into the current project instead, `BRAIN_DIR` is not set or not readable.

---

## What a reinstall does and does not cover

| Covered | Not covered |
|---|---|
| The 5 command files in `.claude/commands/` | `SCHEMA.md`, `wiki/_conventions.md`, `wiki/_tags.md`. Sync carries those, and no install is involved. |
| The 4 skill folders in `.claude/skills/` | `BRAIN_DIR` in `~/.claude/settings.json`. Set once per machine, by hand. |
| | The skill library. It installs separately, per `<library>/INSTALL.md`. |
| | The instruction block on the Cowork, chat, and ChatGPT surfaces. Each is configured in its own app. |

**WARNING:** reinstalling does not fix a wrong `BRAIN_DIR`. A skill that resolves the wrong vault writes
notes into the wrong folder and reports success. Check the path in the verify step above.
