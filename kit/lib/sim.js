/* TSCG Kit — sim.js
 * Generic pieces and the fixed-step simulation.
 * The graph (nodes + wires) is the single source of truth: the Panneau and the
 * Maquette only read it (and write parameters through bindings).
 * Time is in the workshop's own unit (hours, seconds…): model.step(dt).
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";

  // Behaviour lives in the generic kind; a workshop gives each piece a "skin"
  // (name, port labels, parameters) on top of one of these kinds.
  // An `optional` port only exists on a skin that names it in its `ports`
  // (e.g. a Sink opened by a command: a drain, a valve).
  const KINDS = {
    storage:    { inputs:  [{ id: "in", kind: "flux", multi: true }],
                  outputs: [{ id: "out", kind: "flux" }, { id: "level", kind: "info" }] },
    sink:       { inputs:  [{ id: "in", kind: "flux", multi: true }, { id: "cmd", kind: "info", optional: true }], outputs: [] },
    source:     { inputs:  [{ id: "cmd", kind: "info" }], outputs: [{ id: "flow", kind: "flux" }] },
    threshold:  { inputs:  [{ id: "x", kind: "info" }], outputs: [{ id: "u", kind: "info" }] },
    amplify:    { inputs:  [{ id: "x", kind: "info" }], outputs: [{ id: "y", kind: "info" }] },
    transducer: { inputs:  [{ id: "x", kind: "info" }], outputs: [{ id: "flow", kind: "flux" }] },
    gradient:   { inputs:  [{ id: "a", kind: "info", multi: true }, { id: "b", kind: "info" }], outputs: [{ id: "d", kind: "info" }] },
    clock:      { inputs:  [], outputs: [{ id: "out", kind: "info" }] }
  };
  const GENERIC = { storage: "Storage", sink: "Sink", source: "Source", threshold: "Threshold (hystérésis)",
                    amplify: "Amplification", transducer: "Transducer", gradient: "Gradient (écart)", clock: "Clock (rythme)" };
  const INFO_ORDER = ["clock", "gradient", "amplify", "threshold"];
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
  const noise = a => a ? a * (Math.random() * 2 - 1) : 0;
  // repeatable pseudo-random number in [0,1) for day i (irregular days)
  const hash01 = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

  class Model {
    constructor(skins) {
      this.skins = skins;
      this.nodes = []; this.wires = []; this.nextId = 1;
      this.t = 0; this.steps = 0; this.history = [];
      this.env = { night: false };
      this.listeners = new Set();
    }
    on(fn) { this.listeners.add(fn); }
    emit(type, detail) { for (const fn of this.listeners) fn(type, detail); }

    kindOf(n) { return this.skins[n.type].kind; }
    ports(n, side) {
      const s = this.skins[n.type], all = KINDS[s.kind][side === "in" ? "inputs" : "outputs"];
      return all.filter(q => !q.optional || (s.ports && q.id in s.ports));
    }
    byId(id) { return this.nodes.find(n => n.id === id); }
    first(type) { return this.nodes.find(n => n.type === type); }
    all(type) { return this.nodes.filter(n => n.type === type); }
    // the block a binding aims at: a precise block when it names one ({node: id}), else the first of its type
    target(bind) { return bind.node != null ? this.byId(bind.node) : this.first(bind.piece); }
    // display name of a block: its skin name, numbered when several blocks share it ("Room 2")
    label(n) {
      const name = this.skins[n.type].name;
      return this.all(n.type).length > 1 ? `${name} ${n.num || 1}` : name;
    }
    wiresTo(id, port) { return this.wires.filter(w => w.to.node === id && (!port || w.to.port === port)); }
    wiresFrom(id, port) { return this.wires.filter(w => w.from.node === id && (!port || w.from.port === port)); }
    linked(fromType, fromPort, toType, toPort) {
      return this.wires.some(w => this.byId(w.from.node).type === fromType && w.from.port === fromPort &&
                                  this.byId(w.to.node).type === toType && w.to.port === toPort);
    }

    addNode(type, x, y) {
      const used = new Set(this.all(type).map(o => o.num));
      let num = 1; while (used.has(num)) num++;
      const n = { id: this.nextId++, type, num, x, y, p: {} };
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
      const k = this.kindOf(n), keep = n.s || {};
      if (k === "storage") n.s = { x: n.p.x0 };
      else if (k === "source") n.s = { u: 0, manual: keep.manual !== undefined ? keep.manual : (this.skins[n.type].on ? 1 : 0) };
      else if (k === "threshold") n.s = { u: this.skins[n.type].above ? 0 : 1, x: null };
      else if (k === "amplify") n.s = { y: 0, sat: 0 };
      else if (k === "transducer") n.s = { flow: 0, att: keep.att === undefined ? 1 : keep.att };
      else if (k === "gradient") n.s = { d: 0, a: null };
      else if (k === "clock") n.s = { v: null, day: false };
      else n.s = { open: !!keep.open };
    }
    resetAll() { this.t = 0; this.steps = 0; this.history = []; this.nodes.forEach(n => this.resetNode(n)); this.evalInfo(); }

    // The value a node presents on its information output (null = nothing to say).
    infoOut(src) {
      const k = this.kindOf(src);
      if (k === "storage") return src.s.x;
      if (k === "threshold") return src.s.x === null ? 0 : src.s.u;
      if (k === "amplify") return src.s.y;
      if (k === "gradient") return src.s.d;
      if (k === "clock") return src.s.v;
      return null;
    }
    // Value arriving on an information input. A multi input takes the first source that
    // speaks; sources whose skin says `fallback` speak only when no other one does.
    infoIn(n, port) {
      const ws = this.wiresTo(n.id, port);
      if (!ws.length) return null;
      const srcs = ws.map(w => this.byId(w.from.node));
      const ordered = srcs.filter(s => !this.skins[s.type].fallback).concat(srcs.filter(s => this.skins[s.type].fallback));
      for (const s of ordered) { const v = this.infoOut(s); if (v !== null && v !== undefined) return v; }
      return null;
    }

    clockValue(n) {
      const s = this.skins[n.type], t = this.t;
      if (s.mode === "fixed") return { v: n.p.angle, day: true };
      const day = Math.floor(t / 24), h = t - day * 24;
      if (s.mode === "sun") {
        const L = clamp(12 + (n.p.irr || 0) * (hash01(day) * 2 - 1) * 6, 4, 20);
        const rise = 12 - L / 2, set = 12 + L / 2;
        return h >= rise && h < set ? { v: -90 + 180 * (h - rise) / L, day: true } : { v: null, day: false };
      }
      if (s.mode === "night") {          // an internal rhythm on a fixed 24 h schedule: speaks from p.from to p.to (hours)
        const from = n.p.from === undefined ? 18 : n.p.from, to = n.p.to === undefined ? 6 : n.p.to;
        const on = from < to ? (h >= from && h < to) : (h >= from || h < to);
        return { v: on ? n.p.angle : null, day: !on };
      }
      return { v: null, day: false };
    }
    evalInfo() {
      for (let pass = 0; pass < 3; pass++) {
        for (const kind of INFO_ORDER) for (const n of this.nodes) {
          if (this.kindOf(n) !== kind) continue;
          if (kind === "clock") Object.assign(n.s, this.clockValue(n));
          else if (kind === "gradient") {
            const a = this.infoIn(n, "a"), b = this.infoIn(n, "b");
            n.s.a = a;
            if (pass === 2) n.s.d = a === null || b === null ? 0 : a - b + noise(n.p.noise);
            else n.s.d = a === null || b === null ? 0 : a - b;
          } else if (kind === "amplify") {
            const x = this.infoIn(n, "x") || 0, raw = n.p.gain * x;
            n.s.y = clamp(raw, -n.p.max, n.p.max); n.s.sat = Math.abs(raw) >= n.p.max ? 1 : 0;
          } else if (kind === "threshold" && pass === 2) {
            const x = this.infoIn(n, "x"); n.s.x = x;
            if (x !== null) {                // u = 1 below the band (or above it, for a skin with `above`)
              const up = !!this.skins[n.type].above;
              if (x < n.p.set - n.p.h / 2) n.s.u = up ? 0 : 1;
              else if (x > n.p.set + n.p.h / 2) n.s.u = up ? 1 : 0;
            }
          }
        }
      }
      const sun = this.nodes.find(n => this.kindOf(n) === "clock" && this.skins[n.type].mode === "sun");
      this.env.night = sun ? !sun.s.day : false;
    }

    // One step of dt (workshop time unit).
    step(dt) {
      this.evalInfo();
      for (const n of this.nodes) {
        const k = this.kindOf(n);
        if (k === "source") { const cmd = this.infoIn(n, "cmd"); n.s.u = cmd === null ? n.s.manual : (cmd >= 0.5 ? 1 : 0); }
        if (k === "sink" && this.wiresTo(n.id, "cmd").length) { const cmd = this.infoIn(n, "cmd"); n.s.open = cmd !== null && cmd >= 0.5; }
        if (k === "transducer") {
          const x = this.infoIn(n, "x") || 0;
          n.s.flow = clamp(n.p.k * n.s.att * x, -n.p.max, n.p.max) + noise(n.p.noise);
        }
      }
      const net = new Map();
      for (const w of this.wires) {
        if (w.kind !== "flux") continue;
        const a = this.byId(w.from.node), b = this.byId(w.to.node);
        const ka = this.kindOf(a), kb = this.kindOf(b);
        let p = 0;
        if (ka === "source") p = a.s.u * a.p.P / Math.max(1, this.wiresFrom(a.id, "flow").length);
        else if (ka === "transducer") p = a.s.flow / Math.max(1, this.wiresFrom(a.id, "flow").length);
        else if (ka === "storage") {
          const target = kb === "storage" ? b.s.x : kb === "sink" ? b.p.level : null;
          const g = a.p.k + (kb === "sink" && b.s.open ? (b.p.kOpen || 0) : 0);
          if (target !== null) p = g * (a.s.x - target);
        }
        w.power = p;
        if (ka === "storage") net.set(a.id, (net.get(a.id) || 0) - p);
        if (kb === "storage") net.set(b.id, (net.get(b.id) || 0) + p);
      }
      for (const n of this.nodes) {
        if (this.kindOf(n) !== "storage") continue;
        n.s.x += dt * ((net.get(n.id) || 0) + (n.p.base || 0)) / n.p.C;
        if (n.p.decay) n.s.x /= 1 + dt * n.p.decay;          // implicit: steady state = inflow / decay
        if (n.p.lo !== undefined) n.s.x = Math.max(n.p.lo, n.s.x);
        if (n.p.hi !== undefined) n.s.x = Math.min(n.p.hi, n.s.x);
      }
      this.t += dt; this.steps++;
      this.evalInfo();
      const snap = { t: this.t, v: {}, u: {}, open: false, night: this.env.night };
      for (const n of this.nodes) {
        const k = this.kindOf(n);
        if (k === "source") snap.u[n.id] = n.s.u;
        else if (k === "sink") { if (n.s.open) snap.open = true; }
        else if (k === "transducer") snap.v[n.id] = n.s.flow;
        else snap.v[n.id] = this.infoOut(n);
        if (k === "amplify") snap.u[n.id] = n.s.sat;
      }
      this.history.push(snap);
      if (this.history.length > 2000) this.history.shift();
    }

    // ---- bindings, used by the Panneau: {piece, get} | {piece, set:"manual"} | {piece, param}
    //      + an optional {node: id} to aim at one precise block among several of the same type
    isAuto(bind) {
      const n = this.target(bind);
      return !!(n && bind.set === "manual" && this.wiresTo(n.id, "cmd").length);
    }
    read(bind) {
      const n = this.target(bind);
      if (!n) return null;
      if (bind.get === "level") return n.s.x;
      if (bind.get === "u") return n.s.x === null ? null : n.s.u;
      if (bind.get) { const v = n.s[bind.get]; return v === undefined ? null : (typeof v === "boolean" ? (v ? 1 : 0) : v); }
      if (bind.set === "manual") return this.isAuto(bind) ? n.s.u : n.s.manual;
      if (bind.param) return n.p[bind.param];
      return null;
    }
    write(bind, v) {
      const n = this.target(bind);
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
  // default workshop clock: hours, one step = one minute
  K.CLOCK_HOURS = { dt: 1 / 60, stepsPerSec: 5, fmt: t => K.fmtClock(Math.round(t * 60)), fmtSteps: n => K.fmtClock(n) };
})(window.TSCGKit = window.TSCGKit || {});
