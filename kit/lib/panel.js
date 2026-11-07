/* TSCG Kit — panel.js
 * The Panneau: instruments laid out on a grid, LEGO-style. Every instrument
 * keeps one side fixed so the panel packs like Tetris:
 *   lamp   2×2 (square)     toggle 3×2
 *   gauge  2×len            slider 2×len   (len 3..10, vertical or horizontal)
 * Instruments are bound to the graph (read a level, write a parameter); they
 * never hold a model of their own.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const U = 32;                                   // grid unit, px
  const LEN_MIN = 3, LEN_MAX = 10;
  const DEFAULTS = { gauge: { orient: "v", len: 5 }, slider: { orient: "h", len: 5 }, toggle: { orient: "h", len: 0 }, lamp: { orient: "h", len: 0 } };
  const ICON = { gauge: "▮", slider: "⎯●", toggle: "⏻", lamp: "●" };
  function foot(c) {
    if (c.type === "lamp") return { w: 2, h: 2 };
    if (c.type === "toggle") return { w: 3, h: 2 };
    return c.orient === "v" ? { w: 2, h: c.len } : { w: c.len, h: 2 };
  }
  const resizable = c => c.type === "gauge" || c.type === "slider";

  class Panel {
    // o: { instruments, skins, isUnlocked(key), toast(msg), log(type, detail), onChange() }
    constructor(host, model, o) {
      this.m = model; this.o = o; this.controls = []; this.nextId = 1; this.els = new Map();
      host.innerHTML =
        `<div class="pn-toolbar"><span class="pn-tb-label"></span><span class="pn-tb-list"></span></div>
         <div class="pn-scroll"><div class="pn-grid"><div class="pn-empty"></div></div></div>`;
      this.host = host;
      this.tb = host.querySelector(".pn-tb-list");
      this.grid = host.querySelector(".pn-grid");
      this.empty = host.querySelector(".pn-empty");
      this.grid.style.setProperty("--u", U + "px");
      this.relabel();
    }
    relabel() {
      this.host.querySelector(".pn-tb-label").textContent = K.t("pn_add");
      this.empty.textContent = K.t("pn_empty");
    }
    def(c) { return this.o.instruments[c.inst]; }
    has(key) { return this.controls.some(c => c.inst === key); }
    cols() { return Math.max(8, Math.floor(this.grid.clientWidth / U)); }

    renderToolbar() {
      this.tb.textContent = "";
      let any = false;
      for (const key in this.o.instruments) {
        if (!this.o.isUnlocked(key)) continue;
        any = true;
        const d = this.o.instruments[key], piece = this.o.skins[d.bind.piece];
        const present = this.has(key), avail = !!this.m.first(d.bind.piece);
        const b = document.createElement("button");
        b.className = "pn-add"; b.dataset.inst = key;
        b.innerHTML = `<span class="pn-ico">${ICON[d.type]}</span>${d.label}`;
        b.disabled = present || !avail;
        b.title = present ? K.t("pn_present") : !avail ? K.t("pn_need", piece.name) : K.t("pn_addtip");
        b.onclick = () => this.add(key);
        this.tb.appendChild(b);
      }
      if (!any) this.tb.innerHTML = `<span class="k-muted">${K.t("pn_none")}</span>`;
    }

    fits(c, x, y, f) {
      if (x < 0 || y < 0 || x + f.w > this.cols()) return false;
      for (const o of this.controls) {
        if (o === c) continue;
        const g = foot(o);
        if (x < o.x + g.w && o.x < x + f.w && y < o.y + g.h && o.y < y + f.h) return false;
      }
      return true;
    }
    firstFree(c, f) {
      for (let y = 0; y < 400; y++) for (let x = 0; x + f.w <= this.cols(); x++) if (this.fits(c, x, y, f)) return { x, y };
      return { x: 0, y: 0 };
    }
    add(key) {
      const d = this.o.instruments[key], df = DEFAULTS[d.type];
      const c = { id: this.nextId++, inst: key, type: d.type, orient: d.orient || df.orient, len: d.len || df.len, x: 0, y: 0 };
      Object.assign(c, this.firstFree(c, foot(c)));
      this.controls.push(c);
      this.o.log("panel_add", key);
      this.render(); this.o.onChange();
      return c;
    }
    remove(c) {
      this.controls = this.controls.filter(o => o !== c);
      this.o.log("panel_remove", c.inst);
      this.render(); this.o.onChange();
    }
    rotate(c) {
      const turned = Object.assign({}, c, { orient: c.orient === "v" ? "h" : "v" });
      const f = foot(turned);
      const pos = this.fits(c, c.x, c.y, f) ? { x: c.x, y: c.y } : this.firstFree(c, f);
      Object.assign(c, { orient: turned.orient }, pos);
      this.o.log("panel_rotate", `${c.inst}:${c.orient}`);
      this.render();
    }

    place(node, c, x, y) {
      const f = foot(c);
      node.style.left = (x * U + 2) + "px"; node.style.top = (y * U + 2) + "px";
      node.style.width = (f.w * U - 4) + "px"; node.style.height = (f.h * U - 4) + "px";
    }
    render() {
      this.renderToolbar();
      this.grid.querySelectorAll(".pn-ctl").forEach(n => n.remove());
      this.els.clear();
      this.empty.style.display = this.controls.length ? "none" : "";
      let rows = 6;
      for (const c of this.controls) { rows = Math.max(rows, c.y + foot(c).h + 2); this.grid.appendChild(this.make(c)); }
      this.grid.style.minHeight = (rows * U) + "px";
      this.update();
    }

    make(c) {
      const d = this.def(c);
      const node = document.createElement("div");
      node.className = `pn-ctl pn-${c.type} ${c.orient}`;
      node.dataset.inst = c.inst;
      node.title = d.label;
      node.innerHTML =
        `<div class="pn-head"><span class="pn-label">${d.short}</span><span class="pn-tools">` +
        (resizable(c) ? `<button class="pn-rot" title="${K.t("pn_rotate")}">⟳</button>` : "") +
        `<button class="pn-del" title="${K.t("pn_remove")}">×</button></span></div><div class="pn-body"></div>` +
        (resizable(c) ? `<div class="pn-resize" title="${K.t("pn_stretch")}"></div>` : "");
      const body = node.querySelector(".pn-body"), refs = { node };
      if (c.type === "gauge" || c.type === "slider") {
        body.innerHTML = `<div class="pn-track">${d.zone ? `<div class="pn-zone"></div>` : ""}<div class="pn-fill"></div>${c.type === "slider" ? `<div class="pn-knob"></div>` : ""}</div><span class="pn-val"></span>`;
        refs.track = body.querySelector(".pn-track"); refs.fill = body.querySelector(".pn-fill");
        refs.val = body.querySelector(".pn-val"); refs.knob = body.querySelector(".pn-knob");
        if (d.zone) this.setBar(body.querySelector(".pn-zone"), c, this.frac(d, d.zone[0]), this.frac(d, d.zone[1]));
        if (c.type === "slider") refs.track.addEventListener("pointerdown", e => this.startSlide(e, c, refs.track));
      } else if (c.type === "toggle") {
        body.innerHTML = `<button class="pn-switch"><span class="pn-switch-dot"></span><span class="pn-switch-txt"></span></button>`;
        refs.sw = body.querySelector(".pn-switch"); refs.swTxt = body.querySelector(".pn-switch-txt");
        refs.sw.addEventListener("click", () => this.flip(c));
      } else if (c.type === "lamp") {
        body.innerHTML = `<span class="pn-bulb"></span>`;
        refs.lamp = body.querySelector(".pn-bulb");
      }
      node.querySelector(".pn-head").addEventListener("pointerdown", e => { if (!e.target.closest("button")) this.startMove(e, c, node); });
      node.querySelector(".pn-del").addEventListener("click", () => this.remove(c));
      const rot = node.querySelector(".pn-rot"); if (rot) rot.addEventListener("click", () => this.rotate(c));
      const rs = node.querySelector(".pn-resize"); if (rs) rs.addEventListener("pointerdown", e => this.startResize(e, c, node));
      this.place(node, c, c.x, c.y);
      this.els.set(c.id, refs);
      return node;
    }

    frac(d, v) { return Math.max(0, Math.min(1, (v - d.range[0]) / (d.range[1] - d.range[0]))); }
    setBar(bar, c, a, b) {               // a..b as fractions of the track
      if (b < a) { const t = a; a = b; b = t; }
      if (c.orient === "v") { bar.style.bottom = (a * 100) + "%"; bar.style.height = ((b - a) * 100) + "%"; bar.style.left = "0"; bar.style.right = "0"; }
      else { bar.style.left = (a * 100) + "%"; bar.style.width = ((b - a) * 100) + "%"; bar.style.top = "0"; bar.style.bottom = "0"; }
    }
    update() {
      for (const c of this.controls) {
        const r = this.els.get(c.id); if (!r) continue;
        const d = this.def(c), v = this.m.read(d.bind), off = v === null;
        r.node.classList.toggle("off", off);
        r.node.title = off ? K.t("pn_absent", d.label, this.o.skins[d.bind.piece].name) : d.label;
        if (r.fill) {
          const f = off ? 0 : this.frac(d, v), base = d.center !== undefined ? this.frac(d, d.center) : 0;
          this.setBar(r.fill, c, off ? base : base, off ? base : f);
          const dec = d.decimals !== undefined ? d.decimals : (d.step && d.step < 1 ? 1 : 0);
          r.val.textContent = off ? "—" : (d.format ? d.format(v) : `${v.toFixed(dec)} ${d.unit || ""}`);
          if (r.knob) { if (c.orient === "v") { r.knob.style.left = "50%"; r.knob.style.top = ((1 - f) * 100) + "%"; } else { r.knob.style.top = "50%"; r.knob.style.left = (f * 100) + "%"; } }
        }
        if (r.sw) {
          const auto = this.m.isAuto(d.bind);
          r.sw.classList.toggle("on", !off && !!v); r.sw.classList.toggle("auto", auto);
          r.swTxt.textContent = off ? "—" : auto ? K.t("pn_auto") : (v ? (d.onText || K.t("pn_on")) : (d.offText || K.t("pn_off")));
        }
        if (r.lamp) r.lamp.classList.toggle("on", !off && !!v);
      }
    }

    flip(c) {
      const d = this.def(c);
      if (this.m.read(d.bind) === null) return;
      if (this.m.isAuto(d.bind)) { this.o.toast(K.t("pn_isauto")); return; }
      this.m.write(d.bind, this.m.read(d.bind) ? 0 : 1);
      this.o.log("panel_toggle", `${c.inst}=${this.m.read(d.bind)}`);
      this.update();
    }
    startSlide(e, c, track) {
      e.preventDefault(); e.stopPropagation();
      const d = this.def(c);
      if (this.m.read(d.bind) === null) return;
      const set = ev => {
        const r = track.getBoundingClientRect();
        let t = c.orient === "h" ? (ev.clientX - r.left) / r.width : 1 - (ev.clientY - r.top) / r.height;
        t = Math.max(0, Math.min(1, t));
        let v = d.range[0] + t * (d.range[1] - d.range[0]);
        if (d.step) v = Math.round(v / d.step) * d.step;
        this.m.write(d.bind, +v.toFixed(3)); this.update();
      };
      set(e);
      const up = () => { window.removeEventListener("pointermove", set); this.o.log("panel_set", `${c.inst}=${this.m.read(d.bind)}`); };
      window.addEventListener("pointermove", set);
      window.addEventListener("pointerup", up, { once: true });
    }
    startMove(e, c, node) {
      e.preventDefault();
      const r = this.grid.getBoundingClientRect();
      const ox = e.clientX - r.left - c.x * U, oy = e.clientY - r.top - c.y * U;
      let cand = null;
      node.classList.add("dragging");
      const move = ev => {
        const x = Math.round((ev.clientX - r.left - ox) / U), y = Math.round((ev.clientY - r.top - oy) / U);
        cand = { x, y };
        this.place(node, c, Math.max(0, x), Math.max(0, y));
        node.classList.toggle("bad", !this.fits(c, x, y, foot(c)));
      };
      const up = () => {
        window.removeEventListener("pointermove", move);
        if (cand && (cand.x !== c.x || cand.y !== c.y)) {
          if (this.fits(c, cand.x, cand.y, foot(c))) { c.x = cand.x; c.y = cand.y; this.o.log("panel_move", `${c.inst}@${c.x},${c.y}`); }
          else this.o.toast(K.t("pn_nospace"));
        }
        this.render();
      };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up, { once: true });
    }
    startResize(e, c, node) {
      e.preventDefault(); e.stopPropagation();
      const r = this.grid.getBoundingClientRect();
      const move = ev => {
        const along = c.orient === "h" ? (ev.clientX - r.left) / U - c.x : (ev.clientY - r.top) / U - c.y;
        const len = Math.max(LEN_MIN, Math.min(LEN_MAX, Math.round(along)));
        if (len !== c.len && this.fits(c, c.x, c.y, foot(Object.assign({}, c, { len })))) { c.len = len; this.place(node, c, c.x, c.y); }
      };
      const up = () => { window.removeEventListener("pointermove", move); this.o.log("panel_resize", `${c.inst}:${c.len}`); this.render(); };
      window.addEventListener("pointermove", move);
      window.addEventListener("pointerup", up, { once: true });
    }

    serialize() { return this.controls.map(c => ({ inst: c.inst, type: c.type, x: c.x, y: c.y, orient: c.orient, len: c.len })); }
  }

  K.Panel = Panel;
  K.PANEL_UNIT = U;
})(window.TSCGKit = window.TSCGKit || {});
