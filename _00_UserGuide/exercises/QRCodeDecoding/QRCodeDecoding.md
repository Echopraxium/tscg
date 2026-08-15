# QR Code / DataMatrix Decoding — TSCG Exercise

**Domain:** Coding theory / information / computer vision
**Difficulty:** Intermediate
**Natural simulation:** 2D (p5.js) — a module grid you can damage and watch recover

## 1. The system in one paragraph
A QR code (or DataMatrix) stores data in a 2D grid of black/white **modules**,
with finder patterns for location, timing patterns for the grid, format/version
info, and **Reed-Solomon error correction**. **Decoding** is a pipeline: locate
and rectify the grid, sample the modules, remove the mask, de-interleave the
blocks, run error correction, and extract the payload — which still succeeds even
when part of the symbol is damaged.

## 2. Suggested scope (minimal + complete)
Model the **decoding pipeline as stages** (not a full camera decoder), with the
focus on *why error correction makes it robust*. Reduction: a fixed small QR
version, schematic modules, adjustable damage level.

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): the **recovered message** — decoding converges to the correct
  payload even from a noisy/partly-damaged symbol (error correction pulls toward
  the nearest valid codeword).
- **S** (Structure): the **module grid** with finder / alignment / timing patterns
  and the data + ECC layout.
- **F** (Flow): the **pipeline** — locate → sample → unmask → de-interleave →
  RS-decode → payload.
- **I** (Information): the encoded bits, format/version, and crucially the
  **redundancy** — this is an Information-dominant poclet.
- **D** (Dynamics): sequential transformation through stages; error correction as
  convergence to a valid codeword.

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- A **Process / pipeline** concept.
- A **Redundancy / error-correction (robustness)** concept.
- An **Encoding ↔ decoding** concept (Map/Territory: symbol grid ↔ message).
- A **Threshold** concept (the maximum correctable error fraction).
Verify against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** coding-theory/information domain →
  **new-domain finding**. (Related but distinct: the existing generative poclet
  `QRCodeToPocketCity` *produces* from a QR seed; this exercise *reads* one.)
- **Possible M2 candidate?** "Redundancy enabling recovery from partial damage"
  recurs widely (DNA, RAID, natural language). Strong candidate territory — flag
  with discipline, don't formalise on one instance.

## 6. Source documentation
References on QR structure and Reed-Solomon (the Wikipedia articles "QR code" and
"Reed–Solomon error correction"). Attach in the Proposition step.

## 7. Simulation hint (2D, p5.js)
Draw a QR grid with finder patterns highlighted; let the user flip modules to
"damage" it and show the decode succeeding until damage exceeds the ECC limit,
then failing — making the **Threshold** and **redundancy** facets visible. Keep
it schematic; full image decoding is out of scope.
