---
name: process-inbox
description: >
  This skill should be used to compile the brain inbox into the wiki. Triggers include "/process", "process
  the inbox", or a scheduled nightly run. It reads each note in inbox/, builds concept-per-page wiki pages
  with frontmatter and links, moves the source note into raw/, updates _index.md and _log.md, and leaves
  ambiguous notes in the inbox flagged for the user.
---

# Process inbox → wiki

Run on a surface with native disk access to the vault (local Cowork/Claude Code with the Dropbox folder set
to Local/available offline), so step 3's move can actually remove the note from `inbox/`.

For each note in `inbox/`:
1. Read and understand it.
2. Compile into the wiki per `wiki/_conventions.md`, classifying on the three axes: pick the folder by
   lifecycle (`topics/` evergreen vs `projects/<slug>/` active), set `identity`, and tag the subject from the
   controlled vocabulary in `wiki/_tags.md` (don't invent tags — if a subject has no tag, propose adding one
   to `_tags.md`). Concept-per-page (a note may yield several), wikilinks to existing pages, no cross-domain
   duplication.
3. Move the source note from `inbox/` into `raw/<topic>/` (it becomes the immutable source). Set each new
   wiki page's `sources:` to that path.
4. Update `wiki/_index.md` and append to `wiki/_log.md` (`process` entries).
5. If a note is ambiguous or you're unsure where it belongs, LEAVE it in `inbox/` and add a `flag` line to
   `_log.md` describing the uncertainty — never force a bad filing.
6. Report: what you filed (and where), and what you left in the inbox and why.
