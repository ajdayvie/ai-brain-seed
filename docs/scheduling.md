# Scheduling — the nightly compile

The brain maintains itself only if the inbox is processed regularly. This doc ranks three ways to do that,
and states the real failure mode of each.

## The binding constraint

The process step **moves** notes out of `inbox/` and into `raw/`. It deletes files from the vault folder on
disk. So the job must run on a surface with **native disk access to the vault**, with the vault folder set
to Local / "Make available offline".

A cloud runner cannot do it. A connector cannot do it. Both can read the vault, and neither can complete the
move. Do not schedule the compile anywhere that reaches the vault only over the network.

Failure is not destructive. If a run errors before it does work, no notes move and the inbox stays intact.
The next run catches up.

## Option A (recommended) — a scheduled task in the Claude desktop app

Point a Cowork project at the vault folder, then create a scheduled task in that project. A prompt like this
works:

```text
Every night at 2:00 AM, process the brain inbox. Read SCHEMA.md and wiki/_conventions.md first, apply the
process-inbox protocol to every note in inbox/, and summarize what you filed and what you left.
```

This is the simplest option. It uses the login the app already has, so there is no token to create and no
script to maintain. It runs with real disk access, so the move into `raw/` works.

**NOTE:** the task needs the app running when it is due. If the app is closed at that time, the run happens
at next launch, not on time. On a machine you never shut down, that gap is rare. On a laptop that sleeps or
closes each night, the compile drifts to whenever you next open the app.

Pick this option when the desktop app runs on a machine that stays on.

## Option B — OS scheduler plus headless Claude Code

An OS scheduler starts a headless `claude -p` run on a fixed clock. It survives reboots and needs no app
window. This is the most durable option once it works.

**WARNING:** a headless run does **not** inherit the interactive login. It prefers `ANTHROPIC_API_KEY` over
a subscription session, so a task that works by hand can fail every night with no obvious error. **This auth
path is the most common silent failure of this option.**

The fix, once, before you schedule anything:

1. Run `claude setup-token`. It generates a long-lived OAuth token on your existing subscription. It adds no
   billing.
2. Store the result in the environment variable `CLAUDE_CODE_OAUTH_TOKEN`, for the OS account the scheduled
   task runs as.
3. Run the wrapper by hand once, as that account, and confirm it completes.

**NOTE:** an environment variable holds the token in plaintext inside the trust boundary of that OS account.
Anyone with the account has the token.

### The pieces (any OS)

1. **The auth token**, per the warning above.
2. **A wrapper script** that changes to the vault directory, runs the compile prompt, and appends output to
   a log file.
3. **A scheduler entry** that runs the wrapper nightly. 2:00 AM is a good default. It is after the workday
   and before the next one.

The core command:

```
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions
```

`--permission-mode bypassPermissions` is required. An unattended run would otherwise stall on approval
prompts for file moves and edits. It is scoped to a vault of your own notes. Keep the prompt narrow.

### Windows — Task Scheduler

Wrapper `process-inbox.ps1`. Adjust the paths.

```powershell
Set-Location "C:\Users\<you>\Dropbox\AI-Brain"
$log = "C:\Users\<you>\.claude\brain\logs\process-$(Get-Date -Format yyyy-MM).log"
"`n===== $(Get-Date -Format s) =====" | Out-File $log -Append -Encoding utf8
& "$env:USERPROFILE\.local\bin\claude.exe" -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions *>> $log
```

Set the token once with `setx CLAUDE_CODE_OAUTH_TOKEN "<token>"`.

Task settings that matter:

| Setting | Value | Why it matters |
|---|---|---|
| Trigger | Daily at 2:00 AM | After the workday, before the next |
| Action | `powershell.exe -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "<path>\process-inbox.ps1"` | Runs the wrapper with no window |
| Run only when user is logged on | Yes | Interactive logon, so the user environment variable with the token is picked up |
| Run task as soon as possible after a scheduled start is missed | Yes (`StartWhenAvailable`) | Catches up after the machine was off |
| Wake the computer to run this task | Optional | Useful on a machine that sleeps |
| Stop the task if it runs longer than | 1 hour | Stops a hung run |
| If the task is already running | Do not start a new instance | Stops two runs touching the same notes |

### macOS — launchd (or cron)

Wrapper `process-inbox.sh`. Make it executable and adjust the paths.

```bash
#!/bin/bash
export CLAUDE_CODE_OAUTH_TOKEN="<token>"   # or source it from a protected file
cd "$HOME/Dropbox/AI-Brain" || exit 1
LOG="$HOME/.claude/brain/logs/process-$(date +%Y-%m).log"
mkdir -p "$(dirname "$LOG")"
echo -e "\n===== $(date -Iseconds) =====" >> "$LOG"
claude -p "Read SCHEMA.md and wiki/_conventions.md, then apply the process-inbox protocol to everything in inbox/: compile notes into the wiki, move sources into raw/, update wiki/_index.md and wiki/_log.md, and leave a note in inbox/ only for a filing-destination ambiguity, with a flag line in _log.md. Then summarize what was processed." --permission-mode bypassPermissions >> "$LOG" 2>&1
```

Schedule it with a launchd user agent at `~/Library/LaunchAgents/com.brain.process.plist`, using
`StartCalendarInterval` at Hour 2, Minute 0. launchd runs missed jobs on wake. cron does not.

Plain cron also works on any Unix if the machine is reliably awake:

```
0 2 * * * /path/to/process-inbox.sh
```

## Option C — manual cadence

Use this when you have no always-on machine. The compile does not have to be nightly. It has to be regular.

The full fallback policy, all four parts:

1. **Once a day, at the end of any day you captured something.** Run `/process` in the vault. A handful of
   notes takes a minute or two.
2. **Whenever the inbox gets large.** Rule of thumb: **10 or more notes, or any note older than 3 days.**
   Process at either threshold, even on a day you captured nothing.
3. **A recurring reminder** in a calendar or a task app, so step 1 does not depend on memory.
4. **A session-start nudge.** Ask any brain-aware session to check the inbox size and to offer to process
   when it crosses the threshold above.

The failure mode, stated plainly: the inbox tolerates lag. **Nothing is lost while notes wait.** What breaks
the system is **never** processing. The wiki stops growing, and pulls go stale because the newest knowledge
is still sitting unfiled.

Pick the cadence you will actually keep.

## Whichever option: verify the loop monthly

Open `wiki/_log.md` about once a month and check two things.

- **`process` entries at your expected cadence.** Silence in the log means the schedule broke. The common
  causes are an expired token, a moved vault path, and a renamed or disabled task.
- **`flag` entries.** Each one is a note the run could not place. It waits for your decision on where it
  belongs.
