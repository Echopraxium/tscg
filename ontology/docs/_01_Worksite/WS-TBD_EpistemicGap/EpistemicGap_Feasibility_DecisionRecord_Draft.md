# Epistemic gap δ₁ — Feasibility note / Decision Record draft

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.2.0 (draft) · **Date**: 2026-11-15
**Kind**: feasibility study (pipeline Phase 0 + Phase 1). **No ontology file is changed.**
**Worksite id**: not registered. The folder name `WS-TBD_EpistemicGap/` is a
placeholder; rename it with `git mv` once Michel picks the id (decision D1).
**Measured at**: HEAD `5a26560` (2026-11-09), verified with `git log -1` in a fresh clone.

Everything below that is a number comes from a command run in this session. The
inventory script is committed next to this note (`delta1_inventory.py`, standard
library, read-only) and its output at `5a26560` is `delta1_inventory_5a26560.md`.
Everything marked **proposal** is Claude's analysis: Michel decides.

---

## Michel's positions (2026-11-15, after reading v0.1.0)

These are decisions and positions, stated in the conversation; they are not
verifiable at HEAD and are recorded here as said.

1. **A scalar measure of the epistemic gap has no meaning.**
2. **The epistemic gap itself has no meaning** — not only its formula. v0.1.0 proposed
   to keep the concept ("their disparity gives depth") and drop the measure; that
   proposal is withdrawn.
3. **Korzybski's principle is a foundation of TSCG** and stays: the Map is not the
   Territory. It is kept as a principle, without a gap, a distance or a disparity
   derived from it.
4. **Intuition, to be designed**: replace the gap with **validation heuristics** inside
   a **human/machine cybernetic loop**, which has yet to be invented.

What this changes below: §2 (the "concept" column now means Korzybski only), §4
(option (a) removes concept and measure; option (c) becomes the heuristics loop),
§6 (L7) and §7 (D2 answered, D4/D5 narrowed, D13–D15 added).

---

## 0. Baseline (Phase 1)

| check | command | result at `5a26560` |
|---|---|---|
| acceptance gate | `cd ontology/toolchain && python run_all_layers.py` | `GATE: PASS` |
| M0 reasoner sweep | `PATH=<jdk-25>/bin:$PATH python run_all_layers.py --reasoner` (Temurin 25.0.1) | 43 files, 2 not passed (`M0_Bmc` FAILED, `M0_Yggdrasil` ERROR) = frozen `M0_REASONER` |
| validator report | `python ontology/toolchain/validator/tscg_validator.py --source local --layers M3,M2,M0 --doc --ext --report /tmp/val.json` | used for the δ₁ share of D1 / G5 / G8 (§1.6) |

The gate's REASONER block says "no ontology file changed since origin/main". This
note changes no ontology file, so no reasoner run is owed for it.

---

## 1. Q1 — Inventory at HEAD, by layer and by role

### 1.1 Command and totals

The HandOver pattern was extended in two ways: `-i` plus `δ1|spectral_class|delta_?1\b`
(the key `delta1` and the PocletMiner field `spectral_class` were missed), and the path
list was widened to the whole tree (`kit/`, `cli_tools/`, `.claude/skills/`, the root
`index.html` were outside it).

```bash
git grep -n -I -i -E "δ₁|δ1|δ\(M\)|epistemicGap|EpistemicGap|epistemic.gap|spectralClass|SpectralClass|spectral_class|delta_?1\b" \
  -- . ':(exclude)*migration_backups*' ':(exclude)*_backups*'
```

**311 files, 1499 lines.** By area (section A of the inventory output):

| area | role | files | lines |
|---|---|---|---|
| M3 | ontology | 5 | 24 |
| M2 | ontology | 1 | 5 |
| M1 | ontology | 1 | 1 |
| M0_Common | ontology | 1 | 35 |
| M0 instances (+ UserGuide samples) | use | 45 | 194 |
| gate | SHACL (M0 schema, M1 schema) | 2 | 39 |
| gate / tooling | code (check_m0, modernize_m0, migrate_m0) | 3 | 9 |
| skills (`.claude/skills/`) | producer (instructions) | 6 | 33 |
| code | scripts, simulations, apps | 46 | 142 |
| code | pages (sim `static/`, `index.html`) | 29 | 55 |
| data | snapshots (RAG profiles) | 3 | 52 |
| docs | narrative | 140 | 568 |
| historical | `docs/papers/`, old Smart Prompts | 26 | 171 |
| archive | `ontology/Ref/` snapshots | 3 | 171 |

The Kit (`kit/`) has **no** hit. Its word "écart" is a physical gap (angle, humidity),
not δ₁ (checked with `git grep -i -E 'epistemic|δ|écart|spectral' -- kit`).

### 1.2 M3 — 5 files, 23 JSON paths (section B)

| file | node | path | role |
|---|---|---|---|
| `M3_EagleEye` | `m3:eagle_eye:EagleEye` | `coupling_with_MapGrammar/epistemic_gap` {symbol, formula, meaning} | definition (formula), **bare key (D1)** |
| | | `coupling_with_MapGrammar/korzybski` "… δ₁ > 0 in all real systems" | doctrine |
| `M3_SphinxEye` | `m3:sphinx_eye:SphinxEye` | same two paths, mirrored | definition + doctrine, **D1** |
| `M3_GenesisGrammar` | `m3:GenesisGrammar` | `grammar_foundation/connection/epistemic_gap` = the formula | definition (formula), **D1** |
| | | `three_perspectives/…/feedback_loop/convergence` "δ₁ → 0 represents epistemic equilibrium" | doctrine |
| | `m3:CouplingStructure` | `m3:mathematicalForm` "Φ, Ψ …, δ₁ = ‖ASFID_mean − REVOI_mean‖ / √2" | definition (formula) |
| | `m3:AlignmentLoop` | `m3:iteration` "… until δ₁ converges toward epistemic equilibrium" | doctrine |
| | `m3:KorzybskiPrinciple` | `m3:formalization` "Φ … never a perfect isomorphism — δ₁ > 0 …" | doctrine |
| | `m3:SystemicFramework` | `m3:integrationGuidelines/step5` "Document epistemic gaps and alignment scores" | doctrine |
| `M3_GrammarFoundation` | `…:TypeSystem` | `levels/M0/curry_howard` "Poclet = proof term. δ₁ = degree of proof" | doctrine |
| | `…:intersubjectiveBenchmark` | `structure/epistemicScore` {property: `m0:epistemicGap`, formula, range [0,1]} | definition (formula), **bare key `epistemicScore` (D1, G6)** |
| | `…:SpecialElements` | `StereopsisEmptySet` "δ₁ = max", `StereopsisUniversalSet` "δ₁ = 0", "distinct from SpectralClass Coherent" | doctrine, **G8** (`m3:grammar_foundation:epistemicGap`) |
| `M3_OdinsWisdom` | `m3:odins_wisdom.StereopsisEmptySet` | `rdfs:comment` and `m3:epistemicGap` "δ₁ = max" | doctrine, **G8** (`m3:epistemicGap`) |

(The remaining paths are `dcterms:description` sentences of the three grammar headers and
one changelog entry.)

### 1.3 M2 — `M2_GenericConcepts`

- `m2:hasEpistemicGap` is **declared** (DatatypeProperty, domain `m2:GenericConcept`,
  range `xsd:double`) and **used by no GenericConcept** at HEAD
  (`grep -c hasEpistemicGap ontology/M2_GenericConcepts.jsonld` → 1, the declaration).
  The 2026-02-17 snapshot in `ontology/Ref/` still carried values on the concepts.
- `m2:epistemicGapFormula` "δ(M) = ‖P(Reality) − Model‖ ∈ [0,1]" on the ontology header:
  a third formula, and a **phantom predicate (G8)**.
- `m2:Modelisation` / `m2:korzybskiConnection`: "the epistemic gap δ₁ > 0 is constitutive
  of Modelisation" (doctrine).
- The header `dcterms:description` still says each GenericConcept is characterised by
  its "epistemic gap" — no longer true at HEAD.

### 1.4 M1 — one hit not in the HandOver leads

`M1_extensions/optics/M1_Optics.jsonld`, node `m1:MapTerritory_Optics` (an
`owl:Class` subclass of `m2:DomainConceptCombo`) carries `m1:epistemicGap` with a
ket-notation formula ("ΔΘ = ‖Territory_ASFID − Map_REVOI‖"), stored as mojibake.
M1 SHACL SHAPE 11 forbids `m1:hasEpistemicGap` and `m2:hasEpistemicGap` on combo
types, but not this third IRI: the shape does not see it.

### 1.5 M0_Common and the M0 instances

**`M0_Common`** defines `m0:epistemicGap` (float, formula `|asfidMean − revoiMean| / √2`,
the threshold map), `m0:SpectralClass` (`owl:oneOf` of 4 individuals),
`m0:spectralClass` (object property) and mentions δ₁ in `m0:scoringStatus.Complete`.

**A twin measure**: `m0:focalBias` = `revoiMean − asfidMean` (its `m0:formula`), so
`|m0:focalBias| = √2 · δ₁` exactly, and `m0:focalScore` = `stereopsicDepth × (1 − |focalBias|)`.
The focal family ("δ₂" in `docs/CoreHypotheses/ScoringSystem.md`) rests on the same
subtraction of the two means. The HandOver patterns do not catch it (decision D3).

**M0 instances** (43 files, the gate's own discovery `check_m0.discover_instances`).
Form of `m0:epistemicGap` on the `owl:Ontology` node (section C):

| form | instances |
|---|---|
| float | 23 |
| object (`formula`, `deltaVector`, `norm` … bare keys) | 5 |
| typed literal `{"@value": "…", "@type": "xsd:float"}` (C10 FAIL) | 2 (VSM, IChing) |
| string | 1 (Counterpoint) |
| absent | 11 |
| no `owl:Ontology` node | 1 (Triz_Examples) |

On another `@graph` node: 8 more files, of which 4 objects (MtgColorWheel,
PlateTectonics, TrophicPyramid, TVTestPattern). Objects in all: **5 + 4 = 9**, which
matches the 9 recorded in `TSCG_Debt_Overview.md`. Three instances also keep a local
twin (`m0.fireTriangle:`, `m0.thermostat:`, `m0.world2DProjection:epistemicGap`).

**Internal consistency** (same section C; class from the `M0_Common` thresholds, gap
recomputed from the stored means):

- stored class ≠ class given by the thresholds: **3** (VSM 0.08 "Coherent",
  TscgPocletGenerator 0.136 "Coherent", TscgPocletMiner 0.06 "Coherent");
- stored δ₁ ≠ `|asfidMean − revoiMean| / √2` (tolerance 0.005): **5**
  (ButterflyMetamorphosis 0.22 vs 0.078, VSM 0.08 vs 0.057, TscgOntologyExplorer 0.0316
  vs 0.0, TscgPocletGenerator 0.136 vs 0.003, TscgPocletMiner 0.06 vs 0.041).

### 1.6 Formula census (section D) and gate visibility

At least **six families of formulas** coexist, which supports argument 5:

1. `|ASFID_mean − REVOI_mean| / √2` (M3, `M0_Common`, M0 SHACL message);
2. `‖ASFID − REVOI‖` on the 5-vectors: unnormalised (TscgPocletGenerator, NakamotoConsensus),
   `/ √5` (PlateTectonics), `/ max_possible` (MtgColorWheel);
3. ket form `ΔΘ = ‖|Ω⟩ − |M⟩‖` (CellSignalingModes, RGB_Additive, ExposureTriangle,
   TPACK, `M1_Optics`, the simulation parser);
4. `δ(M) = ‖P(Reality) − Model‖` (M2 header);
5. `δ = 1 − (ASFID_mean + REVOI_mean) / 2` (TVTestPattern — not a difference at all);
6. `|mean(ASFID) − mean(REVOI)|` without the √2, called "normalized vectorial distance"
   (PocletMiner system prompt, `SystemPrompts.js:48`).

Share of the δ₁ family in the validator report (findings whose node is a family key;
these are report findings, **not** gate counter deltas — a lot measures its own deltas):

| finding | M3 | M2 | M0 |
|---|---|---|---|
| D1 bare key | 4 (`epistemic_gap` ×3, `epistemicScore`) | — | 13 |
| G8 phantom predicate | 2 | 1 (`epistemicGapFormula`) | 23 |
| G5 / G6 | — | — | 3 / 1 |
| CTX-5i | — | — | 19 |

Most M0 G8 hits are files where `m0:` is misbound (check_m0 C02): their
`m0:epistemicGap` expands into the instance's own namespace, not `M0_Common`.

---

## 2. Q2 — Concept or measure? (proposals)

Since Michel's positions (above), the question is no longer "concept or measure":
both go, and only **Korzybski's principle** stays. Each row therefore asks whether the
statement can be rewritten as Korzybski alone (the Map is not the Territory), with no
gap, distance or disparity left in it.

Two checks a reader can redo by hand (evidence for position 1):

- **Range.** With both means in [0, 1], `|a − b| / √2 ≤ 1/√2 ≈ 0.707`. The declared range
  [0, 1] (`M0_Common`, M0 SHACL, `intersubjectiveBenchmark`) is never reached above 0.707.
  The normalisation is posited, not derived (argument 4).
- **Degeneracy inside M3.** `StereopsisEmptySet` = EmptyTerritory | EmptyMap is glossed
  "δ₁ = max". With every score at 0, the M3 formula gives `|0 − 0| / √2 = 0`, the same as
  `StereopsisUniversalSet` ("δ₁ = 0"). M3 contradicts its own formula on the two special
  elements (argument 3, at the foundation).

| # | doctrine hit | needs the number? | proposal | risk |
|---|---|---|---|---|
| Q2-1 | Eagle/Sphinx `korzybski` "δ₁ > 0 in all real systems" | no — "Gt ≠ Gm structurally" already says it | keep the sentence up to "structurally", drop the δ₁ clause; delete the `epistemic_gap` blocks (bare keys) | low |
| Q2-2 | GenesisGrammar `connection/epistemic_gap` | it *is* the number | delete (bare key) | low |
| Q2-3 | `m3:CouplingStructure/m3:mathematicalForm` | no — Φ and Ψ stand alone | drop the δ₁ clause | low |
| Q2-4 | `m3:KorzybskiPrinciple/m3:formalization` | no | keep "Φ : Gt → Gm is never a perfect isomorphism", drop "δ₁ > 0 …" | low |
| Q2-5 | `m3:AlignmentLoop/m3:iteration` and `feedback_loop/convergence` "until δ₁ converges", "δ₁ → 0 = equilibrium" | **yes, as written**: δ₁ is the loop's only stated stopping criterion | the loop keeps its Φ/Ψ structure; its stopping criterion is what the validation-heuristics loop (option c) is to define. Until then, state the loop without a criterion ("iterative refinement via Φ/Ψ") rather than invent one. Wording is Michel's | **medium** |
| Q2-6 | `TypeSystem/M0/curry_howard` "δ₁ = degree of proof" | the clause does; the reading does not | keep "Poclet = proof term"; drop "δ₁ = degree of proof" (Curry–Howard has inhabitation, not degrees) | low |
| Q2-7 | `intersubjectiveBenchmark/structure/epistemicScore` → `m0:epistemicGap` | the slot does; the benchmark (consensus, ICC/κ, resolution order) does not | remove the `epistemicScore` slot; the benchmark calibrates the 10 scores | medium (it is the benchmark's only named score) |
| Q2-8 | `StereopsisEmptySet` "δ₁ = max", `StereopsisUniversalSet` "δ₁ = 0", "distinct from SpectralClass Coherent" | no — the algebra (neutral element, pseudo-absorbent) and "Territory and Map share nothing" carry it | drop the δ₁ glosses (they also contradict the formula, see above); deletes 2 G8 predicates | low |
| Q2-9 | `SystemicFramework` step 5 "Document epistemic gaps …" | no | "Document where the mapping fails" | low |
| Q2-10 | M2 `m2:epistemicGapFormula` | it is the number | delete (G8) | low |
| Q2-11 | M2 `m2:Modelisation/m2:korzybskiConnection` "δ₁ > 0 is constitutive" | no | "the imperfection of Φ is constitutive of Modelisation" | low |
| Q2-12 | Debt Overview §"Odin's Wisdom": "the gap δ₁ is the source of depth" | the **concept** does: the rationale is the disparity itself | v0.1.0 proposed "the disparity is the source of depth"; withdrawn (position 2). The naming rationale of Odin's Wisdom / Stereopsis needs another ground, or is reduced to "one place where the two views fuse" (D14) | **medium** |

**Verdict (proposal, revised in 0.2.0).** No M3 axiom, operator or type depends on the
formula or on the gap: the algebra of Gs (neutral element, pseudo-absorbent, the
operator `|`) is defined without them. Three statements lose their content: the
AlignmentLoop stopping criterion (Q2-5), the benchmark's score slot (Q2-7), and the
metaphoric rationale of the Stereopsis as "depth from disparity" (Q2-12). These are
wording and rationale decisions, not structural ones: a doctrine edit of medium risk,
not pipeline Scenario 2. Korzybski's principle survives every row (Q2-1, Q2-4, Q2-11
keep it, stated without a gap). Q2-4 and Q2-11 still say "Φ is never a perfect
isomorphism" / "the imperfection of Φ": that is Korzybski in categorical words, not a
gap, but Michel should confirm it does not smuggle the gap back (D4).

---

## 3. Q3 — Consumers and their liveness

"Liveness" is judged by evidence, not by presence on HEAD (precedent `poclet_parser.py`).

| consumer | what it reads or writes | liveness (evidence) | if δ₁ goes |
|---|---|---|---|
| check_m0 C10 / C11 (`SCORE_PROPS`, `ENUM_PROPS`) | type of `m0:epistemicGap`, IRI form of `m0:spectralClass` | **live** — runs in the gate | deleting values can turn C11 PASS on Counterpoint, VSM, IChing (repair by deletion, explained) |
| M0 SHACL (`M0_Instances_Schema_shacl.ttl`, C15) | property shapes on both terms, `ForbidStringSpectralClassShape`, messages | **live** — gate | shapes and messages to retire in the M0 lot |
| M1 SHACL SHAPE 11 | forbids `m1:` / `m2:hasEpistemicGap` on combo types | **live** — gate | keep as a guard, or retire (D8); blind to `m1:epistemicGap` |
| validator D1 / G5 / G8 | counts the family's bare keys and phantoms | **live** — gate | deletions lower these counters: legitimate repairs by deletion |
| gallery generator `cli_tools/regenerate_simulation_gallery/generate_index.js` → root `index.html` | reads `m0:epistemicGap`, shows `δ=` | **live** — `index.html` last changed 2026-11-07 | degrades cleanly: `gap == null` is handled (`index.html` l. 758, 774; generator l. 809) |
| simulation pages (`static/`, `sim/`) | hardcoded copies of δ₁ (no page reads the key) | live pages, **no read** | text goes stale; edit in the narrative lot |
| sim template `instances/poclets/_00_template/src/tscg-shell.js` | "Epistemic Gap δ₁" panel | **producer** for every new simulation | edit in the producers lot |
| skills `tscg-instance-pipeline`, `tscg-create-instance-simulation`, `tscg-tensor-to-structural-grammar-migration` | step 3 writes the gap; badge and example; "δ₁ unchanged" | **producer** — the paused RequisiteVarietyDuo goes through it | edit (Michel saves skill changes) |
| TscgPocletMiner (`SystemPrompts.js`, `PocletPipeline.js`, `renderer.js`, `RagBuilder.js`) | asks the LLM for `epistemic_gap` / `spectral_class`; reads `m2:hasEpistemicGap` | **producer**; app liveness unknown (last touched 2026-09-30) — Michel | its prompt keeps generating δ₁ classes until edited |
| TscgPocletGenerator (`tscg_poclet_generator.py`) | writes a δ template | producer; last touched 2026-03-16 — Michel | edit or mark retired |
| `ontology/toolchain/modernize_m0.py` | computes and writes `m0:epistemicGap` | producer (migration tool, 2026-10-03) | remove the computation |
| RAG `src/tscg/rag/create_tscg_rag*.py`, `poclet_corpus_profile.json` | reads `m2:hasEpistemicGap`; snapshot | **dead read** — the M2 field has no value at HEAD | nothing breaks; regenerate snapshots when RAG is next rebuilt |
| `ontology/sparql/m2_sparql_analysis.py`, `SPARQL_README.md` | `?metaconcept m2:hasEpistemicGap ?gap` | **dead read** — no values, retired "metaconcept" vocabulary, last touched 2026-02-09 | nothing breaks |
| `src/tscg/simulation-engine/poclet_parser.py` (+ 2 copies in instances) | object form `epistemicGap` | dead (precedent) | nothing breaks |
| TscgOntologyExplorer / TscgOntologyAPIServer | no source on HEAD reads the key; only docs and `tscg_api_client_example.py` | **cannot be assessed on HEAD** — Michel | generic display: the value just disappears |
| Kit | — | no consumer | — |

---

## 4. Q4 — Options (impact only; the choice is Michel's)

**(a) Remove the measure and the concept.** (0.2.0: per positions 1–2, the concept
goes too; only Korzybski's principle stays, as M3 doctrine.) Impact: lots L1–L6 below;
the gallery loses the `δ=` badge; the instance pipeline loses a step. Cost: until (c)
exists, TSCG says nothing about how well a Map holds against its Territory. Smallest
modelling change, and it can run **before** (c) is designed (D13).

**(b) Grounding channel.** Per instance, a list of external checks that can fail, each
with an outcome. Existing vocabularies, verified at source on 2026-11-15:

- **EARL 1.0 Schema** — published as a W3C *Working Group Note* (not a Recommendation).
  `earl:Assertion` (`earl:assertedBy`, `earl:subject`, `earl:test`, `earl:result`),
  `earl:TestResult` with `earl:outcome`. Outcome values: `earl:passed`, `earl:failed`,
  `earl:cantTell`, **`earl:inapplicable`**, `earl:untested` (the HandOver omitted
  `inapplicable`). Fits "a check that can fail" directly.
- **PROV-O** — W3C *Recommendation* (2013-04-30). `prov:wasAttributedTo`,
  `prov:wasGeneratedBy`, `prov:used`: who ran the check, when, on which source.
- **DQV** — W3C *Working Group Note* (2016-12-15). `dqv:QualityMeasurement`,
  `dqv:Metric`, `dqv:Dimension`. Useful only if a number is wanted; a measurement by the
  same rater would bring argument 2 back.

Two ways to bring (b) in, impact only:
- **(b1)** use the EARL / PROV terms as they are, declared once in the apex
  (`m3:grammar_foundation:ExternalVocabularyPolicy`: declare, never `owl:imports`). No new
  M2/M1 concept; M3 apex declarations, an instance-pipeline step, a gate check (outcome in
  the enumeration, each assertion has a subject, a test and a source).
- **(b2)** a TSCG concept for "grounding check": must go through `tscg-m2-candidate-filter`.
  Observation, not a verdict: a check on the *model* is metadata about the Map, not a
  generic concept of the *systems* modelled — this is the reflexive-modelling trap of the
  HandOver §6. (b1) avoids it.
- Existing values cannot be converted: no instance records the checks behind its scores.
  Writing `earl:untested` everywhere would be invented content; absence means "nothing
  asserted".

(0.2.0: with positions 1–2, (b) is no longer an alternative to (a). It survives as a
possible **recording format** for the outcomes of (c): EARL outcomes, PROV-O provenance.)

**(c) Validation heuristics in a human/machine cybernetic loop** (Michel's intuition,
2026-11-15; to be invented). A separate design worksite, not a replacement written into
the removal lots. Inputs for that design, as **proposals**:

- *What a heuristic could be*: a question put to a model that **can fail** (does it
  predict something observable? does its simulation behave like the system? does the
  pattern hold in a poclet of another domain? is there a source, or a counter-example?),
  with **who runs it** (human, machine, both), an **outcome** (EARL values fit), and
  **what a failure triggers** (revise the Map, revise a score, record a limit of the
  model). The loop is cybernetic because the outcome feeds back; there is no final
  grade, only a record of what was put to the test and how it went.
- *TSCG already runs such heuristics, on itself*: the M2 candidate filter
  (Decomposability, Transdisciplinarity, Atomicity), the debt-honesty rule,
  baseline-before-blame, the gate and the reasoner (checks that can fail), and the
  diagnosis pipeline (Human / LLM / Formal Tools with separate roles) — a human/machine
  loop already, applied to the ontology rather than to the models. (c) would bring the
  same discipline to M0 instances.
- *Reflexive-modelling trap* (HandOver §6): the loop belongs to the **method**
  (instance pipeline, toolchain, gate), not to the grammar of systems (M2). Modelling it
  as a GenericConcept would make TSCG's own quality control a TSCG instance.
- *RequisiteVarietyDuo* (Ashby, human/AI duo, paused) is close to this subject: a
  tempting test bench, and precisely where the reflexive trap would close. Keep the two
  apart, or link them knowingly (D15).

---

## 5. Q5 — Prerequisites

| # | prerequisite | blocking? | why |
|---|---|---|---|
| P1 | Q2 decisions (doctrine wording) | **blocks L1** (M3), not the opening | M3 is edited first; M2/M0 wording follows it |
| P2 | the 9 malformed `m0:epistemicGap` objects | no | once deprecated, deletion is a legitimate repair (debt-honesty: delete). Their inner bare keys go too, so D1 / G8 fall — each fall explained |
| P3 | M0 namespace backlog (C02 = 22 instances, WS-10) | **blocks an automated M0 edit**, not L0–L3 | in misbound files `m0:epistemicGap` is not the `M0_Common` term (it shows as G8); the counter must match both forms, or the M0 lot rides the WS-10 batches (as WS-13 L5 does) |
| P4 | baselines (gate, reasoner sweep) | no — measured today (§0) | re-measure at the start of each lot |
| P5 | debt instrument | **blocks any deprecation** | without it, deprecating M0 while M3/M2 still assert δ₁ is debt moved out of sight (the reason patches 0001/0002 are suspended). Design: reuse C16 (deprecated set read from the owning file, never hardcoded), extended to every layer and to the δ₁ symbol in string literals of M3/M2 (precedent: the FRB tensor gauge of `tscg_metrics.py`) |
| P6 | FAIL or WARN for that check | needs D7 | see the facts below |

**Facts for P6** (section E; `check_m0` statuses at HEAD: 25 FAIL, 18 PASS). 14 of the 18
PASS instances carry `m0:epistemicGap` or `m0:spectralClass` on their `owl:Ontology` node.
`status_summary()` makes an instance WARN as soon as one check is WARN, and the gate
counts `warnings` = instances in WARN status. So:
- **FAIL**: M0 `errors` +14 or more, PASS 18 → 4 (precedent: the retired `m2:changelog`,
  D5, counted as an error);
- **WARN**: M0 `warnings` 0 → 14, PASS 18 → 4 as well.
Neither keeps those instances green; the HandOver's expectation that WARN would is not
what the checker does at HEAD.

---

## 6. Q6 — Proposed lot breakdown (foundation first, Scenario 4)

Each lot ends with `GATE: PASS`, the reasoner on every changed ontology file (sweep for
M0), and a written reason for every counter move.

| lot | content | expected counter moves | reasoner |
|---|---|---|---|
| **L0** | register the worksite; build the instrument (P5) with negative tests; freeze it | the new counter goes **up** (revealed debt) | none (tooling only) |
| **L1** | M3 doctrine per Q2-1…Q2-9 (5 files, changelog each) | D1 −4 or more (the inner keys of the deleted blocks go too), G8 −2, G6 −1 (deletions); instrument down | 5 files |
| **L2** | M2: delete `m2:epistemicGapFormula`; delete or deprecate `m2:hasEpistemicGap` (D8); reword Modelisation and header; `M1_Optics` `m1:epistemicGap`; SHAPE 11 decision | G8 −1 at least | M2, M1_Optics |
| **L3** | M0 vocabulary: `owl:deprecated` on `m0:epistemicGap`, `m0:spectralClass`, `m0:SpectralClass` + 4 individuals (+ focal family if D3); M0 SHACL messages; check_m0 C16 | C16 appears (FAIL or WARN, D7) | `M0_Common` + sweep |
| **L4** | M0 instances: delete the values (incl. the 9 objects, typed literals, local twins), riding the WS-10 batches (P3); regenerate the gallery | C16 → 0; C10/C11/D1/G8 fall by deletion | sweep |
| **L5** | producers: skills, sim template, PocletMiner prompt, PocletGenerator, `modernize_m0.py` | none (outside the gate) | none |
| **L6** | narrative: CoreHypotheses, Debt Overview, instance READMEs, UserGuide samples | none | none |
| **L7** | option (c): open a separate design worksite for the validation-heuristics loop; not a prerequisite of L1–L6 unless D13 says so | per design | per design |
| **L8** | remove the deprecated terms from `M0_Common` once the counter is 0 | instrument retired | `M0_Common` + sweep |

Historical material (`docs/papers/`, old Smart Prompts, `ontology/Ref/`) is not an
authority (root `CLAUDE.md`) and is left as written unless Michel decides otherwise (D11).

---

## 7. Decisions for Michel (answer in one batch)

- **D1** — Worksite id and priority. `WS-14` is free in `worksite.yaml` but was the draft
  name of WS-13 (renumbered 2026-10-11); `WS-15` avoids the confusion.
- **D2** — *Answered 2026-11-15*: the scalar measure and the gap itself have no meaning
  (positions 1–2). The evidence of §1–§2 stays as the written record.
- **D3** — Scope: δ₁ + spectral classes only, or also the focal family (`m0:focalBias`,
  `m0:focalScore`, `m0:FocalClass`, "δ₂"), which reuses the same subtraction?
- **D4** — Wording of each Q2 row, now under the constraint "Korzybski only, no gap";
  in particular Q2-5 (AlignmentLoop criterion), Q2-7 (benchmark slot), and whether
  "Φ is never a perfect isomorphism" (Q2-4, Q2-11) is Korzybski or the gap in disguise.
- **D5** — *Direction given 2026-11-15*: (a) for the removal, (c) as the replacement to
  invent. To confirm: (b) kept only as a recording format for (c)?
- **D6** — If (b) is kept as the recording format of (c): (b1) EARL/PROV declared in the apex, or (b2) a TSCG concept through the
  candidate filter?
- **D7** — C16 (and the cross-layer counter): FAIL or WARN (facts in §5)?
- **D8** — `m2:hasEpistemicGap` (0 uses): delete outright or deprecate first? SHAPE 11:
  keep as a guard (and extend it to `m1:epistemicGap`) or retire?
- **D9** — Does the M0 instance lot ride the WS-10 batches?
- **D10** — Suspended patches 0001/0002: discard, keeping only the C16 design for L3?
- **D11** — Leave historical material untouched?
- **D12** — RequisiteVarietyDuo: resume now with the gap step simply skipped, or wait for
  L5 (skill edit)?

---

- **D13** — Sequencing: run the removal (L0–L6) first and design (c) afterwards, or
  design (c) first so that the pipeline step and the AlignmentLoop criterion are
  replaced in the same move?
- **D14** — Odin's Wisdom / Stereopsis: what grounds the metaphor once "depth from
  disparity" is withdrawn (Q2-12)? The Gs algebra does not need it; the naming rationale
  in the Debt Overview and in `docs/CoreHypotheses/` does.
- **D15** — RequisiteVarietyDuo and (c): kept apart, or used as the test bench of the
  loop, knowing the reflexive trap?

## 8. Go / no-go (recommendation)

**GO for opening the worksite, with two conditions**: no deprecation before the
instrument (L0) exists, and no M3 edit before D4.

Why go: no M3 axiom depends on the number (§2); every live consumer either degrades
cleanly or is a producer that can be edited (§3); and the measure is already
inconsistent at HEAD (six formulas, unreachable range, M3 contradicting its own
formula, stored classes and values that the thresholds and means do not give).
Keeping δ₁ is itself debt. (0.2.0: with the concept withdrawn too, the case for
removal is stronger; the condition on M3 now reads "no M3 edit before D4 and D14".) What can go wrong is mostly the order of work: deprecating
at M0 first would hide the debt that M3 still asserts.

---

## Sources

- EARL 1.0 Schema, W3C Working Group Note — https://www.w3.org/TR/earl/
- Data Quality Vocabulary, W3C Working Group Note 2016-12-15 — https://www.w3.org/TR/2016/NOTE-vocab-dqv-20161215/
- PROV-O, W3C Recommendation 2013-04-30 — https://www.w3.org/TR/prov-o/

## Changelog

| version | date | change |
|---|---|---|
| 0.2.0 | 2026-11-15 | Michel's positions recorded (scalar and gap meaningless; Korzybski a foundation; validation heuristics in a human/machine cybernetic loop to invent). §2 recast as "Korzybski only"; Q2-5, Q2-12 and verdict revised; §4 (a) removes concept and measure, (b) reduced to a recording format, (c) = heuristics loop with design inputs; L7 re-scoped; D2 answered, D4/D5 narrowed, D13–D15 added. |
| 0.1.0 | 2026-11-15 | Draft: Phase 0 + Phase 1 feasibility study at `5a26560`. |
