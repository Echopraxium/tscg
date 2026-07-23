# M3_SphinxEye.jsonld

**Version:** 3.6.0  
**Layer:** M3  
**Type:** Map Grammar (Gm)  
**Created:** 2026-01-21  
**Last Modified:** 2026-07-23
**Author:** Echopraxium with the collaboration of Claude AI

---

## 🎯 Role

**M3_SphinxEye** defines the **Map Grammar (Gm)** — the epistemic/representational
perspective of TSCG's bicephalous architecture. It formalizes the **REVOI** basis:

```
𝕋₀(+) = {R, E, V, O, Im}

R (Representable)  : Semantic decodability — can it be encoded/named?
E (Evolvable)      : Generativity — does the Map create novel predictions?
V (Verifiable)     : Testability — can Map predictions be checked against Territory?
O (Observable)     : Measurability — can the phenomenon be detected?
Im (Interoperable) : Compatibility — can the Map interface with other Maps/systems?
```

**Metaphor:** The **Sphinx Eye** poses riddles that construct understanding —
seeing systems as **representations** in the Map.

> ⚠️ **R = Representability** (semantic decodability) — never Reproducibility.

---

## 📐 Map Structural Sum +

**Map structural sum** (intra-REVOI):
```
+  :  Gm × Gm → Gm
```

**Example formulas:**
```
R + E          =  ModelQuality   (representable and evolvable model)
O + R + Im + E =  Context        (epistemic frame)
V + E          =  Invariant      (verifiable and evolvable property)
```

**Axioms:**
```
(R + E) + V  =  R + (E + V)    associativity
R + E        =  E + R           commutativity
R + EmptyMap  =  R              neutral element (Empty pentagon)
```

---

## 🏗️ Architecture

```
M3_GrammarFoundation (apex)
         ↓ imported by
M3_SphinxEye ← YOU ARE HERE
(Map Grammar Gm, REVOI, +)
         ↓ imported by
M3_GenesisGrammar
```

**Complementary grammars:**
- M3_EagleEye.jsonld — Territory Grammar Gt (ASFID, ×)
- M3_BicephalousPerspective.jsonld — Stereopsis Grammar Gs (reification of synergy, |)

**Complete architecture:**
```
TSCG Bicephalous Architecture  =  Gt (Territory) + Gm (Map)
Gs (Stereopsis) = reification of their stereopsic synergy
```

---

## 🔗 Coupling with Territory Grammar

Natural transformation **Ψ** couples Map to Territory:
```
Φ : Gt → Gm   (observation: Territory measurements inform Map construction)
Ψ : Gm → Gt   (interpretation: Map predictions guide Territory measurement)
```

The Φ/Ψ enrichment loop between Gm and Gt produces the stereopsic synergy
formalized in Gs (M3_BicephalousPerspective.jsonld).

---

## 📐 REVOI Types

| Dim | Full name | Adjective form | Epistemic role |
|---|---|---|---|
| R | Representability | Representable | Can it be encoded? |
| E | Evolvability | Evolvable | Does it generate novelty? |
| V | Verifiability | Verifiable | Can it be tested? |
| O | Observability | Observable | Can it be measured? |
| Im | Interoperability | Interoperable | Can it interface? |

**Grammatical form:** Adjectives ending in *-able* — simplified from
abstract nouns (*-ility*) in v3.0.0 for consistency.

---

## 🦁 Sphinx Metaphor

The Sphinx poses riddles at the crossroads, constructing understanding:
- **Enigmatic wisdom** — epistemic construction
- **Participatory view** — from within the system
- **Map building** — how we REPRESENT (epistemic)

**Sphinx = Map = REVOI = How models QUALIFY**

---

## 📚 Key Takeaways

1. **Map Grammar Gm** — epistemic/representational perspective
2. **REVOI primitives** — 5 irreducible generators 𝕋₀(+)
3. **+ operator** — structural sum (replaces former ⊗ᵐ notation)
4. **EmptyMap** — neutral element of + (Empty pentagon in symbolic grammar)
5. **Ψ coupling** — natural transformation to Territory Grammar
6. **R = Representability** — never Reproducibility (critical invariant)

**The Sphinx constructs the Map through enigmatic wisdom.** 🦁

---

## 📋 Changelog

*(Derived from `owl:versionInfo` / `m3:changelog` in `M3_SphinxEye.jsonld`.)*

| Version | Date | Changes |
|---|---|---|
| **3.6.0** | 2026-07-23 | LAYERING FIX + CTX-4. `m2:changelog` → **`m3:changelog`** (defined in `M3_GrammarFoundation` 2.5.0): an M3 file must not reference an M2 property (dependency inversion), and the `m2` prefix was undeclared here (CTX-1), so the key resolved to an opaque `m2:` URI scheme. **CTX-4 fix (required, not cosmetic):** the `m3` prefix was *relative*; a relative prefix resolves against `@base` in IDENTIFIER position but NOT in PREDICATE position, so every `m3:*` property here expanded to an unresolved IRI while `m3:*` classes expanded correctly. Prefix made absolute. Data graph unchanged. |

---

*TSCG Framework — Echopraxium with the collaboration of Claude AI*
