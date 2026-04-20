# M0_IChing — I Ching (易經) as SymbolicSystemGrammar

**Ontology type:** `m3:SymbolicSystemGrammar`  
**File:** `instances/symbolic-grammars/M0_IChing.jsonld`  
**Version:** 1.1.0 · **Date:** 2026-02-20  
**Author:** Echopraxium with the collaboration of Claude AI  
**Status:** VALIDATED — First instance of `m3:SymbolicSystemGrammar` in the TSCG framework

---

## Overview

The I Ching (*Book of Changes*, 易經) is a ~3000-year-old Chinese philosophical and divinatory system. In TSCG terms it is the **canonical instance of `m3:SymbolicSystemGrammar`**: a system whose validity is determined by symbolic coherence and contextual pertinence — not by empirical verification or physical law.

Its power lies in a radical minimalism: **2 primitives** (Yin ⚋, Yang ⚊) generate **8 trigram archetypes** via a stacking rule, which in turn generate **64 hexagrams** via a second stacking rule. The resulting 6-bit binary space is exhaustive by construction — every possible combination is produced, no combination is missing. This property is formalized in TSCG as `m2:Representation.spaceCoverage = 1.0` (Generative Exhaustion).

| Property | Value |
|----------|-------|
| Grammar levels | 3 (primitive → trigram → hexagram) |
| Primitives | 2 (Yin ⚋, Yang ⚊) |
| Archetypes (trigrams) | 8 |
| Combinations (hexagrams) | 64 = 2⁶ = 8² |
| Space coverage (RSC) | **1.0** — exhaustive by construction |
| Dynamic mechanism | Changing lines (动爻) → hexagram transformation |
| ASFID mean | 0.85 |
| REVOI mean | 0.80 |
| Epistemic gap | 0.38 (intentional — enables interpretive multiplicity) |

---

## What distinguishes a SymbolicSystemGrammar from a Poclet?

A **Poclet** (`m3:Poclet`) models an observable real-world system and is validated by its ASFID dimensions (measurable territory). A **SymbolicSystemGrammar** (`m3:SymbolicSystemGrammar`) *is* the symbolic universe — it does not model an external system but generates a complete representation space within which any situation can be placed.

| Criterion | Poclet | SymbolicSystemGrammar |
|-----------|--------|-----------------------|
| Validation | Empirical (ASFID observable) | Symbolic arbitration |
| Truth criterion | Predictive accuracy | Coherence + contextual resonance |
| Interpretation | Unique (one correct reading) | Multiple legitimate readings |
| Epistemic gap | Low gap = quality | High gap = generative power |

The **epistemic gap of 0.38** is thus a feature, not a flaw: loose Territory→Map coupling enables the interpretive multiplicity that is the system's purpose. Maximum verifiability would collapse all readings to one — destroying what makes the I Ching valuable.

---

## Grammar Structure

The I Ching is a **3-level generative grammar**:

```
Level 0 — Primitives (alphabet)
  ⚊ Yang  (binary: 1)   — active, creative, undivided
  ⚋ Yin   (binary: 0)   — receptive, yielding, divided

        ↓ Rule 1: stack 3 primitives (bottom → middle → top)

Level 1 — Trigrams (archetypes)
  2³ = 8 named trigrams
  Each = a natural archetype with cosmological correspondences

        ↓ Rule 2: H = T_lower ⊗ T_upper (inner ⊗ outer)

Level 2 — Hexagrams (combinations)
  8² = 64 unique hexagrams
  = complete partition of {Yin, Yang}⁶ = 2⁶ binary space
```

**Binary isomorphism:** the 64 hexagrams are in bijection with the integers 0–63 (6-bit binary strings). Leibniz (1703) recognized this structure as a precursor of binary arithmetic.

---

## The 8 Trigram Archetypes

| Symbol | Chinese | Pinyin | English | Binary | Yang position | Archetype |
|--------|---------|--------|---------|--------|---------------|-----------|
| ☰ | 乾 | Qián | Heaven | `111` | pure yang | Creative force, initiation |
| ☷ | 坤 | Kūn | Earth | `000` | pure yin | Receptive sustenance, completion |
| ☳ | 震 | Zhèn | Thunder | `001` | yang below | Sudden awakening, shock |
| ☴ | 巽 | Xùn | Wind | `110` | yin below | Gradual penetration, gentleness |
| ☵ | 坎 | Kǎn | Water | `010` | yang center | Hidden strength in danger |
| ☲ | 離 | Lí | Fire | `101` | yin center | Radiance clinging to source |
| ☶ | 艮 | Gèn | Mountain | `100` | yang above | Stillness, deliberate pause |
| ☱ | 兌 | Duì | Lake | `011` | yin above | Joyous openness, exchange |

The 8 trigrams form **4 polar pairs** (binary complements):

| Pair | Codes | Principle |
|------|-------|-----------|
| ☰ Heaven / ☷ Earth | `111` / `000` | Creative force vs. receptive sustenance |
| ☳ Thunder / ☴ Wind | `001` / `110` | Sudden initiation vs. gradual penetration |
| ☵ Water / ☲ Fire | `010` / `101` | Hidden depth vs. brilliant surface |
| ☶ Mountain / ☱ Lake | `100` / `011` | Containing stillness vs. joyful openness |

---

## Hexagram Generation

The central grammar rule:

```
H(lower, upper) = T_lower ⊗ T_upper
```

- **Lower trigram** (lines 1–3): inner world, subjective situation, what is hidden
- **Upper trigram** (lines 4–6): outer world, objective situation, what is manifest
- **Asymmetry:** H(Tᵢ, Tⱼ) ≠ H(Tⱼ, Tᵢ) in general — inner/outer position carries semantic weight

### Selected canonical hexagrams

| # | Symbol | Name | Lower ⊗ Upper | Semantics |
|---|--------|------|---------------|-----------|
| 1 | ䷀ | 乾 The Creative | ☰ ⊗ ☰ | Pure yang — maximum creative force |
| 2 | ䷁ | 坤 The Receptive | ☷ ⊗ ☷ | Pure yin — maximum receptive sustenance |
| 11 | ䷊ | 泰 Peace | ☰ ⊗ ☷ | Heaven below, Earth above — forces flow toward each other |
| 12 | ䷋ | 否 Standstill | ☷ ⊗ ☰ | Earth below, Heaven above — forces retreat (inversion of #11) |
| 63 | ䷾ | 既濟 After Completion | ☲ ⊗ ☵ | Every line in correct position — rare perfect order |
| 64 | ䷿ | 未濟 Before Completion | ☵ ⊗ ☲ | Every line out of position — dynamic tension, creative incompletion |

> **Note on #63/#64:** The book ends with *Before Completion* — a profound structural statement: the cycle is never finished, only transformed. Incompletion is the generative principle.

---

## Dynamic Mechanism: Changing Lines (动爻)

The I Ching encodes dynamics through line polarity:

```
Young Yang (少陽) ——— stable, non-changing
Young Yin  (少陰) ——— stable, non-changing
Old Yang   (老陽) ×  → transforms into Young Yin
Old Yin    (老陰) ×  → transforms into Young Yang
```

Changing lines produce a **transformation trajectory**:

```
H_primary →(changing lines)→ H_derived
```

- `H_primary` = present situation
- `H_derived` = emerging future state
- TSCG mapping: δΘ(H_primary, H_derived) = epistemic gap between present Map and future Territory

The full dynamic state space:
- 64 hexagram nodes
- 64 × 64 = **4096 possible transitions** via changing-line combinations
- Non-deterministic: multiple changing lines possible per reading

---

## Semantic Layers

Each hexagram carries 4 interpretive layers:

| Layer | Chinese | Scope | Function |
|-------|---------|-------|----------|
| Judgment | 彖辞 Tuàn Cí | Whole hexagram | Overall oracular appraisal (King Wen, ~1000 BCE) |
| Image | 象辞 Xiàng Cí | Two-trigram natural scene | Metaphor guiding action |
| Line texts | 爻辞 Yáo Cí | Each of 6 lines | Fine-grained reading, activated by changing lines |
| Ten Wings | 十翼 Shí Yì | Entire canon | Confucian philosophical commentary (~500 BCE) |

---

## ASFID Analysis (Eagle Eye — Territory)

| Dimension | Score | Key finding |
|-----------|-------|-------------|
| **Attractor (A)** | 0.85 | 64 local attractors (hexagrams as named stable states). No global attractor — cyclical ergodicity: all 64 states reachable from any starting hexagram |
| **Structure (S)** | **0.97** | Highest score. 3-level strict hierarchy, binary isomorphism {0,1}⁶, 4 polar pairs, 3 structural symmetries (nuclear / inverse / reversed hexagram) |
| **Flow (F)** | 0.72 | Two flows: divinatory (coins/yarrow → hexagram, procedural) and transformative (H_primary → H_derived, symbolic) |
| **Information (I)** | 0.91 | 6 bits per hexagram (maximal Shannon entropy for 64 states), 4 semantic layers, ~18 interpretive channels per hexagram |
| **Dynamics (D)** | 0.80 | Line polarity dynamics (Young/Old inversion) + inter-hexagram dynamics (4096 transitions). Meta-dynamic: #64 encodes perpetual incompletion as generative principle |

---

## REVOI Analysis (Sphinx Eye — Map)

| Dimension | Score | Key finding |
|-----------|-------|-------------|
| **Representability (R)** | **0.95** | Exhaustive by construction: {Yin,Yang}⁶ = 64 = complete 6-bit space. Any situation mappable to one of 64 hexagrams; changing lines add temporal resolution |
| **Evolvability (E)** | 0.88 | Built-in evolution engine: changing lines generate the transformation vector at each reading. Grammar frozen since ~800 BCE; interpretive layers continuously evolving over 3000 years |
| **Verifiability (V)** | 0.50 | Deliberately low — the defining characteristic of symbolic arbitration. Formal grammar is perfectly verifiable (64 = 2⁶, provable). Oracular claims are not empirically falsifiable — this is a feature |
| **Observability (O)** | 0.78 | Structural observability HIGH (64 symbols enumerable, visually distinct). Interpretive observability MEDIUM. Outcome observability LOW |
| **Interoperability (I)** | **0.90** | Exceptional cross-domain reach: binary mathematics (Leibniz 1703), quantum complementarity (Bohr), Jungian archetypes (Jung 1949), Chinese medicine, cybernetics, chaos theory |

---

## M2 GenericConcept Activations

| GenericConcept | Dominance | Formula | Role in I Ching |
|-------------|-----------|---------|-----------------|
| `m2:Polarity` | **0.99** | `S ⊗ I ⊗ A` | Yin/Yang = archetypal N=2 generative complementarity; 4 polar trigram pairs |
| `m2:Signature` | **0.97** | `I ⊗ S` | Each hexagram = unique 6-bit situational signature; bijection with {0,1}⁶ |
| `m2:Composition` | **0.98** | `S ⊗ I` | Core grammar rule IS composition: H = T_lower ⊗ T_upper |
| `m2:Language` | 0.96 | `I ⊗ S ⊗ F` | Complete formal language: alphabet (2) + morphology (8) + syntax (64) + semantics (4 layers) |
| `m2:Hierarchy` | 0.95 | `S ⊗ A` | 3-level strict hierarchy; each level adds qualitatively new semantic content |
| `m2:Transformation` | 0.93 | `D ⊗ S ⊗ I` | Changing-line mechanism: formal transformation system H_primary → H_derived |
| `m2:Pattern` | 0.90 | `S → I → A` | 8 trigrams as universal pattern archetypes applicable across domains |
| `m2:FeedbackLoop` | 0.82 | `Process ⊗ Alignment` | Divination cycle: question → hexagram → reading → action → outcome → new question |

### RepresentationSpaceCoverage = 1.0

The I Ching is a primary instance of the `m2:Representation.spaceCoverage` ValueSpace attribute at its maximum value (introduced in M2_GenericConcepts v15.4.0):

```
m2:Representation.spaceCoverage = 1.0  (Generative Exhaustion)
```

The 64 hexagrams cover the entire 6-bit binary space — no hexagram is missing, no combination is unassigned. Completeness is structurally guaranteed by the grammar rule, not empirically observed.

This property is shared across unrelated domains (same RSC = 1.0):

| Domain | System | Space |
|--------|--------|-------|
| Symbolic divination | I Ching hexagrams | {Yin,Yang}⁶ = 64 |
| Molecular biology | DNA codon table | {A,T,G,C}³ = 64 |
| Music theory | Chromatic scale (equal temperament) | 12-tone octave closure |
| Logic / CS | NAND gate | All Boolean functions |

> The coincidence of **64** between the I Ching and the DNA codon table — achieved via completely different grammars (2 primitives × 6 levels vs. 4 primitives × 3 levels) — is a striking transdisciplinary validation of Generative Exhaustion as limit case of `spaceCoverage`.

---

## Candidate Reclassifications

Two candidate M2 GenericConcepts initially proposed from I Ching analysis were reclassified in v1.1.0:

| Candidate | Reclassification | Rationale |
|-----------|-----------------|-----------|
| **SymbolicArbitration** | Attribute of `m2:Observer` (`validationMode = symbolic`) | Describes how the Observer validates the Map — not a systemic phenomenon independent of Observer |
| **GenerativeExhaustion** | Special case `m2:Representation.spaceCoverage = 1.0` | The continuous range [0,1] is architecturally richer than a binary M2 GenericConcept |

---

## Bicephalous Synthesis

```
Territory strength (ASFID): 0.85
Map strength     (REVOI):   0.80
Epistemic gap    (δΘ):      0.38  ← intentional (enables interpretive multiplicity)
```

| Coupling | Score | Interpretation |
|----------|-------|----------------|
| S ⊗ R | 0.97 | Structural grammar is maximally representable |
| I ⊗ I | 0.91 | Information richness ↔ cross-domain interoperability |
| S ⊗ O | 0.88 | 64 hexagram symbols are visually distinct and enumerable |
| D ⊗ E | 0.84 | Changing-line dynamics well-served by built-in evolution mechanism |
| A ⊗ V | 0.55 | Attractors not empirically verifiable — intentional SSG feature |

---

## Validation

```
SSG Criterion 1 — Finite primitives:        ✅ VALIDATED  2 (Yin, Yang), irreducible and exhaustive
SSG Criterion 2 — Combination rules:        ✅ VALIDATED  2 deterministic rules: 3-stack → 8; 2-stack → 64
SSG Criterion 3 — Multiple interpretations: ✅ VALIDATED  4 semantic layers, 3000 years of commentary without consensus collapse
SSG Criterion 4 — Symbolic arbitration:     ✅ VALIDATED  Validity by coherence/resonance, never by empirical prediction

m2:Representation.spaceCoverage = 1.0:      ✅ VALIDATED  64 = {Yin,Yang}⁶ — bijection proven
```

---

## Contributions to the TSCG Framework

**M2 GenericConcepts validated:** Polarity, Composition, Hierarchy, Transformation, Signature, Language, Pattern, FeedbackLoop

**M2 layer enriched:** `m2:Representation.spaceCoverage` ValueSpace attribute (v15.4.0) — continuous [0.0, 1.0], special case RSC = 1.0 = Generative Exhaustion

**M1 mythology layer populated:**

| Concept | Definition |
|---------|------------|
| `m1:myth:YinLine` | Broken/divided line (⚋) — receptive primitive |
| `m1:myth:YangLine` | Undivided line (⚊) — active primitive |
| `m1:myth:Trigram` | 3-element symbolic archetype from {Yin,Yang}³ |
| `m1:myth:Hexagram` | 6-line situational composite from Trigram ⊗ Trigram |
| `m1:myth:ChangingLine` | Transformation marker (Old Yang/Yin) encoding situational vector |

---

## Files

| File | Description |
|------|-------------|
| `M0_IChing.jsonld` | Full ontology (58 graph entries) |
| `M0_IChing_README.md` | This document |

**Dependencies:**

```
M3_GenesisSpace.jsonld      (m3:SymbolicSystemGrammar type definition)
M2_GenericConcepts.jsonld      (M2 GenericConcepts + Representation.spaceCoverage v15.4.0)
M1_CoreConcepts.jsonld
M1_extensions/mythology/M1_Mythology.jsonld
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0.0 | 2026-02-20 | Initial release. Full grammar specification: 2 primitives, 8 trigram archetypes, 64 hexagram space, ASFID/REVOI analyses, 8 M2 activations, 2 M2 candidates |
| v1.1.0 | 2026-02-20 | Reclassified candidates: SymbolicArbitration → `m2:Observer.validationMode`; GenerativeExhaustion → `m2:Representation.spaceCoverage = 1.0`. Added spaceCoverage reference to m0:m2_composition |
