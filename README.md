# ai-brain-seed

A starter kit for a **personal, LLM-maintained knowledge brain**: plain markdown files in a Dropbox folder
that every AI surface you use — Claude Code, Claude Desktop/Cowork, claude.ai chat on web and phone, even
ChatGPT — can read from and write to. The wiki it grows is the durable source of truth; every tool is just a
client.

```
inbox/  →  raw/     →  wiki/      →  outputs/
capture    immutable   knowledge     deliverables
(fast,     sources     the LLM
no filing)             curates
```

Three verbs run the whole system:

- **capture** — drop anything worth keeping into `inbox/`, zero filing decisions, from any surface
- **process** — an LLM compiles the inbox into a concept-per-page, interlinked, cited wiki (nightly, or on
  demand)
- **pull** — ask the brain anything; it answers from the wiki and cites its pages

## Why

Working with AI across surfaces loses knowledge constantly: decisions, methods, specs, and findings get
produced in one session and evaporate when it ends. Per-tool memory features don't travel. This system makes
the knowledge an **artifact you own** — markdown in your own storage — with a disciplined protocol for how
the AI writes into it and reads out of it, so it **compounds instead of resetting**.

The design follows Andrej Karpathy's framing of AI-agent work (spec / verifier / **environment** — the brain
is the environment's knowledge-base layer, his "LLM wiki" idea made real) with several adaptations: a
frictionless inbox that separates capture from filing, identity-as-metadata so cross-cutting knowledge lives
exactly once, immutable sources so every wiki claim is traceable, and no git — cloud sync is the versioning
layer. The full reasoning is in [docs/background.md](docs/background.md).

## Quick start

**Prerequisites (you, the human):** a Dropbox account (a dedicated one is cleanest), Dropbox for desktop
installed, and the vault folder set to Local / "Make available offline" — details in
[SETUP.md](SETUP.md).

Then pick a path:

1. **Best: clone this repo and let Claude do the rest.** Open Claude Code in the cloned folder and say:
   > Read SETUP.md and set up the brain.
   Or, to learn first:
   > Read SETUP.md and teach me how the brain works before setup.
2. **No download:** paste the contents of [STANDALONE.md](STANDALONE.md) into a Claude conversation with
   the same prompts — it embeds every template.
3. **Manual:** copy `seed-vault/` into your Dropbox, fill the `{{PLACEHOLDERS}}` by hand, and read the
   docs. Works; slower.

## What's in the box

| Path | Contents |
|------|----------|
| [SETUP.md](SETUP.md) | The prompt document: guided interview + build steps an AI follows |
| [STANDALONE.md](STANDALONE.md) | Everything in one paste-able file for setup without the repo |
| [seed-vault/](seed-vault/) | Complete vault skeleton: protocol docs, wiki scaffolding, Claude Code skills & slash commands |
| [docs/background.md](docs/background.md) | The why — Karpathy method, design decisions, guardrails |
| [docs/surfaces.md](docs/surfaces.md) | Wiring up Claude Code, Cowork/Desktop, claude.ai chat, phone |
| [docs/scheduling.md](docs/scheduling.md) | The nightly compile — scheduled task (recommended) and manual alternatives |
| [docs/chatgpt.md](docs/chatgpt.md) | Optional: a private custom GPT as a ChatGPT-side client |
| [docs/backfilling.md](docs/backfilling.md) | Seeding the initial wiki from existing conversations, exports, and memory |

## Two rules people miss

- **The vault is git-free, forever.** This repo is a *distribution mechanism*; the vault it seeds is synced
  and versioned by Dropbox. Don't clone into your Dropbox and leave `.git` behind.
- **Run the process step where the files are local.** It moves files out of `inbox/`, so it needs real disk
  access — a local Claude Code/Cowork session, not a cloud runner or a connector.

## Lineage

Karpathy's LLM-wiki concept and agent-environment framing → the Data Garden / PlantWave implementation
(concept-per-page, index-vs-log, conventions-first, immutable sources) → this design (git-free,
multi-surface, inbox-centric). Spiritual ancestor: Vannevar Bush's Memex (1945).

## License

Public domain ([The Unlicense](LICENSE)). Use it, remix it, republish it — no attribution needed.
