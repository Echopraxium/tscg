# PokerHand3D — TSCG Exercise

**Domain:** Combinatorics / Card Games — **no existing M1 domain** (adjacent to `GameTheory` and `ComputerScience`, but neither fits: see §5)
**Difficulty:** Intermediate
**Natural simulation:** 3D (BabylonJS) — a circular pillar with the ten hand categories browsable weak → strong

> **This is a *worked* exercise.** A **sample workflow run** (M0 model + simulation)
> lives in `workflow_run_sample/`, deliberately marked as a spoiler, because it exists
> to **illustrate the end-to-end TSCG workflow** — it is *one* example resolution, **not
> a definitive answer key** (TSCG has no single correct model). Do it yourself first if
> you want the practice.

## 1. The system in one paragraph
A poker hand is five cards. The rules sort every possible hand into **ten categories**
— high card, pair, two pair, three of a kind, straight, flush, full house, four of a
kind, straight flush, royal flush — ordered from weakest to strongest. That order is
**explained by rarity**: a flush beats a straight because there are fewer flushes. Each
category is really a **geometric/combinatorial pattern** over two axes: the **rank**
(A,2,…,K) and the **suit** (♣♥♦♠). One structural subtlety carries the whole exercise:
the **Ace is dual-valued** (low or high), so the rank ordering used for straights is
*almost cyclic* — A-2-3-4-5 (the wheel) and 10-J-Q-K-A (Broadway) are both straights,
yet **K-A-2-3-4 is illegal**. The Ace is doubled, not identified.

## 2. Suggested scope (minimal + complete)
The **52-card deck** as (rank × suit), the **ten combination types** read as figures,
the **doubled-Ace rule**, and the **rarity → strength** ordering. Model the
**classification** of hands — *not* the game of poker (no betting, no opponents, no
strategy). Be honest that this is a deliberately **structural / classificatory** poclet:
it maps the space of hands, it does not simulate play. That honesty is part of the
lesson (compare Logic Gates: Information-dominant, weak Attractor).

## 3. ASFID sketch (Territory / Eagle Eye)
- **A** (Attractor): **weak** — the weak→strong ranking is an *ordering*, not a state the
  system converges to. Be honest about this. The nuance worth discussing: the royal flush
  is the **maximal element** of the ranking, a top of a hierarchy, not a dynamical attractor.
- **S** (Structure): **dominant** — the pillar's topology (a circle of 4 suit-edges, 14
  rank-floors, the **doubled Ace**), and the geometric figures (line, triangle, square,
  snake, stacked disks).
- **F** (Flow): **near-absent** — nothing is transferred; it is a static classification.
- **I** (Information): **strong** — classifying a hand is a **coding** act; the whole
  poclet is a **representation** (a Map) of a combinatorial **Territory**; and the
  **rarity/probability** of each type is pure Information.
- **D** (Dynamics): **near-absent** — no temporal evolution, no feedback. This is a
  **Structure + Information**, **Map-dominant** poclet (REVOI ≫ ASFID).

## 4. GenericConcepts — a-priori hypotheses (confirm with Claude)
- **Hierarchy** — the weak→strong ordering of the ten categories (grounded in rarity).
- **Topology** — the rank axis is **cyclic in spirit but cut** at the Ace (why the wheel
  exists yet K-A-2-3-4 does not). *This is the central lesson: Map ↔ Territory fidelity.*
- **Symmetry** — the four suits as an interchangeable set (order-4); every figure is
  invariant under suit permutation **except the flush**.
- **Pattern / Representation** — a hand read as the **figure** its five points form (the
  figure *is* the definition: a square literally is four-of-a-kind).
- **Signature** — the card (or sub-figure) that **names or breaks the tie**.
- Verify every one against `M2_GenericConcepts.jsonld` at HEAD.

## 5. Domain question
- **Existing M1 extension?** **No** combinatorics / card-games domain at HEAD →
  **new-domain finding**. Two adjacencies exist and neither fits: **`GameTheory`** names
  the *strategic* layer (moves, payoffs, equilibria) — which this poclet does **not**
  touch; **`ComputerScience`** could host combinatorial classification, but broadly. The
  honest move for a first instance is to use **descriptive strings** (`"Combinatorics"`,
  `"Card Games"`) and **flag `Combinatorics` as a candidate domain** — to be opened only
  when several unrelated instances justify it (the anti-overfitting guardrail). *The very
  fact that no domain fits cleanly is the point of the exercise.*
- **Possible M2 candidate?** A tempting one: **"an element identified for value but not
  for adjacency"** (the doubled Ace — same card at both ends of the axis, yet adjacency is
  cut across it). It might recur (cyclic-but-seamed orderings, a clock with a forbidden
  wrap). Flag it, but hold the rule: a concept needs attested residue across ≥6
  independent domains before it earns admission.

## 6. Source documentation
Standard **5-card poker hand rankings** and their **exact frequencies** over
C(52,5) = **2,598,960** hands (Wikipedia: "Poker probability", "List of poker hands"). A
teaching bonus: every classification is **exactly checkable by hand** against the rules —
so the Map can be judged against a Territory the reader can verify first-hand (free
**Verifiability**, the V of REVOI). The doubled-Ace rule (wheel valid, K-A-2-3-4 invalid)
is itself a small, checkable fact the model must honour.

## 7. Simulation hint (3D, BabylonJS)
Build a **circular pillar**: four vertical **suit-edges**, fourteen **rank-floors** with
the **Ace doubled** (bottom floor = wheel only). Draw each card as a point (rank × suit),
and render the current combination as its **figure** — a cylinder (pair), a triangle
(trips), a square (quads), a **snake** (straight), stacked **disks** of one suit (flush) —
with the **determining card** caged in an octahedron. Add a **strength gauge inverse to
frequency**, so rarity *explains* the ranking rather than the ranking being asserted. Let
the user **browse weak → strong** and **rotate freely**. Make the gap between *the
ordering* and *why* (rarity) visible — and let the doubled Ace make **K-A-2-3-4 visibly
impossible** (you would have to cross the whole height of the pillar to get there).
