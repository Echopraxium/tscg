// rebuild_corpus.js — TscgPocletMiner corpus rebuilder
// Author: Echopraxium with the collaboration of Claude AI
// v2.1.0 — Generates all fields required by renderer.js
//
// Called by main.js IPC handler 'rebuild-corpus':
//   const { rebuildCorpus } = require('./rebuild_corpus');
//   const result = rebuildCorpus({ startDir: __dirname });
//   // result: { count, path, hash, poclets }

'use strict';

const fs     = require('fs');
const path   = require('path');
const crypto = require('crypto');

// ─── Configuration ────────────────────────────────────────────────────────────

const POCLETS_SUBPATH = path.join('..', '..', 'instances', 'poclets');
const OUTPUT_FILENAME = 'poclet_corpus_profile.json';

// ─── Static corpus data ───────────────────────────────────────────────────────

// invariants.criteria — shape expected by renderer.js buildInvariantChecklist()
const INVARIANT_CRITERIA = [
  {
    id: 'real_observable', weight: 2,
    question: 'Is this a real, observable system (not a pure abstraction)?',
    examples_ok: ['RAAS', 'Transistor', 'Fire Triangle']
  },
  {
    id: 'asfid_complete', weight: 2,
    question: 'Can you identify at least A + S + F ASFID dimensions?',
    examples_ok: ['ButterflyMetamorphosis', 'BloodPressureControl']
  },
  {
    id: 'domain_delimited', weight: 1,
    question: 'Is the domain clearly delimited (biology, electronics, …)?',
    examples_ok: ['Yggdrasil (mythology)', 'Transistor (electronics)']
  },
  {
    id: 'non_trivial_dynamics', weight: 2,
    question: 'Does the system exhibit non-trivial regulation or dynamics?',
    examples_ok: ['RAAS (cascade)', 'ExposureTriangle (trade-off)']
  },
  {
    id: 'web_documented', weight: 1,
    question: 'Is it well-documented on the web (Wikipedia, papers)?',
    examples_ok: ['Kidneys', 'AdaptiveImmuneResponse']
  },
  {
    id: 'corpus_gap', weight: 2,
    question: 'Does it fill a domain gap in the current corpus?',
    examples_ok: ['SIR model (epidemiology)', 'Peirce triangle (semiotics)']
  },
  {
    id: 'type_discriminated', weight: 1,
    question: 'Can you determine the type: Poclet vs TransDisclet vs SystemicFramework?',
    examples_ok: ['Transistor (Poclet)', 'Oscillator (TransDisclet)']
  },
];

// screening_criteria — legacy flat list (kept for backward compat)
const SCREENING_CRITERIA = INVARIANT_CRITERIA.map(c => ({
  id: c.id, label: c.question, weight: c.weight
}));

const SCORING_THRESHOLDS = {
  verdict: {
    strong_candidate: { invariants_min: 6, asfid_min: 0.75 },
    candidate:        { invariants_min: 4, asfid_min: 0.60 },
    weak_candidate:   { invariants_min: 2, asfid_min: 0.45 },
  }
};

const WEB_SEARCH_TEMPLATES = {
  wikipedia:      'https://en.wikipedia.org/wiki/{SYSTEM}',
  duckduckgo:     'https://duckduckgo.com/?q={SYSTEM}+{DOMAIN}+system+model',
  scholar:        'https://scholar.google.com/scholar?q={SYSTEM}+system+model',
  gemini_suggest: 'https://gemini.google.com/app?q=Suggest+5+minimal+complete+systems+in+{DOMAIN}+suitable+for+TSCG+poclet+modeling',
};

const GAP_ANALYSIS_CANDIDATES = [
  { system: 'SIR Epidemiological Model',    domain: 'Epidemiology',    type: 'Poclet',       priority: 'high'   },
  { system: "Peirce's Semiotic Triangle",   domain: 'Semiotics',       type: 'Poclet',       priority: 'high'   },
  { system: 'Harmonic Oscillator',          domain: 'Physics',         type: 'TransDisclet', priority: 'high'   },
  { system: "Rogers' Innovation Diffusion", domain: 'Social Sciences', type: 'Poclet',       priority: 'medium' },
  { system: 'Neural Network (Perceptron)',   domain: 'Computer Science',type: 'Poclet',       priority: 'medium' },
  { system: 'Krebs Cycle',                  domain: 'Biochemistry',    type: 'Poclet',       priority: 'medium' },
  { system: 'Supply & Demand Equilibrium',  domain: 'Economics',       type: 'Poclet',       priority: 'medium' },
  { system: 'Predator-Prey (Lotka-Volterra)',domain: 'Ecology',        type: 'Poclet',       priority: 'medium' },
];

// ─── Field extractors ────────────────────────────────────────────────────────
//
// Each poclet JSON-LD has a @graph array with at least one entry typed
// owl:NamedIndividual.  We extract from the first such entry.

function extractPocletEntry(graph) {
  // Prefer entry with m0:domain (the system node, not metadata nodes)
  return (
    graph.find(e => e['m0:domain']) ||
    graph.find(e => e['@type'] && JSON.stringify(e['@type']).includes('NamedIndividual')) ||
    graph[0]
  );
}

function safeStr(v)   { return typeof v === 'string' ? v : (Array.isArray(v) ? v[0] : ''); }
function safeArr(v)   { return Array.isArray(v) ? v : (v ? [v] : []); }
function safeNum(v)   { return typeof v === 'number' ? v : null; }

function extractScores(raw) {
  if (!raw || typeof raw !== 'object') return null;
  return {
    A: safeNum(raw.A),
    S: safeNum(raw.S),
    F: safeNum(raw.F),
    I: safeNum(raw.I),
    D: safeNum(raw.D),
    mean: safeNum(raw.mean)
  };
}

function extractRevoiScores(raw) {
  if (!raw || typeof raw !== 'object') return null;
  return {
    R: safeNum(raw.R),
    E: safeNum(raw.E),
    V: safeNum(raw.V),
    O: safeNum(raw.O),
    I: safeNum(raw.I),
    mean: safeNum(raw.mean)
  };
}

// Strip namespace prefix from a string like "m2:Cascade" → "Cascade"
function stripNs(s) {
  if (typeof s !== 'string') return s;
  const idx = s.indexOf(':');
  return idx >= 0 ? s.slice(idx + 1) : s;
}

// ─── Single file parser ───────────────────────────────────────────────────────

function parsePocletFile(filePath) {
  let raw;
  try {
    raw = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (e) {
    return null; // skip unparseable files
  }

  const graph = raw['@graph'];
  if (!Array.isArray(graph) || graph.length === 0) return null;

  const entry = extractPocletEntry(graph);
  if (!entry) return null;

  // Ontology type: check m3:ontologyType or default to 'Poclet'
  const ontologyTypeRaw = entry['m3:ontologyType'];
  let ontologyType = 'Poclet';
  if (ontologyTypeRaw) {
    const t = ontologyTypeRaw['@id'] || ontologyTypeRaw;
    ontologyType = stripNs(safeStr(t)) || 'Poclet';
  }

  // Only include Poclet entries (skip TransDisclet, TscgTool, etc.)
  // — unless you want them all; set INCLUDE_ALL_TYPES = true below
  const INCLUDE_ALL_TYPES = false;
  if (!INCLUDE_ALL_TYPES && ontologyType !== 'Poclet') return null;

  const filename = path.basename(filePath, '.jsonld');

  // label: prefer rdfs:label, fallback to filename
  const labelRaw = entry['rdfs:label'];
  const label = safeStr(labelRaw) || filename;

  const domain    = safeStr(entry['m0:domain']) || 'Unknown';
  const subdomains = safeArr(entry['m0:subdomains']);

  const asfidScores = extractScores(entry['m0:asfidScores']);
  const revoiScores = extractRevoiScores(entry['m0:revoiScores']);

  const epistemicGap = (typeof entry['m0:epistemicGap'] === 'number')
    ? entry['m0:epistemicGap']
    : null;

  const primaryMetaconcept = stripNs(safeStr(entry['m0:primaryMetaconcept']));

  const validatesRaw = safeArr(entry['m0:validatesMetaconcepts'] || entry['m0:validatedMetaconcepts']);
  const validatesMetaconcepts = validatesRaw.map(v => stripNs(safeStr(v)));

  // Build a rich text description for RAG embedding
  const description = [
    label,
    `Domain: ${domain}`,
    subdomains.length ? `Subdomains: ${subdomains.join(', ')}` : '',
    primaryMetaconcept ? `Primary concept: ${primaryMetaconcept}` : '',
    validatesMetaconcepts.length ? `Validates: ${validatesMetaconcepts.join(', ')}` : '',
    asfidScores ? `ASFID mean: ${asfidScores.mean}` : '',
    revoiScores ? `REVOI mean: ${revoiScores.mean}` : ''
  ].filter(Boolean).join('. ');

  return {
    id: filename,
    label,
    domain,
    subdomains,
    ontologyType,
    asfidScores,
    revoiScores,
    epistemicGap,
    primaryMetaconcept,
    validatesMetaconcepts,
    description,
    sourceFile: filePath
  };
}

// ─── Directory scanner ────────────────────────────────────────────────────────
//
// Recursively walks dir, returning all .jsonld files found.

function walkJsonLd(dir, results = []) {
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walkJsonLd(full, results);
    } else if (entry.isFile() && entry.name.endsWith('.jsonld')) {
      results.push(full);
    }
  }
  return results;
}

// ─── Main exported function ───────────────────────────────────────────────────

/**
 * rebuildCorpus({ startDir })
 *
 * Scans <startDir>/../../instances/poclets/ for .jsonld files,
 * extracts structured metadata from each valid poclet,
 * and writes poclet_corpus_profile.json next to this module.
 *
 * Returns: { count, path, hash, poclets }
 */
function rebuildCorpus({ startDir } = {}) {
  const baseDir      = startDir || __dirname;
  const pocletsDir   = path.resolve(baseDir, POCLETS_SUBPATH);
  const outputPath   = path.join(baseDir, OUTPUT_FILENAME);

  // ── Scan ──────────────────────────────────────────────────────────────────
  const allFiles = walkJsonLd(pocletsDir);

  const poclets = [];
  const skipped = [];

  for (const f of allFiles) {
    const parsed = parsePocletFile(f);
    if (parsed) {
      poclets.push(parsed);
    } else {
      skipped.push(path.basename(f));
    }
  }

  // ── Build all renderer-required fields ───────────────────────────────────

  const domains = [...new Set(poclets.map(p => p.domain))].sort();

  // corpus_stats
  const corpus_stats = {
    total:           poclets.length,
    domains_covered: domains.filter(d => d !== 'Unknown').length,
    validated:       poclets.filter(p => p.asfidScores).length,
  };

  // domain_coverage: { "Biology": ["M0_RAAS", …], … }
  const domain_coverage = {};
  for (const p of poclets) {
    if (!domain_coverage[p.domain]) domain_coverage[p.domain] = [];
    domain_coverage[p.domain].push(p.id);
  }

  // invariants
  const allConcepts = poclets.flatMap(p => p.validatesMetaconcepts);
  const conceptFreq = {};
  for (const c of allConcepts) {
    if (c) conceptFreq[c] = (conceptFreq[c] || 0) + 1;
  }
  const topConcepts = Object.entries(conceptFreq)
    .sort((a, b) => b[1] - a[1]).slice(0, 20)
    .map(([concept, freq]) => ({ concept, freq }));

  const asfidMeans = ['A','S','F','I','D'].reduce((acc, dim) => {
    const vals = poclets.map(p => p.asfidScores?.[dim]).filter(v => v != null);
    acc[dim] = vals.length ? +(vals.reduce((s,v) => s+v, 0) / vals.length).toFixed(3) : null;
    return acc;
  }, {});

  const revoiMeans = ['R','E','V','O','I'].reduce((acc, dim) => {
    const vals = poclets.map(p => p.revoiScores?.[dim]).filter(v => v != null);
    acc[dim] = vals.length ? +(vals.reduce((s,v) => s+v, 0) / vals.length).toFixed(3) : null;
    return acc;
  }, {});

  const invariants = {
    description:          'Statistical invariants distilled from the validated corpus',
    domains,
    topValidatedConcepts: topConcepts,
    corpusMeanASFID:      asfidMeans,
    corpusMeanREVOI:      revoiMeans,
    criteria:             INVARIANT_CRITERIA,  // ← renderer.js buildInvariantChecklist()
  };

  // gap_analysis
  const coveredLower = new Set(domains.map(d => d.toLowerCase()));
  const gap_analysis = {
    description:         'Domains and systems not yet covered in the corpus',
    uncovered_domains:   [...new Set(
      GAP_ANALYSIS_CANDIDATES
        .filter(c => !coveredLower.has(c.domain.toLowerCase()))
        .map(c => c.domain)
    )].sort(),
    priority_candidates: GAP_ANALYSIS_CANDIDATES,
  };

  // ── Output document ────────────────────────────────────────────────────────
  const now = new Date().toISOString().slice(0, 10);

  const output = {
    _meta: {
      title:        'TSCG Poclet Corpus Profile — Auto-generated by rebuild_corpus.js',
      version:      '2.1.0',
      generatedAt:  new Date().toISOString(),
      date:         now,
      authors:      ['Echopraxium with the collaboration of Claude AI'],
      purpose:      'Profiling reference used by TscgPocletMiner to score new candidates against the validated corpus.',
      pocletsDir,
      pocletCount:  poclets.length,
      skippedFiles: skipped,
    },
    corpus_stats,
    domain_coverage,
    invariants,
    gap_analysis,
    scoring_thresholds:   SCORING_THRESHOLDS,
    web_search_templates: WEB_SEARCH_TEMPLATES,
    screening_criteria:   SCREENING_CRITERIA,
    poclets,
  };

  // ── Hash (for dirty detection in rag_engine) ───────────────────────────────
  const content = JSON.stringify(output, null, 2);
  const hash = crypto.createHash('sha256').update(content).digest('hex').slice(0, 16);
  output._meta.hash = hash;

  // ── Write ──────────────────────────────────────────────────────────────────
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');

  console.log(`[rebuild_corpus] Wrote ${poclets.length} poclets → ${outputPath} (hash: ${hash})`);
  if (skipped.length) {
    console.log(`[rebuild_corpus] Skipped (non-Poclet or unparseable): ${skipped.join(', ')}`);
  }

  return { count: poclets.length, path: outputPath, hash, poclets };
}

module.exports = { rebuildCorpus };
