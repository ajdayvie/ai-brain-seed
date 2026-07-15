---
title: Tag Vocabulary
type: reference
identity: na
tags: [brain, knowledge-management]
status: stable
created: {{TODAY}}
updated: {{TODAY}}
sources: []
---

# Tag Vocabulary — the controlled list

Tags are the **subject** axis only (see the three axes in [[_conventions#The three axes]]). This is the
canonical list: every `tags:` value on a wiki page must come from here. Adding a tag means **adding it here
first**, then using it — never the reverse. `maintenance-pass` lints pages against this file.

**Tags are not the place for:**
- **status** — `draft | stable | needs-review` go in the `status:` field, never as tags.
- **type** — `concept | reference | source-summary | …` go in the `type:` field (so no `talk`/`source` tags).
- **identity** — `{{IDENTITY_VALUES}}` go in the `identity:` field.

Keep the list small. Prefer an existing tag over a near-synonym; reach for a new one only when a real subject
has no home here. New tags are added at process time by proposing them here first.

## Canonical tags

### The brain / knowledge system
- `brain` — this knowledge base itself, its architecture and storage.
- `knowledge-management` — PKM concepts, methods, the library/Karpathy framing.
- `workflow` — capture / process / pull and other procedures.

### Starter subjects
<!-- The vocabulary grows with the brain. As real subjects appear during processing, add a tag here with a
     one-line definition, then use it. Group related tags under a heading. Delete this comment once the list
     has real entries. -->

## Retired / redirected (do not use)
<!-- When a tag is replaced or absorbed, move it here with an arrow to its canonical replacement, e.g.:
- `meta`, `system` → use `brain`. -->
