# M2 Behavioral Metaconcepts - Visual Guide

**Quick Reference for v14.3.0**

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   BEHAVIORAL FAMILY                         │
│                                                             │
│   Behavior (S⊗D⊗F) ────────┬──── Dual Polarity            │
│       │                     │     (Territory/Map)           │
│       │ subClassOf          │                               │
│       │                     │                               │
│   Tropism (A⊗S⊗D⊗F) ───────┴──── Double Dual               │
│       │                           (+ Positive/Negative)     │
│       │ decomposedInto                                      │
│       │                                                     │
│   Step (S⊗I⊗D) ────────────────── subClassOf Node          │
│       │                                                     │
│       │ triggers                                            │
│       │                                                     │
│   Action (D⊗I) ────────────────── Atomic Unit              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   WORKFLOW FAMILY                           │
│                                                             │
│   Process (D⊗F) ────────────────── M2 Existing             │
│       │                                                     │
│       │ implementedBy                                       │
│       │                                                     │
│   Workflow (S⊗D⊗F) ────────────── Prescriptive             │
│       │                                                     │
│       │ (shares Steps with Behavior)                        │
│       └──────────► Step (S⊗I⊗D)                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Tensor Formula Progression

```
Action      D ⊗ I                     [Order 2: Atomic]
               ↓ add S
Step        S ⊗ I ⊗ D                 [Order 3: Structural Node]
               ↓ replace I with F
Behavior    S ⊗ D ⊗ F                 [Order 3: Network Pattern]
               ↓ add A
Tropism     A ⊗ S ⊗ D ⊗ F             [Order 4: Gradient-directed]
```

---

## 3. Concrete Example: Butterfly Metamorphosis

```
┌─────────────────────────────────────────────────────────────┐
│  Behavior: "Holometabolic Development"                      │
│  Formula: S⊗D⊗F                                             │
│  Polarity: Dual (Observable/Modelable)                      │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬──────────────┐
        ↓                  ↓                  ↓              ↓
    ┌──────┐          ┌──────┐          ┌──────┐      ┌──────┐
    │ Egg  │ ────→    │Larva │ ────→    │ Pupa │ ───→ │Adult │
    └──────┘          └──────┘          └──────┘      └──────┘
    Step 1            Step 2            Step 3        Step 4
       │                 │                 │             │
       │ triggers        │ triggers        │ triggers    │ triggers
       ↓                 ↓                 ↓             ↓
   Cell Division    Feeding/Growth    Histolysis    Reproduction
   [Action]         [Actions]         Histogenesis  Flight
                                      [Actions]     [Actions]
```

---

## 4. Concrete Example: Phototropism (Tropism)

```
┌─────────────────────────────────────────────────────────────┐
│  Tropism: "Plant Phototropism"                              │
│  Formula: A⊗S⊗D⊗F                                           │
│  Gradient: Light intensity field ───► [Attractor]           │
│  Polarity: Positive (attraction towards light)              │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
    ┌──────┐          ┌──────┐          ┌──────┐
    │Detect│ ────→    │Signal│ ────→    │ Grow │
    └──────┘          └──────┘          └──────┘
    Step 1            Step 2            Step 3
       │                 │                 │
       │ triggers        │ triggers        │ triggers
       ↓                 ↓                 ↓
  Photoreceptor     Auxin             Cell Elongation
  Activation    Redistribution         on Shaded Side
  [Action]          [Action]           [Action]

Result: Stem bends ───► towards ───► Light Source
```

---

## 5. Behavior vs Workflow (Dual Perspectives)

```
┌──────────────────────────────────────────────────────────────┐
│               TERRITORY (What IS observed)                    │
│                                                              │
│   Behavior: "Server Response Pattern"                        │
│   ┌────────┐   ┌─────────┐   ┌─────────┐   ┌────────┐      │
│   │Receive │──→│  Parse  │──→│ Process │──→│ Respond│      │
│   └────────┘   └─────────┘   └─────────┘   └────────┘      │
│      (Measured execution: 15ms, 23ms, 47ms, 8ms)            │
│                                                              │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                 MAP (What SHOULD occur)                       │
│                                                              │
│   Workflow: "REST API Specification"                         │
│   ┌────────┐   ┌─────────┐   ┌─────────┐   ┌────────┐      │
│   │Receive │──→│  Parse  │──→│ Process │──→│ Respond│      │
│   └────────┘   └─────────┘   └─────────┘   └────────┘      │
│      (Prescribed: <20ms, <30ms, <50ms, <10ms)               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. Polarity Comparison Table

| Metaconcept | Polarity Type | Pole 1 | Pole 2 | Additional |
|-------------|---------------|--------|--------|------------|
| **Action** | Bicephalous | Territory (measured) | Map (modeled) | - |
| **Step** | Bicephalous | Territory (observed) | Map (prescribed) | - |
| **Behavior** | Bicephalous | Territory (observable) | Map (modelable) | - |
| **Tropism** | **Double Dual** | Territory/Map | + | Positive/Negative |
| **Workflow** | Faceted | Structural (static) | Executory (dynamic) | - |

---

## 7. Step → Action Trigger Examples

```
┌──────────────────────────────────────────────────────────────┐
│  Step: "Make Roux" (Recipe)                                  │
│  Context: French cooking workflow                            │
└──────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
    [Heat butter]      [Add flour]       [Stir continuously]
    Action 1           Action 2          Action 3
    D⊗I                D⊗I               D⊗I

Result: Roux formed (thickening agent)
```

```
┌──────────────────────────────────────────────────────────────┐
│  Step: "Training Epoch" (Machine Learning)                   │
│  Context: Neural network learning workflow                   │
└──────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
    [Forward Pass]    [Backward Pass]    [Update Weights]
    Action 1          Action 2           Action 3
    D⊗I               D⊗I                D⊗I

Result: Model parameters updated
```

---

## 8. Epistemic Gap Spectrum

```
0.15 ◄────────────────────────────────────────────► 0.22

Action     Tropism    Behavior/Step         Workflow
(0.15)     (0.18)     (0.20)                (0.22)
  │          │           │                     │
  │          │           │                     │
CONCRETE    VERY     OBSERVABLE         PRESCRIPTIVE
ATOMIC   OBSERVABLE   PATTERN             ABSTRACT
```

**Interpretation:**
- Lower gap = More directly measurable
- Higher gap = More abstract/prescriptive

---

## 9. Use Case Decision Tree

```
Need to model sequential system?
    │
    ├─► Pure temporal sequence? ────► Use: Process (D⊗F)
    │
    ├─► Decomposable pattern? ────────┐
    │                                 │
    │   ├─► Observable? ────► Use: Behavior (S⊗D⊗F)
    │   │
    │   └─► Prescriptive? ──► Use: Workflow (S⊗D⊗F)
    │
    ├─► Gradient-driven? ──────► Use: Tropism (A⊗S⊗D⊗F)
    │
    ├─► Network node in sequence? ──► Use: Step (S⊗I⊗D)
    │
    └─► Atomic operation? ────► Use: Action (D⊗I)
```

---

## 10. Real-World Applications

### Biology
```
Tropism: Chemotaxis (E. coli)
    Step: Sense → Action: Receptor binding
    Step: Compare → Action: Compute gradient
    Step: Tumble/Run → Action: Flagellar rotation
```

### Software Engineering
```
Workflow: CI/CD Pipeline
    Step: Build → Action: Compile, Link
    Step: Test → Action: Unit tests, Integration tests
    Step: Deploy → Action: Package, Upload, Restart
```

### Physiology
```
Behavior: Baroreflex
    Step: Sense → Action: Baroreceptor activation
    Step: Integrate → Action: Medulla processing
    Step: Respond → Action: Sympathetic/Parasympathetic output
```

### Cooking
```
Workflow: Recipe
    Step: Prepare → Action: Chop, Measure
    Step: Cook → Action: Heat, Stir, Season
    Step: Plate → Action: Arrange, Garnish
```

---

## 11. Integration with Existing M2

### Related Metaconcepts

| Existing M2 | New M2 | Relationship |
|-------------|--------|--------------|
| **Process** | Workflow | Workflow implementsProcess Process |
| **Node** | Step | Step subClassOf Node |
| **Network** | Behavior | Behavior specializes Network with dynamics |
| **Attractor** | Tropism | Tropism hasGradient Attractor |
| **Regulation** | Tropism | Both use Attractor, different mechanisms |

---

## 12. Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  BEHAVIORAL METACONCEPTS CHEAT SHEET                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Behavior (S⊗D⊗F)                                            ║
║    └─► Decomposable network pattern                          ║
║    └─► Examples: Hunting, HTTP handling, Photosynthesis      ║
║                                                              ║
║  Tropism (A⊗S⊗D⊗F)  [subClassOf Behavior]                   ║
║    └─► Gradient-directed behavior                            ║
║    └─► Examples: Phototropism, Chemotaxis, Geotropism        ║
║                                                              ║
║  Workflow (S⊗D⊗F)                                            ║
║    └─► Prescriptive Process implementation                   ║
║    └─► Examples: Recipe, CI/CD, Clinical protocol            ║
║                                                              ║
║  Step (S⊗I⊗D)  [subClassOf Node]                            ║
║    └─► Temporal node, triggers Actions                       ║
║    └─► Examples: Egg stage, Make roux, Parse request         ║
║                                                              ║
║  Action (D⊗I)                                                ║
║    └─► Atomic operation                                      ║
║    └─► Examples: Cell division, Heat butter, Tokenize        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 13. FAQ

**Q: What's the difference between Behavior and Workflow?**
- **Behavior:** Describes what IS observed (Territory)
- **Workflow:** Prescribes what SHOULD occur (Map)

**Q: Can a Step trigger multiple Actions?**
- **Yes:** Cardinality is 1:N (one Step can trigger N Actions)

**Q: Is Tropism always biological?**
- **No:** Any gradient-directed system (robots, algorithms, economics)

**Q: Why same formula for Behavior and Workflow?**
- **Both are S⊗D⊗F** but serve different epistemic roles (descriptive vs prescriptive)

**Q: Can Actions be decomposed further?**
- **No:** By definition atomic in behavioral context (M2 level)

---

## 14. Validation Status

| Metaconcept | Status | Validated By |
|-------------|--------|--------------|
| Behavior | ✅ Validated | Butterfly, BloodPressure, HTTP |
| Tropism | ✅ Validated | Phototropism (biological literature) |
| Workflow | ✅ Validated | Recipe, CI/CD, Clinical protocols |
| Step | ✅ Validated | All poclets with sequences |
| Action | ✅ Validated | All decomposable behaviors |

---

**End of Visual Guide**
