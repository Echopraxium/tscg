# TSCG HandOver — 2026-11-18: WS-15 SF-3 done; next = preprint v7 rewrite

**Date**: 2026-11-18 · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt §4). It loads and points; it holds no authoritative
framework content. Every number below is a *pointer to re-measure at HEAD*, not a fact.

---

## 1. Load first — by name

- **`head-over-memory`** — counts, versions, structure: read at HEAD, never recite.
- **`tscg-article-pipeline`** — Step 1 (Audit) was run on 2026-11-18 (§3 below); the next
  conversation starts at its **⏸ sync point: Michel picks the strategy**, then Step 2.

Then read at HEAD:
1. `docs/papers/preprints/TSCG_Research_Paper_Draft_v6.md` (the draft to replace).
2. `ontology/docs/_01_Worksite/WS-15/worksite.yaml` and
   `ontology/docs/_01_Worksite/WS-15/EpistemicGap_Feasibility_DecisionRecord_Draft.md`
   (positions 9-19: the decisions that reshape the paper).
3. `ontology/docs/_02_EpistemicReview/MockupValidation_Heuristics_Draft.md` (§7b: the
   alignment loop moved out of the model).
4. `docs/CoreHypotheses/LayerCake_Models_The_Kit.md` §6 (evaluation outside the model).

---

## 2. What happened on 2026-11-18 (4 commits + this HandOver)

| Commit subject (VM SHAs differ from Michel's) | Content |
|---|---|
| WS-15: record Michel's answers of 2026-11-18 | Decision record 0.10.0, position 17 |
| WS-15 SF-7: delete the phantom m2:stereopsicArchitecture | M2 16.40.0 |
| WS-15 SF-3 batch A | δ₁ out of M3/M2 prose; `m3:AlignmentLoop` **deprecated** (moved out of the model) |
| WS-15 SF-3 batches B-D | benchmark deleted; `defeasibilityStatus` generalised; D20 wording; `m2:hasEpistemicGap` deprecated |

Michel's machine, 2026-11-18: `run_all_layers.py --reasoner` -> 6 changed files PASSED,
`GATE: PASS` (batch A). Pushed at 15:30 up to batch A; batches B-D and this HandOver
travel in one last mbox (apply, `--reasoner`, push). *Check with
`git log --oneline origin/main -6`: the top commit should be this HandOver.*

### Decisions of the day (non-verifiable — Michel's words, recorded in positions 17-19)
- Korzybski without the gap: "Φ : Gt → Gm is never a perfect isomorphism".
- **The Territory ↔ Map alignment loop is not in the model**: it is the validation run
  at the end of modelling by the user and the observers — **at least one of them human**
  (an AI may take part). Φ (observation) and Ψ (interpretation) stay in M3.
- At M0, a primitive type is **a qualitative reading grid of the instance, with no
  numeric value**.
- Every TSCG model is **provisional and refutable** (`defeasibilityStatus`).
- Odin's Wisdom / Gs stays an algebra; its naming rationale (Ashby's requisite variety,
  **pilot / co-pilot**: the model is the co-pilot, the user or the critics of the mock-up
  are the pilot; second-order cybernetics) goes to the narrative docs — **not yet written**
  (WS-15 SF-5).
- SF-2 rule: in M0 score blocks, keep the qualitative text, remove the numbers.

### WS-15 after today (verify in `worksite.yaml`)
SF-0, SF-1, **SF-3** done · SF-7 partial · SF-2 todo (rule given) · SF-4 todo
(producers) · SF-5 partial (narrative docs, incl. the Odin rationale) · SF-6 draft
(heuristics). Later: delete the two deprecated terms; 7 broken `\"` sequences in
`M3_GenesisGrammar.jsonld` (encoding lot, not WS-15).

---

## 3. Preprint audit (Step 1 of tscg-article-pipeline, 2026-11-18)

v6 is dated June 2026; ~340 commits since. Re-measure every item at HEAD.

**Major gaps**
1. **Scoring retired** (WS-15): v6 Abstract, §5 (δ₁, EFS/δ₂, SpectralClasses,
   FocalClasses) and part of §6 rest on it. Candidate reframing: §5 becomes "Why TSCG
   does not score itself" — evaluation outside the model, at least one human; defeasible
   models; validation heuristics (SF-6) as ongoing work.
2. **Vocabulary**: "bicephalous" -> "stereopsic" / "dual" (WS-15 SF-7); v6 §1.3 and
   Abstract use the old word.
3. **M3 additions absent from v6**: GrammarFoundation, OdinsWisdom (Gs), Facet as an M3
   principle (WS-0 SC-3), Audience facet (WS-12); AlignmentLoop now deprecated.
4. **Corpus**: new instances since v6 (to confirm at HEAD): Thermostat, World2DProjection,
   QRCodeToPocketCity (poclets), TscgFoundationGrammar (SSG), TscgPocletGenerator,
   TscgLayerCakeMCPServer (tools); status to decide: CanopyGraphVizProto, Theremin.
5. **Simulations**: from one-HTML-page-per-poclet to the ThreeLegs / Kit architecture
   (WS-14; Thermostat first), `LayerCake_Models_The_Kit.md`.
6. **Validation infrastructure** missing from v6 (§4.7 mentions SHACL only): the gate
   `run_all_layers.py` and golden values, document and graph planes, Mn SHACL grammars
   (WS-11), the reasoner on changed files, the LayerCake Health Map, frozen debt counters.

**Minor**
- `KnowledgeFieldConceptCombo` was renamed **`DomainConceptCombo`** (SC-5, 2026-10-12):
  the article-pipeline watchdog still mandates the old name — **update the skill**.
- Author line: v6 has "Michel Kern (aka Echopraxium) with the collaboration of Claude
  AI"; the watchdog says "Echopraxium with the collaboration of Claude AI" — Michel decides.
- GenericConcept count: v6 says 80; on 2026-11-18 a naive count gave 75 direct
  subclasses of `m2:GenericConcept` (78 with multiple parents), 9 families + Combo — fix
  the counting rule before citing any number.
- v6 internal inconsistency: header v16.2.0 vs Appendix C v16.14.0; duplicate §3.6
  heading; empty §3.5.
- `docs/papers/preprints/Zenodo/_05_TSCG_Zenodo_Submission_Notice.md` still describes v4.
- Side finding: `ontology/M2_GenericConcepts_README.md` header lags the M2 file version.

---

## 4. Next — Michel picks

1. **Preprint strategy** (the ⏸ of Step 1): full rewrite v7.0 (recommended on
   2026-11-18), targeted update, or wait for WS-15 SF-6.
2. Then Step 2 (plan section by section), one section per turn.
3. Before or alongside: update `tscg-article-pipeline` (watchdog: DomainConceptCombo;
   "Plan historique" block; author line).

## 5. Guardrails
- Michel decides wording; Claude brings inventory, impact, patches (`git am`, one mbox);
  Claude never pushes. Commit identity: author Echopraxium, no Claude trailer (`CLAUDE.md` §5).
- No count recited: every number comes from a command run in the session.
- Archives untouched (`docs/papers/inputs/`, `ontology/Ref/`, dated records).
