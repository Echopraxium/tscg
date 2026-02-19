# MetaconceptPair Notation — TSCG M2 Framework

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 15.3.3  
**Date:** 2026-02-18

---

## 1. Motivation

Several M2 metaconcepts have always been defined as **bidirectional pairs**: two named,
structurally opposed poles sharing a single base tensor formula. Examples include
`Composition/Decomposition`, `Convergence/Divergence`, `Activation/Inhibition`.

Before v15.3.3 these pairs were encoded inconsistently — the two pole formulas were
sometimes concatenated into a single string with a `/` separator
(e.g. `"S ⊗ I ⊗ A (composition) / S ⊗ I (decomposition)"`), which:

- prevented machine-readable access to individual pole formulas,
- mixed two semantically distinct formulas in one field,
- made the duality implicit rather than formal.

The `MetaconceptPair` class hierarchy introduced in v15.3.3 formalises this pattern
with a **parametric notation** inspired by mathematical conventions.

---

## 2. Class Hierarchy

```
m2:MetaConcept
  └── m2:MetaconceptPair          (abstract — all named-pole dual metaconcepts)
        ├── m2:DimensionPair      (operator: A^p — dimension present or absent)
        ├── m2:SignPair           (operator: (-1)^p — sign reversal)
        ├── m2:GainPair           (operator: G^{(-1)^p} — gain inversion, G > 1)
        └── m2:StructuralPair     (direction or cardinality reversal — no scalar p)
```

A metaconcept is a `MetaconceptPair` if and only if its two poles are:
- **named** (each pole has its own identity),
- **structurally opposed** (one is the formal inverse of the other),
- **sharing the same base tensor formula** (same ASFID dimensions).

> **Distinction from `m2:dualCounterpart`**: `dualCounterpart` links two *different*
> metaconcepts that share a parent but have distinct structures
> (e.g. `LALI ↔ ButterflyEffect`). They are *not* MetaconceptPairs.

---

## 3. JSON-LD Fields

Every `MetaconceptPair` entry adds the following fields alongside the standard
metaconcept fields:

| Field | Type | Description |
|---|---|---|
| `m2:expression` | `string` | Parametric formula unifying both poles — Unicode symbols (e.g. `S ⊗ I ⊗ A^{p}`) |
| `m2:expressionTeX` | `string` | LaTeX rendering of `m2:expression` |
| `m2:expressionASCII` | `string` | ASCII-safe rendering of `m2:expression` (e.g. `S (x) I (x) A^p`) |
| `m2:poleMapping` | `object` | Named poles with individual formulas and semantics |
| `m2:pairType` | `string` | For `StructuralPair` only: `"DirectionReversal"` or `"CardinalityReversal"` |

### `m2:hasTensorFormula` policy for MetaconceptPairs

For `DimensionPair` and `SignPair`, the three formula fields redirect explicitly
to their specific `expression` counterpart:

```
m2:hasTensorFormula     → "→ see m2:expression and m2:poleMapping"
m2:hasTensorFormulaTeX  → "→ see m2:expressionTeX and m2:poleMapping"
m2:hasTensorFormulaASCII→ "→ see m2:expressionASCII and m2:poleMapping"
```

| Subclass | `m2:hasTensorFormula*` | Authoritative source |
|---|---|---|
| `DimensionPair` | redirect string | `m2:expression` + `m2:expressionTeX` + `m2:expressionASCII` + `m2:poleMapping` |
| `SignPair` | redirect string | idem |
| `StructuralPair` | real formula (e.g. `"S ⊗ D"`) | `m2:poleMapping` (no `m2:expression`) |

The old approach of encoding both poles in `m2:hasTensorFormula` as a concatenated
string (e.g. `"-∇·D (convergence) / ∇·D (divergence)"`) is **deprecated**.
The `m2:expression*` + `m2:poleMapping` triplet is the single authoritative source.

### 3.1 DimensionPair — operator `A^{p}`

Used when the two poles differ by the **presence or absence of one ASFID dimension**.

```
p = 1  →  dimension A is present  (richer pole)
p = 0  →  A⁰ = 1  (neutral tensor element — dimension dissolved)
```

```json
{
  "@id": "m2:Composition",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept", "m2:MetaconceptPair", "m2:DimensionPair"],
  "m2:fullName": "Composition (Decomposition)",
  "m2:expression": "S ⊗ I ⊗ A^{p}",
  "m2:expressionTeX": "S \\otimes I \\otimes A^{p}",
  "m2:hasTensorFormula": "S ⊗ I ⊗ A",
  "m2:poleMapping": {
    "p=1": {
      "name": "Composition",
      "formula": "S ⊗ I ⊗ A",
      "semantics": "A present: assembly produces emergent property absent from parts alone"
    },
    "p=0": {
      "name": "Decomposition",
      "formula": "S ⊗ I",
      "semantics": "A⁰ = 1 (neutral tensor element): emergent property dissolves, parts recovered"
    }
  }
}
```

### 3.2 SignPair — operator `(-1)^{p}`

Used when the two poles differ by a **sign reversal** on the shared base formula.

```
p = 0  →  positive pole  (enabling, amplifying, constructive)
p = 1  →  negative pole  (inhibiting, attenuating, destructive)
```

```json
{
  "@id": "m2:Convergence",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept", "m2:MetaconceptPair", "m2:SignPair"],
  "m2:fullName": "Convergence (Divergence)",
  "m2:expression": "(-1)^{p} ∇·D",
  "m2:expressionTeX": "(-1)^{p} \\nabla \\cdot D",
  "m2:hasTensorFormula": "-∇·D (convergence) / ∇·D (divergence)",
  "m2:poleMapping": {
    "p=1": {
      "name": "Convergence",
      "formula": "-∇·D",
      "semantics": "Negative divergence: flows/trajectories focus toward attractor"
    },
    "p=0": {
      "name": "Divergence",
      "formula": "∇·D",
      "semantics": "Positive divergence: flows/trajectories disperse away from repeller"
    }
  }
}
```

### 3.3 StructuralPair — direction or cardinality reversal

Used when the duality **cannot be reduced to a scalar parametric operator** — the
difference is architectural (direction of mapping, or N:1 vs 1:N cardinality).
The `m2:expression` field is `null`; poles are described explicitly via `m2:poleMapping`
with `pole1` / `pole2` keys.

```json
{
  "@id": "m2:Fusion",
  "@type": ["owl:NamedIndividual", "m2:MetaConcept", "m2:MetaconceptPair", "m2:StructuralPair"],
  "m2:fullName": "Fusion (Fission)",
  "m2:expression": null,
  "m2:pairType": "CardinalityReversal",
  "m2:hasTensorFormula": "S ⊗ D",
  "m2:poleMapping": {
    "pole1": {
      "name": "Fusion",
      "formula": "{S₁ ⊗ ... ⊗ Sₙ} → S",
      "cardinality": "N:1",
      "semantics": "N distinct entities merge into one unified entity"
    },
    "pole2": {
      "name": "Fission",
      "formula": "S → {S₁ ⊗ ... ⊗ Sₙ}",
      "cardinality": "1:N",
      "semantics": "One entity splits into N distinct entities"
    }
  }
}
```

---

## 4. Catalogue of MetaconceptPairs (v15.3.3)

**Total: 8 MetaconceptPairs** — 1 DimensionPair, 4 SignPairs, 1 GainPair, 2 StructuralPairs.

### 4.1 DimensionPair (1)

#### Composition (Decomposition) — `m2:Structural`

| | |
|---|---|
| **Expression** | `S ⊗ I ⊗ A^{p}` |
| **p = 1** | **Composition** — `S ⊗ I ⊗ A` — assembly produces emergent property (A present) |
| **p = 0** | **Decomposition** — `S ⊗ I` — A⁰ = 1, emergent property dissolves |

The asymmetry is **ontological**: Composition *gains* A (justifies the assembly);
Decomposition *loses* A (no emergent property remains). This makes Composition
strictly irreversible in information terms.

---

### 4.2 SignPairs (4)

#### Convergence (Divergence) — `m2:Dynamic`

| | |
|---|---|
| **Expression** | `(-1)^{p} ∇·D` |
| **p = 1** | **Convergence** — `-∇·D` — flows focus toward attractor |
| **p = 0** | **Divergence** — `∇·D` — flows disperse away from repeller |

#### Activation (Inhibition) — `m2:Regulatory`

| | |
|---|---|
| **Expression** | `(-1)^{p} (A ⊗ D)` |
| **p = 0** | **Activation** — `+(A ⊗ D)` — positive gain: enables process, opens pathway |
| **p = 1** | **Inhibition** — `-(A ⊗ D)` — negative gain: blocks process, closes pathway |

#### Synergy (Positive / Negative) — `m2:Dynamic`

| | |
|---|---|
| **Expression** | `(-1)^{p} (I ⊗ D)` |
| **p = 0** | **Positive Synergy** — `+(I ⊗ D)` — combined effect > sum of parts: 1+1 > 2 |
| **p = 1** | **Negative Synergy** — `-(I ⊗ D)` — combined effect < sum of parts: 1+1 < 2 |

#### Feedback Loop (Negative / Positive) — `m2:Dynamic`

| | |
|---|---|
| **Expression** | `(-1)^{p} · k · (Process ⊗ Alignment ⊗ Homeostasis)` |
| **p = 1** | **Negative Feedback** — `-k · (…)` — k < 0, error-correcting, stabilising |
| **p = 0** | **Positive Feedback** — `+k · (…)` — k > 0, self-amplifying, destabilising |

---

### 4.3 GainPair (1)

#### Amplification (Attenuation) — `m2:Dynamic`

| | |
|---|---|
| **Expression** | `G^{(-1)^p} · (Ft → D → It → R → O)` |
| **p = 0** | **Amplification** — `G · (Ft → D → It → R → O)` — G > 1: output exceeds input |
| **p = 1** | **Attenuation** — `(1/G) · (Ft → D → It → R → O)` — 0 < 1/G < 1: output less than input |
| **neutral** | **Unity Gain** — `1 · (Ft → D → It → R → O)` — G = 1: neither pole |

**Why `GainPair`, not `SignPair`?** The two poles are not sign-symmetric
(`+F` vs `−F`) but reciprocal (`G·F` vs `(1/G)·F`). Gain is always strictly
positive — there is no "negative gain", only attenuation. The neutral element is
`G = 1` (unity), not `G = 0`. This structure requires a distinct class.

---

### 4.4 StructuralPairs (2)

#### Fusion (Fission) — `m2:Dynamic`

| | |
|---|---|
| **Pair type** | CardinalityReversal |
| **Base formula** | `S ⊗ D` |
| **pole1 — Fusion** | `{S₁ ⊗ ... ⊗ Sₙ} → S` — N:1 merge |
| **pole2 — Fission** | `S → {S₁ ⊗ ... ⊗ Sₙ}` — 1:N split |

#### Coding (Encoding / Decoding) — `m2:Informational`

| | |
|---|---|
| **Pair type** | DirectionReversal |
| **Base formula** | `I ⊗ S ⊗ D` |
| **pole1 — Encoding** | `I_source → I_coded` — source information → coded representation |
| **pole2 — Decoding** | `I_coded → I_source` — coded representation → source information |

---

## 5. What is NOT a MetaconceptPair

Several metaconcepts carry `m2:hasPolarity: "dual"` but are **not** `MetaconceptPair`
because their two aspects are not structurally opposed poles on a shared base formula:

| Metaconcept | Reason |
|---|---|
| `m2:Pattern` | Recognition + Reuse are **use modes** of the same concept, not opposing poles |
| `m2:Identity` | Persistence + Uniqueness are **co-present properties**, not opposing poles |
| `m2:Imbrication` | `S → S` is a deliberate **self-referential** formula (auto-application), not a pair |
| `m2:Cascade`, `m2:Behavior`, `m2:Workflow`, `m2:Step`, `m2:Action`, `m2:Processor`, `m2:Tropism` | `hasPolarity: "dual"` expresses a **Territory/Map perspective duality**, not named opposite poles |
| `m2:LocalActivationLateralInhibition`, `m2:ButterflyEffect` | Linked by `m2:dualCounterpart` — they share a parent (Amplification) but have **different structures** (`⊗⇒(Amplification, Regulation)` vs `⊗⇒(Amplification, Trajectory)`). By design decision, they are structural duals, not a MetaconceptPair. |

---

## 6. Parametric Convention Summary

| Subclass | Operator | p = 0 | p = 1 |
|---|---|---|---|
| `DimensionPair` | `A^{p}` | Dimension absent (A⁰ = 1) | Dimension present |
| `SignPair` | `(-1)^{p}` | Positive pole | Negative pole |
| `GainPair` | `G^{(-1)^p}` (G > 1) | Amplification (G > 1) | Attenuation (1/G < 1) |
| `StructuralPair` | *(none)* | `pole1` | `pole2` |

For `GainPair`, the neutral element is `G = 1` (unity gain) — it is neither pole and
does not correspond to any value of `p`. It is documented in `m2:poleMapping` under
the key `"neutral"` for completeness.

---

## 7. Querying MetaconceptPairs (SPARQL sketch)

```sparql
# All MetaconceptPairs with their type and expression
SELECT ?id ?type ?expression WHERE {
  ?id rdf:type m2:MetaconceptPair .
  ?id rdf:type ?type .
  OPTIONAL { ?id m2:expression ?expression }
  FILTER(?type IN (m2:DimensionPair, m2:SignPair, m2:StructuralPair))
}

# All SignPairs with their pole formulas
SELECT ?id ?pKey ?poleName ?poleFormula WHERE {
  ?id rdf:type m2:SignPair .
  ?id m2:poleMapping ?mapping .
  # (poleMapping entries accessed as nested objects)
}
```

---

## 8. Version History

| Version | Date | Change |
|---|---|---|
| 15.3.3 | 2026-02-18 | Introduction of `MetaconceptPair` class hierarchy. Classification of 7 pairs. |
| 15.3.4 | 2026-02-18 | For all `DimensionPair` and `SignPair`: `m2:hasTensorFormula*` replaced by redirect strings. |
| 15.3.5 | 2026-02-18 | Added `m2:expressionASCII` to all parametric pairs. Redirect strings now reference specific counterpart fields (`m2:expression`, `m2:expressionTeX`, `m2:expressionASCII`). |
| 15.3.6 | 2026-02-18 | Added `m2:GainPair` class: operator `G^{(-1)^p}` (G>1), distinct from `SignPair` (reciprocal inversion, not sign reversal). Classified `m2:Amplification` as `GainPair`. Total: 8 MetaconceptPairs. |
