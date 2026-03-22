# Four-Stroke Engine Poclet

## Overview

The **Four-Stroke Engine** is a minimal yet complete system representation of the thermodynamic cycle that powers most internal combustion engines. This poclet demonstrates how a cyclic process can convert chemical energy (fuel) into mechanical work through four sequential phases: **Intake**, **Compression**, **Power**, and **Exhaust**.

As a TSCG poclet, the Four-Stroke Engine serves three critical functions:
1. **Framework Validation**: Demonstrates TSCG's applicability to thermodynamic systems
2. **M2 GenericConcept Discovery**: Reveals fundamental patterns like Workflow, FeedbackLoop, and Transformation
3. **M1 Domain Bootstrapping**: Identifies thermodynamics-specific concepts (Otto Cycle, Compression Ratio, Valve Timing, Thermal Efficiency)

## System Components

The Four-Stroke Engine consists of **4 sequential strokes** (minimal configuration for a complete thermodynamic cycle):

### 1. Intake Stroke
- **Piston**: Moves downward (Top Dead Center → Bottom Dead Center)
- **Intake Valve**: Open
- **Exhaust Valve**: Closed
- **Action**: Air-fuel mixture drawn into cylinder
- **Volume**: Increases from V_min to V_max

### 2. Compression Stroke
- **Piston**: Moves upward (BDC → TDC)
- **Both Valves**: Closed
- **Action**: Air-fuel mixture compressed
- **Pressure & Temperature**: Increase
- **Compression Ratio**: r = V_max / V_min (typically 8:1 to 12:1)

### 3. Power Stroke (Combustion)
- **Piston**: Moves downward (TDC → BDC)
- **Both Valves**: Closed
- **Trigger**: Spark plug ignites compressed mixture
- **Action**: Rapid combustion → pressure spike → piston pushed down
- **Work Output**: Mechanical energy transferred to crankshaft

### 4. Exhaust Stroke
- **Piston**: Moves upward (BDC → TDC)
- **Intake Valve**: Closed
- **Exhaust Valve**: Open
- **Action**: Combustion products expelled from cylinder
- **Cycle Reset**: Returns to initial state for next cycle

## ASFID Analysis (Eagle Eye — Territory)

| Dimension | Score | Description |
|-----------|-------|-------------|
| **A**ttractor | 0.85 | Steady-state rotation (target RPM), conversion of heat → mechanical work |
| **S**tructure | 0.90 | Piston-cylinder assembly, valves, connecting rod, crankshaft; cyclic topology |
| **F**low | 0.95 | Air-fuel intake, exhaust gas output, energy flow (chemical → heat → work) |
| **I**nformation | 0.80 | Valve timing, ignition timing, compression ratio, P-V-T state variables |
| **D**ynamics | 0.85 | 4-stroke sequence, 2 crankshaft revolutions per cycle, combustion bifurcation |

**Territory ASFID Vector**: `(0.85, 0.90, 0.95, 0.80, 0.85)`
`‖ASFID‖ = 1.969`

## REVOI Analysis (Sphinx Eye — Map)

> **Note v1.1.0**: The Map perspective acronym is **REVOI** (canonical TSCG notation), not ORIVE.  
> Dimension definitions: **R**epresentability · **E**volvability · **V**erifiability · **O**bservability · **I**nteroperability

| Dimension | Score | Description |
|-----------|-------|-------------|
| **R**epresentability | 0.90 | Highly encodable via P-V diagrams, T-s diagrams, thermodynamic equations, animations |
| **E**volvability | 0.85 | Base model readily extended to VVT, GDI, turbocharging, hybrid powertrains |
| **V**erifiability | 0.90 | Validated by 150+ years of engineering practice; matches First & Second Law predictions |
| **O**bservability | 0.90 | Measurable via RPM, cylinder pressure, temperature, airflow sensors |
| **I**nteroperability | 0.85 | Modular design (1-cyl, 4-cyl, V6, V8), fuel flexibility (gasoline, E85, methanol) |

**Map REVOI Vector**: `(0.90, 0.85, 0.90, 0.90, 0.85)`
`‖REVOI‖ = 1.969`

## Epistemic Gap (ΔΘ)

```
ΔΘ = ‖ASFID − REVOI‖
   = ‖(0.85−0.90, 0.90−0.85, 0.95−0.90, 0.80−0.90, 0.85−0.85)‖
   = ‖(−0.05, +0.05, +0.05, −0.10, 0.00)‖
   = √(0.0025 + 0.0025 + 0.0025 + 0.01 + 0)
   = √0.0175
   ≈ 0.132
```

**Interpretation**: Excellent alignment between physical system (Territory) and theoretical model (Map).  
The small gap (0.132) confirms the Otto cycle as a high-fidelity representation of real engine behavior.

> Previous v1.0.x value of ΔΘ = 0.16 was computed against the (now deprecated) ORIVE vector with different dimension semantics.

## Minimality Validation

**Why 4 strokes is minimal**:
- **3 strokes**: Insufficient to separate intake and exhaust phases → incomplete cycle
- **2 strokes**: Exists but less efficient (fuel loss during exhaust overlap)
- **4 strokes**: Optimal balance between completeness and simplicity

**Irreducibility Test**: Removing any stroke destroys the cycle's functionality:
- No Intake → No fuel/air
- No Compression → No pressure for efficient combustion
- No Power → No work output
- No Exhaust → Cylinder fills with combustion products

## M2 GenericConcepts Mobilized

This poclet activates **20 GenericConcepts** (27% of M2_GenericConcepts.jsonld v15.10.1 — 20/75):

> **Note v1.2.0**: Aligned to M2 v15.10.1. Deprecated concepts replaced: `Cycle` → `FeedbackLoop` + `Process`, `Sequence` → `Workflow`, `Flow` → `Channel`, `Synchronization` → `Alignment`. `Efficiency` relocated to M1_Thermodynamics (domain-specific).

### Structural GenericConcepts
- **Component** (S⊗I): 4 strokes as elementary parts
- **Composition** (S⊗I⊗A): Piston + connecting rod + crankshaft assembly
- **Symmetry** (S): Cylindrical geometry
- **Modularity** (S⊗I): Multi-cylinder engines (4-cyl = 4 × single-cyl)

### Dynamic GenericConcepts
- **Process** (D⊗F): Each stroke is a sub-process
- **Step** (S⊗I⊗D): Each stroke as elementary unit in the Workflow
- **Workflow** (S⊗D⊗F): Strict ordered sequencing of the 4 strokes *(replaces deprecated `Sequence`)*
- **FeedbackLoop** (Process⊗Alignment⊗Homeostasis): Periodic return to initial state — defines cyclicity *(replaces deprecated `Cycle`)*
- **Bifurcation** (∂D/∂F): Rapid combustion transition at power stroke onset
- **Transformation** (D⊗S⊗I): Chemical energy → Heat → Mechanical work

### Regulatory GenericConcepts
- **Constraint** (S⊗I): Fixed cylinder volume, compression ratio
- **Threshold** (A⊗I): Ignition point (spark timing)
- **Trigger** (D⊗I): Spark ignites combustion
- **Alignment** (I⊗A⊗S): Multi-cylinder timing coordination *(replaces deprecated `Synchronization`)*

### Energetic GenericConcepts
- **Channel** (S⊗I⊗F): Air-fuel intake path + exhaust gas conduit *(replaces deprecated `Flow`)*
- **Dissipation** (F⊗D): Heat loss through cylinder walls (cooling system)
- **Gradient** (⊗₂F): Pressure gradient drives piston on power stroke

### Teleonomic GenericConcepts
- **Trade-off** (A⊗I⊗F): Higher compression → higher efficiency BUT higher knock risk
- **Balance** (A⊗S⊗F): Valve timing, ignition timing, piston-crankshaft synchronization
- **Emergence** (I⊗S⊗D): Continuous crankshaft rotation emerges from 4 discrete strokes

> `Efficiency` removed from this list — domain-specific metric relocated to **M1_Thermodynamics** as `ThermalEfficiency` (η = 1 − 1/r^(γ−1)).

## Transdisciplinary Validation

The "4-phase cycle" pattern appears across multiple domains:

| Domain | Example | 4 Phases |
|--------|---------|----------|
| **Cardiology** | Cardiac cycle | Atrial diastole, Atrial systole, Ventricular diastole, Ventricular systole |
| **Economics** | Business cycle | Expansion, Peak, Contraction, Trough |
| **Chemistry** | Ion pump | 4 conformational states in Na⁺/K⁺-ATPase |
| **Climatology** | Seasonal cycle | Spring, Summer, Fall, Winter |

This cross-domain recurrence validates **Workflow** + **FeedbackLoop** as the universal M2 pattern capturing both ordered sequencing and cyclic return — the two inseparable faces of any 4-phase cycle.

## M1 Domain Contributions

This poclet identifies **8 thermodynamics-specific concepts** for `M1_extensions/thermodynamics/M1_Thermodynamics.jsonld`:

1. **Stroke**: A phase in an engine cycle (Intake, Compression, Power, Exhaust)
2. **Compression Ratio**: r = V_max / V_min (key performance parameter)
3. **Otto Cycle**: Idealized thermodynamic cycle (basis for gasoline engines)
4. **Valve Timing**: Precise synchronization of intake/exhaust valve opening/closing
5. **Ignition Timing**: Spark timing for combustion initiation
6. **Bore & Stroke**: Cylinder diameter and piston travel distance
7. **Displacement**: Total cylinder volume (engine size metric)
8. **Thermal Efficiency**: η = 1 − (1/r^(γ−1)) — domain-specific metric relocated from M2 (was `m2:Efficiency`, removed in v15)

## Pedagogical Value

The Four-Stroke Engine is ideal for teaching:
- **Systems Thinking**: How sequential processes create emergent behavior (rotation)
- **Energy Conversion**: Chemical → Thermal → Mechanical transformation chain
- **Cyclicity**: Periodic systems and state-space return
- **Trade-offs**: Compression ratio vs. knock resistance
- **Modularity**: Single-cylinder principles scale to multi-cylinder engines

## Historical Context

- **1876**: Nicolaus Otto patents the four-stroke engine
- **1886**: Karl Benz builds first automobile with four-stroke engine
- **1920s–present**: Becomes dominant design for gasoline engines
- **Modern Era**: Electronic fuel injection, variable valve timing enhance efficiency

## Engineering Significance

**Why 4-stroke dominates over 2-stroke**:
- ✅ Better fuel efficiency (no fresh charge loss)
- ✅ Lower emissions (complete exhaust scavenging)
- ✅ Quieter operation
- ✅ Longer engine life (better lubrication)
- ❌ More complex (requires valve train)
- ❌ Lower power-to-weight ratio

## Thermodynamic Efficiency

**Ideal Otto Cycle Efficiency**:
```
η = 1 − (1 / r^(γ−1))
```
Where:
- η = thermal efficiency
- r = compression ratio
- γ = heat capacity ratio (≈1.4 for air)

**Example**: r = 10:1 → η ≈ 60% (ideal)  
**Reality**: Real engines achieve 25–30% due to friction, heat loss, incomplete combustion

## Bicephalous Perspective

### Eagle Eye (Territory — ASFID)
- **Observable**: Piston motion, pressure waves, temperature profiles
- **Measurable**: RPM, torque, power output, fuel consumption
- **Physical**: Real metal components, combustion reactions, heat transfer

### Sphinx Eye (Map — REVOI)
- **Theoretical**: Idealized Otto cycle (reversible, adiabatic, constant volume)
- **Pedagogical**: Simplified P-V diagram for education
- **Epistemic Gap**: ΔΘ = 0.132 (small gap) → high-fidelity model

**Synthesis**: The Four-Stroke model is an excellent map of the territory — it accurately predicts real engine behavior while remaining simple enough for educational and engineering purposes.

## Conclusion

The **Four-Stroke Engine** is a validated TSCG poclet demonstrating:
- ✅ **Minimality**: 4 strokes is the irreducible minimum
- ✅ **Completeness**: All 5 ASFID dimensions present
- ✅ **High Map Quality**: REVOI = (0.90, 0.85, 0.90, 0.90, 0.85)
- ✅ **Small Epistemic Gap**: δ = 0.132 — SpectralClass `OnCriticalLine` (excellent Territory-Map alignment)
- ✅ **Transdisciplinary**: 4-phase cycle pattern appears across domains
- ✅ **Pedagogical**: Universally taught in engineering education
- ✅ **Framework Validation**: Confirms TSCG applicability to thermodynamic systems
- ✅ **M1 CoreConcepts reuse**: `m1core:Oscillator` (crankshaft), `m1core:Processor` (engine as transformer)

**POCLET STATUS**: ✅ VALIDATED

---

## Changelog

| Version | Date | Summary |
|---------|------|---------|
| **1.2.0** | 2026-03-18 | M2 v15.10.1 alignment: Cycle→FeedbackLoop+Process, Sequence→Workflow, Flow→Channel, Synchronization→Alignment; Efficiency→M1_Thermodynamics; `@base` added to jsonld; GenericConceptCoverage 38%→27% (20/75); 8th M1 concept ThermalEfficiency added |
| 1.1.0 | 2026-02-24 | BREAKING: ORIVE → REVOI; R=Representability, E=Evolvability, V=Verifiability; ΔΘ recalculated to 0.132; poclet-loader fields added |
| 1.0.1 | 2026-01-28 | Added transdisciplinary validation and M1 contributions |

---

## References

- Otto, N. A. (1876). *Four-Stroke Internal Combustion Engine* (Patent)
- Heywood, J. B. (1988). *Internal Combustion Engine Fundamentals*. McGraw-Hill.
- Taylor, C. F. (1985). *The Internal Combustion Engine in Theory and Practice*. MIT Press.
- SAE International. *Engine Technology Standards* (J1349, J1995).

## Related Poclets

- **Fire Triangle**: Similar 3-component synergistic system
- **Carnot Cycle**: Idealized thermodynamic cycle (benchmark for efficiency)
- **Krebs Cycle**: Biological metabolic cycle with sequential phases
- **Predator-Prey**: Cyclical dynamics with phase coupling

---

**Document Version**: 1.2.0  
**Date**: March 2026  
**Framework**: TSCG (Transdisciplinary System Construction Game)  
**Authors**: Echopraxium with the collaboration of Claude AI  
**Ontology**: M0_FourStrokeEngine.jsonld  
