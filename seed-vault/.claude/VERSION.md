# Vault version

This file records which version of the **ai-brain-seed** kit this vault was built from, and every update
applied to it since. It is machine-facing bookkeeping. It is not a wiki page, and `/process`, `/pull`, and
`/maintain` ignore it.

**Do not edit the history table by hand.** The update runbook appends to it. A row you write yourself makes
the next update skip a migration it should have applied.

```
seed-version: 0.3.0
installed:    {{TODAY}}
vault-path:   {{VAULT_PATH}}
library-path: {{SKILLS_PATH}}
```

## Applied

| Version | Applied on | How | Notes |
|---|---|---|---|
| 0.3.0 | {{TODAY}} | fresh install | Built new from the 0.3.0 seed. No migration needed. |

## Checking for updates

Run **`/brain-update`** from any Claude Code session on a machine that can reach this vault. It reads the
kit's current version, compares it against `seed-version:` above, and walks you through anything missing.

Nothing expires. A vault that stays at its installed version keeps working. An update is a choice.

The kit lives at <https://github.com/ajdayvie/ai-brain-seed>. Its `UPDATES.md` is the runbook, and
`CHANGELOG.md` says what each version changed.

**Never run git in this vault.** An update clones or fetches the kit somewhere else and copies from there.
