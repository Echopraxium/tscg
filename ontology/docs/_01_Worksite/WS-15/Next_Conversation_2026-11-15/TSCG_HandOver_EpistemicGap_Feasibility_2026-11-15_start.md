# TSCG HandOver — Epistemic gap δ₁: can it be replaced, as a separate worksite, and with which prerequisites?

**Date**: 2026-11-15 · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt v17 §4) — a thin loader, no authoritative framework content.
**Session goal**: a **feasibility study**, not an execution. No ontology file is changed
in the next session.

---

## 1. Load first — by name

- **`head-over-memory`**: every verifiable fact below is a *pointer to check at HEAD*,
  never a fact to recite.
- **`tscg-ontology-diagnosis-pipeline`**: the next session covers **Phase 0
  (change request) and Phase 1 (pre-diagnosis)** only.
- *(If a replacement concept is proposed: `tscg-m2-candidate-filter`.)*

Then read at HEAD: `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` (hard
invariants, debt-honesty rule) and `ontology/docs/_01_Worksite/worksite.yaml`
(registered worksites).

---

## 2. Fresh session state (perishable — verify, do not trust)

- **HEAD when this was written**: `ee07f1a` (2026-11-09). *Unverified: run
  `git show HEAD` first.*
- **Working copy in flight, NOT pushed**: two patches from the 2026-11-15 conversation
  (attach them if you want them as reference):
  - `0001-Lot-A-deprecate-the-epistemic-gap…patch`: `owl:deprecated` on the M0 δ₁
    terms in `M0_Common`, plus a new check_m0 **C16** (deprecated `m0:` terms read from
    `M0_Common`), plus SHACL messages.
  - `0002-Gate-freeze-C16…patch`: freezes C16 in `golden_values.json`.
  - **Status: suspended. Do not apply them as they are.** They deprecate δ₁ in M0
    only, while M3/M2 still state it as doctrine. That would leave a cross-layer
    contradiction that no counter measures. The C16 design (deprecated set read from
    the owning file, never hardcoded) can be reused.
- **Paused instance**: `RequisiteVarietyDuo` (Ashby: human/AI duo), instance pipeline
  step 2 done (analysis file, not in the repo). It waits for this worksite: it must
  not use δ₁.
- **Worksite id**: not registered. Choosing the id and registering it in
  `worksite.yaml` is Michel's call.

---

## 3. What Michel stated (non-verifiable: decisions and positions)

- δ₁ is **arbitrary** and should go, as a worksite of its own.
- Arguments raised in the conversation (**Claude's analysis, to be validated by
  Michel, not decided**):
  1. In M0, δ₁ subtracts the means of two **non-commensurable** axes (ASFID describes
     the Territory, REVOI the quality of the Map).
  2. Both means come from the **same subjective rater**, so δ₁ measures no contact with
     reality.
  3. **Degenerate**: high/high and low/low both give δ₁ ≈ 0. It does not even measure
     the rater's coherence, so renaming it does not save it.
  4. The normalisation and the class thresholds are **posited, not derived**.
  5. **Several δ formulas coexist** (M2 root, M0/M3, preprint): a sign of an
     ungrounded improvisation.
- Direction floated: separate the **concept** (the Map is not the Territory; their
  disparity gives depth, like binocular disparity) from the **measure** (the δ₁
  formula, thresholds, spectral classes). Keep the first, deprecate the second, then
  ground any Map/Territory comparison in **external checks that can fail** (test,
  experiment, source, peer).

---

## 4. The questions the study must answer

**Q1 — Inventory at HEAD, by layer and by role.** Build it with a command, never from
memory. Starting point (extend the patterns if needed):
```bash
git grep -n -I -E "δ₁|δ\(M\)|epistemicGap|EpistemicGap|epistemic.gap|spectralClass|SpectralClass" \
  -- ontology instances docs src _00_UserGuide ':!*migration_backups*' ':!*_backups*'
```
Classify each hit:
- **definition** (declares a term or formula);
- **use** (a value in an instance, a property on a GenericConcept);
- **derived** (spectral classes, thresholds);
- **doctrine** (M3 prose: stereopsis depth, Korzybski, the "degree of proof" reading);
- **narrative** (READMEs, preprints, UserGuide exercises, Kit);
- **code**: live or dead? Liveness ≠ presence on HEAD (precedent: `poclet_parser.py`).

Leads to confirm at HEAD (from the 2026-11-15 survey, *unverified*): the M3 files
`GenesisGrammar`, `GrammarFoundation`, `OdinsWisdom`, `EagleEye`, `SphinxEye`; in M2,
`m2:hasEpistemicGap` and `m2:epistemicGapFormula`; in M0, `M0_Common` plus most
instances; the M0 SHACL schema; check_m0; `TSCG_Debt_Overview.md` (it already records
`m0:epistemicGap` written as an object in some instances).

**Q2 — Concept or measure?** For every *doctrine* hit, does it need the **number**, or
only the **idea** of a disparity? Typical cases to settle: "source of depth of the
Stereopsis", "δ₁ = max" for the Stereopsis empty set, "δ₁ = degree of proof
(Curry-Howard)". If an M3 claim stands only on the formula, that is an
**architectural** dependency (pipeline Scenario 2: high risk).

**Q3 — Consumers.** What *reads* δ₁ or the spectral class? Live JS simulations and the
Kit, Explorer and API servers, SPARQL queries, the RAG corpus, the gate. Removing a
value read by a live consumer breaks it silently.

**Q4 — Replacement options (impact analysis only, the choice is Michel's).**
- (a) **Remove with no replacement**: keep the concept in prose only.
- (b) **Grounding channel**: per instance, a list of checks that can fail, each with a
  status (passed / failed / untested).
- (c) **Something else** proposed by Michel.

Before modelling (b) inside TSCG, check the **existing vocabularies** (Michel's rule:
do not reinvent):
- W3C **EARL** (Evaluation and Report Language): test results with outcomes such as
  passed / failed / cantTell / untested;
- W3C **DQV** (Data Quality Vocabulary): quality measurements;
- **PROV-O**: provenance of a check.

*Claude's recollection, to be verified at the source.* Any new M2/M1 concept goes
through `tscg-m2-candidate-filter` (anti-overfitting).

**Q5 — Prerequisites.** For each, say whether it is blocking:
- the decision on Q2 (doctrine wording);
- the instances where `m0:epistemicGap` is malformed (an object instead of a float):
  once deprecated, deletion becomes a legitimate repair;
- the interplay with the M0 namespace backlog (check_m0 C02: `m0:` misbound in some
  instances), which affects any automated M0 edit;
- the baselines: the gate, and the M0 reasoner sweep (`run_all_layers.py --reasoner`,
  Java 25);
- the debt instrument: a check that counts the remaining uses (C16 design);
- **FAIL or WARN** for that check. FAIL follows the precedent of the retired
  `m2:changelog`; WARN keeps fully-green instances green. Michel's call.

**Q6 — Lot breakdown and order.** Layer by layer, foundation first (pipeline
Scenario 4): M3 doctrine, then M2, then M0 vocabulary and checks, then instances, then
narrative docs. Each lot ends with `GATE: PASS` and the reasoner, and every counter
move is explained (debt-honesty rule).

---

## 5. Expected output of the next session

A **feasibility note / Decision Record draft** under `ontology/docs/_01_Worksite/<WS-id>/`
(delivered as a git patch), containing:
1. the Q1 inventory (with the command that produced it);
2. the concept/measure verdict per doctrine hit (Q2), as **proposals**;
3. the consumers (Q3) with their liveness;
4. the options (Q4) with impact, no choice made;
5. the prerequisites (Q5), each marked blocking or not;
6. a proposed lot breakdown (Q6);
7. **numbered decisions for Michel**, to be answered in one batch;
8. a **go / no-go** recommendation for opening the worksite.

---

## 6. Guardrails for this session

- **Michel decides** the modelling choices. Claude brings inventory, impact and
  alignment with semantic-web practice, and never resolves a semantic question alone.
- **Reflexive modelling trap**: do not turn "TSCG's own quality control" into a TSCG
  instance.
- **No count recited**: every number comes from a command run in the session.
- **Debt honesty**: a deprecation that leaves M3 asserting the formula is debt moved
  out of sight. Measure the cross-layer contradiction, or avoid creating it.
