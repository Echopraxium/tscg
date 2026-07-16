# TSCG — Session Handover (2026-07-16)

**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Context**: resumption of a saturated conversation; SC-1 finalised, pushed, and
reinjected into "TSCG Cyclop v0". This session opened SC-2/SC-3 and a new
positioning worksite.
**Authority reminder (golden rule)**: `/mnt/project/` and the Cyclop snapshot are
**NOT** authorities — the only authority is `git show HEAD:<file>` (verified live
this session). Conventions: English files, French conversation, `@base` short IRIs,
base URI `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`,
changelog 3 entries (M3: up to 7), no `⊗`/`⊗⇒` (× = Gt, + = Gm, | = Gs).

---

## 0. Deliverables produced this session (reinject into Cyclop v0)

1. **`M1_Schema_shacl.ttl` v1.2.0** — SHACL grammar, Fix B graved (see §1).
   Repo home: `ontology/cli-tools/check-M1/M1_Schema_shacl.ttl`.
2. **`Until_Further_Notice_WorksiteEntry.md`** — positioning worksite entry
   (see §4). Intended home: `docs/CoreHypotheses/` (as an entry, not yet a sealed note).

Both validated/parsed. Michel applies his formal gates before commit.

---

## 1. GRAVED — SHACL SHAPE 2↔3 noise fix (Fix B)

**Problem**: in a **merged-corpus** pyshacl run (M1 + M2 loaded together, so the
axiom `m2:DomainConceptCombo rdfs:subClassOf m2:GenericConceptCombo` is present),
`sh:targetClass m2:GenericConceptCombo` follows the subclass and SHAPE 2
double-validates every extension combo (which is a `DomainConceptCombo`), inflicting
~3 spurious violations each. This is ~256 of the 502 measured violations — pure
validator noise, not data defects.

**Key discovery**: `check_M1.py` validates **file-by-file** with
`validate(..., inference="none")` and `advanced` defaulting to **False**, loading
only the single M1 file (no M2). In that per-file mode the subclass axiom is absent,
so SHAPE 2 never targets extension combos — **check_M1's own SHACL sub-check never
had the bug**. The ~256 noise comes from a *merged* run (likely `run_all_layers` or
an ad-hoc full-corpus pyshacl). Fix the grammar → that merged run becomes readable.

**Fix A (SPARQL target) was REJECTED**: `sh:SPARQLTarget` requires `advanced=True`,
which the runner does not pass → the target would be silently ignored → SHAPE 2 would
validate nothing → worse debt. Do not use unless the runner is also patched to
`advanced=True` (bigger blast radius across all 10 shapes).

**Fix B (applied)**: wrap SHAPE 2's constraints in `sh:or` with an escape branch
`[ sh:class m2:DomainConceptCombo ]`. A DomainConceptCombo satisfies the escape
branch → SHAPE 2 passes vacuously (SHAPE 3 validates it). A genuine
(non-domain) GenericConceptCombo fails the escape branch → the real contract applies.
Pure core SHACL — works under `advanced=False, inference="none"`.

**Proven empirically** (isolated data + the real corrected file):
- `OpticalSensor` (extension combo): 0 violations — noise gone.
- `BrokenGeneric` (genuine bad formula): still fully caught — and crucially by
  **SHAPE 9** (the DCC006/DCC008 ComboFormulaShape) with its **specific** messages
  intact. Fix B's only cost (a lumped SHAPE 2 message) is nearly moot because SHAPE 9
  already reports formula defects precisely.

**PENDING**: Michel confirms the count drop on his real merged-corpus run
(502 → ~246) before commit. Bump already applied (1.1.0 → 1.2.0 + header note).

**Left untouched (correctly)**: SHAPE 3's mandatory `m2:knowledgeField` is the known
SC-5 phantom (annotated in the file header as intentional). One stale comment in
SHAPE 3 ("→ m2:KnowledgeFieldConceptCombo" while the code correctly uses
`m2:DomainConceptCombo`) — cosmetic, leave to SC-5.

---

## 2. DECIDED, not yet graved — SC-2 (monoid qualification of atoms)

**Rule locked**: subscript **only on collision** — `S` and `I` are the sole letters
shared across two monoids:
- `S`: Structure (Gt) vs Symbol (Gs) → **St / Ss**
- `I`: Information (Gt) vs Interoperability (Gm) → **It / Im**

All other letters are **bare** (no collision): `A, F, D` (Gt), `R, E, V, O` (Gm),
`T, K, L` (Gs). Poles `_^ _$ _0` are not types → bare. This restores Worksite Map
§1.2 ("A/F/D stay bare", "O needs no index") — an earlier over-generalisation
(subscript everything → `At/Ft/Dt/Om…`) was **wrong and retracted**. Corollary:
`Ft` is malformed — F has no rival, so it is written bare `F`.

Michel's intent verbatim: *"aucune ambiguïté concernant les types monoïdaux… donc
systématiquement indicés par le monoïde… y compris quand la formule n'utilise que
les types d'un seul monoïde"* — but scoped to the collision pair only after we
re-derived it together.

**Ready-to-grave deliverables** (execution order): `notation_disambiguation`
convention in `M3_BicephalousPerspective` (M3 changelog up to 7) → `typeSymbol` in
`M3_EagleEye` moves `S→St`, `I→It` **at the source** (else EagleEye says "S" while
formulas say "St") → `FormulaShape` SHACL forbidding bare `S`/`I` in **atom**
formulas only → normalise the small atom perimeter → fix `Balance`
(`A × S × F | _0` → `A × St × F | _0`; A and F stay bare).

**Reminder**: primitives and monoidal operators live **only in atom formulas**,
never in `Fm2`/`Fm1m2` signatures (arguments are named concepts). So the St/It rule
never touches signatures — the two rules do not cross.

---

## 3. IN PROGRESS — SC-3 (Facet as an M3 principle)

**Ranganathan** (S.R. Ranganathan, *Colon Classification* 1933 — NOT Ramanujan).
Facet = the **axis** (the classifying question); Focus = a **value** on that axis.

**Decision A confirmed = A1**: `m3:Facet` denotes the **axis**; `m3:Focus` the value.
Consequence: `m0:facet.Democratization` (currently a *value* typed `m0:Facet`) is
re-typed `m3:Focus`; the axis it belongs to becomes the `m3:Facet`. This is what makes
multi-valued `appliesToDomains` expressible (a concept carries several foci on the
domain axis, e.g. biochemistry = {Biology, Chemistry}).

**Still open (for Michel)**:
- Boundary §3 (NOT facets: raw scores, grammar primitives ASFID/REVOI/TKSL,
  compositional relations) — confirm as the anti-overfitting dike.
- **D11** — a qualitative guard "option" (`trajectoryShape=Circular`, 2 occurrences,
  1 axis) is *below* the TSCG admission threshold. Claude's lean: **keep it out in v1**
  (admitting it re-creates a Domain/KnowledgeField-style duplicate one storey up).
- **Decision B** — `scoringStatus`: fold into Conferred (it's workflow state, not a
  classification). Claude's lean: fold.
- **v1 scope** — start with the conferred core (`ontologyType`, `domain`,
  `hasFamily`, `roleGrounding`, `hasFacet`); derived (`spectralClass`, `focalClass`,
  `hasDominantM3`) in v2.
- **`hasPolarity`** — admitting it as a facet forces `xsd:string` → controlled
  enumeration; do in v1 only if freezing the enum now.

---

## 4. NEW WORKSITE (positioning, NOT an SC) — "Until Further Notice"

Filed as a **separate worksite** in `docs/CoreHypotheses/` (guardrail corpus), not
the SC tree (SC = ontology engineering; this = epistemological positioning).
Full entry delivered: `Until_Further_Notice_WorksiteEntry.md`. Core points:

- **Thesis**: a framework whose axiom is "the Map is never the Territory" cannot place
  its value in a *final state* (that would be Narcissus). Its value is the
  **disciplined process of revision** (Lakatos: progressive vs degenerating programme).
- **Opening metaphor — the good specialised map**: same territory → hydrologist /
  wind-farm / GSM / rail maps; none less true; quality = fitness-for-audience, not
  correspondence. Two honesties: **perimeter** (declare who it serves *and, by
  complementarity, who it does not*) and **revision** (accurate *until further
  notice*). Guard: declaring an audience never excuses mediocrity *for* that audience.
- **Declared audience (Michel, core of the note)**: NOT the general public, NOT
  systems scientists, NOT single-domain experts — but the **intimidated intermediate
  fringe** (engineers/artists/researchers drawn to systemic thinking yet put off by
  its "elitist" aura). Offer = *"a toolkit to explore a systemic approach to your
  project"*; output = *"a structured lay-out of your understanding, fed by a
  level-appropriate state of the art"* — **NOT a predictive model**. This is the
  `roleGrounding`/Democratization facet stated as the project's mission, and the
  built-in answer to Risk 2 (a non-predictive tool cannot be accused of false
  prediction).
- **Debt-vs-overfitting razor** (from EpistemicResidue): technical debt = an
  *attested* residue the Map recognises but hasn't processed (reducible; the remedy
  is work); overfitting = a Map claiming to absorb a *non-attested* residue (the frog
  swelling). Razor: *an addition is good if it reduces an attested residue, overfitting
  if it claims to reduce a non-attested one.* Supplies the stopping criterion for
  Risk 1. Sibling of FitnessRazor — admission test (irreducible? distinct?) to run
  **externally** before sealing.
- **TSCG as a ModelSupersession meta-instance of itself**: SDAP → v16.x is a real
  `Milestone` trajectory, each step bounding the last. Open whether to grave it.
- **Guard (must be first line)**: "value is in the process" must never excuse shipping
  nothing falsifiable; each Milestone must offer a graspable, breakable handle.

**Two adjacent positioning notes also considered this session** (candidates, not
written): *Domain-algebra — considered and rejected* (the CDU rationale: composition
of orthogonal axes, refusal to reify combinations; a monoid on a facet is a type
error) and *TSCG vs faceted documentary classification* ("from assigned place to
verified contract" — family = `implements`-style contract, niche = intersection of
satisfied contracts, transdisciplinary primitives vs discipline-siloed axes).

---

## 5. CLARIFIED — SC-7 (ModelSupersession)

- `docs/CoreHypotheses/` = a directory of **epistemic guardrails**, not loose theory.
- **ModelSupersession is a TYPE** (12th `ontologyType`), not a doc to write.
  `AttestedEpistemicMorphism.md` is its **guardrail note** — the filename froze one of
  the undecided working names; the sealed type is `m3:ModelSupersession`.
- **Verified on git HEAD: NOTHING is published.** `M3_GenesisGrammar` has 0
  occurrences of ModelSupersession; `M1_ModelSupersession.jsonld`,
  `M0_MolecularBiologyDogmaShift`, and the ModelSupersession CoreHypotheses notes are
  all 404. The entire substrate lives in the **2026-07-03 staging zip = SC-0,
  uncommitted**. SC-7 depends on SC-0 (staging) and SC-5 (Domain fusion).
- The "model locked" predates SC-1: on reopen, re-verify the staged M1 extension
  (old design `fromParadigm`/`toParadigm` + poles → refonte to Milestone-based
  `fromStateOfTheArt`/`toStateOfTheArt`) against SC-1/SC-2 (functions, DomainConceptCombo,
  Fm2 ≥2, collision subscripts).
- Type sealed status mismatch to reconcile: M3 (staging) sealed vs note marked
  "not yet sealed".

---

## 6. FINDING — M1 extension READMEs (Michel's opening point, verified on repo)

Both missing **and** desynchronised:
- **Present but pre-reform (v1.0.0)**: economics, education, electronics, mythology,
  physics — all still carry `⊗`, `KnowledgeField*`, `M3_GenesisSpace`, "tensor
  product", "Genesis Space (ASFID ⊗ REVOI)". None know `Fm1m2`/`DomainConceptCombo`.
  → **rewrite**, not patch (they predate the whole ⊗→×/+/| migration and SC-1).
- **Missing (dir confirmed via .jsonld 200)**: biology, chemistry, energy_generators,
  geology, music, optics, photography, systemic_modeling.
- The `.jsonld` themselves are up to date (DomainConceptCombo + Fm1m2; hard rename
  clean; the one residual `KnowledgeFieldConceptCombo` per file = a legitimate
  changelog line). Naming anomaly: `M1_music.jsonld` (lowercase) vs `M1_Biology.jsonld`.
- The existing TO_DO entry treats all 13 as "to create" — it should be corrected to
  8 "create" + 5 "rewrite". Candidate for its own worksite (depends on SC-1/SC-9
  notation).

---

## 7. STALENESS CORRECTIONS (repo is authority)

- **Fm2 arity = ≥2** (`GenericConcept²⁺`), confirmed by Michel and by the graved
  changelog. Worksite Map §1.1 and SC-1 Handover §1 still say `⁺` (≥1) — stale, fix on
  reopen. Output type `GenericConceptCombo` kept (D1 resolved: not renamed to
  ConceptCombo). DomainConceptCombo is now defined by its `Fm1m2` formula (hybrid ≥1
  Domain + ≥1 GenericConcept), superseding the "distinct epistemological parents"
  criterion.
- **SC-6 backlog = 163** (measured), not 126 (a false partial reconstruction).
- **SC-5 = 502** SHACL violations (not 479); ~256 = the SHAPE 2↔3 validator bug (§1).
- **`check_M1.py` bugs still open**: (1) `publicID=` — IRIs forged under the Windows
  path `E:\…` instead of `@base`, so M1 IRIs don't match M2/M3's; may inflate the 163
  (UNVERIFIED — the count is suspect until fixed). (2) dies on stdout redirect (cp1252)
  → add `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- The `.ttl` (declarative) and `check_M1.py` (imperative) grammars have **diverged**
  (163 vs 502); part is the SHAPE 2↔3 bug (pyshacl-only). Flag, not a task.

---

## 8. NEXT ACTIONS (recommended order)

1. Michel confirms Fix B count drop on the real merged run → commit v1.2.0.
2. **SC-2** (decided; ready to grave — see §2). Then `check_M1.py` `publicID=` fix to
   de-suspect the 163.
3. **SC-3** graving once §3 open points are settled.
4. Correct the TO_DO: M1 README entry (8 create / 5 rewrite); Worksite Map §1.1
   (`⁺`→`²⁺`); add the `Until_Further_Notice` line under a "CoreHypotheses / positioning"
   rubric (separate from the SC list). Suggested TO_DO line is in the entry's §9.
5. Positioning notes (`Until_Further_Notice`, domain-algebra rejected, TSCG-vs-classification)
   when Michel wants — pull sibling notes from git HEAD first, run the irreducibility
   test, do not seal by decree (avoid autarkic validation — ICC).
6. SC-7 stays blocked behind SC-0 + SC-5.

Worksite order unchanged: SC-1✓ → SC-2 → SC-8 → SC-9 → SC-3 → SC-4 → SC-5 → SC-7 → SC-6.
