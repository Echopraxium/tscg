'use strict';

/**
 * renderer.js — TscgPocletMiner UI Controller
 *
 * Handles all UI logic: state machine, round rendering,
 * settings management, RAG build, IPC calls to main process.
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

// ── Constants ─────────────────────────────────────────────────────────────────

const ROUND_LABELS = [
  null,
  { title: 'Round 1 — System Identification',
    sub:   'Describe the system you want to model as a TSCG poclet.' },
  { title: 'Round 2 — ASFID Scoring (Eagle Eye)',
    sub:   'The LLM will assess the 5 Territory dimensions: A · S · F · I · D' },
  { title: 'Round 3 — REVOI Scoring (Sphinx Eye)',
    sub:   'The LLM will assess the 5 Map dimensions: R · E · V · O · I' },
  { title: 'Round 4 — M2 GenericConcept Selection',
    sub:   'The LLM will select the most relevant M2 concepts from the RAG corpus.' },
  { title: 'Round 5 — M0 JSON-LD Generation',
    sub:   'The LLM will generate the complete M0 poclet file.' },
];

const DIM_COLORS = {
  A: 'var(--col-A)', S: 'var(--col-S)', F: 'var(--col-F)',
  I: 'var(--col-I)', D: 'var(--col-D)',
  R: 'var(--col-R)', E: 'var(--col-E)', V: 'var(--col-V)',
  O: 'var(--col-O)',
};

// ── App state ─────────────────────────────────────────────────────────────────

const state = {
  config:       null,   // loaded from main process
  session:      false,  // session active?
  currentRound: 0,      // 0 = not started
  maxRound:     0,      // highest round completed
  roundData:    {},     // accumulated poclet data
  running:      false,  // LLM call in progress
  ragBuilt:     false,
};

// ── DOM refs ──────────────────────────────────────────────────────────────────

const $ = id => document.getElementById(id);

const ui = {
  // header
  chipLlm:      $('chip-llm'),
  chipRag:      $('chip-rag'),
  btnSettings:  $('btn-settings'),
  btnHome:      $('btn-home'),
  btnTscgLogo:  $('btn-tscg-logo'),

  // stepper
  steps:    Array.from({ length: 5 }, (_, i) => $(`step-${i+1}`)),
  conns:    Array.from({ length: 4 }, (_, i) => $(`conn-${i+1}`)),

  // main
  roundContent: $('round-content'),

  // footer
  footerSpinner: $('footer-spinner'),
  footerMsg:     $('footer-msg'),
  btnNew:        $('btn-new-session'),
  btnPrev:       $('btn-prev'),
  btnRun:        $('btn-run'),
  btnNext:       $('btn-next'),
  btnSave:       $('btn-save-jsonld'),

  // sidebar summary
  sbPocletInfo:  $('sb-poclet-info'),
  sbEmpty:       $('sb-empty'),
  sbName:        $('sb-name'),
  sbDomain:      $('sb-domain'),
  sbType:        $('sb-type'),
  sbSpectral:    $('sb-spectral'),
  sbGap:         $('sb-gap'),
  sbAsfidChips:  $('sb-asfid-chips'),
  sbRevoiChips:  $('sb-revoi-chips'),

  // sidebar settings
  providerSelect:     $('provider-select'),
  providerInfoIcon:   $('provider-info-icon'),
  providerInfoName:   $('provider-info-name'),
  providerInfoDesc:   $('provider-info-desc'),
  providerInfoMeta:   $('provider-info-meta'),
  inputGeminiKey:      $('input-gemini-key'),
  inputGeminiModel:    $('input-gemini-model'),
  inputOllamaModel:    $('input-ollama-model'),
  inputDeepseekKey:    $('input-deepseek-key'),
  inputDeepseekModel:  $('input-deepseek-model'),
  inputDeepseekKey:   $('input-deepseek-key'),
  inputAnthropicKey:  $('input-anthropic-key'),
  inputAnthropicModel:$('input-anthropic-model'),
  inputRepoRoot:      $('input-repo-root'),
  ragStatusLine:      $('rag-status-line'),
  btnBuildRag:        $('btn-build-rag'),
  btnBrowseRepo:      $('btn-browse-repo'),
  btnSaveSettings:    $('btn-save-settings'),
  btnTestGemini:      $('btn-test-gemini'),
  btnTestOllama:      $('btn-test-ollama'),
  btnTestDeepseek:    $('btn-test-deepseek'),
  btnTestAnthropic:   $('btn-test-anthropic'),

  // log
  logArea:  $('tab-log').querySelector('#log-area'),

  // tooltip
  tooltip: $('tooltip'),
};

// ── Logging ───────────────────────────────────────────────────────────────────

function log(msg, cls = '') {
  const span = document.createElement('span');
  if (cls) span.className = cls;
  span.textContent = `\n${new Date().toLocaleTimeString()} ${msg}`;
  ui.logArea.appendChild(span);
  ui.logArea.scrollTop = ui.logArea.scrollHeight;
}

// ── Tooltip ───────────────────────────────────────────────────────────────────

function tooltip(el, text) {
  el.addEventListener('mouseenter', () => {
    const r = el.getBoundingClientRect();
    ui.tooltip.textContent = text;
    ui.tooltip.style.left = `${Math.max(8, r.left)}px`;
    ui.tooltip.style.top  = `${r.bottom + 6}px`;
    ui.tooltip.style.opacity = '1';
  });
  el.addEventListener('mouseleave', () => { ui.tooltip.style.opacity = '0'; });
}

// ── Tab switching ─────────────────────────────────────────────────────────────

// ── Tab switching ─────────────────────────────────────────────────────────────

function switchTab(tabId) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  const tabEl = document.querySelector(`[data-tab="${tabId}"]`);
  if (tabEl) tabEl.classList.add('active');
  const panelEl = $(`tab-${tabId}`);
  if (panelEl) panelEl.classList.add('active');
}

document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => switchTab(tab.dataset.tab));
});

// ── Splitter drag ─────────────────────────────────────────────────────────────

(function initSplitter() {
  const splitter = $('splitter');
  const app = $('app');
  let dragging = false;
  splitter.addEventListener('mousedown', () => { dragging = true; });
  document.addEventListener('mousemove', e => {
    if (!dragging) return;
    const total = app.getBoundingClientRect().width;
    const sidebar = total - e.clientX - 5;
    const clamped = Math.max(220, Math.min(520, sidebar));
    app.style.gridTemplateColumns = `1fr 5px ${clamped}px`;
  });
  document.addEventListener('mouseup', () => { dragging = false; });
})();

// ── Header buttons ────────────────────────────────────────────────────────────

ui.btnHome.addEventListener('click', () => {
  window.open('https://echopraxium.github.io/tscg/', '_blank');
});
tooltip(ui.btnHome, 'TSCG GitHub Pages');

ui.btnTscgLogo.addEventListener('click', () => {
  window.open('https://github.com/Echopraxium/tscg', '_blank');
});
tooltip(ui.btnTscgLogo, 'TSCG GitHub repository');

ui.btnSettings.addEventListener('click', () => switchTab('settings'));

// ── Status helpers ────────────────────────────────────────────────────────────

function setStatus(msg, spinner = false) {
  ui.footerMsg.textContent = msg;
  ui.footerSpinner.style.display = spinner ? 'block' : 'none';
}

function updateChips() {
  const cfg = state.config;
  if (!cfg) return;
  const pid = cfg.active;
  const labels = { gemini: '🆓 Gemini Free', ollama: '🏠 Ollama', deepseek: '☁️ DeepSeek', anthropic: '⭐ Claude API' };
  ui.chipLlm.textContent = labels[pid] ?? pid;

  if (state.ragBuilt) {
    ui.chipRag.textContent = 'RAG ✓';
    ui.chipRag.classList.remove('off');
  } else {
    ui.chipRag.textContent = 'RAG ✗';
    ui.chipRag.classList.add('off');
  }
}

// ── Settings: provider list ───────────────────────────────────────────────────

let providersCache = null; // Store providers for info display

async function renderProviderList() {
  let providers = await window.tscgMiner.config.listProviders();
  
  // Reorder: DeepSeek first
  const providerOrder = ['deepseek', 'gemini', 'ollama', 'anthropic'];
  providers.sort((a, b) => {
    const ia = providerOrder.indexOf(a.id);
    const ib = providerOrder.indexOf(b.id);
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
  });
  
  providersCache = providers; // Cache for info display
  
  ui.providerSelect.innerHTML = '';
  
  for (const p of providers) {
    const option = document.createElement('option');
    option.value = p.id;
    option.textContent = `${p.icon} ${p.label}`; // Simplified: just icon + name
    ui.providerSelect.appendChild(option);
  }
  
  // Set current selection
  ui.providerSelect.value = state.config?.active ?? 'deepseek';
  
  // Update info box and show key section
  updateProviderInfo(state.config?.active ?? 'deepseek');
  showKeySection(state.config?.active ?? 'deepseek');
  
  // Handle change event
  ui.providerSelect.addEventListener('change', (e) => {
    selectProvider(e.target.value);
  }, { once: false });
}

function updateProviderInfo(pid) {
  if (!providersCache) return;
  const provider = providersCache.find(p => p.id === pid);
  if (!provider) return;
  
  ui.providerInfoIcon.textContent = provider.icon;
  ui.providerInfoName.textContent = provider.label;
  ui.providerInfoDesc.textContent = provider.description;
  ui.providerInfoMeta.textContent = `Quality: ${provider.quality} · ${provider.speed}`;
}

function selectProvider(pid) {
  if (!state.config) return;
  state.config.active = pid;
  updateProviderInfo(pid);
  showKeySection(pid);
  updateChips();
}

function showKeySection(pid) {
  ['gemini', 'ollama', 'deepseek', 'anthropic'].forEach(id => {
    $(`key-section-${id}`).style.display = id === pid ? 'block' : 'none';
  });
}

// ── Settings: load / save ─────────────────────────────────────────────────────

async function loadSettings() {
  state.config = await window.tscgMiner.config.load();

  // Fill form fields
  const p = state.config.providers;
  ui.inputGeminiKey.value      = p.gemini?.apiKey ?? '';
  ui.inputGeminiModel.value    = p.gemini?.model ?? 'gemini-2.5-flash';
  ui.inputOllamaModel.value    = p.ollama?.model ?? 'phi3.5:3.8b-mini-instruct-q4_K_M';
  ui.inputDeepseekKey.value    = p.deepseek?.apiKey ?? '';
  ui.inputDeepseekModel.value  = p.deepseek?.model ?? 'deepseek-chat';
  ui.inputAnthropicKey.value   = p.anthropic?.apiKey ?? '';
  ui.inputAnthropicModel.value = p.anthropic?.model ?? 'claude-haiku-4-5-20251001';
  ui.inputRepoRoot.value       = state.config.tscgRepoRoot ?? '';

  await renderProviderList();
  updateChips();

  // Check RAG status
  const ragStatus = await window.tscgMiner.rag.status();
  state.ragBuilt = ragStatus.built;
  if (ragStatus.built) {
    ui.ragStatusLine.textContent = `Index ready — ${ragStatus.docCount} chunks`;
    ui.ragStatusLine.style.color = 'var(--accent)';
  }
  updateChips();
}

ui.btnSaveSettings.addEventListener('click', async () => {
  // Read form values back into config
  state.config.providers.gemini.apiKey        = ui.inputGeminiKey.value.trim();
  state.config.providers.gemini.model         = ui.inputGeminiModel.value;
  state.config.providers.ollama.model         = ui.inputOllamaModel.value;
  state.config.providers.deepseek.apiKey      = ui.inputDeepseekKey.value.trim();
  state.config.providers.deepseek.model       = ui.inputDeepseekModel.value;
  state.config.providers.anthropic.apiKey     = ui.inputAnthropicKey.value.trim();
  state.config.providers.anthropic.model      = ui.inputAnthropicModel.value;
  state.config.tscgRepoRoot                   = ui.inputRepoRoot.value.trim();

  await window.tscgMiner.config.save(state.config);
  updateChips();
  log('Settings saved.', 'log-ok');
  setStatus('Settings saved.');
});

// ── Test connections ──────────────────────────────────────────────────────────

async function testConnection(pid) {
  const dot = $(`dot-${pid}`);
  if (dot) dot.className = 'status-dot chk';
  setStatus(`Testing ${pid}…`, true);

  // Save current form values first
  state.config.providers.gemini.apiKey      = ui.inputGeminiKey.value.trim();
  state.config.providers.gemini.model       = ui.inputGeminiModel.value;
  state.config.providers.ollama.model       = ui.inputOllamaModel.value || state.config.providers.ollama.model;
  state.config.providers.deepseek.apiKey    = ui.inputDeepseekKey.value.trim();
  state.config.providers.deepseek.model     = ui.inputDeepseekModel.value;
  state.config.providers.anthropic.apiKey   = ui.inputAnthropicKey.value.trim();
  state.config.providers.anthropic.model    = ui.inputAnthropicModel.value;

  const results = await window.tscgMiner.config.checkAll(state.config);
  const r = results[pid];

  if (dot) dot.className = `status-dot ${r.ok ? 'ok' : 'err'}`;
  setStatus(r.message);
  log(r.message, r.ok ? 'log-ok' : 'log-err');
}

ui.btnTestGemini.addEventListener('click',    () => testConnection('gemini'));
ui.btnTestOllama.addEventListener('click',    () => testConnection('ollama'));
ui.btnTestDeepseek.addEventListener('click',  () => testConnection('deepseek'));
ui.btnTestAnthropic.addEventListener('click', () => testConnection('anthropic'));

// ── RAG build ─────────────────────────────────────────────────────────────────

ui.btnBrowseRepo.addEventListener('click', async () => {
  const dir = await window.tscgMiner.repo.browse();
  if (dir) ui.inputRepoRoot.value = dir;
});

window.tscgMiner.rag.onProgress(msg => {
  // Colour-code errors and warnings in the log
  const isErr  = msg.includes('⚠') || msg.toLowerCase().includes('error');
  const isReady = msg.toLowerCase().includes('rag ready');
  const cls = isErr ? 'log-warn' : isReady ? 'log-ok' : 'log-info';
  log(msg, cls);

  // Update status line (truncate long paths)
  const short = msg.length > 80 ? msg.slice(0, 77) + '…' : msg;
  ui.ragStatusLine.textContent = short;
  ui.ragStatusLine.style.color = isErr ? 'var(--warn)' : 'var(--muted)';
});

ui.btnBuildRag.addEventListener('click', async () => {
  const root = ui.inputRepoRoot.value.trim();
  if (!root) {
    ui.ragStatusLine.textContent = '⚠ Set the TSCG repo root first.';
    ui.ragStatusLine.style.color = 'var(--warn)';
    return;
  }
  state.config.tscgRepoRoot = root;
  await window.tscgMiner.config.save(state.config);

  // Auto-switch to Log tab so the user sees progress in real time
  switchTab('log');

  setStatus('Building RAG index…', true);
  ui.btnBuildRag.disabled = true;
  log(`Building RAG from: ${root}`, 'log-info');
  log('─'.repeat(50), '');

  const result = await window.tscgMiner.rag.build(root);

  ui.btnBuildRag.disabled = false;
  log('─'.repeat(50), '');

  if (result.ok) {
    state.ragBuilt = true;

    // Status line: colour errors count in orange if > 0
    const errPart = result.errors > 0
      ? ` · ⚠ ${result.errors} errors (see log)`
      : ' · 0 errors';
    ui.ragStatusLine.textContent = `✓ ${result.files} files · ${result.chunks} chunks${errPart}`;
    ui.ragStatusLine.style.color = result.errors > 0 ? 'var(--warn)' : 'var(--accent)';

    log(`RAG ready — ${result.files} files · ${result.chunks} chunks · ${result.dupes ?? 0} dupes · ${result.errors} errors`, 'log-ok');
    setStatus(`RAG ready — ${result.chunks} chunks${result.errors > 0 ? ` (${result.errors} errors)` : ''}`);
  } else {
    ui.ragStatusLine.textContent = `✗ ${result.message}`;
    ui.ragStatusLine.style.color = 'var(--danger)';
    log(`RAG build failed: ${result.message}`, 'log-err');
    setStatus('RAG build failed.');
  }
  updateChips();
});

// ── Stepper UI ────────────────────────────────────────────────────────────────

function updateStepper() {
  ui.steps.forEach((step, i) => {
    const r = i + 1;
    step.classList.remove('active', 'done', 'locked');
    if (r < state.currentRound)  step.classList.add('done');
    else if (r === state.currentRound) step.classList.add('active');
    else                          step.classList.add('locked');
  });
  ui.conns.forEach((conn, i) => {
    conn.classList.toggle('done', i + 1 < state.currentRound);
  });
}

// ── Round rendering ───────────────────────────────────────────────────────────

function renderRound(round) {
  const content = ui.roundContent;
  content.innerHTML = '';

  const info = ROUND_LABELS[round];
  const header = el('div', 'round-header', info.title);
  const sub    = el('div', 'round-sub',    info.sub);
  content.appendChild(header);
  content.appendChild(sub);

  const data = state.roundData;

  switch (round) {
    case 1: {
      const textarea = document.createElement('textarea');
      textarea.className = 'user-textarea';
      textarea.id = 'r1-input';
      textarea.placeholder =
        'Describe the system you want to model.\n\nExample:\n"The trophic pyramid is a biological model...\n' +
        'Levels: decomposers, producers, herbivores, carnivores, super-predators."';
      textarea.value = data._r1input ?? '';
      textarea.addEventListener('input', () => { data._r1input = textarea.value; });
      content.appendChild(textarea);

      if (data.systemName) {
        content.appendChild(resultCard('Identified System', renderR1Result(data)));
      }
      break;
    }
    case 2: {
      if (data.asfid) {
        content.appendChild(resultCard('ASFID Scores — Eagle Eye', renderScores(data.asfid, ['A','S','F','I','D'])));
        const mean = el('div', '', `Mean ASFID: ${(data.asfid_mean ?? 0).toFixed(3)}`);
        mean.style.cssText = 'font-size:12px;color:var(--text-dim);margin-top:4px';
        content.appendChild(mean);
      } else {
        content.appendChild(waitCard('ASFID scores will appear here after running this round.'));
      }
      break;
    }
    case 3: {
      if (data.revoi) {
        content.appendChild(resultCard('REVOI Scores — Sphinx Eye', renderScores(data.revoi, ['R','E','V','O','I'])));
        const meta = document.createElement('div');
        meta.style.cssText = 'display:flex;gap:12px;align-items:center;margin-top:6px';
        const spectral = data.spectral_class ?? '—';
        meta.innerHTML = `
          <span class="spectral ${spectral}">${spectral}</span>
          <span style="font-size:12px;color:var(--text-dim)">
            δ = <strong style="font-family:var(--mono)">${(data.epistemic_gap ?? 0).toFixed(3)}</strong>
            &nbsp;·&nbsp; REVOI mean = <strong style="font-family:var(--mono)">${(data.revoi_mean ?? 0).toFixed(3)}</strong>
          </span>
        `;
        content.appendChild(meta);
      } else {
        content.appendChild(waitCard('REVOI scores will appear here after running this round.'));
      }
      break;
    }
    case 4: {
      if (data.genericConcepts?.length) {
        content.appendChild(resultCard('M2 GenericConcepts', renderConcepts(data.genericConcepts)));
        if (data.knowledgeFieldCombos?.length) {
          content.appendChild(resultCard('KnowledgeFieldConceptCombos', renderConcepts(data.knowledgeFieldCombos, true)));
        }
      } else {
        content.appendChild(waitCard('M2 concept selection will appear here after running this round.'));
      }
      break;
    }
    case 5: {
      if (data.jsonld) {
        const jsonText = JSON.stringify(data.jsonld, null, 2);
        const card = document.createElement('div');
        card.className = 'result-card';
        card.innerHTML = `
          <div class="result-card-header" style="display:flex;justify-content:space-between;align-items:center">
            <span>M0 JSON-LD Output</span>
            <button class="btn btn-ghost btn-sm" id="btn-copy-jsonld">⎘ Copy</button>
          </div>
          <div class="result-card-body">
            <pre class="jsonld-viewer">${escHtml(jsonText)}</pre>
          </div>
        `;
        content.appendChild(card);
        card.querySelector('#btn-copy-jsonld').addEventListener('click', () => {
          navigator.clipboard.writeText(jsonText);
          setStatus('JSON-LD copied to clipboard.');
        });
      } else {
        content.appendChild(waitCard('The M0 JSON-LD file will be generated here in Round 5.'));
      }
      break;
    }
  }
}

// ── Render helpers ────────────────────────────────────────────────────────────

function el(tag, cls, text = '') {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text) e.textContent = text;
  return e;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function resultCard(title, bodyEl) {
  const card = document.createElement('div');
  card.className = 'result-card';
  const hdr = el('div', 'result-card-header', title);
  const body = el('div', 'result-card-body');
  body.appendChild(bodyEl);
  card.appendChild(hdr); card.appendChild(body);
  return card;
}

function waitCard(msg) {
  const card = document.createElement('div');
  card.className = 'placeholder';
  card.style.minHeight = '120px';
  card.innerHTML = `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity=".3">
    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
  </svg>
  <div class="placeholder-sub">${msg}</div>`;
  return card;
}

function renderR1Result(data) {
  const wrap = document.createElement('div');
  const rows = [
    ['systemName', data.systemName],
    ['domain',     data.domain],
    ['pocletType', data.pocletType],
    ['attractor',  data.attractor],
  ];
  for (const [k, v] of rows) {
    const row = document.createElement('div');
    row.className = 'sb-row';
    row.innerHTML = `<span class="sb-key">${k}</span><span class="sb-val">${escHtml(String(v ?? '—'))}</span>`;
    wrap.appendChild(row);
  }
  if (data.poles?.length) {
    const pRow = document.createElement('div');
    pRow.style.marginTop = '8px';
    pRow.innerHTML = `<div class="sb-key" style="margin-bottom:5px">Poles</div>
      <div class="concept-list">${data.poles.map(p => `<span class="concept-chip">${escHtml(p)}</span>`).join('')}</div>`;
    wrap.appendChild(pRow);
  }
  if (data.description) {
    const desc = document.createElement('div');
    desc.className = 'sb-desc';
    desc.style.marginTop = '10px';
    desc.textContent = data.description;
    wrap.appendChild(desc);
  }
  return wrap;
}

function renderScores(scores, dims) {
  const wrap = document.createElement('div');
  const grid = document.createElement('div');
  grid.className = 'score-grid';

  for (const dim of dims) {
    const val = parseFloat(scores[dim] ?? 0);
    const color = DIM_COLORS[dim] ?? 'var(--text)';
    const rat = scores[`${dim}_rationale`] ?? '';

    const dimEl  = el('div', 'score-dim', dim);
    dimEl.style.color = color;

    const barWrap = el('div', 'score-bar-wrap');
    const bar = el('div', 'score-bar');
    bar.style.cssText = `width:${(val*100).toFixed(1)}%;background:${color};opacity:.7`;
    barWrap.appendChild(bar);

    const valEl = el('div', 'score-val', val.toFixed(2));
    valEl.style.color = color;

    grid.appendChild(dimEl);
    grid.appendChild(barWrap);
    grid.appendChild(valEl);

    if (rat) {
      const ratEl = el('div', 'score-rat', rat);
      grid.appendChild(ratEl);
    }
  }
  wrap.appendChild(grid);
  return wrap;
}

function renderConcepts(concepts, isCombo = false) {
  const wrap = document.createElement('div');
  wrap.className = 'concept-list';
  for (const c of concepts) {
    const chip = document.createElement('div');
    chip.className = 'concept-chip';
    chip.style.display = 'flex'; chip.style.flexDirection = 'column'; chip.style.gap = '2px';
    chip.innerHTML = `
      <span><strong>${escHtml(c.name)}</strong>
        ${c.formula ? `<span class="formula-badge">${escHtml(c.formula)}</span>` : ''}
        ${isCombo && c.domain ? `<span style="font-size:10px;color:var(--muted);margin-left:4px">${escHtml(c.domain)}</span>` : ''}
      </span>
      ${c.rationale ? `<span style="font-size:10px;color:var(--muted)">${escHtml(c.rationale)}</span>` : ''}
    `;
    wrap.appendChild(chip);
  }
  return wrap;
}

// ── Sidebar summary update ────────────────────────────────────────────────────

function updateSummary() {
  const d = state.roundData;
  const hasData = !!d.systemName;

  ui.sbPocletInfo.style.display = hasData ? 'block' : 'none';
  ui.sbEmpty.style.display      = hasData ? 'none'  : 'block';

  if (!hasData) return;

  ui.sbName.textContent     = d.systemName    ?? '—';
  ui.sbDomain.textContent   = d.domain        ?? '—';
  ui.sbType.textContent     = d.pocletType    ?? '—';
  ui.sbSpectral.textContent = d.spectral_class ?? '—';
  ui.sbGap.textContent      = d.epistemic_gap != null
    ? d.epistemic_gap.toFixed(3) : '—';

  // ASFID mini chips
  ui.sbAsfidChips.innerHTML = '';
  if (d.asfid) {
    for (const dim of ['A','S','F','I','D']) {
      const val = parseFloat(d.asfid[dim] ?? 0);
      const c = document.createElement('span');
      c.className = 'concept-chip';
      c.style.color = DIM_COLORS[dim];
      c.style.border = `1px solid ${DIM_COLORS[dim]}44`;
      c.textContent = `${dim} ${val.toFixed(2)}`;
      ui.sbAsfidChips.appendChild(c);
    }
  }

  // REVOI mini chips
  ui.sbRevoiChips.innerHTML = '';
  if (d.revoi) {
    for (const dim of ['R','E','V','O','I']) {
      const val = parseFloat(d.revoi[dim] ?? 0);
      const c = document.createElement('span');
      c.className = 'concept-chip';
      c.style.color = DIM_COLORS[dim];
      c.style.border = `1px solid ${DIM_COLORS[dim]}44`;
      c.textContent = `${dim} ${val.toFixed(2)}`;
      ui.sbRevoiChips.appendChild(c);
    }
  }
}

// ── Footer buttons ────────────────────────────────────────────────────────────

function updateFooterButtons() {
  const r = state.currentRound;
  const max = state.maxRound;
  const running = state.running;
  const session = state.session;

  ui.btnPrev.disabled = !session || r <= 1 || running;
  ui.btnNext.disabled = !session || r >= max || r >= 5 || running;
  ui.btnRun.disabled  = !session || running;
  ui.btnSave.disabled = !state.roundData.jsonld;

  if (session && r >= 1 && r <= 5) {
    ui.btnRun.textContent = `▶ Run Round ${r}`;
  }
}

// ── New session ───────────────────────────────────────────────────────────────

ui.btnNew.addEventListener('click', async () => {
  await window.tscgMiner.pipeline.reset();
  state.session     = true;
  state.currentRound = 1;
  state.maxRound    = 1;
  state.roundData   = {};
  state.running     = false;

  updateStepper();
  renderRound(1);
  updateSummary();
  updateFooterButtons();
  setStatus('New session started — describe your system in Round 1.');
  log('New poclet session started.', 'log-info');
});

// ── Run current round ─────────────────────────────────────────────────────────

ui.btnRun.addEventListener('click', async () => {
  if (state.running) return;

  const round = state.currentRound;

  // Get user input for round 1
  let userInput = '';
  if (round === 1) {
    userInput = ($('r1-input')?.value ?? '').trim();
    if (!userInput) {
      setStatus('⚠ Please describe the system first.');
      return;
    }
    state.roundData._r1input = userInput;
  }

  state.running = true;
  updateFooterButtons();
  setStatus(`Running Round ${round}…`, true);
  log(`Running Round ${round}…`, 'log-info');

  // Show spinner in content area
  const spinnerEl = document.createElement('div');
  spinnerEl.style.cssText = 'display:flex;align-items:center;gap:10px;padding:12px 0;color:var(--muted);font-size:12px';
  spinnerEl.innerHTML = '<div class="spinner"></div><span>LLM processing…</span>';
  ui.roundContent.appendChild(spinnerEl);

  const result = await window.tscgMiner.pipeline.runRound(round, userInput, state.config);
  state.running = false;

  if (!result.ok) {
    log(`Round ${round} error: ${result.message}`, 'log-err');
    setStatus(`Error: ${result.message}`);
    spinnerEl.remove();
    updateFooterButtons();
    return;
  }

  // Merge result data
  state.roundData = result.roundData;
  state.maxRound  = Math.max(state.maxRound, round);

  // Auto-advance to next round (stay on current to show results)
  if (round < 5) {
    state.currentRound = round + 1;
    state.maxRound     = Math.max(state.maxRound, round + 1);
    updateStepper();
    renderRound(round + 1);
  } else {
    renderRound(5);
  }

  updateSummary();
  updateFooterButtons();
  setStatus(`Round ${round} complete.`);
  log(`Round ${round} complete.`, 'log-ok');
});

// ── Prev / Next ───────────────────────────────────────────────────────────────

ui.btnPrev.addEventListener('click', () => {
  if (state.currentRound > 1) {
    state.currentRound--;
    updateStepper();
    renderRound(state.currentRound);
    updateFooterButtons();
  }
});

ui.btnNext.addEventListener('click', () => {
  if (state.currentRound < state.maxRound && state.currentRound < 5) {
    state.currentRound++;
    updateStepper();
    renderRound(state.currentRound);
    updateFooterButtons();
  }
});

// ── Save JSON-LD ──────────────────────────────────────────────────────────────

ui.btnSave.addEventListener('click', async () => {
  const jsonld = state.roundData.jsonld;
  if (!jsonld) return;
  const content      = JSON.stringify(jsonld, null, 2);
  const systemName   = state.roundData.systemName ?? 'Poclet';
  const suggestedName = `M0_${systemName}.jsonld`;
  const result = await window.tscgMiner.file.saveJsonLd(content, suggestedName);
  if (result.ok) {
    log(`Saved: ${result.filePath}`, 'log-ok');
    setStatus(`Saved: ${result.filePath}`);
  } else if (!result.canceled) {
    log(`Save failed: ${result.message}`, 'log-err');
  }
});

// ── Stepper click navigation ──────────────────────────────────────────────────

ui.steps.forEach((step, i) => {
  step.addEventListener('click', () => {
    const r = i + 1;
    if (!state.session) return;
    if (r > state.maxRound) return;
    state.currentRound = r;
    updateStepper();
    renderRound(r);
    updateFooterButtons();
  });
});

// ── Log buttons ───────────────────────────────────────────────────────────────

$('btn-copy-log').addEventListener('click', () => {
  const text = ui.logArea.innerText || ui.logArea.textContent;
  navigator.clipboard.writeText(text).then(() => {
    const btn = $('btn-copy-log');
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.color = 'var(--accent)';
    setTimeout(() => { btn.textContent = orig; btn.style.color = ''; }, 1800);
  });
});

$('btn-clear-log').addEventListener('click', () => {
  ui.logArea.innerHTML = '';
  log('Log cleared.', 'log-info');
});



function extLink(id, url) {
  const el = $(id);
  if (!el) return;
  el.addEventListener('click', e => { e.preventDefault(); window.open(url, '_blank'); });
}
extLink('lnk-gemini',    'https://aistudio.google.com/app/apikey');
extLink('lnk-ollama',    'https://ollama.com');
extLink('lnk-deepseek',  'https://platform.deepseek.com');
extLink('lnk-anthropic', 'https://console.anthropic.com');

// ── Init ──────────────────────────────────────────────────────────────────────

(async function init() {
  await loadSettings();
  setStatus('Ready — configure settings then start a new session.');
  log('TscgPocletMiner loaded.', 'log-ok');
})();
