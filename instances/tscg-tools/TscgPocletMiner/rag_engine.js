// rag_engine.js — TscgPocletMiner JS-Native RAG Engine
// Author: Echopraxium with the collaboration of Claude AI
//
// Runs entirely in Electron main process (Node.js).
// Uses @xenova/transformers v2 (sentence-transformers/all-MiniLM-L6-v2, ~23 MB WASM).
// No Python, no server, no LLM — pure deterministic semantic search.
//
// Corpus:
//   - POCLET corpus  : poclet_corpus_profile.json  → find similar existing poclets
//   - M2 corpus      : m2_concepts_corpus.json     → suggest GenericConcepts

'use strict';

const path = require('path');
const fs   = require('fs');

// @xenova/transformers v2 is CJS-compatible via dynamic import
let _pipeline = null;

async function getPipeline() {
  if (_pipeline) return _pipeline;
  // Dynamic import needed for ESM package in CJS context
  const { pipeline, env } = await import('@xenova/transformers');
  // Cache model in app data dir to avoid re-download
  env.cacheDir = path.join(require('electron').app.getPath('userData'), 'xenova-cache');
  _pipeline = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
  return _pipeline;
}

// ─── Cosine similarity ────────────────────────────────────────────────────────

function cosine(a, b) {
  let dot = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na  += a[i] * a[i];
    nb  += b[i] * b[i];
  }
  return na === 0 || nb === 0 ? 0 : dot / (Math.sqrt(na) * Math.sqrt(nb));
}

// ─── Embed helper ─────────────────────────────────────────────────────────────

async function embed(pipe, text) {
  const out = await pipe(text, { pooling: 'mean', normalize: true });
  // out.data is a Float32Array of length 384
  return Array.from(out.data);
}

// ─── TscgRagEngine ────────────────────────────────────────────────────────────

class TscgRagEngine {
  constructor() {
    this._ready    = false;
    this._poclets  = [];   // { id, text, meta }
    this._m2       = [];   // { id, text, meta }
    this._pipe     = null;
    this._initPromise = null;
  }

  // Call once at app startup (or lazily on first query)
  async init(onProgress) {
    if (this._ready) return;
    if (this._initPromise) return this._initPromise;

    this._initPromise = (async () => {
      onProgress && onProgress({ step: 'model', msg: 'Loading all-MiniLM-L6-v2…', pct: 0 });
      this._pipe = await getPipeline();

      // ── Load poclet corpus ──────────────────────────────────────────
      onProgress && onProgress({ step: 'corpus_poclets', msg: 'Embedding poclet corpus…', pct: 20 });
      const corpusPath = path.join(__dirname, 'poclet_corpus_profile.json');
      const corpus     = JSON.parse(fs.readFileSync(corpusPath, 'utf-8'));

      for (const [domainKey, names] of Object.entries(corpus.domain_coverage)) {
        for (const name of names) {
          const text = `Poclet: ${name} | Domain: ${domainKey} | Type: Poclet | TSCG validated system`;
          const vec  = await embed(this._pipe, text);
          this._poclets.push({ id: name, vec, meta: { name, domain: domainKey, type: 'Poclet' } });
        }
      }
      // Also add gap_analysis candidates
      for (const c of corpus.gap_analysis.priority_candidates) {
        const text = `Candidate poclet: ${c.system} | Domain: ${c.domain} | Type: ${c.type} | Priority candidate`;
        const vec  = await embed(this._pipe, text);
        this._poclets.push({ id: c.system, vec, meta: { name: c.system, domain: c.domain, type: c.type, isCandidate: true } });
      }

      // ── Load M2 corpus ──────────────────────────────────────────────
      onProgress && onProgress({ step: 'corpus_m2', msg: 'Embedding M2 GenericConcepts…', pct: 55 });
      const m2Path = path.join(__dirname, 'm2_concepts_corpus.json');
      const m2Data = JSON.parse(fs.readFileSync(m2Path, 'utf-8'));

      for (const entry of m2Data) {
        const vec = await embed(this._pipe, entry.text);
        this._m2.push({ id: entry.id, vec, meta: { id: entry.id, label: entry.label, formula: entry.formula } });
      }

      this._ready = true;
      onProgress && onProgress({ step: 'ready', msg: 'RAG ready', pct: 100 });
    })();

    return this._initPromise;
  }

  // ── Query: find similar poclets ───────────────────────────────────────────
  async querySimilarPoclets(queryText, topK = 5) {
    if (!this._ready) throw new Error('RAG not initialized');
    const qVec = await embed(this._pipe, queryText);
    return this._search(this._poclets, qVec, topK);
  }

  // ── Query: suggest M2 GenericConcepts ─────────────────────────────────────
  async suggestGenericConcepts(queryText, topK = 6) {
    if (!this._ready) throw new Error('RAG not initialized');
    const qVec = await embed(this._pipe, queryText);
    return this._search(this._m2, qVec, topK);
  }

  // ── Internal search ───────────────────────────────────────────────────────
  _search(corpus, qVec, topK) {
    const scored = corpus.map(entry => ({
      ...entry.meta,
      score: cosine(qVec, entry.vec)
    }));
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, topK).map(r => ({
      ...r,
      score: Math.round(r.score * 1000) / 1000
    }));
  }
}

// Singleton
const ragEngine = new TscgRagEngine();
module.exports = { ragEngine };
