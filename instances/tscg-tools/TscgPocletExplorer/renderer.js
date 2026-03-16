/**
 * TSCG Poclet Explorer — Renderer
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 2.0.0
 *
 * Handles:
 *   - File tree (left panel): reads poclet list via IPC
 *   - README display (right panel): markdown → HTML via lightweight parser
 *   - Splitter: resizable left/right panels
 *   - Run Poclet button
 *   - Keyboard shortcuts
 */

'use strict';

const { ipcRenderer } = require('electron');

// ── State ─────────────────────────────────────────────────────────
let poclets      = [];
let selectedId   = null;

// ── Init ──────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', async () => {
  ipcRenderer.send('renderer-ready');
  poclets = await ipcRenderer.invoke('get-poclets');
  renderTree();
  initSplitter();
  initKeyboard();
  // Auto-select first poclet if any
  if (poclets.length > 0) selectPoclet(poclets[0].id);
});

// ── File tree ─────────────────────────────────────────────────────
function renderTree() {
  const list  = document.getElementById('tree-list');
  const count = document.getElementById('tree-count');
  count.textContent = poclets.length + ' poclet' + (poclets.length !== 1 ? 's' : '');

  if (!poclets.length) {
    list.innerHTML = `<div style="padding:16px 12px;font-size:11px;color:var(--muted)">
      No poclets found in<br>instances/poclets/</div>`;
    return;
  }

  list.innerHTML = poclets.map(p => {
    // Build sim-type badges:
    // - JS only if sim/ folder exists (hasElectron)
    // - PY only if no sim/ folder but a .bat launcher exists
    const badges = [
      p.hasElectron ? '<span class="tree-badge has-electron">JS</span>'  : '',
      (!p.hasElectron && p.hasPython) ? '<span class="tree-badge has-python">PY</span>' : '',
      (!p.hasElectron && !p.hasPython) ? '<span class="tree-badge">no sim</span>' : ''
    ].join('');

    const iconColor = p.hasSim ? '#79c0ff' : '#c5ccd4';
    return `
      <div class="tree-item" data-id="${p.id}" title="${p.id}">
        <span class="tree-icon" style="color:${iconColor}">&#9654;</span>
        <span class="tree-label">${p.label}</span>
        <span class="tree-badges">${badges}</span>
      </div>`;
  }).join('');

  list.querySelectorAll('.tree-item').forEach(el => {
    el.addEventListener('click', () => selectPoclet(el.dataset.id));
  });
}

async function selectPoclet(id) {
  selectedId = id;
  const p = poclets.find(x => x.id === id);

  // Tree highlight
  document.querySelectorAll('.tree-item').forEach(el =>
    el.classList.toggle('active', el.dataset.id === id));

  // Footer info
  document.getElementById('footer-info').textContent  = p ? p.label : '';
  document.getElementById('footer-path').textContent  = p ? p.simPath : '';

  // Launch buttons
  updateLaunchButtons(p);

  // README panel header
  document.getElementById('readme-poclet-name').textContent = p ? p.label : 'Select a poclet';

  if (!p) { showPlaceholder('No poclet selected'); return; }
  if (!p.hasReadme) {
    showPlaceholder(p.label + '\n\nNo README found.\nExpected: M0_' +
      p.id.replace(/-/g,'') + '_README.md');
    return;
  }

  const md = await ipcRenderer.invoke('get-readme', p.readmePath);
  if (!md) { showPlaceholder('Could not read README.'); return; }
  document.getElementById('readme-body').innerHTML =
    '<div class="readme-md">' + parseMarkdown(md) + '</div>';
}

function updateLaunchButtons(p) {
  const container = document.getElementById('launch-buttons');
  if (!p || !p.hasSim) {
    container.innerHTML =
      '<button class="btn-run" disabled>&#9654; Run Poclet</button>';
    return;
  }

  let html = '';

  if (p.hasElectron) {
    // sim/ folder exists → ElectronJS only
    html += `<button class="btn-run btn-electron"
               onclick="launchElectron()"
               title="Launch ElectronJS simulation">
               &#9654; Run (ElectronJS)
             </button>`;
  } else if (p.hasPython) {
    // No sim/ folder but .bat launcher exists → Python only
    html += `<button class="btn-run btn-python"
               onclick="launchPython()"
               title="Launch Python/Pygame simulation via ${p.batFile ? p.batFile.split('\\').pop() : '.bat'}">
               &#9654; Run Python
             </button>`;
  }

  container.innerHTML = html;
}

function launchElectron() {
  const p = poclets.find(x => x.id === selectedId);
  if (p?.hasElectron) ipcRenderer.send('launch-poclet', p.simPath);
}

function launchPython() {
  const p = poclets.find(x => x.id === selectedId);
  if (p?.hasPython) ipcRenderer.send('launch-python', p.batFile);
}

function showPlaceholder(msg) {
  const body = document.getElementById('readme-body');
  const lines = msg.split('\n');
  body.innerHTML = `
    <div class="readme-placeholder">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="1" opacity=".3">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
        <polyline points="10 9 9 9 8 9"/>
      </svg>
      <div class="ph-title">${escHtml(lines[0])}</div>
      ${lines.slice(1).filter(l=>l.trim()).map(l =>
        `<div class="ph-sub">${escHtml(l)}</div>`).join('')}
    </div>`;
}

// ── Minimal Markdown → HTML parser ───────────────────────────────
// Handles: headings, bold, italic, inline code, code blocks,
// tables, blockquotes, hr, unordered/ordered lists, links, paragraphs.
function parseMarkdown(md) {
  let html = escHtml(md);

  // Fenced code blocks  ```...```
  html = html.replace(/```[\w]*\n([\s\S]*?)```/g,
    (_, code) => `<pre><code>${code.trimEnd()}</code></pre>`);

  // Headings
  html = html.replace(/^######\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^#####\s+(.+)$/gm,  '<h3>$1</h3>');
  html = html.replace(/^####\s+(.+)$/gm,   '<h3>$1</h3>');
  html = html.replace(/^###\s+(.+)$/gm,    '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm,     '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm,      '<h1>$1</h1>');

  // Horizontal rule
  html = html.replace(/^[-*_]{3,}\s*$/gm, '<hr>');

  // Blockquote
  html = html.replace(/^&gt;\s*(.+)$/gm, '<blockquote>$1</blockquote>');

  // Tables  | col | col |
  html = html.replace(/((?:^\|.+\|\n?)+)/gm, m => {
    const rows = m.trim().split('\n');
    if (rows.length < 2) return m;
    const header = rows[0];
    const isDivider = r => /^\|[-| :]+\|$/.test(r.trim());
    let out = '<table>';
    let inBody = false;
    rows.forEach((row, i) => {
      if (isDivider(row)) { out += '<tbody>'; inBody = true; return; }
      const cells = row.replace(/^\||\|$/g, '').split('|');
      const tag   = (!inBody) ? 'th' : 'td';
      out += '<tr>' + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('') + '</tr>';
    });
    out += inBody ? '</tbody>' : '';
    return out + '</table>';
  });

  // Unordered lists
  html = html.replace(/^[-*+]\s+(.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/gs,  '<ul>$1</ul>');

  // Ordered lists
  html = html.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');

  // Inline: bold, italic, inline code, links
  html = html.replace(/\*\*([^*]+)\*\*/g,      '<strong>$1</strong>');
  html = html.replace(/\*([^*]+)\*/g,           '<em>$1</em>');
  html = html.replace(/`([^`]+)`/g,             '<code>$1</code>');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g,'<a href="$2">$1</a>');

  // Paragraphs — blank-line separated blocks not already tagged
  html = html.replace(/\n{2,}/g, '\n\n');
  const blocks = html.split(/\n\n/);
  html = blocks.map(b => {
    const t = b.trim();
    if (!t) return '';
    if (/^<(h[1-6]|ul|ol|li|pre|table|blockquote|hr)/.test(t)) return t;
    return '<p>' + t.replace(/\n/g, '<br>') + '</p>';
  }).join('\n');

  return html;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;')
          .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Keyboard shortcuts ────────────────────────────────────────────
function initKeyboard() {
  document.addEventListener('keydown', e => {
    // Arrow Up/Down → navigate tree
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      const idx  = poclets.findIndex(p => p.id === selectedId);
      const next = e.key === 'ArrowDown'
        ? Math.min(idx + 1, poclets.length - 1)
        : Math.max(idx - 1, 0);
      if (poclets[next]) selectPoclet(poclets[next].id);
      e.preventDefault();
    }
    // Enter → prefer Electron, fallback to Python
    if (e.key === 'Enter') {
      const p = poclets.find(x => x.id === selectedId);
      if (!p) return;
      if (p.hasElectron) launchElectron();
      else if (p.hasPython) launchPython();
    }
  });
}
function initSplitter() {
  const splitter = document.getElementById('splitter');
  const shell    = document.getElementById('shell');
  let dragging = false, startX = 0, startW = 0;

  splitter.addEventListener('mousedown', e => {
    dragging = true; startX = e.clientX;
    startW   = document.getElementById('tree-panel').getBoundingClientRect().width;
    splitter.classList.add('dragging');
    document.body.style.cssText = 'cursor:col-resize;user-select:none';
    e.preventDefault();
  });
  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const newW = Math.max(160, Math.min(520, startW + (e.clientX - startX)));
    shell.style.setProperty('--left-w', newW + 'px');
  });
  document.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    splitter.classList.remove('dragging');
    document.body.style.cssText = '';
  });
}

