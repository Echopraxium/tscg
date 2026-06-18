/**
 * TSCG Simulation — Exposure Triangle (p5.js renderer)
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * Driven by:           M0_ExposureTriangle.jsonld
 * Primary metaconcepts: m2:Balance (A⊗S⊗F) + m2:Trade-off (R⊗V⊗E)
 * ASFID formula:       A ⊗ S ⊗ F ⊗ I ⊗ D
 *
 * Layout: equilateral triangle — ISO▲ (teal) / Aperture◁ (amber) / Shutter▷ (violet)
 *   • Each vertex draggable radially (same system as Fire Triangle)
 *   • COMP [0,1]: 0=min light, 1=max light for every parameter
 *   • EV gauge (left): signed offset from daylight baseline
 *   • Background: simulated photo responsive to all 3 parameters
 */

'use strict';

// ── Physical constants ─────────────────────────────────────────────────────
const BASELINE = { iso: 400, f: 5.6, t: 1 / 250 };
const ISO_MIN  = 100,    ISO_MAX = 6400;
const F_MIN    = 1.4,    F_MAX   = 22;
const T_MIN    = 1/4000, T_MAX   = 30;

// ── Physical ↔ normalised COMP conversions ─────────────────────────────────
// COMP=0 → minimum light contribution; COMP=1 → maximum light contribution
function isoVal(v)  { return ISO_MIN * Math.pow(ISO_MAX / ISO_MIN, v); }
function isoComp(x) { return Math.log(x / ISO_MIN) / Math.log(ISO_MAX / ISO_MIN); }
// Aperture inverted: COMP=0 → f/22 (dark), COMP=1 → f/1.4 (bright)
function fnumVal(v) { return F_MAX * Math.pow(F_MIN / F_MAX, v); }
function fComp(f)   { return Math.log(F_MAX / f) / Math.log(F_MAX / F_MIN); }
function tVal(v)    { return T_MIN * Math.pow(T_MAX / T_MIN, v); }
function tComp(t)   { return Math.log(t / T_MIN) / Math.log(T_MAX / T_MIN); }

// ── EV offset from daylight baseline ──────────────────────────────────────
function evOffset() {
  const iso = isoVal(COMP.iso);
  const f   = fnumVal(COMP.aperture);
  const t   = tVal(COMP.shutter);
  return (Math.log2(iso / BASELINE.iso)
        + 2 * Math.log2(BASELINE.f / f)
        + Math.log2(t / BASELINE.t));
}

// ── Formatting ─────────────────────────────────────────────────────────────
function fmtISO(v)     { return 'ISO\u00a0' + Math.round(isoVal(v)); }
function fmtFNum(v)    { return 'f/' + fnumVal(v).toFixed(1); }
function fmtShutter(v) {
  const t = tVal(v);
  if (t >= 1) return t.toFixed(1) + '\u2033';
  return '1/' + Math.round(1 / t) + '\u2033';
}

// ── EV colour: dark-blue (under) → amber (correct) → white (over) ─────────
function evColor(ev) {
  const t = Math.max(0, Math.min(1, (ev + 3) / 6));
  if (t < 0.5) {
    const f = t / 0.5;
    return [Math.round(25 + f * 230), Math.round(30 + f * 145), Math.round(110 - f * 90)];
  }
  const f = (t - 0.5) / 0.5;
  return [255, Math.round(175 + f * 80), Math.round(20 + f * 235)];
}

// ── Simulation state ───────────────────────────────────────────────────────
const SIM = {
  running:      true,
  speed:        1.0,
  time:         0,
  selectedPole: null
};

// COMP initial = baseline (EV ≈ 0)
const COMP  = { iso: isoComp(BASELINE.iso), aperture: fComp(BASELINE.f), shutter: tComp(BASELINE.t) };
const SAVED = { iso: COMP.iso, aperture: COMP.aperture, shutter: COMP.shutter };

// ── Particles ──────────────────────────────────────────────────────────────
let particles  = [];
let p5Instance = null;
const MAX_PARTS = 180;

class Particle {
  constructor(x, y, vx, vy, col, maxLife, size) {
    this.x = x; this.y = y; this.vx = vx; this.vy = vy;
    this.col = col; this.life = maxLife; this.maxLife = maxLife; this.size = size || 4;
  }
  update(dt) { this.x += this.vx * dt; this.y += this.vy * dt; this.life -= dt; }
  draw(p) {
    const a = Math.max(0, this.life / this.maxLife);
    const [r, g, b] = hexRgb(this.col);
    p.noStroke(); p.fill(r, g, b, a * 170);
    p.ellipse(this.x, this.y, this.size * (0.4 + 0.6 * a));
  }
  isDead() { return this.life <= 0; }
}

function hexRgb(hex) {
  return [parseInt(hex.slice(1,3),16), parseInt(hex.slice(3,5),16), parseInt(hex.slice(5,7),16)];
}

// ── DOM helpers ────────────────────────────────────────────────────────────
function updateStatusIndicator() {
  const dot   = document.getElementById('status-dot');
  const label = document.getElementById('status-label');
  if (!dot || !label) return;
  const ev = evOffset();
  if (!SIM.running) { dot.className='status-dot'; label.textContent='Paused'; return; }
  if (Math.abs(ev) < 0.5) {
    dot.className = 'status-dot running';
    label.textContent = 'Correct EV';
  } else {
    dot.className = 'status-dot cascade';
    label.textContent = ev > 0 ? `Over +${ev.toFixed(1)} EV` : `Under ${ev.toFixed(1)} EV`;
  }
}

function updatePoleInfoPanel(poleId) {
  const box = document.getElementById('pole-info');
  if (!box) return;
  if (!poleId) {
    box.innerHTML = '<div class="level-info-box"><span style="color:var(--muted)">Click a vertex to inspect its pole</span></div>';
    return;
  }
  const pole = POCLET_METADATA.poles.find(p => p.id === poleId);
  if (!pole) return;
  const val = COMP[poleId];
  let dispVal = '';
  if (poleId === 'iso')      dispVal = fmtISO(val);
  if (poleId === 'aperture') dispVal = fmtFNum(val);
  if (poleId === 'shutter')  dispVal = fmtShutter(val);

  box.innerHTML = `
    <div class="level-info-box">
      <div class="level-title">${pole.emoji} ${pole.label}
        <span class="level-rank">[${pole.sublabel}]</span>
      </div>
      <div style="font-size:11px;color:var(--text-dim);margin-bottom:4px">${pole.description}</div>
      <div style="font-size:10.5px;color:var(--warn);margin-bottom:3px">
        ⚖️ Trade-off: ${pole.tradeoff}
      </div>
      <div style="font-size:10px;color:var(--muted);margin-bottom:4px">${pole.examples}</div>
      <div style="font-size:10px;color:var(--muted)">
        ASFID: A=${pole.asfid.A} S=${pole.asfid.S} F=${pole.asfid.F} I=${pole.asfid.I} D=${pole.asfid.D}
      </div>
      <div style="font-size:11px;color:var(--sphinx);margin-top:4px;font-weight:600">Current: ${dispVal} (${(val*100).toFixed(0)}%)</div>
    </div>`;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  const btn = document.querySelector('[data-tab="scores"]');
  if (btn) { btn.classList.add('active'); document.getElementById('panel-scores').classList.add('active'); }
}

// ── Controls ───────────────────────────────────────────────────────────────
function wireControls() {
  const btnPlay  = document.getElementById('btn-play');
  const btnReset = document.getElementById('btn-reset');
  const speedSlider = document.getElementById('speed-slider');

  btnPlay.addEventListener('click', () => {
    SIM.running = !SIM.running;
    btnPlay.textContent = SIM.running ? '⏸ Pause' : '▶ Play';
    btnPlay.classList.toggle('active', SIM.running);
    if (p5Instance) { SIM.running ? p5Instance.loop() : p5Instance.noLoop(); }
    updateStatusIndicator();
  });

  btnReset.addEventListener('click', () => {
    Object.assign(COMP, { iso: isoComp(BASELINE.iso), aperture: fComp(BASELINE.f), shutter: tComp(BASELINE.t) });
    Object.assign(SAVED, COMP);
    SIM.time = 0; SIM.selectedPole = null; particles = [];
    syncCompSliders();
    SIM.running = true; btnPlay.textContent = '⏸ Pause'; btnPlay.classList.add('active');
    if (p5Instance) p5Instance.loop();
    updatePoleInfoPanel(null); updateStatusIndicator();
  });

  speedSlider.addEventListener('input', () => {
    SIM.speed = parseFloat(speedSlider.value);
    document.getElementById('speed-label').textContent = '×' + SIM.speed.toFixed(1);
  });
}

// ── Component sliders ──────────────────────────────────────────────────────
function initCompSliders() {
  [['sl-iso','iso',fmtISO], ['sl-aperture','aperture',fmtFNum], ['sl-shutter','shutter',fmtShutter]].forEach(([id, key, fmt]) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('input', () => {
      COMP[key] = parseFloat(el.value);
      const lbl = document.getElementById(id + '-val');
      if (lbl) lbl.textContent = fmt(COMP[key]);
      updateEVLabel();
    });
  });
  syncCompSliders();
}

function syncCompSliders() {
  [['sl-iso','iso',fmtISO], ['sl-aperture','aperture',fmtFNum], ['sl-shutter','shutter',fmtShutter]].forEach(([id, key, fmt]) => {
    const el = document.getElementById(id);
    if (el) el.value = COMP[key];
    const lbl = document.getElementById(id + '-val');
    if (lbl) lbl.textContent = fmt(COMP[key]);
  });
  updateEVLabel();
}

function updateEVLabel() {
  const ev  = evOffset();
  const el  = document.getElementById('ev-display');
  if (!el) return;
  const col = Math.abs(ev) < 0.5 ? 'var(--accent)' : ev > 0 ? 'var(--eagle)' : 'var(--sphinx)';
  el.textContent = `EV ${ev >= 0 ? '+' : ''}${ev.toFixed(2)}`;
  el.style.color = col;
}

// ── p5 sketch ──────────────────────────────────────────────────────────────
function initP5() {
  const container = document.getElementById('canvas-area');

  const sketch = function(p) {
    let W, H, cx, cy, R;
    let verts = [];

    const POLE_ANGLES = [-Math.PI / 2, Math.PI / 2 + Math.PI / 3, Math.PI / 2 - Math.PI / 3];

    // Photo overlay geometry (top-right corner, over the triangle)
    let photoX, photoY, photoW, photoH;
    const PHOTO_RATIO = 658 / 438;   // width / height of photo_sample.jpg

    function computeGeometry() {
      W  = container.clientWidth  || 640;
      H  = container.clientHeight || 560;
      // Triangle fills the full canvas
      R  = Math.min(W, H) * 0.38;
      cx = W * 0.34;
      cy = H / 2 + R * 0.55;
      // Photo overlay: top-right corner, ~32% of canvas width
      const pad = 16;
      photoW = Math.round(W * 0.44);
      photoH = Math.round(photoW / PHOTO_RATIO);
      photoX = W - pad - photoW;
      photoY = pad;
      verts = POCLET_METADATA.poles.map((pole, i) => ({
        ...pole,
        angle: POLE_ANGLES[i],
        rx: cx + R * Math.cos(POLE_ANGLES[i]),
        ry: cy + R * Math.sin(POLE_ANGLES[i]),
        x:  cx + COMP[pole.id] * R * Math.cos(POLE_ANGLES[i]),
        y:  cy + COMP[pole.id] * R * Math.sin(POLE_ANGLES[i])
      }));
    }

    function updateVertPositions() {
      verts.forEach(v => {
        v.x = cx + COMP[v.id] * R * Math.cos(v.angle);
        v.y = cy + COMP[v.id] * R * Math.sin(v.angle);
      });
    }

    // ── Photo image ─────────────────────────────────────────────
    let baseImg    = null;   // p5.Image — photo_sample.jpg
    let photoCache = null;   // p5.Graphics — cached processed result
    let prevCompKey = '';    // detect COMP changes → invalidate cache

    // ── Drag state ─────────────────────────────────────────────
    let dragPole = null, didDrag = false;

    function radialValue(v) {
      const dx = p.mouseX - cx, dy = p.mouseY - cy;
      return Math.max(0, Math.min(1, (dx * Math.cos(v.angle) + dy * Math.sin(v.angle)) / R));
    }

    p.setup = function() {
      const cnv = p.createCanvas(container.clientWidth || 640, container.clientHeight || 560);
      cnv.canvas.style.position = 'absolute'; cnv.canvas.style.top = '0'; cnv.canvas.style.left = '0';
      computeGeometry();
      p.textFont('Segoe UI, system-ui, sans-serif');
      new ResizeObserver(() => {
        p.resizeCanvas(container.clientWidth, container.clientHeight);
        computeGeometry();
        photoCache = null;  // invalidate on resize
      }).observe(container);

      // Load photo_sample.jpg via native HTMLImageElement (fully bypasses p5/fetch/CSP)
      try {
        const nodePath = require('path');
        const fs       = require('fs');
        const photoPath = nodePath.join(__dirname, 'photo_sample.jpg');
        if (fs.existsSync(photoPath)) {
          const b64     = fs.readFileSync(photoPath).toString('base64');
          const dataURL = 'data:image/jpeg;base64,' + b64;
          // Use native HTMLImageElement — no fetch, no XHR, no CSP issue
          const htmlImg = new Image();
          htmlImg.onload = () => {
            // Wrap in p5.Image so pg.image() works
            const pImg = p.createImage(htmlImg.naturalWidth, htmlImg.naturalHeight);
            pImg.drawingContext.drawImage(htmlImg, 0, 0);
            baseImg = pImg;
          };
          htmlImg.onerror = e => console.warn('[TSCG] photo load error:', e);
          htmlImg.src = dataURL;
        } else {
          console.warn('[TSCG] photo_sample.jpg not found at', photoPath);
        }
      } catch(e) { console.warn('[TSCG] photo load skipped:', e.message); }
    };

    p.draw = function() {
      if (!SIM.running) return;
      SIM.time += SIM.speed * 0.016;
      updateVertPositions();

      const ev = evOffset();

      p.background(13, 17, 23);
      drawBackground(p, ev);   // dark gradient left area
      drawPhoto(p, ev);         // photo panel top-right
      if (particles.length < MAX_PARTS) spawnParticles(p);
      particles = particles.filter(pt => !pt.isDead());
      particles.forEach(pt => { pt.update(SIM.speed); pt.draw(p); });

      drawTriangle(p, ev);
      verts.forEach(v => drawVertex(p, v));
      drawLabels(p, ev);
      drawEVGauge(p, ev);

      if (!dragPole) {
        const near = verts.some(v => p.dist(p.mouseX, p.mouseY, v.x, v.y) < 44);
        container.style.cursor = near ? 'grab' : 'default';
      }
      updateStatusIndicator();
      syncCompSliders();
    };

    p.mousePressed = function() {
      if (p.mouseX < 0 || p.mouseX > p.width || p.mouseY < 0 || p.mouseY > p.height) return;
      verts.forEach(v => {
        if (p.dist(p.mouseX, p.mouseY, v.x, v.y) < 44) {
          dragPole = v.id; didDrag = false; container.style.cursor = 'grabbing';
        }
      });
    };

    p.mouseDragged = function() {
      if (!dragPole) return;
      didDrag = true;
      const v = verts.find(vt => vt.id === dragPole);
      COMP[dragPole] = radialValue(v);
    };

    p.mouseReleased = function() {
      if (dragPole) container.style.cursor = 'default';
      dragPole = null;
    };

    p.mouseClicked = function() {
      if (didDrag) { didDrag = false; return; }
      if (p.mouseX < 0 || p.mouseX > p.width || p.mouseY < 0 || p.mouseY > p.height) return;
      let found = null;
      verts.forEach(v => { if (p.dist(p.mouseX, p.mouseY, v.x, v.y) < 40) found = v.id; });
      SIM.selectedPole = found;
      updatePoleInfoPanel(found);
    };

    // ── Background — full canvas dark gradient ───────────────────
    function drawBackground(p, ev) {
      p.noStroke();
      p.fill(13, 17, 23); p.rect(0, 0, W, H);
      for (let y = 0; y < H; y += 2) {
        const t = y / H;
        p.stroke(15 + t * 18, 20 + t * 14, 40 + t * 8, 60);
        p.line(0, y, W, y);
      }
      p.drawingContext.setLineDash([]);
    }

    // ── Photo panel (top-right) with live exposure effects ────────
    function drawPhoto(p, ev) {
      // Panel backdrop — semi-transparent dark frame
      p.noStroke();
      p.fill(8, 10, 16, 210);
      p.rect(photoX - 6, photoY - 6, photoW + 12, photoH + 28, 8);

      const compKey = [COMP.iso, COMP.aperture, COMP.shutter].map(v => v.toFixed(3)).join('|');
      const needsRedraw = (compKey !== prevCompKey) || !photoCache;

      if (needsRedraw) {
        prevCompKey = compKey;
        if (!photoCache || photoCache.width !== photoW || photoCache.height !== photoH) {
          if (photoCache) photoCache.remove();
          photoCache = p.createGraphics(photoW, photoH);
        }
        const pg = photoCache;
        pg.clear();

        if (baseImg) {
          // Draw base image scaled to panel
          pg.image(baseImg, 0, 0, photoW, photoH);
        } else {
          // Gradient placeholder (autumn leaves palette)
          for (let y = 0; y < photoH; y++) {
            const t = y / photoH;
            pg.stroke(Math.round(80 + t * 60), Math.round(40 + t * 30), Math.round(10 + t * 15));
            pg.line(0, y, photoW, y);
          }
        }

        // ── Apply exposure effects as pixel overlay ───────────────
        pg.loadPixels();
        const px = pg.pixels;
        const ev_ = ev;
        const brightness = Math.pow(2, ev_ * 0.80);

        // Brightness + noise (ISO)
        const isoStops  = Math.log2(Math.max(1, isoVal(COMP.iso) / 100));
        const noiseAmp  = isoStops / Math.log2(64) * 55;

        for (let i = 0; i < px.length; i += 4) {
          const n = noiseAmp > 1 ? (Math.random() - 0.5) * noiseAmp * 2 : 0;
          px[i]   = Math.max(0, Math.min(255, px[i]   * brightness + n));
          px[i+1] = Math.max(0, Math.min(255, px[i+1] * brightness + n));
          px[i+2] = Math.max(0, Math.min(255, px[i+2] * brightness + n));
        }
        pg.updatePixels();

        // Vignette (wide aperture → shallow DoF = edge darkening)
        const fnum = fnumVal(COMP.aperture);
        if (fnum < 5.6) {
          const vigStr = (5.6 - fnum) / (5.6 - F_MIN) * 0.72;
          const vSteps = 28;
          for (let i = 0; i < vSteps; i++) {
            const t  = i / vSteps;
            const rr = Math.max(photoW, photoH) * (0.46 + t * 0.65);
            pg.noStroke();
            pg.fill(5, 8, 13, vigStr * t * t * 210);
            pg.ellipse(photoW / 2, photoH / 2, rr * 2, rr * 2);
          }
        }

        // Motion blur (slow shutter → horizontal streaks)
        const tSec = tVal(COMP.shutter);
        const blurStops = Math.max(0, Math.log2(tSec / 0.02));
        const blurAmt   = Math.min(1, blurStops / 4.5);
        if (blurAmt > 0.05) {
          const numS = Math.round(blurAmt * 50);
          for (let i = 0; i < numS; i++) {
            const sy = Math.random() * photoH;
            const sw = photoW * blurAmt * (0.2 + Math.random() * 0.8);
            const sx = Math.random() * (photoW - sw);
            const sa = blurAmt * 22 * Math.random();
            const g  = 150 + Math.random() * 80;
            pg.noStroke(); pg.fill(g, g, g * 0.9, sa);
            pg.rect(sx, sy, sw, 3);
          }
        }
      }

      // Blit cached panel
      if (photoCache) p.image(photoCache, photoX, photoY);

      // Border
      p.noFill();
      p.stroke(60, 70, 90, 180); p.strokeWeight(1);
      p.rect(photoX - 1, photoY - 1, photoW + 2, photoH + 2, 4);

      // Effects legend below photo
      const legY = photoY + photoH + 8;
      const isoStops = Math.log2(Math.max(1, isoVal(COMP.iso) / 100));
      const grainPct = Math.round(isoStops / Math.log2(64) * 100);
      const tSec2    = tVal(COMP.shutter);
      const blurPct  = Math.round(Math.min(100, Math.max(0, Math.log2(tSec2 / 0.02)) / 4.5 * 100));
      const fnum2    = fnumVal(COMP.aperture);
      const vigPct   = fnum2 < 5.6 ? Math.round((5.6 - fnum2) / (5.6 - F_MIN) * 100) : 0;

      p.textSize(10); p.textStyle(p.NORMAL); p.noStroke();
      const legends = [
        [`Grain ${grainPct}%`,    '#50d2d2'],
        [`Blur ${blurPct}%`,      '#c86eff'],
        [`Vignette ${vigPct}%`,   '#ffaf2d']
      ];
      let lx = photoX;
      legends.forEach(([txt, col]) => {
        const [r, g, b] = hexRgb(col);
        p.fill(r, g, b, 200);
        p.textAlign(p.LEFT, p.TOP);
        p.text(txt, lx, legY);
        lx += p.textWidth(txt) + 22;
      });

      // Photo label
      p.fill(70, 80, 95, 180);
      p.textAlign(p.RIGHT, p.TOP);
      p.textSize(9);
      p.text('photo_sample.jpg · Territory view', photoX + photoW, legY);
    }

    // ── Triangle outline + fill ────────────────────────────────────
    function drawTriangle(p, ev) {
      // Reference triangle (all at COMP=1, max light)
      p.drawingContext.setLineDash([6, 5]);
      p.stroke(121, 192, 255, 55);
      p.strokeWeight(1.2);
      p.noFill();
      p.beginShape();
      verts.forEach(v => p.vertex(v.rx, v.ry));
      p.endShape(p.CLOSE);
      p.drawingContext.setLineDash([]);

      // EV fill
      const [er, eg, eb] = evColor(ev);
      p.noStroke();
      p.fill(er, eg, eb, 28 + Math.abs(Math.sin(SIM.time * 1.2)) * 8);
      p.beginShape();
      verts.forEach(v => p.vertex(v.x, v.y));
      p.endShape(p.CLOSE);

      // Sides — blended colour between adjacent vertex colours
      const vcols = verts.map(v => hexRgb(v.color));
      const burning = Math.abs(ev) < 0.5;

      for (let i = 0; i < 3; i++) {
        const j   = (i + 1) % 3;
        const v1  = verts[i], v2 = verts[j];
        const c1  = vcols[i], c2 = vcols[j];
        const mix = c1.map((c, k) => Math.round((c + c2[k]) / 2));

        if (burning) {
          const pulse = 0.5 + 0.5 * Math.sin(SIM.time * 2.2 + i);
          p.stroke(mix[0], mix[1], mix[2], (18 + 14 * pulse) | 0);
          p.strokeWeight(10); p.noFill();
          p.line(v1.x, v1.y, v2.x, v2.y);
        }
        p.stroke(mix[0], mix[1], mix[2], burning ? 210 : 160);
        p.strokeWeight(burning ? 2.5 : 1.8); p.noFill();
        p.line(v1.x, v1.y, v2.x, v2.y);
      }
      p.drawingContext.setLineDash([]);
    }

    // ── Vertex circles (same drag system as Fire Triangle) ────────
    function drawVertex(p, v) {
      const val        = COMP[v.id];
      const [r, g, b]  = hexRgb(v.color);
      const isDragging = dragPole === v.id;
      const selected   = SIM.selectedPole === v.id;
      const pulse      = 0.5 + 0.5 * Math.sin(SIM.time * 2.6 + (v.id === 'iso' ? 0 : v.id === 'aperture' ? 2 : 4));
      const cr         = (selected || isDragging) ? 22 : 18;

      // Radial rail (centre → 100% ref)
      p.drawingContext.setLineDash([6, 4]);
      p.stroke(r, g, b, isDragging ? 200 : 90);
      p.strokeWeight(isDragging ? 1.8 : 1.3);
      p.line(cx, cy, v.rx, v.ry);
      p.drawingContext.setLineDash([]);

      // Outer glow
      p.noStroke();
      p.fill(r, g, b, (18 + 14 * pulse) | 0);
      p.ellipse(v.x, v.y, (cr + 22) * 2, (cr + 22) * 2);

      // Circle body
      p.fill(r, g, b, 170);
      if (selected || isDragging) { p.stroke(255, 255, 255, 180); p.strokeWeight(2); }
      else                        { p.stroke(r, g, b, 220); p.strokeWeight(1.5); }
      p.ellipse(v.x, v.y, cr * 2, cr * 2);

      // Value arc (0 → current COMP)
      const arcAngle = val * p.TWO_PI;
      p.noFill();
      p.stroke(r, g, b, 220);
      p.strokeWeight(2.5);
      p.arc(v.x, v.y, (cr + 8) * 2, (cr + 8) * 2, -p.HALF_PI, -p.HALF_PI + arcAngle);

      // Baseline tick (COMP at EV=0 for this parameter)
      const baseComp = v.baselineComp;
      const tickA  = baseComp * p.TWO_PI - p.HALF_PI;
      const tr     = cr + 10;
      p.stroke(227, 179, 65, 200);
      p.strokeWeight(2);
      p.line(v.x + (tr - 5) * Math.cos(tickA), v.y + (tr - 5) * Math.sin(tickA),
             v.x + (tr + 5) * Math.cos(tickA), v.y + (tr + 5) * Math.sin(tickA));
    }

    // ── Labels ─────────────────────────────────────────────────────
    function drawLabels(p, ev) {
      p.textAlign(p.CENTER, p.CENTER);
      p.noStroke();

      verts.forEach(v => {
        const [r, g, b] = hexRgb(v.color);
        const dx = v.x - cx, dy = v.y - cy;
        const len = Math.sqrt(dx * dx + dy * dy) || 1;
        const lx  = v.x + (dx / len) * 54;
        const ly  = v.y + (dy / len) * 54;

        // Name
        p.fill(r, g, b, 240);
        p.textSize(13); p.textStyle(p.BOLD);
        p.text(v.emoji + '\u00a0' + v.label, lx, ly);

        // Current value
        let dispVal = '';
        if (v.id === 'iso')      dispVal = fmtISO(COMP[v.id]);
        if (v.id === 'aperture') dispVal = fmtFNum(COMP[v.id]);
        if (v.id === 'shutter')  dispVal = fmtShutter(COMP[v.id]);
        p.fill(220, 230, 235, 210);
        p.textSize(11); p.textStyle(p.NORMAL);
        p.text(dispVal, lx, ly + 17);
      });

      // Centre: EV state
      p.textAlign(p.CENTER, p.CENTER);
      const [er, eg, eb] = evColor(ev);
      const evText = Math.abs(ev) < 0.5
        ? 'BALANCED'
        : ev > 0 ? `+${ev.toFixed(1)} EV  OVER` : `${ev.toFixed(1)} EV  UNDER`;
      const pulse = 0.6 + 0.4 * Math.sin(SIM.time * 3);
      p.fill(er, eg, eb, (210 * (Math.abs(ev) < 0.5 ? 1 : pulse)) | 0);
      p.textSize(14); p.textStyle(p.BOLD);
      p.text(evText, cx, cy + R * 0.38);

      p.fill(100, 110, 120, 90);
      p.textSize(9); p.textStyle(p.NORMAL);
      p.text('m2:Balance', cx, cy - R * 0.38);
    }

    // ── EV Gauge (left side) ───────────────────────────────────────
    function drawEVGauge(p, ev) {
      const gx     = 38;
      const gW     = 14;
      const gTop   = H * 0.12;
      const gBot   = H * 0.82;
      const gH     = gBot - gTop;
      const gCy    = gTop + gH / 2;   // EV=0 centre
      const EV_MAX = 4;               // ±4 EV display range

      // Track
      p.noStroke();
      p.fill(28, 33, 45, 200);
      p.rect(gx - gW / 2 - 2, gTop - 4, gW + 4, gH + 8, 5);

      // Fill: from centre toward over (red) or under (blue)
      const fillH = Math.min(gH / 2, (Math.abs(ev) / EV_MAX) * gH / 2);
      if (ev > 0.1) {
        // Overexposed: fill upward from centre
        const steps = Math.max(1, Math.round(fillH));
        for (let i = 0; i < steps; i++) {
          const frac = i / Math.max(1, steps - 1);
          const col  = evColor(frac * EV_MAX);
          p.fill(col[0], col[1], col[2], 200);
          p.rect(gx - gW / 2, gCy - i - 1, gW, 2);
        }
      } else if (ev < -0.1) {
        // Underexposed: fill downward from centre
        const steps = Math.max(1, Math.round(fillH));
        for (let i = 0; i < steps; i++) {
          const frac = i / Math.max(1, steps - 1);
          const col  = evColor(-frac * EV_MAX);
          p.fill(col[0], col[1], col[2], 200);
          p.rect(gx - gW / 2, gCy + i - 1, gW, 2);
        }
      } else {
        // Correct exposure: green centre pulse
        const pulse = 0.5 + 0.5 * Math.sin(SIM.time * 3);
        p.fill(86, 211, 100, (160 + 60 * pulse) | 0);
        p.rect(gx - gW / 2, gCy - 4, gW, 8, 3);
      }

      // Track border
      p.noFill(); p.stroke(60, 70, 90, 180); p.strokeWeight(1);
      p.rect(gx - gW / 2 - 2, gTop - 4, gW + 4, gH + 8, 5);

      // EV tick marks
      const ticks = [-3, -2, -1, 0, 1, 2, 3];
      ticks.forEach(tv => {
        const ty      = gCy - (tv / EV_MAX) * gH / 2;
        const reached = (tv > 0 && ev >= tv) || (tv < 0 && ev <= tv) || tv === 0;
        const isZero  = tv === 0;
        p.stroke(reached ? 200 : 55, isZero ? 211 : reached ? 200 : 65, isZero ? 100 : reached ? 200 : 80, reached ? 180 : 80);
        p.strokeWeight(isZero ? 1.5 : 1);
        p.line(gx - gW / 2 - 2, ty, gx + gW / 2 + 6, ty);
        p.noStroke();
        p.fill(reached ? 180 : 70, reached ? 185 : 80, reached ? 195 : 90, reached ? 200 : 110);
        p.textAlign(p.LEFT, p.CENTER);
        p.textSize(9); p.textStyle(p.NORMAL);
        p.text((tv > 0 ? '+' : '') + tv, gx + gW / 2 + 9, ty);
      });

      // Current EV label
      const [er, eg, eb] = evColor(ev);
      p.noStroke();
      p.fill(er, eg, eb, 240);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.textSize(11); p.textStyle(p.BOLD);
      p.text((ev >= 0 ? '+' : '') + ev.toFixed(2) + ' EV', gx, gTop - 10);

      // Title
      p.fill(120, 130, 145, 180);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.textSize(8); p.textStyle(p.NORMAL);
      p.text('EXPOSURE', gx, gTop - 22);

      // Bulb
      const bCol = evColor(ev);
      p.noStroke(); p.fill(bCol[0], bCol[1], bCol[2], 210);
      p.ellipse(gx, gBot + 10, 20, 20);
      p.stroke(60, 70, 90, 150); p.strokeWeight(1); p.noFill();
      p.ellipse(gx, gBot + 10, 20, 20);
    }

    // ── Particle spawning ───────────────────────────────────────────
    function spawnParticles(p) {
      const dt = SIM.speed;
      verts.forEach(v => {
        const val = COMP[v.id];
        if (val < 0.08) return;
        const rate = 0.20 * val;
        if (Math.random() > rate * dt) return;
        const angle = Math.atan2(cy - v.y, cx - v.x) + (Math.random() - 0.5) * 0.6;
        const speed = 1.0 + Math.random() * 1.5;
        particles.push(new Particle(
          v.x + (Math.random() - 0.5) * 18,
          v.y + (Math.random() - 0.5) * 18,
          Math.cos(angle) * speed, Math.sin(angle) * speed,
          v.color, 30 + Math.random() * 25, 3 + Math.random() * 4
        ));
      });
    }

  }; // end sketch

  p5Instance = new p5(sketch, container);
}

// ── Entry point ────────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  wireControls();
  initCompSliders();
  initP5();
});
