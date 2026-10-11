# TSCG HandOver — WS-5 debt lots, session 2 (2026-10-11): perspectives settled, Odin's Wisdom, class/instance separation started

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-11 (evening)
**Follows**: `../Next_Conversation_2026-10-06/TSCG_HandOver_WS-5_2026-10-06.md` (critical
path, working method, parked findings) and `TSCG_HandOver_WS-5_2026-10-11_complement.md`
(this folder: WS-13, WS-3 L cluster). Read those first; this file adds what the
2026-10-11 session changed.
**Companion files (same folder)**: `TSCG_RemainingWork.png` / `.dot` (graph v4, still
valid; the C lots below are not drawn yet).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot touches the gate or ontologies.
3. **`tscg-generate-mn-grammars`** — only if a lot touches a SHACL grammar (lot C2 does).
4. Then read from HEAD:
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` **1.10.0** — the working
     authority; §8.0–§8.0f are this session's decisions and lots, §8.1–§8.3 the S5
     worksites.
   - `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` — invariant "Three
     perspectives, three terminology contexts (2026-10-11)".

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of **Lot C1** (on top of
  `4c27674`). Confirm with `git log --oneline -10`.
- **Gate**: `cd ontology/toolchain && python run_all_layers.py` → `GATE: PASS`:

  | Layer | files | errors | warnings | shacl_violations |
  |---|---|---|---|---|
  | M3 | 5 | 141 | 604 | 3 |
  | M2 | 1 | 1 | 1368 | 7 |
  | M1 | 17 | 149 | 1 | 446 (counted twice — `check_M1` double count, still open) |
  | M0 | 43 | 124 | 0 | 22 |

- **Tests**: `cd ontology/toolchain && python -m pytest -q` → 46 passed on Michel's
  machine (Pellet tests skipped in Claude's sandbox: its Java is too old).
- **Reasoner**: `python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py
  --file ontology/M2_GenericConcepts.jsonld` → PASSED (2.0.1, imports resolved locally).
- **Push path** unchanged: Claude → `format-patch` → `git am` + gate on a fresh clone →
  Michel `git am`, gate, tests, push. Several pending patches are named `1_…`, `2_…`.
  Untracked folders on Michel's disk can block `git am` (moved to
  `E:\_00_Michel\_tscg_backup_2026-10-11`).

### Shipped 2026-10-08 → 10-11

| Commit | Content |
|---|---|
| `1346dae` | lot (2a): 4 legacy M3 `changelog` objects dropped (D5) |
| `00f9b49` | lot (2b-M2): `rdfs:label` on the M2 ontology node (G1) |
| `2e78ce9`, `3d59cb5` | Debt Overview 1.1.0 / 1.2.0: decision (A), S5-1/S5-2/S5-3, three perspectives |
| `8e61f7f` | lot (A): `m3:ontologyType` declared in the apex `M3_GrammarFoundation` (Genesis); three perspectives typed; `m3:metaphoricLabel` |
| `6b79fc5` | `owl_reasoning_test` 2.0.0: `owl:imports` resolved locally; inconsistency reported as FAILED |
| `7d2cfb1`, `551e2a6` | "one role, one property" batches 1–2 (5 headers → `dcterms:description` only; 12 SKOS nodes → `skos:definition` only; grammar 0.2.0) |
| `db50204` | 2026-10-11 complement HandOver, WS-13 registered, WS-3 L cluster, graph v4 |
| `f47ced0` | **lot R**: `M3_BicephalousPerspective` → `M3_OdinsWisdom`; `m3:bicephalous:X` → `m3:odins_wisdom.X` |
| `4c27674` | **lot P**: `m2:producingFunction` is an `owl:AnnotationProperty`; `m1:Propagation`, `m1:CascadeAmplification` are Fm2; reasoner 2.0.1 |
| *(Lot C1)* | combos are derived classes: 122 `rdfs:subClassOf` strings → IRIs in 13 extensions; M1 SHACL 1.6.0 / `check_M1` 1.6.0 target combos by `subClassOf`; M1 SHACL 684 → 446 |

### Founding axioms clarified (Michel, 2026-10-10/11) — see Debt Overview §8.0b

- **Three perspectives** (rows) named in **three coexisting terminology contexts**
  (columns) — "not views, not lenses":

  | Monoidal | Epistemological | Metaphoric |
  |---|---|---|
  | Gt (×) | Territory | Eagle Eye — the eye Odin kept |
  | Gm (+) | Map | Sphinx Eye — the eye in Mímir's well |
  | Gs (\|) | Stereopsis | Odin's Wisdom |

  Φ/Ψ = **Synesthesia**. "Bicephalous" retired as a metaphor (lot R2 for the ~45
  remaining adjectives). Fuxi-Nüwa, Ardhanarishvara: documentary echoes only.
- **Commutative Lambek calculus**; precedence × (Gt) > + (Gm) > | (Gs).
- **Primitives always suffixed** in prose: AStFItD, REVOIm, TKSsL; identifiers
  (`m0:asfidScores`…) NOT renamed. R = **Representable**.
- **Namespace form**: `m3:odins_wisdom.typeT` (one colon, the prefix separator); S5-3
  target `m3:eagle_eye.X`; M0 keeps `m0.<instance>:Concept`.
- **One role, one property**: file → `dcterms:description`; SKOS concept →
  `skos:definition` (+ scopeNote, example; no counts); OWL term → `rdfs:comment`.
- **M0 primitive scores** are *stipulated* by the KitArchitects (Michel, Aki),
  credibility by accretion — not factual. The `F_x` notation is retired.
- **Fm2 / Fm1m2 are functions**, not functors; signature annotated by
  `m2:producingFunction`; a combo with no M1 domain is an Fm2.
- **NEW — classes and instances clearly separated** (Debt Overview §8.0f): classes in
  M2/M1, instances in M0; a combo is a **derived class** (`rdfs:subClassOf`), never an
  instance of the combo class; documentation about a class is an annotation.

---

## 2. Next goal — finish the class/instance separation

1. **Lot C2**: remove `m2:GenericConceptCombo` / `m2:DomainConceptCombo` from the
   `@type` of the 139 M1 combos (12 Core + 127 extensions); add a rule forbidding it
   (SHACL + `check_M1`, with a negative test); update the SHAPE 2/3 "Pattern" comments
   and SPARQL README example 6 (`?x a m2:GenericConceptCombo` → `rdfs:subClassOf`);
   record the principle as a Bootstrap invariant. Expected: **counts unchanged**
   (simulated in C1: M1 SHACL 446). Check `instances/tscg-tools/TscgPocletMiner/tools/
   rebuild_m2_corpus.py` (it lists `m2:GenericConceptCombo`) before shipping.
2. **Lot C1b**: the 74 non-combo `rdfs:subClassOf` strings in 6 extensions → IRIs.
   Exposes phantoms (`m2:Cascade`, `m1:CommunicationPattern`, `m1:KnowledgeField`):
   measure, then route to lot-NSRESOLVE.
3. **Retired parent**: the 3 Education combos (`EducationalBalance`, `…TradeOff`,
   `…Synergy`) subclass `m1:KnowledgeFieldGenericCombo` (retired Feb. 2026, declared
   nowhere) — outside every combo check. Michel decides: `m2:DomainConceptCombo`?
   Re-attaching them will **raise** M1 counts (new focus nodes).
4. **Part (a), M2** (WS-1 B2): 1110 uses of data/object properties placed on M2 classes
   (`hasExample` 394, `hasDominantM3` 235, `hasStructuralGrammarFormula` 97,
   `hasFamily` 88, `hasPolarity` 86, `eagleView` 67, `sphinxView` 43, `isStereopsic`
   39…) → re-declare the documenting ones as `owl:AnnotationProperty`. Check the M2
   SHACL and `rdfs:domain` uses first; run Pellet on M2 after.

## 3. Other lots queued (Debt Overview)

- **One role, one property — batch 3**: 33 OWL terms (merge `skos:definition` into
  `rdfs:comment`), incl. the mojibake "Æ’ᵢⱼ" in `m3:CouplingStructure`. Texts are
  Michel's: review table first.
- **Lot R2**: ~45 "bicephalous" adjectives (M2 21, M1 3, M0 23 in 14 instances).
- **Phantom `m2:Cascade`** (M1_Electronics, M1_BusinessModeling, M0 Bmc, TrophicPyramid,
  KindlebergerMinsky) and drifted formula copies in `m1:parentGenericConcepts` →
  lot-NSRESOLVE / WS-3.
- Later worksites: S5-1 gauge (before WS-3); S5-1b M0 scores (with WS-10 NS-4); S5-2
  `m1core` (109 occ., 15 files); S5-3 double colon (2399 occ.); `eagle_eye:typeS/typeI`
  renaming; `F_x` cleanup in `functor_role` blocks and the Fm2 definition; WS-13
  priority (Michel); lot-NSRESOLVE; Health Map regeneration; `check_M1` double count.

## 4. Decisions waiting for Michel

1. Order of the next lots: C2 → C1b → retired parent → (a) — or interleave batch 3 / R2.
2. Retired parent of the 3 Education combos (§2.3).
3. WS-13 priority (still null in `worksite.yaml`).
4. Still open from 2026-10-06 §3: Compendium tab visibility, M0 bare-key gauge owner.

## 5. Outside git — Project Knowledge to refresh

- Reload `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` into the Project
  "TSCG Workshop v1" (invariant of 2026-10-11; lot C2 will add the class/instance one).
- `TSCG_FileTree.md` and `TSCG_ReferenceCorpus.md`: re-upload from HEAD (`docs/reboot-kit/`;
  both carry `M3_OdinsWisdom` since lot R).
