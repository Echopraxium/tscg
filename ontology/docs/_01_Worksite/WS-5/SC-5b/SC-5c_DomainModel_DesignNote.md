# SC-5c — Domain Model: relations and facets (design note)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-12
**Worksite**: WS-5 · lots SC-5b (subdomains become classes) → SC-5c (domain model)
**Status**: DRAFT — decisions taken in conversation on 2026-10-12, to be refined before any
code. Nothing in this note is implemented yet.

> Companion: `SC-5b_Subdomains_Decision_Table.xlsx` (same folder) — the line-by-line table
> of the 128 `m1:subdomains` strings, with the decisions below applied as proposals.

---

## 1. Scope split

- **SC-5b** creates the subdomain classes and their `rdfs:subClassOf` links only, then
  deletes `m1:subdomains` (decision (a), 2026-10-12). Nothing else.
- **SC-5c** adds the domain model of this note: the relations `m1:requires` and
  `m1:hybridOf`, the facets `AbstractionLevel` and `ModelPurpose`, and the Scope view.

## 2. Which subdomains become classes (Q10, adopted)

A subdomain class is created only if an M0 instance or an M1 concept points to it today
(the parents it needs come with it). The others are dropped and recreated when an instance
needs them; the strings stay in git history and in the decision table. Consistent with the
2026-10-12 rule *what can be inferred is not stored*. Effect measured on HEAD `4386b8b`:
77 → 26 KEEP.

## 3. Three relations between domains

| Relation | Meaning | Test | Example |
|---|---|---|---|
| `rdfs:subClassOf` | **is a kind of** | X is still an A without the rest → true for each parent | Geophysics ⊑ Geology, Physics; MusicTheory ⊑ Music |
| `m1:requires` (new) | **relies on the knowledge of** | X needs B to work, without being part of B | Photography requires Optics, Mechanical Engineering, Software Engineering; Population Biology requires Statistics; ElectronicMusic requires Electronics |
| `m1:hybridOf` (new) | **exists only through the crossing** | X is a kind of none of its components; its identity *is* the crossing | Biomimetics hybridOf Biology, Engineering |

Rules:
- A domain may have **n parents** when it truly is a kind of each (Language Theory ⊑
  Language, Mathematics; Mechatronics ⊑ Electromechanics, Electronics, Software
  Engineering; Electromechanics ⊑ Electrical Engineering, Mechanical Engineering).
- **Never declare a parent already implied transitively** (Mechatronics is not declared
  ⊑ Electrical Engineering: Electromechanics gives it). Candidate check for `check_M1`.
- **Hybrid is used judiciously**: only where `subClassOf` and `requires` model the relation
  badly (Michel, 2026-10-12). A hybrid is ⊑ `m1:Domain` directly and carries `m1:hybridOf`
  (2+ IRI values).
- `m1:requires` and `m1:hybridOf` are `owl:AnnotationProperty` with IRI values, like
  `m1:relatedDomains` (no punning on domain classes, no effect on the reasoner).
- `m1:requires` is directed; it should absorb most of today's `m1:relatedDomains`, which
  stays for loose affinity (e.g. Mechatronics relatedDomains Robotics). Direction
  convention for `relatedDomains`: to fix.

**Worked example — games (Michel, 2026-10-12)**:

```
Game                  ⊑ m1:Domain                  (Root)
Card Game             ⊑ Game
Collectible Card Game ⊑ Card Game                  (MtgColorWheel; replaces "Trading Card Games")
Strategy Game         ⊑ Game
Poker                 ⊑ Card Game, Strategy Game   (two parents: a kind of each)
Poker Theory          ⊑ Poker                      AbstractionLevel = Theory
Poker Theory          m1:requires  Game Theory, Probability
Game Theory           ⊑ Mathematics                (a branch of Mathematics, NOT of Game)
```

It shows the recurring pattern *"X Theory ⊑ X, requires the formal tools"* (also MusicTheory
⊑ Music): the theory **of** a domain is a kind of that domain; the mathematics it uses is a
dependency, not a parent. Only Game, Card Game, Collectible Card Game and the Game Theory
relink are created in SC-5b (Q10); Poker, Strategy Game and Poker Theory wait for an M0
instance (the PokerHand3D exercise is not one).

## 4. Scope — a computed view, not stored

| Scope | Computed as |
|---|---|
| Root | ⊑ `m1:Domain` directly, no `m1:hybridOf` |
| Branch | ⊑ one or more other domains |
| Hybrid | carries `m1:hybridOf` |

Scope is derivable from the graph, so it is exposed as a query (TscgOntologyExplorer,
Compendium), never stored. Roots named by Michel: Music, Biology, Game, Finance,
Mathematics (Finance as Root = Finance ⊑ `m1:Domain` directly, Economics through
`requires`/`relatedDomains` — to confirm).

## 5. Two facets (M3 Facet mechanism, SC-3)

| Facet | Values | Cardinality | Example |
|---|---|---|---|
| `AbstractionLevel` | Theory / Application / Practice | one | MusicTheory = Theory; Nuclear Engineering = Application; Broadcast Television = Practice |
| `ModelPurpose` | Pragmatic / Descriptive / Explanatory / Predictive | cumulative | Seismology = Explanatory, Predictive; Comparative Mythology = Descriptive |

- Empirical sciences take `AbstractionLevel` = Theory (knowledge about the real); their
  nuance is carried by `ModelPurpose`.
- The two axes are orthogonal and not derivable: they pass the SC-3 legitimacy test.
- **Blocker to solve in SC-5c**: `m3:hasFacetValue` is an `owl:ObjectProperty` on HEAD.
  Applied to a domain class it would be punning (forbidden 2026-10-11). An annotation
  variant is needed — an M3 change, through the diagnosis pipeline.

## 6. Out of the domain hierarchy

Musical genres (Jazz, Rock, Cuban rap, Indian classical music) are objects a domain studies
or produces, not fields of knowledge: they belong to an M1 concept taxonomy in the music
extension (e.g. `music:Genre`), where the same kind-of / hybrid distinction applies.
Organology ("Music Instruments") is a field and may be a subdomain.

## 7. Open points

1. Facet annotation variant (§5): name and M3 placement.
2. External alignments: UDC / Dewey / Wikidata as `skos:closeMatch` (interoperability,
   Im), also usable as a KEEP/DROP test for future subdomains.
3. `relatedDomains` direction convention; migration of existing values to `m1:requires`.
4. DCC010 and the Explorer: follow `m1:hybridOf` / `m1:requires` where queries need it.
5. Finance as Root (Game Theory ⊑ Mathematics is decided, see §3).
6. **`requires` targets: domains or providers of a DomainContract** (Michel, 2026-10-13).
   `m1:requires` takes a list of IRIs, each either a subclass of `m1:Domain` or a class
   that provides an `m1:DomainContract` (SHACL `sh:or`). Proposed model, reusing the
   existing M2 contract mechanism (`m2:ConceptContract`, mixin `rdfs:subClassOf` +
   `m2:implements`, as for Triggerable / Observable / Composable / Stateful):

   ```
   m1:DomainContract  ⊑ m2:ConceptContract
   m1:DomainTool      ⊑ m1:DomainContract   (an artifact: 3D printer, microscope)
   m1:DomainMethod    ⊑ m1:DomainContract   (a procedure: TRIZ, Bayesian inference)
   m1:DomainExpertise ⊑ m1:DomainContract   (a skill: soldering, sight-reading)
   m1:DomainModel     ⊑ m1:DomainContract   (a formalism: Bayesian network, Markov decision process)
   3DPrinter ⊑ m1:DomainTool ; m2:implements m1:DomainTool ;
             m1:domain FabricationProcess        (FabricationProcess ⊑ Fabrication)
   AdditiveManufacturing m1:requires 3DPrinter
   ```

   Points to settle before implementing:
   - **The contract is not parameterised by a domain** (OWL has no generic interfaces):
     "DomainTool *of* FabricationProcess" = the generic contract + `m1:domain` on the
     provider (minCount 1, SHACL). No per-domain contract classes.
   - **`m2:implements` has `rdfs:domain m2:GenericConcept`**: used on an M1 class it would
     infer that 3DPrinter is a GenericConcept. Widen the domain (e.g. to `owl:Class`) —
     an M2 change, through the diagnosis pipeline.
   - **Each contract needs `m2:contractCapabilities`**, like the four M2 contracts —
     otherwise it is only a category. DomainTool: belongs to ≥1 domain, has an
     input/output. DomainMethod: has steps (`m2:Step`, `m2:Workflow`). DomainExpertise: to
     define.
   - **DomainExpertise vs Domain**: "requires Statistics" (the field) vs "requires
     statistical expertise" (a skill) — keep DomainExpertise for practical skills only.
   - **Formalisms**: DECIDED (Michel, 2026-10-13) — a fourth contract **`m1:DomainModel`**
     (Bayesian network, Markov decision process). The facet formerly named `Model` is renamed
     **`ModelPurpose`** (Michel, 2026-10-13) to avoid the clash.
   - Supersedes the 2026-10-13 `m1:Tool` / `m1:DomainTool`-as-class note. Objects such
   as TV Channel or musical genres are neither domains nor tools → M1 concepts.

## 8. Decisions of 2026-10-13 (Michel) — to apply in the lots named

- **Rename the property `m1:domain` → `m1:belongsToDomain`** (DECIDED). Reason: `m1:domain`
  (property) and `m1:Domain` (class) differed only by case. The class `m1:Domain` keeps its
  name (stabilised by SC-5). Apply in the **lot M0**, which rewrites the 44 M0 values from
  strings to IRIs anyway; plus the 8 M1 files and `M0_INSTANCE_TEMPLATE.jsonld` (measured on
  HEAD `4386b8b`). Rejected names: ApplicationDomain / domainApplication (clash with the
  `AbstractionLevel` value Application, and wrong for combos and tools),
  reificationOfDomain (*reification* is a doctrinal term in M3/M2 — "no reification of
  composite domains" — and an RDF technique). The nuance "an M0 instance exemplifies a
  domain", if wanted, gets its own M0 property in the lot M0 (e.g. `m0:exemplifies`).
- Vocabulary in TSCG docs: "knowledge domain" for `m1:Domain`; "RDF domain (type of the
  subject)" for `rdfs:domain`.
- **`m2:implements`**: its `rdfs:domain m2:GenericConcept` is wrong today (the 15 subjects
  on HEAD are classes ⊑ GenericConcept, so it would type them as instances — punning under
  RDFS). Fix: `rdfs:domain owl:Class`, like `m2:characterizedBy`. Who may implement is
  checked per layer through one extension point (a marker on `m2:GenericConcept` in M2, on
  `m1:DomainContract` in M1), the rule living in `check_M1` until SHACL can validate a whole
  layer (runner is per file, no imports, no inference) — an acknowledged toolchain debt.
  `Implementable` + moving Domain into M2 was rejected (M2 must not name M1).
- **Mixin not applied on HEAD**: the `m2:ConceptContract` comment says contracts are
  implemented by `rdfs:subClassOf` mixin, but the 15 implementors carry only
  `m2:implements`. To settle in SC-5c: apply the mixin, or fix the comment.
- Leftover found: `m1:extension:optics:Optics_Domain` in `M1_Optics.jsonld` carries a string
  `m1:domain` — clean up in SC-5b.

## 9. Reuse before inventing (Michel, 2026-10-13)

**Working rule**: before modelling a notion, check whether an existing vocabulary covers it,
and align to it (`skos:exactMatch` / `skos:closeMatch`) rather than re-inventing it. TSCG
models only what no external vocabulary carries: the links to M2, `m1:requires`,
`m1:hybridOf`, the contracts and the facets.

**First check — OpenAlex** (v2 taxonomy, 6 October 2026: 4 domains, 26 fields, 252
subfields, 4,516 topics; ASJC-based; read from `github.com/ourresearch/openalex-topic-classification`
`v2/changes/topics.csv`; the OpenAlex API itself is not reachable from Claude's sandbox).
Result on the 28 SC-5b lines (decision table, columns "OpenAlex …"):
- only **10 / 28** have an OpenAlex field or subfield: OpenAlex classifies research output
  and stops at ASJC subfields — too coarse for Counterpoint, Trophodynamics, Thermodynamics,
  Color Science… Its 4,516 *topics* are research themes, not disciplines: not alignment
  targets.
- **consistent** with our decisions: Optics ⊑ Physics; Pharmacology as a field of its own
  (supports Root); Developmental / Cell Biology, Physiology under the life sciences.
- **diverges**: Decision Theory = field "Decision Sciences" (not ⊑ Mathematics); Signal
  Processing ⊑ Computer Science (not Electronics); Nuclear Engineering under Energy;
  Endocrinology a sibling of Physiology; Finance ⊑ Economics field (Michel wants Root).

Recommendation: OpenAlex as the alignment target for roots and mid-level domains (fields,
subfields); **Wikidata** ("academic discipline" items, `subclass of`) for deeper subdomains,
plus specialist thesauri where they exist (MeSH, MSC, ACM CCS, PhySH). Every divergence is
kept only with a written reason.

**Decided (Michel, 2026-10-13)**: OpenAlex is the reference vocabulary for roots and
mid-level domains. SC-5b adds `skos:closeMatch` (IRI `https://openalex.org/fields/<id>` or
`https://openalex.org/subfields/<id>`) on the domain classes that have an OpenAlex field or
subfield. Wikidata for finer levels and the written-reason rule for divergences: SC-5c.
First recorded divergence: Endocrinology ⊑ Physiology (OpenAlex: siblings).

## 10. Review outcomes of 2026-10-14 (Michel)

- **Color Science ⊑ Vision Science** (new, closeMatch OpenAlex 2809 Sensory Systems),
  requires Optics, Physiology. Colour is a perception model, not a property of light (cones
  "resonate"; a dyschromatope sees other colours): Optics is on the Territory side, Color
  Science on the Map side. Colour spaces and gamut — the RGB / CMY / CMYK / HSL instances —
  are **`m1:DomainModel` providers of Color Science**: first concrete use case of the
  contract model (§7.6).
- **Semiconductor Physics ⊑ Condensed Matter Physics** (new, OpenAlex 3104) ⊑ Physics,
  requires Quantum Mechanics; Electronic Components ⊑ Electronics requires Semiconductor
  Physics (SC-5c).
- **Signal Processing ⊑ Electronics + Computer Science** (OpenAlex 1711), requires
  **Fourier Transform** — a DomainContract provider (DomainMethod or DomainModel: to
  settle), belongsToDomain Mathematics.
- Arbitrariness is accepted (Michel): a classification is a Map, not the Territory. It is
  made visible (reason per decision, divergence from OpenAlex recorded) and revisable.

## 11. Future work — epistemological prisms (Michel, 2026-10-14)

Idea: an ontology should be *projectable* onto an epistemological prism. Same domain
classes, several hierarchies: the TSCG prism (our `subClassOf`, the default), the OpenAlex
or library prism (Dewey/UDC), a disciplinary prism (e.g. Color Science under Optics for a
physicist), facet prisms (reordering by AbstractionLevel / ModelPurpose). Existing means:
SKOS — one concept in several `skos:ConceptScheme`, each with its own `skos:broader`,
held in separate named graphs; "ontology views" in ontology engineering. In TSCG terms a
projection is a functor (cf. the natural transformation Φ: Gt → Gm of Modelisation in M2).
Nothing to change in SC-5b: the `skos:closeMatch` alignments are the mapping that makes the
OpenAlex projection computable. A worksite of its own, beyond SC-5c, when needed.
