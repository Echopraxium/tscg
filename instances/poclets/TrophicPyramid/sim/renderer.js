/**
 * TSCG Simulation — Trophic Pyramid 3D Renderer (BabylonJS)
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 3.0.0
 *
 * Changes v3:
 *  - HUD 2D labels (CSS overlay, 3D→2D projection)
 *  - Energy/matter flow particles (upward stream + heat sparks)
 *  - Environmental parameters: Light, Water, O2, CO2, Temperature
 *  - Environmental sliders drive pyramid scale and particle intensity
 *  - Tab order: Description | Concepts | Synergy | Scores
 */

'use strict';

// ── Simulation state ──────────────────────────────────────────────
const SIM = {
  running:      true,
  speed:        1.0,
  apexRemoved:  false,
  cascadeTimer: 0,
  selectedRank: null,
  time:         0
};

// Environmental parameters [0..1]
const ENV = {
  light:  0.75,   // solar irradiance (photosynthesis driver)
  water:  0.70,   // freshwater availability
  o2:     0.21,   // atmospheric O2 fraction (reference: 0.21)
  co2:    0.42,   // normalized CO2 (0=280ppm pre-industrial, 1=1000ppm critical)
  temp:   0.38    // normalized surface temp anomaly (0=-2°C, 1=+6°C vs pre-industrial)
};

// Derived biomass multipliers from ENV
function envMultiplier(rank) {
  // Producers most sensitive to light + water + CO2
  if (rank === 1) return Math.pow(ENV.light * ENV.water * (1 - ENV.co2 * 0.4), 0.4);
  // Higher levels follow producer with lag
  const base = envMultiplier(1);
  return Math.pow(base, 1 + (rank - 1) * 0.15);
}

const POP = { 0:1.0, 1:1.0, 2:1.0, 3:1.0, 4:1.0 };
const POP_TARGET = { 0:1.0, 1:1.0, 2:1.0, 3:1.0, 4:1.0 };

// ── BabylonJS globals ─────────────────────────────────────────────
let engine, scene, camera, glowLayer;
let levelMeshes    = {};
let levelMaterials = {};
let energyParticles = {};   // upward flow per boundary
let heatParticles   = {};   // dissipation sparks per boundary
let hudDiv;                 // DOM overlay for 2D labels

// Level geometry (Y-up, square frustums via tessellation=4)
const GEO = {
  1: { dBot:5.2, dTop:4.0, h:1.4, y:0.7  },
  2: { dBot:4.0, dTop:2.9, h:1.4, y:2.4  },
  3: { dBot:2.9, dTop:1.8, h:1.4, y:4.1  },
  4: { dBot:1.8, dTop:0.5, h:1.4, y:5.8  }
};
const DECOMP = { x:4.0, z:0, d:0.7, h:7.0, y:3.5 };

const COLORS = {
  0: '#6e7681', 1: '#56d364', 2: '#79c0ff', 3: '#d2a8ff', 4: '#f78166'
};

// Level metadata for HUD labels
const LEVEL_INFO = {
  0: { short:'Decomposers',       energy:'40–60% flux',   emoji:'🍄' },
  1: { short:'Producers',         energy:'10 000 kJ/m²',  emoji:'🌿' },
  2: { short:'Herbivores',        energy:'1 000 kJ/m²',   emoji:'🐛' },
  3: { short:'Carnivores',        energy:'100 kJ/m²',     emoji:'🦊' },
  4: { short:'Apex Predators',    energy:'10 kJ/m²',      emoji:'🦅' }
};

function hexC3(h) {
  return new BABYLON.Color3(
    parseInt(h.slice(1,3),16)/255,
    parseInt(h.slice(3,5),16)/255,
    parseInt(h.slice(5,7),16)/255);
}
function hexC4(h,a=1) { const c=hexC3(h); return new BABYLON.Color4(c.r,c.g,c.b,a); }
function lerp(a,b,t) { return a+(b-a)*t; }
function smoothstep(t) { t=Math.max(0,Math.min(1,t)); return t*t*(3-2*t); }

// ── Entry point ───────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  buildHUD();
  initBabylon();
  wireControls();
  wireEnvSliders();
});

// ── 2D HUD overlay ────────────────────────────────────────────────
//
// Architecture:
//   hudDiv          absolute container over canvas-area (pointer-events:none)
//   #hud-svg        SVG layer — connector lines + anchor dots, rebuilt each frame
//   #hud-label-N    fixed-X label panels — only Y tracks the 3D level centre
//
// HUD behaviour:
//   • Label X is CONSTANT (right column) — text never drifts left/right
//   • Label Y tracks only the projected Y of the level's geometric centre
//   • SVG anchor dot sits on the projected SW-NE base diagonal of each frustum
//     and MOVES with camera orbit
//   • Dashed line connects moving anchor → fixed label left edge

const HUD_LABEL_W = 220;   // label panel width  (px)
const HUD_MARGIN_R = 18;   // gap from canvas right edge (px)

function buildHUD() {
  hudDiv = document.createElement('div');
  hudDiv.id = 'hud-overlay';
  Object.assign(hudDiv.style, {
    position:'absolute', inset:'0',
    pointerEvents:'none', overflow:'visible', zIndex:'5'
  });
  document.getElementById('canvas-area').appendChild(hudDiv);

  // SVG layer — rebuilt each frame inside updateHUD
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.id = 'hud-svg';
  Object.assign(svg.style, {
    position:'absolute', inset:'0',
    width:'100%', height:'100%',
    pointerEvents:'none', overflow:'visible'
  });
  hudDiv.appendChild(svg);

  // Fixed label panels (one per level)
  [1, 2, 3, 4].forEach(rank => {
    const col = COLORS[rank];
    const el  = document.createElement('div');
    el.id = 'hud-label-' + rank;
    Object.assign(el.style, {
      position:       'absolute',
      width:          HUD_LABEL_W + 'px',
      display:        'flex',
      flexDirection:  'column',
      alignItems:     'flex-start',
      gap:            '3px',
      pointerEvents:  'none',
      transform:      'translateY(-50%)',   // centre vertically on label.top
      background:     'rgba(13,17,23,0.80)',
      border:         `1px solid ${col}44`,
      borderLeft:     `4px solid ${col}`,
      borderRadius:   '0 6px 6px 0',
      padding:        '6px 12px 6px 10px',
      opacity:        '0',
      transition:     'opacity 0.35s'
    });
    el.innerHTML = `
      <span style="font-size:17px;font-weight:800;color:${col};
                   font-family:'Segoe UI',system-ui,sans-serif;
                   text-shadow:0 0 10px ${col}99,0 1px 4px #000e;
                   white-space:nowrap;">
        ${LEVEL_INFO[rank].emoji}&nbsp;${LEVEL_INFO[rank].short}
      </span>
      <span style="font-size:13px;color:#b1bac4;white-space:nowrap;
                   font-family:'Cascadia Code','Fira Code',monospace;">
        ${LEVEL_INFO[rank].energy}
      </span>
      <span id="hud-pop-${rank}" style="font-size:12px;color:${col}bb;
             white-space:nowrap;font-family:'Cascadia Code','Fira Code',monospace;">
        pop &times;1.00
      </span>`;
    hudDiv.appendChild(el);
  });
}

// ── Project 3D world-space → 2D screen (CSS pixels) ───────────────
// clientWidth/clientHeight are reliable at all times (unlike canvas.width
// which can be 0 before BabylonJS completes its first resize).
function project2D(pos3D, W, H) {
  if (!scene || !camera || !W || !H) return null;

  // Guard: getTransformMatrix() can return an identity/invalid matrix
  // during the very first frames before BabylonJS completes its first render.
  const tm = scene.getTransformMatrix();
  if (!tm || !isFinite(tm.m[0])) return null;

  const vp = camera.viewport.toGlobal(W, H);
  const sc = BABYLON.Vector3.Project(
    pos3D,
    BABYLON.Matrix.Identity(),
    tm,
    vp
  );

  // Reject NaN, Infinity, and points outside the depth clip
  if (!isFinite(sc.x) || !isFinite(sc.y) || !isFinite(sc.z)) return null;
  if (sc.z <= 0 || sc.z >= 1) return null;
  return { x: sc.x, y: sc.y };
}

function updateHUD() {
  if (!scene || !camera) return;

  const canvas = document.getElementById('render-canvas');
  const W = canvas.clientWidth;
  const H = canvas.clientHeight;
  if (!W || !H) return;

  const labelX = W - HUD_LABEL_W - HUD_MARGIN_R;
  const svgParts = [];

  [1, 2, 3, 4].forEach(rank => {
    const el  = document.getElementById('hud-label-' + rank);
    if (!el) return;

    const g   = GEO[rank];
    const col = COLORS[rank];

    // Label Y — only the Y coordinate tracks the 3D level centre
    const centre2D = project2D(new BABYLON.Vector3(0, g.y, 0), W, H);
    if (!centre2D) { el.style.opacity = '0'; return; }

    el.style.opacity = '0.97';
    el.style.left    = labelX + 'px';
    el.style.top     = Math.round(centre2D.y) + 'px';

    // Live pop text
    const popEl = document.getElementById('hud-pop-' + rank);
    if (popEl) {
      const isRemoved = SIM.apexRemoved && rank === 4;
      popEl.textContent = isRemoved
        ? '\u2717 REMOVED'
        : 'pop \u00D7' + POP[rank].toFixed(2);
      popEl.style.color = isRemoved ? '#f78166' : col + 'bb';
    }

    // SVG anchor — midpoint of SW-NE base diagonal of the frustum
    const r         = g.dBot / 2;
    const yBase     = g.y - g.h / 2;
    const anchor2D  = project2D(new BABYLON.Vector3(r * 0.5, yBase, r * 0.5), W, H);
    if (!anchor2D) return;

    const ax     = anchor2D.x;
    const ay     = anchor2D.y;
    const lx     = labelX;
    const ly     = centre2D.y;
    const elbowX = lx - 28;
    const elbowY = ly;

    // Final NaN guard before writing SVG attributes
    if (!isFinite(ax) || !isFinite(ay) || !isFinite(ly)) return;

    svgParts.push(`
      <line x1="${Math.round(ax)}" y1="${Math.round(ay)}"
            x2="${Math.round(elbowX)}" y2="${Math.round(elbowY)}"
            stroke="${col}" stroke-width="1.5" stroke-opacity="0.65"
            stroke-dasharray="5 3"/>
      <line x1="${Math.round(elbowX)}" y1="${Math.round(elbowY)}"
            x2="${Math.round(lx)}" y2="${Math.round(elbowY)}"
            stroke="${col}" stroke-width="1.5" stroke-opacity="0.65"
            stroke-dasharray="5 3"/>
      <circle cx="${Math.round(ax)}" cy="${Math.round(ay)}" r="4"
              fill="${col}" fill-opacity="0.85"
              stroke="rgba(13,17,23,0.9)" stroke-width="1.5"/>
      <circle cx="${Math.round(elbowX)}" cy="${Math.round(elbowY)}" r="2.5"
              fill="${col}" fill-opacity="0.5"/>`);
  });

  const svg = document.getElementById('hud-svg');
  if (svg) svg.innerHTML = svgParts.join('');
}

// ── BabylonJS init ────────────────────────────────────────────────
function initBabylon() {
  const canvas = document.getElementById('render-canvas');
  engine = new BABYLON.Engine(canvas, true);
  scene  = buildScene();

  engine.runRenderLoop(() => {
    if (!SIM.running) return;
    SIM.time += SIM.speed * 0.016;
    updatePopulations();
    updateMeshes();
    updateHUD();
    scene.render();
  });

  window.addEventListener('resize', () => { engine.resize(); });
}

function buildScene() {
  const sc = new BABYLON.Scene(engine);
  sc.clearColor = new BABYLON.Color4(0.051, 0.067, 0.090, 1);

  // Camera
  camera = new BABYLON.ArcRotateCamera('cam', -Math.PI/5, 1.1, 15,
    new BABYLON.Vector3(0, 3.5, 0), sc);
  camera.attachControl(document.getElementById('render-canvas'), true);
  camera.lowerRadiusLimit = 5; camera.upperRadiusLimit = 32;
  camera.wheelPrecision = 50;

  // Lights
  const hemi = new BABYLON.HemisphericLight('h', new BABYLON.Vector3(0,1,0), sc);
  hemi.intensity = 0.5;
  hemi.diffuse   = new BABYLON.Color3(0.85, 0.9, 1.0);
  hemi.groundColor = new BABYLON.Color3(0.08, 0.1, 0.13);

  const sun = new BABYLON.DirectionalLight('sun', new BABYLON.Vector3(-1,-2,-0.5), sc);
  sun.intensity = 0.8;

  // Glow
  glowLayer = new BABYLON.GlowLayer('glow', sc);
  glowLayer.intensity = 0.5;

  buildLevels(sc);
  buildFloor(sc);
  buildParticles(sc);

  // Click picking
  sc.onPointerObservable.add(info => {
    if (info.type !== BABYLON.PointerEventTypes.POINTERPICK) return;
    const rank = info.pickInfo.pickedMesh?.metadata?.rank;
    selectLevel(rank !== undefined ? rank : null);
  });

  return sc;
}

function buildLevels(sc) {
  [1,2,3,4].forEach(rank => {
    const g = GEO[rank];
    const mat = new BABYLON.StandardMaterial('m'+rank, sc);
    mat.diffuseColor  = hexC3(COLORS[rank]);
    mat.specularColor = new BABYLON.Color3(0.25,0.25,0.25);
    mat.specularPower = 40;
    mat.alpha = 0.85;
    levelMaterials[rank] = mat;

    const mesh = BABYLON.MeshBuilder.CreateCylinder('lv'+rank, {
      diameterTop: g.dTop, diameterBottom: g.dBot,
      height: g.h, tessellation: 4
    }, sc);
    mesh.position.y = g.y;
    mesh.material   = mat;
    mesh.metadata   = { rank };
    levelMeshes[rank] = mesh;

    // Wire overlay
    const wm = new BABYLON.StandardMaterial('wm'+rank, sc);
    wm.emissiveColor = hexC3(COLORS[rank]).scale(0.4);
    wm.wireframe = true; wm.alpha = 0.25;
    const wMesh = mesh.clone('wlv'+rank);
    wMesh.material = wm; wMesh.isPickable = false; wMesh.metadata = {};
  });
}

function buildFloor(sc) {
  const m = BABYLON.MeshBuilder.CreateGround('floor',{width:16,height:12,subdivisions:16},sc);
  const mat = new BABYLON.StandardMaterial('fm', sc);
  mat.diffuseColor  = new BABYLON.Color3(0.06,0.08,0.11);
  mat.wireframe = true;
  m.material  = mat; m.position.y = -0.02; m.isPickable = false;
}

// ── Particle systems ──────────────────────────────────────────────
// ── Create a shared procedural particle texture (white radial gradient) ──
// Using DynamicTexture avoids the texImage2D/mipmap WebGL errors that occur
// when loading a tiny data-URI PNG (8×8) with BabylonJS's mipmap pipeline.
function makeParticleTex(sc) {
  const size = 32;
  const tex  = new BABYLON.DynamicTexture('ptex', { width: size, height: size }, sc, false);
  tex.hasAlpha = true;
  tex.wrapU = BABYLON.Texture.CLAMP_ADDRESSMODE;
  tex.wrapV = BABYLON.Texture.CLAMP_ADDRESSMODE;
  const ctx = tex.getContext();
  const cx  = size / 2;
  const grad = ctx.createRadialGradient(cx, cx, 0, cx, cx, cx);
  grad.addColorStop(0,   'rgba(255,255,255,1)');
  grad.addColorStop(0.4, 'rgba(255,255,255,0.8)');
  grad.addColorStop(1,   'rgba(255,255,255,0)');
  ctx.clearRect(0, 0, size, size);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  tex.update();
  return tex;
}

function buildParticles(sc) {
  // Create one shared procedural texture for all particle systems
  const ptex = makeParticleTex(sc);

  // ── Upward energy stream between each pair of adjacent levels ──
  [1,2,3].forEach(rank => {
    const g   = GEO[rank];
    const gUp = GEO[rank+1];
    const ps  = new BABYLON.ParticleSystem('ep'+rank, 120, sc);
    ps.particleTexture = ptex;

    // Emitter at top surface of lower level
    ps.emitter = new BABYLON.Vector3(0, g.y + g.h/2, 0);
    const spread = g.dTop * 0.35;
    ps.minEmitBox = new BABYLON.Vector3(-spread, 0, -spread);
    ps.maxEmitBox = new BABYLON.Vector3( spread, 0,  spread);

    // Colour: gradient from lower level colour to upper level colour
    ps.color1    = hexC4(COLORS[rank],   0.9);
    ps.color2    = hexC4(COLORS[rank+1], 0.7);
    ps.colorDead = new BABYLON.Color4(1, 0.6, 0.2, 0);

    ps.minSize = 0.10; ps.maxSize = 0.22;
    ps.minLifeTime = 0.7; ps.maxLifeTime = 1.4;
    ps.emitRate = 18;
    ps.gravity  = new BABYLON.Vector3(0, 0, 0);
    // Upward with gentle spiral
    ps.direction1 = new BABYLON.Vector3(-0.15, 1.2, -0.15);
    ps.direction2 = new BABYLON.Vector3( 0.15, 1.8,  0.15);
    ps.minEmitPower = 0.6; ps.maxEmitPower = 1.1;
    ps.updateSpeed  = 0.025;
    ps.start();
    energyParticles[rank] = ps;
  });

  // ── Heat dissipation sparks at each level boundary ──
  [2,3,4].forEach(rank => {
    const g  = GEO[rank];
    const ps = new BABYLON.ParticleSystem('ht'+rank, 60, sc);
    ps.particleTexture = ptex;

    ps.emitter = new BABYLON.Vector3(0, g.y - g.h/2 - 0.05, 0);
    const sp = g.dBot * 0.45;
    ps.minEmitBox = new BABYLON.Vector3(-sp, 0, -sp);
    ps.maxEmitBox = new BABYLON.Vector3( sp, 0,  sp);

    ps.color1    = new BABYLON.Color4(1.0, 0.65, 0.15, 0.85);
    ps.color2    = new BABYLON.Color4(0.9, 0.30, 0.05, 0.5);
    ps.colorDead = new BABYLON.Color4(0.4, 0.1, 0, 0);

    ps.minSize = 0.04; ps.maxSize = 0.11;
    ps.minLifeTime = 0.25; ps.maxLifeTime = 0.55;
    ps.emitRate = 10;
    ps.gravity  = new BABYLON.Vector3(0, -0.6, 0);
    ps.direction1 = new BABYLON.Vector3(-1.0, 0.5, -1.0);
    ps.direction2 = new BABYLON.Vector3( 1.0, 1.2,  1.0);
    ps.minEmitPower = 0.25; ps.maxEmitPower = 0.65;
    ps.updateSpeed  = 0.04;
    ps.start();
    heatParticles[rank] = ps;
  });
}

// ── Population dynamics ───────────────────────────────────────────
function updatePopulations() {
  const envBase = envMultiplier(1);

  if (SIM.apexRemoved) {
    SIM.cascadeTimer = Math.min(SIM.cascadeTimer + SIM.speed * 0.012, 1.0);
    const t = SIM.cascadeTimer;
    POP_TARGET[4] = 0.05;
    POP_TARGET[3] = lerp(1.0, 2.5, smoothstep(Math.max(0, t-0.1)));
    POP_TARGET[2] = lerp(1.0, 0.4 * envBase, smoothstep(Math.max(0, t-0.3)));
    POP_TARGET[1] = lerp(1.0, 1.5 * envBase, smoothstep(Math.max(0, t-0.5)));
    POP_TARGET[0] = lerp(1.0, 1.2, smoothstep(Math.max(0, t-0.5)));
  } else {
    SIM.cascadeTimer = 0;
    const osc = SIM.time;
    // Gentle Lotka-Volterra + ENV influence
    POP_TARGET[1] = envBase       * (1.0 + 0.05 * Math.sin(osc*0.4));
    POP_TARGET[2] = envBase*0.95  * (1.0 + 0.04 * Math.sin(osc*0.4 + 1.2));
    POP_TARGET[3] = envBase*0.90  * (1.0 + 0.03 * Math.sin(osc*0.4 + 2.4));
    POP_TARGET[4] = envBase*0.85  * (1.0 + 0.02 * Math.sin(osc*0.4 + 3.6));
    POP_TARGET[0] = Math.sqrt(1 - envBase) * 0.5 + envBase * 0.7;
  }

  [0,1,2,3,4].forEach(r => { POP[r] = lerp(POP[r], POP_TARGET[r], 0.03*SIM.speed); });
}

function updateMeshes() {
  const isCollapsing = ENV.co2 > 0.75 || ENV.temp > 0.75 || ENV.water < 0.2;

  [1,2,3,4].forEach(rank => {
    const mesh = levelMeshes[rank];
    if (!mesh) return;
    const scale = Math.cbrt(Math.max(0.05, POP[rank]));
    mesh.scaling.x = scale; mesh.scaling.z = scale;

    const mat = levelMaterials[rank];
    // Selection highlight
    mat.emissiveColor = SIM.selectedRank === rank
      ? hexC3(COLORS[rank]).scale(0.4)
      : BABYLON.Color3.BlackReadOnly;

    // Apex fade on cascade
    if (rank === 4 && SIM.apexRemoved)
      mat.alpha = lerp(mat.alpha, 0.12, 0.05);
    else
      mat.alpha = lerp(mat.alpha, 0.85, 0.05);

    // Env stress: pulse red tint on collapse
    if (isCollapsing && rank >= 3) {
      const pulse = 0.5 + 0.5*Math.sin(SIM.time * 3);
      mat.emissiveColor = new BABYLON.Color3(0.4*pulse, 0, 0);
    }
  });

  // Particle rates driven by ENV
  const lightFactor = ENV.light;
  [1,2,3].forEach(rank => {
    const ps = energyParticles[rank];
    if (ps) {
      const rate = Math.round(lightFactor * 22 * POP[rank] * (4-rank) / 1.5);
      ps.emitRate = Math.max(2, rate);
    }
  });

  // Adjust glow with CO2/temp stress
  if (glowLayer) {
    const stress = (ENV.co2 + ENV.temp) / 2;
    glowLayer.intensity = lerp(0.35, 0.9, stress);
  }
}

// ── Level selection ───────────────────────────────────────────────
function selectLevel(rank) {
  SIM.selectedRank = rank;
  if (rank !== null) {
    // Switch to Scores tab
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    const btn = document.querySelector('[data-tab="scores"]');
    if (btn) { btn.classList.add('active');
               document.getElementById('panel-scores').classList.add('active'); }
  }
  updateLevelInfoPanel(rank);
}

function updateLevelInfoPanel(rank) {
  const box = document.getElementById('level-info');
  if (!box) return;
  if (rank === null) {
    box.innerHTML='<div class="level-info-box"><span style="color:var(--muted)">Click a level in the 3D view to inspect</span></div>';
    return;
  }
  const lv = POCLET_METADATA.levels.find(l=>l.rank===rank);
  if (!lv) return;
  const envMul = envMultiplier(rank);
  const pop = (POP[rank] * envMul).toFixed(2);
  const col  = SIM.apexRemoved && rank===4 ? 'var(--eagle)' : 'var(--accent)';
  const status = SIM.apexRemoved && rank===4 ? '✗ REMOVED — cascade active' : `pop ×${pop}`;
  box.innerHTML=`<div class="level-info-box">
    <div class="level-title">${lv.label} <span class="level-rank">[Rank ${lv.rank||'⟂'}]</span></div>
    <div style="color:var(--muted);font-size:11px;margin-bottom:4px">${lv.sublabel} · <em>${lv.organisms}</em></div>
    <div style="font-size:11px;color:var(--text-dim);margin-bottom:4px">${lv.info.slice(0,160)}…</div>
    <div style="font-size:10px;color:var(--muted)">ASFID: A=${lv.asfid.A} S=${lv.asfid.S} F=${lv.asfid.F} I=${lv.asfid.I} D=${lv.asfid.D}</div>
    <div style="font-size:11px;color:${col};margin-top:4px;font-weight:600">${status}</div>
  </div>`;
}

// ── Wire controls ─────────────────────────────────────────────────
function wireControls() {
  const btnPlay    = document.getElementById('btn-play');
  const btnReset   = document.getElementById('btn-reset');
  const btnCascade = document.getElementById('btn-cascade');
  const speedSlider = document.getElementById('speed-slider');
  const statusDot   = document.getElementById('status-dot');
  const statusLabel = document.getElementById('status-label');

  btnPlay.addEventListener('click', () => {
    SIM.running = !SIM.running;
    btnPlay.textContent = SIM.running ? '⏸ Pause' : '▶ Play';
    btnPlay.classList.toggle('active', SIM.running);
    statusDot.className = 'status-dot' + (SIM.running ? (SIM.apexRemoved?' cascade':' running') : '');
    statusLabel.textContent = SIM.running ? (SIM.apexRemoved?'CASCADE':'Running') : 'Paused';
  });

  btnReset.addEventListener('click', () => {
    SIM.apexRemoved=false; SIM.cascadeTimer=0; SIM.time=0; SIM.selectedRank=null;
    [0,1,2,3,4].forEach(r=>{ POP[r]=1; POP_TARGET[r]=1; });
    // Reset ENV sliders to defaults
    ENV.light=0.75; ENV.water=0.70; ENV.o2=0.21; ENV.co2=0.42; ENV.temp=0.38;
    syncEnvSliders();
    btnCascade.textContent='🐺 Remove Apex Predator'; btnCascade.classList.remove('active');
    SIM.running=true; btnPlay.textContent='⏸ Pause'; btnPlay.classList.add('active');
    statusDot.className='status-dot running'; statusLabel.textContent='Running';
    updateLevelInfoPanel(null);
  });

  btnCascade.addEventListener('click', () => {
    SIM.apexRemoved=!SIM.apexRemoved; SIM.cascadeTimer=0;
    if (SIM.apexRemoved) {
      btnCascade.textContent='🔄 Restore Apex Predator'; btnCascade.classList.add('active');
      statusDot.className='status-dot cascade'; statusLabel.textContent='CASCADE';
    } else {
      btnCascade.textContent='🐺 Remove Apex Predator'; btnCascade.classList.remove('active');
      statusDot.className='status-dot running'; statusLabel.textContent='Running';
    }
  });

  speedSlider.addEventListener('input', () => {
    SIM.speed = parseFloat(speedSlider.value);
    document.getElementById('speed-label').textContent = '×' + SIM.speed.toFixed(1);
  });
}

// ── Environmental sliders ─────────────────────────────────────────
function wireEnvSliders() {
  const defs = [
    { id:'sl-light', key:'light', label:'sl-light-val', fmt: v=>`${Math.round(v*100)}%`     },
    { id:'sl-water', key:'water', label:'sl-water-val', fmt: v=>`${Math.round(v*100)}%`     },
    { id:'sl-co2',   key:'co2',   label:'sl-co2-val',   fmt: v=>`${Math.round(280+v*720)} ppm` },
    { id:'sl-temp',  key:'temp',  label:'sl-temp-val',  fmt: v=>`+${(v*6-0).toFixed(1)} °C` }
  ];
  defs.forEach(({ id, key, label, fmt }) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('input', () => {
      ENV[key] = parseFloat(el.value);
      const lbl = document.getElementById(label);
      if (lbl) lbl.textContent = fmt(ENV[key]);
      updateEnvWarnings();
    });
  });
  syncEnvSliders();
}

function syncEnvSliders() {
  const vals = {
    'sl-light': ENV.light, 'sl-water': ENV.water,
    'sl-co2': ENV.co2,     'sl-temp':  ENV.temp
  };
  const fmts = {
    'sl-light': v=>`${Math.round(v*100)}%`,
    'sl-water': v=>`${Math.round(v*100)}%`,
    'sl-co2':   v=>`${Math.round(280+v*720)} ppm`,
    'sl-temp':  v=>`+${(v*6).toFixed(1)} °C`
  };
  const lbls = {
    'sl-light':'sl-light-val','sl-water':'sl-water-val',
    'sl-co2':'sl-co2-val','sl-temp':'sl-temp-val'
  };
  Object.keys(vals).forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = vals[id];
    const lbl = document.getElementById(lbls[id]);
    if (lbl) lbl.textContent = fmts[id](vals[id]);
  });
  updateEnvWarnings();
}

function updateEnvWarnings() {
  const warn = document.getElementById('env-warnings');
  if (!warn) return;
  const msgs = [];
  if (ENV.co2 > 0.60) msgs.push(`⚠ CO₂ ${Math.round(280+ENV.co2*720)} ppm — ocean acidification risk`);
  if (ENV.temp > 0.50) msgs.push(`⚠ +${(ENV.temp*6).toFixed(1)}°C — tipping point approaching`);
  if (ENV.water < 0.30) msgs.push(`⚠ Water stress — producer collapse risk`);
  if (ENV.light < 0.30) msgs.push(`⚠ Low irradiance — NPP severely reduced`);
  if (msgs.length === 0) msgs.push('✓ Environmental parameters within safe bounds');
  warn.innerHTML = msgs.map(m =>
    `<div style="color:${m.startsWith('⚠')?'var(--warn)':'var(--accent)'};font-size:10.5px">${m}</div>`
  ).join('');
}
