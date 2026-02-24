# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**TSCG (The Systemic Construction Game)** is a transdisciplinary framework for modeling complex systems using a unified ontological "construction kit." The metaphor is LEGO Technic: reusable conceptual blocks that snap together across biology, chemistry, engineering, mythology, and social sciences. The philosophical basis is Korzybski's "The map is not the territory."

Research preprint: DOI [10.5281/zenodo.18471860](https://doi.org/10.5281/zenodo.18471860)

## Common Commands

No build system is currently configured. Key scripts to run directly:

```bash
# Validate model structure across ontologies
python diagnostic_models.py

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
| **M2** | Metaconcepts | 68 universal patterns applicable across all domains | `ontology/M2_MetaConcepts.jsonld/.ttl` |
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

The production file is `M2_MetaConcepts.jsonld`; `M2_MetaConcepts_Ref.jsonld` is the reference/backup version. Draft/experimental work lives in `ontology/docs/`.

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
M2  Metaconcepts          ~72 patterns   ─ tensor products of M3 dimensions
 ↕  (instantiation)
M1  Core + Domain Concepts variable      ─ generic and domain-specific concepts
 ↕  (validation)
M0  Poclets / Case Studies ~16+ models   ─ minimal complete real-world systems
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
| `M2_MetaConcepts.jsonld` | ~72 metaconcepts as tensor products of M3 dimensions, organised in 5 families: Ontological, Structural, Dynamic, Control, Information |

### M1 Ontology Files (extensible set)

| File | Role |
|------|------|
| `M1_CoreConcepts.jsonld` | Base ontology — generic transdisciplinary concepts |
| `M1_Biology.jsonld` | Domain extension — biology |
| `M1_Chemistry.jsonld` | Domain extension — chemistry |
| `M1_Optics.jsonld` | Domain extension — optics |
| `M1_Photography.jsonld` | Domain extension — photography |
| `M1_Mythology.jsonld` | Domain extension — mythology |

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

### Reference Ontologies (GitHub raw URIs)

Base: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`

| File | URI |
|------|-----|
| M3 Genesis Space | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld` |
| M3 Eagle Eye (ASFID) | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_EagleEye.jsonld` |
| M3 Sphinx Eye (REVOI) | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_SphinxEye.jsonld` |
| M2 Metaconcepts | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_MetaConcepts.jsonld` |
| M1 Core Concepts | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld` |
| M1 Biology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Biology.jsonld` |
| M1 Chemistry | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Chemistry.jsonld` |
| M1 Optics | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Optics.jsonld` |
| M1 Photography | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Photography.jsonld` |
| M1 Mythology | `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_Mythology.jsonld` |

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
