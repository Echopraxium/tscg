/* TSCG Kit — synoptic.js
 * The Synoptique: an SVG node editor over the Model. Pieces are added from a
 * palette, moved by their title bar, and wired from an output (right) to an
 * input (left) of the same kind. Selecting a piece shows its parameters.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const NW = 176, HEAD = 34, ROW = 24;
  const REJECT = {
    self: "Une pièce ne se branche pas sur elle-même.",
    flux_to_info: "Un flux (orange) ne se branche que sur une entrée de flux.",
    info_to_flux: "Une information (bleu) ne se branche que sur une entrée d'information."
  };
  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  class Synoptic {
    // o: { order, home, fluxLabel, isUnlocked(type), hood(), toast(msg), onChange() }
    constructor(host, model, o) {
      this.m = model; this.o = o;
      this.selected = null; this.drag = null; this.dragWire = null; this.live = [];
      host.innerHTML =
        `<div class="sy-palette"><h2 class="k-h2">Pièces</h2><div class="sy-list"></div>
           <div class="sy-legend"><div><i style="background:var(--flux)"></i>${o.fluxLabel || "flux"}</div>
           <div><i style="background:var(--info)"></i>information</div>
           <p>Tire un fil d'une sortie (à droite d'une pièce) vers une entrée (à gauche) de la même couleur.</p></div></div>
         <div class="sy-stage"><svg class="sy-svg" aria-label="Synoptique : pièces et fils"></svg><div class="sy-params"></div></div>`;
      this.host = host;
      this.svg = host.querySelector(".sy-svg");
      this.list = host.querySelector(".sy-list");
      this.params = host.querySelector(".sy-params");
      this.svg.addEventListener("pointerdown", e => { if (e.target === this.svg) this.select(null); });
      window.addEventListener("pointermove", e => this.onMove(e));
      window.addEventListener("pointerup", e => this.onUp(e));
    }
    skin(n) { return this.m.skins[n.type]; }
    nodeHeight(n) {
      const rows = Math.max(this.m.ports(n, "in").length, this.m.ports(n, "out").length, 1);
      return HEAD + 10 + rows * ROW + 30;
    }
    portPos(n, port, side) {
      const i = this.m.ports(n, side).findIndex(q => q.id === port);
      return { x: n.x + (side === "in" ? 0 : NW), y: n.y + HEAD + 18 + i * ROW };
    }
    // Forward wires are curves; a wire going back to the left is routed below both pieces.
    wirePath(a, b, na, nb, k) {
      if (b.x >= a.x + 12 || !na || !nb) {
        const dx = Math.max(50, Math.abs(b.x - a.x) / 2);
        return `M${a.x} ${a.y} C${a.x + dx} ${a.y} ${b.x - dx} ${b.y} ${b.x} ${b.y}`;
      }
      const lane = Math.max(na.y + this.nodeHeight(na), nb.y + this.nodeHeight(nb)) + 22 + 14 * k, r = 10;
      const xr = a.x + 24 + 10 * k, xl = Math.max(6 + 4 * k, b.x - 24 - 10 * k);
      return `M${a.x} ${a.y} H${xr - r} Q${xr} ${a.y} ${xr} ${a.y + r} V${lane - r} Q${xr} ${lane} ${xr - r} ${lane}` +
             ` H${xl + r} Q${xl} ${lane} ${xl} ${lane - r} V${b.y + r} Q${xl} ${b.y} ${xl + r} ${b.y} H${b.x}`;
    }

    renderPalette() {
      this.list.textContent = "";
      for (const t of this.o.order) {
        const s = this.m.skins[t], open = this.o.isUnlocked(t);
        const b = document.createElement("button");
        b.className = "sy-piece"; b.disabled = !open; b.dataset.piece = t;
        b.innerHTML = `${s.name}<small>${open ? (this.o.hood() ? K.GENERIC[s.kind] : s.blurb) : "verrouillée"}</small>`;
        b.onclick = () => this.add(t);
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
        const d = this.wirePath(a, b, na, nb, b.x < a.x + 12 ? back++ : 0);
        const path = el("path", { d, class: `wire ${w.kind}${this.selected === "w" + w.id ? " selected" : ""}` }, gW);
        const hit = el("path", { d, class: "wire-hit" }, gW);
        hit.addEventListener("pointerdown", e => { e.stopPropagation(); this.select("w" + w.id); });
        this.live.push({ wire: w, path });
      }
      for (const n of m.nodes) {
        const s = this.skin(n), h = this.nodeHeight(n), hood = this.o.hood();
        const g = el("g", { class: "node" + (this.selected === "n" + n.id ? " selected" : ""), transform: `translate(${n.x},${n.y})`, "data-node": n.id }, gN);
        el("rect", { class: "node-body", width: NW, height: h, rx: 10 }, g);
        const head = el("path", { class: "node-head", d: `M0 10 Q0 0 10 0 H${NW - 10} Q${NW} 0 ${NW} 10 V${HEAD} H0 Z` }, g);
        const title = el("text", { class: "node-title", x: 12, y: hood ? 16 : 22 }, g); title.textContent = s.name;
        if (hood) el("text", { class: "node-gen", x: 12, y: 29 }, g).textContent = K.GENERIC[s.kind];
        for (const part of [head, title]) { part.style.cursor = "grab"; part.addEventListener("pointerdown", e => this.startDrag(e, n)); }
        g.addEventListener("pointerdown", e => { if (!e.defaultPrevented) this.select("n" + n.id); });
        m.ports(n, "in").forEach((q, i) => {
          const y = HEAD + 18 + i * ROW;
          el("circle", { class: `port ${q.kind}`, cx: 0, cy: y, r: 7, "data-node": n.id, "data-port": q.id, "data-side": "in" }, g);
          el("text", { class: "port-label", x: 12, y: y + 4 }, g).textContent = (s.ports || {})[q.id] !== undefined ? s.ports[q.id] : q.id;
        });
        m.ports(n, "out").forEach((q, i) => {
          const y = HEAD + 18 + i * ROW;
          const c = el("circle", { class: `port ${q.kind}`, cx: NW, cy: y, r: 7, "data-node": n.id, "data-port": q.id, "data-side": "out" }, g);
          c.addEventListener("pointerdown", e => this.startWire(e, n, q));
          el("text", { class: "port-label", x: NW - 12, y: y + 4, "text-anchor": "end" }, g).textContent = (s.ports || {})[q.id] !== undefined ? s.ports[q.id] : q.id;
        });
        const rows = Math.max(m.ports(n, "in").length, m.ports(n, "out").length, 1);
        const val = el("text", { class: "node-value", x: 12, y: HEAD + 10 + rows * ROW + 14 }, g);
        this.live.push({ node: n, val });
      }
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
      if (k === "sink") return (s.levelText || "niveau") + " : " + n.p.level + " " + (s.unit || "");
      if (k === "source") return n.s.u ? (s.onText || "marche") : (s.offText || "arrêt");
      if (k === "threshold") return n.s.x === null ? "non relié" : (n.s.u ? (s.onText || "fermé") : (s.offText || "ouvert"));
      if (k === "amplify") return (n.s.sat ? "saturé · " : "") + "sortie " + n.s.y.toFixed(1);
      if (k === "transducer") return n.s.flow.toFixed(1) + " " + (s.unit || "");
      if (k === "gradient") return n.s.a === null ? "rien à viser" : "écart " + n.s.d.toFixed(0) + " " + (s.unit || "");
      if (k === "clock") return n.s.v === null ? (s.offText || "—") : (s.onText || "") + " " + n.s.v.toFixed(0) + " " + (s.unit || "");
      return "";
    }
    update(running) {
      for (const r of this.live) {
        if (r.wire) { r.path.classList.toggle("active", r.wire.kind === "flux" && running && Math.abs(r.wire.power || 0) > 0.01); continue; }
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
      if (this.drag) { this.drag = null; return; }
      if (!this.dragWire) return;
      const dw = this.dragWire; this.dragWire = null;
      const t = document.elementFromPoint(e.clientX, e.clientY);
      if (t && t.dataset && t.dataset.side === "in") this.connect(dw.from, { node: +t.dataset.node, port: t.dataset.port });
      this.render();
    }
    connect(from, to) {
      const r = this.m.connect(from, to);
      if (!r.ok && REJECT[r.reason]) { this.o.toast(REJECT[r.reason]); this.m.emit("wire_reject", r.reason); }
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
      this.select("n" + n.id); this.o.onChange();
      return n;
    }
    deleteSelected() {
      if (!this.selected) return;
      const id = +this.selected.slice(1);
      if (this.selected[0] === "n") this.m.removeNode(id); else this.m.removeWire(id);
      this.selected = null; this.render(); this.renderParams(); this.o.onChange();
    }
    select(key) { this.selected = key; this.render(); this.renderParams(); }

    renderParams() {
      const box = this.params;
      if (!this.selected) { box.innerHTML = `<span class="k-muted">Clique une pièce pour la régler. Touche Suppr pour enlever une pièce ou un fil.</span>`; return; }
      if (this.selected[0] === "w") { box.innerHTML = `<span>Fil sélectionné.</span><button class="sy-del">Supprimer le fil</button>`; box.querySelector(".sy-del").onclick = () => this.deleteSelected(); return; }
      const n = this.m.byId(+this.selected.slice(1)); if (!n) return;
      const s = this.skin(n), ps = s.params || {};
      box.innerHTML = `<b>${s.name}</b>${this.o.hood() ? ` <span class="k-muted">· ${K.GENERIC[s.kind]}</span>` : ""}` +
        Object.entries(ps).filter(([k, d]) => !d.hidden).map(([k, d]) => `<label>${d.label}<input type="number" data-k="${k}" step="${d.step}"${d.min !== undefined ? ` min="${d.min}"` : ""}${d.max !== undefined ? ` max="${d.max}"` : ""} value="${n.p[k]}"></label>`).join("") +
        `<button class="sy-del">Supprimer la pièce</button>`;
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
