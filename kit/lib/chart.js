/* TSCG Kit — chart.js
 * Curves of every storage level over the last hours, read from the Model history.
 * Optional target band, source on/off strip and perturbation strip.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  class Chart {
    // o: { range:[lo,hi], band:[a,b], showBand(), legendEl, perturbLabel }
    constructor(canvas, model, o) { this.c = canvas; this.m = model; this.o = o; }
    draw() {
      const cv = this.c, m = this.m, o = this.o;
      const dpr = window.devicePixelRatio || 1, w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return;
      if (cv.width !== Math.round(w * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
      const c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, w, h);
      const css = getComputedStyle(document.documentElement), v = n => css.getPropertyValue(n).trim();
      const [lo, hi] = o.range || [0, 32];
      const L = 32, R = 8, T = 6, B = 30, pw = w - L - R, ph = h - T - B;
      const span = 480, m1 = Math.max(span, m.minutes), m0 = m1 - span;
      const X = t => L + (t - m0) / span * pw, Y = val => T + (1 - (val - lo) / (hi - lo)) * ph;
      c.font = "11px system-ui, sans-serif"; c.lineWidth = 1;
      for (let t = Math.ceil(lo / 10) * 10; t <= hi; t += 10) {
        c.strokeStyle = v("--grid"); c.beginPath(); c.moveTo(L, Y(t)); c.lineTo(w - R, Y(t)); c.stroke();
        c.fillStyle = v("--quiet"); c.fillText(t + "°", 2, Y(t) + 4);
      }
      for (let t = Math.ceil(m0 / 120) * 120; t <= m1; t += 120) { c.fillStyle = v("--quiet"); c.fillText(Math.round(t / 60) + " h", X(t) - 8, h - 2); }
      if (o.band && o.showBand()) { c.fillStyle = v("--band"); c.fillRect(L, Y(o.band[1]), pw, Y(o.band[0]) - Y(o.band[1])); }
      const legend = [];
      const storages = m.nodes.filter(n => m.kindOf(n) === "storage");
      for (const n of storages) {
        const col = m.skins[n.type].color || v("--flux");
        c.strokeStyle = col; c.lineWidth = 2; c.beginPath(); let on = false;
        for (const s of m.history) {
          if (s.m < m0 || !(n.id in s.x)) { on = false; continue; }
          const x = X(s.m), y = Y(Math.max(lo, Math.min(hi, s.x[n.id])));
          if (!on) { c.moveTo(x, y); on = true; } else c.lineTo(x, y);
        }
        c.stroke();
        legend.push(`<span style="color:${col}">■</span> ${m.skins[n.type].name}`);
      }
      const src = m.nodes.find(n => m.kindOf(n) === "source");
      const bw = Math.max(1, pw / span);
      if (src) {
        c.fillStyle = v("--flux"); c.globalAlpha = .55;
        for (const s of m.history) if (s.m >= m0 && s.u[src.id]) c.fillRect(X(s.m - 1), h - B + 4, bw, 4);
        c.globalAlpha = 1; legend.push(`<span style="color:${v("--flux")};opacity:.6">▬</span> ${m.skins[src.type].name} en marche`);
      }
      if (m.history.some(s => s.open)) {
        c.fillStyle = v("--info"); c.globalAlpha = .55;
        for (const s of m.history) if (s.m >= m0 && s.open) c.fillRect(X(s.m - 1), h - B + 10, bw, 4);
        c.globalAlpha = 1; legend.push(`<span style="color:${v("--info")};opacity:.6">▬</span> ${o.perturbLabel || "perturbation"}`);
      }
      if (o.legendEl) o.legendEl.innerHTML = legend.join(" &nbsp; ");
    }
  }
  K.Chart = Chart;
})(window.TSCGKit = window.TSCGKit || {});
