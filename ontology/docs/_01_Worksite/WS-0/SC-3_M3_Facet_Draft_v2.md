# SC-3 — M3 Facet Model — DRAFT v2 (FROZEN, working names, NOT graved)

**Author**: Echopraxium with the collaboration of Claude AI
**Status**: **FROZEN** — all model decisions closed. Ready for the graving phase,
which stays behind the §6 locks. Supersedes v0 and v1.
**Scope**: graves the Facet *mechanism* + the **Audience** facet only.
`ontologyType` untouched (NATURE = backbone, not a facet). No SCALE/NATURE.
**HEAD re-measure (2026-08-28)**: M3_GenesisGrammar 4.5.0 · M2_GenericConcepts 16.19.0 ·
M0_Common 1.1.0 — unchanged. Target IRIs collision-free. `skos` already in M3 `@context`.

---

## Decision log (closed)

- **#1** carrier property = generic **`m3:hasFacetValue`** (axis is an *individual*, so no
  per-axis property; the axis is read via `valueOf`).
- **#2** Audience is **optional** — no "≥1 Audience" obligation; migration touches only
  Democratization carriers.
- **#3** inter-value relations **deferred** — the produce→consume chain is documented in
  prose in `Audience`'s `rdfs:comment`; **no** relation property is graved
  (`broader`/`narrower`/`related`/`precedes`/`consumes` all excluded) until a *second*
  ordered facet demands one. (Head Chef's overfitting guard: reveal, don't reify on one case.)

---

## 1. The model

A Facet is a **classificatory axis** that files a special case (the platypus) on an
**orthogonal** dimension, *without touching the backbone tree* — controlled value-set,
orthogonal, non-derivable from the trunk: semantically far stronger than a tag.

| level | construct | example |
|---|---|---|
| mechanism class | `m3:Facet` (owl:Class) | — |
| **an axis** (a facet) | *individual* `a m3:Facet` = `skos:ConceptScheme` | `m3:Audience` |
| a **value** | `m3:FacetValue` (owl:Class) = `skos:Concept` | `m3:audience.KitUser` |
| value → its axis | `m3:valueOf` (⊑ `skos:inScheme`) | `audience.KitUser valueOf Audience` |
| carrier → value | `m3:hasFacetValue` (multi, IRI-only) | `FireTriangle hasFacetValue audience.KitUser` |

**Doctrine (narrow, kept from HEAD `m0:Facet`)**: a facet value is a role — externally
conferred, contingent, Map-perspective, anchored on `m2:Role` (Ss|K); distinct from
`m0:ScoringProperty` and `m0:FocalProperty`. Faceted classification (Ranganathan 1933):
axis = *facet*, value = *focus*.

**Contract = the value itself.** No separate contract object: a `m3:FacetValue` carries its
obligations as its own properties. A value with none = a bare (valid) value. Contracts are
**compositional**: an instance carrying several values honours the **union** of their
obligations, each a conditional SHACL shape ("IF carrier has value V THEN provide X").
AUDIENCE values carry **no contract**.

**Inter-value relations**: deferred (Decision #3). When a future ordered facet needs them,
use **SKOS** (`broader`/`narrower`/`related`) — **never `owl:subClassOf`** (would re-import
the subsumption tree the facet exists to avoid), closed within one axis via `valueOf`.

---

## 2. M3 — JSON-LD fragment to insert into `M3_GenesisGrammar.jsonld` @graph

```jsonld
{ "@id": "m3:Facet", "@type": "owl:Class",
  "rdfs:label": "Facet",
  "rdfs:comment": "A classificatory axis (Ranganathan faceted classification, 1933): an orthogonal, non-derivable dimension that files instances without altering the backbone type tree. Each individual 'a m3:Facet' is also a skos:ConceptScheme. Values are m3:FacetValue. Semantically a conferred, contingent, Map-perspective role (anchored on m2:Role Ss|K); distinct from ScoringProperty/FocalProperty." },

{ "@id": "m3:FacetValue", "@type": "owl:Class",
  "rdfs:comment": "A value of a facet (the 'focus' in Ranganathan's sense). Also a skos:Concept. Belongs to exactly one axis via m3:valueOf. MAY carry contractual obligations directly as its own properties (SHACL-enforced on any carrier that declares it)." },

{ "@id": "m3:valueOf", "@type": "owl:ObjectProperty",
  "rdfs:subPropertyOf": { "@id": "skos:inScheme" },
  "rdfs:domain": { "@id": "m3:FacetValue" }, "rdfs:range": { "@id": "m3:Facet" },
  "rdfs:comment": "Links a facet value to the axis (m3:Facet individual) it is a value of. Closes any inter-value relation within one axis." },

{ "@id": "m3:hasFacetValue", "@type": "owl:ObjectProperty",
  "rdfs:range": { "@id": "m3:FacetValue" },
  "rdfs:comment": "Declares that this instance carries one or more facet values. Multi-valued. Values MUST be IRIs of registered m3:FacetValue individuals. FORBIDDEN: bare string values. Replaces m0:hasFacet." },

{ "@id": "m3:Audience", "@type": ["m3:Facet", "skos:ConceptScheme"],
  "rdfs:label": "Audience",
  "rdfs:comment": "AUDIENCE facet: for whom the artifact is produced (read 'for whom', not 'by whom'). Values follow the Kit produce->consume chain — KitArchitect produces for KitCrafter, who produces for KitUser (offset by one along the chain) — but that ordering is documentation only: no relation property is graved (SC-3 Decision #3). Optional facet. Closed value-set." },

{ "@id": "m3:audience.KitArchitect", "@type": ["m3:FacetValue", "skos:Concept"],
  "m3:valueOf": { "@id": "m3:Audience" }, "rdfs:label": "KitArchitect",
  "rdfs:comment": "Models/refactors the ontology architecture (M3/M2/M1)." },
{ "@id": "m3:audience.KitCrafter", "@type": ["m3:FacetValue", "skos:Concept"],
  "m3:valueOf": { "@id": "m3:Audience" }, "rdfs:label": "KitCrafter",
  "rdfs:comment": "Fabricates Kits using an Architect's ontologies." },
{ "@id": "m3:audience.KitUser", "@type": ["m3:FacetValue", "skos:Concept"],
  "m3:valueOf": { "@id": "m3:Audience" }, "rdfs:label": "KitUser",
  "rdfs:comment": "Uses what the Crafter fabricated. Absorbs the former m0:facet.Democratization (novice audience)." }
```

---

## 3. M0 — remove from `M0_Common.jsonld` (the whole `m0:facet.*` apparatus)

```
□ m0:Facet (class)              □ m0:hasFacet (property)
□ m0:facet.Democratization      (+ facetAnchor, facetFormula "Ss|K", facetContractFields)
□ m0:illustratesConcept         □ m0:RoleGrounding (enum class)
□ m0:roleGrounding              □ m0:roleGrounding.Reused  □ m0:roleGrounding.Designed
```

---

## 4. SHACL — `check-M0/M0_Instances_Schema_shacl.ttl`

- **Remove**: `DemocratizationFacetContractShape`, `RoleGroundingShape`, `ForbidStringRoleGroundingShape`.
- **Keep, renamed**: `ForbidStringHasFacetShape` → `ForbidStringHasFacetValueShape`
  (`m3:hasFacetValue` must be an IRI, never a string).
- **No presence shape** — Audience is optional (Decision #2).

---

## 5. MIGRATION (`Democratization → KitUser`)

- Every instance with `m0:hasFacet: m0:facet.Democratization` → `m3:hasFacetValue: m3:audience.KitUser`.
- `m0:illustratesConcept` / `m0:roleGrounding` on those instances → **dropped** (contract not
  carried to KitUser).
- ⚠ **Target set unconfirmed**: GitHub API was rate-limited; the exact instances declaring
  `facet.Democratization` / `illustratesConcept` were NOT listed. Establish by local
  `git grep` before migrating — the drop cost depends on it.

---

## 6. GRAVING LOCKS (before any commit)

- **WS-5 gate** `axis.py` (AUDIENCE only): green on migrated corpus — `grave_after: WS-5`.
  Checks (no presence check): `hasFacetValue` is IRI · resolves to a registered `FacetValue`
  · `valueOf` resolves to a registered axis.
- **Pellet punning**: `Audience` is an individual `a m3:Facet` (Facet = owl:Class) + `valueOf ⊑ inScheme`.
  Confirm Pellet OWL DL tolerates the class/individual punning before graving.
- **WS-4 naming**: freeze IRIs (`m3:Facet`, `m3:FacetValue`, `m3:valueOf`, `m3:hasFacetValue`,
  `m3:Audience`, `m3:audience.*`).
- **Michel's formal gates**: linter · Pellet · SHACL CONFORMS:True · run_all_layers · golden diff.
- **Fresh HEAD-anchored session, one isolated lot at a time** (Record §8).

---

*Model frozen. Next actionable step (unlocked, advances WS-5): build `axis.py` reduced to
AUDIENCE against §2. EpistemicResidue/Sieve later becomes a `FacetValue` WITH a contract —
the mechanism will already be in place.*
