# TSCG — Worksite Map (Master Index)

**Version**: 1.0.0
**Date**: 2026-07-11
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Purpose**: freeze the decisions locked in the 2026-07-11 session and index the
active sub-worksites (SC-*) so that **exactly one** is opened per conversation,
each with its own spec doc, without any single context having to hold the whole
tree.

---

## 0. How to use this document

The worksite branched into a tree during design. The mitigation is procedural,
not heroic: **open one sub-worksite (SC-n) per session**, anchored on the repo
files and confirmed by Michel, and let each SC's spec doc hand over to the next.
This map is the durable index; it is the first file to read when resuming.

Rule of thumb learned this session: reasoning across several branches at once,
from memory, produces errors. Reasoning one anchored branch at a time does not.
This map exists to enforce that discipline.

---

## 1. Locked decisions (frozen 2026-07-11 — do not re-litigate)

### 1.1 Functional grammar model (the root result)

`Fm2` and `Fm1m2` are **functions** (n-ary emergence operations), **not
functors**. Rationale: their essence is *combination with emergence*
("combinés, pas associés"), which is non-compositional; a functor must preserve
composition, so an emergence operation is non-functorial. The term *functor* is
also already reserved in the foundation for M0 dimension evaluation
`F_x : System → Score`.

```
Fm2   : GenericConcept⁺                → ConceptCombo         (⊆ GenericConcept)
Fm1m2 : Domain⁺ , GenericConcept⁺      → DomainConceptCombo   (⊆ GenericConcept)
```

- **`Fm1` does NOT exist.** No reification of composite domains. Multi-domain
  conjunction (biochemistry) is carried by **juxtaposed domain arguments** in
  the `Fm1m2` domain slot: `Fm1m2(Biology, Chemistry, NamedConcept)`. Reifying
  `Fm1` was rejected as decorative complexity.
- **A combo's "formula" IS the function signature** — `Fm2(Process, Alignment)`,
  `Fm1m2(Biology, Chemistry, C)`. There is **no monoidal expansion** of a combo,
  ever, and nothing to "develop bout-à-bout" (the arguments are combined, not
  associated). This is why M1 needs no expanded form.
- **Monoidal formulas (`× / + / |`) are reserved for ATOMS** (primitive types and
  their assemblies), e.g. `Process = D × F`.
- **Free recursion**: any argument satisfying `IsA GenericConcept` is valid —
  atomic concepts, `ConceptCombo`, and `DomainConceptCombo` alike. No special
  cases.
- **Rename** `KnowledgeFieldConceptCombo → DomainConceptCombo` (already planned).
- **Function arguments are juxtaposed by comma, never joined by a grammar
  operator.** `×/+/|` appear only *inside* an atom's formula, never between the
  inputs of `Fm1m2`/`Fm2`.
- **`⊗⇒` is Hilbert/tensor-era residue** (like `⊗`) and must be purged from the
  foundation docs. `Fm2`/`Fm1m2` are the named function forms; there is no
  operator symbol between their arguments.

### 1.2 Primitive notation & monoid qualification

- Canonical ASFID (M3_EagleEye): **A, S, F, I, D**. Canonical REVOI: R, E, V, O,
  Im. Stereopsis (TKSL): T, K, Ss, L, poles.
- These four two-letter symbols are **distinct primitives** (already defined in
  M3_BicephalousPerspective), not variants of one letter:
  - `St` = **Structure** / Territory (Gt)
  - `Ss` = **Symbol** / Stereopsis (Gs)
  - `It` = **Information** / Territory (Gt)
  - `Im` = **Interoperability** / Map (Gm)
- **Rule change (decided)**: `S` and `I` are **always monoid-subscripted in every
  atom formula** (`St`/`Ss`, `It`/`Im`), removing the previous context-dependent
  rule ("unindexed in pure-Territory, indexed in hybrid"). `A/F/D` stay bare (no
  collision). This applies to **atoms only** (combos have no monoidal formula).
- `×` is reserved to the **Gt** monoid and never overloaded (not for function
  signatures, not for domain conjunction).

### 1.3 Facet as an M3 principle

Spec already drafted: `Facet_as_M3_Principle_ArchitectureNote.md`.

- **A facet is an orthogonal classification axis with a controlled value-set**
  (Ranganathan: facet = axis, focus = value).
- **Realisation = reified descriptor (voie 2)**: `m3:facet.X a m3:Facet ;
  m3:onProperty <property> ; m3:hasFocus (…)`. The facet descriptor *references*
  the classifying property; it is never a property nor a value directly.
- **Sub-types**: `ConferredFacet` / `DerivedFacet` only. **No `StateFacet`**
  (one-member = micro-overfitting); `scoringStatus` is **excluded** (workflow
  state, not a classification of the entity).
- `roleGrounding` is a **qualifier of the Democratization facet**, not an
  autonomous facet.
- `hasPolarity` **is** a facet (was missed); admitting it implies converting it
  from free `xsd:string` to a controlled enumeration.
- Boundary (NOT facets): raw scores, grammar primitives (ASFID/REVOI/TKSL),
  compositional relations (`comboOf`, `hasMorphism`, formulas).

### 1.4 Families as contracts

- The 9 family signatures **overlap** (Regulatory & Teleonomic both High A;
  Informational & Adaptive both High It; Dynamic & Energetic both High D) — so
  mono-classification is approximate. **`hasFamily` should be multi-valued.**
- Model: family membership as an **`implements`-style contract** (declare +
  verify against the family's structural signature), not a hand-assigned tag.
- **Cardinality becomes an explicit per-facet attribute** {single, multi}:
  `ontologyType` = single, `domain`/`hasFamily` = multi.
- **Consequence of §1.1 to resolve in SC-4**: only atoms have monoidal formulas,
  so family-by-formula-contract applies to atoms; **combos derive their family
  from their parent arguments**, not from a formula. This mechanism is open.

---

## 2. Sub-worksites (SC-*)

| ID | Title | Depends on | Risk | Status |
|---|---|---|---|---|
| **SC-0** | Commit the 2026-07-03 staging | — (orthogonal) | low | pending (nothing committed) |
| **SC-1** | Functional grammar model (root) | — | med | **specified, ready to grave** |
| **SC-2** | Monoid-qualification rule (atoms) | SC-1 | low-med | specified |
| **SC-3** | Facet M3 principle | SC-1 | med | note drafted |
| **SC-4** | Families-as-contracts + multi | SC-1, SC-2, SC-3 | med | scoped |
| **SC-5** | Domain-fusion Phase 0 | SC-1, SC-3 | **HIGH** | change-request exists |
| **SC-6** | M1 conformance (named args) | SC-1, SC-5 | high effort | scoped |
| **SC-7** | ModelSupersession | SC-0, SC-5 | med | model locked, graving pending |
| **SC-8** | FeedbackLoop reclassification | SC-1 | low | README exists (2026-07-07) |
| **SC-9** | Global `⊗` / `⊗⇒` purge | SC-1 (notation) | low-med | **newly scoped — 39 files** |

### SC-0 · Commit the 2026-07-03 staging
`/mnt/project/` is **behind** the session zip: it lacks the M3 `ModelSupersession`
sealing, the `Milestone`/`EpistemicMorphism` combos, and the M3 cleanup. Nothing
was committed. Orthogonal to everything else; Michel's timing. Requires his formal
gates (linter, Pellet, SHACL) before commit.

### SC-1 · Functional grammar model  ← **start here**
Grave §1.1. Deliverables: a **foundation note** (proposition), then edits to M2
(`ConceptCombo`/`DomainConceptCombo` as `GenericConcept` subclasses, rename,
formula-as-signature), M3 if needed, and **purge of `⊗⇒` residue** from the
foundation docs. Fully specified this session; lowest risk / highest leverage
because it redimensions SC-2, SC-6, SC-8.

### SC-2 · Monoid-qualification rule (atoms only)
Grave §1.2. Deliverables: update the `notation_disambiguation` convention in
`M3_BicephalousPerspective` (M3 changelog may reach 7 — rollback safety);
`FormulaShape` SHACL forbidding bare `S`/`I` in atom formulas; normalise the
(small) atom perimeter; fix `Balance` (`A × S × F | _0` → `A × St × F | _0`).
**Open**: does `M3_EagleEye` `typeSymbol` move `S→St` / `I→It`, or keep bare with
qualification enforced only in formulas?

### SC-3 · Facet M3 principle
Grave §1.3 from `Facet_as_M3_Principle_ArchitectureNote.md`. Conferred core v1:
`ontologyType`, `hasFamily`, `hasPolarity`, the Democratization axis. Derived
facets (`spectralClass`, `focalClass`, `hasDominantM3`) in v2. Domain facet
(`appliesToDomains`) arrives with SC-5.

### SC-4 · Families-as-contracts + multi-valued `hasFamily`
Audit the atom concepts against provisional family contracts (presence vs
dominance — Michel to calibrate); relax `hasFamily` to multi; `FamilyContractShape`
SHACL. Must resolve how **combos** inherit family from parents (no formula).

### SC-5 · Domain-fusion Phase 0  (HIGH risk — M2 foundation)
From `M2_DomainFusion_ChangeRequest.md`. **This is where ALL remaining
`KnowledgeField` vocabulary is absorbed into `Domain`.**

**Root cause**: `Domain` (registry, `m1:domain:*`) and `KnowledgeField`
(extension, `m2:KnowledgeField`) are the **same referent modelled twice** — both
phantom classes with instances. This is why M1 SHACL SHAPE 3 requires a phantom
`m2:knowledgeField` property (2 of the 17 `M1_CoreConcepts` violations).

**Not a rename — a duplicate resolution.** It cannot be done with `sed`:
define `m2:Domain` as a real M2 class, create `m2:appliesToDomains` (= the domain
facet, multi-valued, from SC-3), deprecate `m2:KnowledgeField` + the phantom
`m2:knowledgeField`, **repair the SHACL first**, then retype the 21 domains,
compartments, `owl:imports M1_Domains`.

**Grounded form inventory** (verified 2026-07-11 — six distinct forms, easy to miss):

| Form | Occurrences | Fate |
|---|---|---|
| `m2:KnowledgeFieldConceptCombo` | 256 | **renamed in SC-1** (not here) |
| `m2:knowledgeField` (property) | 55 | phantom → deprecate, replace by `m2:appliesToDomains` |
| `m2:KnowledgeField` (class) | 12 | phantom → absorbed into `m2:Domain` |
| `KnowledgeFieldConcept` | 4 | to rule on |
| `m1:KnowledgeFieldGenericCombo` | 3 | to rule on |
| `m1:KnowledgeField` | 2 | absorbed |
| `m1:KnowledgeFieldInstanceShape` | 1 | SHACL shape → rename |
| `m1:KnowledgeFieldConceptComboShape` | 1 | SHACL shape → rename (SC-1 target class) |

Heaviest non-combo files: M1_Education (13), M3_GenesisGrammar (11),
M1_Schema_shacl.ttl (11), M2_GenericConcepts (9), M1_Geology (6).

**`D-order` still unconfirmed** (duplicate → SHACL → script → data → grave).
Unblocks the 17 `M1_CoreConcepts` violations.

### SC-6 · M1 conformance (named-argument signatures)
Rewrite `Fm1m2(Domain, …primitives…)` entries into named-argument signatures
`Fm1m2(Domain, NamedConcept, …)`. **Semantic** work (recover the right named M2
concepts), per M1 extension — the heaviest branch, done last or incrementally.
Subsumes the confirmed `M1_Biology` `Fm1m2(Biology, S × I × F)` bug.
*Count of affected entries is UNVERIFIED* (earlier scans were built on a criterion
Michel flagged as my own reading; re-derive against the confirmed §1.1 rule before
trusting any number).

### SC-7 · ModelSupersession
Refonte `M1_ModelSupersession`: `Paradigm` = ordered `Milestone` sequence;
`fromStateOfTheArt`/`toStateOfTheArt` (range `Milestone`); remove poles; import
`M1_CoreConcepts`. Then `M1_Domains` entry, then `M0_MolecularBiologyDogmaShift`.
Model locked in the handover; blocked behind SC-5.

### SC-8 · FeedbackLoop reclassification
From `M2_FeedbackLoop_Reclassification_README.md`. Becomes trivial once SC-1 is
graved: its formula simply **is** `Fm2(Process, Alignment)`. Move M2 →
`M1_CoreConcepts`; purge `⊗` and scalar `k·` residues; Homeostasis re-audit
deferred (domino).

### SC-9 · Global `⊗` / `⊗⇒` purge  (newly scoped)
The operator `⊗` was retired on 2026-07-06, but **39 files still carry it**
(measured 2026-07-11) — this is far larger than assumed and was hiding inside
other sub-worksites.

- **22 M0 instances**: M0_FourStrokeEngine (34), M0_ExposureTriangle (30),
  M0_ComplexChemicalSynapse (26), M0_TrophicPyramid (26), M0_CellSignalingModes
  (25), M0_RGB_Additive (19), M0_NakamotoConsensus (17), M0_AdaptativeImmuneResponse
  (15), M0_ButterflyMetamorphosis (14), M0_Tpack (14), M0_TvTestPattern (13),
  M0_ColorSynthesis (10), + 10 more.
- **5 M3 files**: M3_GrammarFoundation (8), M3_GenesisGrammar (2), M3_EagleEye (1),
  M3_SphinxEye (1).
- **12 docs**: `Structural_Grammar_Foundation.md` (32),
  `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md` (31),
  OntologyModeling_Guidelines (5), TSCG_Smart_Prompt (4), + others.

**`⊗⇒` is the same residue class** (Hilbert/tensor-era "function type
(emergence)") — superseded by the named `Fm2`/`Fm1m2` forms of SC-1. The two
foundation docs above still *define* `⊗⇒`; SC-1 rewrites those two, SC-9 does the
rest.

Mostly mechanical (`⊗` → `×`/`+`/`|` per monoid), but **not blind**: each
occurrence must be mapped to the right monoid operator, so it needs SC-1's
notation rules settled first. Existing asset: the
`tscg-tensor-to-structural-grammar-migration` skill.

---

## 3. Dependency graph (textual)

```
SC-1 (root)
 ├─→ SC-2 ─→ SC-4
 ├─→ SC-3 ─┬→ SC-4
 │         └→ SC-5 ─┬→ SC-6
 │                  └→ SC-7
 ├─→ SC-5 (also needs DomainConceptCombo from SC-1)
 ├─→ SC-8
 └─→ SC-9 (needs SC-1/SC-2 notation rules)
SC-0  (orthogonal; SC-7 also needs SC-0's staged combos)
```

**Recommended order**: SC-1 → SC-2 → SC-8 (quick win) → SC-9 (mechanical, clears
debt) → SC-3 → SC-4 → SC-5 → SC-7 → SC-6. SC-0 at Michel's convenience.

**Rename ownership (avoid collisions — the substring trap):**
- `KnowledgeFieldConceptCombo` → `DomainConceptCombo` = **SC-1**.
- every other `KnowledgeField*` form → absorbed into `Domain` = **SC-5**.
- Never `sed s/KnowledgeField/Domain/` — it would corrupt both at once.

---

## 4. Repo / staging state (2026-07-11)

- `/mnt/project/` = last committed baseline; **does not** contain the 2026-07-03
  session work.
- Session zip = staging (M3 sealing + M1 combos + `M1_ModelSupersession` draft),
  itself **not** carrying the SHACL `@context` fixes nor any SC-1..SC-8 work.
- Nothing from any of this is committed. All generated files live in `outputs`
  on copies; Michel runs his own formal gates before commit.

---

## 5. Conventions (apply to every generated file)

1. `dcterms:creator` = "Echopraxium with the collaboration of Claude AI".
2. Files in English; conversation in French.
3. Ontology URI root: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` (via `@base`; short IRIs).
4. `m2:changelog`: 3 most recent entries — **except M3 files, up to 7** (rollback
   safety on the foundational layer; documented in the M3 SHACL message).
5. M1 extensions referenced in M0 as `M1_extensions/extension_name/M1_ExtensionName.jsonld`.
6. No tensor residue: no `⊗`, no `⊗⇒`. `×`=Gt, `+`=Gm, `|`=Gs.
7. Surgical `str_replace` edits; validate JSON + SHACL (pyshacl CONFORMS:True)
   before graving.

---

## 6. Next action

Open **SC-1** (functional grammar model). First deliverable: the foundation note
(proposition) fixing the two signatures, `Fm1` removal, formula-as-signature, free
recursion, the rename, and the `⊗⇒` purge — before any file edit.
