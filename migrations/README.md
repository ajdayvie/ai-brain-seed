# migrations/

One document per version step. Each one takes a vault **from the version below it to its own version**, and
nothing else.

The runbook that drives them is [../UPDATES.md](../UPDATES.md). It resolves the vault, works out its
version, picks the migrations, and holds the safety contract. A migration document assumes all of that
already happened.

## The migrations

| File | Takes a vault | Size | What it adds |
|---|---|---|---|
| [0.2.0-skill-library.md](0.2.0-skill-library.md) | 0.1.0 -> 0.2.0 | Large, about an hour | The skill library, `/brain-skill`, the rewritten install flow, tag vocabulary |
| [0.3.0-audio-digest.md](0.3.0-audio-digest.md) | 0.2.0 -> 0.3.0 | Small, 5 to 15 minutes | The digest verb, `digests/`, `/digest`, and the update path itself |

Apply them **in ascending order, one at a time**. A later migration assumes the earlier ones ran.

---

## The contract every migration follows

A migration document is read by an AI working in **someone else's vault**, on a machine it has not seen,
with real knowledge in it. So it carries all of this, in this order.

1. **What it adds**, in one paragraph. No marketing.
2. **Preconditions** — the exact files and text that must be present, and what to do when one is missing.
3. **New files**, each with its source path in `seed-vault/` or `seed-library/` and its destination path in
   the vault. Say which placeholders each one needs.
4. **Anchored edits** to existing files. Every edit names the **text to find** and the **text to write**.
   Never "replace `SCHEMA.md` with the template" — the owner's file is edited and the template is not.
5. **A missing-anchor rule** per edit: what it means, and what to do instead. The default is always: stop,
   show the owner the surrounding lines, and let them decide.
6. **Dependencies** the owner must install by hand, with the exact command, and what degrades if they skip
   it.
7. **Verification** — concrete steps with a pass or fail, not "check it works".
8. **What this migration must not touch**, restated, because the reader may have only this file loaded.
9. **Rollback** — how to undo it from the `.pre-<version>` backups.

**Additive beats surgical.** A migration that creates new files and makes three small anchored edits is one
an AI can apply correctly in a vault it has never seen. A migration that rewrites a file the owner has been
editing for months is not. When a change is too large to be surgical, say so in the document and make it a
**guided re-seed** with the owner in the loop, the way 0.2.0 does.

---

## Releasing a new version

Five files move together. Missing one leaves an existing vault unable to update.

1. `VERSION` — bump it.
2. `CHANGELOG.md` — add the section, with the migration link.
3. `migrations/<version>-<slug>.md` — write it, following the contract above.
4. `migrations/README.md` — add the row to the table.
5. `seed-vault/.claude/VERSION.md` — bump `seed-version:` and the fresh-install row, so a **new** vault is
   stamped with the right version.

Then run `python tools/build-standalone.py`, which regenerates `STANDALONE.md` from the sources.

**Test the migration against a copy of a real vault at the previous version**, not against a fresh seed. A
fresh seed has no owner edits in it, so it never exercises the anchored-edit path, which is the part that
breaks.
