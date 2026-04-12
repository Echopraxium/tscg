#!/usr/bin/env node
/**
 * generate_index.js
 * =================
 * TSCG Static Poclet Gallery Generator
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Scans instances/poclets/ for sub-folders that contain a "static/" directory
 * with at least one .html file, reads the matching M0_*.jsonld and *README*.md,
 * then emits a standalone index.html at the repository root.
 *
 * Usage:
 *   node generate_index.js [options]
 *
 * Options:
 *   --root   <path>   Repository root override (optional — auto-detected by
 *                     walking up from the script's own directory)
 *   --output <path>   Output file (default: <root>/index.html)
 *   --help            Show this help
 *
 * Example:
 *   node generate_index.js
 *   node tools/generate_index.js
 *   node generate_index.js --output /tmp/gallery.html
 */

'use strict';

const fs   = require('fs');
const path = require('path');

// ── CLI args ─────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
Usage: node generate_index.js [options]

Options:
  --root     <path>   Repository root override (default: auto-detected by
                      walking up from the script's own directory until
                      instances/poclets/ is found)
  --output   <path>   Output file (default: <root>/index.html)
  --site-url <url>    Public base URL of the gallery
                      (e.g. https://echopraxium.github.io/tscg).
                      Enables <link rel="canonical"> and absolute URLs
                      in JSON-LD structured data. Trailing slash optional.
  --help              Show this help
`);
  process.exit(0);
}

function argVal(flag) {
  const i = args.indexOf(flag);
  return (i !== -1 && args[i + 1]) ? args[i + 1] : null;
}

/**
 * Auto-detect repository root by walking up from __dirname until a directory
 * containing a .git/ folder is found (most reliable repo root marker).
 * Falls back to looking for instances/poclets/, then process.cwd().
 * This makes the script location-independent regardless of where it is placed.
 */
function detectRoot() {
  let candidate = path.resolve(__dirname);
  for (let i = 0; i < 12; i++) {
    if (fs.existsSync(path.join(candidate, '.git')))               return candidate;
    if (fs.existsSync(path.join(candidate, 'instances', 'poclets'))) return candidate;
    const parent = path.dirname(candidate);
    if (parent === candidate) break;   // reached filesystem root
    candidate = parent;
  }
  return process.cwd();  // last resort
}

const _rootOverride = argVal('--root');
const _detectedRoot = detectRoot();
const ROOT        = path.resolve(_rootOverride || _detectedRoot);
const OUTPUT      = path.resolve(argVal('--output') || path.join(ROOT, 'index.html'));
const POCLETS_DIR = path.join(ROOT, 'instances', 'poclets');
const ROOT_SOURCE = _rootOverride ? '--root flag' :
  (fs.existsSync(path.join(ROOT, '.git')) ? 'auto (.git)' : 'auto (instances/poclets)');
// Public base URL — enables canonical link and absolute JSON-LD URLs (optional).
const SITE_URL = (argVal('--site-url') || '').replace(/\/+$/, '');

// ── Helpers ───────────────────────────────────────────────────────────────────
function exists(p) { try { fs.accessSync(p); return true; } catch { return false; } }
function readText(p) { try { return fs.readFileSync(p, 'utf-8'); } catch { return null; } }

function findFile(dir, predicate) {
  if (!exists(dir)) return null;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isFile() && predicate(entry.name)) return full;
    if (entry.isDirectory() && !entry.name.startsWith('.')) {
      const found = findFile(full, predicate);
      if (found) return found;
    }
  }
  return null;
}

/**
 * Like findFile but prefers files whose name contains preferHint (folder name).
 * e.g. in ColorSynthesis/, prefers M0_ColorSynthesis_Federated.jsonld over
 * M0_CMYK_Subtractive.jsonld even though CMYK sorts first alphabetically.
 * Falls back to first match if no candidate contains the hint.
 */
function findPreferredFile(dir, predicate, preferHint) {
  if (!exists(dir)) return null;
  const candidates = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isFile() && predicate(entry.name))
      candidates.push(path.join(dir, entry.name));
  }
  if (!candidates.length) return null;
  const hint = preferHint.toLowerCase();
  const preferred = candidates.find(f => path.basename(f).toLowerCase().includes(hint));
  return preferred || candidates[0];
}

function relPath(absPath) {
  return path.relative(ROOT, absPath).replace(/\\/g, '/');
}

function humanize(s) {
  return s.replace(/([A-Z])/g, ' $1').replace(/[_-]+/g, ' ').trim();
}

// ── SEO helpers ───────────────────────────────────────────────────────────────

/** Extract the first non-heading, non-empty text paragraph from markdown. */
function firstParagraph(md, maxLen = 200) {
  if (!md) return '';
  for (const line of md.split('\n')) {
    const t = line.trim();
    if (!t) continue;
    if (/^(#|\||```|---|===)/.test(t)) continue;
    return t.replace(/[*_`\[\]()]/g, '').replace(/\s+/g, ' ').trim().slice(0, maxLen);
  }
  return '';
}

/** Collect sorted unique domain strings from the poclet list. */
function uniqueDomains(poclets) {
  return [...new Set(poclets.map(p => p.domain).filter(Boolean))].sort();
}

/**
 * Build the complete SEO block to inject inside <head>:
 *   – standard meta tags (description, keywords, author, robots, theme-color)
 *   – Open Graph tags
 *   – Twitter Card tags
 *   – canonical link (if --site-url is set)
 *   – JSON-LD structured data (WebSite + ItemList)
 */
function buildSeoHead(poclets, now) {
  const domains     = uniqueDomains(poclets);
  const domainList  = domains.length ? domains.join(', ') : 'multiple scientific domains';
  const n           = poclets.length;

  // ── Meta description ──────────────────────────────────────────────────────
  const description =
    `TSCG (Transdisciplinary System Conceptual Grammar) Poclet Gallery — ` +
    `${n} interactive simulation${n !== 1 ? 's' : ''} for systemic modelling ` +
    `and ontology-driven cross-domain analysis. ` +
    `Domains covered: ${domainList}.`;

  // ── Keywords — framework vocation + technical vocabulary + discovered domains
  const FRAMEWORK_KEYWORDS = [
    // Vocation & identity
    'TSCG', 'Transdisciplinary System Conceptual Grammar',
    'transdisciplinary framework', 'transdisciplinarity',
    'systemic modeling', 'systemic modelling', 'complex systems',
    'ontology', 'ontology-driven', 'knowledge representation',
    'cross-domain analysis', 'cross-domain patterns',
    'simulation', 'interactive simulation', 'scientific visualization',
    // Architecture layers
    'poclet', 'GenericConcepts', 'M0', 'M1', 'M2', 'M3',
    'Genesis Space', 'EagleEye', 'SphinxEye', 'bicephalous architecture',
    // Analysis dimensions
    'ASFID', 'REVOI', 'epistemic gap', 'epistemic distance',
    'Attractor', 'Structure', 'Flow', 'Information', 'Dynamics',
    'Representability', 'Evolvability', 'Verifiability', 'Observability', 'Interoperability',
    // Ontology types
    'TransDisclet', 'TscgTool', 'CaseStudy', 'SymbolicSystemGrammar',
    // Tech stack
    'JSON-LD', 'OWL', 'SPARQL', 'RDF',
  ];
  const keywords = [...FRAMEWORK_KEYWORDS, ...domains].join(', ');

  // ── Open Graph ────────────────────────────────────────────────────────────
  const ogTitle   = `TSCG — Poclet Gallery (${n} simulation${n !== 1 ? 's' : ''})`;
  const siteUrl   = SITE_URL;
  const canonical = siteUrl ? `\n  <link rel="canonical" href="${siteUrl}/">` : '';
  const ogUrl     = siteUrl
    ? `\n  <meta property="og:url"         content="${siteUrl}/">`
    : '';

  // ── JSON-LD: WebSite + ItemList ───────────────────────────────────────────
  const schemaWebSite = {
    '@context':    'https://schema.org',
    '@type':       'WebSite',
    'name':        'TSCG Poclet Gallery',
    'description': description,
    'keywords':    FRAMEWORK_KEYWORDS.slice(0, 12).join(', '),
    'author': {
      '@type': 'Person',
      'name':  'Echopraxium',
      'url':   'https://github.com/Echopraxium',
    },
    'dateModified': now,
    ...(siteUrl ? { 'url': siteUrl + '/' } : {}),
  };

  const schemaItemList = {
    '@context':       'https://schema.org',
    '@type':          'ItemList',
    'name':           'TSCG Poclets',
    'description':    `List of ${n} TSCG poclet simulation${n !== 1 ? 's' : ''}`,
    'numberOfItems':  n,
    'itemListElement': poclets.map((p, i) => {
      const item = {
        '@type':    'ListItem',
        'position': i + 1,
        'name':     p.label,
      };
      if (p.domain)   item['description'] = p.domain + ' domain';
      if (siteUrl)    item['url']         = siteUrl + '/' + p.htmlRelPath;
      if (p.version)  item['version']     = p.version;
      return item;
    }),
  };

  const jsonLd =
    `  <script type="application/ld+json">\n` +
    `  ${JSON.stringify(schemaWebSite,  null, 2).replace(/\n/g, '\n  ')}\n` +
    `  </script>\n` +
    `  <script type="application/ld+json">\n` +
    `  ${JSON.stringify(schemaItemList, null, 2).replace(/\n/g, '\n  ')}\n` +
    `  </script>`;

  return `  <!-- ── SEO ─────────────────────────────────────────────────────────── -->
  <meta name="description"  content="${description}">
  <meta name="keywords"     content="${keywords}">
  <meta name="author"       content="Echopraxium">
  <meta name="robots"       content="index, follow">
  <meta name="theme-color"  content="#0d1117">
  <meta name="generator"    content="generate_index.js (TSCG)">
  <meta name="date"         content="${now}">${canonical}
  <!-- Open Graph -->
  <meta property="og:type"         content="website">
  <meta property="og:site_name"    content="TSCG Poclet Gallery">
  <meta property="og:title"        content="${ogTitle}">
  <meta property="og:description"  content="${description}">${ogUrl}
  <!-- Twitter Card -->
  <meta name="twitter:card"        content="summary">
  <meta name="twitter:title"       content="${ogTitle}">
  <meta name="twitter:description" content="${description}">
  <!-- JSON-LD structured data -->
${jsonLd}
  <!-- ─────────────────────────────────────────────────────────────────── -->`;
}

// ── Discovery ─────────────────────────────────────────────────────────────────
function discoverPoclets() {
  // POCLETS_DIR existence already verified in main()

  const results = [];

  for (const entry of fs.readdirSync(POCLETS_DIR, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue;

    const pocletDir = path.join(POCLETS_DIR, entry.name);
    const staticDir = path.join(pocletDir, 'static');

    // Only include poclets that have static/*.html
    if (!exists(staticDir)) continue;
    const htmlFiles = fs.readdirSync(staticDir).filter(f => f.endsWith('.html'));
    if (!htmlFiles.length) continue;

    const htmlRelPath = relPath(path.join(staticDir, htmlFiles[0]));

    // M0_*.jsonld → metadata  (prefer file matching folder name, e.g. ColorSynthesis)
    const jsonldFile = findPreferredFile(pocletDir,
      n => n.startsWith('M0_') && n.endsWith('.jsonld'), entry.name);
    const meta = jsonldFile ? parseJsonld(jsonldFile) : {};

    // *README*.md → prose  (prefer file matching folder name)
    const readmeFile = findPreferredFile(pocletDir,
      n => /readme/i.test(n) && n.endsWith('.md'), entry.name);
    const readme = readmeFile ? (readText(readmeFile) || '') : '';

    results.push({
      id:          entry.name,
      label:       meta.label   || humanize(entry.name),
      domain:      meta.domain  || '',
      version:     meta.version || '',
      gap:         (meta.gap != null) ? meta.gap : null,
      asfid:       meta.asfid  || null,
      revoi:       meta.revoi  || null,
      htmlRelPath,
      hasReadme:   readme.length > 0,
      readme,
    });
  }


  // Domain overrides (corrections not yet in M0_*.jsonld)
  const DOMAIN_OVERRIDES = {
    'FireTriangle':     'Chemistry/Physics',
    'FourStrokeEngine': 'Thermodynamics',
    'CounterPoint':     'Music',
    'Counterpoint':     'Music',
  };
  // Label overrides (when M0 label is wrong or refers to a sub-poclet)
  const LABEL_OVERRIDES = {
    'ColorSynthesis': 'Color Synthesis',
    'Transistor':     'Transistor',
  };
  results.forEach(p => {
    if (DOMAIN_OVERRIDES[p.id]) p.domain = DOMAIN_OVERRIDES[p.id];
    if (LABEL_OVERRIDES[p.id])  p.label  = LABEL_OVERRIDES[p.id];
  });
  results.sort((a, b) => a.label.localeCompare(b.label));
  return results;
}

function parseJsonld(filePath) {
  try {
    const raw  = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    const node = (raw['@graph'] || [raw])[0] || {};
    const as   = node['m0:asfidScores'] || null;
    const rv   = node['m0:revoiScores'] || null;
    return {
      label:   (node['rdfs:label'] || '').replace(/\s*\([^)]+\)\s*$/, '').trim() || '',
      domain:  (node['m0:domain'] && node['m0:domain'] !== 'Poclet') ? node['m0:domain'] : '',
      version: node['m0:version']      || '',
      gap:     (node['m0:epistemicGap'] != null)
                 ? parseFloat(node['m0:epistemicGap']) : null,
      asfid:   as ? ['A','S','F','I','D'].map(k => parseFloat(as[k] || 0)) : null,
      revoi:   rv ? ['R','E','V','O','I'].map(k => parseFloat(rv[k] || 0)) : null,
    };
  } catch { return {}; }
}

// ── Client-side JavaScript (kept outside HTML template to preserve regex backslashes) ──

// ── HTML generation ───────────────────────────────────────────────────────────
// Returns the HTML shell (DOCTYPE through #shell div). The <script> block is
// appended separately by main() to avoid backslash-corruption in template literals.
function generateHtml(poclets) {
  const now    = new Date().toISOString().split('T')[0];
  const seoHead = buildSeoHead(poclets, now);
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'self' https://echopraxium.github.io;
                 script-src 'self' 'unsafe-inline' 'unsafe-eval';
                 style-src  'self' 'unsafe-inline';
                 img-src    'self' data: blob:;
                 connect-src 'self' http://127.0.0.1:* ws://127.0.0.1:*;">
  <title>TSCG &mdash; Poclet Gallery</title>
${seoHead}
  <style>
/* ── Reset & variables ──────────────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0d1117; --bg-panel:#161b22; --bg-card:#1c2130; --bg-hover:#21262d;
  --border:#30363d; --border2:#3d444f;
  --eagle:#f78166; --sphinx:#79c0ff; --accent:#56d364; --warn:#e3b341;
  --muted:#8b949e; --text:#e6edf3; --text-dim:#b1bac4;
  --col-A:#ffb840; --col-S:#64c8ff; --col-F:#3dc896;
  --col-I:#c882ff; --col-D:#ff6464;
  --col-R:#79c0ff; --col-E:#56d364; --col-V:#f78166;
  --col-O:#d2a8ff; --col-Im:#e3b341;
  --header-h:46px; --footer-h:44px; --left-w:290px; --split-w:5px;
  --radius:6px;
  --font:'Segoe UI',system-ui,-apple-system,sans-serif;
  --mono:'Cascadia Code','Fira Code','Consolas',monospace;
}
html,body{height:100%;overflow:hidden;font-family:var(--font);
  background:var(--bg);color:var(--text);font-size:13px;line-height:1.5;}

/* ── Shell grid ─────────────────────────────────────────────────────── */
#shell{
  display:grid;
  grid-template-rows:var(--header-h) 1fr var(--footer-h);
  grid-template-columns:var(--left-w) var(--split-w) 1fr;
  grid-template-areas:
    "header header header"
    "tree   split  readme"
    "footer footer footer";
  height:100vh;
}

/* ── Header ─────────────────────────────────────────────────────────── */
#header{grid-area:header;display:flex;align-items:baseline;gap:12px;padding:0 16px;
  background:var(--bg-panel);border-bottom:1px solid var(--border);}
.logo{font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--eagle);text-transform:uppercase;cursor:pointer;background:none;border:none;padding:0;font-family:var(--font);line-height:1;}
.logo:hover{color:#ff9178;}
.title{font-size:14px;font-weight:600;flex:1;line-height:1;}
.chip{padding:2px 8px;border-radius:20px;font-size:11px;font-weight:500;border:1px solid transparent;}
.chip-count{background:rgba(86,211,100,.12);border-color:rgba(86,211,100,.3);color:var(--accent);}
.chip-date {background:rgba(121,192,255,.12);border-color:rgba(121,192,255,.3);color:var(--sphinx);}

/* ── Tag Filter ─────────────────────────────────────────────────────── */
.tag-filter-section{padding:12px;border-bottom:1px solid var(--border);background:var(--bg-card);}
.tag-filter-label{font-size:12px;font-weight:600;color:var(--text-dim);margin-bottom:8px;
  text-transform:uppercase;letter-spacing:.5px;}
.tag-select-row{display:flex;gap:6px;align-items:stretch;}
.tag-select{flex:1;background:var(--bg-panel);border:1px solid var(--border);
  border-radius:var(--radius);color:var(--text);padding:6px 8px;font-size:13px;
  font-family:var(--font);cursor:pointer;outline:none;transition:border-color .2s;}
.tag-select:hover{border-color:var(--border2);}
.tag-select:focus{border-color:var(--accent);}
.tag-select option{background:var(--bg-panel);color:var(--text);padding:4px;}
.clear-tags-btn{width:32px;background:var(--bg-panel);border:1px solid var(--border);
  border-radius:var(--radius);color:var(--muted);font-size:16px;font-weight:bold;
  cursor:pointer;outline:none;transition:all .2s;display:flex;align-items:center;
  justify-content:center;padding:0;flex-shrink:0;}
.clear-tags-btn:hover{background:var(--bg-hover);border-color:var(--border2);color:var(--text);}
.clear-tags-btn:active{transform:scale(.95);}
.clear-tags-btn:disabled{opacity:.3;cursor:not-allowed;}
.clear-tags-btn:disabled:hover{background:var(--bg-panel);border-color:var(--border);
  color:var(--muted);transform:none;}
.selected-tags-container{margin-top:12px;max-height:120px;overflow-y:auto;overflow-x:hidden;
  padding:8px;background:var(--bg);border:1px solid var(--border);
  border-radius:var(--radius);min-height:48px;}
.selected-tags-container::-webkit-scrollbar{width:8px;}
.selected-tags-container::-webkit-scrollbar-track{background:var(--bg-panel);border-radius:4px;}
.selected-tags-container::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px;}
.selected-tags-container::-webkit-scrollbar-thumb:hover{background:var(--muted);}
.selected-tags-empty{color:var(--muted);font-size:12px;font-style:italic;
  text-align:center;padding:8px 0;}
.tag-pill{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;margin:3px;
  border-radius:12px;font-size:12px;font-weight:500;cursor:pointer;
  transition:all .2s;user-select:none;}
.tag-pill:hover{transform:translateY(-1px);filter:brightness(1.15);}
.tag-pill:active{transform:translateY(0);}
.tag-remove{width:14px;height:14px;border-radius:50%;background:rgba(0,0,0,.3);
  display:flex;align-items:center;justify-content:center;font-size:10px;
  font-weight:bold;transition:background .2s;}
.tag-pill:hover .tag-remove{background:rgba(0,0,0,.5);}
.tag-color-0{background:linear-gradient(135deg,#ff6b6b,#ee5a6f);color:#fff;}
.tag-color-1{background:linear-gradient(135deg,#4ecdc4,#44a08d);color:#fff;}
.tag-color-2{background:linear-gradient(135deg,#ffd93d,#f6b93b);color:#2c2c2c;}
.tag-color-3{background:linear-gradient(135deg,#6c5ce7,#5f27cd);color:#fff;}
.tag-color-4{background:linear-gradient(135deg,#fd79a8,#e84393);color:#fff;}
.tag-color-5{background:linear-gradient(135deg,#00b894,#00a896);color:#fff;}
.tag-color-6{background:linear-gradient(135deg,#74b9ff,#0984e3);color:#fff;}
.tag-color-7{background:linear-gradient(135deg,#ff7675,#d63031);color:#fff;}

/* ── Tree panel ─────────────────────────────────────────────────────── */
#tree-panel{grid-area:tree;display:flex;flex-direction:column;
  background:var(--bg-panel);border-right:1px solid var(--border);
  overflow:hidden;min-width:160px;}
#tree-header{display:flex;justify-content:space-between;align-items:center;
  padding:8px 12px;font-size:11px;font-weight:500;
  color:var(--muted);
  border-bottom:1px solid var(--border);flex-shrink:0;}
.tree-count-num{color:var(--accent);font-weight:600;}
#tree-list{overflow-y:auto;flex:1;}
.tree-item{display:flex;align-items:center;gap:8px;padding:7px 12px;
  cursor:pointer;border-left:3px solid transparent;
  transition:background .12s,border-color .12s;}
.tree-item:hover{background:var(--bg-hover);}
.tree-item.active{background:rgba(121,192,255,.08);border-left-color:var(--sphinx);}
.tree-item.filtered{display:none;}
.tree-icon{font-size:10px;color:var(--border2);flex-shrink:0;}
.tree-label{flex:1;font-size:12px;color:var(--text-dim);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.tree-item.active .tree-label{color:var(--text);}

/* ── Splitter ───────────────────────────────────────────────────────── */
#splitter{grid-area:split;background:var(--border);cursor:col-resize;
  transition:background .15s;z-index:10;}
#splitter:hover,#splitter.dragging{background:var(--sphinx);}

/* ── README panel ───────────────────────────────────────────────────── */
#readme-panel{grid-area:readme;display:flex;flex-direction:column;
  overflow:hidden;min-width:200px;}
#readme-header{display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:8px 16px;flex-shrink:0;
  background:var(--bg-panel);border-bottom:1px solid var(--border);}
#readme-poclet-name{font-size:14px;font-weight:600;flex:1;}
#readme-body{flex:1;overflow-y:auto;padding:20px 24px;background:var(--bg);}

/* ── Scores strip ───────────────────────────────────────────────────── */
#scores-strip{display:none;align-items:center;gap:14px;flex-wrap:nowrap;
  padding:7px 16px;background:var(--bg-panel);
  border-bottom:1px solid var(--border);flex-shrink:0;overflow-x:auto;}
#scores-strip.visible{display:flex;}
.score-group{display:flex;align-items:center;gap:7px;flex-shrink:0;}
.score-group-label{font-size:10px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;flex-shrink:0;}
.score-group-label.eagle{color:var(--eagle);}
.score-group-label.sphinx{color:var(--sphinx);}
.score-mini{display:flex;align-items:center;gap:4px;}
.score-mini-ltr{font-family:var(--mono);font-size:10px;font-weight:700;
  width:13px;text-align:center;flex-shrink:0;}
.score-mini-bg{width:44px;height:4px;background:var(--bg-card);border-radius:2px;overflow:hidden;}
.score-mini-fill{height:100%;border-radius:2px;}
.score-sep{width:1px;height:22px;background:var(--border);flex-shrink:0;}
.gap-mini{display:flex;align-items:center;gap:6px;flex-shrink:0;
  padding:3px 8px;background:var(--bg-card);border-radius:4px;border:1px solid var(--border);}
.gap-mini-lbl{font-size:10px;color:var(--muted);}
.gap-mini-val{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--accent);}

/* ── Placeholder ────────────────────────────────────────────────────── */
.readme-placeholder{height:100%;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:10px;
  color:var(--muted);text-align:center;opacity:.6;}
.ph-title{font-size:15px;font-weight:600;color:var(--text-dim);}
.ph-sub{font-size:12px;}

/* ── Markdown ───────────────────────────────────────────────────────── */
.readme-md{max-width:820px;font-size:13px;line-height:1.75;color:var(--text-dim);}
.readme-md h1{font-size:20px;font-weight:700;color:var(--text);
  border-bottom:1px solid var(--border);padding-bottom:6px;margin:24px 0 12px;}
.readme-md h2{font-size:15px;font-weight:700;color:var(--text);
  border-bottom:1px solid var(--border);padding-bottom:4px;margin:20px 0 8px;}
.readme-md h3{font-size:13px;font-weight:700;color:var(--text-dim);margin:16px 0 6px;}
.readme-md p{margin:0 0 10px;}
.readme-md strong{color:var(--text);}
.readme-md code{font-family:var(--mono);font-size:11.5px;background:var(--bg-card);
  padding:1px 5px;border-radius:3px;color:var(--sphinx);}
.readme-md pre{background:var(--bg-card);border:1px solid var(--border);
  border-radius:var(--radius);padding:12px 14px;overflow-x:auto;margin:10px 0;}
.readme-md pre code{background:none;padding:0;font-size:11.5px;color:var(--text-dim);}
.readme-md table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12px;}
.readme-md th{background:var(--bg-card);color:var(--text);font-weight:700;
  padding:6px 10px;border:1px solid var(--border);text-align:left;}
.readme-md td{padding:5px 10px;border:1px solid var(--border);color:var(--text-dim);}
.readme-md ul,.readme-md ol{padding-left:20px;margin:6px 0 10px;}
.readme-md li{margin-bottom:3px;}
.readme-md blockquote{border-left:3px solid var(--sphinx);padding:4px 12px;
  margin:8px 0;color:var(--muted);background:rgba(121,192,255,.04);
  border-radius:0 4px 4px 0;}
.readme-md hr{border:none;border-top:1px solid var(--border);margin:16px 0;}
.readme-md a{color:var(--sphinx);text-decoration:none;}
.readme-md a:hover{text-decoration:underline;}

/* ── Footer ─────────────────────────────────────────────────────────── */
#footer{grid-area:footer;display:flex;align-items:center;gap:10px;padding:0 16px;
  background:var(--bg-panel);border-top:1px solid var(--border);}
#launch-btn{padding:5px 16px;border-radius:var(--radius);
  background:rgba(86,211,100,.12);border:1px solid rgba(86,211,100,.35);
  color:var(--accent);font-size:12px;font-weight:600;font-family:var(--font);
  cursor:pointer;text-decoration:none;display:inline-flex;align-items:center;gap:6px;
  transition:background .15s,border-color .15s;}
#launch-btn:hover{background:rgba(86,211,100,.22);border-color:rgba(86,211,100,.55);}
#launch-btn.hidden{display:none;}
#footer-info{font-size:12px;color:var(--text-dim);flex:1;}
#footer-path{font-size:10px;color:var(--border2);font-family:var(--mono);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:400px;}
.status-dot{width:7px;height:7px;border-radius:50%;background:var(--accent);
  margin-left:auto;flex-shrink:0;}

/* ── Scrollbar ──────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:4px;}
::-webkit-scrollbar-thumb:hover{background:var(--muted);}
  </style>
</head>
<body>
<div id="shell">

  <!-- HEADER -->
  <header id="header">
    <button id="tscg-logo-btn" class="logo" onclick="window.open('https://github.com/Echopraxium/tscg','_blank')">TSCG</button>
    <span class="title">Poclet Gallery &mdash; Static Simulations</span>
    <span class="chip chip-count" id="hdr-count">0 simulations</span>
    <span class="chip chip-date">${now}</span>
  </header>

  <!-- TREE -->
  <div id="tree-panel">
    <!-- Tag filter section -->
    <div class="tag-filter-section">
      <div class="tag-filter-label">🏷️ Filter by Tags</div>
      <div class="tag-select-row">
        <select id="tag-select" class="tag-select">
          <option value="">— Select a tag —</option>
        </select>
        <button id="clear-tags-btn" class="clear-tags-btn" title="Clear all tags">✕</button>
      </div>
      <div id="selected-tags" class="selected-tags-container">
        <div class="selected-tags-empty">No tags selected</div>
      </div>
    </div>
    <div id="tree-header">
      <div class="tree-count">Showing <span class="tree-count-num" id="visible-count">0</span> of <span class="tree-count-num" id="tree-count">0</span> poclets</div>
    </div>
    <div id="tree-list"></div>
  </div>

  <!-- SPLITTER -->
  <div id="splitter"></div>

  <!-- README + SCORES -->
  <div id="readme-panel">
    <div id="readme-header">
      <span id="readme-poclet-name" style="color:var(--muted)">Select a poclet</span>
      <span id="readme-domain" style="font-size:11px;color:var(--muted)"></span>
    </div>
    <div id="scores-strip"></div>
    <div id="readme-body">
      <div class="readme-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="1" opacity=".3">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
        </svg>
        <div class="ph-title">Select a poclet</div>
        <div class="ph-sub">Click a poclet in the left panel to read its README</div>
        <div class="ph-sub" style="margin-top:6px;font-size:10px;color:var(--border2)">
          &uarr;&darr; Arrow keys to navigate &nbsp;&middot;&nbsp;
          Enter to open simulation
        </div>
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer id="footer">
    <a id="launch-btn" class="hidden" href="#" target="_blank" rel="noopener">
      &#9654; Open Simulation
    </a>
    <span id="footer-info"></span>
    <span id="footer-path"></span>
    <div class="status-dot"></div>
  </footer>


<!-- TSCG logo tooltip -->
<div id="tscg-tip" style="
  position:fixed;z-index:999999;
  background:#1c2130;color:#e6edf3;
  border:1px solid #3d444f;border-radius:6px;
  padding:4px 10px;font-size:11px;font-weight:500;
  letter-spacing:0.04em;white-space:nowrap;
  pointer-events:none;opacity:0;transition:opacity 0.18s;
">TSCG Github repository</div>
<script>
(function(){
  const btn = document.getElementById('tscg-logo-btn');
  const tip = document.getElementById('tscg-tip');
  if (!btn || !tip) return;
  btn.addEventListener('mouseenter', function() {
    const r = btn.getBoundingClientRect();
    tip.style.left = Math.max(8, r.left) + 'px';
    tip.style.top  = (r.bottom + 6) + 'px';
    tip.style.transform = 'none';
    tip.style.opacity = '1';
  });
  btn.addEventListener('mouseleave', function() { tip.style.opacity = '0'; });
})();
</script>

</div><!-- #shell -->
`;
}

const _CLIENT_JS_B64 = 'J3VzZSBzdHJpY3QnOwovLyDilIDilIAgRW1iZWRkZWQgZGF0YSDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIAKY29uc3QgUE9DTEVUUyA9IERBVEFfUExBQ0VIT0xERVI7CmNvbnN0IEJBU0VfVVJMID0gU0lURV9VUkxfUExBQ0VIT0xERVI7Ci8vIEdlbmVyYXRlZDogREFURV9QTEFDRUhPTERFUgoKY29uc3QgQVNGSURfQ09MT1JTID0gWyd2YXIoLS1jb2wtQSknLCd2YXIoLS1jb2wtUyknLCd2YXIoLS1jb2wtRiknLCd2YXIoLS1jb2wtSSknLCd2YXIoLS1jb2wtRCknXTsKY29uc3QgUkVWT0lfQ09MT1JTID0gWyd2YXIoLS1jb2wtUiknLCd2YXIoLS1jb2wtRSknLCd2YXIoLS1jb2wtViknLCd2YXIoLS1jb2wtTyknLCd2YXIoLS1jb2wtSW0pJ107CgpsZXQgc2VsZWN0ZWRJZCA9IG51bGw7CmNvbnN0IHNlbGVjdGVkVGFncyA9IG5ldyBTZXQoKTsKCndpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdET01Db250ZW50TG9hZGVkJywgKCkgPT4gewogIHBvcHVsYXRlVGFnU2VsZWN0KCk7CiAgcmVuZGVyVHJlZSgpOwogIGluaXRUcmVlTGlzdGVuZXJzKCk7CiAgaW5pdFRhZ0xpc3RlbmVycygpOwogIGluaXRTcGxpdHRlcigpOwogIGluaXRLZXlib2FyZCgpOwogIGZpbHRlclBvY2xldHMoKTsKfSk7CgovLyDilIDilIAgVGFnIG1hbmFnZW1lbnQg4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSACgpmdW5jdGlvbiBwb3B1bGF0ZVRhZ1NlbGVjdCgpIHsKICBjb25zdCBhbGxUYWdzID0gbmV3IFNldCgpOwogIFBPQ0xFVFMuZm9yRWFjaChwID0+IHsKICAgIGlmIChwLmRvbWFpbikgYWxsVGFncy5hZGQocC5kb21haW4pOwogIH0pOwogIGNvbnN0IHNvcnRlZCA9IFsuLi5hbGxUYWdzXS5zb3J0KCk7CiAgY29uc3Qgc2VsZWN0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3RhZy1zZWxlY3QnKTsKICBzb3J0ZWQuZm9yRWFjaCh0YWcgPT4gewogICAgY29uc3Qgb3B0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnb3B0aW9uJyk7CiAgICBvcHQudmFsdWUgPSB0YWc7CiAgICBvcHQudGV4dENvbnRlbnQgPSB0YWc7CiAgICBzZWxlY3QuYXBwZW5kQ2hpbGQob3B0KTsKICB9KTsKfQoKZnVuY3Rpb24gZ2V0VGFnQ29sb3IodGFnKSB7CiAgbGV0IGhhc2ggPSAwOwogIGZvciAobGV0IGkgPSAwOyBpIDwgdGFnLmxlbmd0aDsgaSsrKSB7CiAgICBoYXNoID0gdGFnLmNoYXJDb2RlQXQoaSkgKyAoKGhhc2ggPDwgNSkgLSBoYXNoKTsKICB9CiAgcmV0dXJuIE1hdGguYWJzKGhhc2gpICUgODsKfQoKZnVuY3Rpb24gcmVuZGVyU2VsZWN0ZWRUYWdzKCkgewogIGNvbnN0IGNvbnRhaW5lciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzZWxlY3RlZC10YWdzJyk7CiAgY29uc3QgY2xlYXJCdG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnY2xlYXItdGFncy1idG4nKTsKICAKICBpZiAoc2VsZWN0ZWRUYWdzLnNpemUgPT09IDApIHsKICAgIGNvbnRhaW5lci5pbm5lckhUTUwgPSAnPGRpdiBjbGFzcz0ic2VsZWN0ZWQtdGFncy1lbXB0eSI+Tm8gdGFncyBzZWxlY3RlZDwvZGl2Pic7CiAgICBjbGVhckJ0bi5kaXNhYmxlZCA9IHRydWU7CiAgICByZXR1cm47CiAgfQogIAogIGNsZWFyQnRuLmRpc2FibGVkID0gZmFsc2U7CiAgCiAgbGV0IGh0bWwgPSAnJzsKICBzZWxlY3RlZFRhZ3MuZm9yRWFjaCh0YWcgPT4gewogICAgY29uc3QgY29sb3JDbGFzcyA9ICd0YWctY29sb3ItJyArIGdldFRhZ0NvbG9yKHRhZyk7CiAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJ0YWctcGlsbCAnICsgY29sb3JDbGFzcyArICciIGRhdGEtdGFnPSInICsgZXNjKHRhZykgKyAnIj4nICsKICAgICAgJzxzcGFuPicgKyBlc2ModGFnKSArICc8L3NwYW4+JyArCiAgICAgICc8c3BhbiBjbGFzcz0idGFnLXJlbW92ZSI+4pyVPC9zcGFuPicgKwogICAgICAnPC9kaXY+JzsKICB9KTsKICAKICBjb250YWluZXIuaW5uZXJIVE1MID0gaHRtbDsKICAKICBjb250YWluZXIucXVlcnlTZWxlY3RvckFsbCgnLnRhZy1waWxsJykuZm9yRWFjaChwaWxsID0+IHsKICAgIHBpbGwuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7CiAgICAgIGNvbnN0IHRhZyA9IHBpbGwuZGF0YXNldC50YWc7CiAgICAgIHNlbGVjdGVkVGFncy5kZWxldGUodGFnKTsKICAgICAgcmVuZGVyU2VsZWN0ZWRUYWdzKCk7CiAgICAgIGZpbHRlclBvY2xldHMoKTsKICAgIH0pOwogIH0pOwp9CgpmdW5jdGlvbiBmaWx0ZXJQb2NsZXRzKCkgewogIGNvbnN0IGl0ZW1zID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLnRyZWUtaXRlbScpOwogIGxldCB2aXNpYmxlQ291bnQgPSAwOwogIGxldCBmaXJzdFZpc2libGVJdGVtID0gbnVsbDsKICAKICBpdGVtcy5mb3JFYWNoKGl0ZW0gPT4gewogICAgY29uc3QgcG9jbGV0ID0gUE9DTEVUUy5maW5kKHAgPT4gcC5pZCA9PT0gaXRlbS5kYXRhc2V0LmlkKTsKICAgIGlmICghcG9jbGV0KSByZXR1cm47CiAgICAKICAgIGlmIChzZWxlY3RlZFRhZ3Muc2l6ZSA9PT0gMCkgewogICAgICBpdGVtLmNsYXNzTGlzdC5yZW1vdmUoJ2ZpbHRlcmVkJyk7CiAgICAgIGlmICghZmlyc3RWaXNpYmxlSXRlbSkgZmlyc3RWaXNpYmxlSXRlbSA9IGl0ZW07CiAgICAgIHZpc2libGVDb3VudCsrOwogICAgICByZXR1cm47CiAgICB9CiAgICAKICAgIGNvbnN0IGhhc01hdGNoID0gQXJyYXkuZnJvbShzZWxlY3RlZFRhZ3MpLnNvbWUoc2VsZWN0ZWRUYWcgPT4gCiAgICAgIHBvY2xldC5kb21haW4gJiYgKAogICAgICAgIHBvY2xldC5kb21haW4udG9Mb3dlckNhc2UoKS5pbmNsdWRlcyhzZWxlY3RlZFRhZy50b0xvd2VyQ2FzZSgpKSB8fAogICAgICAgIHNlbGVjdGVkVGFnLnRvTG93ZXJDYXNlKCkuaW5jbHVkZXMocG9jbGV0LmRvbWFpbi50b0xvd2VyQ2FzZSgpKQogICAgICApCiAgICApOwogICAgCiAgICBpZiAoaGFzTWF0Y2gpIHsKICAgICAgaXRlbS5jbGFzc0xpc3QucmVtb3ZlKCdmaWx0ZXJlZCcpOwogICAgICBpZiAoIWZpcnN0VmlzaWJsZUl0ZW0pIGZpcnN0VmlzaWJsZUl0ZW0gPSBpdGVtOwogICAgICB2aXNpYmxlQ291bnQrKzsKICAgIH0gZWxzZSB7CiAgICAgIGl0ZW0uY2xhc3NMaXN0LmFkZCgnZmlsdGVyZWQnKTsKICAgIH0KICB9KTsKICAKICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndmlzaWJsZS1jb3VudCcpLnRleHRDb250ZW50ID0gdmlzaWJsZUNvdW50OwogIAogIC8vIEF1dG8tc2VsZWN0IGZpcnN0IHZpc2libGUgaXRlbQogIGlmIChmaXJzdFZpc2libGVJdGVtKSB7CiAgICBzZWxlY3RQb2NsZXRFbGVtZW50KGZpcnN0VmlzaWJsZUl0ZW0pOwogIH0gZWxzZSB7CiAgICAvLyBObyB2aXNpYmxlIGl0ZW1zIC0gY2xlYXIgc2VsZWN0aW9uCiAgICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcudHJlZS1pdGVtJykuZm9yRWFjaChpID0+IGkuY2xhc3NMaXN0LnJlbW92ZSgnYWN0aXZlJykpOwogICAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2xhdW5jaC1idG4nKS5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTsKICAgIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdmb290ZXItaW5mbycpLnRleHRDb250ZW50ID0gJyc7CiAgfQp9CgpmdW5jdGlvbiBzZWxlY3RQb2NsZXRFbGVtZW50KGl0ZW0pIHsKICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcudHJlZS1pdGVtJykuZm9yRWFjaChpID0+IGkuY2xhc3NMaXN0LnJlbW92ZSgnYWN0aXZlJykpOwogIGl0ZW0uY2xhc3NMaXN0LmFkZCgnYWN0aXZlJyk7CiAgc2VsZWN0UG9jbGV0KGl0ZW0uZGF0YXNldC5pZCk7Cn0KCmZ1bmN0aW9uIGluaXRUYWdMaXN0ZW5lcnMoKSB7CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3RhZy1zZWxlY3QnKS5hZGRFdmVudExpc3RlbmVyKCdjaGFuZ2UnLCBlID0+IHsKICAgIGNvbnN0IHRhZyA9IGUudGFyZ2V0LnZhbHVlOwogICAgaWYgKHRhZyAmJiAhc2VsZWN0ZWRUYWdzLmhhcyh0YWcpKSB7CiAgICAgIHNlbGVjdGVkVGFncy5hZGQodGFnKTsKICAgICAgcmVuZGVyU2VsZWN0ZWRUYWdzKCk7CiAgICAgIGZpbHRlclBvY2xldHMoKTsKICAgIH0KICAgIGUudGFyZ2V0LnZhbHVlID0gJyc7CiAgfSk7CiAgCiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2NsZWFyLXRhZ3MtYnRuJykuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiB7CiAgICBzZWxlY3RlZFRhZ3MuY2xlYXIoKTsKICAgIHJlbmRlclNlbGVjdGVkVGFncygpOwogICAgZmlsdGVyUG9jbGV0cygpOwogIH0pOwp9CgovLyDilIDilIAgVHJlZSByZW5kZXJpbmcg4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSA4pSACgpmdW5jdGlvbiByZW5kZXJUcmVlKCkgewogIGNvbnN0IGxpc3QgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1saXN0Jyk7CiAgY29uc3QgbiAgICA9IFBPQ0xFVFMubGVuZ3RoOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd0cmVlLWNvdW50JykudGV4dENvbnRlbnQgPSBuOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd2aXNpYmxlLWNvdW50JykudGV4dENvbnRlbnQgPSBuOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdoZHItY291bnQnKS50ZXh0Q29udGVudCAgPQogICAgbiArICcgc2ltdWxhdGlvbicgKyAobiAhPT0gMSA/ICdzJyA6ICcnKTsKICBpZiAoIW4pIHsKICAgIGxpc3QuaW5uZXJIVE1MID0KICAgICAgJzxkaXYgc3R5bGU9InBhZGRpbmc6MTZweCAxMnB4O2ZvbnQtc2l6ZToxMXB4O2NvbG9yOnZhcigtLW11dGVkKSI+Tm8gc3RhdGljIHNpbXVsYXRpb25zIGZvdW5kLjwvZGl2Pic7CiAgICByZXR1cm47CiAgfQogIGxpc3QuaW5uZXJIVE1MID0gUE9DTEVUUy5tYXAocCA9PgogICAgJzxkaXYgY2xhc3M9InRyZWUtaXRlbSIgZGF0YS1pZD0iJyArIGVzYyhwLmlkKSArICciJyArCiAgICAocC5kb21haW4gPyAnIHRpdGxlPSInICsgZXNjKHAuZG9tYWluKSArICciJyA6ICcnKSArCiAgICAnIHN0eWxlPSJjdXJzb3I6cG9pbnRlciI+JyArCiAgICAnPHNwYW4gY2xhc3M9InRyZWUtaWNvbiI+JiM5NjU0Ozwvc3Bhbj4nICsKICAgICc8c3BhbiBjbGFzcz0idHJlZS1sYWJlbCI+JyArIGVzYyhwLmxhYmVsKSArICc8L3NwYW4+JyArCiAgICAnPC9kaXY+JwogICkuam9pbignJyk7Cn0KCmZ1bmN0aW9uIHNlbGVjdFBvY2xldChpZCkgewogIHNlbGVjdGVkSWQgPSBpZDsKICBjb25zdCBwICAgID0gUE9DTEVUUy5maW5kKHggPT4geC5pZCA9PT0gaWQpOwogIGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoJy50cmVlLWl0ZW0nKS5mb3JFYWNoKGVsID0+CiAgICBlbC5jbGFzc0xpc3QudG9nZ2xlKCdhY3RpdmUnLCBlbC5kYXRhc2V0LmlkID09PSBpZCkpOwogIGNvbnN0IG5hbWVFbCAgID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlYWRtZS1wb2NsZXQtbmFtZScpOwogIGNvbnN0IGRvbWFpbkVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlYWRtZS1kb21haW4nKTsKICBuYW1lRWwudGV4dENvbnRlbnQgICA9IHAgPyBwLmxhYmVsICAgOiAnU2VsZWN0IGEgcG9jbGV0JzsKICBuYW1lRWwuc3R5bGUuY29sb3IgICA9IHAgPyAndmFyKC0tdGV4dCknIDogJ3ZhcigtLW11dGVkKSc7CiAgZG9tYWluRWwudGV4dENvbnRlbnQgPSBwICYmIHAuZG9tYWluID8gcC5kb21haW4gOiAnJzsKICByZW5kZXJTY29yZXNTdHJpcChwKTsKICBjb25zdCBidG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnbGF1bmNoLWJ0bicpOwogIGlmIChwKSB7IGJ0bi5ocmVmID0gQkFTRV9VUkwgPyBCQVNFX1VSTCArICcvJyArIHAuaHRtbFJlbFBhdGggOiBwLmh0bWxSZWxQYXRoOyBidG4uY2xhc3NMaXN0LnJlbW92ZSgnaGlkZGVuJyk7IH0KICBlbHNlICAgeyBidG4uY2xhc3NMaXN0LmFkZCgnaGlkZGVuJyk7IH0KICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnZm9vdGVyLWluZm8nKS50ZXh0Q29udGVudCA9CiAgICBwID8gcC5sYWJlbCArIChwLnZlcnNpb24gPyAnICB2JyArIHAudmVyc2lvbiA6ICcnKSA6ICcnOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdmb290ZXItcGF0aCcpLnRleHRDb250ZW50ID0KICAgIHAgPyAoQkFTRV9VUkwgPyBCQVNFX1VSTCArICcvJyArIHAuaHRtbFJlbFBhdGggOiBwLmh0bWxSZWxQYXRoKSA6ICcnOwogIGlmICghcCkgICAgICAgICAgIHsgc2hvd1BsYWNlaG9sZGVyKCdObyBwb2NsZXQgc2VsZWN0ZWQnKTsgcmV0dXJuOyB9CiAgaWYgKCFwLmhhc1JlYWRtZSkgeyBzaG93UGxhY2Vob2xkZXIocC5sYWJlbCArICdcblxuTm8gUkVBRE1FIGZvdW5kLicpOyByZXR1cm47IH0KICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVhZG1lLWJvZHknKS5pbm5lckhUTUwgPQogICAgJzxkaXYgY2xhc3M9InJlYWRtZS1tZCI+JyArIHBhcnNlTWFya2Rvd24ocC5yZWFkbWUpICsgJzwvZGl2Pic7CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlYWRtZS1ib2R5Jykuc2Nyb2xsVG9wID0gMDsKfQoKZnVuY3Rpb24gcmVuZGVyU2NvcmVzU3RyaXAocCkgewogIGNvbnN0IHN0cmlwID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3Njb3Jlcy1zdHJpcCcpOwogIGlmICghcCB8fCAoIXAuYXNmaWQgJiYgIXAucmV2b2kgJiYgcC5nYXAgPT0gbnVsbCkpIHsKICAgIHN0cmlwLmNsYXNzTmFtZSA9ICcnOyBzdHJpcC5pbm5lckhUTUwgPSAnJzsgcmV0dXJuOwogIH0KICBzdHJpcC5jbGFzc05hbWUgPSAndmlzaWJsZSc7CiAgbGV0IGh0bWwgPSAnJzsKICBpZiAocC5hc2ZpZCkgewogICAgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtZ3JvdXAiPjxzcGFuIGNsYXNzPSJzY29yZS1ncm91cC1sYWJlbCBlYWdsZSI+QVNGSUQ8L3NwYW4+JzsKICAgIFsnQScsJ1MnLCdGJywnSScsJ0QnXS5mb3JFYWNoKChkLCBpKSA9PiB7CiAgICAgIGNvbnN0IHBjdCA9IE1hdGgucm91bmQocC5hc2ZpZFtpXSAqIDEwMCk7CiAgICAgIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLW1pbmkiPicgKwogICAgICAgICc8c3BhbiBjbGFzcz0ic2NvcmUtbWluaS1sdHIiIHN0eWxlPSJjb2xvcjonICsgQVNGSURfQ09MT1JTW2ldICsgJyI+JyArIGQgKyAnPC9zcGFuPicgKwogICAgICAgICc8ZGl2IGNsYXNzPSJzY29yZS1taW5pLWJnIj48ZGl2IGNsYXNzPSJzY29yZS1taW5pLWZpbGwiIHN0eWxlPSJ3aWR0aDonICsgcGN0ICsKICAgICAgICAnJTtiYWNrZ3JvdW5kOicgKyBBU0ZJRF9DT0xPUlNbaV0gKyAnIj48L2Rpdj48L2Rpdj48L2Rpdj4nOwogICAgfSk7CiAgICBodG1sICs9ICc8L2Rpdj4nOwogIH0KICBpZiAocC5hc2ZpZCAmJiAocC5yZXZvaSB8fCBwLmdhcCAhPSBudWxsKSkgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtc2VwIj48L2Rpdj4nOwogIGlmIChwLnJldm9pKSB7CiAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1ncm91cCI+PHNwYW4gY2xhc3M9InNjb3JlLWdyb3VwLWxhYmVsIHNwaGlueCI+UkVWT0k8L3NwYW4+JzsKICAgIFsnUicsJ0UnLCdWJywnTycsJ0knXS5mb3JFYWNoKChkLCBpKSA9PiB7CiAgICAgIGNvbnN0IHBjdCA9IE1hdGgucm91bmQocC5yZXZvaVtpXSAqIDEwMCk7CiAgICAgIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLW1pbmkiPicgKwogICAgICAgICc8c3BhbiBjbGFzcz0ic2NvcmUtbWluaS1sdHIiIHN0eWxlPSJjb2xvcjonICsgUkVWT0lfQ09MT1JTW2ldICsgJyI+JyArIGQgKyAnPC9zcGFuPicgKwogICAgICAgICc8ZGl2IGNsYXNzPSJzY29yZS1taW5pLWJnIj48ZGl2IGNsYXNzPSJzY29yZS1taW5pLWZpbGwiIHN0eWxlPSJ3aWR0aDonICsgcGN0ICsKICAgICAgICAnJTtiYWNrZ3JvdW5kOicgKyBSRVZPSV9DT0xPUlNbaV0gKyAnIj48L2Rpdj48L2Rpdj48L2Rpdj4nOwogICAgfSk7CiAgICBodG1sICs9ICc8L2Rpdj4nOwogIH0KICBpZiAocC5yZXZvaSAmJiBwLmdhcCAhPSBudWxsKSBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1zZXAiPjwvZGl2Pic7CiAgaWYgKHAuZ2FwICE9IG51bGwpIHsKICAgIGh0bWwgKz0gJzxkaXYgY2xhc3M9ImdhcC1taW5pIj48c3BhbiBjbGFzcz0iZ2FwLW1pbmktbGJsIj4mZGVsdGE7PC9zcGFuPicgKwogICAgICAnPHNwYW4gY2xhc3M9ImdhcC1taW5pLXZhbCI+JyArIHAuZ2FwLnRvRml4ZWQoMykgKyAnPC9zcGFuPjwvZGl2Pic7CiAgfQogIHN0cmlwLmlubmVySFRNTCA9IGh0bWw7Cn0KCmZ1bmN0aW9uIHNob3dQbGFjZWhvbGRlcihtc2cpIHsKICBjb25zdCBsaW5lcyA9IG1zZy5zcGxpdCgnXG4nKTsKICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVhZG1lLWJvZHknKS5pbm5lckhUTUwgPQogICAgJzxkaXYgY2xhc3M9InJlYWRtZS1wbGFjZWhvbGRlciI+JyArCiAgICAnPHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSInICsKICAgICcgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgb3BhY2l0eT0iLjMiPicgKwogICAgJzxwYXRoIGQ9Ik0xNCAySDZhMiAyIDAgMCAwLTIgMnYxNmEyIDIgMCAwIDAgMiAyaDEyYTIgMiAwIDAgMCAyLTJWOHoiLz4nICsKICAgICc8cG9seWxpbmUgcG9pbnRzPSIxNCAyIDE0IDggMjAgOCIvPjwvc3ZnPicgKwogICAgJzxkaXYgY2xhc3M9InBoLXRpdGxlIj4nICsgZXNjKGxpbmVzWzBdKSArICc8L2Rpdj4nICsKICAgIGxpbmVzLnNsaWNlKDEpLmZpbHRlcihsID0+IGwudHJpbSgpKS5tYXAobCA9PgogICAgICAnPGRpdiBjbGFzcz0icGgtc3ViIj4nICsgZXNjKGwpICsgJzwvZGl2PicpLmpvaW4oJycpICsKICAgICc8L2Rpdj4nOwp9CgpmdW5jdGlvbiBwYXJzZU1hcmtkb3duKG1kKSB7CiAgbGV0IGggPSBlc2NNZChtZCk7CiAgaCA9IGgucmVwbGFjZSgvYGBgW1x3XSpcbihbXHNcU10qPylgYGAvZywKICAgIChfLCBjKSA9PiAnPHByZT48Y29kZT4nICsgYy50cmltRW5kKCkgKyAnPC9jb2RlPjwvcHJlPicpOwogIGggPSBoLnJlcGxhY2UoL14jezQsfVxzKyguKykkL2dtLCAnPGgzPiQxPC9oMz4nKTsKICBoID0gaC5yZXBsYWNlKC9eIyMjXHMrKC4rKSQvZ20sICAgJzxoMz4kMTwvaDM+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXiMjXHMrKC4rKSQvZ20sICAgICc8aDI+JDE8L2gyPicpOwogIGggPSBoLnJlcGxhY2UoL14jXHMrKC4rKSQvZ20sICAgICAnPGgxPiQxPC9oMT4nKTsKICBoID0gaC5yZXBsYWNlKC9eWy0qX117Myx9XHMqJC9nbSwgJzxocj4nKTsKICBoID0gaC5yZXBsYWNlKC9eJmd0O1xzKiguKykkL2dtLCAgJzxibG9ja3F1b3RlPiQxPC9ibG9ja3F1b3RlPicpOwogIGggPSBoLnJlcGxhY2UoLygoPzpeXHwuK1x8XG4/KSspL2dtLCBtID0+IHsKICAgIGNvbnN0IHJvd3MgPSBtLnRyaW0oKS5zcGxpdCgnXG4nKTsKICAgIGlmIChyb3dzLmxlbmd0aCA8IDIpIHJldHVybiBtOwogICAgbGV0IG91dCA9ICc8dGFibGU+JywgaW5Cb2R5ID0gZmFsc2U7CiAgICByb3dzLmZvckVhY2gocm93ID0+IHsKICAgICAgaWYgKC9eXHxbLXwgOl0rXHwkLy50ZXN0KHJvdy50cmltKCkpKSB7IG91dCArPSAnPHRib2R5Pic7IGluQm9keSA9IHRydWU7IHJldHVybjsgfQogICAgICBjb25zdCBjZWxscyA9IHJvdy5yZXBsYWNlKC9eXHx8XHwkL2csICcnKS5zcGxpdCgnfCcpOwogICAgICBjb25zdCB0YWcgPSBpbkJvZHkgPyAndGQnIDogJ3RoJzsKICAgICAgb3V0ICs9ICc8dHI+JyArIGNlbGxzLm1hcChjID0+ICc8JyArIHRhZyArICc+JyArIGMudHJpbSgpICsgJzwvJyArIHRhZyArICc+Jykuam9pbignJykgKyAnPC90cj4nOwogICAgfSk7CiAgICByZXR1cm4gb3V0ICsgKGluQm9keSA/ICc8L3Rib2R5PicgOiAnJykgKyAnPC90YWJsZT4nOwogIH0pOwogIGggPSBoLnJlcGxhY2UoL15bLSorXVxzKyguKykkL2dtLCAnPGxpPiQxPC9saT4nKTsKICBoID0gaC5yZXBsYWNlKC8oKD86PGxpPi4qPFwvbGk+XG4/KSspL2csICc8dWw+JDE8L3VsPicpOwogIGggPSBoLnJlcGxhY2UoL15cZCtcLlxzKyguKykkL2dtLCAnPGxpPiQxPC9saT4nKTsKICBoID0gaC5yZXBsYWNlKC9cKlwqKFteKl0rKVwqXCovZywgJzxzdHJvbmc+JDE8L3N0cm9uZz4nKTsKICBoID0gaC5yZXBsYWNlKC9cKihbXipdKylcKi9nLCAgICAgJzxlbT4kMTwvZW0+Jyk7CiAgaCA9IGgucmVwbGFjZSgvYChbXmBdKylgL2csICAgICAgICc8Y29kZT4kMTwvY29kZT4nKTsKICBoID0gaC5yZXBsYWNlKC9cWyhbXlxdXSspXF1cKChbXildKylcKS9nLAogICAgJzxhIGhyZWY9IiQyIiB0YXJnZXQ9Il9ibGFuayIgcmVsPSJub29wZW5lciI+JDE8L2E+Jyk7CiAgcmV0dXJuIGguc3BsaXQoL1xuezIsfS8pLm1hcChiID0+IHsKICAgIGNvbnN0IHQgPSBiLnRyaW0oKTsKICAgIGlmICghdCkgcmV0dXJuICcnOwogICAgaWYgKC9ePChoWzEtNl18dWx8b2x8cHJlfHRhYmxlfGJsb2NrcXVvdGV8aHIpLy50ZXN0KHQpKSByZXR1cm4gdDsKICAgIHJldHVybiAnPHA+JyArIHQucmVwbGFjZSgvXG4vZywgJzxicj4nKSArICc8L3A+JzsKICB9KS5qb2luKCdcbicpOwp9CgpmdW5jdGlvbiBlc2NNZChzKSB7CiAgcmV0dXJuIHMucmVwbGFjZSgvJi9nLCcmYW1wOycpLnJlcGxhY2UoLzwvZywnJmx0OycpCiAgICAgICAgICAucmVwbGFjZSgvPi9nLCcmZ3Q7JykucmVwbGFjZSgvIi9nLCcmcXVvdDsnKTsKfQpmdW5jdGlvbiBlc2MocykgewogIHJldHVybiBTdHJpbmcoc3x8JycpLnJlcGxhY2UoLyYvZywnJmFtcDsnKS5yZXBsYWNlKC88L2csJyZsdDsnKQogICAgLnJlcGxhY2UoLz4vZywnJmd0OycpLnJlcGxhY2UoLyIvZywnJnF1b3Q7Jyk7Cn0KCmZ1bmN0aW9uIGluaXRUcmVlTGlzdGVuZXJzKCkgewogIGNvbnN0IGxpc3QgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1saXN0Jyk7CiAgbGlzdC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIGUgPT4gewogICAgY29uc3QgaXRlbSA9IGUudGFyZ2V0LmNsb3Nlc3QoJy50cmVlLWl0ZW0nKTsKICAgIGlmIChpdGVtICYmICFpdGVtLmNsYXNzTGlzdC5jb250YWlucygnZmlsdGVyZWQnKSkgewogICAgICBzZWxlY3RQb2NsZXRFbGVtZW50KGl0ZW0pOwogICAgfQogIH0pOwogIGxpc3QuYWRkRXZlbnRMaXN0ZW5lcignZGJsY2xpY2snLCBlID0+IHsKICAgIGNvbnN0IGl0ZW0gPSBlLnRhcmdldC5jbG9zZXN0KCcudHJlZS1pdGVtJyk7CiAgICBpZiAoIWl0ZW0pIHJldHVybjsKICAgIGNvbnN0IHAgPSBQT0NMRVRTLmZpbmQoeCA9PiB4LmlkID09PSBpdGVtLmRhdGFzZXQuaWQpOwogICAgaWYgKCFwKSByZXR1cm47CiAgICBjb25zdCB1cmwgPSBCQVNFX1VSTCA/IEJBU0VfVVJMICsgJy8nICsgcC5odG1sUmVsUGF0aCA6IHAuaHRtbFJlbFBhdGg7CiAgICB3aW5kb3cub3Blbih1cmwsICdfYmxhbmsnKTsKICB9KTsKfQoKZnVuY3Rpb24gaW5pdEtleWJvYXJkKCkgewogIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBlID0+IHsKICAgIGNvbnN0IHZpc2libGVQb2NsZXRzID0gUE9DTEVUUy5maWx0ZXIocCA9PiB7CiAgICAgIGlmIChzZWxlY3RlZFRhZ3Muc2l6ZSA9PT0gMCkgcmV0dXJuIHRydWU7CiAgICAgIHJldHVybiBBcnJheS5mcm9tKHNlbGVjdGVkVGFncykuc29tZSh0YWcgPT4KICAgICAgICBwLmRvbWFpbiAmJiAoCiAgICAgICAgICBwLmRvbWFpbi50b0xvd2VyQ2FzZSgpLmluY2x1ZGVzKHRhZy50b0xvd2VyQ2FzZSgpKSB8fAogICAgICAgICAgdGFnLnRvTG93ZXJDYXNlKCkuaW5jbHVkZXMocC5kb21haW4udG9Mb3dlckNhc2UoKSkKICAgICAgICApCiAgICAgICk7CiAgICB9KTsKICAgIGNvbnN0IGlkeCA9IHZpc2libGVQb2NsZXRzLmZpbmRJbmRleChwID0+IHAuaWQgPT09IHNlbGVjdGVkSWQpOwogICAgaWYgKGUua2V5ID09PSAnQXJyb3dEb3duJykgewogICAgICBjb25zdCBuZXh0ID0gTWF0aC5taW4oaWR4ICsgMSwgdmlzaWJsZVBvY2xldHMubGVuZ3RoIC0gMSk7CiAgICAgIGlmICh2aXNpYmxlUG9jbGV0c1tuZXh0XSkgc2VsZWN0UG9jbGV0KHZpc2libGVQb2NsZXRzW25leHRdLmlkKTsKICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpOwogICAgfQogICAgaWYgKGUua2V5ID09PSAnQXJyb3dVcCcpIHsKICAgICAgY29uc3QgcHJldiA9IE1hdGgubWF4KGlkeCAtIDEsIDApOwogICAgICBpZiAodmlzaWJsZVBvY2xldHNbcHJldl0pIHNlbGVjdFBvY2xldCh2aXNpYmxlUG9jbGV0c1twcmV2XS5pZCk7CiAgICAgIGUucHJldmVudERlZmF1bHQoKTsKICAgIH0KICAgIGlmIChlLmtleSA9PT0gJ0VudGVyJykgewogICAgICBjb25zdCBwID0gUE9DTEVUUy5maW5kKHggPT4geC5pZCA9PT0gc2VsZWN0ZWRJZCk7CiAgICAgIGlmIChwKSB7IGNvbnN0IHVybCA9IEJBU0VfVVJMID8gQkFTRV9VUkwgKyAnLycgKyBwLmh0bWxSZWxQYXRoIDogcC5odG1sUmVsUGF0aDsgd2luZG93Lm9wZW4odXJsLCAnX2JsYW5rJyk7IH0KICAgIH0KICB9KTsKfQoKZnVuY3Rpb24gaW5pdFNwbGl0dGVyKCkgewogIGNvbnN0IHNwbGl0dGVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3NwbGl0dGVyJyk7CiAgY29uc3Qgc2hlbGwgICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2hlbGwnKTsKICBsZXQgZHJhZ2dpbmcgPSBmYWxzZSwgc3RhcnRYID0gMCwgc3RhcnRXID0gMDsKICBzcGxpdHRlci5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCBlID0+IHsKICAgIGRyYWdnaW5nID0gdHJ1ZTsgc3RhcnRYID0gZS5jbGllbnRYOwogICAgc3RhcnRXICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1wYW5lbCcpLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLndpZHRoOwogICAgc3BsaXR0ZXIuY2xhc3NMaXN0LmFkZCgnZHJhZ2dpbmcnKTsKICAgIGRvY3VtZW50LmJvZHkuc3R5bGUuY3NzVGV4dCA9ICdjdXJzb3I6Y29sLXJlc2l6ZTt1c2VyLXNlbGVjdDpub25lJzsKICAgIGUucHJldmVudERlZmF1bHQoKTsKICB9KTsKICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZW1vdmUnLCBlID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGNvbnN0IHcgPSBNYXRoLm1heCgxODAsIE1hdGgubWluKDY0MCwgc3RhcnRXICsgKGUuY2xpZW50WCAtIHN0YXJ0WCkpKTsKICAgIHNoZWxsLnN0eWxlLmdyaWRUZW1wbGF0ZUNvbHVtbnMgPSB3ICsgJ3B4IHZhcigtLXNwbGl0LXcpIDFmcic7CiAgfSk7CiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsICgpID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGRyYWdnaW5nID0gZmFsc2U7CiAgICBzcGxpdHRlci5jbGFzc0xpc3QucmVtb3ZlKCdkcmFnZ2luZycpOwogICAgZG9jdW1lbnQuYm9keS5zdHlsZS5jc3NUZXh0ID0gJyc7CiAgfSk7Cn0K';

// ── Main ──────────────────────────────────────────────────────────────────────
function main() {
  console.log('[TSCG] generate_index.js — Static Poclet Gallery Generator');
  console.log('  Root    :', ROOT, '(' + ROOT_SOURCE + ')');
  console.log('  Output  :', OUTPUT);
  console.log('  Site URL:', SITE_URL || '(not set — canonical & absolute JSON-LD URLs disabled)');
  console.log('  Scanning:', POCLETS_DIR);
  if (!fs.existsSync(POCLETS_DIR)) {
    console.error('[ERROR] instances/poclets/ not found at:', POCLETS_DIR);
    console.error('        Run from inside the repository, or use --root <repo-root>');
    process.exit(1);
  }

  const poclets = discoverPoclets();

  if (!poclets.length) {
    console.warn('[WARN] No poclets with static/*.html found — generating empty gallery.');
  } else {
    console.log('\n  Found ' + poclets.length + ' poclet(s) with static HTML:');
    poclets.forEach(p => {
      const scores = p.asfid ? ' | ASFID \u2713' : '';
      const gap    = p.gap != null ? ' | \u03b4=' + p.gap.toFixed(3) : '';
      console.log('    [' + (p.domain || '?') + '] ' + p.label + scores + gap);
      console.log('         \u2192 ' + p.htmlRelPath);
    });
  }

  // CLIENT_JS is embedded as a template literal at module scope
  const now         = new Date().toISOString().split('T')[0];
  // Decode CLIENT_JS from base64 (avoids ALL escaping/template issues)
  const clientJS = Buffer.from(_CLIENT_JS_B64, 'base64').toString('utf-8')
    .replace('DATA_PLACEHOLDER', () => JSON.stringify(poclets))
    .replace('DATE_PLACEHOLDER',     () => now)
    .replace('SITE_URL_PLACEHOLDER', () => JSON.stringify(SITE_URL));

  const htmlShell   = generateHtml(poclets);
  const scriptBlock = '\n<script>\n' + clientJS + '\n</script>\n</body>\n</html>';
  fs.writeFileSync(OUTPUT, htmlShell + scriptBlock, 'utf-8');

  const kb = (fs.statSync(OUTPUT).size / 1024).toFixed(1);
  console.log('\n  \u2713 Written: ' + OUTPUT + '  (' + kb + ' KB)');
  console.log('  \u2713 Done.\n');
}

main();


