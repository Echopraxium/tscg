# TSCG — Worksite Map (Master Index)

**Version**: 2.2.1
**Date**: 2026-07-30
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Supersedes**: v2.1.0 (2026-07-24). Folds in (a) SC-2 completion — committed and
pushed to origin/main per handover 2026-07-25, HEAD-confirmed 2026-07-30
(M2_GenericConcepts 16.19.0); and (b) the SC-3 design decision (this session),
recorded in `SC-3_Facet_Decision_Record.md` v1.0.0.

**Authority reminder**: the only authority for corpus state is `git show HEAD:<file>`.
SC-2 and SC-3 lines were re-measured at HEAD 2026-07-30 (M0_Common 1.1.0,
M2_GenericConcepts 16.19.0, M3_GenesisGrammar 4.5.0); all OTHER status figures remain
at their 2026-07-24 measurement and are NOT refreshed here — re-measure before acting.
Where this map cites a *decision*, that decision is frozen and marked as such. A frozen
decision is not evidence that the work shipped.

**What this merge did**: v1.0.0 held the frozen design decisions, the conventions
block, the dependency graph and the KnowledgeField inventory. The interim WS-n draft
added the addressing scheme but, written without the old map in context, dropped all
of that and mis-allocated SC-4/SC-5/SC-8. This version restores the 2026-07-11
content, keeps the WS-n scheme, corrects the allocations against HEAD, and records
where declared-July status no longer matches measured-HEAD.

---

## 0. HOW TO USE THIS DOCUMENT

The worksite is a tree. Mitigation is procedural: open one sub-item per session,
anchored on repo files at HEAD and confirmed by Michel, each spec doc handing over
to the next. This map is the durable index — first file to read when resuming.

Rule reconfirmed every session: reasoning across several branches at once, from
memory, produces errors. One anchored branch at a time does not.

---

## 1. ADDRESSING SCHEME

```
WS-n / <sub-item> / <step>
```

| level | meaning | example |
|---|---|---|
| WS-n | worksite with its own README | WS-0 |
| sub-item | the taxonomy that worksite already uses | SC-2, CTX-4, VOC family A |
| step | numbered step inside the sub-item | step 3 |

Two rules that make the scheme survive:

1. **WS-n is a stable identity, allocated in opening order, NEVER reassigned.**
   Priority is a field (§2), not the number. Renumbering by priority would falsify
   every document citing WS-3.
2. **Existing sub-item taxonomies are NOT renumbered.** SC-n occurs 83 times across
   21 files at HEAD, mostly in changelogs (history). WS-n is a container above them.

Families in service, all preserved: SC-n (83), VOC (25), SHAPE n (23), D1..D11 (14),
CTX-n (13), FRB (11), NOT-1, DUP-n.

**Known instability to repair (DEBT)**: SC-5 already denotes TWO referents in the
corpus — a 2026-07-11 comment in `M1_Schema_shacl.ttl` ties it to the Domain fusion,
while that file's v1.2.0/v1.3.0 changelog ties it to SHACL hardening. Same
identifier, two meanings, fifteen lines apart — the instability rule 1 forbids,
already realised. Disambiguation is a backlog item (§8).

---

## 2. PRIORITY (mutable — reorder freely, never renumber)

| rank | item | why now |
|---:|---|---|
| ✅ | WS-0 / SC-2 | COMPLETE — committed, pushed origin/main (M2 16.19.0); gauge 43->0; verified 2026-07-30 |
| 1 | WS-5 / Validator | every item below needs the same measurement primitives; building it first makes them cheap and reproducible. Reinforced by SC-3: its graving is a wide semantic migration, hand-adjudicated without the engine |
| 2 | WS-2 / CTX-4 | prerequisite for SHACL enforcement above M1; cheap, net-negative |
| 4 | WS-0 / SC-6 | DCC006=127 monoidal-operator-in-signature (the bulk); heavy, semantic |
| 5 | WS-1 / VOC | blocks the M2 graph grammar (SC-11b) |
| 6 | WS-3 / Gs review | register opened; Michel's decisions, no deadline |
| 7 | WS-4 / GrammarSignature | scoped; four open decisions, none blocking |
| 8 | WS-0 / SC-10 (M3 grammar) | prerequisites MET; plumbing, not arbitration |
| 9 | WS-0 / SC-3 | **DESIGN DECIDED 2026-07-30** (Decision Record 1.0.0); NOT graved — graving recommended AFTER WS-5 (wide ontologyType migration) |
| 9 | WS-0 / SC-4, SC-5, SC-7, SC-8 | design frozen 2026-07-11; NOT graved (§4) |
| 10 | WS-6 / Changelog | unblocked since m3:changelog exists |
| 11 | WS-7 / M3 F-axiom, WS-8 / Until Further Notice | deferred / continuous |

---

## 3. FROZEN DECISIONS (2026-07-11 — do not re-litigate)

Decisions, not shipped states. Several remain un-graved at HEAD (§4).

### 3.1 Functional grammar model — root result (graved as SC-1)

`Fm2`/`Fm1m2` are **functions**, not functors: essence is combination WITH emergence
("combinés, pas associés"), non-compositional; a functor must preserve composition.
*functor* is reserved for M0 evaluation `F_x : System -> Score`.

```
Fm2   : GenericConcept²⁺           -> GenericConceptCombo   (subset of GenericConcept)
Fm1m2 : Domain⁺ , GenericConcept⁺  -> DomainConceptCombo    (subset of GenericConceptCombo)
```

> **Correction to the 2026-07-11 wording**: that map wrote the target as
> `ConceptCombo`. SC-1 retired that name for `GenericConceptCombo` (0 occurrences of
> bare `ConceptCombo` at HEAD). Reintroducing `ConceptCombo` as an abstract genus is
> an OPEN WS-4 proposal, not a revival of the old name.

- **`Fm1` does NOT exist.** Multi-domain conjunction rides juxtaposed domain
  arguments: `Fm1m2(Biology, Chemistry, NamedConcept)`.
- **A combo's formula IS its function signature.** No monoidal expansion of a combo.
  Monoidal formulas (`× / + / |`) are reserved for ATOMS.
- **Arguments comma-juxtaposed**, never joined by a grammar operator.
- **`⊗⇒` is tensor-era residue** — purged from the foundation by SC-1; rest by SC-9.

### 3.2 Primitive notation & monoid qualification (graved as SC-2)

- ASFID A,S,F,I,D. REVOI R,E,V,O,Im. Stereopsis T,K,Ss,L.
- Four two-letter primitives are DISTINCT: `St` Structure/Gt, `Ss` Symbol/Gs,
  `It` Information/Gt, `Im` Interoperability/Gm.
- **Rule**: S and I are ALWAYS monoid-subscripted in every **monoidal formula**;
  A/F/D stay bare. Monoidal formulas only.
- `×` reserved to Gt, never overloaded.

> **Vocabulary note (2026-07-24)**: the 2026-07-11 map said "atom formula", which
> collides with M3's generator sense of "atomic". SC-2 replaced it by "monoidal
> formula" in `M3_BicephalousPerspective` 1.5.1 and `tscg_metrics.py` 1.1.0.

### 3.3 Facet as an M3 principle (SC-3 — DESIGN DECIDED 2026-07-30, NOT graved)

**Full record**: `SC-3_Facet_Decision_Record.md` v1.0.0. This section is the summary;
the record is authoritative. It **supersedes §5 only** of
`_01_Facet_as_M3_Principle_ArchitectureNote.md` v0.1.0 (the rest of that note stands).

- **A1 adopted**: `m3:Facet` = orthogonal axis, `m3:Focus` = value (Ranganathan).
- **SC-3 = LIFT, not invent**: `m0:Facet` + `m0:hasFacet` already exist at HEAD
  (multi-valued); `m3:Facet`/`m3:Focus` absent. The work remounts the M0 mechanism.
- **Conferred/Derived sub-typing RETRACTED** (was the old §3.3 line). It contradicts
  the HEAD `m0:Facet` doctrine — facets are conferred, Map-perspective roles, DISTINCT
  from `m0:ScoringProperty`/`m0:FocalProperty`. So `spectralClass`/`focalClass`/
  `hasDominantM3` are NOT facets; they stay outside. No `StateFacet` (population 1).
- **`ontologyType` was overloaded → decomposed** into orthogonal axes (names → WS-4):
  - **SCALE** (new, mandatory 1): Poclet · CaseStudy · RealWorldSystem
  - **NATURE** (new, mandatory 1, default *SystemModel*): SystemModel · Framework ·
    Grammar · Tool  *(do NOT name the default just "Model": every M0 is a model)*
  - **AUDIENCE** (recast from Democratization; `minCount 1`, no max): KitArchitect ·
    KitCrafter · KitUser — derived from the Kit mission; orthogonal to meta-level
    (proven: Explorer M0→Architect vs FireTriangle M0→User)
  - **DOMAIN** (existing, coupled to SC-5, multi): "transdisciplinary" = ≥2 domain foci
- **A1 debt discharged**: the axis of which `Democratization` is a focus is now named —
  AUDIENCE (Democratization = AUDIENCE:KitUser).
- **Rejected axes** (record §3): Perimeter (derived from Domain≥2), Objective
  (=Audience/Nature), Map/Territory triad (level confusion + grammars-not-facets),
  UserRole (classifies persons), KitTester (activity, not audience).
- Boundary (NOT facets, unchanged): raw scores, grammar primitives, compositional
  relations.
- **Open at graving** (record §7-8): OWL 2 punning check on Pellet; SHACL admission
  contract (§3 criteria — likely a WS-5 executable check, not frozen M3 SHACL); the
  layer-role residue (Genesis/GenericConcepts/DomainExtension, likely redundant with
  meta-level); DOMAIN axis typed WITH SC-5, not in SC-3.
- **`hasPolarity`** (old §3.3 item) — NOT re-examined this session; if it is a facet it
  is a further conferred axis, still free string at HEAD. Carry to the graving session.

### 3.4 Families as contracts (SC-4 — NOT graved at HEAD)

- 9 family signatures OVERLAP → mono-classification approximate; **`hasFamily`
  multi-valued.** Contract model (declare + verify), not hand tag. Cardinality
  per-facet: `ontologyType` single, `domain`/`hasFamily` multi.
- **Open**: combos have no formula → derive family from parents; mechanism unresolved.

---

## 4. SUB-WORKSITE REGISTER — WS-0 (Structural Cleanup)

Status measured at HEAD 2026-07-24; where it differs from 2026-07-11, both shown.

| id | title | 2026-07-11 said | HEAD 2026-07-24 |
|---|---|---|---|
| SC-0 | commit 2026-07-03 staging | pending | staged, uncommitted |
| SC-1 | functional grammar (root) | ready to grave | graved, pushed; 2 KnowledgeFieldConceptCombo residual |
| SC-2 | monoid-qualification (atoms) | specified | ✅ COMPLETE — 16.19.0 committed + pushed; gauge NOT-1 43->0; verified HEAD 2026-07-30 |
| SC-3 | facet M3 principle | note drafted | **DESIGN DECIDED 2026-07-30** — 4-axis model (SCALE/NATURE/AUDIENCE/DOMAIN); A1 adopted; Conferred/Derived retracted. Decision Record 1.0.0. NOT graved |
| SC-4 | families-as-contracts + multi | scoped | NOT graved |
| SC-5 | domain-fusion Phase 0 | change-request exists | NOT done (KnowledgeField* alive, 82 occ, 10 spellings) |
| SC-6 | M1 conformance (named args) | scoped | DCC006=127 (bulk); M1 total errors 151 at HEAD golden (was 163; EXP001=12 retired) |
| SC-7 | ModelSupersession | model locked | NOT graved; staged in SC-0 |
| SC-8 | FeedbackLoop reclassification | README exists | NOT done (FeedbackLoop still M2, formula not a signature) |
| SC-9 | ⊗/⊗⇒ purge | 39 files | live ⊗ 89; \otimes 7 (TeX, FRB-blind); Hilbert 13 |
| SC-10 | M3 grammar | — (new 2026-07-24) | prerequisites MET |
| SC-11 | M2 grammar | — (new 2026-07-24) | 11a doc ready; 11b blocked by WS-1 |

### SC-2 — COMPLETE (historical detail retained)

All 5 steps done; committed and pushed origin/main per handover 2026-07-25
(M2_GenericConcepts 16.19.0, M3_BicephalousPerspective 1.5.1, tscg_metrics.py 1.1.0).
The step table below is kept as the record of what shipped.

| step | content | status |
|---|---|---|
| 1 | convention in M3_BicephalousPerspective 1.5.0 (->1.5.1) | done |
| 2 | typeSymbol S->St, I->It in M3_EagleEye 2.10.0 | done |
| 3 | SHACL shape forbidding bare S/I in monoidal formulas | produced this session |
| 4 | migrate formula values | produced this session |
| 5 | M2_GenericConcepts_README — Notation Convention, Takeaways, Statistics | done |

Decisions: D1 76-mechanical (9 -> WS-3); D2 CTX-4 isolated lot; D3 shape at
`cli-tools/check-M2/M2_MonoidalFormula_Schema_shacl.ttl`; D4 run via
`tscg_metrics --shacl-path` (interim -> WS-5 runner); D5 Symmetry/State mechanical
only; D6 Gradient migrate I, `or` -> WS-3. formulaTeX + m2:expressionTeX deleted.
"atom" -> "monoidal".

This session's lots (in outputs/, PENDING gates + HEAD re-verification):
- **Lot A** M2_GenericConcepts 16.18.1 — CTX-4 + CTX-1, unresolved predicates
  174->0, triples 2345 unchanged. Commit ISOLATED, first.
- **Lot B** same 16.19.0 — 76 migrations (58 Gt, 18 Gm), 4 TeX fields deleted
  (triples ->2343), 9 carve-outs to WS-3; M2_MonoidalFormula_Schema_shacl.ttl 0.1.0;
  M3_BicephalousPerspective 1.5.1; tscg_metrics.py 1.1.0. NOT-1 43->0, SHACL 45->0.
- Confirms old-map SC-2: Balance `A × S × F | _0` -> `A × St × F | _0` DONE; open
  question "does typeSymbol move S->St?" RESOLVED YES (step 2).

### SC-5 — Domain-fusion Phase 0 (HIGH risk, from 2026-07-11)

**Not a rename — a duplicate resolution.** `Domain` (registry) and `KnowledgeField`
(extension) are the same referent modelled twice; hence M1 SHACL requires a phantom
`m2:knowledgeField`. Sequence: repair SHACL first, define `m2:Domain` as a real
class, create `m2:appliesToDomains` (SC-3 domain facet), deprecate `m2:KnowledgeField`
+ phantom, retype 21 domains, `owl:imports M1_Domains`. **Never
`sed s/KnowledgeField/Domain/`** — corrupts the SC-1 combo rename simultaneously.

HEAD spellings (82 occ): KnowledgeField 42, KnowledgeFieldConceptCombo 19,
KnowledgeFieldGenericCombo 8, KnowledgeFieldConcepts 3, KnowledgeFieldConcept 3,
InstanceShape 2, GenericCombos 2, KnowledgeFields 1, Shape 1, MetaCombo 1.

### SC-10 — M3 grammar (new)

Prerequisites MET: 5 M3 files absolute-prefixed, 0 unresolved predicates.
`run_all_layers.py` records an M3_Schema.shacl.ttl (2026-07-03, CONFORMS:True,
13 shapes) NEVER wired into a script. Work = plumbing. Cautions: predates
SC-1/SC-2/SC-5 (re-check assertions); a July CONFORMS:True is exactly the claim to
retest (SHAPE 9 lesson).

### SC-11 — M2 grammar (new), two planes

| step | plane | tool | blocked by |
|---|---|---|---|
| 11a | document | JSON Schema | WS-5 engine only — NOT WS-1 |
| 11b | graph | SHACL | WS-1 (VOC) |

11a sees all 3480 pairs incl. 1695 bare; expect a blunt first result, route via a
tolerated whitelist + decline gauge. 11b: only 1785 pairs reach the graph — VOC
first. Both grammars **generated from the term registry** (194 M2 predicates + bare
keys, an order past M1's 11 shapes; hand-writing = a second source of truth).

---

## 5. OTHER WORKSITES (WS-1 … WS-8)

- **WS-1 VOC** — bare keys 4281 occ / 1301 distinct; 693 family-A, 303 false friends,
  853 undefined-but-prefixed. Blocks SC-11b.
- **WS-2 CTX** — CTX-1 fixed this session (single occurrence, gauge 1->0, Lot A).
  CTX-4 21 (10 M1 extensions + this file). CTX-5 31.
- **WS-3 Gs review** — M2_Formulas_Review_with_Gs_Residues.md 1.0.0: pre-Gs cohort
  46/75 recorded before SC-2 erases the marker; 9 carve-outs; isomer classes;
  Gradient `or` debt.
- **WS-4 GrammarSignature** — TSCG_GrammarSignature_Worksite_README.md 1.0.0:
  has-particle collision, 231-key blast radius, five naming criteria, four open
  decisions.
- **WS-5 Validator** — Python engine + Electron interface; JSON contract; headless
  rule; decision-capture not reporting; engine-first scope guard; reflexive M0
  status. Report configuration by QUERY is the stated core. **Existing asset**:
  `cli-tools/README.md` v1.0.0 already documents `tscg_paths.py` (relocatable root),
  the acceptance-gate philosophy (exact reference values, not pass/fail), the four
  silent SC-1 tooling bugs, and names `check-M2/`/`check-M3/` as the intended home
  for future checkers — where SC-2's shape already sits. The engine grows from here,
  not from scratch. Known gap to close: the SHACL pass is hard-wired to `check-M1`
  (line 305) and ignores `--shacl-path`; a runner for an arbitrary shape file is
  job one.
- **WS-6 Changelog** — canonical @graph[ontology].metadata.changelog; m3:changelog
  exists; lot 2 = 17 m2: + 3 m1: + 4 bare; metadata undeclared.
- **WS-7 M3 F-axiom** — F_CategoryTheoryNote scalar residue; preprint §1.5.7 stale.
- **WS-8 Until Further Notice** — continuous, docs/CoreHypotheses/.

---

## 6. CONVENTIONS (from 2026-07-11 §5, preserved and extended)

1. dcterms:creator = "Echopraxium with the collaboration of Claude AI".
2. Files in English; conversation in French.
3. Ontology URI root
   `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` via @base.
   **Prefix values in @context must be ABSOLUTE** (CTX-4 lesson): a relative mN
   prefix resolves in identifier position but not predicate position, silently
   blinding SHACL.
4. changelog: 3 most recent — EXCEPT M3 files, up to 7 (rollback safety; 7 is not a
   violation).
5. M1 extensions referenced in M0 as
   `M1_extensions/extension_name/M1_ExtensionName.jsonld`.
6. No tensor residue: no ⊗, no ⊗⇒, no \otimes. ×=Gt, +=Gm, |=Gs.
7. Surgical str_replace; validate JSON + SHACL (CONFORMS:True) before graving;
   `git show HEAD:<file>` before any edit; never trust snapshots.
8. A gauge reading 0 is a claim, and claims get tested (three detector bugs caught
   this way in two sessions). Every gauge needs a fixture proving it can be non-zero.

**Rename ownership (substring trap)**: KnowledgeFieldConceptCombo ->
DomainConceptCombo = SC-1; every other KnowledgeField* -> Domain = SC-5; never
`sed s/KnowledgeField/Domain/`.

---

## 7. DEPENDENCY GRAPH

```
SC-1 (root, graved)
 ├─→ SC-2 ─→ SC-4                      (SC-2 in flight)
 ├─→ SC-3 ─┬→ SC-4
 │         └→ SC-5 ─┬→ SC-6
 │                  └→ SC-7
 ├─→ SC-5 (also needs DomainConceptCombo from SC-1)
 ├─→ SC-8
 └─→ SC-9 (needs SC-1/SC-2 notation rules)
SC-0 (orthogonal; SC-7 also needs SC-0's staged combos)

WS-5 (validator) ── enables ──> SC-10, SC-11a, cheap re-measurement of all above
WS-1 (VOC) ─────── blocks ────> SC-11b
SC-10 (M3 grammar): no blockers, prerequisites met
```

**Recommended order**: ~~SC-2~~ (done) -> WS-5 engine -> CTX-4 lot -> SC-6 -> SC-10 ->
VOC/SC-11 -> SC-3 GRAVING (design done; grave after WS-5) -> SC-4 -> SC-5 -> SC-7.
SC-0 and SC-9 at Michel's convenience.

---

## 8. CROSS-CUTTING BACKLOG (not a worksite)

- **Stale "163" in golden note** — `golden_values.json` reads errors=151 (measured
  2026-07-23) but its prose `note` still says "163 check_M1 errors". The 12 EXP001
  (retired D8) were removed by SC-6-partial between 07-13 and 07-23; the drop is
  legitimate and recorded. Update the note string to 151. Display only, not a
  measurement bug — and NOT the `publicID=` bug earlier suspected.
- **SC-5 identifier collision** (§1) — two referents in M1_Schema_shacl.ttl.
  Disambiguate (SC-5a Domain-fusion / SC-5b SHACL-hardening) or pick one canonical.
  First real test of the WS-n stability rule.
- **README <-> jsonld drift, 5 M3 files** (2026-07-23); rule
  README.version == jsonld.owl:versionInfo.
- M3_GrammarFoundation declares @vocab = owl#; changelog 2.3.0 typo
  DomainConceptCombo -> DomainConceptCombo.
- ontology/docs/ holds 80+ .md incl. duplicates and predecessor worksite dirs
  (_00_Worksite_00_SC1-9, _01_Worksite_01, _02_Worksite_02). Curation + possible
  rename to WS-n (cited in no jsonld/ttl, so cheap).
- **FRB blind spot**: counts literal ⊗ only, not \otimes (7 occ, all in TeX fields
  SC-2 deletes). (x) is a false alarm outside M1_Geology.
- **diagnosis-pipeline skill**: Scenario 1 rates renaming Risk:Low ~15min — true of
  execution, false of evaluation. Add Phase 0.5 (name candidacy). WS-4 §8.
- **δ₁ provenance**: ~17 scalar m0:epistemicGap (snapshot-measured), only 2 with a
  provenance marker; precision exceeds provenance; SpectralClass derives from them;
  MultisubjectiveScoreEvaluationProtocol exists but was not followed. Needs a
  provenance field, not better numbers. (HEAD path of M0 poclets not located this
  session.)
- **Layered-architectures poclet** (candidate): m3:SystemicFramework instance
  generalising MOF/OSI/Marr/TriskeleToolchain/Semantic-Web/TSCG; taxonomy of layer
  relations. NOT StructuralGrammar/LayerCake (loaded names). Future.
- **Case divergence, local disk vs versioned (Windows `core.ignorecase`)** — several
  instance dirs/files differ in case between the working tree and what is committed:
  `Kidneys`↔`kidneys`, `Vsm`↔`vsm`, `Raas`↔`raas`, `Tpack`↔`tpack`,
  `Yggdrasil`↔`yggdrasil`, `Iching`↔`iching`, `M0_Vco`↔`M0_VCO`, `M1_Music`↔`M1_music`.
  Invisible on a case-insensitive FS; surfaces at any clone on a case-sensitive FS
  (Linux/CI) and made ~31 raw-GitHub URLs 404 (raw is case-sensitive). Fixed at source
  by generating URL lists from `git ls-files` (repo case, gitignore-respecting) rather
  than an `os.walk` of local disk — see `create_files_URIS.py`. Disk realignment (fresh
  `git clone`) deferred until a multi-platform need arises. Repo case itself is
  sometimes mixed (e.g. `raas/M0_RAAS.jsonld` + `M0_raas_README.md`) — full
  normalisation is a separate small worksite.

---

## 9. NEXT ACTION

SC-2 shipped; SC-3 design decided (Decision Record 1.0.0, this session). Open ONE next
worksite in a FRESH conversation anchored on HEAD:

- **WS-5 (Validator engine)** — recommended. Structural; unblocks cheap per-decision
  measurement for everything below, including the wide SC-3 graving.
- **WS-2 / CTX-4** — cheaper alternative if a short, safe, net-negative lot is wanted
  (~19 occ, mostly mechanical across M1 extensions).

Do NOT start the SC-3 GRAVING before WS-5: it is a wide ontologyType migration across
M3/M2/M0 and would be hand-adjudicated without the engine (as SC-3's design was).

---

## CHANGELOG

- **2.2.1** (2026-07-30) — Backlog (§8): recorded the local-vs-versioned **case
  divergence** debt (Windows `core.ignorecase`), its consequence (404 raw URLs, since
  raw GitHub is case-sensitive), the source fix (`git ls-files` in `create_files_URIS.py`),
  and the deferred disk realignment. No worksite state changed.


- **2.2.0** (2026-07-30) — Folded two states the v2.1.0 map predated. (1) **SC-2
  COMPLETE**: priority, register (§4), SC-2 subsection, dependency order (§7) and
  NEXT ACTION (§9) updated from "in flight" to shipped (16.19.0, pushed; HEAD-verified
  2026-07-30). (2) **SC-3 DESIGN DECIDED**: §3.3 rewritten to the four-axis model
  (SCALE/NATURE/AUDIENCE/DOMAIN), A1 adopted, Conferred/Derived sub-typing RETRACTED
  (contradicts HEAD m0:Facet doctrine), ontologyType decomposition, AUDIENCE derived
  from the Kit mission, rejected axes and open-at-graving items recorded; points to
  `SC-3_Facet_Decision_Record.md` v1.0.0, which supersedes §5 of the architecture note.
  SC-3 detached from the frozen-design group in §2/§4 and marked NOT graved, to grave
  after WS-5. Only SC-2/SC-3 lines re-measured; all other figures untouched.
- **2.1.0** (2026-07-24) — Reconciled against the on-disk WS-0 content read late in
  the session (`_01_Facet_as_M3_Principle_ArchitectureNote.md`, `cli-tools/README.md`).
  Four corrections: (1) SC-6 line now carries the real golden ventilation
  (DCC006=127; M1 total 151, was 163, EXP001=12 retired) instead of the stale
  "114/155"; (2) SC-3 marked partial — D11 is RULED (option+axis+enum = facet),
  A1 recommended, only `hasPolarity` un-graved; (3) WS-5 entry records that
  `cli-tools/README.md` v1.0.0 already documents the tooling and reserves
  check-M2/check-M3; (4) backlog gains the stale-"163"-note item and confirms it is
  a display string, not the `publicID=` bug. HEAD golden_values.json (2026-07-23)
  cited as authority for the counts.
- **2.0.0** (2026-07-24) — Merge of v1.0.0 (2026-07-11) and the interim WS-n draft.
  Restored 2026-07-11 frozen decisions (§3), conventions (§6), dependency graph (§7)
  and KnowledgeField inventory that the interim draft dropped. Corrected the interim
  mis-allocation: SC-4 = families, SC-5 = Domain-fusion, SC-8 = FeedbackLoop.
  Recorded the SC-5 identifier collision as backlog. Reconciled declared-July vs
  measured-HEAD status per SC. Added SC-10 (M3 grammar) and SC-11 (M2 grammar) at the
  end of the sequence, not into SC-4/SC-8. Folded in this session's SC-2 lots,
  WS-3/WS-4/WS-5 scoping, and the δ₁ and layered-architectures findings.
- 1.2.0 (2026-07-24, interim, superseded) — WS-n scheme, WS-5 raise, validator
  architecture. Written without the 2026-07-11 map in context.
- 1.0.0 (2026-07-11) — original master index; frozen design decisions.
