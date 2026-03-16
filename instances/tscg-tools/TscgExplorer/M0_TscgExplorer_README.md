# M0_TscgExplorer — TscgTool Ontology README

**Version**: 1.0.0  
**Date**: 2026-03-01  
**Authors**: Echopraxium with the collaboration of Claude AI  
**Ontology type**: `m3:TscgTool`  
**File**: `M0_TscgExplorer.jsonld`

---

## Executive Summary

`M0_TscgExplorer` is the first instance of the **`m3:TscgTool`** ontology type — a new category added to `M3_GenesisSpace.jsonld` (v3.6.0) specifically for software tools that operate reflexively **on the TSCG framework itself**.

Unlike a standard Poclet (which models an external system such as biology or engineering), `TscgExplorer` models a tool whose **subject matter IS the TSCG M2 GenericConcept corpus**. This makes it a second-order artefact: a Map of a Map.

**Key results**:
1. ✅ **ASFID overall: 0.78** — rich structural and informational content
2. ✅ **REVOI overall: 0.78** — equally strong representability and observability
3. ✅ **Epistemic gap δ = 0.00** — perfect Territory/Map symmetry (mature tool)
4. ✅ **8 M2 GenericConcepts** identified as characterising the tool itself
5. ✅ **3 projection modes** formalised as `owl:NamedIndividual` instances
6. ✅ **Framework reflexivity** demonstrated: TSCG analyses itself through its own constructs

---

## Table of Contents

1. [System Description](#1-system-description)
2. [TSCG Layer Position](#2-tscg-layer-position)
3. [ASFID Analysis (Territory)](#3-asfid-analysis-territory)
4. [REVOI Analysis (Map)](#4-revoi-analysis-map)
5. [Epistemic Gap](#5-epistemic-gap)
6. [GenericConcepts Used](#6-genericconcepts-used)
7. [Projection Modes](#7-projection-modes)
8. [Reflexivity Note](#8-reflexivity-note)
9. [Companion File](#9-companion-file)

---

## 1. System Description

### 1.1 What is TscgExplorer?

**TscgExplorer** is an interactive 2D visualisation tool for the **81 M2 GenericConcepts** of the TSCG framework, implemented as a Python/pygame desktop application (`tscg_explorer.py`).

**Function**: Navigate, inspect and analyse the M2 GenericConcept corpus through three complementary 2D projections of the underlying 10-dimensional tensor space.

**Architecture**:
```
tscg_explorer.py
├── LEFT  panel  — IS-A Tree Explorer (collapsible families/nodes)
├── CENTER panel — 2D concept net (3 projection modes, zoom, pan)
│                  ├── Legend (family colours, node shapes)
│                  └── Mode buttons [A] [B] [C]
└── RIGHT panel  — Concept Profile (formula tiles, ASFID/REVOI scores)
                   ── horizontal splitter ──
                   README (scrollable M2 quick reference)
```

**Three vertical panels** separated by two draggable vertical splitters.  
**One horizontal splitter** inside the right panel (profile / readme).

### 1.2 Key Characteristics

| Aspect | Value |
|--------|-------|
| Tool type | Interactive visualiser / corpus explorer |
| Implementation | Python 3 / pygame |
| Target artefacts | `M2_GenericConcepts.jsonld` (81 concepts) |
| Node shapes | ▲ Triangle = atomic · ◆ Diamond = Combo |
| Node colours | By family (10 distinct colours) |
| Formula display | Coloured tiles + ⊗ (circle-cross) operators |
| Projection modes | 3 (A, B, C — see §7) |
| Edge types | Solid blue = IS-A · Dashed orange = Combo ⊗⇒ |
| Dependency | `pip install pygame` |

---

## 2. TSCG Layer Position

```
M3  GenesisSpace  — bicephalous basis (ASFID ⊕ REVOI)
 │
M2  GenericConcepts — 81 universal patterns        ← INPUT of TscgExplorer
 │
M1  CoreConcepts / Domain Extensions
 │
M0  TscgExplorer  ◄─────────────────────────────── THIS FILE
     (m3:TscgTool — models a tool that reads M2)
```

`TscgExplorer` is positioned at M0 level but typed as `m3:TscgTool`, not `m3:Poclet`. The distinction:

| Property | `m3:Poclet` | `m3:TscgTool` |
|----------|-------------|----------------|
| Subject matter | External system (biology, physics…) | TSCG artefacts themselves |
| Validation | Empirical (domain experts) | Framework reflexivity |
| Completeness | All ASFID dims required | Tool-specific |
| Example | `M0_RAAS.jsonld` | `M0_TscgExplorer.jsonld` |

---

## 3. ASFID Analysis (Territory)

> Eagle Eye perspective — *what the tool IS*

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **A** Attractor | 0.70 | Primary goal: reveal density zones and structural gaps in the 81-concept corpus. The tool converges toward visualisation clarity as its stable state. |
| **S** Structure | 0.90 | Core output IS a structural representation: the 2D network graph with IS-A and Combo ⊗⇒ edges. Three panels, mode buttons, legend — all explicit structural choices. |
| **F** Flow | 0.80 | Multiple interaction flows: node selection, README reading, pan/zoom, mode switching. The tool mediates the cognitive flow between analyst and M2 ontology. |
| **I** Information | 0.90 | Rich information display: tensor formulas, ASFID/REVOI counts, family, superclass, Combo components, ConceptContracts, embedded README. |
| **D** Dynamics | 0.60 | 60 fps rendering; real-time state updates on interaction. Dynamics present but secondary — the tool is primarily structural/informational rather than temporally evolving. |

**ASFID vector**: `[0.70, 0.90, 0.80, 0.90, 0.60]`  
**ASFID overall**: **0.78**

**Dominant dimensions**: S (Structure) and I (Information) — coherent with a tool whose primary purpose is rendering structured knowledge.

---

## 4. REVOI Analysis (Map)

> Sphinx Eye perspective — *how the tool is KNOWN*

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **R** Representability | 0.90 | Encodes 81 GenericConcepts as visual nodes across three distinct 2D projections of the same tensor space. High semantic encodability. |
| **E** Evolvability | 0.80 | Concept data is embedded as Python structures mirroring JSON-LD — straightforward to update as M2 grows. New projection modes require only a new position-computation function. |
| **V** Verifiability | 0.70 | Visual verification: IS-A edges connect correct superclasses, Combo edges point to declared components. No automated consistency checker yet (planned as separate `TscgTool`). |
| **O** Observability | 0.90 | All concept properties directly observable via profile panel on click. Three modes reveal density zones, gaps, and Territory/Map balance. |
| **Im** Interoperability | 0.60 | Self-contained; no external API calls. Future versions could load from `M2_GenericConcepts.jsonld` via rdflib. Interoperability with other TSCG tools planned but not in v1.0.0. |

**REVOI vector**: `[0.90, 0.80, 0.70, 0.90, 0.60]`  
**REVOI overall**: **0.78**

**Dominant dimensions**: R (Representability) and O (Observability) — coherent with a visualisation tool designed to make invisible structure visible.

---

## 5. Epistemic Gap

```
δ = |ASFID_overall − REVOI_overall| = |0.78 − 0.78| = 0.00
```

**Interpretation**: Perfect Territory/Map symmetry. The tool is as well-observable (REVOI) as it is structurally rich (ASFID). This is the signature of a **mature, well-designed tool** — the map faithfully represents the territory.

| δ range | Maturity |
|---------|----------|
| 0.00 – 0.10 | Mature — tool well understood and well represented |
| 0.10 – 0.30 | Developing — some aspects not yet captured in the model |
| 0.30 – 0.60 | Emerging — significant epistemic gaps remain |
| > 0.60 | Speculative — model far from reality |

`TscgExplorer` sits at the optimal end of this scale.

---

## 6. GenericConcepts Used

The tool itself is characterised by 8 M2 GenericConcepts — a reflexive application of the framework:

| GenericConcept | Formula | Role in TscgExplorer |
|----------------|---------|----------------------|
| **Network** | S ⊗ I ⊗ F ⊗ D ⊗ Im | The concept graph IS a network: nodes + IS-A/Combo edges |
| **Representation** | S ⊗ I ⊗ V ⊗ R | Three projection modes = three representations of the same tensor space |
| **Observer** | A ⊗ I ⊗ R | The analyst navigating the tool acts as Observer of the M2 corpus |
| **ValueSpace** | I ⊗ V ⊗ O ⊗ R ⊗ Im | Each concept's tensor formula IS its ValueSpace, displayed in the profile panel |
| **Hierarchy** | A ⊗ S ⊗ V ⊗ R | IS-A edges render the rdfs:subClassOf hierarchy as visible solid blue lines |
| **Cascade** | S ⊗ I ⊗ D ⊗ F ⊗ R | Combo ⊗⇒ edges visualise synergistic assembly chains |
| **Topology** | S ⊗ I ⊗ A ⊗ V | Each projection mode reveals a different topological reading of concept space |
| **FeedbackLoop** | A ⊗ S ⊗ I ⊗ F ⊗ D ⊗ V ⊗ R ⊗ E | User interaction → display update → refined understanding → new interaction (Φ/Ψ epistemic loop) |

---

## 7. Projection Modes

Three modes project the 10D tensor space onto a 2D plane, each revealing different structural properties:

### Mode A — ASFID ratio × Dimensionality (default)
```
X = ASFID_count / total_dims  ∈ [0, 1]
    0 = pure REVOI (Map)   1 = pure ASFID (Territory)
Y = total tensor dimensions  ∈ [1, 8]
```
**Reveals**: Eagle Eye vs Sphinx Eye balance across the corpus. Concepts clustering toward X=1 are Territory-dominant; toward X=0 they are Map-dominant.

### Mode B — Family × Dimensionality
```
X = family index (ordinal, 0–9 across 10 families)
Y = total tensor dimensions  ∈ [1, 8]
```
**Reveals**: Intra-family dimensional spread. Families with wide Y ranges have both simple and complex concepts. Cross-family comparison of dimensionality.

### Mode C — ASFID count × REVOI count
```
X = number of ASFID dimensions in formula  ∈ [0, 5]
Y = number of REVOI dimensions in formula  ∈ [0, 5]
```
**Reveals**: Pure bicephalous decomposition. Concepts on the X-axis are pure Territory; on the Y-axis pure Map; on the diagonal they are balanced.

---

## 8. Reflexivity Note

> *"A TscgTool exhibits framework reflexivity: TSCG analyses itself through its own GenericConcepts."*

**Manifestation**: `tscg-explorer` uses `m2:Network`, `m2:Representation`, `m2:Observer`, `m2:Hierarchy` to describe a tool that **displays those very same concepts**.

**Korzybski connection**: The tool is a **Map of the Map** — it renders the M2 GenericConcept layer (which is itself a Map of Territory phenomena) as a navigable 2D graph. This is a second-order cartographic act.

**Epistemic value**: Visualising density zones and gaps in the concept net reveals whether the TSCG framework has **blind spots** — regions of systemic experience not yet captured by a GenericConcept.

The `m3:FeedbackLoop` between analyst and tool mirrors the Φ/Ψ alignment loop at the heart of the bicephalous architecture:
```
Φ: analyst observes concept net → insight about M2 structure
Ψ: insight refines analyst's model → changes what they look for next
```

---

## 9. Companion File

| File | Description |
|------|-------------|
| `M0_TscgExplorer.jsonld` | This ontology (m3:TscgTool) |
| `tscg_explorer.py` | Python/pygame implementation |
| `tscg_explorer_README.md` | Technical README for the Python tool |

**Ontology imports**:
```json
"owl:imports": [
  "M2_GenericConcepts.jsonld",
  "M1_CoreConcepts.jsonld"
]
```

**GitHub location** (planned):
```
instances/tscg-tools/TscgExplorer/
  ├── M0_TscgExplorer.jsonld
  ├── M0_TscgExplorer_README.md
  └── tscg_explorer.py
```

---

*Echopraxium with the collaboration of Claude AI — 2026-03-01*
