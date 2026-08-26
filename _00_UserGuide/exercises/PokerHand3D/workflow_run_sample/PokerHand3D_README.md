# PokerHand3D — Exercise Reference Solution

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** UserGuide exercise (reference solution) — *not* a gallery poclet
**Files:** `PokerHand3D.jsonld` (the M0-layer instance) · `M0_PokerHand3D_Simulation.html` + `src/` (BabylonJS simulation)

---

## What this is

A small, exact, self-contained model — a **3D map of the ten poker hand
combinations**. It was built as a *worked exercise* for the TSCG UserGuide, in
the spirit of Stroboscopic Yin-Yang: minimal and transparent, chosen so a
beginner meets the real modelling questions (*is there an M1 domain? is this an
M2 candidate?*) rather than being impressed by complexity.

It visualises the **combinatorial grammar of 5-card hands**, not the game of
poker: there is no betting, no opponent, no strategy.

## The model — a circular pillar

- **Four vertical edges = the four suits** (♣ ♥ ♦ ♠).
- **Fourteen floors = the ranks**, with the **Ace doubled**: the bottom floor is
  reserved for the *wheel* (A-2-3-4-5), the top floor for the Ace-high.
- **Each card = one point** (rank floor × suit edge), a small sphere coloured by
  suit.

The ten categories then read as **geometric figures**:

| Category | Figure |
|---|---|
| Pair / Two Pair | one / two bicolour **cylinders** (segment per pair) |
| Three of a Kind | magenta **triangle** (surface + bicolour edges) |
| Four of a Kind | magenta **square** |
| Full House | triangle (trips) + cylinder (pair) |
| Straight | a **snake** of bicolour cylinders across floors |
| Flush | a stack of **disks** of one suit on a single edge |
| Straight Flush / Royal | snake **and** disks on one edge (a straight that is also a flush) |

The **determining card** (the one that names or breaks the tie) is caged in an
**octahedron** — magenta when it belongs to the figure, beige when it is a
kicker. Off-figure kickers are drawn beige, smaller and dimmer, so the figure
stands out.

### The pedagogical nugget

Because the Ace is **doubled rather than identified**, the rank axis is *cyclic
in spirit but cut at the Ace*. A literal circle would wrongly permit the
round-the-corner straight **K-A-2-3-4**; the doubled Ace makes that illegal move
**visually impossible**. This is a small, honest lesson in **Map ↔ Territory
fidelity**: the map must not over-generate what the territory forbids.

The **strength gauge** is *inversely proportional to a hand's frequency* (over
the 2,598,960 possible hands), so **rarity explains the ranking** rather than the
ranking being merely asserted.

## TSCG reading (from `PokerHand3D.jsonld`)

**Territory (ASFID):** A 0.30 · S 0.95 · F 0.10 · It 0.85 · D 0.10 — **mean 0.46**.
Structure-dominant with strong Information; Flow and Dynamics near zero (a static
classification — legitimate *Stase*).

**Map (REVOI):** R 0.95 · E 0.55 · V 0.90 · O 0.90 · Im 0.65 — **mean 0.79**.

**Epistemic gap δ₁ = 0.23 → Liminal.** The Map mean exceeds the Territory mean: a
**Map-dominant** instance. Its value is not *what the system is* but *how it makes
the hand-space knowable* — which is exactly why it carries the
**Democratization facet** (`roleGrounding = Designed`).

**GenericConcepts mobilised (M2):** Hierarchy, Topology, Symmetry, Invariant
(Structural); Pattern, Representation, Signature, Code (Informational).

## The domain question (the point of the exercise)

No existing M1 extension covers this system. Rather than force one, `m1:domain`
uses **descriptive strings** — `"Combinatorics"`, `"Card Games"` — and this is
*part of the lesson*: a good first model often has **no domain yet**, and that is
a finding, not a defect. `Combinatorics` is noted as a future domain **candidate**
— to be opened only once several unrelated instances justify it (the
anti-overfitting guardrail). The naming debate this exercise provokes (Strategy
Games? Game Theory? Data Visualization? Computer Science?) is itself the teaching
moment.

## Validation

- **SHACL (standalone):** *Conforms*.
- **`check_m0_instances.py` C01–C15:** all pass, **C15 SHACL Conforms**. The one
  **WARN (C03)** is expected: the local alias `m0.pokerHand3D` resolves to the
  *exercise* path, not the canonical `instances/poclets/` path — a direct
  consequence of this being an exercise solution named `PokerHand3D.jsonld` rather
  than a gallery `M0_*` instance.

## Possible extension

Several pillars arranged in a **ring for a 6-seat table**, which would introduce
**hand comparison** — and thus genuinely engage the **Dynamics / Attractor**
dimensions (the pot flows to the winning pillar).
