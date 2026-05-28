# TSCG Simulation Migration Guide
## Python/Pygame → Electron + P5.js

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 1.0.0 · **Date:** 2026-03-13  
**Applies to:** All `instances/` simulations (poclets, transdisclets, tscg-tools)

---

## 1. Motivation

Python/Pygame simulations have four structural limitations for TSCG:

| Problem | Impact |
|---------|--------|
| No native GUI widgets (buttons, sliders, tabs) | UI built from rectangles/text = fragile, ugly |
| Unicode rendering unreliable (⊗, →, Φ, Ψ) | Mathematical symbols corrupt on some platforms |
| No HTML/CSS layout | Sidebar, tabs, info panels require hundreds of lines of pygame code |
| No hyperlinks / README display | Cannot show poclet documentation inline |

**Electron + P5.js** solves all four: CSS handles layout, HTML handles text/tabs/sidebar, P5.js handles the animated canvas, and Unicode is trivially supported everywhere.

---

## 2. Template Architecture (fixed — reuse across all simulations)

```
sim_name/
├── main.js         ← Electron process    [NEVER MODIFY]
├── styles.css      ← TSCG design system  [NEVER MODIFY]
├── index.html      ← Layout shell        [LIGHT ADAPTATION]
├── metadata.js     ← Poclet data         [REPLACE PER POCLET]
├── renderer.js     ← P5.js sketch        [REPLACE PER POCLET]
├── package.json    ← npm config          [UPDATE name/desc]
└── lib/
    └── p5.min.js   ← Local P5.js copy
```

**The invariant:** `main.js` and `styles.css` are **identical** in every simulation.  
`index.html` only changes in the header chips and sidebar tab content.  
`metadata.js` and `renderer.js` are the only poclet-specific files.

---

## 3. Migration Checklist (per simulation)

### Step 1 — Copy the template
```bash
cp -r trophic_pyramid_sim/  new_poclet_sim/
cd new_poclet_sim/
```

### Step 2 — Create `metadata.js`

Extract from your `M0_xxx.jsonld`:

```javascript
const POCLET_METADATA = {
  id: 'M0_YourPoclet',
  label: 'Your Poclet Name',
  version: '1.0.0',
  domain: 'Your Domain',
  type: 'Poclet',           // or 'TransDisclet' / 'TscgTool'

  synergy: {
    formula: 'YourCombo = Domain ⊙ (ConceptA ⊗ ConceptB)',
    compiledTensor: 'X ⊗ Y ⊗ Z',
    emergentProperty: 'Description of emergent property',
  },

  asfid: { A: 0.0, S: 0.0, F: 0.0, I: 0.0, D: 0.0, mean: 0.0 },
  revoi: { R: 0.0, E: 0.0, V: 0.0, O: 0.0, I: 0.0, mean: 0.0 },
  epistemicGap: 0.0,

  primaryGenericConcepts: [ /* ... */ ],
  secondaryGenericConcepts: [ /* ... */ ],

  // Simulation-specific data (poles, states, parameters...)
  poles: [ /* ... */ ]
};

if (typeof module !== 'undefined') module.exports = { POCLET_METADATA };
```

### Step 3 — Write `renderer.js`

Minimal P5.js structure:

```javascript
'use strict';

const SIM = { running: true, speed: 1.0, time: 0 };

new p5(function(p) {
  let W, H;

  p.setup = function() {
    const el = document.getElementById('canvas-area');
    W = el.offsetWidth; H = el.offsetHeight;
    p.createCanvas(W, H).parent('canvas-area');
    p.frameRate(60);
  };

  p.windowResized = function() {
    W = document.getElementById('canvas-area').offsetWidth;
    H = document.getElementById('canvas-area').offsetHeight;
    p.resizeCanvas(W, H);
  };

  p.draw = function() {
    if (!SIM.running) return;
    SIM.time += SIM.speed;
    p.background(13, 17, 23);
    // --- YOUR SIMULATION HERE ---
  };

  p.mousePressed = function() {
    // --- OPTIONAL INTERACTION ---
    window.dispatchEvent(new CustomEvent('element-selected', { detail: { id: null } }));
  };

}, 'canvas-area');

// Wire up controls
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-play').addEventListener('click', () => {
    SIM.running = !SIM.running;
    /* update button state */
  });
  document.getElementById('btn-reset').addEventListener('click', () => {
    SIM.time = 0;
    /* reset simulation state */
  });
  document.getElementById('speed-slider').addEventListener('input', (e) => {
    SIM.speed = parseFloat(e.target.value);
    document.getElementById('speed-label').textContent = `×${SIM.speed.toFixed(1)}`;
  });
});
```

### Step 4 — Adapt `index.html`

Only three zones need updating:

```html
<!-- 1. Header chips -->
<span class="chip domain">YOUR DOMAIN</span>
<span class="chip type">m3:Poclet</span>   <!-- or TransDisclet / TscgTool -->
<span class="chip version">v1.0.0</span>

<!-- 2. Scores panel — update values -->
<div class="score-bar-fill" style="width:85%;background:var(--col-A)"></div>
<!-- etc. for all 10 dimensions -->

<!-- 3. Tab content (Concepts / Synergy / Notes) -->
<!-- Copy structure from trophic_pyramid's index.html and replace text -->
```

### Step 5 — Update `package.json`

```json
{
  "name": "tscg-yourpoclet-sim",
  "description": "TSCG Simulation — YourPoclet",
  "_tscg": {
    "pocletId": "M0_YourPoclet",
    "synergy": "YourCombo = Domain ⊙ (A ⊗ B)"
  }
}
```

---

## 4. Pygame → P5.js Translation Reference

### Coordinate system
| Pygame | P5.js |
|--------|-------|
| `surface.get_width()` | `p.width` (or canvas `el.offsetWidth`) |
| `pygame.draw.rect(surf, color, (x,y,w,h))` | `p.rect(x, y, w, h)` |
| `pygame.draw.circle(surf, color, (cx,cy), r)` | `p.ellipse(cx, cy, r*2)` |
| `pygame.draw.line(surf, color, pt1, pt2)` | `p.line(x1,y1,x2,y2)` |
| `screen.fill((13,17,23))` | `p.background(13,17,23)` |
| `font.render(text, True, color)` | `p.text(text, x, y)` after `p.fill(r,g,b)` |
| `pygame.time.get_ticks()` | `SIM.time` (frame counter) |
| `clock.tick(60)` | `p.frameRate(60)` in `setup()` |

### Colors
```javascript
// Pygame: (r, g, b)      P5.js: p.fill(r, g, b) or p.fill(r, g, b, alpha)
// Pygame: (r, g, b, a)   P5.js: p.fill(r, g, b, a)   [a: 0-255]

// CSS variable → use in HTML/CSS; in P5 use hex2rgb helper:
function hex2rgb(hex) {
  return [parseInt(hex.slice(1,3),16), parseInt(hex.slice(3,5),16), parseInt(hex.slice(5,7),16)];
}
```

### FSM (Finite State Machine) pattern
The pygame FSM approach maps directly:
```javascript
// Pygame (Python)             →  P5.js (JavaScript)
# class SimState(Enum):           const STATE = {
#   IDLE = 'idle'                   IDLE: 'idle',
#   RUNNING = 'running'             RUNNING: 'running',
#   PAUSED = 'paused'               PAUSED: 'paused'
#   CASCADE = 'cascade'             CASCADE: 'cascade'
                                  };
# self.state = SimState.IDLE     let currentState = STATE.IDLE;

# if self.state == SimState.CASCADE:   if (currentState === STATE.CASCADE) {
#     self._update_cascade()               updateCascade();
```

### Controls (the big win vs pygame)
```html
<!-- Pygame: 50 lines of pygame.draw.rect + mouse collision detection -->
<!-- Electron: -->
<button class="ctrl-btn" id="btn-play">▶ Play</button>
<input type="range" id="speed-slider" min="0.2" max="3.0" step="0.2" value="1.0">
```

---

## 5. Existing Simulations — Migration Priority

| Simulation | File | Status | Notes |
|-----------|------|--------|-------|
| Phase Transition | `phase_transition_sim.py` | 🔄 TO MIGRATE | FSM architecture — direct translation |
| VCO | `vco_sim.py` | 🔄 TO MIGRATE | Oscilloscope display → P5.js canvas |
| Color Synthesis | `color_synthesis_sim.py` | 🔄 TO MIGRATE | Color wheel → P5.js ellipses |
| Kindleberger-Minsky | (Python) | 🔄 TO MIGRATE | Timeline chart → P5.js / Chart.js |
| TSCG Explorer | `tscg_explorer.py` | 🔄 TO MIGRATE | Network graph — P5.js or D3.js |
| Trophic Pyramid | `trophic_pyramid_sim/` | ✅ DONE | Template reference |

### Migration complexity estimate

| Complexity | Criterion | Examples |
|-----------|-----------|---------|
| **Low** (1–2h) | FSM + simple shapes | Phase Transition, VCO |
| **Medium** (3–4h) | Custom graphics + interaction | Color Synthesis, Kindleberger |
| **High** (1–2 days) | Complex network graph, 3D | TSCG Explorer (consider D3.js) |

---

## 6. 3D Note — When to use BabylonJS

Use **BabylonJS** instead of P5.js when the system requires genuine 3D:
- Molecular structures (Chemistry poclets)
- 3D phase space (Phase Transition in 3D)
- Spatial ecosystem models

```html
<!-- In index.html, replace P5 with BabylonJS: -->
<script src="./lib/babylon.js"></script>
<!-- renderer.js then uses: const engine = new BABYLON.Engine(canvas) -->
```

The template layout (`main.js`, `styles.css`, `index.html` structure) remains **identical** — only the rendering engine changes.

---

*TSCG Framework v15.10.1 — Echopraxium with the collaboration of Claude AI — 2026-03-13*
