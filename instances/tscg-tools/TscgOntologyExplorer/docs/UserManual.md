# TscgOntologyExplorer — User's Manual

**Version:** 1.1 | **Author:** Echopraxium with the collaboration of Claude AI

---

## Introduction

TscgOntologyExplorer is a specialized ontology browser built for the **TSCG framework** (Transdisciplinary System Construction Game). It provides a structured view of TSCG ontologies across the four modeling layers, with integrated SPARQL querying, property inspection, and cross-navigation between concepts.

> TscgOntologyExplorer is read-only by design — it is an *explorer*, not an editor. It loads JSON-LD ontology files from your local TSCG repository and provides navigation, search, and query capabilities.

### Key Capabilities

- Browse the **class hierarchy** of any TSCG ontology layer
- Inspect **real property values** fetched from the Python bridge
- Navigate between concepts via **clickable IRI chips**
- Query any loaded ontology with **SPARQL** (predefined or custom)
- Explore **imports and namespace prefixes** of each ontology
- Search objects with **full regex support**
- Export ontologies as **Turtle (.ttl)** or other RDF formats

---

## TSCG Architecture

TSCG organizes knowledge into four hierarchical *meta-levels*, from the most abstract (M3) to the most concrete (M0):

| Layer | Name | Description |
|-------|------|-------------|
| **M3** | Genesis Grammar | Structural primitives — type atoms A,S,F,I,D,R,E,V,O,I |
| **M2** | Generic Concepts | ~80 transdisciplinary concepts with structural formulas |
| **M1** | Domain Extensions | Biology, Physics, Economics… specializing M2 concepts |
| **M0** | Instances (Poclets) | Concrete systems with ASFID/REVOI scores |

```
M3  →  M2  →  M1  →  M0
(Genesis)  (Concepts)  (Domains)  (Instances)
```

Each layer *imports* the one above it. An M0 Poclet references M1 domain concepts, which in turn specialize M2 Generic Concepts, which are typed by M3 structural primitives.

---

## M3 — Genesis Grammar

M3 defines the **Structural Grammar** of TSCG — the primitive type atoms from which all higher-level concepts are composed. It is grounded in **Lambek Calculus** and **free commutative monoidal categories**.

### ASFID — Territory Grammar (Eagle Eye)

Five dimensions describing systems as they *are* (ontological perspective):

| Atom | Dimension | Role |
|------|-----------|------|
| A | Attractor | Stability basins, convergence tendencies |
| S | Structure | Architectural organization, bonds |
| F | Flow | Exchange, circulation, openness |
| I | Information | Patterns, codes, signals |
| D | Dynamics | Change, transformation, time evolution |

### REVOI — Map Grammar (Sphinx Eye)

Five dimensions describing systems as they are *represented* (epistemic perspective):

| Atom | Dimension | Role |
|------|-----------|------|
| R | Representable | Can be formally modeled |
| E | Evolvable | Model can be updated over time |
| V | Verifiable | Empirically testable predictions |
| O | Observable | Measurable outputs exist |
| I | Interoperable | Integrates with other models |

### Monoidal Composition

Concepts are composed using the **monoidal product ⊗** — not a tensor product (no scalar multiplication or metric required):

```
Memory  =  S ⊗ I ⊗ D        (Structure ⊗ Information ⊗ Dynamics)
```

### M3 Files

- `M3_GenesisGrammar.jsonld` — Core grammar, M3Dimension class, dimension symbols
- `M3_EagleEye.jsonld` — ASFID properties (physicalInterpretation, rangeAnalog…)
- `M3_SphinxEye.jsonld` — REVOI properties
- `M3_GrammarFoundation.jsonld` — Base grammar classes

---

## M2 — Generic Concepts

M2 contains ~80 **transdisciplinary GenericConcepts** — patterns that appear across multiple domains. Each concept has a structural formula expressing its ASFID/REVOI composition.

### Concept Families

| Family | Examples |
|--------|----------|
| Structural | Hierarchy, Network, Modularity, Topology |
| Dynamic | Process, Trajectory, Bifurcation, Emergence |
| Regulatory | Regulation, FeedbackLoop, Homeostasis |
| Adaptive | Adaptation, Resilience, Self-Organization |
| Energetic | Dissipation, Entropy, Transducer |
| Informational | Code, Signal, Language, Pattern |
| Ontological | Identity, System, Observer, Environment |
| Teleonomic | Goal, Behavior, Workflow, Action |
| Relational | Relation, Link, Channel, Mediator |

### ConceptContracts

Behavioral interfaces that a GenericConcept can fulfill via `m2:implements`:

- **Composable** — can participate in part-whole relations
- **Observable** — has measurable outputs
- **Stateful** — maintains internal state
- **Triggerable** — can be activated by external events

### Structural Grammar Properties

| Property | Content | Example |
|----------|---------|---------|
| `hasStructuralGrammarFormula` | Unicode monoidal expression | `S ⊗ I ⊗ D` |
| `hasStructuralGrammarFormulaTeX` | LaTeX rendering | `S \otimes I \otimes D` |
| `hasStructuralGrammarFormulaRawText` | ASCII-safe | `S (x) I (x) D` |

---

## M1 — Domain Extensions

M1 files specialize M2 Generic Concepts for specific knowledge domains. Each extension is in its own subfolder under `ontology/M1_extensions/`.

### Available Extensions

Biology · Chemistry · Economics · Education · Electronics · Energy Generators · Geology · Music · Mythology · Optics · Photography · Physics · Systemic Modeling

### Loading M1 Extensions

Click the **M1** button in the toolbar. A dropdown appears with `M1_CoreConcepts` at the top (★) and all domain extensions below. Each opens as a new document tab.

> Extensions are discovered automatically — add a new `.jsonld` file in a subfolder of `M1_extensions/` and it appears in the dropdown on next launch.

---

## M0 — Instances (Poclets)

M0 contains concrete system models called **Poclets** (Proof-of-Concept + -let). A Poclet models a real-world system by assigning ASFID and REVOI scores and linking to M1/M2 concepts.

### Epistemic Gap δ₁

The epistemic gap measures how well the Map (REVOI) captures the Territory (ASFID):

```
δ₁  =  ‖ ASFID_scores − REVOI_scores ‖  ∈ [0, 1]
```

A small δ₁ means the model accurately represents the system. A large δ₁ signals modeling gaps.

> δ₁ is computed *per instance* at M0 level. It is NOT a fixed property of M2 Generic Concepts.

---

## JSON-LD Format

TSCG ontologies are stored as **JSON-LD files** (.jsonld). JSON-LD is JSON with a semantic layer — it maps compact keys to full IRIs and enables RDF/SPARQL processing.

### @context — Namespace Prefixes

The `@context` object defines shorthand prefixes for long URIs:

```json
"@context": {
  "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
  "m2":   "M2_GenericConcepts.jsonld#",
  "m3":   "M3_GenesisGrammar.jsonld#",
  "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
  "owl":  "http://www.w3.org/2002/07/owl#"
}
```

### @graph — Concept Nodes

Each concept is a JSON object inside the `@graph` array:

```json
{
  "@id":   "m2:Memory",
  "@type": "owl:Class",
  "rdfs:label": "Memory",
  "rdfs:subClassOf": { "@id": "m2:GenericConcept" },
  "m2:hasStructuralGrammarFormula": "S ⊗ I ⊗ D",
  "m2:hasFamily": "m2:Dynamic",
  "m2:implements": { "@id": "m2:Stateful" }
}
```

---

## Object Explorer

The leftmost panel shows the hierarchy of objects in the active ontology document.

```
┌─ OBJECT EXPLORER ──────────────────────────┐
│ ⬡ Classes                          ▼      │  ← Mode selector
├──────────────────────────────────────────┤
│ Show group…              [✕ All]          │  ← Group filter
├──────────────────────────────────────────┤
│ ▼ owl:Thing                               │
│   ▼ GenericConcept                        │
│     ▶ Bifurcation                         │
│       Coherence                           │
│       Memory                              │
└──────────────────────────────────────────┘
```

### Mode Selector

The dropdown at the top switches between different object types:

- **⬡ Classes** — shows `owl:Class` hierarchy via `rdfs:subClassOf` (default)
- **⬡ ObjectProperty** — flat list of object properties
- **⬡ DatatypeProperty** — flat list of datatype properties
- **⬡ NamedIndividual** — flat list of named individuals

For ontologies with no `owl:Class` nodes (e.g. M3_EagleEye), the first available type is selected automatically.

### Group Filter

In Classes mode, the second dropdown filters by Level-1 group. Select multiple groups — they appear as colored pills. Click **✕ All** to clear.

### Search — `Ctrl+F`

Opens the inline search bar. The tree filters in real time, expanding all collapsed nodes automatically. Three search modes:

| Query | Behavior | Example |
|-------|----------|---------|
| `memory` | Case-insensitive contains | Finds Memory, MemoryCell… |
| `^Me` | Starts with | Memory, Mediator, Modularity… |
| `loop$` | Ends with | FeedbackLoop |
| `/^[A-Z]{2}/` | Explicit regex | Names starting with 2 capitals |

The first match is auto-selected and scrolled into view. Press `Esc` to close.

---

## Property Inspector

Click any object in the Explorer to load its properties. Values come directly from the Python bridge parsing the JSON-LD file.

### IRI Chips

Property values that are IRIs within the *current document* appear as **clickable chips**:

- **Click** → navigates to that object in the Explorer tree (expanding collapsed nodes if needed)
- **Hover** → shows the full IRI as tooltip

### Complex Values (Blank Nodes)

Anonymous nested objects (JSON-LD blank nodes) are expanded inline as `key: value | key: value` pairs.

---

## Imports Tab

Shows all dependencies of the active ontology document.

### @context Namespaces

Each prefix defined in `@context` appears as a chip. Click to:

- **Internal TSCG prefix** (violet chip) → loads that ontology as a new document tab
- **External prefix** (grey chip) → opens in browser

### owl:imports

Explicit OWL imports appear as chips showing the filename stem. Click → loads the imported file.

---

## SPARQL Panel

The rightmost tab provides a full SPARQL 1.1 query editor against the active ontology.

### Predefined Queries

| Category | Examples |
|----------|---------|
| 🔍 Exploration | List classes, properties, all triples |
| ⬡ M2 GenericConcepts | By family, structural formulas, dual polarity |
| 🦅 M3 Dimensions | ASFID and REVOI dimension lists |
| 📦 M0 Instances | Poclets, ASFID scores |
| 🔧 Utilities | Named graphs, imports, ontology metadata |

### Save As…

After a successful query, **Save As…** exports results:

- **SELECT** queries → `SPARQL_OUTPUT_<timestamp>.csv`
- **CONSTRUCT** queries → `SPARQL_OUTPUT_<timestamp>.ttl`

Files are saved to `instances/tscg-tools/TscgOntologyExplorer/output/`.

---

## Export

Use **File → Export As…** (`Ctrl+Shift+E`) to export the active ontology:

| Format | Extension | Use case |
|--------|-----------|---------|
| Turtle | .ttl | Protégé, OWL tools — recommended |
| RDF/XML | .rdf | Broad OWL compatibility |
| N-Triples | .nt | Simple line-by-line RDF |
| JSON-LD | .jsonld | Re-export with absolute IRIs |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Find in Object Explorer |
| `Esc` | Close search bar / close dropdown |
| `Ctrl+Shift+E` | Export As… |
| `F1` | User's Manual |
| `Ctrl+,` | Preferences |

---

## SPARQL Quick Reference

### List all GenericConcepts with formulas

```sparql
PREFIX m2: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?concept ?label ?formula WHERE {
  ?concept rdfs:subClassOf+ m2:GenericConcept .
  ?concept m2:hasStructuralGrammarFormula ?formula .
  OPTIONAL { ?concept rdfs:label ?label }
} ORDER BY ?label
```

### Concepts by family

```sparql
SELECT ?family (COUNT(?c) AS ?count) WHERE {
  ?c rdfs:subClassOf+ m2:GenericConcept .
  ?c m2:hasFamily ?family .
} GROUP BY ?family ORDER BY DESC(?count)
```

### All triples for a specific concept

```sparql
SELECT ?p ?o WHERE {
  <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#Memory>
  ?p ?o .
}
```

---

*TscgOntologyExplorer — Echopraxium with the collaboration of Claude AI — 2026*
