---
name: audio-digest
description: >
  This skill should be used when the user wants the hard content of the current session turned into
  something they can LISTEN to later — a spoken-word script, plus a pre-rendered MP3, written to the
  brain's digests/ section. Triggers include "/digest", "make an audio digest", "digest that for the
  drive", "explain that to me for later", "record that for the car", or "I want to listen to this
  on the go". It writes the digest and replies with ONE line — it must not clutter the session it
  was called from. It is NOT a capture: durable knowledge still goes to inbox/ via capture-to-inbox.
---

# Audio digest -> `digests/`

**Vault root — resolve this before you touch any path.** `<brain>` is the value of the `BRAIN_DIR`
environment variable, set per machine in `~/.claude/settings.json` under `env`. Read it with
`echo "$BRAIN_DIR"`. If it is unset, use whichever directory available to this session holds both `SCHEMA.md`
and a `wiki/` folder. **Never write a bare relative path like `digests/`.** This skill runs from any project
directory, and a relative path resolves against that project instead of the brain.

## Step 0 — load the binding protocol

Read **`<brain>/SCHEMA.md` §6f** and follow it. It is authoritative, it may have changed, and this skill does
not copy its rules. **SCHEMA wins over this file** on any rule. This file carries the job shape and the
script spec, which are structure, not protocol.

A digest touches no wiki page, so `wiki/_conventions.md` and `wiki/_tags.md` are not needed here.

---

## What this is, in one line

**A digest is an interface, never a record.** The wiki holds what is true. A digest holds one explanation
of it, shaped for ears, that ages out.

Three consequences, all binding:

- A digest is **not** a capture. If the content is durable, offer `/capture` separately — after, and only
  if the owner is at a stopping point.
- **`/process` must never read `digests/`.** A spoken restatement compiled into the wiki would pollute
  the source of truth with lossy prose.
- Digests **age out of the root**, but they are not deleted. At 60 days they move to `heard/` and stay
  there. `/maintain` owns that move. See Retention.

---

## The job

### 1. Choose the material

Default scope is the substantive content of the current session — the reasoning, the trade-offs, the
numbers, the thing that was hard to hold in your head. An argument narrows it (`/digest the pricing math`).

**The anti-goal: this is not a session summary.** A summary says *"we decided X."* A digest explains
*what X is and why it beat Y*, slowly enough to follow with your eyes on the road. If you find yourself
listing what happened, you are writing the wrong artifact.

Pick 2–4 ideas and teach them properly. Do not survey everything that was said.

### 2. Write the script

Target **600–900 words**, which lands near four to six minutes. Follow the spec below — it is the whole
value of this skill.

### 3. Write the file

`<brain>/digests/YYYY-MM-DD-HHMM-<short-slug>.md`, in the shape given below.

### 4. Render the audio

```bash
python "<brain>/.claude/scripts/render-digest.py" "<path-to-the-digest.md>"
```

It prints one line of JSON with the real duration. **Put that measured runtime in the frontmatter** —
do not estimate it.

The renderer needs `edge-tts` installed (`pip install edge-tts`) and a network connection. `ffprobe`, from
FFmpeg, is optional: without it the JSON reports `"seconds": null`, and you then say the runtime is unknown
rather than guessing one.

If the render fails, leave `audio: none`, say so in your one line, and carry on. **The markdown is the
artifact. The MP3 is a convenience.** A failed render never stops the digest from being written.

### 5. Catalog it

Append one line to `<brain>/digests/_catalog.md`, newest at the top, in the format given below.

### 6. Report — one line, then stop

> Digest recorded: **&lt;title&gt;** — 4 min — `digests/2026-09-13-1420-<slug>.md` + MP3

**No preview of the script. No summary of the summary. No offer to continue. No follow-up question.**
The owner called this so the session would *not* be interrupted. Honor that.

---

## The script spec

### Shape

1. **Cold open, two sentences.** The listener has no context, is hours away, and may be driving. Say
   what this is about and why they would care.
2. **The answer, then the reasoning.** Inverted from normal written order on purpose — a listener cannot
   skim back.
3. **One sentence of footing, early.** *"We measured the first part. The cost numbers are guesses."*
4. **The explanation.** The bulk, and the point.
5. **End on the open question, or the call the listener still owns.**

### Rules

- **No markdown that reads badly aloud.** No bullets, tables, headings, links, file paths, code
  identifiers, or citation markers anywhere in the body.
- **A table becomes a spoken comparison, with every number kept.** *"Three options were on the table.
  The cheapest ran about four dollars a month, but it couldn't hold a filesystem."* Never drop a figure
  to make a sentence speakable — say the figure in words.
- **Numbers as speech.** "About fifteen dollars a month." "Roughly three to five times faster." "One
  and a half megabytes." "Between thirty and forty percent."
- **Use the real term, define it in one clause, then keep using it.** The listener wants to *learn* the
  vocabulary, not have it removed. "An MCP server — that's just a small program that hands an AI a menu
  of things it's allowed to do — sits between…"
- **Signposts instead of headings.** *"First…"* · *"Here's where it got interesting."* · *"The part I'd
  push back on is…"*
- **Strip internal scaffolding.** No agent names, lane numbers, branch names, commit hashes, tool names,
  or file paths. If the listener would have to have been in the session to parse it, rewrite it.
- **Second person, contractions, conversational.** A colleague explaining on a walk — not a narrator.
- **Say the footing out loud.** "We measured this." / "That's an estimate." / "Nobody's checked that."
  Never launder a guess into a fact to make the sentence flow.

---

## File shape

```markdown
---
title: Why we're putting a server between the agent and the files
recorded: 2026-09-13 14:20
runtime: 4 min 31 s
source: <the project or session this came from>
about: MCP servers, why the brain needs one, what it costs
audio: 2026-09-13-1420-mcp-gateway.mp3
state: new
captured: no
---

# Why we're putting a server between the agent and the files

<!-- Read aloud from the next line, verbatim. Do not summarize.
     Everything above this line is filing metadata. -->

So — the thing we worked out today was...
```

**That HTML comment is load-bearing, not decoration.** Connector review forbids putting "read this
verbatim" in an MCP tool description, and claude.ai and Claude desktop silently discard the MCP
`instructions` field. The inside of the file is the only channel that reaches the phone. Always include it.

`about:` is written for how the owner will ask for it out loud — *"the one about the server thing"* — never
for how a filename reads.

---

## Catalog line

Newest at the top of `<brain>/digests/_catalog.md`:

```
- **Why we're putting a server between the agent and the files** — 4 min — 2026-09-13 — new —
  MCP servers, why the brain needs one, what it costs. `2026-09-13-1420-mcp-gateway.md`
```

---

## Retention

**Nothing is deleted. `heard/` is an archive.**

| Where | Rule |
|---|---|
| `digests/` root | Older than 60 days -> move to `heard/`, markdown and MP3 together |
| `digests/heard/` | Kept. Nothing is deleted. |

**`/maintain` does the move**, per `SCHEMA.md` §6d. This skill never moves and never deletes anything.
Neither verb deletes a digest or its MP3.

`heard/` grows without bound, and each MP3 runs about two megabytes, so a hundred digests is roughly two
hundred megabytes of synced storage. That is the known cost of the "nothing is deleted" rule. An owner who
wants a delete step adds it to `SCHEMA.md` §6f and to `/maintain` deliberately. It is not a default.

---

## Do not

- Do not offer a digest proactively. Wait to be asked. An offer that fires in normal operation is noise,
  and it trains the owner to ignore the channel.
- Do not write to `wiki/`, `inbox/`, `raw/`, or `outputs/`. This skill owns `digests/` and nothing else.
- Do not run git in the vault. Ever.
