---
description: Check the ai-brain-seed kit for updates and install the ones I approve
---
Apply the **brain-update** skill. Any argument narrows it: $ARGUMENTS

Resolve the vault as `$BRAIN_DIR`. If that is unset or ambiguous, ask me for the absolute path and wait.
Never guess a default.

Follow the skill's Step 0 first: read `SCHEMA.md` §13 and `.claude/VERSION.md`, and work from those, not from
memory. Then fetch the kit into a scratch folder **outside the vault** and follow its `UPDATES.md`.

With no argument, check and report only:

- the version my vault is on, and the version the kit is on;
- one line per missing version, saying what it adds, from the kit's `CHANGELOG.md`;
- how long each would take.

**Then stop and ask which ones to apply.** Do not write anything into the vault before I say yes. Show me a
diff before every edit to a file I already have. Never run git in the vault.
