/* ══════════════════════════════════════════════════════════════
   TSCG POCLET SIMULATION SHELL — reusable behaviour
   Author: Echopraxium with the collaboration of Claude AI
   Version: 1.0.0

   Chrome behaviour shared by every poclet simulation:
     • tab switching
     • a WORKING splitter (the earlier templates declared one in
       CSS but never wired it up)
     • an on-screen diagnostic console
     • BabylonJS screenshot export
     • score bar rendering from a scores object

   Load BEFORE the poclet's own script. Exposes window.TSCG.
   The poclet script must set TSCG.engine / TSCG.camera for the
   screenshot helper to work.
   ══════════════════════════════════════════════════════════════ */
'use strict';

window.TSCG = (function () {

  const api = {
    engine: null,      // set by the poclet script
    camera: null,      // set by the poclet script
    pocletId: 'poclet'
  };

  // ── Diagnostics ────────────────────────────────
  // Simulations are opened as files as often as they are served, so a
  // visible console beats devtools for reporting what actually failed.
  const _lines = [];
  function _paint() {
    const el = document.getElementById('diag');
    if (el) el.innerHTML = _lines.join('\n');
  }
  api.log  = m => { _lines.push('  ' + m); _paint(); };
  api.ok   = m => { _lines.push('<b>' + m + '</b>'); _paint(); };
  api.fail = (m, d) => {
    _lines.push('<b>FAILED — ' + m + '</b>' + (d ? '\n   ' + d : ''));
    const el = document.getElementById('diag');
    if (el) el.classList.add('fail');
    _paint();
  };
  api.toggleDiag = () => {
    const el = document.getElementById('diag');
    if (el) el.classList.toggle('on');
  };

  window.addEventListener('error', e => {
    const w = e.filename ? (' at ' + String(e.filename).split('/').pop() + ':' + e.lineno) : '';
    api.fail('Script error' + w, e.message || 'unknown');
  });
  window.addEventListener('unhandledrejection', e => {
    api.fail('Promise rejected', String(e.reason && e.reason.message ? e.reason.message : e.reason));
  });

  // ── Tabs ───────────────────────────────────────
  api.activateTab = function (index) {
    document.querySelectorAll('.tab-btn')
      .forEach((b, i) => b.classList.toggle('active', i === index));
    document.querySelectorAll('.tab-panel')
      .forEach((p, i) => p.classList.toggle('active', i === index));
  };

  // ── Splitter ───────────────────────────────────
  // Drives --sidebar-w on :root. The grid re-flows, so the canvas
  // container changes size and the engine must be told to resize.
  api.initSplitter = function (opts) {
    const o = Object.assign({ min: 260, max: 720 }, opts || {});
    const el = document.getElementById('splitter');
    if (!el) return;
    let dragging = false;

    const apply = px => {
      const w = Math.max(o.min, Math.min(o.max, px));
      document.documentElement.style.setProperty('--sidebar-w', w + 'px');
      if (api.engine) api.engine.resize();
    };

    const onMove = e => {
      if (!dragging) return;
      const x = (e.touches ? e.touches[0].clientX : e.clientX);
      apply(window.innerWidth - x);
      e.preventDefault();
    };
    const stop = () => {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('dragging');
      document.body.style.cursor = '';
      if (api.engine) api.engine.resize();
    };
    const start = e => {
      dragging = true;
      el.classList.add('dragging');
      document.body.style.cursor = 'col-resize';
      e.preventDefault();
    };

    el.addEventListener('mousedown', start);
    el.addEventListener('touchstart', start, { passive: false });
    window.addEventListener('mousemove', onMove);
    window.addEventListener('touchmove', onMove, { passive: false });
    window.addEventListener('mouseup', stop);
    window.addEventListener('touchend', stop);

    // Double-click restores the default width
    el.addEventListener('dblclick', () => apply(360));
  };

  // ── Screenshot ─────────────────────────────────
  api.exportScreenshot = function () {
    if (!api.engine || !api.camera) {
      api.fail('Screenshot unavailable', 'TSCG.engine / TSCG.camera not set');
      return;
    }
    BABYLON.Tools.CreateScreenshot(api.engine, api.camera, { width: 1920, height: 1080 }, data => {
      const a = document.createElement('a');
      a.href = data;
      a.download = api.pocletId + '_' + Date.now() + '.png';
      a.click();
    });
  };

  // ── Score bars ─────────────────────────────────
  // scores = { A,S,F,It,D, R,E,V,O,Im } in [0,1]
  const DIM_COLOR = {
    A:'#f78166', S:'#56d364', F:'#79c0ff', It:'#d2a8ff', D:'#e3b341',
    R:'#79c0ff', E:'#56d364', V:'#f78166', O:'#d2a8ff', Im:'#e3b341'
  };
  const GAP_CLASS = g =>
    g < 0.05 ? ['Coherent',       'Map and Territory tightly aligned'] :
    g < 0.15 ? ['OnCriticalLine', 'Map and Territory balanced'] :
    g < 0.30 ? ['Divergent',      'Map and Territory pulling apart'] :
               ['Enigmatic',      'Map and Territory in tension'];

  api.renderScores = function (hostId, scores) {
    const host = document.getElementById(hostId);
    if (!host) return;
    const row = (d, v) =>
      `<div class="score-row">
         <span class="score-dim" style="color:${DIM_COLOR[d]}">${d}</span>
         <div class="score-bar-bg"><div class="score-bar-fill"
              style="width:${(v*100).toFixed(0)}%;background:${DIM_COLOR[d]}"></div></div>
         <span class="score-val">${v.toFixed(2)}</span>
       </div>`;

    const asfid = ['A','S','F','It','D'], revoi = ['R','E','V','O','Im'];
    const mean = ks => ks.reduce((a,k) => a + scores[k], 0) / ks.length;
    const mA = mean(asfid), mR = mean(revoi), gap = Math.abs(mR - mA);
    const [cls, desc] = GAP_CLASS(gap);

    host.innerHTML =
      `<div class="score-group">
         <div class="score-group-label eagle">ASFID — Territory (Eagle Eye)</div>
         ${asfid.map(d => row(d, scores[d])).join('')}
         <div class="score-mean">mean = <b>${mA.toFixed(2)}</b></div>
       </div>
       <div class="score-group">
         <div class="score-group-label sphinx">REVOI — Map (Sphinx Eye)</div>
         ${revoi.map(d => row(d, scores[d])).join('')}
         <div class="score-mean">mean = <b>${mR.toFixed(2)}</b></div>
       </div>
       <div class="gap-badge">
         <div class="gap-label">Epistemic Gap δ₁</div>
         <div class="gap-val">${gap.toFixed(3)}</div>
         <div class="gap-desc">${cls} — REVOI ${mR.toFixed(2)} vs ASFID ${mA.toFixed(2)}<br>${desc}</div>
       </div>`;
  };

  // ── M2 concept list ────────────────────────────
  // concepts = [{ name, formula, family, familyColor, desc, role }]
  api.renderConcepts = function (hostId, concepts) {
    const host = document.getElementById(hostId);
    if (!host) return;
    const byFamily = {};
    for (const c of concepts) (byFamily[c.family] = byFamily[c.family] || []).push(c);

    host.innerHTML = Object.entries(byFamily).map(([fam, list]) => {
      const col = list[0].familyColor || '#79c0ff';
      return `<div class="concept-family">
        <h4 style="color:${col};border-bottom-color:${col}33">● ${fam} (${list.length})</h4>
        ${list.map(c => `
          <div class="concept-item">
            <div class="concept-head">
              <span class="concept-name">${c.name}</span>
              <span class="concept-formula">${c.formula}</span>
            </div>
            <p class="concept-desc">${c.desc}</p>
            <p class="concept-role"><strong>Role:</strong> ${c.role}</p>
          </div>`).join('')}
      </div>`;
    }).join('');
  };

  return api;
})();

// Global aliases kept for inline handlers in the markup
function activateTab(i) { window.TSCG.activateTab(i); }
function exportScreenshot() { window.TSCG.exportScreenshot(); }
