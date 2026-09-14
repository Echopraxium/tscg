/* ══════════════════════════════════════════════════════════════
   World 2D Projection — TSCG Poclet simulation
   Author: Echopraxium with the collaboration of Claude AI
   Framework: TSCG (Transdisciplinary System Construction Game)

   Round 1 (interactivity) + Round 2 (pedagogy: coarse continents + Arctic).

   Territory/Map made interactive:
     • BOTTOM panel — 3D globe (BabylonJS) = the TERRITORY (neutral beige +
       recognisable coarse coastlines).
     • TOP panel    — 2D projection (p5.js) = the MAP, coloured by an exact
       area-distortion choropleth on the graticule, with coastlines overlaid so
       the distortion is legible (Greenland balloons on Mercator).

   Selection is by ZONE (continent or polar cap), not by point — click the globe.
   Distortion notation of GenericConcept formulas: × (Territory) · + (Map) · | (Stereopsis).

   Authority: CLIENT of M0_World2DProjection.jsonld (HEAD). Scores, facet values
   and the canonical epistemic gap come from that M0; projection MATHS lives here.
   ══════════════════════════════════════════════════════════════ */
'use strict';

(function () {

  const DEG = Math.PI / 180;

  // ── Constants read from M0 ──────────────────────────────────
  const M0_SCORES = {
    A: 0.55, S: 0.90, F: 0.35, It: 0.85, D: 0.45,
    R: 0.95, E: 0.70, V: 0.90, O: 0.90, Im: 0.85
  };
  const M0_ASFID_MEAN = 0.62;
  const M0_REVOI_MEAN = 0.86;
  const M0_EPISTEMIC_GAP = 0.17;
  const M0_SPECTRAL_CLASS = 'Liminal';

  // ════════════════════════════════════════════════════════════
  // 1. Projections — forward only (lonRad, latRad) -> {x, y}
  // ════════════════════════════════════════════════════════════
  const ROBINSON_X = [1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730,
    0.9600, 0.9427, 0.9216, 0.8962, 0.8679, 0.8350, 0.7986, 0.7597,
    0.7186, 0.6732, 0.6213, 0.5722, 0.5322];
  const ROBINSON_Y = [0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100,
    0.3720, 0.4340, 0.4958, 0.5571, 0.6176, 0.6769, 0.7346, 0.7903,
    0.8435, 0.8936, 0.9394, 0.9761, 1.0000];

  function robinsonLerp(table, absLatDeg) {
    const t = Math.min(absLatDeg, 90) / 5;
    const i = Math.min(Math.floor(t), 17);
    const f = t - i;
    return table[i] * (1 - f) + table[i + 1] * f;
  }

  function mollweideTheta(lat) {
    if (Math.abs(Math.abs(lat) - Math.PI / 2) < 1e-9) return lat > 0 ? Math.PI / 2 : -Math.PI / 2;
    let th = lat;
    for (let n = 0; n < 12; n++) {
      const dth = -(2 * th + Math.sin(2 * th) - Math.PI * Math.sin(lat)) /
                   (2 + 2 * Math.cos(2 * th));
      th += dth;
      if (Math.abs(dth) < 1e-10) break;
    }
    return th;
  }

  const PROJECTIONS = {
    Mercator: {
      label: 'Mercator', distortion: 'Conformal', graticule: 'Cylindrical', latMax: 85 * DEG,
      fwd: (lon, lat) => ({ x: lon, y: Math.log(Math.tan(Math.PI / 4 + lat / 2)) })
    },
    Mollweide: {
      label: 'Mollweide', distortion: 'EqualArea', graticule: 'Pseudocylindrical', latMax: 90 * DEG,
      fwd: (lon, lat) => {
        const th = mollweideTheta(lat);
        return { x: (2 * Math.SQRT2 / Math.PI) * lon * Math.cos(th), y: Math.SQRT2 * Math.sin(th) };
      }
    },
    AzimuthalEquidistant: {
      label: 'Azimuthal Equidistant', distortion: 'Equidistant', graticule: 'Azimuthal', latMax: 90 * DEG,
      fwd: (lon, lat) => {
        const rho = Math.PI / 2 - lat;
        return { x: rho * Math.sin(lon), y: -rho * Math.cos(lon) };
      }
    },
    Robinson: {
      label: 'Robinson', distortion: 'Compromise', graticule: 'Pseudocylindrical', latMax: 90 * DEG,
      fwd: (lon, lat) => {
        const latDeg = Math.abs(lat) / DEG;
        const X = robinsonLerp(ROBINSON_X, latDeg);
        const Y = robinsonLerp(ROBINSON_Y, latDeg) * (lat < 0 ? -1 : 1);
        return { x: 0.8487 * X * lon, y: 1.3523 * Y };
      }
    },
    GallPeters: {
      label: 'Gall-Peters', distortion: 'EqualArea', graticule: 'Cylindrical', latMax: 90 * DEG,
      fwd: (lon, lat) => ({ x: lon / Math.SQRT2, y: Math.SQRT2 * Math.sin(lat) })
    }
  };
  const PROJ_ORDER = ['Mercator', 'Mollweide', 'AzimuthalEquidistant', 'Robinson', 'GallPeters'];

  function projectClamped(proj, lon, lat) {
    const lm = proj.latMax;
    return proj.fwd(lon, Math.max(-lm, Math.min(lm, lat)));
  }

  // ════════════════════════════════════════════════════════════
  // 2. Exact geometry — sphere area, projected area, Tissot, spherical polygon
  // ════════════════════════════════════════════════════════════
  function sphereCellArea(lat0, lat1, lon0, lon1) {
    return Math.abs((lon1 - lon0) * (Math.sin(lat1) - Math.sin(lat0)));
  }

  function projQuadArea(proj, lat0, lat1, lon0, lon1) {
    const K = 4;
    const pts = [];
    for (let n = 0; n < K; n++) { const t = n / K; pts.push(projectClamped(proj, lon0 + (lon1 - lon0) * t, lat0)); }
    for (let n = 0; n < K; n++) { const t = n / K; pts.push(projectClamped(proj, lon1, lat0 + (lat1 - lat0) * t)); }
    for (let n = 0; n < K; n++) { const t = n / K; pts.push(projectClamped(proj, lon1 + (lon0 - lon1) * t, lat1)); }
    for (let n = 0; n < K; n++) { const t = n / K; pts.push(projectClamped(proj, lon0, lat1 + (lat0 - lat1) * t)); }
    let a = 0;
    const m = pts.length;
    for (let i = 0; i < m; i++) { const j = (i + 1) % m; a += pts[i].x * pts[j].y - pts[j].x * pts[i].y; }
    return Math.abs(a) / 2;
  }

  function tissot(proj, lon, lat) {
    const eps = 1e-4;
    const latC = Math.max(-89 * DEG, Math.min(89 * DEG, lat));
    const P = projectClamped(proj, lon, latC);
    const Plon = projectClamped(proj, lon + eps, latC);
    const Plat = projectClamped(proj, lon, latC + eps);
    const dXl = (Plon.x - P.x) / eps, dYl = (Plon.y - P.y) / eps;
    const dXp = (Plat.x - P.x) / eps, dYp = (Plat.y - P.y) / eps;
    const cosLat = Math.cos(latC) || 1e-6;
    const h = Math.sqrt(dXp * dXp + dYp * dYp);
    const k = Math.sqrt(dXl * dXl + dYl * dYl) / cosLat;
    const s = Math.abs(dXl * dYp - dYl * dXp) / cosLat;
    const sumSq = h * h + k * k;
    const A = Math.sqrt(Math.max(0, sumSq + 2 * s));
    const B = Math.sqrt(Math.max(0, sumSq - 2 * s));
    const a = (A + B) / 2, b = (A - B) / 2;
    return { areaFactor: s, anisotropy: b > 1e-9 ? a / b : 999 };
  }

  // Chamberlain-Duquette spherical polygon area (unit sphere), pts in radians [[lon,lat],...].
  function sphericalPolygonArea(pts) {
    let sum = 0;
    for (let i = 0; i < pts.length; i++) {
      const j = (i + 1) % pts.length;
      sum += (pts[j][0] - pts[i][0]) * (2 + Math.sin(pts[i][1]) + Math.sin(pts[j][1]));
    }
    return Math.abs(sum) / 2;
  }
  function capArea(capLatRad) { return 2 * Math.PI * (1 - Math.sin(Math.abs(capLatRad))); }

  // Shoelace area of a projected closed ring (pts already {x,y}).
  function ringArea(pts) {
    let a = 0;
    for (let i = 0; i < pts.length; i++) { const j = (i + 1) % pts.length; a += pts[i].x * pts[j].y - pts[j].x * pts[i].y; }
    return Math.abs(a) / 2;
  }

  // ════════════════════════════════════════════════════════════
  // 3. Zones (Round 2) — coarse continents + polar caps (simulation data, not M0)
  //    Coordinates are deliberately low-res, hand-simplified, public-domain.
  // ════════════════════════════════════════════════════════════
  const CONTINENTS = {
    Greenland: [[-45, 83], [-20, 80], [-15, 76], [-20, 70], [-43, 60], [-55, 64], [-73, 78], [-60, 82]],
    Africa: [[-17, 15], [10, 37], [32, 31], [43, 11], [51, 12], [40, -5], [35, -20], [20, -35], [12, -6], [8, 4], [-8, 4]],
    Australia: [[113, -22], [122, -18], [130, -12], [142, -11], [150, -22], [153, -28], [147, -38], [130, -32], [115, -35], [113, -26]],
    SouthAmerica: [[-80, 8], [-60, 10], [-50, 0], [-35, -8], [-40, -23], [-58, -35], [-65, -45], [-72, -52], [-75, -45], [-70, -18], [-81, -6]],
    NorthAmerica: [[-168, 66], [-140, 70], [-125, 70], [-95, 72], [-80, 68], [-60, 50], [-70, 42], [-80, 25], [-97, 18], [-105, 23], [-117, 32], [-125, 40], [-140, 60]],
    Eurasia: [[-10, 36], [0, 43], [10, 55], [30, 70], [70, 73], [105, 78], [140, 73], [160, 68], [140, 55], [135, 45], [122, 40], [120, 25], [105, 10], [95, 5], [80, 8], [72, 20], [57, 25], [45, 40], [28, 36], [10, 38]]
  };
  const CONTINENT_ORDER = ['Greenland', 'Africa', 'Eurasia', 'NorthAmerica', 'SouthAmerica', 'Australia'];
  const CAPS = { Arctic: 66.5, Antarctic: -66.5 };

  function contRad(name) { return CONTINENTS[name].map(p => [p[0] * DEG, p[1] * DEG]); }
  function capRing(latDeg) {
    const pts = [];
    for (let lon = -180; lon <= 180; lon += 10) pts.push([lon * DEG, latDeg * DEG]);
    return pts;
  }

  function pointInPoly(lonDeg, latDeg, poly) {
    let inside = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
      if (((yi > latDeg) !== (yj > latDeg)) &&
          (lonDeg < (xj - xi) * (latDeg - yi) / (yj - yi) + xi)) inside = !inside;
    }
    return inside;
  }

  function zoneAtLatLon(latRad, lonRad) {
    const latDeg = latRad / DEG, lonDeg = lonRad / DEG;
    if (latDeg >= CAPS.Arctic) return { kind: 'cap', name: 'Arctic' };
    if (latDeg <= CAPS.Antarctic) return { kind: 'cap', name: 'Antarctic' };
    for (const n of CONTINENT_ORDER) if (pointInPoly(lonDeg, latDeg, CONTINENTS[n])) return { kind: 'cont', name: n };
    return null;
  }

  // ════════════════════════════════════════════════════════════
  // 4. Graticule grid + per-projection precomputation
  // ════════════════════════════════════════════════════════════
  const state = {
    stepDeg: 15, tau: 0.10, hueMode: 'auto', current: 'Mercator',
    showCoast: true,
    nLat: 0, nLon: 0, latEdges: [], lonEdges: [], cache: {},
    morphing: false, morphT: 1, morphFrom: 'Mercator', morphTo: 'Mercator', morphStart: 0,
    selection: null   // {kind:'cell',i,j} | {kind:'cont',name} | {kind:'cap',name}
  };

  function buildGrid() {
    const step = state.stepDeg;
    const latEdges = [], lonEdges = [];
    for (let d = -90; d <= 90 + 1e-6; d += step) latEdges.push(Math.max(-90, Math.min(90, d)) * DEG);
    for (let d = -180; d <= 180 + 1e-6; d += step) lonEdges.push(d * DEG);
    state.latEdges = latEdges; state.lonEdges = lonEdges;
    state.nLat = latEdges.length; state.nLon = lonEdges.length;
    state.cache = {};
    for (const key of PROJ_ORDER) precomputeProjection(key);
  }

  function precomputeProjection(key) {
    const proj = PROJECTIONS[key];
    const { nLat, nLon, latEdges, lonEdges } = state;
    const vx = new Float64Array(nLat * nLon);
    const vy = new Float64Array(nLat * nLon);
    for (let i = 0; i < nLat; i++)
      for (let j = 0; j < nLon; j++) {
        const p = projectClamped(proj, lonEdges[j], latEdges[i]);
        vx[i * nLon + j] = p.x; vy[i * nLon + j] = p.y;
      }
    const nCells = (nLat - 1) * (nLon - 1);
    const rRaw = new Float64Array(nCells);
    const shape = new Float64Array(nCells);
    let sumMap = 0, sumSphere = 0, c = 0;
    for (let i = 0; i < nLat - 1; i++)
      for (let j = 0; j < nLon - 1; j++) {
        const aS = sphereCellArea(latEdges[i], latEdges[i + 1], lonEdges[j], lonEdges[j + 1]);
        const aM = projQuadArea(proj, latEdges[i], latEdges[i + 1], lonEdges[j], lonEdges[j + 1]);
        rRaw[c] = aS > 1e-12 ? aM / aS : 1;
        sumMap += aM; sumSphere += aS;
        shape[c] = tissot(proj, (lonEdges[j] + lonEdges[j + 1]) / 2, (latEdges[i] + latEdges[i + 1]) / 2).anisotropy;
        c++;
      }
    const globalScale = sumMap > 1e-12 ? sumSphere / sumMap : 1;
    const rNorm = new Float64Array(nCells);
    for (let n = 0; n < nCells; n++) rNorm[n] = rRaw[n] * globalScale;
    state.cache[key] = { vx, vy, rNorm, shape, globalScale };
  }

  function activeKey() { return state.morphing ? state.morphTo : state.current; }
  function activeIsEqualArea() { return PROJECTIONS[activeKey()].distortion === 'EqualArea'; }
  function effectiveHueMode() {
    if (state.hueMode !== 'auto') return state.hueMode;
    return activeIsEqualArea() ? 'shape' : 'area';
  }

  // raw projected position (lerped during morph), lon/lat in radians
  function rawProj(lon, lat) {
    if (!state.morphing) return projectClamped(PROJECTIONS[state.current], lon, lat);
    const a = projectClamped(PROJECTIONS[state.morphFrom], lon, lat);
    const b = projectClamped(PROJECTIONS[state.morphTo], lon, lat);
    const t = state.morphT;
    return { x: a.x * (1 - t) + b.x * t, y: a.y * (1 - t) + b.y * t };
  }

  // ════════════════════════════════════════════════════════════
  // 5. Colour grammar
  // ════════════════════════════════════════════════════════════
  const COL_NEUT = [207, 210, 214];
  const COL_OVER = [214, 31, 154];
  const COL_UNDER = [23, 182, 214];
  const AREA_DMAX = Math.log(8);
  const SHAPE_DMAX = Math.log(4);

  function lerpCol(g, t, tgt) {
    const u = Math.max(0, Math.min(1, t));
    return [Math.round(g[0] + (tgt[0] - g[0]) * u),
            Math.round(g[1] + (tgt[1] - g[1]) * u),
            Math.round(g[2] + (tgt[2] - g[2]) * u)];
  }
  function areaColour(rNorm) {
    const tau = state.tau;
    if (rNorm > 1 + tau) return lerpCol(COL_NEUT, (Math.log(rNorm) - Math.log(1 + tau)) / AREA_DMAX, COL_OVER);
    if (rNorm < 1 - tau) return lerpCol(COL_NEUT, (Math.log(1 - tau) - Math.log(Math.max(1e-6, rNorm))) / AREA_DMAX, COL_UNDER);
    return COL_NEUT.slice();
  }
  function shapeColour(ab) {
    const tau = state.tau;
    if (ab > 1 + tau) return lerpCol(COL_NEUT, (Math.log(ab) - Math.log(1 + tau)) / SHAPE_DMAX, COL_OVER);
    return COL_NEUT.slice();
  }

  // ════════════════════════════════════════════════════════════
  // 6. MAP panel — p5.js (instance mode)
  // ════════════════════════════════════════════════════════════
  let p5map = null;

  function vpos(idx) {
    if (!state.morphing) { const C = state.cache[state.current]; return { x: C.vx[idx], y: C.vy[idx] }; }
    const A = state.cache[state.morphFrom], B = state.cache[state.morphTo], t = state.morphT;
    return { x: A.vx[idx] * (1 - t) + B.vx[idx] * t, y: A.vy[idx] * (1 - t) + B.vy[idx] * t };
  }
  function cellValue(cellIdx, mode) {
    const field = mode === 'shape' ? 'shape' : 'rNorm';
    if (!state.morphing) return state.cache[state.current][field][cellIdx];
    const A = state.cache[state.morphFrom], B = state.cache[state.morphTo], t = state.morphT;
    return A[field][cellIdx] * (1 - t) + B[field][cellIdx] * t;
  }

  const mapSketch = (p) => {
    p.setup = function () {
      const host = document.getElementById('panel-map');
      p.createCanvas(host.clientWidth, host.clientHeight).parent(host);
      p.pixelDensity(1);
    };
    p.windowResized = function () {
      const host = document.getElementById('panel-map');
      if (host) p.resizeCanvas(host.clientWidth, host.clientHeight);
    };
    p.draw = function () {
      p.background(11, 15, 22);
      if (!state.nLon) return;
      if (state.morphing) {
        state.morphT = Math.min(1, (performance.now() - state.morphStart) / 700);
        if (state.morphT >= 1) { state.morphing = false; state.current = state.morphTo; updateSelReadout(); }
      }
      const { nLat, nLon } = state;
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      for (let idx = 0; idx < nLat * nLon; idx++) {
        const v = vpos(idx);
        if (v.x < minX) minX = v.x; if (v.x > maxX) maxX = v.x;
        if (v.y < minY) minY = v.y; if (v.y > maxY) maxY = v.y;
      }
      const bw = (maxX - minX) || 1, bh = (maxY - minY) || 1, m = 28;
      const sc = Math.min((p.width - 2 * m) / bw, (p.height - 2 * m) / bh);
      const ox = (p.width - bw * sc) / 2 - minX * sc;
      const oy = (p.height - bh * sc) / 2 + maxY * sc;
      const SX = (x) => ox + x * sc, SY = (y) => oy - y * sc;
      const mode = effectiveHueMode();

      // choropleth cells
      p.noStroke();
      let c = 0;
      for (let i = 0; i < nLat - 1; i++)
        for (let j = 0; j < nLon - 1; j++) {
          const a = vpos(i * nLon + j), b = vpos(i * nLon + (j + 1));
          const d = vpos((i + 1) * nLon + (j + 1)), e = vpos((i + 1) * nLon + j);
          const col = mode === 'shape' ? shapeColour(cellValue(c, mode)) : areaColour(cellValue(c, mode));
          p.fill(col[0], col[1], col[2]);
          p.quad(SX(a.x), SY(a.y), SX(b.x), SY(b.y), SX(d.x), SY(d.y), SX(e.x), SY(e.y));
          c++;
        }

      // graticule
      p.stroke(30, 40, 60, 150); p.strokeWeight(1); p.noFill();
      for (let i = 0; i < nLat; i++) { p.beginShape(); for (let j = 0; j < nLon; j++) { const v = vpos(i * nLon + j); p.vertex(SX(v.x), SY(v.y)); } p.endShape(); }
      for (let j = 0; j < nLon; j++) { p.beginShape(); for (let i = 0; i < nLat; i++) { const v = vpos(i * nLon + j); p.vertex(SX(v.x), SY(v.y)); } p.endShape(); }

      // coastlines (Round 2) — outlines over the choropleth
      if (state.showCoast) {
        p.stroke(20, 24, 34, 220); p.strokeWeight(1.4); p.noFill();
        for (const n of CONTINENT_ORDER) drawRingMap(p, contRad(n), SX, SY, true);
      }

      // selection highlight (thick black)
      drawSelectionMap(p, SX, SY);
    };
  };

  function drawRingMap(p, ptsRad, SX, SY, close) {
    p.beginShape();
    for (const q of ptsRad) { const pr = rawProj(q[0], q[1]); p.vertex(SX(pr.x), SY(pr.y)); }
    p.endShape(close ? p.CLOSE : undefined);
  }

  function selectionRingRad() {
    const s = state.selection;
    if (!s) return null;
    if (s.kind === 'cont') return contRad(s.name);
    if (s.kind === 'cap') return capRing(CAPS[s.name]);
    return null; // cell handled separately
  }

  function drawSelectionMap(p, SX, SY) {
    const s = state.selection;
    if (!s) return;
    p.stroke(0); p.strokeWeight(3.5); p.noFill();
    if (s.kind === 'cell') {
      const { nLon } = state, { i, j } = s;
      if (i < state.nLat - 1 && j < nLon - 1) {
        const a = vpos(i * nLon + j), b = vpos(i * nLon + (j + 1));
        const d = vpos((i + 1) * nLon + (j + 1)), e = vpos((i + 1) * nLon + j);
        p.quad(SX(a.x), SY(a.y), SX(b.x), SY(b.y), SX(d.x), SY(d.y), SX(e.x), SY(e.y));
      }
      return;
    }
    const ring = selectionRingRad();
    if (ring) drawRingMap(p, ring, SX, SY, true);
  }

  // ════════════════════════════════════════════════════════════
  // 7. GLOBE panel — BabylonJS (the Territory)
  // ════════════════════════════════════════════════════════════
  const globe = { engine: null, scene: null, camera: null, root: null, R: 1.6, selLines: null, autoRotate: false, trizAnim: null };

  function llToXyz(lat, lon, r) {
    return new BABYLON.Vector3(r * Math.cos(lat) * Math.cos(lon), r * Math.sin(lat), r * Math.cos(lat) * Math.sin(lon));
  }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  function graticuleLines() {
    const lines = [];
    for (let d = -90; d <= 90; d += state.stepDeg) { const lat = d * DEG, pts = []; for (let a = -180; a <= 180; a += 5) pts.push(llToXyz(lat, a * DEG, globe.R * 1.001)); lines.push(pts); }
    for (let d = -180; d <= 180; d += state.stepDeg) { const lon = d * DEG, pts = []; for (let a = -90; a <= 90; a += 5) pts.push(llToXyz(a * DEG, lon, globe.R * 1.001)); lines.push(pts); }
    return lines;
  }
  function coastLinesGlobe() {
    const lines = [];
    for (const n of CONTINENT_ORDER) {
      const pts = CONTINENTS[n].map(q => llToXyz(q[1] * DEG, q[0] * DEG, globe.R * 1.002));
      pts.push(pts[0]);
      lines.push(pts);
    }
    for (const capName of ['Arctic', 'Antarctic']) {
      const pts = []; for (let lon = -180; lon <= 180; lon += 10) pts.push(llToXyz(CAPS[capName] * DEG, lon * DEG, globe.R * 1.002)); lines.push(pts);
    }
    return lines;
  }

  function buildGlobe() {
    const canvas = document.getElementById('canvas-globe');
    const engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: true });
    const scene = new BABYLON.Scene(engine);
    scene.clearColor = new BABYLON.Color4(0.020, 0.027, 0.047, 1);
    const camera = new BABYLON.ArcRotateCamera('cam', Math.PI / 2, Math.PI / 2.4, 5.2, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, true);
    camera.wheelPrecision = 40; camera.lowerRadiusLimit = 3.2; camera.upperRadiusLimit = 9;
    new BABYLON.HemisphericLight('h', new BABYLON.Vector3(0.4, 1, 0.3), scene);
    const dir = new BABYLON.DirectionalLight('d', new BABYLON.Vector3(-0.6, -0.7, -0.5), scene); dir.intensity = 0.5;

    const root = new BABYLON.TransformNode('globeRoot', scene);
    root.rotationQuaternion = BABYLON.Quaternion.Identity();

    const sphere = BABYLON.MeshBuilder.CreateSphere('earth', { diameter: globe.R * 2, segments: 48 }, scene);
    const mat = new BABYLON.StandardMaterial('beige', scene);
    mat.diffuseColor = new BABYLON.Color3(0.847, 0.780, 0.635);
    mat.specularColor = new BABYLON.Color3(0.08, 0.08, 0.08);
    sphere.material = mat; sphere.parent = root;

    const grat = BABYLON.MeshBuilder.CreateLineSystem('grat', { lines: graticuleLines() }, scene);
    grat.color = new BABYLON.Color3(0.25, 0.22, 0.16); grat.parent = root;

    const coast = BABYLON.MeshBuilder.CreateLineSystem('coast', { lines: coastLinesGlobe() }, scene);
    coast.color = new BABYLON.Color3(0.32, 0.26, 0.16); coast.parent = root;

    globe.engine = engine; globe.scene = scene; globe.camera = camera; globe.root = root;

    scene.onPointerObservable.add((pi) => {
      if (pi.type !== BABYLON.PointerEventTypes.POINTERPICK) return;
      const hit = pi.pickInfo;
      if (!hit || !hit.hit || !hit.pickedPoint) return;
      const local = BABYLON.Vector3.TransformCoordinates(hit.pickedPoint, BABYLON.Matrix.Invert(root.getWorldMatrix()));
      const lat = Math.asin(Math.max(-1, Math.min(1, local.y / globe.R)));
      const lon = Math.atan2(local.z, local.x);
      selectAtLatLon(lat, lon);
    });

    engine.runRenderLoop(() => {
      const now = performance.now();
      if (globe.trizAnim) {
        const t = Math.min(1, (now - globe.trizAnim.start) / globe.trizAnim.dur);
        root.rotationQuaternion = BABYLON.Quaternion.Slerp(globe.trizAnim.q0, globe.trizAnim.q1, ease(t));
        if (t >= 1) globe.trizAnim = null;
      } else if (globe.autoRotate) {
        root.rotationQuaternion = root.rotationQuaternion.multiply(BABYLON.Quaternion.RotationAxis(BABYLON.Axis.Y, 0.0035));
      }
      scene.render();
    });
    window.addEventListener('resize', () => engine.resize());
    TSCG.engine = engine; TSCG.camera = camera;
    const badge = document.getElementById('engine-badge');
    if (badge) badge.textContent = 'engine: BabylonJS ' + (BABYLON.Engine.Version || '');
  }

  function rebuildGlobeGraticule() {
    if (!globe.scene) return;
    const old = globe.scene.getMeshByName('grat'); if (old) old.dispose();
    const grat = BABYLON.MeshBuilder.CreateLineSystem('grat', { lines: graticuleLines() }, globe.scene);
    grat.color = new BABYLON.Color3(0.25, 0.22, 0.16); grat.parent = globe.root;
  }

  function quatFromTo(a, b) {
    a = a.normalizeToNew(); b = b.normalizeToNew();
    const d = BABYLON.Vector3.Dot(a, b);
    if (d > 0.999999) return BABYLON.Quaternion.Identity();
    if (d < -0.999999) {
      let axis = BABYLON.Vector3.Cross(BABYLON.Axis.Y, a);
      if (axis.lengthSquared() < 1e-6) axis = BABYLON.Vector3.Cross(BABYLON.Axis.X, a);
      return BABYLON.Quaternion.RotationAxis(axis.normalize(), Math.PI);
    }
    return BABYLON.Quaternion.RotationAxis(BABYLON.Vector3.Cross(a, b).normalize(), Math.acos(Math.max(-1, Math.min(1, d))));
  }

  function trizTo(lat, lon) {
    const q1 = quatFromTo(llToXyz(lat, lon, 1), globe.camera.position.normalizeToNew());
    globe.trizAnim = { q0: globe.root.rotationQuaternion.clone(), q1, start: performance.now(), dur: 650 };
  }

  function drawGlobeSelection() {
    if (globe.selLines) { globe.selLines.dispose(); globe.selLines = null; }
    const s = state.selection; if (!s) return;
    let pts = [];
    if (s.kind === 'cell') {
      const la0 = state.latEdges[s.i], la1 = state.latEdges[s.i + 1];
      const lo0 = state.lonEdges[s.j], lo1 = state.lonEdges[s.j + 1];
      const N = 12, r = globe.R * 1.004;
      for (let n = 0; n <= N; n++) pts.push(llToXyz(la0, lo0 + (lo1 - lo0) * n / N, r));
      for (let n = 0; n <= N; n++) pts.push(llToXyz(la0 + (la1 - la0) * n / N, lo1, r));
      for (let n = 0; n <= N; n++) pts.push(llToXyz(la1, lo1 + (lo0 - lo1) * n / N, r));
      for (let n = 0; n <= N; n++) pts.push(llToXyz(la1 + (la0 - la1) * n / N, lo0, r));
    } else if (s.kind === 'cont') {
      pts = CONTINENTS[s.name].map(q => llToXyz(q[1] * DEG, q[0] * DEG, globe.R * 1.005)); pts.push(pts[0]);
    } else if (s.kind === 'cap') {
      for (let lon = -180; lon <= 180; lon += 6) pts.push(llToXyz(CAPS[s.name] * DEG, lon * DEG, globe.R * 1.005));
    }
    const sel = BABYLON.MeshBuilder.CreateLines('sel', { points: pts }, globe.scene);
    sel.color = new BABYLON.Color3(0, 0, 0); sel.parent = globe.root; sel.renderingGroupId = 1;
    globe.selLines = sel;
  }

  // ════════════════════════════════════════════════════════════
  // 8. Selection + read-out
  // ════════════════════════════════════════════════════════════
  function selectAtLatLon(lat, lon) {
    const z = zoneAtLatLon(lat, lon);
    if (z) { state.selection = z; }
    else {
      const { latEdges, lonEdges } = state; let i = 0, j = 0;
      for (let k = 0; k < latEdges.length - 1; k++) if (lat >= latEdges[k] && lat < latEdges[k + 1]) { i = k; break; }
      for (let k = 0; k < lonEdges.length - 1; k++) if (lon >= lonEdges[k] && lon < lonEdges[k + 1]) { j = k; break; }
      state.selection = { kind: 'cell', i, j };
    }
    afterSelect();
  }

  function selectZoneByName(name) {
    if (!name) { state.selection = null; }
    else if (CAPS[name] !== undefined) state.selection = { kind: 'cap', name };
    else state.selection = { kind: 'cont', name };
    afterSelect();
  }

  function selectionCentroid() {
    const s = state.selection;
    if (!s) return null;
    if (s.kind === 'cell') return { lat: (state.latEdges[s.i] + state.latEdges[s.i + 1]) / 2, lon: (state.lonEdges[s.j] + state.lonEdges[s.j + 1]) / 2 };
    if (s.kind === 'cap') return { lat: (CAPS[s.name] + (CAPS[s.name] > 0 ? 90 : -90)) / 2 * DEG, lon: 0 };
    let sl = 0, so = 0; const pol = CONTINENTS[s.name];
    for (const q of pol) { so += q[0]; sl += q[1]; }
    return { lat: sl / pol.length * DEG, lon: so / pol.length * DEG };
  }

  function afterSelect() {
    drawGlobeSelection();
    const c = selectionCentroid();
    if (c) trizTo(c.lat, c.lon);
    updateSelReadout();
    const zsel = document.getElementById('zone-select');
    if (zsel) {
      const s = state.selection;
      zsel.value = (s && (s.kind === 'cont' || s.kind === 'cap')) ? s.name : '';
    }
  }

  function selectionDistortion() {
    const s = state.selection; if (!s) return null;
    const proj = PROJECTIONS[activeKey()];
    const gscale = state.cache[activeKey()].globalScale;
    let aSphere, aMap, cLat, cLon;
    if (s.kind === 'cell') {
      aSphere = sphereCellArea(state.latEdges[s.i], state.latEdges[s.i + 1], state.lonEdges[s.j], state.lonEdges[s.j + 1]);
      aMap = projQuadArea(proj, state.latEdges[s.i], state.latEdges[s.i + 1], state.lonEdges[s.j], state.lonEdges[s.j + 1]);
      const cc = selectionCentroid(); cLat = cc.lat; cLon = cc.lon;
    } else {
      const ring = s.kind === 'cont' ? contRad(s.name) : capRing(CAPS[s.name]);
      aSphere = s.kind === 'cap' ? capArea(CAPS[s.name] * DEG) : sphericalPolygonArea(ring);
      aMap = ringArea(ring.map(q => projectClamped(proj, q[0], q[1])));
      const cc = selectionCentroid(); cLat = cc.lat; cLon = cc.lon;
    }
    const rNorm = aSphere > 1e-9 ? (aMap / aSphere) * gscale : 1;
    const ab = tissot(proj, cLon, cLat).anisotropy;
    return { rNorm, ab };
  }

  function zoneLabel() {
    const s = state.selection; if (!s) return '';
    if (s.kind === 'cell') { const c = selectionCentroid(); return 'cell ~(' + (c.lat / DEG).toFixed(0) + '°, ' + (c.lon / DEG).toFixed(0) + '°)'; }
    if (s.kind === 'cap') return s.name + ' cap';
    return s.name;
  }

  function updateSelReadout() {
    const el = document.getElementById('sel-readout'); if (!el) return;
    const d = selectionDistortion();
    if (!d) { el.textContent = ''; return; }
    el.innerHTML = '<b>' + zoneLabel() + '</b> · area ×' + d.rNorm.toFixed(2) + ' · shape a/b ' + d.ab.toFixed(2);
  }

  // ════════════════════════════════════════════════════════════
  // 9. Controls
  // ════════════════════════════════════════════════════════════
  function setProjection(key) {
    if (key === state.current && !state.morphing) return;
    state.morphFrom = state.morphing ? state.morphTo : state.current;
    state.morphTo = key; state.morphT = 0; state.morphing = true; state.morphStart = performance.now();
    updateLegend(); updateSelReadout();
  }

  function updateLegend() {
    const mode = effectiveHueMode();
    const title = document.getElementById('lg-title');
    const note = document.getElementById('lg-note');
    const lo = document.getElementById('lg-lo'), hi = document.getElementById('lg-hi');
    if (mode === 'shape') {
      title.textContent = 'Hue = SHAPE distortion (Tissot a/b)';
      lo.textContent = 'isotropic'; hi.textContent = 'anisotropic';
      note.innerHTML = 'Active projection is <b>equal-area</b>: areas are faithful, so the choropleth ' +
        'switches to <b>shape</b> distortion. Grey = round Tissot circle.';
    } else {
      title.textContent = 'Hue = AREA distortion (log r)';
      lo.textContent = 'undersized'; hi.textContent = 'oversized';
      note.innerHTML = 'Grey = faithful within <b>±τ</b>. Cyan = shrunk, magenta = inflated. ' +
        'τ is a <b>convention of the Map</b>, not a fact of the Territory.';
    }
  }

  function wireControls() {
    const projSel = document.getElementById('proj-select');
    PROJ_ORDER.forEach(k => { const o = document.createElement('option'); o.value = k; o.textContent = PROJECTIONS[k].label; projSel.appendChild(o); });
    projSel.value = state.current;
    projSel.addEventListener('change', e => setProjection(e.target.value));

    const zoneSel = document.getElementById('zone-select');
    const zEmpty = document.createElement('option'); zEmpty.value = ''; zEmpty.textContent = '— none —'; zoneSel.appendChild(zEmpty);
    const zArc = document.createElement('option'); zArc.value = 'Arctic'; zArc.textContent = 'Arctic cap ★'; zoneSel.appendChild(zArc);
    const zAnt = document.createElement('option'); zAnt.value = 'Antarctic'; zAnt.textContent = 'Antarctic cap'; zoneSel.appendChild(zAnt);
    CONTINENT_ORDER.forEach(n => { const o = document.createElement('option'); o.value = n; o.textContent = n.replace(/([A-Z])/g, ' $1').trim(); zoneSel.appendChild(o); });
    zoneSel.addEventListener('change', e => selectZoneByName(e.target.value));

    const arctic = document.getElementById('btn-arctic');
    if (arctic) arctic.addEventListener('click', () => selectZoneByName('Arctic'));

    const tau = document.getElementById('tau-slider'), tauVal = document.getElementById('tau-val');
    tau.addEventListener('input', e => { state.tau = parseInt(e.target.value, 10) / 100; tauVal.textContent = state.tau.toFixed(2); updateSelReadout(); });

    document.getElementById('hue-select').addEventListener('change', e => { state.hueMode = e.target.value; updateLegend(); });

    document.getElementById('dens-select').addEventListener('change', e => {
      state.stepDeg = parseInt(e.target.value, 10);
      if (state.selection && state.selection.kind === 'cell') { state.selection = null; if (globe.selLines) { globe.selLines.dispose(); globe.selLines = null; } }
      buildGrid(); rebuildGlobeGraticule(); updateSelReadout();
    });

    const coastBtn = document.getElementById('btn-coast');
    coastBtn.classList.toggle('on', state.showCoast);
    coastBtn.addEventListener('click', () => { state.showCoast = !state.showCoast; coastBtn.classList.toggle('on', state.showCoast); const c = globe.scene && globe.scene.getMeshByName('coast'); if (c) c.setEnabled(state.showCoast); });

    const auto = document.getElementById('btn-autorotate');
    auto.addEventListener('click', () => { globe.autoRotate = !globe.autoRotate; auto.classList.toggle('on', globe.autoRotate); });

    document.getElementById('btn-reset').addEventListener('click', resetAll);
    const diagBtn = document.getElementById('btn-diag');
    if (diagBtn) diagBtn.addEventListener('click', function () { TSCG.toggleDiag(); this.classList.toggle('on'); });
  }

  function resetAll() {
    state.selection = null; state.hueMode = 'auto'; state.tau = 0.10; state.showCoast = true;
    if (globe.selLines) { globe.selLines.dispose(); globe.selLines = null; }
    if (globe.root) globe.root.rotationQuaternion = BABYLON.Quaternion.Identity();
    globe.autoRotate = false;
    const coast = globe.scene && globe.scene.getMeshByName('coast'); if (coast) coast.setEnabled(true);
    const auto = document.getElementById('btn-autorotate'); if (auto) auto.classList.remove('on');
    const coastBtn = document.getElementById('btn-coast'); if (coastBtn) coastBtn.classList.add('on');
    document.getElementById('tau-slider').value = 10; document.getElementById('tau-val').textContent = '0.10';
    document.getElementById('hue-select').value = 'auto';
    document.getElementById('zone-select').value = '';
    setProjection('Mercator'); updateSelReadout();
  }

  // ════════════════════════════════════════════════════════════
  // 10. Sidebar — canonical scores (M0) + M2 concepts
  // ════════════════════════════════════════════════════════════
  const DIM_COLOR = { A: '#f78166', S: '#56d364', F: '#79c0ff', It: '#d2a8ff', D: '#e3b341', R: '#79c0ff', E: '#56d364', V: '#f78166', O: '#d2a8ff', Im: '#e3b341' };

  function renderCanonicalScores(hostId) {
    const host = document.getElementById(hostId); if (!host) return;
    const row = (d, v) =>
      '<div class="score-row"><span class="score-dim" style="color:' + DIM_COLOR[d] + '">' + d + '</span>' +
      '<div class="score-bar-bg"><div class="score-bar-fill" style="width:' + (v * 100).toFixed(0) + '%;background:' + DIM_COLOR[d] + '"></div></div>' +
      '<span class="score-val">' + v.toFixed(2) + '</span></div>';
    const asfid = ['A', 'S', 'F', 'It', 'D'], revoi = ['R', 'E', 'V', 'O', 'Im'];
    host.innerHTML =
      '<div class="score-group"><div class="score-group-label eagle">ASFID — Territory (Eagle Eye)</div>' +
      asfid.map(d => row(d, M0_SCORES[d])).join('') + '<div class="score-mean">mean = <b>' + M0_ASFID_MEAN.toFixed(2) + '</b></div></div>' +
      '<div class="score-group"><div class="score-group-label sphinx">REVOI — Map (Sphinx Eye)</div>' +
      revoi.map(d => row(d, M0_SCORES[d])).join('') + '<div class="score-mean">mean = <b>' + M0_REVOI_MEAN.toFixed(2) + '</b></div></div>' +
      '<div class="gap-badge"><div class="gap-label">Epistemic Gap δ₁ (canonical, from M0)</div>' +
      '<div class="gap-val">' + M0_EPISTEMIC_GAP.toFixed(2) + '</div>' +
      '<div class="gap-desc"><b>' + M0_SPECTRAL_CLASS + '</b> — |ASFID − REVOI| / √2. ' +
      'Not a defect: the gap is a <b>theorem</b> (Gauss, Theorema Egregium) — no flat map can equal the sphere.</div></div>';
  }

  function renderConceptsList() {
    TSCG.renderConcepts('concepts-host', [
      { name: 'Representation', formula: 'It × St', family: 'Epistemics', familyColor: '#d2a8ff', desc: 'A projection is a representation of the globe.', role: 'The map itself.' },
      { name: 'Constraint', formula: 'St × A × D | O + V', family: 'Epistemics', familyColor: '#d2a8ff', desc: 'Theorema Egregium: the irreducible trade-off.', role: 'No lossless projection exists.' },
      { name: 'Invariant', formula: 'St × A', family: 'Epistemics', familyColor: '#d2a8ff', desc: 'Each projection preserves one metric invariant (or none).', role: 'Angle / area / distance.' },
      { name: 'Modelisation', formula: 'D × F × It | R + V + E', family: 'Epistemics', familyColor: '#d2a8ff', desc: 'The map as a knowable model of an un-fully-knowable Territory.', role: 'Map-as-model.' },
      { name: 'Signature', formula: 'It × Ss | V', family: 'Measurement', familyColor: '#56d364', desc: "Tissot's indicatrix — the local distortion signature.", role: 'Per-point distortion.' },
      { name: 'Gradient', formula: 'It × T', family: 'Measurement', familyColor: '#56d364', desc: 'Distortion grows with latitude / radius.', role: 'Mercator poles, azimuthal rim.' },
      { name: 'Polarity', formula: 'St × It × A', family: 'Measurement', familyColor: '#56d364', desc: 'Over- vs under-sized area.', role: 'The diverging choropleth.' },
      { name: 'Symmetry', formula: 'St', family: 'Structure', familyColor: '#79c0ff', desc: 'The graticule symmetry of each family.', role: 'Construction skeleton.' },
      { name: 'Topology', formula: 'St | L', family: 'Structure', familyColor: '#79c0ff', desc: 'Sphere vs plane — the un-preservable relation.', role: 'Genus mismatch.' },
      { name: 'Space', formula: 'St | L', family: 'Structure', familyColor: '#79c0ff', desc: 'Maps sphere-space onto plane-space.', role: 'The projection domain.' },
      { name: 'Observer', formula: 'It × A', family: 'Perspective', familyColor: '#f78166', desc: 'Which invariant to keep is an observer choice.', role: 'Map-side decision.' }
    ]);
  }

  // ════════════════════════════════════════════════════════════
  // 11. Init
  // ════════════════════════════════════════════════════════════
  function init() {
    try {
      TSCG.pocletId = 'World2DProjection';
      TSCG.initSplitter();
      buildGrid();
      buildGlobe();
      p5map = new p5(mapSketch);
      wireControls();
      renderCanonicalScores('scores-host');
      renderConceptsList();
      updateLegend();
      const host = document.getElementById('panel-map');
      if (window.ResizeObserver && host) new ResizeObserver(() => { if (p5map) p5map.windowResized(); }).observe(host);
      const gpanel = document.getElementById('panel-globe');
      if (window.ResizeObserver && gpanel && globe.engine) new ResizeObserver(() => globe.engine.resize()).observe(gpanel);
      TSCG.ok('World2DProjection ready — ' + (state.nLat - 1) * (state.nLon - 1) + ' cells · ' + CONTINENT_ORDER.length + ' continents');
    } catch (err) {
      TSCG.fail('Init', err && err.message ? err.message : String(err));
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

})();
