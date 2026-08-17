# TSCG Smart Prompt v17.0.0 — Deterministic Session Loader

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-11
**Supersedes**: v16.3.0 (a 499-line content snapshot — retired as structurally dirty)

> **What changed and why.** v16.x carried framework *content* — versions, corpus
> counts, HEAD sha, primitive tables, formulas. All of that goes **dirty** the
> moment the repo moves, and it drifted (e.g. v16.3.0 held both
> `_^ | _$ = StereopsisEmptySet` and `_0 = _^ | _$` — a contradiction, and a
> stale primitive count). A prompt must never be a second copy of HEAD.
>
> This version carries **no verifiable facts**. It is a *loader*: it names the
> authorities to load, states the one governing rule, and gives you a slot to
> inject fresh session state. Paste it as the **first message** of a new
> TSCG conversation.

---

## 1. Load first — by name (this is the deterministic part)

Before doing anything else, load these skills:

- **`head-over-memory`** — the authority discipline (verify at source; never
  recite a verifiable fact from memory or corpus).
- **`tscg-ontology-diagnosis-pipeline`** — the 6-phase validation pipeline for
  any ontology change.
- *(add the task-specific skill: `tscg-instance-pipeline`,
  `tscg-create-instance-simulation`, `tscg-rust-vm`, `tscg-article-pipeline`, …)*

Naming a skill **is a direct instruction, not a heuristic match** — it is the
reliable way to force it into context. Do not rely on auto-triggering.

---

## 2. The one rule that governs everything

**HEAD is the only authority.** HEAD = the latest commit on `main` of the public
repo (`github.com/Echopraxium/tscg`).

Do **not** recite framework facts — versions, corpus counts, file structure,
primitive alphabets, golden values — from memory or from the project corpus.
**Read them from HEAD**: raw CDN (`https://raw.githubusercontent.com/Echopraxium/tscg/main/…`,
unrestricted) or `git show HEAD:<file>` in a freshly-fetched clone.

Durable invariants (notation, REVOI, namespaces, conventions) live in
**`TSCG_ReferenceCorpus_Bootstrap.md`** — read it, don't re-list it here.
The full routing table (which file owns which authority) lives in
**`TSCG_ReferenceCorpus.md`**.

Full discipline, including the verify-before-assert reflex and the executable
checks: the **`head-over-memory`** skill.

---

## 3. Fresh session state — injected below, never from memory

*(This is the perishable half. It must be supplied fresh each session, because
it has no source of truth and would be dirty in memory. Fill it in, or delete
the lines that don't apply.)*

- **Current HEAD**: `<sha>` — *treat as unverified; confirm with `git show HEAD` before trusting.*
- **Active worksite**: `WS-n` — `<one-line state>`
- **Today's goal**: `<…>`
- **Working copy in flight** (conversation edits, NOT yet committed): `<…>`
- **Gates pending my decision**: `<…>`

---

## 4. HandOver — the same instrument, mid-worksite

A **HandOver** is what you paste to *continue an in-progress worksite* in a new
conversation (whereas this Smart Prompt *opens* a session). It obeys the **same
two rules**:

1. It **MUST begin by loading `head-over-memory`** (and the relevant pipeline
   skill) — by name, exactly as §1.
2. It carries **no authoritative framework content** — only pointers to HEAD and
   the **fresh session state** of §3 (where the worksite stands, what's in the
   working copy, what gate is open).

So both instruments are thin loaders. The Smart Prompt boots a clean session;
the HandOver resumes a worksite. Neither is ever allowed to become a content
snapshot again — that is what made v16.x rot.

---

**Version**: 17.0.0 · **Author**: Echopraxium with the collaboration of Claude AI

*This file should itself live in the repo (so it has a HEAD) — suggested:
`ontology/docs/_01_Worksite/` alongside the worksite map.*
