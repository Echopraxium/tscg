# TSCG Smart Prompt v15.9.0 - Duplication, Propagation, Narration & Authoring Conventions

**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Version**: 15.9.0  
**Date**: 2026-03-01  
**Author**: Echopraxium with the collaboration of Claude AI  
**Major Updates v15.7.0→v15.9.0**:
- ✅ **v15.8.0** : m2:Oscillator (Combo, full ASFID 5D: S⊗A⊗I⊗D⊗F)
- ✅ **v15.9.0** : m2:Duplication (Dynamic), m2:Propagation (Combo), m2:Narration (Combo — richest 8D)
- ✅ **Authoring conventions** : URI root, @base, changelog discipline, IRI patterns for M0/M1 files

---

## 🎯 Context: What is TSCG?

TSCG (Transdisciplinary System Construction Game) is an **ontological framework** for analyzing and modeling complex systems across disciplines. It provides a rigorous mathematical foundation for understanding systemic patterns through a **bicephalous architecture** that combines Territory measurement (Eagle Eye/ASFID) with Map construction (Sphinx Eye/REVOI).

### Core Principle (Korzybski Extended)
**"The map is not the territory, but the map influences how we observe the territory"**
- Classic (Korzybski, 1933): Map ≠ Territory
- TSCG Extension: **Bidirectional feedback loop** formalized through Σ coupling matrix

---

## 📐 Authoring & File Conventions

These rules apply to **all generated ontology files** (.jsonld). The conversation with Claude may be in French, but all generated files must be in **English**.

### 1. Author field
All `.jsonld` files must carry the following author declaration:
```json
"dcterms:creator": "Echopraxium with the collaboration of Claude AI"
```

### 2. URI root
The canonical base URI for the TSCG repository is:
```
https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology
```

### 3. @base — Short IRIs for M0 and M1 files
All `M0_xxx.jsonld`, `M1_CoreConcepts.jsonld`, and `M1_xxx.jsonld` extension files must use `@base` in their `@context` (same principle as `M3_GenesisSpace.jsonld` and `M2_GenericConcepts.jsonld`):
```json
"@context": {
  "@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/",
  ...
}
```

### 4. M1 extension IRI pattern
When referencing M1 domain extensions in `M0_xxx.jsonld` files, use the following IRI style:
```
M1_extensions/extension_name/M1_ExtensionName.jsonld
```
**Examples**:
- `M1_extensions/biology/M1_Biology.jsonld`
- `M1_extensions/chemistry/M1_Chemistry.jsonld`
- `M1_extensions/optics/M1_Optics.jsonld`
- `M1_extensions/photography/M1_Photography.jsonld`
- `M1_extensions/mythology/M1_Mythology.jsonld`

### 5. Changelog discipline
In the `m2:changelog` field of any ontology file, **keep only the 3 most recent entries**. Remove older entries during each update.

---

## 🗂️ Framework Architecture (4 Layers)

```
M3_GenesisSpace.jsonld      ← Mathematical foundation (ASFID ⊕ REVOI, 10D Hilbert space)
        ↓ imports
M2_GenericConcepts.jsonld   ← Universal transdisciplinary patterns (81 GenericConcepts)
        ↓ characterizedBy
M1_CoreConcepts.jsonld      ← KnowledgeField, KnowledgeFieldConcept, KnowledgeFieldGenericCombo
M1_extensions/biology/M1_Biology.jsonld
M1_extensions/chemistry/M1_Chemistry.jsonld  …
        ↓ instantiates
M0_RAAS.jsonld, M0_Yggdrasil.jsonld, …  ← Concrete systems (Poclets)
```

---

## M3 - Genesis Space (Foundational Basis)

**Complete 10D orthonormal Hilbert space** for all TSCG analysis.

### Eagle Eye (ASFID) — Territory Measurement (5D)
| Symbol | Name | Role |
|--------|------|------|
| **A** | Attractor | Stable states, equilibria, set points |
| **S** | Structure | Organization, topology, spatial arrangement |
| **F** | Flow | Movement, circulation, transfers |
| **I** | Information | Data, signals, codes (I_t in hybrid formulas) |
| **D** | Dynamics | Change, temporal evolution |

### Sphinx Eye (REVOI) — Map Construction (5D)
| Symbol | Name | Role |
|--------|------|------|
| **R** | Representability | Can it be symbolized/encoded? |
| **E** | Evolvability | Can it adapt/extend? |
| **V** | Verifiability | Can it be tested? |
| **O** | Observability | Can it be measured? |
| **I** | Interoperability | Can it integrate? (I_m in hybrid formulas) |

**⚠️ CRITICAL**: R = **Representability** (semantic decodability/encodability). NEVER Reproducibility.  
**I disambiguation**: Use I_t (Territory/ASFID) and I_m (Map/REVOI) in hybrid formulas.

### Mathematical Properties
- **Hilbert space**: 10D = H_ASFID(5D) ⊕ H_REVOI(5D)
- **Orthogonality**: ⟨ASFID, REVOI⟩ = 0 (validated)
- **Completeness**: ∀s ∈ System: s = α·ASFID + β·REVOI for unique α,β

### Feedback Loop (Territory ↔ Map)

```
Territory (ASFID) ──Φ (observation)──> Map (REVOI)
                  <──Ψ (interpretation)──
```

**Coupling Matrix Σ** (5×5): σᵢⱼ = coupling strength between ASFID-i and REVOI-j  
- High σ ≈ 0.8–0.9: Mature domain (physics, engineering)  
- Low σ ≈ 0.2–0.4: Immature domain (early social sciences)

**Operators**:
- **Φ: H_ASFID → H_REVOI** — Observation (Territory data → Map representation)
- **Ψ: H_REVOI → H_ASFID** — Interpretation (Map predictions → Territory measurements)

**Iteration**: `v_T^(n+1) = v_T^(n) + α·Ψ(Φ(v_T^(n)))`  converges to epistemic equilibrium.

---

## M2 - GenericConcepts Layer ⭐ **v15.9.0**

**81 transdisciplinary GenericConcepts** — universally valid patterns derived from M3 tensor products.  
M2 is **strictly pure**: no KnowledgeField references. KnowledgeField, KnowledgeFieldConcept and KnowledgeFieldGenericCombo are defined in M1_CoreConcepts.

### ⊗ Semantics in TSCG
**⊗ is a lattice join (⊔), NOT a Kronecker product.**  
Shared dimensions between GenericConceptCombo parents are deduplicated: F ⊔ F = F.  
`dim(Combo) = |⋃ᵢ dims(Mᵢ)|`  

Exception: `⊗₂F` (in Gradient) means F measured at two *distinct* points — this is a genuine 2nd-order product (differential), not a duplication.

### OWL Architecture
```
owl:Thing
  └── m2:ConceptContract   (behavioral interface, no tensor formula)
        ├── m2:Triggerable
        ├── m2:Observable
        ├── m2:Composable
        └── m2:Stateful
  └── m2:GenericConceptFamily  (10 families)
  └── m2:GenericConcept        (81 concepts, rdfs:subClassOf)
        └── m2:GenericConceptCombo  (synergistic N-ary combinations)
```

### GenericConcept Families (10) — Total: 81

| Family | Count | Primary dimensions |
|--------|------:|--------------------|
| **Structural** | 12 | S, I |
| **Dynamic** | 15 | D, F |
| **Ontological** | 8 | S, F, I |
| **Regulatory** | 7 | A, S, F |
| **Informational** | 6 | I, S |
| **Combo** | 8 | — (synergistic ⊗ⁿ⇒) |
| **Relational** | 5 | S, I, F |
| **Adaptive** | 4 | A, I, D |
| **Energetic** | 2 | F, D |
| **Teleonomic** | 1 | A, I, D |

**Removed from M2** (moved to M1): Domain, KnowledgeField, KnowledgeFieldGenericCombo.

### GenericConcept Reference by Family

**Adaptive (4)**: Resilience `A⊗S`, Adaptation `I⊗F⊗D`, Emergence `I⊗S⊗D`, Memory `∫(D−F)dτ`

**Combo (8)**: GenericConceptCombo `⊗ⁿ⇒Mᵢ`, Cascade `⊗⇒(Process,Step,Trajectory)`,  
Processor `S⊗I⊗D⊗F⊗V⊗R`, LocalActivationLateralInhibition `⊗⇒(Amplification,Regulation)|F_A<<F_R`,  
ButterflyEffect `⊗⇒(Amplification,Trajectory)|λ>0`,  
Oscillator `⊗⇒(Component,Process,Trajectory)|Circular` → `S⊗A⊗I⊗D⊗F`,  
Propagation `⊗⇒(Cascade,Duplication,Network)` → `S⊗I⊗A⊗D⊗F⊗V⊗Im` (7D) *(new v15.9.0)*,  
Narration `⊗⇒(Transformation,Representation,Relation)` → `S⊗I⊗D⊗F⊗V⊗R⊗A⊗Im` (8D) *(new v15.9.0)*

**Dynamic (15)**: Bifurcation `∂D/∂F` *(rdfs:subClassOf Duplication)*, Transformation `D⊗S⊗I`, Process `D⊗F`, Trajectory `A⊗D⊗F`,  
Event `D⊗I`, Synergy `I⊗D`, Fusion `S⊗D`, Convergence `-∇·D/∇·D`, Behavior `S⊗D⊗F`,  
Tropism `A⊗S⊗D⊗F`, Action `D⊗I`, Amplification `Ft→D→It→R→O`,  
Alignment `I⊗A⊗S`, FeedbackLoop `⊗⇒(Process,Alignment,Homeostasis)`,  
Duplication `S⊗I⊗F⊗D⊗V` *(new v15.9.0)*

**Energetic (2)**: Dissipation `F⊗D`, Storage `S⊗F`

**Informational (6)**: Code `I⊗S`, Coding `I⊗S⊗D`, Language `I⊗S⊗F`,  
Pattern `S→I→A`, Signal `I⊗F`, ValueSpace `It→V→O→R→Im`

**Ontological (8)**: Resource `F⊗I⊗R`, System `S⊗F`, Environment `F⊗I`,  
Observer `I⊗A`, State `I`, Substrate `S⊗F`, Gradient `⊗₂F or ⊗₂I`, Space `S⊗I`, Imbrication `S→S`

> ⚠️ Note: Representation `I⊗S` and Signature `I⊗S` (Informational) and Interoperability (Structural) — verify current counts if editing.

**Regulatory (7)**: Homeostasis `A⊗S⊗F`, Regulation `A⊗S⊗F`, Constraint `S⊗I`,  
Threshold `A⊗I`, Trigger `D⊗I`, Activation `A⊗D`, Balance `A⊗S⊗F`

**Relational (5)**: Agent `S⊗I⊗D`, Role `S⊗I`, Mediator `F⊗I⊗S`, Link `S⊗I⊗F`, Relation `S⊗I`

**Structural (12)**: Interoperability `S⊗I⊗F⊗V⊗E`, Hierarchy `S⊗A`, Network `S⊗I⊗F`,  
Symmetry `S`, Modularity `S⊗I`, Topology `S⊗I`, Segmentation `S⊗I⊗D`, Invariant `S⊗A`,  
Capacity `S⊗I`, Node `S⊗I`, Path `S⊗I⊗D`, Channel `S⊗I⊗F`

**Teleonomic (1)**: Purpose `A⊗I⊗D`

---

## M1 - KnowledgeField Layer

**KnowledgeField extensions** add domain-specific concepts via `m2:characterizedBy` links to M2 GenericConcepts.

### Core Concepts (M1_CoreConcepts.jsonld)
Defines the three root classes used by all M1 extensions:
- `m1:KnowledgeField` — disciplinary domain
- `m1:KnowledgeFieldConcept` — domain-specific concept characterized by ≥1 M2 GenericConcept
- `m1:KnowledgeFieldGenericCombo` — parameterizable reusable pattern within a KnowledgeField

### M1 IS-A vs characterizedBy Rule
- `rdfs:subClassOf m2:GenericConcept` — correct for M1 root concepts (KnowledgeFieldConcept, …)
- `m2:characterizedBy` — replaces incorrect IS-A (ChemicalReaction is characterized-by Process, not IS-A Process)

### Available M1 Extensions
| File | Domain | IRI path |
|------|--------|----------|
| `M1_CoreConcepts.jsonld` | Core | `M1_CoreConcepts.jsonld` |
| `M1_Biology.jsonld` | Biology | `M1_extensions/biology/M1_Biology.jsonld` |
| `M1_Chemistry.jsonld` | Chemistry | `M1_extensions/chemistry/M1_Chemistry.jsonld` |
| `M1_Optics.jsonld` | Optics | `M1_extensions/optics/M1_Optics.jsonld` |
| `M1_Photography.jsonld` | Photography | `M1_extensions/photography/M1_Photography.jsonld` |
| `M1_Mythology.jsonld` | Mythology | `M1_extensions/mythology/M1_Mythology.jsonld` |

---

## M0 - Poclets (Concrete System Instances)

Poclets are **minimal complete system instances** — the most concrete layer. Each poclet instantiates M1/M2 concepts and undergoes full bicephalous ASFID+REVOI analysis.

| File | System | Domain |
|------|--------|--------|
| `M0_RAAS.jsonld` | Renin-Angiotensin-Aldosterone System | Biology |
| `M0_Yggdrasil.jsonld` | World Tree | Norse Mythology |
| `M0_NuclearReactorTypology.jsonld` | 9-pole enneagram reactor typology | Nuclear Engineering |
| `M0_ButterflyMetamorphosis.jsonld` | Metamorphosis cycle | Biology |
| `M0_BloodPressureControl.jsonld` | Blood pressure regulation | Biology |
| `M0_AdaptiveImmuneResponse.jsonld` | Immune response | Biology |
| `M0_CellSignalingModes.jsonld` | Cell signaling | Biology |
| `M0_Kidneys.jsonld` | Renal system | Biology |
| `M0_Transistor.jsonld` | Transistor operation | Electronics |

---

## 🧭 Decision Trees

### Where does a new concept belong?

```
New pattern identified
  │
  ├─ Valid across ALL knowledge fields without exception?
  │    └─ YES → M2 GenericConcept
  │              ├─ Combines N existing GenericConcepts? → GenericConceptCombo (Combo family)
  │              └─ Atomic pattern? → appropriate family (Dynamic, Structural...)
  │
  ├─ Valid across ≥3 DIFFERENT KnowledgeFields?
  │    └─ YES → M1_CoreConcepts KnowledgeFieldConcept
  │
  ├─ Reusable within SINGLE KnowledgeField with variants?
  │    └─ YES → KnowledgeFieldGenericCombo (M1 extension)
  │
  └─ Unique concrete instance?
       └─ YES → M0 Poclet
```

### Which ConceptContract to assign?

```
GenericConcept to classify
  │
  ├─ Can be initiated by an external Trigger? → m2:Triggerable
  ├─ Can be measured by an Observer?          → m2:Observable
  ├─ Can be assembled into a larger structure? → m2:Composable
  └─ Maintains persistent internal state?     → m2:Stateful
     (contracts are NOT mutually exclusive — State is Observable AND Stateful)
```

### ⊗ vs ⊙ vs ⊗₂

| Operator | Meaning | Use case |
|----------|---------|----------|
| `⊗` | Lattice join (dimension union, F⊔F=F) | GenericConcept formulas, Combo compiled formulas |
| `⊗₂F` | 2nd-order product (F at 2 distinct points) | Gradient (differential) |
| `⊗ⁿ⇒` | N-ary synergistic combination with emergence | GenericConceptCombo assembly |
| `⊙` | Disciplinary qualification (not tensor product) | KnowledgeFieldGenericCombo |

---

## 📋 TSCG Analysis Workflow

1. **ASFID first**: measure Territory dimensions (Eagle Eye) → get ASFID vector [A, S, F, I, D] ∈ [0,1]⁵
2. **REVOI second**: evaluate Map quality (Sphinx Eye) → get REVOI vector [R, E, V, O, I] ∈ [0,1]⁵
3. **Epistemic gap**: δ = 1 − mean(σᵢᵢ) — measures Territory/Map coupling maturity
4. **Identify GenericConcepts**: match ASFID signature to tensor formulas
5. **Check ConceptContracts**: does the system have Triggerable components? Observable states? Stateful memory?
6. **Assign M1/M0 concepts**: use `m2:characterizedBy` to link KnowledgeField-specific patterns to M2 basis
7. **Σ matrix**: estimate 5×5 coupling matrix, track evolution over time
8. **Iterate Φ/Ψ**: refine Territory↔Map alignment toward epistemic equilibrium

---

## 💡 Tips & Critical Rules

1. **R = Representability** (semantic encodability), NEVER Reproducibility
2. **⊗ in TSCG = lattice join** (F⊔F=F) — do NOT apply Kronecker product semantics
3. **⊗₂F ≠ duplication** — only use when the concept genuinely needs F at two distinct locations (e.g., Gradient = differential)
4. **M2 is pure**: no KnowledgeField references — if a concept needs disciplinary context, it belongs in M1
5. **IS-A vs characterizedBy**: `rdfs:subClassOf m2:GenericConcept` for M1 root concepts; `m2:characterizedBy` replaces wrong IS-A
6. **ConceptContracts are orthogonal to families**: a concept can implement multiple contracts across different families
7. **Always start with ASFID** before REVOI (Territory before Map)
8. **Validate transdisciplinarity**: M2 requires validation across ≥6 unrelated domains; M1_Core requires ≥3 domains
9. **Epistemic gap δ**: document `m2:hasEpistemicGap` ∈ [0,1] — lower = more mature
10. **Changelog discipline**: keep only the **3 most recent entries** in `m2:changelog`
11. **Author field**: always `"dcterms:creator": "Echopraxium with the collaboration of Claude AI"`
12. **@base**: all M0 and M1 files must declare `"@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"`
13. **M1 IRI style**: `M1_extensions/domain_name/M1_DomainName.jsonld`
14. **Language**: generated files in English, conversation may be in French

---

## 📚 References & Resources

**TSCG Core Files**:
| File | Layer | Version | Content |
|------|-------|---------|---------|
| `M3_GenesisSpace.jsonld` | M3 | 3.0.0 | ASFID ⊕ REVOI Hilbert space, Φ/Ψ operators |
| `M3_EagleEye.jsonld` | M3 | — | ASFID dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | 3.0.0 | REVOI dimension definitions |
| `M2_GenericConcepts.jsonld` | M2 | **15.9.0** | 81 GenericConcepts, 4 ConceptContracts |
| `M1_CoreConcepts.jsonld` | M1 | — | KnowledgeField, KnowledgeFieldConcept, KnowledgeFieldGenericCombo |
| `M1_extensions/biology/M1_Biology.jsonld` | M1 | — | Biological KnowledgeFieldConcepts |
| `M1_extensions/chemistry/M1_Chemistry.jsonld` | M1 | — | Chemical KnowledgeFieldConcepts |
| `M1_extensions/optics/M1_Optics.jsonld` | M1 | — | Optical patterns |
| `M1_extensions/photography/M1_Photography.jsonld` | M1 | — | Photography patterns |
| `M1_extensions/mythology/M1_Mythology.jsonld` | M1 | — | Mythological patterns |
| `M0_NuclearReactorTypology.jsonld` | M0 | — | 9-pole enneagram poclet |
| `M0_RAAS.jsonld` | M0 | — | Renin-Angiotensin-Aldosterone System |

**Key Literature**:
- Korzybski, A. (1933). *Science and Sanity*. "The map is not the territory"

---

## 🔄 Changelog

### v15.9.0 (2026-02-28) — Duplication, Propagation, Narration ⭐
1. ✅ **m2:Duplication** added (Dynamic, `S⊗I⊗F⊗D⊗V`) — structural replication with information preservation
2. ✅ **m2:Propagation** added (Combo, `⊗⇒(Cascade,Duplication,Network)` → 7D: `S⊗I⊗A⊗D⊗F⊗V⊗Im`)
3. ✅ **m2:Narration** added (Combo, `⊗⇒(Transformation,Representation,Relation)` → 8D richest Combo: `S⊗I⊗D⊗F⊗V⊗R⊗A⊗Im`)
4. ✅ **m2:Bifurcation** updated: `rdfs:subClassOf m2:Duplication` (semantic refinement)
5. ✅ **Counts**: Dynamic 14→15 | Combo 6→8 | dualPolarity 14→16 | neutralPolarity 52→53 | **Total 78→81**

### v15.8.0 (2026-02-27) — m2:Oscillator ⭐
1. ✅ **m2:Oscillator** added (Combo family, Territory perspective)
2. ✅ **Ternary combo** `⊗⇒(Component, Process, Trajectory | trajectoryShape=Circular)`
3. ✅ **rdfs:subClassOf m2:Component** → S dimension unlocked → full ASFID 5D: `S⊗A⊗I⊗D⊗F`
4. ✅ **4 ValueSpace attributes**: frequency, amplitude, phase, damping_ratio
5. ✅ **Counts**: m2:Combo 5→6 | neutralPolarity 51→52 | **Total 77→78**

### v15.7.0 (2026-02-24) — ConceptContract System ⭐
1. ✅ **ConceptContract** abstract class declared (owl:Thing, no tensor formula)
2. ✅ **m2:implements** AnnotationProperty declared
3. ✅ **4 ConceptContracts** created: Triggerable, Observable, Composable, Stateful
4. ✅ **16 GenericConcepts** updated with mixin rdfs:subClassOf + m2:implements

---

**End of TSCG Smart Prompt v15.9.0**

**Feedback**: Echopraxium (GitHub: https://github.com/Echopraxium/tscg)
