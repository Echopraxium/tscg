'use strict';

/**
 * RagBuilder — On-the-fly RAG from the local TSCG repository.
 *
 * Aligned with the Python create_tscg_rag.py script:
 *   - Scans the ENTIRE repo (not just 4 hardcoded paths)
 *   - Indexes: .jsonld, .md, .txt, .js, .py, .cs, .fs, .html
 *   - Excludes: .ttl, .tar, .gz, .zip, node_modules, .git, _archives, __pycache__, _protos
 *   - JSON-LD: natural-language conversion per @graph entry (matching _entry_to_text)
 *   - Markdown: section-based chunking by # headers with breadcrumb
 *   - Plain text: paragraph chunking with overlap
 *   - Exact deduplication via MD5 (whitespace-normalised)
 *
 * Expected chunk count: ~6 000–9 000 (vs 641 with the previous narrow scan)
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

const fs   = require('fs');
const path = require('path');
const { TfIdfRetriever } = require('./TfIdfRetriever');

// ── Configuration (mirrors Python constants) ──────────────────────────────────

const INDEXED_EXTENSIONS = new Set(['jsonld', 'md', 'txt', 'js', 'py', 'cs', 'fs', 'html']);

const EXCLUDED_EXTENSIONS = new Set(['ttl', 'tar', 'gz', 'zip', 'bz2', 'xz', '7z']);

const IGNORED_PATH_FRAGMENTS = [
  'node_modules', '.git', '__pycache__', 'bin', 'obj',
  'db_tscg_rag', '_archives', '_protos',
];

// Files with low semantic value — mirrored from Python LOW_VALUE_FILENAMES
const LOW_VALUE_FILENAMES = new Set([
  'files.txt', 'macros.txt', 'TSCG_File_Tree.md',
  'encoding_correspondances.json', 'requirements.txt',
  'check_encoding_issues.py', 'create_files_URIS.py',
  'package.json', 'package-lock.json',
]);

// JSON-LD fields to skip (metadata-only, no RAG value)
const SKIP_JSONLD_FIELDS = new Set([
  'm2:changelog', 'dcterms:creator', 'dcterms:modified', 'dcterms:created',
  'owl:versionInfo', 'schema:version', 'dcterms:rights', 'dcterms:license',
]);

// OWL infrastructure types — no standalone RAG value
const SKIP_TYPES = new Set([
  'owl:ObjectProperty', 'owl:DatatypeProperty', 'owl:AnnotationProperty',
  'owl:TransitiveProperty', 'owl:SymmetricProperty', 'owl:FunctionalProperty',
  'owl:Ontology', 'skos:ConceptScheme', 'rdf:Property',
]);

const CHUNK_SIZE     = 1500;
const CHUNK_OVERLAP  = 200;
const MIN_CHUNK_SIZE = 100;

// ── RagBuilder class ──────────────────────────────────────────────────────────

class RagBuilder {
  /**
   * @param {string} tscgRepoRoot  Absolute path to the TSCG repo root
   *   e.g. "E:\\_00_Michel\\_00_Lab\\_00_GitHub\\tscg"
   */
  constructor(tscgRepoRoot) {
    if (!tscgRepoRoot) throw new Error('RagBuilder: tscgRepoRoot is required');
    this._root      = tscgRepoRoot;
    this._retriever = new TfIdfRetriever();
    this._built     = false;
    this._stats     = { files: 0, chunks: 0, dupes: 0, errors: 0 };
  }

  /**
   * Scan the entire repo, build the TF-IDF index.
   * @param {function} [onProgress]  Optional (message: string) callback
   * @returns {Promise<object>}      Build stats
   */
  async build(onProgress = null) {
    const log = msg => { if (onProgress) onProgress(msg); };

    log('RAG: collecting files from repo…');
    const files = this._collectFiles();
	
	log(`RAG: ${files.length} files found — segmenting…`);
	// throw new Error('🔥 TEST: New code IS loaded!');

    const allChunks  = [];
    const seenHashes = new Set();
    let dupes = 0;

    for (const filePath of files) {
      try {
        const segments = this._segmentFile(filePath);
        for (const seg of segments) {
          const h = this._hash(seg.text);
          if (seenHashes.has(h)) { dupes++; continue; }
          seenHashes.add(h);
          allChunks.push(seg);
        }
        this._stats.files++;
      } catch (err) {
        this._stats.errors++;
        const relPath = filePath.replace(this._root, '').replace(/\\/g, '/');
        log(`RAG ⚠ error: ${relPath} — ${err.message}`);
      }
    }

    this._stats.dupes  = dupes;
    this._stats.chunks = allChunks.length;

    log(`RAG: building TF-IDF index from ${allChunks.length} unique chunks…`);
    this._retriever.addDocuments(allChunks);
    this._built = true;

    log(`RAG ready — ${this._stats.files} files · ${allChunks.length} chunks · ${dupes} dupes · ${this._stats.errors} errors`);
    return { ...this._stats };
  }

  /**
   * Retrieve the top-k most relevant chunks for a query.
   * Returns formatted context text ready to inject into a system prompt.
   *
   * @param {string} query
   * @param {number} [topK=6]
   * @returns {string}
   */
  retrieve(query, topK = 6) {
    if (!this._built) return '';
    const results = this._retriever.search(query, topK);
    if (results.length === 0) return '';

    const lines = ['### TSCG Knowledge Context (RAG)\n'];
    for (const r of results) {
      lines.push(`**[${r.metadata.source ?? r.id}]** (score: ${r.score.toFixed(3)})`);
      lines.push(r.text.trim());
      lines.push('');
    }
    return lines.join('\n');
  }

  get isBuilt()  { return this._built; }
  get stats()    { return { ...this._stats }; }
  get docCount() { return this._retriever.size; }

  // ── File collection ───────────────────────────────────────────────────────

  //_collectFiles() {
  //  const result = [];
  //  this._walkDir(this._root, result);
  //  return result;
  //}
  
  _collectFiles() {
  const result = [];
	  console.log('[DEBUG] Starting scan from:', this._root);
	  
	  // List root directories
	  const rootDirs = fs.readdirSync(this._root, { withFileTypes: true })
	    .filter(d => d.isDirectory())
	    .map(d => d.name);
	  console.log('[DEBUG] Root directories:', rootDirs);
	  
	  this._walkDir(this._root, result, 0);  // ← Pass initial depth = 0
	  console.log('[DEBUG] Total files collected:', result.length);
	  
	  // Comptage par extension
	  const byExt = {};
	  result.forEach(f => {
		const ext = f.split('.').pop()?.toLowerCase() ?? 'none';
		byExt[ext] = (byExt[ext] || 0) + 1;
	  });
	  console.log('[DEBUG] Files by extension:', byExt);
	  
	  return result;
  }

  _walkDir(dir, result, depth = 0) {
	let entries;
	try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
	catch { return; }

	// Warn about deep directories
	if (depth > 5) {
	  console.log(`[WARN] Deep directory (depth ${depth}): ${path.relative(this._root, dir)}`);
	}

	for (const entry of entries) {
		const full = path.join(dir, entry.name);
		const rel  = path.relative(this._root, full).replace(/\\/g, '/');

		// ← AJOUTE CE BLOC DE DEBUG
		if (entry.isFile() && rel.endsWith('.js')) {
		  const skipped = IGNORED_PATH_FRAGMENTS.some(f => rel.includes(f));
		  if (skipped) {
			const match = IGNORED_PATH_FRAGMENTS.find(f => rel.includes(f));
			console.log(`[SKIP JS] ${rel} (matched: ${match})`);
		  }
		}

		// Debug pour node_modules
		if (rel.includes('node_modules')) {
		  console.log(`[SKIP node_modules] ${rel.substring(0, 100)}`);
		}

		// Skip ignored path fragments
		if (IGNORED_PATH_FRAGMENTS.some(f => rel.includes(f))) continue;

		if (entry.isDirectory()) {
		  this._walkDir(full, result, depth + 1);  // ← Pass depth+1
		} 
		else if (entry.isFile()) {
		  const ext  = entry.name.split('.').pop()?.toLowerCase() ?? '';
		  if (EXCLUDED_EXTENSIONS.has(ext))        continue;
		  if (!INDEXED_EXTENSIONS.has(ext))        continue;
		  if (LOW_VALUE_FILENAMES.has(entry.name)) continue;
		  result.push(full);
		}
	} // for	
  } // _walkDir()

  // ── Segmentation dispatcher ───────────────────────────────────────────────

  _segmentFile(filePath) {
    const ext = filePath.split('.').pop()?.toLowerCase() ?? '';
    const raw = fs.readFileSync(filePath, 'utf-8');

    if (ext === 'jsonld') return this._segmentJsonLd(raw, filePath);
    if (ext === 'md')     return this._segmentMarkdown(raw, filePath);
    return this._segmentPlain(raw, filePath);
  }

  // ── JSON-LD segmentation (mirrors Python _entry_to_text) ─────────────────

  _segmentJsonLd(text, filePath) {
    const fileName = path.basename(filePath);
    const stem     = fileName.toUpperCase();
    let layer = 'M0';
    if      (stem.startsWith('M3_')) layer = 'M3';
    else if (stem.startsWith('M2_')) layer = 'M2';
    else if (stem.startsWith('M1_')) layer = 'M1';

    let data;
    try { data = JSON.parse(text); }
    catch { return this._segmentPlain(text, filePath); }

    const segments = [];
    const graph = data['@graph'] ?? (Array.isArray(data) ? data : null);

    if (graph) {
      for (let i = 0; i < graph.length; i++) {
        const entry = graph[i];
        if (!entry || typeof entry !== 'object') continue;

        // label hoisted here so the nested loop can reference it safely
        const label = this._str(entry['rdfs:label'] ?? entry['@id'] ?? `entry_${i}`);

        const nl = this._entryToText(entry, layer);
        if (nl) {
          segments.push({
            id:   `${fileName}::${label}`,
            text: nl,
            metadata: { source: fileName, layer, label, type: 'jsonld_entry', filePath },
          });
        }

        // Recurse into nested lists (e.g. dimensions in M3_EagleEye)
        const parentLabel = label;
        for (const [key, val] of Object.entries(entry)) {
          if (key.startsWith('@') || SKIP_JSONLD_FIELDS.has(key)) continue;
          if (!Array.isArray(val)) continue;
          for (let j = 0; j < val.length; j++) {
            const nested = val[j];
            if (!nested || typeof nested !== 'object') continue;
            if (!('@id' in nested) && !('rdfs:label' in nested)) continue;
            let nestedNl = this._entryToText(nested, layer);
            if (!nestedNl) continue;
            if (parentLabel) nestedNl = `Context: ${parentLabel}\n${nestedNl}`;
            const nestedLabel = this._str(nested['rdfs:label'] ?? `nested_${i}_${j}`);
            segments.push({
              id:   `${fileName}::${label}::${key}::${j}`,
              text: nestedNl,
              metadata: { source: fileName, layer, label: nestedLabel, type: 'jsonld_nested', filePath },
            });
          }
        }
      }
    } else {
      // Single object
      const nl = this._entryToText(data, layer) ?? JSON.stringify(data).slice(0, 500);
      if (nl.length >= MIN_CHUNK_SIZE) {
        segments.push({
          id:   `${fileName}::full`,
          text: nl,
          metadata: { source: fileName, layer, type: 'jsonld_document', filePath },
        });
      }
    }

    return segments;
  }

  /**
   * Convert a JSON-LD @graph entry to natural language.
   * Mirrors Python _entry_to_text().
   */
  _entryToText(entry, layer) {
    const rawType = entry['@type'] ?? '';
    const types   = new Set(Array.isArray(rawType) ? rawType : [rawType]);
    if ([...types].some(t => SKIP_TYPES.has(t))) return null;

    const meaningfulKeys = Object.keys(entry).filter(
      k => !k.startsWith('@') && !SKIP_JSONLD_FIELDS.has(k)
    );
    if (meaningfulKeys.length === 0) return null;

    const label = this._str(entry['rdfs:label'] ?? '');
    if (!label) return null;

    const parts = [];

    // Header with layer / family / perspective
    const subclass = entry['rdfs:subClassOf'] ?? '';
    const families = [];
    const subArr   = Array.isArray(subclass) ? subclass : [subclass];
    for (const s of subArr) {
      if (typeof s === 'string' && s && !['m2:MetaConcept','m2:MetaconceptPair','m2:MetaconceptCombo'].includes(s)) {
        families.push(s.split(':').pop());
      }
    }
    const perspective = this._str(entry['m2:perspective'] ?? '');
    let header = `${label} [${layer}`;
    if (families.length) header += ` / ${families[0]}`;
    if (perspective)     header += ` / ${perspective}`;
    header += ']';
    parts.push(header);

    // Tensor formula
    const formula = this._str(
      entry['m2:hasTensorFormula'] ?? entry['m3:tensorFormula'] ?? entry['tscg:tensorFormula'] ?? ''
    );
    if (formula) {
      const dominant = entry['m2:hasDominantM3'] ?? [];
      const dims = (Array.isArray(dominant) ? dominant : [dominant])
        .filter(d => typeof d === 'string')
        .map(d => d.split(':').pop());
      parts.push(dims.length
        ? `Tensor formula: ${formula} (${dims.join(', ')})`
        : `Tensor formula: ${formula}`
      );
    }

    // Definition
    const comment = this._str(entry['rdfs:comment'] ?? entry['dcterms:description'] ?? '');
    if (comment) parts.push(`Definition: ${comment}`);

    // Polarity / epistemic gap
    const polarity = this._str(entry['m2:hasPolarity'] ?? '');
    const gap      = entry['m2:hasEpistemicGap'];
    const meta     = [];
    if (polarity) meta.push(`Polarity: ${polarity}`);
    if (gap != null) meta.push(`Epistemic gap: ${typeof gap === 'number' ? gap.toFixed(2) : gap}`);
    if (meta.length) parts.push(meta.join(' | '));

    // Examples
    const examples = entry['m2:hasExample'] ?? entry['m3:dimensionExamples'] ?? [];
    const exArr = Array.isArray(examples) ? examples : [examples];
    if (exArr.length) parts.push(`Examples: ${exArr.slice(0, 4).map(String).join('; ')}`);

    // M3 symbol
    const symbol = this._str(entry['m3:dimensionSymbol'] ?? '');
    if (symbol) parts.push(`Symbol: ${symbol}`);

    // ASFID / REVOI scores (M0 poclets)
    const asfid = entry['m0:asfidScore'];
    const revoi = entry['m0:revoiScore'];
    if (asfid) parts.push(`ASFID: A=${asfid.A} S=${asfid.S} F=${asfid.F} I=${asfid.I} D=${asfid.D}`);
    if (revoi) parts.push(`REVOI: R=${revoi.R} E=${revoi.E} V=${revoi.V} O=${revoi.O} I=${revoi.I}`);

    if (parts.length < 2) return null;
    return parts.join('\n');
  }

  // ── Markdown segmentation (mirrors Python _segment_markdown) ──────────────

  _segmentMarkdown(text, filePath) {
    const fileName = path.basename(filePath);
    const segments = [];
    const lines    = text.split('\n');
    const headerRe = /^(#{1,6})\s+(.+)$/;

    let currentLines  = [];
    let currentHeader = null;
    let headerStack   = {};   // level → header text

    const breadcrumb = () => Object.keys(headerStack)
      .sort((a, b) => a - b)
      .map(k => headerStack[k])
      .join(' > ');

    const flush = () => {
      if (!currentLines.length) return;
      const sectionText = currentLines.join('\n').trim();
      if (sectionText.length < MIN_CHUNK_SIZE) return;

      const crumb = breadcrumb();
      const full  = (crumb && crumb !== (currentHeader ?? ''))
        ? `[${crumb}]\n${sectionText}`
        : sectionText;

      // Large sections → sliding window chunks
      const chunks = this._chunkText(full);
      for (let i = 0; i < chunks.length; i++) {
        segments.push({
          id:   `${fileName}::${currentHeader ?? 'intro'}::${segments.length}`,
          text: chunks[i],
          metadata: {
            source:    fileName,
            type:      'markdown_section',
            header:    currentHeader ?? 'intro',
            breadcrumb: crumb,
            filePath,
          },
        });
      }
    };

    for (const line of lines) {
      const m = headerRe.exec(line);
      if (m) {
        flush();
        const level = m[1].length;
        currentHeader = m[2].trim();
        // Drop same-level and deeper headers from stack
        for (const k of Object.keys(headerStack)) {
          if (Number(k) >= level) delete headerStack[k];
        }
        headerStack[level] = currentHeader;
        currentLines = [line];
      } else {
        currentLines.push(line);
      }
    }
    flush();

    return segments.length ? segments : this._segmentPlain(text, filePath);
  }

  // ── Plain text segmentation (paragraph-based with overlap) ───────────────

  _segmentPlain(text, filePath) {
    const fileName  = path.basename(filePath);
    const segments  = [];
    const paragraphs = text.split(/\n\n+/).map(p => p.trim()).filter(Boolean);
    let   current = [];
    let   length  = 0;

    const flush = () => {
      if (!current.length) return;
      const t = current.join('\n\n');
      if (t.length < MIN_CHUNK_SIZE) return;
      segments.push({
        id:   `${fileName}::chunk_${segments.length}`,
        text: t,
        metadata: { source: fileName, type: 'text_chunk', filePath },
      });
    };

    for (const para of paragraphs) {
      if (length + para.length > CHUNK_SIZE && current.length) {
        flush();
        // Overlap: keep last paragraph
        current = current.length > 0 ? [current[current.length - 1], para] : [para];
        length  = current.reduce((a, s) => a + s.length, 0);
      } else {
        current.push(para);
        length += para.length;
      }
    }
    flush();

    return segments;
  }

  // ── Text chunker for long markdown sections ───────────────────────────────

  _chunkText(text) {
    if (text.length <= CHUNK_SIZE) return [text];

    const chunks = [];
    let start = 0;
    while (start < text.length) {
      const end = Math.min(start + CHUNK_SIZE, text.length);
      chunks.push(text.slice(start, end));
      start += CHUNK_SIZE - CHUNK_OVERLAP;
      if (start >= text.length) break;
    }
    return chunks;
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  _str(v) {
    if (!v) return '';
    if (typeof v === 'string') return v;
    if (typeof v === 'object' && v !== null) return v['@value'] ?? v['rdfs:label'] ?? '';
    return String(v);
  }

  /**
   * Whitespace-normalised hash for exact dedup (mirrors Python _normalize_text + MD5).
   * Uses a simple djb2 hash (no crypto dependency needed for dedup in JS).
   */
  _hash(text) {
    const norm = text.replace(/\s+/g, ' ').trim().toLowerCase();
    let h = 5381;
    for (let i = 0; i < norm.length; i++) {
      h = ((h << 5) + h) ^ norm.charCodeAt(i);
      h = h >>> 0; // keep unsigned 32-bit
    }
    return h.toString(16);
  }
}

module.exports = { RagBuilder };
