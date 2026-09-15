# Skills — turning a repeated method into a skill

This document explains the skill library: what it is, why it sits beside the vault, and what the system does
with a method you keep repeating. Read it if you are deciding whether you want this part of the kit.

The library is optional. The brain works without it.

The binding contract lives in the library itself, at `seed-library/CONVENTIONS.md`. **That file is the rule.**
This document explains the shape. Where they disagree, the contract wins.

---

## 1. The idea

**A skill is a verb. Knowledge is a noun.**

The wiki holds the nouns: facts, decisions, findings, corrected claims. The library holds the verbs: the
methods you would otherwise explain again in every new session.

Working with the brain surfaces those methods. The same recipe gets explained again. The same checklist gets
rebuilt from scratch. The same steps get pasted into a new session, a little differently each time. The
system should notice and offer to turn one into a skill.

## 2. Where the library sits

The library is a **sibling of the vault**, in the same synced folder. The default name is `AI-Skills`.

```
~/Dropbox/
  AI-Brain/                    the vault. Knowledge.
  AI-Skills/                   the library. Methods.
    README.md                  what this is, and the one-store rule
    CONVENTIONS.md             the contract
    INSTALL.md                 per-machine install. Junction or copy.
    registry.md                the catalog. Built and declined.
    tools/package-skill.py     builds a .skill bundle for the account store
    skills/<name>/SKILL.md     a master. Bundle contents only.
    skills/<name>.BUILD.md     build and install notes, BESIDE the folder, never inside it
```

**Why the library is not inside the vault.** A tool is not knowledge. Putting methods inside a knowledge
base blurs what the brain is.

**`BUILD.md` goes beside the skill folder, never inside it.** The packager sweeps everything under the skill
folder into the bundle. A `BUILD.md` inside becomes context cost on every load, with no run-time value.

## 3. Where a master lives, and how far it reaches

A skill that needs the brain to exist stays in `<vault>/.claude/skills/`, so the vault keeps installing
itself. Everything else goes in the library.

A skill that runs a shell command, a script, or a file write works only where there is disk access, which
means Claude Code and Cowork. A pure-instruction skill can reach every surface.

**`seed-library/CONVENTIONS.md` §1 is the binding version of that guidance.** Read it there before you build.

## 4. The offer

**The AI proposes. It never builds silently.**

Two moments, and nowhere else:

- **capture** — you are present and have just decided something is worth keeping. If it is a method, now is
  the moment to ask.
- **maintain** — you are deliberately looking for improvements, so a sweep belongs here.

**Never at process.** Process runs nightly and unattended. An offer there would never be seen by anyone, and
a scheduled run must not stop to ask a question.

**Never at pull.** Pull answers a question. An offer there interrupts the answer.

The third way in, and the main path: **`/brain-skill` with no argument sweeps on demand**, when you ask for
it.

### The signal is a judgment, and the bar is high on purpose

Two things must both be true. A method that clears only the first one is not a candidate.

> **1. It is a method you will run again.**
> **2. It is worth a maintained artifact.**

A skill is a real cost. It is a file you keep current, install on each surface, and stop from going
stale. Most captured steps are not worth that. **Do not offer for minor process detail.**

Gate 2 is met when the method is one of three kinds. **Name the kind in the offer.** If you cannot name one,
do not offer.

- **A business process you run** — how you quote, onboard, review, invoice, or ship.
- **A personalization** — how you want work done: your standards, your format, your voice.
- **A way of working with AI you repeat** and that saves you time.

**When in doubt, stay silent.** The two costs are not equal. A missed candidate is recoverable, because
`/brain-skill` sweeps for it later. A wrong offer is an interruption that cannot be taken back.

Do not offer when the content is a fact, a finding, a reference, a decision, or a corrected claim. Those are
knowledge, a decision included, which can feel active but records what was chosen rather than how to do
something. Do not offer for one-off troubleshooting, for a setup done once for one machine or one artifact,
or for a short sequence with no judgment in it that any assistant would get right without a skill. Stay
silent when `registry.md` shows you already declined it.

Three examples that fix the line:

- A note on **how you set up every project spreadsheet, in your standard layout** is a personalization
  you repeat. **Offer.**
- A note on **the steps that fixed one broken build last week** is written as steps, but it is a one-off.
  **Say nothing.**
- A note on **what an article about giraffes said** is knowledge, not a method. **Say nothing.**

### The volume rules, and they are strict

- **One offer per candidate per session.**
- **The offer is one line, after the work finishes.** It never blocks or delays the capture.
- **Never build without a yes.**
- **A declined candidate is recorded in `registry.md` with its reason, and is not raised again.**

## 5. What a yes does — build now, on this surface

**No inbox note. No queue. No second command.** You are present and you said yes.

Two things happen, in this order:

1. **The master is written** to `<library>/skills/<name>/SKILL.md`, with `<name>.BUILD.md` beside the folder,
   and a row is added to `<library>/registry.md`. **The master is written in every case, on every surface.**
   It is the durable copy, and it is what lets the method reach other surfaces later.
2. **It is installed in whatever form this surface supports.** Then the AI says plainly what was installed
   and what you still have to do by hand.

| Surface | The installed form |
|---|---|
| Claude Code, Cowork | A skill, installed into `~/.claude/skills/` per `<library>/INSTALL.md` |
| claude.ai chat | No install from chat. A bundle is built for the account store for you to upload, or the method is added to a Project's instructions. |
| ChatGPT | A custom GPT built from a generated builder prompt, or the method added to an existing GPT's or Project's instructions |

The rule, rather than a taxonomy: **install it the way this surface installs a method.** If the surface
has no mechanism for that, say so and produce the artifact you can install by hand.

A build also appends an entry to `<vault>/wiki/_log.md`, recording what was built. That is the "what changed"
record. Nothing else writes into `wiki/` outside of process.

### The memory trap

Some surfaces offer only a **memory** feature. A memory entry is an acceptable *installed form*. It is
**never** the artifact.

**Per-surface memory does not travel between surfaces and is not durable**, which is the exact problem this
whole system exists to fix. The master goes in the library. The memory entry is a local copy. **Never store a
method only in a surface's memory and call it saved.**

## 6. `/brain-skill` and its three modes

Five verbs move knowledge: capture, process, pull, maintain, digest. **`/brain-skill` turns a repeated
method into a skill.** It is backed by a vault skill named `skill-library`.

The command is named `brain-skill` and not `skill` so it does not collide with other skill-building commands
you may already have installed.

1. **`/brain-skill` with no argument — sweep on demand.** It scans recent wiki pages and recent `_log.md`
   entries for methods you follow by hand, skips anything `registry.md` already records as built or declined,
   and proposes what is left. **It builds each accepted candidate immediately.** It writes nothing without a
   yes.
2. **`/brain-skill build <name>` — build one named method now.** It writes the master, writes
   `<name>.BUILD.md` beside the folder, adds the registry row, appends to `_log.md`, and installs the skill
   in the form this surface supports. For a pure-instruction skill it also emits the ChatGPT artifact into
   `<name>.BUILD.md`: a builder prompt for a new custom GPT, or an instruction block for an existing GPT or
   Project. It says which it chose and why, in one sentence. Because the artifact is regenerated on every
   build, refreshing a ChatGPT copy is a paste, not a rewrite.
3. **`/brain-skill install` — install the library on this machine** per `<library>/INSTALL.md`. It then
   reports which skill reaches which surface, and names any master with no install.

## 7. The rules that keep the library honest

**The one-store rule.** A skill lives in exactly one store. Four stores in the system is fine. **Two copies
of one skill is the bug.** When the same name exists in two stores, both load, and which one wins is
ambiguous. There is no error, no warning, and no log line. `registry.md` is what makes it visible: one row
per skill, one store per row.

**Junction over copy.** Use a junction where the operating system allows it. A junction makes drift
structurally impossible, because the installed path and the master are the same bytes. A copy is a snapshot
that drifts the moment you edit the master, and you must redo it after every edit. **Junctions are
directory-only.** A lone command file is not a directory, so it must be copied and re-copied. On Windows a
junction needs no administrator rights, and a symbolic link does. On macOS and Linux `ln -s` needs no
elevated rights. The exact commands are in `seed-library/INSTALL.md`.

**Provenance — compute it, do not remember it.** The upload to the account store is the step with no safety
net. A rebuilt master that was never uploaded leaves every chat surface serving an old version, and nothing
anywhere reports the gap. The kit ships `seed-library/tools/package-skill.py`, and its build is
**deterministic**: two runs on an unchanged master produce byte-identical output with the same SHA-256. That
determinism is what makes the check real. Record the SHA-256 of the uploaded bundle in that skill's
`BUILD.md`, with the date. Before you assume the live copy matches, rebuild and compare the hash. **Verify
the published payload, not just that the upload reported success.**

### Packaging traps

These apply to the account store and to nothing else. Each one is real.

**WARNING:** never build a bundle with PowerShell `Compress-Archive`. It writes backslash path separators
inside the zip. The skills UI rejects the archive with an error about characters in the path. That error
points at the file's location rather than at the bytes inside, so the wrong thing gets debugged. A Python
`zipfile` packager is immune, because `ZipInfo` rewrites the separator on write.

**WARNING:** the reading tools hide the defect. Python's `zipfile.namelist()` normalizes a backslash to a
forward slash on read, and the Windows extractor accepts a backslash archive and installs it. The packager
was checked against a hand-built backslash archive. Its raw-header check returned true, while
`zipfile.namelist()` read that same archive back as `demo/SKILL.md`. **The only reliable check is the raw
local-file-header bytes, which the packager performs before it finishes.**

**WARNING:** only the frontmatter keys `name` and `description` round-trip. An extra key can make an upload
land the `SKILL.md` alone and silently drop every other file in the bundle. The packager refuses the build
when it finds any other key.

**WARNING:** watch for functional duplicates that no name collision catches. Two differently named skills
covering the same ground both load, and the model picks one. The one-line summaries in `registry.md` are how
you spot it.

The packager also refuses a `name:` value that does not match the folder name, a `BUILD.md` inside the skill
folder, a missing `SKILL.md`, and an empty folder. It skips `.DS_Store`, `Thumbs.db`, and `.keep`.

## 8. What is not a skill

Declining is a real outcome. The reason goes on a `declined` row in `registry.md`, so the next sweep does not
propose the same thing again. Four common reasons:

- **Three rules, not a method.** Put it in a `CLAUDE.md`, or in project instructions.
- **Already covered by an existing skill.** Absorb it there, where it will actually be read.
- **A conclusion, not a method.** That is knowledge. It belongs on a wiki page.
- **Done once, with no sign it repeats.** Wait for the second time.

An empty library is the correct state until you have a method worth building.

## 9. What this does not promise

Six honest limits. Read them before you rely on any of this.

- **The offer is a judgment, not a guarantee.** It will miss methods. It will sometimes propose one you do
  not want. Declining is cheap, and the reason gets recorded.
- **Reach is bounded, and ChatGPT has no skill store.** A method reaches ChatGPT as a custom GPT, or as
  instruction text inside an existing GPT or Project, and nothing else.
- **The owner picks the GPT. The model does not select it.** A Claude skill is chosen by the model from its
  description, on demand. ChatGPT has no equivalent to that, so a method in a custom GPT is reached by naming
  it. ChatGPT's features change, so check current behavior before you design around it.
- **A GPT's or a Project's instructions are a copy that a human refreshes.** They do not stay in sync with
  the master. Nothing on the ChatGPT side reports the gap, and the text cannot be hashed from outside, so
  `registry.md` and a hand refresh are the only control.
- **A skill does not sync when it needs a per-machine install.** The account store is the only Claude store
  that syncs by itself. The vault store and the library are both per machine, so a skill in either one is not
  on your other machine until you install it there.
- **The uploaded bundle is not checked for you.** Nothing reports a master that was rebuilt and never
  uploaded. The hash in `BUILD.md` is the only record, and you write it.

---

## Where to look next

| File | What it is |
|---|---|
| `seed-library/CONVENTIONS.md` | The contract. Binding. |
| `seed-library/INSTALL.md` | The per-machine runbook, the account store, and ChatGPT. |
| `seed-library/registry.md` | The catalog. Built and declined, and the one-store rule made visible. |
| `docs/surfaces.md` | Per-surface wiring for the brain itself. |
