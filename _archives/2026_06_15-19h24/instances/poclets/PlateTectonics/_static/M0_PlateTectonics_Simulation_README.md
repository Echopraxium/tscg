# TSCG - Plate Tectonics Simulation

**Version 6.5.0** | Wilson Cycle Poclet | Interactive 3D Mantle Deformation

## Overview

This interactive 3D simulation visualizes plate tectonics with a focus on mantle convection and crustal deformation. Users can interact with a 3D grid representing the asthenosphere, apply compression/dilation forces to individual cells, and observe real-time stress accumulation leading to automatic fault ruptures (earthquakes).

## Key Features

### 3D Mantle Grid
- **8×3×4 cell grid** representing the asthenosphere (viscous mantle layer)
- Each cell is an interactive 3D box with color-coded states:
  - **Normal**: Orange/red (default)
  - **Pre-selection (hover)**: Bright orange with orange wireframe
  - **Active selection**: Bright RED with white wireframe
  - **Deformed**: Amber with orange wireframe

### Cell Interaction
| Action | Result |
|--------|--------|
| **Mouse over** | Orange highlight (pre-selection, does NOT affect current selection) |
| **Click** | Select cell → turns RED + white wireframe |
| **Click on selected cell** | Deselect cell |
| **Click outside 3D model** | Deselect current cell |

### XYZ Deformation Control

The XYZ control panel (bottom right) allows precise deformation of the selected cell:

| Axis | Positive (+) | Negative (-) |
|------|--------------|---------------|
| **X** | Lateral compression (convergence) | Lateral dilation (divergence) |
| **Y** | Subsidence (slab pull, convergence) | Uplift (upwelling, divergence) |
| **Z** | Depth compression | Depth dilation |

#### Two Operation Modes

**🎬 Real Time Mode** (default)
- Deformation applies IMMEDIATELY as you move the sliders
- Visual feedback appears instantly
- Stress accumulates in real time

**⚙️ Configure Mode**
- Adjust sliders without applying deformation
- Click "Apply Deformation" button to commit changes
- Allows fine-tuning before execution

### Stress & Earthquake System

- Stress accumulates based on:
  - Convection intensity (0.05 - 1.0)
  - Deformation magnitude (via XYZ controls)
  - Plate asymmetry
- **Threshold: 90% stress** → automatic earthquake
- Earthquake effects:
  - Camera shake
  - Particle burst
  - Visual flash effect
  - Stress reset (reduced by 70%)
  - 2-second cooldown period

### Plate System

#### Surface Plates (3×3 grid)
- **Left side (X < 0)**: 9 continental plate segments
- **Right side (X > 0)**: 9 oceanic plate segments
- **Boundaries**: Fault zones that change color based on stress levels

#### Tectonic Features
- **Mid-Ocean Ridge**: Central volcanic ridge (new crust creation)
- **Subduction Zone**: Right side with descending slab (crust recycling)
- **Mantle Plume**: Interactive hotspot (button-activated)
- **Mountain**: Example orogenic feature
- **Wilson Cycle**: 7-stage continental cycle animation

### Controls

#### Global Simulation Controls (bottom bar)

| Control | Function |
|---------|----------|
| **Pause/Play** | Stop/resume simulation time |
| **Reset** | Reset all parameters, stress, deformation, and camera |
| **Convection** | Heat flux (0.05-1.0) → controls plate drift speed |
| **Slab Density** | Subduction angle (0.1-1.0) |
| **Asymmetry** | Euler rotation for left plates (-1 to +1) |
| **Mantle Plume** | Activate hotspot rising animation |
| **Wilson Cycle** | Play 7-stage Wilson cycle animation |
| **Legend** | Show/hide HUD overlay |

#### Camera Controls
- **Left drag**: Rotate view
- **Right drag**: Pan
- **Scroll**: Zoom in/out

### Visual Feedback

#### Wireframe Colors
| State | Wireframe Color |
|-------|-----------------|
| Normal cell | Light gray |
| Pre-selection (hover) | Orange |
| Active selection | **White** |
| Deformed cell | Amber |

#### Stress Indicator
- **0-50%**: Green bar
- **50-80%**: Yellow/amber bar
- **80-100%**: Red bar
- **≥90%**: Automatic earthquake trigger

#### Status Indicator (top of control bar)
- **Green pulsing**: Simulation running normally
- **Blue pulsing**: Information message (mode change, deformation type)
- **Red pulsing**: Warning (earthquake)
- **Orange pulsing**: Special event (mantle plume)

### Geological Layers Visualization

The HUD (bottom left) shows the following layers (from bottom to top):

1. **Upper Mantle** (dark red) - Deep rigid base at Y ≈ -3.2
2. **Asthenosphere** (orange) - Interactive 3D grid cells (Y: -2.0 to -0.55)
3. **Lithosphere** (golden brown) - Rigid layer at Y ≈ -0.60
4. **Continental Crust** (light brown) - 30-70 km thick, left side
5. **Oceanic Crust** (dark blue) - 7-10 km thick, right side
6. **Ocean** (translucent blue) - Water layer, right side

### Deformation Physics (Real Geology)

| Force | Effect on Plates |
|-------|------------------|
| **Y+ (subsidence)** | Slab pull, convergence (subduction) |
| **Y- (uplift)** | Upwelling, divergence (ridge push) |
| **X+ (compression)** | Lateral convergence (mountain building) |
| **X- (dilation)** | Lateral divergence (rifting) |
| **Z±** | Oblique/transform motion |

### Stress Propagation

When you deform a cell:
1. Cell scaling changes visually
2. Stress increases proportionally to deformation magnitude
3. Stress propagates to adjacent fault zones
4. Fault zones change color (green → yellow → red)
5. At 90% stress → automatic earthquake releases energy

### Wilson Cycle Animation

7 stages simulated (click Wilson Cycle button):
1. Continental Rifting
2. Young Ocean (Red Sea stage)
3. Mature Ocean (Atlantic stage)
4. Subduction Initiated
5. Terminal Ocean (Mediterranean stage)
6. Continental Collision (Himalaya stage)
7. Cratonization → Cycle restarts

Camera automatically follows the active stage.

### Sidebar Tabs

#### Description
- System overview
- Mantle grid interaction guide
- Deformation physics explanation
- Plate configuration
- Control reference

#### Concepts
- Primary geological concepts (6)
- Secondary concepts (4)
- Each with TSCG pole notation (e.g., S⊗F⊗I⊗D)

#### Synergy
- KnowledgeFieldConceptCombo explanations
- Wilson Cycle emergence
- Walker Thermostat (1981) - tectonic carbon cycle

### Technical Notes

- **Engine**: Babylon.js 6.26.0
- **Grid dimensions**: 8 columns × 3 rows × 4 depth layers
- **Cell size**: ~1.7m width × ~0.48m height × ~1.15m depth (scaled representation)
- **Total scene bounds**: X: [-7, +7], Y: [-4.7, +2.7], Z: [-2.58, +2.58]
- **Rendering groups**: 
  - Group 0: Opaque geometry
  - Group 1: Mantle cells (transparent)
  - Group 2: Cell wireframes
  - Group 3: Reserved for future gizmos

### Performance Tips

- **Real Time mode** uses more CPU but provides immediate feedback
- **Configure mode** is more efficient for multiple adjustments
- Reduce convection slider if performance degrades
- Pause simulation when not actively observing

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Cell won't select | Ensure you're clicking directly on orange cell (not on wireframe only) |
| No deformation visible | Check that Real Time mode is ON or click Apply in Configure mode |
| Can't deselect | Click on selected cell again OR click on empty background |
| Earthquake too frequent | Reduce convection or deformation magnitude |
| Camera stuck | Click Reset button |

### Version History

**v6.5.0** (current)
- Fixed `registerBeforeFrame` → `registerBeforeRender`
- All UI text in English
- Legend moved to bottom left
- XYZ panel moved to bottom right (fully interactive)
- Real Time / Configure mode toggle
- Proper selection/deselection behavior
- Wireframe colors: light gray (normal), white (selected)

### Credits

- **TSCG Framework**: Conceptual modeling with pole notation (ASFID/REVOI)
- **Geological validation**: Wilson Cycle, plate tectonics theory
- **Babylon.js**: 3D rendering engine

### License

Part of TSCG Poclet Gallery - Interactive geological simulations

---

**Enjoy exploring plate tectonics!** Click on orange cells, adjust XYZ sliders, and watch stress build until the next earthquake. 🌋