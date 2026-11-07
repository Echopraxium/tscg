/* TSCG Kit — app.js
 * The workshop shell, identical for every workshop:
 *   top row    : tutorial banner (left) | tabs [Scale model | Curves] (right)
 *   bottom row : tabs [Synoptic | Panel], full width
 * Owns the clock, the main loop, "under the hood", free mode, the language
 * switch and the session export.
 * Usage: TSCGKit.start(factory), where factory(L) returns the workshop definition
 * with every text written as L(english, french).
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const VERSION = "0.9.2";
  const SPEEDS = [0.25, 0.5, 1, 2, 4, 8, 16];
  const LAYOUT_KEY = "tscg-kit-layout";
  const build = factory => factory((en, fr) => (K.lang === "fr" ? fr : en));

  K.start = function (factory) {
    let W = typeof factory === "function" ? build(factory) : factory;
    // the workshop's clock: model time per step, steps per real second at ×1, formatting
    const CLK = Object.assign({}, K.CLOCK_HOURS, W.clock || {});
    document.documentElement.lang = K.lang;
    document.body.innerHTML =
      `<header class="k-header">
         <a class="k-home" id="kHome" data-tip="home_tip"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11 L12 3.8 L21 11 M5.5 9.5 V20 H18.5 V9.5 M10 20 V14.5 H14 V20"/></svg></a>
         <h1 id="kTitle"></h1>
         <div class="k-transport">
           <button id="kPlay" class="primary" data-tip="play_tip"></button>
           <button id="kSlow" class="k-arrow" data-tip="speed_down">▼</button>
           <span id="kSpeed" class="k-speed" data-tip="speed_label"></span>
           <button id="kFast" class="k-arrow" data-tip="speed_up">▲</button>
           <button id="kReset" data-tip="reset_tip">↺</button>
           <span id="kClock" class="k-clock"></span>
         </div>
         <span class="k-spacer"></span>
         <button id="kHood" data-t="hood" data-tip="hood_tip"></button>
         <button id="kFree" data-t="free" data-tip="free_tip"></button>
         <button id="kExport" data-t="export" data-tip="export_tip"></button>
         <button id="kLang" class="k-lang" data-t="lang_btn" data-tip="lang_tip"></button>
         <button id="kTheme" class="k-theme" data-tip="theme_tip"></button>
       </header>
       <main class="k-main">
         <div class="k-banner" id="kBanner" aria-live="polite"></div>
         <div class="k-split k-split-v" id="kSplitCols"></div>
         <section class="k-right">
           <div class="k-tabs" role="tablist">
             <button class="k-rtab active" role="tab" data-rtab="maquette" data-t="maquette"></button>
             <button class="k-rtab" role="tab" data-rtab="curves" data-t="curves"></button>
           </div>
           <div class="k-rpanes">
             <div class="k-maquette k-rpane active" data-rpane="maquette"><div class="k-view" id="kView"></div></div>
             <div class="k-curves k-rpane" data-rpane="curves"><canvas id="kChart"></canvas><div class="k-legend" id="kLegend"></div></div>
           </div>
         </section>
         <div class="k-split k-split-h" id="kSplitBanner"></div>
         <section class="k-left">
           <div class="k-tabs" role="tablist">
             <button class="k-tab" role="tab" data-tab="synoptic" data-t="tab_syn"></button>
             <button class="k-tab" role="tab" data-tab="panel" data-t="tab_panel"></button>
             <div class="k-tools" role="toolbar" data-tipl="tools">
               <button id="kToolClear" class="k-tool">${K.iconSvg("clearall", "k-ticon")}</button>
               <button id="kToolErase" class="k-tool">${K.iconSvg("eraser", "k-ticon")}</button>
               <span class="k-tsep"></span>
               <button id="kToolSnap" class="k-tool" aria-pressed="true">${K.iconSvg("grid", "k-ticon")}</button>
             </div>
           </div>
           <div class="k-panes">
             <div class="k-pane k-pane-panel" data-pane="panel"></div>
             <div class="k-pane k-pane-synoptic" data-pane="synoptic"></div>
           </div>
         </section>
       </main>
       <div class="k-toast" id="kToast" role="status"></div>`;
    const $ = sel => document.querySelector(sel);

    const S = { running: false, speed: 1, hood: false, free: false, tab: "synoptic", rtab: "maquette",
                pieces: new Set(), instruments: new Set(), log: [], t0: Date.now(),
                predictions: {}, answers: null, done: false };
    const model = new K.Model(W.skins);
    const log = (type, detail) => S.log.push({ t: +((Date.now() - S.t0) / 1000).toFixed(1), sim: +model.t.toFixed(3), type, detail: detail === undefined ? "" : detail });
    model.on(log);
    let toastTimer = null;
    const toast = msg => { const t = $("#kToast"); t.textContent = msg; t.classList.add("show"); clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove("show"), 2800); };

    const app = { S, model, log, toast, W, clock: CLK, fmtSteps: CLK.fmtSteps };
    const changed = () => { app.panel.renderToolbar(); app.panel.update(); app.tutorial.refresh(); };
    app.synoptic = new K.Synoptic($('[data-pane="synoptic"]'), model, {
      order: W.order, home: W.home, fluxLabel: () => app.W.fluxLabel,
      isUnlocked: t => S.free || S.pieces.has(t), hood: () => S.hood, toast, onChange: changed });
    app.panel = new K.Panel($('[data-pane="panel"]'), model, {
      instruments: W.instruments, skins: W.skins,
      isUnlocked: k => (S.free || S.instruments.has(k)), toast, log, onChange: () => app.tutorial.refresh() });
    app.view = W.view($("#kView"), model, { log, toast, hood: () => S.hood, running: () => S.running });
    app.chart = new K.Chart($("#kChart"), model, Object.assign({}, W.chart, { legendEl: $("#kLegend"), app }));

    app.running = () => S.running;
    app.unlock = u => {
      (u.pieces || []).forEach(p => S.pieces.add(p));
      (u.instruments || []).forEach(i => S.instruments.add(i));
      app.synoptic.renderPalette(); app.panel.renderToolbar();
    };
    app.attention = tab => document.querySelectorAll(".k-tab").forEach(b => b.classList.toggle("attn", b.dataset.tab === tab && tab !== S.tab));
    app.goTab = tab => {
      S.tab = tab;
      document.querySelectorAll(".k-tab").forEach(b => { b.classList.toggle("active", b.dataset.tab === tab); b.setAttribute("aria-selected", b.dataset.tab === tab); });
      document.querySelectorAll(".k-pane").forEach(p => p.classList.toggle("active", p.dataset.pane === tab));
      if (tab === "synoptic") app.synoptic.render(); else app.panel.render();
      log("tab", tab); app.tutorial.refresh();
    };
    // right column: the scale model and the curves share one compartment, as two tabs
    app.goRTab = tab => {
      S.rtab = tab;
      document.querySelectorAll(".k-rtab").forEach(b => { b.classList.toggle("active", b.dataset.rtab === tab); b.setAttribute("aria-selected", b.dataset.rtab === tab); b.classList.remove("attn"); });
      document.querySelectorAll(".k-rpane").forEach(p => p.classList.toggle("active", p.dataset.rpane === tab));
      if (tab === "curves") app.chart.draw();
      log("rtab", tab);
    };
    // ---- toolbar of the bottom tabs: clear everything (two clicks), erase the selection, snap (Panel)
    let clearArmed = 0;
    $("#kToolClear").onclick = () => {
      if (Date.now() - clearArmed > 3000) { clearArmed = Date.now(); $("#kToolClear").classList.add("armed"); toast(K.t("tool_clear_confirm")); return; }
      clearArmed = 0; $("#kToolClear").classList.remove("armed");
      app.synoptic.clear(); app.panel.clear(); log("clear_all", ""); app.tutorial.refresh();
    };
    $("#kToolErase").onclick = () => { if (S.tab === "synoptic") app.synoptic.deleteSelected(); else app.panel.deleteSelected(); };
    $("#kToolSnap").onclick = () => app.panel.setSnap(!app.panel.snap);
    app.updateTools = () => {
      const syn = S.tab === "synoptic", e = $("#kToolErase"), sn = $("#kToolSnap"), c = $("#kToolClear");
      e.disabled = syn ? !app.synoptic.selected : !app.panel.controls.some(x => x.id === app.panel.selected);
      e.title = K.t(syn ? "tool_erase" : "tool_erase_pn");
      sn.hidden = syn; $(".k-tsep").hidden = syn; sn.classList.toggle("on", app.panel.snap); sn.setAttribute("aria-pressed", app.panel.snap); sn.title = K.t("tool_snap");
      c.title = K.t("tool_clear"); c.disabled = !model.nodes.length && !app.panel.controls.length;
      if (clearArmed && Date.now() - clearArmed > 3000) { clearArmed = 0; c.classList.remove("armed"); }
    };
    // the scale model fills its compartment: the drawing keeps its proportions (it is centred,
    // never stretched) and the viewBox grows to the compartment's shape, so the scene's
    // background runs to the edges with an equal margin on the four sides
    const fitView = () => {
      const host = $("#kView"), svg = host && host.querySelector("svg"); if (!svg) return;
      const r = host.getBoundingClientRect(); if (!r.width || !r.height) return;
      const key = Math.round(r.width) + "x" + Math.round(r.height); if (svg.dataset.fit === key) return;
      svg.dataset.fit = key;
      const [bx, by, bw, bh] = (svg.dataset.base || (svg.dataset.base = svg.getAttribute("viewBox"))).split(/[\s,]+/).map(Number);
      const s = Math.min(r.width / bw, r.height / bh), vw = r.width / s, vh = r.height / s;
      svg.setAttribute("viewBox", `${(bx - (vw - bw) / 2).toFixed(1)} ${(by - (vh - bh) / 2).toFixed(1)} ${vw.toFixed(1)} ${vh.toFixed(1)}`);
    };
    app.fitView = fitView;
    app.curvesHint = on => { const b = document.querySelector('.k-rtab[data-rtab="curves"]'); if (b) b.classList.toggle("attn", on && S.rtab !== "curves"); };
    app.goFree = () => {
      S.free = true; $("#kFree").classList.add("on");
      app.tutorial.mode = "free"; log("mode_free", "");
      app.synoptic.renderPalette(); app.panel.renderToolbar(); app.tutorial.render();
    };
    app.backToTutorial = () => {
      S.free = false; $("#kFree").classList.remove("on"); log("mode_tutorial", "");
      app.synoptic.renderPalette(); app.panel.renderToolbar();
      app.tutorial.start(S.done ? 0 : app.tutorial.i);
    };
    app.tutorial = new K.Tutorial($("#kBanner"), W, app);

    // ---- static labels, re-applied on a language switch
    const playLabel = () => { $("#kPlay").textContent = K.t(S.running ? "pause" : "play"); };
    function relabel() {
      document.title = app.W.pageTitle || app.W.title;
      $("#kTitle").textContent = app.W.title;
      $("#kHome").href = (app.W.homeUrl || "../index.html") + "?lang=" + K.lang;
      document.querySelectorAll("[data-t]").forEach(e => { e.textContent = K.t(e.dataset.t); });
      document.querySelectorAll("[data-tip]").forEach(e => { e.title = K.t(e.dataset.tip); });
      playLabel();
      $("#kSpeed").textContent = app.speedText ? app.speedText() : "";
    }
    // Switching language rebuilds the workshop texts; the graph, the panel, the clock and
    // the tutorial progress are kept.
    app.setLang = lang => {
      K.setLang(lang);
      if (typeof factory === "function") {
        const W2 = build(factory);
        app.W = W2; model.skins = W2.skins;
        app.tutorial.W = W2; app.tutorial.steps = W2.steps;
        app.panel.o.instruments = W2.instruments; app.panel.o.skins = W2.skins;
        app.chart.o = Object.assign({}, W2.chart, { legendEl: $("#kLegend"), app });
      }
      log("lang", lang);
      relabel(); app.synoptic.relabel(); app.panel.relabel();
      app.synoptic.renderPalette(); app.synoptic.render(); app.synoptic.renderParams();
      app.panel.render(); app.tutorial.render();
      try { const u = new URL(location.href); u.searchParams.set("lang", lang); history.replaceState(null, "", u); } catch (e) { /* file:// or sandbox */ }
    };

    // ---- header controls
    const setPlay = on => { S.running = on; playLabel(); log(on ? "play" : "pause", ""); app.tutorial.refresh(); };
    $("#kPlay").onclick = () => setPlay(!S.running);
    // speed: arrows step through SPEEDS; the label says how much simulated time one real second covers
    const num = v => (Math.round(v * 10) / 10).toString();
    const speedText = () => {
      const spr = CLK.stepsPerSec * S.speed * CLK.dt;          // model units per real second
      if (CLK.speedLabel) return CLK.speedLabel(spr, K.L);
      const r = 1 / spr;                                       // real seconds per simulated hour
      return r >= 1 ? `${num(r)} s = 1 h` : `1 s = ${num(spr)} h`;
    };
    const setSpeed = d => {
      const i = Math.max(0, Math.min(SPEEDS.length - 1, SPEEDS.indexOf(S.speed) + d));
      S.speed = SPEEDS[i]; $("#kSpeed").textContent = speedText(); log("speed", S.speed);
      $("#kSlow").disabled = i === 0; $("#kFast").disabled = i === SPEEDS.length - 1;
    };
    app.speedText = speedText;
    $("#kSlow").onclick = () => setSpeed(-1);
    $("#kFast").onclick = () => setSpeed(+1);

    // ---- splitters: drag to resize the compartments (double-click resets); remembered per browser
    // layout: top row = tutorial (left) + scale model / curves (right); bottom row, full width = Synoptic / Panel
    const main = $(".k-main");
    const layout = (() => { try { return JSON.parse(localStorage.getItem(LAYOUT_KEY)) || {}; } catch (e) { return {}; } })();
    const applyLayout = () => {
      main.style.gridTemplateColumns = layout.cols ? `${layout.cols}px 6px minmax(300px,1fr)` : "";
      main.style.gridTemplateRows = layout.top ? `${layout.top}px 6px minmax(0,1fr)` : "";
    };
    const saveLayout = () => { try { localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout)); } catch (e) { /* storage blocked */ } };
    const relayout = () => { app.synoptic.render(); app.panel.render(); app.chart.draw(); };
    function splitter(el, key, compute) {
      el.addEventListener("pointerdown", e => {
        e.preventDefault(); el.setPointerCapture(e.pointerId); el.classList.add("on");
        const move = ev => { layout[key] = Math.round(compute(ev)); applyLayout(); app.chart.draw(); };
        el.addEventListener("pointermove", move);
        el.addEventListener("pointerup", () => { el.removeEventListener("pointermove", move); el.classList.remove("on"); saveLayout(); relayout(); log("layout", key); }, { once: true });
      });
      el.addEventListener("dblclick", () => { delete layout[key]; applyLayout(); saveLayout(); relayout(); });
    }
    const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
    splitter($("#kSplitCols"), "cols", ev => { const r = main.getBoundingClientRect(); return clamp(ev.clientX - r.left, 300, r.width - 306); });
    splitter($("#kSplitBanner"), "top", ev => { const r = main.getBoundingClientRect(); return clamp(ev.clientY - r.top, 140, r.height - 220); });
    applyLayout();
    $("#kReset").onclick = () => { model.resetAll(); app.tutorial.restartCurrent(); log("reset", ""); app.synoptic.render(); };
    $("#kHood").onclick = e => {
      S.hood = !S.hood; e.target.classList.toggle("on", S.hood); log("hood", S.hood);
      app.synoptic.renderPalette(); app.synoptic.render(); app.synoptic.renderParams(); app.tutorial.render();
    };
    $("#kFree").onclick = () => { if (!S.free) app.goFree(); };
    $("#kLang").onclick = () => app.setLang(K.lang === "fr" ? "en" : "fr");
    const themeIcon = () => { $("#kTheme").textContent = K.theme === "dark" ? "☀" : "☾"; };
    $("#kTheme").onclick = () => { K.setTheme(K.theme === "dark" ? "light" : "dark"); themeIcon(); log("theme", K.theme); app.synoptic.render(); app.chart.draw(); };
    themeIcon();
    $("#kExport").onclick = () => {
      const t = app.tutorial, Wn = app.W;
      const data = { tool: "TSCG Kit", workshop: Wn.id, version: VERSION, lang: K.lang, exported: new Date().toISOString(),
        progress: S.free ? "free" : t.mode === "final" ? "done" : t.steps[t.i].id,
        predictions: Object.fromEntries(Object.entries(S.predictions).map(([id, k]) => [id, Wn.steps.find(s => s.id === id).predict.choices[k]])),
        answers: S.answers,
        state: { graph: model.serialize(), panel: app.panel.serialize() },
        log: S.log };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
      a.download = `tscg-${Wn.id}-session-${new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-")}.json`;
      document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
      log("export", "");
    };
    document.querySelectorAll(".k-tab").forEach(b => b.onclick = () => app.goTab(b.dataset.tab));
    document.querySelectorAll(".k-rtab").forEach(b => b.onclick = () => app.goRTab(b.dataset.rtab));
    window.addEventListener("keydown", e => {
      const typing = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
      if ((e.key === "Delete" || e.key === "Backspace") && !typing) { e.preventDefault(); if (S.tab === "synoptic") app.synoptic.deleteSelected(); else app.panel.deleteSelected(); }
      if (e.key === " " && !typing && document.activeElement.tagName !== "BUTTON") { e.preventDefault(); setPlay(!S.running); }
    });

    // ---- main loop: accumulate real time, run whole simulation steps
    let last = performance.now(), acc = 0, chartT = 0;
    function frame(now) {
      const dt = Math.min(0.25, (now - last) / 1000); last = now;
      if (S.running) {
        acc += dt * CLK.stepsPerSec * S.speed;
        let guard = 0;
        while (acc >= 1 && guard++ < 600) { model.step(CLK.dt); app.tutorial.tick(); acc -= 1; }
      }
      app.synoptic.update(S.running); app.panel.update(); app.view.update(S.running); fitView(); app.tutorial.refresh(); app.updateTools();
      $("#kClock").textContent = CLK.fmt(model.t);
      if (now - chartT > 120) { app.chart.draw(); chartT = now; }
      requestAnimationFrame(frame);
    }

    setSpeed(0);
    app.step = n => { for (let i = 0; i < n; i++) { model.step(CLK.dt); app.tutorial.tick(); } };   // for tests
    relabel();
    app.synoptic.renderParams();
    app.goTab("synoptic");
    app.tutorial.start(0);
    requestAnimationFrame(frame);
    window.TSCG = app;            // handle for tests and for curious KitArchitects
    return app;
  };
  K.VERSION = VERSION;
})(window.TSCGKit = window.TSCGKit || {});
