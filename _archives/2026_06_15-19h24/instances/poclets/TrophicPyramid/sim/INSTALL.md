# TSCG Simulation — Trophic Pyramid
## Installation & Setup (v2.0 — BabylonJS 3D)

**Author:** Echopraxium with the collaboration of Claude AI

---

## Quick Start

```bash
# From the tscg/ repository ROOT:

# 1. Install dependencies (one-time for all simulations)
npm install

# 2. Copy BabylonJS to the sim lib/ folder
mkdir -p instances/poclets/TrophicPyramid/sim/lib
cp node_modules/babylonjs/babylon.js instances/poclets/TrophicPyramid/sim/lib/

# 3. Launch
npm run sim:trophic
```

---

## Root package.json scripts (tscg/package.json)

```json
{
  "name": "tscg-simulations",
  "scripts": {
    "sim:trophic" : "electron instances/poclets/TrophicPyramid/sim",
    "sim:vco"     : "electron instances/poclets/vco/sim",
    "sim:phase"   : "electron instances/poclets/phase-transition/sim"
  },
  "devDependencies": { "electron": "^29.0.0" },
  "dependencies":    { "babylonjs": "^6.0.0" }
}
```

## File Structure

```
tscg/                           ← repository root
  package.json                  ← ONE npm config for all sims
  poclets_registry.js           ← Poclet Explorer registry
  node_modules/
    babylonjs/babylon.js        ← installed once
    .bin/electron               ← installed once
  explorer/
    index.html                  ← Poclet Explorer UI
  instances/poclets/TrophicPyramid/sim/
    main.js                     ← Electron process  [TEMPLATE]
    index.html                  ← UI layout         [TEMPLATE]
    styles.css                  ← TSCG design system[TEMPLATE]
    metadata.js                 ← Poclet data       [POCLET-SPECIFIC]
    renderer.js                 ← BabylonJS scene   [POCLET-SPECIFIC]
    package.json                ← { "main": "main.js" } only
    lib/
      babylon.js                ← local copy (copied from node_modules)
```

## Adding a new simulation

1. Copy the `sim/` folder to your new poclet directory
2. Replace `metadata.js` and `renderer.js`  
3. Copy `lib/babylon.js` (or `lib/p5.min.js` if using P5.js)
4. Add an entry to `tscg/poclets_registry.js`
5. Add a script to `tscg/package.json`: `"sim:myname": "electron instances/..."`
