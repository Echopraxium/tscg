# M3_BicephalousPerspective.jsonld

**Version:** 1.2.0  
**Layer:** M3  
**Type:** Stereopsis Grammar (Gs) — Reification of stereopsic synergy  
**Created:** 2026-05-18  
**Last Modified:** 2026-05-27

---

## 🎯 Role

**M3_Stereopsis** is the **reification of stereopsis** — the formal algebraic
structure that emerges from the mutual enrichment loop (Φ/Ψ) between Territory
Grammar Gt (Eagle Eye) and Map Grammar Gm (Sphinx Eye).

```
Stereopsis = the depth perception born from binocular fusion
           = what the two TSCG eyes create together
           = formally: the bicephalous monoid (Gs, |, EmptyStereopsis)
```

**Key insight:** The bicephalous architecture (Eagle Eye + Sphinx Eye) remains
the foundational metaphor — two eyes, two perspectives. Stereopsis is the
**synergy** that emerges from their fusion. Gs **reifies** that synergy as a
first-class algebraic structure with its own operator (|), neutral element
(EmptyStereopsis), and **Base16 primitive alphabet** — 6 primitives:
`{T, _^, _$, K, Ss, L}` (acronym: **TKSL** for the 4 nominal primitives + poles).

---

## 📐 Stereopsis Grammar Gs — Base16

**Bicephalous monoidal operator | :**
```
|  :  (Gt ∪ Gm ∪ Gs)_expr × (Gt ∪ Gm ∪ Gs)_expr  →  Gs_expr
```

| operates universally across all three grammars, always producing
a bicephalous (Gs) type expression.

**𝕋₀(|) = {T, _^, _$, K, Ss, L} — 6 primitives (Base16)**

| Idx | Symbol | Name | Question | Role |
|---|---|---|---|---|
| 0 | **T** | Temporality | When? | Temporal interface Gt↔Gm |
| 1 | **_^** | PositivePole | *(polarity)* | Onset/amplifying modifier |
| 2 | **_$** | NegativePole | *(polarity)* | Terminus/attenuating modifier |
| 3 | **K** | Knowledge | What? | Cognitive contextualisation of It |
| 4 | **Ss** | Symbol *(Stereopsic)* | Sign? | Semiotic bridge signifier↔signified |
| 5 | **L** | Localizability | Converging? | Cybernetic convergence toward A |

**TKSL acronym** — the 4 nominal Gs primitives (T, K, Ss, L). The poles _^/_$
are polarity modifiers and not included in the acronym.

**Example formulas (updated with St/It/O indexation):**
```
A × St × It | R + O | _^  =  Coherence      (bicephalous + positive pole)
F × T                      =  Gradient        (Territory × Gs primitive T)
It | V + O + R + Im       =  ValueSpace      (Territory | Map)
St × It | L                =  Node/Component  (structure+info, converging)
It × Ss                    =  Code            (information encoded as symbol)
Ss × F | K                 =  Language        (symbol-flow in knowledge context)
A × St × F | L             =  Homeostasis     (attractor+structure+flow, converging)
```

**Neutral element:** `m3:bicephalous:StereopsisEmptySet = EmptyTerritory | EmptyMap`

---

## 🔭 T — First Primitive of Gs (Temporality)

**T (Temporality)** is the first primitive of 𝕋₀(|):

```
𝕋₀(|) = {T, _^, _$, K, Ss, L}   ← Base16 alphabet
```

### T is irreducible

T cannot be derived from ASFID or REVOI primitives — it is a genuinely new
ontological category. Like A (Attractor) in Gt which is not defined by other
ASFID types, T is primitive and manifests in different contexts:

```
F | Im   →  manifestation of T in Territory/Map context
             (flux temporality seen through interoperability lens)
D | Im   →  manifestation of T in Territory/Map context
             (dynamic temporality seen through interoperability lens)
```

**F|Im and D|Im are manifestations of T, not its definition.**

### T semantic definition

> Pure Temporality — the temporal interface that emerges from the fusion
> of Territory time (as flow/evolution: F, D) and Map time (as
> synchronisation/interoperability: Im). T captures what is relational
> in time — not what a system does in time (F, D) nor how a model
> qualifies time (Im) but how Territory and Map *correspond* temporally.

### T in practice

| Domain | T manifestation |
|---|---|
| Music | Rhythm — temporal interface between sound flux (F) and listener synchronisation (Im) |
| Digital circuits | Clock signal — coordination between data flow (F) and system interoperability (Im) |
| Biology | Circadian rhythm — temporal binding between metabolic dynamics (D) and inter-cellular synchronisation (Im) |
| Distributed systems | Consensus timing — alignment between state evolution (D) and node interoperability (Im) |

---

## 🧠 K — Knowledge (idx 3)

**K (Knowledge)** is the cognitive interface primitive of 𝕋₀(|):

> Contextualisation of raw Information (It, Territory) into meaning.
> K is the act that transforms It into something a Map can interpret.

### K is irreducible

K cannot be derived from It (Territory) nor from R/E (Map):
- `It` = raw data, signal, information as observed
- `R` = representability quality of the Map
- `K` = the cognitive bridge that makes It *meaningful* within a Map context

### K semantic definition

> Pure Knowledge Interface — the cognitive act that contextualises Territory
> information (It) into Map-interpretable meaning. Not the information itself
> (It) nor its representational quality (R/E), but how observation becomes
> understanding.

*Theoretical basis: Maturana/Varela (cognition as enaction), Husserl (intentionality),
Peirce (interpretant — the meaning produced in a mind by a sign).*

### K in practice

| Domain | K manifestation |
|---|---|
| Immune system | Antigen recognition — molecular It → 'self/non-self' K |
| Natural language | Tokenisation — raw signal It → semantic unit K |
| Science | Paradigm (Kuhn) — raw observations It → theory-laden K |
| Medicine | Diagnosis — symptom It → clinical meaning K in nosological frame |
| Music | Melodic perception — sound waves It → pattern K in tonal context |
| Law | Interpretation — statute text It → legal meaning K in jurisdictional context |

---

## 🔣 Ss — Symbol / Stereopsic (idx 4)

**Ss (Symbol)** is the semiotic interface primitive of 𝕋₀(|):

> The sign-relation between signifier (Territory/Gt) and signified (Map/Gm).
> Ss formalises the Peircean sign at the M3 level.

**Notation disambiguation:** `Ss` (subscript s = Stereopsic) vs `St` (subscript t =
Territory/Structure). In hybrid formulas containing `|`, always use `St` for Structure
and `Ss` for Symbol. In pure intra-Territory formulas, `S` remains unindexed (ASFID).

### Ss is irreducible

- `St` (Territory Structure) = physical/structural organisation
- `R` (Map Representability) = representational quality
- `Ss` = neither — it is the semiotic convention that makes St *carry* Gm meaning

### Ss semantic definition

> Pure Semiotic Interface — the sign-relation between a Territory signifier
> and a Map signified. Not the structure (St) nor the representation (R),
> but the conventional bond that makes one stand for the other.

*Theoretical basis: Peirce (sign = signifier + signified + interpretant),
Saussure (signifier/signified — arbitrary but systematic), Eco (semiotics of culture).*

### Ss in practice

| Domain | Ss manifestation |
|---|---|
| Natural language | Words (St signifiers) ↔ concepts (Gm signified) |
| DNA | Codons (St) ↔ amino acids (Gm) — biochemical semiosis |
| Mathematics | Symbols (St) ↔ mathematical objects (Gm) |
| Music | Notation (St) ↔ sonic events (Gm) — semiotic convention |
| Traffic | Signs (St) ↔ traffic rules (Gm) — social convention |
| Computing | Tokens (St) ↔ computational operations (Gm) |

---

## 📍 L — Localizability (idx 5)

**L (Localizability)** is the cybernetic interface primitive of 𝕋₀(|):

> Ordinal discrimination of convergence direction toward an Attractor (A)
> by successive state comparison. **No metric required** — purely ordinal:
> closer / farther, not *how much* closer.

### L is irreducible

- `A` (Territory Attractor) = the goal/equilibrium state
- `V` (Map Verifiability) = quality of model verification
- `L` = neither — it is the cybernetic comparison that tests
  whether the current trajectory is converging or diverging relative to A

### L semantic definition

> Pure Localizability Interface — ordinal convergence discrimination.
> Answers "Is the current state trajectory approaching the Attractor?"
> without requiring a distance metric. Based on successive state comparison
> (Wiener 1948 negative feedback; Ashby 1956 regulation principle).

**Rejected names:** *Groundedness* (Hilbert-space trap), *Origin* (implies metric).

*Theoretical basis: Wiener (1948) Cybernetics, Ashby (1956) Introduction to Cybernetics,
Conant & Ashby (1970) Every Good Regulator must be a Model of the System.*

### L in practice

| Domain | L manifestation |
|---|---|
| Thermostat | Temperature vs setpoint — converging/diverging, no metric |
| Immune response | Inflammation → homeostasis A — ordinal, not quantified |
| Evolution | Population trajectory → fitness peak A |
| Navigation | Bearing correction → destination A without exact distance |
| Economics | Wicksell rate — convergence toward equilibrium, no exact measure |
| Neural RL | Reward signal — converging toward policy optimum A |

---

## 📏 Notation Convention — St / It / O in Hybrid Formulas

**Rule:** In any formula containing `|`, Territory and Map types carry their monoid
index to prevent ambiguity with new Gs type `Ss`:

```
In hybrid formulas (with |):
  S  →  St   (Structure/Territory — subscript t)
  I  →  It   (Information/Territory — subscript t)
  O  →  O   (Observability/Map — subscript t... wait: O = Observability/Map, subscript m)

Examples:
  A × St × It × D | V        ✅  (was: A × S × I × D | V)
  St × F × It | Im           ✅  (was: S × F × I | Im)
  A × St × F × It × D | R+V  ✅  (was: A × S × F × I × D | R+V)

Pure Territory (no |):
  A × S × F                  ✅  (unchanged — ASFID unaffected)
  D × I × F                  ✅  (unchanged)
```

This convention is **backward-compatible**: scoring (ASFID/REVOI), pure intra-monoid
formulas, and instance files are all unaffected.

---

## 🏗️ Architecture

```
M3_GrammarFoundation (apex)
         ↓ imported by
    ┌────┴────────────────┐
    │                     │
M3_EagleEye         M3_SphinxEye
(Gt/×, ASFID)      (Gm/+, REVOI)
    │                     │
    └──────────┬──────────┘
               ↓ both imported by
M3_BicephalousPerspective ← YOU ARE HERE
(Gs/|, TKSL={T,K,Ss,L} + poles _^/_$)
               ↓ imported by
M3_GenesisGrammar
```

---

## 🌀 Special Elements of |

| Element | Role | Metaphor | δ₁ |
|---|---|---|---|
| `EmptyStereopsis` | Neutral of \| | **Divergent Strabismus** — both eyes diverge, no fusion possible | max |
| `StereopsisUniversalSet` | **Pseudo-absorbent of \|** | **Convergent Strabismus** — degenerate limit: 𝕋₀ = all types, empty of meaning (Borges paradox) | 0 |

```
EmptyStereopsis        =  EmptyTerritory | EmptyMap          (neutral of |,    δ₁ = max)
StereopsisUniversalSet =  𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(|)              (pseudo-absorbent, δ₁ = 0)
                          = all 16 primitives (Base16)
                          StereopsisUniversalSet | a = StereopsisUniversalSet
                          "empty of meaning" — NOT a semantic ideal, a degenerate limit
```

---

## 🔭 Stereopsis Metaphor

Binocular vision creates **depth** from two slightly different flat images:
- Left eye (Eagle Eye / Territory) sees one perspective
- Right eye (Sphinx Eye / Map) sees another
- Brain fuses them → **depth perception** (stereopsis)

Analogously in TSCG:
- Eagle Eye measures Territory (ASFID)
- Sphinx Eye qualifies Map (REVOI)
- Stereopsis fuses them → **systemic depth** — understanding that exists
  in neither perspective alone

**Gs is this depth, formalized.**

---

## 📚 Key Takeaways

1. **Reification of stereopsis** — not a third head, but the formal algebraic
   structure of what two heads produce together
2. **Bicephalous monoid** (Gs, |, EmptyStereopsis) — closes the structural gap
3. **Base16 alphabet** — 𝕋₀(|) = {T, _^, _$, K, Ss, L} — **6 primitives**
4. **TKSL acronym** — 4 nominal Gs primitives (T=Temporality, K=Knowledge,
   Ss=Symbol, L=Localizability), each answering a transcendental question
5. **5-5-6 asymmetry** — Gs has 6 primitives vs 5 for Gt/Gm; semantically justified
6. **Notation convention** — St/It/O in hybrid formulas (containing |); ASFID/REVOI scoring unaffected
7. **| is universal** — operates across all three grammars, always produces Gs types
8. **Divergent/Convergent Strabismus** — documentation metaphors for EmptyStereopsis
   and StereopsisUniversalSet (now 16 primitives)

**Stereopsis is where Territory and Map fuse into something neither is alone.** 🔭
