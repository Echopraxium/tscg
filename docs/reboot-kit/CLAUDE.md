# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TSCG (The Systemic Construction Game)** is a transdisciplinary framework for modeling complex systems using a unified ontological "construction kit." The metaphor is LEGO Technic: reusable conceptual blocks that snap together across biology, chemistry, engineering, mythology, and social sciences. The philosophical basis is Korzybski's "The map is not the territory."

Research preprint: DOI [10.5281/zenodo.18471860](https://doi.org/10.5281/zenodo.18471860)

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

# SPARQL analysis on M2 metaconcepts
python ontology/sparql/m2_sparql_analysis.py
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
| **M2** | GenericConcepts | 81 universal patterns applicable across all domains | `ontology/M2_GenericConcepts.jsonld` |
| **M1** | Core/Domain Concepts | Domain-specific concept extensions (biology, chemistry, etc.) | `ontology/M1_*.jsonld`, `ontology/M1_extensions/` |
| **M0** | Poclets | Validated minimal complete models of real systems | `system-models/poclets/*/M0_*.jsonld/.ttl` |

### M3: The Bicephalous Basis

M3 is split into two complementary perspectives that together form a 10-dimensional space:
- **ASFID (Eagle Eye / Territory)**: Attractor, Structure, Flow, Information, Dynamics — what a system *is*
- **REVOI (Sphinx Eye / Map)**: Representability, Evolvability, Verifiability, Observability, Interoperability — how a system is *known*

Files: `M3_EagleEye.jsonld` (ASFID), `M3_SphinxEye.jsonld` (REVOI), `M3_GenesisSpace.jsonld` (unified with coupling matrices).

### M2: Metaconcept Organization

68 metaconcepts organized into 5 categories, constructed as tensor products of M3 dimensions:
- **Ontological**: fundamental existence patterns
- **Structural**: organizational patterns
- **Dynamic**: change and process patterns
- **Control**: regulation and feedback patterns
- **Information**: knowledge and representation patterns

The production file is `M2_GenericConcepts.jsonld`; `M2_MetaConcepts_Ref.jsonld` is the reference/backup version. Draft/experimental work lives in `ontology/docs/`.

### M0: Poclets

A **poclet** (Proof-Of-Concept LET) is a minimal, complete, validated model of a real system. Each poclet lives in its own directory under `system-models/poclets/` and has dual-format files (`M0_*.jsonld` + `M0_*.ttl`). Models under active repair are in `system-models/poclets/00_to_be_fixed/`.

## File Format Conventions

- All ontologies are maintained in **dual format**: `.jsonld` (JSON-LD) and `.ttl` (RDF/Turtle)
- File naming follows the layer prefix: `M3_`, `M2_`, `M1_`, `M0_`
- RDF namespace base: `http://tscg.net/ontology/`
- SPARQL queries are in `ontology/sparql/`

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

**`jsonld_to_turtle.py`** — `JSONLDToTurtleConverter`: batch-converts all `.jsonld` files in `ontology/` and `system-models/` to `.ttl`, preserving directory structure. Supports dry-run mode and skip-on-error. This is the canonical tool for keeping dual-format files in sync.

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
| `.md` | Per section header, with **parent breadcrumb** prepended (`Parent > Child > Current`) so sub-sections retain context. Files under `ontology/docs/` tagged `ontology_doc: True`. |
| `.py` / `.cs` | Per function/class block |
| `.txt` | By paragraph with overlap |

Key internals:
- `_source_prefix(source)` — generates globally unique segment IDs as `{stem}_{6-char-path-hash}` to avoid collisions when the same filename exists in multiple directories
- `_entry_to_text(entry, layer)` — converts a JSON-LD `@graph` entry to a readable NL summary; returns `None` for OWL infrastructure to skip it
- Layer (`M0`–`M3`) is inferred from the filename prefix

**`query_tscg_rag.py`** — CLI for querying the ChromaDB database.
- Auto-decompresses `db_tscg_rag.tar.gz` if the uncompressed directory is absent
- Deduplicates results by content hash (fetches `top_k × 3` candidates, returns `top_k` unique)
- `--ontology-docs-only` restricts results to `ontology/docs/` files (authoritative documentation)
- `--filter-type jsonld_entry` restricts to ontology concept segments
- Modes: single query, `--interactive` REPL with `stats` / `sources` commands

### `tests/`

**`test_facades.py`** — pytest unit tests covering facade instantiation and score model arithmetic. Integration tests (loading real ontology files) run conditionally when `/mnt/project` is present.

### Key Design Patterns

- **Facade pattern**: only import from `tscg.engine.facade`; never from `core/`, `analysis/`, or `exporters/` directly
- **Lazy loading**: `TSCGEmbedder` defers model load to first call; RAG components instantiate on demand
- **Dataclass results**: `SPARQLResult`, `ExportResult`, `SearchResult`, `OrthogonalityReport` are structured containers — never raw dicts
- **Caching**: `SPARQLExecutor` uses SHA-based query hash; pass `use_cache=False` to bypass

### Dependencies

| Group | Packages |
|-------|---------|
| Core | `rdflib`, `pydantic`, `numpy`, `scipy` |
| RAG/ML | `sentence-transformers`, `chromadb` |
| CLI | `prompt-toolkit`, `rich`, `typer` |
| Optional (Google mode) | `langchain-google-genai` |
| Tests | `pytest` |

## RAG Integration

Two separate RAG implementations exist:

- **`src/tscg/engine/rag/`** — in-process, numpy-backed, used via `RAGFacade` (programmatic use)
- **`src/tscg/rag/`** — ChromaDB-backed, file-based pipeline for building and querying a persistent vector store (CLI use)

### File-based RAG pipeline (`src/tscg/rag/`)

The database (`db_tscg_rag.tar.gz`, ~21 MB) is committed to git. On first query after a fresh clone, `query_tscg_rag.py` auto-decompresses it — no manual setup needed.

To rebuild from scratch (needed after adding/changing ontology files):
```bash
rmdir /s /q src\tscg\rag\db_tscg_rag        # Windows
python src/tscg/rag/create_tscg_rag.py local
```

**Embedding modes:**
- `local` — `sentence-transformers/all-MiniLM-L6-v2` (384-dim, free, offline, recommended)
- `api` — Google `gemini-embedding-001` (768-dim, requires `.api_key` file, quota-limited)

**Useful query flags:**
```bash
--ontology-docs-only      # restrict to ontology/docs/ authoritative files
--filter-type jsonld_entry  # restrict to ontology concept segments only
--top-k 10                # return more results
--show-text               # show full segment text instead of excerpt
--interactive             # REPL mode with stats/sources commands
```

**Previous implementation** archived at `src/tscg/rag/_archives/RAG-prev/` — do not use.

## The Bicephalous Architecture (Eagle Eye / Sphinx Eye)

M3 is the **dual-headed foundation** of TSCG. It defines a 10-dimensional Genesis Space structured as two complementary 5D bases:

```
Genesis Space ℋ = ℋ_ASFID ⊕ ℋ_REVOI
                  (Eagle Eye)  (Sphinx Eye)
```

### Eagle Eye — Territory Space (ASFID)

Measures **what a system IS** — observable phenomena in the physical world.

| Letter | Dimension | Role |
|--------|-----------|------|
| **A** | Attractor | Stable states, equilibria, fixed points |
| **S** | Structure | Organisation, topology, components |
| **F** | Flow | Transfers, fluxes, movements |
| **I** | Information | Signals, encoding, state representation |
| **D** | Dynamics | Change, evolution, temporal behaviour |

### Sphinx Eye — Map Space (REVOI)

Measures **how a system is KNOWN** — quality of the conceptual model that represents it.

| Letter | Dimension | Role |
|--------|-----------|------|
| **R** | Representability | Can the system be modelled? |
| **E** | Evolvability | Can the model adapt over time? |
| **V** | Verifiability | Can predictions be tested? |
| **O** | Observability | Are states measurable? |
| **I** | Interoperability | Can models integrate with others? |

> ⚠️ **REVOI**: R = Representability (NEVER Reproducibility). Always verify before writing.

### Coupling Between Perspectives

Territory (ASFID) and Map (REVOI) are coupled through:
- **Φ**: observation operator (Territory → Map), matrix form `Φ = V Σ U^T`
- **Ψ**: implementation operator (Map → Territory), matrix form `Ψ = U Σ V^T`
- **Σ**: 5×5 coupling matrix encoding ASFID↔REVOI interaction strength (~80% sparse)

The **epistemic gap** `δΘ = ||ASFID_score - REVOI_score||` measures the distance between observable reality and the quality of its conceptual representation. Smaller gap = better framework maturity.

---

## Framework Layers and M0 Ontology Types

### The Four-Layer Stack

```
M3  Genesis Space          3 ontologies  ─ foundational, zero dependencies
 ↕  (tensorization)
M2  GenericConcepts        81 patterns    ─ tensor products of M3 dimensions
 ↕  (instantiation)
M1  Core + Domain Concepts variable      ─ generic and domain-specific concepts
 ↕  (validation)
M0  Poclets / Case Studies ~25+ models   ─ minimal complete real-world systems
```

### M3 Ontology Files (closed set — exactly 3)

| File | Role |
|------|------|
| `M3_GenesisSpace.jsonld` | Unified 10D space + coupling matrices Φ, Ψ, Σ |
| `M3_EagleEye.jsonld` | ASFID basis (Territory) |
| `M3_SphinxEye.jsonld` | REVOI basis (Map) |

### M2 Ontology File (single production file)

| File | Content |
|------|---------|
| `M2_GenericConcepts.jsonld` | 81 GenericConcepts as tensor products of M3 dimensions, organised in 5 families: Ontological, Structural, Dynamic, Control, Information |

### M1 Ontology Files (extensible set)

| File | Role |
|------|------|
| `M1_CoreConcepts.jsonld` | Base ontology — generic transdisciplinary concepts |
| `M1_Biology.jsonld` | Domain extension — biology |
| `M1_Chemistry.jsonld` | Domain extension — chemistry |
| `M1_Economics.jsonld` | Domain extension — economics |
| `M1_Education.jsonld` | Domain extension — education |
| `M1_Electronics.jsonld` | Domain extension — electronics & modular synthesis (17 concepts) |
| `M1_EnergyGenerators.jsonld` | Domain extension — energy generators |
| `M1_Mythology.jsonld` | Domain extension — mythology |
| `M1_Optics.jsonld` | Domain extension — optics |
| `M1_Photography.jsonld` | Domain extension — photography |
| `M1_Physics.jsonld` | Domain extension — physics |

Each M1 domain extension imports `M1_CoreConcepts.jsonld` via `owl:imports` and uses its own namespace (e.g., `m1:optics:`, `m1:photo:`, `m1:mythology:`).

### M0 Instance Types (the three kinds of system model)

Every M0 file declares its type via `"m3:ontologyType": {"@id": "m3:..."}`:

| Type | `@id` | Criteria |
|------|-------|----------|
| **Poclet** | `m3:Poclet` | Minimal + Complete across all ASFID dimensions + validated across ≥3 unrelated domains |
| **Case Study** | `m3:CaseStudy` | Pedagogical or exploratory — may be incomplete or non-minimal |
| **Real-World System** | `m3:RealWorldSystem` | Actual deployed operational system |

A **poclet** is the most rigorous M0 form: it must exhibit all 5 ASFID dimensions and serve as proof-of-concept for systemic principles. It plays a triple role: (1) validates TSCG, (2) reveals M2 metaconcept candidates, (3) populates M1 concepts.

---

## Formula Encoding — Critical Rules

Ontology files contain formulas using **Unicode mathematical and Greek characters**. Corruption of these symbols breaks semantic meaning and JSON validation.

### Characters at Risk

| Symbol | Unicode | Name | Risk |
|--------|---------|------|------|
| `⊗` | U+2297 | Tensor product | High — corrupts to `â€"` sequences |
| `→` | U+2192 | Arrow | High |
| `↔` | U+2194 | Bidirectional arrow | High |
| `Φ` | U+03A6 | Phi (observation operator) | Medium |
| `Ψ` | U+03A8 | Psi (implementation operator) | Medium |
| `Σ` | U+03A3 | Sigma (coupling matrix) | Medium |
| `δ` | U+03B4 | Delta (epistemic gap) | Medium |
| Greek subscripts | U+2080-2089 | ₀₁₂₃... | Medium |

### Rules When Modifying an Ontology File

1. **Always open and write files with explicit `encoding='utf-8'`** in Python scripts.
2. **Never copy-paste formula strings through an ASCII-only tool** — use raw file editing only.
3. **Validate JSON after every modification**: `python -c "import json; json.load(open('file.jsonld', encoding='utf-8'))"`.
4. **Run `check_encoding_issues.py`** after any batch operation to detect corruption early.
5. **Do NOT use `Î` (U+00CE, I with circumflex)** — the official acronym is **REVOI** (plain Latin I, U+0049). If you see `REVOÎ` or `REVOÃˆ` in a file, that is corruption — fix it.

### The It / Im Disambiguation Convention

In **hybrid formulas** combining both ASFID and REVOI dimensions, the letter `I` is ambiguous (it appears in both bases). Use subscript notation:

| Symbol | Meaning | Origin |
|--------|---------|--------|
| `It` | Information (Territory) | ASFID — Eagle Eye |
| `Im` | Interoperability (Map) | REVOI — Sphinx Eye |

Use subscripts **only when both I's coexist in the same formula**:
- Pure ASFID formula → plain `I`
- Pure REVOI formula → plain `I`
- Hybrid formula → `It` and `Im`

```json
// Pure ASFID — no disambiguation needed
"m2:hasTensorFormula": "D ⊗ I ⊗ F"

// Hybrid — disambiguation required
"m2:hasTensorFormula": "A ⊗ S ⊗ F ⊗ It ⊗ D ⊗ R ⊗ E ⊗ V ⊗ O ⊗ Im"
```

### ASCII Fallback Fields

Every metaconcept formula should have three representations for resilience:

```json
"m2:hasTensorFormula":      "D ⊗ I ⊗ F",
"m2:hasTensorFormulaTeX":   "D \\otimes I \\otimes F",
"m2:hasTensorFormulaASCII": "D (x) I (x) F"
```

---

## Key Documentation

- `src/ARCHITECTURE_GUIDE.md` — authoritative Python engine design spec
- `docs/TSCG_M2_Category_Taxonomy.md` — M2 category organization
- `docs/methodology/` — methodological guides
- `README.md` — framework overview with quick-start workflow
- `claude_setup.txt` — setup instructions for this environment

### Repository File URIs (Complete List)

Base: `https://raw.githubusercontent.com/echopraxium/tscg/main/`

#### Root Files

| File | URI |
|------|-----|
| CLAUDE.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/CLAUDE.md` |
| README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/README.md` |
| files.txt | `https://raw.githubusercontent.com/echopraxium/tscg/main/files.txt` |
| claude_setup.txt | `https://raw.githubusercontent.com/echopraxium/tscg/main/claude_setup.txt` |
| create_files_URIS.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/create_files_URIS.py` |

#### ontology/ — Core Ontology Files

| File | URI |
|------|-----|
| M3_GenesisSpace.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld` |
| M3_GenesisSpace.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisSpace.ttl` |
| M3_GenesisSpace_Ref.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_GenesisSpace_Ref.jsonld` |
| M3_EagleEye.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye.jsonld` |
| M3_EagleEye.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_EagleEye.ttl` |
| M3_SphinxEye.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld` |
| M3_SphinxEye.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M3_SphinxEye.ttl` |
| M2_GenericConcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld` |
| M1_CoreConcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld` |
| shacl_shapes.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/shacl_shapes.ttl` |

#### ontology/M1_extensions/ — Domain Extensions

| File | URI |
|------|-----|
| M1_CoreConcepts_NuclearUpdate.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.jsonld` |
| M1_CoreConcepts_NuclearUpdate.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_CoreConcepts_NuclearUpdate.ttl` |
| M1_Extensions_Summary.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/M1_Extensions_Summary.md` |
| biology/M1_Biology.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M1_Biology.jsonld` |
| biology/M2_MetaConcepts_Alignment.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.jsonld` |
| biology/M2_MetaConcepts_Alignment.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/biology/M2_MetaConcepts_Alignment.ttl` |
| chemistry/M1_Chemistry.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/chemistry/M1_Chemistry.jsonld` |
| economics/M1_Economics.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.jsonld` |
| economics/M1_Economics.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics.ttl` |
| economics/M1_Economics_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/economics/M1_Economics_README.md` |
| education/M1_Education.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.jsonld` |
| education/M1_Education.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.ttl` |
| education/M1_Education_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education_README.md` |
| electronics/M1_Electronics.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.jsonld` |
| electronics/M1_Electronics.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics.ttl` |
| electronics/M1_Electronics_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/electronics/M1_Electronics_README.md` |
| energy_generators/M1_EnergyGenerators.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.jsonld` |
| energy_generators/M1_EnergyGenerators.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/energy_generators/M1_EnergyGenerators.ttl` |
| mythology/M1_Mythology.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology.jsonld` |
| mythology/M1_Mythology_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/mythology/M1_Mythology_README.md` |
| optics/M1_Optics.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/optics/M1_Optics.jsonld` |
| photography/M1_Photography.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/photography/M1_Photography.jsonld` |
| physics/M1_Physics.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.jsonld` |
| physics/M1_Physics.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics.ttl` |
| physics/M1_Physics_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/M1_extensions/physics/M1_Physics_README.md` |

#### ontology/Ref/ — Reference Backups

| File | URI |
|------|-----|
| M2_MetaConcepts_Ref.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_MetaConcepts_Ref.jsonld` |
| M2_MetaConcepts_Ref.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M2_MetaConcepts_Ref.ttl` |
| M3_GenesisSpace_Ref.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M3_GenesisSpace_Ref.jsonld` |
| M3_GenesisSpace_Ref.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/Ref/M3_GenesisSpace_Ref.ttl` |

#### ontology/sparql/ — SPARQL Files

| File | URI |
|------|-----|
| m2_sparql_analysis.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/m2_sparql_analysis.py` |
| SPARQL_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/SPARQL_README.md` |
| M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.jsonld` |
| M2_MetaConcepts_2026_02_08_encoding_lint_ok.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_2026_02_08_encoding_lint_ok.ttl` |
| M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.jsonld` |
| M2_MetaConcepts_v15_0_0_WITH_Processor.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_v15_0_0_WITH_Processor.ttl` |
| M2_Processor.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_Processor.jsonld` |
| M2_Processor.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_Processor.ttl` |
| M2_MetaConcepts_SPARQL_Querie_README.txt | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/sparql/M2_MetaConcepts_SPARQL_Querie_README.txt` |

#### ontology/tools/

| File | URI |
|------|-----|
| M2_MetaConcepts_Ref.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/tools/M2_MetaConcepts_Ref.jsonld` |
| M2_MetaConcepts_Ref.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/tools/M2_MetaConcepts_Ref.ttl` |

#### ontology/docs/ — Ontology Documentation & Drafts

| File | URI |
|------|-----|
| M1_CoreConcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts.jsonld` |
| M1_CoreConcepts.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts.ttl` |
| M1_CoreConcepts_NuclearUpdate.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts_NuclearUpdate.jsonld` |
| M1_CoreConcepts_NuclearUpdate.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts_NuclearUpdate.ttl` |
| M1_CoreConcepts_updated.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts_updated.jsonld` |
| M1_CoreConcepts_updated.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts_updated.ttl` |
| M2_MetaConcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts.jsonld` |
| M2_MetaConcepts.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts.ttl` |
| M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_02_06_encoding_lint_checked.jsonld` |
| M2_MetaConcepts_2026_03_04_FixedEncoding.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_2026_03_04_FixedEncoding_validéLint.jsonld` |
| M2_MetaconceptCombo.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaconceptCombo.jsonld` |
| M2_MetaconceptCombo.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaconceptCombo.ttl` |
| M2_Metaconcepts_v13.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Metaconcepts_v13.jsonld` |
| M2_New_5_Metaconcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_New_5_Metaconcepts.jsonld` |
| M2_Pattern_metaconcept.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Pattern_metaconcept.jsonld` |
| M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_KnowledgeFieldMetaCombo_v15_2_0.jsonld` |
| M3_CategoryTheory_v1_0_0.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M3_CategoryTheory_v1_0_0.jsonld` |
| M3_Philosophical_Eye.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M3_Philosophical_Eye.jsonld` |
| TSCG_Formula_Properties_Specification.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_Formula_Properties_Specification.jsonld` |
| m2_Imbrication_entry.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/m2_Imbrication_entry.jsonld` |
| M1_CoreConcepts_v1.2.0_Summary.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_CoreConcepts_v1.2.0_Summary.md` |
| M1_Extensions_Summary.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M1_Extensions_Summary.md` |
| M2_Architecture_Specification_v9.1.0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Architecture_Specification_v9.1.0.md` |
| M2_Behavioral_Sequential_Metaconcepts_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Behavioral_Sequential_Metaconcepts_README.md` |
| M2_Coherence_Analysis.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Coherence_Analysis.md` |
| M2_GenericConcepts_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_GenericConcepts_README.md` |
| M2_Imbrication_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_Imbrication_README.md` |
| M2_KnowledgeField_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_KnowledgeField_README.md` |
| M2_MetaConcepts_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M2_MetaConcepts_README.md` |
| M3_EagleEye_Update_Analysis_v15_1_0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M3_EagleEye_Update_Analysis_v15_1_0.md` |
| M3_GenesisSpace_CategoryTheory_Integration.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M3_GenesisSpace_CategoryTheory_Integration.md` |
| M3_Genesis_Space_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/M3_Genesis_Space_README.md` |
| MetaconceptPair_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/MetaconceptPair_README.md` |
| Poclet_Analysis_Methodology.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Poclet_Analysis_Methodology.md` |
| TSCG_Architectural_Extensions.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_Architectural_Extensions.md` |
| TSCG_Documentation_Index.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_Documentation_Index.md` |
| TSCG_Formula_Encoding_Solution.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_Formula_Encoding_Solution.md` |
| TSCG_M1_Architecture.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_M1_Architecture.md` |
| TSCG_M2_MetaConcepts_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_M2_MetaConcepts_README.md` |
| TSCG_Smart_Prompt_v15_7_0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_Smart_Prompt_v15_7_0.md` |
| TSCG_ValueSpace_Quick_Reference.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_ValueSpace_Quick_Reference.md` |
| TSCG_ValueSpace_User_Guide.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_ValueSpace_User_Guide.md` |
| TSCG_v15_1_0_Final_Classification.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_v15_1_0_Final_Classification.md` |
| TSCG_v15_1_0_Integration_Report.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/TSCG_v15_1_0_Integration_Report.md` |
| Domain_M2_Update_Analysis_v15_1_0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Domain_M2_Update_Analysis_v15_1_0.md` |
| Cascade_Modeling_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Cascade_Modeling_README.md` |
| Amplification_Integration_Summary.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Amplification_Integration_Summary.md` |
| Bicephalous_Integration_Guide.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Bicephalous_Integration_Guide.md` |
| HOWTO_Create_M1_Extension.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/HOWTO_Create_M1_Extension.md` |
| Namespace_Refactoring_Summary.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/Namespace_Refactoring_Summary.md` |
| ontology_analysis.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/ontology/docs/ontology_analysis.md` |

#### system-models/poclets/ — Validated Poclets

| Poclet | File | URI |
|--------|------|-----|
| Adaptive Immune Response | M0_AdaptiveImmuneResponse.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/adaptative_immune_response/M0_AdaptiveImmuneResponse.jsonld` |
| Adaptive Immune Response | M0_AdaptiveImmuneResponse.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/adaptative_immune_response/M0_AdaptiveImmuneResponse.ttl` |
| Adaptive Immune Response | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/adaptative_immune_response/M0_AdaptiveImmuneResponse_README.md` |
| Blood Pressure Control | M0_BloodPressureControl.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/blood_pressure_control/M0_BloodPressureControl.jsonld` |
| Blood Pressure Control | M0_BloodPressureControl.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/blood_pressure_control/M0_BloodPressureControl.ttl` |
| Blood Pressure Control | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/blood_pressure_control/M0_BloodPressureControl_README.md` |
| Butterfly Metamorphosis | M0_ButterflyMetamorphosis.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/butterfly_metamorphosis/M0_ButterflyMetamorphosis.jsonld` |
| Butterfly Metamorphosis | M0_ButterflyMetamorphosis.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/butterfly_metamorphosis/M0_ButterflyMetamorphosis.ttl` |
| Butterfly Metamorphosis | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/butterfly_metamorphosis/butterfly_metamorphosis_README.md` |
| Cell Signaling Modes | M0_CellSignalingModes.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/cell_signaling_modes/M0_CellSignalingModes.jsonld` |
| Cell Signaling Modes | M0_CellSignalingModes.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/cell_signaling_modes/M0_CellSignalingModes.ttl` |
| Cell Signaling Modes | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/cell_signaling_modes/M0_CellSignalingModes_README.md` |
| Color Synthesis | M0_CMYK_Subtractive.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/color_synthesis/M0_CMYK_Subtractive.jsonld` |
| Color Synthesis | M0_CMY_Subtractive.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/color_synthesis/M0_CMY_Subtractive.jsonld` |
| Color Synthesis | M0_ColorSynthesis_Federated.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/color_synthesis/M0_ColorSynthesis_Federated.jsonld` |
| Color Synthesis | M0_HSL_Additive.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/color_synthesis/M0_HSL_Additive.jsonld` |
| Color Synthesis | M0_RGB_Additive.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/color_synthesis/M0_RGB_Additive.jsonld` |
| Complex Chemical Synapse | M0_ComplexChemicalSynapse.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/complex_chemical_synapse/M0_ComplexChemicalSynapse.jsonld` |
| Complex Chemical Synapse | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/complex_chemical_synapse/M0_ComplexChemicalSynapse_README.md` |
| Exposure Triangle | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/exposure_triangle/M0_ExposureTriangle_README.md` |
| Fire Triangle | M0_FireTriangle.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/fire_triangle/M0_FireTriangle.jsonld` |
| Fire Triangle | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/fire_triangle/M0_FireTriangle_README.md` |
| Four-Stroke Engine | M0_FourStrokeEngine.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/four_stroke_engine/M0_FourStrokeEngine.jsonld` |
| Four-Stroke Engine | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/four_stroke_engine/M0_FourStrokeEngine_README.md` |
| Four-Stroke Engine | Sim | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/four_stroke_engine/four_stroke_engine_sim.py` |
| Kidneys | M0_Kidneys.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kidneys/M0_Kidneys.jsonld` |
| Kidneys | M0_Kidneys.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kidneys/M0_Kidneys.ttl` |
| Kidneys | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kidneys/M0_Kidneys_README.md` |
| Nuclear Reactor Typology | M0_NuclearReactorTypology.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/nuclear_reactors_typology/M0_NuclearReactorTypology.jsonld` |
| Nuclear Reactor Typology | M0_NuclearReactorTypology.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/nuclear_reactors_typology/M0_NuclearReactorTypology.ttl` |
| Nuclear Reactor Typology | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/nuclear_reactors_typology/M0_NuclearReactorTypology_README.md` |
| RAAS | M0_RAAS.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/raas/M0_RAAS.jsonld` |
| RAAS | M0_RAAS.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/raas/M0_RAAS.ttl` |
| RAAS | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/raas/RAAS_Complete_README.md` |
| Transistor | M0_Transistor.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/transistor/M0_Transistor.jsonld` |
| Transistor | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/transistor/M0_Transistor_README.md` |
| Transistor | Sim | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/transistor/transistor_sim.py` |
| Yggdrasil | M0_Yggdrasil.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/yggdrasil/M0_Yggdrasil.jsonld` |
| Yggdrasil | M0_Yggdrasil.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/yggdrasil/M0_Yggdrasil.ttl` |
| Yggdrasil | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/yggdrasil/M0_Yggdrasil_README.md` |

| Kindleberger-Minsky | M0_KindlebergerMinsky.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kindleberger-minsky/M0_KindlebergerMinsky.jsonld` |
| Kindleberger-Minsky | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kindleberger-minsky/M0_KindlebergerMinsky_README.md` |
| Kindleberger-Minsky | Sim | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/kindleberger-minsky/kindleberger_minsky_sim.py` |
| MTG Color Wheel | M0_MTG_ColorWheel.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/mtg_color_wheel/M0_MTG_ColorWheel.jsonld` |
| MTG Color Wheel | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/mtg_color_wheel/MTG_ColorWheel_README.md` |
| Phase Transition | M0_PhaseTransition.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/phase_transition/M0_PhaseTransition.jsonld` |
| Phase Transition | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/phase_transition/M0_PhaseTransition_README.md` |
| TPACK | M0_TPACK.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/tpack/M0_TPACK.jsonld` |
| TPACK | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/tpack/TPACK_README.md` |
| VCO | M0_VCO.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/vco/M0_VCO.jsonld` |
| VCO | README | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/vco/M0_VCO_README.md` |
| VCO | Sim | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/poclets/vco/vco_sim.py` |

#### system-models/tscg-tools/tscg-explorer/ — TSCG Meta-Analytical Tool

| File | URI |
|------|-----|
| M0_TscgExplorer.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/tscg-tools/tscg-explorer/M0_TscgExplorer.jsonld` |
| M0_TscgExplorer_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/tscg-tools/tscg-explorer/M0_TscgExplorer_README.md` |
| TSCG_Explorer_Simulation_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/tscg-tools/tscg-explorer/TSCG_Explorer_Simulation_README.md` |
| tscg_explorer.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/tscg-tools/tscg-explorer/tscg_explorer.py` |

#### system-models/systemic-frameworks/vsm/ — VSM

| File | URI |
|------|-----|
| M0_VSM.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM.jsonld` |
| M0_VSM.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM.ttl` |
| M0_VSM_Metaconcepts.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM_Metaconcepts.jsonld` |
| M0_VSM_Metaconcepts.ttl | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM_Metaconcepts.ttl` |
| M0_VSM_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM_README.md` |
| M0_VSM_README_Metaconcepts.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/systemic-frameworks/vsm/M0_VSM_README_Metaconcepts.md` |

#### system-models/symbolic-system-grammars/iching/ — I Ching

| File | URI |
|------|-----|
| M0_IChing.jsonld | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/symbolic-system-grammars/iching/M0_IChing.jsonld` |
| M0_IChing_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/system-models/symbolic-system-grammars/iching/M0_IChing_README.md` |

#### src/ — Python Engine

| File | URI |
|------|-----|
| ARCHITECTURE_GUIDE.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/ARCHITECTURE_GUIDE.md` |
| tscg/engine/core/models.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/core/models.py` |
| tscg/engine/core/ontology_loader.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/core/ontology_loader.py` |
| tscg/engine/facade/ontology.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/facade/ontology.py` |
| tscg/engine/facade/query.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/facade/query.py` |
| tscg/engine/facade/metrics.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/facade/metrics.py` |
| tscg/engine/facade/export.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/facade/export.py` |
| tscg/engine/facade/rag.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/facade/rag.py` |
| tscg/engine/analysis/sparql/executor.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/analysis/sparql/executor.py` |
| tscg/engine/analysis/metrics/orthogonality.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/analysis/metrics/orthogonality.py` |
| tscg/engine/exporters/turtle_exporter.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/exporters/turtle_exporter.py` |
| tscg/engine/rag/embeddings.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/rag/embeddings.py` |
| tscg/engine/rag/vector_store.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/rag/vector_store.py` |
| tscg/engine/rag/retrieval.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/rag/retrieval.py` |
| tscg/engine/classifier/metaconcept_classifier.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/classifier/metaconcept_classifier.py` |
| tscg/engine/reasoner/reasoner.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/engine/reasoner/reasoner.py` |
| tscg/cli/repl/context.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/cli/repl/context.py` |
| tscg/cli/repl/interpreter.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/cli/repl/interpreter.py` |
| tscg/rag/create_tscg_rag.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/create_tscg_rag.py` |
| tscg/rag/query_tscg_rag.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/query_tscg_rag.py` |
| tscg/rag/TSCG_RAG_Segmentation_Guide.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/rag/TSCG_RAG_Segmentation_Guide.md` |
| tscg/simulation-engine/color_synthesis_sim.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/simulation-engine/color_synthesis_sim.py` |
| tscg/simulation-engine/exposure_triangle_sim.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/simulation-engine/exposure_triangle_sim.py` |
| tscg/simulation-engine/fire_triangle_sim.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/simulation-engine/fire_triangle_sim.py` |
| tscg/simulation-engine/four_stroke_engine_sim.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/simulation-engine/four_stroke_engine_sim.py` |
| tscg/simulation-engine/transistor_sim.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/simulation-engine/transistor_sim.py` |
| tscg/ontology_tools/jsonld-to-owl/jsonld_to_turtle.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/jsonld-to-owl/jsonld_to_turtle.py` |
| tscg/ontology_tools/migration/tscg_migration.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/ontology_tools/migration/tscg_migration.py` |
| tscg/tests/test_facades.py | `https://raw.githubusercontent.com/echopraxium/tscg/main/src/tscg/tests/test_facades.py` |

#### docs/ — Documentation

| File | URI |
|------|-----|
| docs/TSCG_M2_Category_Taxonomy.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/TSCG_M2_Category_Taxonomy.md` |
| docs/methodology/Bicephalous_Integration_Guide.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/Bicephalous_Integration_Guide.md` |
| docs/methodology/Standard_Referencing_Pattern.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/methodology/Standard_Referencing_Pattern.md` |
| docs/papers/preprints/TSCG_Research_Paper_Draft_v1.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/TSCG_Research_Paper_Draft_v1.md` |
| docs/papers/preprints/TSCG_Research_Paper_Draft_v2.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/preprints/TSCG_Research_Paper_Draft_v2.md` |
| docs/papers/white-paper/TSCG_WhitePaper.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/papers/white-paper/TSCG_WhitePaper.md` |
| docs/reboot-kit/TSCG_Smart_Prompt_v15_7_0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_7_0.md` |
| docs/reboot-kit/TSCG_Smart_Prompt_v15_8_0.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_Smart_Prompt_v15_8_0.md` |
| docs/reboot-kit/TSCG_ValueSpace_Quick_Reference.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_ValueSpace_Quick_Reference.md` |
| docs/reboot-kit/TSCG_ValueSpace_User_Guide.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/TSCG_ValueSpace_User_Guide.md` |
| docs/reboot-kit/HYBRID_FORMULAS_NOTATION_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/HYBRID_FORMULAS_NOTATION_README.md` |
| docs/reboot-kit/Cascade_Modeling_README.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/Cascade_Modeling_README.md` |
| docs/reboot-kit/poclet_terminology.md | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/poclet_terminology.md` |
| docs/reboot-kit/SmartPrompts/macros.txt | `https://raw.githubusercontent.com/echopraxium/tscg/main/docs/reboot-kit/SmartPrompts/macros.txt` |

### Methodology Documents (in project knowledge base)

| Document | Content |
|----------|---------|
| `Poclet_Analysis_Methodology.md` | Step-by-step poclet analysis heuristic |
| `HYBRID_FORMULAS_NOTATION_README.md` | Formula encoding conventions (It/Im, REVOI standard) |
| `TSCG_ValueSpace_User_Guide.md` | How to use ValueSpace attributes in instantiations |
| `TSCG_ValueSpace_Quick_Reference.md` | Cheat sheet for all 13 ValueSpace attributes |
| `00_TSCG_M3_Bicephalous_Architecture.md` | Theoretical foundation of the dual-headed M3 |
| `00_TSCG_Map_Territory_Theoretical_Foundation.md` | Korzybski philosophical basis |

- `src/ARCHITECTURE_GUIDE.md` — authoritative Python engine design spec
- `docs/TSCG_M2_Category_Taxonomy.md` — M2 category organization
- `docs/methodology/` — methodological guides
- `README.md` — framework overview with quick-start workflow
- `claude_setup.txt` — setup instructions for this environment
