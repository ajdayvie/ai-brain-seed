---
description: Sweep for, build, or install a skill from the skill library
---
Apply the **skill-library** skill in the mode named by: $ARGUMENTS

- No argument — sweep for methods that clear both gates in `SCHEMA.md` §9, propose them one at a time, and
  build nothing.
- `build <name>` — build `<name>` now: write the master, install it on this surface, and log it.
- `install` — install the library on this machine and report what reaches which surface.

The command is `/brain-skill`, not `/skill`. The longer name avoids a collision with other skill-building
commands already installed on this machine.

Resolve the vault as `$BRAIN_DIR` and the library as `$SKILLS_DIR`, falling back to the sibling of
`$BRAIN_DIR` named `{{SKILLS_DIRNAME}}`. Never use a bare relative path.

Follow the skill's Step 0 first: read `<library>/CONVENTIONS.md` and `SCHEMA.md` §6e, and work from those,
not from memory.

Never write a master without my explicit yes.
