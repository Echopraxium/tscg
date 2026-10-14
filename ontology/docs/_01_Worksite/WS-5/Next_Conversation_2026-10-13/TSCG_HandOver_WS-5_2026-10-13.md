# TSCG HandOver — WS-5, 2026-10-13: SC-5b review in progress (11/28 lines), SC-5c domain model drafted

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-13
**Follows**: `../Next_Conversation_2026-10-12/TSCG_HandOver_WS-5_2026-10-12.md`
(working method, push path, lots queued after SC-5b).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts) is **session state at handover time**: re-verify against HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — SC-5b writes M1 classes.
3. Then read from HEAD:
   - `ontology/docs/_01_Worksite/WS-5/SC-5b/SC-5b_Subdomains_Decision_Table.xlsx` — the
     line-by-line decision table (sheet 1: 128 strings; sheet 2: 22 strings on 6 physics
     combos; sheet 3: questions Q1–Q13 with Michel's answers).
   - `ontology/docs/_01_Worksite/WS-5/SC-5b/SC-5c_DomainModel_DesignNote.md` — the domain
     model agreed in conversation (DRAFT, nothing implemented).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of `4386b8b` (HandOver 2026-10-12).
  Ontologies unchanged since `e9beb47` (Lot SC-5). Gate `GATE: PASS` with the 2026-10-12
  counts (M1 17 / 133 / 1 / 296).
- **Measured on HEAD `4386b8b`**: `m1:subdomains` = 139 strings on 22 domain classes
  (128 unique) **+ 22 strings on 6 physics combos** (LatentHeat, TriplePoint, CriticalPoint,
  OrderParameter, PhaseDiagram, Nucleation — ⊑ `m2:DomainConceptCombo`, not domains).

## 2. Decisions taken 2026-10-12/13 (Michel) — detail in the table and the design note

- **Q10 adopted**: a subdomain class is created only if an M0 instance (or M1 concept) cites
  it today → 26 KEEP + 2 RELINK (Blockchain ⊑ ComputerScience, Optics ⊑ Physics) instead of
  77 KEEP. The other strings are dropped (kept in the table and git history).
- **Three relations** (design note §3): `rdfs:subClassOf` = *is a kind of* (n parents
  allowed, never a parent already implied transitively); `m1:requires` (new) = *relies on*;
  `m1:hybridOf` (new) = *exists only through the crossing* (Biomimetics), used judiciously.
- **Scope** = computed view Root / Branch / Hybrid, never stored.
- **Facets** (SC-3 mechanism): `AbstractionLevel` = Theory / Application / Practice (one);
  `ModelPurpose` (renamed from `Model`, 2026-10-13) = Pragmatic / Descriptive / Explanatory / Predictive (cumulative). Empirical
  sciences → Theory. Blocker: `m3:hasFacetValue` is an ObjectProperty → needs an annotation
  variant (M3 change).
- **Contracts** (2026-10-13, design note §7.6): `m1:DomainContract` ⊑ `m2:ConceptContract`,
  subclasses DomainTool / DomainMethod / DomainExpertise / DomainModel; `m1:requires`
  targets a domain or a provider of a DomainContract (e.g. 3DPrinter ⊑ DomainTool,
  m1:domain FabricationProcess). Supersedes the `m1:Tool` idea.
- **Pattern**: *X Theory ⊑ X, requires its formal tools* (MusicTheory ⊑ Music; Poker Theory
  ⊑ Poker requires Game Theory, Probability). Game Theory ⊑ Mathematics.
- **New domain classes**: Mathematics, Game, Card Game, Collectible Card Game (replaces
  "Trading Card Games"), Finance (Root — to confirm), ElectronicMusic (⊑ Music, requires
  Electronics). Photography is **not** ⊑ Optics (Photography requires Optics).
- **Genres** (Jazz, Rock…) are not domains → M1 concept taxonomy in the music extension.
- **Split**: SC-5b = classes + `subClassOf` only, then delete `m1:subdomains`. `requires`,
  `hybridOf`, facets, Scope view = **SC-5c**. `requires` values are noted in the table
  (column "requires → (SC-5c, noted only)").

## 2b. Update 2026-10-14 01:50 — review of the 28 lines COMPLETE

All KEEP/RELINK lines decided (table column "Michel: decision"); see design note §9–§11:
OpenAlex adopted as reference (Q14, `skos:closeMatch` added in SC-5b); new parents Vision
Science, Condensed Matter Physics, plus Mathematics, Game, Card Game, ElectronicMusic;
Pharmacology Root. **Evaluation criterion** (design note §0): internal coherence (gate) +
usefulness as a toolkit; shortcuts legitimate but flagged; usefulness test on 3 instances
before SC-5c. **Step 1 below is done**; resume at step 3 (combos sheet), step 4 (open
questions), then step 5 (implementation).

## 3. Next goal — finish the SC-5b review, then implement

1. **Review the 17 remaining lines** (column "Michel: decision" empty), block by block,
   looking only at `subClassOf`; note `requires` in passing:
   - Block 3 Biology: Developmental Biology, Cell Biology, Physiology, Endocrinology
     (⊑ Physiology), Pharmacology (⊑ Biology + Chemistry).
   - Block 4 Physics / Chemistry: Thermodynamics, Semiconductor Physics, Geophysics
     (⊑ Geology + Physics), Optics (RELINK ⊑ Physics), Image Formation, Color Science.
   - Block 5 Electronics / Education / Mythology: Signal Processing, Analog Electronics,
     Circuit Theory, Instructional Design, Educational Technology, Comparative Mythology.
2. Open from block 2: **Decision Theory** parent (⊑ Mathematics proposed, not yet
   confirmed); its `requires` (Game Theory, Probability) and `relatedDomains` (Politics,
   Project Management, not Philosophy). Note: Bayesian networks / Markov decision processes
   are models, not domains — `requires` targets should be domains (or a separate link to
   concepts, SC-5c).
3. **Sheet 2** (combos): delete `m1:subdomains` on the 6 combos; keep application fields as
   `relatedDomains` or drop — Michel decides per combo.
4. Sheet 3 still open: Q2 (SystemsTheory vs SystemicModeling), Q4 (rename `Strategic`,
   `Financial`, `Geological`), Q6 (IRI rule), Q7 (labels only now, definitions later).
5. **Then implement SC-5b** (diagnosis pipeline): baseline gate → create classes (label +
   `rdfs:subClassOf` IRIs) and relinks → delete `m1:subdomains` (domains + combos) → update
   registry README / Debt Overview → gate (expected: M1 unchanged unless a new class lacks a
   label, SHAPE 5/11) → patches `1_…`.

## 3b. Decided 2026-10-13 evening (design note §8)

- Property `m1:domain` → **`m1:belongsToDomain`** (apply in lot M0, + 8 M1 files and the
  M0 template). Class `m1:Domain` unchanged.
- `m2:implements`: `rdfs:domain` → `owl:Class`; per-layer extension point (SC-5c).
- Facet `Model` renamed **`ModelPurpose`**; 4th contract **`m1:DomainModel`**.
- Still open from the contract model: settle (1) generic contract + `m1:belongsToDomain` on
  the provider, (3) DomainExpertise = practical skills only, mixin applied or not.
- SC-5b also cleans `optics:Optics_Domain` (string `m1:domain`).

## 3c. Decided 2026-10-14 evening (design note §12)

- No stored subdomain lists at any layer: delete `m1:subdomains`, `m1:extension:physics:subdomains`
  (SC-5b) and `m0:subdomains`, `m0.vco:subdomains` (lot M0). Same requires/belongsToDomain
  rule for M0 as for M1.

## 3d. Closed 2026-10-14 23:45 (design note §12–§13)

- Combos sheet closed: delete `m1:extension:physics:subdomains`; the six combos stay in Physics.
- Q2, Q4, Q6, Q7 closed. **Preparation of SC-5b is complete → next: implement SC-5b.**
- New lot **NS-SEP** right after SC-5b: one prefix per defining file (`m1.domains:`, `m1.physics:`…).

## 4. Unchanged from 2026-10-12

Lot M0 (domain IRIs in 41 M0 files, after SC-5b), Protocol, Part (a) M2, engine
`advanced=False`, KnowledgeField leftovers, lot R2, etc. — see the 2026-10-12 HandOver §3–§5.

## 5. Outside git

- Project Knowledge: reload `TSCG_ReferenceCorpus_Bootstrap.md` (pending since 2026-10-12)
  and `TSCG_FileTree.md` once this commit is in (new folder `WS-5/SC-5b/`).
