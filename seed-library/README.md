# Skill library

The companion to the brain. **The brain holds knowledge. The library holds methods.**

A skill is a verb. Knowledge is a noun. The wiki holds the nouns: facts, decisions, findings, corrected
claims. The library holds the verbs: the methods you would otherwise explain again in every new session.

The library is a **sibling of the vault**, in the same synced folder. It is not inside the vault, because a
tool is not knowledge. Putting methods inside a knowledge base blurs what the brain is.

## The one-store rule

**A skill lives in exactly one store.** There are four stores, and four is fine. **Two copies of one skill
is the bug.** When the same skill name exists in two stores, both load, and which one wins is ambiguous.
Nothing reports this. `registry.md` is what makes it visible.

## What is here

| File | What it is |
|---|---|
| `CONVENTIONS.md` | The contract. Where a master lives, how far it reaches, the four stores, naming, provenance, packaging traps, what is not a skill. |
| `INSTALL.md` | The per-machine install runbook, plus the account store and ChatGPT. |
| `registry.md` | The catalog. One row per skill, built and declined. |
| `tools/package-skill.py` | Builds a `.skill` bundle from a master, for upload to the account store. |
| `skills/` | The masters. One folder per skill. |

## The command is `/brain-skill`

Four verbs move knowledge: capture, process, pull, maintain. **`/brain-skill` turns a repeated method into a
skill.** It is backed by a vault skill named `skill-library`.

The command is named `brain-skill` and not `skill` so it does not collide with other skill-building commands
you may already have installed.

## It starts empty

`skills/` holds nothing on day one. It fills one skill at a time. An empty library is the correct state
until you have a method worth building.

The AI offers a candidate during **capture** and during **maintain**. It does not offer during pull or during
process. **The bar is high on purpose:** you will run the method again, **and** it is a business process, a
personalization, or a way of working with AI that you repeat. Minor process detail does not qualify, and
when it is a close call the AI stays silent. **`/brain-skill` with no argument sweeps on demand**, which is
the main way in.

**Building is always a deliberate act.** Nothing is written into this library without your yes. On a yes it
is built now, on the surface the session is running on.

## No git

The same rule as the vault. Dropbox syncs and versions this folder. Do not create a git repo here.
