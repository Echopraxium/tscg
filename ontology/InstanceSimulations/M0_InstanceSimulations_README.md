# TSCG Instance Simulations — Capitalization of Experience

**Version**: 1.0.0  
**Created**: 2026-05-05  
**Authors**: Echopraxium with the collaboration of Claude AI

---

## Overview

This document captures best practices, design patterns, technical solutions, and lessons learned from creating **11 interactive 3D simulations** for TSCG instances (Poclets, Systemic Frameworks, Symbolic System Grammars). It serves as a reflexive knowledge base for future simulation development.

**Completed Simulations**:
1. FireTriangle
2. FourStrokeEngine
3. ExposureTriangle
4. ColorSynthesis
5. Transistor
6. PhaseTransition
7. VCO
8. CounterPoint
9. MtgColorWheel
10. NakamotoConsensus
11. **Ptoe (Periodic Table of Elements)** ← Latest

---

## Technical Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| **3D Rendering** | BabylonJS 6.26.0 | Exclusive for TSCG simulations; Three.js only as design reference |
| **2D Graphics** | p5.js (instance mode) | For 2D simulations or overlays |
| **Layout Reference** | M0_FireTriangle.html | Canonical template for all simulations |
| **Code Validation** | ESLint | Ensures code quality and consistency |
| **Local Server** | `_serve_index-html.bat` | `http://127.0.0.1:8080` in Brave browser |

---

## Design Patterns

### 1. Tabular Interface Pattern

**Description**: Standard 4-tab layout providing consistent navigation across all simulations.

**Tabs**:
- **Tab 0 (Description)**: Instance overview + domain-specific content
  - Example: Element families (Ptoe), reactor types (NuclearReactorTypology)
  - Includes detailed descriptions with scientific justifications and examples
  
- **Tab 1 (Scores)**: ASFID/REVOI visualization
  - Score bars with color-coding per dimension
  - Epistemic gap δ₁ badge with spectral class interpretation
  
- **Tab 2 (Concepts)**: M2 GenericConcepts mobilized
  - Organized by family (Structural, Informational, Ontological, Regulatory, etc.)
  - Each concept: Name + Tensor Formula + Description + Role in this instance
  
- **Tab 3 (User's Guide)**: Interactive controls and navigation instructions

**Best Practice**: Always extract tab content structure from `M0_FireTriangle.html` before starting a new simulation.

---

### 2. Dual View Architecture

**Description**: Main view + auxiliary view pattern allowing switching between complementary visualizations of the same system.

**Implementation**:
- Main canvas (full-size, primary visualization)
- NE floating panel (resizable, auxiliary view)
- Swap button (⇄) to switch views
- Independent camera controls for each view

**Examples**:
- **Ptoe**: Nautilus spiral (main) ↔ Orbital/Bohr model (auxiliary)
- **MtgColorWheel**: Pentagon layout (main) ↔ Alternative view (auxiliary)

**Code Pattern**:
```javascript
// Main scene
const sceneA = new BABYLON.Scene(engine);
const cameraA = new BABYLON.ArcRotateCamera(...)

// Auxiliary scene
const sceneB = new BABYLON.Scene(engine);
const cameraB = new BABYLON.ArcRotateCamera(...)

// Render loop
engine.runRenderLoop(() => {
  if (viewMode === 'main') sceneA.render();
  else sceneB.render();
});
```

---

### 3. Color-Coding by Family/Category

**Description**: Use consistent color mapping for categories/families with legend-driven selection.

**Implementation**:
- Left panel legend with clickable family entries
- Hover effects on legend items
- Path-based highlighting in 3D scene (luminous connections)
- Clear selection button (✕)

**Examples**:
- **Ptoe**: 10 element families
  - Alkali Metals: `#FF4422`
  - Noble Gases: `#FF44BB`
  - Transition Metals: `#FFD030`
  - etc.
  
- **MtgColorWheel**: 5 MTG colors
  - White, Blue, Black, Red, Green (canonical MTG colors)

**Code Pattern**:
```javascript
const familyColors = {
  'am': '#FF4422',  // Alkali Metals
  'ng': '#FF44BB',  // Noble Gases
  // ...
};

// Apply color to mesh
mesh.material.diffuseColor = BABYLON.Color3.FromHexString(familyColors[family]);
```

---

### 4. Geometric Primitives Catalog

**Description**: Reusable 3D shapes with documented rotation/alignment conventions.

#### Cylinder (tessellation=4)
```javascript
const cyl = BABYLON.MeshBuilder.CreateCylinder("cyl", {
  height: h, diameter: d, tessellation: 4
}, scene);
```
- **Alignment**: Corners at 0°/90°/180°/270° — no offset needed
- **Radial alignment**: `rotation.y = Math.atan2(pos.z, pos.x)`

#### Octahedron (bicolor)
```javascript
// Always use makeBicolorOctaParts with tiltQuat composition
const tiltQuat = BABYLON.Quaternion.RotationAxis(radialAxis, Math.PI/2);
const finalQuat = baseQuat.multiply(tiltQuat);
```
- **Critical**: `makeSolidOctaParts` must delegate to `makeBicolorOctaParts(hex1, hex1)` for rotation consistency

#### Ring Pair (selection)
```javascript
function makeRingPair(pos, radius) {
  const equatorial = BABYLON.MeshBuilder.CreateTorus(...);
  const polar = BABYLON.MeshBuilder.CreateTorus(...);
  // White rings for selection feedback
}
```
- **Usage**: More reliable than octahedron-based selection
- **Visibility**: Toggle on hover/click

---

### 5. Content Source Integration

**Description**: Pattern for extracting content from M0 JSON-LD and README files to populate HTML tabs.

**Workflow**:
1. Extract `GenericConceptsMobilized` list from `M0_*.jsonld`
2. Retrieve concept descriptions from `M2_GenericConcepts.jsonld`
3. Extract role descriptions from `M0_*.jsonld` (`conceptList` entries)
4. Extract domain-specific content from `M0_*_README.md` (e.g., "Element Families" section)
5. Generate HTML fragments with consistent styling

**Tooling**:
```python
# Example: extract_m2_concepts.py
import json

# Load M2_GenericConcepts.jsonld
with open('M2_GenericConcepts.jsonld') as f:
    m2_data = json.load(f)

# Extract descriptions for needed concepts
for concept in concepts_needed:
    # Find in m2_data['@graph']
    # Extract rdfs:label, rdfs:comment, m2:hasFamily, m2:hasTensorFormula
```

---

## Technical Solutions

### Aspect Ratio Correction

**Problem**: Objects appear stretched/compressed when canvas aspect ratio ≠ intended ratio.

**Solution**: Always recalculate camera aspect ratio on window resize:
```javascript
window.addEventListener('resize', () => {
  engine.resize();
  camera.aspect = engine.getRenderWidth() / engine.getRenderHeight();
  camera.getProjectionMatrix(true);  // Force update
});
```

---

### BabylonJS Preview Restriction

**Problem**: CSP sandbox in Claude.ai blocks BabylonJS APIs.

**Solution**: Never preview BabylonJS in artifacts.

**Workflow**:
1. Prototype layout/logic in conversation
2. Validate geometry via Python/Matplotlib visualization
3. Create complete HTML file for local testing
4. User tests locally in browser
5. Report issues → Iterate

---

### Windows Multi-Line Command Workaround

**Problem**: `cmd.exe` doesn't support bash-style line continuation with `\`.

**Solutions**:
- **Single-line**: Combine into one long command
- **cmd.exe**: Use `^` for continuation
  ```cmd
  command arg1 ^
    arg2 ^
    arg3
  ```
- **PowerShell**: Use backtick `` ` ``
  ```powershell
  command arg1 `
    arg2 `
    arg3
  ```

---

## Content Patterns

### Element Families Description (Ptoe)

**Template** for documenting categorical subdivisions within an instance:

```html
<div id="family-XX" style="margin-top: 12px;">
  <h4 style="color: #RRGGBB; font-size: 13px;">Category Name</h4>
  <p style="font-size: 12px; line-height: 1.6;">
    Detailed paragraph covering: 
    - Core properties
    - Behavior/reactivity
    - Applications
    - Scientific justification
    Examples: A, B, C.
  </p>
</div>
```

**Applicability**: Any instance with natural categorical subdivisions (chemical families, reactor types, biological taxa, governance models, etc.)

---

### Concepts Tab Structure

**Standard structure** for displaying M2 GenericConcepts:

```html
<div class="tab-panel">
  <h3>M2 GenericConcepts Mobilized</h3>
  <p>Summary: X concepts across Y families</p>

  <!-- Per-family section -->
  <div class="concept-family">
    <h4 style="color: #FAMILY_COLOR;">● Family Name (N)</h4>
    
    <!-- Per-concept entry -->
    <div class="concept-item">
      <div>
        <strong>Concept Name</strong>
        <span>Tensor Formula</span>
      </div>
      <p>Description from M2_GenericConcepts.jsonld</p>
      <p><strong>Role:</strong> Specific role in this instance</p>
    </div>
  </div>
</div>
```

**Color Palette**:
- Structural: `#56d364`
- Informational: `#d2a8ff`
- Ontological: `#79c0ff`
- Regulatory: `#f78166`
- Dynamic: `#e3b341`
- Adaptive: `#79c0ff`
- Energetic: `#f78166`
- Teleonomic: `#d2a8ff`
- Relational: `#56d364`

---

## Lessons Learned

### 1. Always Read Skill First

**Rule**: Before writing any simulation code, read the matching `SKILL.md` file(s).

**Rationale**: Skills encode environment-specific constraints (available libraries, rendering quirks, output paths) not in Claude's training data. Skipping this step leads to costly iterations.

**Example**: `tscg-create-instance-simulation/SKILL.md` documents BabylonJS version, canonical layout, modular architecture.

---

### 2. Prefer Iterative Editing

**Rule**: Build long content (>100 lines) across multiple tool calls.

**Workflow**:
1. Start with outline/structure
2. Add content section by section
3. Review and refine
4. Copy final version to `/mnt/user-data/outputs/`

**Rationale**: Reduces token usage, enables surgical corrections, maintains version control.

---

### 3. Maintain Coherence Across Files

**Rule**: `M0_*.jsonld`, `M0_*_README.md`, and `M0_*.html` must present consistent information.

**Checklist**:
- [ ] Element/component descriptions match between README and HTML
- [ ] GenericConcepts list in JSON-LD matches Concepts tab in HTML
- [ ] ASFID/REVOI scores identical in all files
- [ ] Version numbers synchronized
- [ ] Changelog entries aligned

**Tools**: Future validation script to automate checking.

---

### 4. Local Testing is Mandatory

**Rule**: BabylonJS simulations cannot be validated in Claude.ai artifacts.

**Workflow**:
1. Create complete HTML file
2. Deliver to user
3. User tests locally (Brave/Chrome/Firefox)
4. User reports issues
5. Iterate based on feedback

**Best Practice**: Include testing instructions in delivery message.

---

## Future Directions

### Short-Term (Next 3-6 months)
1. **Automated content extraction pipeline**
   - Script to extract GenericConcepts from M0 JSON-LD
   - Auto-generate HTML tab fragments
   - Validate coherence across files

2. **Component library**
   - Reusable 3D primitives (rings, octahedra, spirals)
   - Documented rotation/alignment conventions
   - Import as ES6 modules

3. **Template repository**
   - Boilerplate HTML/CSS/JS for new simulations
   - Pre-configured BabylonJS setup
   - Standard tab structure

### Long-Term (6-12 months)
1. **Validation script**
   - Check M0_*.jsonld ↔ README ↔ HTML coherence
   - Verify all GenericConcepts have descriptions
   - Ensure ASFID/REVOI scores match

2. **Interactive tutorial**
   - Step-by-step guide for creating simulations
   - Embedded in TscgPocletMiner or standalone web app

3. **Simulation gallery**
   - Unified index with filtering by domain/family
   - Visual thumbnails
   - Performance metrics (load time, frame rate)

---

## References

- **Canonical Layout**: `instances/poclets/FireTriangle/M0_FireTriangle.html`
- **Skill Documentation**: `/mnt/skills/user/tscg-create-instance-simulation/SKILL.md`
- **M2 GenericConcepts**: `ontology/M2_GenericConcepts.jsonld` (v15.11.0)
- **BabylonJS Documentation**: https://doc.babylonjs.com/

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-05 | Initial creation based on 11 completed simulations (FireTriangle through Ptoe) |
