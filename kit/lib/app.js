/* TSCG Kit — app.js
 * The workshop shell, identical for every workshop:
 *   left  : tutorial banner + tabs [Panneau | Synoptique]
 *   right : Maquette (drawn by the workshop) + Courbes
 * Owns the clock, the main loop, "under the hood", free mode and the session export.
 * Usage: TSCGKit.start(workshopDefinition)
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const VERSION = "0.3.0";
  const SPEEDS = [1, 4, 0.5];

  K.start = function (W) {
    // the workshop's clock: model time per step, steps per real second at ×1, formatting
    const CLK = Object.assign({}, K.CLOCK_HOURS, W.clock || {});
    document.title = W.pageTitle || document.title;
    document.body.innerHTML =
      `<header class="k-header">
         <a class="k-home" href="${W.homeUrl || "../index.html"}" title="Tous les ateliers">←</a>
         <h1>${W.title}</h1>
         <div class="k-transport">
           <button id="kPlay" class="primary" title="Lancer / mettre en pause (barre d'espace)">▶ Lancer</button>
           <button id="kSpeed" title="Vitesse du temps">×1</button>
           <button id="kReset" title="Remettre l'horloge à zéro">↺</button>
           <span id="kClock" class="k-clock"></span>
         </div>
         <span class="k-spacer"></span>
         <button id="kHood" title="Montrer les noms génériques des pièces">Sous le capot</button>
         <button id="kFree" title="Débloquer toutes les pièces et quitter le tutoriel">Mode libre</button>
         <button id="kExport" title="Télécharger le journal de la session (pour les tests)">Exporter ma session</button>
       </header>
       <main class="k-main">
         <section class="k-left">
           <div class="k-banner" id="kBanner" aria-live="polite"></div>
           <div class="k-tabs" role="tablist">
             <button class="k-tab" role="tab" data-tab="panel">Panneau</button>
             <button class="k-tab" role="tab" data-tab="synoptic">Synoptique</button>
           </div>
           <div class="k-panes">
             <div class="k-pane k-pane-panel" data-pane="panel"></div>
             <div class="k-pane k-pane-synoptic" data-pane="synoptic"></div>
           </div>
         </section>
         <section class="k-right">
           <div class="k-maquette"><h2 class="k-h2">Maquette</h2><div class="k-view" id="kView"></div></div>
           <div class="k-curves"><h2 class="k-h2">Courbes</h2><canvas id="kChart"></canvas><div class="k-legend" id="kLegend"></div></div>
         </section>
       </main>
       <div class="k-toast" id="kToast" role="status"></div>`;
    const $ = sel => document.querySelector(sel);

    const S = { running: false, speed: 1, hood: false, free: false, tab: "synoptic",
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
      order: W.order, home: W.home, fluxLabel: W.fluxLabel,
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

    // ---- header controls
    const setPlay = on => { S.running = on; $("#kPlay").textContent = on ? "⏸ Pause" : "▶ Lancer"; log(on ? "play" : "pause", ""); app.tutorial.refresh(); };
    $("#kPlay").onclick = () => setPlay(!S.running);
    $("#kSpeed").onclick = e => { S.speed = SPEEDS[(SPEEDS.indexOf(S.speed) + 1) % SPEEDS.length]; e.target.textContent = "×" + S.speed; log("speed", S.speed); };
    $("#kReset").onclick = () => { model.resetAll(); app.tutorial.restartCurrent(); log("reset", ""); app.synoptic.render(); };
    $("#kHood").onclick = e => {
      S.hood = !S.hood; e.target.classList.toggle("on", S.hood); log("hood", S.hood);
      app.synoptic.renderPalette(); app.synoptic.render(); app.synoptic.renderParams(); app.tutorial.render();
    };
    $("#kFree").onclick = () => { if (!S.free) app.goFree(); };
    $("#kExport").onclick = () => {
      const t = app.tutorial;
      const data = { tool: "TSCG Kit", workshop: W.id, version: VERSION, exported: new Date().toISOString(),
        progress: S.free ? "free" : t.mode === "final" ? "done" : t.steps[t.i].id,
        predictions: Object.fromEntries(Object.entries(S.predictions).map(([id, k]) => [id, W.steps.find(s => s.id === id).predict.choices[k]])),
        answers: S.answers,
        state: { graph: model.serialize(), panel: app.panel.serialize() },
        log: S.log };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
      a.download = `tscg-${W.id}-session-${new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-")}.json`;
      document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
      log("export", "");
    };
    document.querySelectorAll(".k-tab").forEach(b => b.onclick = () => app.goTab(b.dataset.tab));
    window.addEventListener("keydown", e => {
      const typing = /INPUT|TEXTAREA/.test(document.activeElement.tagName);
      if ((e.key === "Delete" || e.key === "Backspace") && !typing && S.tab === "synoptic") { e.preventDefault(); app.synoptic.deleteSelected(); }
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
      app.synoptic.update(S.running); app.panel.update(); app.view.update(S.running); app.tutorial.refresh();
      $("#kClock").textContent = CLK.fmt(model.t);
      if (now - chartT > 120) { app.chart.draw(); chartT = now; }
      requestAnimationFrame(frame);
    }

    app.step = n => { for (let i = 0; i < n; i++) { model.step(CLK.dt); app.tutorial.tick(); } };   // for tests
    app.synoptic.renderParams();
    app.goTab("synoptic");
    app.tutorial.start(0);
    requestAnimationFrame(frame);
    window.TSCG = app;            // handle for tests and for curious KitArchitects
    return app;
  };
  K.VERSION = VERSION;
})(window.TSCGKit = window.TSCGKit || {});
