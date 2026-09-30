# WS-1 — Family A triage: bare keys vs standard vocabularies

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-09-30
**Measured on**: HEAD `9505d03`, canonical scope of `tscg_metrics.py` (root `ontology/`) —
4177 bare-key occurrences, 1272 distinct.
**Scope of this triage**: every bare key with ≥ 5 occurrences, every key already in
`STANDARD_REPLACEABLE`, and rare keys whose name looks standard (117 + ~25 keys).
**Status**: PROPOSAL — Michel decides per line (§5), reviewed one line at a time.

## Progress

| Lot | Line | State | Effect |
|---|---|---|---|
| 1a | `examples` / `example` → `skos:example` | DONE 2026-09-30 (Michel approved) | 184 keys renamed (172 lists, 12 strings) + 5 object values converted to named-node lists `{rdfs:label, rdf:value}`; +426 skos:example triples (73 → 499); bogus `owl:examples` (M3_GrammarFoundation, `@vocab owl#`) fixed; 11 conversions stay graph-invisible until their bare parent key is resolved (EagleEye 2, GenesisGrammar 4, M2 `territoryComponent` 5); VOC gauge 4177 → 3983 (−203 keys, +9 from the lot's own changelog entries); gate PASS, golden unchanged |
| 1b | `description` → `dcterms:description` (chosen over `rdfs:comment` on semantic grounds, Michel) | DONE 2026-09-30 | 160 keys renamed (3 inside legacy `metadata` blocks left for a separate lot); +134 dcterms:description triples visible (9 → 143), of which 7 replace bogus `owl:description` (M3 `@vocab owl#`); 26 stay graph-invisible under bare parent keys; VOC gauge 3983 → 3832 (−160 keys, +9 from changelog entries); gate PASS, golden unchanged |

## Method

For each key: (1) read its **actual usage** in the corpus (parent key, value type,
sample values); (2) read the **official definition, domain and range** of the
tempting standard property at its source (DCMI Terms, SKOS Reference, RDF Schema,
OWL Reference, ADMS, schema.org — fetched 2026-09-30); (3) verdict:

| Verdict | Meaning |
|---|---|
| ✅ MATCH | Same meaning, compatible value type. Mechanical replacement. |
| ⚠ CONDITIONAL | Match only in some contexts, or value format must change (e.g. prose → IRI). |
| ✗ FALSE FRIEND | Same or close name, incompatible meaning or range. Do not map. |
| → NATIVE | No standard equivalent found. Stays in Family B (TSCG-native property). |

Name ≠ meaning: several keys split across verdicts depending on where they occur.

---

## 1. ✅ MATCH — mechanical (≈ 799 occ, 19 % of the gauge)

| Bare key | occ | Standard | Why it fits (source definition) | Where it occurs |
|---|---|---|---|---|
| `examples` / `example` | 177 + 12 | `skos:example` | SKOS note, no domain/range restriction | `m2:possibleValues` (103), `domains` (28) |
| `description` | 163 | `dcterms:description` | "An account of the resource", literal | `m2:possibleValues` (103), categories |
| `version` | 83 | `owl:versionInfo` | Annotation property, any construct, string | changelog entries (77), `metadata` (5) |
| `date` | 87 | `dcterms:date` | "Point or period of time associated with an event in the lifecycle of the resource" | changelog entries (77) |
| `changes` | 82 | `adms:versionNotes` | "Description of changes between this version and the previous version", literal | changelog entries (77) |
| `name` | 65 | `rdfs:label` | Human-readable name, literal | aspect / pole nodes |
| `alternative_names` | 22 | `skos:altLabel` | Sub-property of `rdfs:label`, plain literal | `m2:possibleValues` |
| `comment` | 22 | `rdfs:comment` | Human-readable description, literal | aspect nodes |
| `rationale` | 18 | `skos:note` | Generic SKOS note (nuance "justification" is lost — see §5 Q3) | `m2:examples`, amendments |
| `note` | 15 | `skos:note` | Generic SKOS note | various |
| `definition` | 13 | `skos:definition` | SKOS note sub-property | education constructs |
| `label` | 10 of 12 | `rdfs:label` | display name of the node | constraint poles, V levels, T0–T2 |
| `abbreviation` | 8 | `skos:notation` | "Lexical code uniquely identifying the concept within a scheme" (P/I/D in PID) | `m2:possibleValues` |
| `unit` | 5 of 6 | `schema:unitText` | "A string or text indicating the unit of measurement" | M1 Photography, Chemistry |
| `date_modified` / `date_created` | 5 + 4 | `dcterms:modified` / `dcterms:created` | Sub-properties of `dcterms:date`, literal | M2/M3 `metadata` |
| `title` | 3 | `dcterms:title` | "A name given to the resource" | M3 amendments |
| `id` | 3 | `dcterms:identifier` | "Unambiguous reference within a given context", literal | M3 amendments |
| `source` | 2 of 6 | `dcterms:source` | "Related resource from which the described resource is derived" | `m1:discoveryContext` |

**Correction to the earlier `version` concern**: in changelog entries the subject of
`owl:versionInfo` is the **entry node**, not the ontology node, so it does not collide
with the file's own `owl:versionInfo`. The three changelog fields map as a coherent
set: `version`→`owl:versionInfo`, `date`→`dcterms:date`, `changes`→`adms:versionNotes`.

## 2. ⚠ CONDITIONAL — decision or value reshaping needed (≈ 230 occ)

| Bare key | occ | Candidate | Condition / issue |
|---|---|---|---|
| `value` | 103 of 105 | `rdfs:label` (or `skos:prefLabel` if values become `skos:Concept`) | In `m2:possibleValues` it **names** the enumerated value. The 1 float in `m0:styling` → `rdf:value`. Currently classed B2 — moving this part to A is a decision. |
| `pros` / `cons` | 14 + 14 | `schema:positiveNotes` / `schema:negativeNotes` | Exact semantic fit ("pro/con lists"), Text allowed. schema.org domains are advisory (`domainIncludes` Product/Review). Alternative: keep native, since §4 of the scoping note puts pros/cons under documentation. |
| `system` / `instance` | 25 + 5 | `skos:example` | Items that *are* example systems in `domains` / `examples`. Merging loses the explicit "system" role. |
| `symbol` | 18 | `skos:notation` | `_^`, `_0`, `_$` are codes unique within the Base16 scheme — fits. But `m3:symbol` is already a B1 term in `M3_BicephalousPerspective`: pick one. |
| `use` / `usage` / `application` | 13 + 9 + 5 | `skos:scopeNote` (to confirm) | Typical applications / how used. Mixed: some `usage` values in M0 are implementation notes → `skos:note`. |
| `ontology` | 15 | `rdfs:isDefinedBy` | "Resource defining the subject resource" — fits the M1 extension registry, **only if** `"M1_Biology.jsonld"` becomes an IRI. |
| `see_also` | 3 | `rdfs:seeAlso` | Range `rdfs:Resource`: values mix a file name with prose → split IRI + comment. |
| `authors` | 4 | `dcterms:creator` (project convention) | `dcterms:creator` range is Agent; the project already writes it with a string. `dc:creator` (elements 1.1) has no range if strictness matters. |
| `supersedes` / `references` | 1 + 1 | `dcterms:replaces` / `dcterms:references` | Both expect non-literal values; current values are prose / citation strings. (`dcterms:bibliographicCitation` is **not** it: that cites the resource itself.) |
| `range` (M1) | 2 of 4 | `m2:valueRange` | "ISO 50-200" is a value interval → the property created in M2 16.20.0, not `rdfs:range`. The M3 `epistemicScore.range` stays as decided. |

## 3. ✗ FALSE FRIENDS — verified, do not map

| Bare key | occ | Tempting standard | Why it fails |
|---|---|---|---|
| `role` | 152 | `prov:hadRole` | Agent's role in an activity (see scoping note §2) |
| `status` | 145 | `adms:status` | Range `skos:Concept`, workflow maturity; TSCG status is an epistemic string |
| `domain` | 79 | `rdfs:domain` | Relates a **property** to a class; here it is a field of knowledge → native, ideally a link to `M1_Domains` |
| `type` | 30 | `rdf:type` | Range `rdfs:Class`; values are strings ("Formative", "Reset") |
| `notation` | 9 | `skos:notation` | Values are formulas / alphabet definitions, not identifying codes |
| `frequency` | 5 | `dcterms:accrualPeriodicity` | Frequency of additions to a collection |
| `culture` | 10 | `dcterms:coverage` | Spatial/temporal/jurisdiction, not a cultural tradition |
| `source` | 4 of 6 | `dcterms:source` | Source of a **flow** ("F_active") or domain of a morphism (`dom(f)`) |
| `unit` | 1 of 6 | `schema:unitText` | M3 `η: Id_C ⇒ G∘F` is the category-theory unit (natural transformation) |
| `label` | 2 of 12 | `rdfs:label` | M0 UX entries describe a UI field specification, not the node's name |
| `latitude` | 3 | geo latitude | Exposure latitude in photography (±stops) |
| `identity` | 2 | — | Identity morphism `id_A`, category theory |
| `agent` | 5 | `dcterms:Agent` / PROV agent | Prose about a mythic figure's behaviour |

## 4. → NATIVE (Family B) — confirmed no standard

Dominant: `formula` 137, `basis` 116, `characteristics` 65, `formulaPrimary` 36,
`contribution` 30, `semantics` 22, `count` 17, `territory` 17, `map` 16,
`namespace` 15, `mechanism` 14, `validated` / `actualDomains` 11, `M0_instance(s)` 16,
`vs_*` distinctions, and the M1 domain-specific fields (mythology, photography,
education…). Plus the long tail (869 singletons) — needs the fallback rule of §4 of
the scoping note (`m3:documentation` container).

## 5. Decisions for Michel

1. Approve §1 as **lot 1** (≈ 799 occ, mechanical, context-guarded where marked "x of n").
2. Changelog trio (`version` / `date` / `changes`, 77 entries each) — ship in lot 1, or as its own commit?
3. `rationale`: accept `skos:note` (nuance lost) or keep native?
4. §2, one line at a time — in particular `value` (moves 103 occ from B2 to A),
   `pros`/`cons` (schema.org vs documentation container), `symbol` (`skos:notation` vs `m3:symbol`).
5. Tooling: `tscg_metrics.py` `STANDARD_REPLACEABLE` maps `source` and `label`
   unconditionally (wrong in 4 + 2 cases) and lacks `changes`, `abbreviation`,
   `date_created`/`date_modified`, `id`, `unit` — align it with the approved table.

## Sources (fetched 2026-09-30)

- DCMI Metadata Terms — https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
- SKOS Reference — https://www.w3.org/TR/skos-reference/
- RDF Schema 1.1 — https://www.w3.org/TR/rdf-schema/
- OWL Web Ontology Language Reference — https://www.w3.org/TR/owl-ref/
- ADMS — https://www.w3.org/TR/vocab-adms/
- schema.org — https://schema.org/positiveNotes, https://schema.org/unitText
| 1c | changelog entries: `version` → `owl:versionInfo`, `date` → `dcterms:date`, `changes` → `adms:versionNotes` | DONE 2026-09-30 | 246 keys in 82 entries of `m1:`/`m2:`/`m3:changelog` lists (24 files); **ADMS accepted as external vocabulary** (Michel), prefix `adms` declared in the 24 contexts, decision recorded in the `m3:changelog` declaration; all 86 entries now graph-visible (adms:versionNotes 0 → 86); new entries are written in the new form, so the +9-per-lot drift stops; legacy forms (maps keyed by version, `metadata`, `changelogLegacy`, a string entry in M1_Mythology) left for the "vestiges" lot; VOC gauge 3832 → 3586; gate PASS, golden unchanged |
| 1d | container: `m1:changelog` / `m2:changelog` → `m3:changelog` (declared in M3_GrammarFoundation since 2026-07-22) + tools (check_M1 ONT007, M1 and M0 SHACL) | TODO | option (A), Michel 2026-09-30 |

> **Note on the gauge**: each lot adds changelog entries whose own keys (`version`, `date`, `changes`) are still bare — about +9 per lot until the changelog trio line is done (done in lot 1c: the drift has stopped).
