# TSCG Framework - Complete Architecture Guide

**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** February 7, 2026  
**Version:** 0.1.0

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Global Architecture](#global-architecture)
3. [Package Structure](#package-structure)
4. [Facade Pattern](#facade-pattern)
5. [Installation and Usage](#installation-and-usage)
6. [Integration into TSCG Repository](#integration-into-tscg-repository)
7. [Usage Examples](#usage-examples)
8. [Future Development](#future-development)
9. [FAQ](#faq)

---

## Overview

### What is TSCG Framework?

TSCG (Transdisciplinary System Construction Game) is a Python framework for:
- Loading and manipulating RDF/OWL ontologies (JSON-LD format)
- Executing SPARQL queries
- Computing metrics on systems (orthogonality, gaps, correlations)
- Exporting to various formats (Turtle, RDF/XML, etc.)
- Analyzing system models (poclets)

### Why This Architecture?

The architecture is designed following 3 core principles:

1. **Namespace Package (PEP 420)**: Modern Python convention
2. **Facade Pattern**: Stable and simple public API
3. **Separation of Concerns**: Engine ≠ CLI ≠ WebAPI

---

## Global Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                     Users                           │
│   (Python Scripts, Notebooks, Applications)         │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────┴────────┐
         │                │
    ┌────▼─────┐    ┌────▼──────┐    ┌──────▼──────┐
    │ tscg.cli │    │tscg.webapi│    │ Your App    │
    │ (REPL)   │    │ (FastAPI) │    │ (Custom)    │
    └────┬─────┘    └────┬──────┘    └──────┬──────┘
         │               │                   │
         └───────┬───────┴───────────────────┘
                 │
         ┌───────▼────────┐
         │ tscg.engine    │
         │   .facade      │  ← PUBLIC API (Stable)
         │                │
         ├────────────────┤
         │ .core          │
         │ .analysis      │  ← Internal modules
         │ .exporters     │     (Can change)
         │ .math          │
         │ .reasoner      │
         └────────────────┘
```

### Three-Layer Architecture

1. **Interface Layer** (tscg.cli, tscg.webapi, custom apps)
   - User interaction
   - Uses facade API only
   - Independent from engine internals

2. **Facade Layer** (tscg.engine.facade)
   - Public API
   - Stable interface
   - Hides implementation details

3. **Core Layer** (tscg.engine.core, .analysis, etc.)
   - Business logic
   - Internal implementation
   - Can evolve independently

---

## Package Structure

### Directory Tree

```
tscg_framework/
├── src/
│   └── tscg/                          # Namespace package
│       │
│       ├── engine/                    # Core business logic
│       │   ├── __init__.py
│       │   │
│       │   ├── core/                  # Data models & loading
│       │   │   ├── __init__.py
│       │   │   ├── models.py          # ASFIDScore, REVOIScore, etc.
│       │   │   └── ontology_loader.py # JSON-LD → RDF loader
│       │   │
│       │   ├── analysis/              # Analysis tools
│       │   │   ├── sparql/
│       │   │   │   ├── __init__.py
│       │   │   │   └── executor.py    # SPARQL query execution
│       │   │   └── metrics/
│       │   │       ├── __init__.py
│       │   │       └── orthogonality.py # Orthogonality metrics
│       │   │
│       │   ├── exporters/             # Export functionality
│       │   │   ├── __init__.py
│       │   │   └── turtle_exporter.py # Turtle format export
│       │   │
│       │   ├── facade/                # ⭐ PUBLIC API
│       │   │   ├── __init__.py
│       │   │   ├── ontology.py        # OntologyFacade
│       │   │   ├── query.py           # QueryFacade
│       │   │   ├── metrics.py         # MetricsFacade
│       │   │   └── export.py          # ExportFacade
│       │   │
│       │   ├── math/                  # Future: mathematical operations
│       │   │   ├── category/          # Category theory
│       │   │   ├── tensor/            # Tensor algebra
│       │   │   └── spaces/            # Hilbert spaces
│       │   │
│       │   └── reasoner/              # Future: OWL reasoning
│       │
│       ├── cli/                       # Command-line interfaces
│       │   ├── __init__.py
│       │   ├── repl/                  # Interactive REPL
│       │   │   ├── __init__.py
│       │   │   ├── interpreter.py     # Main REPL loop
│       │   │   └── context.py         # Session management
│       │   ├── batch/                 # Batch processing
│       │   └── utils/                 # CLI utilities
│       │
│       └── webapi/                    # REST API (Phase 2)
│           ├── __init__.py
│           ├── app.py                 # FastAPI application
│           ├── routes/                # API endpoints
│           ├── schemas/               # Pydantic schemas
│           └── middleware/            # Middleware
│
├── tests/                             # Test suite
│   └── tscg/
│       ├── engine/
│       ├── cli/
│       └── webapi/
│
├── demos/                             # Usage examples
│   └── basic_usage.py
│
├── docs/                              # Documentation
│
├── pyproject.toml                     # Poetry configuration
├── requirements.txt                   # Pip dependencies
├── README.md                          # Main documentation
├── ARCHITECTURE.md                    # This file
└── .gitignore                         # Git ignore rules
```

### Namespace Package Explanation

**What is a namespace package?**

A namespace package (PEP 420) allows splitting a package across multiple directories without `__path__` manipulation.

**Benefits:**
- ✅ Clean imports: `from tscg.engine.facade import OntologyFacade`
- ✅ No issues with `.` in folder names
- ✅ Standard Python convention
- ✅ Extensible (easy to add tscg.gui, tscg.unreal, etc.)

**How it works:**

```python
# Instead of nested imports like:
from tscg_engine_proto.core.models import ASFIDScore

# You get clean namespace:
from tscg.engine.core.models import ASFIDScore
```

---

## Facade Pattern

### What is the Facade Pattern?

The Facade Pattern provides a **simplified interface** to a complex subsystem. In TSCG:

```
Complex Internal System        Simple Public Interface
┌──────────────────┐          ┌──────────────────┐
│ OntologyLoader   │          │                  │
│ Graph            │  ◄───────┤ OntologyFacade   │
│ Metadata         │          │                  │
│ ValidationRules  │          │ - load()         │
│ ...              │          │ - get_graph()    │
└──────────────────┘          │ - list_loaded()  │
                              └──────────────────┘
```

### Why Use Facades?

**Problem Without Facade:**
```python
# User needs to understand internal structure
from tscg.engine.core.ontology_loader import OntologyLoader
from tscg.engine.core.models import OntologyMetadata

loader = OntologyLoader()
graph = loader.load("file.jsonld")
metadata = loader.metadata.get("file")
# Complex, exposes internals, can break easily
```

**Solution With Facade:**
```python
# Clean, simple, stable API
from tscg.engine.facade import OntologyFacade

ontology = OntologyFacade()
graph = ontology.load("file.jsonld")
metadata = ontology.get_metadata("file")
# Simple, stable, future-proof
```

### The Four Facades

#### 1. OntologyFacade
**Purpose:** Ontology loading and management

```python
from tscg.engine.facade import OntologyFacade

ontology = OntologyFacade()

# Load ontology
graph = ontology.load("M3_EagleEye.jsonld")

# Get loaded ontology
graph = ontology.get_graph("M3_EagleEye")

# List all loaded
names = ontology.list_loaded()

# Get metadata
metadata = ontology.get_metadata("M3_EagleEye")

# Get metaconcepts
concepts = ontology.get_metaconcepts(layer="M3")

# Count triples
count = ontology.get_triple_count("M3_EagleEye")
```

#### 2. QueryFacade
**Purpose:** SPARQL query execution

```python
from tscg.engine.facade import QueryFacade

query_api = QueryFacade(graph)

# Execute SPARQL
results = query_api.execute("""
    SELECT ?s ?p ?o 
    WHERE { ?s ?p ?o } 
    LIMIT 10
""")

# Find metaconcepts
metaconcepts = query_api.find_metaconcepts(layer="M3")

# Find related triples
related = query_api.find_related("http://example.org/concept")

# Clear cache
query_api.clear_cache()
```

#### 3. MetricsFacade
**Purpose:** Metrics computation

```python
from tscg.engine.facade import MetricsFacade
from tscg.engine.core.models import ASFIDScore

metrics = MetricsFacade()

# Compute orthogonality from dict
report = metrics.compute_orthogonality({
    "A": 0.95, "S": 0.88, "F": 0.92, "I": 0.85, "D": 0.90
})

# Compute from ASFID scores
asfid = ASFIDScore(
    attractor=0.95, structure=0.88, flow=0.92,
    information=0.85, dynamics=0.90
)
report = metrics.asfid_orthogonality(asfid)

print(f"Average orthogonality: {report.average_orthogonality:.3f}")
print(f"Condition number: {report.condition_number:.2f}")
```

#### 4. ExportFacade
**Purpose:** Ontology export to various formats

```python
from tscg.engine.facade import ExportFacade

export = ExportFacade()

# Export to Turtle
result = export.to_turtle(graph, "output.ttl")
if result.success:
    print(f"Exported {result.triples_count} triples")

# Export to any RDF format
result = export.to_file(graph, "output.rdf", format="xml")
```

### Facade Design Rules

**✅ DO:**
- Use facades for all external access
- Keep facade methods simple and high-level
- Document all public methods
- Maintain backward compatibility

**❌ DON'T:**
- Access internal modules directly from outside
- Expose complex internal structures
- Break facade API without major version bump

---

## Installation and Usage

### Installation Methods

#### Method 1: Full Installation (Recommended)
```bash
# Clone repository
git clone https://github.com/Echopraxium/tscg.git
cd tscg

# Install with all features
pip install -e .[full]
```

#### Method 2: Minimal Installation (Engine Only)
```bash
# For programmatic use only (no CLI)
pip install -e .
```

#### Method 3: Modular Installation
```bash
# Engine + CLI
pip install -e .[cli]

# Engine + WebAPI (future)
pip install -e .[webapi]
```

### Dependencies Overview

**Core Dependencies (always installed):**
- `rdflib` - RDF graph manipulation
- `pydantic` - Data validation
- `numpy` - Numerical operations
- `scipy` - Scientific computing

**CLI Dependencies (optional):**
- `prompt-toolkit` - Advanced REPL
- `rich` - Beautiful terminal output
- `typer` - CLI framework

**WebAPI Dependencies (optional, Phase 2):**
- `fastapi` - REST API framework
- `uvicorn` - ASGI server

---

## Integration into TSCG Repository

### Current TSCG Repository Structure

```
tscg/                              # GitHub repository
├── ontology/                      # M3, M2, M1 ontologies
├── system-models/                 # M0 poclets
├── docs/                          # Documentation
├── src/
│   ├── TSCG.Orchestrator/        # C# orchestrator
│   └── TSCG.JsonldValidator/     # Validator
└── cli_tools/                     # Existing tools
```

### After Integration

```
tscg/                              # GitHub repository
├── ontology/                      # (unchanged)
├── system-models/                 # (unchanged)
├── docs/                          # (unchanged)
├── src/
│   ├── TSCG.Orchestrator/        # (unchanged)
│   ├── TSCG.JsonldValidator/     # (unchanged)
│   └── tscg/                      # ← NEW: Python engine
│       ├── engine/
│       ├── cli/
│       └── webapi/
├── cli_tools/                     # (unchanged)
├── pyproject.toml                 # ← NEW: Python config
├── requirements.txt               # ← NEW: Dependencies
└── README.md                      # ← UPDATE: Add Python section
```

### Integration Steps

#### Step 1: Copy Files

```bash
# From tscg_framework directory
cp -r src/tscg /path/to/your/tscg/repo/src/
cp pyproject.toml /path/to/your/tscg/repo/
cp requirements.txt /path/to/your/tscg/repo/
```

#### Step 2: Update .gitignore

```bash
# Append Python-specific ignores
cat tscg_framework/.gitignore >> /path/to/your/tscg/repo/.gitignore
```

#### Step 3: Install

```bash
cd /path/to/your/tscg/repo
pip install -e .[cli]
```

#### Step 4: Verify

```bash
# Test import
python -c "from tscg.engine.facade import OntologyFacade; print('OK')"

# Test CLI
tscg-repl
```

#### Step 5: Update Main README

Add section to your main README.md:

```markdown
## Python Business Logic Engine

TSCG now includes a Python engine for ontology manipulation and analysis.

### Quick Start

```bash
# Install
pip install -e .[cli]

# Start REPL
tscg-repl

# Programmatic usage
from tscg.engine.facade import OntologyFacade
ontology = OntologyFacade()
graph = ontology.load("ontology/M3_EagleEye.jsonld")
```

See [src/tscg/README.md](src/tscg/README.md) for full documentation.
```

---

## Usage Examples

### Example 1: Load and Query Ontology

```python
from tscg.engine.facade import OntologyFacade, QueryFacade

# Load ontology
ontology = OntologyFacade()
graph = ontology.load("ontology/M3_EagleEye.jsonld")

print(f"Loaded {len(graph)} triples")

# Query metaconcepts
query = QueryFacade(graph)
results = query.execute("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?concept ?label
    WHERE {
        ?concept rdfs:label ?label .
        FILTER(isIRI(?concept))
    }
    LIMIT 5
""")

print(f"Found {results.row_count} metaconcepts:")
for row in results.bindings:
    print(f"  - {row['label']}")
```

### Example 2: Compute Metrics

```python
from tscg.engine.facade import MetricsFacade
from tscg.engine.core.models import ASFIDScore

# Create ASFID scores
asfid = ASFIDScore(
    attractor=0.95,
    structure=0.88,
    flow=0.92,
    information=0.85,
    dynamics=0.90
)

print(f"Overall ASFID: {asfid.overall:.2f}")

# Compute orthogonality
metrics = MetricsFacade()
report = metrics.asfid_orthogonality(asfid)

print(f"\nOrthogonality Analysis:")
print(f"  Most orthogonal: {report.most_orthogonal_pair}")
print(f"  Similarity: {report.min_similarity:.3f}")
print(f"  Average orthogonality: {report.average_orthogonality:.3f}")
print(f"  Condition number: {report.condition_number:.2f}")
```

### Example 3: Export to Turtle

```python
from tscg.engine.facade import OntologyFacade, ExportFacade

# Load ontology
ontology = OntologyFacade()
graph = ontology.load("ontology/M3_SphinxEye.jsonld")

# Export to Turtle
export = ExportFacade()
result = export.to_turtle(graph, "M3_SphinxEye_export.ttl")

if result.success:
    print(f"✓ {result.message}")
    print(f"  Path: {result.path}")
    print(f"  Triples: {result.triples_count}")
else:
    print(f"✗ Export failed: {result.message}")
```

### Example 4: Interactive REPL Session

```bash
$ tscg-repl

TSCG v0.1.0 Interactive Shell
Type 'help' for commands, 'exit' to quit

>>> load ontology/M3_EagleEye.jsonld
✓ Loaded: M3_EagleEye
  Triples: 127
  Active ontology: M3_EagleEye

>>> show ontologies
┌────────────────┬───────┬─────────┬────────┐
│ Name           │ Layer │ Triples │ Active │
├────────────────┼───────┼─────────┼────────┤
│ M3_EagleEye    │ M3    │ 127     │ ✓      │
└────────────────┴───────┴─────────┴────────┘

>>> show metaconcepts
┌────────────┬───────┬──────────────────────┐
│ Label      │ Layer │ URI                  │
├────────────┼───────┼──────────────────────┤
│ Attractor  │ M3    │ ...eagle_eye#Attr... │
│ Structure  │ M3    │ ...                  │
│ Flow       │ M3    │ ...                  │
│ Information│ M3    │ ...                  │
│ Dynamics   │ M3    │ ...                  │
└────────────┴───────┴──────────────────────┘

>>> export M3_EagleEye_export.ttl
✓ Exported 127 triples to M3_EagleEye_export.ttl

>>> sparql SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 3
Results (3 rows)
┌──────────────┬──────────────┬──────────────┐
│ s            │ p            │ o            │
├──────────────┼──────────────┼──────────────┤
│ ...          │ ...          │ ...          │
└──────────────┴──────────────┴──────────────┘

>>> metrics orthogonality
Computing orthogonality for sample ASFID scores...

Orthogonality Matrix:
     A     S     F     I     D
A   1.00  0.00  0.00  0.00  0.00
S   0.00  1.00  0.00  0.00  0.00
...

Analysis:
  Average orthogonality: 1.000
  Condition number: 1.00

>>> context
Session Context

Loaded ontologies: 1
Active ontology: M3_EagleEye
Triples in active: 127
Variables defined: 0
Command history: 7 commands

>>> exit
Goodbye!
```

### Example 5: Batch Processing Script

```python
#!/usr/bin/env python3
"""
Batch process multiple ontologies
"""

from pathlib import Path
from tscg.engine.facade import OntologyFacade, QueryFacade, ExportFacade

def process_ontology(filepath):
    """Process a single ontology"""
    ontology = OntologyFacade()
    export = ExportFacade()
    
    # Load
    print(f"Processing: {filepath}")
    graph = ontology.load(filepath)
    
    # Query metaconcepts
    query = QueryFacade(graph)
    results = query.find_metaconcepts()
    print(f"  Metaconcepts: {results.row_count}")
    
    # Export to Turtle
    output = filepath.replace(".jsonld", "_export.ttl")
    result = export.to_turtle(graph, output)
    if result.success:
        print(f"  Exported: {output}")
    
    return graph

# Process all M3 ontologies
ontology_dir = Path("ontology")
for ontology_file in ontology_dir.glob("M3_*.jsonld"):
    process_ontology(str(ontology_file))
    print()
```

---

## Future Development

### Phase 2: Advanced Features (6-8 weeks)

**SPARQL Enhancements:**
- Query templates library
- Interactive query builder
- Saved queries management

**Validation:**
- OWL reasoner integration (Owlready2/HermiT)
- SHACL constraint validation
- Consistency checking

**Advanced Metrics:**
- Gap detection algorithms
- Correlation matrices
- Clustering (K-means, hierarchical)
- Entropy calculations

**Ontology Comparison:**
- Diff between ontologies
- Poclet similarity metrics
- Structural comparison

**REST API (tscg.webapi):**
```python
# Future WebAPI implementation
from fastapi import FastAPI
from tscg.engine.facade import OntologyFacade

app = FastAPI()
ontology = OntologyFacade()

@app.get("/ontologies")
def list_ontologies():
    return ontology.list_loaded()

@app.post("/ontologies/load")
def load_ontology(filepath: str):
    graph = ontology.load(filepath)
    return {"triples": len(graph)}

@app.post("/query")
def execute_query(sparql: str):
    # Execute and return results
    pass
```

### Phase 3: Mathematical Formalism (8-10 weeks)

**Category Theory:**
```python
# Future: tscg.engine.math.category
from tscg.engine.math.category import Category, Functor

# Define TSCG as category
tscg_cat = Category("TSCG")
functor = Functor(source=tscg_cat, target=other_cat)
```

**Tensor Algebra:**
```python
# Future: tscg.engine.math.tensor
from tscg.engine.math.tensor import TensorProduct

# Metaconcept combinations
result = TensorProduct(metaconcept_a, metaconcept_b)
# A ⊗ S ⊗ F → Composite metaconcept
```

**Hilbert Spaces:**
```python
# Future: tscg.engine.math.spaces
from tscg.engine.math.spaces import HilbertSpace

# 10D Genesis Space
genesis = HilbertSpace(dimensions=10)
genesis.decompose()  # → ASFID(5D) ⊕ REVOI(5D)
```

**Cascade Modeling:**
```python
# Future: Cascade operations
from tscg.engine.math.cascade import Cascade

# PIFA → REVOI cascade
cascade = Cascade(source="PIFA", target="REVOI")
cascade.evaluate(poclet)
```

### Phase 4: Integration & Interfaces (8-10 weeks)

**GUI (Streamlit):**
```python
# Future: tscg.gui
import streamlit as st
from tscg.engine.facade import OntologyFacade

st.title("TSCG Ontology Explorer")
ontology = OntologyFacade()
# Interactive visualization
```

**Unreal Engine Bridge:**
```python
# Future: tscg.unreal
from tscg.unreal import UnrealBridge

bridge = UnrealBridge()
bridge.load_simulation(poclet)
bridge.run()
```

---

## FAQ

### General Questions

**Q: What is the difference between tscg.engine, tscg.cli, and tscg.webapi?**

A: 
- `tscg.engine` = Core business logic (library)
- `tscg.cli` = Command-line interface (uses engine)
- `tscg.webapi` = REST API (uses engine)

Think of it like: engine is the car, CLI and WebAPI are different interfaces to drive it.

**Q: Can I use only the engine without CLI?**

A: Yes! Just install with `pip install -e .` (no extras). Perfect for use in scripts or notebooks.

**Q: Why use facades instead of direct imports?**

A: Facades provide:
- Stable API (won't break with internal changes)
- Simpler interface (hide complexity)
- Better documentation
- Future-proof (can optimize internals without breaking your code)

### Installation Questions

**Q: What Python version is required?**

A: Python 3.10 or higher.

**Q: Can I install just the CLI without the full engine?**

A: No, CLI depends on engine. But you can install engine without CLI: `pip install -e .`

**Q: How do I update dependencies?**

A:
```bash
# With poetry
poetry update

# With pip
pip install --upgrade -r requirements.txt
```

### Usage Questions

**Q: How do I load ontologies from the project directory?**

A:
```python
from tscg.engine.facade import OntologyFacade

ontology = OntologyFacade()
graph = ontology.load("/mnt/project/M3_EagleEye.jsonld")
```

**Q: Can I query multiple ontologies at once?**

A: Not directly, but you can merge graphs:
```python
from rdflib import Graph

combined = Graph()
combined += ontology.get_graph("M3_EagleEye")
combined += ontology.get_graph("M3_SphinxEye")

query = QueryFacade(combined)
results = query.execute("SELECT ?s ?p ?o LIMIT 10")
```

**Q: How do I save REPL history?**

A: History is automatically saved in `.tscg_history` file.

### Development Questions

**Q: How do I add a new facade method?**

A: 
1. Add method to appropriate facade (e.g., `OntologyFacade`)
2. Implement using internal modules
3. Add docstring with example
4. Add test
5. Update `__all__` in `__init__.py`

**Q: Can I access internal modules directly?**

A: Technically yes, but **don't**. Internal modules can change. Always use facades for external code.

**Q: How do I contribute?**

A: Follow standard GitHub workflow:
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Troubleshooting

**Q: Import error: "No module named 'tscg'"**

A: Make sure you installed the package:
```bash
pip install -e .
```

**Q: REPL command not found: "tscg-repl: command not found"**

A: Install with CLI extras:
```bash
pip install -e .[cli]
```

**Q: RDF parsing error when loading ontology**

A: Check:
- File exists and is valid JSON-LD
- File path is correct
- No encoding issues (should be UTF-8)

**Q: SPARQL query fails with "No graph loaded"**

A: Set graph before querying:
```python
query = QueryFacade()
query.set_graph(graph)  # Don't forget this!
results = query.execute("SELECT ?s ?p ?o LIMIT 10")
```

---

## Appendices

### A. Complete API Reference

See [docs/API_REFERENCE.md](docs/API_REFERENCE.md) for complete API documentation.

### B. Design Decisions

**Why namespace packages?**
- Standard Python convention (PEP 420)
- Clean imports
- Extensible structure

**Why facade pattern?**
- Stable public API
- Hide complexity
- Enable refactoring without breaking changes

**Why separate CLI from engine?**
- Reusability (engine can be used without CLI)
- Testability (can test engine without UI)
- Multiple interfaces (can add GUI, WebAPI, etc.)

### C. Naming Conventions

**Packages:** lowercase with underscores (`tscg.engine`)
**Classes:** PascalCase (`OntologyFacade`)
**Functions/Methods:** snake_case (`load_ontology`)
**Constants:** UPPER_CASE (`TSCG_BASE`)
**Private:** Leading underscore (`_internal_method`)

### D. TSCG-Specific Terms

- **ASFID**: Attractor, Structure, Flow, Information, Dynamics (Territory/EagleEye)
- **REVOI**: Representability, Evolvability, Verifiability, Observability, Interoperability (Map/SphinxEye)
  - **CRITICAL**: R = Representability, NOT Reproducibility
- **Poclet**: Proof-of-concept system instance (minimal complete system)
- **Metaconcept**: Transdisciplinary pattern validated across domains
- **ValueSpace**: Attribute enrichment for metaconcepts
- **Bicephalous**: Dual perspective architecture (EagleEye + SphinxEye)

### E. Version History

**v0.1.0 (2026-02-07)** - Initial release
- Namespace package structure
- Facade API pattern
- Basic REPL functionality
- SPARQL query execution
- Orthogonality metrics
- Turtle export

---

## Contact & Support

**Repository:** https://github.com/Echopraxium/tscg  
**Author:** Echopraxium with the collaboration of Claude AI  
**License:** MIT

For issues, questions, or contributions, please refer to the main TSCG repository.

---

**Generated:** February 7, 2026  
**Document Version:** 1.0  
**Framework Version:** TSCG v14.3.3 + Python Engine v0.1.0
