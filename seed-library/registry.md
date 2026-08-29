# registry.md — the skill catalog

One row per skill. **This file is what makes the one-store rule visible.**

A skill lives in exactly one store. Nothing in the system reports a skill that exists in two stores. Both
copies load, and which one wins is ambiguous. There is no error and no warning. This table is the only place
the duplicate shows up, so **write the row when you build the master, not later**.

**This file also records what the owner declined, and why.** A declined row is what stops the next sweep
proposing the same thing again.

The one-line summaries do a second job. Two differently named skills covering the same ground both load, and
the model picks one. No name collision catches that. Reading the one-line column end to end does.

The contract is in `CONVENTIONS.md`. The install steps are in `INSTALL.md`.

---

## Skills

| Skill | Store | Reaches | Status | Master | One line |
|---|---|---|---|---|---|

<!-- Copy a row to add a skill. Delete nothing above it.
| example-skill-name | library | Claude Code, Cowork | installed | `skills/example-skill-name/` | What it does, in one clause. |
| example-declined-name | — | — | declined | — | Declined 2026-01-31: a conclusion, not a method. Filed as a wiki page. |
-->

### Store

| Value | Meaning |
|---|---|
| `vault` | The master is in `<vault>/.claude/skills/`. It requires the brain to exist. |
| `library` | The master is in `skills/` here. |
| `account` | The master is in `skills/` here, and a bundle is uploaded to the Claude account store. |
| `chatgpt` | No skill store exists. The method is a custom GPT, or instruction text in an existing GPT. See the table below. |

A skill in the account store still keeps its master here. `account` says where the built bundle went. It
does not mean a second master.

A `declined` row has no store. Write `—`.

### Reaches

Write the surfaces out, from the store's row in `CONVENTIONS.md` §2. For example `Claude Code` for a vault
skill, `Claude Code, Cowork` for a library skill, or `all Claude surfaces` for an account-store skill. A
`declined` row has no reach. Write `—`.

### Status

| Value | Meaning |
|---|---|
| `built` | The master exists. It is not installed on any machine. |
| `installed` | Installed on at least one machine, by junction or by copy. |
| `uploaded` | A bundle is in the account store, and its SHA-256 and date are in the skill's `BUILD.md`. |
| `declined` | The owner said no. **The one-line column carries the date and the reason.** |
| `retired` | No longer used. Kept in the table so the name is not reused by accident. |

**A declined row carries its reason, so the sweep does not propose it again.** The four common decline
reasons are in `CONVENTIONS.md` §8. Write the reason in the one-line column, with the date.

---

## ChatGPT carriers

**ChatGPT has no skill store.** A method reaches ChatGPT as its own custom GPT, or as instruction text
added to an existing GPT or Project.

Either one is a copy. **It goes stale the day the master changes, and nothing on the ChatGPT side reports
it.** **This table is the refresh list when a master changes.** Work down it by hand.

| Skill | Carrier | Kind | Last refreshed |
|---|---|---|---|

<!-- Copy this row to record a ChatGPT carrier. Delete nothing above it.
| example-skill-name | Example Research GPT | own GPT | 2026-01-31 |
-->

**Legend.** `Skill` is the master's name. `Carrier` is the custom GPT, GPT, or Project that holds the text.
`Kind` is `own GPT` when the method got its own custom GPT, or `added to` when it went into an existing
GPT or Project. `Last refreshed` is the date the text was last pasted from `skills/<name>.BUILD.md`, as
`YYYY-MM-DD`.
