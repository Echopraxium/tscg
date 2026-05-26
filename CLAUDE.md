# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TSCG (Transdisciplinary System Construction Game)** is a transdisciplinary framework for modeling complex systems using a unified ontological "construction kit." The metaphor is LEGO Technic: reusable conceptual blocks that snap together across biology, chemistry, engineering, mythology, and social sciences. The philosophical basis is Korzybski's "The map is not the territory."

Research preprint: DOI [10.5281/zenodo.18471860](https://doi.org/10.5281/zenodo.18471860) (v3.0, published). Version 4.0 (~11,300 words) is complete and pending Zenodo submission.

## Common Commands

No build system is currently configured. Key scripts to run directly:

```bash
# Generate file URIs for the project
python create_files_URIS.py

# Build RAG vector database (run from src/tscg/rag/)
python src/tscg/rag/create_tscg_rag.py local

# Query RAG database — single shot or interactive
python src/tscg/rag/query_tscg_rag.py "What is ASFID?"
python src/tscg/rag/query_tscg_rag.py --interactive

# SPARQL analysis on M2 GenericConcepts
python ontology/sparql/m2_sparql_analysis.py

# Generate gallery index for simulations
node generate_index.js
```

The Python engine in `src/` is a namespace package (PEP 420). Planned install variants (not yet configured):
- `pip install -e .` — engine only
- `pip install -e .[cli]` — + REPL
- `pip install -e .[full]` — + WebAPI

## Architecture: The Four-Layer Ontological Stack

Every artifact in this repo belongs to one of four layers (M0–M3). This is the most important concept to internalize:

| Layer | Name | Description | Location |
|-------|------|-------------|----------|
| **M3** | Genesis Space | 10D bicephalous basis — the universal meta-framework | `ontology/M3_*.jsonld/.ttl` |
| **M2** | GenericConcepts | 80 atomic transdisciplinary patterns across 9 families | `ontology/M2_GenericConcepts.jsonld` |
| **M1** | Core/Domain Concepts | Domain-specific concept extensions (biology, chemistry, etc.) | `ontology/M1_*.jsonld`, `ontology/M1_extensions/` |
| **M0** | Instances | Poclets, TscgTools, SystemicFrameworks, SymbolicSystemGrammars | `instances/*/` |

### M3: The Bicephalous Basis

M3 is split into two complementary perspectives that together form a 10-dimensional space:
- **ASFID (Eagle Eye / Territory)**: Attractor, Structure, Flow, Information, Dynamics — what a system *is*
- **REVOI (Sphinx Eye / Map)**: Representability, Evolvability, Verifiability, Observability, Interoperability — how a system is *known*

**CRITICAL**: The R in REVOI stands for **Representability** (NEVER Reproducibility).

Files:
- `M3_GenesisSpace.jsonld` — Unified bicephalous foundation with coupling matrices
- `M3_EagleEye.jsonld` — ASFID dimension definitions
- `M3_SphinxEye.jsonld` — REVOI dimension definitions

### M2: GenericConcept Organization

80 atomic transdisciplinary GenericConcepts organized into 9 families:
- **Ontological**: fundamental existence patterns
- **Structural**: organizational patterns
- **Dynamic**: change and process patterns
- **Control**: regulation and feedback patterns
- **Information**: knowledge and representation patterns
- **Emergence**: self-organization and phase transitions
- **Boundary**: interface and containment patterns
- **Temporal**: time and rhythm patterns
- **Relational**: connection and interaction patterns

The Combo family has been **removed from M2** and migrated to M1 (now hosted in `M1_CoreConcepts.jsonld` as `m2:GenericConceptCombo` and `m2:KnowledgeFieldConceptCombo` instances).

The production file is `M2_GenericConcepts.jsonld`. Draft/experimental work lives in `ontology/docs/`.

### M1: Domain Extensions

Domain-specific concept extensions that specialize M2 GenericConcepts:
- `M1_CoreConcepts.jsonld` — Hosts all GenericConceptCombo and KnowledgeFieldConceptCombo instances
- `M1_Biology.jsonld`, `M1_Chemistry.jsonld`, `M1_Physics.jsonld`, etc. — Domain vocabularies
- All M1 extensions stored in: `ontology/M1_extensions/<domain>/M1_<Domain>.jsonld`

### M0: Instances

**Instance types** (declared via `m3:ontologyType`):
- **Poclets** (`m3:Poclet`) — Minimal, complete, validated models of real systems (23+ validated poclets spanning chemistry, physics, biology, music, electronics, economics, mythology, education, governance)
- **TscgTools** (`m3:TscgTool`) — Meta-analytical and development tools (TscgPocletMiner, Tscg3DModeler, TscgExplorer)
- **SystemicFrameworks** (`m3:SystemicFramework`) — Cybernetic and systemic modeling frameworks (VSM)
- **SymbolicSystemGrammars** (`m3:SymbolicSystemGrammar`) — Formal symbolic systems (I Ching)
- **TransDisclets** (`m3:TransDisclet`) — Transdisciplinary conceptual bridges

Each instance lives in its own directory under `instances/<type>/<name>/` with dual-format files (`M0_*.jsonld` + `M0_*.ttl`).

## File Format Conventions

### Ontology Files
- All ontologies are maintained in **dual format**: `.jsonld` (JSON-LD) and `.ttl` (RDF/Turtle)
- File naming follows the layer prefix: `M3_`, `M2_`, `M1_`, `M0_`
- **RDF namespace base**: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`
- **@base convention**: All M0, M1, M2, M3 ontologies use `"@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"` for shorter IRIs
- **Authorship**: All generated ontology files authored as `"Echopraxium with the collaboration of Claude AI"`
- **Changelog**: Keep only the 3 most recent entries in `m2:changelog`
- SPARQL queries are in `ontology/sparql/`

### Critical Ontology Rules
- **ontologyType declaration**: Use ONLY `m3:ontologyType` property (never `tscg:` namespace, never `m2:ontologyCategory`)
- **M1 extension references**: Use format `"M1_extensions/<domain>/M1_<Domain>.jsonld"` (e.g., `"M1_extensions/biology/M1_Biology.jsonld"`)
- **No JSON-LD comments**: Comments forbidden in `.jsonld` files; use `.ttl` format for commented versions
- **SHACL naming**: Use dot separator before "shacl" extension (e.g., `M0_Instances_Schema.shacl.ttl`)

### Simulation Files
- **BabylonJS version**: 6.26.0 is the exclusive 3D library for TSCG simulations
- **CDN**: Use `unpkg.com/babylonjs@6.26.0/babylon.js` (not cdn.babylonjs.com)
- **UX Controls catalog**: Consult `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld` before implementing UI patterns
- **Reference layouts**: `M0_FireTriangle.html`, `MtgColorWheel_sim.html` for BabylonJS patterns

## Python Engine Architecture (`src/`)

Detailed spec in `src/ARCHITECTURE_GUIDE.md` (~1000 lines). The authoritative source of truth for all design decisions.

The public API is exposed exclusively through facades — internal modules must never be imported directly by application code:

```python
from tscg.engine.facade import OntologyFacade, QueryFacade, MetricsFacade, ExportFacade, RAGFacade
```

### `engine/core/`

**`models.py`** — Pydantic data models for all TSCG domain entities:
- `ASFIDScore` / `REVOIScore` — 5-float score objects (values 0.0–1.0) with an `overall` property (mean)
- `Metaconcept` — URI, label, layer (`M3`/`M2`/`M1`), perspective (`ASFID`/`REVOI`), tensor formula
- `Poclet` — Named system instance with domain, description, `ASFIDScore`, `REVOIScore`
- `OntologyMetadata` — File-level metadata (name, format, layer, triple count)

**`ontology_loader.py`** — `OntologyLoader`: parses JSON-LD files via rdflib, extracts metadata and metaconcepts, stores multiple graphs by name. Layer is inferred from filename prefix (`M3_`, `M2_`, etc.).

### `engine/facade/`

The stable public API layer. Each facade is a thin wrapper delegating to the internal module below it.

| Facade | Wraps | Key methods |
|--------|-------|-------------|
| `OntologyFacade` | `OntologyLoader` | `load(path)`, `get_graph(name)`, `list_loaded()`, `get_metaconcepts(layer, perspective)` |
| `QueryFacade` | `SPARQLExecutor` | `set_graph(g)`, `execute(query, use_cache)`, `find_metaconcepts(layer)`, `find_related(uri)` |
| `MetricsFacade` | `OrthogonalityAnalyzer` | `compute_orthogonality(scores_dict)`, `asfid_orthogonality(asfid)`, `revoi_orthogonality(revoi)` |
| `ExportFacade` | `TurtleExporter` | `to_turtle(graph, path, prefixes)`, `to_file(graph, path, format)` |
| `RAGFacade` | `OntologyRetriever` + `MetaconceptRetriever` | `index_ontology(loader)`, `search(query)`, `search_metaconcepts(query)`, `find_similar(uri)` |

### `engine/analysis/`

**`sparql/executor.py`** — `SPARQLExecutor`: executes SPARQL against an rdflib graph with hash-based query caching. Returns `SPARQLResult` (bindings as string dicts, variable list, row count). Pre-built queries: `query_metaconcepts()`, `query_triples_by_subject()`.

**`metrics/orthogonality.py`** — `OrthogonalityAnalyzer`: computes cosine-similarity matrices between dimension score vectors. Returns `OrthogonalityReport` with full similarity matrix, most/least orthogonal pairs, average orthogonality (1 − avg similarity), and condition number.

### `engine/exporters/`

**`turtle_exporter.py`** — `TurtleExporter`: serialises an rdflib Graph to Turtle format, binding standard W3C and TSCG-specific namespaces automatically. Returns `ExportResult` dataclass.

### `engine/rag/`

Three-module RAG stack, composed by `RAGFacade`:

- **`embeddings.py`** — `TSCGEmbedder`: wraps `sentence-transformers/all-MiniLM-L6-v2` (384-dim). Lazy-loads the model on first call. Provides `embed_text()`, `embed_metaconcept()` (label + definition + formula + layer), `embed_poclet()`, `embed_asfid/revoi()` (numeric vectors).
- **`vector_store.py`** — `VectorStore`: in-memory numpy arrays with cosine-similarity search. Persists via `.npz` + `.json` sidecar. Returns `SearchResult` (id, score, metadata).
- **`retrieval.py`** — Two retrievers:
  - `OntologyRetriever`: indexes an entire loaded ontology; filters by layer/perspective at search time
  - `MetaconceptRetriever`: specialized for `Metaconcept` objects; supports `search_by_formula(pattern)`

### `cli/`

**`repl/context.py`** — `ReplContext`: holds the active REPL session — one instance of each facade, the currently selected ontology name, session variables, and command history. Only ever calls facade APIs.

**`repl/interpreter.py`** — `TSCGRepl`: prompt-toolkit REPL with rich terminal UI. Commands: `load`, `show`, `export`, `sparql`, `metrics orthogonality`, `context`, `clear`, `exit`.

### `ontology_tools/`

**`jsonld_to_turtle.py`** — `JSONLDToTurtleConverter`: batch-converts all `.jsonld` files in `ontology/` and `instances/` to `.ttl`, preserving directory structure. Supports dry-run mode and skip-on-error. This is the canonical tool for keeping dual-format files in sync.

### `rag/` (top-level, separate from `engine/rag/`)

**`create_tscg_rag.py`** — Builds the ChromaDB vector database from all 350+ repository files. Run from `src/tscg/rag/`. Key behaviours:
- Repo root is resolved from `__file__` (not CWD) so it works from any directory
- Deduplicates segments with identical content at index time (content-hash)
- Compresses the finished DB to `db_tscg_rag.tar.gz` by default (`--no-compress` to skip)
- `--no-compress` to skip compression; `--verbose` for per-file progress

Segmentation strategies by file type:

| File type | Strategy |
|-----------|----------|
| `.jsonld` | Per `@graph` entry, converted to **natural language summary** (label, definition, tensor formula, M3 dimensions, examples). OWL infrastructure entries (properties, ontology headers) are skipped. |
| `.ttl` | Per triple block (subject changed) with context preservation |
| `.md` | Per heading (level 2+) with context preservation from parent headings |
| `.py` | Per function/class definition with docstrings |
| `.html` | Per structural block (heading + following paragraph) |
| `.js` | Per function definition |

Guide: `src/tscg/rag/TSCG_RAG_Segmentation_Guide.md`.

**`query_tscg_rag.py`** — CLI for querying the vector DB. Two modes:
- Single-shot: `python query_tscg_rag.py "What is a poclet?"`
- Interactive REPL: `python query_tscg_rag.py --interactive`

Both load `db_tscg_rag/` if it exists, or extract from `db_tscg_rag.tar.gz` if needed. Interactive mode supports commands:
- `context` — show retrieval settings
- `set k=N` / `set threshold=X` — adjust parameters
- `reload` — refresh embeddings from disk
- `clear` — clear screen
- `exit` / Ctrl-D — quit

## Methodological Guides

Reference documents for TSCG development workflows:

### Framework Development
- **`TSCG_Smart_Prompt_v16_0_0.md`** — Current framework version snapshot for Claude context initialization
- **`00_TSCG_M3_Bicephalous_Architecture.md`** — Theoretical foundation of the dual-headed M3 (Map/Territory)
- **`00_TSCG_Map_Territory_Theoretical_Foundation.md`** — Korzybski philosophical basis
- **`Structural_Grammar_Foundation.md`** — Lambek calculus foundation (replaces tensor product interpretation)

### Instance Development
- **`Poclet_Analysis_Methodology.md`** — Step-by-step poclet analysis heuristic
- **`HYBRID_FORMULAS_NOTATION_README.md`** — Formula encoding conventions (It/Im, REVOI standard)
- **`TSCG_ValueSpace_User_Guide.md`** — How to use ValueSpace attributes in instantiations
- **`TSCG_ValueSpace_Quick_Reference.md`** — Cheat sheet for all 13 ValueSpace attributes

### Ontology Management
- **`Domain_M2_Update_Analysis_v15_1_0.md`** — M2 update analysis methodology
- **`MetaconceptPair_README.md`** — MetaconceptPair pattern documentation
- **`M2_KnowledgeField_README.md`** — KnowledgeField concept organization

### Simulation Development
- **`tscg-create-instance-simulation` skill** — 4-step BabylonJS simulation pipeline
- **`M0_InstanceSimulation_UXControls.jsonld`** — Living catalog of reusable UI patterns

## Repository Structure

```
tscg/
├── ontology/                       # M0–M3 ontology files
│   ├── M3_GenesisSpace.jsonld      # Bicephalous foundation
│   ├── M3_EagleEye.jsonld          # ASFID dimensions
│   ├── M3_SphinxEye.jsonld         # REVOI dimensions
│   ├── M2_GenericConcepts.jsonld   # 80 GenericConcepts
│   ├── M1_CoreConcepts.jsonld      # Combo instances
│   ├── M1_Domains.jsonld           # Domain registry
│   ├── M1_extensions/              # Domain-specific extensions
│   │   ├── biology/
│   │   ├── chemistry/
│   │   ├── physics/
│   │   └── ...
│   ├── InstanceSimulations/        # Simulation metadata
│   │   ├── M0_InstanceSimulations.jsonld
│   │   └── M0_InstanceSimulation_UXControls.jsonld
│   ├── sparql/                     # SPARQL queries
│   └── docs/                       # Draft/experimental ontologies
│
├── instances/                      # M0 instances
│   ├── poclets/                    # Validated system models
│   │   ├── adaptive-immune-response/
│   │   ├── fire-triangle/
│   │   ├── transistor/
│   │   └── ... (23+ poclets)
│   ├── tscg-tools/                 # Meta-analytical tools
│   │   ├── tscg-poclet-miner/
│   │   ├── tscg-3d-modeler/
│   │   └── tscg-explorer/
│   ├── systemic-frameworks/        # Cybernetic frameworks
│   │   └── vsm/
│   ├── symbolic-system-grammars/   # Formal symbolic systems
│   │   └── iching/
│   └── transdisclet/               # Transdisciplinary bridges
│
├── src/                            # Python engine (namespace package)
│   ├── ARCHITECTURE_GUIDE.md       # Design spec (~1000 lines)
│   └── tscg/
│       ├── engine/
│       │   ├── core/               # Domain models, loader
│       │   ├── facade/             # Public API layer
│       │   ├── analysis/           # SPARQL, metrics
│       │   ├── exporters/          # Turtle export
│       │   ├── rag/                # RAG embeddings/retrieval
│       │   ├── classifier/         # Metaconcept classification
│       │   └── reasoner/           # OWL reasoning
│       ├── cli/                    # REPL
│       ├── rag/                    # ChromaDB scripts
│       ├── simulation-engine/      # Python simulations
│       └── ontology_tools/         # Migration, conversion
│
├── docs/                           # Documentation
│   ├── methodology/                # Development guides
│   ├── papers/                     # Research articles
│   └── reboot-kit/                 # Smart Prompts, guides
│
├── generate_index.js               # Gallery generator
├── create_files_URIS.py            # URI generator
└── CLAUDE.md                       # This file
```

## Key File URIs

### Core Ontology Files

| File | URI |
|------|-----|
| M3_GenesisSpace.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld` |
| M3_EagleEye.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld` |
| M3_SphinxEye.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld` |
| M2_GenericConcepts.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld` |
| M1_CoreConcepts.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld` |
| M1_Domains.jsonld | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Domains.jsonld` |
| M0_Instances_Schema.shacl.ttl | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Instances_Schema.shacl.ttl` |

### M1 Extensions

| Extension | URI |
|-----------|-----|
| M1_Biology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld` |
| M1_Chemistry | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld` |
| M1_Economics | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.jsonld` |
| M1_Education | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.jsonld` |
| M1_Electronics | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld` |
| M1_Geology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/geology/M1_Geology.jsonld` |
| M1_Music | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/music/M1_Music.jsonld` |
| M1_Mythology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology.jsonld` |
| M1_Physics | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.jsonld` |

### Example Poclets (Sample)

| Poclet | M0 File | README |
|--------|---------|--------|
| Adaptive Immune Response | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/adaptive-immune-response/M0_AdaptiveImmuneResponse.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/adaptive-immune-response/M0_AdaptiveImmuneResponse_README.md` |
| Fire Triangle | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/fire-triangle/M0_FireTriangle.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/fire-triangle/M0_FireTriangle_README.md` |
| Transistor | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/transistor/M0_Transistor.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/transistor/M0_Transistor_README.md` |

Full poclet corpus (23+ validated instances) spans chemistry, physics, biology, music, electronics, economics, mythology, education, and governance domains.

### TSCG Tools

| Tool | M0 File | README |
|------|---------|--------|
| TscgPocletMiner | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-poclet-miner/M0_TscgPocletMiner.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-poclet-miner/M0_TscgPocletMiner_README.md` |
| Tscg3DModeler | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-3d-modeler/M0_Tscg3DModeler.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-3d-modeler/M0_Tscg3DModeler_README.md` |
| TscgExplorer | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-explorer/M0_TscgExplorer.jsonld` | `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/tscg-tools/tscg-explorer/M0_TscgExplorer_README.md` |

### Documentation

| Document | URI |
|----------|-----|
| TSCG Smart Prompt v16.0.0 | `https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v16_0_0.md` |
| Architecture Guide | `https://raw.githubusercontent.com/Echopraxium/tscg/main/src/ARCHITECTURE_GUIDE.md` |
| Poclet Analysis Methodology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/methodology/Poclet_Analysis_Methodology.md` |
| ValueSpace User Guide | `https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/TSCG_ValueSpace_User_Guide.md` |
| Hybrid Formulas Notation | `https://raw.githubusercontent.com/Echopraxium/tscg/main/docs/reboot-kit/HYBRID_FORMULAS_NOTATION_README.md` |

## Development Workflow

### Creating a New Poclet

1. **System identification** — Choose a minimal, complete system
2. **ASFID scoring** — Evaluate A, S, F, I, D dimensions (0.0–1.0)
3. **REVOI scoring** — Evaluate R, E, V, O, I dimensions (0.0–1.0)
4. **M2/M1 concept identification** — Map to GenericConcepts and domain extensions
5. **M0 modeling** — Create `M0_<Name>.jsonld` with proper structure
6. **README** — Document system, scoring rationale, concepts
7. **Simulation** (optional) — BabylonJS 6.26.0 interactive visualization

### Running SPARQL Queries

```python
from tscg.engine.facade import OntologyFacade, QueryFacade

# Load ontology
ontology = OntologyFacade()
ontology.load("ontology/M2_GenericConcepts.jsonld")

# Execute query
query = QueryFacade()
query.set_graph(ontology.get_graph("M2_GenericConcepts"))
results = query.execute("""
    SELECT ?concept ?label WHERE {
        ?concept a m2:GenericConcept .
        ?concept rdfs:label ?label .
    }
""")

for row in results.bindings:
    print(f"{row['concept']}: {row['label']}")
```

### Generating File URIs

```bash
python create_files_URIS.py
```

Outputs markdown tables with GitHub raw URIs for all ontology and instance files.

### Building the RAG Database

```bash
cd src/tscg/rag
python create_tscg_rag.py local
```

Creates `db_tscg_rag/` ChromaDB and compresses to `db_tscg_rag.tar.gz`.

### Gallery Generation

```bash
node generate_index.js
```

Generates `index.html` with interactive gallery of all poclet simulations. Metadata read from `m1core:simulationTitle` (preferred) or `rdfs:label`. Scores searched across all `@graph` nodes. Domain tags from `m1:domain` array in `owl:Ontology` node.

## Critical Patterns

### M1 Extension Formula Convention (MANDATORY)

**FORBIDDEN properties in M1 extension files:**
- `m2Basis` / `m2:characterizedBy` — redundant with structural formula
- `m1:extension:X:asfidSignature` — non-standard, replaced by formal formula
- Any domain-prefixed formula property (e.g. `m1:extension:music:tensorFormula`)

**MANDATORY for all M1 extension domain concepts:**
```json
"@type": ["owl:Class", "m2:KnowledgeFieldConceptCombo"],
"rdfs:subClassOf": "m2:KnowledgeFieldConceptCombo",
"m2:knowledgeField": {"@id": "m1:extension:<domain>:<KnowledgeField>"},
"m1:structuralGrammarFormula": "Fm1m2(<Domain>, <ASFID-formula> | <REVOI-formula>)"
```

**In M1_CoreConcepts (GenericConceptCombos):**
```json
"@type": ["owl:Class", "m2:GenericConceptCombo"],
"rdfs:subClassOf": "m2:GenericConceptCombo",
"m1:structuralGrammarFormula": "Fm2(<Concept1>, <Concept2>, ...)"
```

Score DatatypeProperties are **distinct** from MonoidalTypes:
- `m3:eagle_eye:Attractor` = MonoidalType (structural grammar primitive — never used as score property)
- `m0:scoreA` = DatatypeProperty of scoring (distinct IRI)

M0 instances use `_score` aliases in `@context` that resolve to dedicated scoring IRIs:

```json
"@context": {
  "A_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreA",  "@type": "xsd:float"},
  "S_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreS",  "@type": "xsd:float"},
  "F_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreF",  "@type": "xsd:float"},
  "It_score": {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreIt", "@type": "xsd:float"},
  "D_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreD",  "@type": "xsd:float"},
  "R_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreR",  "@type": "xsd:float"},
  "E_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreE",  "@type": "xsd:float"},
  "V_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreV",  "@type": "xsd:float"},
  "O_score":  {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreO",  "@type": "xsd:float"},
  "Im_score": {"@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#scoreIm", "@type": "xsd:float"}
}
```

**Score values format:** `{"@value": "0.85", "@type": "xsd:float"}`

**In README tables:** `| A_score (Attractor) | 0.85 |` — NEVER bare `| A |`

**It_score vs Im_score disambiguation:**
- `It_score` = Information dimension score (Territory/ASFID)
- `Im_score` = Interoperable dimension score (Map/REVOI)

### Epistemic Gap (δ₁)

Normalized vectorial distance between ASFID and REVOI score vectors:

```
δ₁ = ||ASFID - REVOI|| / √10
```

SpectralClasses include: `Coherent`, `OnCriticalLine`, etc.

### M1 Extension Reference Pattern

In M0 instances:

```json
"@context": {
  "m1bio": "M1_extensions/biology/M1_Biology.jsonld#",
  "m1chem": "M1_extensions/chemistry/M1_Chemistry.jsonld#"
}
```

### Metadata Node Pattern

In all M0 instances, `@graph[0]` is the reference node for metadata (`rdfs:label`, `m1:domain`, `m2:version`). Scores may appear in any node.

---

**Version**: Updated for TSCG v16.0.0  
**Last updated**: May 2026  
**Maintained by**: Echopraxium with the collaboration of Claude AI
