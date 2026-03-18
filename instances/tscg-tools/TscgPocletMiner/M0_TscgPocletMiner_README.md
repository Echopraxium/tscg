# TscgPocletMiner — TSCG Tool

**Layer:** M0 — TscgTool  
**Version:** 1.2.0  
**Date:** 2026-03-17  
**Authors:** Echopraxium with the collaboration of Claude AI  
**Repository path:** `instances/tscg-tools/TscgPocletMiner/`

---

## Purpose

TscgPocletMiner is an Electron desktop application for **discovering and evaluating TSCG poclet candidates**. It combines three complementary intelligence sources — all without any external LLM at runtime:

1. **Corpus invariants** — deterministic scoring against the validated poclet corpus
2. **JS-native RAG** — semantic queries via `@xenova/transformers` (all-MiniLM-L6-v2, local/offline)
3. **Web search** — Wikipedia, Google, DuckDuckGo, Google Scholar, Gemini, DeepSeek

---

## Poclet Creation Pipeline

TscgPocletMiner supports the first two stages of the full poclet creation pipeline. The complete pipeline is:

### Stage 1 — Candidate Discovery *(TscgPocletMiner wizard)*

**Step 1 — Name & Domain** (Round 1)
- Enter the system name and its primary discipline
- Automatic gap analysis against the current corpus (domain chips, new-domain flag)
- Optionally select a suggested candidate from the priority list

**Step 2 — System Description** (Round 2)
- Open external sources (Wikipedia, Google, Scholar, Gemini, DeepSeek) to document the system
- **Paste relevant content** (Wikipedia excerpt, Gemini/DeepSeek response) into the paste zone:
  - `doc_quality` auto-adjusted from text length
  - ASFID dimensions pre-scored from keyword signatures
  - RAG similarity search re-run with enriched context
- Adjust the documentation quality slider manually if needed

**Step 3 — ASFID Pre-Screening** (Round 3)
- Score each ASFID dimension (A, S, F, I, D) with contextual hints
- Sliders are pre-populated from the paste zone analysis — adjust as needed

**Step 4 — Type Discriminant** (Round 4)
- Select: **Poclet** / **TransDisclet** / **SystemicFramework**
- TransDisclet warning: structural homology (same ASFID tensor formula) required across disciplines

**Step 5 — Invariants, GenericConcepts & Verdict** (Round 5)
- Check applicable invariants (7 criteria with examples)
- RAG auto-suggests relevant M2 GenericConcepts with tensor formulas
- Final verdict computed: Strong Candidate / Candidate / Weak / Rejected
- **Export JSON scaffold** — contains all pre-scores, suggested concepts, system metadata

---

### Stage 2 — Ontological Analysis *(with Claude AI)*

Using the exported JSON scaffold and the pasted description as input:

**Step 3 — Analysis**
- Identify candidate **M2 GenericConcepts** (new transdisciplinary patterns not yet in M2)
- Identify candidate **M1_CoreConcepts** (`KnowledgeFieldConceptCombo` — synergistic combinations)
- Identify if a **domain M1 extension** is needed (e.g. `M1_Biology`, `M1_Economics`) and which concepts to add or create in it

**Step 4 — Ontology Modelling**
- Create `M0_<PascalCaseName>.jsonld` — the poclet ontology instance
- Create `M0_<PascalCaseName>_README.md` — English documentation
- Files are stored in `instances/poclets/<PascalCaseName>/`
  - Folder name = PascalCase name of the system (1–4 words, e.g. `ButterflyMetamorphosis`, `KindlebergerMinsky`)

**Step 5 — Simulation**
- Generate an Electron JS desktop simulation of the poclet
- Stored alongside the ontology files in the poclet folder

---

## TSCG Classification

| Property | Value |
|---|---|
| Type | `m3:TscgTool` — reflexive (domain IS TSCG itself) |
| ASFID mean | 0.836 |
| REVOI mean | 0.884 |
| Epistemic gap delta | 0.05 |
| Runtime LLM | **None** |
| RAG backend | `@xenova/transformers` all-MiniLM-L6-v2 (JS-native, offline) |
| Tech stack | Electron, Node.js, Vanilla JS |

---

## Architecture

```
Electron renderer (index.html + renderer.js)
    | IPC
main.js
    |-- rag_engine.js      — JS-native RAG (@xenova/transformers)
    |       |-- poclet_corpus_profile.json  — validated poclet corpus
    |       +-- m2_concepts_corpus.json     — M2 GenericConcepts corpus
    |-- rebuild_corpus.js  — regenerates poclet_corpus_profile.json
    +-- restore_rag.js     — decompresses db_tscg_rag.tar.gz (ChromaDB archive)
```

### RAG Modes

| Mode | Corpus | Used in | Purpose |
|---|---|---|---|
| `similar_poclets` | `poclet_corpus_profile.json` | Round 2 | Find existing poclets semantically closest to the candidate |
| `suggest_concepts` | `m2_concepts_corpus.json` | Round 5 | Suggest M2 GenericConcepts based on ASFID profile + description |

---

## The 5-Round Wizard

### Round 1 — Domain Identification
- Enter system name + domain
- Gap analysis chips (green = covered, gold = new domain)
- Click any priority candidate to auto-fill and advance

### Round 2 — Web Verification + Description
- 6 search buttons: Wikipedia, Google, DuckDuckGo, Scholar, Gemini, DeepSeek
  - DeepSeek: pre-built ASFID query copied to clipboard, opens `chat.deepseek.com`
  - Visited buttons turn teal
- **Paste zone**: copy/paste any source text:
  - Auto-scores ASFID dimensions from keyword signatures
  - Auto-sets documentation quality from text length
  - Re-runs RAG with enriched context (debounced 800ms)
  - ASFID hint chips show matched keywords per dimension
- Documentation quality slider (0–3)

### Round 3 — ASFID Pre-Screening
- 5 sliders (A, S, F, I, D) with contextual hints
- Pre-populated from paste zone analysis — adjust manually as needed
- Live bars update in sidebar

### Round 4 — Type Discriminant
- Poclet / TransDisclet / SystemicFramework
- Warning for TransDisclet (structural homology required)

### Round 5 — Invariants + GenericConcepts + Verdict
- 7 invariant checkboxes with examples
- RAG auto-triggers `suggest_concepts` — returns M2 GenericConcepts with tensor formulas
- Verdict computed deterministically
- Gemini suggestion button for domain-wide candidates
- **Export JSON scaffold** feeds Stage 2 (ontology modelling with Claude AI)

---

## Scoring Thresholds

| Verdict | Invariants (/ 7) | ASFID mean |
|---|---|---|
| Strong Candidate | >= 6 | >= 0.75 |
| Candidate | >= 4 | >= 0.60 |
| Weak Candidate | >= 2 | >= 0.45 |
| Rejected | < 2 | < 0.45 |

---

## Files

| File | Description |
|---|---|
| `M0_TscgPocletMiner.jsonld` | TscgTool ontology instance |
| `M0_TscgPocletMiner_README.md` | This file |
| `package.json` | Electron app manifest (`@xenova/transformers` dependency) |
| `main.js` | Main process — IPC handlers, RAG init, corpus rebuild |
| `preload.js` | Secure IPC bridge — exposes `window.tscgAPI` |
| `index.html` | Wizard UI — 5 rounds + sidebar + paste zone |
| `renderer.js` | Wizard logic, paste analysis, RAG integration, scoring engine |
| `rag_engine.js` | JS-native RAG engine — auto-restores ChromaDB archive on first init |
| `restore_rag.js` | Zero-dependency TAR.GZ decompressor (single + multi-volume) |
| `rebuild_corpus.js` | Scans `instances/poclets/` — regenerates `poclet_corpus_profile.json` |
| `poclet_corpus_profile.json` | Validated poclet corpus + gap analysis + scoring thresholds |
| `m2_concepts_corpus.json` | M2 GenericConcepts corpus for RAG embedding |

### Corpus maintenance scripts (Python)

| Script | Purpose |
|---|---|
| `rebuild_corpus.py` | Regenerates `poclet_corpus_profile.json` from `instances/poclets/` |
| `rebuild_m2_corpus.py` | Regenerates `m2_concepts_corpus.json` from `M2_GenericConcepts.jsonld` |

Run after adding new poclets or updating M2:
```bash
python rebuild_corpus.py
python rebuild_m2_corpus.py
```

---

## Running the App

```bash
cd instances/tscg-tools/TscgPocletMiner
npm install
npm start
```

**First startup:** `rag_engine.js` auto-decompresses `src/tscg/rag/db_tscg_rag.tar.gz` into `src/tscg/rag/db_extracted/` if not already present.

**Refresh corpus** after adding poclets: click **Refresh Corpus** in the UI, or run the Python scripts above.

---

## ASFID/REVOI Analysis

**Eagle Eye (Territory)**

| Dim | Score | Rationale |
|---|---|---|
| A — Attractor | 0.80 | Convergence toward accept/reject verdict via wizard + RAG + paste analysis |
| S — Structure | 0.90 | 5-round wizard, corpus JSON, invariant grid, RAG engine, paste zone |
| F — Flow | 0.88 | User input -> paste -> RAG -> ASFID pre-score -> invariants -> verdict -> export |
| I — Information | 0.85 | ASFID scores, RAG results, keyword hits, gap flags, verdict levels |
| D — Dynamics | 0.75 | RAG adapts per query; corpus grows; paste zone re-triggers RAG in real time |

**Sphinx Eye (Map)**

| Dim | Score | Rationale |
|---|---|---|
| R — Representability | 0.90 | Wizard steps, RAG results, ASFID chips all visible and human-readable |
| E — Evolvability | 0.88 | Corpus auto-rebuilds; M2 corpus refreshable; paste zone enriches context |
| V — Verifiability | 0.92 | Deterministic scoring + RAG traceable to ontology files + web confirmation |
| O — Observability | 0.90 | Every score, RAG result, keyword hit, and step displayed transparently |
| I — Interoperability | 0.82 | JSON export feeds Stage 2 (Claude AI); corpus scripts reusable by other tools |

**Epistemic gap delta = 0.05** — Reduced from v1.1.0 (0.06): paste zone provides richer semantic context, narrowing the gap between the candidate description and the TSCG analysis.
