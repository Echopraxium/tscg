# M1_Education — README

**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Layer**: M1 (KnowledgeField Extension)  
**KnowledgeField**: Education  
**Version**: 1.0.0  
**Date**: February 26, 2026  
**Author**: Echopraxium with the collaboration of Claude AI  
**Primary Motivation**: `M0_TPACK.jsonld` poclet analysis  
**Status**: ✅ Initial release — 10 KnowledgeFieldConcepts + 3 KnowledgeFieldGenericCombos

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Why an M1_Education Extension?](#why-an-m1_education-extension)
3. [Architecture](#architecture)
4. [KnowledgeField Declaration](#knowledgefield-declaration)
5. [KnowledgeFieldConcepts (10)](#knowledgefieldconcepts-10)
6. [KnowledgeFieldGenericCombos (3)](#knowledgefieldgenericcombos-3)
7. [M2 GenericConcept Coverage](#m2-genericconcept-coverage)
8. [TSCG Architectural Position](#tscg-architectural-position)
9. [Poclet Traceability](#poclet-traceability)
10. [Files](#files)
11. [Future Work](#future-work)
12. [References](#references)

---

## 🎯 Overview

`M1_Education.jsonld` is the TSCG domain extension for the **Education** KnowledgeField. It provides a vocabulary of 10 education-specific concepts formally grounded in M2 GenericConcepts, plus 3 KnowledgeFieldGenericCombos that specialize universal M2 patterns (Balance, Trade-off, Synergy) for the educational domain.

The extension was motivated by the TPACK poclet (`M0_TPACK.jsonld`), which identified 20 active M2 GenericConcepts in the education domain — the highest transdisciplinary density of any poclet analyzed — warranting a dedicated M1 formalization.

**Scope**: instructional design · pedagogical strategies · learning theory · educational technology · assessment · learner modeling · curriculum structure · scaffolding · communities of practice · knowledge integration (TPACK)

---

## 🔬 Why an M1_Education Extension?

The TPACK poclet analysis revealed that education is not merely a user of generic TSCG concepts: it has a rich domain-specific vocabulary that maps non-trivially to M2 patterns. Three signals justify a dedicated M1 extension:

### 1. High GenericConcept density

TPACK mobilizes 20 out of 74 M2 GenericConcepts (27%) — the highest coverage rate among all analyzed poclets. This indicates a system of high ontological richness requiring domain vocabulary to navigate.

### 2. Transdisciplinary validation anchor

Two M2 GenericConcepts — **Balance** and **Trade-off** — were first validated through TPACK analysis as a third corroborating domain (after Fire Triangle and Exposure Triangle). The education domain now contributes to the cross-domain validation of these concepts.

### 3. Unique domain patterns without M1 home

Concepts like `ScaffoldingMechanism` (temporary support tuned to the Zone of Proximal Development), `LearnerModel` (multi-dimensional representation of a learner's state), or `KnowledgeIntegration` (TPACK's core claim formalized as Synergy + Emergence) have no equivalent in M1_Biology, M1_Chemistry, or other existing extensions. They require M1_Education as their natural home.

---

## 🏗️ Architecture

```
M2_GenericConcepts.jsonld (74 universal patterns)
        ↓  m2:characterizedBy
M1_CoreConcepts.jsonld
  ├── m1:core:KnowledgeField          ← parent of m1:edu:Education
  ├── m1:core:KnowledgeFieldConcept   ← parent of all 10 concepts below
  └── m1:core:KnowledgeFieldGenericCombo ← parent of 3 combos below
        ↓  instantiates
M1_Education.jsonld
  ├── m1:edu:Education                ← KnowledgeField root
  ├── KnowledgeFieldConcepts (10)
  │     PedagogicalStrategy · LearningTheory · InstructionalDesign
  │     TechnologyIntegration · AssessmentStrategy · LearnerModel
  │     CurriculumStructure · ScaffoldingMechanism
  │     CommunityOfPractice · KnowledgeIntegration
  └── KnowledgeFieldGenericCombos (3)
        EducationalBalance · EducationalTradeOff · EducationalSynergy
        ↓  instantiates
M0_TPACK.jsonld (primary motivation poclet)
```

**Namespace**: `m1:edu:` → `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_extensions/education/M1_Education.jsonld#`

---

## 🎓 KnowledgeField Declaration

### Education

```
@id: m1:edu:Education
rdfs:subClassOf: m1:core:KnowledgeField
```

Root KnowledgeField for the education domain. Enables KnowledgeFieldGenericCombos of the form `Education ⊙ m2:GenericConcept`. Subfields: Instructional Design · Educational Technology · Learning Science · Curriculum Development · Teacher Education.

---

## 📚 KnowledgeFieldConcepts (10)

All concepts follow the OWL pattern:
```json
{
  "@type": "owl:Class",
  "rdfs:subClassOf": "m2:GenericConcept",
  "m2:characterizedBy": [ ... ]
}
```

---

### 1. PedagogicalStrategy

**Definition**: A principled approach to organizing learning activities and teacher-student interactions — HOW instruction is structured to achieve learning goals.

**M2 Basis**: `m2:Behavior ⊗ m2:Pattern ⊗ m2:Workflow`  
**ASFID Formula**: `S⊗I⊗D⊗F`

| Dimension | Role |
|-----------|------|
| S | Structured sequence of instructional activities |
| I | Information exchange between teacher and learners |
| D | Temporal unfolding of the pedagogical sequence |
| F | Flow of knowledge and feedback between participants |

**Key strategies**: Direct Instruction · Inquiry-Based Learning · Project-Based Learning · Flipped Classroom · Collaborative Learning · Differentiated Instruction

**TPACK link**: PK (Pedagogical Knowledge) component — the *how to teach* axis.

---

### 2. LearningTheory

**Definition**: A formal model of the cognitive, behavioral, or social mechanisms by which knowledge is acquired, retained, and applied.

**M2 Basis**: `m2:Representation ⊗ m2:Pattern ⊗ m2:Adaptation`  
**ASFID Formula**: `I⊗S⊗D`

| Theory | Core Claim | Pedagogical Implication |
|--------|-----------|------------------------|
| Behaviorism | Stimulus-response conditioning | Reinforcement, drill, mastery learning |
| Cognitivism | Mental schemas and information processing | Advance organizers, worked examples |
| Constructivism | Learner actively builds knowledge | Inquiry, PBL, collaborative discussion |
| Connectivism | Learning as network formation | PLN, curation, networked knowledge |

**TPACK link**: Theoretical foundation of PK — Learning theories inform pedagogical choices.

---

### 3. InstructionalDesign

**Definition**: The systematic process of creating learning experiences — bridging learning theory and classroom practice through structured design phases.

**M2 Basis**: `m2:Workflow ⊗ m2:Composition ⊗ m2:Hierarchy`  
**ASFID Formula**: `S⊗D⊗F`

**Key models**:

| Model | Phases | Nature |
|-------|--------|--------|
| ADDIE | Analysis → Design → Development → Implementation → Evaluation | Phase-gated process |
| Backward Design (UbD) | Goals → Evidence → Learning experiences | Goal-first, assessment-anchored |
| UDL | Engagement · Representation · Action & Expression | Inclusive, multi-modal |

**Constructive alignment principle**: Learning objectives, activities, and assessments must form a coherent triad.

**TPACK link**: The practice layer where TPACK knowledge is applied to produce actual instruction.

---

### 4. TechnologyIntegration

**Definition**: The embedding of digital tools into instructional contexts in ways that **transform** learning experiences — not merely substitute for analog tools.

**M2 Basis**: `m2:Transformation ⊗ m2:Adaptation ⊗ m2:Interoperability`  
**ASFID Formula**: `D⊗S⊗I⊗F`

**SAMR progression** (Puentedura):

| Level | Nature | Example |
|-------|--------|---------|
| Substitution | Direct replacement, no functional change | Word processor for pen-and-paper |
| Augmentation | Replacement with functional improvement | Spell-check, grammar tools |
| Modification | Significant task redesign | Collaborative Google Docs with real-time peer feedback |
| **Redefinition** | New tasks previously inconceivable | Students produce globally shared documentary |

**Design principle**: Technology is not neutral delivery — it transforms both content representation (TCK) and pedagogical possibilities (TPK).

**TPACK link**: TK component + TCK and TPK intersections — the technology axis of TPACK.

---

### 5. AssessmentStrategy

**Definition**: A method for gathering evidence of student learning and providing feedback to inform instruction or certify achievement.

**M2 Basis**: `m2:Signature ⊗ m2:Observer ⊗ m2:Threshold`  
**ASFID Formula**: `I⊗S⊗A`

| Type | Purpose | Frequency |
|------|---------|-----------|
| Formative | Monitor learning to adjust instruction (assessment FOR learning) | Ongoing, embedded |
| Summative | Evaluate learning at end of unit (assessment OF learning) | Periodic, high-stakes |
| Authentic | Real-world application (assessment AS learning) | Culminating |
| Diagnostic | Identify prior knowledge before instruction | Beginning of unit |

**FeedbackLoop pattern**: Assessment → Feedback → Instruction adjustment → Reassessment (`m2:FeedbackLoop`)

**TPACK link**: TPACK surveys and lesson rubrics verify teacher competence — assessment closes the TPACK development loop.

---

### 6. LearnerModel

**Definition**: A representation of a learner's current knowledge state, skills, prior knowledge, and Zone of Proximal Development — the foundation for personalization and differentiation.

**M2 Basis**: `m2:State ⊗ m2:Memory ⊗ m2:Gradient`  
**ASFID Formula**: `I⊗A⊗D`

**Key constructs**:

| Construct | TSCG Mapping | Pedagogical Implication |
|-----------|-------------|------------------------|
| Zone of Proximal Development (Vygotsky) | m2:Gradient between current State and target Attractor | Instruction targets ZPD — not too easy, not too hard |
| Prior Knowledge | m2:Memory (persistent state) | Activating prior knowledge critical for deep learning |
| Learning Profile | m2:State (multi-dimensional) | Foundation for differentiation and personalization |

**Adaptive systems**: Khan Academy, Duolingo continuously update LearnerModel to personalize instruction — a real-time instantiation of `m2:State` update.

**TPACK link**: PK requires understanding learner needs; TCK can personalize to learner model.

---

### 7. CurriculumStructure

**Definition**: The organized framework of content, objectives, and progressions that define what is taught, in what order, and at what depth across a course or program.

**M2 Basis**: `m2:Hierarchy ⊗ m2:Composition ⊗ m2:Scope`  
**ASFID Formula**: `S⊗I⊗A`

**Organizational principles**:

| Principle | Description | TSCG Mapping |
|-----------|-------------|-------------|
| Spiral Curriculum (Bruner, 1960) | Core concepts revisited at increasing depth across years | `m2:Imbrication` — nested revisitation at higher abstraction |
| Scope and Sequence | What is taught (scope) and in what order (sequence) | `m2:Hierarchy ⊗ m2:Trajectory` |
| Vertical Alignment | Coherence across grade levels | `m2:Alignment` across Hierarchy levels |
| Horizontal Alignment | Coherence across subjects at same grade level | `m2:Interoperability` across parallel structures |

**TPACK link**: CK (Content Knowledge) is organized through curriculum — curriculum structure is the scaffold for CK.

---

### 8. ScaffoldingMechanism

**Definition**: Temporary instructional support structures enabling learners to accomplish tasks within the Zone of Proximal Development, progressively faded as competence grows.

**M2 Basis**: `m2:Constraint ⊗ m2:Gradient ⊗ m2:Adaptation`  
**ASFID Formula**: `S⊗I⊗A⊗D`

**Scaffold types and fading strategies**:

| Type | Mechanism | Fading |
|------|-----------|--------|
| Worked examples | Expert solution as reference model | Completion problems → blank problems |
| Hints and prompts | Procedural guidance without full solution | Explicit hints → implicit cues → none |
| Graphic organizers | Visual structure for organizing ideas | Pre-structured → partially filled → blank |
| Peer scaffolding | More capable peer provides ZPD support | Guided pairing → peer collaboration → independent |

**Fading principle**: Scaffolds must make themselves unnecessary — their goal is learner autonomy (`m2:Adaptation` → autonomy).

**TPACK link**: TPK scaffolds technology adoption; PCK scaffolds content understanding.

---

### 9. CommunityOfPractice

**Definition**: A social learning structure where practitioners with shared goals deepen expertise through sustained interaction, sharing of practice, and collective problem-solving (Lave & Wenger, 1991).

**M2 Basis**: `m2:Network ⊗ m2:Role ⊗ m2:Synergy`  
**ASFID Formula**: `S⊗I⊗F`

**Wenger's three elements**:

| Element | Definition | TSCG Mapping |
|---------|-----------|-------------|
| Domain | Shared identity and area of concern | `m1:core:KnowledgeField` + `m2:Identity` |
| Community | Network of practitioners | `m2:Network` + `m2:Role` |
| Practice | Shared repertoire of resources, stories, tools | `m2:Signature` + `m2:Language` |

**Participation trajectory**: Legitimate Peripheral Participation — newcomer → full member (`m2:Trajectory` + `m2:Role`)

**Teacher application**: Professional Learning Communities (PLCs) are the primary mechanism for distributing and developing TPACK across a school or district.

**TPACK link**: CommunityOfPractice is the *TPACK diffusion mechanism* — how the framework spread globally.

---

### 10. KnowledgeIntegration ⭐

**Definition**: The synergistic synthesis of knowledge from multiple distinct domains into a coherent, emergent competence that exceeds the sum of the contributing domains.

**M2 Basis**: `m2:Balance ⊗ m2:Trade-off ⊗ m2:Synergy ⊗ m2:Emergence`  
**ASFID Formula**: `A⊗S⊗F⊗I⊗D` (full 5D coverage)

This is the formal TSCG articulation of **TPACK's core claim**:

```
TPACK = TK ⊗ PK ⊗ CK    where    TPACK >> TK + PK + CK
```

The strict inequality is the emergence condition. TPACK enables teaching that is *impossible* with any single domain alone.

**Venn geometry**: 7 regions — 3 base + 3 pairwise + 1 triple intersection (TPACK center).

**Transdisciplinary scope** — KnowledgeIntegration is not education-specific:

| Domain | Integration |
|--------|-------------|
| Scientific discovery | Physics ⊗ Mathematics ⊗ Experiment |
| Engineering design | Science ⊗ Engineering ⊗ Art (STEM/STEAM) |
| Medical diagnosis | Biology ⊗ Psychology ⊗ Technology |
| TPACK | Technology ⊗ Pedagogy ⊗ Content |

**TPACK link**: Central concept — KnowledgeIntegration IS the formal TSCG representation of TPACK itself.

---

## 🔗 KnowledgeFieldGenericCombos (3)

KnowledgeFieldGenericCombos use the **qualification operator ⊙** (not ⊗) to specialize a universal M2 GenericConcept for the Education KnowledgeField:

```
KnowledgeFieldGenericCombo = KnowledgeField ⊙ GenericConcept
```

All three combos are grounded in the TPACK poclet `m0:balancePrinciple`, `m0:tradeoffPrinciple`, and `m0:intersections`.

---

### EducationalBalance

```
Education ⊙ m2:Balance
rdfs:subClassOf: m1:core:KnowledgeFieldGenericCombo
m2:characterizedBy: m2:Balance (A⊗S⊗F)
```

The domain-specific manifestation of multi-factor equilibrium in educational design.

**Instances**:
- T-P-C balance (TPACK sweet spot)
- Depth vs. breadth balance in curriculum
- Formative vs. summative assessment balance
- Student-centered vs. teacher-centered balance
- Content coverage vs. pedagogical exploration balance

**Cross-poclet validation**: Balance is also instantiated in Fire Triangle (Fuel⊗O₂⊗Heat equilibrium) and Exposure Triangle (ISO⊗Aperture⊗Shutter) — three independent domains confirm this as a universal pattern.

---

### EducationalTradeOff

```
Education ⊙ m2:Trade-off
rdfs:subClassOf: m1:core:KnowledgeFieldGenericCombo
m2:characterizedBy: m2:Trade-off (A⊗I⊗F)
```

The Pareto constraint structure of educational design: teachers cannot simultaneously maximize all desirable objectives under real-world constraints.

**Instances**:
- TK breadth ↔ CK depth (technology exploration takes time from content)
- PK sophistication (inquiry) ↔ CK coverage (direct instruction is faster)
- Technology sophistication ↔ Equity (advanced tools require access)
- Personalization ↔ Scalability (individual tutoring vs. class instruction)

**Decision framework**: Backward design minimizes trade-off costs by anchoring all decisions to learning goals first — ensuring alignment before choosing tools and methods.

**Cross-poclet validation**: Trade-off also confirmed in Fire Triangle (removing any component stops fire) and Exposure Triangle (DoF ↔ Motion ↔ Grain).

---

### EducationalSynergy

```
Education ⊙ m2:Synergy
rdfs:subClassOf: m1:core:KnowledgeFieldGenericCombo
m2:characterizedBy: m2:Synergy (I⊗D)
```

The non-additive integration that produces emergent educational outcomes exceeding the sum of individual components.

**Instances**:
- `TPACK = TK ⊗ PK ⊗ CK >> TK + PK + CK` (Mishra & Koehler, 2006)
- `PCK = PK ⊗ CK >> PK + CK` (Shulman, 1986 — the original synergy insight)
- Collaborative learning: peer group > sum of individuals (Vygotsky, Dillenbourg)
- STEM: Science ⊗ Technology ⊗ Engineering ⊗ Mathematics
- Flipped classroom: pre-class video ⊗ in-class application > lecture OR practice alone

**Emergence signature**: Synergy is recognized when integration enables **new instructional possibilities absent from any single component**.

---

## 📊 M2 GenericConcept Coverage

The 10 KnowledgeFieldConcepts collectively reference **18 distinct M2 GenericConcepts**:

| M2 GenericConcept | Formula | Referenced by |
|-------------------|---------|---------------|
| Balance | A⊗S⊗F | KnowledgeIntegration, EducationalBalance |
| Trade-off | A⊗I⊗F | KnowledgeIntegration, EducationalTradeOff |
| Synergy | I⊗D | KnowledgeIntegration, CommunityOfPractice, EducationalSynergy |
| Emergence | I⊗S⊗D | KnowledgeIntegration |
| Transformation | D⊗S⊗I | TechnologyIntegration |
| Adaptation | I⊗F⊗D | TechnologyIntegration, ScaffoldingMechanism, LearningTheory |
| Interoperability | S⊗I⊗F⊗V⊗E | TechnologyIntegration |
| Workflow | S⊗D⊗F | PedagogicalStrategy, InstructionalDesign |
| Behavior | S⊗D⊗F | PedagogicalStrategy |
| Pattern | S→I→A | PedagogicalStrategy, LearningTheory |
| Hierarchy | S⊗A | InstructionalDesign, CurriculumStructure |
| Composition | S⊗I⊗A | InstructionalDesign, CurriculumStructure |
| Scope | S→I→A→R | CurriculumStructure |
| Representation | I⊗S | LearningTheory |
| Signature | I⊗S | AssessmentStrategy, CommunityOfPractice |
| Observer | I⊗A | AssessmentStrategy |
| Threshold | A⊗I | AssessmentStrategy |
| State | I | LearnerModel |
| Memory | ∫(D−F)dτ | LearnerModel, CommunityOfPractice |
| Gradient | ⊗₂F or ⊗₂I | LearnerModel, ScaffoldingMechanism |
| Constraint | S⊗I | ScaffoldingMechanism |
| Network | S⊗I⊗F | CommunityOfPractice |
| Role | S⊗I | CommunityOfPractice |
| Language | I⊗S⊗F | CommunityOfPractice |

---

## 🗺️ TSCG Architectural Position

```
M3 Genesis Space (10D Hilbert: ASFID ⊕ REVOI)
        ↓
M2 GenericConcepts (74 universal patterns)
        ↓  m2:characterizedBy
M1_CoreConcepts  ←──────────────────────────────────────────┐
M1_Biology                                                   │
M1_Chemistry                                                 │
M1_Mythology                                                 │
M1_Optics / M1_Photography                                  │
M1_Education  ←── (this file)                               │
        ↓  instantiates / motivates                          │
M0_TPACK  ──────────────────────────────────────────────────┘
         (primary motivation poclet)
```

**Relationship with M2**: M1_Education does NOT introduce new M2 concepts. It **instantiates** existing M2 GenericConcepts in the education KnowledgeField using `m2:characterizedBy`. If an education concept appears universal enough (e.g., KnowledgeIntegration in medicine, engineering, science), it should be proposed as a new M2 GenericConcept, not kept in M1.

**Relationship with M0**: M0 poclets in the education domain (TPACK and future ones) use `m1:edu:` concepts as their structural vocabulary, just as `M0_RAAS.jsonld` uses `m1:biology:` concepts.

---

## 🔍 Poclet Traceability

Every KnowledgeFieldConcept carries a `m1:edu:pocletEvidence` field linking it to its M0 motivation:

| Concept | pocletEvidence |
|---------|---------------|
| PedagogicalStrategy | M0_TPACK: PK component |
| LearningTheory | M0_TPACK: PK theoretical foundation |
| InstructionalDesign | M0_TPACK: practice layer where TPACK is applied |
| TechnologyIntegration | M0_TPACK: TK axis + TCK/TPK intersections |
| AssessmentStrategy | M0_TPACK: TPACK measurement instruments |
| LearnerModel | M0_TPACK: PK — understanding learner needs |
| CurriculumStructure | M0_TPACK: CK — content organization |
| ScaffoldingMechanism | M0_TPACK: TPK + PCK support structures |
| CommunityOfPractice | M0_TPACK: global TPACK diffusion mechanism |
| KnowledgeIntegration | M0_TPACK: formal representation of TPACK itself |

---

## 📁 Files

| File | Description |
|------|-------------|
| **M1_Education.jsonld** | This ontology — 13 nodes (1 KnowledgeField + 10 KnowledgeFieldConcepts + 3 Combos) |
| **M1_Education_README.md** | This file |
| **M0_TPACK.jsonld** | Primary motivation poclet (references `m1:edu:` namespace) |
| **TPACK_README.md** | TPACK poclet overview (includes M1_Education summary section) |

---

## 🚀 Future Work

### Immediate

1. ⏳ Register `m1:edu:` namespace in `TSCG_Documentation_Index.md`
2. ⏳ Add `M1_Education` to `TSCG_File_Tree.md`

### New poclets motivating M1_Education expansion

| Candidate poclet | Concepts that would require M1_Education |
|-----------------|------------------------------------------|
| **Bloom's Taxonomy** | CognitiveDomain, AffectiveDomain, PsychomotorDomain, TaxonomicLevel |
| **Vygotsky ZPD** | DevelopmentalZone, MediatedLearning, IntermentalSpace |
| **Constructivism** (Piaget) | CognitiveScheme, Assimilation, Accommodation, Equilibration |
| **Flipped Classroom** | LearningPhase, AsynchronousContent, SynchronousApplication |
| **Universal Design for Learning** | AccessibilityDimension, MultimodalRepresentation |

### Potential new KnowledgeFieldConcepts

| Concept | M2 Basis | Motivation |
|---------|----------|------------|
| LearningObjective | Signature ⊗ Threshold ⊗ Scope | ADDIE / backward design |
| TransferMechanism | Transformation ⊗ Adaptation | How learning generalizes across contexts |
| MotivationRegulator | Homeostasis ⊗ Activation ⊗ Agent | Engagement management in instruction |
| FeedbackCycle | FeedbackLoop ⊗ Regulation | Assessment-instruction loop formalization |
| LiteracyDomain | Language ⊗ Code ⊗ Signature | Digital/data/AI literacy as new TK subcategories |

### Potential new KnowledgeFieldGenericCombos

| Combo | Formula | Domain motivation |
|-------|---------|-------------------|
| EducationalEmergence | Education ⊙ m2:Emergence | Emergent curriculum; emergent understanding |
| EducationalAdaptation | Education ⊙ m2:Adaptation | Adaptive learning systems, differentiated instruction |
| EducationalFeedbackLoop | Education ⊙ m2:FeedbackLoop | Formative assessment cycle |

---

## 📚 References

### Learning Theory Foundations

- Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.
- Piaget, J. (1952). *The origins of intelligence in children*. International Universities Press.
- Bloom, B. S. (1956). *Taxonomy of educational objectives: Cognitive domain*. McKay.
- Gagné, R. M. (1965). *The conditions of learning*. Holt, Rinehart and Winston.
- Siemens, G. (2005). Connectivism: A learning theory for the digital age. *International Journal of Instructional Technology and Distance Learning, 2*(1), 3–10.

### Instructional Design

- Wiggins, G., & McTighe, J. (1998). *Understanding by design*. ASCD.
- Merrill, M. D. (2002). First principles of instruction. *Educational Technology Research and Development, 50*(3), 43–59.
- Meyer, A., Rose, D. H., & Gordon, D. (2014). *Universal design for learning: Theory and practice*. CAST.

### Educational Technology / TPACK

- Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge: A framework for teacher knowledge. *Teachers College Record, 108*(6), 1017–1054.
- Puentedura, R. R. (2006). *Transformation, technology, and education*. [SAMR model]
- Shulman, L. S. (1986). Those who understand: Knowledge growth in teaching. *Educational Researcher, 15*(2), 4–14.

### Communities of Practice

- Lave, J., & Wenger, E. (1991). *Situated learning: Legitimate peripheral participation*. Cambridge University Press.
- Wenger, E. (1998). *Communities of practice: Learning, meaning, and identity*. Cambridge University Press.

### TSCG Framework

- `M2_GenericConcepts.jsonld` v15.7.0 — 74 GenericConcepts (Balance, Trade-off, Synergy, Emergence, etc.)
- `M1_CoreConcepts.jsonld` — KnowledgeField, KnowledgeFieldConcept, KnowledgeFieldGenericCombo
- `M0_TPACK.jsonld` v1.1.0 — Primary motivation poclet (REVOI = 0.94)
- `TSCG_Smart_Prompt_v15_7_0.md` — Framework conventions and OWL patterns

---

**Version**: 1.0.0  
**Date**: February 26, 2026  
**Status**: ✅ Initial release  
**Author**: Echopraxium with the collaboration of Claude AI  
**License**: CC-BY-4.0
