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

- Lowercase kebab-case filenames, like `my-first-concept.md`. One **concept per page**, not one page per
  source.
- Inbox notes: `YYYY-MM-DD-HHMM-<slug>.md`.

## Folders

- `wiki/topics/` — evergreen knowledge by subject. Keep it flat. Nest only when a cluster grows.
- `wiki/projects/<slug>/` — active work. `wiki/archive/` — finished or dormant work.
- A cross-cutting fact lives once, usually in `topics/`. Filter it by tags and identity. Never duplicate it.

## The three axes

Every page is classified on three independent axes, and each axis has its own mechanism. Keep them separate
and filing is mechanical. Collapse two onto one mechanism and filing becomes a judgment call.

- **Lifecycle** (evergreen / active / done) -> **folders**: `topics/`, `projects/<slug>/`, `archive/`.
  Folders encode *only* lifecycle, never subject.
- **Identity** ({{IDENTITY_VALUES_SLASH}}) -> **frontmatter** `identity:`. A filter, never a folder.
- **Subject** (whatever the brain grows to cover) -> **tags and wikilinks**, drawn from the controlled list
  in [[_tags]]. Subject never rides on folders. That is what lets a cross-cutting fact live once and still be
  findable.

So at process time: pick the folder by lifecycle, set `identity`, then tag the subject from [[_tags]] and
link the canonical page. No single decision carries more than one axis.

## Identity is metadata, not a folder

`identity: {{IDENTITY_VALUES}}` in frontmatter. Knowledge is filed by subject. Identity is a filter.

## Linking

- Obsidian wikilinks: `[[slug]]` and `[[slug|text]]`. Inside a markdown table, escape the pipe:
  `[[slug\|text]]`.
- Every page links to at least one other page and is linked from at least one. No orphans.
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

`tags:` is the subject axis, drawn from the controlled vocabulary in [[_tags]]. It is not free-form. Status,
type, and identity have their own fields, and must never be expressed as tags.

## Outputs

Drafts go to `outputs/<project>/drafts/`. Finals go to `outputs/<project>/`. Code outputs go in their own
repo.

## Log entry types

`capture | process | wiki | draft | final | conventions | maintenance | flag`

## Hard rules

- `raw/` and processed source notes are immutable. No fabricated facts. Every claim traces to a source.
- No cross-domain duplication. No git in this vault.
