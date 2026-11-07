/* TSCG Kit — synoptic.js
 * The Synoptique: an SVG node editor over the Model. Pieces are added from a
 * palette, moved by their title bar, and wired from an output (right) to an
 * input (left) of the same kind. Selecting a piece shows its parameters.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const NW = 150, HEAD = 28, ROW = 20, PY = 15;      // compact nodes
  const REJECT = { self: "rej_self", flux_to_info: "rej_flux", info_to_flux: "rej_info" };
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  class Synoptic {
    // o: { order, home, fluxLabel(), isUnlocked(type), hood(), toast(msg), onChange() }
    constructor(host, model, o) {
      this.m = model; this.o = o;
      this.selected = null; this.drag = null; this.dragWire = null; this.live = [];
      host.innerHTML =
        `<div class="sy-palette">
           <div class="sy-blocks"><h2 class="k-h2 sy-h"></h2><div class="sy-list"></div>
             <div class="sy-legend"><div><i style="background:var(--flux)"></i><span class="sy-lflux"></span></div>
             <div><i style="background:var(--info)"></i><span class="sy-linfo"></span></div>
             <p class="sy-help"></p></div></div>
           <div class="sy-infobox"><h2 class="k-h2 sy-ih"></h2><div class="sy-info" aria-live="polite"></div></div></div>
         <div class="sy-stage"><svg class="sy-svg"></svg><div class="sy-params"></div></div>`;
      this.host = host;
      this.svg = host.querySelector(".sy-svg");
      this.list = host.querySelector(".sy-list");
      this.info = host.querySelector(".sy-info");
      this.params = host.querySelector(".sy-params");
      this.svg.addEventListener("pointerdown", e => { if (e.target === this.svg) this.select(null); });
      window.addEventListener("pointermove", e => this.onMove(e));
      window.addEventListener("pointerup", e => this.onUp(e));
      this.relabel();
    }
    relabel() {                         // static strings (language switch)
      const q = s => this.host.querySelector(s);
      q(".sy-h").textContent = K.t("pieces"); q(".sy-lflux").textContent = this.o.fluxLabel() || "flux";
      q(".sy-linfo").textContent = K.t("info"); q(".sy-help").textContent = K.t("wire_help");
      q(".sy-ih").textContent = K.t("info_box");
      this.svg.setAttribute("aria-label", K.t("syn_aria"));
      this.showInfo(this.infoType || null);
    }
    // the compartment under the blocks: what the hovered (or last hovered / selected) block does
    showInfo(t) {
      this.infoType = t;
      if (!t || !this.m.skins[t]) { this.info.innerHTML = `<span class="k-muted">${K.t("pal_hint")}</span>`; return; }
      const s = this.m.skins[t], open = this.o.isUnlocked(t);
      this.info.innerHTML = `<div class="sy-info-h">${K.iconSvg(K.iconOf(s), "k-icon")}<b>${s.name}</b></div><p>${s.blurb}</p>` +
        (this.o.hood() ? `<p class="k-muted">${K.generic(s.kind)}</p>` : "") +
        (open ? "" : `<p class="k-muted">${K.t("locked_info")}</p>`);
    }
    skin(n) { return this.m.skins[n.type]; }
    nodeHeight(n) {
      const rows = Math.max(this.m.ports(n, "in").length, this.m.ports(n, "out").length, 1);
      return HEAD + 8 + rows * ROW + 24;
    }
    portPos(n, port, side) {
      const i = this.m.ports(n, side).findIndex(q => q.id === port);
      return { x: n.x + (side === "in" ? 0 : NW), y: n.y + HEAD + PY + i * ROW };
    }
    // A wire whose target is not clearly to the left is a smooth curve (also for a target
    // above or below in a nearby column); only a real return wire is routed under the pieces.
    isBack(a, b) { return b.x < a.x - 30; }
    wirePath(a, b, na, nb, k) {
      if (!this.isBack(a, b) || !na || !nb) {
        const dx = Math.max(40, Math.abs(b.x - a.x) / 2, Math.min(90, Math.abs(b.y - a.y) / 3));
        return `M${a.x} ${a.y} C${a.x + dx} ${a.y} ${b.x - dx} ${b.y} ${b.x} ${b.y}`;
      }
      const lane = Math.max(na.y + this.nodeHeight(na), nb.y + this.nodeHeight(nb)) + 18 + 12 * k, r = 8;
      const xr = a.x + 20 + 9 * k, xl = Math.max(6 + 4 * k, b.x - 20 - 9 * k);
      return `M${a.x} ${a.y} H${xr - r} Q${xr} ${a.y} ${xr} ${a.y + r} V${lane - r} Q${xr} ${lane} ${xr - r} ${lane}` +
             ` H${xl + r} Q${xl} ${lane} ${xl} ${lane - r} V${b.y + r} Q${xl} ${b.y} ${xl + r} ${b.y} H${b.x}`;
    }

    renderPalette() {
      this.list.textContent = "";
      for (const t of this.o.order) {
        const s = this.m.skins[t], open = this.o.isUnlocked(t);
        const b = document.createElement("button");
        b.className = "sy-piece"; b.disabled = !open; b.dataset.piece = t;
        b.innerHTML = `${K.iconSvg(K.iconOf(s), "k-icon")}<span>${s.name}</span>`;
        b.title = open ? s.blurb : K.t("locked");
        b.onclick = () => this.add(t);
        b.addEventListener("mouseenter", () => this.showInfo(t));
        b.addEventListener("focus", () => this.showInfo(t));
        this.list.appendChild(b);
      }
    }

    render() {
      const svg = this.svg, m = this.m;
      svg.textContent = ""; this.live = [];
      const gW = el("g", {}, svg), gN = el("g", {}, svg);
      let back = 0;
      for (const w of m.wires) {
        const na = m.byId(w.from.node), nb = m.byId(w.to.node);
        const a = this.portPos(na, w.from.port, "out"), b = this.portPos(nb, w.to.port, "in");
        const d = this.wirePath(a, b, na, nb, this.isBack(a, b) ? back++ : 0);
        const path = el("path", { d, class: `wire ${w.kind}${this.selected === "w" + w.id ? " selected" : ""}` }, gW);
        const hit = el("path", { d, class: "wire-hit" }, gW);
        hit.addEventListener("pointerdown", e => { e.stopPropagation(); this.select("w" + w.id); });
        // chevrons travelling along the wire show which way it flows (shown while time runs)
        let len = 200; try { len = path.getTotalLength() || 200; } catch (e) { /* hidden tab */ }
        const chev = el("g", { class: `chev ${w.kind}` }, gW), dur = Math.max(1.1, len / 70);
        const motions = [0, 1, 2].map(k => {
          const c = el("path", { d: "M-3.5 -4 L2.5 0 L-3.5 4" }, chev);
          return el("animateMotion", { dur: dur.toFixed(2) + "s", repeatCount: "indefinite", rotate: "auto", path: d,
            begin: (-k * dur / 3).toFixed(2) + "s", keyPoints: "0;1", keyTimes: "0;1", calcMode: "linear" }, c);
        });
        this.live.push({ wire: w, path, chev, motions, dir: 1 });
      }
      for (const n of m.nodes) {
        const s = this.skin(n), h = this.nodeHeight(n), hood = this.o.hood();
        const outer = el("g", { class: "node" + (this.selected === "n" + n.id ? " selected" : ""), transform: `translate(${n.x},${n.y})`, "data-node": n.id }, gN);
        // inner group carries the animations (lift while dragged, settle on drop, pop when added)
        const anim = this.drag && this.drag.n === n ? " dragging" : this.dropped === n.id ? " dropped" : this.appeared === n.id ? " appear" : "";
        const g = el("g", { class: "node-inner" + anim }, outer);
        el("rect", { class: "node-body", width: NW, height: h, rx: 8 }, g);
        const head = el("path", { class: "node-head", d: `M0 8 Q0 0 8 0 H${NW - 8} Q${NW} 0 ${NW} 8 V${HEAD} H0 Z` }, g);
        el("path", { class: "node-icon", d: K.iconPath(K.iconOf(s)), transform: "translate(8 6) scale(0.667)" }, g);
        const title = el("text", { class: "node-title", x: 29, y: hood ? 13 : 18 }, g); title.textContent = s.name;
        if (hood) el("text", { class: "node-gen", x: 29, y: 24 }, g).textContent = K.generic(s.kind);
        for (const part of [head, title]) { part.style.cursor = "grab"; part.addEventListener("pointerdown", e => this.startDrag(e, n)); }
        outer.addEventListener("pointerdown", e => { if (!e.defaultPrevented) this.select("n" + n.id); });
        m.ports(n, "in").forEach((q, i) => {
          const y = HEAD + PY + i * ROW;
          el("circle", { class: `port ${q.kind}`, cx: 0, cy: y, r: 6, "data-node": n.id, "data-port": q.id, "data-side": "in" }, g);
          el("text", { class: "port-label", x: 10, y: y + 3.5 }, g).textContent = (s.ports || {})[q.id] !== undefined ? s.ports[q.id] : q.id;
        });
        m.ports(n, "out").forEach((q, i) => {
          const y = HEAD + PY + i * ROW;
          const c = el("circle", { class: `port ${q.kind}`, cx: NW, cy: y, r: 6, "data-node": n.id, "data-port": q.id, "data-side": "out" }, g);
          c.addEventListener("pointerdown", e => this.startWire(e, n, q));
          el("text", { class: "port-label", x: NW - 10, y: y + 3.5, "text-anchor": "end" }, g).textContent = (s.ports || {})[q.id] !== undefined ? s.ports[q.id] : q.id;
        });
        const rows = Math.max(m.ports(n, "in").length, m.ports(n, "out").length, 1);
        const val = el("text", { class: "node-value", x: 10, y: HEAD + 8 + rows * ROW + 12 }, g);
        this.live.push({ node: n, val });
      }
      // an appear / drop animation plays once, on the render that follows the event
      this.appeared = null; this.dropped = null;
      if (this.dragWire) {
        this.dragWire.path = el("path", { class: `wire ${this.dragWire.kind}`, d: "" }, svg);
        this.dragWire.path.style.pointerEvents = "none";
      }
      this.update(false);
    }

    describe(n) {
      const s = this.skin(n), k = this.m.kindOf(n);
      if (s.describe) return s.describe(n, this.m);
      if (k === "storage") return n.s.x.toFixed(1) + " " + (s.unit || "");
      if (k === "sink") return (s.levelText || K.t("d_level")) + K.L(": ", " : ") + n.p.level + " " + (s.unit || "");
      if (k === "source") return n.s.u ? (s.onText || K.t("d_on")) : (s.offText || K.t("d_off"));
      if (k === "threshold") return n.s.x === null ? K.t("d_unlinked") : (n.s.u ? (s.onText || K.t("d_closed")) : (s.offText || K.t("d_open")));
      if (k === "amplify") return (n.s.sat ? K.t("d_sat") : "") + K.t("d_out") + " " + n.s.y.toFixed(1);
      if (k === "transducer") return n.s.flow.toFixed(1) + " " + (s.unit || "");
      if (k === "gradient") return n.s.a === null ? K.t("d_notarget") : K.t("d_gap") + " " + n.s.d.toFixed(0) + " " + (s.unit || "");
      if (k === "clock") return n.s.v === null ? (s.offText || "—") : (s.onText || "") + " " + n.s.v.toFixed(0) + " " + (s.unit || "");
      return "";
    }
    update(running) {
      for (const r of this.live) {
        if (r.wire) {
          const w = r.wire, src = this.m.byId(w.from.node);
          const on = running && (w.kind === "flux" ? Math.abs(w.power || 0) > 0.01 : !!src && this.m.infoOut(src) !== null);
          r.chev.style.display = on ? "" : "none";
          const dir = w.kind === "flux" && (w.power || 0) < 0 ? -1 : 1;     // heat can flow backwards between two stores
          if (dir !== r.dir) { r.dir = dir; r.motions.forEach(a => a.setAttribute("keyPoints", dir > 0 ? "0;1" : "1;0")); }
          continue;
        }
        r.val.textContent = this.describe(r.node);
      }
    }

    point(e) { const r = this.svg.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
    startDrag(e, n) {
      e.preventDefault(); e.stopPropagation(); this.select("n" + n.id);
      const p = this.point(e); this.drag = { n, dx: p.x - n.x, dy: p.y - n.y };
    }
    startWire(e, n, q) {
      e.preventDefault(); e.stopPropagation();
      this.dragWire = { from: { node: n.id, port: q.id }, kind: q.kind };
      this.render();
    }
    onMove(e) {
      if (this.drag) {
        const p = this.point(e), r = this.svg.getBoundingClientRect(), n = this.drag.n;
        n.x = Math.max(4, Math.min(r.width - NW - 4, p.x - this.drag.dx));
        n.y = Math.max(4, Math.min(r.height - 40, p.y - this.drag.dy));
        this.render();
      } else if (this.dragWire && this.dragWire.path) {
        const a = this.portPos(this.m.byId(this.dragWire.from.node), this.dragWire.from.port, "out");
        this.dragWire.path.setAttribute("d", this.wirePath(a, this.point(e)));
      }
    }
    onUp(e) {
      if (this.drag) {
        const n = this.drag.n; this.drag = null;
        this.dropped = n.id; this.render();
        return;
      }
      if (!this.dragWire) return;
      const dw = this.dragWire; this.dragWire = null;
      const t = document.elementFromPoint(e.clientX, e.clientY);
      if (t && t.dataset && t.dataset.side === "in") this.connect(dw.from, { node: +t.dataset.node, port: t.dataset.port });
      this.render();
    }
    connect(from, to) {
      const r = this.m.connect(from, to);
      if (!r.ok && REJECT[r.reason]) { this.o.toast(K.t(REJECT[r.reason])); this.m.emit("wire_reject", r.reason); }
      this.render(); this.o.onChange();
      return r;
    }
    add(type) {
      // home positions are designed for a wide stage; squeeze them horizontally to fit this one
      const r = this.svg.getBoundingClientRect(), homes = this.o.home || {}, home = homes[type] || { x: 40, y: 40 };
      const maxX = Math.max(1, ...Object.values(homes).map(h => h.x));
      const scale = r.width ? Math.min(1, (r.width - NW - 12) / maxX) : 1;
      let x = Math.round(home.x * scale), y = home.y;
      while (this.m.nodes.some(n => Math.abs(n.x - x) < 30 && Math.abs(n.y - y) < 30)) { x += 30; y += 30; }
      if (r.width) x = Math.max(8, Math.min(x, r.width - NW - 8));
      const n = this.m.addNode(type, x, y);
      this.appeared = n.id;
      this.select("n" + n.id); this.o.onChange();
      return n;
    }
    deleteSelected() {
      if (!this.selected) return;
      const id = +this.selected.slice(1);
      if (this.selected[0] === "n") this.m.removeNode(id); else this.m.removeWire(id);
      this.selected = null; this.render(); this.renderParams(); this.o.onChange();
    }
    select(key) {
      this.selected = key; this.render(); this.renderParams();
      if (key && key[0] !== "w") { const n = this.m.byId(+key.slice(1)); if (n) this.showInfo(n.type); }
    }

    renderParams() {
      const box = this.params;
      if (!this.selected) { box.innerHTML = `<span class="k-muted">${K.t("params_hint")}</span>`; return; }
      if (this.selected[0] === "w") { box.innerHTML = `<span>${K.t("wire_selected")}</span><button class="sy-del">${K.t("del_wire")}</button>`; box.querySelector(".sy-del").onclick = () => this.deleteSelected(); return; }
      const n = this.m.byId(+this.selected.slice(1)); if (!n) return;
      const s = this.skin(n), ps = s.params || {};
      box.innerHTML = `<b>${s.name}</b>${this.o.hood() ? ` <span class="k-muted">· ${K.generic(s.kind)}</span>` : ""}` +
        Object.entries(ps).filter(([k, d]) => !d.hidden).map(([k, d]) => `<label>${d.label}<input type="number" data-k="${k}" step="${d.step}"${d.min !== undefined ? ` min="${d.min}"` : ""}${d.max !== undefined ? ` max="${d.max}"` : ""} value="${n.p[k]}"></label>`).join("") +
        `<button class="sy-del">${K.t("del_piece")}</button>`;
      box.querySelectorAll("input").forEach(inp => inp.onchange = () => {
        const d = ps[inp.dataset.k]; let v = parseFloat(inp.value);
        if (!isFinite(v)) v = d.v;
        this.m.write({ piece: n.type, param: inp.dataset.k }, v);
        inp.value = n.p[inp.dataset.k];
        this.m.emit("param", `${n.type}.${inp.dataset.k}=${n.p[inp.dataset.k]}`);
      });
      box.querySelector(".sy-del").onclick = () => this.deleteSelected();
    }
  }

  K.Synoptic = Synoptic;
})(window.TSCGKit = window.TSCGKit || {});
