---
name: maintenance-pass
description: >
  This skill should be used to clean, audit, or lint the brain. Triggers include "/maintain", "run a
  maintenance pass", "check for broken links", or "find contradictions". It scans the wiki for broken
  wikilinks, orphan pages, contradictions, stale pages, and invalid frontmatter, reports findings, applies
  safe fixes, and logs the pass.
---

# Maintenance pass (lint)

1. Scan `wiki/` for: broken `[[links]]`, orphan pages, contradictions between pages on the same topic, stale
   pages (whose `sources:` changed), missing/invalid frontmatter vs `_conventions.md`, and **off-vocabulary
   tags** — any `tags:` value not in `wiki/_tags.md`, plus tags that encode status/type/identity (which
   belong in their own fields). Map retired tags to their canonical replacement per `_tags.md`.
2. Report findings grouped by category with page paths.
3. Apply safe fixes (broken links, missing frontmatter fields, relink orphans into `_index.md`, remap retired
   tags to their canonical form). Do NOT silently resolve contradictions, and do NOT invent new canonical
   tags — propose vocabulary additions to `_tags.md` for the user. List both for the user.
4. Update `_index.md` if needed; append a `maintenance` entry to `_log.md`.
