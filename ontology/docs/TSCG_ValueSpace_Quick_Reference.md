# TSCG ValueSpace Attributes: Quick Reference Card

**Version**: 14.4.0 | **Date**: 2026-02-05

---

## 11 Enriched Metaconcepts × 13 Attributes × 72 Values

### 1. Trajectory.shape (9 values)

| Value | When to Use | Example |
|-------|-------------|---------|
| **Linear** | Monotonic straight path | RAAS blood pressure convergence |
| **Circular** | Periodic return to start | Cardiac cycle, AC signal |
| **Elliptical** | Closed orbit with foci | Planetary orbit (Kepler) |
| **Spiral** | Converging/diverging helix | Damped oscillator to rest |
| **Hyperbolic** | Escape trajectory | Comet flyby (no return) |
| **Random** | Stochastic Brownian | Molecular diffusion |
| **Constrained** | On manifold/surface | Pendulum on arc, bead on wire |
| **Chaotic** | Deterministic but aperiodic | Lorenz attractor, weather |
| **Piecewise** | Distinct segments | Rocket stages, lifecycle |

**Default**: Linear  
**JSON**: `"shape": "Linear"`

---

### 2. Amplification.direction (3 values)

| Value | Formula | Example |
|-------|---------|---------|
| **Amplifying** | G > 1 | Op-amp (voltage ×100), RAAS cascade |
| **Attenuating** | 0 < G < 1 | Resistor divider, filter |
| **Unity** | G = 1 | Buffer amplifier (isolation) |

**Default**: Amplifying  
**JSON**: `"direction": "Amplifying"`

---

### 3. Regulation.feedback_polarity (3 values)

| Value | Behavior | Example |
|-------|----------|---------|
| **Negative** | Error-correcting, stabilizing | Thermostat, RAAS, PID controller |
| **Positive** | Self-amplifying, destabilizing | Chain reaction, viral spread |
| **Mixed** | Context-dependent switching | Schmitt trigger, bistable gene circuit |

**Default**: Negative (95% of control systems)  
**JSON**: `"feedback_polarity": "Negative"`

---

### 4. Regulation.control_type (9 values)

| Value | Formula | When to Use |
|-------|---------|-------------|
| **Proportional** | u = Kₚ·e | Simple biological systems, basic control |
| **Integral** | u = Kᵢ·∫e dt | Eliminate steady-state error |
| **Derivative** | u = Kd·de/dt | Anticipatory (rare alone) |
| **PI** | u = Kₚ·e + Kᵢ·∫e | Common practical control |
| **PD** | u = Kₚ·e + Kd·de/dt | Fast with damping |
| **PID** | Full 3-term | Industrial standard (95% of loops) |
| **Bang-bang** | On/off binary | Thermostat, simple switches |
| **Adaptive** | Self-tuning | Time-varying systems |
| **MPC** | Model predictive | Complex optimization |

**Default**: Proportional  
**JSON**: `"control_type": "PID"`

---

### 5. Process.time_discretization (3 values)

| Value | Description | Example |
|-------|-------------|---------|
| **Continuous** | dx/dt = f(x) | Chemical reactions, diffusion, biology |
| **Discrete** | x[n+1] = f(x[n]) | Digital control, generations, batches |
| **Hybrid** | Mixed continuous + discrete | Sampled-data systems, event-driven |

**Default**: Continuous  
**JSON**: `"time_discretization": "Continuous"`

---

### 6. Process.reversibility (3 values)

| Value | Thermodynamics | Example |
|-------|----------------|---------|
| **Reversible** | ΔS = 0 | Ideal elastic collision (idealization) |
| **Irreversible** | ΔS > 0 | Combustion, aging, RAAS (real processes) |
| **Quasi-reversible** | ΔS ≈ 0 | Very slow near-equilibrium (Carnot limit) |

**Default**: Irreversible (99% of real systems)  
**JSON**: `"reversibility": "Irreversible"`

---

### 7. Convergence.convergence_pattern (5 values)

| Value | Damping | Behavior | Example |
|-------|---------|----------|---------|
| **Monotonic** | ζ > 1 | No overshoot, smooth | RAAS, overdamped shock absorber |
| **Oscillatory** | 0 < ζ < 1 | Ringing, overshoot | Underdamped spring, RLC circuit |
| **Critical** | ζ = 1 | Fastest no-overshoot | Optimized control, car suspension |
| **Undamped** | ζ = 0 | Sustained oscillation | Ideal pendulum (no friction) |
| **Divergent** | ζ < 0 | Unstable (moves away) | Inverted pendulum, runaway |

**Default**: Monotonic  
**JSON**: `"convergence_pattern": "Monotonic"`

---

### 8. Bifurcation.bifurcation_type (7 values)

| Value | Characteristic | Example |
|-------|----------------|---------|
| **Saddle-node** | Creation/annihilation of equilibria | Tipping point (climate), catastrophe |
| **Transcritical** | Stability exchange | Laser threshold |
| **Pitchfork** | Symmetry breaking (1→3 eq.) | Euler buckling, ferromagnet |
| **Hopf** | Fixed point → limit cycle | Oscillation onset (heart arrhythmia) |
| **Period-doubling** | T → 2T (route to chaos) | Logistic map, dripping faucet |
| **Homoclinic** | Cycle → saddle collision | Shil'nikov chaos |
| **Heteroclinic** | Saddle → saddle connection | Lorenz attractor |

**Default**: Saddle-node  
**JSON**: `"bifurcation_type": "Hopf"`

---

### 9. Symmetry.symmetry_type (8 values)

| Value | Invariance | Conservation (Noether) | Example |
|-------|------------|------------------------|---------|
| **Translational** | x → x + a | Momentum | Crystal lattice, homogeneous space |
| **Rotational** | x → R(θ)·x | Angular momentum | Snowflake, circle, sphere |
| **Reflective** | x → -x | Parity | Bilateral animals, palindrome |
| **Temporal** | t → t + τ | Energy | Steady-state, autonomous system |
| **Scale** | x → λx | (Power law) | Fractal, critical phenomena |
| **Gauge** | ψ → e^(iα)ψ | Charge | EM (U(1)), weak force (SU(2)) |
| **Permutation** | Exchange particles | (Statistics) | Bosons, fermions |
| **Duality** | Strong ↔ weak | - | EM duality (E ↔ B) |

**Default**: Translational  
**JSON**: `"symmetry_type": "Rotational"`

---

### 10. Threshold.threshold_behavior (4 values)

| Value | Width | Reversibility | Example |
|-------|-------|---------------|---------|
| **Sharp** | Δx → 0 | Same threshold | Digital logic, neuron spike |
| **Smooth** | Finite | Same curve | Sigmoid, dose-response, RAAS receptor |
| **Hysteretic** | Loop | Different up/down | Schmitt trigger, ferromagnet |
| **Stochastic** | Noise-dependent | Probabilistic | Ion channel, thermal activation |

**Default**: Sharp  
**JSON**: `"threshold_behavior": "Smooth"`

---

### 11. Network.topology (8 values)

| Value | Degree Distribution | Example |
|-------|---------------------|---------|
| **Scale-free** | Power law P(k)~k^(-γ) | Internet, WWW, protein networks |
| **Small-world** | High clustering + short paths | Social networks, neural nets |
| **Random** | Poisson (Erdős-Rényi) | Null model, early universe |
| **Lattice** | Regular grid (constant k) | Crystal, image pixels, cellular automaton |
| **Hierarchical** | Nested modules | Organizations, taxonomy, bronchial tree |
| **Star** | Central hub + periphery | Client-server, hub airport |
| **Ring** | Circular (k=2) | Token ring, circular DNA |
| **Fully-connected** | Complete graph (k=N-1) | Mesh network, small group |

**Default**: Random  
**JSON**: `"topology": "Scale-free"`

---

### 12. Signal.signal_type (4 values)

| Value | Form | Example |
|-------|------|---------|
| **Analog** | s(t) ∈ ℝ, continuous | Voltage, sound, hormone concentration (RAAS) |
| **Digital** | s[n] ∈ {0,1,...,2^b-1} | Computer data, CD audio (16-bit) |
| **Discrete-event** | Event sequence {tᵢ} | Neuron spikes, photon counting, packets |
| **Hybrid** | Analog + digital mix | ADC/DAC, sampled-data control |

**Default**: Analog  
**JSON**: `"signal_type": "Analog"`

---

### 13. Gradient.gradient_type (6 values)

| Value | Formula | Example |
|-------|---------|---------|
| **Linear** | f(x) = mx + b | Temperature in rod, voltage across resistor |
| **Exponential** | f(x) = A·e^(kx) | Atmospheric pressure, radioactive decay |
| **Sigmoid** | f(x) = L/(1+e^(-k(x-x₀))) | Dose-response, RAAS receptor saturation |
| **Step** | f(x) = H(x-x₀) | Phase transition (1st order), digital threshold |
| **Power-law** | f(x) = A·x^n | Gravitational potential (1/r), diffusion |
| **Gaussian** | f(x) = A·e^(-(x-μ)²/2σ²) | Normal distribution, beam profile |

**Default**: Linear  
**JSON**: `"gradient_type": "Sigmoid"`

---

## Quick Decision Trees

### Choosing convergence_pattern

```
Does system overshoot target?
├─ No → Monotonic (smooth, no overshoot)
├─ Yes, decays → Oscillatory (ringing, damps down)
├─ Yes, fastest no-overshoot → Critical (optimal)
├─ Yes, sustained → Undamped (energy conserving)
└─ Moves away → Divergent (UNSTABLE!)
```

### Choosing feedback_polarity

```
After perturbation, error over time:
├─ Decreases → Negative (stabilizing, 95% of cases)
├─ Increases → Positive (amplifying, runaway)
└─ Depends on state → Mixed (bistable switch)
```

### Choosing signal_type

```
Is amplitude quantized?
├─ No (continuous) → Analog
└─ Yes (discrete)
    ├─ Regular sampling → Digital
    └─ Event timing → Discrete-event
```

---

## Usage Examples

### Biological System (RAAS)
```json
{
  "trajectory": {"shape": "Linear"},
  "amplification": {"direction": "Amplifying"},
  "regulation": {"feedback_polarity": "Negative", "control_type": "Proportional"},
  "process": {"time_discretization": "Continuous", "reversibility": "Irreversible"},
  "convergence": {"convergence_pattern": "Monotonic"},
  "threshold": {"threshold_behavior": "Smooth"},
  "signal": {"signal_type": "Analog"},
  "gradient": {"gradient_type": "Sigmoid"}
}
```

### Engineered Controller (PID)
```json
{
  "regulation": {"feedback_polarity": "Negative", "control_type": "PID"},
  "process": {"time_discretization": "Hybrid"},
  "convergence": {"convergence_pattern": "Critical"},
  "signal": {"signal_type": "Digital"}
}
```

### Network (Social)
```json
{
  "network": {"topology": "Scale-free"},
  "signal": {"signal_type": "Discrete-event"},
  "symmetry": {"symmetry_type": "Scale"}
}
```

---

## Validation Checklist

Before finalizing your instantiation:

- [ ] Attribute name spelled exactly as in M2?
- [ ] Value is from allowed `possibleValues`?
- [ ] Rationale provided for non-obvious choices?
- [ ] Only semantically relevant attributes included?
- [ ] Consistent (no contradictions across attributes)?

---

## Common Mistakes

❌ **Wrong**: `"reversible": true`  
✅ **Right**: `"reversibility": "Reversible"`

❌ **Wrong**: `"shape": "Curved"`  
✅ **Right**: `"shape": "Spiral"` (use valid value)

❌ **Wrong**: Using all 13 attributes for every system  
✅ **Right**: Use only relevant attributes

---

## Resources

- **Full ontology**: M2_MetaConcepts.jsonld (v14.4.0)
- **User guide**: TSCG_ValueSpace_User_Guide.md
- **Final report**: ValueSpace_Enrichment_Final_Report.md

---

**TSCG v14.4.0 - 2026-02-05**
