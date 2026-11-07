/* TSCG Kit — tutorial.js
 * Runs a workshop's steps as data. Each step:
 *   { id, title, goal, hint?, unlock:{pieces, instruments}, enter?(app),
 *     need(app) -> null | {msg, tab},           structure still missing
 *     check(app, mem) -> {p, done, status},     called once per simulated minute
 *     predict?:{q, choices}, takeaway, hood }
 * The final card may ask optional open questions (answers go into the export);
 * by default it asks nothing and leaves the discovery to the user.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  // check helpers; durations are counted in simulation steps
  K.elapse = steps => (app, mem) => {
    mem.n = (mem.n || 0) + 1;
    return { p: mem.n / steps, done: mem.n >= steps, status: K.t("tu_runningof", app.fmtSteps(mem.n), app.fmtSteps(steps)) };
  };
  K.hold = (steps, pred, offMsg) => (app, mem) => {
    const ok = pred(app); mem.n = ok ? (mem.n || 0) + 1 : 0;
    return { p: mem.n / steps, done: mem.n >= steps, status: ok ? K.t("tu_runningof", app.fmtSteps(mem.n), app.fmtSteps(steps)) : offMsg };
  };
  const esc = s => String(s).replace(/[&<>"]/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]));

  class Tutorial {
    // W: workshop (steps, final, free); app: { S, model, log, unlock(u), goTab(tab), goFree(), running() }
    constructor(host, W, app) {
      this.host = host; this.W = W; this.steps = W.steps; this.app = app;
      this.mode = "steps"; this.i = 0; this.mem = {}; this.res = null; this.finished = false;
    }
    start(i) {
      this.mode = "steps"; this.i = i; this.mem = {}; this.res = null; this.finished = false;
      const st = this.steps[i];
      this.app.unlock(st.unlock || {});
      if (st.enter) st.enter(this.app);
      this.app.log("step_enter", st.id);
      this.render();
    }
    restartCurrent() {
      if (this.mode !== "steps") return;
      this.mem = {}; this.res = null; this.finished = false;
      const st = this.steps[this.i]; if (st.enter) st.enter(this.app);
      this.render();
    }
    need() {
      if (this.mode !== "steps" || this.finished) return null;
      return this.steps[this.i].need(this.app);
    }
    waitingPrediction() { const st = this.steps[this.i]; return this.mode === "steps" && st.predict && this.app.S.predictions[st.id] === undefined; }
    tick() {
      if (this.mode !== "steps" || this.finished) return;
      if (this.need()) { this.mem = {}; this.res = null; return; }
      if (this.waitingPrediction()) return;
      this.res = this.steps[this.i].check(this.app, this.mem);
      if (this.res.done) { this.finished = true; this.app.log("step_done", this.steps[this.i].id); this.render(); }
    }

    render() {
      const S = this.app.S, h = this.host;
      if (this.mode === "free") {
        h.innerHTML = `<div class="tu-head"><h3>${K.t("tu_free")}</h3></div><div class="tu-goal">${this.W.free.text}</div>` +
          (S.hood && this.W.free.hood ? `<div class="tu-hood">${this.W.free.hood}</div>` : "") +
          `<div class="tu-row"><button class="tu-back">${K.t("tu_back")}</button></div>`;
        h.querySelector(".tu-back").onclick = () => this.app.backToTutorial();
        return;
      }
      if (this.mode === "final") return this.renderFinal();
      const st = this.steps[this.i], n = this.steps.length;
      let html = `<div class="tu-head"><span class="tu-no">${K.t("tu_step", this.i + 1, n)}</span><h3>${st.title}</h3></div><div class="tu-goal">${st.goal}</div>`;
      if (st.predict) {
        const pk = S.predictions[st.id];
        if (pk === undefined) html += `<div class="tu-q">${st.predict.q}</div><div class="tu-choices">` +
          st.predict.choices.map((c, k) => `<button data-choice="${k}">${c}</button>`).join("") + `</div>`;
        else html += `<div class="tu-hint">${K.t("tu_bet", st.predict.choices[pk])}</div>`;
      }
      if (st.hint && !this.finished) html += `<div class="tu-hint">${st.hint}</div>`;
      html += `<div class="tu-progress"><div></div></div><div class="tu-status-row"><span class="tu-status"></span><button class="tu-goto" hidden></button></div>`;
      if (this.finished) {
        html += `<div class="tu-takeaway">${st.takeaway}</div>`;
        if (S.hood && st.hood) html += `<div class="tu-hood">${st.hood}</div>`;
        html += `<div class="tu-row"><button class="primary tu-next">${this.i + 1 < n ? K.t("tu_next") : K.t("tu_finish")}</button></div>`;
      }
      h.innerHTML = html;
      h.querySelectorAll("[data-choice]").forEach(b => b.onclick = () => {
        S.predictions[st.id] = +b.dataset.choice; this.app.log("predict", `${st.id}: ${st.predict.choices[+b.dataset.choice]}`); this.render();
      });
      const nx = h.querySelector(".tu-next");
      if (nx) nx.onclick = () => { if (this.i + 1 < n) this.start(this.i + 1); else { this.mode = "final"; this.app.S.done = true; this.app.log("tutorial_done", ""); this.app.unlock(this.W.final.unlock || {}); this.render(); } };
      this.refresh();
    }
    renderFinal() {
      const S = this.app.S, F = this.W.final, h = this.host;
      let html = `<div class="tu-head"><h3>${F.title}</h3></div><div class="tu-goal">${F.text}</div>`;
      if (!F.questions || !F.questions.length) {          // default: no questions, let the user discover
        html += (S.hood && F.hood ? `<div class="tu-hood">${F.hood}</div>` : "") +
          `<div class="tu-row"><button class="primary tu-free">${K.t("tu_openfree")}</button></div>`;
      } else if (!S.answers) {
        html += F.questions.map((q, k) => `<label class="tu-ask">${q}<textarea data-q="${k}" rows="2" placeholder="${K.t("tu_ph")}"></textarea></label>`).join("") +
          `<div class="tu-row"><button class="primary tu-save">${K.t("tu_save")}</button><button class="tu-skip">${K.t("tu_skip")}</button></div>`;
      } else {
        html += `<div class="tu-takeaway">${K.t("tu_thanks")}</div>` +
          (S.hood && F.hood ? `<div class="tu-hood">${F.hood}</div>` : "") +
          `<div class="tu-row"><button class="primary tu-free">${K.t("tu_openfree")}</button></div>`;
      }
      h.innerHTML = html;
      const save = h.querySelector(".tu-save");
      if (save) save.onclick = () => {
        S.answers = F.questions.map((q, k) => ({ q, a: h.querySelector(`[data-q="${k}"]`).value.trim() }));
        this.app.log("answers", S.answers.map(x => esc(x.a)).join(" | ")); this.render();
      };
      const skip = h.querySelector(".tu-skip");
      if (skip) skip.onclick = () => { S.answers = []; this.app.log("answers_skipped", ""); this.render(); };
      const fr = h.querySelector(".tu-free"); if (fr) fr.onclick = () => this.app.goFree();
    }

    // light per-frame refresh: progress bar, status line, "go to tab" hint
    refresh() {
      const bar = this.host.querySelector(".tu-progress>div"), status = this.host.querySelector(".tu-status"), go = this.host.querySelector(".tu-goto");
      const nd = this.need();
      this.app.attention(nd && nd.tab ? nd.tab : null);
      const st = this.mode === "steps" ? this.steps[this.i] : null;     // a step that asks to read the curves
      this.app.curvesHint(!!(st && st.curves && !this.finished));
      if (!bar || !status) return;
      if (this.finished) { bar.style.width = "100%"; status.textContent = K.t("tu_done"); go.hidden = true; return; }
      bar.style.width = Math.min(100, Math.round(100 * ((this.res && this.res.p) || 0))) + "%";
      if (nd) status.textContent = nd.msg;
      else if (this.waitingPrediction()) status.textContent = K.t("tu_answer");
      else if (!this.app.running()) status.textContent = K.t("tu_play");
      else status.textContent = this.res ? this.res.status : K.t("tu_running");
      const want = nd && nd.tab && nd.tab !== this.app.S.tab ? nd.tab : null;
      go.hidden = !want;
      if (want) { go.textContent = want === "panel" ? K.t("tu_gopanel") : K.t("tu_gosyn"); go.onclick = () => this.app.goTab(want); }
    }
  }
  K.Tutorial = Tutorial;
})(window.TSCGKit = window.TSCGKit || {});
