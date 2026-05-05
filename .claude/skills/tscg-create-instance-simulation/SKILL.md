---
name: tscg-create-instance-simulation
description: >
  Create interactive 3D simulations for TSCG instances (Poclets, Systemic Frameworks,
  Symbolic System Grammars, etc.) using BabylonJS with modular architecture. This skill
  generates browser-based 3D simulations following standardized UI layout with ESLint-validated
  code. Works in 4 sequential steps: Inputs & Layout → Visualization Conceptualization →
  Prototype Creation & Iteration → Manual Testing & Finalization. Use when user wants to
  create a 3D simulation, mentions "visualization", "BabylonJS", "interactive simulation",
  or asks to visualize a TSCG instance. Prerequisites: Instance must be modeled using
  tscg-instance-pipeline skill first (M0_*.jsonld and M0_*_README.md required).
  Do NOT use for Case Studies or systems not yet modeled in TSCG.
---

# create_instance_simulation

Create interactive 3D simulations for TSCG instances (Poclets, Systemic Frameworks, Symbolic System Grammars, etc.) using BabylonJS with modular architecture.

## Overview

This skill generates browser-based 3D simulations for TSCG instances following a standardized UI layout and modular file structure. It works in conjunction with the `tscg-instance-pipeline` skill, which must be run first to create the M0 ontology and documentation.

**Prerequisites**: Instance must be modeled using `tscg-instance-pipeline` skill, producing:
- `M0_InstanceName.jsonld` (ontology)
- `M0_InstanceName_README.md` (documentation)
- Identified M2 GenericConcepts and M1 Core concepts

**Output**: Fully functional standalone HTML simulation with:
- Modular architecture (HTML + separate CSS/JS files in src/ folder)
- Standard TSCG UI layout with reusable UX controls
- BabylonJS 3D visualization
- ESLint-validated JavaScript code
- Interactive sidebar with ontology metadata

**Knowledge Resources**: This skill leverages accumulated UX experience from 11+ simulations documented in:
- `ontology/InstanceSimulations/M0_InstanceSimulations.jsonld` - Design patterns, technical solutions, lessons learned
- `ontology/InstanceSimulations/M0_InstanceSimulations_README.md` - Narrative guide with code examples
- `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld` - UX component catalog (layouts, controls, interactions)
- `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md` - Copy-paste ready UX patterns

## When to Use This Skill

Use this skill when:
- User wants to create a 3D simulation for a TSCG instance
- User mentions "simulation", "3D visualization", "BabylonJS", or "interactive visualization"
- User asks to visualize a system/process that was modeled in `tscg-instance-pipeline`
- User says "create simulation for [instance name]"

Do NOT use this skill for:
- Case Studies or Real World Systems (too complex)
- Static documentation or diagrams (use standard tools)
- Non-TSCG projects

## Workflow

This skill operates in **4 sequential steps**. Each step must be completed and validated before proceeding to the next.

### Step 1: Inputs & Standard Layout Definition

**Objective**: Gather inputs and confirm standard UI layout.

#### Required Inputs

1. **ontologyType** (string): Type of instance
   - Examples: "Poclet", "SystemicFramework", "SymbolicSystemGrammar", "TransDisclet", "CaseStudy"
   - Maps to directory path:
     - `Poclet` → `instances/poclets/`
     - `SystemicFramework` → `instances/systemic-frameworks/`
     - `SymbolicSystemGrammar` → `instances/symbolic-system-grammars/`
     - `TransDisclet` → `instances/transdisclet/`
     - `CaseStudy` → `instances/case-studies/`

2. **instanceName** (string): Short name used for files and directory
   - Example: "NuclearReactorsTypology"
   - Used in paths: `instances/poclets/NuclearReactorsTypology/static/`

3. **M0_*.jsonld** (file): Instance ontology created by `tscg-instance-pipeline`
   - Contains: scores, M2/M1 concepts, m1:simulationTitle, structure

4. **M0_*_README.md** (file): Instance documentation
   - Contains: descriptions, context, educational content

#### Standard UI Layout

All simulations follow this standard layout (defined in UX Controls catalog):

```
┌────────────────────────────────────────────────────────────┐
│ [🏠 Home] [TSCG]  Instance Title                           │ ← Header (40px)
├───────────────────────────────────┬──┬─────────────────────┤
│                                   │ S│ Tab: Description    │
│                                   │ P│      Scores         │
│   BabylonJS 3D Canvas            │ L│      M2 Concepts    │
│   (Central view)                 │ I│      User's Guide   │
│                                   │ T│                     │
│                                   │ T│ [Tab content from   │
│                                   │ E│  M0_*.jsonld]       │
│                                   │ R│                     │
├───────────────────────────────────┴──┴─────────────────────┤
│ [Reset] [Optional: Auto Rotate, sliders, combos, etc.]     │ ← Bottom bar (32px)
└────────────────────────────────────────────────────────────┘
```

**Components** (see `M0_InstanceSimulation_UXControls.jsonld` for detailed specs):
- **Header**: Home icon → Gallery, TSCG icon → GitHub repo, Instance title
- **Canvas**: BabylonJS 3D view (1 engine + 1 scene by default)
- **Splitter**: 5px vertical draggable bar (DragToAdjust pattern)
- **Sidebar**: 4 tabs with content from M0_*.jsonld (TabPanel pattern)
  - Description (from README + domain-specific content)
  - Scores (ASFID + REVOI with epistemic gap δ₁ badge)
  - M2 Concepts (GenericConcepts mobilized, organized by family)
  - User's Guide (interaction instructions)
- **Bottom bar**: Reset button (mandatory) + optional controls

#### File Structure Generated

**New convention (v1.0.0+)**: CSS and JS files are placed in `src/` subdirectory for separation of concerns.

```
instances/{type-plural}/{instanceName}/static/
├── M0_{instanceName}.html                  ← HTML structure
├── src/
│   ├── {instanceName}.css                  ← Styles (all in one file)
│   └── {instanceName}.js                   ← JavaScript code
├── .eslintrc.json                          ← ESLint config (browser env)
├── test_data.json                          ← Optional test data
├── _00_serve_poclet-sim.bat                ← Local server script
└── M0_{instanceName}_SimulationIssues.md   ← Issue tracking (created empty)
```

**Rationale**: Modular architecture (HTML structure, CSS styling, JS behavior) improves maintainability and code reuse.

#### UX Controls Reference

**Before implementing any UI component**, consult:
- `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld` - Formal UX component definitions
- `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md` - Code examples for each pattern

**Standard UX Patterns Available**:
- **Layout**: MainCanvasLayout, DualCanvasLayout (Main + NE Panel), ResizableSplitter
- **Navigation**: ArcRotateCamera, HomeButton, TscgBadge
- **Selection**: CombolistWithClear, LegendList (family/category selection)
- **Action**: ActionButton (Reset, Home, Swap), ToggleButton (Auto Rotate)
- **Parameter**: Slider (Speed, Zoom), NumericStepper (Z number arrows)
- **Panel**: TabPanel (4-tab sidebar), ResizablePanel (NE floating)
- **Feedback**: HoverIndicator, ProgressGauge (horizontal bars, vertical stacks), StatusBadge
- **Interaction**: ClickToSelect, HoverToPreview, DragToAdjust

#### Step 1 Output

- Confirmation of inputs received
- Layout structure confirmed with user
- Path structure validated
- UX Controls catalog referenced

---

### Step 2: Visualization Conceptualization

**Objective**: Choose visualization pattern, validate ontology data, and select UX controls.

#### 2.1: Read & Validate M0_*.jsonld

**Extract Data**:
- `m1:simulationTitle` (or `m1core:simulationTitle` - see error detection below)
- Epistemic gap: `δ₁`, `ASFID_mean`, `REVOI_mean`, `spectralClass`
- M2 GenericConcepts used
- M1 Core concepts used
- Domain-specific content (e.g., element families, reactor types)

**Error Detection**: Obsolete Namespace `m1core:`

If `m1core:simulationTitle` is found (should be `m1:simulationTitle`):

1. **Signal Error** to user:
   ```
   ⚠️  Warning: Obsolete namespace detected
   File: M0_InstanceName.jsonld
   Found: "m1core:simulationTitle"
   Should be: "m1:simulationTitle"
   
   This will be logged in SHACL_GrammarIssues.jsonld
   ```

2. **Log to** `ontology/TSCG_Grammar/SHACL_GrammarIssues.jsonld`:
   ```json
   {
     "@id": "issue:NNN",
     "@type": "m3:GrammarIssue",
     "dcterms:title": "Obsolete namespace m1core: used",
     "m3:issueType": "NamespaceViolation",
     "m3:severity": "Warning",
     "m3:detectedIn": "M0_InstanceName.jsonld",
     "m3:detectedProperty": "m1core:simulationTitle",
     "m3:correctProperty": "m1:simulationTitle",
     "m3:detectedBy": "create_instance_simulation skill",
     "m3:detectedDate": "YYYY-MM-DD",
     "m3:status": "Logged"
   }
   ```

3. **Auto-execute migration script** (dry-run mode):
   ```bash
   cd ontology/TSCG_Grammar
   python migrate_m1core_to_m1.py --dry-run
   ```
   Display results and suggest user run without `--dry-run` to apply corrections.

#### 2.2: Choose Visualization Pattern & UX Controls

Two scenarios:

**Case A: User Proposes Concept**
- User describes visualization idea and interaction model
- Assistant validates against UX Controls catalog
- Documents the pattern and selected controls
- Proceeds to pattern documentation

**Case B: Assistant Suggests Patterns**

1. **Analyze** M2 GenericConcepts from instance
   - Pattern → Suggest: Spiral, Grid, Network
   - Hierarchy → Suggest: Tree, Pyramid, Concentric levels
   - Flow → Suggest: Arrows, Paths, Sequential animation
   - Structure → Suggest: 3D mesh, Atomic model, Lattice

2. **Search** pattern library in `ontology/InstanceSimulations/M0_InstanceSimulations.jsonld`:
   - Find similar instances with same M2 concepts
   - Present 2-3 relevant patterns with examples
   - Include UX controls used in each example

3. **Propose** patterns with UX controls:
   ```
   Based on M2 concepts (Pattern, Hierarchy, Structure), here are 3 visualization patterns:
   
   1. **Logarithmic Spiral** (used in Ptoe)
      - Good for: Sequential ordering, periodic systems, 100+ elements
      - BabylonJS: ParametricCurve, InstancedMesh, CustomShader
      - UX Controls: CombolistWithClear (element selector), LegendList (10 families),
                    DualCanvasLayout (Nautilus + Orbital), NumericStepper (Z arrows)
      - Example: Elements arranged on Nautilus shell spiral with family selection
   
   2. **Concentric Levels** (used in TrophicPyramid)
      - Good for: Hierarchical structures, trophic levels
      - BabylonJS: BoxGeometry, Layers, ScalingAnimation
      - UX Controls: ProgressGauge (vertical stacks for energy levels), 
                    TabPanel (standard 4-tab sidebar)
      - Example: Pyramid with stacked levels showing energy flow
   
   3. **Grid Layout** (used in NuclearReactorsTypology)
      - Good for: Classification, categorical organization
      - BabylonJS: InstancedMesh, Grid positioning, Color coding
      - UX Controls: LegendList (reactor families), ResizableSplitter,
                    HoverIndicator (show reactor details on hover)
      - Example: Reactors in categorized grid
   
   Which pattern + UX controls combination fits your instance best?
   ```

4. **User selects** pattern and controls

#### 2.3: Document Selection

**Record in** `ontology/InstanceSimulations/M0_InstanceSimulations.jsonld`:

```json
{
  "@id": "m0:InstanceName_Simulation",
  "@type": "m3:InstanceSimulation",
  "m3:instanceName": "InstanceName",
  "m3:ontologyType": "Poclet",
  "m1:simulationTitle": "Full Display Title",
  "m3:visualizationPattern": "LogarithmicSpiral",
  "m3:uxControlsUsed": ["CombolistWithClear", "LegendList", "DualCanvasLayout", "NumericStepper"],
  "m3:epistemicGap": {
    "δ₁": 0.08,
    "ASFID_mean": 0.81,
    "REVOI_mean": 0.89,
    "spectralClass": "OnCriticalLine"
  },
  "m3:babylonJSTechniques": [
    "ParametricCurve for spiral path",
    "InstancedMesh for 118 elements",
    "CustomShader for glow effects"
  ],
  "m3:createdDate": "YYYY-MM-DD"
}
```

#### Step 2 Output

- Visualization pattern selected and documented
- UX controls identified from catalog
- Data extraction from M0_*.jsonld completed
- Ready to proceed to prototyping

---

### Step 3: Prototype Creation & Iteration

**Objective**: Generate working simulation prototype with selected UX controls.

#### 3.1: Initial Code Generation

**Read UX Controls README** before writing any code:
```
ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md
```

This file contains copy-paste ready code examples for all standard UX patterns. Use these as templates.

**Generate Files**:

1. **M0_{instanceName}.html**
   - Standard header (Home button, TSCG badge, title, chips)
   - Main layout grid (left panel, canvas, splitter, sidebar)
   - Bottom bar (Reset button + optional controls)
   - Tab structure (Description, Scores, Concepts, User's Guide)
   - Link to CSS: `<link rel="stylesheet" href="src/{instanceName}.css">`
   - Link to JS: `<script src="src/{instanceName}.js"></script>`
   - Link to BabylonJS: `<script src="https://cdn.babylonjs.com/babylon.js"></script>`

2. **src/{instanceName}.css**
   - Import or copy standard TSCG styles
   - Apply CSS conventions from UX Controls (color palette, spacing, transitions)
   - Instance-specific style adaptations

3. **src/{instanceName}.js**
   - BabylonJS setup (engine, scene, camera, lights)
   - Implement selected visualization pattern
   - Integrate selected UX controls (copy from UXControls README)
   - Tab switching logic
   - Splitter drag logic
   - Reset function
   - Render loop

**Code Structure Pattern**:
```javascript
// ──────────────────────────────────────────
// Periodic Table of Elements (Ptoe)
// Author: Echopraxium with the collaboration of Claude AI
// Framework: TSCG
// ──────────────────────────────────────────

// ═══ 1. BabylonJS Setup ═══
const canvas = document.getElementById('canvas-a');
const engine = new BABYLON.Engine(canvas, true);
const scene = new BABYLON.Scene(engine);

// Camera (ArcRotate pattern from UX Controls)
const camera = new BABYLON.ArcRotateCamera('cam', Math.PI/4, Math.PI/3, 10, 
  new BABYLON.Vector3(0, 0, 0), scene);
camera.attachControl(canvas, true);

// ═══ 2. UX Controls Integration ═══
// (Copy-paste from M0_InstanceSimulation_UXControls_README.md)

// CombolistWithClear pattern
const elemSelect = document.getElementById('elem-select');
elemSelect.addEventListener('change', e => { /* ... */ });

// LegendList pattern
document.querySelectorAll('.leg').forEach(item => {
  item.addEventListener('click', e => { /* ... */ });
});

// ═══ 3. 3D Scene Construction ═══
// (Instance-specific visualization)

// ═══ 4. Render Loop ═══
engine.runRenderLoop(() => scene.render());
window.addEventListener('resize', () => engine.resize());
```

#### 3.2: Validation & ESLint

**Run ESLint** (mandatory):
```bash
cd instances/{type}/{name}/static
eslint --config .eslintrc.json src/{name}.js
```

**ESLint Config** (`.eslintrc.json`):
```json
{
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "globals": {
    "BABYLON": "readonly"
  },
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "script"
  },
  "rules": {
    "no-unused-vars": "warn",
    "no-undef": "error"
  }
}
```

**Fix Errors**:
- 0 errors required to proceed
- Warnings documented in `M0_{name}_SimulationIssues.md`

#### 3.3: Iteration Cycles

**User Feedback Loop**:
1. User tests prototype locally (`_00_serve_poclet-sim.bat`)
2. User reports issues/requests
3. Assistant fixes issues using `str_replace` (surgical edits)
4. Repeat until user satisfied

**Common Iterations**:
- Adjust camera position/limits
- Tweak colors/sizes/spacing
- Add/remove UX controls
- Performance optimization (instanced meshes, LOD)
- Responsive layout fixes

#### Step 3 Output

- Working prototype delivered
- ESLint validation passed (0 errors)
- User has tested and approved base functionality
- Ready for Claude review

---

### Step 4: Manual Testing & Finalization

**Objective**: Final validation, catalog updates, and green light for deployment.

#### 4.1: Claude Review

**Assistant re-reviews**:
- Code quality (modularity, readability, comments)
- UX Controls implementation correctness
- Performance considerations
- Accessibility (keyboard navigation, ARIA labels if applicable)
- Cross-browser compatibility notes

**Checklist**:
- [ ] All UX controls from catalog implemented correctly
- [ ] Code follows TSCG conventions (author attribution, etc.)
- [ ] ESLint passed with 0 errors
- [ ] No console errors in browser
- [ ] Splitter works (DragToAdjust pattern)
- [ ] Tabs switch correctly (TabPanel pattern)
- [ ] BabylonJS scene renders smoothly
- [ ] Reset button returns to initial state
- [ ] Camera controls intuitive (ArcRotateCamera pattern)

#### 4.2: Update Catalogs

**Add to** `ontology/InstanceSimulations/M0_InstanceSimulations.jsonld`:
- Full simulation entry with metadata
- Pattern description
- BabylonJS techniques used
- Link to instance files

**Add to** `ontology/InstanceSimulations/M0_InstanceSimulations_README.md`:
- New simulation listed in "Completed Simulations"
- Pattern description in relevant section
- Code examples if introducing new techniques

**CRITICAL: Update UX Controls Catalog if Applicable**

If this simulation introduces **new UX controls** OR **modifies existing controls**:

1. **Document New Control** in `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld`:
   ```json
   {
     "@id": "m0:NewControlName",
     "rdfs:label": "Descriptive Name",
     "rdfs:comment": "What this control does and when to use it",
     "m0:components": { /* HTML structure */ },
     "m0:behavior": { /* Interaction patterns */ },
     "m0:styling": { /* CSS patterns */ },
     "m0:examples": ["InstanceName: specific usage"]
   }
   ```

2. **Add Code Example** to `ontology/InstanceSimulations/M0_InstanceSimulation_UXControls_README.md`:
   - Section heading for new control
   - HTML snippet
   - CSS snippet
   - JavaScript snippet
   - Usage notes

3. **Document Modification** if existing control was enhanced:
   - Update control definition with new capabilities
   - Add new example to existing section
   - Note version change in changelog

**Examples of Updates**:
- **New Control**: "Floating tooltip with element details on hover" (not in catalog)
  → Add as `m0:FloatingTooltip` with complete docs
- **Modified Control**: "LegendList now supports multi-select mode"
  → Update `m0:LegendList` definition, add multi-select code example
- **Enhanced Pattern**: "DualCanvasLayout now supports 3-canvas mode"
  → Update pattern documentation with 3rd canvas example

**Rationale**: The UX Controls catalog is a **living document**. Each simulation may introduce innovations that benefit future simulations. Keeping the catalog up-to-date ensures knowledge accumulates rather than being lost.

#### 4.3: Final Deliverables

**Package for User**:
- All files in `instances/{type}/{name}/static/` directory
- `M0_{name}_SimulationIssues.md` with final status
- Confirmation that catalogs are updated

**Green Light Criteria**:
- [ ] All features implemented and tested
- [ ] No known critical bugs
- [ ] Code quality acceptable (ESLint passed)
- [ ] Catalogs updated (InstanceSimulations + UXControls if applicable)
- [ ] Documentation complete

#### Step 4 Output

- Simulation finalized and ready for deployment
- Catalogs updated with new knowledge
- User receives green light confirmation

---

## Files Created/Modified

### Per Instance (in `instances/{type}/{name}/static/`)

**Created**:
- `M0_{name}.html` - Main HTML structure
- `src/{name}.css` - Styles (all in one file)
- `src/{name}.js` - JavaScript code (ESLint validated)
- `.eslintrc.json` - ESLint configuration
- `test_data.json` - Optional test data
- `_00_serve_poclet-sim.bat` - Local server script
- `M0_{name}_SimulationIssues.md` - Issue tracker

**Modified**: None (all new files)

### Repository-Wide Knowledge Resources (in `ontology/InstanceSimulations/`)

**Created** (if not exists):
- `M0_InstanceSimulations.jsonld` - Simulation catalog (design patterns, technical solutions)
- `M0_InstanceSimulations_README.md` - Narrative guide with code examples
- `M0_InstanceSimulation_UXControls.jsonld` - UX component catalog (formal definitions)
- `M0_InstanceSimulation_UXControls_README.md` - Copy-paste ready UX patterns

**Modified**:
- `M0_InstanceSimulations.jsonld` - Add new simulation entry
- `M0_InstanceSimulations_README.md` - Add simulation to completed list, document patterns
- `M0_InstanceSimulation_UXControls.jsonld` - Add/update UX controls if new/modified
- `M0_InstanceSimulation_UXControls_README.md` - Add/update code examples if new/modified

### Grammar & Migration (in `ontology/TSCG_Grammar/`)

**Created** (if not exists):
- `SHACL_GrammarIssues.jsonld` - Grammar error log
- `migrate_m1core_to_m1.py` - Migration script

**Modified**:
- `SHACL_GrammarIssues.jsonld` - Append errors (if found)

---

## Testing & Validation

### Automated Validation

**ESLint** (mandatory):
```bash
eslint --config .eslintrc.json src/{name}.js
```
- Must pass with 0 errors
- Warnings documented in SimulationIssues.md

**Manual Validation** (recommended):
- Test in browser (Chrome, Firefox, Edge)
- Check console for errors (F12 DevTools)
- Verify all UI components functional
- Test on different screen sizes
- Validate against UX Controls catalog patterns

### Quality Checklist

Before delivering prototype:
- [ ] ESLint validation passed (0 errors)
- [ ] All UX components from catalog implemented correctly
- [ ] Splitter works (DragToAdjust pattern)
- [ ] Tabs switch correctly (TabPanel pattern)
- [ ] BabylonJS scene renders
- [ ] No console errors
- [ ] Code follows TSCG conventions (author attribution, etc.)
- [ ] SimulationIssues.md initialized

Before Step 4 Green Light:
- [ ] User has tested all features
- [ ] All reported issues resolved
- [ ] Claude review completed
- [ ] Catalogs ready for update (including UXControls if applicable)

---

## Best Practices

### Code Structure

**Modular Architecture**:
- Separate HTML/CSS/JS files in `src/` folder (not monolithic)
- Reuse UX patterns from catalog whenever possible
- Instance-specific adaptations clearly documented

**BabylonJS Setup**:
- Use stable CDN version (https://cdn.babylonjs.com/babylon.js)
- One engine per canvas
- Proper disposal in reset functions
- Window resize handler
- Follow ArcRotateCamera pattern from UX Controls

**UI Components**:
- **Always consult** `M0_InstanceSimulation_UXControls_README.md` before implementing controls
- Use copy-paste ready code examples
- Adapt patterns to instance needs
- Document any deviations from standard patterns

### Using the UX Controls Catalog

**Workflow**:
1. **Identify needed controls** during Step 2 (Conceptualization)
2. **Read catalog entry** in `M0_InstanceSimulation_UXControls.jsonld`
3. **Copy code example** from `M0_InstanceSimulation_UXControls_README.md`
4. **Adapt to instance** (colors, labels, data bindings)
5. **Test implementation**
6. **Document innovations** if you enhance/modify the pattern

**Example - Adding CombolistWithClear**:
1. Open `M0_InstanceSimulation_UXControls_README.md`
2. Find "Selection Controls > Combolist + Clear Button"
3. Copy HTML/CSS/JavaScript snippets
4. Replace placeholder data with instance-specific values (e.g., 118 elements)
5. Test dropdown selection and clear button
6. If you add new feature (e.g., keyboard navigation), document it in UXControls catalog

### Updating UX Controls Catalog

**When to Update**:
- You create a **new UX control** not in the catalog
- You **significantly enhance** an existing control (new mode, feature, behavior)
- You discover a **better implementation** of a standard pattern

**How to Update**:
1. **Add to JSON-LD** (`M0_InstanceSimulation_UXControls.jsonld`):
   - Complete definition with components, behavior, styling
   - Examples referencing your instance
2. **Add to README** (`M0_InstanceSimulation_UXControls_README.md`):
   - Code snippets (HTML, CSS, JavaScript)
   - Usage notes and best practices
3. **Update changelog** in both files
4. **Test examples** work standalone (copy-paste into empty HTML file)

**Quality Standard**:
- Code examples must be **complete and runnable**
- Descriptions must be **clear enough for someone unfamiliar with your simulation**
- Patterns must be **generic enough to apply to other instances**

### Documentation

**In Code**:
- Author attribution: "Echopraxium with the collaboration of Claude AI"
- Section comments for major blocks
- Explain non-obvious BabylonJS techniques
- Reference UX Controls catalog when using standard patterns

**In SimulationIssues.md**:
- Date each iteration
- Clear issue descriptions
- Document why changes were made
- Track ESLint warnings

**In Catalogs**:
- Complete pattern descriptions
- Link to similar instances
- Document BabylonJS techniques used
- Keep UX Controls catalog up-to-date

### Performance

- Use instanced meshes for repeated geometry
- Dispose unused meshes/materials
- Optimize render loop (avoid heavy computations)
- Consider LOD (Level of Detail) for complex scenes

---

## Troubleshooting

**Splitter not draggable**:
- Check for `mousedown` events (not `pointerdown`)
- Verify CSS `cursor: col-resize` on splitter element
- Ensure `--sidebar-w` CSS variable is defined
- Reference: DragToAdjust pattern in UX Controls catalog

**Tabs not switching**:
- Verify `activateTab(idx)` function is defined
- Check onclick handlers reference correct function
- Ensure `.active` CSS class toggles visibility
- Reference: TabPanel pattern in UX Controls catalog

**BabylonJS scene not rendering**:
- Check canvas element exists (`getElementById('canvas-main')`)
- Verify engine.runRenderLoop() is called
- Look for JavaScript errors in console
- Ensure camera and light are added to scene
- Reference: ArcRotateCamera pattern in UX Controls catalog

**ESLint validation fails**:
- Review specific errors reported
- Check for undefined variables (BabylonJS globals)
- Verify .eslintrc.json has `"BABYLON": "readonly"` in globals
- Consider auto-fix: `eslint --fix src/{name}.js`

**UX Control not working as expected**:
- Verify you copied the complete code example from UXControls README
- Check CSS classes match the catalog specification
- Ensure event listeners are attached after DOM loads
- Compare your implementation to reference instance in catalog

---

## Advanced Features

### Multiple Views (Optional)

For instances needing 2-3 views (like Ptoe - Nautilus + Orbital):

**Pattern**: DualCanvasLayout (see UX Controls catalog)
```html
<div id="view-ne">
  <div id="ne-titlebar">
    <button id="ne-toggle">−</button>
    <button id="swap-btn">⇄</button>
  </div>
  <div id="ne-body">
    <canvas id="canvas-secondary"></canvas>
  </div>
  <div id="ne-resize-handle"></div>
</div>
```

**Setup**:
- Second engine + scene for secondary canvas
- Swap button exchanges main/secondary views
- Collapse/expand toggle for NE panel
- Resize handle for panel dimensions (DragToAdjust pattern)

**See Example**: `instances/poclets/Ptoe/static/` for full implementation  
**See Catalog**: `M0_InstanceSimulation_UXControls.jsonld` → `m0:DualCanvasLayout`

### Custom Controls

**Bottom Bar Extensions** (see ParameterControls in UX Controls catalog):
- Sliders for continuous parameters (speed, scale, etc.)
- ComboBoxes for mode selection
- Toggle buttons for feature activation
- Play/Pause for animations

**Implementation**:
```html
<div id="bottom-bar">
  <button id="reset-btn">Reset</button>
  <label>
    <input type="checkbox" id="auto-rotate-cb">
    Auto Rotate
  </label>
  <input type="range" id="speed-slider" min="0" max="2" step="0.1" value="1">
  <label>Speed</label>
</div>
```

**See Catalog**: `M0_InstanceSimulation_UXControls_README.md` → "Complete Example: Auto Rotate Toggle + Slider"

### Test Data

**Optional** `test_data.json`:
```json
{
  "elements": [
    {"id": 1, "name": "Item A", "value": 42},
    {"id": 2, "name": "Item B", "value": 73}
  ],
  "config": {
    "defaultSpeed": 1.0,
    "maxItems": 100
  }
}
```

**Load in JavaScript**:
```javascript
// Note: fetch() requires server, not file:// protocol
// Use _00_serve_poclet-sim.bat for testing
fetch('test_data.json')
  .then(r => r.json())
  .then(data => {
    console.log('Test data loaded:', data);
    // Use data.elements, data.config, etc.
  });
```

---

## Version History

- **v1.0.0** (2026-04-30): Initial skill creation
  - 4-step workflow (Inputs, Conceptualization, Prototyping, Finalization)
  - Modular architecture (HTML + src/CSS + src/JS)
  - ESLint validation (browser environment)
  - Error detection (m1core: → m1:) with migration script
  - Pattern library (M0_InstanceSimulations catalogs)
  - Issue tracking (SimulationIssues.md)
  - Tested splitter pattern (mousedown events)
  - Claude review integration

- **v1.1.0** (2026-05-05): UX Controls Catalog Integration
  - Added `ontology/InstanceSimulations/` directory for knowledge resources
  - Introduced UX Controls catalog (M0_InstanceSimulation_UXControls.*)
  - Documented 11 simulations' worth of UX patterns
  - Established src/ folder convention for CSS/JS separation
  - Mandatory catalog consultation before implementing UI components
  - Catalog update workflow for new/modified controls
  - Copy-paste ready code examples for all standard UX patterns

---

## Related Skills

- **tscg-instance-pipeline**: Prerequisite - creates M0 ontology and documentation
- **tscg-article-pipeline**: For research article generation from TSCG instances

---

## License & Attribution

Created by: Echopraxium with the collaboration of Claude AI
Framework: TSCG (Transdisciplinary System Construction Game)
Repository: https://github.com/Echopraxium/tscg

---

## Knowledge Resources Location

**UX Controls Catalog**: `ontology/InstanceSimulations/`
- `M0_InstanceSimulation_UXControls.jsonld` - Formal UX component definitions
- `M0_InstanceSimulation_UXControls_README.md` - Code examples and usage guide

**Design Patterns & Solutions**: `ontology/InstanceSimulations/`
- `M0_InstanceSimulations.jsonld` - Simulation catalog with patterns and techniques
- `M0_InstanceSimulations_README.md` - Narrative guide with lessons learned

These resources are **living documents** maintained across all simulation development and must be consulted during Step 2 (Conceptualization) and updated during Step 4 (Finalization) when applicable.
