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
#header{grid-area:header;display:flex;align-items:center;gap:12px;padding:0 16px;
  background:var(--bg-panel);border-bottom:1px solid var(--border);}
.logo{font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--eagle);text-transform:uppercase;cursor:pointer;background:none;border:none;padding:0;font-family:var(--font);}
.title{font-size:14px;font-weight:600;flex:1;}
.chip{padding:2px 8px;border-radius:20px;font-size:11px;font-weight:500;border:1px solid transparent;}
.chip-count{background:rgba(86,211,100,.12);border-color:rgba(86,211,100,.3);color:var(--accent);}
.chip-date {background:rgba(121,192,255,.12);border-color:rgba(121,192,255,.3);color:var(--sphinx);}

/* ── Tree panel ─────────────────────────────────────────────────────── */
#tree-panel{grid-area:tree;display:flex;flex-direction:column;
  background:var(--bg-panel);border-right:1px solid var(--border);
  overflow:hidden;min-width:160px;}
#tree-header{display:flex;justify-content:space-between;align-items:center;
  padding:8px 12px;font-size:11px;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);
  border-bottom:1px solid var(--border);flex-shrink:0;}
#tree-count{font-weight:400;color:var(--border2);}
#tree-list{overflow-y:auto;flex:1;}
.tree-item{display:flex;align-items:center;gap:8px;padding:7px 12px;
  cursor:pointer;border-left:3px solid transparent;
  transition:background .12s,border-color .12s;}
.tree-item:hover{background:var(--bg-hover);}
.tree-item.active{background:rgba(121,192,255,.08);border-left-color:var(--sphinx);}
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
    <div id="tree-header">
      Poclets <span id="tree-count">0</span>
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
  transform:translateX(-50%);
">TSCG Github repository</div>
<script>
(function(){
  const btn = document.getElementById('tscg-logo-btn');
  const tip = document.getElementById('tscg-tip');
  if (!btn || !tip) return;
  btn.addEventListener('mouseenter', function() {
    const r = btn.getBoundingClientRect();
    tip.style.left = (r.left + r.width / 2) + 'px';
    tip.style.top  = (r.bottom + 6) + 'px';
    tip.style.opacity = '1';
  });
  btn.addEventListener('mouseleave', function() { tip.style.opacity = '0'; });
})();
</script>

</div><!-- #shell -->
`;
}

const _CLIENT_JS_B64 = 'J3VzZSBzdHJpY3QnOwovLyDilIDilIAgRW1iZWRkZWQgZGF0YSDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIAKY29uc3QgUE9DTEVUUyA9IERBVEFfUExBQ0VIT0xERVI7CmNvbnN0IEJBU0VfVVJMID0gU0lURV9VUkxfUExBQ0VIT0xERVI7Ci8vIEdlbmVyYXRlZDogREFURV9QTEFDRUhPTERFUgoKY29uc3QgQVNGSURfQ09MT1JTID0gWyd2YXIoLS1jb2wtQSknLCd2YXIoLS1jb2wtUyknLCd2YXIoLS1jb2wtRiknLCd2YXIoLS1jb2wtSSknLCd2YXIoLS1jb2wtRCknXTsKY29uc3QgUkVWT0lfQ09MT1JTID0gWyd2YXIoLS1jb2wtUiknLCd2YXIoLS1jb2wtRSknLCd2YXIoLS1jb2wtViknLCd2YXIoLS1jb2wtTyknLCd2YXIoLS1jb2wtSW0pJ107CgpsZXQgc2VsZWN0ZWRJZCA9IG51bGw7Cgp3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHsKICByZW5kZXJUcmVlKCk7CiAgaW5pdFRyZWVMaXN0ZW5lcnMoKTsKICBpbml0U3BsaXR0ZXIoKTsKICBpbml0S2V5Ym9hcmQoKTsKICBpZiAoUE9DTEVUUy5sZW5ndGgpIHNlbGVjdFBvY2xldChQT0NMRVRTWzBdLmlkKTsKfSk7CgpmdW5jdGlvbiByZW5kZXJUcmVlKCkgewogIGNvbnN0IGxpc3QgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1saXN0Jyk7CiAgY29uc3QgbiAgICA9IFBPQ0xFVFMubGVuZ3RoOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd0cmVlLWNvdW50JykudGV4dENvbnRlbnQgPSBuOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdoZHItY291bnQnKS50ZXh0Q29udGVudCAgPQogICAgbiArICcgc2ltdWxhdGlvbicgKyAobiAhPT0gMSA/ICdzJyA6ICcnKTsKICBpZiAoIW4pIHsKICAgIGxpc3QuaW5uZXJIVE1MID0KICAgICAgJzxkaXYgc3R5bGU9InBhZGRpbmc6MTZweCAxMnB4O2ZvbnQtc2l6ZToxMXB4O2NvbG9yOnZhcigtLW11dGVkKSI+Tm8gc3RhdGljIHNpbXVsYXRpb25zIGZvdW5kLjwvZGl2Pic7CiAgICByZXR1cm47CiAgfQogIGxpc3QuaW5uZXJIVE1MID0gUE9DTEVUUy5tYXAocCA9PgogICAgJzxkaXYgY2xhc3M9InRyZWUtaXRlbSIgZGF0YS1pZD0iJyArIGVzYyhwLmlkKSArICciJyArCiAgICAocC5kb21haW4gPyAnIHRpdGxlPSInICsgZXNjKHAuZG9tYWluKSArICciJyA6ICcnKSArCiAgICAnIHN0eWxlPSJjdXJzb3I6cG9pbnRlciI+JyArCiAgICAnPHNwYW4gY2xhc3M9InRyZWUtaWNvbiI+JiM5NjU0Ozwvc3Bhbj4nICsKICAgICc8c3BhbiBjbGFzcz0idHJlZS1sYWJlbCI+JyArIGVzYyhwLmxhYmVsKSArICc8L3NwYW4+JyArCiAgICAnPC9kaXY+JwogICkuam9pbignJyk7CiAgbGlzdC5xdWVyeVNlbGVjdG9yQWxsKCcudHJlZS1pdGVtJykuZm9yRWFjaChlbCA9PgogICAgZWwuYWRkRXZlbnRMaXN0ZW5lcignY2xpY2snLCAoKSA9PiBzZWxlY3RQb2NsZXQoZWwuZGF0YXNldC5pZCkpKTsKfQoKZnVuY3Rpb24gc2VsZWN0UG9jbGV0KGlkKSB7CiAgc2VsZWN0ZWRJZCA9IGlkOwogIGNvbnN0IHAgICAgPSBQT0NMRVRTLmZpbmQoeCA9PiB4LmlkID09PSBpZCk7CiAgZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbCgnLnRyZWUtaXRlbScpLmZvckVhY2goZWwgPT4KICAgIGVsLmNsYXNzTGlzdC50b2dnbGUoJ2FjdGl2ZScsIGVsLmRhdGFzZXQuaWQgPT09IGlkKSk7CiAgY29uc3QgbmFtZUVsICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVhZG1lLXBvY2xldC1uYW1lJyk7CiAgY29uc3QgZG9tYWluRWwgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVhZG1lLWRvbWFpbicpOwogIG5hbWVFbC50ZXh0Q29udGVudCAgID0gcCA/IHAubGFiZWwgICA6ICdTZWxlY3QgYSBwb2NsZXQnOwogIG5hbWVFbC5zdHlsZS5jb2xvciAgID0gcCA/ICd2YXIoLS10ZXh0KScgOiAndmFyKC0tbXV0ZWQpJzsKICBkb21haW5FbC50ZXh0Q29udGVudCA9IHAgJiYgcC5kb21haW4gPyBwLmRvbWFpbiA6ICcnOwogIHJlbmRlclNjb3Jlc1N0cmlwKHApOwogIGNvbnN0IGJ0biA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdsYXVuY2gtYnRuJyk7CiAgaWYgKHApIHsgYnRuLmhyZWYgPSBCQVNFX1VSTCA/IEJBU0VfVVJMICsgJy8nICsgcC5odG1sUmVsUGF0aCA6IHAuaHRtbFJlbFBhdGg7IGJ0bi5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTsgfQogIGVsc2UgICB7IGJ0bi5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTsgfQogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdmb290ZXItaW5mbycpLnRleHRDb250ZW50ID0KICAgIHAgPyBwLmxhYmVsICsgKHAudmVyc2lvbiA/ICcgIHYnICsgcC52ZXJzaW9uIDogJycpIDogJyc7CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2Zvb3Rlci1wYXRoJykudGV4dENvbnRlbnQgPQogICAgcCA/IChCQVNFX1VSTCA/IEJBU0VfVVJMICsgJy8nICsgcC5odG1sUmVsUGF0aCA6IHAuaHRtbFJlbFBhdGgpIDogJyc7CiAgaWYgKCFwKSAgICAgICAgICAgeyBzaG93UGxhY2Vob2xkZXIoJ05vIHBvY2xldCBzZWxlY3RlZCcpOyByZXR1cm47IH0KICBpZiAoIXAuaGFzUmVhZG1lKSB7IHNob3dQbGFjZWhvbGRlcihwLmxhYmVsICsgJ1xuXG5ObyBSRUFETUUgZm91bmQuJyk7IHJldHVybjsgfQogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZWFkbWUtYm9keScpLmlubmVySFRNTCA9CiAgICAnPGRpdiBjbGFzcz0icmVhZG1lLW1kIj4nICsgcGFyc2VNYXJrZG93bihwLnJlYWRtZSkgKyAnPC9kaXY+JzsKICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgncmVhZG1lLWJvZHknKS5zY3JvbGxUb3AgPSAwOwp9CgpmdW5jdGlvbiByZW5kZXJTY29yZXNTdHJpcChwKSB7CiAgY29uc3Qgc3RyaXAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2NvcmVzLXN0cmlwJyk7CiAgaWYgKCFwIHx8ICghcC5hc2ZpZCAmJiAhcC5yZXZvaSAmJiBwLmdhcCA9PSBudWxsKSkgewogICAgc3RyaXAuY2xhc3NOYW1lID0gJyc7IHN0cmlwLmlubmVySFRNTCA9ICcnOyByZXR1cm47CiAgfQogIHN0cmlwLmNsYXNzTmFtZSA9ICd2aXNpYmxlJzsKICBsZXQgaHRtbCA9ICcnOwogIGlmIChwLmFzZmlkKSB7CiAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1ncm91cCI+PHNwYW4gY2xhc3M9InNjb3JlLWdyb3VwLWxhYmVsIGVhZ2xlIj5BU0ZJRDwvc3Bhbj4nOwogICAgWydBJywnUycsJ0YnLCdJJywnRCddLmZvckVhY2goKGQsIGkpID0+IHsKICAgICAgY29uc3QgcGN0ID0gTWF0aC5yb3VuZChwLmFzZmlkW2ldICogMTAwKTsKICAgICAgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtbWluaSI+JyArCiAgICAgICAgJzxzcGFuIGNsYXNzPSJzY29yZS1taW5pLWx0ciIgc3R5bGU9ImNvbG9yOicgKyBBU0ZJRF9DT0xPUlNbaV0gKyAnIj4nICsgZCArICc8L3NwYW4+JyArCiAgICAgICAgJzxkaXYgY2xhc3M9InNjb3JlLW1pbmktYmciPjxkaXYgY2xhc3M9InNjb3JlLW1pbmktZmlsbCIgc3R5bGU9IndpZHRoOicgKyBwY3QgKwogICAgICAgICclO2JhY2tncm91bmQ6JyArIEFTRklEX0NPTE9SU1tpXSArICciPjwvZGl2PjwvZGl2PjwvZGl2Pic7CiAgICB9KTsKICAgIGh0bWwgKz0gJzwvZGl2Pic7CiAgfQogIGlmIChwLmFzZmlkICYmIChwLnJldm9pIHx8IHAuZ2FwICE9IG51bGwpKSBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1zZXAiPjwvZGl2Pic7CiAgaWYgKHAucmV2b2kpIHsKICAgIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLWdyb3VwIj48c3BhbiBjbGFzcz0ic2NvcmUtZ3JvdXAtbGFiZWwgc3BoaW54Ij5SRVZPSTwvc3Bhbj4nOwogICAgWydSJywnRScsJ1YnLCdPJywnSSddLmZvckVhY2goKGQsIGkpID0+IHsKICAgICAgY29uc3QgcGN0ID0gTWF0aC5yb3VuZChwLnJldm9pW2ldICogMTAwKTsKICAgICAgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtbWluaSI+JyArCiAgICAgICAgJzxzcGFuIGNsYXNzPSJzY29yZS1taW5pLWx0ciIgc3R5bGU9ImNvbG9yOicgKyBSRVZPSV9DT0xPUlNbaV0gKyAnIj4nICsgZCArICc8L3NwYW4+JyArCiAgICAgICAgJzxkaXYgY2xhc3M9InNjb3JlLW1pbmktYmciPjxkaXYgY2xhc3M9InNjb3JlLW1pbmktZmlsbCIgc3R5bGU9IndpZHRoOicgKyBwY3QgKwogICAgICAgICclO2JhY2tncm91bmQ6JyArIFJFVk9JX0NPTE9SU1tpXSArICciPjwvZGl2PjwvZGl2PjwvZGl2Pic7CiAgICB9KTsKICAgIGh0bWwgKz0gJzwvZGl2Pic7CiAgfQogIGlmIChwLnJldm9pICYmIHAuZ2FwICE9IG51bGwpIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLXNlcCI+PC9kaXY+JzsKICBpZiAocC5nYXAgIT0gbnVsbCkgewogICAgaHRtbCArPSAnPGRpdiBjbGFzcz0iZ2FwLW1pbmkiPjxzcGFuIGNsYXNzPSJnYXAtbWluaS1sYmwiPiZkZWx0YTs8L3NwYW4+JyArCiAgICAgICc8c3BhbiBjbGFzcz0iZ2FwLW1pbmktdmFsIj4nICsgcC5nYXAudG9GaXhlZCgzKSArICc8L3NwYW4+PC9kaXY+JzsKICB9CiAgc3RyaXAuaW5uZXJIVE1MID0gaHRtbDsKfQoKZnVuY3Rpb24gc2hvd1BsYWNlaG9sZGVyKG1zZykgewogIGNvbnN0IGxpbmVzID0gbXNnLnNwbGl0KCdcbicpOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZWFkbWUtYm9keScpLmlubmVySFRNTCA9CiAgICAnPGRpdiBjbGFzcz0icmVhZG1lLXBsYWNlaG9sZGVyIj4nICsKICAgICc8c3ZnIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIicgKwogICAgJyBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxIiBvcGFjaXR5PSIuMyI+JyArCiAgICAnPHBhdGggZD0iTTE0IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY4eiIvPicgKwogICAgJzxwb2x5bGluZSBwb2ludHM9IjE0IDIgMTQgOCAyMCA4Ii8+PC9zdmc+JyArCiAgICAnPGRpdiBjbGFzcz0icGgtdGl0bGUiPicgKyBlc2MobGluZXNbMF0pICsgJzwvZGl2PicgKwogICAgbGluZXMuc2xpY2UoMSkuZmlsdGVyKGwgPT4gbC50cmltKCkpLm1hcChsID0+CiAgICAgICc8ZGl2IGNsYXNzPSJwaC1zdWIiPicgKyBlc2MobCkgKyAnPC9kaXY+Jykuam9pbignJykgKwogICAgJzwvZGl2Pic7Cn0KCmZ1bmN0aW9uIHBhcnNlTWFya2Rvd24obWQpIHsKICBsZXQgaCA9IGVzY01kKG1kKTsKICBoID0gaC5yZXBsYWNlKC9gYGBbXHddKlxuKFtcc1xTXSo/KWBgYC9nLAogICAgKF8sIGMpID0+ICc8cHJlPjxjb2RlPicgKyBjLnRyaW1FbmQoKSArICc8L2NvZGU+PC9wcmU+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXiN7NCx9XHMrKC4rKSQvZ20sICc8aDM+JDE8L2gzPicpOwogIGggPSBoLnJlcGxhY2UoL14jIyNccysoLispJC9nbSwgICAnPGgzPiQxPC9oMz4nKTsKICBoID0gaC5yZXBsYWNlKC9eIyNccysoLispJC9nbSwgICAgJzxoMj4kMTwvaDI+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXiNccysoLispJC9nbSwgICAgICc8aDE+JDE8L2gxPicpOwogIGggPSBoLnJlcGxhY2UoL15bLSpfXXszLH1ccyokL2dtLCAnPGhyPicpOwogIGggPSBoLnJlcGxhY2UoL14mZ3Q7XHMqKC4rKSQvZ20sICAnPGJsb2NrcXVvdGU+JDE8L2Jsb2NrcXVvdGU+Jyk7CiAgaCA9IGgucmVwbGFjZSgvKCg/Ol5cfC4rXHxcbj8pKykvZ20sIG0gPT4gewogICAgY29uc3Qgcm93cyA9IG0udHJpbSgpLnNwbGl0KCdcbicpOwogICAgaWYgKHJvd3MubGVuZ3RoIDwgMikgcmV0dXJuIG07CiAgICBsZXQgb3V0ID0gJzx0YWJsZT4nLCBpbkJvZHkgPSBmYWxzZTsKICAgIHJvd3MuZm9yRWFjaChyb3cgPT4gewogICAgICBpZiAoL15cfFstfCA6XStcfCQvLnRlc3Qocm93LnRyaW0oKSkpIHsgb3V0ICs9ICc8dGJvZHk+JzsgaW5Cb2R5ID0gdHJ1ZTsgcmV0dXJuOyB9CiAgICAgIGNvbnN0IGNlbGxzID0gcm93LnJlcGxhY2UoL15cfHxcfCQvZywgJycpLnNwbGl0KCd8Jyk7CiAgICAgIGNvbnN0IHRhZyA9IGluQm9keSA/ICd0ZCcgOiAndGgnOwogICAgICBvdXQgKz0gJzx0cj4nICsgY2VsbHMubWFwKGMgPT4gJzwnICsgdGFnICsgJz4nICsgYy50cmltKCkgKyAnPC8nICsgdGFnICsgJz4nKS5qb2luKCcnKSArICc8L3RyPic7CiAgICB9KTsKICAgIHJldHVybiBvdXQgKyAoaW5Cb2R5ID8gJzwvdGJvZHk+JyA6ICcnKSArICc8L3RhYmxlPic7CiAgfSk7CiAgaCA9IGgucmVwbGFjZSgvXlstKitdXHMrKC4rKSQvZ20sICc8bGk+JDE8L2xpPicpOwogIGggPSBoLnJlcGxhY2UoLygoPzo8bGk+Lio8XC9saT5cbj8pKykvZywgJzx1bD4kMTwvdWw+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXlxkK1wuXHMrKC4rKSQvZ20sICc8bGk+JDE8L2xpPicpOwogIGggPSBoLnJlcGxhY2UoL1wqXCooW14qXSspXCpcKi9nLCAnPHN0cm9uZz4kMTwvc3Ryb25nPicpOwogIGggPSBoLnJlcGxhY2UoL1wqKFteKl0rKVwqL2csICAgICAnPGVtPiQxPC9lbT4nKTsKICBoID0gaC5yZXBsYWNlKC9gKFteYF0rKWAvZywgICAgICAgJzxjb2RlPiQxPC9jb2RlPicpOwogIGggPSBoLnJlcGxhY2UoL1xbKFteXF1dKylcXVwoKFteKV0rKVwpL2csCiAgICAnPGEgaHJlZj0iJDIiIHRhcmdldD0iX2JsYW5rIiByZWw9Im5vb3BlbmVyIj4kMTwvYT4nKTsKICByZXR1cm4gaC5zcGxpdCgvXG57Mix9LykubWFwKGIgPT4gewogICAgY29uc3QgdCA9IGIudHJpbSgpOwogICAgaWYgKCF0KSByZXR1cm4gJyc7CiAgICBpZiAoL148KGhbMS02XXx1bHxvbHxwcmV8dGFibGV8YmxvY2txdW90ZXxocikvLnRlc3QodCkpIHJldHVybiB0OwogICAgcmV0dXJuICc8cD4nICsgdC5yZXBsYWNlKC9cbi9nLCAnPGJyPicpICsgJzwvcD4nOwogIH0pLmpvaW4oJ1xuJyk7Cn0KCmZ1bmN0aW9uIGVzY01kKHMpIHsKICByZXR1cm4gcy5yZXBsYWNlKC8mL2csJyZhbXA7JykucmVwbGFjZSgvPC9nLCcmbHQ7JykKICAgICAgICAgIC5yZXBsYWNlKC8+L2csJyZndDsnKS5yZXBsYWNlKC8iL2csJyZxdW90OycpOwp9CmZ1bmN0aW9uIGVzYyhzKSB7CiAgcmV0dXJuIFN0cmluZyhzfHwnJykucmVwbGFjZSgvJi9nLCcmYW1wOycpLnJlcGxhY2UoLzwvZywnJmx0OycpCiAgICAucmVwbGFjZSgvPi9nLCcmZ3Q7JykucmVwbGFjZSgvIi9nLCcmcXVvdDsnKTsKfQoKZnVuY3Rpb24gaW5pdFRyZWVMaXN0ZW5lcnMoKSB7CiAgY29uc3QgbGlzdCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd0cmVlLWxpc3QnKTsKICBsaXN0LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgZSA9PiB7CiAgICBjb25zdCBpdGVtID0gZS50YXJnZXQuY2xvc2VzdCgnLnRyZWUtaXRlbScpOwogICAgaWYgKGl0ZW0pIHNlbGVjdFBvY2xldChpdGVtLmRhdGFzZXQuaWQpOwogIH0pOwogIGxpc3QuYWRkRXZlbnRMaXN0ZW5lcignZGJsY2xpY2snLCBlID0+IHsKICAgIGNvbnN0IGl0ZW0gPSBlLnRhcmdldC5jbG9zZXN0KCcudHJlZS1pdGVtJyk7CiAgICBpZiAoIWl0ZW0pIHJldHVybjsKICAgIGNvbnN0IHAgPSBQT0NMRVRTLmZpbmQoeCA9PiB4LmlkID09PSBpdGVtLmRhdGFzZXQuaWQpOwogICAgaWYgKCFwKSByZXR1cm47CiAgICBjb25zdCB1cmwgPSBCQVNFX1VSTCA/IEJBU0VfVVJMICsgJy8nICsgcC5odG1sUmVsUGF0aCA6IHAuaHRtbFJlbFBhdGg7CiAgICB3aW5kb3cub3Blbih1cmwsICdfYmxhbmsnKTsKICB9KTsKfQoKZnVuY3Rpb24gaW5pdEtleWJvYXJkKCkgewogIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCBlID0+IHsKICAgIGNvbnN0IGlkeCA9IFBPQ0xFVFMuZmluZEluZGV4KHAgPT4gcC5pZCA9PT0gc2VsZWN0ZWRJZCk7CiAgICBpZiAoZS5rZXkgPT09ICdBcnJvd0Rvd24nKSB7CiAgICAgIGNvbnN0IG5leHQgPSBNYXRoLm1pbihpZHggKyAxLCBQT0NMRVRTLmxlbmd0aCAtIDEpOwogICAgICBpZiAoUE9DTEVUU1tuZXh0XSkgc2VsZWN0UG9jbGV0KFBPQ0xFVFNbbmV4dF0uaWQpOwogICAgICBlLnByZXZlbnREZWZhdWx0KCk7CiAgICB9CiAgICBpZiAoZS5rZXkgPT09ICdBcnJvd1VwJykgewogICAgICBjb25zdCBwcmV2ID0gTWF0aC5tYXgoaWR4IC0gMSwgMCk7CiAgICAgIGlmIChQT0NMRVRTW3ByZXZdKSBzZWxlY3RQb2NsZXQoUE9DTEVUU1twcmV2XS5pZCk7CiAgICAgIGUucHJldmVudERlZmF1bHQoKTsKICAgIH0KICAgIGlmIChlLmtleSA9PT0gJ0VudGVyJykgewogICAgICBjb25zdCBwID0gUE9DTEVUUy5maW5kKHggPT4geC5pZCA9PT0gc2VsZWN0ZWRJZCk7CiAgICAgIGlmIChwKSB7IGNvbnN0IHVybCA9IEJBU0VfVVJMID8gQkFTRV9VUkwgKyAnLycgKyBwLmh0bWxSZWxQYXRoIDogcC5odG1sUmVsUGF0aDsgd2luZG93Lm9wZW4odXJsLCAnX2JsYW5rJyk7IH0KICAgIH0KICB9KTsKfQoKZnVuY3Rpb24gaW5pdFNwbGl0dGVyKCkgewogIGNvbnN0IHNwbGl0dGVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3NwbGl0dGVyJyk7CiAgY29uc3Qgc2hlbGwgICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2hlbGwnKTsKICBsZXQgZHJhZ2dpbmcgPSBmYWxzZSwgc3RhcnRYID0gMCwgc3RhcnRXID0gMDsKICBzcGxpdHRlci5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCBlID0+IHsKICAgIGRyYWdnaW5nID0gdHJ1ZTsgc3RhcnRYID0gZS5jbGllbnRYOwogICAgc3RhcnRXICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1wYW5lbCcpLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLndpZHRoOwogICAgc3BsaXR0ZXIuY2xhc3NMaXN0LmFkZCgnZHJhZ2dpbmcnKTsKICAgIGRvY3VtZW50LmJvZHkuc3R5bGUuY3NzVGV4dCA9ICdjdXJzb3I6Y29sLXJlc2l6ZTt1c2VyLXNlbGVjdDpub25lJzsKICAgIGUucHJldmVudERlZmF1bHQoKTsKICB9KTsKICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZW1vdmUnLCBlID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGNvbnN0IHcgPSBNYXRoLm1heCgxNjAsIE1hdGgubWluKDUyMCwgc3RhcnRXICsgKGUuY2xpZW50WCAtIHN0YXJ0WCkpKTsKICAgIHNoZWxsLnN0eWxlLmdyaWRUZW1wbGF0ZUNvbHVtbnMgPSB3ICsgJ3B4IHZhcigtLXNwbGl0LXcpIDFmcic7CiAgfSk7CiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsICgpID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGRyYWdnaW5nID0gZmFsc2U7CiAgICBzcGxpdHRlci5jbGFzc0xpc3QucmVtb3ZlKCdkcmFnZ2luZycpOwogICAgZG9jdW1lbnQuYm9keS5zdHlsZS5jc3NUZXh0ID0gJyc7CiAgfSk7Cn0=';

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


