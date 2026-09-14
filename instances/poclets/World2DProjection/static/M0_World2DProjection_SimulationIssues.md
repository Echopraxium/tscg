# World 2D Projection — Simulation Issues & Iteration Log

**Author:** Echopraxium with the collaboration of Claude AI
**Skill:** `tscg-create-instance-simulation` · **Stack:** p5.js (2D Map) + BabylonJS (3D globe)

---

## Round 1 — 2026-09-14 · Interactivity (option A: graticule only)

**Delivered.** Two stacked panels (top = 2D projection / p5.js = the Map; bottom = 3D globe /
BabylonJS = the Territory, neutral beige). Shell chrome reused unchanged; `#view-main`
re-styled into a vertical stack by `World2DProjection.css`.

Implemented:
- 5 forward projections (exact, closed-form except Robinson's lookup table): Mercator,
  Mollweide, Azimuthal Equidistant (polar aspect), Robinson, Gall-Peters.
- Exact area-distortion choropleth on graticule cells: `rNorm = (aMap/aSphere)` normalised
  so the whole-map mean ≈ 1; diverging cyan → grey → magenta; intensity in `log`; τ neutral band.
- Auto switch to **shape** distortion (Tissot a/b, numeric) when the active projection is
  equal-area (Mollweide, Gall-Peters) — otherwise the choropleth would read "all faithful".
- Animated **morphing** between projections (700 ms lerp of vertex positions + cell metric);
  the globe does NOT move — only the Map morphs (the epistemic gap animated).
- Zone selection by **clicking the globe** → thick black cell contour + Triz-style rotation
  (slerp) bringing the centroid to face the camera + area/shape read-out on the Map.
- Controls: projection select, τ slider, hue mode (auto/area/shape), graticule cell size,
  auto-rotate, reset. Always-visible Map legend.
- Sidebar: **canonical** ASFID/REVOI scores + δ₁ badge (see reconciliation below).

### Reconciliation — gap badge (shell vs M0, M0 authoritative)
The shell's `TSCG.renderScores` computes the gap as the **raw** `|REVOI_mean − ASFID_mean|`
= `|0.86 − 0.62|` = **0.24 → "Divergent"**, and uses the class labels
Coherent/OnCriticalLine/Divergent/Enigmatic. The committed **M0** graves the canonical scalar
`δ₁ = |0.62 − 0.86| / √2 = **0.17 → "Liminal"**` (band 0.15 ≤ δ₁ < 0.30). For THIS poclet the
M0 is authoritative, so the simulation renders **0.17 / Liminal** via its own
`renderCanonicalScores` (not the shell's `renderScores`).
→ *Separate template lot (not this Step 4):* the shell's gap formula (missing `/√2`) and its
spectral vocabulary diverge from the M0 convention. Worth a `tscg-ontology-diagnosis`-style
fix on `_00_template/src/tscg-shell.js` so every future poclet inherits the correct scalar.

### Known limitations / deferred (Round 2–3)
- **No continents (Round 2, option B).** Add embedded coarse land outlines for recognisability
  (Greenland vs Africa) + the Arctic flagship demo (polar cap zone).
- **Cell area = shoelace with K=4 edge subdivision** (polygon follows curved meridians).
  Validated: Mollweide rNorm spread 1.34 → **1.02**, Gall-Peters exact 1.000. Residual is the
  K=4 chording; raise K if a finer graticule ever needs it.
- **Robinson interpolation is linear** between 5° table rows (Round 1). Round 3: Snyder's
  higher-order (Aitken/Neville) interpolation for a smoother graticule.
- **GL line width.** Globe graticule and selection contour use `LineSystem`/`CreateLines`,
  whose width is not reliably controllable in WebGL. Round 3: GreasedLine or thin tubes for a
  genuinely "thick" black selection contour.
- **`AREA_DMAX = log(8)` / `SHAPE_DMAX = log(4)`** saturation caps are hand-set for contrast;
  revisit once continents are in (Round 2) to keep the Arctic reading legible.
- **Horizontal split fixed at 50/50.** A draggable horizontal splitter between Map and globe
  is a Round-3 polish item.
- **Triz camera direction snapshotted at click.** If the user orbits after selecting, the
  facing is not re-solved. Round 3: re-solve on orbit end, or track continuously.

### Validation
- `node --check` on `src/World2DProjection.js`: (see session log)
- ESLint (`.eslintrc.json`, browser env, BABYLON/p5/TSCG globals): (see session log)
- Projection maths sanity (node): equal-area check (Gall-Peters, Mollweide → rNorm≈1),
  Mercator polar area blow-up, Azimuthal centre-distance. (see session log)
- Visual/manual testing: **pending Michel** (serverless — open `M0_World2DProjection.html`).

---

## Round 2 — 2026-09-14 · Pedagogy (option B: coarse continents + Arctic)

**Delivered (additive over Round 1).**
- Embedded **coarse continent outlines** (hand-simplified, public-domain, low-res):
  Greenland, Africa, Eurasia, North America, South America, Australia. Drawn as
  outlines on BOTH panels — on the beige globe (neutral sepia) and over the map
  choropleth (so Greenland's balloon on Mercator is legible against the magenta field).
- **Selection is now by ZONE**, per the spec ("zones not points"): clicking the globe
  hit-tests continents (point-in-polygon) and the polar caps; falls back to a graticule
  cell only outside any zone. A **Zone** combo + a one-click **Arctic ★** button (the
  flagship: Mercator explodes at the pole, Azimuthal-Equidistant polar shows it clean).
- **Zone area distortion** measured exactly: spherical polygon area (Chamberlain-Duquette)
  for continents, analytic cap area `2π(1−sin|φ|)` for the polar caps; projected area by
  shoelace; normalised by the projection's global area scale. Read-out shows area ×r and
  shape a/b for the selected zone.
- **Coastlines** toggle (globe mesh enable/disable + map overlay).

### Validation (Node)
- `sphericalPolygonArea` vs exact graticule-quad area: diff ≤ 3e-16. ✓
- Zone rNorm: **Mercator inflates Greenland ×4.11, shrinks Africa ×0.36** (the classic
  Greenland≈Africa illusion); equal-area Gall-Peters 1.00/1.00, Mollweide 0.92/1.01
  (residual = coarse continent vertices at high latitude; equal-area shows shape mode anyway). ✓
- `node --check` + ESLint (browser env, BABYLON/p5/TSCG globals): 0 errors, 0 warnings. ✓

### Deferred to Round 3 (polish)
- Continent edges are NOT subdivided for the zone-area shoelace (unlike graticule cells),
  hence the small Mollweide-Greenland residual (0.92). Subdivide if a precise EqualArea
  read-out is wanted; cosmetic today since equal-area auto-switches to shape hue.
- GL line width (thick black selection contour), fixed 50/50 Map/Globe split, and the
  Robinson linear interpolation remain Round-3 items (see Round 1 log).
- Continents avoid the ±180° dateline by construction (no wrapping logic yet).
- Visual/manual testing: **pending Michel**.
