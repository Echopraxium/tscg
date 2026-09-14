# TSCG Session HandOver — `World2DProjection` poclet · Step 4 (Simulation) — Rounds 1–2

**Date**: 2026-09-14 · **Author**: Echopraxium with the collaboration of Claude AI
**This session did**: **Step 4 — built the standalone HTML simulation, Rounds 1 (interactivity) + 2 (pedagogy).** Two-panel serverless sim under `instances/poclets/World2DProjection/static/`; ESLint clean; projection maths validated in Node. Michel saved all files locally. **Commit + regenerated `TSCG_FileTree.md` prepared** (see §1).
**Next session goal**: **Step 4 — Round 3 (polish)**, then optionally **publish** (open a repo issue).

---

## 0. Bootstrap (do this first)

1. Load skills by name: `head-over-memory`, `tscg-create-instance-simulation` (+ `tscg-instance-pipeline` for Step-4 context).
2. Fetch the Smart Prompt from HEAD (`docs/reboot-kit/TSCG_SmartPrompt.md`) and follow it.
3. **HEAD is the only authority.** Re-verify every fact (files, SHA, M0 anchors/scores) from HEAD before relying on it. This document is a pointer, not a source of truth.

---

## 1. Commit & FileTree (Head-Chef action on your machine)

The files are already in your working tree (you saved them). To commit + refresh the FileTree:

```bash
cd <your tscg clone>
git add instances/poclets/World2DProjection/static
python tscg_generate_filetree.py          # rewrites docs/reboot-kit/TSCG_FileTree.md from git ls-files
git add docs/reboot-kit/TSCG_FileTree.md
git commit -m "feat(World2DProjection): Step 4 standalone simulation (Rounds 1-2) + FileTree"
git push origin main
```

Then **reload `docs/reboot-kit/TSCG_FileTree.md` into Project Knowledge** (it is a drift-prone resident copy; owner maintenance). A regenerated copy from this session is attached — but prefer regenerating on your own up-to-date clone so the tree is exact.

> Note: the FileTree regenerated here reports **1761 tracked files** (was 1752), i.e. the 8 new `static/` files + the 2026-09-13 HandOver. `tscg_generate_filetree.py` reads `git ls-files`, so the new files must be `git add`-ed **before** running it.

---

## 2. Fresh session state

- **Current HEAD**: confirm with `git show HEAD` after your push (the commit from §1).
- **Committed poclet** at `instances/poclets/World2DProjection/`:
  - `M0_World2DProjection.jsonld` — the model (classification + metadata; **no projection math**).
  - `M0_World2DProjection_README.md` — incl. the Theorema-Egregium proof.
  - `M0_World2DProjection_analysis.md` — Step-2 record + **consolidated simulation spec** (§ "Simulation design").
  - **`static/`** (this session):
    - `M0_World2DProjection.html` — shell chrome + two stacked panels.
    - `src/World2DProjection.js` — the whole engine (Rounds 1+2).
    - `src/World2DProjection.css` — two-panel layout + distortion colour grammar.
    - `src/tscg-shell.{css,js}` — copied verbatim from `_00_template/` (autonomy; not edited).
    - `.eslintrc.json`, `_00_serve_poclet-sim.bat`, `M0_World2DProjection_SimulationIssues.md`.
- **Gate open**: none. This step touched no ontology, so **no M0 gate re-run needed** (M0/SHACL/check_m0 were already green at Step 3). SC-6 / golden-debt items remain pre-existing and NOT ours.
- **In flight**: nothing (files saved).

---

## 3. What the simulation already does (verified)

- **BOTTOM = 3D globe (BabylonJS)** = Territory: uniform beige sphere, dark graticule, coarse
  coastlines (sepia); **click a continent / polar cap → zone selection** (black contour +
  Triz slerp bringing the centroid to face the camera); auto-rotate.
- **TOP = 2D projection (p5.js)** = Map: exact **area-distortion choropleth** on graticule cells
  (cyan under · grey faithful · magenta over), intensity in log, **τ slider** neutral band;
  coastlines overlaid so the distortion is recognisable.
- **Auto-switch to shape** distortion (Tissot a/b) when the active projection is equal-area
  (Mollweide, Gall-Peters); manual hue override; always-visible legend.
- **Morphing** between projections (globe fixed, only the Map morphs = the epistemic gap animated).
- **5 forward projections**: Mercator, Mollweide, Azimuthal Equidistant (polar), Robinson, Gall-Peters.
- **Zone area** exact: spherical polygon (Chamberlain-Duquette) for continents, `2π(1−sin|φ|)` for caps.
- **Sidebar**: canonical **δ₁ = 0.17 / Liminal** rendered from M0 (own renderer, NOT the shell's `renderScores`).
- **Validation (Node)**: ESLint 0/0; Gall-Peters equal-area exact (spread 1.000); Mollweide 1.02;
  Mercator polar inflation ~35× at 80°N; **Mercator Greenland ×4.11 / Africa ×0.36** (the illusion, quantified);
  `sphericalPolygonArea` matches exact quad to ≤3e-16.

---

## 4. NEXT — Round 3 (polish). Michel-piloted, ⏸ after each pass.

From `M0_World2DProjection_SimulationIssues.md` (authoritative list):
1. **Thick black selection contour** — replace `LineSystem`/`CreateLines` (GL width uncontrollable)
   with GreasedLine or thin tubes on the globe; thicker map outline already OK.
2. **Horizontal Map/Globe splitter** — currently fixed 50/50; add a draggable divider.
3. **Robinson interpolation** — currently linear between 5° rows; use Snyder's higher-order
   (Aitken/Neville) for a smoother graticule.
4. **Saturation caps** (`AREA_DMAX=log 8`, `SHAPE_DMAX=log 4`) — recalibrate now that continents
   are visible, so the Arctic reads legibly without clipping.
5. **Continent edge subdivision** for the zone-area shoelace (removes the Mollweide-Greenland 0.92
   residual); cosmetic, since equal-area auto-switches to shape hue.
6. **Dateline wrapping** — continents currently avoid ±180° by construction; add wrap handling if a
   Pacific-centred aspect is ever wanted.

**Then (optional) publish**: open an issue on `github.com/Echopraxium/tscg/issues` with the poclet.

---

## 5. Reminders / invariants

- **The sim is a CLIENT of M0.** Code derives from the committed M0 (5 anchors + facet values);
  links point up (M0→M1→M2→M3). M0 is never a rival source of truth. Do NOT reify morph frames as M0 instances.
- **Colour grammar (no collisions)**: cyan/magenta/grey = distortion (2D Map) · thick black = selection ·
  beige = neutral globe (Territory).
- **Notation**: GenericConcept formulas use `×` `+` `|` only — `⊗` never appears.
- **Data = simulation, not ontology**: coastlines are coarse, hand-simplified, public-domain; countries
  are NOT M0 instances.
- **Open template-side lot (NOT this poclet)**: the shell's `renderScores` computes the gap as raw
  `|mean−mean|` = 0.24 → "Divergent" and uses Coherent/OnCriticalLine/Divergent/Enigmatic labels,
  whereas the M0 convention is `δ₁ = |·|/√2` with the Liminal spectral band. Worth a
  `tscg-ontology-diagnosis`-style fix on `_00_template/src/tscg-shell.js` so every future poclet
  inherits the correct scalar. Track separately from World2DProjection.
