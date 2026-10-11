# WS-3 Addendum — The L cluster (GS-3, GS-4, findings F7–F8)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-11 (session of 2026-10-10)
**Target**: merge into `ontology/docs/_01_Worksite/WS-3/M2_Formulas_Review_with_Gs_README.md`
(§5 decision records, §6 findings, §8 next candidates, §9 changelog → v1.1.0, §10 status)
**Measured on**: HEAD `7d2cfb1` — re-measure at session start (head-over-memory)
**Replaces**: the draft "WS-13 — Audit of L" (folded here: an L audit is a sub-scope of
the Gs review, not a parallel worksite)
**Consumer**: WS-13 Structural Core — `m1:Component` needs an M2 parent carrying L

---

## Trigger

While modernising `Component` for the *Digital-Logic-Sim* poclet candidate, the only way
to give `m1:Component` an orientation toward the whole's Attractor was through an M2
parent carrying L (combo arguments are named concepts, never primitives — SC-1). None
carries L cleanly. Investigation shows L is **misallocated** across M2.

## Attested residue (HEAD)

`m3:bicephalous:typeL` — label *Localizability*, question *"Converging?"*, definition:
ordinal discrimination of the convergence direction toward an Attractor by successive
state comparison (Wiener, Ashby, Conant & Ashby, Powers). `m3:rejected_names` rejects
*"Origin"* because it *suggests a metric/spatial notion*.

| Concept | Formula at HEAD | L… |
|---|---|---|
| `Homeostasis` | `A × St × F \| L` | ✅ M3 sense |
| `Bifurcation` | `D × F \| L` | ✅ plausible |
| `Topology`, `Space` | `St \| L` | ❌ spatial reading (rejected by M3) |
| `Node`, `Capacity` | `St × It \| L` | ❌ spatial reading |
| `Component` | `St × It \| L` | ❌ — leaves M2 (WS-13) |
| `Regulation` | `A × St × F` | absent — L *is* cybernetic regulation |
| `Alignment` | `It × A × St` | absent — "progressively reduce discrepancy" |
| `Tropism` | `A × St × D × F` | absent — "orientation toward an Attractor" |
| `Convergence` | `F × D \| _^` / `F × D \| _$` | absent — converge/diverge encoded by poles |

L is present where its **rejected** reading applies and absent where its **definition**
applies. Michel's hypothesis: L is under-analysed; the name ("Localizability" = place)
drove the attributions more than the definition (convergence).

---

## GS-3 — `m2:Convergence` : `F × D | _^ / _$` → `A × F × D | L`

**Status**: DECIDED by Michel (2026-10-10). Execution pending.

**Attested residue.** L's definition is literally "converging vs diverging" — the two
poles `Convergence` already carries — yet L is absent from its formula. The concept that
should carry the primitive does not (§7.1 razor: an attested residue, not a "too basic"
impression).

**Michel's reading (option a).** Convergence integrates the Attractor: the point where
flows gather plays the role of the Attractor — a lens' focus included. Consistent with
TSCG usage: an Attractor is not necessarily a goal.

| Component | Role |
|---|---|
| `A` | the gathering point (focus, basin) |
| `F × D` | flows / trajectories that evolve (kept from HEAD) |
| `\| L` | ordinal discrimination: getting closer or farther |

**Open within GS-3**: do the poles `_^` / `_$` stay (the two values L discriminates) or
become redundant with L? Collision check (§7.3) to run before execution.

**Remaining work when executed**: rewrite `rdfs:comment` (convergence *toward an
Attractor*), collision check over M2 + M1 Core + M1 extensions (R3 normalised).

## GS-4 — L is the *sense* of tropism; `Tropism` is a consumer of L

**Status**: PRINCIPLE DECIDED by Michel (2026-10-10). Formula not yet decided.

L is the compass (discriminates direction, implies no movement); `m2:Tropism`
(`A × St × D × F`, ⊂ `Behavior`) is the walk (behaviour following a gradient). A tropism
without direction discrimination would be random motion — L appears constitutive.
Candidate formula: `A × St × D × F | L`. **Michel decides** (rule A: `Tropism ⊂ Behavior`
already conforms; adding `| L` keeps it conformant).

---

## F7 — L's label contradicts its own definition *(M3 wording — open)*

"Localizability" evokes place; M3 itself rejected the spatial reading. Probable root
cause of the misallocation. A tropism-family label ("Tropicity", "tropic orientation")
would match the definition — **not "Tropism"**, already an M2 concept (cross-layer
homonym, cf. WS-13 rule H). M3 change: Michel only.

## F8 — `Ss` label/comment drift *(M3 wording — open)*

Label **"Symbol — Stereopsic (Ss)"**, but the comment frames it as answering *"What is
the sign for?"* (Peirce / Saussure sign theory). The wording led to a misreading during
the 2026-10-10 session. Harden like F1.

---

## §8 additions — next candidates (the L work front)

- **Spatial usages**: `Topology`, `Space` (`St | L`), `Node`, `Capacity` (`St × It | L`) —
  for each, L justified in the M3 sense, or removed. Per R4 the `Node`/`Capacity`
  collision is not a defect in itself; examine it only as a signal.
- **Absences**: `Regulation`, `Alignment` — add L only where constitutive (§7.1).
- **`Bifurcation`**: L carrier, or consumer of `Convergence`?
- **Allocation rule for L** to write into the M2 README once the cluster is settled.

## §9 changelog line

| **1.1.0** | 2026-10-11 | L cluster opened (trigger: Digital-Logic-Sim / Component). GS-3 `Convergence = A × F × D \| L` DECIDED; GS-4 principle "L = sense, Tropism = consumer" DECIDED (formula pending). Findings F7 (L label) and F8 (Ss label/comment). Next candidates: spatial usages of L, absences, Bifurcation, allocation rule. |

## §10 status additions

| Item | State |
|---|---|
| GS-3 `Convergence` | DECIDED — execution pending (poles question open) |
| GS-4 `Tropism` | PRINCIPLE DECIDED — formula pending |
| F7 L label, F8 Ss wording | M3 wording repairs — open |
| L work front (§8) | Open |
