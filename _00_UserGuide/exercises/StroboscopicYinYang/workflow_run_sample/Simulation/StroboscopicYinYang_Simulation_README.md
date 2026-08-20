# Stroboscopic Yin-Yang — Simulation README

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-20 · **Simulation version**: 1.1.0
**File**: `StroboscopicYinYang_sim.html` (single-file, serverless, p5.js)
**Companion**: `M0_StroboscopicYinYang_README.md` (the ontology/model README)

> This document covers the **visualization only** — how it is designed, how to drive it,
> and what each pattern means. The TSCG model itself (ASFID/REVOI scores, GenericConcepts,
> framework findings) is documented in the M0 README.

---

## 1. What it shows

A yin-yang disc rotating in front of an observer whose vision is **sampled frame by
frame**. The point of the sketch is that the *same* unchanging disc yields a whole ladder
of different perceived patterns — a single figure, a frozen figure, an apparent reversal,
or 2, 3, 4 … 8 superimposed figures with grey shading — purely as a function of how far
the disc turns between two frames.

## 2. One parameter: **Δθ, degrees per frame**

The frame **is** the sampler, so there is no separate rotation speed and sampling rate:
the only meaningful quantity is their ratio, expressed as the angular advance per frame.

- **Δθ sweeps automatically from 0° to 360°, then loops.**
- Because the yin-yang has **order-2 rotational symmetry** (it maps onto itself every
  180°), the whole ladder of patterns **repeats twice** across the 0–360° range.

### Landmarks

| Δθ (°/frame) | What you see |
|---|---|
| 0 | Still — the plain yin-yang |
| 22.5 | **8 figures** |
| 45 | **4 figures** |
| 60 | **3 figures** |
| 90 | **2 figures** |
| 120 | 3 figures |
| 135 | 4 figures |
| just under 180 | **Apparent reversal** (wagon-wheel effect) |
| 180 | **Frozen** — order-2 symmetry lands every frame on the same figure |
| 270 | 2 figures |
| just under 360 | Apparent reversal |
| 360 | **Frozen** — one full turn per frame |

Between these locked ratios the sampled orientations spread out and the image becomes a
**grey wash** ("Unlocked" in the readout).

### The rule behind the table

Fold Δθ into the symmetry period: `frac = (Δθ mod 180) / 180`. When `frac ≈ p/q` for a
small integer `q`, successive frames land on **q distinct orientations** → *q*
superimposed yin-yangs. `q = 1` gives the single-figure regimes (frozen, reversal, slow
drift); the perceived per-frame rotation is Δθ folded into (−90°, +90°].

## 3. Controls

| Control | Behaviour |
|---|---|
| **Speed Scan** (default, active) | Δθ sweeps automatically and loops 0 → 360 → 0, **pausing ~1.3 s on each new N-figure pattern** so it can be examined. |
| **Select Speed** | Press the button to toggle; it renames itself and **enables the Δθ slider** for manual exploration. Press again to resume scanning. |
| **Δθ slider** | Sits immediately right of that button. Disabled during Speed Scan, active in Select Speed. |
| **⏸ Stop / ▶ Run** | Freezes the animation — see §5. |
| **Side panel tabs** | Description (landmarks + how to falsify), ASFID/REVOI (the model's scores), Concepts (M2 formulas read from HEAD), Notes (rendering + limits). |
| **Splitter** | Drag to resize the canvas against the panel. |

The on-canvas readout reports the current regime, Δθ, the perceived Δθ, the apparent
figure count, and how many frames are being integrated.

## 4. How it renders

Each frame the disc advances by Δθ. The display shows the **average of the last 8 frames**
— a persistence-of-vision window. Copies are composited at alpha `1/i`, which yields an
exact equal-weight running average, so at a locked ratio the *q* coincident orientations
produce grey levels in clean steps of `1/q` and the pattern stays **crisp and
high-contrast** rather than washing toward uniform grey. A CSS `contrast` filter further
separates the levels.

The **concentric rings** ("cercles") come for free: the S-curve boundary sits at a
different angle for each radius, so the q-fold modulation is phase-shifted ring by ring.

**Territory reference.** A single outer tick shows the *true* rotation direction. Its
on-screen speed is deliberately capped so the reference itself does not alias on the
viewer's monitor — keeping the Territory (what the disc does) visually distinct from the
Map (what is perceived) at all times.

## 5. The falsification button (why Stop matters)

Pressing **⏸ Stop** does more than pause: it drops the integration to a **single frame**,
so the sweep is zero and the **plain yin-yang reappears, crisp**. This is the
simulation's built-in experiment — it demonstrates that the rings and rays are **produced
by integrating successive frames, not by the figure itself**. The disc never changed; the
observer's sampling did. This is the concrete reason the model scores **V = 0.95**
(Verifiability): the viewer can falsify the claim in one click.

## 6. Honest limits

- **"Per frame" means *your* browser's frame** (60, 120 or 144 Hz). The patterns depend
  only on Δθ, so they are identical across machines, but the *scroll speed* of the sweep
  will differ.
- **The monitor is a second sampler** stacked on the simulated one. At extreme settings
  the displayed image can diverge from the idealized figure count the model computes — a
  fitting meta-lesson about stacked observers.
- **The yin-yang is angularly smooth** (essentially one half-turn split), so high-`q`
  figures read mainly through the two dots and the S-curve edges. A disc with fine radial
  markings would show sharper high-`q` rays — a natural future option.
- The figure count is capped at the integration depth (**8 frames**), so `q > 8` is not
  resolved.

## 7. Design rationale (TSCG reading)

The sketch is a hands-on rendering of the poclet's thesis: **each pattern is a different
Map of one unchanging Territory**, selected by the observer's sampling. It makes the
reduction `Φ: Gt → Gm` and observer-relativity (`m2:Observer`) directly visible, and it
illustrates the *sensory-cone ∩ cognitive-sphere* architecture note — the patterns are an
artifact of the **temporal rim of the sensory cone**, not a property of the disc.

## 8. Running it

Open `StroboscopicYinYang_sim.html` in any modern browser — no server, no build step.
p5.js is loaded from a CDN, permitted by the file's Content-Security-Policy.

*TSCG Framework — Echopraxium with the collaboration of Claude AI — August 2026.*
