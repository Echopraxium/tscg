# _03_SerendipCrates

**Author**: Echopraxium with the collaboration of Claude AI
**Created**: 2026-10-22

> **Project-idea crates — not Rust crates.** Nothing here is code to build. (In this
> repository, `crates/` folders elsewhere — e.g. in `TriskeleToolchain` — are Rust packages.)

## What this folder is

A place to set aside **project ideas** for TSCG that are not yet formalised: an idea is
packed in a crate, stored, and opened later — in the spirit of the three princes of
Serendip, who found what they were not looking for.

It exists so that unformalised ideas have their own clearly marked place, instead of
accumulating in the Core Hypotheses (`docs/CoreHypotheses/`), which are guidelines and
must not become a repository of unformalised ideas. TSCG's value is to **name and
model**: a crate is a waiting room, not a destination.

## Layout

One sub-folder per crate:

```
_03_SerendipCrates/
  README.md            ← this file
  <CrateName>/
    CRATE.md           ← the crate's label: date, status, possible destination
    ...                ← HandOvers, notes, sources, drafts
```

`<CrateName>` is CamelCase and names the idea, not a date.

## Life cycle of a crate

| Status | Meaning |
|---|---|
| `sealed` | Packed and stored; nobody is working on it |
| `open` | Under analysis in a session |
| `graduated` | Became something formal — a Core Hypothesis, a worksite, an M0 instance… The crate records where it went, then leaves this folder |
| `abandoned` | Dropped. The crate **stays here**, with the reason, so the dead end is not walked again (the "open drawer") |

A crate graduates only by becoming something **formal**. Analysis alone does not
graduate it.

## Rules

- Each crate has a `CRATE.md` — no crate without a label.
- Nothing in a crate is authoritative: framework facts are read on HEAD
  (`head-over-memory`).
- A crate adds nothing to the ontologies. Anything it proposes to grave goes through the
  usual pipelines.
