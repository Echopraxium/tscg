# TscgOntologyExplorer — README

**Type:** `m3:TscgTool`  
**Version:** 1.0.0  
**Domain:** TSCG (reflexive — TSCG models itself)  
**Author:** Echopraxium with the collaboration of Claude AI  
**Path:** `instances/tscg-tools/TscgOntologyExplorer/`  
**M0 Ontology:** `M0_TscgOntologyExplorer.jsonld`  

---

## Overview

TscgOntologyExplorer is a TSCG-dedicated ontology browser and explorer built with ElectronJS (vanilla JS, no React, no bundlers). It serves as a focused alternative to Protégé, designed specifically around the TSCG M3→M2→M1→M0 layer architecture.

The tool operates in two modes:

- **Browse mode** (default) — read-only navigation of any TSCG `.jsonld` ontology
- **Edit mode** — property editing with SHACL validation gate before any disk write

### Key differentiator: the Bootstrap Strange Loop

TscgOntologyExplorer can load and edit its own `M0_TscgOntologyExplorer.jsonld` specification in Edit mode. Each iteration of the tool can thus refine its own formal description, which then drives the next development cycle. This reflexive self-improvement loop is the TSCG TscgTool principle in action (Hofstadter Strange Loop).

---

## UI Layout

```
┌─────────────────┬──────────────────────┬───────────────────────────┐
│  Object         │  Property            │  [Description] [Gap] [↕] │
│  Explorer       │  Inspector           │                           │
│                 │                      │  NeighborLayer tab:       │
│  ▼ M2           │  ▼ Metadata          │  ┌──────────┐            │
│    ▶ Regulation │    label: …          │  │ M3 (↑)   │──────────► │
│    ▶ Homeostasis│    comment: …        │  └──────────┘            │
│    ▶ Emergence  │    version: …        │  ┌──────────┐            │
│    ▶ …          │  ▼ OntologyType      │  │ M1 (↓)   │──────────► │
│                 │    TscgTool          │  └──────────┘            │
│  [108 items]    │  ▼ Scores            │                           │
│                 │    A: 0.85  S: 0.90  │  δ₁ = 0.0316             │
│                 │    F: 0.80  …        │  ◉ Coherent               │
└─────────────────┴──────────────────────┴───────────────────────────┘
     Left panel        Center panel              Right panel
  (Blender Outliner)  (Blender Properties)    (tabbed — 3 tabs)
```

### Left panel — Object Explorer

Tree of objects in the active ontology. Each node is selectable; selection feeds the center and right panels. Expand/collapse chevrons for nested structures. Style inspired by Blender's Outliner.

### Center panel — Property Inspector

Collapsible drawers for each property group. In **Browse mode** all fields are read-only. In **Edit mode** supported fields become form inputs.

| Drawer | Properties shown |
|--------|-----------------|
| `@context` | Namespace prefixes and short-key aliases |
| Metadata | `rdfs:label`, `rdfs:comment`, `dcterms:creator`, dates, `owl:versionInfo` |
| OntologyType | `m3:ontologyType`, `m1:domain` |
| Scores | `m0:asfidScores`, `m0:revoiScores` (inline mini radar) |
| Changelog | `m2:changelog` entries (rolling 3-entry view) |
| Imports | `owl:imports` list |
| Custom | All other properties not covered above |

### Right panel — Tabbed panel

Three tabs, inspired by TSCG simulation sidebars:

**Description** — label, comment, type, domain, version in human-readable format.

**Epistemic Gap** — full ASFID/REVOI radar chart (Canvas 2D), δ₁ value, SpectralClass badge (Coherent / OnCriticalLine / Liminal / Enigmatic), and gap justification text.

**Neighbor Layer (↕)** — adjacent TSCG layers shown as clickable links. Clicking a layer makes it the new active ontology in the Object Explorer.

```
Active layer  │  Neighbors shown
──────────────┼─────────────────────────────────────────
M3            │  M2 (below)
M2            │  M3 (above) · M1 CoreConcepts + extensions (below)
M1 extension  │  M2 (above) · M0 instances using this extension (below)
M0 instance   │  M1 domain extension (above)
```

Navigation history (Back / Forward) is maintained across all layer switches.

---

## Modes

### Browse mode (default)

- All ontology properties rendered as formatted, read-only fields
- ASFID/REVOI radar chart computed live from scores
- Cross-layer navigation via Neighbor Layer tab
- No write access to disk

Entry points:
- Preconfigured quick-access buttons: **M3** · **M2** · **M1**
- File dialog: open any `.jsonld` from the local TSCG repository

### Edit mode *(not yet implemented)*

- Planned for a future version
- Supported properties become editable form fields
- On save attempt: pyshacl validation runs against `M0_Instances_Schema.shacl.ttl`
  - **Pass** → file written to disk, changelog entry auto-timestamped
  - **Fail** → validation report displayed inline, save blocked
- Unsaved changes indicated by a modified indicator in the title bar

**Supported editable properties (v1.0):**
- `rdfs:label`, `rdfs:comment`
- `owl:versionInfo`
- `m1:domain`
- `m0:asfidScores` (A, S, F, It, D sliders 0.0–1.0)
- `m0:revoiScores` (R, E, V, O, Im sliders 0.0–1.0)
- `m2:changelog` (add/edit/remove entries, rolling 3-entry enforcement)

---

## Bootstrap Mechanism

The bootstrap Strange Loop operates as follows:

```
1. Open M0_TscgOntologyExplorer.jsonld in Edit mode
2. Identify a missing or underspecified feature
   (e.g., "add SPARQL query panel as a new Attractor")
3. Edit the M0 property in the Property Inspector
4. Trigger SHACL validation (automatic on save)
5. Save if valid → M0 updated → new authoritative specification
6. Implement the feature in the ElectronJS codebase
7. Return to step 1 for next iteration
```

This loop makes `M0_TscgOntologyExplorer.jsonld` both the **product** (formal specification) and the **subject** (data processed by the tool itself) — the TSCG reflexivity principle.

---

## ASFID / REVOI Analysis

### ASFID scores (Territory — Eagle Eye)

| Dim | Score | Justification |
|-----|-------|---------------|
| A_score   | 0.85  | Strong dual attractor: Browse mode (navigation) and Edit mode (modification) are clearly defined stable goals |
| S_score   | 0.90  | Well-defined 3-column architecture with explicit drawer and tab structure |
| F_score   | 0.80  | Clear flow: Load → Select → Display → (Edit → Validate → Save). Cross-layer navigation adds secondary flow. |
| It_score  | 0.85  | Rich information: JSON-LD graph, ASFID/REVOI scores, δ₁, SpectralClass, layer relationships |
| D_score   | 0.70  | Mode switching, cross-layer navigation, SHACL feedback — moderate complexity, not fully stabilized at v1.0 |

**Mean:** 0.82

### REVOI scores (Map — Sphinx Eye)

| Dim | Score | Justification |
|-----|-------|---------------|
| R_score   | 0.80  | M0 faithfully represents architecture, UI layout, modes, and bootstrap. Minor gap: dynamic state (current selection, navigation history) not representable statically. |
| E_score   | 0.90  | Highest score: bootstrap mechanism is the core design — every iteration refines the specification |
| V_score   | 0.85  | SHACL gate before any save. The tool is itself SHACL-validatable, closing the reflexive loop. |
| O_score   | 0.80  | Active ontology, selected object, mode, validation status all visible at all times |
| Im_score  | 0.75  | ElectronJS + JSON-LD (W3C) + SHACL (W3C). Slight reduction: TSCG-specific conventions limit portability. |

**Mean:** 0.82

### Epistemic Gap

```
δ₁ = √[(0.85-0.80)² + (0.90-0.90)² + (0.80-0.85)² + (0.85-0.80)² + (0.70-0.75)²] / √10
   = √[0.0025 + 0 + 0.0025 + 0.0025 + 0.0025] / √10
   = √0.01 / 3.162
   = 0.0316
```

**SpectralClass: Coherent** [0, 0.05) — near-perfect Territory/Map alignment. The M0 specification faithfully captures the tool. Residual gap on Dynamics and Interoperability.

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Runtime | ElectronJS (vanilla JS, no React/bundlers) |
| JSON-LD parsing | `jsonld` npm package |
| SHACL validation | `pyshacl` via `child_process` (Python subprocess) |
| Radar chart | Canvas 2D (no external chart library) |
| UI theme | Vanilla HTML/CSS — dark theme consistent with TSCG tools suite |

---

## Repository Structure

```
instances/tscg-tools/TscgOntologyExplorer/
├── M0_TscgOntologyExplorer.jsonld     ← M0 specification (this instance)
├── M0_TscgOntologyExplorer_README.md  ← This file
├── package.json
├── main.js                          ← Electron main process
├── preload.js                       ← Context bridge (ipcRenderer)
├── renderer/
│   ├── index.html
│   ├── style.css                    ← Dark theme
│   └── renderer.js                  ← UI logic
├── core/
│   ├── OntologyLoader.js            ← JSON-LD load + parse
│   ├── GraphIndex.js                ← M3→M2→M1→M0 index builder
│   ├── ShaclValidator.js            ← pyshacl subprocess wrapper
│   └── EpistemicCalc.js             ← δ₁ computation + SpectralClass
├── views/
│   ├── ObjectExplorer.js            ← Left panel tree
│   ├── PropertyInspector.js         ← Center panel drawers
│   ├── TabDescription.js            ← Right panel — Description tab
│   ├── TabEpistemicGap.js           ← Right panel — Gap + radar
│   └── TabNeighborLayer.js          ← Right panel — Cross-layer nav
└── config/
    └── paths.json                   ← Preconfigured M3/M2/M1 paths
```

---

## Development Roadmap

| Phase | Features | Estimated effort |
|-------|----------|-----------------|
| MVP (v1.0) | Browse mode, 3-column layout, radar chart, δ₁, Neighbor Layer navigation | ~20h |
| v1.1 | Edit mode, SHACL gate, save pipeline, changelog auto-update | ~15h |
| v1.2 | Bootstrap loop UX, navigation history, cross-instance corpus view | ~10h |
| v2.0 | SPARQL query panel, D3.js force graph, side-by-side instance comparison | ~20h |

---

*Author: Echopraxium with the collaboration of Claude AI — 2026-05-15*
