---
name: capture-to-inbox
description: >
  This skill should be used when the user wants to quickly save something to the knowledge brain without
  filing it. Triggers include "capture this", "save this to the brain", "add to inbox", the /capture command,
  or when you proactively offer to capture durable knowledge. It writes ONE timestamped note to inbox/ and
  does no filing or wiki editing — capture is intentionally fast and dumb.
---

# Capture → inbox

1. Read `SCHEMA.md` §6a if not loaded.
2. Gather the content: either the text the user gives, or the durable knowledge from the current session
   (decisions, methods, specs, findings, corrected facts — skip transient chatter).
3. Write ONE file to `inbox/` named `YYYY-MM-DD-HHMM-<short-slug>.md`. Start it with a single `context:` line
   (where it came from / what it's about), then the content as clean markdown.
4. Do NOT create or edit wiki pages. Do NOT decide a topic/project/identity. That happens at process time.
5. Confirm what was captured and where.
