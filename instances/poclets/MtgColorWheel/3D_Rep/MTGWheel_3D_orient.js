/**
 * MTGWheel_3D.js
 * Magic: The Gathering Color Wheel — Three.js r128
 *
 * Usage: include this script in an HTML page that already loads Three.js r128.
 * The script expects a <canvas id="c"> inside a <div id="wrap"> in the DOM.
 *
 * <div id="wrap" style="width:100%;height:540px;background:#000;">
 *   <canvas id="c" style="width:100%;height:100%;display:block;"></canvas>
 * </div>
 * <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
 * <script src="MTGWheel_3D.js"></script>
 */

(function () {

  // ─── DOM setup ────────────────────────────────────────────────────────────
  const wrap   = document.getElementById('wrap');
  const canvas = document.getElementById('c');
  const W = wrap.clientWidth || 680;
  const H = wrap.clientHeight || 540;
  canvas.width  = W * devicePixelRatio;
  canvas.height = H * devicePixelRatio;

  // ─── Renderer ─────────────────────────────────────────────────────────────
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 1);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);

  // ─── Camera ───────────────────────────────────────────────────────────────
  const camera = new THREE.PerspectiveCamera(42, W / H, 0.1, 100);
  camera.position.set(0, 1.4, 5.5);
  camera.lookAt(0, 0, 0);

  // ─── Lights ───────────────────────────────────────────────────────────────
  scene.add(new THREE.AmbientLight(0xffffff, 0.7));
  const sun = new THREE.DirectionalLight(0xfffaf0, 0.85);
  sun.position.set(4, 6, 5);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0xd0d8ff, 0.4);
  fill.position.set(-5, 2, -4);
  scene.add(fill);

  // ─── Mana colors ──────────────────────────────────────────────────────────
  // Note: K is used for Black to avoid confusion with Blue (B)
  const MANA = [
    { name: 'White', letter: 'W', hex: '#C8A87A' },
    { name: 'Blue',  letter: 'B', hex: '#3A7FD5' },
    { name: 'Black', letter: 'K', hex: '#2A1F28' },
    { name: 'Red',   letter: 'R', hex: '#C82020' },
    { name: 'Green', letter: 'G', hex: '#1A7A40' },
  ];
  const n = 5;

  // ─── Geometry constants ───────────────────────────────────────────────────
  const R1      = 1.5;    // pentagon radius
  const Y1      = -0.45;  // wheel plane Y
  const Y2      = 0.45;
  const Ymid    = (Y1 + Y2) / 2;

  // Sphere sizes
  const S_PRIMARY = 0.23 * 1.08 * 1.05;   // primaries  ≈ 0.260
  const S_BICOLOR = 0.23 * 0.85 * 0.91 * 0.91; // bicolor ≈ 0.160
  const S_DOD     = 0.22 * 0.85;           // dodecahedron ≈ 0.187

  // Tube radii
  const R_ARC  = 0.035;
  const R_DIAG = 0.028;

  // ─── Color utilities ──────────────────────────────────────────────────────
  function hexToRGB(h) {
    return {
      r: parseInt(h.slice(1, 3), 16) / 255,
      g: parseInt(h.slice(3, 5), 16) / 255,
      b: parseInt(h.slice(5, 7), 16) / 255,
    };
  }

  function luminance(hex) {
    const c = hexToRGB(hex);
    return 0.299 * c.r + 0.587 * c.g + 0.114 * c.b;
  }

  // Contrast: dark edge on light colors, white edge on dark colors
  function edgeColor(hex) {
    return luminance(hex) > 0.45 ? 0x000000 : 0xffffff;
  }

  // ─── Arc curve (circular arc in XZ plane at fixed Y) ──────────────────────
  class ArcCurve extends THREE.Curve {
    constructor(R, Y, a0, a1) {
      super();
      this.R = R; this.Y = Y; this.a0 = a0; this.a1 = a1;
    }
    getPoint(t) {
      const a = this.a0 + t * (this.a1 - this.a0);
      return new THREE.Vector3(Math.cos(a) * this.R, this.Y, Math.sin(a) * this.R);
    }
  }

  // ─── Split arc tube (two colored halves along an arc) ────────────────────
  function makeSplitArcTube(R, Y, a0, a1, hex1, hex2, tubeR, grp) {
    const mid = (a0 + a1) / 2;
    [hex1, hex2].forEach((hex, k) => {
      const curve = new ArcCurve(R, Y, k === 0 ? a0 : mid, k === 0 ? mid : a1);
      const geo   = new THREE.TubeGeometry(curve, 30, tubeR, 10, false);
      const col   = hexToRGB(hex);
      const mesh  = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({
        color: new THREE.Color(col.r, col.g, col.b),
      }));
      mesh.add(new THREE.LineSegments(
        new THREE.EdgesGeometry(geo),
        new THREE.LineBasicMaterial({ color: edgeColor(hex), transparent: true, opacity: 0.35 }),
      ));
      grp.add(mesh);
    });
  }

  // ─── Split straight tube (two colored halves along a line) ───────────────
  function makeSplitStraightTube(pA, pB, hex1, hex2, tubeR, grp) {
    const mid = new THREE.Vector3().addVectors(pA, pB).multiplyScalar(0.5);
    [[pA, mid, hex1], [mid, pB, hex2]].forEach(([start, end, hex]) => {
      const geo  = new THREE.TubeGeometry(new THREE.LineCurve3(start, end), 8, tubeR, 10, false);
      const col  = hexToRGB(hex);
      const mesh = new THREE.Mesh(geo, new THREE.MeshLambertMaterial({
        color: new THREE.Color(col.r, col.g, col.b),
      }));
      mesh.add(new THREE.LineSegments(
        new THREE.EdgesGeometry(geo),
        new THREE.LineBasicMaterial({ color: edgeColor(hex), transparent: true, opacity: 0.35 }),
      ));
      grp.add(mesh);
    });
  }

  // ─── Solid sphere (primary mana color) ───────────────────────────────────
  function makeSolidSphere(pos, hex, r) {
    const col  = hexToRGB(hex);
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(r, 32, 20),
      new THREE.MeshLambertMaterial({ color: new THREE.Color(col.r, col.g, col.b) }),
    );
    mesh.position.copy(pos);
    return mesh;
  }

  // ─── Split sphere texture (left = hex1, right = hex2) ────────────────────
  function makeSplitTex(hex1, hex2) {
    const cv  = document.createElement('canvas');
    cv.width  = 256; cv.height = 128;
    const ctx = cv.getContext('2d');
    ctx.fillStyle = hex1; ctx.fillRect(0,   0, 128, 128);
    ctx.fillStyle = hex2; ctx.fillRect(128, 0, 128, 128);
    return new THREE.CanvasTexture(cv);
  }

  // ─── Split sphere (bicolor)
  //   dirXZ: direction from parent2 → parent1 (the connecting axis)
  //   +PI/2 makes the seam perpendicular to that axis ─────────────────────
  function makeSplitSphere(pos, hex1, hex2, r, dirXZ) {
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(r, 48, 32),
      new THREE.MeshLambertMaterial({ map: makeSplitTex(hex1, hex2) }),
    );
    mesh.position.copy(pos);
    if (dirXZ) {
      const dx = dirXZ.x, dz = dirXZ.z;
      const l  = Math.sqrt(dx * dx + dz * dz);
      if (l > 0.0001) mesh.rotation.y = Math.atan2(-dz / l, dx / l) + Math.PI / 2;
    }
    return mesh;
  }

  // ─── Pentagon helpers ─────────────────────────────────────────────────────
  function pentaAngles() {
    return Array.from({ length: n }, (_, i) => (2 * Math.PI * i / n) - Math.PI / 2);
  }

  function pentaPoints(R, Y) {
    return pentaAngles().map(a => new THREE.Vector3(Math.cos(a) * R, Y, Math.sin(a) * R));
  }

  // ─── Build scene ──────────────────────────────────────────────────────────
  const angV = pentaAngles();
  const p1   = pentaPoints(R1, Y1);
  const grp  = new THREE.Group();

  // 1. Arc tubes — 5 adjacent pairs
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    let a0 = angV[i], a1 = angV[j];
    if (a1 < a0) a1 += 2 * Math.PI;
    makeSplitArcTube(R1, Y1, a0, a1, MANA[i].hex, MANA[j].hex, R_ARC, grp);
  }

  // 2. Straight tubes — 5 diagonal pairs
  for (let i = 0; i < n; i++) {
    const k = (i + 2) % n;
    makeSplitStraightTube(p1[i], p1[k], MANA[i].hex, MANA[k].hex, R_DIAG, grp);
  }

  // 3. Bicolor spheres at arc midpoints (adjacent pairs)
  for (let i = 0; i < n; i++) {
    const j = (i + 1) % n;
    let a0 = angV[i], a1 = angV[j];
    if (a1 < a0) a1 += 2 * Math.PI;
    const amid = (a0 + a1) / 2;
    const pos  = new THREE.Vector3(Math.cos(amid) * R1, Y1, Math.sin(amid) * R1);
    const dir  = new THREE.Vector3(p1[i].x - p1[j].x, 0, p1[i].z - p1[j].z);
    grp.add(makeSplitSphere(pos, MANA[i].hex, MANA[j].hex, S_BICOLOR, dir));
  }

  // 4. Bicolor spheres at diagonal midpoints
  for (let i = 0; i < n; i++) {
    const k   = (i + 2) % n;
    const pos = new THREE.Vector3().addVectors(p1[i], p1[k]).multiplyScalar(0.5);
    const dir = new THREE.Vector3(p1[i].x - p1[k].x, 0, p1[i].z - p1[k].z);
    grp.add(makeSplitSphere(pos, MANA[i].hex, MANA[k].hex, S_BICOLOR, dir));
  }

  // 5. Primary solid spheres (rendered last → drawn on top)
  for (let i = 0; i < n; i++) {
    grp.add(makeSolidSphere(p1[i], MANA[i].hex, S_PRIMARY));
  }

  // 6. Central dodecahedron — Artifact pseudo-color
  const dodGeo = new THREE.DodecahedronGeometry(S_DOD);
  const dod    = new THREE.Mesh(dodGeo, new THREE.MeshLambertMaterial({ color: 0xe8e4d8 }));
  dod.position.set(0, Y1, 0); // in the wheel plane, at center
  dod.add(new THREE.LineSegments(
    new THREE.EdgesGeometry(dodGeo),
    new THREE.LineBasicMaterial({ color: 0x555555 }),
  ));
  grp.add(dod);

  // Center group so rotation.x pivots around the geometric midpoint
  grp.position.y = -Ymid;
  grp.rotation.x = 0.25;
  scene.add(grp);

  // ─── Mouse / touch drag rotation ─────────────────────────────────────────
  let drag = false, lx = 0, ly = 0;

  canvas.addEventListener('mousedown', e => {
    drag = true; lx = e.clientX; ly = e.clientY;
    canvas.style.cursor = 'grabbing';
  });
  window.addEventListener('mouseup', () => {
    drag = false; canvas.style.cursor = 'grab';
  });
  window.addEventListener('mousemove', e => {
    if (!drag) return;
    grp.rotation.y += (e.clientX - lx) * 0.004;
    grp.rotation.x += (e.clientY - ly) * 0.004;
    lx = e.clientX; ly = e.clientY;
  });
  canvas.addEventListener('touchstart', e => {
    drag = true; lx = e.touches[0].clientX; ly = e.touches[0].clientY;
  }, { passive: true });
  canvas.addEventListener('touchend', () => { drag = false; });
  canvas.addEventListener('touchmove', e => {
    grp.rotation.y += (e.touches[0].clientX - lx) * 0.004;
    grp.rotation.x += (e.touches[0].clientY - ly) * 0.004;
    lx = e.touches[0].clientX; ly = e.touches[0].clientY;
  }, { passive: true });

  // ─── Render loop ──────────────────────────────────────────────────────────
  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }
  animate();

})();
