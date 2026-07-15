---
title: Conventions
type: reference
identity: na
status: stable
created: {{TODAY}}
updated: {{TODAY}}
sources: []
---

# Conventions — how this wiki thinks

> Approved by {{OWNER_NAME}} ({{TODAY}}). The contract for every page.

## Naming
- Lowercase kebab-case filenames (`my-first-concept.md`). One **concept per page**, not one page per source.
- Inbox notes: `YYYY-MM-DD-HHMM-<slug>.md`.

## Folders
- `wiki/topics/` evergreen knowledge by subject (flat; nest only when big).
- `wiki/projects/<slug>/` active efforts; `wiki/archive/` finished/dormant.
- A cross-cutting fact lives once (usually in `topics/`); filter by tags/identity, never duplicate.

## The three axes
Every page is classified on three independent axes, each with its own mechanism. Keep them separate and
filing is mechanical; collapse two onto one mechanism and filing becomes a judgment call.
- **Lifecycle** (evergreen / active / done) → **folders**: `topics/` · `projects/<slug>/` · `archive/`. Folders encode *only* lifecycle, never subject.
- **Identity** ({{IDENTITY_VALUES_SLASH}}) → **frontmatter** `identity:`. A filter, never a folder.
- **Subject** (whatever the brain grows to cover) → **tags + wikilinks**, drawn from the controlled list in [[_tags]]. Subject never rides on folders — that's what lets a cross-cutting fact live once and still be findable.

So at process time: pick the folder by lifecycle, set `identity`, then tag by subject from [[_tags]] and link the canonical page. No single decision carries more than one axis.

## Identity (metadata, not folders)
`identity: {{IDENTITY_VALUES}}` in frontmatter. Knowledge is filed by subject; identity is a filter.

## Linking
- Obsidian wikilinks `[[slug]]` / `[[slug|text]]`. Every page links to >=1 other and is linked from >=1 (no orphans).
- Prefer linking the canonical page over restating it.

## Frontmatter (every page)
```yaml
---
title:
type: concept | reference | source-summary | canonical | process | log
identity: {{IDENTITY_VALUES}}
tags: []
status: draft | stable | needs-review
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
---
```
`tags:` are the subject axis, drawn from the controlled vocabulary in [[_tags]] — not free-form. Status, type,
and identity have their own fields and must never be expressed as tags.

## Outputs
Drafts -> `outputs/<project>/drafts/`. Finals -> `outputs/<project>/`. Code outputs go in their own repo.

## Log entry types
`capture | process | wiki | draft | final | conventions | maintenance | flag`

## Hard rules
- `raw/` and processed source notes are immutable. No fabricated facts; every claim traces to a source.
- No cross-domain duplication. No git in this vault.
