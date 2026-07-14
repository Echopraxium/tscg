# TSCG — Session Handover

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-07-03
**Purpose**: resume this work in a fresh conversation without re-deriving the design.
**Language note**: files in English, conversation in French.

---

## 0. The one item still open

**`D-order` (Decision 4/4 of the Domain-fusion Phase 0) is NOT yet confirmed.**
Proposed etiological order (see §4): **duplicate → SHACL → script → data → grave.**
Confirm this first thing next session, then execution can begin.

The other three §9 decisions ARE confirmed:
- **D-compartment-home**: compartments live in `M1_Domains.jsonld` (Option A).
- **D-namespaceSegment**: domain instance `m1:extension:Biology` (no subdivision);
  concepts `m1:extension:biology:CellularCommunication` (lowercase `biology:`
  subdivision). `extension` is the SEGMENT; `biology` is a subdivision inside it.
- **D-appliesToDomains-name**: `m2:appliesToDomains`.

---

## 1. Delivered this session (all in outputs, validated on copies)

**M3 layer — DONE, CONFORMS: True:**
- `M3_Schema.shacl.ttl` + `M3_Schema_README.md` — M3 SHACL grammar, 13 shapes, 189 triples (8 Part-A families + 3 Part-B).
- 5 cleaned M3 files: `M3_GenesisGrammar.jsonld` (+ sealed `m3:ModelSupersession`), `M3_EagleEye`, `M3_SphinxEye`, `M3_BicephalousPerspective`, `M3_GrammarFoundation`. Fixes: absolute `m3:`/`m2:` prefixes, `owl:imports` `@id`-coerced, `@base` aligned, `layerOrder`→`layerIndex` (M3=3…M0=0).
- `m3:ModelSupersession` sealed (D1–D6): flat enum `supersessionRelation` {refutation, boundingByMorphism, boundingByImpossibility, vindication}, `relationDefeasibility` {revisable, settled}, `arbitrationMode` = externally_established, `layerIndex` 0. D6 = light reuse of `m3:morphismType` (no `Cat_Models`).

**M1 layer — partial:**
- `M1_CoreConcepts.jsonld` — added two GenericConceptCombos, clean (0 new violations):
  - `m1:Milestone = Fm2(Identity, Trajectory)` → expanded `St × It × A × D × F | V + E`
  - `m1:EpistemicMorphism = Fm2(Modelisation, Transformation)` → expanded `St × It × D × F | R + V + E`
- `M1_ModelSupersession.jsonld` + README — **created but now SUPERSEDED**: it still has the old `fromParadigm/toParadigm` + poles design. Needs the refonte in §3.

**Tooling:**
- `tscg-generate-Mn-grammars_SKILL_corrected.md` v1.2.0 — GenesisSpace→GenesisGrammar, refreshed ontologyType list (+ModelSupersession), monoidal-type vocabulary, owl:imports coercion rule. (Michel to copy into skills source.)

**The big pending proposal:**
- `M2_DomainFusion_ChangeRequest.md` — the Phase 0 for the Domain/KnowledgeField fusion (see §4).

---

## 2. Locked design — the ModelSupersession instance model

The first seed is `M0_MolecularBiologyDogmaShift.jsonld` (central dogma DNA→protein, `boundingByMorphism`). Design settled over many turns:

- **One `Paradigm`, not two.** A paradigm's evolution is an **ordered sequence of `Milestone`** (a table), not a `from/to` pair of distinct objects. The central dogma is ONE paradigm crossing a milestone (one-way flow → bidirectional flow).
- **`Milestone`** = `Fm2(Identity, Trajectory)` — generic, in M1_CoreConcepts (DONE). An identity at an ordered point of its trajectory.
- **`ModelSupersession`** carries `m1:fromStateOfTheArt` / `m1:toStateOfTheArt` — two properties whose **range is `Milestone`** (two milestones of the sequence, the prior and new state of the art). NOT range Paradigm.
- **Poles `_^`/`_$` ABANDONED** — decorative: order is carried by the sequence position, a pole would just re-encode it.
- **Paradigm formulas are Map|Stereopsis (Gm|Gs), not Territory.** A paradigm is a *map/model*, not a territory. The morphism's flow lives at the ModelSupersession level.
- **CRITICAL grammar rule** (learned late, corrects earlier work): `Fm2(…)` / `Fm1m2(…)` take **named concepts as arguments ONLY** — never monoidal primitives. The monoidal formula (`S × I × F`…) is the **result**, stored in `m1:structuralGrammarFormulaExpanded` (a real, pre-existing property). So `M1_Biology`'s `Fm1m2(Biology, S × I × F)` is a **confirmed bug** (primitive as argument).

---

## 3. Pending graving — `M1_ModelSupersession` refonte

Rewrite the extension to the §2 model:
- `Paradigm` class carries an **ordered sequence of `Milestone`** (evolution).
- `fromStateOfTheArt` / `toStateOfTheArt` (range `Milestone`), replacing fromParadigm/toParadigm.
- keep `survivingInvariant` (distinguishes bounding from refutation), `anomaly`.
- **remove all pole traces** (`_^`/`_$`).
- **import `M1_CoreConcepts`** (to reference `Milestone` and `EpistemicMorphism`).
- Then: `M1_Domains` entry for the ModelSupersession domain (transversal) → the M0 instance.

---

## 4. The Domain-fusion Phase 0 (must run BEFORE §3, per D-order)

Full detail in `M2_DomainFusion_ChangeRequest.md`. Summary:

**Root cause**: `Domain` (registry, `m1:domain:*`) and `KnowledgeField` (extension, `m2:KnowledgeField`) are the same referent modeled twice — both phantom classes with instances. This is why the M1 SHACL SHAPE 3 requires a phantom `m2:knowledgeField` property.

**Resolution (decided)**:
- Define **`m2:Domain`** as a real class in M2 (attributes: label, comment, definition, subdomains, relatedDomains, extensionFile, `m1:namespaceSegment`; NO `role`).
- Instances live in `M1_Domains` as `m1:extension:<Name>` (e.g. `m1:extension:Biology`).
- Rename `m2:KnowledgeFieldConceptCombo` → **`m2:DomainConceptCombo`**.
- New property **`m2:appliesToDomains`** (range `m2:Domain`, minCount 1, NO maxCount — multi-domain right, e.g. biochemistry). Values = array of `@id` like `{"@id":"m1:extension:Biology"}`.
- Deprecate `m2:KnowledgeField` + phantom `m2:knowledgeField`.
- **Compartments** = instances of existing **`m2:Segmentation`** (no new class): `m1:compartment:CoreConcepts`, `m1:compartment:extension`, both in `M1_Domains`.

**Etiological execution order (D-order, to confirm):**
1. Resolve the duplicate (define m2:Domain, rename, appliesToDomains, compartments, deprecate).
2. Fix M1 SHACL grammar: SHAPE 3 → require `m2:appliesToDomains` (real); SHAPE 7 → exclude `m1:CorePattern` (ends the SHAPE7↔SHAPE8 contradiction); + CompartmentShape.
3. Harden `check_M1.py`: check IRI-resolution (not just key presence), and/or run SHACL by default.
4. Fix data THROUGH the repaired validators: re-type 21 domains → `m2:Domain`; remove extension field-instances (Option A); correct `Fm1m2` misuses; add `appliesToDomains`; add `owl:imports M1_Domains` to extensions.
5. Resume graving (§3): M1_ModelSupersession refonte → M1_Domains entry → M0 instance.

---

## 5. Key findings / gotchas

- **M1_CoreConcepts has 17 SHACL violations, but they are NOT what they seem**: 12 = `rdfs:subClassOf` as string-literal not IRI (fix = ONE `@context` line `"rdfs:subClassOf":{"@type":"@id"}` → drops to 5); 1 = `m3:` prefix ABSENT from M1_CoreConcepts `@context` (so `m3:ontologyType` unresolved; also header wrongly typed `m3:DomainExtension`, should be CoreConcepts); 2 = SHACL BUG (SHAPE 3 requires phantom `m2:knowledgeField`); 2 = SHACL CONTRADICTION (CorePatterns MultipolarNetwork/CyclicTension have raw formulas allowed by SHAPE 8 but rejected by SHAPE 7).
- **Why defects slipped through**: `check_M1.py` is lenient (tests key presence, not IRI resolution), SHACL is optional (`--shacl` flag), the SHACL itself has bugs, and the two validators contradict each other. → the whole point of the "validation first" repair order.
- `m1:structuralGrammarFormulaExpanded` IS a real property (Cascade has it) — my Milestone/EpistemicMorphism use it correctly.
- `m2:Segmentation` exists (family Structural) and uses proper `@id` subClassOf — the model for compartments.

---

## 6. Conventions (apply to every generated .jsonld)

1. `dcterms:creator` = "Echopraxium with the collaboration of Claude AI".
2. Files in English; conversation in French.
3. URI root = `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology` (source writes `ttps` — read `https`).
4. `m2:changelog`: keep the 3 most recent entries max — **EXCEPT M3 files, which allow up to 7** (rollback safety on the foundational layer; documented in the M3 SHACL shape message so 7 is not read as a violation).
5. `@base` + short IRIs. M1 extensions referenced in M0 as `M1_extensions/extension_name/M1_ExtensionName.jsonld`.
   Note: `M3_GenesisSpace.jsonld` in the convention text is a DEAD vestige — the real file is `M3_GenesisGrammar.jsonld`.

---

## 7. Scope reminder

Everything was produced on COPIES in outputs; `/mnt/project/` is read-only. Michel must run his own formal gates (linter, Pellet reasoner, `cli-tools/`, re-validation) and his semantic Phase-4 sign-off before committing — especially for the M2-foundation Domain fusion (Scenario 2, HIGH risk).

---

## 8. First actions next session

1. Confirm **D-order** (§0).
2. Approve `M2_DomainFusion_ChangeRequest.md` §2–§7 (or adjust).
3. Execute step 1 (Domain fusion) on copies → validate → continue down the etiological order.
