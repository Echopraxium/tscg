# TSCG User Guide: Working with ValueSpace Attributes
## Practical Guide for Instantiating Metaconcepts with Typed Attributes

**Version**: 1.0.0  
**Date**: 2026-02-05  
**Author**: Echopraxium with the collaboration of Claude AI  
**Target Audience**: TSCG users creating poclets (M0) or domain concepts (M1)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding ValueSpace Attributes](#understanding-valuespace-attributes)
3. [Available Attributes Reference](#available-attributes-reference)
4. [Instantiation Patterns](#instantiation-patterns)
5. [Complete Examples](#complete-examples)
6. [Templates](#templates)
7. [Common Pitfalls](#common-pitfalls)
8. [FAQs](#faqs)

---

## Quick Start

### What Are ValueSpace Attributes?

**ValueSpace attributes** allow you to configure metaconcepts without creating subtypes.

**Example**: Instead of creating `TrajectoryLinear`, `TrajectoryCircular`, etc., you use:

```json
{
  "@type": "m2:Trajectory",
  "shape": "Linear"  // ← attribute value
}
```

**Benefits**:
- ✅ Cleaner ontology (no subtype explosion)
- ✅ Easy to change (just modify attribute value)
- ✅ Well-documented (each value has description, examples)
- ✅ Validated (only allowed values accepted)

---

### 3-Step Workflow

#### Step 1: Choose Metaconcept

Identify which M2 metaconcept best describes your system component.

**Example**: RAAS blood pressure regulation → `m2:Regulation`

#### Step 2: Check Available Attributes

Look up which attributes that metaconcept has.

**Example**: `Regulation` has:
- `feedback_polarity` (Negative, Positive, Mixed)
- `control_type` (P, I, D, PI, PD, PID, Bang-bang, Adaptive, MPC)

#### Step 3: Select Appropriate Values

Choose the value that matches your system.

**Example**:
```json
{
  "@type": "m2:Regulation",
  "feedback_polarity": "Negative",  // Error-correcting
  "control_type": "Proportional"    // Simple biological response
}
```

---

## Understanding ValueSpace Attributes

### Attribute Anatomy

Each attribute is defined as a **ValueSpace** with:

```json
{
  "attribute_name": {
    "@type": "m2:ValueSpace",
    "m2:valueType": "Discrete symbolic",
    "m2:possibleValues": [
      {
        "value": "ValueName",
        "description": "What it means",
        "examples": ["Example 1", "Example 2"],
        "characteristics": "Key properties",
        // ... more metadata
      }
    ],
    "m2:default": "DefaultValue"
  }
}
```

### How to Use in Your Poclets/Concepts

**Simple syntax**:
```json
{
  "@id": "m0:MySystem",
  "@type": "m2:Metaconcept",
  "attribute_name": "ChosenValue"
}
```

**Full syntax** (with justification):
```json
{
  "@id": "m0:MySystem",
  "@type": "m2:Metaconcept",
  "attribute_name": "ChosenValue",
  "attribute_name_rationale": "Why I chose this value"
}
```

---

## Available Attributes Reference

### Complete List (13 Attributes)

| Metaconcept | Attribute | # Values | Quick Pick Guide |
|-------------|-----------|----------|------------------|
| **Trajectory** | shape | 9 | Linear (most common), Circular (periodic), Spiral (damped oscillation) |
| **Amplification** | direction | 3 | Amplifying (gain>1), Attenuating (gain<1), Unity (buffer) |
| **Regulation** | feedback_polarity | 3 | Negative (stabilizing, 95% of cases), Positive (runaway), Mixed (bistable) |
| **Regulation** | control_type | 9 | Proportional (simple), PID (industrial), Bang-bang (on/off) |
| **Process** | time_discretization | 3 | Continuous (physics/biology), Discrete (computer), Hybrid (sampled) |
| **Process** | reversibility | 3 | Irreversible (most real processes), Reversible (idealization) |
| **Convergence** | convergence_pattern | 5 | Monotonic (no overshoot), Oscillatory (ringing), Critical (optimal) |
| **Bifurcation** | bifurcation_type | 7 | Hopf (oscillation onset), Saddle-node (tipping point) |
| **Symmetry** | symmetry_type | 8 | Translational (space), Temporal (time), Rotational (circular) |
| **Threshold** | threshold_behavior | 4 | Smooth (biological), Sharp (digital), Hysteretic (memory) |
| **Network** | topology | 8 | Scale-free (hubs), Small-world (social), Hierarchical (organization) |
| **Signal** | signal_type | 4 | Analog (continuous), Digital (binary), Discrete-event (spikes) |
| **Gradient** | gradient_type | 6 | Linear (uniform), Sigmoid (saturation), Exponential (decay/growth) |

---

## Instantiation Patterns

### Pattern 1: Simple Attribute Assignment

**Use when**: Single metaconcept with one attribute

```json
{
  "@id": "m0:MyProcess",
  "@type": "m2:Process",
  "time_discretization": "Continuous"
}
```

---

### Pattern 2: Multiple Attributes (Same Metaconcept)

**Use when**: Metaconcept has multiple attributes (e.g., Regulation, Process)

```json
{
  "@id": "m0:MyRegulator",
  "@type": "m2:Regulation",
  "feedback_polarity": "Negative",
  "control_type": "PID"
}
```

---

### Pattern 3: Nested Components

**Use when**: System has multiple components with different attributes

```json
{
  "@id": "m0:MySystem",
  "@type": "m2:System",
  
  "regulation": {
    "@type": "m2:Regulation",
    "feedback_polarity": "Negative",
    "control_type": "Proportional"
  },
  
  "signal": {
    "@type": "m2:Signal",
    "signal_type": "Analog"
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Continuous",
    "reversibility": "Irreversible"
  }
}
```

---

### Pattern 4: With Rationale (Recommended)

**Use when**: Documenting design decisions

```json
{
  "@id": "m0:RAAS_Convergence",
  "@type": "m2:Convergence",
  "convergence_pattern": "Monotonic",
  "convergence_rationale": "Biological homeostasis typically exhibits smooth approach without overshoot to avoid stress on system"
}
```

---

### Pattern 5: Array of Instances

**Use when**: Multiple similar components with different attribute values

```json
{
  "@id": "m0:SignalProcessingPipeline",
  "stages": [
    {
      "@type": "m2:Amplification",
      "direction": "Amplifying",
      "stage_name": "Preamplifier",
      "gain": 10
    },
    {
      "@type": "m2:Amplification",
      "direction": "Attenuating",
      "stage_name": "Filter",
      "gain": 0.5
    },
    {
      "@type": "m2:Amplification",
      "direction": "Amplifying",
      "stage_name": "Power amplifier",
      "gain": 100
    }
  ]
}
```

---

## Complete Examples

### Example 1: RAAS (Biological Homeostasis)

**Full annotation** of Renin-Angiotensin-Aldosterone System:

```json
{
  "@id": "m0:RAAS_Complete",
  "@type": ["m2:Cascade", "m2:Homeostasis"],
  "rdfs:label": "Renin-Angiotensin-Aldosterone System",
  "rdfs:comment": "Hormonal cascade regulating blood pressure",
  
  "trajectory": {
    "@type": "m2:Trajectory",
    "shape": "Linear",
    "rationale": "Monotonic convergence toward BP setpoint"
  },
  
  "amplification": {
    "@type": "m2:Amplification",
    "direction": "Amplifying",
    "rationale": "Enzymatic cascade with gain at each stage"
  },
  
  "regulation": {
    "@type": "m2:Regulation",
    "feedback_polarity": "Negative",
    "control_type": "Proportional",
    "rationale": "Error-correcting homeostasis with proportional biological response"
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Continuous",
    "reversibility": "Irreversible",
    "rationale": "Enzymatic reactions in continuous time with heat dissipation"
  },
  
  "convergence": {
    "@type": "m2:Convergence",
    "convergence_pattern": "Monotonic",
    "rationale": "Smooth approach to setpoint without overshoot"
  },
  
  "threshold": {
    "baroreceptor": {
      "@type": "m2:Threshold",
      "threshold_behavior": "Smooth",
      "rationale": "Graded receptor response, not all-or-nothing"
    },
    "enzyme_activation": {
      "@type": "m2:Threshold",
      "threshold_behavior": "Smooth",
      "rationale": "Michaelis-Menten kinetics (sigmoid saturation)"
    }
  },
  
  "network": {
    "@type": "m2:Network",
    "topology": "Hierarchical",
    "rationale": "Kidney (sensor) → Cascade → Effectors (branching tree)"
  },
  
  "signal": {
    "@type": "m2:Signal",
    "signal_type": "Analog",
    "rationale": "Continuous hormone concentrations, not digital"
  },
  
  "gradient": {
    "@type": "m2:Gradient",
    "gradient_type": "Sigmoid",
    "rationale": "Receptor activation saturates at high [Ang II]"
  }
}
```

---

### Example 2: Thermostat (Engineering Control)

```json
{
  "@id": "m0:Thermostat",
  "@type": "m2:Regulation",
  "rdfs:label": "Home Heating Thermostat",
  
  "feedback_polarity": "Negative",
  "control_type": "Bang-bang",
  "rationale": "Simple on/off control (furnace fully on or off)",
  
  "threshold": {
    "@type": "m2:Threshold",
    "threshold_behavior": "Hysteretic",
    "rationale": "Different thresholds for heating on (20°C) vs off (22°C) to prevent chattering"
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Hybrid",
    "rationale": "Continuous temperature evolution, discrete furnace switching"
  },
  
  "convergence": {
    "@type": "m2:Convergence",
    "convergence_pattern": "Oscillatory",
    "rationale": "Bang-bang control causes limit cycle oscillation around setpoint"
  },
  
  "signal": {
    "temperature_sensor": {
      "@type": "m2:Signal",
      "signal_type": "Analog",
      "rationale": "Thermistor provides continuous voltage"
    },
    "furnace_control": {
      "@type": "m2:Signal",
      "signal_type": "Digital",
      "rationale": "Relay provides binary on/off"
    }
  }
}
```

---

### Example 3: Social Network (Complex System)

```json
{
  "@id": "m0:TwitterNetwork",
  "@type": "m2:Network",
  "rdfs:label": "Twitter Follow Network",
  
  "topology": "Scale-free",
  "rationale": "Few celebrities (hubs) with millions of followers, most users have few followers (power-law degree distribution)",
  
  "symmetry": {
    "@type": "m2:Symmetry",
    "symmetry_type": "Scale",
    "rationale": "Self-similar structure (looks same at different scales)"
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Discrete",
    "rationale": "Follow/unfollow events are discrete actions"
  },
  
  "signal": {
    "information_propagation": {
      "@type": "m2:Signal",
      "signal_type": "Discrete-event",
      "rationale": "Tweets are discrete events, retweets propagate asynchronously"
    }
  },
  
  "amplification": {
    "@type": "m2:Amplification",
    "direction": "Amplifying",
    "rationale": "Viral tweets amplify exponentially through retweets"
  }
}
```

---

### Example 4: Pendulum (Physical System)

```json
{
  "@id": "m0:DampedPendulum",
  "@type": ["m2:Process", "m2:Trajectory"],
  "rdfs:label": "Damped Pendulum",
  
  "trajectory": {
    "@type": "m2:Trajectory",
    "shape": "Spiral",
    "rationale": "Inward spiral toward equilibrium due to damping"
  },
  
  "convergence": {
    "@type": "m2:Convergence",
    "convergence_pattern": "Oscillatory",
    "rationale": "Underdamped system oscillates with decaying amplitude"
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Continuous",
    "reversibility": "Irreversible",
    "rationale": "Friction dissipates energy (entropy increases)"
  },
  
  "symmetry": {
    "@type": "m2:Symmetry",
    "symmetry_type": "Rotational",
    "rationale": "Circular motion (before damping dominates)"
  },
  
  "bifurcation": {
    "@type": "m2:Bifurcation",
    "bifurcation_type": "Hopf",
    "condition": "If energy input (e.g., periodic forcing) added, can transition from fixed point to limit cycle"
  }
}
```

---

## Templates

### Template 1: Biological Process

```json
{
  "@id": "m0:YourBiologicalProcess",
  "@type": "m2:Process",
  "rdfs:label": "Your Process Name",
  
  "time_discretization": "Continuous",  // Biology is usually continuous
  "reversibility": "Irreversible",      // Biology is thermodynamically irreversible
  
  "signal": {
    "@type": "m2:Signal",
    "signal_type": "Analog"             // Hormone/neurotransmitter concentrations
  },
  
  "threshold": {
    "@type": "m2:Threshold",
    "threshold_behavior": "Smooth"      // Biological receptors are graded
  }
}
```

---

### Template 2: Control System

```json
{
  "@id": "m0:YourController",
  "@type": "m2:Regulation",
  "rdfs:label": "Your Controller Name",
  
  "feedback_polarity": "Negative",     // Most control is stabilizing
  "control_type": "PID",               // Industrial standard
  
  "convergence": {
    "@type": "m2:Convergence",
    "convergence_pattern": "Oscillatory"  // PID often has slight overshoot
  },
  
  "signal": {
    "sensor": {
      "@type": "m2:Signal",
      "signal_type": "Analog"
    },
    "controller": {
      "@type": "m2:Signal",
      "signal_type": "Digital"          // Microcontroller
    }
  }
}
```

---

### Template 3: Network/Graph

```json
{
  "@id": "m0:YourNetwork",
  "@type": "m2:Network",
  "rdfs:label": "Your Network Name",
  
  "topology": "Scale-free",  // or Small-world, Hierarchical, Random, etc.
  
  "signal": {
    "@type": "m2:Signal",
    "signal_type": "Discrete-event"  // Messages/packets
  },
  
  "process": {
    "@type": "m2:Process",
    "time_discretization": "Discrete"  // Event-driven
  }
}
```

---

## Common Pitfalls

### ❌ Pitfall 1: Using Invalid Values

**Wrong**:
```json
{
  "@type": "m2:Trajectory",
  "shape": "Curved"  // ❌ Not a valid value!
}
```

**Right**:
```json
{
  "@type": "m2:Trajectory",
  "shape": "Spiral"  // ✅ Valid value from ValueSpace
}
```

**Solution**: Always check `m2:possibleValues` in M2_MetaConcepts.jsonld

---

### ❌ Pitfall 2: Mixing Up Similar Attributes

**Wrong**:
```json
{
  "@type": "m2:Process",
  "reversible": true  // ❌ Attribute is 'reversibility', not 'reversible'
}
```

**Right**:
```json
{
  "@type": "m2:Process",
  "reversibility": "Reversible"  // ✅ Correct attribute name and value
}
```

**Solution**: Use exact attribute names from documentation

---

### ❌ Pitfall 3: Not Providing Rationale

**Weak**:
```json
{
  "@type": "m2:Convergence",
  "convergence_pattern": "Monotonic"
}
```

**Strong**:
```json
{
  "@type": "m2:Convergence",
  "convergence_pattern": "Monotonic",
  "convergence_rationale": "Biological homeostasis avoids overshoot to minimize stress"
}
```

**Solution**: Always explain your choices (helps others understand your design)

---

### ❌ Pitfall 4: Over-Specifying

**Too much**:
```json
{
  "@type": "m2:Process",
  "time_discretization": "Continuous",
  "reversibility": "Irreversible",
  "trajectory": {...},
  "convergence": {...},
  "bifurcation": {...},
  "symmetry": {...}
  // ❌ Not every attribute is relevant for every system!
}
```

**Just right**:
```json
{
  "@type": "m2:Process",
  "time_discretization": "Continuous",
  "reversibility": "Irreversible"
  // ✅ Only attributes that matter for this specific process
}
```

**Solution**: Only use attributes that are **semantically relevant** to your system

---

## FAQs

### Q1: Do I have to use all available attributes?

**No.** Only use attributes that are relevant to your system.

**Example**: For a simple biological process, you might only specify:
- `time_discretization`: Continuous
- `reversibility`: Irreversible

Skip attributes like `bifurcation_type` unless your system exhibits bifurcations.

---

### Q2: Can I add custom attributes?

**In M0 poclets**: Yes, you can add domain-specific properties alongside standard attributes.

**Example**:
```json
{
  "@type": "m2:Process",
  "time_discretization": "Continuous",
  "custom:enzymeType": "Serine protease"  // Custom property
}
```

**In M2 metaconcepts**: No, only through formal TSCG extension process.

---

### Q3: What if my system doesn't fit any value?

**Options**:
1. Choose closest value and document deviation in rationale
2. Propose new value (file issue/request)
3. Use custom property for now

**Example**:
```json
{
  "@type": "m2:Convergence",
  "convergence_pattern": "Oscillatory",  // Closest match
  "convergence_note": "Actually quasi-periodic (not exactly oscillatory)"
}
```

---

### Q4: How do I know which attributes a metaconcept has?

**Method 1**: Check M2_MetaConcepts.jsonld directly

**Method 2**: Use this quick reference:

| Metaconcept | Has Attributes? | Which Ones? |
|-------------|-----------------|-------------|
| Trajectory | ✅ | shape |
| Amplification | ✅ | direction |
| Regulation | ✅ | feedback_polarity, control_type |
| Process | ✅ | time_discretization, reversibility |
| Convergence | ✅ | convergence_pattern |
| Bifurcation | ✅ | bifurcation_type |
| Symmetry | ✅ | symmetry_type |
| Threshold | ✅ | threshold_behavior |
| Network | ✅ | topology |
| Signal | ✅ | signal_type |
| Gradient | ✅ | gradient_type |
| Others | ❌ | (Not yet enriched) |

---

### Q5: Can values change over time?

**Yes**, for dynamic systems you can specify temporal evolution:

```json
{
  "@id": "m0:AdaptiveController",
  "@type": "m2:Regulation",
  "control_type": "Adaptive",
  "control_evolution": {
    "t0": {"control_type": "Proportional"},
    "t1": {"control_type": "PI"},
    "t2": {"control_type": "PID"}
  }
}
```

---

### Q6: What's the difference between attribute and property?

**Attribute** (ValueSpace):
- Predefined discrete values
- Documented with examples
- Type-checked against allowed values

**Property** (regular):
- Arbitrary values
- Domain-specific
- Not constrained

**Example**:
```json
{
  "convergence_pattern": "Monotonic",  // ← Attribute (from ValueSpace)
  "convergence_rate": 0.05            // ← Property (numerical, domain-specific)
}
```

---

## Best Practices Summary

### ✅ DO

1. **Use attributes** when available (instead of creating subtypes)
2. **Provide rationale** for non-obvious choices
3. **Be selective** (only use relevant attributes)
4. **Check valid values** before using
5. **Document deviations** if system doesn't fit perfectly

### ❌ DON'T

1. **Don't invent values** (stick to predefined ValueSpace)
2. **Don't over-specify** (not every attribute is always relevant)
3. **Don't use wrong attribute names** (check spelling exactly)
4. **Don't skip rationale** for complex systems
5. **Don't mix attributes and properties** without clarity

---

## Conclusion

**ValueSpace attributes** provide a powerful, clean way to configure TSCG metaconcepts without ontology proliferation.

**Key Takeaways**:
- 13 attributes available across 11 metaconcepts
- 72 validated discrete values
- Use only what's relevant to your system
- Always provide rationale for design decisions
- Check M2_MetaConcepts.jsonld for authoritative reference

**Happy modeling!** 🎯

---

**End of Guide**

*Version 1.0.0 - 2026-02-05*
