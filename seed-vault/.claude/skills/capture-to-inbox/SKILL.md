---
name: capture-to-inbox
description: >
  This skill should be used when the user wants to quickly save something to the knowledge brain without
  filing it. Triggers include "capture this", "save this to the brain", "add to inbox", the /capture command,
  or when you proactively offer to capture durable knowledge. It writes ONE timestamped note to the vault's
  inbox/ and does no filing or wiki editing — capture is intentionally fast and dumb.
---

# Capture -> inbox

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `inbox/`.** This skill runs from any project
directory, and a relative path resolves against that project instead of the brain.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §6a** and follow it. It is authoritative, it may have changed, and this skill does
not copy its rules. Capture touches no wiki page, so `wiki/_conventions.md` and `wiki/_tags.md` are not
needed here.

## The job

1. Gather the content: the text the user gives, or the durable knowledge from the current session. Durable
   means a decision, a method, a spec, a finding, or a corrected fact. Skip transient chatter.
2. Write ONE file to `<brain>/inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md`. Start it with a single
   `context:` line saying where it came from and what it is about. The content follows as clean markdown. No
   frontmatter.
3. **Make the note self-sufficient**, per SCHEMA §6a step 3. The note is filed later, on a different machine,
   by a run that can see only the vault. Write down the substance itself. Cite a repo, a branch, a
   transcript, or a URL as provenance in addition to the content, never instead of it. When the capture came
   from work in another repo, say so in the `context:` line.
4. **Offer a skill only when the note clears both gates in `SCHEMA.md` §9.** The owner will run the method
   again, **and** it is a business process, a personalization, or a way of working with AI that they repeat.
   **Name that kind in the offer. If you cannot name one, do not offer.** Stay silent for minor process
   detail, for one-off troubleshooting, and for a fact, a finding, a reference, a decision, or a corrected
   claim. **When in doubt, stay silent.** Offer once, in one line, after the note is written. The
   offer never blocks or delays the capture. On a yes, hand off to the **skill-library** skill in build mode,
   which builds it now per `SCHEMA.md` §6e.
5. Do NOT create or edit a wiki page. Do NOT choose a topic, project, or identity. That happens at process
   time.
6. Confirm what was captured, and echo the full path you wrote.
