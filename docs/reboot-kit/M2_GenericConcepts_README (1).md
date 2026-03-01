# M2_GenericConcepts_README.md

**File:** `M2_GenericConcepts.jsonld`  
**Version:** 15.9.0 · **Date:** 2026-02-28  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** ACTIVE — 81 GenericConcepts across 10 families

---

## Overview

`M2_GenericConcepts.jsonld` is the **universal operational layer** of the TSCG framework. It defines the **GenericConcepts** (also called *metaconcepts*) — the abstract, transdisciplinary operational patterns that recur across all knowledge domains. These are the "verbs and nouns of complex systems" expressed as tensor products over the M3 Genesis Space dimensions.

Every M2 GenericConcept:
- Is **domain-agnostic** — valid in biology, physics, economics, mythology, computing, etc.
- Is **formalized** as a tensor product of M3 dimensions (ASFID and/or REVOI)
- Is **validated transdisciplinarily** across ≥ 3 domains (preferably 5–6)
- Serves as a **building block** for M1 domain concepts and M0 poclets

### Architectural Position

```
M3  Genesis Space  (ASFID ⊗ REVOI — 10 fundamental dimensions)
 ↓
M2  GenericConcepts  ← THIS FILE
 ↓
M1  Domain Extensions  (M1_Biology, M1_Chemistry, M1_Economics…)
 ↓
M0  Poclets  (minimal complete system instances)
```

---

## Dimensional Vocabulary

### ASFID — Territory (Eagle Eye)

| Dim | Name | Role |
|-----|------|------|
| **A** | Attractor | Stable states, goals, equilibria, thresholds |
| **S** | Structure | Topology, architecture, organization |
| **F** | Flow | Flux, transfer, exchange |
| **I** | Information | Content, signal, state |
| **D** | Dynamics | Temporal evolution, change rate |

### REVOI — Map (Sphinx Eye)

| Dim | Name | Role |
|-----|------|------|
| **R** | Representability | Semantic encodability/decodability |
| **E** | Evolvability | Adaptability of the model |
| **V** | Verifiability | Testability, fidelity, coherence |
| **O** | Observability | Measurability of internal states |
| **Im** | Interoperability | Compatibility between subsystems |

> ⚠️ **R = Representability** (semantic decodability). Never Reproducibility.

---

## Statistics (v15.9.0)

| Metric | Value |
|--------|-------|
| Total GenericConcepts | **81** |
| Atomic concepts | 73 |
| GenericConceptCombos | 7 (+ 1 abstract parent) |
| Families | 10 |
| ConceptContracts | 4 (Triggerable, Observable, Composable, Stateful) |
| Transdisciplinary validation domains covered | 15+ |

---

## Family Breakdown

### Structural (20 concepts)
*Topology, architecture, organization. High S.*

`Channel` · `Cluster` · `Capacity` · `Component` · `Composition` · `Hub` · `Hierarchy` · `Identity` · `Imbrication` · `Interoperability` · `Invariant` · `Modularity` · `Network` · `Node` · `Path` · `Polarity` · `Segmentation` · `Step` · `Symmetry` · `Topology` · `Workflow`

### Dynamic (15 concepts)
*Processes, transformations, temporal evolution. High D.*

`Action` · `Activation` · `Alignment` · `Amplification` · `Behavior` · `Bifurcation` · `Convergence` · `Duplication` *(new v15.9.0)* · `Event` · `FeedbackLoop` · `Fusion` · `Process` · `Synergy` · `Transformation` · `Trajectory` · `Tropism`

### Informational (8 concepts)
*Data, representation, communication. High I.*

`Code` · `Coding` · `Language` · `Pattern` · `Representation` · `Signal` · `Signature` · `ValueSpace`

### Ontological (9 concepts)
*Fundamental system entities and boundaries. S→F patterns.*

`Environment` · `Gradient` · `Imbrication` · `Observer` · `Resource` · `Space` · `State` · `Substrate` · `System`

### Regulatory (9 concepts)
*Control, stabilization, constraint. High A.*

`Activation` · `Balance` · `Constraint` · `Homeostasis` · `Regulation` · `Scope` · `Threshold` · `Trade-off` · `Trigger`

### Relational (5 concepts)
*Interactions between entities and roles.*

`Agent` · `Link` · `Mediator` · `Relation` · `Role`

### Adaptive (4 concepts)
*Learning, evolution, environmental response. High I, medium F.*

`Adaptation` · `Emergence` · `Memory` · `Resilience`

### Energetic (2 concepts)
*Energy, matter, information flows. High F, high D.*

`Dissipation` · `Storage`

### Teleonomic (1 concept)
*Goal-directedness, purpose. High A.*

`Self-Organization`

### Combo (8 concepts)
*GenericConceptCombos — emergent patterns from N-ary tensor assembly.*

`GenericConceptCombo` *(abstract)* · `ButterflyEffect` · `Cascade` · `LocalActivationLateralInhibition` · `Narration` *(new v15.9.0)* · `Oscillator` · `Processor` · `Propagation` *(new v15.9.0)*

---

## GenericConceptCombos

GenericConceptCombos (⊗⇒) are GenericConcepts produced by the **synergistic N-ary tensor assembly** of existing parent concepts. The resulting concept has semantic identity irreducible to any subset of its parents. Shared dimensions are contracted via lattice join (F⊔F=F).

### Formula

```
⊗ⁿ⇒(M₁, M₂, …, Mₙ) = lattice_join(dims(M₁) ∪ dims(M₂) ∪ … ∪ dims(Mₙ))
```

### Catalog (v15.9.0)

| Concept | Parents | Expanded Formula | Dim | Unique contributions |
|---------|---------|-----------------|-----|---------------------|
| **Cascade** | Process, Step, Trajectory | S⊗I⊗A⊗D⊗F | 5 | Full ASFID — first 5D Combo |
| **LocalActivationLateralInhibition** | Amplification, Regulation | — | — | Short-range activation + long-range inhibition |
| **ButterflyEffect** | Amplification, Trajectory | — | — | Chaotic trajectory (λ>0) |
| **Oscillator** | Component, Process, Trajectory | S⊗A⊗I⊗D⊗F | 5 | subClassOf Component → S unlocked |
| **Propagation** *(new)* | Cascade, Duplication, Network | S⊗I⊗A⊗D⊗F⊗V⊗Im | **7** | A (threshold/saturation) · V (fidelity) · Im (node compatibility) |
| **Narration** *(new)* | Transformation, Representation, Relation | S⊗I⊗D⊗F⊗V⊗R⊗A⊗Im | **8** | D+F (temporal unfolding) · R (encodability) · A+Im (telos + shared understanding) |

### Dimensional Coverage by Combo

```
Cascade         [S · I · A · D · F]                        = 5D  (full ASFID)
Oscillator      [S · A · I · D · F]                        = 5D  (full ASFID, structural)
Propagation     [S · I · A · D · F · V · Im]               = 7D  (ASFID + REVOI V,Im)
Narration       [S · I · D · F · V · R · A · Im]           = 8D  (ASFID + REVOI V,R,Im)
```

Narration is the **richest GenericConceptCombo** (8D), fully spanning ASFID Territory (S,I,D,F,A) and key REVOI Map dimensions (V,R,Im).

---

## New Concepts in v15.9.0

### `m2:Duplication`

> Active process producing one or more faithful copies of a source structure, preserving its informational content through a transfer flux over time.

| Property | Value |
|----------|-------|
| Family | Dynamic |
| Formula | `S ⊗ I ⊗ F ⊗ D ⊗ V` |
| rdfs:subClassOf | `m2:Process` · `m2:Triggerable` · `m2:Observable` |
| Epistemic gap | 0.22 |
| Perspective | dual |

**Specialization of `m2:Process` (D⊗F):**

| Dimension | Origin | Role |
|-----------|--------|------|
| D | *inherited* from Process | Temporal dynamics of the copying process |
| F | *inherited* from Process | Transfer flux producing the copy |
| S | *added* | Source structure being copied |
| I | *added* | Informational content preserved faithfully |
| V | *added* (replaces R) | Fidelity verifiability — copy ≡ original |

**Fidelity spectrum (V axis):**

```
V → 1  Perfect copy     DNA replication (10⁻⁹ error rate), SHA-256 file copy
V ≈ 0.5  Imperfect copy  RNA virus replication, cultural transmission with drift
V → 0  Degenerate       → m2:Bifurcation (copies diverge to distinct attractors)
```

**Transdisciplinary validation (6 domains):** Molecular Biology · Computing · Epidemiology · Physics · Social Sciences · Developmental Biology

**Relation to Bifurcation:** `m2:Bifurcation rdfs:subClassOf m2:Duplication` — semantic specialization where V→0. Not dimensional inheritance (Bifurcation = ∂D/∂F, Dynamic family).

---

### `m2:Propagation`

> Branching spread of a faithfully copied entity through a network, where each receiving node becomes a new emitter.

| Property | Value |
|----------|-------|
| Family | Combo |
| Formula | `⊗⇒(Cascade, Duplication, Network)` |
| Expanded | `S ⊗ I ⊗ A ⊗ D ⊗ F ⊗ V ⊗ Im` |
| Dimensions | 7 |
| Perspective | dual |

**Lattice join decomposition:**

```
Cascade     = {S, I, A, D, F}   → unique: A
Duplication = {S, I, F, D, V}   → unique: V
Network     = {S, I, F, D, Im}  → unique: Im
Contracted  = {S, I, F, D}

Propagation = {S, I, A, D, F, V, Im}  →  7 dimensions
```

**Unique dimensional contributions:**

| Dimension | From | Semantic role |
|-----------|------|--------------|
| **A** | Cascade | Propagation threshold (R₀=1) and saturation attractor (herd immunity) |
| **V** | Duplication | Copy fidelity — discriminant vs Diffusion (V≈0) |
| **Im** | Network | Node compatibility: receiver can become emitter |

**Propagation regimes (A-attractor):**

| Regime | Condition | Example |
|--------|-----------|---------|
| SubThreshold | R₀ < 1 | Epidemic dying out, contained panic |
| Critical | R₀ = 1 | Endemic disease |
| Supercritical | R₀ > 1 | Epidemic outbreak, Minsky Boom, viral meme |
| Saturated | Network full | Herd immunity, bubble peak |

**Key distinction — Propagation vs Diffusion:** V is the discriminant. Diffusion (V≈0) is random spread without fidelity. Propagation (V>0) preserves copy identity at each node.

**Transdisciplinary validation (6 domains):** Epidemiology · Finance (Kindleberger-Minsky) · Computing/Cybersecurity · Physics · Social Sciences · Neuroscience

**Planned M1 instances:**
- `m1:Contagion` (M1_CoreConcepts / M1_Biology) — biological/social propagation
- `m1:FinancialContagion` (M1_Economics) — Kindleberger-Minsky bank-to-bank panic
- `m1:WavePropagation` (M1_Physics) — electromagnetic/acoustic wave spread

---

### `m2:Narration`

> Temporal transformation of a semantic network of Representations and their Relations — a semantic network morphism unfolding over time.

| Property | Value |
|----------|-------|
| Family | Combo |
| Formula | `⊗⇒(Transformation, Representation, Relation)` |
| Expanded | `S ⊗ I ⊗ D ⊗ F ⊗ V ⊗ R ⊗ A ⊗ Im` |
| Dimensions | **8** (richest Combo to date) |
| Epistemic gap | 0.35 |
| Perspective | dual |

**Lattice join decomposition:**

```
Transformation = {S, I, D, F, V}   → unique: D, F
Representation = {S, I, V, R}      → unique: R
Relation       = {S, I, A, Im}     → unique: A, Im
Contracted     = {S, I, V}

Narration = {S, I, D, F, V, R, A, Im}  →  8 dimensions
```

**Unique dimensional contributions:**

| Dimension | From | Semantic role |
|-----------|------|--------------|
| **D** | Transformation | Temporal unfolding — beginning, development, end |
| **F** | Transformation | Narrative flux — causality, consequence, continuity between nodes |
| **R** | Representation | Semantic encodability/decodability of nodes |
| **A** | Relation | Narrative telos — resolution, moral, conclusion, collapse |
| **Im** | Relation | Interoperability — shared understanding between emitter and receiver |

**Morphism nature:** Narration is formally a **semantic network morphism** — a structure-preserving map between semantic states. V ensures coherence (meaning preserved or coherently evolved); Im ensures shareability (emitter and receiver on the same semantic substrate).

**Narrative topology (ValueSpace):** Linear · Branching · Circular · Nested · Network (rhizomatic)

**Attractor types (ValueSpace):** Resolution · Transformation · OpenEnded · Collapse

**Naming rationale:** *Narration* (process noun) over *Narrative* (artifact noun) — consistent with M2 process vocabulary (Transformation, Regulation, Adaptation…). The active process of narrating is the M2 pattern; the resulting artifact is an M0/M1 instantiation.

**Transdisciplinary validation (6 domains):** Mythology/Anthropology · Literature/Narratology · Science/Epistemology · Finance/Economics (Kindleberger-Minsky bubble as collective belief narration) · Law · Neuroscience/Cognitive Science

**Key distinction — Narration vs Propagation:**

| | Narration | Propagation |
|--|-----------|-------------|
| Content | **Transforms** — evolves toward telos | **Copies** — preserved faithfully |
| V | Coherence of transformation | Fidelity of copy |
| Kindleberger-Minsky | Collective belief: "new paradigm" → Collapse | Panic: bank run spreads through interbank network |

---

## ConceptContracts

ConceptContracts are behavioral mixins orthogonal to families — they cut across multiple families to group concepts by shared capability. Applied via `rdfs:subClassOf` (mixin pattern).

| Contract | Semantics | Implementors (selected) |
|----------|-----------|------------------------|
| `m2:Triggerable` | Can be initiated by an external condition | Event, Process, Cascade, Transformation, Action, Duplication, Propagation, Narration |
| `m2:Observable` | Internal states can be measured/tracked | State, Trajectory, Behavior, Gradient, Observer, Duplication, Propagation, Narration |
| `m2:Composable` | Can be assembled into larger structures | Component, Node, Step |
| `m2:Stateful` | Maintains persistent internal state over time | Memory, Storage, Homeostasis, State |

---

## Bicephalous Strategy

GenericConcepts use one of three perspective modes:

| Mode | Eagle (ASFID) | Sphinx (REVOI) | Count |
|------|--------------|----------------|-------|
| `territory` | Primary, IMMUTABLE | — | 29 |
| `map` | Fallback only | Primary | 10 |
| `dual` | Primary, IMMUTABLE | PROPOSITION | 26 + 3 new |
| `hybrid` | ASFID + REVOI in single formula | — | 4 |

> REVOI formulas are marked `PROPOSITION (validation in progress)` — empirically validated through poclet analysis (7 poclets at v15.8.0).

---

## Key Architectural Relationships

```
m2:Process (D⊗F)
  └── m2:Duplication (S⊗I⊗F⊗D⊗V)    [specialization: adds S,I,V]
        └── m2:Bifurcation (∂D/∂F)    [semantic: V→0 degenerate case]

m2:GenericConceptCombo (abstract)
  ├── m2:Cascade      ⊗⇒(Process, Step, Trajectory)           [5D]
  ├── m2:Oscillator   ⊗⇒(Component, Process, Trajectory)      [5D]
  ├── m2:Propagation  ⊗⇒(Cascade, Duplication, Network)       [7D]
  └── m2:Narration    ⊗⇒(Transformation, Representation, Relation) [8D]

m2:Homeostasis → semantic morphism_inclusion → m2:Regulation
m2:Bifurcation → semantic fidelity_degeneration → m2:Duplication
```

---

## Tensor Formula Notation

### Atomic GenericConcept
```
Concept = D₁ ⊗ D₂ ⊗ … ⊗ Dₙ
```
where each Dᵢ ∈ {A, S, F, I, D, R, E, V, O, Im}

### GenericConceptCombo
```
⊗⇒(M₁, M₂, …, Mₙ) = lattice_join(dims(M₁) ∪ dims(M₂) ∪ … ∪ dims(Mₙ))
```

Shared dimensions are contracted: F⊔F=F, S⊔S=S, etc.
Unique dimensions from each parent are the **emergent contributions**.

### Specialization (subClassOf)
```
Child ⊃ Parent    Child inherits {Parent dims} and adds {extra dims}
```
Example: `Duplication (S⊗I⊗F⊗D⊗V) ⊃ Process (D⊗F)` — inherits D,F; adds S,I,V

---

## M1/M0 Usage Patterns

### M1 — Domain specialization via `m2:characterizedBy`
```json
{
  "@id": "m1:Contagion",
  "m2:characterizedBy": "m2:Propagation",
  "rdfs:comment": "Biological/social Propagation with host specificity and epidemiological fidelity"
}
```

### M0 — Poclet referencing M2 concepts
```json
{
  "@id": "m0:KindlebergerMinskyCycle",
  "m2:characterizedBy": ["m2:Propagation", "m2:Narration", "m2:Bifurcation"]
}
```

### M1 Domain extension files

| Domain | File | M2 usage (selected) |
|--------|------|---------------------|
| Biology | M1_Biology.jsonld | Cascade, Regulation, Homeostasis, Propagation |
| Chemistry | M1_Chemistry.jsonld | Transformation, Cascade, Network, Link |
| Optics | M1_Optics.jsonld | Signal, Transformation, Pattern |
| Photography | M1_Photography.jsonld | Composition, Balance, Threshold |
| Mythology | M1_Mythology.jsonld | Narration, Pattern, Identity, Relation |
| Economics *(planned)* | M1_Economics.jsonld | Propagation, Narration, Bifurcation, Oscillator |

---

## Versioning

| Version | Date | Key additions |
|---------|------|--------------|
| **v15.9.0** | 2026-02-28 | `Duplication` (Dynamic) · `Propagation` (Combo, 7D) · `Narration` (Combo, 8D) · Bifurcation updated (subClassOf Duplication) |
| v15.8.0 | 2026-02-27 | `Oscillator` (Combo, 5D, subClassOf Component) |
| v15.7.0 | 2026-02-24 | ConceptContract system (Triggerable, Observable, Composable, Stateful) |
| v15.5.x | 2026-02 | Cascade, Processor, LALI, ButterflyEffect (Combo family) |
| v15.2.0 | 2026-02-17 | KnowledgeField, KnowledgeFieldMetaCombo |
| v14.x | — | Domain (deprecated), base 60 concepts |

---

## Related Files

| File | Layer | Relation |
|------|-------|---------|
| `M3_GenesisSpace.jsonld` | M3 | Defines the 10 ASFID⊗REVOI dimensions |
| `M3_EagleEye.jsonld` | M3 | ASFID Eagle Eye dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | REVOI Sphinx Eye dimension definitions |
| `M2_FormulasReference.json` | M2 | Compact tensor formula lookup table (update needed: +3 new concepts) |
| `M1_CoreConcepts.jsonld` | M1 | Core transdisciplinary concepts using M2 patterns |
| `M1_Biology.jsonld` | M1 | Biology domain extension |
| `M1_Chemistry.jsonld` | M1 | Chemistry domain extension |
| `M1_Mythology.jsonld` | M1 | Mythology extension — uses m2:Narration, m2:Pattern |
| `M0_RAAS.jsonld` | M0 | RAAS poclet — validated m2:Cascade, m2:Homeostasis |
| `MetaconceptPair_README.md` | docs | Semantic morphism_inclusion patterns |
| `TSCG_Smart_Prompt_v15_8_0.md` | docs | Current smart prompt for TSCG sessions |

> ⚠️ **`M2_FormulasReference.json` is not yet updated** with Duplication, Propagation, Narration. Update required.

---

## Design Principles

**Transdisciplinarity:** Every GenericConcept must be validated across ≥ 3 domains (preferably 6). A concept valid in only one domain belongs in M1, not M2.

**Purity:** M2 vocabulary is universal and domain-agnostic. No domain-specific nouns (Contagion → Propagation; Narrative → Narration).

**Non-proliferation:** Before creating a new GenericConcept, verify it cannot be expressed as a GenericConceptCombo of existing concepts. The fidelity spectrum on Duplication (V axis) is an example of parameterizing a continuous family rather than creating multiple discrete concepts.

**Bicephalous consistency:** Every GenericConcept has at minimum an Eagle Eye (ASFID) formula marked IMMUTABLE. Sphinx Eye (REVOI) formulas are PROPOSITION until validated through poclets.

**Process vocabulary:** M2 names are process nouns (Narration, Transformation, Regulation) not artifact nouns (Narrative, Transform, Rule). The active pattern, not the resulting object.

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
