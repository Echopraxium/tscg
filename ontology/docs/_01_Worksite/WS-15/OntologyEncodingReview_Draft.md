# Ontology Encoding Review — draft 0.1.0

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-11-16
**Measured on**: HEAD `97af180`
**Worksite**: WS-15 SF-7 (reuse existing vocabularies)
**Status**: approach approved by Michel on 2026-11-16. The pointers of §2 and the fate of
each finding of §3 remain Michel's decisions, taken one by one; until then every verdict
below is a proposal.

## 0. What this is

A review of **how TSCG encodes its content with external vocabularies**: for each term
used, does the use match what the vocabulary's specification says? It is the practice the
literature calls *ontology evaluation* or *vocabulary reuse assessment*; OOPS! (pitfall
scanner) and FOOPS! (FAIR checks) automate part of it. This review is a first manual pass,
limited to the external terms; it does not judge TSCG's own terms.

It has two outputs:
1. **Examples** for the Semweb atlas: one pointer per vocabulary to a node that shows good
   use. The atlas build will read the node at HEAD; nothing is copied here.
2. **Findings**: uses that depart from the specification, each with a proposed option.

**Scope**: `ontology/*.jsonld`, `ontology/M1_extensions/`, `ontology/TSCG_InstanceGrammar/`,
`ontology/InstanceSimulations/`, `instances/**/M0_*.jsonld`; backups and `_archives/`
excluded. Counts come from `git grep` on the scope above; re-run before quoting them.

## 1. Inventory of external terms (HEAD `97af180`)

| Vocabulary | Terms used (occurrences) |
|---|---|
| RDF | `rdf:type` as an explicit key (2); otherwise `@type` |
| RDFS | label (1258), comment (896), subClassOf (382), domain (106), range (104), seeAlso (49), isDefinedBy (37), subPropertyOf (28) |
| OWL | Class (438), versionInfo (289), NamedIndividual (174), Ontology (93), DatatypeProperty (72), AnnotationProperty (69), imports (64), ObjectProperty (43), deprecated (42), Thing (6), inverseOf (4), oneOf (3), SymmetricProperty (2), equivalentClass (1) |
| XSD | float (321), string (53), boolean (4), integer (3), double (1) |
| SHACL | only in the gate's shape files (`ontology/toolchain/check-M0`, `check-M1`, `check-M2`, `grammars/`) |
| SKOS | example (219), definition (90), altLabel (47), note (39), Concept (23), scopeNote (19), inScheme (14), notation (12), prefLabel (12), topConceptOf (12), closeMatch (12), broader (10), related (9), ConceptScheme (5), editorialNote (3), Collection, member, hasTopConcept, changeNote (2 each) |
| DCTerms | created (331), creator (274), date (223), description (216), modified (66), title (23), references (13), format (11), type (11), **documentation (7)**, identifier (4), source (3), requires (2), subject (1) |
| ADMS | versionNotes (220) |
| schema.org | value (15) |
| PROV-O, DCAT, FOAF | not used |

## 2. Proposed examples for the atlas (good use)

| Vocabulary | Pointer (file → node) | What it shows |
|---|---|---|
| RDFS | `M2_GenericConcepts.jsonld` → `m2:Process` | label, comment, subClassOf on a generic concept |
| OWL | `M0_Common.jsonld` → a node carrying `owl:deprecated` | deprecation instead of deletion (WS-15 step 1) |
| OWL | any M0 `owl:Ontology` node → `owl:imports` | imports only TSCG's own layers, never an external vocabulary (project rule) |
| SKOS | `M3_GenesisGrammar.jsonld` → `m3:Audience` | a facet as a `skos:ConceptScheme`, its values as `skos:Concept` |
| SKOS | `M1_Domains.jsonld` → a domain with `skos:closeMatch` to OpenAlex | alignment to an external classification — the reuse rule at work |
| DCTerms | any `owl:Ontology` node | created / modified / description as file metadata |
| ADMS | any `m3:changelog` entry | `adms:versionNotes` with `owl:versionInfo` and `dcterms:date` |
| XSD | a typed literal (`"@type": "xsd:…"`) | datatypes on literals |
| SHACL | `ontology/toolchain/check-M0/M0_Instances_Schema_shacl.ttl` | SHACL as a gate, not a definer |
| RDF | `@type` on any node | JSON-LD writes `rdf:type` as `@type` |

Michel to confirm or replace each pointer. The atlas would show the current node, a link
to the file, and say so if a pointer stops resolving.

## 3. Findings (uses that depart from the specification)

Severity: **error** = breaks a rule stated by the specification; **deviation** = outside
the specification's intent, harmless for parsers; **style** = inconsistency, no semantic
effect. Specification statements are given as I understand them and must be checked
against the cited text before any change.

| # | Finding | Where (count) | Severity | Options (Michel decides) |
|---|---|---|---|---|
| E1 | `skos:broader` and `skos:related` point to the same concept. SKOS integrity condition S27: `skos:related` is disjoint with `skos:broaderTransitive`. | `M3_GrammarFoundation.jsonld`: `m3:GenesisExtension` → `m3:Genesis`, `m3:TransDisclet` → `m3:Poclet` (2) | error | drop `skos:related` where `skos:broader` holds |
| E2 | `dcterms:documentation` is not a DCMI term (no such property in the `dcterms:` namespace). Its links also point to `ontology/poclets/ColorSynthesis/…`, a folder that does not exist (the files are under `instances/poclets/ColorSynthesis/`). | `M0_ColorSynthesis.jsonld` (7) | error | `rdfs:seeAlso` or `dcterms:hasPart` / `dcterms:references`, path fixed |
| D1 | `dcterms:creator` with a plain string. DCMI gives `dcterms:creator` the range `dcterms:Agent` (a resource, not a literal); `dc:creator` (elements 1.1) is the literal-friendly variant. | almost every file (273) | deviation | (a) keep, and record the choice; (b) switch to `dc:creator`; (c) one agent node `Echopraxium` referenced by IRI. (a) costs nothing; (c) is the cleanest |
| D2 | `schema:value` inside `skos:example` nodes. In schema.org, `value` is the value of a `QuantitativeValue` / `PropertyValue`, not an example text. | `M2_GenericConcepts` (9), `M1_Chemistry` (5), `M3_GrammarFoundation` (1) | deviation | plain strings in `skos:example` (as in the 200+ other uses), or `rdf:value` |
| D3 | `owl:Class` nodes also placed in a SKOS hierarchy (`skos:broader`, `skos:inScheme`, `skos:topConceptOf`): a class used as a concept (OWL 2 punning). Legal in OWL 2 DL, but the class tree and the concept tree then say two things about the same IRI. | `M3_GrammarFoundation.jsonld` (11 nodes) | deviation | keep (document the punning) or separate the category concepts from the classes; a modelling decision |
| D4 | Dates as untyped strings (`"dcterms:created": "2026-09-30"`). DCMI recommends W3CDTF; a typed `xsd:date` lets tools sort and compare. | `created`, `date`, `modified` (≈ 620) | style | type them in a scripted lot, or leave |
| S1 | `owl:imports` written two ways: relative (`"M2_GenericConcepts.jsonld"`, resolved against `@base`) and absolute raw URL. | 64 imports, both forms | style | one form; to decide with the persistent-IRI question (w3id, see 2026-10-26 arbitration sheet §4) |
| S2 | `rdf:type` written as an explicit key next to `@type`. | `M0_FourStrokeEngine`, `M0_Counterpoint` (2) | style | fold into `@type` |
| R1 | Score aliases (`A_score` … typed `xsd:float`) still declared in the `@context` of M0 instances, after their uses were deleted. | most M0 files (≈ 20 lines each) | — | **routed to WS-15** (SF-1/SF-2), not judged here |

Not findings: `adms:versionNotes` on changelog entry nodes (ADMS defines it for assets; the
extension to a version note is in its spirit); `owl:Thing` as a superclass (redundant but
harmless); SHACL confined to the gate (matches the project rule).

## 4. Next steps (proposals)

1. Michel: confirm the pointers of §2; decide E1, E2 (they look like plain corrections), and
   choose an option for D1–D4, S1, S2.
2. Claude: the atlas build reads the pointers at HEAD (a `semweb_examples.yaml` next to
   the atlas, owned by Michel) and shows them in each vocabulary sheet.
3. Corrections chosen in step 1 go through the diagnosis pipeline, one lot each; E1 and E2
   touch M3 and M0 files, so the reasoner runs on each changed file.
4. Later, once the WS-10 file-level defects are gone: run OOPS! and FOOPS! as an outside
   check of this review.
