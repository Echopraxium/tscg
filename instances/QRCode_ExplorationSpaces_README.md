# QRCode Exploration Spaces

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-06-28
**Status**: Conceptual Proposal — pending instance type decision
**TSCG Version**: 16.2.0
**Related**: `M0_QRCode.jsonld` (Poclet, to be created), ExploratorySpace (instance type candidate)

---

## 1. Overview

A QR code is, at first glance, a compact data carrier. Looked at through the TSCG lens, it reveals something richer: a **complete ASFID system** where a geometric structure (S) encodes information (It), guides a reading flow (F) toward a unique decoded message (A), and remains recoverable despite partial damage (D via Reed-Solomon). It is a minimal, self-sufficient system — a natural Poclet candidate.

But the QR code also opens a second question: **what happens when its 2D binary matrix is treated not as data to decode, but as a spatial seed for exploration?**

This README documents the proposal to turn the QR code matrix into a **navigable 3D space** — and to examine whether this idea constitutes a new TSCG instance type with a distinct ontological status.

---

## 2. Exploration Modalities

### 2.1 Module Extrusion (most immediate)

The most direct mapping: each dark module is extruded vertically, its height proportional to its position, surrounding density, or payload value. The result is a **3D relief landscape** where the finder patterns become towers, the timing patterns become ridges, and the data region becomes a varied terrain.

The explorer navigates from the data region toward the finder towers — traversing the decoding path in physical space. The Attractor (the decoded message) is literally elevated above the field.

### 2.2 Non-Euclidean Geometries

The flat grid of a QR code is a choice, not a necessity. The same adjacency relationships can be embedded in:

- **Hyperbolic space**: the grid expands exponentially from the center — finder patterns at the boundary become unreachable horizons, mirroring the information-theoretic boundary of the error correction capacity.
- **Spherical space**: modules wrap around a closed surface; the exploration has no edge, only curvature — the decoded message is everywhere equidistant from itself.
- **Elliptic geometry**: antipodal modules are identified — every module has a shadow-twin on the opposite side of the sphere.

### 2.3 Cartographic Projections onto a Sphere

The QR matrix is projected onto a sphere using standard geographic projections, each producing a qualitatively different exploration experience:

| Projection | Character | Distortion |
|---|---|---|
| Mercator | Familiar, rectilinear center | Polar exaggeration |
| Azimuthal equidistant | Finder patterns at poles | Radial symmetry |
| Gnomonic | Great-circle paths as straight lines | Strong peripheral distortion |
| Mollweide | Area-preserving | Shape distortion at edges |
| Dymaxion (Fuller) | Minimal distortion, unfolded icosahedron | Discontinuous |

Each projection makes a different feature of the QR structure salient. Gnomonic projection, for instance, makes the reading path (a geodesic) appear as a straight line through the 3D globe.

### 2.4 Torus Surface

The QR matrix tiles naturally onto a torus: left/right edges join, top/bottom edges join. The result is a **topologically closed exploration space with no boundary** — the explorer can traverse the entire surface without ever reaching an edge. The four-color theorem guarantees that the finder patterns can be distinctly colored on this surface.

This modality is particularly interesting because the torus has genus 1: it introduces a **non-trivial topological invariant** absent from the flat grid. Two exploration paths that look equivalent on the flat QR code may be topologically distinct on the torus.

### 2.5 Morphing Between Two QR Codes

Two QR codes encoding different messages share the same structural skeleton (finder patterns, timing patterns, format information). The data modules differ. A **continuous morphing** between the two matrices — interpolating module heights or opacities — produces an exploration where the decoded message gradually shifts, the error correction regions absorb the transition, and the structural invariants remain stable throughout.

This modality visualizes the **epistemic gap** (δ₁) between two encodings of related messages: as the morphing proceeds, the structural similarity (S) remains high while the informational content (It) changes — a concrete demonstration of the Map/Territory duality.

### 2.6 SHA-256 Hash Chain Traversal

A QR code encodes a string. That string can be hashed (SHA-256), and the hash re-encoded as a new QR code. Iterating produces a **deterministic sequence of QR matrices** linked by a cryptographic chain.

The exploration becomes a journey through hash space: each step is unpredictable from the previous matrix alone (pre-image resistance), yet the chain is fully verifiable backward. The explorer cannot predict the next room but can always verify they are on the canonical path.

This modality is the most structurally interesting from a TSCG perspective: the Attractor of the chain is the **fixed point** (a hash that encodes itself — a theoretical object that does not exist for SHA-256 but defines the unreachable horizon of the traversal). The Dynamics (D) are cryptographic and irreversible.

### 2.7 Additional Modalities Identified

- **Frequency domain exploration**: apply 2D DCT or FFT to the module matrix and explore the frequency coefficients as a 3D landscape — low frequencies (structural patterns) form smooth hills; high frequencies (data entropy) form jagged peaks.
- **Temporal unfolding**: animate the QR encoding process step by step — data placement, masking, format information — as a construction sequence the explorer can rewind and fast-forward.
- **Multi-layer version stacking**: QR codes exist in 40 versions (21×21 to 177×177). Stack all versions concentrically, each version as a shell — the explorer moves inward from version 40 to version 1, the message becoming progressively coarser.

---

## 3. TSCG Framing

### 3.1 QR Code as Poclet (confirmed)

The QR code itself is ASFID-complete and constitutes a standard `m3:Poclet`:

| Dimension | Expression |
|---|---|
| **A** Attractor | The decoded message — unique equilibrium state of the entire structure |
| **S** Structure | Finder patterns + timing + alignment + format information modules |
| **F** Flow | Zigzag reading path through the data region |
| **It** Information | Reed-Solomon encoding — the jewel: 30% module loss tolerated |
| **D** Dynamics | Error correction and recovery — self-repairing under damage |

This instance (`M0_QRCode.jsonld`) is independent of the exploration concept and should be modeled first.

### 3.2 Exploration Spaces and the Gs Grammar

The exploration modalities are not primarily ASFID phenomena — they are **Gs (Stereopsis grammar) phenomena**, engaging all four TKSL primitives:

| Primitive | Role in exploration |
|---|---|
| **T** Temporality | The traversal unfolds in time; the SHA-256 chain is irreversible |
| **K** Knowledge | The explorer accretes understanding of the encoding structure as they navigate |
| **Ss** Symbol | The QR matrix functions as a navigable sign — symbol become place |
| **L** Localizability | The explorer discriminates position relative to the decoded message (Attractor) |

Crucially, **L (Localizability)** — defined in M3 as "ordinal discrimination of convergence direction toward an Attractor by comparison of successive states" — is the core navigational primitive: at every step, the explorer assesses whether they are moving toward or away from the decoded message. This makes QR exploration spaces the **first M0 candidate with Gs as primary grammar** rather than ASFID.

### 3.3 Instance Type: ExploratorySpace (candidate)

The exploration modalities do not fit cleanly into the four existing M0 types:

| Type | Why it does not fit |
|---|---|
| `m3:Poclet` | Poclets model external systems; exploration is a *construction*, not an observation |
| `m3:SystemicFramework` | Frameworks are methodologies; exploration is an experiential artifact |
| `m3:SymbolicSystemGrammar` | SSGs require multiple cultural interpretations; QR has one valid decoding |
| `m3:TscgTool` | Tools serve the TSCG pipeline; exploration serves the explorer |

**`m3:ExploratorySpace`** is proposed as a new instance type with the following admission criteria:
1. Primary grammar is **Gs** (not ASFID/Gm)
2. The artifact is **navigable** — the user traverses it, not merely observes it
3. A **semantic Attractor** exists — the exploration converges toward a meaning, not just a geometric end
4. At least **3 distinct modalities** are available (not a single fixed rendering)

The QR exploration satisfies all four criteria across the 7+ modalities documented above.

**Admission test (same discipline as M2 purity)**: before creating this type, at least **3 independent instances** should be identified. Candidates: Yi Jing hexagram hypercube, Mandelbrot set as navigable territory, counterpoint score as architectural space.

---

## 4. Technical Approach

**Library**: Three.js (design prototyping convention — BabylonJS reserved for validated TSCG instance simulations)
**Target**: Mobile-first, self-contained HTML (no build step, CDN imports only)
**Controls**: Touch drag (orbit), pinch (zoom), tap (reveal module value / decoded fragment)
**Rendering**: WebGL via Three.js r128; fallback canvas for low-end devices

**Recommended implementation sequence**:
1. Module extrusion (Section 2.1) — simplest, validates the base renderer
2. Sphere projection with Mollweide (Section 2.3) — validates projection pipeline
3. SHA-256 chain (Section 2.6) — validates the generative/traversal mechanic
4. Morphing (Section 2.5) — validates interpolation between instances

---

## 5. Open Questions

1. **ExploratorySpace vs Enigma**: does `m3:Enigma` (currently count=0) already cover navigable symbolic puzzles? Definition needed before creating a new type.
2. **Minimum corpus**: 3 confirmed ExploratorySpace instances required before type is admitted to M3. Current candidates are hypothetical.
3. **Boundary with simulation**: at what point does a TSCG Poclet simulation (step 4 of the instance pipeline) become an ExploratorySpace? The distinction is intentionality: simulation *explains* a system; exploration *inhabits* one.
4. **Gs scoring**: the existing ASFID/REVOI scoring protocol does not cover Gs-primary instances. A Gs scoring dimension (T/K/Ss/L presence and strength) would need to be defined before `M0_QRCodeExploration.jsonld` can be scored.

---

## 6. Next Steps

- [ ] Model `M0_QRCode.jsonld` as a standard Poclet (prerequisite)
- [ ] Define `m3:Enigma` formally and compare with ExploratorySpace semantics
- [ ] Identify 3 ExploratorySpace candidates beyond QR
- [ ] Prototype modality 2.1 (extrusion) in Three.js — mobile-first
- [ ] Propose Gs scoring dimensions for `m0:` level
