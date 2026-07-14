# 2D Barcode Pedagogical Poclet and Democratization Facet

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-06-28
**Status**: Infrastructure complete (M0_Common v1.2.0 + SHACL v1.6) — instances to be tagged
**TSCG Version**: 16.2.0
**Related files**: `M0_Common.jsonld` v1.2.0, `M0_Instances_Schema.shacl.ttl` v1.6

---

## Part 1 — The 2D Barcode Pedagogical Poclet

### 1.1 Concept

The goal is a comparative interactive simulation that demonstrates how three 2D barcode symbologies solve the same fundamental problem — **encoding a message so it remains readable under any orientation and survives partial physical damage** — using three different geometric strategies.

The three symbologies:

| Symbology | Geometry | Localization strategy |
|---|---|---|
| **QR Code** | Square grid of square modules | 3 finder patterns at corners + alignment + timing |
| **DataMatrix** | Square or rectangular grid | Solid L-shaped border + dotted clock track on 2 opposite sides |
| **MaxiCode** | Fixed 28×28 hexagonal grid | Central bullseye (concentric rings) + hexagonal modules |

### 1.2 Why Three, Not One

Comparing three symbologies with a *controlled variation* reveals structure that a single example cannot. If you hold the **payload (Ss)** and **error correction (It)** constant and vary only the **geometry (S)** and **localization strategy (L)**, the reader understands that L is not incidental — it is the *defining design choice* that distinguishes one symbology from another.

This controlled variation is close to an experiment: it demonstrates that the **L (Localizability) primitive** from the TSCG Stereopsis grammar (Gs) is the core discriminating dimension across 2D barcode design space.

### 1.3 TSCG Analysis

#### ASFID (Territory — Gt)

| Dimension | Common to all three | QR specific | DataMatrix specific | MaxiCode specific |
|---|---|---|---|---|
| **A** | Decoded message is the unique attractor | Strong (3 finders) | Strong (L-border) | Strong (bullseye) |
| **S** | Binary module matrix | Square, variable size (21→177) | Square/rect, variable size | Fixed 28×28 hexagonal |
| **F** | Zigzag/serpentine reading path | Column pairs, right to left | Diagonal reading path | Radial reading from center |
| **It** | Reed-Solomon ECC | Up to 30% module loss | Up to 30% module loss | 3 primary + 3 secondary |
| **D** | Self-correction under damage | Mask pattern selection | No masking (L-border sufficient) | Fixed encoding, no mask |

#### Gs (Stereopsis — L primitive as central feature)

The **L (Localizability)** primitive — *ordinal discrimination of the direction of convergence toward an Attractor by comparison of successive states* — manifests differently in each symbology:

- **QR**: reader locates itself by triangulating from 3 finder patterns → **localization by triangulation**
- **DataMatrix**: reader orients using the solid L-border as a clock + the dotted track as a cadence reference → **localization by frame + cadence**
- **MaxiCode**: reader locates center by detecting the bullseye and reads radially outward → **localization by radial center**

Three distinct answers to the same question: *"How does the reading head know where it is?"*

### 1.4 Pedagogical Value

This poclet is the **strongest candidate in the current corpus for illustrating the L primitive**, which was previously the most abstract and least illustrated of the four Gs/TKSL primitives (T, K, Ss, L). The simulation makes L *concrete and contrasting*: the same primitive, three implementations, visible side by side.

Secondary concepts illustrated:

- `m2:Coding` (Encoding/Decoding pair) — the transformation `It × St × D | _^/_$`
- `m2:Redundancy` — error correction as structural over-specification
- `m2:Symmetry` — QR finder pattern (rotationally asymmetric by design to allow orientation detection)
- `m2:Trade-off` — module density vs. error correction capacity vs. physical size

### 1.5 Simulation Design

**Library**: p5.js (2D symbolic simulation convention for TSCG pedagogical content)
**Target**: Mobile-first, self-contained HTML
**Interaction model**: Step-by-step animated pipeline — user taps through each stage:

```
Stage 1 — Locate    : highlight the localization structure (finder / L-border / bullseye)
Stage 2 — Orient    : show orientation disambiguation
Stage 3 — Sample    : animate the reading path (zigzag / diagonal / radial)
Stage 4 — Unmask    : apply/remove the mask pattern (QR only)
Stage 5 — Correct   : simulate damage + recovery via ECC
Stage 6 — Decode    : reveal the message
```

**Scope discipline**: Reed-Solomon GF(256) arithmetic is **not** implemented — error correction is demonstrated as *"N modules can be lost and the message remains recoverable"* with a visual stub. Full ECC implementation would be a separate engineering exercise, not a pedagogical necessity.

---

## Part 2 — The Democratization Facet

### 2.1 Motivation

As the TSCG M0 corpus grows, a structural gap emerged: the existing M0 properties (ASFID/REVOI scores, spectralClass, focalClass, scoringStatus) describe a system's *intrinsic qualities*, but say nothing about its *affordance* — what role it plays for a particular audience.

Several poclets are demonstrably effective at making systemic modeling accessible to non-specialists (FireTriangle, ExposureTriangle, CellSignalingModes). This affordance is:
- **Orthogonal** to the instance type (a Poclet, SystemicFramework, or TscgTool can all have it)
- **Externally conferred** (by usage context, not intrinsic to the system modeled)
- **Map-perspective** (it describes how the instance is represented and used, not what the system does)

This is precisely the definition of a **role** in BFO (Basic Formal Ontology) — and maps directly onto `m2:Role` (`Ss | K`, perspective map) already present in M2_GenericConcepts.

### 2.2 Design Principles

The facet mechanism follows three principles established during design:

1. **Orthogonality**: facets are *not* sub-types of `m3:ontologyType`. Creating `m3:PedagogicPoclet` would re-open the combinatorial explosion that the four-type taxonomy was designed to prevent. A facet is a separate axis.

2. **Contract over label**: declaring a facet is not a badge — it obligates the instance to provide structured content (enforced by SHACL). Without the contract, the facet degenerates into a self-congratulatory tag.

3. **Parsimony**: the mechanism is built into `M0_Common.jsonld` (shared vocabulary) and `M0_Instances_Schema.shacl.ttl` (enforced contract), not in a separate file. Consistent with the principle *"shared M0 properties over per-file definitions"*.

### 2.3 Architecture

#### M0_Common.jsonld — New nodes (v1.2.0)

| Node | Type | Role |
|---|---|---|
| `m0:Facet` | `owl:Class` | Abstract superclass of all facet types |
| `m0:hasFacet` | `owl:ObjectProperty` | Links an instance to its declared facets |
| `m0:facet.Democratization` | `owl:NamedIndividual`, `m0:Facet` | First registered facet |
| `m0:illustratesConcept` | `owl:AnnotationProperty` | **Required** by Democratization contract |
| `m0:RoleGrounding` | `owl:Class` (`owl:oneOf`) | Enum: `Reused` / `Designed` |
| `m0:roleGrounding.Reused` | `owl:NamedIndividual` | Externally conferred role |
| `m0:roleGrounding.Designed` | `owl:NamedIndividual` | Teleologically intrinsic role |
| `m0:roleGrounding` | `owl:ObjectProperty` | Optional grounding qualifier |

#### M0_Instances_Schema.shacl.ttl — New shapes (v1.6)

| Shape | Type | Constraint |
|---|---|---|
| `m0:DemocratizationFacetContractShape` | SPARQL | `hasFacet = Democratization` → `illustratesConcept` minCount 1 |
| `m0:ForbidStringHasFacetShape` | `sh:not` | `hasFacet` must be IRI, never string |
| `m0:RoleGroundingShape` | `sh:property` | `roleGrounding` must be `Reused` or `Designed` |
| `m0:ForbidStringRoleGroundingShape` | `sh:not` | `roleGrounding` must be IRI, never string |

#### Ontological grounding

```
m0:facet.Democratization
  anchored on  →  m2:Role  (Ss | K, perspective map)
  grounding    →  BFO role (externally conferred, contingent)
  distinct from →  m0:ScoringProperty (derived quality, calculated)
                   m0:FocalProperty   (Gs depth, conditional on stereopsic GCs)
```

### 2.4 The roleGrounding Distinction

| Value | Meaning | BFO analogy | Example |
|---|---|---|---|
| `m0:roleGrounding.Reused` | Instance designed for its primary systemic purpose; proves effective pedagogically as a secondary affordance | **BFO role** — externally conferred by usage context | FireTriangle, ExposureTriangle |
| `m0:roleGrounding.Designed` | Instance specifically conceived to serve a pedagogical purpose | **BFO function** — teleologically intrinsic to the design intent | 2D Barcode decoder comparator |

The distinction matters for corpus analysis: `Reused` instances are opportunistic pedagogical assets discovered post-hoc; `Designed` instances are deliberate investments in the democratization mission.

### 2.5 Usage Pattern

```json
{
  "@id": "M0_FireTriangle.jsonld",
  "@type": "owl:Ontology",
  "m3:ontologyType": { "@id": "m3:Poclet" },

  "m0:hasFacet": { "@id": "m0:facet.Democratization" },
  "m0:roleGrounding": { "@id": "m0:roleGrounding.Reused" },
  "m0:illustratesConcept": "ASFID completeness — all five Territory dimensions (Attractor, Structure, Flow, Information, Dynamics) are necessary and sufficient for combustion"
}
```

```json
{
  "@id": "M0_ExposureTriangle.jsonld",

  "m0:hasFacet": { "@id": "m0:facet.Democratization" },
  "m0:roleGrounding": { "@id": "m0:roleGrounding.Reused" },
  "m0:illustratesConcept": { "@id": "m2:Balance" }
}
```

```json
{
  "@id": "M0_2DBarcodeDecoder.jsonld",

  "m0:hasFacet": { "@id": "m0:facet.Democratization" },
  "m0:roleGrounding": { "@id": "m0:roleGrounding.Designed" },
  "m0:illustratesConcept": "Localizability (L primitive, Gs grammar) — three distinct geometric strategies for a reading head to locate itself within a 2D symbol"
}
```

### 2.6 Corpus Instances Eligible for Democratization Tagging

Based on current corpus analysis, the following instances are immediate candidates:

| Instance | `illustratesConcept` | `roleGrounding` |
|---|---|---|
| `M0_FireTriangle` | ASFID completeness | Reused |
| `M0_ExposureTriangle` | `m2:Balance` | Reused |
| `M0_TrophicPyramid` | `m2:Hierarchy` + energy flow | Reused |
| `M0_ButterflyMetamorphosis` | `m2:Transformation` + phase discontinuity | Reused |
| `M0_PhaseTransition` | `m2:Bifurcation` | Reused |
| `M0_2DBarcodeDecoder` *(to create)* | L primitive (Localizability) | Designed |

### 2.7 Extension Mechanism

The facet infrastructure is designed for future facets beyond Democratization. Admission criteria for a new facet:

1. **Orthogonal** to `m3:ontologyType` — applicable across ≥2 instance types
2. **Applicable** to ≥3 existing instances — not a one-off
3. **Contractual** — imposes at least one required field (enforced by SHACL)
4. **Map-perspective** — describes affordance or role, not intrinsic Territory properties

Candidate future facets (not yet defined):
- `m0:facet.Comparative` — instance explicitly contrasts ≥2 systems on the same structural axis
- `m0:facet.Interactive` — instance has a mandatory interactive simulation (not just static JSON-LD)

---

## 3. Summary of Deliverables

### Infrastructure (completed 2026-06-28)

| File | Version | Changes |
|---|---|---|
| `M0_Common.jsonld` | 1.2.0 | +8 nodes: Facet infrastructure (Facet class, hasFacet, facet.Democratization, illustratesConcept, RoleGrounding, roleGrounding enum + property) |
| `M0_Instances_Schema.shacl.ttl` | 1.6 | +4 shapes: DemocratizationFacetContractShape, ForbidStringHasFacetShape, RoleGroundingShape, ForbidStringRoleGroundingShape |

### Pending

| Task | Priority |
|---|---|
| Apply Democratization tags to FireTriangle, ExposureTriangle, TrophicPyramid, ButterflyMetamorphosis, PhaseTransition | High |
| Create `M0_QRCode.jsonld` as standard Poclet | High |
| Create `M0_2DBarcodeDecoder.jsonld` (Designed, Democratization) | Medium |
| Build p5.js simulation for 2D barcode comparator | Medium |
| Define `m3:Enigma` formally (blocker for ExploratorySpace type decision) | Low |
