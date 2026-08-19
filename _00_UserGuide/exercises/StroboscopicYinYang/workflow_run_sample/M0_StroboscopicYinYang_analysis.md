# TSCG Analysis — Stroboscopic Yin-Yang

*Author: Echopraxium with the collaboration of Claude AI — 2026-08-19*
*All framework facts (M2 formulas, domain existence, SHACL schema) read from HEAD.*

## Verdict: Alignment (with a documented Gap)

The system models cleanly with existing M2 GenericConcepts and all five ASFID
dimensions. It also produces **one positive-value Gap** (a missing M1 domain) and
**flags one M2 candidate** — neither blocks modeling; both are recorded below.

---

## ASFID Lens (Territory / Eagle Eye)

- **A (Attractor) — weak (0.30).** Honest finding: the disc converges to *no* state;
  the perceived regime is a *function of speed*, not an attractor. The only fixed-point
  flavour appears at special speeds (ω = k·f_s) where the figure looks *frozen* — but
  those are resonance-like fixed points **of the perception**, not of the disc. A is
  therefore present but deliberately low, comparable to how Logic Gates is
  Information-dominant with little dynamics.
- **S (Structure) — moderate (0.65).** The disc's **order-2 rotational symmetry**
  (S-curve + two dots, invariant under 180°) plus the sampling apparatus (retina/strobe).
- **F (Flow) — strong (0.80).** Two coupled flows: the **continuous rotation** (the
  Territory) and the **discrete sample stream** the eye/strobe produces (the Map).
- **I (Information) — dominant (0.90).** The drivers: **rotation speed ω**,
  **sampling rate f_s**, and their **phase φ**. This poclet is Information/Dynamics-dominant.
- **D (Dynamics) — dominant (0.90).** The **beat** between two rates that produces the
  perceived regime (smooth / frozen / reversed / morphing).

## REVOI Lens (Map / Sphinx Eye)

- **V (Verifiability) — 0.95.** Gold standard: the reader confirms every regime with
  their **own eyes** in seconds. Free, first-person falsifiability.
- **O (Observability) — 0.90.** Freeze and reversal are directly perceptible.
- **R (Representability) — 0.85.** One disc + two sliders fully represents the model.
- **Im (Interoperability) — 0.85.** "Aliasing / wagon-wheel" is shared vocabulary
  across signal processing, film, and audio.
- **E (Evolvability) — 0.75.** The same Map generalises to any discretely-sampled
  continuous process.

**asfidMean = 0.71 · revoiMean = 0.86 · δ₁ = |0.71 − 0.86|/√2 = 0.106 → OnCriticalLine.**
The gap is not model error — it *is* the phenomenon: perception legitimately builds a
Map that diverges from the Territory. The instance is **Slightly Hyperopic**
(focalScore ≈ 0.64, Map marginally dominant over Territory) — fitting, since the lesson
is that what you *perceive* can outrun what the disc *does*.

---

## Anticipated M2 GenericConcepts (verified against HEAD)

Central lesson — the reduction **Φ: Gt → Gm** made visible — is carried not by a single
"Sampling" concept (none exists at HEAD) but by a *cluster*:

- **Transducer** (`F × St × It`) — eye/strobe turns continuous motion into samples.
- **Channel** (`St × F | Ss`) — the sampler as the sampling channel (stereopsic).
- **Segmentation** (`St × It × D`) — discrete sampling cuts motion into frames.
- **Coding (Encoding/Decoding)** (`It × St × D`) — sampling encodes, perception decodes.
- **Signal** (`It × F`) — continuous rotation and the sampled stream.
- **Representation** (`It × St`) / **Signature** (`It × Ss | V`) — the perceived image.
- **Observer** (`It × A`) / **Observable** — the regime is observer-relative.
- **Coherence/Incoherence** (`A × St × It | R + O`) — phase-lock (frozen) vs smear.
- **Modelisation** (`D × F × It | R + V + E`) — building the perceived Map.
- **Bifurcation** (`D × F | L`) / **Threshold** (`A × It`) / **Trigger** (`D × It`) —
  the regime switch at critical speeds ω = k·f_s.
- **Symmetry** (`St`) — order-2 rotational symmetry (halves the freeze period).
- Supporting: **Process, Trajectory, Transformation, System, Component, Topology,
  State, Pattern**.

23 GenericConcepts total (full list with formulas in the M0 file and README).

---

## M2 Candidate — FLAG only (do not promote)

🆕 **M2 Candidate: Aliasing (Stroboscopic Sampling Artifact)**
- **Proposed formula:** `F × D × It | Ss` — *PROPOSAL, not verified at HEAD.*
- **Role:** an artifact produced when a continuous Flow is discretely sampled and the
  sample rate beats against the process rate, yielding a *perceived* Dynamics that
  differs from the *actual* one (freeze / reversal / morph).
- **Status:** *Proposal — to be validated.*
- **Anti-overfitting hold:** the pattern recurs widely (wagon-wheel on film, digital
  audio foldback, moiré, strobe photography, Nyquist violation), but per the
  anti-overfitting rule it needs **attested residue across ≥6 independent domains**
  before it earns a concept. **Recommendation: flag, do not promote.**

## Domain Question — Gap (positive value)

- **Existing M1 extension? No.** Verified at HEAD: `M1_extensions/perception/` and
  `.../psychophysics/` return **404**; `M1_extensions/optics/` returns **200**.
- **New-domain finding: Perception (temporal sampling).** Adjacent to `optics`, but
  genuinely different — optics models the physics of light and lenses, this models the
  *temporal sampling of perception*. `m1:domain` is set to `"Perception"` (accepted by
  SHACL as a free string); it is **not yet registered** in `M1_Domains.jsonld`.
- **Recommendation:** proceed with `m1:domain = "Perception"` now; **defer** creating a
  full `M1_Perception.jsonld` extension until a second, unrelated perception poclet
  justifies it (avoid a one-instance domain). This is Michel's call.

---

## Comparison with existing instances

- **Logic Gates** — shares the "Information-dominant, weak-Attractor, honest about it"
  profile.
- **Fire Triangle** — shares the minimal-yet-complete, emergence-from-parts shape (here
  the emergent property is the *perceived regime*, from the beat of two rates).
- **Phase Transition / Bifurcation poclets** — share the critical-value regime switch,
  but here the bifurcation lives in the *perception*, not the physical system.

## Recommended Decision

**Continue to Modeling** (done) and **Simulation** (done). Two items await Michel's
decision at a later sync point: (1) whether to open a minimal `Perception` M1 extension
or defer; (2) whether to keep tracking the `Aliasing` M2 candidate toward its 6-domain
threshold. Neither blocks this instance.
