'use strict';

/**
 * TfIdfRetriever — In-memory TF-IDF similarity search.
 *
 * Zero npm dependencies. Sufficient for the TSCG corpus size
 * (~75 M2 GenericConcepts + ~23 poclets + M1 extensions).
 *
 * Usage:
 *   const retriever = new TfIdfRetriever();
 *   retriever.addDocuments(chunks);          // [{ id, text, metadata }]
 *   const results = retriever.search(query, topK=5);
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */
class TfIdfRetriever {
  constructor() {
    this._docs    = [];   // { id, text, metadata, terms }
    this._idf     = {};   // term → idf score
    this._built   = false;
  }

  /** Add an array of document chunks and build the index. */
  addDocuments(chunks) {
    for (const chunk of chunks) {
      this._docs.push({
        id:       chunk.id,
        text:     chunk.text,
        metadata: chunk.metadata ?? {},
        terms:    this._tokenize(chunk.text),
      });
    }
    this._buildIdf();
    this._built = true;
  }

  /** Return top-k most relevant chunks for the query. */
  search(query, topK = 5) {
    if (!this._built || this._docs.length === 0) return [];

    const queryTerms = this._tokenize(query);
    const queryVec   = this._tfidfVector(queryTerms);

    const scored = this._docs.map(doc => ({
      ...doc,
      score: this._cosine(queryVec, this._tfidfVector(doc.terms)),
    }));

    return scored
      .filter(d => d.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);
  }

  get size() { return this._docs.length; }

  // ── private ────────────────────────────────────────────────────────────────

  _tokenize(text) {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9À-ÿ⊗⊕→↔]/g, ' ')
      .split(/\s+/)
      .filter(t => t.length > 1 && !STOP_WORDS.has(t));
  }

  _buildIdf() {
    const N    = this._docs.length;
    const df   = {};
    for (const doc of this._docs) {
      const seen = new Set(doc.terms);
      for (const t of seen) df[t] = (df[t] ?? 0) + 1;
    }
    this._idf = {};
    for (const [term, freq] of Object.entries(df)) {
      this._idf[term] = Math.log((N + 1) / (freq + 1)) + 1; // smoothed
    }
  }

  _tf(term, terms) {
    const count = terms.filter(t => t === term).length;
    return count / (terms.length || 1);
  }

  _tfidfVector(terms) {
    const vec = {};
    const unique = [...new Set(terms)];
    for (const term of unique) {
      const idf = this._idf[term] ?? 0;
      if (idf > 0) vec[term] = this._tf(term, terms) * idf;
    }
    return vec;
  }

  _cosine(a, b) {
    let dot = 0, normA = 0, normB = 0;
    const allKeys = new Set([...Object.keys(a), ...Object.keys(b)]);
    for (const k of allKeys) {
      const va = a[k] ?? 0;
      const vb = b[k] ?? 0;
      dot   += va * vb;
      normA += va * va;
      normB += vb * vb;
    }
    if (normA === 0 || normB === 0) return 0;
    return dot / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}

// Common English/French stop words — tuned for ontology text
const STOP_WORDS = new Set([
  'a','an','the','is','are','was','were','be','been','being',
  'have','has','had','do','does','did','will','would','could','should','may','might',
  'of','in','on','at','to','for','with','by','from','as','or','and','but','not',
  'this','that','these','those','it','its','which','who','what','where','when','how',
  'le','la','les','un','une','des','du','de','et','en','au','aux','par','pour',
  'est','sont','être','avoir','dans','sur','avec','qui','que','dont',
  'can','each','all','any','also','than','then','into','more','such',
]);

module.exports = { TfIdfRetriever };
