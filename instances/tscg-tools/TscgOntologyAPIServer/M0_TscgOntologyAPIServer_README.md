# TscgOntologyAPIServer

**Type:** `m3:TscgTool`  
**Version:** 1.1.0  
**Author:** Echopraxium with the collaboration of Claude AI  
**ASFID mean:** 0.858 — **REVOI mean:** 0.906 — **δ₁:** 0.0339 (Coherent)

---

## Overview

`TscgOntologyAPIServer` is a standalone FastAPI/pyoxigraph REST server that exposes the full TSCG ontology corpus via **SPARQL 1.1** and corpus-management endpoints.  
It is the **Phase 3** evolution of the `tscg-python-bridge` embedded in `TscgOntologyExplorer`: same `TscgStore` core, promoted to an independent, controllable service.

Any third-party client (curl, Postman, Python `requests`, SPARQL tools) can query the TSCG knowledge graph without TSCG-specific code — only W3C standards (SPARQL 1.1, REST/HTTP, JSON-LD, OpenAPI 3.0).

---

## Repository layout

```
instances/tscg-tools/TscgOntologyAPIServer/
├── M0_TscgOntologyAPIServer.jsonld       ← ontology (this file's companion)
├── M0_TscgOntologyAPIServer_README.md    ← this file
├── _00_start_server.bat                  ← starts the standalone server (port 8000)
├── _01_run_client_example.bat            ← runs the API test client
└── src/
    ├── tscg_api_server.py                ← FastAPI server (core)
    ├── tscg_api_cli.py                   ← CLI controller
    ├── tscg_api_client_example.py        ← Python client + demo
    ├── _setup.bat                        ← installs Python dependencies
    ├── _run_tests.bat                    ← runs the unit test suite (72 tests)
    └── requirements.txt
```

`TscgOntologyExplorer` launches the server via the **`tscg-api-bridge`** plugin:

```
TscgOntologyExplorer/plugins/tscg-api-bridge/
└── index.js     ← Electron plugin (replaces tscg-python-bridge)
```

---

## Installation

Run `_setup.bat` from `instances/tscg-tools/TscgOntologyAPIServer/src/` to install all Python dependencies in one step:

```bat
REM Windows
src\_setup.bat
```

Or manually:

```bash
cd instances/tscg-tools/TscgOntologyAPIServer/src
pip install -r requirements.txt
```

`requirements.txt` includes: `fastapi`, `uvicorn`, `pyoxigraph`, `rdflib`, `pydantic`, `requests`, `pytest`, `httpx`.

---

## Starting the server

### Quick start (Windows batch files)

| Batch file | Location | Description |
|-----------|----------|-------------|
| `_setup.bat` | `src/` | Install Python dependencies (`pip install -r requirements.txt`) |
| `_00_start_server.bat` | root | Start standalone server on `http://127.0.0.1:8000` |
| `_01_run_client_example.bat` | root | Run the API test client demo (requires server running) |
| `src\_run_tests.bat` | `src/` | Run unit test suite (72 tests, interactive module selection) |

**Typical workflow:**
```
1. src\_setup.bat                  ← install dependencies (once)
2. _00_start_server.bat            ← start server (or launch via TscgOntologyExplorer)
3. _01_run_client_example.bat      ← verify all 10 demo steps
```

> **Note:** Port 8000 is shared between the standalone server and the TscgOntologyExplorer plugin.
> If TscgOntologyExplorer is already running, the standalone server will detect the conflict
> and ask whether to start a second in-memory instance on port 8001.

---

### Option A — Python CLI (standalone, without Electron)

```bash
# Minimal (in-memory, no auto-load)
python tscg_api_cli.py start

# With persistence and auto-load
python tscg_api_cli.py start \
    --port 8000 \
    --store-path ./tscg_store.oxg \
    --ontology-dir ../../../../ontology

# Check status
python tscg_api_cli.py status

# Hot-reload all files
python tscg_api_cli.py reload

# Reload a single file
python tscg_api_cli.py reload --file path/to/M0_MyPoclet.jsonld

# Stop
python tscg_api_cli.py stop

# Restart
python tscg_api_cli.py restart --ontology-dir ../../../../ontology

# Export store as N-Triples
python tscg_api_cli.py export --output tscg_export.nt
```

### Option B — Direct (no PID management)

```bash
python tscg_api_server.py \
    --host 127.0.0.1 \
    --port 8000 \
    --store-path ./tscg_store.oxg \
    --ontology-dir ../../../../ontology \
    --log-level warning
```

### Option C — Via TscgOntologyExplorer (Electron)

The **`tscg-api-bridge`** plugin auto-starts the server when TscgOntologyExplorer launches.  
Menu items: **Start / Stop / Restart / Configure / Open Swagger UI**.  
Plugin meta keys (set in plugin config):

| Key | Default | Description |
|-----|---------|-------------|
| `tscg-python-executable` | `python` | Python binary |
| `tscg-api-host` | `127.0.0.1` | Bind address |
| `tscg-api-port` | `8000` | Bind port |
| `tscg-api-store-path` | _(in-memory)_ | Persistent `.oxg` store path |
| `tscg-api-ontology-dir` | _(none)_ | Auto-load directory |
| `tscg-api-log-level` | `warning` | uvicorn log level |

---

## API Endpoints

### Server

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Liveness probe — uptime, graph count, triple count |
| GET | `/info` | Server metadata — version, store path, library versions |
| GET | `/docs` | Swagger UI (interactive API explorer) |
| GET | `/redoc` | ReDoc documentation |

### Corpus management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/corpus/load` | Load a single JSON-LD file as a named graph |
| POST | `/corpus/load-pattern` | Load all JSON-LD files under a root directory |
| GET | `/corpus/list` | List all named graphs with their IRIs |
| GET | `/corpus/layers` | Graph counts grouped by M3/M2/M1/M0 |
| POST | `/corpus/reload` | Hot-reload a single file |
| POST | `/corpus/reload-all` | Re-parse all previously loaded files |
| DELETE | `/corpus/graph` | Remove a named graph |
| DELETE | `/corpus/clear` | Clear the entire store |
| GET | `/corpus/export` | Export full store as N-Triples |

### SPARQL

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/corpus/sparql` | Execute SPARQL SELECT / ASK / CONSTRUCT |

### IRI resolution

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/iri/expand?iri=m3:Attractor` | Expand a compact TSCG IRI |
| POST | `/iri/expand` | Expand with a supplied `@context` dict |

---

## SPARQL examples

```sparql
-- List all Poclets
PREFIX m3: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?poclet ?label WHERE {
    ?poclet m3:ontologyType m3:Poclet .
    OPTIONAL { ?poclet rdfs:label ?label }
} ORDER BY ?label
```

```sparql
-- All instances with δ₁ < 0.05 (SpectralClass Coherent)
PREFIX m0: <https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Poclet#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?label ?gap ?spectral WHERE {
    ?inst m0:epistemicGap ?gap ; rdfs:label ?label .
    OPTIONAL { ?inst m0:spectralClass ?spectral }
    FILTER(?gap < 0.05)
} ORDER BY ASC(?gap)
```

---

## Python client

```python
from tscg_api_client_example import TscgAPIClient

client = TscgAPIClient(host='localhost', port=8000)

# Load ontology
client.load_dir('../../../../ontology')

# SPARQL query
poclets = client.get_all_poclets()

# Run demo
from tscg_api_client_example import demo
demo(client, ontology_dir='../../../../ontology')
```

Run the full demo:

```bash
python tscg_api_client_example.py --ontology-dir ../../../../ontology
```

---

## Architecture

```
tscg-api-bridge (Electron plugin)
        │  spawn
        ▼
tscg_api_server.py          ← FastAPI + uvicorn
    ├── TscgStore            ← pyoxigraph named-graph store
    │   ├── Named graph per .jsonld file
    │   └── SPARQL 1.1 engine
    ├── /corpus/* endpoints  ← load / list / reload / export
    ├── /corpus/sparql       ← SPARQL SELECT/ASK/CONSTRUCT
    ├── /iri/expand          ← compact IRI → full URI
    └── /docs                ← Swagger UI (OpenAPI 3.0)

tscg_api_cli.py             ← CLI: start/stop/restart/status/reload/export
    └── PID file: TscgOntologyAPIServer/tscg_api_server.pid
```

---

## TSCG Scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| A (Attractor) | 0.82 | Triple attractor: TscgStore state + server lifecycle + persisted .oxg file |
| S (Structure) | 0.90 | 4-layer architecture (API → TscgStore → Persistence → CLI) + named graph partitioning |
| F (Flow) | 0.85 | 3 flows: HTTP request/response, persistence (in-memory ↔ .oxg), lifecycle (CLI → process) |
| It (Information) | 0.90 | Full M3→M0 hierarchy queryable; IRI expander; Swagger auto-documents all endpoints |
| D (Dynamics) | 0.82 | Async FastAPI handlers; hot-reload; CLI restart = full store rebuild |
| **ASFID mean** | **0.858** | |
| R (Representability) | 0.88 | OpenAPI spec + Swagger = formal API contract; .oxg file = diffable state snapshot |
| E (Evolvability) | 0.90 | New endpoints via @router; SPARQL extensible without code change; backends swappable |
| V (Verifiability) | 0.92 | 58-test suite (IRI ×18, TscgStore ×20, FastAPI ×20); /health testable by monitors |
| O (Observability) | 0.88 | Swagger UI; /health + /info; CLI status; all queries logged |
| Im (Interoperability) | 0.95 | SPARQL 1.1 + REST/HTTP + JSON-LD + OpenAPI 3.0 — all W3C standards |
| **REVOI mean** | **0.906** | |
| **δ₁** | **0.0339** | **SpectralClass: Coherent** |

---

## GenericConcepts mobilized (M2)

| Concept | Formula | Role |
|---------|---------|------|
| Processor | `Fm2(Process, Structure, Information) \| V` | FastAPI app as a whole |
| Interface | `S × It` | REST API boundary |
| Pipeline | `S × F × It` | Request → TscgStore → response |
| Mediator | `S × It × F \| Im` | IRI Expander + CorpusEndpoints |
| Adapter | `S × It` | Multi-format serializer |
| FeedbackLoop | `A × S × F × It × D` | Hot-reload mechanism |
| Memory | `A × It \| R` | PersistenceManager (.oxg file) |
| Context | `S × It × A` | Named graph management |

---

## Reflexivity note

`TscgOntologyAPIServer` is **doubly reflexive**:
1. It exposes its own M0 specification via `/corpus/load`, making itself queryable through SPARQL.
2. It serves the ontology that defines `m3:TscgTool`, including itself.

```sparql
SELECT ?tool WHERE { ?tool a m3:TscgTool }
-- Returns TscgOntologyAPIServer among results
```
