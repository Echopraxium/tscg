/* ══════════════════════════════════════════════════════════════
   QRCodeToPocketCity — CORE LAYER
   Author: Echopraxium with the collaboration of Claude AI
   Version: 1.0.0
   Engine: BabylonJS 6.x

   Reads DATA (the QR matrix) and STYLE (QRCITY_STYLESHEETS) and
   builds the city. CORE never hardcodes an appearance value.

   THE BINDING CONSTRAINT
   ──────────────────────
   Seen orthographically from directly above, the city must still
   be a scannable QR code. A dark module stays predominantly dark
   from above; a light module stays predominantly light. Every
   geometric decision below serves that rule — which is why the
   Bird's-eye camera is orthographic, roofs are flat and dark,
   chimney caps match the roof exactly, and signs are vertical.
   ══════════════════════════════════════════════════════════════ */
'use strict';

// Shown in the header and the diagnostic log, so a cached or stale copy is
// identifiable without guesswork.
const BUILD = 'v2.2';

/* ═══════════════ 1. DETERMINISM ═══════════════ */
// Mulberry32: same seed, same city — always, across sessions.
function makePRNG(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s + 0x6D2B79F5) >>> 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function textToSeed(str) {
  let h = 5381;
  for (let i = 0; i < str.length; i++) h = (h * 33 ^ str.charCodeAt(i)) >>> 0;
  return h;
}
function hashStr(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
async function sha256Seed(n) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(String(n)));
  return new Uint32Array(buf)[0];
}

/* ═══════════════ 2. DATA — QR MATRIX ═══════════════ */
// QR sizes are fixed by ISO/IEC 18004 at 21 + 4(version-1):
// 21, 25, 29, 33, 37, 41, 45, 49. There is no 32 or 48.
function sizeToVersion(n) { return (n - 21) / 4 + 1; }

function toMatrix(qr) {
  const n = qr.getModuleCount();
  return { n, mat: Array.from({ length: n }, (_, r) =>
    Array.from({ length: n }, (_, c) => qr.isDark(r, c) ? 1 : 0)) };
}
function extractQR(text, forcedN) {
  if (forcedN) {
    for (let v = sizeToVersion(forcedN); v <= 8; v++) {
      for (const ecc of ['H','Q','M','L']) {
        try { const q = qrcode(v, ecc); q.addData(text); q.make(); return toMatrix(q); }
        catch (e) { /* try next */ }
      }
    }
  }
  for (const ecc of ['M','L']) {
    try {
      const q = qrcode(0, ecc); q.addData(text); q.make();
      if (q.getModuleCount() <= 49) return toMatrix(q);
    } catch (e) {}
  }
  try { const q = qrcode(8, 'L'); q.addData(text.slice(0, 120)); q.make(); return toMatrix(q); }
  catch (e) { return null; }
}
function finderCorners(n) {
  return [{ r:0, c:0, idx:0 }, { r:0, c:n-7, idx:1 }, { r:n-7, c:0, idx:2 }];
}
function finderInfo(r, c, corners) {
  for (const f of corners) {
    if (r >= f.r && r < f.r+7 && c >= f.c && c < f.c+7)
      return { idx:f.idx, isCenter: r>=f.r+2 && r<f.r+5 && c>=f.c+2 && c<f.c+5 };
  }
  return null;
}

/* ═══════════════ 3. GRID CONSTANTS ═══════════════ */
const MOD    = 1.0;     // grid pitch — the city's only unit
const BODY_W = 0.998;   // body inset avoids coplanar z-fighting with neighbours
const CAP_W  = 1.0;     // roof caps span the FULL pitch: blocks stay contiguous
const FOFF   = 0.5005;  // facade plane offset
const WIN_W  = 0.15;    // reference window width (chimney height matches)
const SPAN   = 0.82;    // usable facade width for the opening grid
const SIGN_RATIO_DEFAULT = 0.75;
const SIGN_TOP_GAP = 0.13;

// ── Matrix → world mapping ──
// Verified against Babylon's actual projection: with the bird camera at
// alpha = -pi/2, a naive z = r - half + 0.5 puts QR row 0 at the BOTTOM of
// the screen, mirroring the code vertically. Flipping the row axis puts the
// three finder patterns back at top-left, top-right and bottom-left.
function colToX(c, half) { return c - half + 0.5; }
function rowToZ(r, half) { return half - r - 0.5; }

const FACES = [
  { nx:0,  nz:1,  ry:0,          tx:1, tz:0 },
  { nx:0,  nz:-1, ry:Math.PI,    tx:1, tz:0 },
  { nx:1,  nz:0,  ry:Math.PI/2,  tx:0, tz:1 },
  { nx:-1, nz:0,  ry:-Math.PI/2, tx:0, tz:1 }
];
const ADJ = [
  { dr:1, dc:0, fi:0 }, { dr:-1, dc:0, fi:1 },
  { dr:0, dc:1, fi:2 }, { dr:0, dc:-1, fi:3 }
];

/* ═══════════════ 4. PROCEDURAL TEXTURES ═══════════════ */
let scene = null;   // set during boot; textures need it

function canvasTexture(name, size, draw) {
  const dt = new BABYLON.DynamicTexture(name, { width:size, height:size }, scene, true);
  draw(dt.getContext(), size);
  dt.update();
  dt.wrapU = dt.wrapV = BABYLON.Texture.WRAP_ADDRESSMODE;
  return dt;
}
function shade(hex, k) {
  const c = BABYLON.Color3.FromHexString(hex).scale(k);
  return '#' + new BABYLON.Color3(
    Math.min(1,c.r), Math.min(1,c.g), Math.min(1,c.b)).toHexString().slice(1);
}

function brickTexture(spec, i) {
  return canvasTexture('brick'+i, 128, (g, S) => {
    const rnd = makePRNG(spec.seed);
    g.fillStyle = spec.mortar; g.fillRect(0,0,S,S);
    const rows = 8, bw = S/4, bh = S/rows;
    for (let row = 0; row < rows; row++) {
      const off = (row % 2) * (bw/2);
      for (let col = -1; col < 5; col++) {
        g.fillStyle = shade(spec.brick, 1 + (rnd()-0.5)*spec.jitter);
        g.fillRect(col*bw + off + 1, row*bh + 1, bw-2, bh-2);
      }
    }
  });
}

// Irregular ashlar: block widths and course phase both vary, so the
// vertical joints never line up — that is what separates stone from brick.
function stoneTexture(spec, i) {
  return canvasTexture('stone'+i, 128, (g, S) => {
    const rnd = makePRNG(spec.seed);
    g.fillStyle = spec.mortar; g.fillRect(0,0,S,S);
    const courses = 6, ch = S/courses;
    for (let row = 0; row < courses; row++) {
      const n = 2 + Math.floor(rnd()*3);
      const cuts = [0];
      for (let k = 1; k < n; k++) cuts.push(rnd());
      cuts.push(1); cuts.sort((a,b) => a-b);
      const phase = rnd()*0.4 - 0.2;
      for (let k = 0; k < n; k++) {
        const x0 = (cuts[k]+phase)*S, x1 = (cuts[k+1]+phase)*S;
        g.fillStyle = shade(spec.stone, 1 + (rnd()-0.5)*spec.jitter);
        // drawn three times so blocks crossing the seam stay continuous
        [0, -S, S].forEach(o =>
          g.fillRect(x0+o+1.2, row*ch+1.2, (x1-x0)-2.4, ch-2.4));
      }
    }
  });
}

// Rendered plaster. Unlike brick or stone it has no courses and no joints:
// its character is a soft mottling plus faint trowel sweeps, which is what
// separates hand-applied render from masonry.
function plasterTexture(spec, i) {
  return canvasTexture('plaster'+i, 128, (g, S) => {
    const rnd = makePRNG(spec.seed);
    g.fillStyle = spec.base; g.fillRect(0, 0, S, S);

    // Overlapping translucent blobs, drawn wrapped so the tile has no seam
    for (let k = 0; k < spec.mottle; k++) {
      const x = rnd()*S, y = rnd()*S, r = 4 + rnd()*16;
      g.fillStyle = shade(spec.base, 1 + (rnd()-0.5)*spec.jitter);
      g.globalAlpha = 0.10 + rnd()*0.16;
      const blob = (px, py) => { g.beginPath(); g.arc(px, py, r, 0, 6.284); g.fill(); };
      blob(x, y);
      if (x < r)   blob(x + S, y);
      if (x > S-r) blob(x - S, y);
      if (y < r)   blob(x, y + S);
      if (y > S-r) blob(x, y - S);
    }

    // Shallow trowel sweeps: the mark of hand application
    g.globalAlpha = 0.07;
    g.lineWidth = 2.4;
    for (let k = 0; k < spec.sweeps; k++) {
      const y = rnd()*S, x = rnd()*S, w = 26 + rnd()*54;
      g.strokeStyle = shade(spec.base, rnd() < 0.5 ? 1.13 : 0.89);
      g.beginPath();
      g.moveTo(x, y);
      g.quadraticCurveTo(x + w/2, y + (rnd()-0.5)*9, x + w, y);
      g.stroke();
    }
    g.globalAlpha = 1;
  });
}

function glassTexture(spec, i) {
  return canvasTexture('glass'+i, 128, (g, S) => {
    const rnd = makePRNG(spec.seed);
    g.fillStyle = spec.mullion; g.fillRect(0,0,S,S);
    const cols = 4, rows = 8, pw = S/cols, ph = S/rows;
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
      let col = shade(spec.tint, 0.72 + rnd()*0.62);
      if (rnd() < spec.litProb) col = spec.litTint;
      g.fillStyle = col;
      g.fillRect(c*pw+1.5, r*ph+1.5, pw-3, ph-3);
    }
  });
}

/* ── Corporate signs ──
   2–3 glyphs. Purely alphabetic marks read as acronyms; introducing a
   symbol shortens the alphabetic part, which keeps forms like <@> or
   a|Z legible rather than noisy. Signs are vertical, so they never
   appear in the Bird's-eye reading. */
const LG_UP  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const LG_LOW = 'abcdefghijkmnopqrstuvwxyz';   // no 'l': reads as 1 or |
const LG_SYM = '@&§$•+±×¶‡◆★♥Ω∆ΣΦΨπλµ∞≡';
const LG_BR  = [['<','>'],['[',']'],['(',')'],['{','}'],['/','/'],['|','|']];
const pick = (r, s) => s[Math.floor(r()*s.length)];
const LG_FORMS = [
  r => pick(r,LG_UP)+pick(r,LG_UP)+pick(r,LG_UP),
  r => pick(r,LG_UP)+pick(r,LG_UP),
  r => pick(r,LG_UP)+pick(r,LG_UP)+pick(r,LG_LOW),
  r => pick(r,LG_UP)+pick(r,LG_UP)+pick(r,LG_SYM),
  r => pick(r,LG_SYM)+pick(r,LG_UP)+pick(r,LG_UP),
  r => pick(r,LG_LOW)+'|'+pick(r,LG_UP),
  r => { const b = LG_BR[Math.floor(r()*LG_BR.length)]; return b[0]+pick(r,LG_SYM)+b[1]; },
  r => { const b = LG_BR[Math.floor(r()*LG_BR.length)]; return b[0]+pick(r,LG_UP)+b[1]; },
  r => pick(r,LG_SYM)
];

function logoTexture(rng, palette, i) {
  const bg = palette[Math.floor(rng()*palette.length)];
  const c  = BABYLON.Color3.FromHexString(bg);
  // Foreground is computed for contrast, never trusted from the palette:
  // a pale brand colour must not end up as pale text on a pale sign.
  const lum = 0.2126*c.r + 0.7152*c.g + 0.0722*c.b;
  const fg  = lum > 0.5 ? '#14171c' : '#ffffff';
  const text = LG_FORMS[Math.floor(rng()*LG_FORMS.length)](rng);

  const tex = canvasTexture('logo'+i, 256, (g, S) => {
    // Babylon planes face -Z by default, so every facade quad presents its
    // BACK face outward. Flat colours are unaffected, but a texture is
    // mirrored in U — which is why the lettering read backwards. Drawing the
    // canvas pre-mirrored cancels it, without touching any geometry.
    g.translate(S, 0); g.scale(-1, 1);
    g.fillStyle = bg; g.fillRect(0,0,S,S);
    g.strokeStyle = fg; g.globalAlpha = 0.4; g.lineWidth = 6;
    g.strokeRect(18,18,S-36,S-36); g.globalAlpha = 1;
    let size = text.length === 1 ? 176 : text.length === 2 ? 136 : 104;
    g.fillStyle = fg; g.textAlign = 'center'; g.textBaseline = 'middle';
    for (let k = 0; k < 10; k++) {
      g.font = size + 'px "Cantata One", Georgia, serif';
      if (g.measureText(text).width <= S - 68) break;
      size -= 6;
    }
    g.fillText(text, S/2, S/2 + size*0.04);
  });
  return { tex, text };
}

/* ═══════════════ 5. STYLE COMPILER ═══════════════ */
const _compiled = {};

function mat(name, hex, glowHex, glow) {
  const m = new BABYLON.StandardMaterial(name, scene);
  const c = BABYLON.Color3.FromHexString(hex);
  m.diffuseColor  = c;
  // ambientColor opts the material into scene.ambientColor
  m.ambientColor  = c;
  m.specularColor = new BABYLON.Color3(0.05, 0.05, 0.05);
  m.emissiveColor = glowHex
    ? BABYLON.Color3.FromHexString(glowHex).scale(glow || 1)
    : c.scale(0.16);
  return m;
}
function texMat(name, texture) {
  const m = new BABYLON.StandardMaterial(name, scene);
  m.diffuseTexture = texture;
  // Ambient follows the texture, so brick and stone lift like flat colours
  m.ambientTexture = texture;
  m.specularColor  = new BABYLON.Color3(0.04, 0.04, 0.04);
  m.emissiveColor  = new BABYLON.Color3(0.14, 0.14, 0.14);
  return m;
}

function compileStyle(id) {
  if (_compiled[id]) return _compiled[id];
  const S = QRCITY_STYLESHEETS[id];
  const INV = S.inverted || {};

  // Textures are shared by both polarities: brick stays brick.
  const tex = [];
  S.facade.brick.forEach((s,i) => tex.push(texMat(id+'_br'+i, brickTexture(s,id+i))));
  (S.facade.stone||[]).forEach((s,i) => tex.push(texMat(id+'_st'+i, stoneTexture(s,id+i))));
  (S.facade.plaster||[]).forEach((s,i) => tex.push(texMat(id+'_pl'+i, plasterTexture(s,id+i))));
  const glass = S.facade.glass.map((s,i) => texMat(id+'_gl'+i, glassTexture(s,id+i)));

  const facadesN = S.facade.flat.map((c,i) => mat(id+'_fN'+i, c)).concat(tex);
  const invFlat  = INV.facadeFlat || S.facade.flat;
  // Inverted facades are warm ochre, so brick and stone belong there too.
  // Glass stays off: curtain walls read cold and fight the warm palette.
  const facadesI = invFlat.map((c,i) => mat(id+'_fI'+i, c)).concat(tex);

  const pick2 = (a, b) => (a !== undefined ? a : b);

  const c = {
    def: S,
    rules: Object.assign({}, S.rules),
    logos: [],
    normal: {
      ground: mat(id+'_gnd', S.ground),
      plate:  mat(id+'_plt', S.plate),
      roof:   mat(id+'_rf',  S.roof),
      // The chimney cap matches the roof EXACTLY: from directly above the
      // cap is the only visible part, so any lighter tone shows up as a
      // grey dot on an otherwise solid black QR module.
      chimTop:  mat(id+'_ct', S.roof),
      chimSide: mat(id+'_cs', S.chimney),
      door:  mat(id+'_dr', S.door),
      frame: mat(id+'_fr', S.frame),
      step:  mat(id+'_sp', S.step),
      facades: facadesN, glass
    },
    inv: {
      ground: mat(id+'_ignd', pick2(INV.ground, S.plate)),
      plate:  mat(id+'_iplt', pick2(INV.plate,  S.ground)),
      roof:   mat(id+'_irf',  pick2(INV.roof,   S.ground)),
      chimTop:  mat(id+'_ict', pick2(INV.roof, S.ground)),
      chimSide: mat(id+'_ics', pick2(INV.chimney, S.chimney)),
      door:  mat(id+'_idr', pick2(INV.door,  S.door)),
      frame: mat(id+'_ifr', pick2(INV.frame, S.frame)),
      step:  mat(id+'_isp', pick2(INV.step,  S.step)),
      facades: facadesI, glass: []
    },
    winLit:  (() => {
      const m = mat(id+'_wl', S.window.lit, S.window.litGlow, S.window.glow);
      if (S.window.glow >= 1) {
        // A window is a light source, not a lit surface: drive it purely
        // from emissive so distance and shading stop dimming it.
        m.disableLighting = true;
        m.emissiveColor = BABYLON.Color3.FromHexString(S.window.lit)
                            .scale(Math.min(1.6, S.window.glow));
      }
      return m;
    })(),
    winDark: mat(id+'_wd', S.window.dark),
    landmark: S.landmark.colors.map((col,i) => mat(id+'_lm'+i, col))
  };

  // A pool of ready-made signs. One texture per building would mean
  // hundreds of canvases; a fixed pool bounds that and stays deterministic.
  const lr = makePRNG(0x109000 ^ hashStr(id));
  const pal = (S.logo && S.logo.palette) || ['#2c3e50'];
  for (let i = 0; i < 18; i++) {
    const L = logoTexture(lr, pal, id+'_'+i);
    c.logos.push({ mat: texMat(id+'_lg'+i, L.tex), text: L.text });
  }

  _compiled[id] = c;
  return c;
}

// Surround material, cached per theme. A `waves` spec draws a procedural
// sea; otherwise it is a flat expanse.
const _surround = {};
function surroundMaterial(def, id) {
  if (_surround[id]) return _surround[id];
  const sur = def.surround;
  let m;
  if (sur.waves) {
    const tex = canvasTexture('sea_'+id, 256, (g, S) => {
      const rnd = makePRNG(sur.waves.seed);
      g.fillStyle = sur.color; g.fillRect(0, 0, S, S);
      // Broken horizontal crests: enough to read as water in motionless 3D
      for (let i = 0; i < sur.waves.count; i++) {
        const y = rnd() * S, w = 18 + rnd() * 70, x = rnd() * S;
        g.strokeStyle = sur.waves.crest;
        g.globalAlpha = 0.12 + rnd() * 0.30;
        g.lineWidth = 1 + rnd() * 2.2;
        g.beginPath();
        g.moveTo(x, y);
        g.bezierCurveTo(x + w*0.3, y - 3, x + w*0.7, y + 3, x + w, y);
        g.stroke();
      }
      g.globalAlpha = 1;
    });
    tex.uScale = tex.vScale = 7;
    m = texMat('surround_'+id, tex);
  } else {
    m = mat('surround_'+id, sur.color);
  }
  _surround[id] = m;
  return m;
}

/* ═══════════════ 6. STATE ═══════════════ */
const DEFAULTS = {
  text:    'Welcome to Pocket City !!',
  forcedN: 29,                 // fits the default text at ECC level Q
  styleId: 'daylight',
  mode:    'bird'
};

const ST = {
  mat:null, n:0, seed:0, text:DEFAULTS.text,
  inverted:false, styleId:DEFAULTS.styleId, forcedN:DEFAULTS.forcedN, mode:DEFAULTS.mode
};
let SS = null;   // compiled stylesheet
let V  = null;   // active polarity variant
let city = null;

let engine, camOrtho, camPersp, activeCam;
let lightAmbient, lightSun, lightFill;

/* ═══════════════ 7. MESH BATCHING ═══════════════ */
// At 49x49 a naive build is ~23 000 meshes. Thin instances collapse each
// (geometry, material) pair into a single draw call.
let batches = null;
function batchReset() { batches = new Map(); }

function push(key, kind, material, px, py, pz, sx, sy, sz, ry, rx) {
  let b = batches.get(key);
  if (!b) { b = { kind, material, list: [] }; batches.set(key, b); }
  const m = BABYLON.Matrix.Compose(
    new BABYLON.Vector3(sx, sy, sz),
    BABYLON.Quaternion.RotationYawPitchRoll(ry || 0, rx || 0, 0),
    new BABYLON.Vector3(px, py, pz));
  b.list.push(m);
}

function batchFlush(parent) {
  let total = 0, draws = 0;
  for (const [key, b] of batches) {
    if (!b.list.length) continue;
    const src =
      b.kind === 'box'  ? BABYLON.MeshBuilder.CreateBox(key, { size: 1 }, scene) :
      // slice 0.5 keeps the upper half only: a dome, not a ball sunk in a roof
      b.kind === 'dome' ? BABYLON.MeshBuilder.CreateSphere(key,
                            { diameter: 1, slice: 0.5, segments: 14 }, scene) :
      BABYLON.MeshBuilder.CreatePlane(key, { size: 1, sideOrientation: BABYLON.Mesh.DOUBLESIDE }, scene);
    src.material = b.material;
    src.parent = parent;
    src.isPickable = false;
    // Lit windows are emitters: fog must not swallow them with distance
    if (key === 'winL') src.applyFog = false;
    const buf = new Float32Array(b.list.length * 16);
    b.list.forEach((m, i) => m.copyToArray(buf, i * 16));
    src.thinInstanceSetBuffer('matrix', buf, 16, true);
    total += b.list.length; draws++;
  }
  return { total, draws };
}

/* ═══════════════ 8. ARCH TUNNELS ═══════════════ */
const ARCH_MIN = 2, ARCH_MAX = 4;
function archCap(n) {
  const a = SS.rules.archCap;
  return n >= 45 ? a.large : n >= 33 ? a.mid : a.small;
}
function isDark(m, n, r, c, inv) {
  if (r < 0 || r >= n || c < 0 || c >= n) return false;   // outside = street
  return inv ? m[r][c] !== 1 : m[r][c] === 1;
}

function findArchRuns(m, n, inv, corners, rng) {
  const cand = [];
  const scan = h => {
    for (let a = 0; a < n; a++) {
      let b = 0;
      while (b < n) {
        const r0 = h ? a : b, c0 = h ? b : a;
        if (!isDark(m, n, r0, c0, inv)) { b++; continue; }
        let len = 0;
        while (isDark(m, n, h ? a : b+len, h ? b+len : a, inv)) len++;
        if (len >= ARCH_MIN && len <= ARCH_MAX) {
          // Both ends must open onto street, else the tunnel connects nothing
          const open = !isDark(m, n, h?a:b-1, h?b-1:a, inv)
                    && !isDark(m, n, h?a:b+len, h?b+len:a, inv);
          let finder = false;
          if (!inv) for (let i = 0; i < len; i++)
            if (finderInfo(h?a:b+i, h?b+i:a, corners)) { finder = true; break; }
          if (open && !finder) cand.push({ r:r0, c:c0, len, horizontal:h });
        }
        b += len;
      }
    }
  };
  // Collect from BOTH axes before sampling: capping during the first scan
  // would fill the budget with horizontal runs only.
  scan(true); scan(false);
  for (let i = cand.length-1; i > 0; i--) {
    const j = Math.floor(rng()*(i+1));
    [cand[i], cand[j]] = [cand[j], cand[i]];
  }
  const cap = archCap(n), prob = SS.rules.archProb;
  const runs = [], used = new Set();
  for (const cd of cand) {
    if (runs.length >= cap) break;
    if (rng() > prob * 4) continue;
    const cells = [];
    let clash = false;
    for (let i = 0; i < cd.len; i++) {
      const k = (cd.horizontal ? cd.r : cd.r+i) + ',' + (cd.horizontal ? cd.c+i : cd.c);
      cells.push(k);
      if (used.has(k)) clash = true;
    }
    if (clash) continue;
    cells.forEach(k => used.add(k));
    runs.push(cd);
  }
  return { runs, used };
}

// The arch keeps its own geometry: a hole cannot be thin-instanced.
// ExtrudePolygon with a hole is native Babylon — no CSG library needed.
function buildArch(parent, run, n, rng) {
  const TW = 0.54, AH = 0.78, rad = TW/2, straight = AH - rad, LIP = 0.012;
  const R = SS.rules;
  const h = Math.max(1.7, R.height.min + rng()*(R.height.max - R.height.min));
  const L = run.len * MOD, half = n/2;

  const outer = [
    new BABYLON.Vector3(-BODY_W/2, 0, -L/2),
    new BABYLON.Vector3( BODY_W/2, 0, -L/2),
    new BABYLON.Vector3( BODY_W/2, 0,  L/2),
    new BABYLON.Vector3(-BODY_W/2, 0,  L/2)
  ];
  const box = BABYLON.MeshBuilder.ExtrudePolygon('archBody',
    { shape: outer, depth: h, sideOrientation: BABYLON.Mesh.DOUBLESIDE }, scene, earcut);
  box.material = V.facades[Math.floor(rng()*V.facades.length)];
  box.position.y = h;
  box.parent = parent;
  box.isPickable = false;

  // The opening is carved by a subtractive-looking void: two side walls and
  // an arched soffit built as thin plates. Cheaper and more robust than CSG.
  const voidMat = V.step;
  const segs = 12;
  const pts = [];
  pts.push(new BABYLON.Vector3(-rad, LIP, 0));
  for (let i = 0; i <= segs; i++) {
    const a = Math.PI - (i/segs)*Math.PI;
    pts.push(new BABYLON.Vector3(rad*Math.cos(a), straight + rad*Math.sin(a), 0));
  }
  pts.push(new BABYLON.Vector3(rad, LIP, 0));
  const soffit = BABYLON.MeshBuilder.ExtrudeShape('archVoid',
    { shape: pts, path: [new BABYLON.Vector3(0,0,-L/2), new BABYLON.Vector3(0,0,L/2)],
      sideOrientation: BABYLON.Mesh.DOUBLESIDE, cap: BABYLON.Mesh.NO_CAP }, scene);
  soffit.material = voidMat;
  soffit.parent = parent;
  soffit.isPickable = false;

  // Centre of the run, using the same flipped row mapping as everything else
  const cx = run.horizontal
    ? (colToX(run.c, half) + colToX(run.c + run.len - 1, half)) / 2
    :  colToX(run.c, half);
  const cz = run.horizontal
    ?  rowToZ(run.r, half)
    : (rowToZ(run.r, half) + rowToZ(run.r + run.len - 1, half)) / 2;
  [box, soffit].forEach(msh => {
    msh.position.x = cx; msh.position.z = cz;
    if (run.horizontal) msh.rotation.y = Math.PI/2;
  });
  box.position.y = h;

  // Roof caps per module keep the top view contiguous
  for (let i = 0; i < run.len; i++) {
    const rr = run.horizontal ? run.r : run.r + i;
    const cc = run.horizontal ? run.c + i : run.c;
    const x = colToX(cc, half), z = rowToZ(rr, half);
    push('cap', 'box', V.roof, x, h + 0.03, z, CAP_W, 0.06, CAP_W, 0);
    const sides = run.horizontal ? [FACES[0], FACES[1]] : [FACES[2], FACES[3]];
    const acols = 1 + Math.floor(rng()*2);
    for (const f of sides) addFacade(x, z, h, f, acols, rng, AH + 0.18, -1, h);
    if (rng() < 0.5) addChimney(x, z, h, rng);
  }
}

/* ═══════════════ 8b. DOMES ═══════════════ */
// A dome sits inside its module footprint and takes the roof colour, so the
// top-down reading is untouched — the module still reads as one solid dark
// square. A 2x2 dome spans four modules, which only works if all four are
// dark, unclaimed, and share one roof height; the pre-pass enforces that.
function findDomeBlocks(M, n, inverted, corners, usedByArch, rng, prob) {
  const claimed = new Map();          // 'r,c' -> { anchor, size, height }
  if (!prob) return claimed;

  const dark = (r, c) => {
    if (r < 0 || r >= n || c < 0 || c >= n) return false;
    let d = M[r][c] === 1;
    if (inverted) d = !d;
    return d;
  };
  const free = (r, c) =>
    dark(r, c) &&
    !usedByArch.has(r + ',' + c) &&
    !claimed.has(r + ',' + c) &&
    (inverted || !finderInfo(r, c, corners));

  const R = SS.rules;
  const big = [];
  for (let r = 0; r < n - 1; r++) {
    for (let c = 0; c < n - 1; c++) {
      if (rng() > prob * 0.35) continue;               // 2x2 stays rare
      if (!(free(r,c) && free(r,c+1) && free(r+1,c) && free(r+1,c+1))) continue;
      const h = rand(rng, R.height);                   // one height for all four
      for (const [rr, cc] of [[r,c],[r,c+1],[r+1,c],[r+1,c+1]])
        claimed.set(rr + ',' + cc, { anchor: (rr === r && cc === c), size: 2, height: h, r, c });
      big.push([r, c]);
    }
  }
  // Single-module domes on whatever is left
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      if (!free(r, c)) continue;
      if (rng() > prob) continue;
      claimed.set(r + ',' + c, { anchor: true, size: 1, height: rand(rng, R.height), r, c });
    }
  }
  return claimed;
}

function addDome(x, z, h, size) {
  const d = size * 0.94;              // just inside the footprint
  push('dome', 'dome', V.roof, x, h + 0.05, z, d, d * 0.62, d, 0);
}

/* ═══════════════ 9. CITY BUILDER ═══════════════ */
function rand(rng, range) { return range.min + rng()*(range.max - range.min); }

// A module carrying a dome. All four modules of a 2x2 share one height so the
// hemisphere lands on a flat roof; only the anchor draws the dome itself.
function placeDomeModule(x, z, half, claim, rng, r, c, M, n, inv) {
  const h = claim.height;
  const fi = Math.floor(rng() * V.facades.length);
  push('body' + fi, 'box', V.facades[fi], x, h/2, z, BODY_W, h, BODY_W, 0);
  push('cap', 'box', V.roof, x, h + 0.03, z, CAP_W, 0.06, CAP_W, 0);

  if (claim.anchor) {
    // Centre of the block: the anchor module for 1x1, the shared corner for 2x2
    const cx = colToX(claim.c + (claim.size - 1) / 2, half);
    const cz = rowToZ(claim.r + (claim.size - 1) / 2, half);
    addDome(cx, cz, h, claim.size);
  }

  const cols = winCount(rng);
  const door = planDoor(r, c, M, n, inv, rng, cols);
  if (h > 1.0) {
    for (let f = 0; f < FACES.length; f++)
      addFacade(x, z, h, FACES[f], cols, rng, 0,
                (door && door.faceIdx === f) ? door.col : -1, h);
  }
  if (door) addDoor(x, z, FACES[door.faceIdx], cols, door.col);
}
function winCount(rng) {
  const w = SS.rules.windowsPerFace;
  return w.min + Math.floor(rng()*(w.max - w.min + 1));
}
function signSize() {
  return BODY_W * ((SS.def.logo && SS.def.logo.size) || SIGN_RATIO_DEFAULT);
}
function signBand() { return signSize() + SIGN_TOP_GAP + 0.06; }

function buildCity() {
  const t0 = performance.now();
  const { mat: M, n, seed, inverted } = { mat:ST.mat, n:ST.n, seed:ST.seed, inverted:ST.inverted };
  const rng = makePRNG(seed);
  V = inverted ? SS.inv : SS.normal;

  if (city) city.dispose(false, false);
  city = new BABYLON.TransformNode('city', scene);
  batchReset();

  const corners = finderCorners(n);
  const names = SS.def.landmark.names, cols = SS.def.landmark.colors;
  const lmTypes = [0,1,2].map(() => Math.floor(rng()*cols.length));
  // The builder reports landmarks; it never writes to the DOM.
  const landmarks = lmTypes.map((t,i) => ({ finder:i+1, name:names[t], color:cols[t] }));

  const half = n/2;
  // Quiet zone: exactly one module of margin, the QR spec minimum
  const gnd = BABYLON.MeshBuilder.CreateGround('ground', { width:n+2, height:n+2 }, scene);
  gnd.material = V.ground; gnd.parent = city; gnd.isPickable = false;

  // No earcut, no ExtrudePolygon: fall back to a city without arches
  const archesAvailable = (typeof earcut !== 'undefined');
  const { runs, used } = archesAvailable
    ? findArchRuns(M, n, inverted, corners, rng)
    : { runs: [], used: new Set() };

  // Domes are claimed before the main pass so a 2x2 can level its four roofs
  const domes = findDomeBlocks(M, n, inverted, corners, used, rng,
                               SS.rules.domeProb || 0);

  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      let dark = M[r][c] === 1;
      if (inverted) dark = !dark;
      if (!dark) continue;

      const x = colToX(c, half), z = rowToZ(r, half);
      // Dark plate under every dark module: belt-and-braces so no light
      // seam shows between buildings at oblique angles.
      // Plates overlap by 2% and sit slightly higher: edge-to-edge coplanar
      // quads produce a crawling seam where the ground shows through.
      push('plate', 'plane', V.plate, x, 0.02, z, MOD*1.02, MOD*1.02, 1, 0, Math.PI/2);
      if (used.has(r + ',' + c)) continue;

      const claim = domes.get(r + ',' + c);
      if (claim) { placeDomeModule(x, z, half, claim, rng, r, c, M, n, inverted); continue; }

      const fi = inverted ? null : finderInfo(r, c, corners);
      if (fi) placeLandmark(x, z, lmTypes[fi.idx], fi.isCenter, rng, r, c, M, n, inverted);
      else    placeBuilding(x, z, r, c, M, n, inverted, rng);
    }
  }

  for (const run of runs) {
    try { buildArch(city, run, n, rng); }
    catch (e) { TSCG.fail('Arch skipped', e.message); }
  }

  const stats = batchFlush(city);
  return {
    instances: stats.total, draws: stats.draws,
    arches: runs.length, landmarks,
    ms: Math.round(performance.now() - t0)
  };
}

function placeLandmark(x, z, ti, isCenter, rng, r, c, M, n, inv) {
  const R = SS.rules;
  const h = isCenter ? rand(rng, R.landmarkKeep) : rand(rng, R.landmarkRing);
  const canGlass = V.glass.length > 0;
  const useGlass = canGlass && isCenter && rng() < R.landmarkGlassProb;
  const gi = V.glass.length ? Math.floor(rng()*V.glass.length) : 0;
  const key  = useGlass ? 'glass'+gi : 'lm'+(ti % SS.landmark.length);
  const fmat = useGlass ? V.glass[gi] : SS.landmark[ti % SS.landmark.length];

  push(key, 'box', fmat, x, h/2, z, BODY_W, h, BODY_W, 0);
  // Black roof like every other building: from above landmarks must not
  // stand out, or they would corrupt their own finder pattern.
  push('cap', 'box', V.roof, x, h+0.03, z, CAP_W, 0.06, CAP_W, 0);

  const cols = winCount(rng);
  const door = planDoor(r, c, M, n, inv, rng, cols);
  if (!useGlass && h > 1.0) {
    for (let f = 0; f < FACES.length; f++)
      addFacade(x, z, h, FACES[f], cols, rng, 0,
                (door && door.faceIdx === f) ? door.col : -1, h);
  }
  if (rng() < R.landmarkChimneyProb) addChimney(x, z, h, rng);
  if (door) addDoor(x, z, FACES[door.faceIdx], cols, door.col);
}

function placeBuilding(x, z, r, c, M, n, inv, rng) {
  const R = SS.rules;
  const h = rand(rng, R.height);
  const canGlass = V.glass.length > 0;
  const useGlass = canGlass && h > R.glassMinHeight && rng() < R.glassProb;
  const gi = V.glass.length ? Math.floor(rng()*V.glass.length) : 0;
  const fi = Math.floor(rng()*V.facades.length);
  const key  = useGlass ? 'glass'+gi : 'body'+fi;
  const bMat = useGlass ? V.glass[gi] : V.facades[fi];

  push(key, 'box', bMat, x, h/2, z, BODY_W, h, BODY_W, 0);
  push('cap', 'box', V.roof, x, h+0.03, z, CAP_W, 0.06, CAP_W, 0);

  const nc = Math.floor(rng()*R.chimneyMax);
  for (let i = 0; i < nc; i++) addChimney(x, z, h, rng);

  // The door is planned BEFORE the facades so its grid cell can be reserved
  const cols = winCount(rng);
  const door = planDoor(r, c, M, n, inv, rng, cols);

  const logoProb = (R.logoProb !== undefined ? R.logoProb : 0) * 1.38;
  const wantsLogo = h >= (R.logoMinHeight || 2.2) && rng() < logoProb;
  const logoFace = wantsLogo ? Math.floor(rng()*FACES.length) : -1;

  if (h > 1.0) {
    for (let f = 0; f < FACES.length; f++) {
      const ceiling = (f === logoFace) ? h - signBand() : h;
      if (!useGlass) addFacade(x, z, h, FACES[f], cols, rng, 0,
                               (door && door.faceIdx === f) ? door.col : -1, ceiling);
    }
  }
  if (logoFace >= 0) addSign(x, z, h, FACES[logoFace], rng);
  if (door) addDoor(x, z, FACES[door.faceIdx], cols, door.col);
}

function addChimney(x, z, h, rng) {
  const CH = WIN_W;                       // height matches one window width
  const ox = (rng()-0.5)*0.44, oz = (rng()-0.5)*0.44;
  push('chimS', 'box', V.chimSide, x+ox, h + 0.06 + CH/2, z+oz, 0.11, CH, 0.11, 0);
  // Cap is wider than the shaft (0.15 vs 0.11) so from directly above it
  // fully occludes the light-grey shaft and the module reads as pure dark.
  push('chimT', 'box', V.chimTop,  x+ox, h + 0.06 + CH + 0.02, z+oz, 0.15, 0.04, 0.15, 0);
}

/* ── Facade opening grid ──
   Windows and the door share one column grid, so they align instead of
   being placed independently. The door owns its ground-floor cell; two
   adjacent free cells may merge into a bay window. */
function colCentre(i, cols, w) { return ((i + (w||1)/2)/cols - 0.5) * SPAN; }

function addFacade(x, z, bldH, face, cols, rng, minY, doorCol, ceiling) {
  const R = SS.rules;
  const cellW = SPAN/cols;
  const W_W = Math.min(cellW*0.62, WIN_W);
  const W_H = W_W * 2;                    // single window: strict 2:1 portrait
  const bayProb = R.bayProb !== undefined ? R.bayProb : 0.18;
  const top = (ceiling !== undefined ? ceiling : bldH) - 0.10;
  const floors = Math.floor(bldH);

  for (let fl = 0; fl < floors; fl++) {
    const wy = 0.62 + fl;
    if (wy < minY) continue;
    if (wy + W_H >= top) continue;
    const ground = (fl === 0);
    let ci = 0;
    while (ci < cols) {
      if (ground && ci === doorCol) { ci++; continue; }
      if (rng() < R.windowAbsentProb) { ci++; continue; }

      let width = 1;
      const nextFree = (ci+1 < cols) && !(ground && (ci+1) === doorCol);
      if (nextFree && rng() < bayProb) width = 2;

      const lit = rng() < R.windowLitProb;
      const along = colCentre(ci, cols, width);
      // A bay keeps the single-window height and spans two cells, so it
      // reads as a picture window rather than a stretched portrait one.
      const w = width === 1 ? W_W : Math.min(cellW*2*0.72, WIN_W*2.4);

      push(lit ? 'winL' : 'winD', 'plane', lit ? SS.winLit : SS.winDark,
           x + face.nx*FOFF + face.tx*along, wy + W_H/2,
           z + face.nz*FOFF + face.tz*along, w, W_H, 1, face.ry);

      if (width === 2) {
        const mid = colCentre(ci, cols, 2);
        push('mull', 'plane', V.frame,
             x + face.nx*(FOFF+0.002) + face.tx*mid, wy + W_H/2,
             z + face.nz*(FOFF+0.002) + face.tz*mid, 0.012, W_H, 1, face.ry);
      }
      ci += width;
    }
  }
}

function planDoor(r, c, M, n, inv, rng, cols) {
  const sides = [];
  for (const a of ADJ) if (!isDark(M, n, r+a.dr, c+a.dc, inv)) sides.push(a.fi);
  if (!sides.length) return null;        // fully enclosed: no street frontage
  return { faceIdx: sides[Math.floor(rng()*sides.length)],
           col: Math.floor(rng()*cols) };
}

function addDoor(x, z, face, cols, col) {
  const cellW = SPAN/cols;
  const DW = Math.min(cellW*0.62, 0.26), DH = DW*2;
  const FW = DW + 0.055, FH = DH + 0.04;
  const along = colCentre(col, cols, 1);
  push('dFrame', 'plane', V.frame,
       x + face.nx*FOFF + face.tx*along, FH/2,
       z + face.nz*FOFF + face.tz*along, FW, FH, 1, face.ry);
  push('dPanel', 'plane', V.door,
       x + face.nx*(FOFF+0.004) + face.tx*along, DH/2 + 0.012,
       z + face.nz*(FOFF+0.004) + face.tz*along, DW, DH, 1, face.ry);
  const sw = face.nx !== 0 ? 0.05 : FW, sd = face.nz !== 0 ? 0.05 : FW;
  push('dStep', 'box', V.step,
       x + face.nx*0.52 + face.tx*along, 0.015,
       z + face.nz*0.52 + face.tz*along, sw, 0.03, sd, 0);
}

function addSign(x, z, h, face, rng) {
  if (!SS.logos.length) return;
  const idx = Math.floor(rng()*SS.logos.length);
  const s = signSize();
  const y = h - SIGN_TOP_GAP - s/2;      // hangs just under the roofline
  push('logo'+idx, 'plane', SS.logos[idx].mat,
       x + face.nx*(FOFF+0.004), y, z + face.nz*(FOFF+0.004), s, s, 1, face.ry);
}


/* ═══════════════ 9b. AUTO WALK — street pathfinding ═══════════════ */
// The street network INSIDE a QR code is not connected: light modules form
// dozens of isolated pockets, so no route exists from corner to corner.
// Measured on TSCG: 60 separate components at 33x33. What makes a walk
// possible is the quiet zone — the one-module margin the QR spec requires,
// which forms a continuous ring around the whole code.
//
// Routing on the ring alone would trivially skirt the city, so ring cells
// carry a higher traversal cost. At cost 4 the route spends roughly half
// its length inside the code instead of all of it on the perimeter.
const RING_COST = 4;

// Padded coordinates: r,c in 0..n+1, where 0 and n+1 are the quiet zone
// and the code occupies 1..n. Matrix row = r-1, matrix col = c-1.
function buildRoute(M, n, inverted, from, to) {
  const N = n + 2, half = n / 2;
  const isRing = (r, c) => r === 0 || c === 0 || r === N-1 || c === N-1;
  const walkable = (r, c) => {
    if (r < 0 || r >= N || c < 0 || c >= N) return false;
    if (isRing(r, c)) return true;                  // quiet zone is open ground
    let dark = M[r-1][c-1] === 1;
    if (inverted) dark = !dark;
    return !dark;                                   // light module = street
  };

  const key = (r, c) => r * N + c;
  const start = from || [N-1, N-1], goal = to || [0, 0];
  const dist = new Map([[key(...start), 0]]);
  const prev = new Map();
  let frontier = [[0, start[0], start[1]]];

  while (frontier.length) {
    frontier.sort((a, b) => a[0] - b[0]);
    const [d, r, c] = frontier.shift();
    if (d > (dist.get(key(r, c)) ?? Infinity)) continue;
    if (r === goal[0] && c === goal[1]) break;
    for (const [dr, dc] of [[1,0],[-1,0],[0,1],[0,-1]]) {
      const nr = r + dr, nc = c + dc;
      if (!walkable(nr, nc)) continue;
      const nd = d + (isRing(nr, nc) ? RING_COST : 1);
      if (nd < (dist.get(key(nr, nc)) ?? Infinity)) {
        dist.set(key(nr, nc), nd);
        prev.set(key(nr, nc), key(r, c));
        frontier.push([nd, nr, nc]);
      }
    }
  }
  if (!prev.has(key(...goal))) return null;

  const cells = [];
  for (let k = key(...goal); k !== undefined; k = prev.get(k))
    cells.push([Math.floor(k / N), k % N]);
  cells.reverse();

  // Padded cell → world, reusing the same mapping as the city itself
  return cells.map(([r, c]) =>
    new BABYLON.Vector3(colToX(c - 1, half), EYE, rowToZ(r - 1, half)));
}

const AUTO = { on:false, path:null, seg:0, t:0, speed:1.9, trail:null, leg:0 };

// A landmark or the city centre is usually a BUILDING, so a route cannot end
// on it — it has to aim at a nearby street cell instead.
//
// But "nearby" is not enough: only about half the light modules belong to the
// component the quiet-zone ring connects, so the closest street cell is often
// stranded in an isolated pocket and no route exists. Candidates are therefore
// restricted to the cells actually reachable from the ring.
function reachableCells(M, n, inverted) {
  const N = n + 2;
  const isRing = (r, c) => r === 0 || c === 0 || r === N-1 || c === N-1;
  const open = (r, c) => {
    if (r < 0 || r >= N || c < 0 || c >= N) return false;
    if (isRing(r, c)) return true;
    let dark = M[r-1][c-1] === 1;
    if (inverted) dark = !dark;
    return !dark;
  };
  const seen = new Set([0]);
  const stack = [[0, 0]];
  while (stack.length) {
    const [r, c] = stack.pop();
    for (const [dr, dc] of [[1,0],[-1,0],[0,1],[0,-1]]) {
      const nr = r + dr, nc = c + dc;
      if (!open(nr, nc)) continue;
      const k = nr * N + nc;
      if (seen.has(k)) continue;
      seen.add(k); stack.push([nr, nc]);
    }
  }
  return seen;
}

function nearestWalkable(M, n, inverted, r0, c0, reach) {
  const N = n + 2;
  const cells = reach || reachableCells(M, n, inverted);
  let best = null, bd = Infinity;
  for (const k of cells) {
    const r = Math.floor(k / N), c = k % N;
    const d = (r-r0)*(r-r0) + (c-c0)*(c-c0);
    if (d < bd) { bd = d; best = [r, c]; }
  }
  return best;
}

// Itineraries, in padded coordinates. Leg 0 is the corner-to-corner crossing;
// leg 1 visits the top-left landmark, the centre, then the bottom-left one.
function itineraries(M, n, inv) {
  const N = n + 2, mid = Math.round(N / 2);
  const reach = reachableCells(M, n, inv);       // computed once per itinerary
  const nw = (r, c) => nearestWalkable(M, n, inv, r, c, reach);
  return [
    { name: 'Corner to corner', legs: [[N-1, N-1], [0, 0]] },
    { name: 'Landmark tour',    legs: [nw(4, 4), nw(mid, mid), nw(N-4, 4)] }
  ];
}

function routeThrough(M, n, inv, legs) {
  const full = [];
  for (let i = 0; i + 1 < legs.length; i++) {
    const part = buildRoute(M, n, inv, legs[i], legs[i+1]);
    if (!part) return null;
    full.push(...(i ? part.slice(1) : part));
  }
  return full;
}
const WALK_PITCH = -0.30;               // ~17 degrees down

// A route drawn on the pavement, in the manner of a wayfinding overlay:
// short green dashes laid end to end along the path, lifted just clear of
// the ground so they read without z-fighting.
function buildTrail(path) {
  disposeTrail();
  const node = new BABYLON.TransformNode('trail', scene);

  const mat = new BABYLON.StandardMaterial('trailMat', scene);
  mat.diffuseColor  = BABYLON.Color3.FromHexString('#2bff7a');
  mat.emissiveColor = BABYLON.Color3.FromHexString('#2bff7a');
  mat.disableLighting = true;
  mat.alpha = 0.95;

  // The halo needs a bloom pass. Themes other than Night do not declare one,
  // so the trail brings its own and gives it back when it stops.
  if (!glowLayer) glowLayer = new BABYLON.GlowLayer('glow', scene, { blurKernelSize: 40 });
  trailGlowRestore = glowLayer.intensity;
  glowLayer.intensity = Math.max(glowLayer.intensity, 0.75);

  // A chevron band, lying flat in XZ and pointing along +Z. CreatePolygon
  // builds it from the outline; earcut does the triangulation.
  // Half-width, tip depth, band thickness — proportioned from the reference
  // wayfinding chevron (D/W ~ 0.72, T/W ~ 0.64).
  //
  // T is measured VERTICALLY, but the eye reads the thickness PERPENDICULAR
  // to the arm, which is smaller by cos(arm angle). At 45 degrees that lost
  // a third of the apparent weight, which is why the first attempt looked
  // like wire. Here the perpendicular thickness lands at ~52% of the
  // half-width, matching the reference.
  const W = 0.32, D = 0.24, T = 0.21;
  const shape = [
    new BABYLON.Vector3(-W, 0,  0),
    new BABYLON.Vector3( 0, 0,  D),
    new BABYLON.Vector3( W, 0,  0),
    new BABYLON.Vector3( W, 0, -T),
    new BABYLON.Vector3( 0, 0,  D - T),
    new BABYLON.Vector3(-W, 0, -T)
  ];
  const src = BABYLON.MeshBuilder.CreatePolygon('chevron',
    { shape, sideOrientation:BABYLON.Mesh.DOUBLESIDE }, scene, earcut);
  src.material = mat;
  src.parent = node;
  src.isPickable = false;
  src.applyFog = false;

  // Chevron footprint is 0.45 deep; the gap keeps successive tips distinct
  // without letting the trail break up.
  const DASH = 0.45, GAP = 0.17;

  // Walk the polyline at constant spacing so dashes stay even through turns
  const mats = [];
  let carry = 0;
  for (let i = 0; i + 1 < path.length; i++) {
    const a = path[i], b = path[i+1];
    const seg = BABYLON.Vector3.Distance(a, b);
    if (seg < 1e-6) continue;
    const dirX = (b.x - a.x) / seg, dirZ = (b.z - a.z) / seg;
    const yaw  = Math.atan2(dirX, dirZ);
    for (let d = carry; d < seg; d += DASH + GAP) {
      const t = (d + DASH/2) / seg;
      if (t > 1) break;
      mats.push(BABYLON.Matrix.Compose(
        new BABYLON.Vector3(1, 1, 1),
        BABYLON.Quaternion.RotationYawPitchRoll(yaw, 0, 0),
        new BABYLON.Vector3(a.x + (b.x-a.x)*t, 0.05, a.z + (b.z-a.z)*t)));
    }
    carry = (carry - seg) % (DASH + GAP);
    if (carry < 0) carry += DASH + GAP;
  }
  const buf = new Float32Array(mats.length * 16);
  mats.forEach((m, i) => m.copyToArray(buf, i * 16));
  src.thinInstanceSetBuffer('matrix', buf, 16, true);
  src.frustumCulled = false;

  AUTO.trail = node;
  return mats.length;
}

let trailGlowRestore = null;

function disposeTrail() {
  if (AUTO.trail) { AUTO.trail.dispose(false, true); AUTO.trail = null; }
  if (glowLayer && trailGlowRestore !== null) {
    glowLayer.intensity = trailGlowRestore;
    trailGlowRestore = null;
  }
}

function autoWalkStart(which) {
  AUTO.leg = which || 0;
  const routes = itineraries(ST.mat, ST.n, ST.inverted);
  const r = routes[AUTO.leg % routes.length];
  AUTO.path = routeThrough(ST.mat, ST.n, ST.inverted, r.legs);
  AUTO.name = r.name;
  if (!AUTO.path || AUTO.path.length < 2) {
    setHint('No route found across this code');
    return false;
  }
  AUTO.on = true; AUTO.seg = 0; AUTO.t = 0;
  if (ST.mode !== 'walk') setMode('walk');
  camPersp.position.copyFrom(AUTO.path[0]);
  pitch = WALK_PITCH; applyLook();
  const dashes = buildTrail(AUTO.path);
  setHint(AUTO.name + ' — ' + AUTO.path.length + ' steps, ' + dashes +
          ' chevrons. Any movement key takes over');
  return true;
}
// Arriving somewhere should propose the next leg rather than just stopping
function autoWalkFinish() {
  autoWalkStop('Arrived — ' + AUTO.name + ' complete');
  const nb = $('btn-next-route');
  if (nb) nb.classList.add('on');
}

function autoWalkStop(msg) {
  AUTO.on = false;
  disposeTrail();
  const b = $('btn-autowalk');
  if (b) { b.classList.remove('on'); b.textContent = 'Auto walk \u25B6'; }
  if (msg) setHint(msg);
}

// Advance along the polyline, turning to face the direction of travel.
// Yaw is eased rather than snapped so corners read as turns, not cuts.
function tickAuto(dt) {
  const p = AUTO.path;
  if (!p || AUTO.seg >= p.length - 1) { autoWalkFinish(); return; }

  const a = p[AUTO.seg], b = p[AUTO.seg + 1];
  const segLen = BABYLON.Vector3.Distance(a, b) || 1;
  AUTO.t += (AUTO.speed * dt) / segLen;
  while (AUTO.t >= 1 && AUTO.seg < p.length - 1) {
    AUTO.t -= 1; AUTO.seg++;
    if (AUTO.seg >= p.length - 1) { autoWalkFinish(); return; }
  }
  const s = p[AUTO.seg], e = p[AUTO.seg + 1];
  camPersp.position = BABYLON.Vector3.Lerp(s, e, Math.min(1, AUTO.t));
  camPersp.position.y = EYE;

  const target = Math.atan2(e.x - s.x, e.z - s.z);
  let diff = target - yaw;
  while (diff >  Math.PI) diff -= 2*Math.PI;
  while (diff < -Math.PI) diff += 2*Math.PI;
  yaw += diff * Math.min(1, dt * 5);
  // A pedestrian following a route watches the ground a few paces ahead
  // rather than the skyline; it also keeps the dashed trail in frame.
  pitch += (WALK_PITCH - pitch) * Math.min(1, dt * 3);
  applyLook();
}

/* ═══════════════ 10. SCENE + CAMERAS ═══════════════ */
const ISO_AZ = Math.PI/4, ISO_EL = Math.atan(1/Math.SQRT2), EYE = 1.65;
const MV = { fwd:false, back:false, left:false, right:false, up:false, down:false, run:false };
let yaw = Math.PI, pitch = 0;

let glowLayer = null;

function applySceneStyle() {
  const d = SS.def;
  // Themes that declare a glowLayer get a bloom pass over emissive surfaces,
  // which is what makes lit windows behave like sources instead of swatches.
  const gl = d.glowLayer;
  if (gl && !glowLayer) glowLayer = new BABYLON.GlowLayer('glow', scene, {
    blurKernelSize: gl.blurKernel || 40
  });
  if (glowLayer) glowLayer.intensity = gl ? gl.intensity : 0;
  scene.clearColor = BABYLON.Color4.FromHexString(d.sky + 'ff');
  if (d.fog) {
    scene.fogMode = BABYLON.Scene.FOGMODE_EXP2;
    scene.fogColor = BABYLON.Color3.FromHexString(d.fog.color);
    scene.fogDensity = d.fog.density;
  } else scene.fogMode = BABYLON.Scene.FOGMODE_NONE;

  const ambCol = BABYLON.Color3.FromHexString(d.light.ambient.color);
  lightAmbient.diffuse   = ambCol;
  lightAmbient.intensity = d.light.ambient.intensity;
  // A HemisphericLight weights a surface by 0.5*(1 + normal.y), and its
  // groundColor defaults to BLACK. Vertical facades therefore received only
  // half the ambient that the Three.js prototype's AmbientLight gave them,
  // which is what made the city read as too dark. Lifting groundColor
  // restores an even base without flattening the sun's modelling.
  lightAmbient.groundColor = ambCol.scale(d.light.ambient.ground !== undefined
    ? d.light.ambient.ground : 0.62);

  // Babylon's ambient term is ambientColor * scene.ambientColor, the closest
  // equivalent to a Three.js AmbientLight. Kept modest so it lifts the
  // shadowed sides without washing out the palette.
  scene.ambientColor = ambCol.scale(0.22);
  lightSun.diffuse   = BABYLON.Color3.FromHexString(d.light.sun.color);
  lightSun.intensity = d.light.sun.intensity;
  lightSun.direction = new BABYLON.Vector3(...d.light.sun.dir);
  lightFill.diffuse   = BABYLON.Color3.FromHexString(d.light.fill.color);
  lightFill.intensity = d.light.fill.intensity;
  lightFill.direction = new BABYLON.Vector3(...d.light.fill.dir);
}

// Orthographic framing. Perspective would make off-centre buildings lean
// outward, so their roofs would no longer cover their footprint and the
// Bird's-eye QR reading would break at the edges.
let orthoZoom = 1;                       // 1 = whole city framed

function fitOrtho(n) {
  const el = document.getElementById('view-main');
  const aspect = Math.max(0.2, el.clientWidth / Math.max(1, el.clientHeight));
  // An orthographic camera ignores `radius`, so the wheel cannot zoom by
  // moving the camera — the frustum itself has to shrink.
  const need = (n + 2) / 2 * 1.06 / orthoZoom;

  // Fit the CONSTRAINING axis. Scaling only the horizontal half-extent by
  // aspect crops the city left and right as soon as the view is taller than
  // wide — which is exactly what a widened side panel produces.
  // Half-extents stay proportional to the aspect, so the QR stays square.
  const D = Math.max(need, need / aspect);

  camOrtho.orthoLeft = -D*aspect; camOrtho.orthoRight = D*aspect;
  camOrtho.orthoTop  =  D;        camOrtho.orthoBottom = -D;
}

function setMode(mode) {
  ST.mode = mode;
  const vsel = $('view-select');
  if (vsel && vsel.value !== mode) vsel.value = mode;
  const free = (mode === 'walk' || mode === 'fly');
  const mm = $('minimap-wrap');
  if (mm) mm.classList.toggle('on', free);

  if (free) {
    activeCam = camPersp;
    scene.activeCamera = camPersp;
    camOrtho.detachControl();
    camPersp.fov = 1.05;                  // presets reset the zoom
    const start = ST.n/2 * 0.9;
    camPersp.position = new BABYLON.Vector3(0, mode === 'walk' ? EYE : 6, start);
    yaw = Math.PI; pitch = mode === 'walk' ? 0 : -0.25;
    applyLook();
    setHint(mode === 'walk'
      ? 'Click canvas to look · WASD to move · Shift to run · Esc releases'
      : 'Click canvas to look · WASD · Space / C for altitude · Esc releases');
    return;
  }

  activeCam = camOrtho;
  scene.activeCamera = camOrtho;
  camOrtho.attachControl(document.getElementById('canvas-main'), true);
  if (document.pointerLockElement) document.exitPointerLock();
  const d = Math.max(ST.n, 20) * 1.6;

  // Both are camera PRESETS, not locks. Tilt stays free from either one, so
  // the reader can lift off from the QR reading and reveal the 3D city —
  // the readability chip then reports when the code is still decodable.
  camOrtho.lowerBetaLimit = 0.0005;
  camOrtho.upperBetaLimit = Math.PI*0.495;
  camOrtho.radius = d;

  orthoZoom = 1;                          // presets re-frame the whole city

  if (mode === 'bird') {
    camOrtho.beta = 0.0005; camOrtho.alpha = -Math.PI/2;
    setHint("Bird's eye — this is the source QR. Drag to tilt and reveal the city");
  } else {
    camOrtho.alpha = -Math.PI/2 + ISO_AZ;
    camOrtho.beta  = Math.PI/2 - ISO_EL;
    setHint('Isometric — drag to orbit · scroll to zoom · press 2 to snap back to the QR');
  }
  camOrtho.target = BABYLON.Vector3.Zero();
  fitOrtho(ST.n);
  updateReadability();
}

// A roof at height h shifts by h*tan(beta) relative to its own footprint
// when the camera tilts. The module still reads while that shift stays
// well under half a module, so the threshold depends on the tallest
// building the active stylesheet allows.
// Bird's eye is a preset, not a state: as soon as the user tilts away from
// top-down the view really is isometric, so the combo must say so — and it
// must flip back on its own if they return to the top-down angle.
// 3.5% of the full tilt range (0 .. pi/2): the selector flips to Isometric
// past this, and back to Bird's eye within it — without ever re-framing.
const BIRD_TOL = 0.035;
const BIRD_BETA = (Math.PI / 2) * BIRD_TOL;

let viewSyncArmed = false;              // only after the first frame settles

const BIRD_ALPHA = -Math.PI / 2;        // the azimuth that squares the code

function syncViewSelect() {
  const sel = $('view-select');
  if (!viewSyncArmed || !sel || ST.mode === 'walk' || ST.mode === 'fly') return;
  const atBird = camOrtho.beta < BIRD_BETA;
  const should = atBird ? 'bird' : 'iso';

  if (sel.value !== should) sel.value = should;
  ST.mode = should;                     // keep state honest, without re-framing
}

// Squaring the code to the frame in Bird's eye.
//
// A one-shot snap on the transition was not enough: ArcRotateCamera keeps
// applying `inertialAlphaOffset` in its own _checkInputs for many frames
// after the pointer is released, so it dragged the azimuth back off true as
// soon as the snap finished. The correction therefore runs continuously
// while the view is overhead, and zeroes the inertia it is competing with.
function tickBirdSnap(dt) {
  if (ST.mode !== 'bird') return;
  if (pointerDragging) return;          // never fight an active drag

  // Nearest azimuth that is equivalent to the canonical one
  const turns  = Math.round((camOrtho.alpha - BIRD_ALPHA) / (Math.PI * 2));
  const target = BIRD_ALPHA + turns * Math.PI * 2;
  const d = target - camOrtho.alpha;

  if (Math.abs(d) < 0.0015 && Math.abs(camOrtho.inertialAlphaOffset) < 1e-4) {
    camOrtho.alpha = target;
    camOrtho.inertialAlphaOffset = 0;
    return;
  }
  // Cancel the camera's own drift, then ease toward true
  camOrtho.inertialAlphaOffset *= 0.35;
  camOrtho.alpha += d * Math.min(1, dt * 7);
}

// The camera must be left alone while the user is actually dragging
let pointerDragging = false;

function updateReadability() {
  syncViewSelect();
  const chip = $('chip-read');
  if (!chip || !SS) return;
  if (ST.mode === 'walk' || ST.mode === 'fly') {
    chip.textContent = 'ground view';
    chip.className = 'hchip';
    return;
  }
  const hMax = SS.rules.height.max;
  const shift = hMax * Math.tan(Math.max(0, camOrtho.beta));
  const deg = camOrtho.beta * 180 / Math.PI;

  if (ST.inverted) {
    chip.textContent = 'inverted — not a QR';
    chip.className = 'hchip read-no';
  } else if (shift < 0.25) {
    chip.textContent = 'QR readable · ' + deg.toFixed(1) + '°';
    chip.className = 'hchip read-yes';
  } else if (shift < 0.5) {
    chip.textContent = 'marginal · ' + deg.toFixed(1) + '°';
    chip.className = 'hchip read-mid';
  } else {
    chip.textContent = '3D view · ' + deg.toFixed(0) + '°';
    chip.className = 'hchip read-no';
  }
}

function applyLook() {
  const dir = new BABYLON.Vector3(
    Math.sin(yaw)*Math.cos(pitch), Math.sin(pitch), Math.cos(yaw)*Math.cos(pitch));
  camPersp.setTarget(camPersp.position.add(dir));
}
function tickFree(dt) {
  if (AUTO.on && ST.mode === 'walk') { tickAuto(dt); return; }
  const base = ST.mode === 'walk' ? 2.8 : 9;   // module widths per second
  const sp = base * (MV.run ? 2.4 : 1) * dt;
  const fw = new BABYLON.Vector3(Math.sin(yaw), 0, Math.cos(yaw));
  const rt = new BABYLON.Vector3(Math.cos(yaw), 0, -Math.sin(yaw));
  if (MV.fwd)   camPersp.position.addInPlace(fw.scale(sp));
  if (MV.back)  camPersp.position.addInPlace(fw.scale(-sp));
  if (MV.left)  camPersp.position.addInPlace(rt.scale(-sp));
  if (MV.right) camPersp.position.addInPlace(rt.scale(sp));
  if (ST.mode === 'walk') camPersp.position.y = EYE;
  else {
    if (MV.up)   camPersp.position.y += sp;
    if (MV.down) camPersp.position.y -= sp;
    camPersp.position.y = Math.max(0.6, Math.min(90, camPersp.position.y));
  }
  applyLook();
}

/* ═══════════════ 11. UI GLUE ═══════════════ */
const $ = id => document.getElementById(id);
function setHint(s) { $('hint').textContent = s; }

function drawThumb() {
  const cv = $('qr-thumb'); if (!cv) return;
  const g = cv.getContext('2d'), n = ST.n, px = cv.width/n;
  g.fillStyle = '#ffffff'; g.fillRect(0,0,cv.width,cv.height);
  g.fillStyle = '#14171c';
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    let dark = ST.mat[r][c] === 1;
    if (ST.inverted) dark = !dark;
    if (dark) g.fillRect(Math.floor(c*px), Math.floor(r*px), Math.ceil(px), Math.ceil(px));
  }
}

function report(s) {
  $('id-seed').textContent  = '0x' + ST.seed.toString(16).padStart(8,'0').toUpperCase();
  $('id-grid').textContent  = ST.n + ' × ' + ST.n;
  updateReadability();
  $('chip-grid').textContent  = ST.n + '×' + ST.n;
  $('chip-theme').textContent = SS.def.name;
  const bEl = $('chip-build');
  if (bEl) bEl.textContent = BUILD;
  $('st-inst').textContent = s.instances.toLocaleString();
  $('st-draw').textContent = s.draws;
  $('st-arch').textContent = s.arches;
  $('st-ms').textContent   = s.ms + ' ms';

  const host = $('landmark-list');
  // Landmark roofs are dark like every other roof — they have to be, or they
  // would corrupt their own finder pattern. The colour is on the facades, so
  // it only shows once the camera tilts away from the QR reading.
  const topDown = (ST.mode !== 'walk' && ST.mode !== 'fly' && camOrtho.beta < 0.06);
  host.innerHTML = s.landmarks.map(l =>
    `<div class="lm-row">
       <span class="lm-swatch" style="background:${l.color}"></span>
       <span class="lm-name">${l.name}</span>
       <span class="lm-idx">finder ${l.finder}</span>
     </div>`).join('')
    + `<div class="lm-note">${topDown
        ? 'Facade colour — tilt away from the QR reading to see it'
        : 'Facade colour, visible on the sides'}</div>`;
  drawThumb();
}

function rebuild() {
  if (AUTO.on) autoWalkStop();      // the route belongs to the old city
  if (ST.mat) report(buildCity());
}

function generate(text) {
  const res = extractQR(text, ST.forcedN);
  if (!res) { setHint('Could not encode that text — try shorter input or a larger grid'); return; }
  const wanted = ST.mode;              // capture: rebuild() can rewrite it
  ST.mat = res.mat; ST.n = res.n; ST.text = text; ST.seed = textToSeed(text);
  fitOrtho(ST.n);
  rebuild();
  setMode(wanted);
}

function setStyle(id) {
  ST.styleId = id;
  SS = compileStyle(id);
  applySceneStyle();
  const sel = $('style-select');
  if (sel && sel.value !== id) sel.value = id;
  rebuild();
}

// Populated from the registry, so adding a stylesheet needs no HTML edit
function buildStyleSelect() {
  const sel = $('style-select');
  if (!sel) return;
  sel.innerHTML = QRCITY_STYLE_IDS
    .map(id => `<option value="${id}">${QRCITY_STYLESHEETS[id].name}</option>`)
    .join('');
  sel.value = ST.styleId;
  sel.addEventListener('change', e => setStyle(e.target.value));
}


/* ═══════════════ 11b. MINIMAP ═══════════════ */
// At street level the city is a maze with no horizon, so a top-down inset
// showing the route and the walker's heading is what makes Walk legible.
// It draws the same matrix the city was built from, using the same
// col/row mapping, so map and world can never disagree.
let mmCtx = null;

function minimapReady() {
  const cv = $('minimap');
  if (!cv) return null;
  if (!mmCtx) mmCtx = cv.getContext('2d');
  return mmCtx;
}

let minimapOpen = true;

function drawMinimap() {
  if (!minimapOpen) return;
  const g = minimapReady();
  if (!g || !ST.mat) return;
  const cv = $('minimap');
  const n = ST.n, half = n / 2;
  const S = cv.width, pad = 4;
  const px = (S - pad * 2) / n;

  const inv = ST.inverted;
  g.clearRect(0, 0, S, S);
  g.fillStyle = 'rgba(6,10,22,0.92)';
  g.fillRect(0, 0, S, S);

  // Streets light, buildings dark — matching the normal reading
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      let dark = ST.mat[r][c] === 1;
      if (inv) dark = !dark;
      g.fillStyle = dark ? 'rgba(150,170,205,0.32)' : 'rgba(12,20,38,0.9)';
      g.fillRect(pad + c * px, pad + r * px, Math.ceil(px), Math.ceil(px));
    }
  }

  // World → map, inverting the very mapping the builder used
  const toMapX = wx => pad + (wx + half - 0.5) * px + px / 2;
  const toMapY = wz => pad + (half - 0.5 - wz) * px + px / 2;

  if (AUTO.path && AUTO.path.length > 1) {
    g.strokeStyle = 'rgba(246,193,75,0.85)';
    g.lineWidth = Math.max(1.2, px * 0.42);
    g.lineJoin = g.lineCap = 'round';
    g.beginPath();
    AUTO.path.forEach((p, i) =>
      i ? g.lineTo(toMapX(p.x), toMapY(p.z)) : g.moveTo(toMapX(p.x), toMapY(p.z)));
    g.stroke();

    const a = AUTO.path[0], b = AUTO.path[AUTO.path.length - 1];
    g.fillStyle = 'rgba(86,211,100,0.95)';
    g.beginPath(); g.arc(toMapX(a.x), toMapY(a.z), px * 0.9, 0, 6.284); g.fill();
    g.fillStyle = 'rgba(247,129,102,0.95)';
    g.beginPath(); g.arc(toMapX(b.x), toMapY(b.z), px * 0.9, 0, 6.284); g.fill();
  }

  // The walker: a heading cone, so the map reads as orientation not just position
  const wx = toMapX(camPersp.position.x), wy = toMapY(camPersp.position.z);
  const fov = 0.6, len = Math.max(7, px * 4.5);
  g.fillStyle = 'rgba(255,255,255,0.16)';
  g.beginPath();
  g.moveTo(wx, wy);
  g.arc(wx, wy, len, -yaw - Math.PI/2 - fov, -yaw - Math.PI/2 + fov);
  g.closePath(); g.fill();

  g.fillStyle = '#ffffff';
  g.beginPath(); g.arc(wx, wy, Math.max(2, px * 0.75), 0, 6.284); g.fill();
}

/* ═══════════════ 12. BOOT ═══════════════ */
window.addEventListener('DOMContentLoaded', async () => {
  let stage = 'start';
  try {
    stage = 'libraries';
    TSCG.ok('════ QRCity build ' + BUILD + ' ════');
    TSCG.log('auto-walk trail: glowing chevrons');
    if (typeof qrcode === 'undefined') throw new Error('qrcode-generator not loaded');
    if (typeof BABYLON === 'undefined') throw new Error('BabylonJS not loaded');
    // qrcode and BabylonJS are required; earcut is not. It only serves the
    // arch geometry, so its absence disables arches rather than the city.
    TSCG.ok('QRCity ' + BUILD + ' — BabylonJS ' + BABYLON.Engine.Version);
    TSCG.log('device pixel ratio ' + (window.devicePixelRatio || 1) +
             ', rendering at ' + (1 / engine.getHardwareScalingLevel()).toFixed(2) + 'x');
    if (typeof earcut === 'undefined')
      TSCG.log('earcut unavailable — arch tunnels disabled, city otherwise intact');

    stage = 'engine';
    const canvas = $('canvas-main');
    // The fourth argument is adaptToDeviceRatio, and it defaults to FALSE.
    // Left off, the WebGL backing store is sized in CSS pixels and the browser
    // then resamples it up to physical pixels: invisible at 100% zoom on a 1x
    // display, but a visible softening at any browser zoom and on every HiDPI
    // screen — at dpr 2 only half the native detail is ever rendered.
    engine = new BABYLON.Engine(canvas, true,
      { preserveDrawingBuffer:true, stencil:true }, true);

    // Rendering at dpr 3 or 4 costs a lot for very little gain, so the scale
    // is clamped. hardwareScalingLevel is the inverse of the ratio: 0.5 means
    // render at twice the CSS resolution.
    const dpr = window.devicePixelRatio || 1;
    engine.setHardwareScalingLevel(1 / Math.min(dpr, 2));
    scene  = new BABYLON.Scene(engine);
    scene.clearColor = new BABYLON.Color4(0.04,0.06,0.10,1);

    camOrtho = new BABYLON.ArcRotateCamera('camOrtho', -Math.PI/2 + ISO_AZ,
                 Math.PI/2 - ISO_EL, 60, BABYLON.Vector3.Zero(), scene);
    camOrtho.mode = BABYLON.Camera.ORTHOGRAPHIC_CAMERA;
    camOrtho.lowerRadiusLimit = 5; camOrtho.upperRadiusLimit = 400;
    // Neutralise the built-in wheel handling: it only moves the camera,
    // which does nothing in orthographic mode.
    camOrtho.inputs.removeByType('ArcRotateCameraMouseWheelInput');
    camPersp = new BABYLON.UniversalCamera('camPersp', new BABYLON.Vector3(0, EYE, 12), scene);
    camPersp.fov = 1.05; camPersp.minZ = 0.05;
    activeCam = camOrtho; scene.activeCamera = camOrtho;
    // Report readability continuously as the user tilts
    camOrtho.onViewMatrixChangedObservable.add(updateReadability);

    lightAmbient = new BABYLON.HemisphericLight('amb', new BABYLON.Vector3(0,1,0), scene);
    lightSun  = new BABYLON.DirectionalLight('sun',  new BABYLON.Vector3(-0.35,-0.85,-0.28), scene);
    lightFill = new BABYLON.DirectionalLight('fill', new BABYLON.Vector3( 0.45,-0.55, 0.40), scene);

    TSCG.engine = engine; TSCG.camera = camOrtho; TSCG.pocletId = 'qrcity';
    TSCG.initSplitter();
    TSCG.ok('Engine ready');

    stage = 'fonts';
    // Sign textures are drawn on a canvas, so the display face must be
    // resident first — otherwise every sign bakes in the fallback serif.
    try {
      if (document.fonts && document.fonts.load) {
        await document.fonts.load('48px "Cantata One"');
        await document.fonts.ready;
        TSCG.ok('Cantata One ready' +
          (document.fonts.check('48px "Cantata One"') ? '' : ' (fallback serif)'));
      }
    } catch (e) { TSCG.log('Font step skipped: ' + e.message); }

    stage = 'stylesheet';
    SS = compileStyle(ST.styleId);
    applySceneStyle();
    TSCG.ok('Stylesheets: ' + QRCITY_STYLE_IDS.join(', '));

    stage = 'city';
    $('text-input').value = DEFAULTS.text;
    $('size-select').value = String(DEFAULTS.forcedN);
    generate(DEFAULTS.text);
    TSCG.ok('City built');

    viewSyncArmed = true;               // the camera now holds a real angle

    stage = 'render loop';
    let prev = performance.now();
    engine.runRenderLoop(() => {
      const now = performance.now(), dt = Math.min((now-prev)/1000, 0.05); prev = now;
      if (ST.mode === 'walk' || ST.mode === 'fly') { tickFree(dt); drawMinimap(); }
      else tickBirdSnap(dt);       // no-op unless the view is overhead
      scene.render();
    });
    // The orthographic frustum is aspect-dependent, so it must be recomputed
    // whenever the canvas container changes shape — not only on window
    // resize. A splitter drag changes the container without any window event,
    // which is what was squashing the view.
    const viewEl = $('view-main');
    const applyScale = () => {
      // Browser zoom and moving to another display both change devicePixelRatio
      const r = window.devicePixelRatio || 1;
      engine.setHardwareScalingLevel(1 / Math.min(r, 2));
    };
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(() => { applyScale(); engine.resize(); fitOrtho(ST.n); }).observe(viewEl);
    } else {
      window.addEventListener('resize', () => { engine.resize(); fitOrtho(ST.n); });
    }
    TSCG.ok('Running');

  } catch (err) {
    TSCG.fail('Startup [' + stage + ']', err.message);
    TSCG.toggleDiag();
  }

  /* ── Controls ── */
  $('btn-build').addEventListener('click', () => generate($('text-input').value.trim() || DEFAULTS.text));
  $('text-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') generate(e.target.value.trim() || DEFAULTS.text);
  });
  $('size-select').addEventListener('change', e => {
    ST.forcedN = parseInt(e.target.value, 10);
    generate($('text-input').value.trim() || DEFAULTS.text);
  });
  $('view-select').addEventListener('change', e => setMode(e.target.value));
  buildStyleSelect();
  $('btn-invert').addEventListener('click', () => {
    ST.inverted = !ST.inverted;
    $('btn-invert').classList.toggle('on', ST.inverted);
    rebuild();
  });
  $('btn-nextseed').addEventListener('click', async () => {
    ST.seed = await sha256Seed(ST.seed);
    rebuild();
    setHint('New seed — same QR plan, different city');
  });
  $('btn-diag').addEventListener('click', () => TSCG.toggleDiag());

  $('minimap-toggle').addEventListener('click', () => {
    minimapOpen = !minimapOpen;
    $('minimap-wrap').classList.toggle('collapsed', !minimapOpen);
    $('minimap-toggle').textContent = minimapOpen ? '\u2212' : '+';
    if (minimapOpen) drawMinimap();
  });

  $('btn-reset').addEventListener('click', () => {
    // Full restore: text, grid, theme, polarity, seed and view.
    //
    // Order matters. setStyle() and generate() both rebuild, and a rebuild
    // reaches syncViewSelect(), which reads the camera's current tilt and
    // writes ST.mode. Setting the view first therefore had it overwritten
    // before it could take effect. The view is restored LAST, explicitly,
    // once nothing else will touch it.
    if (AUTO.on) autoWalkStop();
    $('btn-next-route').classList.remove('on');

    ST.inverted = false;
    $('btn-invert').classList.remove('on');
    ST.forcedN  = DEFAULTS.forcedN;
    orthoZoom   = 1;
    $('text-input').value  = DEFAULTS.text;
    $('size-select').value = String(DEFAULTS.forcedN);

    setStyle(DEFAULTS.styleId);        // unconditional: a guard could skip
    generate(DEFAULTS.text);           // restores the original seed too

    setMode(DEFAULTS.mode);            // last word on the view
    setHint('Reset to defaults');
  });

  $('btn-autowalk').addEventListener('click', () => {
    const b = $('btn-autowalk');
    if (AUTO.on) { autoWalkStop('Auto walk stopped'); return; }
    $('btn-next-route').classList.remove('on');
    if (autoWalkStart(0)) { b.classList.add('on'); b.textContent = 'Stop \u25A0'; }
  });

  $('btn-next-route').addEventListener('click', () => {
    const b = $('btn-autowalk');
    $('btn-next-route').classList.remove('on');
    const next = (AUTO.leg + 1) % 2;
    if (autoWalkStart(next)) { b.classList.add('on'); b.textContent = 'Stop \u25A0'; }
  });

  /* ── Pointer state: the bird snap must not fight an active drag ── */
  const canvasP = $('canvas-main');
  canvasP.addEventListener('pointerdown', () => { pointerDragging = true; });
  window.addEventListener('pointerup',    () => { pointerDragging = false; });
  window.addEventListener('pointercancel',() => { pointerDragging = false; });

  /* ── Orthographic wheel zoom ── */
  const canvasZ = $('canvas-main');
  canvasZ.addEventListener('wheel', e => {
    e.preventDefault();
    const step = Math.exp(-e.deltaY * 0.0012);
    if (ST.mode === 'walk' || ST.mode === 'fly') {
      // Zoom by narrowing the field of view: the observer stays put, which
      // is what a walker expects from a zoom rather than a dolly.
      camPersp.fov = Math.max(0.22, Math.min(1.45, camPersp.fov / step));
    } else {
      orthoZoom = Math.max(0.35, Math.min(14, orthoZoom * step));
      fitOrtho(ST.n);
    }
  }, { passive:false });

  /* ── Free-look ── */
  const canvas = $('canvas-main');
  canvas.addEventListener('click', () => {
    if (ST.mode === 'walk' || ST.mode === 'fly') canvas.requestPointerLock();
  });
  document.addEventListener('mousemove', e => {
    if (document.pointerLockElement !== canvas) return;
    yaw   -= e.movementX * 0.0022;
    pitch  = Math.max(-1.35, Math.min(1.35, pitch - e.movementY * 0.0022));
    applyLook();
  });
  const KEY = { KeyW:'fwd', ArrowUp:'fwd', KeyS:'back', ArrowDown:'back',
                KeyA:'left', ArrowLeft:'left', KeyD:'right', ArrowRight:'right',
                Space:'up', KeyC:'down' };
  window.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
    const free = ST.mode === 'walk' || ST.mode === 'fly';
    if (free && KEY[e.code]) {
      if (AUTO.on) autoWalkStop('Manual control');   // the walker takes over
      MV[KEY[e.code]] = true; e.preventDefault();
    }
    if (e.key === 'Shift') MV.run = true;
    if (e.key === '1') setMode('iso');
    if (e.key === '2') setMode('bird');
    if (e.key === '3') setMode('walk');
    if (e.key === '4') setMode('fly');
    if (e.key === 'i' || e.key === 'I') $('btn-invert').click();
    if (e.key === 'n' || e.key === 'N') $('btn-nextseed').click();
  });
  window.addEventListener('keyup', e => {
    if (KEY[e.code]) MV[KEY[e.code]] = false;
    if (e.key === 'Shift') MV.run = false;
  });
  window.addEventListener('blur', () => { for (const k in MV) MV[k] = false; });

  /* ── Sidebar content from the ontology ── */
  TSCG.renderScores('scores-host', {
    A:0.85, S:0.92, F:0.70, It:0.88, D:0.72,
    R:0.95, E:0.88, V:0.92, O:0.90, Im:0.82
  });
  TSCG.renderConcepts('concepts-host', M2_CONCEPTS);
});

/* ═══════════════ 13. M2 CONCEPTS (from the ontology) ═══════════════ */
const M2_CONCEPTS = [
  { name:'Constraint', formula:'St × A × D | O + V', family:'Regulatory', familyColor:'#f78166',
    desc:'Restriction on possible system states, limiting degrees of freedom.',
    role:'The top-view readability rule — the pivot of the entire system' },
  { name:'Trade-off', formula:'A × I × F', family:'Regulatory', familyColor:'#f78166',
    desc:'Necessary compromise between incompatible objectives.',
    role:'Normal vs inverted polarity: the two readings cannot both hold' },
  { name:'Code', formula:'It × Ss', family:'Informational', familyColor:'#d2a8ff',
    desc:'System of rules for systematic transformation between domains.',
    role:'The QR encoding — and the city as a second encoding of one payload' },
  { name:'Signature', formula:'It × Ss | V', family:'Informational', familyColor:'#d2a8ff',
    desc:'Characteristic pattern enabling unique identification.',
    role:'The seed in hex — what distinguishes one city from another' },
  { name:'Invariant', formula:'S × A', family:'Structural', familyColor:'#56d364',
    desc:'Property preserved under transformation.',
    role:'The module grid: survives every stylesheet, seed and polarity' },
  { name:'Identity', formula:'St × It × A | V + E', family:'Structural', familyColor:'#56d364',
    desc:'Persistent property making an entity distinguishable across transformations.',
    role:'Same text always yields the same city — the seed is its identity card' },
  { name:'Segmentation', formula:'S × I × D', family:'Structural', familyColor:'#56d364',
    desc:'Partition of a whole into distinct but exhaustive regions.',
    role:'The n×n module grid partitioning the plane' },
  { name:'Symmetry', formula:'S', family:'Structural', familyColor:'#56d364',
    desc:'Invariance under transformation.',
    role:'Finder patterns — three corners, not four: broken deliberately so a scanner can resolve rotation' },
  { name:'Topology', formula:'St | L', family:'Structural', familyColor:'#56d364',
    desc:'Structural properties preserved under continuous deformation: connectivity, genus.',
    role:'Arch tunnels add graph edges the flat QR does not have' },
  { name:'Network', formula:'S × I × F', family:'Structural', familyColor:'#56d364',
    desc:'Set of nodes connected by edges enabling distributed interaction.',
    role:'The street connectivity graph' },
  { name:'Layer', formula:'St × It × A | R', family:'Structural', familyColor:'#56d364',
    desc:'Stable ordered positional partition in a stack; co-equal strata.',
    role:'The stylesheet as an interpretation layer over unchanged data' },
  { name:'Space', formula:'St | L', family:'Ontological', familyColor:'#79c0ff',
    desc:'Dimensional framework in which system states and trajectories exist.',
    role:'The city as inhabited extent rather than image' },
  { name:'Transformation', formula:'D × S × I', family:'Dynamic', familyColor:'#e3b341',
    desc:'Change of form, structure or state.',
    role:'Matrix → geometry, and re-interpretation between stylesheets' },
  { name:'Role', formula:'Ss | K', family:'Relational', familyColor:'#ff9edb',
    desc:'Functional position or responsibility within a structure.',
    role:'Finder patterns as civic landmarks; the Democratization facet itself' }
];
