# TSCG — Vocabulary Consolidation (VOC worksite) — Scoping Note

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: 0.1.0 (SCOPING — no file edited yet)
**Date**: 2026-07-22
**Status**: capture of the 2026-07-22 architecture discussion, for execution
after Michel's per-block decisions (§5). This is a hand-off, not an edit.
**Authority**: measured against `git show HEAD` (`5dcd8e9`, 2026-07-21). Every
count below must be re-confirmed by the tool on first run.

---

## 0. Problem statement

The corpus uses ~1387 distinct **bare keys** (JSON keys declared in no
`@context`), for **6444 occurrences** across 27 canonical `.jsonld` files. A bare
key is not a badly-named property — it is JSON that never crosses into RDF:

- in the 24 files **without `@vocab`**: the key is **dropped on expansion** — the
  data is *absent* from the graph, not merely mistyped;
- in the 3 files **with `@vocab`**: worse — keys map onto a namespace they do not
  belong to (two M3 files project theirs into `owl#`, minting bogus `owl:role`,
  `owl:status`).

Either way this is **incompatible with reasoner/SHACL validation**: a reasoner
sees an almost-empty ontology where `m2:eagleView` exists but its content
(formula, basis, status) never entered the graph. The whole semantic payload sits
in a JSON shell no reasoner touches. This is δ₁ applied to the files themselves:
the gap between what the file *displays* and what the graph *contains*.

**Terminology decision (2026-07-22)**: the target is a **property**, not a key.
"Key" is the current (defective) JSON state; "property" is the RDF target state.
"Officialising a key" = promoting a key to a declared property. Michel's
preference for "property" is adopted for the target throughout.

---

## 1. The layering rule — "follow the rails"

**Decision (Michel, 2026-07-22)**: vocabularies are **specialised per layer**, and
each property is defined in the M3 file that **owns the boundary it describes** —
following the frontiers/interfaces the corpus already formalises, not a new
partition invented for this worksite.

The rails already exist in the corpus:

| Rail (existing) | Where | Owns |
|---|---|---|
| `m3:layerOrder` (1→4) | `M3_GenesisGrammar` | the 4-layer ordering (Genesis=1, GenericConcepts=2, DomainExtension/SystemicFramework=3, Poclet/CaseStudy=4…) |
| `derived_layers` node ("foundation_of") | `M3_GenesisGrammar` | the M3→M2 generation interface |
| `m3:Morphism` family (`hasMorphism`, `morphismSource/Target`) | `M3_GenesisGrammar` | cross-layer morphisms |
| Territory/Map axis | `M3_BicephalousPerspective` | the Gt/Gm/Gs interface — hosts `role`, `semantics`, `symbol`, `definition`, `examples` |
| apex (transversal) | `M3_GrammarFoundation` | properties crossing all 4 layers (e.g. `m3:changelog`, added 2026-07-22) |

**Placement rule derived from the rails:**

1. **Transversal** (meaningful at every layer) → `M3_GrammarFoundation` (apex).
   Precedent: `m3:changelog` (v2.5.0).
2. **Territory/Map descriptor** (about the Gt/Gm/Gs axis) → `M3_BicephalousPerspective`.
3. **Layer-interface / morphism / ontology-typing** → `M3_GenesisGrammar`.
4. **Specific to one lower layer** (e.g. the `eagleView` sub-fields proper to M2
   GenericConcepts) → that layer's canonical file, prefixed accordingly
   (`m2:` in `M2_GenericConcepts`, `m1:` in the M1 extensions, `m0:` in `M0_Common`).

**Hard constraint (Michel)**: only `m3:`/`m2:`/`m1:`/`m0:` — **no `tscg:`**, and
**never `m2:` used inside an M3 file** (dependency inversion). By symmetry, a
property meaningful only at M2 must NOT be defined in M3 (would pull layer-specific
vocabulary into the foundation — the same defect reversed). This is why the rule is
*specialisation*, not *centralisation*.

---

## 2. Due-diligence: do not reinvent the wheel (verified 2026-07-22)

Before officialising any native property, existing standard vocabularies were
checked **by semantics and typing, not by name**. The check itself proved the point
that name ≠ meaning.

### Family A — replace with an existing standard (confirmed)

| Bare key | occ | Standard property | Verified |
|---|---|---|---|
| `description` | 260 | `dcterms:description` | ✓ |
| `examples` / `example` | 293 | `skos:example` | ✓ (SKOS has 7 note properties incl. example) |
| `name` / `label` | 114 | `rdfs:label` | ✓ |
| `alternative_names` | 44 | `skos:altLabel` | ✓ (synonyms, acronyms, spellings) |
| `comment` | 38 | `rdfs:comment` | ✓ |
| `note` / `rationale` | 48 | `skos:note` (or `skos:scopeNote`) | ✓ |
| `definition` | 19 | `skos:definition` | ✓ |
| `date` | 80 | `dcterms:date` | ✓ |
| `version` | 71 | `owl:versionInfo` | ✓ |

Subtotal replaceable-by-standard: **~1045 occ**. Mechanical once the table is
approved. (`changelog`/`changes` already handled by `m3:changelog`, itself aligned
in-intent with `adms:versionNotes`.)

### False friends — same name, incompatible semantics (REJECT)

| Bare key | Tempting standard | Why it fails |
|---|---|---|
| `status` | `adms:status` | `adms:status` is an `owl:ObjectProperty`, range `skos:Concept`, for **workflow** status (accepted/deprecated/experimental). TSCG `status` is an **epistemic** string ("PROPOSITION"/"VALIDATED"). Incompatible type + meaning. |
| `role` | `prov:hadRole` | `prov:hadRole` is the role of an **agent in an activity** (`prov:Role` via `prov:qualifiedAssociation`). TSCG `role` is the role of a **primitive in a formula**. Foreign ontology. |

⇒ `status` and `role` are **authentically TSCG-native** — established by verification,
not assumed by default. They go to Family B.

---

## 3. Family B — TSCG-native properties (the real work), split in two

A discovery on 2026-07-22 splits B and makes half of it safe/mechanical.

### B1 — already `m3:`-prefixed but DEFINED NOWHERE (declare only)

`M3_BicephalousPerspective` uses **24 `m3:*` keys, 0 of them declared** as
`owl:*Property`. They already resolve to an IRI (unlike bare keys), so the work is
**only to add the definition node** — usages are untouched, data unchanged. Exactly
the `m3:changelog` move, in series. Safe.

The 24: `analogyInGs`, `analogyInGt`, `definition`, `derivation`, `epistemicGap`,
`examples`, `formula_role`, `grammar`, `independence`, `notation_disambiguation`,
`notation_note`, `openQuestion`, `pairWith`, `rejected_names`, `role`, `semantics`,
`symbol`, `theoretical_basis`, `transcendentalQuestion`, `triadicPattern`,
`typeIndex`, `typeSymbol`, `usage`, `visual`.
(Note: `definition`/`examples` here are candidates for the Family-A standards
instead — decide per property.)

### B2 — bare keys needing BOTH prefix AND definition (decision required)

The dominant native bare keys, almost all sub-fields of the `eagleView` /
`sphinxView` blocks in M2: `formula` (365), `role` (308), `status` (294),
`basis` (266), `value` (178), `characteristics` (130), `semantics` (36),
`pros`/`cons` (56), `mechanism` (22)…

These are not scattered problems — they are **a handful of recurring documentary
structures repeated hundreds of times**. That reframes B2 as: *decide the fate of
the `eagleView`/`sphinxView` block shape once*, not term by term.

### C — false positives (exclude)

Single letters and two-letter primitives (`S`, `I`, `F`, `D`, `A`, `Gt`, `St`,
`Ss`, `Im`, `T`, `K`, `L`…) are **formula values**, not keys. Exclude from the count.

---

## 4. The open architectural question (Michel decides, per block)

For each `eagleView`/`sphinxView` sub-field: **data or documentation?**

- **Data** (e.g. `formula` — a reasoner should validate it against the grammar;
  this is the very object of SC-2) → reify: a class `m2:EagleView` with
  `m2:hasFormula`, `m2:hasBasis`… visible, SHACL-checkable.
- **Documentation** (e.g. `pros`/`cons`/`rationale`/`mechanism`) → a single
  declared container `m3:documentation` (transversal, apex) under which invisibility
  becomes *intended and verifiable*, not accidental.

Intuition (to confirm): it is **mixed** — the data/documentation frontier runs
*inside* the eagleView block. `formula` is data; `pros`/`cons` is documentation.
That mixed frontier is precisely the accidental δ₁.

**Watch — latent duplication**: `role` exists both as `m3:role` (B1, in Bicephalous)
and as bare `role` (B2, 308× in M2 eagleView). Defining `m3:role` (M3 layer) *and*
`m2:role` (M2 layer) is legitimate under per-layer specialisation **only if their
semantics genuinely differ**; otherwise it re-creates the retired eagleView/D8
duplicate. Check case-by-case.

---

## 5. Progress counter (VOC = 6th validator family)

This worksite becomes the **VOC** module of `M0_TscgOntologyValidator` (joining
CTX/FRB/DUP/NOT/STR). Purely deterministic — a term is declared or it is not — so it
sits squarely in "detection, no semantic judgement". The triage (data vs
documentation, layer assignment) stays with Michel.

| Layer | bare-key occ (canonical) |
|---|---|
| M2 | 3962 |
| M1 | 1572 |
| M3 | 738 |
| M0 | 172 |
| **total** | **6444** (1387 distinct) |

Target when VOC ships: **0 undeclared keys** on canonical files (Family C excluded).

---

## 6. Execution order (proposed)

1. **Family A** — apply the standard-replacement table (mechanical, after approval).
2. **B1** — declare the 24 already-prefixed `m3:*` in their owning M3 file
   (`M3_BicephalousPerspective` for the Territory/Map set), following §1. Safe:
   definitions only, no usage change, no data change.
3. **Michel's per-block decision** on the eagleView/sphinxView shape (§4).
4. **B2** — execute the decided shape (reify as data, or move under
   `m3:documentation`), per layer, following the §1 rails.
5. Fold all of the above into VOC (validator) as the standing gauge.

**Golden discipline**: like the CTX/changelog lots, declaring previously-invisible
keys makes new triples visible → **golden delta unpredictable → isolated commits**,
`--update-golden` with recorded reason.

---

## 7. Relation to the harness question (2026-07-22)

The in-chat code sandbox (git-HEAD clone + rdflib/pyshacl/pyoxigraph/owlready2)
already **is** the harness that runs these checks; every measurement in this note was
produced there. An MCP server adds only cross-session persistence and a stable tool
contract — i.e. the validator's endgame. Recommendation: stay in the sandbox for
now; reserve MCP for a **small remote** validator (≈CTX/FRB/DUP/NOT/STR/VOC tools)
when it must run outside the chat. OntoGPT is the wrong fit (text→ontology
extraction, not corpus hygiene).
