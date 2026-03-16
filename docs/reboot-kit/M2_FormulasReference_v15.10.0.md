# M2_FormulasReference

**Version:** 15.10.0  
**Date:** 2026-03-13  
**Author:** Echopraxium with the collaboration of Claude AI  
**Total GenericConcepts:** 76  

> GenericConceptCombos (Cascade, Oscillator, Propagation, Narration, ButterflyEffect, LALI, Processor, StratifiedDissipation, CascadeAmplification) migrated to M1_CoreConcepts.jsonld v2.0.0 — NOT in this file.

## ⚠️ Pending Verification

- FeedbackLoop: composite pattern in Dynamic family — verify canonical formula
- Scope: verify A⊗S⊗I against Regulatory family neighbors

---

## Structural (22 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Capacity` | `S⊗I⊗A⊗E⊗O` | 5 |  |
| `Channel` | `S⊗I⊗F⊗E` | 4 |  |
| `Cluster` | `A⊗I⊗S⊗D⊗O` | 5 |  |
| `Component` | `S⊗I⊗F⊗R` | 4 |  |
| `Composition` | `S⊗I⊗A` | 3 |  |
| `Hierarchy` | `A⊗S⊗V⊗R` | 4 |  |
| `Hub` | `S⊗F⊗E` | 3 |  |
| `Identity` | `S⊗I⊗A⊗V⊗E` | 5 |  |
| `Imbrication` | `S⊗S` | 2 |  |
| `Interoperability` | `S⊗I⊗F⊗V⊗E` | 5 |  |
| `Invariant` | `A⊗S⊗V` | 3 |  |
| `Layer` | `S⊗I⊗A⊗R` | 4 | added v15.10.0 · rdfs:subClassOf m2:Segmentation (S⊗I⊗D⊗R) — D→A substitution: stable positional order |
| `Modularity` | `S⊗I⊗Im` | 3 |  |
| `Network` | `S⊗I⊗F⊗D⊗Im` | 5 |  |
| `Node` | `S⊗I⊗F⊗Im` | 4 |  |
| `Path` | `S⊗I⊗D⊗O` | 4 |  |
| `Polarity` | `A⊗I⊗S⊗R` | 4 |  |
| `Segmentation` | `S⊗I⊗D⊗R` | 4 |  |
| `Step` | `S⊗I⊗D⊗Im` | 4 |  |
| `Symmetry` | `S` | 1 |  |
| `Topology` | `S⊗I⊗A⊗V` | 4 |  |
| `Workflow` | `D⊗F⊗S⊗V` | 4 |  |

## Dynamic (17 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Action` | `D⊗I⊗E` | 3 |  |
| `Activation` | `A⊗D` | 2 |  |
| `Alignment` | `I⊗A⊗S` | 3 | missing_since_added — added v15.9.0 |
| `Amplification` | `Ft⊗D⊗It⊗R⊗O` | 5 |  |
| `Behavior` | `D⊗F⊗S⊗R` | 4 |  |
| `Bifurcation` | `A⊗D⊗S` | 3 |  |
| `Convergence` | `D` | 1 |  |
| `Duplication` | `S⊗I⊗F⊗D⊗V` | 5 | added v15.9.0 |
| `Event` | `D⊗I⊗O` | 3 |  |
| `FeedbackLoop` | `S⊗I⊗A⊗D⊗F⊗V⊗E` | 7 | Composite ⊗⇒(Process, Alignment, Homeostasis); placed in Dynamic family by convention |
| `Fusion` | `S⊗D` | 2 |  |
| `Process` | `D⊗F⊗R` | 3 |  |
| `Synergy` | `D⊗I⊗R` | 3 |  |
| `Trajectory` | `A⊗D⊗F` | 3 |  |
| `Transformation` | `S⊗I⊗D⊗F⊗V` | 5 |  |
| `Trigger` | `D⊗I⊗V` | 3 |  |
| `Tropism` | `A⊗S⊗D⊗F` | 4 |  |

## Ontological (9 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Context` | `O⊗R⊗Im⊗E` | 4 | subClassOf: `m2:Environment` · perspective: *map* · Pure Map concept. rdfs:subClassOf m2:Environment. O=observable field, R=encodability, Im=shared interpretive frame, E=context can evolve. |
| `Environment` | `F⊗I⊗O` | 3 |  |
| `Gradient` | `F` | 1 |  |
| `Observer` | `A⊗I⊗R` | 3 |  |
| `Resource` | `F⊗I⊗R⊗Im` | 4 | Collision resolution vs Signal (F⊗I⊗R): Im=Interoperability — a resource is shareable/interoperable across subsystems |
| `Space` | `S⊗I⊗D⊗E` | 4 |  |
| `State` | `I` | 1 |  |
| `Substrate` | `S⊗F⊗O` | 3 |  |
| `System` | `S⊗F⊗V` | 3 |  |

## Regulatory (8 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Balance` | `A⊗S⊗F⊗O⊗V` | 5 |  |
| `Calibration` | `A⊗I⊗V` | 3 | added v15.10.0 |
| `Constraint` | `S⊗I⊗F⊗V⊗R` | 5 |  |
| `Homeostasis` | `A⊗S⊗F⊗V⊗E` | 5 |  |
| `Regulation` | `A⊗S⊗F⊗V⊗R` | 5 |  |
| `Scope` | `A⊗S⊗I` | 3 |  |
| `Threshold` | `A⊗I⊗O` | 3 |  |
| `Trade-off` | `A⊗I⊗F` | 3 |  |

## Informational (8 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Code` | `S⊗I⊗V` | 3 |  |
| `Coding` | `S⊗I⊗D⊗F⊗R` | 5 |  |
| `Language` | `S⊗I⊗F⊗A⊗R` | 5 |  |
| `Pattern` | `S⊗It⊗A⊗R⊗Im` | 5 |  |
| `Representation` | `S⊗I⊗V⊗R` | 4 |  |
| `Signal` | `F⊗I⊗R⊗O` | 4 | Collision resolution vs Resource (F⊗I⊗R): O=Observability — a signal is detectable/measurable |
| `Signature` | `S⊗I⊗A⊗O` | 4 |  |
| `ValueSpace` | `It⊗V⊗O⊗R⊗Im` | 5 |  |

## Relational (5 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Agent` | `S⊗I⊗D⊗A⊗E` | 5 |  |
| `Link` | `S⊗I⊗F⊗V` | 4 |  |
| `Mediator` | `S⊗I⊗F⊗O` | 4 |  |
| `Relation` | `S⊗I⊗A⊗Im` | 4 |  |
| `Role` | `S⊗I⊗F⊗O⊗R` | 5 |  |

## Adaptive (4 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Adaptation` | `I⊗F⊗D` | 3 |  |
| `Emergence` | `S⊗I⊗D⊗V` | 4 |  |
| `Memory` | `D⊗F⊗D` | 3 |  |
| `Resilience` | `A⊗S⊗E` | 3 |  |

## Energetic (2 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Dissipation` | `D⊗F⊗V` | 3 |  |
| `Storage` | `S⊗F⊗R` | 3 |  |

## Teleonomic (1 concepts)

| Concept | Formula | Dims | Notes |
|---------|---------|-----:|-------|
| `Self-Organization` | `A⊗I⊗D` | 3 |  |

---

## Collision Policy

Formulas unique via REVOI disambiguation. If ASFID formula collides, add minimal REVOI dimension(s) to create bijection.

## Related Files

| File | Role |
|------|------|
| `M2_GenericConcepts.jsonld` | Source ontology |
| `M2_GenericConcepts_README.md` | Full documentation with family breakdown |
| `M1_CoreConcepts.jsonld` | TransdisciplinaryCombos (migrated from M2 Combo family) |