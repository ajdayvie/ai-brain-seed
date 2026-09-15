# Changelog

Every released version of the seed kit, newest first. The current version is in [VERSION](VERSION).

A vault records the version it was built from, and every update applied to it, in
`<vault>/.claude/VERSION.md`. To bring an existing vault up to date, see [UPDATES.md](UPDATES.md).

**Versions are per-kit, not per-vault feature set.** A vault can sit at any version and still work. Nothing
here expires.

---

## 0.3.0 — 2026-09-15

**Added: the digest verb.** A fifth knowledge verb. `/digest` turns the substantive content of a session
into a spoken-word script plus a pre-rendered MP3, written to a new `digests/` section of the vault, for
listening to later.

- New vault folder `digests/`, with `digests/heard/` and `digests/_catalog.md`.
- New skill `audio-digest`, new command `/digest`, new script `.claude/scripts/render-digest.py`.
- `SCHEMA.md` gains **§6f DIGEST**, and §3 gains `digests/` as a section that sits outside the golden flow.
- `/process` is now explicitly forbidden from reading `digests/`. A spoken restatement compiled into the
  wiki would put lossy prose into the source of truth.
- `/maintain` gains the retention move: digests older than 60 days go to `heard/`. Nothing is deleted.

**Added: the update path.** An existing vault can now be brought forward without a reinstall.

- [UPDATES.md](UPDATES.md), the AI-facing update runbook. It probes a vault, works out its version, and
  applies each migration in order.
- `migrations/`, one document per version step.
- `<vault>/.claude/VERSION.md`, the version marker a vault carries.
- New skill `brain-update` and command `/brain-update`, so a vault at 0.3.0 or later can check for its own
  updates from any machine.

**Migration:** [migrations/0.3.0-audio-digest.md](migrations/0.3.0-audio-digest.md). It is additive. It
creates new files and makes three anchored edits to `SCHEMA.md`. It touches no wiki page, no note, and no
source.

---

## 0.2.0 — 2026-08-29

**Added: the skill library.** The brain holds knowledge. A repeatable method is not knowledge, it is a
skill, and skills now live in a library beside the vault.

- New `seed-library/` skeleton: `CONVENTIONS.md`, `INSTALL.md`, `registry.md`, `README.md`, and
  `tools/package-skill.py`.
- New skill `skill-library` and command `/brain-skill`, with the two-gate offer rule.
- `SCHEMA.md` gains §6e SKILL and rewrites §9 around the offer behavior.

**Rewritten: the install flow.** `SETUP.md` was replaced by `INSTALL.md`, a guided intake the AI reads and
follows. `STANDALONE.md` became a generated single-paste edition of the whole kit.

**Added:** `docs/skills.md`, `<vault>/.claude/INSTALL.md` as a per-machine runbook, controlled tag
vocabulary in `wiki/_tags.md`, and the self-sufficient-note rule in `SCHEMA.md` §6a.

**Migration:** [migrations/0.2.0-skill-library.md](migrations/0.2.0-skill-library.md). This one is large.
It is a guided re-seed of the vault's protocol and skill files, not a patch.

---

## 0.1.0 — 2026-07-15

Initial release. The vault skeleton, the four verbs (capture, process, pull, maintain), `SCHEMA.md`,
`PROCESS.md`, the wiki scaffolding, and the surface, scheduling, ChatGPT, and backfill docs.

Licensed as public domain under the Unlicense from 2026-07-15.
