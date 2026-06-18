# TscgPocletMiner — LLM + RAG Architecture

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 1.0.0

---

## Overview

TscgPocletMiner is an ElectronJS application that guides the user through
the **5-round TSCG poclet analysis pipeline** using an AI language model backend.

The key design goal: **no Claude Pro subscription required**. Users can choose
from multiple LLM backends, including free local options.

---

## LLM Backends

| Backend | Type | Cost | Quality | Setup |
|---------|------|------|---------|-------|
| **Ollama (Phi-3.5 Mini)** | Local | Free | ⭐⭐⭐ | Install Ollama |
| **DeepSeek API** | Cloud | Pay-per-use (~$0.01/session) | ⭐⭐⭐⭐⭐ | API key |
| **Claude API (Anthropic)** | Cloud | Pay-per-use | ⭐⭐⭐⭐⭐ | API key |

### Recommended for Michel's hardware (4 GB VRAM / 16 GB RAM)

For the **local backend**, use Phi-3.5 Mini (fits entirely in 4 GB VRAM):

```bash
ollama pull phi3.5:3.8b-mini-instruct-q4_K_M
```

Alternative if Phi-3.5 Mini is unavailable:
```bash
ollama pull smollm2:1.7b-instruct-q4_K_M   # lighter, faster
```

---

## On-the-fly RAG

The RAG (Retrieval-Augmented Generation) index is built **at runtime** from
the user's local TSCG repository. No pre-built ChromaDB corpus is shipped.

### What is indexed

1. `ontology/M2_GenericConcepts.jsonld` — 75 atomic GenericConcepts (priority: high)
2. `ontology/M1_CoreConcepts.jsonld` — Combos and KnowledgeFieldConceptCombos (priority: high)
3. `ontology/M1_extensions/**` — Domain extensions (priority: medium)
4. `instances/poclets/**` — Validated M0 poclets (priority: medium)

### Implementation

- **Algorithm:** TF-IDF with cosine similarity (pure JS, zero npm dependencies)
- **Storage:** In-memory only (rebuilt on each app launch)
- **Indexing time:** ~1-2 seconds for the full TSCG corpus

TF-IDF is sufficient because the TSCG corpus is small (~75 M2 concepts + ~23 poclets).
For a larger corpus, replace `TfIdfRetriever` with `@xenova/transformers` embeddings.

---

## File Structure

```
TscgPocletMiner/
├── main.js              ← Electron main process (IPC handlers)
├── preload.js           ← contextBridge (Node ↔ Renderer bridge)
├── package.json
├── renderer/
│   └── index.html       ← UI (to be implemented)
└── src/
    ├── llm/
    │   ├── LLMProvider.js       ← Abstract base class
    │   ├── OllamaProvider.js    ← Local (Ollama, OpenAI-compatible)
    │   ├── DeepSeekProvider.js  ← Cloud (DeepSeek API)
    │   ├── AnthropicProvider.js ← Cloud (Claude API)
    │   └── ProviderFactory.js   ← Factory + config management
    ├── rag/
    │   ├── RagBuilder.js        ← On-the-fly RAG from JSON-LD files
    │   └── TfIdfRetriever.js    ← In-memory TF-IDF (zero deps)
    └── tscg/
        ├── SystemPrompts.js     ← TSCG-specific prompts (5 rounds)
        └── PocletPipeline.js    ← 5-round wizard orchestrator
```

---

## The 5-Round Pipeline

| Round | Task | LLM Output |
|-------|------|-----------|
| 1 | System identification | systemName, domain, poles, attractor |
| 2 | ASFID scoring (Eagle Eye) | 5 scores + rationales |
| 3 | REVOI scoring (Sphinx Eye) | 5 scores + δ + SpectralClass |
| 4 | GenericConcept selection | M2 concepts + KnowledgeFieldCombos |
| 5 | M0 JSON-LD generation | Complete poclet file |

---

## Quick Start

```bash
cd TscgPocletMiner
npm install
npm start
```

1. In the Settings panel, select your LLM backend and configure it
2. Set your local TSCG repository root path
3. Click "Build RAG Index" (takes ~2 seconds)
4. Start a new poclet session and describe your system
5. Step through the 5 rounds
6. Save the generated M0 JSON-LD file

---

## Config File

Stored in Electron `userData` as `tscg_miner_config.json`:

```json
{
  "active": "ollama",
  "tscgRepoRoot": "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg",
  "providers": {
    "ollama":    { "model": "phi3.5:3.8b-mini-instruct-q4_K_M" },
    "deepseek":  { "apiKey": "sk-..." },
    "anthropic": { "apiKey": "sk-ant-...", "model": "claude-haiku-4-5-20251001" }
  }
}
```

---

## Adding a New Backend

1. Create `src/llm/MyProvider.js` extending `LLMProvider`
2. Implement `complete()`, `isAvailable()`, `getId()`, `getName()`
3. Register it in `ProviderFactory.js` (add to `REGISTRY` and `PROVIDER_META`)

That's it — no other changes needed.
