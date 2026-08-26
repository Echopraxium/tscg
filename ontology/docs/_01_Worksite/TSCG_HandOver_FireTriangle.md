# TSCG — HandOver: FireTriangle Conformance Pass

> Paste this as the **first message** of a fresh conversation in the TSCG project to
> resume this worksite. Same two rules as any HandOver: load skills **by name**, and
> carry **no authoritative content** — read every fact (the current file, the schema, the
> validator, the M2 formulas) from HEAD, never from memory or from this HandOver.

---

## 1. Load first — by name
- **`head-over-memory`** — authority discipline.
- **`tscg-ontology-diagnosis-pipeline`** — the 6-phase validation pipeline.
- **`tscg-instance-pipeline`** — M0 instance mechanics.

Naming a skill is a direct instruction, not a heuristic match.

## 2. The one rule
**HEAD is the only authority** (`github.com/Echopraxium/tscg`). Read the current
FireTriangle, the SHACL schema, the validator, and the M2 formulas from HEAD (raw CDN or
`git show HEAD`). Do not recite any of them from memory or from this document.

## 3. The worksite — FireTriangle Conformance Pass

**Why it matters.** `M0_FireTriangle.jsonld` is the reference template the
`tscg-instance-pipeline` skill tells users to *"follow scrupulously"*. But on HEAD it is
stale and **non-conformant** — so it teaches retired notation and a forbidden pattern,
and a copied instance would fail the mandatory SHACL gate. Fixing it protects the whole
onboarding path.

**Confirmed defects on HEAD (re-verify at session start — do not trust this list):**
- `instances/poclets/FireTriangle/M0_FireTriangle.jsonld` is **v1.2.1** and contains
  **retired operators** — 6× `⊗` and 1× `⊕`. Must become `×` / `+` / `|` only.
- It uses the **nested score pattern** (`asfidScores` / `reviScores`) — **forbidden by the
  SHACL v1.6 schema**. Must become **flat** `scoreA … scoreIm`.
- It reportedly carries other SHACL violations (e.g. `m1core:simulationTitle`,
  `M0_Poclet#…`) — confirm the full list by running the validator.

**Goal.** Rewrite `M0_FireTriangle.jsonld` so it **passes the M0 SHACL gate**, with
correct notation and flat scores, and **bump its version** — making it a trustworthy
reference again.

**Authority files to read from HEAD:**
- instance: `instances/poclets/FireTriangle/M0_FireTriangle.jsonld`
- schema: `ontology/TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl`
- validator: `ontology/TSCG_InstanceGrammar/validate_m0_instance.py`
- M2 formulas (to re-verify FireTriangle's formulas): `ontology/M2_GenericConcepts.jsonld`

**Definition of done (the gate):**
- `pyshacl` reports **Conforms: True** on the rewritten instance.
- **Zero** `⊗` / `⊕` — only `×` / `+` / `|`. Flat scores. Version bumped.
- Decide (Michel) whether the skill's reference note needs updating too, or whether
  fixing FireTriangle is enough to restore it as the canonical example.

## 4. Discipline / traps
- **ORIVE write-path trap.** FireTriangle carries **REVOI** scores, and Claude's
  server-side write path can silently corrupt `REVOI → ORIVE` (hidden at readback).
  **Deliver the rewritten file as a local Python script for Michel to run — or have Michel
  edit manually — never through the write path.** Then grep the result for `ORIVE` /
  `orive` to confirm it's clean.
- **Notation ≠ blind sed.** Replacing `⊗` in a live `.jsonld` is a semantic edit: confirm
  each formula against the real M2 formula on HEAD before writing it.
- **Surgical commit.** One worksite, explicit `git add` by path. Never `git add -A` or
  `git add .` at the repo root.
- **Michel owns semantic decisions** — e.g. whether any formula or score value should
  change, versus only the notation/pattern. Claude proposes, validates, flags.

## 5. Fresh session state (perishable — confirm, never from memory)
- **Current HEAD:** `<confirm with git rev-parse HEAD>`
- **Active worksite:** FireTriangle Conformance Pass
- **Goal today:** migrate `M0_FireTriangle.jsonld` to pass SHACL v1.6 (operators → `×/+/|`,
  nested scores → flat, clear remaining violations), bump version, deliver via script.
- **Working copy in flight:** none.
- **Gates pending Michel's decision:** whether to also annotate/repoint the
  `tscg-instance-pipeline` reference to FireTriangle.

---

*Context (not authority): discovered 2026-08-19 during the Stroboscopic Yin-Yang run —
the run correctly refused to copy FireTriangle and built a clean instance instead, which
is what surfaced these defects.*
