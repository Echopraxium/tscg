# M2_KnowledgeField_README.md

**Metaconcepts:** `m2:KnowledgeField` · `m2:KnowledgeFieldMetaCombo`  
**Introduced in:** M2_MetaConcepts.jsonld v15.2.0 · **Date:** 2026-02-17  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** ACTIVE — Replaces `m2:Domain` (deprecated in v15.2.0)

---

## Overview

`KnowledgeField` and `KnowledgeFieldMetaCombo` are two complementary metaconcepts introduced in v15.2.0 that together solve the fundamental problem of **disciplinary specialization** in the TSCG framework: how to model domain-specific concepts (chemical bonds, biological organs, mechanical gears…) without polluting the universal M2 layer with domain-specific entries.

| Metaconcept | Category | Formula | Role |
|-------------|----------|---------|------|
| `m2:KnowledgeField` | Ontological | `∑ᵢ σᵢ \|uᵢ⟩⊗\|vᵢ⟩` | Models complete epistemic fields (Sciences, Arts…) |
| `m2:KnowledgeFieldMetaCombo` | Compositional | `KnowledgeField ⊙ Metaconcept(s)` | Creates domain-specific concept variants at M1 |

---

## Discovery Context

`KnowledgeField` evolved from the earlier `m2:Domain` metaconcept (deprecated v15.2.0). The rename clarifies a crucial architectural distinction: a **knowledge field** is not merely a "domain" — it is a structured epistemic space where Territory phenomena (ASFID) and Map frameworks (REVOI) are **coupled** through the epistemic practices of a discipline.

`KnowledgeFieldMetaCombo` was identified during the systematic analysis of poclets across disciplines (M1_Chemistry, M1_Biology, M1_Optics, M1_Engineering…). In every case, domain-specific concepts followed the same pattern: a universal metaconcept plus a disciplinary qualifier. Without an explicit factorization pattern, this would have required 200+ domain-specific entries in M2 — a direct violation of the M2 universality principle.

---

## m2:KnowledgeField

### Definition

> A structured field of knowledge where Territory phenomena (ASFID) and Map frameworks (REVOI) are coupled through epistemic practices. KnowledgeField is the **first TSCG metaconcept requiring both Eagle Eye and Sphinx Eye simultaneously** — it is intrinsically bicephalous.

### Tensor Formula

```
KnowledgeField = ∑ᵢ σᵢ |uᵢ⟩⊗|vᵢ⟩    (5D SVD, ASFID ⊗ REVOI)
```

Where:
- `|uᵢ⟩ ∈ ℋ_ASFID` — ASFID basis vectors (Territory modes)
- `|vᵢ⟩ ∈ ℋ_REVOI` — REVOI basis vectors (Map modes)
- `σᵢ` — singular values encoding coupling strength between perspectives
- The full tensor product is 25-dimensional (5×5); SVD reduces it to 5 principal modes

**LaTeX:** `\sum_{i=1}^{5} \sigma_i |u_i\rangle \otimes |v_i\rangle \quad (\text{5D SVD}, \; ASFID \otimes REVOI)`

### Key Properties

| Property | Value |
|----------|-------|
| Category | `m2:Ontological` |
| Polarity | `hybrid` |
| Perspective | `hybrid` (ASFID ⊗ REVOI simultaneously) |
| Epistemic Gap | 0.4 |
| Bicephality constraint | `α_T > 0.5` AND `α_M > 0.5` (both perspectives mandatory) |

### The Dual Role: NOUN and ADJECTIVE

`KnowledgeField` has two distinct instantiation modes, both essential to the TSCG architecture:

#### NOUN instances — Complete Epistemic Fields

Represent complete scientific or professional disciplines with their full ASFID⊗REVOI theory. Defined in M1 extensions.

```
Chemistry      →  M1_Chemistry.jsonld
Biology        →  M1_Biology.jsonld
Optics         →  M1_Optics.jsonld
Mechanics      →  M1_Engineering.jsonld
Electronics    →  M1_Electronics.jsonld (proposed)
Photography    →  M1_Photography.jsonld
```

**State vector:** `|KnowledgeField⟩ = α_T |Territory⟩ + α_M |Map⟩ + ∑ᵢ σᵢ|ASFID_i⊗REVOI_i⟩`

#### ADJECTIVE instances — Disciplinary Tags

Lightweight projections derived from NOUN instances, used exclusively within the `KnowledgeFieldMetaCombo` pattern. Defined in M1 extensions as qualifiers.

```
Chemistry   →  Chemical    (tag for KnowledgeFieldMetaCombo)
Biology     →  Biological
Optics      →  Optical
Mechanics   →  Mechanical
Electronics →  Electronic
```

> **Rule:** Always use the ADJECTIVE form in a KnowledgeFieldMetaCombo. `Chemical ⊙ Link`, never `Chemistry ⊙ Link`.

### Mathematical Formulation

#### Full Tensor Product Space

```
Full space:   ℋ_ASFID ⊗ ℋ_REVOI = ℂ²⁵  (25 dimensions)
Reduced (SVD): ℂ⁵  (5 principal modes, ~80% variance captured)
```

#### Coupling Matrix α

The 5×5 matrix α encodes ASFID-REVOI interaction strength. Its sparsity (~80% zero entries — only 5 of 25 non-zero terms) reflects the fact that each discipline couples specific ASFID and REVOI dimensions preferentially.

#### SVD Decomposition

```
KnowledgeField_matrix = U · Σ · V^T

where:
  U = left singular vectors (ASFID basis)
  V = right singular vectors (REVOI basis)
  Σ = diagonal (σ₁ ≥ σ₂ ≥ σ₃ ≥ σ₄ ≥ σ₅ ≥ 0)
```

#### 5D Principal Modes Structure

| Term | Role |
|------|------|
| `σ₁\|u₁⟩⊗\|v₁⟩` | Dominant ASFID dimension (Territory anchor) |
| `σ₂\|u₂⟩⊗\|v₂⟩` | Dominant REVOI dimension (Map anchor) |
| `σ₃\|u₃⟩⊗\|v₃⟩` | Primary ASFID⊗REVOI coupling (epistemic mode 1) |
| `σ₄\|u₄⟩⊗\|v₄⟩` | Secondary coupling (epistemic mode 2) |
| `σ₅\|u₅⟩⊗\|v₅⟩` | Tertiary coupling (epistemic mode 3) |

#### Epistemic Depth Metric

```
Epistemic_Depth(KF) = ||ASFID|| · ||REVOI|| · cos(θ)
```

The alignment angle θ between ASFID and REVOI subspaces characterizes field maturity:

| θ | Interpretation |
|---|---------------|
| θ ≈ 0° | Mature field — Territory well-represented by Map (e.g., Newtonian mechanics) |
| θ ≈ 45° | Developing field — active research, emerging models |
| θ ≈ 90° | Crisis or pseudoscience — Territory-Map disconnect |

### Conceptual Stereopsis Analogy

`KnowledgeField` is to epistemic depth what **binocular vision** is to physical depth:

| Human Binocular Vision | TSCG KnowledgeField |
|------------------------|---------------------|
| Left eye (2D) + Right eye (2D) | ASFID (5D) + REVOI (5D) |
| → 3D depth perception | → Epistemic depth |
| Binocular parallax | Coupling matrix α |
| Visual cortex fusion | KnowledgeField hybridization |
| Distance to objects | Alignment angle θ |

### Domain Maturity Classification

Measured via `σ_mean = (1/5) ∑ᵢ₌₁⁵ σᵢ`:

| Maturity | Threshold | Examples |
|----------|-----------|---------|
| **Mature** | `σ_mean > 0.8` | Classical mechanics (0.90), Chemistry (0.85), Optics (0.80), Nuclear engineering (0.86) |
| **Developing** | `0.6 < σ_mean < 0.8` | Biology (0.75), Materials science (0.65–0.70), Quantum computing (0.60–0.65) |
| **Immature** | `σ_mean < 0.6` | Consciousness studies (0.30–0.40), contested economics (0.45–0.55) |

Temporal indicators:
- `dσ_mean/dt > 0` — field is progressing
- `dσ_mean/dt ≈ 0` — stagnation, possible paradigm shift needed
- `dσ_mean/dt < 0` — crisis

### Field Examples (NOUN instances)

| Field | 5D Decomposition | σ_mean | Epistemic Depth |
|-------|-----------------|--------|----------------|
| **Chemistry** | S (structures) + R (laws) + D⊗E + F⊗I + A⊗V | 0.85 | Very High (θ≈10°) |
| **Biology** | D (evolution) + R (self-org.) + S⊗E + F⊗I + A⊗O | 0.75 | Medium-High (θ≈30°) |
| **Optics** | S (waves/particles) + V (dualism) + I⊗R + F⊗O + A⊗E | 0.80 | High (θ≈20°) |
| **Mechanics** | F (forces) + R (laws) + S⊗A + D⊗I + V⊗O | 0.90 | Very High (θ≈5°) |
| **Electronics** | F (electron flow) + S (circuits) + D⊗I + A⊗R + V⊗O | 0.82 | High (θ≈15°) |

### Relation to Poclets

Poclets are **rank-1 projections** of KnowledgeField NOUN instances — they capture the dominant mode of the parent field:

```
|Poclet⟩ ≈ σ₁|u₁⟩⊗|v₁⟩
```

Examples:
- Fire Triangle (`M0_FireTriangle.jsonld`) → σ₁ mode of Chemistry
- Exposure Triangle (`M0_ExposureTriangle.jsonld`) → σ₁ mode of Photography
- RGB Color Model → σ₁ mode of Optics

### Transdisciplinarity

Two knowledge fields are transdisciplinary if their Hilbert spaces share dimensions:

```
Transdisciplinarity(KF₁, KF₂) = dim(ℋ_KF₁ ∩ ℋ_KF₂) > 0
```

Examples:
- Optics ∩ Photography: High overlap (color, light, aperture)
- Chemistry ∩ Biology: Medium overlap (molecular, energetic concepts)
- Economics ∩ Physics: Low overlap (analogical only)

> M2 metaconcepts live in **ALL** knowledge fields — they are the universal intersection.

### Distinction from Related Metaconcepts

| Concept | Distinction |
|---------|------------|
| `m2:System` | Bounded entity with internal organization; KnowledgeField is epistemic space coupling phenomena and frameworks |
| `m2:Environment` | External context of a system; KnowledgeField is structured knowledge space |
| `m2:Representation` | Single Map; KnowledgeField couples ALL maps with Territory across a field |
| `m2:Observer` | Measuring entity; KnowledgeField is the coupled space Observer operates within |
| `m2:Domain` (deprecated) | Old metaconcept replaced by KnowledgeField — same mathematical foundation, clearer dual-role semantics |

---

## m2:KnowledgeFieldMetaCombo

### Definition

> A factorization metaconcept coupling a KnowledgeField (ADJECTIVE form) with one or more universal Metaconcepts to create domain-specific specializations. Prevents M2 pollution by deferring concrete domain-specific instantiation to M1 extensions. Uses the qualification operator ⊙ rather than the tensor product ⊗.

### Formula

```
KnowledgeFieldMetaCombo = KnowledgeField(adjective) ⊙ Metaconcept(s)
```

**LaTeX:** `\text{KnowledgeField} \odot \bigotimes_{i=1}^{n} M_i`

### Key Properties

| Property | Value |
|----------|-------|
| Category | `m2:Compositional` |
| Polarity | `neutral` |
| Perspective | `dual` |
| Epistemic Gap | 0.3 |
| Instantiation constraint | **M1 extensions ONLY — never directly in M2** |

### The ⊙ Operator: Qualification, Not Fusion

The operator ⊙ is a **Disciplinary Qualification Operator** — fundamentally different from the tensor product ⊗:

```
Formal definition: (KnowledgeField ⊙ Metaconcept)(x) = Metaconcept(x | context = KnowledgeField)
```

| Operator | Type | Dimensionality | Semantics |
|----------|------|----------------|-----------|
| `⊗` (tensor product) | Fusion — emergent | 5D + 5D → 25D (emergent) | Creates NEW properties neither parent possesses alone |
| `⊙` (qualification) | Projection — contextual | 5D → 5D (preserved) | SAME pattern with added disciplinary context |

> **Example:** `Chemical ⊙ Link = Link pattern (S⊗F) operating within chemistry context` — the Link's tensor dimensions are preserved, but the pattern is now scoped to chemical bonds, reaction pathways, molecular networks.

### Instantiation Constraint

KnowledgeFieldMetaCombo can **only** be instantiated in M1 domain extensions — never directly in M2.

```
✅ CORRECT:
  M2_MetaConcepts.jsonld → defines KnowledgeFieldMetaCombo (abstract pattern)
  M1_Chemistry.jsonld    → instantiates ChemicalLink using KnowledgeFieldMetaCombo

❌ VIOLATION:
  M2_MetaConcepts.jsonld → creates ChemicalLink directly (M2 pollution)
```

**Rationale:** The universal layer M2 must remain free of domain-specific content. Every new M1 domain extension instantiates the KnowledgeFieldMetaCombo pattern for its own concepts — M2 stays clean.

### Examples by Domain

| M2 Pattern | M1 Instance | Decomposition | M1 File |
|------------|-------------|---------------|---------|
| KnowledgeFieldMetaCombo | `ChemicalLink` | `Chemical ⊙ Link` | M1_Chemistry.jsonld |
| KnowledgeFieldMetaCombo | `BiologicalProcessor` | `Biological ⊙ Processor` | M1_Biology.jsonld |
| KnowledgeFieldMetaCombo | `MechanicalComponent` | `Mechanical ⊙ Component` | M1_Engineering.jsonld |
| KnowledgeFieldMetaCombo | `ElectronicTrigger` | `Electronic ⊙ Trigger` | M1_Electronics.jsonld |
| KnowledgeFieldMetaCombo | `OpticalTransformation` | `Optical ⊙ Transformation` | M1_Optics.jsonld |
| KnowledgeFieldMetaCombo | `ThermalReservoir` | `Thermal ⊙ Reservoir` | M1_Thermodynamics.jsonld |

**Concrete M0 instances (second instantiation):**

```
ChemicalLink (M1)        → CovalentBond, IonicBond, HydrogenBond (M0)
BiologicalProcessor (M1) → Liver, Mitochondrion, RibosomeComplex (M0)
MechanicalComponent (M1) → Gear, Lever, Bearing, Spring (M0)
ElectronicTrigger (M1)   → Transistor, Relay, SchmittTrigger, JKFlipFlop (M0)
```

### Parsimony Impact

Without this pattern, every domain variant of every metaconcept would need to be defined in M2:

| Scenario | M2 entries | Architecture |
|----------|-----------|-------------|
| **Without** KnowledgeFieldMetaCombo | 10 fields × 20 metaconcepts = **200+ entries** | M2 polluted with domain specifics |
| **With** KnowledgeFieldMetaCombo | 1 pattern + 10 fields + 20 metaconcepts = **31 entries** | Clean separation M2/M1 |

**Parsimony gain: ~6.5×**

### Distinction from MetaconceptCombo

Both are compositional patterns, but they operate differently:

| | MetaconceptCombo | KnowledgeFieldMetaCombo |
|--|-----------------|------------------------|
| **Formula** | `M₁ ⊗ M₂ ⇒ M_emergent` | `KnowledgeField ⊙ Metaconcept` |
| **Operation** | Tensor fusion | Disciplinary qualification |
| **Dimensionality** | 5D + 5D → emergent (richer) | 5D → 5D (preserved) |
| **Result** | New metaconcept with emergent properties | Same metaconcept with domain context |
| **Example** | `FeedbackLoop = Process ⊗ Alignment ⊗ Homeostasis` | `ChemicalLink = Chemical ⊙ Link` |
| **Location** | M2 (universal emergent pattern) | M1 (domain instantiation) |

> MetaconceptCombo creates **new universal patterns**; KnowledgeFieldMetaCombo **specializes existing patterns** to domains. They are complementary, not competing.

---

## Three-Layer Instantiation Cascade

The full instantiation chain from abstract M2 pattern to concrete M0 instance:

```
M2  →  KnowledgeFieldMetaCombo (abstract pattern, definition only)
        ↓  ⊙  Chemical
M1  →  ChemicalLink (domain concept in M1_Chemistry.jsonld)
        ↓  instantiation
M0  →  CovalentBond, IonicBond, ReactionPathway (concrete poclet instances)
```

```
M2  →  KnowledgeFieldMetaCombo (abstract pattern, definition only)
        ↓  ⊙  Biological
M1  →  BiologicalProcessor (domain concept in M1_Biology.jsonld)
        ↓  instantiation
M0  →  Liver, Mitochondrion, RibosomeComplex (concrete poclet instances)
```

---

## M1 Extension Pattern

### Defining a KnowledgeField (NOUN) in M1

```json
{
  "@id": "m1:Chemistry",
  "@type": ["owl:NamedIndividual", "m2:KnowledgeField"],
  "rdfs:label": "Chemistry",
  "m2:knowledgeFieldRole": "NOUN",
  "m2:hasTensorFormula": "∑ᵢ σᵢ |uᵢ⟩⊗|vᵢ⟩",
  "m2:sigma_mean": 0.85,
  "m2:alignmentAngle": "~10°",
  "m2:maturityLevel": "mature",
  "rdfs:comment": "Study of matter, its properties, and transformations"
}
```

### Defining the ADJECTIVE tag in M1

```json
{
  "@id": "m1:Chemical",
  "@type": ["owl:NamedIndividual", "m2:KnowledgeField"],
  "m2:knowledgeFieldRole": "ADJECTIVE",
  "m2:derivedFrom": "m1:Chemistry",
  "rdfs:comment": "Disciplinary tag for use in KnowledgeFieldMetaCombo"
}
```

### Instantiating KnowledgeFieldMetaCombo in M1

```json
{
  "@id": "m1:ChemicalLink",
  "@type": ["owl:NamedIndividual", "m1:Concept"],
  "rdfs:label": "Chemical Link",
  "m1:hasParentMetaconcept": "m2:KnowledgeFieldMetaCombo",
  "m1:knowledgeFieldMetaComboDef": {
    "formula": "Chemical ⊙ Link",
    "knowledgeField": "m1:Chemical",
    "combinedMetaconcept": "m2:Link"
  },
  "rdfs:comment": "Link pattern (S⊗F) specialized to chemical bonds, reaction pathways, molecular networks"
}
```

### Instantiating a concrete M0 concept

```json
{
  "@id": "m0:CovalentBond",
  "@type": ["owl:NamedIndividual", "m1:ChemicalLink"],
  "rdfs:label": "Covalent Bond",
  "rdfs:comment": "Shared electron pair creating stable interatomic link"
}
```

---

## Architectural Impact on TSCG

### Before v15.2.0 (m2:Domain)

```
M2_MetaConcepts.jsonld (v14.x)
├── m2:Domain  (limited — no dual-role, no ADJECTIVE form)
└── No factorization pattern → risk of M2 pollution with domain concepts
```

### After v15.2.0 (KnowledgeField + KnowledgeFieldMetaCombo)

```
M2_MetaConcepts.jsonld (v15.2.0)
├── m2:KnowledgeField  (NOUN/ADJECTIVE dual role, full SVD formalism)
├── m2:KnowledgeFieldMetaCombo  (factorization pattern, ⊙ operator)
└── Clear separation: M2 = universal, M1 = domain-specific

M1_Chemistry.jsonld     → Chemistry (NOUN) + Chemical (ADJECTIVE) + ChemicalLink, ChemicalProcessor...
M1_Biology.jsonld       → Biology (NOUN) + Biological (ADJECTIVE) + BiologicalProcessor...
M1_Optics.jsonld        → Optics (NOUN) + Optical (ADJECTIVE) + OpticalTransformation...
```

---

## Design Principles

**Parsimony:** Define the abstract pattern once in M2; instantiate in any number of M1 domains without touching M2.

**Separation:** M2 contains only universal abstractions; domain specifics belong in M1 extensions.

**Extensibility:** Adding a new discipline (e.g., M1_Acoustics) requires only a new M1 file — M2 remains unchanged.

**Coherence:** All domain-specific concepts follow the same factorization grammar: `ADJECTIVE ⊙ Metaconcept`.

**Validation:** Each M1 instantiation independently validates the universality of the underlying M2 metaconcept.

---

## Related Files

| File | Layer | Relation |
|------|-------|---------|
| `M3_GenesisSpace.jsonld` | M3 | Defines ASFID and REVOI Hilbert spaces |
| `M3_EagleEye.jsonld` | M3 | ASFID dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | REVOI dimension definitions |
| `M2_MetaConcepts.jsonld` | M2 | Contains KnowledgeField and KnowledgeFieldMetaCombo |
| `M1_Chemistry.jsonld` | M1 | Chemistry KnowledgeField + domain concepts |
| `M1_Biology.jsonld` | M1 | Biology KnowledgeField + domain concepts |
| `M1_Optics.jsonld` | M1 | Optics KnowledgeField + domain concepts |
| `M1_Photography.jsonld` | M1 | Photography KnowledgeField + domain concepts |
| `Domain_Hybrid_Tensor_Product_5D_README.md` | docs | SVD formalism derivation |

---

## Changelog

| Version | Change |
|---------|--------|
| **v15.2.0** | `m2:KnowledgeField` and `m2:KnowledgeFieldMetaCombo` introduced. `m2:Domain` deprecated. |
| v14.x | `m2:Domain` (precursor — no dual-role semantics, no ⊙ operator) |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
