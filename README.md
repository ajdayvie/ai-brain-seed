# ai-brain-seed

A starter kit for a **personal, LLM-maintained knowledge brain**. The brain is a folder of plain markdown
files in your own cloud storage. Every AI surface you use can read it and write to it: Claude Code, Claude
desktop and Cowork, claude.ai chat on web and phone, and ChatGPT.

The wiki it grows is the durable source of truth. Every tool is a client. The brain holds knowledge, and a
**skill library** beside it holds the methods that repeat.

```
inbox/  ->  raw/     ->  wiki/      ->  outputs/
capture     immutable    knowledge     deliverables
(fast,      sources      the LLM
no filing)               curates
```

Four verbs run the whole system.

- **capture** — write anything worth keeping to `inbox/`, from any surface, with no filing decision
- **process** — an LLM compiles the inbox into a concept-per-page wiki, linked and cited. It runs nightly,
  or on demand.
- **pull** — ask the brain a question. It answers from the wiki and cites the pages.
- **maintain** — a lint pass over the wiki: broken links, orphan pages, contradictions, stale pages

A fifth verb works on methods rather than knowledge.

- **`/brain-skill`** — turn a repeated method into a skill. The AI offers rarely, and only for a business
  process, a personalization, or a way of working with AI that you repeat. On your yes it builds the skill
  and writes the master into the library.

## Install

Download or clone this repository. Open an AI assistant in that folder. Say exactly this:

```
help me install an AI brain
```

The assistant reads [INSTALL.md](INSTALL.md) and runs the guided intake. It teaches you the system first,
asks you a short set of questions, then builds your vault, installs the Claude Code skills, and verifies the
loop end to end. The core install takes about 30 minutes. Connecting extra surfaces and the first
backfill pass add more.

**Prerequisites (you, the human):** a Dropbox account, Dropbox for desktop installed on this machine, and the
vault folder set to Local / "Make available offline". The assistant states the full list and waits for you.
It never signs up for an account, grants a permission, or generates a token on your behalf.

### Other paths

**Teach me first.** To understand the system with nothing written to disk, say:

```
teach me how the brain works
```

**No download.** Paste the whole of [STANDALONE.md](STANDALONE.md) into an AI chat, then use either prompt
above. That one file embeds every template in this repository.

**Manual.** Copy `seed-vault/` into your synced folder, replace the `{{PLACEHOLDER}}` values by hand, and
read the docs. This works. It is slower and easier to get wrong.

## What's in the box

| Path | Contents |
|------|----------|
| [INSTALL.md](INSTALL.md) | The guided intake. The AI reads this file and follows it. |
| [CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md) | Thin routers. They point an assistant at `INSTALL.md`. |
| [STANDALONE.md](STANDALONE.md) | The whole kit in one paste-able file. Generated, so do not hand-edit it. |
| [seed-vault/](seed-vault/) | The vault skeleton: protocol docs, wiki scaffolding, Claude Code skills and slash commands |
| [seed-library/](seed-library/) | The skill library skeleton: the skill contract, the registry, and the per-machine install |
| [docs/background.md](docs/background.md) | The why: the knowledge-loss problem, the method, the design decisions |
| [docs/surfaces.md](docs/surfaces.md) | Per-surface wiring for Claude Code, Cowork and desktop, claude.ai chat, and ChatGPT |
| [docs/skills.md](docs/skills.md) | The skill library: the stores, what each one reaches, and the offer behavior |
| [docs/scheduling.md](docs/scheduling.md) | The nightly compile: options A, B, and C, and the fallback policy |
| [docs/chatgpt.md](docs/chatgpt.md) | The private custom GPT: builder prompt and preview tests |
| [docs/backfilling.md](docs/backfilling.md) | Seeding the wiki from existing conversations, exports, and memory |
| [tools/build-standalone.py](tools/build-standalone.py) | Regenerates `STANDALONE.md` |

## Two rules people miss

- **The vault is git-free, forever.** This repository is only a distribution mechanism. Dropbox syncs and
  versions the vault it seeds. If you clone, do not leave a `.git` folder in the vault.
- **Process runs where the files are local.** It moves notes out of `inbox/`, so it needs real disk access.
  Use a local Claude Code or Cowork session, not a cloud runner and not a connector.

## Where this came from

This kit was not designed in the abstract. It is extracted from a **working brain that has been in daily use
since June 2026** — captured from across several AI surfaces, compiled nightly, and pulled from during real
work. Every rule here earned its place by breaking first. The nightly compile is ranked the way it is because
the other route failed twice. Notes are filed from their own content because a queue of unfileable notes once
sat in the inbox for fourteen days. The skill offer asks rarely because an earlier version would have asked
constantly.

So the seed is a **snapshot of something running**, not a proposal. It will keep changing as the original
does.

### Lineage, with credit

- **Andrej Karpathy** — the agent-environment framing (spec, verifier, environment), and the sketch of an
  LLM-maintained markdown wiki that replaces RAG at personal scale. The brain is the knowledge-base layer of
  that environment. That idea is the seed of this whole design.
- **The Data Garden / PlantWave implementation** — a production build of that wiki idea, and the source of
  the working parts adopted here: concept-per-page, index versus log, conventions first, immutable sources,
  the `outputs/` stage, frontmatter for querying, and periodic maintenance passes. This design is an
  evolution of it, and the credit stands.
- **Vannevar Bush's Memex** (1945) — the spiritual ancestor, with the LLM finally doing the curation Bush
  could not automate.

**What this design adds** to what it inherited: no git, so cloud sync is the versioning layer. Many surfaces
rather than one. An inbox that separates capture from filing. Identity as metadata rather than a folder. And
a skill library beside the wiki, so repeated methods compound the way knowledge does.

The full reasoning is in [docs/background.md](docs/background.md).

## License

Public domain, under [The Unlicense](LICENSE). Use it, remix it, republish it. No attribution needed.
