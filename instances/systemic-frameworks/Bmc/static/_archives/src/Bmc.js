/**
 * TSCG — Business Model Canvas Simulation
 * Author: Echopraxium with the collaboration of Claude AI
 * Date: 2026-06-20
 *
 * Architecture:
 *   - HTML/CSS: layout, sidebar, controls (native)
 *   - p5.js: 9-block BMC canvas + animated flux particles
 *   - Morphism: lerp-based interpolation between phase configs over MORPH_MS ms
 */

'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MORPH_MS    = 1800;   // morphism duration in ms
const MAX_PARTS   = 280;    // particle pool size
const PHASE_NAMES  = ['Démarrage', 'Croissance', 'Maturité', 'Déclin', 'Transition'];
const PH_COLORS    = ['#4A90E2', '#22C97A', '#F5A623', '#E64141', '#E8A020'];
const PHASE_TRANSITION_IDX = 4;  // index of Transition phase

// ASFID color palette
const COL = {
  A: '#ffb840', S: '#64c8ff', F: '#3dc896', It: '#c882ff', D: '#ff6464',
  bg: '#0d1117', panel: '#161b22', card: '#1c2130', border: '#30363d',
  text: '#e6edf3', muted: '#8b949e'
};

// ── BMC Block definitions (layout proportional coords 0-1) ────────────────
// Layout mirrors canonical BMC: left=infra, center=VP, right=customer
// Grid: 5 columns × 2 rows  (VP spans full height in col 2)
//   col0: KP        rows 0+1
//   col1: KA row0 / KR row1
//   col2: VP        rows 0+1  (center)
//   col3: CR row0 / CH row1
//   col4: CS        rows 0+1
// Bottom band: C$ (cols 0-1-2) | RS (cols 3-4)
const BLOCKS = [
  { id:'KP', label:'Key Partners',        abbr:'KP', dim:'S',  col:0, row:0, colSpan:1, rowSpan:2 },
  { id:'KA', label:'Key Activities',      abbr:'KA', dim:'F',  col:1, row:0, colSpan:1, rowSpan:1 },
  { id:'KR', label:'Key Resources',       abbr:'KR', dim:'S',  col:1, row:1, colSpan:1, rowSpan:1 },
  { id:'VP', label:'Value Proposition',   abbr:'VP', dim:'A',  col:2, row:0, colSpan:1, rowSpan:2 },
  { id:'CR', label:'Customer Relations',  abbr:'CR', dim:'D',  col:3, row:0, colSpan:1, rowSpan:1 },
  { id:'CH', label:'Channels',            abbr:'CH', dim:'F',  col:3, row:1, colSpan:1, rowSpan:1 },
  { id:'CS', label:'Customer Segments',   abbr:'CS', dim:'It', col:4, row:0, colSpan:1, rowSpan:2 },
  { id:'CS$', label:'Cost Structure',     abbr:'C$', dim:'F',  col:0, row:2, colSpan:3, rowSpan:1 },
  { id:'RS', label:'Revenue Streams',     abbr:'RS', dim:'F',  col:3, row:2, colSpan:2, rowSpan:1 },
];

// Tooltip descriptions per block
// → See usecases.js
// ── Flux paths (from → to, color dimension, base intensity key) ────────────
// Each path: list of block IDs forming the route
const FLUX_PATHS = [
  { id:'vp_ch',   from:'VP',  to:'CH',  via:[],       dim:'A',  key:'vp',    label:'VP → Channels' },
  { id:'ch_cs',   from:'CH',  to:'CS',  via:[],       dim:'F',  key:'vp',    label:'Channels → CS' },
  { id:'vp_cr',   from:'VP',  to:'CR',  via:[],       dim:'D',  key:'vp',    label:'VP → CR' },
  { id:'cs_rs',   from:'CS',  to:'RS',  via:[],       dim:'It', key:'conv',  label:'CS → RS (conversion)' },
  { id:'ka_vp',   from:'KA',  to:'VP',  via:[],       dim:'F',  key:'vp',    label:'KA → VP' },
  { id:'kr_ka',   from:'KR',  to:'KA',  via:[],       dim:'S',  key:'cost',  label:'KR → KA' },
  { id:'kp_ka',   from:'KP',  to:'KA',  via:[],       dim:'S',  key:'cost',  label:'KP → KA' },
  { id:'ka_cost', from:'KA',  to:'CS$', via:[],       dim:'F',  key:'cost',  label:'KA → Cost' },
  { id:'kr_cost', from:'KR',  to:'CS$', via:[],       dim:'F',  key:'cost',  label:'KR → Cost' },
  { id:'rs_sub',  from:'RS',  to:'CS',  via:[],       dim:'A',  key:'cross', label:'CrossSubsidy RS→CS' },
  { id:'net_fx',  from:'CS',  to:'VP',  via:[],       dim:'It', key:'net',   label:'Network Effect CS→VP' },
];

// → See usecases.js
// ── App State ──────────────────────────────────────────────────────────────
let caseIdx    = 0;
let fluxLayout = 'default';   // 'default' | 'experimental'
let phaseIdx   = 0;
let playing    = false;
let speed      = 1;
let morphT     = 1.0;   // 0→1 during morph, 1 = stable
let morphStart = 0;
let morphFrom  = null;  // previous phase params
let morphTo    = null;  // target phase params

// Current interpolated params (updated during morphism)
let params = { vp:.7, conv:.5, cross:.3, net:.4, cost:.5 };

// Slider values (may diverge from case params when user adjusts manually)
let sliderOverride = false;

// Play clock
let playT       = 0;
let lastFrameMs = 0;
const PHASE_DURATION = 4000; // ms per phase before auto-advance

// ── Particle system ────────────────────────────────────────────────────────
class Particle {
  constructor(path, t) {
    this.path = path;
    this.t    = t;    // position along path 0→1
    this.speed = 0.004 + Math.random() * 0.003;
    this.alpha = 0;
    this.alive = true;
    this.size  = 2.5 + Math.random() * 2;
  }
  update(intensity) {
    this.t += this.speed * intensity * 1.2;
    if (this.t < 0.15) this.alpha = this.t / 0.15;
    else if (this.t > 0.85) this.alpha = (1 - this.t) / 0.15;
    else this.alpha = 1;
    if (this.t >= 1) this.alive = false;
  }
}

let particles  = [];
let blockRects = {};  // id → {x,y,w,h,cx,cy}
let spawnTimers = {};
FLUX_PATHS.forEach(fp => { spawnTimers[fp.id] = 0; });

// ── p5 sketch ──────────────────────────────────────────────────────────────
const sketch = (p) => {

  p.setup = () => {
    const cont = document.getElementById('p5-container');
    const cnv  = p.createCanvas(cont.offsetWidth, cont.offsetHeight);
    cnv.parent('p5-container');
    p.textFont('Arial');
    computeBlockRects(p.width, p.height);
    p.frameRate(60);
  };

  p.windowResized = () => {
    const cont = document.getElementById('p5-container');
    p.resizeCanvas(cont.offsetWidth, cont.offsetHeight);
    computeBlockRects(p.width, p.height);
  };

  p.draw = () => {
    p.background(13, 17, 23);  // --bg-deep
    updateMorph();
    updatePlay();
    spawnParticles(p);
    updateParticles();
    drawFluxPaths(p);
    drawBlocks(p);
    drawParticles(p);
    updateLiveMetrics();
  };

  p.mouseMoved = () => {
    showBlockTooltip(p.mouseX, p.mouseY);
  };
  p.mouseOut  = () => hideTooltip();
};

// ── Layout computation ─────────────────────────────────────────────────────
function computeBlockRects(W, H) {
  // Margins
  const mx = 24, my = 20;
  const w  = W - mx * 2;
  const h  = H - my * 2;

  // 5 equal columns, 3 rows (row2 = bottom band = 22% height)
  const colW   = w / 5;
  const row0H  = h * 0.42;
  const row1H  = h * 0.36;
  const row2H  = h * 0.22;
  const rowY   = [my, my + row0H, my + row0H + row1H];
  const rowH   = [row0H, row1H, row2H];

  BLOCKS.forEach(b => {
    const x = mx + b.col * colW;
    const y = rowY[b.row];
    const bw = colW * b.colSpan - 4;
    const bh = (b.rowSpan === 2 ? row0H + row1H : rowH[b.row]) - 4;
    blockRects[b.id] = { x, y, w: bw, h: bh, cx: x + bw/2, cy: y + bh/2 };
  });
}

// ── Flux path geometry (straight lines between block centers with offset) ──
function pathCenter(id) {
  const r = blockRects[id];
  return r ? { x: r.cx, y: r.cy } : { x: 0, y: 0 };
}

function getPathPoints(fp) {
  const A = pathCenter(fp.from);
  const B = pathCenter(fp.to);
  // Slight curve via midpoint offset
  const mx = (A.x + B.x) / 2;
  const my = (A.y + B.y) / 2 + (fp.id === 'rs_sub' ? -30 : 0);
  return { A, M: { x: mx, y: my }, B };
}

function lerpPath(fp, t) {
  // Quadratic bezier: A → M → B
  const { A, M, B } = getPathPoints(fp);
  const x = (1-t)*(1-t)*A.x + 2*(1-t)*t*M.x + t*t*B.x;
  const y = (1-t)*(1-t)*A.y + 2*(1-t)*t*M.y + t*t*B.y;
  return { x, y };
}

// ── Particles ──────────────────────────────────────────────────────────────
function pathIntensity(fp) {
  const k = fp.key;
  let v = params[k] !== undefined ? params[k] : 0.5;

  // Amplify contrast: power curve makes low values much lower, high values stay high
  v = Math.pow(v, 0.7);

  // Transition phase: modulate emerging/fading flux intensities
  if (phaseIdx === PHASE_TRANSITION_IDX && morphT >= 1) {
    const ph = CASES[caseIdx].phases[PHASE_TRANSITION_IDX];
    if (ph) {
      if (ph.fadingFluxes   && ph.fadingFluxes.includes(fp.id))   v *= 0.15;
      if (ph.emergingFluxes && ph.emergingFluxes.includes(fp.id)) v *= 0.8;
    }
  }
  return Math.max(0, v);
}

// ── Transition helpers ─────────────────────────────────────────────────────
function isTransitionPhase() {
  return phaseIdx === PHASE_TRANSITION_IDX;
}

function currentTransitionData() {
  if (!isTransitionPhase()) return null;
  return CASES[caseIdx].phases[PHASE_TRANSITION_IDX] || null;
}

// Slow sine flicker for unstable blocks (0→1)
function flickerAlpha(p, speed) {
  return 0.5 + 0.5 * Math.sin(p.millis() * 0.001 * speed);
}

// ── Draw flux path ghost lines ─────────────────────────────────────────────
function drawFluxPaths(p) {
  const td = currentTransitionData();

  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.02) return;

    const { A, M, B } = getPathPoints(fp);
    const col = p.color(COL[fp.dim] || '#ffffff');

    let baseAlpha = 30 + intensity * 40;
    let strokeW   = 1;
    let dashed    = false;

    if (td && morphT >= 1) {
      if (td.fadingFluxes && td.fadingFluxes.includes(fp.id)) {
        // Fading: flickering dim line
        baseAlpha = 15 + flickerAlpha(p, 1.5) * 20;
        strokeW   = 0.5;
        dashed    = true;
      } else if (td.emergingFluxes && td.emergingFluxes.includes(fp.id)) {
        // Emerging: amber tint, pulsing
        baseAlpha = 20 + flickerAlpha(p, 2.2) * 50;
        strokeW   = 1.5;
        // Override color with amber for emerging paths
        const amberCol = p.color('#E8A020');
        amberCol.setAlpha(baseAlpha);
        p.stroke(amberCol);
        p.strokeWeight(strokeW);
        p.noFill();
        p.beginShape();
        p.vertex(A.x, A.y);
        p.quadraticVertex(M.x, M.y, B.x, B.y);
        p.endShape();
        return; // drawn, skip default
      }
    }

    col.setAlpha(baseAlpha);
    p.stroke(col);
    p.strokeWeight(strokeW);
    p.noFill();

    if (dashed) {
      // Simulate dashed line with short segments
      const steps = 20;
      for (let i = 0; i < steps; i += 2) {
        const t0 = i / steps;
        const t1 = (i + 0.8) / steps;
        const pos0 = lerpBezier(A, M, B, t0);
        const pos1 = lerpBezier(A, M, B, t1);
        p.line(pos0.x, pos0.y, pos1.x, pos1.y);
      }
    } else {
      p.beginShape();
      p.vertex(A.x, A.y);
      p.quadraticVertex(M.x, M.y, B.x, B.y);
      p.endShape();
    }
  });
}

function lerpBezier(A, M, B, t) {
  return {
    x: (1-t)*(1-t)*A.x + 2*(1-t)*t*M.x + t*t*B.x,
    y: (1-t)*(1-t)*A.y + 2*(1-t)*t*M.y + t*t*B.y,
  };
}

// ── Draw blocks ────────────────────────────────────────────────────────────
function drawBlocks(p) {
  const td = currentTransitionData();

  BLOCKS.forEach(b => {
    const r   = blockRects[b.id];
    if (!r) return;
    const col = COL[b.dim] || '#ffffff';
    let pCol  = p.color(col);

    const intensity   = blockActivation(b);
    const isInstable  = td && td.instableBlocks && td.instableBlocks.includes(b.id) && morphT >= 1;

    // Transition: instable blocks flicker in amber
    if (isInstable) {
      const flicker = flickerAlpha(p, 2.5);  // stable sine, no random
      pCol = p.color('#E8A020');

      // Outer glow — amber pulse
      pCol.setAlpha(flicker * 60);
      p.fill(pCol);
      p.noStroke();
      p.rect(r.x - 6, r.y - 6, r.w + 12, r.h + 12, 12);

      // Block body — dim between dark and amber-tinted
      p.fill(p.lerpColor(p.color(28, 33, 48), p.color(40, 35, 20), flicker * 0.6));
      pCol.setAlpha(100 + flicker * 155);
      p.stroke(pCol);
      p.strokeWeight(2);
      p.rect(r.x, r.y, r.w, r.h, 6);

      // "?" instability indicator top-right
      p.noStroke();
      p.fill(232, 160, 32, 180 + flicker * 75);
      p.textSize(10);
      p.textAlign(p.RIGHT, p.TOP);
      p.textStyle(p.BOLD);
      p.text('⟳', r.x + r.w - 5, r.y + 3);

    } else {
      // Normal rendering
      if (intensity > 0.1) {
        pCol.setAlpha(intensity * 40);
        p.fill(pCol);
        p.noStroke();
        p.rect(r.x - 4, r.y - 4, r.w + 8, r.h + 8, 10);
      }
      p.fill(28, 33, 48);
      pCol.setAlpha(180 + intensity * 75);
      p.stroke(pCol);
      p.strokeWeight(1.5);
      p.rect(r.x, r.y, r.w, r.h, 6);
    }

    // ── Layout constants ──────────────────────────────────────────────────
    const GAUGE_PAD   = 3;
    const GAUGE_MAX_W = 8;
    const GAUGE_MIN_W = 3;
    const DIM_SIZE    = 15;          // 1.7× original 9px → 15px
    const DIM_H       = DIM_SIZE + 4; // height reserved for dim label above gauge
    const GAUGE_TOP   = r.y + GAUGE_PAD + DIM_H;   // gauge starts below dim label
    const GAUGE_BOT   = r.y + r.h - GAUGE_PAD;
    const GAUGE_H     = GAUGE_BOT - GAUGE_TOP;      // shorter gauge, leaves room for label

    // ── Gauge A — ASFID activation ────────────────────────────────────────
    {
      const flow    = gaugeFlow(b);
      const absFlow = Math.abs(flow);
      const gW      = GAUGE_MIN_W + absFlow * (GAUGE_MAX_W - GAUGE_MIN_W);
      const gaugeCol = isInstable ? p.color('#E8A020') : p.color(col);
      const trackX   = r.x + GAUGE_PAD;

      // Dim label TOP-LEFT, above the gauge
      const dimCol = isInstable ? p.color('#E8A020') : p.color(col);
      dimCol.setAlpha(210);
      p.fill(dimCol);
      p.noStroke();
      p.textFont('Arial');
      p.textSize(DIM_SIZE);
      p.textStyle(p.BOLD);
      p.textAlign(p.LEFT, p.TOP);
      p.text(b.dim, trackX + 1, r.y + GAUGE_PAD);
      p.textStyle(p.NORMAL);

      // Gauge starts BELOW the dim label
      const gTop = r.y + GAUGE_PAD + DIM_SIZE + 3;
      const gBot = r.y + r.h - GAUGE_PAD;
      const gH   = gBot - gTop;

      // Track
      p.fill(15, 18, 28, 180);
      p.rect(trackX, gTop, gW, gH, 2);
      // Fill (from bottom)
      const fillH = intensity * gH;
      const fillY = gTop + gH - fillH;
      gaugeCol.setAlpha(160 + absFlow * 80);
      p.fill(gaugeCol);
      p.rect(trackX, fillY, gW, fillH, 2);

      // ── Trend indicator at vertical midpoint of gauge ─────────────────────
      // ▲ filling  ▼ emptying  = stable (|flow| < 4%)
      const midY    = gTop + gH / 2;
      const midX    = trackX + gW / 2;
      const STABLE_THRESHOLD = 0.04;

      gaugeCol.setAlpha(230);
      p.fill(gaugeCol);
      p.noStroke();

      if (absFlow < STABLE_THRESHOLD) {
        // ── "=" sign — two small horizontal bars ──
        const bW = gW - 1;  // bar width fills gauge
        const bH = 1.5;
        const bX = trackX + 0.5;
        p.rect(bX, midY - 3, bW, bH, 1);
        p.rect(bX, midY + 1, bW, bH, 1);
      } else if (flow > 0) {
        // ── ▲ triangle pointing UP ──
        const tw = gW - 1;
        const th = Math.min(gH * 0.18, tw * 0.8);
        p.triangle(
          midX,          midY - th,      // apex top
          trackX + 0.5,  midY,           // bottom-left
          trackX + gW - 0.5, midY        // bottom-right
        );
      } else {
        // ── ▼ triangle pointing DOWN ──
        const tw = gW - 1;
        const th = Math.min(gH * 0.18, tw * 0.8);
        p.triangle(
          midX,          midY + th,      // apex bottom
          trackX + 0.5,  midY,           // top-left
          trackX + gW - 0.5, midY        // top-right
        );
      }

      // Flow arrow at fill boundary (kept for additional visual cue)
      if (absFlow > 0.05) {
        const arrowY = flow > 0 ? fillY - 1 : fillY + fillH + 1;
        const dir    = flow > 0 ? -1 : 1;
        gaugeCol.setAlpha(180);
        p.fill(gaugeCol);
        p.triangle(trackX + gW/2, arrowY + dir*4,
                   trackX,        arrowY - dir*2,
                   trackX + gW,   arrowY - dir*2);
      }

      // ── Gauge V (VP/RS only) — stacked BELOW dim label, beside gauge A ───
      const hasGaugeV = (b.id === 'VP' || b.id === 'RS');
      if (hasGaugeV) {
        const vLevel   = getOsterwalderValue(b.id);
        const absVFlow = absFlow * 0.6;
        const gVW      = 5;
        const gVX      = trackX + gW + 2;
        const GOLD     = isInstable ? p.color('#E8A020') : p.color('#F5A623');

        // "V"/"R" label: BELOW the dim label (dim takes DIM_SIZE px, V/R below it)
        GOLD.setAlpha(190);
        p.fill(GOLD);
        p.textFont('Arial');
        p.textSize(9);
        p.textStyle(p.BOLD);
        p.textAlign(p.LEFT, p.TOP);
        p.text(b.id === 'VP' ? 'V' : 'R', gVX + 1, r.y + GAUGE_PAD + DIM_SIZE + 1);
        p.textStyle(p.NORMAL);

        // Gauge V starts same top as Gauge A (below both labels)
        p.fill(15, 18, 28, 160);
        p.rect(gVX, gTop, gVW, gH, 2);
        const vFillH = vLevel * gH;
        GOLD.setAlpha(140 + absVFlow * 80);
        p.fill(GOLD);
        p.rect(gVX, gTop + gH - vFillH, gVW, vFillH, 2);
      }
    }
    // ── End gauges ────────────────────────────────────────────────────────

    // ── Abbreviation — top of block, not centered ─────────────────────────
    const ABBR_SIZE  = b.id === 'CS$' ? 18 : 22;
    const LABEL_SIZE = 11;
    const CONTENT_X  = r.x + 18;   // left margin — closer to left edge
    const CONTENT_W  = r.w - 22;   // usable width

    const TITLE_TOP = r.y + 10;    // abbr starts near top

    const abbrevCol = isInstable ? p.color('#E8A020') : p.color(col);
    abbrevCol.setAlpha(220);
    p.fill(abbrevCol);
    p.textFont('Arial');
    p.textSize(ABBR_SIZE);
    p.textAlign(p.LEFT, p.TOP);
    p.textStyle(p.BOLD);
    p.text(b.abbr, CONTENT_X, TITLE_TOP);

    // Sub-title (Key Partners...) — directly under abbr, tight interligne
    const SUBTITLE_TOP = TITLE_TOP + ABBR_SIZE * 1.1;
    p.fill(190, 200, 215);
    p.textFont('Arial');
    p.textSize(LABEL_SIZE);
    p.textStyle(p.NORMAL);
    p.textAlign(p.LEFT, p.TOP);
    const maxChars = Math.max(8, Math.floor(CONTENT_W / (LABEL_SIZE * 0.6)));
    const lines = wrapText(b.label, maxChars);
    const lineH = LABEL_SIZE * 1.15;   // tight interligne
    lines.forEach((ln, i) => {
      p.text(ln, CONTENT_X, SUBTITLE_TOP + i * lineH);
    });

    // ── Bullets — 1.6× larger (8.5 → 13.5px) ────────────────────────────
    const bullets = getBlockBullets(b.id);
    let bulletEndY = SUBTITLE_TOP + lines.length * lineH;
    if (bullets && bullets.length > 0) {
      const BULLET_SIZE  = Math.round(LABEL_SIZE * 1.04);  // 11 × 1.04 ≈ 11px (+30% vs previous 0.8×)
      const BULLET_LINEH = BULLET_SIZE * 1.45;
      bulletEndY = SUBTITLE_TOP + lines.length * lineH + 8;
      const bulletColor = isInstable ? p.color('#E8A020') : p.color(col);
      const maxBulletW  = CONTENT_W - 10;

      bullets.slice(0, 3).forEach((bull, i) => {
        const y = bulletEndY + i * BULLET_LINEH;
        if (y > r.y + r.h - 6) return;   // clip
        // Dot
        bulletColor.setAlpha(160);
        p.fill(bulletColor);
        p.noStroke();
        p.circle(CONTENT_X + 4, y + BULLET_SIZE * 0.35, 4);
        // Text
        p.fill(185, 195, 210, 210);
        p.textFont('Arial');
        p.textSize(BULLET_SIZE);
        p.textStyle(p.NORMAL);
        p.textAlign(p.LEFT, p.TOP);
        let txt = bull;
        while (txt.length > 3 && p.textWidth(txt) > maxBulletW - 12) {
          txt = txt.slice(0, -2) + '…';
        }
        p.text(txt, CONTENT_X + 12, y);
      });
      bulletEndY += bullets.slice(0, 3).length * BULLET_LINEH;
      p.textAlign(p.CENTER, p.CENTER);
    }

    // ── Osterwalder badges ────────────────────────────────────────────────
    {
      const ost = getOsterwalderAttrs(b.id);
      if (ost) {
        const BADGE_SZ = 9;
        const BADGE_LH = BADGE_SZ + 5;
        let badgeY = bulletEndY + 6;
        p.textFont('Arial');
        p.textSize(BADGE_SZ);
        p.textStyle(p.NORMAL);
        p.textAlign(p.LEFT, p.CENTER);
        const GOLD = p.color('#F5A623');

        const badges = [];
        if (b.id === 'VP' && ost.valueLevel) {
          const vl    = ost.valueLevel;
          const vlIdx = VALUE_LEVEL_IDX[vl] || 0;
          const stars = '★'.repeat(vlIdx + 1) + '☆'.repeat(3 - vlIdx);
          badges.push({ txt: stars + ' ' + (VALUE_LEVEL_LABELS[vl] || vl), col: GOLD });
          if (ost.priceLvl) {
            badges.push({ txt: (PRICE_LEVEL_ICONS[ost.priceLvl] || '') + ' ' + ost.priceLvl,
                          col: p.color('#79c0ff') });
          }
        }
        if (b.id === 'RS' && ost.revenueType) {
          badges.push({ txt: (REVENUE_ICONS[ost.revenueType] || '💰') + ' ' + ost.revenueType,
                        col: p.color('#3dc896') });
        }
        if (b.id === 'CS' && ost.segmentType) {
          badges.push({ txt: (SEGMENT_ICONS[ost.segmentType] || '👥') + ' ' + ost.segmentType,
                        col: p.color('#c882ff') });
        }
        if (b.id === 'CR' && ost.relType) {
          badges.push({ txt: (REL_ICONS[ost.relType] || '↔') + ' ' + ost.relType,
                        col: p.color('#ff6464') });
        }

        badges.forEach(bd => {
          if (badgeY > r.y + r.h - 6) return;
          bd.col.setAlpha(30);
          p.fill(bd.col);
          p.noStroke();
          p.rect(CONTENT_X, badgeY - BADGE_SZ/2 - 1, CONTENT_W - 4, BADGE_SZ + 3, 3);
          bd.col.setAlpha(220);
          p.fill(bd.col);
          let txt = bd.txt;
          while (txt.length > 3 && p.textWidth(txt) > CONTENT_W - 8) txt = txt.slice(0, -1);
          p.text(txt, CONTENT_X + 3, badgeY);
          badgeY += BADGE_LH;
        });
        p.textAlign(p.CENTER, p.CENTER);
      }
    }
    // ── End Osterwalder badges ────────────────────────────────────────────

    // Instability label during Transition
    if (isInstable) {
      const sinceStable = morphT >= 1 ? (performance.now() - (morphStart + MORPH_MS)) : 0;
      if (morphT < 1 || sinceStable < 3000) {
        p.fill(232, 160, 32, 200);
        p.textFont('Arial');
        p.textSize(8);
        p.textAlign(p.CENTER, p.BOTTOM);
        p.text('⟳ en mutation', r.cx, r.y + r.h - 4);
      }
    }
  });

  // Transition phase: banner shown during morphism + 3s after, then gone
  if (isTransitionPhase() && td && td.transitionLabel) {
    // Banner visible during morph (morphT < 1) and for 3s after (bannerT)
    const sinceStable = morphT >= 1 ? (performance.now() - (morphStart + MORPH_MS)) : 0;
    const BANNER_HOLD = 3000; // ms to keep banner after morph ends
    if (morphT < 1 || sinceStable < BANNER_HOLD) {
      const bannerAlpha = morphT < 1
        ? Math.min(255, morphT * 600)
        : Math.max(0, 255 * (1 - sinceStable / BANNER_HOLD));
      const W = p.width;
      p.fill(20, 17, 10, bannerAlpha * 0.85);
      p.noStroke();
      p.rect(W/2 - 230, 6, 460, 24, 4);
      p.fill(232, 160, 32, bannerAlpha);
      p.textFont('Arial');
      p.textSize(11);
      p.textAlign(p.CENTER, p.CENTER);
      p.textStyle(p.BOLD);
      p.text('⟳ ' + td.transitionLabel, W/2, 18);
      p.textStyle(p.NORMAL);
    }
  }
}

function spawnParticles(p) {
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.08) return;  // hard cutoff — no particles on very weak flows
    spawnTimers[fp.id] = (spawnTimers[fp.id] || 0) + 1;
    // Spawn rate inversely proportional to intensity — high intensity = frequent spawns
    // Range: intensity 0.1 → rate 50 frames; intensity 1.0 → rate 3 frames
    const rate = Math.max(3, Math.round(30 / (intensity * intensity)));
    if (spawnTimers[fp.id] >= rate && particles.length < MAX_PARTS) {
      particles.push(new Particle(fp, 0));
      spawnTimers[fp.id] = 0;
    }
  });
}

function updateParticles() {
  particles.forEach(pt => {
    const intensity = pathIntensity(pt.path);
    pt.update(intensity);
  });
  particles = particles.filter(pt => pt.alive);
}

// ── Tangent of quadratic Bézier at t (normalized direction vector) ─────────
function tangentPath(fp, t) {
  const { A, M, B } = getPathPoints(fp);
  // Derivative of quadratic Bézier: dB/dt = 2(1-t)(M-A) + 2t(B-M)
  const dx = 2*(1-t)*(M.x - A.x) + 2*t*(B.x - M.x);
  const dy = 2*(1-t)*(M.y - A.y) + 2*t*(B.y - M.y);
  return Math.atan2(dy, dx);  // angle in radians
}

// ── Tangent for straight line (experimental layout) ───────────────────────
function tangentLine(A, B) {
  return Math.atan2(B.y - A.y, B.x - A.x);
}

function drawParticles(p) {
  particles.forEach(pt => {
    const pos   = lerpPath(pt.path, pt.t);
    const angle = tangentPath(pt.path, pt.t);
    const intensity = pathIntensity(pt.path);

    // Chevron size: base 10px, scales with intensity and particle alpha
    const sz    = (8 + intensity * 6) * pt.alpha;
    const col   = p.color(COL[pt.path.dim] || '#ffffff');

    // Glow halo
    col.setAlpha(pt.alpha * 45);
    p.noStroke();
    p.fill(col);
    p.circle(pos.x, pos.y, sz * 2.2);

    // Chevron — drawn as two lines forming a "›" shape, rotated to tangent
    col.setAlpha(pt.alpha * 220);
    p.stroke(col);
    p.strokeWeight(1.8);
    p.noFill();

    p.push();
    p.translate(pos.x, pos.y);
    p.rotate(angle);
    // Chevron: two strokes meeting at tip (right), opening to left
    const h = sz * 0.45;  // half-height of chevron opening
    const w = sz * 0.55;  // depth of chevron
    p.line(-w, -h,  0, 0);  // top arm → tip
    p.line(-w,  h,  0, 0);  // bottom arm → tip
    p.pop();

    p.noStroke();
  });
}

// ── Draw flux paths — dispatches to layout renderer ───────────────────────
function drawFluxPaths(p) {
  if (fluxLayout === 'experimental') {
    drawFluxPathsExperimental(p);
  } else {
    drawFluxPathsDefault(p);
  }
}

// ── Layout DEFAULT — Bézier ghost lines ───────────────────────────────────
function drawFluxPathsDefault(p) {
  const td = currentTransitionData();
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.02) return;
    const { A, M, B } = getPathPoints(fp);
    const col = p.color(COL[fp.dim] || '#ffffff');
    let baseAlpha = 30 + intensity * 40;
    let strokeW   = 1;
    let dashed    = false;
    if (td && morphT >= 1) {
      if (td.fadingFluxes && td.fadingFluxes.includes(fp.id)) {
        baseAlpha = 15 + flickerAlpha(p, 1.5) * 20; strokeW = 0.5; dashed = true;
      } else if (td.emergingFluxes && td.emergingFluxes.includes(fp.id)) {
        const amberCol = p.color('#E8A020');
        amberCol.setAlpha(20 + flickerAlpha(p, 2.2) * 50);
        p.stroke(amberCol); p.strokeWeight(1.5); p.noFill();
        p.beginShape(); p.vertex(A.x, A.y);
        p.quadraticVertex(M.x, M.y, B.x, B.y); p.endShape();
        return;
      }
    }
    col.setAlpha(baseAlpha);
    p.stroke(col); p.strokeWeight(strokeW); p.noFill();
    if (dashed) {
      for (let i = 0; i < 20; i += 2) {
        const p0 = lerpBezier(A, M, B, i/20);
        const p1 = lerpBezier(A, M, B, (i+0.8)/20);
        p.line(p0.x, p0.y, p1.x, p1.y);
      }
    } else {
      p.beginShape(); p.vertex(A.x, A.y);
      p.quadraticVertex(M.x, M.y, B.x, B.y); p.endShape();
    }
  });
}

// ── Layout EXPERIMENTAL — connectors on block edges + animated pipe ────────
// Connector anchors: each FLUX_PATH defines fromAnchor/toAnchor on block edges
const FLUX_ANCHORS = {
  vp_ch:   { from:'VP',  fromEdge:'right',  to:'CH',  toEdge:'left'   },
  ch_cs:   { from:'CH',  fromEdge:'right',  to:'CS',  toEdge:'left'   },
  vp_cr:   { from:'VP',  fromEdge:'right',  to:'CR',  toEdge:'left'   },
  cs_rs:   { from:'CS',  fromEdge:'bottom', to:'RS',  toEdge:'right'  },
  ka_vp:   { from:'KA',  fromEdge:'right',  to:'VP',  toEdge:'left'   },
  kr_ka:   { from:'KR',  fromEdge:'top',    to:'KA',  toEdge:'bottom' },
  kp_ka:   { from:'KP',  fromEdge:'right',  to:'KA',  toEdge:'left'   },
  ka_cost: { from:'KA',  fromEdge:'bottom', to:'CS$', toEdge:'top'    },
  kr_cost: { from:'KR',  fromEdge:'bottom', to:'CS$', toEdge:'top'    },
  rs_sub:  { from:'RS',  fromEdge:'top',    to:'CS',  toEdge:'bottom' },
  net_fx:  { from:'CS',  fromEdge:'left',   to:'VP',  toEdge:'right'  },
};

function edgePoint(blockId, edge) {
  const r = blockRects[blockId];
  if (!r) return { x:0, y:0 };
  switch (edge) {
    case 'left':   return { x: r.x,           y: r.cy };
    case 'right':  return { x: r.x + r.w,     y: r.cy };
    case 'top':    return { x: r.cx,           y: r.y  };
    case 'bottom': return { x: r.cx,           y: r.y + r.h };
    default:       return { x: r.cx,           y: r.cy };
  }
}

function drawFluxPathsExperimental(p) {
  const now = p.millis();
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.05) return;
    const anchor = FLUX_ANCHORS[fp.id];
    if (!anchor) return;

    const A = edgePoint(anchor.from, anchor.fromEdge);
    const B = edgePoint(anchor.to,   anchor.toEdge);
    if (!A || !B) return;

    const col     = p.color(COL[fp.dim] || '#ffffff');
    const pipeW   = 3 + intensity * 8;   // pipe width 3→11px
    const flowSpd = intensity * 0.4;     // animation speed

    // ── Pipe track (background) ───────────────────────────────────────────
    col.setAlpha(30);
    p.stroke(col); p.strokeWeight(pipeW); p.strokeCap(p.ROUND);
    p.noFill();
    p.line(A.x, A.y, B.x, B.y);

    // ── Animated chevron sliding along pipe ──────────────────────────────
    const t    = ((now * flowSpd * 0.001) % 1.0);
    const SEG  = 0.35;
    const chevX = A.x + (B.x - A.x) * (t + SEG * 0.5);
    const chevY = A.y + (B.y - A.y) * (t + SEG * 0.5);
    const angle = tangentLine(A, B);
    const sz    = 5 + intensity * 5;

    col.setAlpha(180 + intensity * 70);
    p.stroke(col);
    p.strokeWeight(2);
    p.noFill();
    p.push();
    p.translate(chevX, chevY);
    p.rotate(angle);
    p.line(-sz * 0.5, -sz * 0.45,  0, 0);
    p.line(-sz * 0.5,  sz * 0.45,  0, 0);
    p.pop();
    p.noStroke();

    // ── Connector circles on block edges ──────────────────────────────────
    col.setAlpha(200); p.fill(col);
    p.circle(A.x, A.y, 9);
    p.fill(28, 33, 48);
    p.circle(A.x, A.y, 5);
    col.setAlpha(200); p.fill(col);
    p.circle(B.x, B.y, 9);
    col.setAlpha(160 + intensity * 60); p.fill(col);
    p.circle(B.x, B.y, 5);
  });
  p.strokeCap(p.SQUARE);  // restore default
}

// ── Gauge flow (débit) — signed derivative of block level ─────────────────
// Computed from morphism progress: how fast is this block's param changing?
// Returns value in [-1, +1] : positive = filling, negative = emptying
let _prevParams = null;
let _prevParamsFrame = 0;

function gaugeFlow(b) {
  // During morphism: compute derivative from morphFrom → morphTo
  if (morphT >= 1 || !morphFrom || !morphTo) {
    // Stable phase — no flow (or tiny noise for "alive" feeling)
    return 0;
  }

  // Map block to its primary param key
  const keyMap = {
    VP: 'vp',  CS: 'conv', CH: 'vp',  CR: 'vp',
    RS: 'conv', KA: 'cost', KR: 'cost', KP: 'cost', 'CS$': 'cost',
  };
  const k = keyMap[b.id];
  if (!k) return 0;

  const from = Math.pow(morphFrom[k] || 0, 0.6);
  const to   = Math.pow(morphTo[k]   || 0, 0.6);
  const delta = to - from;  // signed: + = filling, - = emptying

  // Scale by morphism speed (faster morph = higher flow)
  const speed = Math.min(1, Math.abs(delta) * 2.5);
  return Math.sign(delta) * speed;
}

// ── Get Osterwalder VALUE LEVEL as 0→1 (for Gauge V) ─────────────────────
function getOsterwalderValue(blockId) {
  const ost = getOsterwalderAttrs(blockId);
  if (!ost) return 0.5;
  if (blockId === 'VP' && ost.valueLevel) {
    return (VALUE_LEVEL_IDX[ost.valueLevel] || 0) / 3;
  }
  if (blockId === 'RS' && ost.revenueType) {
    // Revenue complexity as value: asset-sale=0.25, usage=0.5, subscription=0.6,
    // advertising=0.7, brokerage=0.75, licensing=0.8, cross-subsidy=1.0
    const map = { 'asset-sale':0.25,'usage':0.5,'subscription':0.6,
                  'advertising':0.7,'brokerage':0.75,'licensing':0.8,'cross-subsidy':1.0 };
    return map[ost.revenueType] || 0.5;
  }
  return 0.5;
}

// ── Get Osterwalder attributes for a block in current case+phase ──────────
function getOsterwalderAttrs(blockId) {
  const cs  = CASES[caseIdx];
  const ph  = cs ? cs.phases[phaseIdx] : null;
  const bc  = ph && ph.blockContent ? ph.blockContent[blockId] : null;
  if (bc && bc.osterwalder) return bc.osterwalder;
  const gen = GENERIC_BLOCKS[phaseIdx];
  if (gen && gen[blockId] && gen[blockId].osterwalder) return gen[blockId].osterwalder;
  return null;
}

// ── Get bullets for a block in current case+phase ─────────────────────────
// ── Smart bullet generator ─────────────────────────────────────────────────
// Priority: 1) case blockContent  2) generated from phase data  3) generic fallback
function getBlockBullets(blockId) {
  const cs = CASES[caseIdx];
  const ph = cs ? cs.phases[phaseIdx] : null;

  // 1. Case-specific blockContent (highest priority)
  if (ph && ph.blockContent && ph.blockContent[blockId] &&
      Array.isArray(ph.blockContent[blockId].bullets) &&
      ph.blockContent[blockId].bullets.length > 0) {
    return ph.blockContent[blockId].bullets;
  }

  // 2. Generate contextual bullets from phase narrative/driver + case pattern
  if (ph && cs) {
    const generated = generateBullets(blockId, cs, ph, phaseIdx);
    if (generated && generated.length > 0) return generated;
  }

  // 3. Generic phase fallback
  const generic = GENERIC_BLOCKS[phaseIdx];
  if (generic && generic[blockId] && generic[blockId].bullets) {
    return generic[blockId].bullets;
  }
  return [];
}

// ── Generate bullets from case+phase data ─────────────────────────────────
function generateBullets(blockId, cs, ph, phIdx) {
  const phName = PHASE_NAMES[phIdx] || '';
  const isT    = phIdx === PHASE_TRANSITION_IDX;
  const driver = ph.driver || '';
  const narr   = ph.narrative || '';
  const short  = cs.short || cs.name;

  // Extract key phrases from driver (split on '. ' and take first 3)
  const driverParts = driver.split(/[.!]/).map(s => s.trim()).filter(s => s.length > 3 && s.length < 30);

  // Bullet sets per block × phase pattern
  // Key: we derive content from the narrative/driver text, not hardcoded per company
  switch (blockId) {

    case 'VP': {
      // Extract VP description from narrative (after '—')
      const vpHint  = narr.includes('—') ? narr.split('—').slice(1).join('—').trim() : narr;
      const vpShort = vpHint.replace(/['"«»]/g, '').substring(0, 26);
      const phLabels= ['Hypothesis only','PMF achieved ✓','Category leader','VP eroded ↓','VP in flux ⟳'];
      // Key metric from driver (price, market share, revenue)
      const metrics = driver.match(/[\$€£][\d.]+[BM]?[^\s,.]*/gi) ||
                      driver.match(/\d+%[^\s,.]*/gi) ||
                      driver.match(/\d+[MBK]\+?[^\s,.]*/gi) || [];
      const metric = metrics[0] ? metrics[0].substring(0, 22) : (driverParts[0] || '');
      return [
        phLabels[phIdx] || phName,
        vpShort || short,
        metric || (isT ? '≥3 blocks changing ⟳' : driverParts[1] || phName),
      ].filter(s => s && s.trim().length > 1).slice(0, 3);
    }

    case 'RS': {
      // Look for RS clues in driver
      const rsClues = driver.match(/\$[\d.]+[BM]?\/?(mo|yr|km|hr|unit|user)?|€\/km|pay-per|subscription|ad revenue|freemium|commission|brokerage|cross-subsidy/gi) || [];
      const rsHint  = rsClues.slice(0, 2).join(' · ') || (driverParts[1] || '');
      const rsPhase = ['Near zero / grants','MRR growing','Diversified RS','RS declining ↓','RS in transition ⟳'];
      return [
        rsPhase[phIdx] || phName,
        rsHint.substring(0, 26) || driver.substring(0, 22),
        driverParts[0] || '',
      ].filter(Boolean).slice(0, 3);
    }

    case 'CS': {
      // Extract segment size from driver + narrative
      const csClues = driver.match(/\d+[MBK]?\+?\s*(?:users?|subscribers?|clients?|cards?|hosts?|guests?|merchants?|countries|drivers?|riders?|stores?|languages?)/gi) || [];
      const csHint  = csClues[0] ? csClues[0].trim().substring(0, 26) : '';
      // Extract second figure if present
      const csHint2 = csClues[1] ? csClues[1].trim().substring(0, 26) : '';
      const csPhase = ['Niche early adopters','Early majority','Mass market','CS shrinking ↓','CS segment shift ⟳'];
      const bullets = [
        csPhase[phIdx] + (csHint ? ': ' + csHint : '') ,
        csHint2 || (driverParts[1] || driverParts[0] || short),
        short + ' — ' + phName,
      ].filter(s => s && s.trim().length > 2);
      return bullets.slice(0, 3);
    }

    case 'KA': {
      const kaPhase = [
        ['Build + discover','MVP iteration','Fundraising'],
        ['Scale operations','Process build','Team growth'],
        ['Optimize + retain','Upsell / expand','International'],
        ['Cost-cutting','Restructuring','Defend market'],
        ['BM redesign ⟳','New capability','Org restructuring'],
      ];
      // Enrich with driver keywords
      const kaKeys = driver.match(/[A-Z][a-z]+(?:ing|ment|ion|tion)/g) || [];
      const base = kaPhase[phIdx] || kaPhase[0];
      if (kaKeys[0]) base[0] = kaKeys[0].substring(0, 22);
      return base.slice(0, 3);
    }

    case 'KR': {
      const krPhase = [
        ['Founder + seed','Early prototype','Tech platform'],
        ['Sales playbook','Customer data','Brand growing'],
        ['Brand (moat)','Data advantage','Distribution'],
        ['Eroding brand','Aging tech stack','Talent risk'],
        ['New tech/IP ⟳','Brand repositioning','Transition assets'],
      ];
      return (krPhase[phIdx] || krPhase[0]).slice(0, 3);
    }

    case 'KP': {
      // Try to extract partner hints from driver
      const kpHints = driver.match(/[A-Z][a-z]+(?:s)?\s+(?:KP|partner|supplier|investor|network)/gi) || [];
      const kpPhase = [
        ['Early suppliers','Angel investors','Advisors / incubator'],
        ['Channel partners','Key suppliers','Strategic investors'],
        ['Ecosystem partners','OEM / white-label','Strategic alliances'],
        ['Partners leaving ↓','Supplier leverage ↑','M&A targets'],
        ['New strategic KP ⟳','Pivot investors','Capability partners'],
      ];
      const base = kpPhase[phIdx] || kpPhase[0];
      if (kpHints[0]) base[0] = kpHints[0].substring(0, 22);
      return base.slice(0, 3);
    }

    case 'CR': {
      const crPhase = [
        ['Hands-on','Founders respond','White-glove'],
        ['Self-service','CS team','Community building'],
        ['Automated low-touch','Account mgmt','Self-serve community'],
        ['Automated only','Low investment','Churn > acquisition'],
        ['CR in transition ⟳','Old CS retained','New segment acquired'],
      ];
      return (crPhase[phIdx] || crPhase[0]).slice(0, 3);
    }

    case 'CH': {
      const chPhase = [
        ['Direct outreach','Founder network','ProductHunt / press'],
        ['SEO + paid','Partner channels','Word of mouth'],
        ['Omni-channel','Partners 40%+','International CH'],
        ['Existing only','No new investment','Channel decay'],
        ['Old CH phased out ⟳','New CH emerging','Dual-mode CH'],
      ];
      return (chPhase[phIdx] || chPhase[0]).slice(0, 3);
    }

    case 'CS$': {
      // Try to extract cost figures from driver
      const costFigs = driver.match(/\$[\d.]+[BM]?\/?(yr|mo)?/gi) || [];
      const costPhase = [
        ['High burn rate','Team salaries','Infrastructure'],
        ['CAC dominant','Unit economics ↑','Burn ↑ (growth invest)'],
        ['Optimized costs','Fixed costs spread','EBITDA positive'],
        ['Rigid fixed costs','RS < C$ gap ↑','Margin compression'],
        ['Transition costs ↑ ⟳','Dual-mode ops','Restructuring charges'],
      ];
      const base = costPhase[phIdx] || costPhase[0];
      if (costFigs[0]) base[1] = costFigs[0].substring(0, 22);
      return base.slice(0, 3);
    }

    default:
      return [];
  }
}

function blockActivation(b) {
  // Map block to its primary param, amplified for visual contrast
  const raw = {
    VP:   params.vp,
    CS:   params.conv,
    CH:   params.vp * 0.9,
    CR:   params.vp * 0.85,
    RS:   params.conv,
    KA:   params.cost * 0.9,
    KR:   params.cost * 0.85,
    KP:   params.cost * 0.75,
    'CS$': params.cost,
  };
  // Amplify contrast: remap [0, 1] → exaggerated visual range
  const v = raw[b.id] !== undefined ? raw[b.id] : 0.4;
  // Apply a power curve to exaggerate differences (low=darker, high=brighter)
  return Math.min(1, Math.pow(v, 0.6));
}

function wrapText(text, maxChars) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  words.forEach(w => {
    if ((cur + ' ' + w).trim().length > maxChars && cur) {
      lines.push(cur.trim());
      cur = w;
    } else {
      cur = (cur + ' ' + w).trim();
    }
  });
  if (cur) lines.push(cur.trim());
  return lines;
}

// ── Morphism ───────────────────────────────────────────────────────────────
function startMorph(fromParams, toParams) {
  morphFrom  = { ...fromParams };
  morphTo    = { ...toParams };
  morphT     = 0;
  morphStart = performance.now();
}

function updateMorph() {
  if (morphT >= 1) return;
  const elapsed = performance.now() - morphStart;
  morphT = Math.min(1, elapsed / MORPH_MS);
  const ease = easeInOut(morphT);

  ['vp','conv','cross','net','cost'].forEach(k => {
    params[k] = morphFrom[k] + (morphTo[k] - morphFrom[k]) * ease;
  });

  // If user hasn't overridden sliders, animate them too
  if (!sliderOverride) {
    document.getElementById('sl-vp').value    = params.vp;
    document.getElementById('sl-conv').value  = params.conv;
    document.getElementById('sl-cross').value = params.cross;
    document.getElementById('sl-net').value   = params.net;
    document.getElementById('sl-cost').value  = params.cost;
  }

  // Update morph bar
  document.getElementById('morph-bar-fill').style.width = (morphT * 100) + '%';
  document.getElementById('morph-label').textContent =
    morphT < 1 ? 'Morphing…' : '—';
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

// ── Play / phase advance ───────────────────────────────────────────────────
function updatePlay() {
  if (!playing) return;
  const now  = performance.now();
  const dt   = now - lastFrameMs;
  lastFrameMs = now;
  if (dt > 200) return;  // tab was hidden

  playT += dt * speed;
  const dur = PHASE_DURATION;
  const progress = playT / (dur * PHASE_NAMES.length);
  document.getElementById('progress-fill').style.width = (progress * 100) + '%';

  const newPhase = Math.min(PHASE_NAMES.length - 1, Math.floor(playT / dur));
  if (newPhase !== phaseIdx) {
    jumpPhase(newPhase);
  }

  if (playT >= dur * PHASE_NAMES.length) {
    playing = false;
    document.getElementById('btn-play').textContent = '▶ Play';
    document.getElementById('btn-play').classList.remove('active');
    document.getElementById('status-dot').className = 'status-dot paused';
    document.getElementById('status-label').textContent = 'Done';
  }
}

// ── Phase jump ─────────────────────────────────────────────────────────────
function jumpPhase(idx) {
  const prevPhase = phaseIdx;
  phaseIdx = Math.max(0, Math.min(PHASE_NAMES.length - 1, idx));

  const cs   = CASES[caseIdx];
  const prev = cs.phases[prevPhase];
  const next = cs.phases[phaseIdx];

  // Extract only numeric params for morphism
  const pick = ph => ({ vp: ph.vp, conv: ph.conv, cross: ph.cross, net: ph.net, cost: ph.cost });
  startMorph(pick(prev), pick(next));

  // Clear particles on phase change for clean visual transition
  particles = [];

  // Update narrative
  document.getElementById('phase-narrative-text').textContent = next.narrative;
  document.getElementById('phase-driver-text').textContent    = next.driver;
  document.getElementById('ls-phase').textContent = PHASE_NAMES[phaseIdx];

  // Show transition label in compbar if Transition phase
  const patEl = document.getElementById('case-pattern');
  if (phaseIdx === PHASE_TRANSITION_IDX && next.transitionLabel) {
    if (patEl) patEl.textContent = '⟳ ' + next.transitionLabel;
  } else {
    if (patEl) patEl.textContent = cs.pattern || '';
  }

  // Phase buttons
  document.querySelectorAll('.phase-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === phaseIdx);
  });

  sliderOverride = false;
}

// ── Case selection ─────────────────────────────────────────────────────────
function selectCase(idx) {
  caseIdx   = idx;
  phaseIdx  = 0;
  playT     = 0;
  sliderOverride = false;

  const cs = CASES[idx];
  const ph = cs.phases[0];

  // Only copy numeric params — do NOT pollute with narrative/driver strings
  params = { vp: ph.vp, conv: ph.conv, cross: ph.cross, net: ph.net, cost: ph.cost };
  morphT = 1;  // no morph on case switch

  // Clear all particles so new case starts fresh
  particles = [];
  Object.keys(spawnTimers).forEach(k => { spawnTimers[k] = 0; });

  // Sync sliders
  document.getElementById('sl-vp').value    = params.vp;
  document.getElementById('sl-conv').value  = params.conv;
  document.getElementById('sl-cross').value = params.cross;
  document.getElementById('sl-net').value   = params.net;
  document.getElementById('sl-cost').value  = params.cost;

  document.getElementById('phase-narrative-text').textContent = ph.narrative;
  document.getElementById('phase-driver-text').textContent    = ph.driver;
  document.getElementById('ls-case').textContent  = cs.name;
  document.getElementById('ls-phase').textContent = PHASE_NAMES[0];

  // Show pattern in compbar
  const patEl = document.getElementById('case-pattern');
  if (patEl) patEl.textContent = cs.pattern || '';

  document.querySelectorAll('.phase-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === 0);
  });

  document.getElementById('progress-fill').style.width = '0%';
  document.getElementById('morph-bar-fill').style.width = '0%';
  document.getElementById('morph-label').textContent = '—';
}

// ── Live metrics ───────────────────────────────────────────────────────────
function updateLiveMetrics() {
  const nPart = particles.length;
  const ratio = params.conv > 0 ? (params.conv / Math.max(0.01, params.cost)).toFixed(2) : '—';
  document.getElementById('ls-particles').textContent = nPart;
  document.getElementById('ls-ratio').textContent = ratio + 'x';
}

// ── Tooltip ────────────────────────────────────────────────────────────────
function showBlockTooltip(mx, my) {
  const tt = document.getElementById('block-tooltip');
  let found = null;
  BLOCKS.forEach(b => {
    const r = blockRects[b.id];
    if (!r) return;
    if (mx >= r.x && mx <= r.x + r.w && my >= r.y && my <= r.y + r.h) found = b;
  });
  if (!found) { hideTooltip(); return; }

  const r    = blockRects[found.id];
  const act  = blockActivation(found).toFixed(2);
  const id   = found.id;

  // Try to get case-specific block content for current phase
  const cs   = CASES[caseIdx];
  const ph   = cs ? cs.phases[phaseIdx] : null;
  const bcObj = ph && ph.blockContent ? ph.blockContent[id] : null;
  const bcGeneric = GENERIC_BLOCKS[phaseIdx] ? GENERIC_BLOCKS[phaseIdx][id] : null;
  const bc   = bcObj || bcGeneric;

  // Phase label and color
  const phName  = PHASE_NAMES[phaseIdx] || '';
  const phColor = PH_COLORS[phaseIdx]   || '#8b949e';

  // Generic TSCG framing (always shown)
  const generic = BLOCK_DESC[id] || '';

  // Build tooltip HTML
  let html = `
    <div class="tt-title">${found.label} <span style="color:var(--sphinx)">(${found.abbr})</span></div>
    <div class="tt-dim">
      ASFID: <strong>${found.dim}</strong> &nbsp;·&nbsp;
      Activation: <strong>${act}</strong> &nbsp;·&nbsp;
      <span style="color:${phColor};font-weight:700">${phName}</span>
    </div>`;

  if (bc) {
    // Case-specific content: use desc for tooltip, bullets as preview
    const desc  = bc.desc || '';
    const descLines = desc.split('\\n').map(l => l.trim()).filter(Boolean);
    html += `<div class="tt-case-label">${cs ? cs.name : ''} — ${PHASE_NAMES[phaseIdx]}</div>`;
    html += `<div class="tt-block-content">`;
    descLines.forEach(l => {
      const formatted = l.replace(/^(GUESTS|HOSTS|B2B|B2C):/,
        '<span class="tt-segment">$1:</span>');
      html += `<div class="tt-bc-line">${formatted}</div>`;
    });
    html += `</div>`;
    html += `<div class="tt-sep"></div>`;
  }

  // Always append generic TSCG framing
  html += `<div class="tt-body">${generic}</div>`;

  tt.innerHTML = html;
  tt.style.display = 'block';

  // Position: to the RIGHT of the block title, at title height
  const TITLE_TOP_PX = r.y + 10;   // matches TITLE_TOP in drawBlocks
  const CONTENT_X_PX = r.x + 18;   // matches CONTENT_X in drawBlocks
  const ABBR_W       = found.abbr.length * 14 + found.label.length * 7 + 20;
  const W = document.getElementById('canvas-area').clientWidth;
  const TT_W = 264;

  let tx = CONTENT_X_PX + ABBR_W;  // right of title
  let ty = TITLE_TOP_PX;

  // If not enough room on the right, flip to left
  if (tx + TT_W > W - 4) tx = r.x - TT_W - 4;
  // Clamp vertically
  tx = Math.max(4, tx);
  ty = Math.max(4, Math.min(ty, window.innerHeight - 200));

  tt.style.left = tx + 'px';
  tt.style.top  = ty + 'px';
}

function hideTooltip() {
  document.getElementById('block-tooltip').style.display = 'none';
}

// ── Public controls (called from HTML) ────────────────────────────────────
window.setFluxLayout = function(layout) {
  fluxLayout = layout;
  particles  = [];  // clear particles when switching
  document.querySelectorAll('.layout-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.layout === layout);
  });
};

window.togglePlay = function() {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  const dot = document.getElementById('status-dot');
  const lbl = document.getElementById('status-label');
  if (playing) {
    if (playT >= PHASE_DURATION * PHASE_NAMES.length) {
      playT = 0; phaseIdx = 0;
      jumpPhase(0);
    }
    lastFrameMs = performance.now();
    btn.textContent = '⏸ Pause';
    btn.classList.add('active');
    dot.className = 'status-dot running';
    lbl.textContent = 'Playing';
  } else {
    btn.textContent = '▶ Play';
    btn.classList.remove('active');
    dot.className = 'status-dot paused';
    lbl.textContent = 'Paused';
  }
};

window.resetSim = function() {
  playing = false;
  playT   = 0; phaseIdx = 0;
  document.getElementById('btn-play').textContent = '▶ Play';
  document.getElementById('btn-play').classList.remove('active');
  document.getElementById('status-dot').className = 'status-dot';
  document.getElementById('status-label').textContent = 'Stopped';
  selectCase(caseIdx);
  particles = [];
};

window.setSpeed = function(s) {
  speed = s;
  ['btn-spd1','btn-spd2','btn-spd4'].forEach(id => {
    document.getElementById(id).classList.remove('spd-active');
  });
  document.getElementById('btn-spd' + s).classList.add('spd-active');
};

window.seekProgress = function(e) {
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  playT = ratio * PHASE_DURATION * PHASE_NAMES.length;
  const newPhase = Math.min(PHASE_NAMES.length - 1, Math.floor(playT / PHASE_DURATION));
  jumpPhase(newPhase);
  document.getElementById('progress-fill').style.width = (ratio * 100) + '%';
};

window.activateTab = function(idx) {
  document.querySelectorAll('.tab-panel').forEach((p, i) => {
    p.classList.toggle('active', i === idx);
  });
  document.querySelectorAll('.tab-btn').forEach((b, i) => {
    b.classList.toggle('active', i === idx);
  });
};

// ── Slider event listeners ─────────────────────────────────────────────────
function bindSliders() {
  const map = {
    'sl-vp':   'vp',   'sl-conv': 'conv', 'sl-cross': 'cross',
    'sl-net':  'net',  'sl-cost': 'cost'
  };
  Object.entries(map).forEach(([id, key]) => {
    const el = document.getElementById(id);
    el.addEventListener('input', () => {
      params[key] = parseFloat(el.value);
      sliderOverride = true;
      morphT = 1; // cancel morphism
    });
  });
}

// ── Build compbar UI ───────────────────────────────────────────────────────
function buildUI() {
  // Case dropdown
  const sel = document.getElementById('case-select');
  CASES.forEach((c, i) => {
    const opt = document.createElement('option');
    opt.value = i; opt.textContent = c.name;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => selectCase(parseInt(sel.value)));

  // Phase buttons
  const pb = document.getElementById('phase-btns');
  PHASE_NAMES.forEach((nm, i) => {
    const btn = document.createElement('button');
    btn.className = 'phase-btn' + (i === 0 ? ' active' : '');
    btn.textContent = (i + 1) + ' ' + nm;
    btn.style.background   = hexAlpha(PH_COLORS[i], 0.12);
    btn.style.borderColor  = hexAlpha(PH_COLORS[i], 0.25);
    btn.style.color        = PH_COLORS[i];
    btn.onclick = () => { jumpPhase(i); playT = i * PHASE_DURATION; };
    pb.appendChild(btn);
  });
}

function hexAlpha(hex, a) {
  const r = parseInt(hex.slice(1,3), 16);
  const g = parseInt(hex.slice(3,5), 16);
  const b = parseInt(hex.slice(5,7), 16);
  return `rgba(${r},${g},${b},${a})`;
}

// ── Splitter drag ──────────────────────────────────────────────────────────
function initSplitter() {
  const splitter = document.getElementById('splitter');
  const app      = document.getElementById('app');
  let dragging   = false;
  let startX, startW;

  splitter.addEventListener('mousedown', e => {
    dragging = true;
    startX   = e.clientX;
    startW   = parseInt(getComputedStyle(document.documentElement)
                 .getPropertyValue('--sidebar-w'));
    splitter.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  });
  window.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta = startX - e.clientX;
    const newW  = Math.max(180, Math.min(500, startW + delta));
    document.documentElement.style.setProperty('--sidebar-w', newW + 'px');
  });
  window.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    splitter.classList.remove('dragging');
    document.body.style.cursor = '';
  });
}

// ── Init ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  buildUI();
  bindSliders();
  initSplitter();
  selectCase(0);
  new p5(sketch, document.getElementById('p5-container'));
  document.getElementById('btn-spd1').classList.add('spd-active');
});
