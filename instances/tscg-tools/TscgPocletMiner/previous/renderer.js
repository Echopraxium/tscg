// renderer.js — TscgPocletMiner Wizard Logic, Scoring Engine & RAG Integration
// Author: Echopraxium with the collaboration of Claude AI
// v1.2.0 — Clickable priority candidates

'use strict';

// ─── State ────────────────────────────────────────────────────────────────────

const state = {
  corpus:        null,
  ragReady:      false,
  ragInitiated:  false,
  currentRound:  1,
  totalRounds:   5,
  systemName:    '',
  domain:        '',
  isNewDomain:   false,
  docQuality:    2,
  pastedContent: '',        // paste zone content (Round 2)
  asfid: { A: 0.5, S: 0.5, F: 0.5, I: 0.5, D: 0.5 },
  candidateType: null,
  invariantChecks: {},
  suggestedConcepts: [],   // from RAG round 5
  verdict: null
};

// ─── ASFID question definitions ──────────────────────────────────────────────

const ASFID_QUESTIONS = [
  { dim:'A', label:'Attractor',  question:'Does the system converge toward a stable state, equilibrium, or attractor?', hint:'e.g. homeostasis, Q-point, settled clot, final metamorphosis stage' },
  { dim:'S', label:'Structure',  question:'Does the system have clearly delimited components, boundaries, and interfaces?', hint:'e.g. RAAS enzymes, transistor terminals, Yggdrasil world-tree levels' },
  { dim:'F', label:'Flow',       question:'Does the system involve observable flows of matter, energy, or information?', hint:'e.g. hormonal flow, electron current, nutrient cycling' },
  { dim:'I', label:'Information',question:'Does the system encode, transform, or route information in a structured way?', hint:'e.g. RAAS signal encoding, transistor I-V equations, immune memory' },
  { dim:'D', label:'Dynamics',   question:'Does the system exhibit feedback, adaptation, oscillation, or non-trivial dynamics?', hint:'e.g. negative feedback in blood pressure, switching, phase transition' }
];

// ─── DOM helpers ──────────────────────────────────────────────────────────────

const $  = (id)  => document.getElementById(id);
const $$ = (sel) => document.querySelectorAll(sel);

function showRound(n) {
  for (let i = 1; i <= state.totalRounds; i++) {
    const el = $(`round-${i}`);
    if (el) el.classList.toggle('hidden', i !== n);
  }
  updateProgress(n);
  updateNav(n);
}

// Round badge labels — kept in sync with index.html round-title spans
const ROUND_TITLES = [
  '',                                          // 0 — unused
  'Domain Identification',                     // Round 1
  'Web Verification + RAG Context',            // Round 2
  'ASFID Pre-Screening',                       // Round 3
  'Type Discriminant',                         // Round 4
  'Invariants, GenericConcepts & Verdict'      // Round 5
];

function updateProgress(n) {
  for (let i = 1; i <= state.totalRounds; i++) {
    const dot = $(`dot-${i}`);
    if (!dot) continue;
    dot.classList.remove('active', 'done');
    if (i < n)  dot.classList.add('done');
    if (i === n) dot.classList.add('active');
  }

  const roundEl = $(`round-${n}`);
  if (!roundEl) return;

  // Badge: step number only  →  [Round 2 / 5]
  const badge = roundEl.querySelector('.round-badge');
  if (badge) badge.textContent = `Round ${n} / ${state.totalRounds}`;

  // System name: displayed after the round-title, in its own element
  // We inject/update a <span id="round-N-system"> after .round-title
  const header = roundEl.querySelector('.round-header');
  if (!header) return;

  let sysSpan = roundEl.querySelector('.round-system-name');
  if (!sysSpan) {
    sysSpan = document.createElement('span');
    sysSpan.className = 'round-system-name';
    sysSpan.style.cssText = [
      'font-size:15px',
      'color:var(--gold)',
      'font-weight:600',
      'margin-left:8px',
      'opacity:0.90',
      'white-space:nowrap',
      'overflow:hidden',
      'text-overflow:ellipsis',
      'max-width:360px'
    ].join(';');
    header.appendChild(sysSpan);
  }

  // Round title: smaller than the poclet name
  const titleEl = header.querySelector('.round-title');
  if (titleEl) titleEl.style.fontSize = '12px';

  sysSpan.textContent = (n > 1 && state.systemName) ? `- ${state.systemName}` : '';
}

function updateNav(n) {
  $('btn-prev').disabled = (n === 1);
  const isLast = (n === state.totalRounds);
  $('btn-next').classList.toggle('hidden', isLast);
  $('btn-compute').classList.toggle('hidden', !isLast);
}

// ─── RAG status banner ────────────────────────────────────────────────────────

function setRagBanner(msg, color) {
  const el = $('rag-status');
  if (!el) return;
  el.textContent = msg;
  el.style.color = color || 'var(--dim)';
}

// ─── Init ─────────────────────────────────────────────────────────────────────

async function init() {
  const result = await window.tscgAPI.loadCorpus();
  if (!result.ok) { console.error('Corpus load failed:', result.error); return; }
  state.corpus = result.data;

  $('corpus-count').textContent  = state.corpus.corpus_stats.total;
  $('domains-count').textContent = state.corpus.corpus_stats.domains_covered;

  buildDomainChips();
  buildASFIDQuestions();
  buildInvariantChecklist();
  buildPriorityList();
  bindEvents();
  showRound(1);

  // Start RAG init in background (non-blocking)
  startRagInit();
}

async function startRagInit() {
  if (state.ragInitiated) return;
  state.ragInitiated = true;

  setRagBanner('⏳ RAG: loading all-MiniLM-L6-v2…', 'var(--dim)');

  window.tscgAPI.onRagProgress((p) => {
    if (p.step === 'ready') {
      state.ragReady = true;
      setRagBanner('✅ RAG ready', 'var(--green)');
      setTimeout(() => setRagBanner('', ''), 3000);
    } else {
      setRagBanner(`⏳ RAG: ${p.msg} (${p.pct}%)`, 'var(--dim)');
    }
  });

  const res = await window.tscgAPI.ragInit();
  if (!res.ok) {
    setRagBanner(`⚠ RAG unavailable: ${res.error}`, 'var(--orange)');
  }
}

// ─── Round 1 ──────────────────────────────────────────────────────────────────

function buildDomainChips() {
  const covered = Object.keys(state.corpus.domain_coverage);
  $('domain-chips').innerHTML = covered.map(d =>
    `<span class="chip covered" data-domain="${d}">${d}</span>`
  ).join('');
}

function updateDomainChips(userDomain) {
  const norm = userDomain.toLowerCase().trim();
  const chips = $$('#domain-chips .chip');
  let isNew = true;

  chips.forEach(chip => {
    const d = chip.dataset.domain.toLowerCase();
    const match = d === norm || norm.includes(d) || d.includes(norm);
    chip.classList.toggle('covered', match);
    chip.classList.toggle('new', false);
    if (match) isNew = false;
  });

  // Add chip for genuinely new domain
  const existing = Array.from(chips).find(c => c.dataset.domain.toLowerCase() === norm);
  if (isNew && norm && !existing) {
    const c = document.createElement('span');
    c.className = 'chip new'; c.dataset.domain = norm;
    c.textContent = userDomain + ' ✨';
    $('domain-chips').appendChild(c);
  }

  state.isNewDomain = isNew && norm.length > 0;
  $('gap-flag').classList.toggle('hidden', !state.isNewDomain);
  $('sb-gap').textContent = state.isNewDomain ? 'Yes ✨' : 'No (known)';
  $('sb-gap').style.color = state.isNewDomain ? 'var(--gold)' : 'var(--dim)';
}


// ─── Round 2: Paste zone analysis ─────────────────────────────────────────────

// ASFID keyword signatures — ordered by specificity
const ASFID_KEYWORDS = {
  A: ['equilibrium','homeostasis','steady.?state','attractor','setpoint','set.?point',
      'stable','stability','converge','convergence','fixed.?point','balance','regulated',
      'maintained','maintained at','normal level','blood pressure','pH','temperature'],
  S: ['component','structure','boundary','interface','organ','enzyme','receptor',
      'terminal','node','layer','compartment','module','element','part','protein',
      'cell','tissue','circuit','network topology','anatomy'],
  F: ['flow','flux','current','circulation','transport','diffusion','signal',
      'hormone','electron','nutrient','blood','lymph','cascade','secretion',
      'release','uptake','absorption','emission','transfer','propagat'],
  I: ['encod','information','signal','message','code','instruct','data',
      'blueprint','DNA','RNA','gene','transcri','translat','receptor binding',
      'inhibit','activat','phosphorylat','alloster','feedback signal'],
  D: ['feedback','dynamic','oscillat','adapt','regulat','cycle','loop',
      'nonlinear','phase transition','bifurcat','chaos','amplif','damping',
      'negative feedback','positive feedback','homeostatic','allostasis','control']
};

function scoreTextForASFID(text) {
  const lower = text.toLowerCase();
  const scores = {};
  const hits   = {};

  for (const [dim, keywords] of Object.entries(ASFID_KEYWORDS)) {
    const matched = keywords.filter(kw => new RegExp(kw, 'i').test(lower));
    // Sigmoid-like scaling: 0 hits→0.3, 3 hits→0.7, 6+→0.95
    const raw = matched.length;
    scores[dim] = raw === 0 ? 0.30
                : raw === 1 ? 0.55
                : raw === 2 ? 0.65
                : raw <= 4  ? 0.75
                : raw <= 6  ? 0.85
                :             0.95;
    hits[dim] = matched.slice(0, 3); // top 3 for display
  }
  return { scores, hits };
}

function autoDocQuality(text) {
  const len = text.trim().length;
  if (len === 0)    return 0;
  if (len < 100)    return 1;
  if (len < 500)    return 2;
  return 3;
}

function handlePastedContent() {
  const ta   = $('paste-content');
  const hint = $('paste-hint');
  const row  = $('asfid-hint-row');
  if (!ta) return;

  const text = ta.value;
  state.pastedContent = text;

  // Visual feedback on textarea
  ta.classList.toggle('has-content', text.trim().length > 0);

  if (!text.trim()) {
    if (hint) hint.textContent = '';
    if (row)  row.innerHTML = '';
    return;
  }

  // ── Auto doc-quality ────────────────────────────────────────────────────
  const dq = autoDocQuality(text);
  const dqEl = $('doc-quality');
  const dqValEl = $('doc-quality-val');
  if (dqEl)    { dqEl.value = dq; state.docQuality = dq; }
  if (dqValEl) dqValEl.textContent = dq;

  // ── ASFID keyword analysis ──────────────────────────────────────────────
  const { scores, hits } = scoreTextForASFID(text);

  // Update sliders in Round 3 (may not be rendered yet — also store in state)
  for (const [dim, score] of Object.entries(scores)) {
    state.asfid[dim] = score;
    const slider = $(`slider-${dim}`);
    const val    = $(`val-${dim}`);
    if (slider) { slider.value = score; }
    if (val)    val.textContent = score.toFixed(2);
  }
  updateLiveASFID();

  // ── Show ASFID hint chips ───────────────────────────────────────────────
  if (row) {
    row.innerHTML = Object.entries(hits).map(([dim, words]) => {
      const hasHit = words.length > 0;
      const label  = hasHit
        ? `${dim}: ${words.slice(0,2).join(', ')}`
        : `${dim}: —`;
      return `<span class="asfid-hint-chip ${hasHit ? 'hit' : ''}" title="ASFID dimension ${dim}">${label}</span>`;
    }).join('');
  }

  // ── Hint message ───────────────────────────────────────────────────────
  const wordCount = text.trim().split(/\s+/).length;
  if (hint) {
    hint.textContent = `✅ ${wordCount} words analysed — doc quality set to ${dq}/3, ASFID pre-scores updated`;
    hint.style.color = 'var(--teal)';
  }

  // ── Re-run RAG with enriched query ─────────────────────────────────────
  // Debounce: wait 800ms after last keystroke before re-querying
  clearTimeout(handlePastedContent._timer);
  handlePastedContent._timer = setTimeout(() => {
    runRagSimilarPoclets();
  }, 800);
}

// ─── Round 2 ──────────────────────────────────────────────────────────────────

function buildSearchButtons() {
  const tpls   = state.corpus.web_search_templates;
  const sysEnc = encodeURIComponent(state.systemName);
  const domEnc = encodeURIComponent(state.domain);
  const slug   = state.systemName.replace(/\s+/g, '_');

  // DeepSeek query (copied to clipboard — no URL param support)
  const deepseekQuery = `Explain "${state.systemName}" as a minimal complete system in ${state.domain}. ` +
    `Does it have: (A) a stable attractor/equilibrium? (S) clear components and boundaries? ` +
    `(F) observable flows of matter/energy/information? (I) structured information encoding? ` +
    `(D) feedback loops or non-trivial dynamics? Is it well documented?`;

  const buttons = [
    { id: 'btn-deepseek',label: '🤖 DeepSeek',         url: null, clipboard: deepseekQuery },
    { id: 'btn-gemini',  label: '✨ Gemini',            url: tpls.gemini_verify.replace('{SYSTEM}', sysEnc).replace('{DOMAIN}', domEnc) },
    { id: 'btn-google',  label: '🔍 Google',           url: tpls.google.replace('{SYSTEM}', sysEnc).replace('{DOMAIN}', domEnc) },
    { id: 'btn-wiki',    label: '📖 Wikipedia',       url: tpls.wikipedia.replace('{SYSTEM}', slug) },
    { id: 'btn-scholar', label: '📚 Scholar',          url: tpls.scholar.replace('{SYSTEM}', sysEnc) },
  ];

  $('search-buttons').innerHTML = buttons.map(b =>
    `<button class="btn-search" id="${b.id}"
             data-url="${b.url || ''}"
             data-clipboard="${b.clipboard ? encodeURIComponent(b.clipboard) : ''}"
             title="${b.clipboard ? 'Copies query to clipboard, then opens DeepSeek' : b.label}">
       ${b.label}
     </button>`
  ).join('');

  // Track visited count to suggest doc-quality bump
  let visitedCount = 0;

  $$('#search-buttons .btn-search').forEach(btn => {
    btn.addEventListener('click', async () => {
      // DeepSeek: copy query to clipboard first, then open chat
      if (btn.dataset.clipboard) {
        try {
          await navigator.clipboard.writeText(decodeURIComponent(btn.dataset.clipboard));
          btn.textContent = '🤖 DeepSeek ✅ (query copied)';
          btn.style.borderColor = 'var(--teal)';
        } catch {
          btn.textContent = '🤖 DeepSeek (copy failed)';
        }
        window.tscgAPI.openURL('https://chat.deepseek.com/');
      } else {
        window.tscgAPI.openURL(btn.dataset.url);
      }

      // Visual visited feedback
      btn.classList.add('visited');
      visitedCount++;

      // After 2+ sources opened, suggest bumping doc-quality
      if (visitedCount === 2) {
        const hint = $('doc-quality-hint');
        if (hint) {
          hint.textContent = '💡 Found documentation? Adjust quality above.';
          hint.classList.remove('hidden');
        }
      }
    });
  });
}

async function runRagSimilarPoclets() {
  const container = $('rag-poclets-results');
  if (!container) return;

  if (!state.ragReady) {
    container.innerHTML = `<div class="rag-note">⏳ RAG still loading — try again in a moment.</div>`;
    return;
  }

  container.innerHTML = `<div class="rag-note">🔍 Searching corpus…</div>`;
  const contextSnippet = state.pastedContent ? state.pastedContent.slice(0, 300) : '';
  const query = `${state.systemName} ${state.domain} system feedback regulation ${contextSnippet}`.trim();
  const res   = await window.tscgAPI.ragQuery({ query, mode: 'similar_poclets', topK: 5 });

  if (!res.ok) {
    container.innerHTML = `<div class="rag-note" style="color:var(--orange)">⚠ ${res.error}</div>`;
    return;
  }

  const items = res.results.filter(r => !r.isCandidate);
  if (!items.length) {
    container.innerHTML = `<div class="rag-note">No close matches in corpus — likely a new domain. ✨</div>`;
    return;
  }

  const warning = items[0].score > 0.88
    ? `<div class="rag-warning">⚠ High similarity to <strong>${items[0].name}</strong> (${items[0].score}) — verify this isn't already modelled.</div>`
    : '';

  container.innerHTML = warning + items.map(r => `
    <div class="rag-row">
      <span class="rag-name">${r.name}</span>
      <span class="rag-domain">${r.domain}</span>
      <span class="rag-score">${r.score}</span>
    </div>
  `).join('');
}

// ─── Round 3 ──────────────────────────────────────────────────────────────────

function buildASFIDQuestions() {
  $('asfid-questions').innerHTML = ASFID_QUESTIONS.map(q => `
    <div class="asfid-question">
      <div class="q-label"><span class="dim-badge">${q.dim}</span><strong>${q.label}</strong></div>
      <div style="font-size:12px;color:var(--text);">${q.question}</div>
      <div style="font-size:11px;color:var(--dim);">💡 ${q.hint}</div>
      <div style="display:flex;align-items:center;gap:10px;margin-top:4px;">
        <span style="font-size:11px;color:var(--dim);">0</span>
        <input type="range" class="score-slider" id="slider-${q.dim}" min="0" max="1" step="0.05" value="0.5">
        <span style="font-size:11px;color:var(--dim);">1</span>
        <span class="score-value" id="val-${q.dim}">0.50</span>
      </div>
    </div>
  `).join('');

  ASFID_QUESTIONS.forEach(q => {
    $(`slider-${q.dim}`).addEventListener('input', () => {
      const v = parseFloat($(`slider-${q.dim}`).value);
      state.asfid[q.dim] = v;
      $(`val-${q.dim}`).textContent = v.toFixed(2);
      updateLiveASFID();
    });
  });
}

function updateLiveASFID() {
  let sum = 0;
  ['A','S','F','I','D'].forEach(d => {
    const v = state.asfid[d]; sum += v;
    $(`bar-${d}`).style.width = (v * 100) + '%';
    $(`num-${d}`).textContent  = v.toFixed(2);
  });
  $('asfid-mean').textContent = (sum / 5).toFixed(2);
}

// ─── Round 4 ──────────────────────────────────────────────────────────────────

function bindTypeCards() {
  $$('.type-card').forEach(card => {
    card.addEventListener('click', () => {
      $$('.type-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      state.candidateType = card.dataset.type;
      $('sb-type').textContent = state.candidateType;
      $('transdisclet-warning').classList.toggle('hidden', state.candidateType !== 'TransDisclet');
    });
  });
}

// ─── Round 5 ──────────────────────────────────────────────────────────────────

function buildInvariantChecklist() {
  if (!state.corpus) return;
  $('inv-checklist').innerHTML = state.corpus.invariants.criteria.map(c => `
    <div class="inv-row">
      <input type="checkbox" id="inv-${c.id}" data-id="${c.id}">
      <div>
        <div class="inv-id">${c.id} — weight ${c.weight}</div>
        <div class="inv-text">${c.question}</div>
        <div style="font-size:10px;color:var(--dim);margin-top:2px;">
          ✅ ${(c.examples_ok || []).slice(0,2).join(' · ')}
        </div>
      </div>
    </div>
  `).join('');
}

async function runRagSuggestConcepts() {
  const container = $('rag-concepts-results');
  if (!container) return;

  if (!state.ragReady) {
    container.innerHTML = `<div class="rag-note">⏳ RAG still loading…</div>`;
    return;
  }

  container.innerHTML = `<div class="rag-note">🔍 Querying M2 GenericConcepts…</div>`;
  const query = `${state.systemName} ${state.domain} ${state.candidateType || ''} feedback regulation flow dynamics`;
  const res   = await window.tscgAPI.ragQuery({ query, mode: 'suggest_concepts', topK: 6 });

  if (!res.ok) {
    container.innerHTML = `<div class="rag-note" style="color:var(--orange)">⚠ ${res.error}</div>`;
    return;
  }

  state.suggestedConcepts = res.results;
  container.innerHTML = res.results.map(r => `
    <div class="rag-row rag-concept-row" data-id="${r.id}">
      <label style="display:flex;align-items:center;gap:8px;cursor:pointer;width:100%;">
        <input type="checkbox" class="concept-check" data-id="${r.id}" data-label="${r.label}" checked style="accent-color:var(--purple);">
        <span class="rag-name" style="color:var(--purple);">${r.label}</span>
        <span class="rag-formula" style="color:var(--dim);font-size:10px;">${r.formula}</span>
        <span class="rag-score" style="margin-left:auto;">${r.score}</span>
      </label>
    </div>
  `).join('');
}

function buildPriorityList() {
  if (!state.corpus) return;

  const candidates = state.corpus.gap_analysis.priority_candidates.slice(0, 8);

  $('priority-list').innerHTML = [
    `<div style="font-size:11px;color:var(--dim);margin-bottom:6px;">
       💡 No idea yet? Click a suggestion below to use it as your starting point
     </div>`,
    ...candidates.map(c => `
      <div class="cand-row cand-clickable"
           data-system="${c.system}"
           data-domain="${c.domain}"
           data-type="${c.type}"
           title="Click to start with: ${c.system}">
        <div>
          <div class="cand-name">${c.system}</div>
          <div class="cand-dom">${c.domain}</div>
        </div>
        <div style="display:flex;flex-direction:column;align-items:flex-end;gap:2px;">
          <span class="cand-type">${c.type}</span>
          ${c.priority === 'high'
            ? '<span style="font-size:9px;color:var(--gold);">★ high priority</span>'
            : '<span style="font-size:9px;color:var(--dim);">medium</span>'}
        </div>
      </div>
    `)
  ].join('');

  // Click → pre-fill Round 1 and advance to Round 2
  $$('#priority-list .cand-clickable').forEach(row => {
    row.addEventListener('click', () => {
      const system = row.dataset.system;
      const domain = row.dataset.domain;

      // Update state
      state.systemName = system;
      state.domain     = domain;

      // Update DOM inputs
      $('inp-system').value = system;
      $('inp-domain').value = domain;

      // Update sidebar
      $('sb-system').textContent = system;
      $('sb-domain').textContent = domain;

      // Update domain chips
      updateDomainChips(domain);

      // Advance to Round 2 (triggers web search buttons + RAG)
      buildSearchButtons();
      runRagSimilarPoclets();
      state.currentRound = 2;
      showRound(2);
    });
  });
}

// ─── Verdict engine ───────────────────────────────────────────────────────────

function computeVerdict() {
  let invCount = 0;
  $$('#inv-checklist input[type="checkbox"]').forEach(cb => {
    if (cb.checked) invCount++;
    state.invariantChecks[cb.dataset.id] = cb.checked;
  });

  const asfidMean = ['A','S','F','I','D'].reduce((s,d) => s + state.asfid[d], 0) / 5;
  const t = state.corpus.scoring_thresholds.verdict;

  let verdict, cls;
  if (invCount >= t.strong_candidate.invariants_min && asfidMean >= t.strong_candidate.asfid_min)
    { verdict = '🟢 Strong Candidate'; cls = 'strong'; }
  else if (invCount >= t.candidate.invariants_min && asfidMean >= t.candidate.asfid_min)
    { verdict = '🟡 Candidate'; cls = 'cand'; }
  else if (invCount >= t.weak_candidate.invariants_min && asfidMean >= t.weak_candidate.asfid_min)
    { verdict = '🟠 Weak Candidate'; cls = 'weak'; }
  else
    { verdict = '🔴 Rejected'; cls = 'reject'; }

  state.verdict = { verdict, cls, invCount, asfidMean, docQuality: state.docQuality };

  $('verdict-box').className = `verdict-box ${cls}`;
  $('verdict-label').textContent = verdict;
  $('v-inv').textContent   = invCount;
  $('v-asfid').textContent = asfidMean.toFixed(2);
  $('v-doc').textContent   = state.docQuality;

  const details = {
    strong: 'Excellent candidate. Proceed directly to M0 poclet scaffolding.',
    cand:   'Good candidate. Refine ASFID scores or document edge cases before scaffolding.',
    weak:   'Borderline candidate. Strengthen evidence and re-evaluate invariants.',
    reject: 'Not suitable as a poclet. Reframe the system or choose a different candidate.'
  };
  $('verdict-detail').textContent = details[cls];
  $('verdict-section').style.display = 'flex';

  buildGeminiButton();
}

function buildGeminiButton() {
  const url = state.corpus.web_search_templates.gemini_suggest
    .replace('{DOMAIN}', encodeURIComponent(state.domain));
  $('gemini-buttons').innerHTML =
    `<button class="btn-search gemini" data-url="${url}">✨ Gemini: suggest more in ${state.domain || 'this domain'}</button>`;
  $$('#gemini-buttons .btn-search').forEach(btn =>
    btn.addEventListener('click', () => window.tscgAPI.openURL(btn.dataset.url))
  );
}

// ─── Export ───────────────────────────────────────────────────────────────────

async function exportCandidate() {
  // Collect checked RAG concept suggestions
  const checkedConcepts = [];
  $$('.concept-check').forEach(cb => {
    if (cb.checked) checkedConcepts.push(cb.dataset.id);
  });

  const slug = (state.systemName || 'unknown').toLowerCase().replace(/\s+/g, '_');
  const data = {
    _tscg_scaffold: true,
    system:   state.systemName,
    domain:   state.domain,
    type:     state.candidateType,
    verdict:  state.verdict,
    asfid_prescores: state.asfid,
    doc_quality: state.docQuality,
    is_new_domain: state.isNewDomain,
    invariants_checked: state.invariantChecks,
    suggested_generic_concepts: checkedConcepts,
    pasted_content_excerpt: state.pastedContent ? state.pastedContent.slice(0, 500) : '',
    system_slug: slug,
    generated: new Date().toISOString()
  };
  const result = await window.tscgAPI.exportCandidate(data);
  if (result.ok) alert(`✅ Exported to:\n${result.path}`);
  else           alert(`❌ Export failed: ${result.error}`);
}

// ─── Navigation ───────────────────────────────────────────────────────────────

function canAdvance() {
  if (state.currentRound === 1) return state.systemName.trim() && state.domain.trim();
  if (state.currentRound === 4) return state.candidateType !== null;
  return true;
}

function goNext() {
  if (!canAdvance()) return;
  if (state.currentRound === 1) buildSearchButtons();
  if (state.currentRound === 1) runRagSimilarPoclets();   // fire after advancing to round 2
  if (state.currentRound === 4) runRagSuggestConcepts();  // fire after advancing to round 5
  state.currentRound++;
  showRound(state.currentRound);
}

function goPrev() {
  if (state.currentRound > 1) { state.currentRound--; showRound(state.currentRound); }
}

function restart() {
  Object.assign(state, {
    currentRound: 1, systemName: '', domain: '', isNewDomain: false,
    docQuality: 2, candidateType: null,
    asfid: { A:0.5, S:0.5, F:0.5, I:0.5, D:0.5 },
    invariantChecks: {}, suggestedConcepts: [], verdict: null
  });
  $('inp-system').value = ''; $('inp-domain').value = '';
  const pz = $('paste-content'); if (pz) { pz.value = ''; pz.classList.remove('has-content'); }
  const ph = $('paste-hint');    if (ph) ph.textContent = '';
  const pr = $('asfid-hint-row');if (pr) pr.innerHTML = '';
  $('doc-quality').value = 2; $('doc-quality-val').textContent = '2';
  ASFID_QUESTIONS.forEach(q => {
    const s = $(`slider-${q.dim}`); if (s) s.value = 0.5;
    const v = $(`val-${q.dim}`);   if (v) v.textContent = '0.50';
  });
  $$('.type-card').forEach(c => c.classList.remove('selected'));
  $('verdict-section').style.display = 'none';
  const rpr = $('rag-poclets-results');    if (rpr) rpr.innerHTML = '';
  const rcr = $('rag-concepts-results');   if (rcr) rcr.innerHTML = '';
  updateLiveASFID();
  buildDomainChips();
  showRound(1);
}

// ─── Bind all events ──────────────────────────────────────────────────────────

function bindEvents() {
  $('btn-next').addEventListener('click', goNext);
  $('btn-prev').addEventListener('click', goPrev);
  $('btn-compute').addEventListener('click', computeVerdict);
  $('btn-restart').addEventListener('click', restart);
  $('btn-export').addEventListener('click', exportCandidate);

  $('inp-system').addEventListener('input', e => {
    state.systemName = e.target.value;
    $('sb-system').textContent = state.systemName || '—';
  });
  $('inp-domain').addEventListener('input', e => {
    state.domain = e.target.value;
    $('sb-domain').textContent = state.domain || '—';
    updateDomainChips(state.domain);
  });
  $('doc-quality').addEventListener('input', e => {
    state.docQuality = parseInt(e.target.value);
    $('doc-quality-val').textContent = state.docQuality;
  });

  // Paste zone (Round 2)
  const pasteEl = $('paste-content');
  if (pasteEl) {
    pasteEl.addEventListener('input', handlePastedContent);
    pasteEl.addEventListener('paste', () => setTimeout(handlePastedContent, 50));
  }
  bindTypeCards();

  // ── RAG DB Restore Modal ─────────────────────────────────────────────────
  const btnOpenModal  = $('btn-open-rag-modal');
  const modal         = $('rag-restore-modal');
  const btnModalClose = $('btn-modal-close');
  const btnPickArc    = $('btn-pick-archive');
  const btnPickOut    = $('btn-pick-outdir');
  const btnRestore    = $('btn-restore-start');
  const arcInput      = $('rag-archive-path');
  const outInput      = $('rag-out-dir');
  const logEl         = $('rag-restore-log');
  const statusEl      = $('restore-status');

  if (btnOpenModal) {
    btnOpenModal.addEventListener('click', () => modal.classList.remove('hidden'));
  }
  if (btnModalClose) {
    btnModalClose.addEventListener('click', () => modal.classList.add('hidden'));
  }
  // Close on overlay click
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.add('hidden');
    });
  }

  if (btnPickArc) {
    btnPickArc.addEventListener('click', async () => {
      const file = await window.tscgAPI.pickArchive();
      if (file) arcInput.value = file;
    });
  }
  if (btnPickOut) {
    btnPickOut.addEventListener('click', async () => {
      const dir = await window.tscgAPI.pickOutDir();
      if (dir) outInput.value = dir;
    });
  }

  if (btnRestore) {
    btnRestore.addEventListener('click', async () => {
      const archiveFile = arcInput  && arcInput.value.trim();
      const outDir      = outInput  && outInput.value.trim();
      if (!archiveFile) { statusEl.textContent = '⚠ Select an archive first.'; statusEl.style.color = 'var(--orange)'; return; }
      if (!outDir)      { statusEl.textContent = '⚠ Select an output directory.'; statusEl.style.color = 'var(--orange)'; return; }

      // Clear log, show it
      logEl.textContent = '';
      logEl.classList.add('visible');
      statusEl.textContent = '⏳ Extracting…';
      statusEl.style.color = 'var(--dim)';
      btnRestore.disabled  = true;

      // Stream progress messages
      window.tscgAPI.onRagDbProgress((msg) => {
        logEl.textContent += msg + '\n';
        logEl.scrollTop = logEl.scrollHeight;
      });

      const result = await window.tscgAPI.restoreRag(archiveFile, outDir);
      window.tscgAPI.offRagDbProgress();

      if (result.ok) {
        statusEl.textContent = `✅ Done — ${result.filesExtracted} files in ${result.volumeCount} volume(s)`;
        statusEl.style.color = 'var(--green)';
        logEl.textContent += `\nDB directory: ${result.dbDir}`;
      } else {
        statusEl.textContent = `❌ ${result.error}`;
        statusEl.style.color = 'var(--red)';
      }
      btnRestore.disabled = false;
    });
  }


  // Refresh Corpus button
  const btnRefresh = $('btn-refresh-corpus');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', async () => {
      btnRefresh.textContent = '⏳ Rebuilding…';
      btnRefresh.disabled = true;
      try {
        const result = await window.tscgAPI.rebuildCorpus();
        if (result.ok) {
          // Reload corpus state
          const cr = await window.tscgAPI.loadCorpus();
          if (cr.ok) {
            state.corpus = cr.data;
            $('corpus-count').textContent  = state.corpus.corpus_stats.total;
            $('domains-count').textContent = state.corpus.corpus_stats.domains_covered;
            buildDomainChips();
            buildPriorityList();
            buildInvariantChecklist();
          }
          // Re-init RAG with new corpus
          state.ragReady = false;
          state.ragInitiated = false;
          startRagInit();
          setRagBanner(`✅ Corpus refreshed: ${result.total} instances, ${result.domains} domains`, 'var(--green)');
          setTimeout(() => setRagBanner('', ''), 4000);
        } else {
          setRagBanner(`❌ Rebuild failed: ${result.error}`, 'var(--red)');
        }
      } finally {
        btnRefresh.textContent = '⟳ Refresh Corpus';
        btnRefresh.disabled = false;
      }
    });
  }

}

document.addEventListener('DOMContentLoaded', init);
