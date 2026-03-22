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

    // M0_*.jsonld → metadata
    const jsonldFile = findFile(pocletDir, n =>
      n.startsWith('M0_') && n.endsWith('.jsonld'));
    const meta = jsonldFile ? parseJsonld(jsonldFile) : {};

    // *README*.md → prose
    const readmeFile = findFile(pocletDir, n =>
      /readme/i.test(n) && n.endsWith('.md'));
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
      label:   node['rdfs:label']      || '',
      domain:  node['m0:domain']       || '',
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
.logo{font-size:11px;font-weight:700;letter-spacing:.14em;color:var(--eagle);text-transform:uppercase;}
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
.tree-domain{font-size:10px;color:var(--border2);white-space:nowrap;flex-shrink:0;}

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
    <span class="logo">TSCG</span>
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

</div><!-- #shell -->
`;
}

const _CLIENT_JS_B64 = 'J3VzZSBzdHJpY3QnOwovLyDilIDilIAgRW1iZWRkZWQgZGF0YSDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIDilIAKY29uc3QgUE9DTEVUUyA9IERBVEFfUExBQ0VIT0xERVI7Ci8vIEdlbmVyYXRlZDogREFURV9QTEFDRUhPTERFUgoKY29uc3QgQVNGSURfQ09MT1JTID0gWyd2YXIoLS1jb2wtQSknLCd2YXIoLS1jb2wtUyknLCd2YXIoLS1jb2wtRiknLCd2YXIoLS1jb2wtSSknLCd2YXIoLS1jb2wtRCknXTsKY29uc3QgUkVWT0lfQ09MT1JTID0gWyd2YXIoLS1jb2wtUiknLCd2YXIoLS1jb2wtRSknLCd2YXIoLS1jb2wtViknLCd2YXIoLS1jb2wtTyknLCd2YXIoLS1jb2wtSW0pJ107CgpsZXQgc2VsZWN0ZWRJZCA9IG51bGw7Cgp3aW5kb3cuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsICgpID0+IHsKICByZW5kZXJUcmVlKCk7CiAgaW5pdFNwbGl0dGVyKCk7CiAgaW5pdEtleWJvYXJkKCk7CiAgaWYgKFBPQ0xFVFMubGVuZ3RoKSBzZWxlY3RQb2NsZXQoUE9DTEVUU1swXS5pZCk7Cn0pOwoKZnVuY3Rpb24gcmVuZGVyVHJlZSgpIHsKICBjb25zdCBsaXN0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3RyZWUtbGlzdCcpOwogIGNvbnN0IG4gICAgPSBQT0NMRVRTLmxlbmd0aDsKICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1jb3VudCcpLnRleHRDb250ZW50ID0gbjsKICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnaGRyLWNvdW50JykudGV4dENvbnRlbnQgID0KICAgIG4gKyAnIHNpbXVsYXRpb24nICsgKG4gIT09IDEgPyAncycgOiAnJyk7CiAgaWYgKCFuKSB7CiAgICBsaXN0LmlubmVySFRNTCA9CiAgICAgICc8ZGl2IHN0eWxlPSJwYWRkaW5nOjE2cHggMTJweDtmb250LXNpemU6MTFweDtjb2xvcjp2YXIoLS1tdXRlZCkiPk5vIHN0YXRpYyBzaW11bGF0aW9ucyBmb3VuZC48L2Rpdj4nOwogICAgcmV0dXJuOwogIH0KICBsaXN0LmlubmVySFRNTCA9IFBPQ0xFVFMubWFwKHAgPT4KICAgICc8ZGl2IGNsYXNzPSJ0cmVlLWl0ZW0iIGRhdGEtaWQ9IicgKyBlc2MocC5pZCkgKyAnIj4nICsKICAgICc8c3BhbiBjbGFzcz0idHJlZS1pY29uIj4mIzk2NTQ7PC9zcGFuPicgKwogICAgJzxzcGFuIGNsYXNzPSJ0cmVlLWxhYmVsIj4nICsgZXNjKHAubGFiZWwpICsgJzwvc3Bhbj4nICsKICAgIChwLmRvbWFpbiA/ICc8c3BhbiBjbGFzcz0idHJlZS1kb21haW4iPicgKyBlc2MocC5kb21haW4pICsgJzwvc3Bhbj4nIDogJycpICsKICAgICc8L2Rpdj4nCiAgKS5qb2luKCcnKTsKICBsaXN0LnF1ZXJ5U2VsZWN0b3JBbGwoJy50cmVlLWl0ZW0nKS5mb3JFYWNoKGVsID0+CiAgICBlbC5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsICgpID0+IHNlbGVjdFBvY2xldChlbC5kYXRhc2V0LmlkKSkpOwp9CgpmdW5jdGlvbiBzZWxlY3RQb2NsZXQoaWQpIHsKICBzZWxlY3RlZElkID0gaWQ7CiAgY29uc3QgcCAgICA9IFBPQ0xFVFMuZmluZCh4ID0+IHguaWQgPT09IGlkKTsKICBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCcudHJlZS1pdGVtJykuZm9yRWFjaChlbCA9PgogICAgZWwuY2xhc3NMaXN0LnRvZ2dsZSgnYWN0aXZlJywgZWwuZGF0YXNldC5pZCA9PT0gaWQpKTsKICBjb25zdCBuYW1lRWwgICA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZWFkbWUtcG9jbGV0LW5hbWUnKTsKICBjb25zdCBkb21haW5FbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZWFkbWUtZG9tYWluJyk7CiAgbmFtZUVsLnRleHRDb250ZW50ICAgPSBwID8gcC5sYWJlbCAgIDogJ1NlbGVjdCBhIHBvY2xldCc7CiAgbmFtZUVsLnN0eWxlLmNvbG9yICAgPSBwID8gJ3ZhcigtLXRleHQpJyA6ICd2YXIoLS1tdXRlZCknOwogIGRvbWFpbkVsLnRleHRDb250ZW50ID0gcCAmJiBwLmRvbWFpbiA/IHAuZG9tYWluIDogJyc7CiAgcmVuZGVyU2NvcmVzU3RyaXAocCk7CiAgY29uc3QgYnRuID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2xhdW5jaC1idG4nKTsKICBpZiAocCkgeyBidG4uaHJlZiA9IHAuaHRtbFJlbFBhdGg7IGJ0bi5jbGFzc0xpc3QucmVtb3ZlKCdoaWRkZW4nKTsgfQogIGVsc2UgICB7IGJ0bi5jbGFzc0xpc3QuYWRkKCdoaWRkZW4nKTsgfQogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdmb290ZXItaW5mbycpLnRleHRDb250ZW50ID0KICAgIHAgPyBwLmxhYmVsICsgKHAudmVyc2lvbiA/ICcgIHYnICsgcC52ZXJzaW9uIDogJycpIDogJyc7CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2Zvb3Rlci1wYXRoJykudGV4dENvbnRlbnQgPQogICAgcCA/IHAuaHRtbFJlbFBhdGggOiAnJzsKICBpZiAoIXApICAgICAgICAgICB7IHNob3dQbGFjZWhvbGRlcignTm8gcG9jbGV0IHNlbGVjdGVkJyk7IHJldHVybjsgfQogIGlmICghcC5oYXNSZWFkbWUpIHsgc2hvd1BsYWNlaG9sZGVyKHAubGFiZWwgKyAnXG5cbk5vIFJFQURNRSBmb3VuZC4nKTsgcmV0dXJuOyB9CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlYWRtZS1ib2R5JykuaW5uZXJIVE1MID0KICAgICc8ZGl2IGNsYXNzPSJyZWFkbWUtbWQiPicgKyBwYXJzZU1hcmtkb3duKHAucmVhZG1lKSArICc8L2Rpdj4nOwogIGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdyZWFkbWUtYm9keScpLnNjcm9sbFRvcCA9IDA7Cn0KCmZ1bmN0aW9uIHJlbmRlclNjb3Jlc1N0cmlwKHApIHsKICBjb25zdCBzdHJpcCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdzY29yZXMtc3RyaXAnKTsKICBpZiAoIXAgfHwgKCFwLmFzZmlkICYmICFwLnJldm9pICYmIHAuZ2FwID09IG51bGwpKSB7CiAgICBzdHJpcC5jbGFzc05hbWUgPSAnJzsgc3RyaXAuaW5uZXJIVE1MID0gJyc7IHJldHVybjsKICB9CiAgc3RyaXAuY2xhc3NOYW1lID0gJ3Zpc2libGUnOwogIGxldCBodG1sID0gJyc7CiAgaWYgKHAuYXNmaWQpIHsKICAgIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLWdyb3VwIj48c3BhbiBjbGFzcz0ic2NvcmUtZ3JvdXAtbGFiZWwgZWFnbGUiPkFTRklEPC9zcGFuPic7CiAgICBbJ0EnLCdTJywnRicsJ0knLCdEJ10uZm9yRWFjaCgoZCwgaSkgPT4gewogICAgICBjb25zdCBwY3QgPSBNYXRoLnJvdW5kKHAuYXNmaWRbaV0gKiAxMDApOwogICAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1taW5pIj4nICsKICAgICAgICAnPHNwYW4gY2xhc3M9InNjb3JlLW1pbmktbHRyIiBzdHlsZT0iY29sb3I6JyArIEFTRklEX0NPTE9SU1tpXSArICciPicgKyBkICsgJzwvc3Bhbj4nICsKICAgICAgICAnPGRpdiBjbGFzcz0ic2NvcmUtbWluaS1iZyI+PGRpdiBjbGFzcz0ic2NvcmUtbWluaS1maWxsIiBzdHlsZT0id2lkdGg6JyArIHBjdCArCiAgICAgICAgJyU7YmFja2dyb3VuZDonICsgQVNGSURfQ09MT1JTW2ldICsgJyI+PC9kaXY+PC9kaXY+PC9kaXY+JzsKICAgIH0pOwogICAgaHRtbCArPSAnPC9kaXY+JzsKICB9CiAgaWYgKHAuYXNmaWQgJiYgKHAucmV2b2kgfHwgcC5nYXAgIT0gbnVsbCkpIGh0bWwgKz0gJzxkaXYgY2xhc3M9InNjb3JlLXNlcCI+PC9kaXY+JzsKICBpZiAocC5yZXZvaSkgewogICAgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtZ3JvdXAiPjxzcGFuIGNsYXNzPSJzY29yZS1ncm91cC1sYWJlbCBzcGhpbngiPlJFVk9JPC9zcGFuPic7CiAgICBbJ1InLCdFJywnVicsJ08nLCdJJ10uZm9yRWFjaCgoZCwgaSkgPT4gewogICAgICBjb25zdCBwY3QgPSBNYXRoLnJvdW5kKHAucmV2b2lbaV0gKiAxMDApOwogICAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJzY29yZS1taW5pIj4nICsKICAgICAgICAnPHNwYW4gY2xhc3M9InNjb3JlLW1pbmktbHRyIiBzdHlsZT0iY29sb3I6JyArIFJFVk9JX0NPTE9SU1tpXSArICciPicgKyBkICsgJzwvc3Bhbj4nICsKICAgICAgICAnPGRpdiBjbGFzcz0ic2NvcmUtbWluaS1iZyI+PGRpdiBjbGFzcz0ic2NvcmUtbWluaS1maWxsIiBzdHlsZT0id2lkdGg6JyArIHBjdCArCiAgICAgICAgJyU7YmFja2dyb3VuZDonICsgUkVWT0lfQ09MT1JTW2ldICsgJyI+PC9kaXY+PC9kaXY+PC9kaXY+JzsKICAgIH0pOwogICAgaHRtbCArPSAnPC9kaXY+JzsKICB9CiAgaWYgKHAucmV2b2kgJiYgcC5nYXAgIT0gbnVsbCkgaHRtbCArPSAnPGRpdiBjbGFzcz0ic2NvcmUtc2VwIj48L2Rpdj4nOwogIGlmIChwLmdhcCAhPSBudWxsKSB7CiAgICBodG1sICs9ICc8ZGl2IGNsYXNzPSJnYXAtbWluaSI+PHNwYW4gY2xhc3M9ImdhcC1taW5pLWxibCI+JmRlbHRhOzwvc3Bhbj4nICsKICAgICAgJzxzcGFuIGNsYXNzPSJnYXAtbWluaS12YWwiPicgKyBwLmdhcC50b0ZpeGVkKDMpICsgJzwvc3Bhbj48L2Rpdj4nOwogIH0KICBzdHJpcC5pbm5lckhUTUwgPSBodG1sOwp9CgpmdW5jdGlvbiBzaG93UGxhY2Vob2xkZXIobXNnKSB7CiAgY29uc3QgbGluZXMgPSBtc2cuc3BsaXQoJ1xuJyk7CiAgZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlYWRtZS1ib2R5JykuaW5uZXJIVE1MID0KICAgICc8ZGl2IGNsYXNzPSJyZWFkbWUtcGxhY2Vob2xkZXIiPicgKwogICAgJzxzdmcgd2lkdGg9IjQ4IiBoZWlnaHQ9IjQ4IiB2aWV3Qm94PSIwIDAgMjQgMjQiIGZpbGw9Im5vbmUiJyArCiAgICAnIHN0cm9rZT0iY3VycmVudENvbG9yIiBzdHJva2Utd2lkdGg9IjEiIG9wYWNpdHk9Ii4zIj4nICsKICAgICc8cGF0aCBkPSJNMTQgMkg2YTIgMiAwIDAgMC0yIDJ2MTZhMiAyIDAgMCAwIDIgMmgxMmEyIDIgMCAwIDAgMi0yVjh6Ii8+JyArCiAgICAnPHBvbHlsaW5lIHBvaW50cz0iMTQgMiAxNCA4IDIwIDgiLz48L3N2Zz4nICsKICAgICc8ZGl2IGNsYXNzPSJwaC10aXRsZSI+JyArIGVzYyhsaW5lc1swXSkgKyAnPC9kaXY+JyArCiAgICBsaW5lcy5zbGljZSgxKS5maWx0ZXIobCA9PiBsLnRyaW0oKSkubWFwKGwgPT4KICAgICAgJzxkaXYgY2xhc3M9InBoLXN1YiI+JyArIGVzYyhsKSArICc8L2Rpdj4nKS5qb2luKCcnKSArCiAgICAnPC9kaXY+JzsKfQoKZnVuY3Rpb24gcGFyc2VNYXJrZG93bihtZCkgewogIGxldCBoID0gZXNjTWQobWQpOwogIGggPSBoLnJlcGxhY2UoL2BgYFtcd10qXG4oW1xzXFNdKj8pYGBgL2csCiAgICAoXywgYykgPT4gJzxwcmU+PGNvZGU+JyArIGMudHJpbUVuZCgpICsgJzwvY29kZT48L3ByZT4nKTsKICBoID0gaC5yZXBsYWNlKC9eI3s0LH1ccysoLispJC9nbSwgJzxoMz4kMTwvaDM+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXiMjI1xzKyguKykkL2dtLCAgICc8aDM+JDE8L2gzPicpOwogIGggPSBoLnJlcGxhY2UoL14jI1xzKyguKykkL2dtLCAgICAnPGgyPiQxPC9oMj4nKTsKICBoID0gaC5yZXBsYWNlKC9eI1xzKyguKykkL2dtLCAgICAgJzxoMT4kMTwvaDE+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXlstKl9dezMsfVxzKiQvZ20sICc8aHI+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXiZndDtccyooLispJC9nbSwgICc8YmxvY2txdW90ZT4kMTwvYmxvY2txdW90ZT4nKTsKICBoID0gaC5yZXBsYWNlKC8oKD86Xlx8LitcfFxuPykrKS9nbSwgbSA9PiB7CiAgICBjb25zdCByb3dzID0gbS50cmltKCkuc3BsaXQoJ1xuJyk7CiAgICBpZiAocm93cy5sZW5ndGggPCAyKSByZXR1cm4gbTsKICAgIGxldCBvdXQgPSAnPHRhYmxlPicsIGluQm9keSA9IGZhbHNlOwogICAgcm93cy5mb3JFYWNoKHJvdyA9PiB7CiAgICAgIGlmICgvXlx8Wy18IDpdK1x8JC8udGVzdChyb3cudHJpbSgpKSkgeyBvdXQgKz0gJzx0Ym9keT4nOyBpbkJvZHkgPSB0cnVlOyByZXR1cm47IH0KICAgICAgY29uc3QgY2VsbHMgPSByb3cucmVwbGFjZSgvXlx8fFx8JC9nLCAnJykuc3BsaXQoJ3wnKTsKICAgICAgY29uc3QgdGFnID0gaW5Cb2R5ID8gJ3RkJyA6ICd0aCc7CiAgICAgIG91dCArPSAnPHRyPicgKyBjZWxscy5tYXAoYyA9PiAnPCcgKyB0YWcgKyAnPicgKyBjLnRyaW0oKSArICc8LycgKyB0YWcgKyAnPicpLmpvaW4oJycpICsgJzwvdHI+JzsKICAgIH0pOwogICAgcmV0dXJuIG91dCArIChpbkJvZHkgPyAnPC90Ym9keT4nIDogJycpICsgJzwvdGFibGU+JzsKICB9KTsKICBoID0gaC5yZXBsYWNlKC9eWy0qK11ccysoLispJC9nbSwgJzxsaT4kMTwvbGk+Jyk7CiAgaCA9IGgucmVwbGFjZSgvKCg/OjxsaT4uKjxcL2xpPlxuPykrKS9nLCAnPHVsPiQxPC91bD4nKTsKICBoID0gaC5yZXBsYWNlKC9eXGQrXC5ccysoLispJC9nbSwgJzxsaT4kMTwvbGk+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXCpcKihbXipdKylcKlwqL2csICc8c3Ryb25nPiQxPC9zdHJvbmc+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXCooW14qXSspXCovZywgICAgICc8ZW0+JDE8L2VtPicpOwogIGggPSBoLnJlcGxhY2UoL2AoW15gXSspYC9nLCAgICAgICAnPGNvZGU+JDE8L2NvZGU+Jyk7CiAgaCA9IGgucmVwbGFjZSgvXFsoW15cXV0rKVxdXCgoW14pXSspXCkvZywKICAgICc8YSBocmVmPSIkMiIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIiPiQxPC9hPicpOwogIHJldHVybiBoLnNwbGl0KC9cbnsyLH0vKS5tYXAoYiA9PiB7CiAgICBjb25zdCB0ID0gYi50cmltKCk7CiAgICBpZiAoIXQpIHJldHVybiAnJzsKICAgIGlmICgvXjwoaFsxLTZdfHVsfG9sfHByZXx0YWJsZXxibG9ja3F1b3RlfGhyKS8udGVzdCh0KSkgcmV0dXJuIHQ7CiAgICByZXR1cm4gJzxwPicgKyB0LnJlcGxhY2UoL1xuL2csICc8YnI+JykgKyAnPC9wPic7CiAgfSkuam9pbignXG4nKTsKfQoKZnVuY3Rpb24gZXNjTWQocykgewogIHJldHVybiBzLnJlcGxhY2UoLyYvZywnJmFtcDsnKS5yZXBsYWNlKC88L2csJyZsdDsnKQogICAgICAgICAgLnJlcGxhY2UoLz4vZywnJmd0OycpLnJlcGxhY2UoLyIvZywnJnF1b3Q7Jyk7Cn0KZnVuY3Rpb24gZXNjKHMpIHsKICByZXR1cm4gU3RyaW5nKHN8fCcnKS5yZXBsYWNlKC8mL2csJyZhbXA7JykucmVwbGFjZSgvPC9nLCcmbHQ7JykKICAgIC5yZXBsYWNlKC8+L2csJyZndDsnKS5yZXBsYWNlKC8iL2csJyZxdW90OycpOwp9CgpmdW5jdGlvbiBpbml0S2V5Ym9hcmQoKSB7CiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIGUgPT4gewogICAgY29uc3QgaWR4ID0gUE9DTEVUUy5maW5kSW5kZXgocCA9PiBwLmlkID09PSBzZWxlY3RlZElkKTsKICAgIGlmIChlLmtleSA9PT0gJ0Fycm93RG93bicpIHsKICAgICAgY29uc3QgbmV4dCA9IE1hdGgubWluKGlkeCArIDEsIFBPQ0xFVFMubGVuZ3RoIC0gMSk7CiAgICAgIGlmIChQT0NMRVRTW25leHRdKSBzZWxlY3RQb2NsZXQoUE9DTEVUU1tuZXh0XS5pZCk7CiAgICAgIGUucHJldmVudERlZmF1bHQoKTsKICAgIH0KICAgIGlmIChlLmtleSA9PT0gJ0Fycm93VXAnKSB7CiAgICAgIGNvbnN0IHByZXYgPSBNYXRoLm1heChpZHggLSAxLCAwKTsKICAgICAgaWYgKFBPQ0xFVFNbcHJldl0pIHNlbGVjdFBvY2xldChQT0NMRVRTW3ByZXZdLmlkKTsKICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpOwogICAgfQogICAgaWYgKGUua2V5ID09PSAnRW50ZXInKSB7CiAgICAgIGNvbnN0IHAgPSBQT0NMRVRTLmZpbmQoeCA9PiB4LmlkID09PSBzZWxlY3RlZElkKTsKICAgICAgaWYgKHApIHdpbmRvdy5vcGVuKHAuaHRtbFJlbFBhdGgsICdfYmxhbmsnKTsKICAgIH0KICB9KTsKfQoKZnVuY3Rpb24gaW5pdFNwbGl0dGVyKCkgewogIGNvbnN0IHNwbGl0dGVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3NwbGl0dGVyJyk7CiAgY29uc3Qgc2hlbGwgICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgnc2hlbGwnKTsKICBsZXQgZHJhZ2dpbmcgPSBmYWxzZSwgc3RhcnRYID0gMCwgc3RhcnRXID0gMDsKICBzcGxpdHRlci5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCBlID0+IHsKICAgIGRyYWdnaW5nID0gdHJ1ZTsgc3RhcnRYID0gZS5jbGllbnRYOwogICAgc3RhcnRXICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgndHJlZS1wYW5lbCcpLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLndpZHRoOwogICAgc3BsaXR0ZXIuY2xhc3NMaXN0LmFkZCgnZHJhZ2dpbmcnKTsKICAgIGRvY3VtZW50LmJvZHkuc3R5bGUuY3NzVGV4dCA9ICdjdXJzb3I6Y29sLXJlc2l6ZTt1c2VyLXNlbGVjdDpub25lJzsKICAgIGUucHJldmVudERlZmF1bHQoKTsKICB9KTsKICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZW1vdmUnLCBlID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGNvbnN0IHcgPSBNYXRoLm1heCgxNjAsIE1hdGgubWluKDUyMCwgc3RhcnRXICsgKGUuY2xpZW50WCAtIHN0YXJ0WCkpKTsKICAgIHNoZWxsLnN0eWxlLmdyaWRUZW1wbGF0ZUNvbHVtbnMgPSB3ICsgJ3B4IHZhcigtLXNwbGl0LXcpIDFmcic7CiAgfSk7CiAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignbW91c2V1cCcsICgpID0+IHsKICAgIGlmICghZHJhZ2dpbmcpIHJldHVybjsKICAgIGRyYWdnaW5nID0gZmFsc2U7CiAgICBzcGxpdHRlci5jbGFzc0xpc3QucmVtb3ZlKCdkcmFnZ2luZycpOwogICAgZG9jdW1lbnQuYm9keS5zdHlsZS5jc3NUZXh0ID0gJyc7CiAgfSk7Cn0=';

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
    .replace('DATE_PLACEHOLDER', () => now);

  const htmlShell   = generateHtml(poclets);
  const scriptBlock = '\n<script>\n' + clientJS + '\n</script>\n</body>\n</html>';
  fs.writeFileSync(OUTPUT, htmlShell + scriptBlock, 'utf-8');

  const kb = (fs.statSync(OUTPUT).size / 1024).toFixed(1);
  console.log('\n  \u2713 Written: ' + OUTPUT + '  (' + kb + ' KB)');
  console.log('  \u2713 Done.\n');
}

main();


