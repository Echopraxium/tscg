// ──────────────────────────────────────────────────────────────
// Butterfly Metamorphosis Poclet — BabylonJS Simulation
// Author: Echopraxium with the collaboration of Claude AI
// Framework: TSCG (Transdisciplinary System Construction Game)
//
// Approach: PARAMETRIC morphing (not mesh morph-targets). A single
// parametric rig (segmented body + wings + legs + antennae + chrysalis
// shell) is rebuilt every frame from an interpolated parameter vector.
// Topology never changes, so egg <-> caterpillar <-> imago all share
// one rig. Appendages GROW (embryonic wings/limbs) rather than magically
// fade, which is closer to the biology (Structure dimension).
// ──────────────────────────────────────────────────────────────

(function () {
  'use strict';

  const DATA = window.TSCG_BUTTERFLY;
  const POLES = DATA.POLES;
  const SPECIES = DATA.SPECIES;
  const META = DATA.META;

  // ═══ State ═══
  const state = {
    speciesId: 'monarch',   // default: Monarch (a nod to "Under the Dome")
    phase: 0,               // continuous position in [0 .. POLES.length-1]
    playing: false,
    speed: 1,               // 1 / 2 / 3 / 5
    autoRotate: false,
    lastTime: 0
  };
  const SEG_TIME = 2.8;       // seconds per pole-to-pole segment at speed x1
  const MAX_PHASE = POLES.length - 1;

  // ═══ 1. BabylonJS Setup ═══
  const canvas = document.getElementById('canvas-main');
  const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true, stencil: true });
  const scene = new BABYLON.Scene(engine);
  scene.clearColor = new BABYLON.Color4(0.05, 0.07, 0.10, 1.0);

  // Camera: ArcRotate gives azimuth + elevation + zoom -> practically
  // view the model from any angle. Alpha unrestricted (full spin),
  // beta near-full. Wheel / pinch to zoom.
  const camera = new BABYLON.ArcRotateCamera(
    'cam', Math.PI / 2.2, Math.PI / 2.4, 12,
    new BABYLON.Vector3(0, 0.5, 0), scene);
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 4;
  camera.upperRadiusLimit = 30;
  camera.lowerBetaLimit = 0.05;
  camera.upperBetaLimit = Math.PI - 0.05;
  camera.wheelDeltaPercentage = 0.01;
  camera.pinchDeltaPercentage = 0.01;
  camera.panningSensibility = 0;

  const hemi = new BABYLON.HemisphericLight('hemi', new BABYLON.Vector3(0, 1, 0), scene);
  hemi.intensity = 0.75;
  hemi.groundColor = new BABYLON.Color3(0.15, 0.18, 0.22);
  const dir = new BABYLON.DirectionalLight('dir', new BABYLON.Vector3(-0.4, -1, -0.6), scene);
  dir.intensity = 0.8;

  // ═══ 2. Materials ═══
  function mat(name, hex) {
    const m = new BABYLON.StandardMaterial(name, scene);
    m.diffuseColor = BABYLON.Color3.FromHexString(hex);
    m.specularColor = new BABYLON.Color3(0.1, 0.1, 0.1);
    return m;
  }
  const bodyMat = mat('bodyMat', '#888888');
  const wingMat = mat('wingMat', '#e07b1a');
  wingMat.backFaceCulling = false;
  const wingSpotMat = mat('wingSpotMat', '#ffffff');
  wingSpotMat.backFaceCulling = false;
  const legMat = mat('legMat', '#222222');
  const antMat = mat('antMat', '#222222');
  const chrysMat = mat('chrysMat', '#3f7d4e');
  chrysMat.alpha = 0.5;
  chrysMat.backFaceCulling = false;
  chrysMat.specularColor = new BABYLON.Color3(0.3, 0.3, 0.3);
  const chrysAccentMat = mat('chrysAccentMat', '#ffd23f');

  // ═══ 3. Parametric Rig (built once, updated every frame) ═══
  const root = new BABYLON.TransformNode('root', scene);

  // --- Body: fixed pool of segment spheres arranged along +Z (front = +Z)
  const SEG_COUNT = 14;
  const bodySegs = [];
  for (let i = 0; i < SEG_COUNT; i++) {
    const s = BABYLON.MeshBuilder.CreateSphere('seg' + i, { diameter: 1, segments: 10 }, scene);
    s.material = bodyMat;
    s.parent = root;
    bodySegs.push(s);
  }
  // Head sphere at the front (+Z)
  const head = BABYLON.MeshBuilder.CreateSphere('head', { diameter: 1, segments: 12 }, scene);
  head.material = bodyMat;
  head.parent = root;

  // --- Legs: 6 thin cylinders under the thorax (front third)
  const legs = [];
  for (let i = 0; i < 6; i++) {
    const leg = BABYLON.MeshBuilder.CreateCylinder('leg' + i, { height: 1, diameterTop: 0.04, diameterBottom: 0.08, tessellation: 6 }, scene);
    leg.material = legMat;
    leg.parent = root;
    legs.push(leg);
  }

  // --- Antennae: 2 thin cylinders + club tips at the head
  const antennae = [];
  for (let i = 0; i < 2; i++) {
    const a = BABYLON.MeshBuilder.CreateCylinder('ant' + i, { height: 1, diameterTop: 0.05, diameterBottom: 0.05, tessellation: 6 }, scene);
    a.material = antMat;
    a.parent = root;
    const tip = BABYLON.MeshBuilder.CreateSphere('antTip' + i, { diameter: 0.16, segments: 8 }, scene);
    tip.material = antMat;
    tip.parent = a;
    tip.position.y = 0.5; // top of the cylinder (local)
    antennae.push(a);
  }

  // --- Wings: fore + hind on each side, parented to a flap pivot.
  //     Pivot rotates about Z (body long axis) -> flap. Wings lie in the
  //     XZ plane (disc rotated so its normal points up in Y).
  function makeWing(side, kind) {
    const pivot = new BABYLON.TransformNode('wingPivot_' + side + '_' + kind, scene);
    pivot.parent = root;
    const disc = BABYLON.MeshBuilder.CreateDisc('wing_' + side + '_' + kind, { radius: 1, tessellation: 40 }, scene);
    disc.material = wingMat;
    disc.parent = pivot;
    disc.rotation.x = Math.PI / 2;             // lay flat (normal -> +Y)
    disc.position.x = side * 1.0;              // offset outward along span
    // eyespot decal (shown only for eyespot species)
    const spot = BABYLON.MeshBuilder.CreateDisc('wingSpot_' + side + '_' + kind, { radius: 0.28, tessellation: 20 }, scene);
    spot.material = wingSpotMat;
    spot.parent = disc;
    spot.position.z = 0.02;                     // sit just above membrane
    spot.rotation = new BABYLON.Vector3(0, 0, 0);
    // tail (Swallowtail) — small elongated flap on the hindwing trailing edge
    let tail = null;
    if (kind === 'hind') {
      tail = BABYLON.MeshBuilder.CreateDisc('wingTail_' + side, { radius: 0.35, tessellation: 12 }, scene);
      tail.material = wingMat;
      tail.parent = disc;
      tail.scaling = new BABYLON.Vector3(0.35, 1.4, 1);
      tail.position = new BABYLON.Vector3(side * 0.2, -1.0, 0);
    }
    return { pivot: pivot, disc: disc, spot: spot, tail: tail, side: side, kind: kind };
  }
  const wings = [
    makeWing(1, 'fore'), makeWing(-1, 'fore'),
    makeWing(1, 'hind'), makeWing(-1, 'hind')
  ];

  // --- Chrysalis shell: a translucent teardrop enclosing the body.
  const chrysalis = BABYLON.MeshBuilder.CreateSphere('chrysalis', { diameterX: 1, diameterY: 1, diameterZ: 1, segments: 20 }, scene);
  chrysalis.material = chrysMat;
  chrysalis.parent = root;
  // gold spots ring (Monarch / Vanessa / Peacock)
  const goldSpots = [];
  for (let i = 0; i < 8; i++) {
    const g = BABYLON.MeshBuilder.CreateSphere('gold' + i, { diameter: 0.12, segments: 6 }, scene);
    g.material = chrysAccentMat;
    g.parent = chrysalis;
    const ang = (i / 8) * Math.PI * 2;
    g.position = new BABYLON.Vector3(Math.cos(ang) * 0.42, 0.25, Math.sin(ang) * 0.42);
    goldSpots.push(g);
  }

  // ═══ 4. Interpolation helpers ═══
  function smooth(t) { return t * t * (3 - 2 * t); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function lerpColor(c1, c2, t) {
    return new BABYLON.Color3(lerp(c1.r, c2.r, t), lerp(c1.g, c2.g, t), lerp(c1.b, c2.b, t));
  }
  function hex(h) { return BABYLON.Color3.FromHexString(h); }

  // Body colour per pole (egg -> larva -> pupa/chrysalis -> imago), by species
  function poleBodyColor(sp, idx) {
    const p = sp.palette;
    switch (POLES[idx].key) {
      case 'egg': return hex(p.egg);
      case 'larva': return hex(p.caterpillar);
      case 'prepupa': return lerpColor(hex(p.caterpillar), hex(p.body), 0.5);
      case 'pupa': return hex(p.body);
      case 'emergence': return hex(p.body);
      case 'imago': return hex(p.body);
      default: return hex(p.body);
    }
  }

  // Interpolated parameter vector at the current phase
  function currentParams() {
    const i0 = Math.min(Math.floor(state.phase), MAX_PHASE);
    const i1 = Math.min(i0 + 1, MAX_PHASE);
    const t = smooth(state.phase - i0);
    const a = POLES[i0], b = POLES[i1];
    const sp = SPECIES[state.speciesId];
    return {
      i0: i0, i1: i1, t: t,
      bodyLength: lerp(a.bodyLength, b.bodyLength, t),
      bodyRadius: lerp(a.bodyRadius, b.bodyRadius, t),
      taper: lerp(a.taper, b.taper, t),
      legLen: lerp(a.legLen, b.legLen, t),
      wingExtent: lerp(a.wingExtent, b.wingExtent, t),
      antenna: lerp(a.antenna, b.antenna, t),
      chrysalisA: lerp(a.chrysalisA, b.chrysalisA, t),
      headSize: lerp(a.headSize, b.headSize, t),
      bodyColor: lerpColor(poleBodyColor(sp, i0), poleBodyColor(sp, i1), t)
    };
  }

  // ═══ 5. Apply parameters to the rig (called every frame) ═══
  function applyRig(P, timeSec) {
    const sp = SPECIES[state.speciesId];
    const flags = sp.flags;
    const pal = sp.palette;
    const half = P.bodyLength / 2;

    // Idle animations only when paused exactly on a pole
    const onPole = !state.playing && Math.abs(state.phase - Math.round(state.phase)) < 0.001;
    const poleForm = POLES[Math.round(state.phase)].form;
    const crawl = (onPole && poleForm === 'larva');   // caterpillar = pole 2 (index 1)
    const flap = (onPole && poleForm === 'imago');    // imago = pole 6 (index 5)

    bodyMat.diffuseColor = P.bodyColor;

    // --- Body segments along Z, with a taper profile + optional crawl wave
    for (let i = 0; i < SEG_COUNT; i++) {
      const u = SEG_COUNT === 1 ? 0.5 : i / (SEG_COUNT - 1);   // 0..1 along body
      let z = (u - 0.5) * P.bodyLength;
      // taper: ends thinner than middle
      const bulge = 1 - P.taper * Math.pow(Math.abs(u - 0.5) * 2, 2);
      let r = P.bodyRadius * Math.max(0.08, bulge);
      let yOff = 0;
      if (crawl) {
        // peristaltic wave travelling head-ward: local bulge + gentle lift
        const wave = Math.sin(u * Math.PI * 3 - timeSec * 4);
        r *= 1 + 0.18 * wave;
        z += 0.10 * Math.sin(u * Math.PI * 3 - timeSec * 4);
        yOff = 0.06 * Math.max(0, wave);
      }
      const seg = bodySegs[i];
      seg.position.set(0, r * 0.5 - P.bodyRadius * 0.3 + yOff, z);
      seg.scaling.set(r, r, r);
    }

    // --- Head at the front (+Z), scaled by headSize (hidden for egg)
    const headR = P.bodyRadius * 1.25 * P.headSize;
    head.scaling.set(headR, headR, headR);
    head.position.set(0, headR * 0.5 - P.bodyRadius * 0.3, half + headR * 0.4);
    head.setEnabled(P.headSize > 0.02);

    // --- Legs under the thorax (front third), fan out; height = legLen
    const legShow = P.legLen > 0.02;
    for (let i = 0; i < 6; i++) {
      const leg = legs[i];
      leg.setEnabled(legShow);
      if (!legShow) continue;
      const sideSign = (i % 2 === 0) ? 1 : -1;
      const rowFrac = Math.floor(i / 2) / 2;          // 0, .5, 1
      const lz = lerp(half * 0.2, half * 0.7, rowFrac);
      const h = 0.9 * P.legLen;
      leg.scaling.set(1, h, 1);
      leg.position.set(sideSign * (P.bodyRadius * 0.9), -P.bodyRadius * 0.5 - h * 0.4, lz);
      leg.rotation.set(0, 0, sideSign * -0.5);
      legMat.diffuseColor = hex(pal.body);
    }

    // --- Antennae from the head, angled up/forward; length = antenna
    const antShow = P.antenna > 0.02;
    for (let i = 0; i < 2; i++) {
      const a = antennae[i];
      a.setEnabled(antShow);
      if (!antShow) continue;
      const sideSign = (i === 0) ? 1 : -1;
      const h = 1.1 * P.antenna;
      a.scaling.set(1, h, 1);
      a.position.set(sideSign * headR * 0.4, headR * 0.4, half + headR * 0.4);
      a.rotation.set(-0.7, 0, sideSign * -0.35);
      antMat.diffuseColor = hex(pal.body);
    }

    // --- Wings: extent scales size; flap oscillates dihedral; species traits
    const wingShow = P.wingExtent > 0.02;
    const span = P.wingExtent * sp.wingspanScale;
    const flapAngle = flap ? (0.35 + 0.35 * Math.sin(timeSec * 3)) : 0.12;
    wingMat.diffuseColor = hex(pal.wingPrimary);
    if (flags.iridescent) {
      wingMat.emissiveColor = hex(pal.wingPrimary).scale(0.35);
      wingMat.specularColor = new BABYLON.Color3(0.6, 0.7, 1.0);
    } else {
      wingMat.emissiveColor = new BABYLON.Color3(0, 0, 0);
      wingMat.specularColor = new BABYLON.Color3(0.1, 0.1, 0.1);
    }
    wingSpotMat.diffuseColor = hex(pal.wingSpot);

    for (let k = 0; k < wings.length; k++) {
      const w = wings[k];
      w.pivot.setEnabled(wingShow);
      if (!wingShow) continue;
      // pivot at the thorax
      w.pivot.position.set(0, P.bodyRadius * 0.2, half * 0.35);
      // dihedral flap: right side up when angle>0, left mirrored
      w.pivot.rotation.z = w.side * -flapAngle;
      // fore vs hind size + placement
      const isFore = w.kind === 'fore';
      const sx = span * (isFore ? 1.15 : 0.95);
      const sz = span * (isFore ? 1.35 : 1.05);
      w.disc.scaling.set(sx, sz, 1);
      w.disc.position.x = w.side * span * 0.95;
      w.disc.position.z = isFore ? span * 0.25 : -span * 0.55;
      // eyespots (Peacock) — one per wing near the outer edge
      w.spot.setEnabled(flags.eyespots);
      if (flags.eyespots) {
        w.spot.position.set(0, isFore ? 0.35 : -0.2, 0.02);
        w.spot.scaling.set(0.9, 0.9, 1);
      }
      // tails (Swallowtail) on hindwings only
      if (w.tail) w.tail.setEnabled(flags.wingTails);
    }

    // --- Chrysalis shell: translucent, encloses body; visible poles 3-5.
    // At the Pupa, low-ish alpha reveals the forming imago inside
    // (imaginal discs / candidate "Latency").
    const showChrys = P.chrysalisA > 0.01;
    chrysalis.setEnabled(showChrys);
    if (showChrys) {
      chrysMat.diffuseColor = hex(pal.chrysalis);
      chrysMat.alpha = P.chrysalisA;
      const cw = P.bodyRadius * 2.4;
      const cl = (P.bodyLength * 0.95 + P.bodyRadius * 2) * 0.55;
      chrysalis.scaling.set(cw, cl, cw);
      chrysalis.rotation.x = Math.PI / 2;      // long axis along the body (Z)
      chrysalis.position.set(0, 0, 0);
      for (let i = 0; i < goldSpots.length; i++) goldSpots[i].setEnabled(flags.chrysalisGoldSpots);
    }
  }

  // ═══ 6. Render / animation loop ═══
  function tick() {
    const now = performance.now() / 1000;
    const dt = state.lastTime ? now - state.lastTime : 0;
    state.lastTime = now;

    if (state.playing) {
      state.phase += (dt / SEG_TIME) * state.speed;
      if (state.phase >= MAX_PHASE) { state.phase = MAX_PHASE; setPlaying(false); }
      syncTimeline();
    }
    if (state.autoRotate) camera.alpha += dt * 0.5;

    const P = currentParams();
    applyRig(P, now);
  }
  scene.registerBeforeRender(tick);
  engine.runRenderLoop(function () { scene.render(); });
  window.addEventListener('resize', function () { engine.resize(); });

  // ═══ 7. UI Controls ═══
  const playBtn = document.getElementById('play-btn');
  const resetBtn = document.getElementById('reset-btn');
  const rotBtn = document.getElementById('rotate-btn');
  const speciesSel = document.getElementById('species-select');
  const speedBtns = Array.prototype.slice.call(document.querySelectorAll('.speed-btn'));
  const milestones = Array.prototype.slice.call(document.querySelectorAll('.milestone'));
  const phaseLabel = document.getElementById('phase-label');
  const statusLine = document.getElementById('status-line');
  const speciesClear = document.getElementById('species-clear');
  const chipSpecies = document.getElementById('chip-species');
  const latinName = document.getElementById('latin-name');

  function setPlaying(on) {
    state.playing = on;
    playBtn.innerHTML = on ? '&#10074;&#10074; Pause' : '&#9654; Play';
    playBtn.classList.toggle('playing', on);
  }
  function jumpTo(idx) {
    setPlaying(false);
    state.phase = idx;
    syncTimeline();
  }
  function syncTimeline() {
    const nearest = Math.round(state.phase);
    milestones.forEach(function (m, i) { m.classList.toggle('active', i === nearest); });
    const p = POLES[nearest];
    const txt = (nearest + 1) + ' / 6 · ' + p.label;
    if (phaseLabel) phaseLabel.textContent = txt;
    if (statusLine) statusLine.textContent = txt;
  }
  function syncSpecies() {
    const sp = SPECIES[state.speciesId];
    if (chipSpecies) chipSpecies.textContent = sp.common;
    if (latinName) latinName.textContent = sp.latin;
  }

  playBtn.addEventListener('click', function () {
    if (state.phase >= MAX_PHASE) state.phase = 0;   // replay from egg
    setPlaying(!state.playing);
  });
  resetBtn.addEventListener('click', function () {
    setPlaying(false);
    state.phase = 0;
    state.autoRotate = false;
    rotBtn.classList.remove('on');
    camera.alpha = Math.PI / 2.2; camera.beta = Math.PI / 2.4; camera.radius = 12;
    syncTimeline();
  });
  rotBtn.addEventListener('click', function () {
    state.autoRotate = !state.autoRotate;
    rotBtn.classList.toggle('on', state.autoRotate);
  });
  speciesSel.addEventListener('change', function (e) {
    state.speciesId = e.target.value;
    syncSpecies();
  });
  speciesClear.addEventListener('click', function () {
    state.speciesId = 'monarch';
    speciesSel.value = 'monarch';
    syncSpecies();
  });
  speedBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      state.speed = parseInt(b.getAttribute('data-speed'), 10);
      speedBtns.forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
    });
  });
  milestones.forEach(function (m, i) {
    m.addEventListener('click', function () { jumpTo(i); });
  });

  // ═══ 8. Sidebar (tabs + content from M0 metadata) ═══
  function buildSidebar() {
    document.getElementById('tab-description').innerHTML =
      '<p>' + META.description + '</p>' +
      '<p class="meta"><b>Domain:</b> ' + META.domain + '<br>' +
      '<b>Version:</b> ' + META.version + ' · <b>Status:</b> ' + META.status + '</p>';

    function scoreRows(obj, labels) {
      return labels.map(function (l) {
        const v = obj[l[0]];
        return '<div class="score-row"><span>' + l[1] + '</span>' +
          '<span class="bar"><i style="width:' + (v * 100) + '%"></i></span>' +
          '<b>' + v.toFixed(2) + '</b></div>';
      }).join('');
    }
    document.getElementById('tab-scores').innerHTML =
      '<h4>ASFID · Eagle Eye (Territory)</h4>' +
      scoreRows(META.asfid, [['A', 'Attractor'], ['S', 'Structure'], ['F', 'Flow'], ['I', 'Information'], ['D', 'Dynamics']]) +
      '<p class="mean">mean ' + META.asfid.mean.toFixed(2) + '</p>' +
      '<h4>REVOI · Sphinx Eye (Map)</h4>' +
      scoreRows(META.revoi, [['R', 'Representability'], ['E', 'Evolvability'], ['V', 'Verifiability'], ['O', 'Observability'], ['Im', 'Interoperability']]) +
      '<p class="mean">mean ' + META.revoi.mean.toFixed(2) + ' · provisional</p>' +
      '<div class="gap-badge">Epistemic gap δ₁ = ' + META.epistemicGap.toFixed(2) + ' (provisional)</div>';

    document.getElementById('tab-concepts').innerHTML =
      '<p class="meta">M2 GenericConcepts per M2 v16.16.0 (Structural Grammar). ' +
      'Switch / Mode / Cycle / Latency (obsolete) remapped to Behavior · Step · Stase · Potentialization.</p>' +
      META.m2.map(function (c) {
        return '<div class="m2-row"><span class="m2-name">' + c.name + '</span>' +
          '<span class="m2-dom">' + c.dominance.toFixed(2) + '</span>' +
          '<code class="m2-formula">' + c.formula + '</code>' +
          '<p class="m2-note">' + c.note + '</p></div>';
      }).join('');

    document.getElementById('tab-guide').innerHTML =
      '<ul>' +
      '<li><b>▶ Play</b> — run the full metamorphosis, egg → imago.</li>' +
      '<li><b>Timeline dots</b> — jump straight to any of the 6 poles.</li>' +
      '<li><b>x1 / x2 / x3 / x5</b> — metamorphosis speed.</li>' +
      '<li><b>Species</b> — Monarch, Swallowtail, Blue Morpho, Peacock, Painted Lady.</li>' +
      '<li><b>Auto-rotate</b> — toggle a slow turntable (off by default).</li>' +
      '<li><b>Drag / pinch</b> — orbit freely and zoom to inspect.</li>' +
      '<li>Pause on the <b>Caterpillar</b> to see it crawl, or the <b>Imago</b> to see it flap.</li>' +
      '<li>On the <b>Pupa</b>, the translucent chrysalis reveals the imago forming inside — imaginal discs dormant (<i>Stase</i>, S × A) then activated at emergence (<i>Potentialization</i>, A × D × F).</li>' +
      '</ul>';
  }
  buildSidebar();

  const tabButtons = Array.prototype.slice.call(document.querySelectorAll('.tab-btn'));
  const tabPanels = Array.prototype.slice.call(document.querySelectorAll('.tab-panel'));
  tabButtons.forEach(function (btn, i) {
    btn.addEventListener('click', function () {
      tabButtons.forEach(function (b) { b.classList.remove('active'); });
      tabPanels.forEach(function (p) { p.classList.remove('active'); });
      btn.classList.add('active');
      tabPanels[i].classList.add('active');
    });
  });

  // Resizable splitter (DragToAdjust pattern — mousedown, updates --sidebar-w)
  const splitter = document.getElementById('splitter');
  let dragging = false;
  splitter.addEventListener('mousedown', function (e) {
    dragging = true;
    splitter.classList.add('dragging');
    e.preventDefault();
  });
  window.addEventListener('mousemove', function (e) {
    if (!dragging) return;
    let w = window.innerWidth - e.clientX;
    w = Math.max(200, Math.min(600, w));
    document.documentElement.style.setProperty('--sidebar-w', w + 'px');
    engine.resize();
  });
  window.addEventListener('mouseup', function () {
    if (!dragging) return;
    dragging = false;
    splitter.classList.remove('dragging');
    engine.resize();
  });

  // ═══ 9. Init ═══
  syncSpecies();
  syncTimeline();

})();
