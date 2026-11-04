/* TSCG Kit — sim.js
 * Generic pieces and the fixed-step simulation.
 * The graph (nodes + wires) is the single source of truth: the Panneau and the
 * Maquette only read it (and write parameters through bindings).
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";

  // Behaviour lives in the generic kind; a workshop gives each piece a "skin"
  // (name, port labels, parameters) on top of one of these kinds.
  const KINDS = {
    storage:   { inputs:  [{ id: "in", kind: "flux", multi: true }],
                 outputs: [{ id: "out", kind: "flux" }, { id: "level", kind: "info" }] },
    sink:      { inputs:  [{ id: "in", kind: "flux", multi: true }], outputs: [] },
    source:    { inputs:  [{ id: "cmd", kind: "info" }], outputs: [{ id: "flow", kind: "flux" }] },
    threshold: { inputs:  [{ id: "x", kind: "info" }],   outputs: [{ id: "u", kind: "info" }] }
  };
  const GENERIC = { storage: "Storage", sink: "Sink", source: "Source", threshold: "Threshold (hystérésis)" };

  class Model {
    constructor(skins) {
      this.skins = skins;
      this.nodes = []; this.wires = []; this.nextId = 1;
      this.minutes = 0; this.history = [];
      this.listeners = new Set();
    }
    on(fn) { this.listeners.add(fn); }
    emit(type, detail) { for (const fn of this.listeners) fn(type, detail); }

    kindOf(n) { return this.skins[n.type].kind; }
    ports(n, side) { return KINDS[this.kindOf(n)][side === "in" ? "inputs" : "outputs"]; }
    byId(id) { return this.nodes.find(n => n.id === id); }
    first(type) { return this.nodes.find(n => n.type === type); }
    wiresTo(id, port) { return this.wires.filter(w => w.to.node === id && (!port || w.to.port === port)); }
    wiresFrom(id, port) { return this.wires.filter(w => w.from.node === id && (!port || w.from.port === port)); }
    linked(fromType, fromPort, toType, toPort) {
      return this.wires.some(w => this.byId(w.from.node).type === fromType && w.from.port === fromPort &&
                                  this.byId(w.to.node).type === toType && w.to.port === toPort);
    }

    addNode(type, x, y) {
      const n = { id: this.nextId++, type, x, y, p: {} };
      const ps = this.skins[type].params || {};
      for (const k in ps) n.p[k] = ps[k].v;
      this.resetNode(n);
      this.nodes.push(n);
      this.emit("node_add", type);
      return n;
    }
    removeNode(id) {
      const n = this.byId(id); if (!n) return;
      this.nodes = this.nodes.filter(m => m.id !== id);
      this.wires = this.wires.filter(w => w.from.node !== id && w.to.node !== id);
      this.emit("node_delete", n.type);
    }
    // Returns {ok:true, wire} or {ok:false, reason}. Ports must carry the same kind.
    connect(from, to) {
      const a = this.byId(from.node), b = this.byId(to.node);
      if (!a || !b) return { ok: false, reason: "missing" };
      if (a === b) return { ok: false, reason: "self" };
      const qo = this.ports(a, "out").find(q => q.id === from.port);
      const qi = this.ports(b, "in").find(q => q.id === to.port);
      if (!qo || !qi) return { ok: false, reason: "port" };
      if (qo.kind !== qi.kind) return { ok: false, reason: qo.kind === "flux" ? "flux_to_info" : "info_to_flux" };
      const dup = this.wires.find(w => w.from.node === a.id && w.from.port === from.port && w.to.node === b.id && w.to.port === to.port);
      if (dup) return { ok: true, wire: dup };
      if (!qi.multi) this.wires = this.wires.filter(w => !(w.to.node === b.id && w.to.port === to.port));
      const w = { id: this.nextId++, from: { node: a.id, port: from.port }, to: { node: b.id, port: to.port }, kind: qo.kind, power: 0 };
      this.wires.push(w);
      this.emit("wire_add", `${a.type}.${from.port} -> ${b.type}.${to.port}`);
      return { ok: true, wire: w };
    }
    removeWire(id) {
      this.wires = this.wires.filter(w => w.id !== id);
      this.emit("wire_delete", id);
    }

    resetNode(n) {
      const k = this.kindOf(n);
      if (k === "storage") n.s = { x: n.p.x0 };
      else if (k === "source") n.s = { u: 0, manual: n.s ? n.s.manual : 0 };
      else if (k === "threshold") n.s = { u: 1, x: null };
      else n.s = { open: n.s ? n.s.open : false };
    }
    resetAll() { this.minutes = 0; this.history = []; this.nodes.forEach(n => this.resetNode(n)); }

    // Value arriving on an information input, or null when nothing is plugged in.
    infoIn(n, port) {
      const w = this.wiresTo(n.id, port)[0];
      if (!w) return null;
      const src = this.byId(w.from.node), k = this.kindOf(src);
      if (k === "storage") return src.s.x;
      if (k === "threshold") return src.s.x === null ? 0 : src.s.u;
      return null;
    }

    // One step of dtMin simulated minutes: Newton exchange between storages,
    // bang-bang thresholds with hysteresis, sources on/off.
    step(dtMin) {
      const dtH = dtMin / 60;
      for (const n of this.nodes) {
        if (this.kindOf(n) !== "threshold") continue;
        const x = this.infoIn(n, "x"); n.s.x = x;
        if (x !== null) {
          if (x < n.p.set - n.p.h / 2) n.s.u = 1;
          else if (x > n.p.set + n.p.h / 2) n.s.u = 0;
        }
      }
      for (const n of this.nodes) {
        if (this.kindOf(n) !== "source") continue;
        const cmd = this.infoIn(n, "cmd");
        n.s.u = cmd === null ? n.s.manual : (cmd >= 0.5 ? 1 : 0);
      }
      const net = new Map();
      for (const w of this.wires) {
        if (w.kind !== "flux") continue;
        const a = this.byId(w.from.node), b = this.byId(w.to.node);
        const ka = this.kindOf(a), kb = this.kindOf(b);
        let p = 0;
        if (ka === "source") p = a.s.u * a.p.P / Math.max(1, this.wiresFrom(a.id, "flow").length);
        else if (ka === "storage") {
          const target = kb === "storage" ? b.s.x : kb === "sink" ? b.p.level : null;
          const g = a.p.k + (kb === "sink" && b.s.open ? (b.p.kOpen || 0) : 0);
          if (target !== null) p = g * (a.s.x - target);
        }
        w.power = p;
        if (ka === "storage") net.set(a.id, (net.get(a.id) || 0) - p);
        if (kb === "storage") net.set(b.id, (net.get(b.id) || 0) + p);
      }
      for (const n of this.nodes) if (this.kindOf(n) === "storage") n.s.x += dtH * (net.get(n.id) || 0) / n.p.C;
      this.minutes += dtMin;
      const snap = { m: this.minutes, x: {}, u: {}, open: false };
      for (const n of this.nodes) {
        const k = this.kindOf(n);
        if (k === "storage") snap.x[n.id] = n.s.x;
        if (k === "source") snap.u[n.id] = n.s.u;
        if (k === "sink" && n.s.open) snap.open = true;
      }
      this.history.push(snap);
      if (this.history.length > 1440) this.history.shift();
    }

    // ---- bindings, used by the Panneau: {piece, get:"level"|"u"} | {piece, set:"manual"} | {piece, param}
    isAuto(bind) {
      const n = this.first(bind.piece);
      return !!(n && bind.set === "manual" && this.wiresTo(n.id, "cmd").length);
    }
    read(bind) {
      const n = this.first(bind.piece);
      if (!n) return null;
      if (bind.get === "level") return n.s.x;
      if (bind.get === "u") return n.s.x === null ? null : n.s.u;
      if (bind.set === "manual") return this.isAuto(bind) ? n.s.u : n.s.manual;
      if (bind.param) return n.p[bind.param];
      return null;
    }
    write(bind, v) {
      const n = this.first(bind.piece);
      if (!n) return false;
      if (bind.set === "manual") {
        if (this.isAuto(bind)) return false;
        n.s.manual = v ? 1 : 0; n.s.u = n.s.manual; return true;
      }
      if (bind.param) {
        const d = (this.skins[n.type].params || {})[bind.param] || {};
        if (d.min !== undefined) v = Math.max(d.min, v);
        if (d.max !== undefined) v = Math.min(d.max, v);
        n.p[bind.param] = v; return true;
      }
      return false;
    }

    serialize() {
      return {
        nodes: this.nodes.map(n => ({ id: n.id, type: n.type, x: Math.round(n.x), y: Math.round(n.y), p: Object.assign({}, n.p) })),
        wires: this.wires.map(w => ({ from: w.from, to: w.to, kind: w.kind }))
      };
    }
  }

  K.KINDS = KINDS;
  K.GENERIC = GENERIC;
  K.Model = Model;
  K.fmtClock = m => `${Math.floor(m / 60)} h ${String(Math.round(m % 60)).padStart(2, "0")}`;
})(window.TSCGKit = window.TSCGKit || {});
