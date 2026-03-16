# MTG Color Wheel — TSCG Poclet

**Domain:** Cultural Artifact (Gaming / Philosophy)  
**Version:** 1.1.0  
**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-02-26  
**Status:** VALIDATED

---

## Overview

This poclet models the **Color Wheel** from *Magic: The Gathering* (MTG), one of the most successful and enduring philosophical classification systems to emerge from game design. Since 1993, this pentagonal framework has structured the gameplay, narrative, and aesthetic identity of a game played by 20M+ people across more than 11 languages.

The system partitions philosophical orientations into **five irreducible poles** — White, Blue, Black, Red, Green — arranged on a **pentagram** with:
- **5 allied pairs** (adjacent on the pentagon): shared values, mechanical synergy
- **5 enemy pairs** (non-adjacent / star diagonals): fundamental value conflicts

---

## The Pentagram

```
              WHITE (Order)
                  ●  (90°)
                 /|\
                / | \
    (162°) ●  /  |  \  ● (18°)
          GREEN   |   BLUE
               \  |  /
                \ | /
    (234°) ●----\|/----● (306°)
           RED       BLACK
```

**Canonical clockwise order (Color Pie):** White → Blue → Black → Red → Green → White

| Color  | Angle | Allies      | Enemies     | Core Value   | Mana Symbol |
|--------|-------|-------------|-------------|--------------|-------------|
| White  |  90°  | Blue, Green | Black, Red  | Order        | {W}         |
| Blue   |  18°  | White, Black| Red, Green  | Knowledge    | {U}         |
| Black  | 306°  | Blue, Red   | White, Green| Ambition     | {B}         |
| Red    | 234°  | Black, Green| White, Blue | Freedom      | {R}         |
| Green  | 162°  | Red, White  | Blue, Black | Nature       | {G}         |

---

## Color Profiles

### ⬜ White — Order & Community
- **Philosophy:** The many are stronger than the one. Order brings peace, law brings justice.
- **Methods:** Laws, institutions, collective work, discipline
- **Strengths:** Small efficient creatures, life gain, exile/removal, mass boardwipes, protection
- **Weaknesses:** Rigid conformism, sacrifices individual for collective, lacks card draw
- **Lacks:** Flexibility, individuality, spontaneity
- **Symbolism:** Plains, angels, soldiers, clerics, sun

### 🔵 Blue — Knowledge & Perfection
- **Philosophy:** Everything can be improved. Knowledge is power. Through understanding we transcend our limits.
- **Methods:** Study, technology, magic, manipulation
- **Strengths:** Counterspells, card draw, flying creatures, control, artifact synergy, transformation
- **Weaknesses:** Analytical coldness, unethical manipulation, paralyzing perfectionism
- **Lacks:** Intuition, tradition, acceptance of imperfection
- **Symbolism:** Islands, water, wizards, sphinxes, merfolk

### ⬛ Black — Ambition & Power
- **Philosophy:** Every being has the right to do whatever it takes to survive and thrive. Morality is a luxury of the weak. Death is a resource.
- **Methods:** Power at any cost, resource exploitation (including death)
- **Strengths:** Creature destruction (targeted removal), hand disruption (discard), reanimation, life payment for power
- **Weaknesses:** Pathological egoism, destructive cynicism, parasitism
- **Lacks:** Altruism, scruples, sense of community
- **Symbolism:** Swamps, death, demons, vampires, zombies, necromancers

### 🔴 Red — Freedom & Passion
- **Philosophy:** Feel, don't think. Act now, worry later. Freedom is worth any price. Live in the moment.
- **Methods:** Intuition, passion, creative destruction, art
- **Strengths:** Direct damage (burn), haste, aggressive cheap creatures, chaos effects, artifact/enchantment destruction
- **Weaknesses:** Self-destructive chaos, impulsivity, anarchy; cards often have drawbacks
- **Lacks:** Discipline, planning, restraint
- **Symbolism:** Mountains, fire, lightning, goblins, dragons, warriors

### 🟢 Green — Nature & Growth
- **Philosophy:** Everything has its place in the natural order. Respect tradition and the web of life. Growth through time, not force.
- **Methods:** Adaptation, ecosystem reliance, acceptance
- **Strengths:** Large creatures, mana acceleration (ramp), enchantments, creature buffs, artifact/flying hate
- **Weaknesses:** Fatalism, rejection of progress, law of the jungle
- **Lacks:** Innovation, will to change destiny, individualism
- **Symbolism:** Forests, elves, beasts, druids, life cycle

---

## Allied Pairs (Pentagon Edges)

| Pair          | Guild (Ravnica) | Shared Value                      | Synergy                              |
|---------------|-----------------|-----------------------------------|--------------------------------------|
| White + Blue  | Azorius         | Order through structure/knowledge | Institutional wisdom, rational ethics |
| Blue + Black  | Dimir           | Power through knowledge           | Machiavellian intelligence, control  |
| Black + Red   | Rakdos          | Individual supremacy              | Passionate self-interest, aggression |
| Red + Green   | Gruul           | Instinct over intellect           | Wild freedom, natural power          |
| Green + White | Selesnya        | Collective harmony                | Communal tradition, organic order    |

---

## Enemy Pairs (Pentagram Diagonals)

| Pair           | Opposition               | Fundamental Conflict                          |
|----------------|--------------------------|-----------------------------------------------|
| White vs Black | Collectivism/Individualism| Community good vs personal gain              |
| Blue vs Red    | Intellect/Emotion        | Calculated thought vs spontaneous action     |
| Black vs Green | Ambition/Acceptance      | Changing destiny vs accepting fate           |
| Red vs White   | Freedom/Order            | Spontaneity vs structure                     |
| Green vs Blue  | Tradition/Progress       | Natural evolution vs artificial improvement  |

---

## TSCG Analysis

### Eagle Eye — Territory (ASFID)

| Dimension        | Score | Interpretation                                         |
|-----------------|-------|--------------------------------------------------------|
| A (Attractor)   | 0.65  | Moderate — philosophical attractor basins per color    |
| S (Structure)   | 0.80  | High — explicit pentagonal topology, 10 edges          |
| F (Flow)        | 0.45  | Low-Moderate — mana flows in gameplay; weak in theory  |
| I (Information) | 0.85  | Very High — rich philosophical/mechanical/narrative info|
| D (Dynamics)    | 0.50  | Moderate — stable core, dynamic meta-game/narrative    |

**ASFID Vector:** (0.65, 0.80, 0.45, 0.85, 0.50) — mean = 0.65  
**State Vector:** `|Ω_colorWheel⟩ = 0.65|A⟩ + 0.80|S⟩ + 0.45|F⟩ + 0.85|I⟩ + 0.50|D⟩`  
**Profile:** I-S dominant (highly structured information architecture)

### Sphinx Eye — Map (REVOI)

| Dimension            | Score | Interpretation                                          |
|---------------------|-------|--------------------------------------------------------|
| R (Representability) | 0.90  | Very High — perfect semantic decodability across cultures|
| E (Evolvability)     | 0.85  | High — core stable, continuously absorbs new mechanics |
| V (Verifiability)    | 0.70  | Moderate — verifiable at gameplay level, fuzzy at theory|
| O (Observability)    | 0.75  | High — model crystal clear, philosophical territory fuzzy|
| I (Interoperability) | 0.90  | Very High — 31 possible color combinations, cross-domain|

**REVOI Vector:** (0.90, 0.85, 0.70, 0.75, 0.90) — mean = 0.82  
**State Vector:** `|M_colorWheel⟩ = 0.90|R⟩ + 0.85|E⟩ + 0.70|V⟩ + 0.75|O⟩ + 0.90|I⟩`

### Epistemic Gap

```
Δθ = |ASFID_mean - REVOI_mean| = |0.65 - 0.82| = 0.17  (Map > Territory)
```

**Interpretation:** The Color Wheel as a MAP is significantly stronger than the philosophical Territory it describes. Typical of normative/prescriptive frameworks — the model is clearer than reality. The Color Wheel is a **world-making device**, not merely a descriptive tool.

---

## M2 Generic Concept Mobilization

28 M2 generic concepts instantiated, including: Structure, Component, Relation, Opposition, Synergy, Constraint, Trade-off, Balance, **Polarity** (critical: N-ary, N=5), Attractor, Network, Code, Identity, Boundary, Fusion, Composition, Emergence, Diversity, Complementarity, Tension, Symmetry, Topology, Cycle, Spectrum, Archetype, Mode, Layer, Imbrication.

### Key TSCG Discovery

> **N-ary Polarity (N=5):** Magic Color Wheel forced recognition that real-world conceptual frameworks exhibit N-ary polarity (not just binary). This led to the redefinition of `m2:Polarity` as parametric (N ∈ {1, 2, 3, 4, 5, ...}) — a paradigm shift validated by Wu Xing (N=5), Political Compass (N=4), and Enneagram (N=9).

---

## New M2 Candidate Concepts

| Concept       | Formula     | Status                                     |
|---------------|-------------|--------------------------------------------|
| Polarity-N    | S⊗I⊗A       | CANDIDATE — N-ary polarity validation needed|
| Alliance      | I⊗S         | CANDIDATE — overlaps Synergy, Relation     |
| Antagonism    | I⊗D         | CANDIDATE — overlaps Opposition, Tension   |

---

## Files

| File                          | Description                              |
|-------------------------------|------------------------------------------|
| `M0_MTG_ColorWheel.jsonld`    | Main ontology (JSON-LD)                  |
| `README_MTG_ColorWheel.md`    | This file                                |
| `sim_mtg_color_wheel.py`      | Interactive Pygame simulation            |

---

## References

- MTG Wiki: Color — https://mtg.fandom.com/wiki/Color
- Mark Rosewater's Color Pie Articles — https://magic.wizards.com
- TSCG M2 GenericConcepts: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld
- TSCG M1 CoreConcepts: https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld
