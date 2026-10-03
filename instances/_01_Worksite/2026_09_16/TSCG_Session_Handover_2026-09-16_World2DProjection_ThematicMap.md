# TSCG Session HandOver — `World2DProjection` poclet · Step 4 (Simulation) — Thematic-map redesign (Passes A + B done)

**Date**: 2026-09-16 · **Author**: Echopraxium with the collaboration of Claude AI
**This session did**: turned the `World2DProjection` simulation into a **geographic thematic map**.
- **Pass A** — 2D map: blue oceans + **per-zone area-distortion choropleth** over Natural Earth countries/states, thin borders, light graticule, blue lakes; legend reworded.
- **Pass B** — 3D globe: **blue oceans + beige land + blue lakes**, coloured **per vertex** (perfectly aligned with the borders); country borders on top.
- New sim data: `W2P_ZONES.js` (countries + states) and `W2P_LAKES.js`. Old `W2P_COASTLINE.js` superseded.
- Committed and pushed.

**Next session goal**: **Pass C — zone selection + globe↔map linking (TRIZ-style)**, then **Pass D — layout redesign**, an **Antarctica rendering fix**, and **Pass E — projection-catalogue expansion**. §3 integrates Michel's 7 remarks.

---

## 0. Bootstrap (do this first)

1. Load skills by name: `head-over-memory`, `tscg-create-instance-simulation` (+ `tscg-instance-pipeline` for Step-4 context).
2. Fetch the Smart Prompt from HEAD (`docs/reboot-kit/TSCG_SmartPrompt.md`) and follow it.
3. **HEAD is the only authority.** Re-verify every fact (files, SHA, anchors) from HEAD before relying on it:
   `git fetch --depth 1 origin main && git reset --hard origin/main`. This document is a pointer, not a source of truth.

---

## 1. Committed state

- **HEAD** at hand-off: **`c5fdefa`** — *"fix(World2DProjection): hue legend moved into left panel (CSS follow-up to A+B)"*, on top of **`93144af`** *"feat(World2DProjection): thematic per-zone choropleth (A) + blue geographic globe (B)"*. Confirm current HEAD with `git log -1`.
- Poclet at `instances/poclets/World2DProjection/`. Simulation under **`static/`** (NOT `_static/` — a stale local copy existed once):
  - `M0_World2DProjection.html` — shell + left controls + two panels + right tabs. Loads, in order: `tscg-shell.js`, **`src/W2P_ZONES.js`**, **`src/W2P_LAKES.js`**, `src/World2DProjection.js`.
  - `src/World2DProjection.js` — the whole engine (5 projections + morph; p5 map; Babylon globe).
  - `src/W2P_ZONES.js` — **473 zones** (287 states / 186 countries). Natural Earth 50m admin-0 + admin-1, simplified 0.15°, exterior rings, dateline-aware, 2-dp. Each zone `{n:name, a:adminCountry, l:level(0 country/1 state), c:[lon,lat] repr-point, p:[ring,…]}`. **Sim data, NOT M0.**
  - `src/W2P_LAKES.js` — **244 major lake rings** (NE 50m lakes). Sim data.
  - `src/World2DProjection.css`, `src/tscg-shell.{css,js}`, `.eslintrc.json`, `_00_serve_poclet-sim.bat`, `M0_World2DProjection_SimulationIssues.md`.
- **Ontology UNCHANGED**: `M0_World2DProjection.jsonld` was not touched. **M0 gate not required** (the sim is a client of M0). Verified: commit `93144af` changed only sim files + FileTree, no `.jsonld`/`.ttl`.
- `W2P_COASTLINE.js` is superseded by the zones; it was never git-tracked — delete any local untracked copy.

---

## 2. What's done & verified (A + B)

- **2D map**: blue oceans (fill of the projected map boundary) · **per-zone choropleth** — each country/state tinted by its **area distortion**, sampled from the normalized `rNorm` field at the zone centroid (`cellAtDeg`), quantized into `CHORO_CLASSES = 5` diverging classes · thin borders · light graticule overlay · blue lakes. Legend = "AREA distortion per zone".
  Verified data-driven: **Azimuthal** → concentric rings, **Gall-Peters** → all grey (equal-area = faithful), **Mercator** → poles magenta / equator cyan.
- **3D globe**: sphere `segments: 160`, vertex-coloured ocean/land/lake by each vertex's own lat/lon (`lat=asin(y/R)`, `lon=atan2(z,x)`) → aligns exactly with the border lines (same `llToXyz` frame). Material `diffuseColor` white so vertex colours show. Country borders drawn on top.
- **Data**: `W2P_ZONES` (473), `W2P_LAKES` (244). Zone parents that carry states: **USA(50) · Russia(84) · China(31) · Brazil · Canada · India · Indonesia · Australia · South Africa**.

---

## 3. NEXT — remaining work (Head-Chef piloted, ⏸ after each pass). Michel's 7 remarks are mapped here.

### Pass C — Zone selection + globe↔map linking  [Michel #1, #2, #3, #4]
**Root cause of #1 (coarse selection that ignores the real borders):** the OLD selection model is still live — `state.selection = {cont|cap|cell}` over the **crude 8–20-point `CONTINENTS` blobs**. The black outline seen in the screenshots is that blob (e.g. "Eurasia"), not the real polygons. Migrate to a zone model:
- **`state.selZone`** = a `W2P_ZONES` entry (or `null`). Remove `cont/cap/cell`, `CONTINENTS`/`CAPS`, `zoneAtLatLon`, `selectZoneByName`, `selectionRingRad`.
- **Highlight follows the REAL polygon on BOTH sides (#1):**
  - `drawSelectionMap` → draw `selZone` rings (via `splitRingDeg`, thick bright stroke).
  - `drawGlobeSelection` → draw `selZone` rings on the sphere (bright, at `R*1.005`). NOTE: the item-1 **tube** was built for the old blob ring; for a many-vertex real zone use a bright `CreateLineSystem` (or GreasedLine) — reconsider tube vs line.
- **Granularity = countries + states (#2):** already in the data/display for the 9 federal countries incl. **USA/China/Australia/Russia**. Make selection operate at that granularity; repopulate the zone `<select>` with `W2P_ZONES` grouped by parent country (`<optgroup>`). *If Argentina/Mexico/Kazakhstan states are also wanted, they are absent from NE 50m admin-1 → would need NE 10m admin-1 (heavier).* Confirm with Michel before pulling 10m.
- **Globe orient-to-user (#3):** on select, `trizTo(selZone.c)` — slerp the zone centroid to face the camera. The `trizTo`/`quatFromTo` slerp already exists; wire it through `afterSelect` → `selectionCentroid` → `zone.c`.
- **Bidirectional sync (#4):**
  - **map click → globe**: store the map `SX/SY` transform in `state` during `p.draw`; on `p.mousePressed`, project each zone ring to screen and point-in-polygon in **screen space** → set `selZone` → highlight both + orient globe.
  - **globe click → map**: repoint the existing `scene.onPointerObservable` (already converts pick → local xyz → lat/lon) to `zoneAt(lon,lat)` → `selZone` → highlight both + orient.
  - *(Stretch, harder half of the original "rotate → select": auto-select the zone at the sub-camera point during drag/on drag-end. Optional.)*
- **Reference the TRIZ instance** for 3D picking + rotation-to-user: `instances/systemic-frameworks/Triz/` — read from HEAD before coding (Michel explicitly pointed here).
- Update `afterSelect` / `updateSelReadout` / `selectionDistortion` / `zoneLabel` to be zone-based (name + parent country + its area/shape distortion).

### Pass D — Layout redesign  [Michel #5]
Current layout (Layout1) wastes horizontal space around a small centred map and a small centred globe. Target (Layout2):
- **2D map = LARGE, left column, full height, wide** — this also fully solves the old "wider map" request (the square-in-a-short-panel letterbox disappears when the map panel is tall).
- **Right column = Hue-legend panel (top) + 3D globe (bottom).**
- Decide where the **left controls** (Projection/Distortion/Hue/Graticule/Zone/Globe) and the **right Description/ASFID/Concepts/README tabs** go (Layout2 is a crop that omits them) — likely keep controls as a narrow left rail and keep the tabs reachable (below / toggle). Restructure `#view-main`, the panels, `#map-legend`, and the globe canvas placement in HTML + CSS. Map fit becomes width-driven in a tall panel.

### Bug — Antarctica pole-enclosing polygon  [Michel #6]
Antarctica is a **pole-enclosing ring**: lon −180→180, lat down to −90, 87 parts. On cylindrical projections (Mercator `latMax=85°`, Gall-Peters) the per-zone fill renders as a **bowtie / crossed triangles** (the yellow box in Layout2). This is a **bug**, not intended.
Fix: detect a ring that spans the full longitude and reaches |lat|→90, and **close the fill along the map's bottom (south) edge** (insert corner vertices at the projection's south limit across the width), or clip the polygon to the projection domain before filling. Map-side only (the globe/sphere is fine). Do it with Pass D or as a standalone quick fix — it's a visible eyesore.

### Pass E — Projection catalogue 20–40  [Michel #7]
Currently **5** projections: Mercator, Mollweide, Azimuthal Equidistant, Robinson, Gall-Peters. Michel wants **20–40** (cf. https://map-projections.net/singleview.php) — the scalar-parameter families are not enough for him. Two routes:
- **(a) Hand-code forward formulas** into the existing engine — keeps the custom **morph** + **per-cell area** machinery; ~work per projection. Candidates: Equirectangular, Miller, Cylindrical Equal-Area, Sinusoidal, Eckert I–VI, Hammer, Aitoff, Winkel Tripel, Kavrayskiy VII, Wagner VI, Natural Earth, Patterson, Van der Grinten, Stereographic, Orthographic, Gnomonic, Lambert Conformal Conic, Albers, Bonne, Werner, Cassini, Loximuthal, Sinusoidal…
- **(b) Integrate `d3-geo-projection`** (150+ ready) — but it reworks `rawProj`, the morph, and the per-cell area around d3 projections. Evaluate the trade-off first.
Big pass; do **after** C and D.

---

## 4. Reminders / invariants (unchanged)

- **The sim is a CLIENT of M0.** Zones/lakes/coastlines are simulation DISPLAY data, **never M0 instances** (countries are not M0). Links point up M0→M1→M2→M3. **M0 gate not required while the `.jsonld` is untouched.**
- **Globe = the Territory = the truth → no distortion tint** (blue oceans + neutral land + selection highlight). The area-distortion choropleth lives on the **Map only**.
- Notation: GenericConcept formulas use `×` `+` `|` only — `⊗` never.
- Generated files in **English**; conversation in **French**. `dcterms:creator = "Echopraxium with the collaboration of Claude AI"`.
- Serve via `_00_serve_poclet-sim.bat` (http://127.0.0.1). The `file://` self-load console error is benign; the `babylon.js.map` CSP source-map error is benign (add `https://cdn.babylonjs.com` to the `connect-src` meta for a clean console if wanted).

---

## 5. Rendering points to re-verify

- Per-zone colour is sampled at the centroid inside a **15° cell** → **one colour per zone** (states mitigate this for the big federal countries; large single-zone countries get an average value).
- Ocean **perimeter fill** on **Azimuthal** (possible slit along ±180°) and on the ellipse projections.
- Globe border/coast **softness** (vertex colours at 160 segments ≈ 1.4°; the drawn borders sharpen it). Raise tessellation or switch to a texture if crisper coasts are wanted.
- **Morph performance** (many polygons projected per frame).
- Deferred (older `SimulationIssues`): Robinson higher-order interpolation; saturation-cap recalibration; and the **template-side `renderScores` δ₁ fix** (raw `|mean−mean|` = 0.24 → "Divergent" vs the M0 `δ₁ = |·|/√2` = 0.17 → "Liminal") on `_00_template/src/tscg-shell.js` — a separate lot, not this poclet.
