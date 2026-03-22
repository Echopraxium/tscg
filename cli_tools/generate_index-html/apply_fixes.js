/**
 * apply_fixes.js — TSCG one-shot patch script
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Run ONCE from the repo root:  node apply_fixes.js
 *
 * Fixes ALL M0_*.html simulation files found in instances/poclets/:
 *   1. CSP: adds 'unsafe-eval' to script-src
 *   2. Home button: replaces old unicode/button with white SVG <a>
 *   3. Home button CSS: fully visited-proof
 *   4. Home button JS handler: removed (navigation via href)
 */
'use strict';
const fs   = require('fs');
const path = require('path');

const ROOT    = path.resolve(__dirname);
const POCLETS = path.join(ROOT, 'instances', 'poclets');
const SITE_URL = 'https://echopraxium.github.io/tscg';

const SVG = '<svg width="22" height="22" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display:block;"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" fill="#ffffff" style="fill:#ffffff !important"/></svg>';

const NEW_CSS = `/* ── Home button — SVG icon, visited-proof ── */
#btn-home,
#btn-home:link,
#btn-home:visited,
#btn-home:hover,
#btn-home:active {
  display: inline-flex;
  align-items: center;
  background: none !important;
  border: none !important;
  cursor: pointer;
  padding: 4px 6px;
  margin-right: 4px;
  opacity: 0.85;
  transition: opacity 0.15s;
  text-decoration: none !important;
  filter: none !important;
  -webkit-filter: none !important;
  color: inherit !important;
}
#btn-home:hover { opacity: 1 !important; }
#btn-home svg, #btn-home:visited svg { filter: none !important; }
#btn-home path, #btn-home:visited path { fill: #ffffff !important; }`;

// Find all M0_*.html recursively under instances/poclets/
function findSimulations(dir) {
  const results = [];
  if (!fs.existsSync(dir)) return results;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) results.push(...findSimulations(full));
    else if (entry.isFile() && entry.name.startsWith('M0_') && entry.name.endsWith('.html'))
      results.push(full);
  }
  return results;
}

function patchFile(filePath) {
  let src = fs.readFileSync(filePath, 'utf-8');
  let changed = false;

  // ── 1. CSP: add 'unsafe-eval' ─────────────────────────────────────────────
  if (!src.includes("'unsafe-eval'")) {
    src = src.replace(
      "script-src 'self' 'unsafe-inline'",
      "script-src 'self' 'unsafe-inline' 'unsafe-eval'"
    );
    changed = true;
  }

  // ── 2. Replace old #btn-home CSS (any variant) ────────────────────────────
  const cssStart = src.indexOf('/* ── Home button');
  const cssEnd   = src.indexOf('#btn-home:hover');
  if (cssStart !== -1 && cssEnd !== -1) {
    const hoverEnd = src.indexOf('\n', cssEnd) + 1;
    src = src.slice(0, cssStart) + NEW_CSS + '\n' + src.slice(hoverEnd);
    changed = true;
  }

  // ── 3. Replace btn-home element (button or <a> with unicode) ─────────────
  // Match any existing btn-home element
  const btnRe = /<(?:button|a)\s+id="btn-home"[\s\S]*?<\/(?:button|a)>/;
  const newEl = `<a id="btn-home" href="${SITE_URL}/" title="Back to Poclet Gallery" target="_self">${SVG}</a>`;
  if (btnRe.test(src)) {
    src = src.replace(btnRe, newEl);
    changed = true;
  }

  // ── 4. Remove any JS handler for btn-home ────────────────────────────────
  src = src.replace(
    /\n?\/\/ [─\-]+ Home button[^\n]*\n/g, '\n'
  );
  src = src.replace(
    /document\.getElementById\('btn-home'\)\.addEventListener\('click'[^;]+;\n?/g, ''
  );

  if (changed) {
    fs.writeFileSync(filePath, src, 'utf-8');
    return true;
  }
  return false;
}

// ── Main ─────────────────────────────────────────────────────────────────────
console.log('[TSCG] apply_fixes.js — Patching simulation files');
console.log('  Root:', ROOT);

const files = findSimulations(POCLETS);
if (!files.length) {
  console.error('  [ERROR] No M0_*.html found under instances/poclets/');
  process.exit(1);
}

let patched = 0;
files.forEach(f => {
  const rel = path.relative(ROOT, f);
  const ok  = patchFile(f);
  console.log('  ' + (ok ? '✓ patched' : '· skipped') + '  ' + rel);
  if (ok) patched++;
});

console.log('\n  ✓ Done — ' + patched + '/' + files.length + ' file(s) patched.');
console.log('  → Now run: node generate_index.js --site-url ' + SITE_URL);
