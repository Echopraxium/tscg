# Core Hypotheses — Suggested Reading Order

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-19
**Location**: `docs/CoreHypotheses/README.md`

The documents in this folder are not independent: several use notions that
another one introduces (the Map–Territory distinction, δ₁, ASFID / REVOI, the
Layer Cake, Ontological Overfitting…). The order below is a **suggestion** — a
path in which each document only assumes what came before it. Every document
remains readable on its own; forward references are signposted.

TSCG is a toolkit with a pedagogical vocation, not a theory of reality. These
documents are positions and hypotheses about that toolkit — open and revisable,
not established results.

---

## 1. What TSCG is — and is not

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 1 | `_00_TSCG_as_StereoscopicGlasses.md` | The vocation: a toolkit for reading systems, theories, models or myths in one structural language | — |
| 2 | `_01_Narcissus_and_Icarus_as_Safeguards.md` | The two failure modes the toolkit guards against: self-flattery (Narcissus) and over-claiming (Icarus) | 1 |

## 2. The architecture — Core Hypotheses 1 to 4

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 3 | `TerritoryMap_Dichotomy.md` (CH1) | Map vs Territory; ASFID / REVOI / Stereopsis; the epistemic gap δ₁ | 1 |
| 4 | `SystemicEsperanto.md` (CH2) | M2 generic concepts as a shared, transdisciplinary vocabulary | 1 |
| 5 | `LegoTechnic_Modularity.md` (CH3) | Composition: building models from reusable pieces | 3, 4 |
| 6 | `LayerCake_Models_The_Kit.md` (CH4) | M3–M1 describe the kit, not the world; M0 is a scale model | 3, 4, 5 |

## 3. The epistemological ground

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 7 | `ContextSwitching.md` | Every paradigm has its turtle: coherence relative to declared criteria; context switching; locked-in-one-context as the pathology; rediscovery over recitation | 3, 6 |

## 4. Measuring and trusting

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 8 | `ScoringSystem.md` | δ₁ (epistemic gap) and δ₂ (focal score) in detail | 3 |
| 9 | `MultisubjectiveScoreEvaluationProtocol.md` | How scores are produced by several evaluators; defeasibility | 8 |
| 10 | `CredibilityAccretion_Process.md` | How credibility grows from converging evaluations | 9, 2 |

## 5. Guard-rails and epistemology

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 11 | `OntologicalOverfitting.md` | The anti-pattern of adding pieces the Territory never asked for | 3, 4 |
| 12 | `The_Epistemic_Residue.md` | The residue a model does not absorb, *before* its verdict; its four fates | 2, 3, 4, 7, 11 |
| 13 | `ModelSupersession.md` | The paradigm shift *after* the verdict, as recorded by the history of culture — a context switch made by a whole community | 6, 7, 9, 10, 12 |

12 and 13 are companions: read them in that order. 7 is the prerequisite of both.
7 and 12 also answer each other: `ContextSwitching.md` uses the notion of residue
(an error is a mismatch of criteria, and every criterion leaves a residue), which
`The_Epistemic_Residue.md` develops; the residue, in turn, is where a switch of
criteria begins. 7 can be read without 12; 12 reads better after 7.

## 6. Exploratory

| # | Document | Introduces | Assumes |
|---|---|---|---|
| 14 | `Archetypes_as_CrossCultural_Artifacts.md` | Jungian archetypes as a source of structural hypotheses | 3, 4, 9, 10 |
| 15 | `EpistemicPivot.md` | One object, many ways in: modes of access and readers' prisms around a fixed object; what is invariant, what each mode loses; where the regress stops. A rediscovery and synthesis of published ideas, no innovation claimed | 3, 4, 7 |

---

## Keeping this file current

When a document is added to this folder, give it a place in this table and list
the documents it assumes. If a new document cannot be placed without reordering,
that is a sign it introduces a notion the others now depend on — say so here.

Numbers are positions in this table, not file names: files are never renamed to follow
the order. Each document is to carry an **`Assumes:`** line in its header, pointing back here
(done so far for `ContextSwitching.md`, `ModelSupersession.md` and `EpistemicPivot.md`).
