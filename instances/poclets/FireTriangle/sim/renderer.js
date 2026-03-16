/**
 * TSCG Simulation \u2014 Fire Triangle (p5.js renderer)
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * Driven by:           M0_FireTriangle.jsonld
 * Primary metaconcept: m2:Balance \u2014 A\u2297S\u2297I  (ternary co-presence above threshold)
 * ASFID formula:       A \u2297 S \u2297 F \u2297 I \u2297 D
 *
 * Layout: equilateral triangle (Heat\u25b2 / Fuel\u25c1 / O\u2082\u25b7) on p5.js canvas.
 *   \u2022 Each vertex has a value slider in the Components bar.
 *   \u2022 Flame animates at center when all 3 components \u2265 threshold.
 *   \u2022 Extinction buttons drop one component below its threshold.
 *   \u2022 Click a vertex to inspect its pole detail in the Scores tab.
 */

'use strict';

// \u2500\u2500 Simulation state \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
const SIM = {
  running:      true,
  speed:        1.0,
  time:         0,
  ignitionTime: 0,
  wasBurning:   false,
  selectedPole: null,  // 'heat' | 'fuel' | 'oxygen' | null
  temp:         0      // [0..1] — combustion temperature (drives flame color + size)
};

// Component values [0..1]
const COMP  = { heat: 0.58, fuel: 0.62, oxygen: 0.60 };

// Ignition thresholds (below these \u2192 that component is "broken")
const THRESH = { heat: 0.25, fuel: 0.30, oxygen: 0.16 };

// Saved values for toggle-restore on extinction buttons
const SAVED  = { heat: 0.58, fuel: 0.62, oxygen: 0.60 };

// \u2500\u2500 Particles \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
let particles   = [];
let p5Instance  = null;
const MAX_PARTS = 220;

class Particle {
  constructor(x, y, vx, vy, col, maxLife, size) {
    this.x = x; this.y = y;
    this.vx = vx; this.vy = vy;
    this.col = col;
    this.life = maxLife; this.maxLife = maxLife;
    this.size = size || 5;
  }
  update(dt) {
    this.x    += this.vx * dt;
    this.y    += this.vy * dt;
    this.vy   -= 0.05 * dt;          // gentle buoyancy
    this.life -= dt;
  }
  draw(p) {
    const a = Math.max(0, this.life / this.maxLife);
    const [r, g, b] = hexRgb(this.col);
    p.noStroke();
    p.fill(r, g, b, a * 190);
    const s = this.size * (0.4 + 0.6 * a);
    p.ellipse(this.x, this.y, s, s);
  }
  isDead() { return this.life <= 0; }
}

// \u2500\u2500 Helpers \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function hexRgb(hex) {
  return [
    parseInt(hex.slice(1, 3), 16),
    parseInt(hex.slice(3, 5), 16),
    parseInt(hex.slice(5, 7), 16)
  ];
}

function isBurning() {
  return COMP.heat   > THRESH.heat   &&
         COMP.fuel   > THRESH.fuel   &&
         COMP.oxygen > THRESH.oxygen;
}

function poleByKey(key) {
  return POCLET_METADATA.poles.find(p => p.id === key);
}

// \u2500\u2500 DOM update helpers \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function updateStatusIndicator() {
  const dot   = document.getElementById('status-dot');
  const label = document.getElementById('status-label');
  if (!dot || !label) return;
  if (!SIM.running) {
    dot.className   = 'status-dot';
    label.textContent = 'Paused';
    return;
  }
  if (isBurning()) {
    dot.className   = 'status-dot cascade';
    label.textContent = 'COMBUSTION';
  } else {
    dot.className   = 'status-dot running';
    label.textContent = 'Running';
  }
}

function updatePoleInfoPanel(poleId) {
  const box = document.getElementById('pole-info');
  if (!box) return;
  if (!poleId) {
    box.innerHTML = '<div class="level-info-box"><span style="color:var(--muted)">Click a vertex to inspect its pole</span></div>';
    return;
  }
  const pole = poleByKey(poleId);
  if (!pole) return;
  const val   = COMP[poleId];
  const above = val > pole.threshold;
  const col   = above ? 'var(--accent)' : 'var(--eagle)';
  const status = above
    ? `\u2714 Active \u2014 ${(val * 100).toFixed(0)}% (threshold: ${(pole.threshold * 100).toFixed(0)}%)`
    : `\u2717 Below threshold \u2014 ${(val * 100).toFixed(0)}% < ${(pole.threshold * 100).toFixed(0)}%`;
  box.innerHTML = `
    <div class="level-info-box">
      <div class="level-title">${pole.emoji} ${pole.label}
        <span class="level-rank">[${pole.sublabel}]</span>
      </div>
      <div style="font-size:11px;color:var(--text-dim);margin-bottom:4px">${pole.description}</div>
      <div style="font-size:10.5px;color:var(--warn);margin-bottom:3px">
        \u2702\ufe0f Extinction: ${pole.extinctionMethod}
      </div>
      <div style="font-size:10px;color:var(--muted)">
        ASFID: A=${pole.asfid.A} S=${pole.asfid.S} F=${pole.asfid.F} I=${pole.asfid.I} D=${pole.asfid.D}
      </div>
      <div style="font-size:11px;color:${col};margin-top:4px;font-weight:600">${status}</div>
    </div>`;
  // Auto-switch to Scores tab
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  const btn = document.querySelector('[data-tab="scores"]');
  if (btn) {
    btn.classList.add('active');
    document.getElementById('panel-scores').classList.add('active');
  }
}

// \u2500\u2500 Controls \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function wireControls() {
  const btnPlay    = document.getElementById('btn-play');
  const btnReset   = document.getElementById('btn-reset');
  const btnSmother = document.getElementById('btn-smother');
  const btnFreeze   = document.getElementById('btn-freeze');
  const btnDefuel  = document.getElementById('btn-defuel');
  const speedSlider = document.getElementById('speed-slider');

  btnPlay.addEventListener('click', () => {
    SIM.running = !SIM.running;
    btnPlay.textContent = SIM.running ? '\u23f8 Pause' : '\u25b6 Play';
    btnPlay.classList.toggle('active', SIM.running);
    if (p5Instance) { SIM.running ? p5Instance.loop() : p5Instance.noLoop(); }
    updateStatusIndicator();
  });

  btnReset.addEventListener('click', () => {
    Object.assign(COMP,  { heat: 0.58, fuel: 0.62, oxygen: 0.60 });
    Object.assign(SAVED, { heat: 0.58, fuel: 0.62, oxygen: 0.60 });
    SIM.time = 0; SIM.ignitionTime = 0; SIM.wasBurning = false; SIM.selectedPole = null; SIM.temp = 0;
    particles = [];
    syncCompSliders();
    SIM.running = true;
    btnPlay.textContent = '\u23f8 Pause'; btnPlay.classList.add('active');
    if (p5Instance) p5Instance.loop();
    [btnSmother, btnFreeze, btnDefuel].forEach(b => b && b.classList.remove('active'));
    updatePoleInfoPanel(null);
    updateStatusIndicator();
  });

  // Extinction toggles
  function makeExtinctionToggle(btn, key) {
    if (!btn) return;
    btn.addEventListener('click', () => {
      const suppressed = COMP[key] <= THRESH[key] + 0.05;
      if (suppressed) {
        COMP[key] = SAVED[key];   // restore
        btn.classList.remove('active');
      } else {
        SAVED[key] = COMP[key];   // save before suppressing
        COMP[key] = THRESH[key] * 0.4;   // well below threshold
        btn.classList.add('active');
      }
      syncCompSliders();
    });
  }
  makeExtinctionToggle(btnSmother, 'oxygen');
  makeExtinctionToggle(btnFreeze,   'heat');
  makeExtinctionToggle(btnDefuel,  'fuel');

  speedSlider.addEventListener('input', () => {
    SIM.speed = parseFloat(speedSlider.value);
    document.getElementById('speed-label').textContent = '\u00d7' + SIM.speed.toFixed(1);
  });
}

function initCompSliders() {
  const defs = [
    { id: 'sl-heat',   key: 'heat',   lbl: 'sl-heat-val'   },
    { id: 'sl-fuel',   key: 'fuel',   lbl: 'sl-fuel-val'   },
    { id: 'sl-oxygen', key: 'oxygen', lbl: 'sl-oxygen-val' }
  ];
  defs.forEach(({ id, key, lbl }) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('input', () => {
      COMP[key] = parseFloat(el.value);
      const lblEl = document.getElementById(lbl);
      if (lblEl) lblEl.textContent = (COMP[key] * 100).toFixed(0) + '%';
      updateCompWarnings();
    });
  });
  syncCompSliders();
}

function syncCompSliders() {
  [['sl-heat','heat'],['sl-fuel','fuel'],['sl-oxygen','oxygen']].forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (el) el.value = COMP[key];
    const lbl = document.getElementById(id + '-val');
    if (lbl) lbl.textContent = (COMP[key] * 100).toFixed(0) + '%';
  });
  updateCompWarnings();
}

function updateCompWarnings() {
  const warn = document.getElementById('comp-warnings');
  if (!warn) return;
  const msgs = [];
  if (COMP.fuel   <= THRESH.fuel)   msgs.push('\u26a0 Fuel below threshold \u2014 no combustion');
  if (COMP.oxygen <= THRESH.oxygen) msgs.push('\u26a0 O\u2082 < 16% \u2014 fire smothered');
  if (COMP.heat   <= THRESH.heat)   msgs.push('\u26a0 Heat below activation energy');
  if (!msgs.length) {
    msgs.push(isBurning()
      ? '\uD83D\uDD25 Combustion active \u2014 all conditions met'
      : '\u2713 Components ready for ignition');
  }
  warn.innerHTML = msgs.map(m =>
    `<div style="color:${m.startsWith('\u26a0') ? 'var(--warn)' : m.startsWith('\uD83D\uDD25') ? 'var(--eagle)' : 'var(--accent)'};font-size:10.5px">${m}</div>`
  ).join('');
}

// \u2500\u2500 p5 sketch \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
function initP5() {
  const container = document.getElementById('canvas-area');

  const sketch = function(p) {
    let W, H, cx, cy, R;
    let verts = [];   // [{...pole, angle, rx, ry, x, y}]
                      // rx/ry = reference position at COMP=1.0
                      // x/y   = current position (= COMP * R along radial axis)

    // Angles: Heat = top (-PI/2), Fuel = bottom-left, O2 = bottom-right
    const POLE_ANGLES = [-Math.PI / 2, Math.PI / 2 + Math.PI / 3, Math.PI / 2 - Math.PI / 3];

    function computeGeometry() {
      W = container.clientWidth  || 640;
      H = container.clientHeight || 560;
      R  = Math.min(W, H) * 0.42;
      cx = W * 0.46;
      cy = H / 2 + R * 0.25;
      verts = POCLET_METADATA.poles.map((pole, i) => ({
        ...pole,
        angle: POLE_ANGLES[i],
        rx: cx + R * Math.cos(POLE_ANGLES[i]),   // 100% reference position
        ry: cy + R * Math.sin(POLE_ANGLES[i]),
        x:  cx + COMP[pole.id] * R * Math.cos(POLE_ANGLES[i]),
        y:  cy + COMP[pole.id] * R * Math.sin(POLE_ANGLES[i])
      }));
    }

    // Recompute actual x/y from COMP each frame (geometry stays fixed)
    function updateVertPositions() {
      verts.forEach(v => {
        v.x = cx + COMP[v.id] * R * Math.cos(v.angle);
        v.y = cy + COMP[v.id] * R * Math.sin(v.angle);
      });
    }

    p.setup = function() {
      const cnv = p.createCanvas(
        container.clientWidth  || 640,
        container.clientHeight || 560
      );
      cnv.canvas.style.position = 'absolute';
      cnv.canvas.style.top      = '0';
      cnv.canvas.style.left     = '0';
      computeGeometry();
      p.textFont('Segoe UI, system-ui, sans-serif');

      new ResizeObserver(() => {
        p.resizeCanvas(container.clientWidth, container.clientHeight);
        computeGeometry();
      }).observe(container);
    };

    p.draw = function() {
      if (!SIM.running) return;
      SIM.time += SIM.speed * 0.016;

      // Keep vertex positions in sync with COMP values
      updateVertPositions();

      // Ignition edge detection
      const burning = isBurning();
      if (burning && !SIM.wasBurning) SIM.ignitionTime = SIM.time;
      SIM.wasBurning = burning;

      // ── Temperature dynamics ─────────────────────────────────────
      // Target: product of normalised COMP excess above each threshold
      if (burning) {
        const fi = Math.max(0, (COMP.fuel   - THRESH.fuel)   / (1 - THRESH.fuel));
        const oi = Math.max(0, (COMP.oxygen - THRESH.oxygen) / (1 - THRESH.oxygen));
        const hi = Math.max(0, (COMP.heat   - THRESH.heat)   / (1 - THRESH.heat));
        const target = Math.pow(fi * oi * hi, 0.45);
        SIM.temp += (target - SIM.temp) * 0.006 * SIM.speed;  // slow rise
      } else {
        SIM.temp += (0 - SIM.temp) * 0.018 * SIM.speed;       // faster cool-down
      }
      SIM.temp = Math.max(0, Math.min(1, SIM.temp));

      // Background
      p.background(13, 17, 23);
      drawDotGrid(p);

      // Particles
      if (particles.length < MAX_PARTS) spawnParticles(p);
      particles = particles.filter(pt => !pt.isDead());
      particles.forEach(pt => { pt.update(SIM.speed); pt.draw(p); });

      // Scene
      drawTriangle(p);
      if (burning || SIM.temp > 0.02) drawFlame(p);
      verts.forEach(v => drawVertex(p, v));
      drawLabels(p);
      drawTempGauge(p);

      updateStatusIndicator();
    };

    // ── Drag state ─────────────────────────────────────────────────
    let dragPole  = null;   // id of vertex being dragged
    let didDrag   = false;  // suppress click when drag happened

    // Project mouse onto the radial axis of a vertex; return clamped [0..1] value
    function radialValue(v) {
      const dx = p.mouseX - cx, dy = p.mouseY - cy;
      const ax = Math.cos(v.angle), ay = Math.sin(v.angle);
      const proj = dx * ax + dy * ay;          // signed projection onto axis
      return Math.max(0, Math.min(1, proj / R));
    }

    p.mousePressed = function() {
      if (p.mouseX < 0 || p.mouseX > p.width || p.mouseY < 0 || p.mouseY > p.height) return;
      verts.forEach(v => {
        if (p.dist(p.mouseX, p.mouseY, v.x, v.y) < 44) {
          dragPole = v.id;
          didDrag  = false;
          container.style.cursor = 'grabbing';
        }
      });
    };

    p.mouseDragged = function() {
      if (!dragPole) return;
      didDrag = true;
      const v   = verts.find(vt => vt.id === dragPole);
      const val = radialValue(v);
      COMP[dragPole] = val;
      syncCompSliders();    // keep sliders in sync
    };

    p.mouseReleased = function() {
      if (dragPole) container.style.cursor = 'default';
      dragPole = null;
    };

    p.mouseClicked = function() {
      if (didDrag) { didDrag = false; return; }   // was a drag, not a click
      if (p.mouseX < 0 || p.mouseX > p.width || p.mouseY < 0 || p.mouseY > p.height) return;
      let found = null;
      verts.forEach(v => {
        if (p.dist(p.mouseX, p.mouseY, v.x, v.y) < 40) found = v.id;
      });
      SIM.selectedPole = found;
      updatePoleInfoPanel(found);
    };

    // ── Background dot grid ─────────────────────────────────────────
    function drawDotGrid(p) {
      p.noStroke();
      p.fill(255, 255, 255, 7);
      const sp = 32;
      for (let x = sp; x < W; x += sp)
        for (let y = sp; y < H; y += sp)
          p.ellipse(x, y, 1.8, 1.8);
    }

    // ── Triangle outline ────────────────────────────────────────────
    function drawTriangle(p) {
      // ── Reference triangle (all poles at 100%) — light blue outline ──
      p.drawingContext.setLineDash([6, 5]);
      p.stroke(121, 192, 255, 160);   // sphinx blue, lumineux
      p.strokeWeight(1.8);
      p.noFill();
      p.beginShape();
      verts.forEach(v => p.vertex(v.rx, v.ry));
      p.endShape(p.CLOSE);
      p.drawingContext.setLineDash([]);

      // Side order: Heat\u2192Fuel, Fuel\u2192O2, O2\u2192Heat
      // Colour of each side = the opposite vertex's component (what it "protects")
      const sides = [
        { from: 0, to: 1, compKey: 'oxygen', col: '#79c0ff' },  // O2-side
        { from: 1, to: 2, compKey: 'heat',   col: '#f78166' },  // Heat-side
        { from: 2, to: 0, compKey: 'fuel',   col: '#56d364' }   // Fuel-side
      ];

      const burning = isBurning();

      sides.forEach(s => {
        const v1  = verts[s.from];
        const v2  = verts[s.to];
        const val = COMP[s.compKey];
        const thr = THRESH[s.compKey];
        const active = val > thr;
        const [r, g, b] = hexRgb(s.col);

        if (!active) p.drawingContext.setLineDash([9, 6]);
        else         p.drawingContext.setLineDash([]);

        // Glow pass when burning
        if (active && burning) {
          const pulse = 0.5 + 0.5 * Math.sin(SIM.time * 2.8);
          p.strokeWeight(10);
          p.stroke(r, g, b, (20 + 18 * pulse) | 0);
          p.noFill();
          p.line(v1.x, v1.y, v2.x, v2.y);
        }

        // Main line
        p.strokeWeight(active ? 2.5 + val * 2.5 : 1.2);
        p.stroke(r, g, b, active ? 200 : 50);
        p.noFill();
        p.line(v1.x, v1.y, v2.x, v2.y);
      });
      p.drawingContext.setLineDash([]);

      // Warm fill when burning
      if (burning) {
        const age  = SIM.time - SIM.ignitionTime;
        const fill = Math.min(1, age * 2.5);
        p.noStroke();
        p.fill(255, 110, 25, (fill * 20 + 7 * Math.sin(SIM.time * 1.8)) | 0);
        p.beginShape();
        verts.forEach(v => p.vertex(v.x, v.y));
        p.endShape(p.CLOSE);
      }
    }

    // ── Vertex circles ─────────────────────────────────────────────────────
    function drawVertex(p, v) {
      const val        = COMP[v.id];
      const [r, g, b]  = hexRgb(v.color);
      const isDragging = dragPole === v.id;
      const active     = val > v.threshold;
      const selected   = SIM.selectedPole === v.id;
      const pulse      = 0.5 + 0.5 * Math.sin(SIM.time * 2.6 + (v.id === 'heat' ? 0 : v.id === 'fuel' ? 2 : 4));
      const cr         = (selected || isDragging) ? 22 : 18;

      // ── Radial rail (centre → 100% ref position) — drag guide
      p.drawingContext.setLineDash([6, 4]);
      p.stroke(r, g, b, isDragging ? 200 : 90);
      p.strokeWeight(isDragging ? 1.8 : 1.3);
      p.line(cx, cy, v.rx, v.ry);
      p.drawingContext.setLineDash([]);

      // Outer glow
      p.noStroke();
      p.fill(r, g, b, active ? (18 + 14 * pulse) | 0 : 8);
      p.ellipse(v.x, v.y, (cr + 22) * 2, (cr + 22) * 2);

      // Circle body
      p.fill(r, g, b, active ? 170 : 50);
      if (selected || isDragging) { p.stroke(255, 255, 255, 180); p.strokeWeight(2); }
      else                        { p.stroke(r, g, b, active ? 220 : 80); p.strokeWeight(1.5); }
      p.ellipse(v.x, v.y, cr * 2, cr * 2);

      // Value arc
      const arcAngle = val * p.TWO_PI;
      p.noFill();
      p.stroke(r, g, b, active ? 210 : 100);
      p.strokeWeight(2.5);
      p.arc(v.x, v.y, (cr + 8) * 2, (cr + 8) * 2, -p.HALF_PI, -p.HALF_PI + arcAngle);

      // Threshold tick
      const tickA = v.threshold * p.TWO_PI - p.HALF_PI;
      const tr    = cr + 10;
      p.stroke(227, 179, 65, 180);
      p.strokeWeight(2);
      p.line(v.x + (tr - 5) * Math.cos(tickA), v.y + (tr - 5) * Math.sin(tickA),
             v.x + (tr + 5) * Math.cos(tickA), v.y + (tr + 5) * Math.sin(tickA));

      // Warning ring when below threshold
      if (!active) {
        const wp = 0.5 + 0.5 * Math.sin(SIM.time * 5.5);
        p.noFill();
        p.stroke(247, 129, 102, (160 * wp) | 0);
        p.strokeWeight(2);
        p.ellipse(v.x, v.y, (cr + 16) * 2, (cr + 16) * 2);
      }
    }

    // ── Labels ──────────────────────────────────────────────────────
    function drawLabels(p) {
      p.textAlign(p.CENTER, p.CENTER);
      p.noStroke();

      verts.forEach(v => {
        const val    = COMP[v.id];
        const active = val > v.threshold;
        const [r, g, b] = hexRgb(v.color);

        // Offset label outward from center
        const dx  = v.x - cx, dy = v.y - cy;
        const len = Math.sqrt(dx * dx + dy * dy);
        const lx  = v.x + (dx / len) * 52;
        const ly  = v.y + (dy / len) * 52;

        // Name + emoji
        p.fill(r, g, b, active ? 240 : 110);
        p.textSize(13);
        p.textStyle(p.BOLD);
        p.text(v.emoji + '\u00a0' + v.label, lx, ly);

        // Value
        p.fill(active ? 220 : 110, active ? 230 : 110, active ? 235 : 115, 210);
        p.textSize(11);
        p.textStyle(p.NORMAL);
        p.text((val * 100).toFixed(0) + '%', lx, ly + 17);

        // Threshold
        p.fill(227, 179, 65, 150);
        p.textSize(10);
        p.text('min\u00a0' + (v.threshold * 100).toFixed(0) + '%', lx, ly + 30);
      });

      // Center status
      p.textAlign(p.CENTER, p.CENTER);
      if (isBurning()) {
        const pulse = 0.55 + 0.45 * Math.sin(SIM.time * 4);
        p.fill(255, 135, 25, (220 * pulse) | 0);
        p.textSize(14); p.textStyle(p.BOLD);
        p.text('COMBUSTION', cx, cy + R * 0.40);
        p.fill(180, 180, 180, 140);
        p.textSize(10); p.textStyle(p.NORMAL);
        p.text('C + O\u2082 \u2192 CO\u2082 + \u0394H', cx, cy + R * 0.40 + 18);
      } else {
        p.fill(139, 148, 158, 160);
        p.textSize(11); p.textStyle(p.ITALIC);
        const missing = [];
        if (COMP.fuel   <= THRESH.fuel)   missing.push('Fuel\u2191');
        if (COMP.oxygen <= THRESH.oxygen) missing.push('O\u2082\u2191');
        if (COMP.heat   <= THRESH.heat)   missing.push('Heat\u2191');
        p.text(missing.length ? 'No ignition: ' + missing.join(', ') : 'Ready', cx, cy + R * 0.40);
      }

      // Center "synergy zone" label
      p.textStyle(p.NORMAL);
      p.fill(100, 110, 120, 90);
      p.textSize(9);
      p.text('m2:Balance', cx, cy - R * 0.40);
    }

    // ── Temperature → colour interpolation ─────────────────────────
    // Stops: dark-red → red → orange → yellow → yellow-white → white-hot
    function tempColor(T) {
      const stops = [
        [0.00, 140,   8,   0],
        [0.20, 255,  30,   0],
        [0.45, 255, 120,   0],
        [0.70, 255, 210,  20],
        [0.85, 255, 240, 110],
        [1.00, 255, 255, 230]
      ];
      T = Math.max(0, Math.min(1, T));
      for (let i = 1; i < stops.length; i++) {
        if (T <= stops[i][0]) {
          const s0 = stops[i - 1], s1 = stops[i];
          const f  = (T - s0[0]) / (s1[0] - s0[0]);
          return [
            Math.round(s0[1] + (s1[1] - s0[1]) * f),
            Math.round(s0[2] + (s1[2] - s0[2]) * f),
            Math.round(s0[3] + (s1[3] - s0[3]) * f)
          ];
        }
      }
      return [255, 255, 230];
    }

    // ── Flame (size + colour driven by SIM.temp) ────────────────────
    function drawFlame(p) {
      const T = SIM.temp;
      if (T < 0.02) return;

      // Height: grows from tiny to tall as T rises
      const flH = R * (0.18 + 0.80 * T);

      p.push();
      p.translate(cx, cy + R * 0.12);

      // Four concentric layers: outer (cooler) → core (hotter)
      // Each layer references a different point on the temperature scale
      const layerDefs = [
        { sc: 1.00, tFactor: 0.50, alpha: 185 },  // outer envelope — cooler
        { sc: 0.72, tFactor: 0.75, alpha: 210 },  // mid zone
        { sc: 0.44, tFactor: 1.00, alpha: 225 },  // inner zone — actual T
        { sc: 0.18, tFactor: 1.25, alpha: 240 }   // white-hot core — hotter
      ];

      layerDefs.forEach(({ sc, tFactor, alpha }) => {
        const col     = tempColor(Math.min(1, T * tFactor));
        const wobble  = Math.sin(SIM.time * (3.0 + sc * 5)) * 7 * sc;
        const wBase   = R * (0.10 + 0.18 * T) * sc;
        const hLayer  = flH * sc;

        p.noStroke();
        p.fill(col[0], col[1], col[2], (alpha * T) | 0);
        p.beginShape();
        p.vertex(wobble, -hLayer);
        p.bezierVertex(
           wBase + wobble, -hLayer * 0.5,
           wBase * 1.4,     hLayer * 0.12,
           0,               hLayer * 0.18
        );
        p.bezierVertex(
          -wBase * 1.4,     hLayer * 0.12,
          -wBase + wobble, -hLayer * 0.5,
           wobble,         -hLayer
        );
        p.endShape(p.CLOSE);
      });

      // Base glow halo — colour follows temperature
      const haloCol = tempColor(T * 0.6);
      const gR      = R * 0.16 * T;
      p.noStroke();
      p.fill(haloCol[0], haloCol[1], haloCol[2], (40 * T) | 0);
      p.ellipse(0, flH * 0.12, gR * 2.2, gR * 1.3);

      p.pop();
    }

    // ── Temperature gauge ───────────────────────────────────────────
    // Vertical thermometer on the left side of the canvas.
    // Scale: 20 °C (T=0) → 2 000 °C (T=1)
    function drawTempGauge(p) {
      const T       = SIM.temp;
      const gx      = 38;          // centre-x of the gauge bar
      const gW      = 14;          // bar width
      const gTop    = H * 0.12;    // gauge top y
      const gBottom = H * 0.82;    // gauge bottom y
      const gH      = gBottom - gTop;

      const tempC   = Math.round(20 + T * 1980);  // °C display value

      // ── Background track ─────────────────────────────────────────
      p.noStroke();
      p.fill(28, 33, 45, 200);
      p.rect(gx - gW / 2 - 2, gTop - 4, gW + 4, gH + 8, 5);

      // ── Filled portion (bottom → current level) ──────────────────
      const fillH  = gH * T;
      const fillY  = gBottom - fillH;

      if (T > 0.005) {
        // Draw gradient by thin horizontal slices
        const steps = Math.max(1, Math.round(fillH));
        for (let i = 0; i < steps; i++) {
          const frac = i / Math.max(1, steps - 1);          // 0=bottom 1=top
          const col  = tempColor(T * frac);
          p.noStroke();
          p.fill(col[0], col[1], col[2], 210);
          p.rect(gx - gW / 2, fillY + (steps - 1 - i) * (fillH / steps),
                 gW, fillH / steps + 1);
        }
      }

      // ── Track border ─────────────────────────────────────────────
      p.noFill();
      p.stroke(60, 70, 90, 180);
      p.strokeWeight(1);
      p.rect(gx - gW / 2 - 2, gTop - 4, gW + 4, gH + 8, 5);

      // ── Tick marks + labels (physical temperatures) ───────────────
      const ticks = [
        { c: 300,  label: '300°C',  note: 'Wood ignition'   },
        { c: 580,  label: '580°C',  note: 'Methane'         },
        { c: 1200, label: '1200°C', note: 'Wood flame'      },
        { c: 1800, label: '1800°C', note: 'Acetylene'       }
      ];

      ticks.forEach(({ c, label, note }) => {
        const tNorm = (c - 20) / 1980;
        const ty    = gBottom - gH * tNorm;
        const reachd = T >= tNorm;

        p.stroke(reachd ? 200 : 55, reachd ? 200 : 65, reachd ? 200 : 80, reachd ? 160 : 80);
        p.strokeWeight(1);
        p.line(gx - gW / 2 - 2, ty, gx + gW / 2 + 6, ty);

        p.noStroke();
        p.fill(reachd ? 180 : 80, reachd ? 185 : 90, reachd ? 195 : 100, reachd ? 200 : 110);
        p.textAlign(p.LEFT, p.CENTER);
        p.textSize(9);
        p.textStyle(p.NORMAL);
        p.text(label, gx + gW / 2 + 9, ty);
      });

      // ── Current temperature label ─────────────────────────────────
      const labelY = Math.max(gTop + 10, Math.min(gBottom - 10, gBottom - gH * T - 10));
      const col    = tempColor(T);
      p.noStroke();
      p.fill(col[0], col[1], col[2], T > 0.02 ? 240 : 100);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.textSize(12);
      p.textStyle(p.BOLD);
      p.text(tempC + ' °C', gx, labelY);

      // ── Title ─────────────────────────────────────────────────────
      p.fill(120, 130, 145, 180);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.textSize(9);
      p.textStyle(p.NORMAL);
      p.text('TEMP', gx, gTop - 8);

      // ── Bulb at bottom ────────────────────────────────────────────
      const bCol = tempColor(T);
      p.noStroke();
      p.fill(bCol[0], bCol[1], bCol[2], T > 0.02 ? 210 : 60);
      p.ellipse(gx, gBottom + 10, 20, 20);
      p.stroke(60, 70, 90, 150);
      p.strokeWeight(1);
      p.noFill();
      p.ellipse(gx, gBottom + 10, 20, 20);
    }

    // ── Particle spawning ───────────────────────────────────────────
    function spawnParticles(p) {
      const dt = SIM.speed;
      const burning = isBurning();

      // Per-vertex particles flowing toward center
      verts.forEach(v => {
        const val   = COMP[v.id];
        const thresh = THRESH[v.id];
        if (val < thresh * 0.4) return;

        const rate = v.id === 'heat' ? 0.22 : v.id === 'fuel' ? 0.28 : 0.20;
        if (Math.random() > rate * dt) return;

        const angle = Math.atan2(cy - v.y, cx - v.x) + (Math.random() - 0.5) * 0.7;
        const speed = 1.3 + Math.random() * 1.8;
        const jx    = (Math.random() - 0.5) * 20;
        const jy    = (Math.random() - 0.5) * 20;
        particles.push(new Particle(
          v.x + jx, v.y + jy,
          Math.cos(angle) * speed, Math.sin(angle) * speed,
          v.color, 38 + Math.random() * 30,
          4 + Math.random() * 5
        ));
      });

      // Combustion products (CO2/smoke) rising from center when burning
      if (burning && Math.random() < 0.55 * dt) {
        particles.push(new Particle(
          cx + (Math.random() - 0.5) * R * 0.12,
          cy - R * 0.05,
          (Math.random() - 0.5) * 1.2,
          -(1.8 + Math.random() * 2.5),
          '#e3b341', 28 + Math.random() * 22, 4 + Math.random() * 4
        ));
      }
    }

  }; // end sketch

  p5Instance = new p5(sketch, container);
}

// \u2500\u2500 Entry point \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
window.addEventListener('DOMContentLoaded', () => {
  wireControls();
  initCompSliders();
  initP5();
});
