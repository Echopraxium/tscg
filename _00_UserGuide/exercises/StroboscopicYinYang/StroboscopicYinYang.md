# Stroboscopic Yin-Yang — TSCG Exercise

**Domain:** Perception / psychophysics (temporal sampling) — adjacent to optics
**Difficulty:** Intermediate
**Natural simulation:** 2D (p5.js) — a spinning yin-yang with speed (and strobe) controls

> **This is a *worked* exercise.** A **sample workflow run** (M0 model + simulation)
> lives in `workflow_run_sample/`, deliberately marked as a spoiler, because it exists
> to **illustrate the end-to-end TSCG workflow** — it is *one* example resolution, **not
> a definitive answer key** (TSCG has no single correct model). Do it yourself first if
> you want the practice.

## 1. The system in one paragraph
A yin-yang disc spins. The eye does not see the continuous rotation directly — it
**samples** it (retinal persistence, ~1/16 s of integration). Depending on the
rotation speed, you perceive different **regimes**: smooth rotation, a frozen figure,
apparent *reversal* (the wagon-wheel effect), or morphing patterns. Two coupled
phenomena are at play: **retinal persistence** (the eye time-integrates the continuous
motion into a smeared image) and **stroboscopic aliasing** (discrete sampling beating
against the rotation frequency). Both are functions of one control — the speed.

## 2. Suggested scope (minimal + complete)
One yin-yang disc, a **speed** control, and (optionally) a **sampling/strobe rate**.
Model the relation *speed → perceived regime*, not the visual cortex. The essential
object is the interaction of two rates (rotation vs sampling), and what it does to the
**perceived** image versus the **actual** one.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): weak — there is **no** state the system converges to; the perceived
  regime is a *function of speed*, not an attractor. Be honest about this (like Logic
  Gates is Information-dominant). The nuance worth discussing: at **special speeds**
  (rotation frequency an integer multiple of the sampling rate) the pattern appears
  *frozen* — resonance-like fixed points of the *perception*, not of the disc.
- **S** (Structure): the disc's **order-2 rotational symmetry** (the S-curve + two dots)
  and the sampling apparatus (retina, or a strobe).
- **F** (Flow): the **continuous rotation** (the Territory) versus the **discrete sample
  stream** the eye/strobe produces (the Map).
- **I** (Information): **rotation speed**, **sampling rate**, and the **phase relation**
  between them — the drivers. This poclet is Information/Dynamics-dominant.
- **D** (Dynamics): the **beat** between two rates producing the perceived regime —
  smooth, frozen, or reversed (aliasing).

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Sampling / reduction** concept — the perceived image is a **Map** the eye builds
  by reducing a continuous **Territory**. This is the central lesson (Φ: Gt → Gm made
  visible).
- A **Beat / aliasing between two rates** concept (rotation vs sampling).
- A **Threshold / critical value** concept (the special speeds where it freezes/reverses).
- A **Symmetry** concept (order-2 rotational). Verify all against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** perception/psychophysics domain at HEAD →
  **new-domain finding**. Note the adjacency to `optics` (which exists) — but optics
  models the physics of light and lenses, not the *temporal* sampling of perception, so
  this is a genuinely different domain.
- **Possible M2 candidate?** "An artifact produced by discretely sampling a continuous
  process" recurs widely — digital audio aliasing, moiré, wagon wheels on film, strobe
  photography. A strong candidate to *flag*, but hold to the anti-overfitting rule: it
  needs attested residue across ≥6 independent domains before it earns a concept.

## 6. Source documentation
References on persistence of vision and temporal aliasing (the Wikipedia articles
"Persistence of vision", "Wagon-wheel effect", and "Stroboscopic effect"). A teaching
bonus: the effect is **directly verifiable by the reader's own eyes** — so the model can
be judged against a reality the user perceives first-hand (free **Verifiability**, the V
of REVOI).

## 7. Simulation hint (2D, p5.js)
Draw a yin-yang, with a **speed** slider and an optional **strobe/frame-rate** slider.
Simulate the two regimes: **motion blur** for retinal persistence, and **discrete frame
sampling** for strobe aliasing. As the user raises the speed, they should find the
points where the disc appears to **freeze** and then **rotate backwards** — discovering
the wagon-wheel effect themselves. The gap between "what the disc does" (Territory) and
"what you see" (Map) is the whole point.
