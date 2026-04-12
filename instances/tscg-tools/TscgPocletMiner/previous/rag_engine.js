// rag_engine.js — TscgPocletMiner JS-Native RAG Engine
// Author: Echopraxium with the collaboration of Claude AI
// v1.2.0
//
// Runs entirely in Electron main process (Node.js).
// Uses @xenova/transformers v2 (sentence-transformers/all-MiniLM-L6-v2, ~23 MB WASM).
// No Python, no server, no LLM — pure deterministic semantic search.
//
// Corpus:
//   - POCLET corpus  : poclet_corpus_profile.json  → find similar existing poclets
//   - M2 corpus      : m2_concepts_corpus.json     → suggest GenericConcepts
//
// ChromaDB RAG archive (restore_rag.js):
//   Located at RAG_ARCHIVE_PATH below.
//   Auto-extracted to RAG_EXTRACT_DIR on first init if not already present.

'use strict';

const path = require('path');
const fs   = require('fs');

// ─── RAG archive path ─────────────────────────────────────────────────────────
//
// The compressed ChromaDB RAG lives at:
//   <repo_root>/src/tscg/rag/db_tscg_rag.tar.gz
//
// TscgPocletMiner lives at:
//   <repo_root>/instances/tscg-tools/TscgPocletMiner/
//
// So from __dirname we go up 3 levels to reach the repo root.

const REPO_ROOT      = path.resolve(__dirname, '..', '..', '..');
const RAG_ARCHIVE_PATH = path.join(REPO_ROOT, 'src', 'tscg', 'rag', 'db_tscg_rag.tar.gz');
const RAG_EXTRACT_DIR  = path.join(REPO_ROOT, 'src', 'tscg', 'rag', 'db_extracted');

// ─── @xenova/transformers pipeline ───────────────────────────────────────────

let _pipeline = null;

async function getPipeline() {
  if (_pipeline) return _pipeline;
  const { pipeline, env } = await import('@xenova/transformers');
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
  return Array.from(out.data);
}

// ─── Auto-restore ChromaDB archive ───────────────────────────────────────────
//
// Called by init() before embedding.
// If RAG_EXTRACT_DIR/chroma.sqlite3 already exists → skip.
// Otherwise decompresses RAG_ARCHIVE_PATH → RAG_EXTRACT_DIR via restore_rag.js.

async function ensureRagExtracted(onProgress) {
  const sqlitePath = path.join(RAG_EXTRACT_DIR, 'chroma.sqlite3');

  if (fs.existsSync(sqlitePath)) {
    onProgress && onProgress({ step: 'rag_db', msg: 'ChromaDB already extracted', pct: 5 });
    return RAG_EXTRACT_DIR;
  }

  if (!fs.existsSync(RAG_ARCHIVE_PATH)) {
    onProgress && onProgress({
      step: 'rag_db_missing',
      msg: `RAG archive not found: ${RAG_ARCHIVE_PATH}`,
      pct: 5
    });
    console.warn(`[rag_engine] RAG archive not found: ${RAG_ARCHIVE_PATH}`);
    return null;
  }

  onProgress && onProgress({ step: 'rag_db', msg: 'Extracting ChromaDB archive…', pct: 3 });
  try {
    const { restoreRagDb } = require('./restore_rag');
    const result = await restoreRagDb(
      RAG_ARCHIVE_PATH,
      RAG_EXTRACT_DIR,
      msg => console.log('[rag_engine] restore:', msg)
    );
    onProgress && onProgress({ step: 'rag_db', msg: 'ChromaDB extracted', pct: 5 });
    return result.dbDir;
  } catch (err) {
    console.error('[rag_engine] RAG extraction failed:', err.message);
    onProgress && onProgress({ step: 'rag_db_error', msg: `Extraction failed: ${err.message}`, pct: 5 });
    return null;
  }
}

// ─── TscgRagEngine ────────────────────────────────────────────────────────────

class TscgRagEngine {
  constructor() {
    this._ready       = false;
    this._poclets     = [];
    this._m2          = [];
    this._pipe        = null;
    this._initPromise = null;
  }

  // ── Init ─────────────────────────────────────────────────────────────────────
  async init(onProgress) {
    if (this._ready) return;
    if (this._initPromise) return this._initPromise;

    this._initPromise = (async () => {

      // 0 — Ensure ChromaDB archive is extracted (non-blocking if missing)
      await ensureRagExtracted(onProgress);

      // 1 — Load embedding model
      onProgress && onProgress({ step: 'model', msg: 'Loading all-MiniLM-L6-v2…', pct: 10 });
      this._pipe = await getPipeline();

      // 2 — Load poclet corpus (new format: corpus.poclets[])
      onProgress && onProgress({ step: 'corpus_poclets', msg: 'Embedding poclet corpus…', pct: 25 });
      const corpusPath = path.join(__dirname, 'poclet_corpus_profile.json');
      const corpus     = JSON.parse(fs.readFileSync(corpusPath, 'utf-8'));

      const pocletList = Array.isArray(corpus.poclets) ? corpus.poclets : [];
      for (const p of pocletList) {
        const text = p.description || [
          `Poclet: ${p.label}`,
          `Domain: ${p.domain}`,
          p.subdomains?.length        ? `Subdomains: ${p.subdomains.join(', ')}` : '',
          p.primaryMetaconcept        ? `Primary concept: ${p.primaryMetaconcept}` : '',
          p.validatesMetaconcepts?.length
            ? `Validates: ${p.validatesMetaconcepts.join(', ')}` : ''
        ].filter(Boolean).join('. ');

        const vec = await embed(this._pipe, text);
        this._poclets.push({
          id:  p.id,
          vec,
          meta: {
            name:               p.label,
            domain:             p.domain,
            type:               p.ontologyType || 'Poclet',
            asfidMean:          p.asfidScores?.mean  ?? null,
            revoiMean:          p.revoiScores?.mean  ?? null,
            epistemicGap:       p.epistemicGap       ?? null,
            primaryMetaconcept: p.primaryMetaconcept || ''
          }
        });
      }

      // Also embed gap_analysis candidates so they show up in similarity search
      const candidates = corpus.gap_analysis?.priority_candidates || [];
      for (const c of candidates) {
        const text = `Candidate poclet: ${c.system} | Domain: ${c.domain} | Type: ${c.type} | Priority candidate`;
        const vec  = await embed(this._pipe, text);
        this._poclets.push({
          id:  c.system,
          vec,
          meta: { name: c.system, domain: c.domain, type: c.type, isCandidate: true }
        });
      }

      // 3 — Load M2 corpus (new format: { _meta, concepts: [] })
      onProgress && onProgress({ step: 'corpus_m2', msg: 'Embedding M2 GenericConcepts…', pct: 60 });
      const m2Path = path.join(__dirname, 'm2_concepts_corpus.json');
      const m2Raw  = JSON.parse(fs.readFileSync(m2Path, 'utf-8'));

      // Support both flat array (old) and { concepts: [] } (new rebuild_m2_corpus.py)
      const m2List = Array.isArray(m2Raw) ? m2Raw : (m2Raw.concepts || []);

      for (const entry of m2List) {
        const vec = await embed(this._pipe, entry.text);
        this._m2.push({
          id:  entry.id,
          vec,
          meta: {
            id:      entry.id,
            label:   entry.label,
            formula: entry.formula || '',
            family:  entry.family  || ''
          }
        });
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

  // ── Corpus dirty flag (called after rebuild-corpus) ───────────────────────
  markCorpusDirty() {
    this._ready       = false;
    this._poclets     = [];
    this._m2          = [];
    this._pipe        = null;
    this._initPromise = null;
    console.log('[rag_engine] Corpus marked dirty — will re-embed on next rag-init');
  }

  // ── Expose archive/extract paths for UI display ───────────────────────────
  getArchiveInfo() {
    return {
      archivePath:  RAG_ARCHIVE_PATH,
      extractDir:   RAG_EXTRACT_DIR,
      archiveExists: fs.existsSync(RAG_ARCHIVE_PATH),
      extracted:     fs.existsSync(path.join(RAG_EXTRACT_DIR, 'chroma.sqlite3'))
    };
  }
}

// Singleton
const ragEngine = new TscgRagEngine();
module.exports = { ragEngine, RAG_ARCHIVE_PATH, RAG_EXTRACT_DIR };
