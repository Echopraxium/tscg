---
name: head-over-memory
description: >
  Authority discipline for all TSCG work. Governs where a stated fact is allowed
  to come from, so that stale "memory" vestiges (wrong versions, counts, SHAs,
  file structure) can never slip into a response unmarked and cause silent
  regressions. Enforces three rules — authority order (HEAD/source > durable
  corpus > memory as last resort), explicit marking of any memory-sourced claim
  ("The memory archive says: …"), and the hard asymmetry that a VERIFIABLE fact
  never comes from memory at all. Load this skill (by name) at the start of every
  TSCG conversation, via the Smart Prompt or a HandOver, and apply it before
  asserting any framework fact — a version number, a corpus count, a file's
  structure, a primitive alphabet, a golden value, or "we decided X".
---

# head-over-memory — the authority discipline

## Why this exists

A stale memory fact does not announce itself. It enters a response with the same
confident tone as a verified fact ("M2 has 80 patterns", "HEAD is d92ded2"), and
the reader can only catch it if they already know it is wrong — too late. Silent
*and* confident is the worst combination: it produces regressions the human must
police invisibly, which is demoralizing. This skill makes the vestige visible
**before** it does damage.

## The three rules

### R1 — Authority order
For any fact, source it in this order and stop at the first that applies:

1. **HEAD / live source** — the committed state of `main` on the public repo.
   Read via raw CDN (`https://raw.githubusercontent.com/Echopraxium/tscg/main/…`,
   unrestricted) or `git show HEAD:<file>` in a freshly-fetched clone.
2. **Durable corpus** — the conceptual `.md` essays (rationale, not live structure).
3. **Memory** — last resort only, and only for non-verifiable things (see R3).

### R2 — Marking
Nothing from memory is ever stated bare. If a claim leans on memory, prefix it
explicitly: **"The memory archive says: …"**. The absence of that mark is a claim
that the fact was verified at source. Marking is the reliability signal.

### R3 — Asymmetry (the hard rule)
A **verifiable** fact NEVER comes from memory — marked or not. Versions, corpus
counts, file structure, primitive alphabets, SHAs, golden values all exist at a
source, so they are **read** at the source or not stated. Memory's "last resort"
applies only to the **non-verifiable**: a work preference, a semantics the human
settled verbally, a "we had agreed that…". Citing memory does not launder a
verifiable fact.

## Triage heuristic (apply before every factual assertion)

> **"Does this fact have a HEAD where I could verify it?"**
> - **Yes** → go read it (curl / `git show HEAD`). Do not recite it.
> - **No**  → memory is admissible, but marked ("The memory archive says: …").

Calibration: this is not a ritual. Don't fetch for trivially stable things or
narrate "let me verify" on every line — that becomes its own friction. Fetch when
the fact is load-bearing (drives a change, a formula, a count, a commit) and
could plausibly have drifted.

## Executable checks are the real determinism

Loading a fact from the right place raises reliability; it is not a guarantee of
correct *behaviour* turn after turn. The only thing at probability 1 is a check
that can **fail**:

- `git show HEAD:<file>` — the committed truth of a single file.
- `git fetch --depth 1 origin main && git reset --hard origin/main` — refresh a
  stale VM clone to equal HEAD.
- `run_all_layers.py` — the acceptance gate (golden values, errors, SHACL
  violations). Nothing is committed until this passes.
- SHACL (`pyshacl`) / the reasoner — structural validation that returns failure.

When a verifiable fact matters, prefer producing the check over asserting the
fact. A check that can return FAIL is worth more than any confident sentence.

## Anti-pattern (what this skill exists to stop)

Stating a framework fact — a version, a count, a structure, a SHA — in a
confident, unmarked sentence, sourced from memory or from a project-corpus
snapshot, without having read HEAD. If you notice yourself about to do this:
stop, run the triage heuristic, and either read the source or mark the claim.
