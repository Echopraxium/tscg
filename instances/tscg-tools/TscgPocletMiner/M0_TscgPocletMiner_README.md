# TscgPocletMiner — TSCG Tool

**Layer:** M0 — TscgTool  
**Version:** 1.1.0  
**Date:** 2026-03-16  
**Authors:** Echopraxium with the collaboration of Claude AI  
**Repository path:** `instances/tscg-tools/tscg-poclet-miner/`

---

## Purpose

TscgPocletMiner is an Electron desktop application for **discovering and evaluating TSCG poclet candidates**. It combines three complementary intelligence sources — all without any external LLM:

1. **Corpus invariants** — deterministic scoring against the 21 validated poclets
2. **TSCG RAG** — semantic queries into the ChromaDB vector database (similar instances + GenericConcept suggestions)
3. **Web search** — Wikipedia, Google Scholar, DuckDuckGo, Gemini for external validation

---

## TSCG Classification

| Property | Value |
|---|---|
| Type | `m3:TscgTool` — reflexive (domain IS TSCG itself) |
| ASFID mean | 0.826 |
| REVOI mean | 0.884 |
| Epistemic gap δ | 0.06 |
| Runtime LLM | **None** |
| RAG backend | ChromaDB + `all-MiniLM-L6-v2` (local, offline) |
| Tech stack | Electron, Node.js, Vanilla JS, Python (bridge) |

---

## Architecture: RAG Bridge

The TSCG RAG is Python-based. TscgPocletMiner calls it via a **`child_process.spawn` bridge**:

```
Electron renderer
    ↓ IPC (ragQuery)
main.js
    ↓ spawn(python rag_bridge.py --query "..." --mode similar_poclets)
rag_bridge.py
    ↓ subprocess
query_tscg_rag.py (ChromaDB)
    ↓ JSON to stdout
main.js → renderer (results array)
```

**Why `child_process.spawn`?** Zero additional dependencies — reuses the existing `query_tscg_rag.py` CLI as-is. Python must be in PATH (or set `TSCG_PYTHON` env var).

### RAG Bridge modes

| Mode | Filter | Used in | Purpose |
|---|---|---|---|
| `similar_poclets` | M0 layer, `jsonld_entry` | Round 2 | Find existing instances semantically closest to the candidate |
| `suggest_concepts` | M2 layer, `jsonld_entry` | Round 5 | Suggest relevant GenericConcepts based on ASFID profile |

---

## The 5-Round Wizard

### Round 1 — Domain Identification
- Enter system name + domain
- Gap analysis against 10 covered domains (chips, highlighted if new)

### Round 2 — Web Verification + RAG Similar Poclets ⚡
- Web search URLs auto-generated (Wikipedia, DuckDuckGo, Scholar)
- **RAG auto-triggered**: `similar_poclets` query finds the nearest M0 instances in the corpus
- RAG results shown with similarity score, label, definition excerpt

### Round 3 — ASFID Pre-Screening
- 5 sliders (A, S, F, I, D) with contextual hints
- Live bars update in sidebar

### Round 4 — Type Discriminant
- Poclet / TransDisclet / SystemicFramework selection
- Warning raised for TransDisclet (structural homology required)

### Round 5 — Invariants + RAG GenericConcepts + Verdict ⚡
- 9 invariant checkboxes with examples
- **RAG auto-triggered**: `suggest_concepts` builds query from ASFID profile + system name → returns relevant M2 GenericConcepts with tensor formulas
- Final verdict computed (deterministic)
- Gemini URL opened for domain-wide candidate suggestions
- **Export**: JSON scaffold enriched with RAG-suggested concepts and similar poclets

---

## Scoring Thresholds

| Verdict | Invariants (/ 9) | ASFID mean |
|---|---|---|
| 🟢 Strong Candidate | ≥ 8 | ≥ 0.75 |
| 🟡 Candidate | ≥ 6 | ≥ 0.60 |
| 🟠 Weak Candidate | ≥ 4 | ≥ 0.50 |
| 🔴 Rejected | < 4 | < 0.50 |

---

## Files

| File | Description |
|---|---|
| `M0_TscgPocletMiner.jsonld` | TscgTool ontology instance |
| `M0_TscgPocletMiner_README.md` | This file |
| `package.json` | Electron app manifest |
| `main.js` | Main process — IPC handlers including `rag-query` (child_process.spawn) |
| `preload.js` | Secure IPC bridge — exposes `tscgAPI.ragQuery()` |
| `index.html` | Wizard UI with RAG result panels |
| `renderer.js` | Wizard logic, RAG integration, scoring engine |
| `rag_bridge.py` | Python bridge: calls `query_tscg_rag.py`, outputs JSON to stdout |
| `poclet_corpus_profile.json` | Reference corpus (21 poclets + invariants + gap analysis) |

---

## Running the App

```bash
cd instances/tscg-tools/tscg-poclet-miner
npm install
npm start
```

**Python requirement:** `python` must be in PATH. If not:
```bash
# Windows
set TSCG_PYTHON=C:\Python312\python.exe
npm start

# macOS/Linux
TSCG_PYTHON=/usr/bin/python3 npm start
```

**First RAG query:** `query_tscg_rag.py` auto-decompresses `db_tscg_rag.tar.gz` (~21 MB) on first run. Subsequent queries are fast.

---

## ASFID/REVOI Analysis

**Eagle Eye (Territory)**

| Dim | Score | Rationale |
|---|---|---|
| A — Attractor | 0.75 | Convergence toward accept/reject verdict via wizard + RAG enrichment |
| S — Structure | 0.90 | 5-round wizard, corpus JSON, invariant grid, RAG bridge, scoring engine |
| F — Flow | 0.88 | User → Q&A → RAG spawn → scoring → web search → verdict → export |
| I — Information | 0.85 | ASFID scores, RAG semantic results, gap flags, verdict levels |
| D — Dynamics | 0.75 | RAG adapts to each query; corpus grows with new poclets |

**Sphinx Eye (Map)**

| Dim | Score | Rationale |
|---|---|---|
| R — Representability | 0.90 | RAG results + wizard steps fully visible; scorecard human-readable |
| E — Evolvability | 0.88 | RAG DB auto-rebuilds as corpus grows; corpus profile externalized |
| V — Verifiability | 0.92 | Deterministic scoring + RAG traceable to ontology files + web confirmation |
| O — Observability | 0.90 | Every RAG result, score, and step displayed transparently |
| I — Interoperability | 0.82 | JSON export with RAG concepts; rag_bridge.py reusable by other tools |

**Epistemic gap δ = 0.06** — Reduced from v1.0.0 (0.08): RAG semantic context compensates for user's limited TSCG framework knowledge.
