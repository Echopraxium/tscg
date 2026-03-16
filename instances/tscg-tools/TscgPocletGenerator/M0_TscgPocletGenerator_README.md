# TSCG Poclet Generator — TscgTool Analysis

**Framework:** TSCG v15.9.0  
**Ontology type:** `m3:TscgTool`  
**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-03-06  
**Version:** 1.0.0  
**File:** `M0_TscgPocletGenerator.jsonld`

---

## Overview

The **TSCG Poclet Generator** is a PySide6 desktop application that operationalizes the TSCG
framework as a generation pipeline. It takes a natural language description of any system and
produces a complete poclet deliverable set:

| Output | Description |
|--------|-------------|
| `M0_SystemName.jsonld` | JSON-LD ontology with ASFID/REVOI scoring |
| `M0_SystemName_README.md` | Structured documentation |
| `system_name_sim.py` | Pygame simulation |

This ontology is a **dogfooding** instance: the TSCG framework analyzes its own generation
tool, producing a `m3:TscgTool` ontology that describes the tool that generates ontologies.

> *"The map describes a tool that draws maps. The tool that draws maps is itself on the map."*
> — Korzybski extended reading

---

## Architecture — 8 Components

```
┌─────────────────────────────────────────────────────────┐
│  User Request (natural language)                        │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │   Smart Prompt Loader   │  ← TSCG grammar (v15.9.0)
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │     RAG Augmentor       │  ← ChromaDB + all-MiniLM-L6-v2
          │  (tscg_rag_augmentor)   │    top-K relevant TSCG chunks
          └────────────┬────────────┘
                       │  augmented system prompt
          ┌────────────▼────────────┐
          │   Backend Selector      │  ← Anthropic / Gemini /
          │   + LLM Worker          │    Ollama / OpenAI-compat
          │   (QThread)             │
          └────────────┬────────────┘
                       │  raw LLM output
          ┌────────────▼────────────┐
          │   Output Parser         │  ← regex on fenced code blocks
          └────────────┬────────────┘
                       │
          ┌────────────▼────────────┐
          │   Output Tabs (×3)      │  ← JSON-LD / README / sim.py
          │   + History Manager     │    with syntax highlighting
          └─────────────────────────┘
```

---

## TSCG Bicephalous Analysis

### Eagle Eye — Territory Space (ASFID)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **A** Attractor  | 0.88 | Converges toward a validated poclet deliverable set. RAG augmentation reinforces this attractor by grounding LLM output in validated TSCG examples. |
| **S** Structure  | 0.92 | 8-component modular architecture with clear separation of concerns. Layered: UI / Generation Logic / LLM Backend / RAG Pipeline. |
| **F** Flow       | 0.90 | Unidirectional pipeline: Request → RAG → Prompt → LLM → Parse → Display. Well-bounded sequential stages. |
| **I** Information| 0.93 | High information density: natural language → JSON-LD + scored vectors + tensor formulas + Pygame code. |
| **D** Dynamics   | 0.82 | Non-blocking QThread, lazy RAG init, settings persistence, history. Slightly lower: dynamics are sequential rather than adaptive. |
| **Mean**         | **0.89** | |

### Sphinx Eye — Map Space (REVOI)

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **R** Representability | 0.90 | Well-modeled as a pipeline FSM. TSCG framework provides its own representational vocabulary for this analysis. |
| **E** Evolvability     | 0.92 | Highly modular: new backends, templates, RAG sources, output formats addable with minimal coupling. |
| **V** Verifiability    | 0.84 | JSON-LD outputs are OWL/SPARQL-validatable. No automated test suite yet, hence 0.84. |
| **O** Observability    | 0.88 | Multiple surfaces: status bar, progress bar, RAG chunk display with relevance scores, history panel, syntax highlighting. |
| **I** Interoperability | 0.93 | 4 standard LLM protocols + PySide6 cross-platform + standard JSON-LD + Markdown output. |
| **Mean**               | **0.894** | |

### Epistemic Gap δ

```
δ = ||(ASFID - REVOI)|| = 0.136

ΔVector = (A: −0.02, S: 0.00, F: +0.06, I: +0.05, D: −0.11)
```

**Interpretation:** Small gap — the map closely follows the territory. The main
discrepancy on the D axis (territory 0.82 vs. map 0.93) reflects that the tool's
adaptive behavior is partially emergent from LLM non-determinism, which the map
(interoperability-oriented) does not fully capture.

---

## GenericConcepts Mobilized (8)

| GenericConcept | Formula | Role in the system |
|----------------|---------|-------------------|
| **Processor**    | `S⊗I⊗D⊗F⊗V` | The app as a whole: transforms user request through a defined structure and flow into a verified output. |
| **Pipeline**     | `S⊗F⊗I` | The generation flow: sequential, unidirectional, clearly bounded stages. |
| **Interface**    | `S⊗I` | PySide6 UI: structural boundary mediating between human intent and LLM engine. |
| **FeedbackLoop** | `A⊗S⊗F⊗I⊗D` | RAG augmentation: TSCG knowledge base feeds back into new generation — TSCG bootstraps itself. |
| **Adapter**      | `S⊗I` | Multi-backend abstraction: normalizes Anthropic/Gemini/Ollama/OpenAI-compat into a uniform call interface. |
| **Context**      | `I⊗S⊗A` | Active context window: Smart Prompt + RAG chunks + user request as the attractor-setting information envelope. |
| **Narration**    | `I⊗D⊗S⊗F⊗A⊗E⊗O⊗R` | Transforms informal description into formal ontological narrative, preserving system identity across representation. |
| **Propagation**  | `F⊗I⊗D` | User request propagates: editor → RAG → LLM → parser → 3 output tabs, transformed at each stage. |

---

## Synergy Principle

```
SmartPrompt ⊗ RAGContext ⊗ LLMEngine → PocletDeliverableSet
```

**Emergent property:** *Ontological translation* — natural language system descriptions
are faithfully converted into rigorous TSCG-compliant formal representations including
scored ASFID/REVOI vectors, epistemic gap δ, mobilized GenericConcepts with tensor
formulas, and runnable Pygame simulations.

---

## LLM Backends

| Backend | Protocol | Notes |
|---------|----------|-------|
| **Anthropic Claude API** | `anthropic` SDK | claude-opus-4-5, sonnet, haiku |
| **Google Gemini** | `google-generativeai` SDK | Free tier via aistudio.google.com |
| **Ollama** | REST `/api/chat` | Local, no API key, any GGUF model |
| **OpenAI-compatible** | `openai` SDK | LM Studio, Jan, vLLM, any compat endpoint |

---

## Reflexivity Analysis (Dogfooding)

The TSCG Poclet Generator exhibits **complete framework reflexivity**:

1. The tool uses TSCG grammar (Smart Prompt v15.9.0) to **generate** TSCG artifacts
2. The tool is itself **described by** a TSCG ontology (`M0_TscgPocletGenerator.jsonld`)
3. That ontology was itself **generated using** TSCG concepts and the TSCG analysis methodology

This constitutes a fixed point in the TSCG representational system:

```
TSCG(TscgPocletGenerator) → PocletDeliverableSet
                          ∧
TSCG(TscgPocletGenerator) ∈ TscgOntology
```

The system is simultaneously **operator** (it generates ontologies) and **object** (it is
described by an ontology). This is the strongest validation of the framework's
universality: if TSCG can rigorously describe its own generation tool, it can describe
any system.

---

## Installation & Usage

```bash
# Dependencies
pip install PySide6 anthropic google-generativeai openai requests
pip install chromadb sentence-transformers   # optional, for RAG

# Run
python tscg_poclet_generator.py
```

**Workflow:**
1. Load Smart Prompt (`📂` button) — e.g. `TSCG_Smart_Prompt_v15_9_0.md`
2. *(Optional)* Click **⚡ Initialize RAG** then **🔍 Augment with RAG**
3. Type your poclet request in the input area
4. Select README template and sim.py UI layout
5. Click **⚡ Generate Poclet**
6. Review the 3 output tabs, then **💾 Save All Files…**

---

## Repository Location

```
instances/tscg-tools/poclet_generator/
├── M0_TscgPocletGenerator.jsonld    ← this file
├── M0_TscgPocletGenerator_README.md ← this README
├── tscg_poclet_generator.py         ← PySide6 application
└── tscg_rag_augmentor.py            ← RAG module
```

---

## References

- TSCG Framework v15.9.0 — <https://github.com/Echopraxium/tscg>
- Korzybski, A. (1933). *Science and Sanity*. Institute of General Semantics.
- TSCG Smart Prompt v15.9.0 — `docs/reboot-kit/TSCG_Smart_Prompt_v15_9_0.md`
- ChromaDB — <https://www.trychroma.com>
- PySide6 — <https://doc.qt.io/qtforpython>
