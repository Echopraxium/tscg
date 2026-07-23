# M3_EagleEye.jsonld

**Version:** 2.10.0  
**Layer:** M3  
**Type:** Territory Grammar (Gt)  
**Created:** 2026-01-21  
**Last Modified:** 2026-07-23
**Author:** Echopraxium with the collaboration of Claude AI

---

## 🎯 Role

**M3_EagleEye** defines the **Territory Grammar (Gt)** — the ontological/empirical
perspective of TSCG's bicephalous architecture. It formalizes the **ASFID** basis:

```
𝕋₀(×) = {A, St, F, It, D}

A (Attractor)  : Convergence points, stable states, equilibria
St (Structure) : Spatial/topological organisation
F (Flow)       : Movement, exchange, transport
It (Information): Encoded content, state complexity
D (Dynamics)   : Temporal evolution, change rate
```

**Metaphor:** The **Eagle Eye** provides panoramic vision of reality — seeing
systems **as they are** in the Territory.

---

## 📐 Territory Monoidal Product ×

**Territory structural product** (intra-ASFID):
```
×  :  Gt × Gt → Gt
```

**Example formulas:**
```
D × It × F =  Process        (temporal sequence with flow)
A × St × F =  Homeostasis    (stable regulation)
St × It × A =  Composition    (structural assembly)
F × T      =  Gradient       (× with bicephalous primitive T)
```

**Axioms:**
```
(A × B) × C  =  A × (B × C)   associativity
A × B        =  B × A          commutativity
A × EmptyTerritory  =  A       neutral element (Black)
```

---

## 🏗️ Architecture

```
M3_GrammarFoundation (apex)
         ↓ imported by
M3_EagleEye ← YOU ARE HERE
(Territory Grammar Gt, ASFID, ×)
         ↓ imported by
M3_GenesisGrammar
```

**Complementary grammars:**
- M3_SphinxEye.jsonld — Map Grammar Gm (REVOI, +)
- M3_BicephalousPerspective.jsonld — Stereopsis Grammar Gs (reification of synergy, |)

**Complete architecture:**
```
TSCG Bicephalous Architecture  =  Gt (Territory) + Gm (Map)
Gs (Stereopsis) = reification of their stereopsic synergy
```

---

## 🔗 Coupling with Map Grammar

Natural transformation **Φ** couples Territory to Map:
```
Φ : Gt → Gm   (observation: Territory measurements inform Map construction)
Ψ : Gm → Gt   (interpretation: Map predictions guide Territory measurement)
```

The Φ/Ψ enrichment loop between Gt and Gm produces the stereopsic synergy
formalized in Gs (M3_BicephalousPerspective.jsonld).

---

## ⚡ F — The Morphic Type

Flow (F) has a unique dual ontological nature in Gt:
```
F ∈ Ob(Cat_M3) ∩ Mor(Cat_M3)
```

F is both an **object** (like A, St, It, D — describes a state) and a
**morphism** (describes transitions between states). Any M2 structural
formula containing F inherits latent morphic capacity.

---

## 🦅 Eagle Metaphor

The eagle flies high above the territory, seeing vast landscapes with clarity:
- **Panoramic vision** — holistic system view
- **Sharp perception** — precise empirical measurement
- **Territory mapping** — what IS (ontological)

**Eagle = Territory = ASFID = What systems ARE**

---

## 📚 Key Takeaways

1. **Territory Grammar Gt** — ontological/empirical perspective
2. **ASFID primitives** — 5 irreducible generators 𝕋₀(×) = {A, St, F, It, D}
   (SC-2: `S`/`I` always subscripted; `A`/`F`/`D` bare)
3. **× operator** — structural product (replaces former ⊗ᵗ notation)
4. **EmptyTerritory** — neutral element of × (Black in symbolic grammar)
5. **Φ coupling** — natural transformation to Map Grammar
6. **F morphic** — only type with entity AND morphism nature

**The Eagle sees the Territory as it is.** 🦅

---

## 📋 Changelog

*(Derived from `owl:versionInfo` / `m3:changelog` in `M3_EagleEye.jsonld`.)*

| Version | Date | Changes |
|---|---|---|
| **2.10.0** | 2026-07-23 | **SC-2 STEP 2 — monoid qualification at the source.** `m3:typeSymbol` `S` → **`St`** (Structure/Territory) and `I` → **`It`** (Information/Territory), with matching `rdfs:label` updates and the alphabet listings `{A,S,F,I,D}` → `{A,St,F,It,D}`. Rationale (SC-1.2): `S` and `I` are the only ASFID letters that collide across monoids (`St`/`Ss`, `It`/`Im`), so they are **always** subscripted; `A`/`F`/`D` stay bare. Class `@id` values (`m3:eagle_eye:typeS`/`typeI`) are **unchanged** — only the symbol and labels move, so no cross-file reference breaks. **Also fixed (Map side)**: this file described Sphinx Eye's alphabet as `{R,E,V,O,I}` — the fifth REVOI primitive is `Im` (Interoperability), never a bare `I`; corrected to `{R,E,V,O,Im}`. Historical changelog entries left untouched. |
| **2.9.0** | 2026-07-23 | LAYERING FIX + CTX-4. `m2:changelog` → **`m3:changelog`** (defined in `M3_GrammarFoundation` 2.5.0): an M3 file must not reference an M2 property (dependency inversion), and the `m2` prefix was undeclared here (CTX-1), so the key resolved to an opaque `m2:` URI scheme. **CTX-4 fix (required, not cosmetic):** the `m3` prefix was *relative*; a relative prefix resolves against `@base` in IDENTIFIER position but NOT in PREDICATE position, so every `m3:*` property here expanded to an unresolved IRI while `m3:*` classes expanded correctly. Prefix made absolute. Data graph unchanged. |

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI*
