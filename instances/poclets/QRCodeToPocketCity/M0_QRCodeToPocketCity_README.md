# M0_QRCodeToPocketCity

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-02
**Version**: 1.0.0
**Instance type**: `m3:Poclet`
**Facet**: `m0:facet.Democratization` (roleGrounding: `Designed`)
**Status**: Modelled + simulated

---

## 1. What this poclet is about

A QR code is transformed into a navigable 3D miniature city. Dark modules
become buildings, light modules become streets. The transformation is
**procedural, deterministic and constrained**:

- **Procedural** — heights, windows, doors, chimneys, materials, arches and
  landmarks are all generated, not authored.
- **Deterministic** — the same text always produces exactly the same city.
  The seed is the city's identity card.
- **Constrained** — seen orthographically from directly above, the city must
  **still be a scannable QR code** encoding the original payload.

That last point is what makes this a system rather than a rendering. The
same information carries two simultaneous encodings — one machine-readable,
one human-inhabitable — and they are required not to conflict.

---

## 2. Why it qualifies as a poclet

| Criterion | Assessment |
|---|---|
| **Minimal** | Nothing can be removed without breaking either the QR reading or the city. Remove the orthographic camera and the code stops decoding; remove the module grid and there is no city. |
| **Complete (ASFID)** | All five Territory dimensions are present and load-bearing — see §4. |
| **External system** | QR codes are an ISO/IEC 18004 standard, not a TSCG artifact. The city is the construction; the code is the given. |
| **Empirical arbitration** | Uniquely direct: point a phone at the Bird's-eye view. It decodes or it does not. No expert judgement required. |

That last row is worth pausing on. Most poclets are arbitrated by structural
plausibility. This one carries a **binary empirical test** that any reader can
run in five seconds. Within the corpus, that is unusual.

---

## 3. The binding constraint

> A dark module must remain predominantly dark when seen from directly above.
> A light module must remain predominantly light.

Everything else is free. This is a **fertile constraint**: it grants wide
latitude in 3D while preserving the 2D semantics. Its consequences propagate
through the entire design:

| Consequence | Why the constraint forces it |
|---|---|
| Orthographic projection is mandatory | Under perspective, off-centre buildings lean outward and their roofs no longer cover their footprint — the pattern breaks at the edges |
| Roof caps span the full grid pitch (1.0) | Building bodies are inset to 0.998 to avoid z-fighting between neighbours; the caps close the gap so blocks read as contiguous |
| A dark ground plate sits under every dark module | Belt-and-braces: even at an oblique angle no light seam shows between buildings |
| Chimney caps match the roof colour exactly | From directly above the cap is the *only* visible part of a chimney; any lighter tone appears as a dot on the module |
| Inclined roofs and inclined streets were abandoned | Both break the predominance rule at the margins |
| Signs, windows, doors and arches are unconstrained | All are vertical surfaces — invisible from above |

**Verification**: open the simulation, switch to Bird's eye, and scan the
screen with any phone. It should decode the text you typed.

---

## 4. ASFID — Territory (Eagle Eye)

| Dim | Score | Expression in this system |
|---|---|---|
| **A** Attractor | 0.85 | The decoded payload: the unique state the whole structure converges on. Secondarily the readability constraint, which every generation decision must satisfy. |
| **S** Structure | 0.92 | Module grid, finder patterns, timing patterns, quiet zone, and the derived building geometry. Fully determined and inspectable. |
| **F** Flow | 0.70 | Two flows: the scanner's zigzag reading path, and the explorer's traversal of streets and arches. Real, but not the system's centre of gravity. |
| **It** Information | 0.88 | Payload plus Reed-Solomon redundancy, plus the seed that carries the city's identity. |
| **D** Dynamics | 0.72 | SHA-256 seed chaining, stylesheet re-interpretation, polarity inversion — the space of cities reachable from one code. |

Mean ASFID = **0.814**

## 5. REVOI — Map (Sphinx Eye)

| Dim | Score | Justification |
|---|---|---|
| **R** Representability | 0.95 | The artifact *is* a representation; representability is its subject matter. |
| **E** Evolvability | 0.88 | Stylesheets, seeds, grid sizes and polarity all vary independently. |
| **V** Verifiability | 0.92 | Directly falsifiable by scanning. Rare and valuable. |
| **O** Observability | 0.90 | Every generated element is visible; live counters expose instances, draw calls, arch count, build time. |
| **Im** Interoperability | 0.82 | Standard QR (ISO/IEC 18004) in, standard web out. Slightly below the rest because the city format is bespoke. |

Mean REVOI = **0.894**

### Epistemic gap

```
δ₁ = |0.894 − 0.814| = 0.080  →  OnCriticalLine [0.05, 0.15)
```

Map slightly ahead of Territory, which is the expected signature of an
artifact whose *purpose* is representation. The margin is small enough that
the two eyes are not in tension.

---

## 6. M2 GenericConcepts mobilized (12)

| Concept | Formula | Family | Role in this poclet |
|---|---|---|---|
| `m2:Code` | `It × Ss` | Informational | The QR encoding — and the city as a second encoding of the same payload |
| `m2:Constraint` | `St × A × D \| O + V` | Regulatory | The top-view readability rule. **The pivot of the whole system** |
| `m2:Invariant` | `S × A` | Structural | What survives every stylesheet, seed and polarity: the module grid |
| `m2:Identity` | `St × It × A \| V + E` | Structural | The seed as the city's identity card |
| `m2:Signature` | `It × Ss \| V` | Informational | The seed rendered in hex; distinguishes one city from another |
| `m2:Segmentation` | `S × I × D` | Structural | Partition of the plane into modules |
| `m2:Symmetry` | `S` | Structural | Finder patterns — and their *deliberately broken* fourth corner |
| `m2:Topology` | `St \| L` | Structural | Arch tunnels adding graph edges absent from the flat code |
| `m2:Network` | `S × I × F` | Structural | The street connectivity graph |
| `m2:Space` | `St \| L` | Ontological | The city as inhabited extent rather than image |
| `m2:Layer` | `St × It × A \| R` | Structural | The stylesheet as an interpretation layer |
| `m2:Transformation` | `D × S × I` | Dynamic | Matrix → geometry, and re-interpretation between stylesheets |
| `m2:Trade-off` | `A × I × F` | Regulatory | Normal vs inverted polarity: the two readings cannot both hold |
| `m2:Role` | `Ss \| K` | Relational | Finder patterns as civic landmarks; the Democratization facet itself |

### Honest note on a missing concept

**Reed-Solomon error correction has no clean M2 representative.** The nearest
candidates (`m2:Redundancy` does not exist in M2 v16.x) leave the poclet's most
mathematically substantial component under-described. Two readings:

1. Error correction is a *specialisation* of `m2:Code` and needs no separate
   concept.
2. Structural redundancy — over-specification enabling recovery under damage —
   is transdisciplinary and irreducible, and its absence is a genuine gap.

Reading (2) would need ≥6 domain validations before proposing anything, per the
anti-overfitting rule. Flagged here, not resolved.

---

## 7. Structural signature

The three broken-out sub-signatures:

```
dual_encoding        one payload, two simultaneous readings that must not conflict
constrained_generation   procedural freedom bounded by a single testable invariant
navigable_symbol     a sign that has become a place
```

The last is where this poclet touches the **Gs (Stereopsis)** grammar. The
explorer accretes knowledge (K) by traversing (T) a symbol (Ss) while judging
their position relative to the landmarks (L). This is the strongest Gs-side
candidate in the corpus so far, which is why `m0:note` flags it as a future
`m3:ExploratorySpace` candidate.

It is typed `m3:Poclet` for now: creating a new instance type requires **≥3
instances**, and only this one exists.

---

## 8. Democratization facet

This is the **first instance carrying `roleGrounding: Designed`** — conceived
for pedagogical purpose rather than found effective after the fact.

```json
"m0:hasFacet":     { "@id": "m0:facet.Democratization" },
"m0:roleGrounding":{ "@id": "m0:roleGrounding.Designed" },
"m0:illustratesConcept": [
  "Map/Territory duality — one payload, two simultaneous encodings that must not conflict",
  { "@id": "m2:Constraint" },
  { "@id": "m2:Invariant" }
]
```

Why it teaches well: the Map/Territory distinction is usually explained by
analogy. Here it is **operational**. The QR reading and the city reading are
both real, both complete, and visibly different — and a scanner arbitrates
between them without appeal to authority.

---

## 9. Simulation

```
_static/                           ← the launcher serves THIS as web root
├── M0_QRCodeToPocketCity.html     page shell
├── _00_serve_poclet-sim.bat       local server launcher
├── lib/                           vendored third-party (see lib/README.md)
│   ├── qrcode.js                  essential — no QR, no poclet
│   └── earcut.min.js              BabylonJS needs it for the arch tunnels
└── src/
    ├── tscg-shell.css             shared chrome  (copy of _TEMPLATE_poclet-sim)
    ├── tscg-shell.js              shared chrome  (copy of _TEMPLATE_poclet-sim)
    ├── qrcity.css                 poclet overrides, loaded after the shell
    ├── qrcity-stylesheets.js      STYLE — declarative stylesheet registry
    └── qrcity.js                  CORE — generator + BabylonJS scene
```

The shell files are **copied** into `src/` rather than referenced from
`../../../_TEMPLATE_poclet-sim/`. The launcher serves `_static/` as the web
root, so anything above it is unreachable and the page loads unstyled.

Engine: **BabylonJS 6.x** (the only remaining CDN library, ~4 MB), per the
TSCG convention for validated instance simulations. (The design prototype used Three.js because it was built on a
phone; the production simulation follows the convention.)

Separation of concerns, mirroring CanopyGraphViz:

- **DATA** — the QR matrix. Pure structure, no appearance.
- **STYLE** — `qrcity-stylesheets.js`. Declarative JSON. Also carries generation
  *rules*, so switching stylesheet changes geometry, not just colour.
- **CORE** — `qrcity.js`. Reads STYLE, never hardcodes an appearance value.

### Controls

| Action | Control |
|---|---|
| Encode text | Text field → **Build** |
| Grid size | Dropdown (QR versions only: 21…49) |
| View | Isometric / Bird's eye / Walk / Fly |
| Polarity | Invert reading |
| Re-interpret | Next seed (SHA-256 of current seed) |
| Stylesheet | Daylight / Night / Blueprint / Terracotta |

---

## 10. Open questions

1. **ExploratorySpace as an instance type** — needs ≥3 members. Candidates:
   Yi Jing hexagram hypercube, a navigable Mandelbrot set, counterpoint score
   as architecture. Also unresolved: whether `m3:Enigma` (currently count 0)
   already covers this family.
2. **Redundancy in M2** — see §6. Flagged, not proposed.
3. **Underground layer** — trapdoors and corridors would add a *second*
   connectivity graph, independent of the surface. Designed, not built.
4. **Deriving decoration from data** — building heights currently come from the
   seed, not from the payload bits. Deriving them from local module density
   would make the decoration information-bearing rather than arbitrary.
