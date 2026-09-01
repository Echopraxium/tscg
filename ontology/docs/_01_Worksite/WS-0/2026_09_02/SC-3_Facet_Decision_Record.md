# SC-3 — Facet as an M3 Principle: Decision Record

**Version**: 2.0.0
**Date**: 2026-09-01
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Worksite**: WS-0 / SC-3
**Status**: GRAVED — the frozen model was applied to HEAD-anchored files and passed
every gate that can run without the Head Chef's machine (linter, AXIS, Pellet OWL DL,
SHACL CONFORMS). Committed as one atomic 6-file lot after the Head Chef's formal gates.
**Supersedes**: **v1.0.0 (2026-07-30) — the four-axis model is ABANDONED** (see §1).
The two *conceptual results* of v1.0.0 §5 (the legitimacy criterion and the axis
filter) are **retained** — indeed they are what condemns the four-axis model (§1).

**Authority**: corpus facts below were measured at `git show HEAD:<file>` on
2026-08-28 (HEAD `7da58af`): M3_GenesisGrammar 4.5.0 · M2_GenericConcepts 16.19.0 ·
M0_Common 1.1.0 · M3_GrammarFoundation 2.5.0. Target IRIs collision-free; `skos`
already in M3 `@context`. Re-measure before trusting any number here.

---

## 0. WHAT CHANGED SINCE v1.0.0 — the re-scope (read first)

v1.0.0 proposed decomposing the overloaded `ontologyType` into **four axes**
(SCALE / NATURE / AUDIENCE / DOMAIN), all typed as facets. **That decomposition is
withdrawn.** Applying v1.0.0's own §5 legitimacy criterion to itself shows three of
the four were not facets at all:

- **NATURE** (SystemModel / Framework / Grammar / Tool) is **the backbone**, not a
  facet. It is *what the artifact essentially is* — Territory, exactly-one, a tree.
  Typing it as a facet **fabricates an orthogonality** — the precise abuse v1.0.0 §5
  warns against ("abusive when it fabricates an orthogonality to dodge a needed
  correction of the backbone"). NATURE stays the backbone tree.
- **SCALE** (Poclet / CaseStudy / RealWorldSystem) is a **refinement of the
  SystemModel branch** of the backbone, not an orthogonal facet.
- **DOMAIN** was always coupled to SC-5, never graved here.
- **AUDIENCE** is the *only* axis that passes the conferred / contingent /
  Map-perspective test → **the single genuine facet.**

**New SC-3 scope**: grave the **Facet mechanism** + the **Audience** facet only.
**`ontologyType` is left entirely untouched** — no SCALE, no NATURE, no DOMAIN.

Second change, mechanical but load-bearing: v1.0.0's plan was to *lift* `m0:Facet`
into `m3:Facet` and re-type properties. v2.0.0 instead **removes the entire `m0:facet.*`
apparatus** and graves a **fresh M3 mechanism aligned to SKOS**, with the value class
renamed `m3:Focus` → **`m3:FacetValue`**.

---

## 1. THE FROZEN MODEL (all decisions closed)

A Facet is a **classificatory axis** that files a special case (the platypus) on an
**orthogonal, non-derivable** dimension, *without touching the backbone tree*.
Semantically far stronger than a tag: controlled value-set + axis membership +
orthogonality + an optional per-value contract.

| level | construct | example |
|---|---|---|
| mechanism class | `m3:Facet` (`owl:Class`) | — |
| **an axis** (a facet) | *individual* `a m3:Facet` = `skos:ConceptScheme` | `m3:Audience` |
| a **value** | `m3:FacetValue` (`owl:Class`) = `skos:Concept` | `m3:audience.KitUser` |
| value → its axis | `m3:valueOf` (⊑ `skos:inScheme`) | `audience.KitUser valueOf Audience` |
| carrier → value | `m3:hasFacetValue` (multi, IRI-only, **no domain**) | `inst hasFacetValue audience.KitUser` |

**Doctrine (narrow, kept from HEAD `m0:Facet`)**: a facet value is a role — externally
**conferred, contingent, Map-perspective**, anchored on `m2:Role` (Ss | K); **distinct
from** `m0:ScoringProperty` (derived quality) and `m0:FocalProperty` (Gs stereopsis).
Faceted classification (Ranganathan 1933): axis = *facet*, value = *focus*.

**Contract = the value itself.** No separate contract object: a `m3:FacetValue` carries
its obligations as its own properties. A value with none is a bare (valid) value.
Contracts are **compositional** — a carrier holding several values honours the **union**
of their obligations, each a conditional SHACL shape ("IF carrier has value V THEN
provide X"). **AUDIENCE values carry no contract.** (This is the hook by which
`EpistemicResidue/Sieve` will later be a `FacetValue` *with* a contract — the mechanism
is now in place.)

---

## 2. DECISIONS (closed)

- **#1 — carrier property = generic `m3:hasFacetValue`.** The axis is an *individual*
  (`a m3:Facet`), so there is no per-axis property; the axis is read via `valueOf`.
- **#2 — Audience is OPTIONAL** — **no "≥1 Audience" obligation.** *(This reverses
  v1.0.0 §4's `minCount 1` for AUDIENCE.)* No presence shape is graved; migration
  touches only Democratization carriers.
- **#3 — inter-value relations DEFERRED.** The produce→consume chain
  (KitArchitect → KitCrafter → KitUser, offset by one) is **documentation only**, in
  `m3:Audience`'s `rdfs:comment`. **No** relation property is graved
  (`broader`/`narrower`/`related`/`precedes`/`consumes` all excluded). If a *second*
  ordered facet later demands ordering, use **SKOS** (`broader`/`narrower`/`related`),
  never `owl:subClassOf` (which would re-import the subsumption tree the facet exists to
  avoid), closed within one axis via `valueOf`. (Head Chef's overfitting guard: reveal,
  don't reify on one case.)

---

## 3. NAMING — convention (A), de-facto for WS-4

Values use the **per-axis** convention: **`m3:audience.<Value>`** (dot separator,
consistent with the former `m0:facet.Democratization`), *not* a generic
`m3:facet.<Value>`. Rationale: the axis is visible in the IRI and it scales to N axes
(`reproductionMode.Ovipare`, `audience.KitUser`), while the axis binding is anyway
carried by `valueOf`. Classes CamelCase (`m3:Facet`, `m3:FacetValue`), properties
camelCase (`m3:valueOf`, `m3:hasFacetValue`), axis individual CamelCase (`m3:Audience`).
WS-4 (GrammarSignature) is not yet a formal worksite; this is the convention to
formalise there.

---

## 4. THE AUDIENCE AXIS

Derived from TSCG's own mission ("a toolkit to fabricate Kits", Lego-Technic sense),
so the value-set is **closed and principled**:

- `m3:audience.KitArchitect` — models/refactors the ontology architecture (M3/M2/M1).
- `m3:audience.KitCrafter` — fabricates Kits using an Architect's ontologies.
- `m3:audience.KitUser` — uses what the Crafter fabricated. **Absorbs the former
  `m0:facet.Democratization`** (novice audience).

**Read as AUDIENCE (for whom), not stage (by whom).** Audience and stage are offset by
one along the produce→consume chain; modelling *audience* keeps the facet a conferred,
Map-perspective property of the artifact. **Orthogonality to meta-level, proven on the
corpus**: `TscgOntologyExplorer` (M0, KitArchitect) vs `FireTriangle` (M0, KitUser) —
audience varies at fixed meta-level, so it is not the layer axis in disguise.

---

## 5. MIGRATION (`Democratization → KitUser`)

- Every instance with `m0:hasFacet m0:facet.Democratization` →
  `m3:hasFacetValue m3:audience.KitUser`.
- On those instances, `m0:illustratesConcept` / `m0:roleGrounding` are **dropped** —
  the old Democratization contract is **not** carried over to KitUser (AUDIENCE has no
  contract).
- **Gauge X = 1** (measured at HEAD by `git grep`): only `QRCodeToPocketCity` actually
  declared the facet in an M0 instance file. FireTriangle / ExposureTriangle are *cited
  in doctrine* but do **not** declare it. M0 migration is therefore one file.

---

## 6. WHAT WAS GRAVED (the atomic 6-file lot)

| file | change |
|---|---|
| `ontology/M3_GenesisGrammar.jsonld` | 4.5.0 → **4.6.0**; §1 fragment inserted (`m3:Facet`, `m3:FacetValue`, `m3:valueOf`, `m3:hasFacetValue`, `m3:Audience` + 3 `audience.*`); changelog |
| `ontology/M0_Common.jsonld` | 1.1.0 → **1.3.0**; entire `m0:facet.*` apparatus removed; changelog (3) |
| `ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl` | **v1.7**; 3 shapes removed (`DemocratizationFacetContractShape`, `RoleGroundingShape`, `ForbidStringRoleGroundingShape`); survivor renamed + repointed `ForbidStringHasFacetShape` → `ForbidStringHasFacetValueShape` (`m0:hasFacet` → `m3:hasFacetValue`) |
| `instances/poclets/QRCodeToPocketCity/M0_QRCodeToPocketCity.jsonld` | Democratization → `m3:hasFacetValue m3:audience.KitUser`; `owl:versionInfo` + changelog → **1.1.0** |
| `ontology/cli-tools/validator/checks/axis.py` | NEW — the WS-5 **AXIS** check family that gates SC-3 (AXIS-1..5), detection-only, mirrors `ctx.py` |
| `ontology/cli-tools/validator/tscg_validator.py` | 2 lines — import + register `AXIS` in `_IMPLEMENTED` |

**Version-lag correction found & fixed** (head-over-memory catch): `M0_Common`'s
`owl:versionInfo` was a stale **1.1.0** while its changelog head was already **1.2.0**
(the entry that *added* the facet apparatus). The SC-3 removal is therefore **1.3.0**,
which also repairs the lag. This is why v2's M0 bump is 1.3.0, not the 1.2.0 a naive
read of the stale `versionInfo` would suggest.

**Gates passed (everything runnable off the Head Chef's machine):**
- **linter** — 0 new warning on the graved files (in-tree HEAD-vs-graved warning sets
  identical; the only warning, `@base /ontology/`, is a pre-existing repo-wide false
  positive).
- **AXIS gate** — 0 finding on the lot; proven *live* (falsifiable): the un-migrated
  QRCode yields 3× `AXIS-3`, the migrated one yields 0.
- **Pellet (OWL DL)** — consistent, no inconsistent class. **This confirms the
  `Audience` class/individual punning** (`Audience` an individual `a m3:Facet` while
  `m3:Facet` is `owl:Class`) — v1.0.0 §8's open punning risk is now **discharged by a
  real reasoner**, not merely analytically.
- **SHACL CONFORMS:True** — migrated QRCode against the edited M0 SHACL (pyshacl).
- **run_all_layers** — SC-3 exonerated: the only moves were (a) `ENC001` (CRLF), a
  Windows `autocrlf` checkout artifact on 2 *M1* files SC-3 never touches — fixed
  separately by a `.gitattributes` `*.jsonld/*.ttl text eol=lf` rule; and (b) a
  `−16 shacl_violations` golden drift that reproduces on pristine HEAD (a pyshacl
  version effect, not a loosened shape — the M1 SHACL schema is byte-identical to HEAD).

---

## 7. CARRIED FORWARD FROM v1.0.0 (still valid)

- **Legitimacy criterion for faceting.** A facet is *legitimate* when it **reveals** an
  orthogonality already present that the backbone tree ignored; *abusive* when it
  **fabricates** an orthogonality to dodge real modelling or a needed backbone
  correction. (This is exactly what disqualifies NATURE and SCALE as facets — §0.)
- **Axis filter.** An axis enters only if orthogonal to all existing axes **and**
  non-derivable from them.
- **Rejected candidate axes** (v1.0.0 §3) remain rejected: PERIMETER (derived from
  DOMAIN), OBJECTIVE (correlated, not orthogonal), Map/Territory/Stereopsis triad
  (level confusion), UserRole (classifies persons, not the artifact), KitTester
  (an activity, transversal to the chain).

---

## 8. STILL OWED / OUT OF SCOPE (do not lose)

- **`.gitattributes` hygiene** (separate commit, not SC-3): pin `*.jsonld` / `*.ttl` to
  `eol=lf` so Windows `autocrlf` stops producing phantom CRLF (the ENC001 source).
- **Golden `shacl_violations` 680 → 664** (M1 / SC-6, not SC-3): confirm no shape was
  loosened (M1 SHACL is unchanged), then either pin the pyshacl version that produced
  680 or `--update-golden` to 664 with a recorded note.
- **Phase-shift oscillator poclet** — the original topic that spawned SC-3 (Reading C:
  round-trip as a fidelity test; support circuit = transistor + 3×RC, sinusoidal).
  Étape 2 (analysis) never started.
- **EpistemicResidue / Sieve** — a `FacetValue` **with** a contract (round-trip +
  residue delta), NOT a new `ontologyType`. Now unblocked: the mechanism is graved.
- **Layer-role residue** (v1.0.0 §1: `Genesis`/`GenesisExtension`/…) — likely redundant
  with meta-level; separate cleanup.
- **SC-5 (Domain fusion)** — carries the DOMAIN axis, deliberately not in SC-3.

---

## CHANGELOG

- **2.0.0** (2026-09-01) — **RE-SCOPE.** Four-axis `ontologyType` decomposition
  ABANDONED: NATURE = backbone, SCALE = backbone refinement, DOMAIN = SC-5; only
  AUDIENCE is a genuine facet. `ontologyType` left untouched. Mechanism graved fresh in
  M3 and aligned to SKOS; value class renamed `m3:Focus` → `m3:FacetValue`; links
  `m3:valueOf` (⊑ `skos:inScheme`) + generic `m3:hasFacetValue`. `m0:facet.*` apparatus
  removed from M0_Common (not lifted). Contract-on-value doctrine. Decisions #1 (generic
  carrier property), #2 (Audience OPTIONAL — reverses v1's minCount 1), #3 (inter-value
  relations deferred, SKOS-only if ever). Naming convention (A) `m3:audience.<Value>`.
  Migration gauge X = 1 (QRCodeToPocketCity). Graved as a 6-file atomic lot; all
  runnable gates green (Pellet confirms the Audience punning). M0_Common versionInfo
  lag (1.1.0 vs changelog 1.2.0) corrected to 1.3.0.
- **1.0.0** (2026-07-30) — Initial decision record. Four-axis model
  (SCALE/NATURE/AUDIENCE/DOMAIN); A1 adopted (`m3:Facet` axis / `m3:Focus` value);
  §5 Conferred/Derived sub-typing retracted; ontologyType decomposition; AUDIENCE axis
  derived from the Kit mission with empirical orthogonality proof; rejected axes and the
  two conceptual results recorded; names deferred to WS-4. **[Four-axis model superseded
  by 2.0.0; the two conceptual results and the rejected-axes list stand.]**
