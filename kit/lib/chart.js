/* TSCG Kit — chart.js
 * Curves read from the Model history (one point per simulation step).
 * Configured by the workshop (W.chart):
 *   range:[lo,hi], tickY, span, tick, label(t)   axes, in the workshop's time unit
 *   band:[a,b], showBand(app)                    optional target zone
 *   series:[{piece, label, color, unit, decimals, fmt}]   default: every storage
 *   lines:[{piece, param | value(node), label, color, unit}]   dashed horizontal line at a parameter (e.g. set point)
 *   the legend shows the current value of every series and line
 *   strips:[{label, color, on(snap, model), shade}]  on/off bars under the curves,
 *                                                    or full-height shading (shade:true)
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  class Chart {
    constructor(canvas, model, o) { this.c = canvas; this.m = model; this.o = o; }
    draw() {
      const cv = this.c, m = this.m, o = this.o;
      const dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return;
      // resize the bitmap whenever the box changes (width OR height), or stale pixels stay visible
      if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
      const c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, w, h);
      const css = getComputedStyle(document.documentElement), v = n => css.getPropertyValue(n).trim();
      const col = x => (x || "").startsWith("--") ? v(x) : x;
      const [lo, hi] = o.range || [0, 32], tickY = o.tickY || 10;
      const strips = (o.strips || []).filter(s => !s.shade), shades = (o.strips || []).filter(s => s.shade);
      const L = 34, R = 8, T = 6, B = 22 + 7 * strips.length, pw = w - L - R, ph = h - T - B;
      const span = o.span || 8, t1 = Math.max(span, m.t), t0 = t1 - span;
      const X = t => L + (t - t0) / span * pw, Y = val => T + (1 - (clampV(val) - lo) / (hi - lo)) * ph;
      function clampV(val) { return Math.max(lo, Math.min(hi, val)); }
      const hist = m.history.filter(s => s.t >= t0);
      const bw = Math.max(1, pw / Math.max(1, span / (this.o.app ? this.o.app.clock.dt : 1)));
      for (const s of shades) {                    // full-height shading (e.g. night)
        c.fillStyle = col(s.color); c.globalAlpha = .14;
        for (const p of hist) if (s.on(p, m)) c.fillRect(X(p.t) - bw, T, bw + 0.5, ph);
        c.globalAlpha = 1;
      }
      c.font = "11px system-ui, sans-serif"; c.lineWidth = 1;
      for (let y = Math.ceil(lo / tickY) * tickY; y <= hi; y += tickY) {
        c.strokeStyle = v("--grid"); c.beginPath(); c.moveTo(L, Y(y)); c.lineTo(w - R, Y(y)); c.stroke();
        c.fillStyle = v("--quiet"); c.fillText(String(y), 2, Y(y) + 4);
      }
      const tick = o.tick || 2, label = o.label || (t => t + " h");
      for (let t = Math.ceil(t0 / tick - 1e-9) * tick; t <= t1 + 1e-9; t += tick) { c.fillStyle = v("--quiet"); c.fillText(label(+t.toFixed(6)), X(t) - 8, h - 2); }
      if (o.band && (!o.showBand || o.showBand(o.app))) { c.fillStyle = v("--band"); c.fillRect(L, Y(o.band[1]), pw, Y(o.band[0]) - Y(o.band[1])); }
      const legend = [];
      const series = o.series
        ? o.series.map(s => Object.assign({}, s, { node: m.first(s.piece), color: col(s.color) })).filter(s => s.node)
        : m.nodes.filter(n => m.kindOf(n) === "storage").map(n => ({ node: n, label: m.skins[n.type].name, color: m.skins[n.type].color || v("--flux"), unit: m.skins[n.type].unit }));
      const show = (s, val) => val === null || val === undefined ? "—" : s.fmt ? s.fmt(val) : val.toFixed(s.decimals !== undefined ? s.decimals : 1) + (s.unit ? " " + s.unit : "");
      const lineLegend = [];
      for (const ln of (o.lines || [])) {                 // dashed reference lines (set point…)
        const n = m.first(ln.piece); if (!n) continue;
        const val = ln.value ? ln.value(n) : n.p[ln.param], c2 = col(ln.color || "--good");
        c.save(); c.strokeStyle = c2; c.lineWidth = 1.5; c.setLineDash([6, 4]);
        c.beginPath(); c.moveTo(L, Y(val)); c.lineTo(w - R, Y(val)); c.stroke(); c.restore();
        lineLegend.push(`<span style="color:${c2}">┄</span> ${ln.label} <b>${show(ln, val)}</b>`);
      }
      for (const s of series) {
        const id = s.node.id;
        c.strokeStyle = s.color; c.lineWidth = 2; c.beginPath(); let on = false;
        for (const p of hist) {
          const val = p.v[id];
          if (val === null || val === undefined) { on = false; continue; }
          const x = X(p.t), y = Y(val);
          if (!on) { c.moveTo(x, y); on = true; } else c.lineTo(x, y);
        }
        c.stroke();
        const last = hist.length ? hist[hist.length - 1].v[id] : m.infoOut(s.node);
        legend.push(`<span style="color:${s.color}">■</span> ${s.label || m.skins[s.node.type].name} <b>${show(s, last)}</b>`);
      }
      legend.push(...lineLegend);
      strips.forEach((s, i) => {
        const y = h - B + 4 + 7 * i;
        c.fillStyle = col(s.color); c.globalAlpha = .6;
        let any = false;
        for (const p of hist) if (s.on(p, m)) { any = true; c.fillRect(X(p.t) - bw, y, bw + 0.5, 4); }
        c.globalAlpha = 1;
        if (any || m.history.some(p => s.on(p, m))) legend.push(`<span style="color:${col(s.color)};opacity:.7">▬</span> ${s.label}`);
      });
      for (const s of shades) if (m.history.some(p => s.on(p, m))) legend.push(`<span style="color:${col(s.color)};opacity:.5">█</span> ${s.label}`);
      if (o.legendEl) o.legendEl.innerHTML = legend.join(" &nbsp; ");
    }
  }
  K.Chart = Chart;
})(window.TSCGKit = window.TSCGKit || {});
