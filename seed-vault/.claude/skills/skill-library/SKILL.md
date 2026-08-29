---
name: skill-library
description: >
  This skill should be used to sweep for, build, or install skills held in the owner's skill library.
  Triggers include "/brain-skill", "build a skill", "turn this into a skill", "make this repeatable",
  "install my skills", and "what could be a skill". It proposes repeatable methods, builds a master into the
  library and installs it on the current surface, and installs the library on this machine. It never builds a
  skill without the owner's yes.
---

# Skill library

**Library root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. `<library>` is the value of the `SKILLS_DIR` environment variable. Read it with
`echo "$SKILLS_DIR"`. If it is unset, use the sibling of `<brain>` named `{{SKILLS_DIRNAME}}`. **Never write
a bare relative path.** This skill runs from any project directory, and a relative path resolves against that
project instead of the brain or the library.

If `<library>` does not resolve to a folder holding `registry.md`, stop and report which paths you tried.
**Do not create a library without the owner's yes.**

## Step 0 — load the binding protocol, every run, before anything else

Read these two files and follow them. They are authoritative, they may have changed since the last run, and
this skill **deliberately does not copy their rules**. Do not work from memory.

- **`<library>/CONVENTIONS.md`** — the library contract: where a master lives, how far a skill reaches, the
  four stores, the one-store rule, junction versus copy, provenance, the packaging traps, and what is not a
  skill.
- **`<brain>/SCHEMA.md` §6e** — governs this job. §9 governs when to offer.

Where this skill and those files disagree, **they win**. Say so in the report, so the skill gets fixed.

## The signal

**The bar is high on purpose.** Both gates must hold. The owner will run the method again, **and** it is
worth a maintained artifact, meaning a **business process** they run, a **personalization** of how they want
work done, or a **way of working with AI** they repeat. **Name that kind in the offer. If you cannot name
one, do not offer.**

Stay silent for minor process detail, for one-off troubleshooting, and for a fact, a finding, a reference, a
decision, or a corrected claim. **When in doubt, stay silent.** The full rule, with all three worked
examples, is in `<brain>/SCHEMA.md` §9.

## The job

Pick the mode from the argument. No argument means sweep.

### Mode 1 — sweep (no argument)

1. Read `<library>/registry.md` first, so a declined skill is not proposed again.
2. Scan recent pages under `<brain>/wiki/` and recent entries in `<brain>/wiki/_log.md` for a repeatable
   method the owner still runs by hand.
3. Propose each candidate. **One offer each.** Say in one sentence what the skill would do.
4. **Build nothing without a yes.** A proposal is not a yes.
5. On a yes, run Mode 2 for that candidate now.

### Mode 2 — build (`build <name>`, or a yes to an offer)

The owner is present and has said yes. **Build it now.** No inbox note, no queue, no second command.

1. **Write the master** to `<library>/skills/<name>/SKILL.md`. Frontmatter carries `name` and `description`
   only. Read `<library>/CONVENTIONS.md` for where the master lives and how far the skill reaches.
2. **Write `<library>/skills/<name>.BUILD.md`**, beside the folder and never inside it.
3. **Add a row** for the skill to `<library>/registry.md`, marked built. A skill the owner declines gets a
   declined row with the reason instead.
4. **Install it in the form this surface supports**, per the table below, then per `<library>/INSTALL.md`.
5. **Append an entry** to `<brain>/wiki/_log.md` recording what was built. That is the "what changed" record,
   and it is the one wiki write allowed outside process.
6. **Report** what was installed, and what the owner must still do by hand.

| Surface | The installed form |
|---|---|
| Claude Code, Cowork | A skill, installed into `~/.claude/skills/` per `<library>/INSTALL.md` |
| claude.ai chat | No install from chat. Build a bundle for the account store for the owner to upload, or add the method to a Project's instructions. |
| ChatGPT | A custom GPT built from a generated builder prompt, or the method added to an existing GPT's or a Project's instructions |

**The rule, rather than a taxonomy:** install it the way this surface installs a method. If the surface
has no mechanism for that, say so and produce the artifact the owner can install by hand.

**The memory trap.** Some surfaces offer only a **memory** feature. A memory entry is an acceptable installed
form. It is **never** the artifact. Per-surface memory does not travel between surfaces and is not durable,
which is the exact problem this system exists to fix. **The master goes in the library. The memory entry is a
local copy.** Never store a method only in a surface's memory and call it saved.

**The master is written in every case, on every surface.** It is the durable copy, and it is what lets the
method reach other surfaces later.

### Mode 3 — install the library (`install`)

1. Follow `<library>/INSTALL.md` for this machine.
2. Report which skill reaches which surface.
3. Name anything that is a master with no install.

## Hard rules

- **Never write a master without an explicit yes from the owner.** A proposal is not a yes.
- **Never put `BUILD.md` inside the skill folder.** The packager sweeps the folder into the bundle, so a
  `BUILD.md` inside becomes context cost on every load with no run-time value.
- **Never let one skill exist in two stores.** Both copies load, and which one wins is ambiguous.
- **Never claim a skill reaches a surface it was not installed on.** Only the account store syncs by itself.
  **ChatGPT has no skill store**, which is why the unit there is a custom GPT.
- **An instruction copy in a GPT or a Project is a copy, and it goes stale the day the master changes.** Never
  describe it as synced. `<library>/registry.md` is the refresh list.
- Never run git in the vault or in the library.
