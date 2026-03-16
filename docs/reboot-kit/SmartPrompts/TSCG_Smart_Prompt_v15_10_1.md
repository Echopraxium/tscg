# TSCG Smart Prompt v15.10.1 - Architecture Consolidation & Corpus Expansion

**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Version**: 15.10.1  
**Date**: 2026-03-16  
**Author**: Echopraxium with the collaboration of Claude AI  
**Major Updates v15.9.0→v15.10.1**:
- ✅ **v15.10.0** : M2 Combo family migrated to M1_CoreConcepts; m2:Layer + m2:Context added; M2 now strictly atomic (75 concepts, 9 families)
- ✅ **v15.10.1** : m2:GenericConceptCombo restored as owl:Class in M2; m2:KnowledgeFieldConceptCombo added; M1_CoreConcepts v2.1.0 hosts all combo instances; StratifiedDissipation + CascadeAmplification added
- ✅ **Instances structure** : `system-models/` → `instances/` (poclets/, tscg-tools/, systemic-frameworks/, symbolic-system-grammars/)
- ✅ **New ontology types** : `m3:TransDisclet` (natively cross-disciplinary) + `m3:Enigma` (apparent-impossibility models)
- ✅ **Poclet corpus** : 21 validated poclets across 10+ domains

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
M2_GenericConcepts.jsonld   ← Universal atomic patterns (75 GenericConcepts, 9 families)
                              + m2:GenericConceptCombo (class) + m2:KnowledgeFieldConceptCombo (class)
        ↓ instantiates (combo classes)
M1_CoreConcepts.jsonld      ← KnowledgeField root concepts + 9 GenericConceptCombo instances
M1_extensions/biology/M1_Biology.jsonld
M1_extensions/chemistry/M1_Chemistry.jsonld  …
        ↓ instantiates
instances/poclets/RAAS/M0_RAAS.jsonld, …    ← Concrete systems (Poclets)
instances/tscg-tools/…                      ← TSCG tooling instances
instances/systemic-frameworks/…             ← External methodologies mapped to TSCG
instances/symbolic-system-grammars/…        ← Symbolic grammars (e.g. I Ching)
```

---

## 🗃️ Repository — instances/ Structure

The `instances/` folder replaces the former `system-models/` folder. It contains four sub-categories:

| Sub-folder | Content | Example |
|---|---|---|
| `instances/poclets/` | Single-domain concrete poclets (M0) | `Raas/M0_RAAS.jsonld` |
| `instances/tscg-tools/` | Reflexive tools (TSCG itself is the domain) | `TscgExplorer/`, `TscgPocletGenerator/` |
| `instances/systemic-frameworks/` | External established methodologies (e.g. VSM) | `Vsm/` |
| `instances/symbolic-system-grammars/` | Formal symbolic grammars | `Iching/` |

> ⚠️ **TscgTool vs Poclet**: TscgTools are reflexive (TSCG is the domain) and do not require a domain-specific M1 extension. Poclets validate single-domain systems and reference a M1 extension.

---

## M3 — Genesis Space (Foundational Basis) `v3.8.0`

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

### M3 Ontology Types (11)
`m3:TscgOntologyType` defines 11 architectural types for all TSCG ontologies:

| Type | Description |
|---|---|
| `m3:Genesis` | M3 foundational basis (M3_GenesisSpace.jsonld) |
| `m3:GenesisExtension` | Extensions of the M3 mathematical foundation |
| `m3:GenericConcepts` | M2 layer — transdisciplinary atomic patterns |
| `m3:DomainExtension` | M1 layer — disciplinary vocabularies |
| `m3:SystemicFramework` | Established external methodology mapped to TSCG |
| `m3:Poclet` | M0 — minimal single-domain system model |
| `m3:CaseStudy` | Pedagogical example (may be incomplete) |
| `m3:RealWorldSystem` | Concrete empirical system |
| `m3:SymbolicSystemGrammar` | Formal symbolic grammar (e.g. I Ching) |
| `m3:TscgTool` | Reflexive tool where TSCG itself is the domain |
| **`m3:TransDisclet`** | M0 — system natively existing across 2+ disciplines simultaneously *(v3.7.0)* |

### 🆕 m3:TransDisclet
A **TransDisclet** (Transdisciplinary + diminutive `-let`, analogous to "Poclet") models a system that exists **natively and autonomously** across multiple disciplines — not by analogy but by native instantiation.

**Defining criterion**: The same ASFID structure is identifiable in each disciplinary instance, and the cross-domain homology is structural, not merely metaphorical.

**Contrasts**:
- vs `m3:Poclet`: Poclet = one system in one domain (e.g. RAAS in biology). TransDisclet = same concept natively in 2+ disciplines (e.g. Transducer in electronics, biology, acoustics, physics).
- vs `m3:SystemicFramework`: Framework = external methodology mapped into TSCG. TransDisclet = concrete system natively present across disciplines.

**Qualification criteria** (all 3 required):
1. System exists natively in at least 2 distinct disciplines
2. Same GenericConcept structure (ASFID) identifiable in each disciplinary instance
3. Cross-domain homology is structural, not merely metaphorical

**Storage**: `instances/transdisclet/` (e.g. `instances/transdisclet/M0_Transducer.jsonld`)

### 🆕 m3:Enigma *(planned)*
An **Enigma** models systems built on **apparent impossibilities** that resolve through a mandatory ternary mediator structure.

**Core pattern**: `X ⊗ Mediator → Y` — direct binary relationships never exist; the Mediator is structurally required.

**Key properties**:
- The apparent impossibility is the pedagogical mechanism (categorical bias gap)
- Always resolves through a ternary structure (never binary)
- The Mediator is not optional — it is constitutive

**Example**: Fire Triangle (Fire = Fuel ⊗ Oxygen ⊗ Heat) — "fire from nothing" resolves through the three-part mediator structure.

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

**Iteration**: `v_T^(n+1) = v_T^(n) + α·Ψ(Φ(v_T^(n)))` converges to epistemic equilibrium.

---

## M2 — GenericConcepts Layer ⭐ `v15.10.1`

**75 atomic transdisciplinary GenericConcepts** across 9 families — universally valid patterns derived from M3 tensor products.  
M2 is **strictly atomic**: no KnowledgeField references, no Combo instances.  
Combo instances live in **M1_CoreConcepts.jsonld**.  
M2 defines the **class hierarchy** only: `m2:GenericConceptCombo` (owl:Class) and `m2:KnowledgeFieldConceptCombo` (owl:Class, subClassOf GenericConceptCombo).

### ⊗ Semantics in TSCG
**⊗ is a lattice join (⊔), NOT a Kronecker product.**  
Shared dimensions between GenericConceptCombo parents are deduplicated: F ⊔ F = F.  
`dim(Combo) = |⋃ᵢ dims(Mᵢ)|`  

Exception: `⊗₂F` (in Gradient) means F measured at two *distinct* points — genuine 2nd-order product (differential), not duplication.

### OWL Architecture
```
owl:Thing
  └── m2:ConceptContract   (behavioral interface, no tensor formula)
        ├── m2:Triggerable
        ├── m2:Observable
        ├── m2:Composable
        └── m2:Stateful
  └── m2:GenericConceptFamily  (9 families)
  └── m2:GenericConcept        (75 atomic concepts, rdfs:subClassOf)
  └── m2:GenericConceptCombo   (class only in M2 — instances in M1_CoreConcepts)
        └── m2:KnowledgeFieldConceptCombo (cross-KnowledgeField combos)
```

### GenericConcept Families (9) — Total: 75

| Family | Count | Primary dimensions |
|--------|------:|--------------------|
| **Structural** | 21 | S, I, A, R |
| **Dynamic** | 15 | D, F |
| **Ontological** | 10 | S, F, I, O, R |
| **Regulatory** | 9 | A, S, F, I |
| **Informational** | 8 | I, S |
| **Relational** | 5 | S, I, F |
| **Adaptive** | 4 | A, I, D |
| **Energetic** | 2 | F, D |
| **Teleonomic** | 1 | A, I, D |

> ⚠️ **Combo family removed from M2** (v15.10.0): All 9 GenericConceptCombo instances migrated to M1_CoreConcepts.jsonld. M2 retains only the `m2:GenericConceptCombo` and `m2:KnowledgeFieldConceptCombo` **class declarations**.

### GenericConcept Reference by Family

**Adaptive (4)**: Resilience `A⊗S`, Adaptation `I⊗F⊗D`, Emergence `I⊗S⊗D`, Memory `∫(D−F)dτ`

**Dynamic (15)**: Bifurcation `∂D/∂F` *(subClassOf Duplication)*, Duplication `S⊗I⊗F⊗D⊗V`,  
Transformation `D⊗S⊗I`, Process `D⊗F`, Trajectory `A⊗D⊗F`, Event `D⊗I`, Synergy `I⊗D`,  
Fusion `S⊗D`, Convergence `-∇·D/∇·D`, Behavior `S⊗D⊗F`, Tropism `A⊗S⊗D⊗F`,  
Action `D⊗I`, Amplification `Ft→D→It→R→O`, Alignment `I⊗A⊗S`,  
FeedbackLoop `⊗⇒(Process,Alignment,Homeostasis)`

**Energetic (2)**: Dissipation `F⊗D`, Storage `S⊗F`

**Informational (8)**: Code `I⊗S`, Coding `I⊗S⊗D`, Representation `I⊗S`, Language `I⊗S⊗F`,  
Pattern `S→I→A`, Signature `I⊗S`, Signal `I⊗F`, ValueSpace `It→V→O→R→Im`

**Ontological (10)**: Context `O⊗R⊗Im⊗E` *(new v15.10.0)*, Resource `F⊗I⊗R`, System `S⊗F`,  
Environment `F⊗I`, Observer `I⊗A`, State `I`, Substrate `S⊗F`,  
Gradient `⊗₂F or ⊗₂I`, Space `S⊗I`, Imbrication `S→S`

**Regulatory (9)**: Homeostasis `A⊗S⊗F`, Regulation `A⊗S⊗F`, Constraint `S⊗I`,  
Scope `S→I→A→R`, Threshold `A⊗I`, Trigger `D⊗I`, Activation `A⊗D`,  
Balance `A⊗S⊗F`, Trade-off `A⊗I⊗F`

**Relational (5)**: Agent `S⊗I⊗D`, Role `S⊗I`, Mediator `F⊗I⊗S`, Link `S⊗I⊗F`, Relation `S⊗I`

**Structural (21)**: Layer `S⊗I⊗A⊗R` *(new v15.10.0)*, Interoperability `S⊗I⊗F⊗V⊗E`,  
Hierarchy `S⊗A`, Network `S⊗I⊗F`, Symmetry `S`, Modularity `S⊗I`, Topology `S⊗I`,  
Segmentation `S⊗I⊗D`, Invariant `S⊗A`, Capacity `S⊗I`, Node `S⊗I`, Path `S⊗I⊗D`,  
Channel `S⊗I⊗F`, Cluster `S⊗I⊗A`, Component `S⊗I`, Hub `S⊗F`, Composition `S⊗I⊗A`,  
Polarity `S⊗I⊗A`, Identity `S→I→A→V→E`, Workflow `S⊗D⊗F`, Step `S⊗I⊗D`

**Teleonomic (1)**: Self-Organization `A⊗I⊗D`

---

## M1 — KnowledgeField Layer

### M1_CoreConcepts.jsonld `v2.1.0`
Central file hosting:
- **Root classes**: `m1:KnowledgeField`, `m1:KnowledgeFieldConcept`, `m1:KnowledgeFieldGenericCombo`
- **CorePattern instances**: `MultipolarNetwork (S⊗I⊗A)`, `CyclicTension (D⊗A⊗F)`
- **9 GenericConceptCombo instances** (typed as `['owl:Class', 'm2:GenericConceptCombo']`):

| Combo | Formula | Compiled dimensions |
|---|---|---|
| `Cascade` | `⊗⇒(Process,Step,Trajectory)` | `S⊗I⊗A⊗D⊗F` |
| `Processor` | `S⊗I⊗D⊗F⊗V⊗R` | 6D |
| `LocalActivationLateralInhibition` | `⊗⇒(Amplification,Regulation)\|F_A<<F_R` | — |
| `ButterflyEffect` | `⊗⇒(Amplification,Trajectory)\|λ>0` | — |
| `Oscillator` | `⊗⇒(Component,Process,Trajectory)\|Circular` → `S⊗A⊗I⊗D⊗F` | 5D |
| `Propagation` | `⊗⇒(Cascade,Duplication,Network)` → `S⊗I⊗A⊗D⊗F⊗V⊗Im` | 7D |
| `Narration` | `⊗⇒(Transformation,Representation,Relation)` → `S⊗I⊗D⊗F⊗V⊗R⊗A⊗Im` | 8D (richest) |
| `StratifiedDissipation` *(new v2.0.0)* | `S⊗I⊗A⊗D⊗F⊗V⊗R` | 7D |
| `CascadeAmplification` *(new v2.0.0)* | `⊗²⇒(Cascade,Amplification)\|gain>1` | — |

### M1 IS-A vs characterizedBy Rule
- `rdfs:subClassOf m2:GenericConcept` — correct for M1 root concepts
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
| `M1_Economics.jsonld` | Economics | `M1_extensions/economics/M1_Economics.jsonld` |

---

## M0 — Poclet Corpus (21 validated poclets)

Poclets are **minimal complete system instances** — the most concrete layer. Each poclet instantiates M1/M2 concepts and undergoes full bicephalous ASFID+REVOI analysis.

### instances/poclets/

| Folder | System | Domain |
|--------|--------|--------|
| `AdaptativeImmuneResponse/` | Adaptive immune response | Biology |
| `BloodPressureControl/` | Blood pressure regulation | Biology |
| `ButterflyMetamorphosis/` | Metamorphosis cycle | Biology |
| `CellSignalingModes/` | Cell signaling modes | Neuroscience/Biology |
| `ColorSynthesis/` | RGB/CMY/CMYK/HSL synthesis *(federated)* | Optics/Photography |
| `ComplexChemicalSynapse/` | Chemical synapse | Neuroscience/Biology |
| `ExposureTriangle/` | Exposure triangle | Photography |
| `FireTriangle/` | Fire triangle | Chemistry |
| `FourStrokeEngine/` | Four-stroke engine cycle | Mechanics |
| `Kidneys/` | Renal system | Biology |
| `KindlebergerMinsky/` | Financial bubble model | Economics/Finance |
| `MtgColorWheel/` | MTG color wheel | Game Design |
| `NuclearReactorsTypology/` | 9-pole enneagram reactor typology | Nuclear Engineering |
| `PhaseTransition/` | Phase transition (solid/liquid/gas) | Physics/Thermodynamics |
| `Raas/` | Renin-Angiotensin-Aldosterone System | Biology |
| `Tpack/` | TPACK pedagogical model | Education |
| `Transistor/` | Transistor operation | Electronics |
| `TrophicPyramid/` | Trophic pyramid | Ecology |
| `TvTestPattern/` | TV test pattern | Electronics/Broadcasting |
| `Vco/` | Voltage-Controlled Oscillator | Electronics |
| `Yggdrasil/` | World Tree | Norse Mythology |

### Other instance categories

| Folder | Content |
|--------|---------|
| `instances/tscg-tools/TscgExplorer/` | M2 GenericConcepts interactive explorer (Python) |
| `instances/tscg-tools/TscgPocletGenerator/` | CLI pipeline for poclet generation |
| `instances/systemic-frameworks/Vsm/` | Viable System Model mapped to TSCG |
| `instances/symbolic-system-grammars/Iching/` | I Ching as symbolic grammar |

---

## 🧭 Decision Trees

### Where does a new concept belong?

```
New pattern identified
  │
  ├─ Valid across ALL knowledge fields without exception?
  │    └─ YES → M2 GenericConcept (atomic, no KnowledgeField reference)
  │              ├─ Combines N existing GenericConcepts synergistically? → GenericConceptCombo instance in M1_CoreConcepts
  │              └─ Atomic pattern? → appropriate family (Dynamic, Structural...)
  │
  ├─ Valid across ≥3 DIFFERENT KnowledgeFields?
  │    └─ YES → M1_CoreConcepts KnowledgeFieldConcept
  │
  ├─ Reusable within SINGLE KnowledgeField with variants?
  │    └─ YES → KnowledgeFieldGenericCombo (M1 extension)
  │
  ├─ Same system concept natively in 2+ disciplines (not analogy)?
  │    └─ YES → m3:TransDisclet → instances/transdisclet/
  │
  ├─ System based on apparent impossibility resolving via ternary mediator?
  │    └─ YES → m3:Enigma
  │
  └─ Unique concrete instance in one domain?
       └─ YES → M0 Poclet → instances/poclets/
```

### TscgTool vs Poclet vs TransDisclet vs Enigma

| Type | Domain | Defining criterion | Storage |
|---|---|---|---|
| `m3:Poclet` | Single KnowledgeField | One system, one domain | `instances/poclets/` |
| `m3:TscgTool` | TSCG itself (reflexive) | No domain M1 extension needed | `instances/tscg-tools/` |
| `m3:TransDisclet` | 2+ disciplines natively | Same ASFID structure in each | `instances/transdisclet/` |
| `m3:Enigma` | Any | Apparent impossibility + mandatory ternary mediator | `instances/enigmas/` |

### Which ConceptContract to assign?

```
GenericConcept to classify
  │
  ├─ Can be initiated by an external Trigger? → m2:Triggerable
  ├─ Can be measured by an Observer?          → m2:Observable
  ├─ Can be assembled into a larger structure? → m2:Composable
  └─ Maintains persistent internal state?     → m2:Stateful
     (contracts are NOT mutually exclusive)
```

### ⊗ vs ⊙ vs ⊗₂

| Operator | Meaning | Use case |
|----------|---------|----------|
| `⊗` | Lattice join (dimension union, F⊔F=F) | GenericConcept formulas |
| `⊗₂F` | 2nd-order product (F at 2 distinct points) | Gradient (differential) |
| `⊗ⁿ⇒` | N-ary synergistic combination with emergence | GenericConceptCombo assembly |
| `⊙` | Disciplinary qualification (not tensor product) | KnowledgeFieldGenericCombo |

---

## 📋 TSCG Analysis Workflow

1. **ASFID first**: measure Territory dimensions (Eagle Eye) → get ASFID vector [A, S, F, I, D] ∈ [0,1]⁵
2. **REVOI second**: evaluate Map quality (Sphinx Eye) → get REVOI vector [R, E, V, O, I] ∈ [0,1]⁵
3. **Epistemic gap**: δ = 1 − mean(σᵢᵢ) — measures Territory/Map coupling maturity
4. **Identify GenericConcepts**: match ASFID signature to tensor formulas
5. **Check ConceptContracts**: Triggerable? Observable? Stateful? Composable?
6. **Assign M1/M0 concepts**: use `m2:characterizedBy` to link KnowledgeField-specific patterns to M2 basis
7. **Σ matrix**: estimate 5×5 coupling matrix, track evolution over time
8. **Iterate Φ/Ψ**: refine Territory↔Map alignment toward epistemic equilibrium

---

## 💡 Tips & Critical Rules

1. **R = Representability** (semantic encodability), NEVER Reproducibility
2. **⊗ in TSCG = lattice join** (F⊔F=F) — do NOT apply Kronecker product semantics
3. **⊗₂F ≠ duplication** — only use when the concept genuinely needs F at two distinct locations
4. **M2 is strictly atomic**: no KnowledgeField references, no Combo instances — only class declarations
5. **GenericConceptCombo instances live in M1_CoreConcepts** — not in M2
6. **IS-A vs characterizedBy**: `rdfs:subClassOf m2:GenericConcept` for M1 root concepts; `m2:characterizedBy` replaces wrong IS-A
7. **ConceptContracts are orthogonal to families**: a concept can implement multiple contracts
8. **Always start with ASFID** before REVOI (Territory before Map)
9. **Validate transdisciplinarity**: M2 requires validation across ≥6 unrelated domains; M1_Core requires ≥3 domains
10. **Epistemic gap δ**: document `m2:hasEpistemicGap` ∈ [0,1] — lower = more mature
11. **Changelog discipline**: keep only the **3 most recent entries** in `m2:changelog`
12. **Author field**: always `"dcterms:creator": "Echopraxium with the collaboration of Claude AI"`
13. **@base**: all M0 and M1 files must declare `"@base": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"`
14. **M1 IRI style**: `M1_extensions/domain_name/M1_DomainName.jsonld`
15. **Language**: generated files in English, conversation may be in French
16. **instances/ structure**: use `instances/poclets/`, `instances/tscg-tools/`, `instances/systemic-frameworks/`, `instances/symbolic-system-grammars/` — NOT the former `system-models/`
17. **TransDisclet**: requires structural homology (not analogy) across 2+ disciplines; same ASFID signature in each
18. **Enigma**: always resolves through mandatory ternary mediator — `X ⊗ Mediator → Y`; direct binary relationships never exist

---

## 📚 References & Resources

**TSCG Core Files**:
| File | Layer | Version | Content |
|------|-------|---------|---------|
| `M3_GenesisSpace.jsonld` | M3 | **3.8.0** | ASFID ⊕ REVOI, Φ/Ψ operators, 11 TscgOntologyTypes |
| `M3_EagleEye.jsonld` | M3 | — | ASFID dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | 3.0.0 | REVOI dimension definitions |
| `M2_GenericConcepts.jsonld` | M2 | **15.10.1** | 75 atomic GenericConcepts, 9 families, ConceptContracts |
| `M1_CoreConcepts.jsonld` | M1 | **2.1.0** | Root classes + 9 GenericConceptCombo instances |
| `M1_extensions/biology/M1_Biology.jsonld` | M1 | — | Biological KnowledgeFieldConcepts |
| `M1_extensions/chemistry/M1_Chemistry.jsonld` | M1 | — | Chemical KnowledgeFieldConcepts |
| `M1_extensions/optics/M1_Optics.jsonld` | M1 | — | Optical patterns |
| `M1_extensions/photography/M1_Photography.jsonld` | M1 | — | Photography patterns |
| `M1_extensions/mythology/M1_Mythology.jsonld` | M1 | — | Mythological patterns |
| `M1_extensions/economics/M1_Economics.jsonld` | M1 | — | Economics patterns |

**Key Literature**:
- Korzybski, A. (1933). *Science and Sanity*. "The map is not the territory"

---

## 🔄 Changelog

### v15.10.1 (2026-03-13) — Combo Architecture Stabilization ⭐
1. ✅ **m2:GenericConceptCombo** restored as `owl:Class` in M2 (instances remain in M1_CoreConcepts)
2. ✅ **m2:KnowledgeFieldConceptCombo** added (`owl:Class`, `subClassOf m2:GenericConceptCombo`) — cross-KnowledgeField combos
3. ✅ **M1_CoreConcepts v2.1.0**: all 9 combo instances typed as `['owl:Class', 'm2:GenericConceptCombo']`; `TransdisciplinaryCombo` class removed (redundant)
4. ✅ **New combos**: `StratifiedDissipation` (`S⊗I⊗A⊗D⊗F⊗V⊗R`, 7D) + `CascadeAmplification` (`⊗²⇒(Cascade,Amplification)|gain>1`)

### v15.10.0 (2026-03-13) — M2 Atomic Strictness ⭐
1. ✅ **Combo family migrated** from M2 to M1_CoreConcepts (7 combos → `m1core:TransdisciplinaryCombo`)
2. ✅ **m2:Layer** added (Structural, `S⊗I⊗A⊗R`, `subClassOf m2:Segmentation`)
3. ✅ **m2:Context** added (Ontological, `O⊗R⊗Im⊗E`, pure Map, `subClassOf m2:Environment`)
4. ✅ **M2 now strictly atomic**: 75 GenericConcepts across 9 families (Combo family suppressed)

### v15.9.0 (2026-02-28) — Duplication, Propagation, Narration ⭐
1. ✅ **m2:Duplication** added (Dynamic, `S⊗I⊗F⊗D⊗V`)
2. ✅ **m2:Propagation** added (Combo, 7D: `S⊗I⊗A⊗D⊗F⊗V⊗Im`)
3. ✅ **m2:Narration** added (Combo, 8D richest: `S⊗I⊗D⊗F⊗V⊗R⊗A⊗Im`)
4. ✅ **Bifurcation** updated: `rdfs:subClassOf m2:Duplication`; Total 78→81

---

**End of TSCG Smart Prompt v15.10.1**

**Feedback**: Echopraxium (GitHub: https://github.com/Echopraxium/tscg)
