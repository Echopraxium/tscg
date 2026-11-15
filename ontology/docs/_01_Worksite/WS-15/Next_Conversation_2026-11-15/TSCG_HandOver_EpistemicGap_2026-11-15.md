# TSCG HandOver — Scoring family retirement (after step 1) and epistemic review

**Date**: 2026-11-15 · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt v17 §4) — a thin loader, no authoritative framework content.
**Worksite**: WS-15 (folder `ontology/docs/_01_Worksite/WS-15/`; was `WS-TBD_EpistemicGap/` until the id was chosen, same day).

---

## 1. Load first — by name

- **`head-over-memory`**: every verifiable fact below is a *pointer to check at HEAD*.
- **`tscg-ontology-diagnosis-pipeline`**: every remaining lot changes ontology files.
- *(If a new M2/M1 concept is ever proposed: `tscg-m2-candidate-filter`.)*

Then read at HEAD, in this order:
1. `ontology/docs/_01_Worksite/WS-15/EpistemicGap_Feasibility_DecisionRecord_Draft.md`
   — Michel's positions (numbered), the inventory, the open decisions (§7).
2. `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` §8.0h — what step 1 did, what is
   left and how it is measured.
3. `docs/CoreHypotheses/LayerCake_Models_The_Kit.md` §6 — *Evaluation is outside the
   model* (the principle behind the whole worksite).
4. `ontology/docs/_02_EpistemicReview/` — two parked/draft notes (facets for M0
   instances; mock-up validation heuristics).

---

## 2. Session state (perishable — verify, do not trust)

- The 2026-11-15 session produced 16 commits, applied and pushed by Michel (he applied
  some as `git mv` + content-only patches because of Windows case-insensitivity: his
  SHAs differ from the session's, the trees are identical). *Unverified here: run
  `git log --oneline -20` and check that the last commit is "Naming: references after
  the M0_VCO / RAAS / TPACK README renames".*
- Last gate on Michel's machine (Windows, Java 25): `GATE: PASS`, PATH_CHECK 0, M0
  reasoner sweep 43 files / failed 0 / error 1 (Yggdrasil, pre-existing).
- Tools changed that day, to read at HEAD before use: `run_all_layers.py` 1.8.0
  (section PATH_CHECK; reasoner file list from git; an unfrozen section fails),
  `path_check.py`, `check-M0/check_m0_instances.py` 1.8.1 (C10/C11 retired, C16
  deprecated-term guard, C03 acronym alias rule), M0 SHACL schema v1.9.
- Paused instance: `RequisiteVarietyDuo` (Ashby, human/AI duo) — analysis file outside
  the repo; it must not use scores or gaps; decision D15 of the note concerns it.

---

## 3. What Michel decided (non-verifiable: decisions and positions)

Recorded in the note (positions 1–16); in short:
- No scores, no epistemic gap (δ₁), no focal score (δ₂). A model — a mock-up as the
  toolkit — is not legitimate to evaluate itself; evaluation is subjective, belongs to
  the user and the observers (at least one human), outside the model.
- The three monoids and the Layer Cake are not a model of reality (an architecture
  "until further notice" for building mock-ups; M2 concepts are proxies).
- Korzybski's principle is a foundation and stays. Gs is not a feedback loop.
- Method: deprecate the definitions (with the epistemological reason in the comment),
  delete their uses; M0 first (done), then M3/M2 prose; in several steps.
- `M0_Common` stays as the federating namespace with its generic properties.
- Intersubjective scoring removed (README deleted; M3 declarations still to go).
- Naming norm: instance folders start with a capital; `.jsonld`/`.md` names keep
  acronyms in capitals with underscores (`M0_VCO.jsonld`, `M0_RAAS_README.md`); the
  ontology alias of an acronym is lowercase (`m0.vco`).
- Facets for M0 instances: parked, not to be touched now.
- Validation/refutation heuristics for mock-ups and for the Toolkit must be proposed
  (draft only).

---

## 4. Next steps (choose with Michel; each lot ends with GATE: PASS + reasoner)

1. **M3/M2 prose and declarations** — needs Michel's wording first: D4 (each Q2 row
   rewritten as Korzybski only, no gap), D14 (ground of the Odin's Wisdom / Stereopsis
   metaphor without "depth from disparity"), D20 (definition of the M3 primitives
   without the "evaluation at M0" role). Then deprecate/delete
   `intersubjectiveBenchmark`, `defeasibilityStatus` (D17), `m2:hasEpistemicGap` (D8),
   delete the δ₁ phantoms. Foundation first: M3, then M2. Pipeline Scenario 2 for D20.
2. **M0 step 2: ad hoc score encodings** not using `M0_Common` terms (`A_score` objects,
   `asfidState`, numbers inside ASFID/REVOI analyses, local `…Score`). Measured by
   `delta1_inventory.py` section F. Blocked on a rule to decide with Michel: the
   qualitative text next to the numbers — kept as description of the mock-up, or
   deleted with them?
3. **Producers outside the gate**: instance-pipeline and simulation skills (Michel
   saves skill changes), the simulation template score panel, gallery radars and δ
   badge, PocletMiner prompt, PocletGenerator, `modernize_m0.py`,
   `migrate_m0_to_v1_5.py`.
4. **Narrative**: CoreHypotheses (ScoringSystem, Multisubjective protocol, Credibility
   Accretion, Narcissus §2 — D18, Epistemic Residue), READMEs, UserGuide samples.
5. **Smaller items**: other acronyms in file names (`M0_Bmc`, `M0_Triz`, `M0_Ptoe`… —
   each rename changes the instance IRI); a `pre-commit` hook calling
   `path_check.py`; the worksite priority (D1; the id is WS-15); move the study under `_02_EpistemicReview`
   or not.

---

## 5. Guardrails

- **Michel decides** wording and modelling; Claude brings inventory, impact, patches.
- **Debt honesty**: a counter falls only when the defect disappears; reveal first,
  then repair, and write why in the commit and in `golden_values.json`.
- **Windows**: a case-only rename cannot be applied with `git am` there — split into
  `git mv` (two steps through a temporary name, in a `.bat`) + a content-only patch.
- **No count recited**: every number comes from a command run in the session.
- **Reflexive trap**: the validation heuristics belong to the method, not to M2.
