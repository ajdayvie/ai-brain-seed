# Backfilling — seeding the wiki from existing context

A new brain starts empty, but you don't. Backfill is the controlled import of durable knowledge from what
already exists: old AI conversations, exported chat histories, per-tool memory features, project documents,
and your own head.

**Backfill does not introduce a new knowledge path.** It is a coordinated series of ordinary captures:

```
Past conversations / documents / memory
        ↓ review and triage
Approved capture manifest
        ↓ individual captures
      inbox/
        ↓ the normal process step (manual or nightly)
       raw/  →  wiki/
```

Never write historical material directly into `wiki/` or `raw/` — everything enters through the inbox so the
normal process step makes the filing decisions with full conventions in force.

## The golden rule: don't file everything at once

The tempting failure mode is a giant week-one import of everything you've ever discussed with an AI. Resist
it. The brain compounds by ingesting knowledge *as it becomes relevant*: when a topic comes up in real work,
capture what you know, and let processing build the pages. A modest seed plus steady capture beats a huge
stale import every time.

That said, three deliberate backfill passes are worth doing early:

## Pass 1 — the brain-dump interview (recommended first seed)

The fastest way to a useful initial wiki. In a Claude session attached to the vault:

> Interview me to seed my brain. Ask me one domain at a time: what I work on, the projects currently in
> flight, the key decisions already made and why, the methods and specs I reuse, and the facts I keep
> re-explaining to AIs. After each domain, capture what I told you as one or more inbox notes (normal
> capture rules — no filing). Stop when I say done.

Do 20–60 minutes, let the nightly (or a manual `/process`) compile it, then review `wiki/_index.md`. You'll
have a real, cited starter wiki within a day.

## Pass 2 — per-tool memory exports

Your AI tools have been quietly accumulating memory. Harvest it once:

- **Your assistant's saved memory:** ask the tool to display everything it remembers about you ("show me
  everything in your memory about me"), paste the output into a backfill conversation, and capture the
  durable parts as inbox notes (source: "saved assistant memory, exported YYYY-MM-DD").
- **Claude Code auto-memory / project memories:** review `~/.claude/projects/*/memory/` files and capture
  the durable, non-code facts.
- Treat these as *claims to verify*, not gospel — memory features accumulate errors. Mark anything doubtful
  as such in the capture note.

## Pass 3 — selected high-value conversations and documents

For the handful of conversations or documents that contain real decisions and specs:

### Mode A — selected-conversation backfill (highest quality)

Open the original conversation (in Claude or ChatGPT with its Brain GPT) and ask:

> Review this conversation for backfill. Identify durable decisions, methods, specifications, findings,
> corrected facts, important rationale, and unresolved questions. Compare against the existing brain, show
> me the proposed capture before writing anything, and capture only what is not already in the brain.

### Mode B — exported-history backfill (bulk review)

For large histories, export first (ChatGPT: Settings → Data Controls → Export Data →
`conversations.json`. Claude: Settings → Privacy → export). Then, in a dedicated backfill session, begin
with a **read-only inventory**:

> Review this exported conversation history for a brain backfill. First produce an inventory only: identify
> conversations likely to contain durable decisions, methods, specifications, findings, corrected facts, or
> consequential unresolved questions. Compare candidates with the current brain. Do not write any files yet.

Split oversized exports by project, date range, or subject before review.

### Mode C — documents and cross-platform material

The same workflow covers project context files, design records, master-context documents, notes from other
LLMs, and collections of markdown. Provide the files, request a read-only inventory, then approve captures.

## The capture manifest (for any sizeable pass)

Before writing anything, have the AI produce a manifest — temporary workflow state, not brain knowledge —
listing per candidate source: title, original date, platform, the durable content spotted, existing brain
coverage (none / partial / covered / conflicting), proposed disposition (capture / skip / merge / review),
proposed note slug, and confidence.

Favor **net-new knowledge**. Skip sources that contain only casual questions, temporary troubleshooting,
repeated explanations, superseded plans with no reusable rationale, material already in the brain, or
AI-generated claims that were never accepted or used. But don't skip a superseded decision whose reversal
contains a reusable lesson — capture it as a corrected/historical decision.

**From ChatGPT, the same manifest flow applies.** The `Brain` GPT presents a read-only inventory and a
capture manifest first. Once you approve that listed batch, it runs the batch as ordinary inbox captures,
with no redundant approval for each note. It never writes into `wiki/` or `raw/`. See `docs/chatgpt.md` for
the setup and the exact wording of the GPT rules.

Work in **reviewable batches** (roughly 5–20 related sources), approve each batch explicitly, and have the
AI report at the end of each: sources reviewed, skipped, notes created with exact paths, conflicts left for
you, and the next unreviewed range — so a backfill can pause and resume across sessions.

## Writing backfill notes

Backfill notes are ordinary inbox notes with one extra habit. Record the historical source *inside* the
note, and use the **current capture time** in the filename.

**The self-sufficient-note rule matters most here.** A backfill note is filed later, on a machine that
cannot open the conversation, the export, or the document it came from. **Synthesize the durable content
into the note itself.** Record the historical source as provenance **in addition to** that content, never
instead of it. A note whose body is a title and a date is unfileable, and it will sit in the inbox forever.

```markdown
context: Backfill from ChatGPT conversation "<title>", originally dated YYYY-MM-DD, reviewed and captured YYYY-MM-DD.

<clean durable knowledge — synthesis, not a transcript dump>

## Source reference
- Platform: ChatGPT
- Original title: <conversation title>
- Original date: YYYY-MM-DD
```

Preserve exact wording only when it matters (approved copy, contract language, prompts, naming decisions,
canonical definitions). Otherwise synthesize into concise factual markdown. One conversation usually yields
one note. Split only when a source contains clearly independent durable subjects. Backfill never makes final
wiki filing decisions — the normal process step decides whether one capture becomes one page, several, or
updates to existing pages.
