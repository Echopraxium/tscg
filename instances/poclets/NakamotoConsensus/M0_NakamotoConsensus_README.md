# Nakamoto Consensus — TSCG Poclet

**Author:** Echopraxium with the collaboration of Claude AI  
**Version:** 15.10.1  
**Date:** 2026-03-23  
**Ontology file:** `M0_Poclet_NakamotoConsensus.jsonld`  
**Simulation:** `NakamotoConsensus_sim.html`

---

## Overview

The **Nakamoto Consensus** models Bitcoin's proof-of-work as a **Prigogine dissipative structure** maintained far from thermodynamic equilibrium, via a **Ginzburg-Landau 1D formalism**. It achieves exceptional TSCG coverage: ASFID 5/5, REVOI 5/5, SpectralClass **Coherent** (δ₁ = 0.030).

This poclet also motivated three **M3 architectural discoveries** (F ≥ 0 axiom relaxation, F as morphic dimension, F_potential / F_active distinction) and five new M2 candidates (Entropy, Stase, Coherence, Processor, Transducer) plus four Combos (Inertia, Potentialization, Absorbing State, Topological Defect).

**Source paper:**  
Ranaora & Yii (2026) — *"A Phenomenological Statistical-Physics Framework for Distributed Consensus"*  
Information Physics Institute, Sydney  
DOI: [10.5281/zenodo.19160047](https://zenodo.org/records/19160047)

---

## System Description

The Nakamoto Consensus is the distributed agreement mechanism underpinning Bitcoin. Miners compete to solve a cryptographic puzzle (Proof-of-Work). The network adopts the longest valid chain, creating a global attractor. Ranaora & Yii show this maps exactly onto a 1D Ginzburg-Landau field theory: hash power acts as effective temperature, chain coherence is the order parameter, and forks are topological defects (KT vortices).

---

## Master Equations

| Name | Formula | Interpretation |
|---|---|---|
| Effective temperature | `k_B · T_eff(t) = P_net(t) · τ_L` | Hash power → thermodynamic temperature |
| Critical block size | `V_B,crit ≈ C_eff · (τ_B/Γ_c − τ₀)` | Max stable block size before propagation delay dominates |
| Probabilistic finality | `P_reorg(z) = (q/p)^z = exp(−z/ξ)` | Fork probability after z confirmations |
| Correlation length | `ξ⁻¹ = ln(p/q)` | Fork persistence depth |
| Nakamoto action | `S_PoW(t₁,t₂) = τ_B · ∫ P_net(t) dt` | Analogue of least-action principle |

---

## TSCG Analysis

### ASFID State (Territory / Eagle Eye 🦅)

| Dim | Score | Justification |
|-----|-------|---------------|
| **A** Attractor | 0.92 | Longest-chain rule = global consensus attractor; Ginzburg-Landau order parameter |
| **S** Structure | 0.89 | Merkle-tree chain + P2P gossip topology; Table I structural homology |
| **F** Flow | 0.95 | Hash computation as continuous F_active; F_potential in mining pools (F ≥ 0 discovery) |
| **I** Information | 0.91 | Nonce entropy, block propagation, difficulty bits as information encoding |
| **D** Dynamics | 0.93 | Real-time difficulty adjustment, fork race, irreversible PoW entropy production |

**Mean ASFID:** 0.920

### REVOI State (Map / Sphinx Eye 🦁)

| Dim | Score | Justification |
|-----|-------|---------------|
| **R** Representability | 0.91 | Full Ginzburg-Landau 1D formalism; Table I isomorphism dictionary |
| **E** Evolvability | 0.83 | Framework extendable to PoS, DAG (lower score: extensions require new formalisms) |
| **V** Verifiability | 0.95 | 5 explicit falsifiable predictions (§VII.D of source paper) |
| **O** Observability | 0.89 | All parameters observable on-chain (hash rate, block time, fork rate) |
| **Im** Interoperability | 0.85 | Direct connection with Cryptocalc; bridges 4 transdisciplinary domains |

**Mean REVOI:** 0.890

### Epistemic Gap

```
δ₁ = |ASFID_vec − REVOI_vec| / √5 ≈ 0.030
SpectralClass: Coherent  [0.00, 0.05)
```

The near-zero gap confirms that the Ginzburg-Landau formalism provides a genuine Territory model (not just a metaphor), with high verifiability and observability.

---

## Components

| Component | ASFID contribution | Description |
|---|---|---|
| Mining Pool (Honest) | F, D, A | Continuous hash computation → F_active; drives chain growth toward attractor |
| Mining Pool (Attacker) | F, D | Competing hash computation; fork initiator when ≥ q fraction |
| P2P Network | S, I | Block gossip topology; propagation delay τ_L |
| Blockchain | S, A | Merkle chain structure + longest-chain attractor |
| Difficulty Adjustment | D, I, A | Regulation loop every 2016 blocks; keeps τ_B ≈ 600 s |
| Transaction | I, F | Information flux through mempool → block |
| Fork | S, A, I | Topological defect — resolved by attractor (longest chain) |

---

## GenericConcepts Mobilized (14)

### Atomic (10)

| Concept | Tensor | Family | Role |
|---|---|---|---|
| Dissipation | `F⊗D` | Energetic | Hash computation as irreversible energy degradation |
| Entropy | `F⊗I⊗D` | Energetic | PoW entropy; source of irreversibility (Feynman) |
| Attractor | `A` | Dynamic | Longest-chain rule as global order parameter |
| Process | `D⊗F` | Dynamic | Block mining as temporally unfolded hash search |
| Cascade | `S⊗I⊗A⊗D⊗F` | Dynamic | Chain growth as amplifying 5D cascade |
| Threshold | `D⊗I` | Dynamic | Difficulty adjustment mechanism |
| Regulation | `A⊗I⊗D` | Dynamic | Difficulty regulation loop (τ_B target) |
| Signal | `I⊗F` | Informational | Block propagation through P2P gossip |
| Network | `S⊗I` | Structural | P2P topology with gossip protocol |
| Coherence | `A⊗S⊗I⊗R⊗O` | Structural/Ontol. | Consensus as bicephalous coherence |

### Combos (4) — new M2 candidates from this session

| Concept | Formula | Tensor | Role |
|---|---|---|---|
| Inertia | `⊗⇒(Memory, Entropy)` | `S⊗F⊗I⊗D` | Accumulated PoW defines attack cost |
| Potentialization | `⊗⇒(Activation, Process)` | `A⊗D⊗F` | F=0 → F_active transition (mining startup) |
| Absorbing State | `⊗⇒(Stase, Entropy)` | `S⊗A⊗F⊗I⊗D` | Transaction finality (6-confirmation rule) |
| Topological Defect | `⊗⇒(Incoherence, Invariant)` | `S⊗A⊗I⊗R⊗O` | Persistent fork as KT vortex |

---

## Key Insights

1. **F ≥ 0 axiom** — This poclet forced the relaxation of the TSCG M3 axiom `F ≠ 0` to `F ≥ 0`: chain stasis (F=0) is a valid fundamental state (no new blocks), while active mining is F_active, and mining pool reserves are F_potential.

2. **F as morphic dimension** — F is the sole ASFID dimension that structurally requires a source→target relation: `F ∈ Mor(Cat_M3) ∩ Ob(Cat_M3)`. All M2 concepts containing F are natural candidates for entity/morphism duality.

3. **Causal chain** — The poclet reveals a coherent irreversibility chain: `F_active → [Dissipation] → Entropy → [Memory] → Inertia → [maximal] → Absorbing State`.

4. **Topological defect** — A blockchain fork is a KT vortex: local Incoherence protected by a discrete topological invariant (chain index n ∈ ℤ), non-eliminable by continuous deformation.

5. **Falsifiability** — 5 explicit falsifiable predictions in §VII.D of the source paper make this one of the highest-V poclets in the catalogue (V = 0.95).

---

## Transdisciplinary Isomorphisms (Table I)

### Statistical Physics ↔ Nakamoto

| Statistical Physics | Bitcoin / Nakamoto |
|---|---|
| Temperature k_B·T | k_B·T_eff = P_net · τ_L |
| Order parameter φ | Chain coherence (consensus level) |
| Phase transition | Fork resolution / consensus achievement |
| Dissipative structure | Mining pool dynamics (Prigogine) |
| Ginzburg-Landau field | Network hash-state field |
| Thermal fluctuation | Mining variance / block time jitter |
| Correlation length ξ | Fork persistence depth |
| Vortex (KT transition) | Persistent chain fork |
| Entropy S | PoW entropy S_PoW |
| Least-action S[φ] | Nakamoto action S_PoW(t₁,t₂) |

### Biology ↔ Nakamoto

| Biology | Bitcoin / Nakamoto |
|---|---|
| Quorum sensing | 51% majority rule |
| Immune memory | Accumulated PoW (Inertia) |
| Absorbing state | Finalized transaction (6+ confirmations) |
| Phenotypic stasis | Chain stasis — F=0 |
| Dissipation | Continuous hash computation |

---

## References

- Ranaora & Yii (2026) — *A Phenomenological Statistical-Physics Framework for Distributed Consensus: Phase Transitions and Thermodynamic Stability* — Information Physics Institute, Sydney — [https://zenodo.org/records/19160047](https://zenodo.org/records/19160047) — DOI: 10.5281/zenodo.19160047
- Nakamoto, S. (2008) — *Bitcoin: A Peer-to-Peer Electronic Cash System*
- Prigogine, I. (1978) — *From Being to Becoming* (dissipative structures)
- Feynman, R. P. (1965) — *The Feynman Lectures on Physics*, Vol. I, Ch. 46 (irreversibility and entropy)
- TSCG Framework v15.10.1 — [https://github.com/Echopraxium/tscg](https://github.com/Echopraxium/tscg)
