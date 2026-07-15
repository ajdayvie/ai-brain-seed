# Scheduling — the nightly compile

The brain maintains itself only if the inbox is regularly processed. The recommended setup is a **scheduled
task on an always-on local machine running headless Claude Code**; alternatives follow for other situations.

**The binding constraint:** the process step *moves* notes from `inbox/` into `raw/` — it deletes files from
the local Dropbox vault. So the job must run somewhere with **native disk access to the vault** (Dropbox
folder set to Local / "Make available offline"). Cloud-hosted schedulers cannot see the vault; don't use
them for this.

## Option A (recommended) — OS scheduler + headless Claude Code

An always-on machine (a desktop that stays on, a home server, a mini PC) runs the compile nightly with no
GUI and no app window. This is the most robust option: it survives reboots and needs nothing open.

### The pieces (any OS)

1. **Auth token.** A bare headless `claude -p` subprocess does not inherit the interactive app's login. Run
   `claude setup-token` once — it generates a long-lived OAuth token on your existing Claude subscription
   (no extra billing). Store it in the environment variable `CLAUDE_CODE_OAUTH_TOKEN` for the account the
   task runs as. Note: stored as an env var it sits in plaintext within your OS account's trust boundary.
2. **Wrapper script** that: changes to the vault directory, runs the compile prompt, and appends to a log
   file. The core command:
   ```
   claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions
   ```
   `--permission-mode bypassPermissions` is required — unattended file moves/edits would otherwise stall on
   approval prompts. It is scoped to a vault of your own notes; keep the prompt narrow.
3. **Scheduler entry** that runs the wrapper nightly (2:00 AM is a good default — after your workday, before
   the next).

Failure is non-destructive: if a run errors before doing work, no notes are moved and the inbox is intact —
the next night catches up.

### Windows — Task Scheduler

Wrapper `process-inbox.ps1` (adjust paths):

```powershell
Set-Location "C:\Users\<you>\Dropbox\AI-Brain"
$log = "C:\Users\<you>\.claude\brain\logs\process-$(Get-Date -Format yyyy-MM).log"
"`n===== $(Get-Date -Format s) =====" | Out-File $log -Append -Encoding utf8
& "$env:USERPROFILE\.local\bin\claude.exe" -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions *>> $log
```

Task settings that matter: Daily at 2:00 AM · Action:
`powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "<path>\process-inbox.ps1"`
· **Run only when user is logged on** (Interactive logon, so the user env var with the token is picked up) ·
**Run task as soon as possible after a scheduled start is missed** (`StartWhenAvailable`) · optionally **Wake
the computer to run this task** · stop after 1 hour · do not start a new instance if already running. Set the
token once with `setx CLAUDE_CODE_OAUTH_TOKEN "<token>"`.

### macOS — launchd (or cron)

Wrapper `process-inbox.sh` (make executable, adjust paths):

```bash
#!/bin/bash
export CLAUDE_CODE_OAUTH_TOKEN="<token>"   # or source it from a protected file
cd "$HOME/Dropbox/AI-Brain" || exit 1
LOG="$HOME/.claude/brain/logs/process-$(date +%Y-%m).log"
mkdir -p "$(dirname "$LOG")"
echo -e "\n===== $(date -Iseconds) =====" >> "$LOG"
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave any ambiguous note in inbox/ with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions >> "$LOG" 2>&1
```

Schedule with a launchd user agent (`~/Library/LaunchAgents/com.brain.process.plist`) using
`StartCalendarInterval` at Hour 2, Minute 0 — launchd runs missed jobs on wake, which cron does not. Plain
cron (`0 2 * * * /path/to/process-inbox.sh`) also works on any Unix if the machine is reliably awake.

## Option B — Cowork / Claude Desktop scheduled task

If you'd rather stay inside the app: in a Cowork project pointed at the vault, create a scheduled task
("every night at 2:00 AM, process the brain inbox per SCHEMA.md…"). Simpler to set up, but it requires the
desktop app to be open and the machine awake at run time — fine for a desktop you never close, fragile
otherwise.

## Option C — manual cadence (no always-on machine)

The compile doesn't have to be nightly; it has to be *regular*. If you work from a laptop that sleeps:

- **End-of-day habit:** run `/process` in Claude Code (in the vault) at the end of any day you captured
  something. It takes a minute or two for a handful of notes.
- **Reminder-driven:** set a recurring reminder (calendar, todo app) — "process the brain inbox" — daily or
  every few days. When it fires, open the vault in Claude Code and run `/process`.
- **Opportunistic:** whenever a session's Claude notices a non-empty inbox in the vault, it may offer to
  process; accept when convenient.

The inbox is designed to tolerate lag — notes just wait, nothing is lost. What breaks the system is *never*
processing: the wiki stops compounding and pulls go stale. Pick the cadence you'll actually keep.

## Whichever option: verify the loop monthly

Check `wiki/_log.md` occasionally — you should see `process` entries at your expected cadence, and any
`flag` entries are ambiguous notes waiting for your judgment. Silence in the log means the schedule broke
(commonly: expired token, moved vault path, renamed task).
