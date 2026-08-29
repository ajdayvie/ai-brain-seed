#!/usr/bin/env python3
"""Regenerate STANDALONE.md from INSTALL.md, the seed-vault files, and docs/.

Run from the repo root:  python tools/build-standalone.py

STANDALONE.md is a generated file. Edit the sources, then rebuild.
Part II is read from INSTALL.md, so the two never drift apart.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The marker in INSTALL.md that separates the human preamble from the AI-facing body.
INSTALL_MARKER = "**Everything below this line is addressed to the AI.**"

VAULT_FILES = [
    "SCHEMA.md",
    "CLAUDE.md",
    "PROCESS.md",
    "README.md",
    "wiki/_conventions.md",
    "wiki/_tags.md",
    "wiki/_index.md",
    "wiki/_log.md",
    ".claude/INSTALL.md",
    ".claude/skills/capture-to-inbox/SKILL.md",
    ".claude/skills/process-inbox/SKILL.md",
    ".claude/skills/maintenance-pass/SKILL.md",
    ".claude/skills/skill-library/SKILL.md",
    ".claude/commands/capture.md",
    ".claude/commands/process.md",
    ".claude/commands/pull.md",
    ".claude/commands/maintain.md",
    ".claude/commands/brain-skill.md",
]

# The skill library, written beside the vault. `skills/` starts empty, so only the
# four documents and the packager are templates.
LIBRARY_FILES = [
    "README.md",
    "CONVENTIONS.md",
    "INSTALL.md",
    "registry.md",
]

LIBRARY_SCRIPTS = [
    ("tools/package-skill.py", "python"),
]

DOC_PARTS = [
    ("docs/surfaces.md", "Part V — Surfaces"),
    ("docs/skills.md", "Part VI — The skill library"),
    ("docs/scheduling.md", "Part VII — Scheduling the compile"),
    ("docs/chatgpt.md", "Part VIII — ChatGPT (optional)"),
    ("docs/backfilling.md", "Part IX — Backfilling"),
]

# Cross-reference rewrites: repo paths -> standalone part names.
# Longest / most specific patterns first.
XREFS = [
    # Statements that only make sense with the repo present. Rewrite or drop them
    # before the path rewrites below can touch them.
    (r"If you have this document but not the repository files, use `STANDALONE\.md`\."
     r" It embeds every template\.\n+", ""),
    (r"This repository holds everything you need\.", "This document holds everything you need."),
    (r"if this repository was cloned, make sure", "make sure"),
    (r"\*\*Do not write outside this repository\*\*", "**Do not write any file**"),

    (r"`?seed-vault/\.claude/INSTALL\.md`?", "the `.claude/INSTALL.md` template in Part III"),
    (r"`?seed-vault/SCHEMA\.md`?", "the `SCHEMA.md` template in Part III"),
    (r"`?seed-vault/`?(?=[\s,.])", "the vault templates in Part III"),
    (r"`?seed-library/CONVENTIONS\.md`?", "the `CONVENTIONS.md` template in Part IV"),
    (r"`?seed-library/INSTALL\.md`?", "the `INSTALL.md` template in Part IV"),
    (r"`?seed-library/registry\.md`?", "the `registry.md` template in Part IV"),
    (r"`?seed-library/README\.md`?", "the `README.md` template in Part IV"),
    (r"`?seed-library/tools/package-skill\.py`?", "the `tools/package-skill.py` template in Part IV"),
    (r"`?seed-library/`?(?=[\s,.])", "the library templates in Part IV"),
    (r"`?docs/background\.md`?", "Part I (Background)"),
    (r"`?docs/surfaces\.md`?", "Part V (Surfaces)"),
    (r"`?docs/skills\.md`?", "Part VI (The skill library)"),
    (r"`?docs/scheduling\.md`?", "Part VII (Scheduling)"),
    (r"`?docs/chatgpt\.md`?", "Part VIII (ChatGPT)"),
    (r"`?docs/backfilling\.md`?", "Part IX (Backfilling)"),
    (r"repo-root `INSTALL\.md`", "Part II"),
    (r"`STANDALONE\.md`", "this document"),
    # Collapse markdown links left pointing at a rewritten target.
    (r"\[([^\]]+)\]\(Part ([IVX]+) \(([^)]+)\)\)", r"Part \2 (\3)"),
]

PREAMBLE = """\
# STANDALONE.md — install an LLM-maintained knowledge brain (single-file edition)

> **Human:** paste this whole document into an AI assistant. A Claude Code session on the machine that
> holds your synced folder is the best place. Then say one of these:
>
> ```
> help me install an AI brain
> ```
>
> The assistant teaches you the system, asks a short set of questions, then builds your vault from the
> templates in Part III and verifies it.
>
> ```
> teach me how the brain works
> ```
>
> The assistant explains the system and writes nothing.
>
> This is the self-contained edition of the **ai-brain-seed** kit. Same content, no download needed.
>
> The kit is extracted from a working brain in daily use since June 2026, so it is a snapshot of something
> running rather than a proposal. It descends from Andrej Karpathy's LLM-wiki idea and agent-environment
> framing, and from the Data Garden / PlantWave implementation of that idea, which supplied
> concept-per-page, the index-versus-log split, conventions first, and immutable sources. Vannevar Bush's
> Memex (1945) is the spiritual ancestor. Part I carries the full reasoning.
>
> Everything below is addressed to the AI.

---

You are installing (or explaining) a **personal LLM-maintained knowledge brain**. The brain is a
plain-markdown knowledge base in a synced folder, reachable from every AI surface the owner uses. The wiki,
not chat history and not model memory, is the durable source of truth.

This document has nine parts.

- **Part I — Background.** The why. Read it first. You cannot install what you do not understand.
- **Part II — The guided intake.** The teach step, the interview, and the build steps. Follow it in order.
- **Part III — Vault file templates.** Every file the vault needs, verbatim, with `{{PLACEHOLDER}}` values.
- **Part IV — Library file templates.** Every file the skill library needs, beside the vault.
- **Part V — Surfaces.** Wiring for Claude Code, Cowork and desktop, claude.ai chat, and ChatGPT.
- **Part VI — The skill library.** How a repeated method becomes a skill, and how far each one reaches.
- **Part VII — Scheduling.** The compile: options A, B, and C, and the fallback policy.
- **Part VIII — ChatGPT** (optional). A private custom GPT as a ChatGPT-side client.
- **Part IX — Backfilling.** Seeding the wiki from existing context.

Read Part I now. Then follow Part II.
"""

PART_II_NOTE = """\
> **Standalone note.** This edition ships no folders to copy. Wherever Part II says to copy the seed vault,
> write each file from **Part III** at its stated path instead. Wherever it says to copy the seed library,
> write each file from **Part IV**. Then apply the placeholder replacements. The tree to create is:
>
> ```
> <vault>/
>   SCHEMA.md  CLAUDE.md  PROCESS.md  README.md
>   inbox/.keep   raw/.keep   outputs/.keep
>   wiki/_conventions.md  wiki/_tags.md  wiki/_index.md  wiki/_log.md
>   wiki/topics/.keep  wiki/projects/.keep  wiki/archive/.keep
>   .claude/INSTALL.md
>   .claude/skills/capture-to-inbox/SKILL.md
>   .claude/skills/process-inbox/SKILL.md
>   .claude/skills/maintenance-pass/SKILL.md
>   .claude/skills/skill-library/SKILL.md
>   .claude/commands/capture.md  process.md  pull.md  maintain.md  brain-skill.md
>
> <library>/
>   README.md  CONVENTIONS.md  INSTALL.md  registry.md
>   skills/.keep
>   tools/package-skill.py
> ```
>
> Empty folders get a `.keep` file. Never create a git repo in either folder.

"""


def apply_xrefs(text: str) -> str:
    for pattern, repl in XREFS:
        text = re.sub(pattern, repl, text)
    return text


def body_after_heading(text: str) -> str:
    """Drop a file's first line (its H1) and any blank lines after it."""
    return text.split("\n", 1)[1].lstrip("\n")


def install_body() -> str:
    """The AI-facing half of INSTALL.md, below the marker line."""
    text = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    if INSTALL_MARKER not in text:
        raise SystemExit(
            f"INSTALL.md no longer contains the marker line:\n  {INSTALL_MARKER}\n"
            "Restore it, or update INSTALL_MARKER in this script."
        )
    return text.split(INSTALL_MARKER, 1)[1].lstrip("\n")


def main() -> None:
    parts: list[str] = [PREAMBLE]

    background = (ROOT / "docs/background.md").read_text(encoding="utf-8")
    parts.append("\n---\n\n# Part I — Background\n\n"
                 + apply_xrefs(body_after_heading(background)))

    parts.append("\n---\n\n# Part II — The guided intake\n\n"
                 + PART_II_NOTE
                 + apply_xrefs(install_body()))

    parts.append("\n---\n\n# Part III — Vault file templates\n\n"
                 "Write each file at the stated path, relative to the vault root, verbatim. Then apply the\n"
                 "placeholder replacements from Part II, step 4.\n")
    for rel in VAULT_FILES:
        content = (ROOT / "seed-vault" / rel).read_text(encoding="utf-8")
        parts.append(f"\n## File: `{rel}`\n\n````markdown\n{content}````\n")

    parts.append("\n---\n\n# Part IV — Library file templates\n\n"
                 "Write each file at the stated path, relative to the **library** root, which sits beside\n"
                 "the vault. Then apply the placeholder replacements from Part II, step 4. The `skills/`\n"
                 "folder starts empty. It fills as candidates are built.\n")
    for rel in LIBRARY_FILES:
        content = (ROOT / "seed-library" / rel).read_text(encoding="utf-8")
        parts.append(f"\n## File: `{rel}`\n\n````markdown\n{content}````\n")
    for rel, lang in LIBRARY_SCRIPTS:
        content = (ROOT / "seed-library" / rel).read_text(encoding="utf-8")
        parts.append(f"\n## File: `{rel}`\n\n````{lang}\n{content}````\n")

    for rel, title in DOC_PARTS:
        content = (ROOT / rel).read_text(encoding="utf-8")
        parts.append(f"\n---\n\n# {title}\n\n" + apply_xrefs(body_after_heading(content)))

    out = ROOT / "STANDALONE.md"
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
