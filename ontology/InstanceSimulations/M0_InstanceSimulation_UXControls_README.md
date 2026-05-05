# TSCG Instance Simulation UX Controls — Pattern Library

**Version**: 1.0.0  
**Created**: 2026-05-05  
**Authors**: Echopraxium with the collaboration of Claude AI

---

## Overview

This document catalogs **reusable UX components and interaction patterns** for TSCG instance simulations. It ensures consistent user experience across all simulations by providing standard controls, layouts, and behaviors with copy-paste ready code examples.

**File Structure Convention** (NEW from v1.0.0):
```
instances/poclets/PocletName/
├── M0_PocletName.html          ← Root HTML file
├── src/
│   ├── pocletname.css          ← Styles
│   └── pocletname.js           ← Logic & BabylonJS code
├── M0_PocletName.jsonld        ← Ontology
└── M0_PocletName_README.md     ← Documentation
```

**Rationale**: Separation of concerns (HTML structure, CSS styling, JS behavior) improves maintainability and code reuse.

---

## Table of Contents

1. [Layout Patterns](#layout-patterns)
2. [Navigation Controls](#navigation-controls)
3. [Selection Controls](#selection-controls)
4. [Action Controls](#action-controls)
5. [Parameter Controls](#parameter-controls)
6. [Panel Controls](#panel-controls)
7. [Feedback Controls](#feedback-controls)
8. [Interaction Patterns](#interaction-patterns)
9. [CSS Conventions](#css-conventions)
10. [Complete Examples](#complete-examples)

---

## Layout Patterns

### 1. Main Canvas Layout

**Description**: Primary 3D viewport with fixed header/footer and left panel.

**Structure**:
```
┌─────────────────────────────────────────────┐
│ HEADER (40px): Home | TSCG | Title | Chips │
├────────┬───────────────────────────┬────────┤
│ LEFT   │                           │ RIGHT  │
│ PANEL  │    MAIN CANVAS (3D)       │ TABS   │
│ (203px)│                           │ (360px)│
│        │                           │        │
├────────┴───────────────────────────┴────────┤
│ FOOTER (32px): Status | Controls | Hint    │
└─────────────────────────────────────────────┘
```

**HTML**:
```html
<div id="layout">
  <div id="left-panel"><!-- Legends, selectors --></div>
  <div id="view-main"><canvas id="canvas-a"></canvas></div>
  <div id="splitter"></div>
  <div id="sidebar"><!-- Tabs --></div>
</div>
```

**CSS**:
```css
#layout {
  position: fixed;
  top: 40px;
  bottom: 32px;
  left: 0;
  right: 0;
  display: grid;
  grid-template-columns: 203px minmax(200px, 1fr) 5px var(--sidebar-w, 360px);
  grid-template-rows: 1fr;
  gap: 0;
}
```

---

### 2. Dual Canvas Layout (Main + Auxiliary)

**Description**: Primary canvas + floating NE panel for complementary visualization.

**Structure**:
```
┌──────────────────────────────────┐
│ MAIN CANVAS (Nautilus)           │  ┌────────┐
│                                  │  │   NE   │
│                                  │  │ PANEL  │
│                                  │  │(Bohr)  │
│                                  │  │        │
│                                  │  └────────┘
└──────────────────────────────────┘
```

**Complete code examples provided in full README...**

---

## Complete Example: Auto Rotate Toggle + Slider

**HTML**:
```html
<div style="display: flex; align-items: center; gap: 12px; padding: 0 14px;">
  <button class="bbtn" id="autorotate-toggle">⟳ Auto Rotate</button>
  <input type="range" id="speed-slider" min="10" max="200" value="50" style="flex: 1;">
  <span id="speed-display" style="font-size: 10px; min-width: 40px;">×1.0</span>
</div>
```

**JavaScript**:
```javascript
let autoRotate = false;
let rotationSpeed = 1.0;

// Toggle button
document.getElementById('autorotate-toggle').addEventListener('click', e => {
  autoRotate = !autoRotate;
  e.target.classList.toggle('on', autoRotate);
  document.getElementById('speed-slider').disabled = !autoRotate;
});

// Speed slider
document.getElementById('speed-slider').addEventListener('input', e => {
  rotationSpeed = parseFloat(e.target.value) / 100;
  document.getElementById('speed-display').textContent = `×${rotationSpeed.toFixed(1)}`;
});

// Apply in render loop
scene.registerBeforeRender(() => {
  if (autoRotate) {
    camera.alpha += rotationSpeed * 0.01;
  }
});
```

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-05 | Initial creation. Documented 11 simulations' worth of UX patterns. Established src/ folder convention for CSS/JS separation. |
