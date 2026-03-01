# M0_KindlebergerMinsky_README.md

**File:** `M0_KindlebergerMinsky.jsonld`  
**Version:** 1.0.0 · **Date:** 2026-02-28  
**Author:** Echopraxium with the collaboration of Claude AI  
**Domain:** Finance / Economics — Financial economics, Behavioral finance, Macroeconomics, Systemic risk  
**Status:** ACTIVE

---

## Executive Summary

The Kindleberger-Minsky poclet models the **5-phase speculative cycle** (Displacement → Boom → Euphoria → Distress → Revulsion) as identified by Hyman Minsky (*Financial Instability Hypothesis*) and systematized by Charles Kindleberger (*Manias, Panics and Crashes*, 1978).

**Key results:**

| Metric | Value |
|--------|-------|
| ASFID mean | **0.91** (Eagle-dominant) |
| REVOI mean | **0.82** |
| Epistemic gap δΘ | **0.09** (retrospectively strong, prospectively limited) |
| Primary M2 patterns | `m2:Propagation` + `m2:Narration` (both new in v15.9.0) |
| Secondary M2 patterns | 10 additional concepts |
| Historical instances | **6** (1637–2022) |
| Simulation markers | **30 cells** (6 instances × 5 phases) |
| Transdisciplinary domains | **6** |

This poclet is the **discovery context** for two new M2 GenericConcepts (`Propagation` and `Narration`) and the genesis of `M1_Economics.jsonld`.

---

## Table of Contents

1. [What is the Kindleberger-Minsky Cycle?](#1-what-is-the-kindleberger-minsky-cycle)
2. [ASFID Analysis](#2-asfid-analysis)
3. [REVOI Analysis](#3-revoi-analysis)
4. [The 5 Poles](#4-the-5-poles)
5. [Primary M2 Patterns](#5-primary-m2-patterns)
6. [Historical Instances](#6-historical-instances)
7. [Simulation Markers](#7-simulation-markers)
8. [Transdisciplinary Validation](#8-transdisciplinary-validation)
9. [M1_Economics Concepts](#9-m1_economics-concepts)
10. [Architectural Notes](#10-architectural-notes)

---

## 1. What is the Kindleberger-Minsky Cycle?

### Definition

> A recurrent 5-phase pattern in which a financial system transitions from stable equilibrium through speculative excess to systemic collapse, driven by credit expansion, leverage amplification, narrative contagion, and panic propagation.

### Theoretical Basis

| Author | Contribution |
|--------|-------------|
| **Hyman Minsky** (1986) | *Financial Instability Hypothesis* — stability is destabilizing; firms evolve from hedge → speculative → Ponzi finance |
| **Charles Kindleberger** (1978) | Systematized 5-phase cycle across historical crises; international contagion dimension |
| **Robert Shiller** (2019) | *Narrative Economics* — market narratives as causal forces (validates `m2:Narration`) |
| **Irving Fisher** (1933) | Debt-deflation theory — the mechanism of Revulsion phase amplification |
| **Walter Bagehot** (1873) | Lender of Last Resort principle — the `m2:Regulation` counter-force |

### System Architecture

```
DISPLACEMENT  →  BOOM  →  EUPHORIA  →  DISTRESS  →  REVULSION
    I⊗D           F⊗D⊗A      A⊗S         I⊗D⊗A        F⊗D
  [Event]      [Amplif.]   [Narration] [Bifurcation] [Propagation]

Narration arc:  "new paradigm" ──────────────────────→ "never again"
Propagation:    SubThreshold ──────────────────────→ Saturated
```

---

## 2. ASFID Analysis

### Scores

| Dimension | Score | Justification |
|-----------|-------|--------------|
| **A** Attractor | 0.92 | Three explicit attractors: speculative bubble (Euphoria), Minsky Moment bifurcation (Distress), post-crash equilibrium (Revulsion). R₀>1 during Boom, R₀<1 after Minsky Moment |
| **S** Structure | 0.85 | Interbank network topology, leverage ratios, market architecture. Slightly reduced by shadow banking opacity |
| **F** Flow | 0.92 | Credit flows (Boom), capital flight (Revulsion) — among the most measurable financial quantities |
| **I** Information | 0.90 | Market narratives, speculative signals central but partially opaque (Shiller: quantifiable via surveys/media) |
| **D** Dynamics | 0.95 | Best-formalized dimension: SIR-like epidemic models, Minsky phase taxonomy, quantitative chronologies |
| **Mean** | **0.91** | Eagle-dominant: Territory well-observed retrospectively |

### Eagle Eye formula by pole

```
Displacement:  I ⊗ D         — information shock + new dynamics
Boom:          F ⊗ D ⊗ A     — credit flux + acceleration + speculative attractor forming
Euphoria:      A ⊗ S          — attractor fully dominates structure
Distress:      I ⊗ D ⊗ A     — information reversal + dynamics reversal + attractor switch
Revulsion:     F ⊗ D          — capital flight flux + crash dynamics
```

---

## 3. REVOI Analysis

### Scores

| Dimension | Score | Justification |
|-----------|-------|--------------|
| **R** Representability | 0.85 | Framework well-encoded in literature, textbooks, policy papers. Shared vocabulary (Minsky Moment, displacement, euphoria) |
| **E** Evolvability | 0.78 | Extended by Shiller (narratives), network contagion models; contested as predictive tool |
| **V** Verifiability | 0.75 | **Retrospective**: strong (post-crisis). **Prospective**: very limited (bubble timing fundamentally unpredictable) |
| **O** Observability | 0.82 | Observable via: leverage ratios, credit spreads, VIX, margin debt, P/E, P/Rent, Tobin's Q |
| **Im** Interoperability | 0.88 | Framework applies across crises (1637, 1929, 1987, 2000, 2008, 2022) and crisis types |
| **Mean** | **0.82** | Map-strong but V limited by fundamental forecasting opacity |

### Epistemic Gap

```
δΘ = |ASFID_mean − REVOI_mean| = |0.91 − 0.82| = 0.09
```

**Interpretation:** Legitimate Eagle-dominant gap. Territory phenomena (phases, credit dynamics, panic propagation) are well-observed. The gap reflects the fundamental reflexivity of financial markets — acknowledged by Kindleberger himself: *"I can explain every past crisis; I cannot predict the next one."*

---

## 4. The 5 Poles

### Overview

| Pole | ASFID Formula | Primary M2 | ASFID Mean | Dominant signal |
|------|--------------|------------|------------|-----------------|
| **Displacement** | I ⊗ D | `m2:Event` | 0.79 | Exogenous shock → new information |
| **Boom** | F ⊗ D ⊗ A | `m2:Amplification` | 0.88 | Credit flux + leverage acceleration |
| **Euphoria** | A ⊗ S | `m2:Narration` | 0.90 | Speculative attractor + belief network peak |
| **Distress** | I ⊗ D ⊗ A | `m2:Bifurcation` | 0.92 | Minsky Moment — attractor switches |
| **Revulsion** | F ⊗ D | `m2:Propagation` | 0.91 | Panic cascade + credit freeze |

### Pole 1 — Displacement

Exogenous shock displaces the economy from equilibrium. New profit opportunities appear. Information asymmetry between early movers and majority. The Narration begins: a new semantic network forms around "unprecedented opportunity." Dynamics are positive but slow.

*Secondary M2:* `m2:Event` · `m2:Trigger` · `m2:Bifurcation` (first state change from equilibrium) · `m2:Narration` (onset)

### Pole 2 — Boom (Credit Expansion)

Easy credit fuels investment. **Minsky's key insight:** stability is destabilizing — the very absence of crisis encourages risk-taking. Pro-cyclical positive feedback: asset price rise → collateral rise → more credit → more investment → price rise. Leverage ratios increase. Narration in Supercritical propagation regime.

*Leverage mechanism:* `m2:Amplification` (gain > 1) + `m2:FeedbackLoop` (positive)

*Secondary M2:* `m2:Cascade` · `m2:Network` · `m2:Propagation` · `m2:Narration` · `m2:Threshold`

### Pole 3 — Euphoria (Overtrading / Peak)

*"This time is different."* Speculative attractor fully dominates (A⊗S). Narration at maximum density: internally coherent (V high), widely shared (Im high). New participants enter (retail, taxi drivers). Prices decouple from fundamental value. Insiders quietly exit. Price velocity peaks then shows first deceleration. Volume at maximum.

*Key markers:* Reinhart & Rogoff "This Time Is Different" linguistic signature. `m2:Narration` attractorType=Collapse already structurally implied.

*Secondary M2:* `m2:Oscillator` · `m2:Identity` · `m2:Emergence` · `m2:Memory`

### Pole 4 — Distress (Minsky Moment)

**Bifurcation:** first major default or forced seller reveals systemic fragility. Information reversal (I). Panic propagation begins — R₀ crosses 1. Narration Collapse attractor becomes manifest. Dynamics reverse sharply. Volume spikes (distressed selling). Central Bank may activate as Lender of Last Resort.

*Minsky Moment:* term coined by Paul McCulley (PIMCO, 1998). The moment when over-leveraged investors are forced to sell good assets to pay down debt, depressing prices further.

*Secondary M2:* `m2:Trigger` · `m2:Threshold` · `m2:Propagation` (onset) · `m2:Narration` (collapse transition)

### Pole 5 — Revulsion (Panic & Crash)

Panic fully propagates (Propagation → Saturated regime). Forced selling cascade: each liquidation depresses prices → triggers more margin calls → more liquidations. Credit freeze: interbank lending halts (Im ≈ 0). Narration Collapse attractor fully reached: "Never again." Fisher (1933) Debt Deflation spiral. LOLR intervention (Bagehot) may truncate.

*Secondary M2:* `m2:Cascade` · `m2:Dissipation` · `m2:Regulation` (LOLR) · `m2:Convergence`

---

## 5. Primary M2 Patterns

### `m2:Propagation` — Financial Panic as Network Propagation

| TSCG dimension | Financial mapping |
|---------------|-------------------|
| **S** | Interbank exposure network (bilateral credit lines, CDS, repo) |
| **I** | Panic signal content (counterparty default risk, liquidity shortage) |
| **A** | Minsky Moment threshold (R₀ = 1) and saturation (full panic) |
| **D** | Panic dynamics: hours to days in acute phase |
| **F** | Capital flight, margin calls, repo withdrawal between nodes |
| **V** | Panic signal fidelity (high: legitimate risk; low: pure contagion) |
| **Im** | Bank-to-bank compatibility: credit lines, CDS contracts, common exposures |

**SIR epidemic analogy:**

```
S (Susceptible) = Solvent but exposed banks
I (Infected)    = Banks under panic run / margin call
R (Recovered)   = Restructured / bailed-out / failed banks
R₀ equivalent  = Leverage ratio × exposure concentration / resolution speed
```

**Propagation regime by phase:**

| Phase | Panic R₀ | Regime |
|-------|----------|--------|
| Boom | < 0.5 | SubThreshold (optimism dominant) |
| Euphoria | < 0.3 | SubThreshold (invincibility narrative) |
| Distress | 0.3 → 3.0 | **Critical → Supercritical** (Minsky Moment: R₀ = 1) |
| Revulsion | 3.0 → 0.5 | **Supercritical → Saturated → SubThreshold** |

### `m2:Narration` — Collective Belief as Semantic Network Morphism

| TSCG dimension | Financial mapping |
|---------------|-------------------|
| **S** | Market belief network topology (analyst consensus, media, social networks) |
| **I** | Collective belief content (speculative thesis, valuation narrative) |
| **D** | Temporal unfolding across 5 Minsky phases |
| **F** | Narrative flux: financial media, analyst reports, social proof |
| **V** | Narrative coherence (maximum in Euphoria; zero in Revulsion) |
| **R** | Narrative encodability (Shiller: surveys, media analysis, Google Trends) |
| **A** | Collapse attractor — Minsky Moment telos implicit in Euphoria structure |
| **Im** | Shared market interpretation framework (Bloomberg, CNBC, analyst consensus) |

**Narrative arc across phases:**

| Phase | Dominant narrative node |
|-------|------------------------|
| Displacement | *"Unprecedented opportunity — early mover advantage"* |
| Boom | *"New paradigm — traditional valuation metrics obsolete"* |
| Euphoria | *"This time is different — [asset] always goes up"* |
| Distress | *"Isolated problem — contained, buy the dip"* |
| Revulsion | *"Total fraud — I will never invest in [asset] again"* |

**Key distinction — Propagation vs Narration in this poclet:**

> The panic **Propagates** through the interbank network (faithful copy of panic signal, V > 0).  
> The collective belief is **Narrated** — it transforms across phases toward the Collapse attractor.  
> These are co-occurring patterns operating on different substrates simultaneously.

---

## 6. Historical Instances

### Summary Table

| Instance | Asset | Displacement start | Peak price | Trough | Drawdown from peak |
|----------|-------|-------------------|-----------|--------|-------------------|
| **Tulip Mania** | Semper Augustus bulb (guilders) | 50 (1634) | 6,700 (Feb 3, 1637) | ~10 (May 1637) | **-99.9%** |
| **South Sea Bubble** | South Sea Co. stock (GBP) | 100 (1711) | 1,050 (Jun 24, 1720) | 100 (Dec 1720) | **-90.5%** |
| **Wall Street 1929** | DJIA (USD) | 95 (1922) | 381 (Sep 3, 1929) | 41 (Jul 8, 1932) | **-89.2%** |
| **Dot-com 2000** | NASDAQ Composite (USD) | 700 (1993) | 5,132 (Mar 10, 2000) | 1,114 (Oct 9, 2002) | **-78.3%** |
| **GFC 2008** | S&P 500 (USD) / Case-Shiller | 1,100 (2001) | 1,565 S&P (Oct 2007) | 667 (Mar 9, 2009) | **-57.4%** |
| **Crypto 2021-22** | Bitcoin BTC (USD) | 3,500 (2019) | 69,044 (Nov 10, 2021) | 15,599 (Nov 2022) | **-77.5%** |

### Bubble Amplitude (Peak / Displacement-start price)

```
Tulip Mania   ████████████████████████████████████████████████  ×134
Crypto 2021   ████████████████████  ×19.7
Dot-com       ███████  ×7.3
South Sea     ██████████  ×10.5
Wall St 1929  ████  ×4.0
GFC 2008      ██  ×1.8 (housing index — harder to measure)
```

### Total Cycle Durations

| Instance | Displacement → Peak | Peak → Trough | Total |
|----------|--------------------:|---------------:|------:|
| Tulip Mania | ~28 months | ~4 months | ~32 months |
| South Sea | ~9 years | ~6 months | ~10 years |
| Wall Street 1929 | ~8 years | ~33 months | ~11 years |
| Dot-com | ~7 years | ~30 months | ~9 years |
| GFC 2008 | ~7 years | ~18 months | ~9 years |
| Crypto 2021 | ~34 months | ~12 months | ~46 months |

---

## 7. Simulation Markers

### Schema

Each pole × instance cell contains four structured objects for simulation use:

```
dateRange          → start, end, duration
assetReference     → name, unit, priceStart, priceEnd, pricePeak, priceTrough, changePercent
transactionVolume  → indicator, valueStart, valueEnd, unit, trend
dynamics           → regime, priceVelocity (%/month), acceleration (sign), volatility, dominantForce
```

### Price Velocity Profile (%/month) — Comparative

| Phase | Tulip | South Sea | Wall St | Dot-com | GFC | Crypto |
|-------|------:|----------:|--------:|--------:|----:|-------:|
| Displacement | +15 | +0.3 | +1.2 | +1.5 | +0.6 | +7 |
| Boom | +35 | +10 | +2.0 | +3.5 | +1.1 | +50 |
| Euphoria | +100 | +60 | +1.5 | +6.0 | +0.3 | +4 |
| Distress | -500 | -15 | -4 | -8 | -2 | -10 |
| Revulsion | -90 | -30 | -3 | -3 | -8 | -8 |

*Unit: % per month. Distress velocities are acute-phase peaks.*

### Acceleration Sign — Phase × Instance

| Phase | Tulip | South Sea | Wall St | Dot-com | GFC | Crypto |
|-------|-------|-----------|---------|---------|-----|--------|
| Displacement | + | ≈0 | + | + | + | + |
| Boom | ++ | + | + | ++ | + | ++ |
| Euphoria | +→0 | +→0 | − | +→0 | − | ± |
| Distress | −−− | −− | −− | −− | −− | −− |
| Revulsion | −−−→0 | −−− | −−− | −− | −−− | −−− |

### Normalized Volume Profile (Displacement = 1.0)

| Phase | Tulip | South Sea | Wall St | Dot-com | GFC | Crypto |
|-------|------:|----------:|--------:|--------:|----:|-------:|
| Displacement | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| Boom | 5 | 5 | 2.5 | 10 | 2.5 | 5 |
| Euphoria | 20 | 10 | 4 | 25 | 1.3 | 20 |
| Distress | 0.5 | 5 | 6 | 20 | 2 | 10 |
| Revulsion | 0.01 | 0.1 | 0.5 | 8 | 0.3 | 2 |

### Phase Duration (normalized to total cycle)

| Phase | Min | Typical | Max |
|-------|----:|--------:|----:|
| Displacement | 5% | 20% | 50% |
| Boom | 10% | 25% | 40% |
| Euphoria | 3% | 15% | 25% |
| Distress | 1% | 10% | 20% |
| Revulsion | 10% | 30% | 60% |

### Propagation R₀ Equivalent by Phase

| Phase | Panic R₀ range | Opportunity narrative R₀ |
|-------|---------------|--------------------------|
| Displacement | < 0.3 | 0.5 → 1.0 |
| Boom | < 0.5 | 1.2 → 2.0 |
| Euphoria | < 0.3 | 2.0 → 5.0 |
| Distress | 0.3 → 3.0 | < 0.3 |
| Revulsion | 3.0 → 0.5 | < 0.1 |

---

## 8. Transdisciplinary Validation

The Kindleberger-Minsky 5-phase structure recurs across 6 domains:

| Domain | Instance | Propagation (Im) | Narration (A) |
|--------|----------|------------------|---------------|
| **Finance / Economics** | 2008 GFC, 1929, 2000, 1637 | Interbank exposure network | Minsky Moment collapse |
| **Ecology** | Predator-prey bust, invasive species collapse | Ecosystem trophic network | Population collapse (overshoot) |
| **Technology** | Gartner Hype Cycle, tech shakeouts | Network effects / compatibility | Trough of Disillusionment |
| **Sociology** | Moral panics (Cohen), social movements | Social network ties (Granovetter) | Institutionalization or collapse |
| **Epidemiology** | SIR epidemic cycle (S→I→R ≡ Boom→Euphoria→Revulsion) | Host compatibility (R₀) | Herd immunity / resolution |
| **Military** | War cycles: mobilization → peak → collapse | Alliance network | Exhaustion / armistice attractor |

---

## 9. M1_Economics Concepts

This poclet is the discovery context for `M1_Economics.jsonld`. Concepts extracted from pole analysis:

| M1 Concept | Used in pole(s) | Characterizes M2 |
|------------|----------------|-----------------|
| `m1econ:ExogenousShock` | Displacement | `m2:Event` · `m2:Trigger` |
| `m1econ:InformationAsymmetry` | Displacement · Euphoria | `m2:Information` · `m2:Observer` |
| `m1econ:ProfitOpportunity` | Displacement | `m2:Attractor` |
| `m1econ:CreditExpansion` | Boom | `m2:Flow` · `m2:Amplification` |
| `m1econ:LeverageCycle` | Boom | `m2:Amplification` · `m2:FeedbackLoop` |
| `m1econ:SpeculativePremium` | Boom · Euphoria | `m2:Gradient` · `m2:Threshold` |
| `m1econ:MarketSentiment` | Boom · Euphoria | `m2:Narration` · `m2:Signal` |
| `m1econ:AssetBubble` | Euphoria · Revulsion | `m2:Attractor` · `m2:Oscillator` |
| `m1econ:FundamentalValue` | Euphoria | `m2:Attractor` (target reference) |
| `m1econ:MinskyCrisis` | Distress | `m2:Bifurcation` · `m2:Threshold` |
| `m1econ:SystemicRisk` | Distress · Revulsion | `m2:Emergence` · `m2:Propagation` |
| `m1econ:CreditCrunch` | Distress · Revulsion | `m2:Flow` (reversal) · `m2:Regulation` |
| `m1econ:DebtDeflation` | Revulsion | `m2:Cascade` · `m2:Dissipation` |
| `m1econ:FinancialContagion` | Revulsion | `m2:Propagation` (M1 instance) |

---

## 10. Architectural Notes

### Discovery Context

This poclet was identified during M2 analysis as requiring **two new GenericConcepts** that did not yet exist in M2:

- **`m2:Propagation`** — financial panic cannot be modeled by existing Cascade (linear) or Network (static substrate). The 1→N branching pattern with threshold attractor and copy fidelity required a dedicated M2.
- **`m2:Narration`** — the transformation of collective market beliefs across phases is a semantic network morphism irreducible to Signal (1:1), Pattern (static), or Transformation (content-agnostic).
- **`m2:Duplication`** — identified as missing M2 prerequisite for Propagation.

### Bicephalous Balance

```
Eagle Eye (Territory): ASFID = 0.91  ████████████████████  Strong
Sphinx Eye (Map):      REVOI  = 0.82  ████████████████      Moderate
Epistemic Gap δΘ:              0.09   ░░░                   Legitimate
```

The V=0.75 (Verifiability) score is the key constraint: post-crisis analysis is powerful; pre-crisis prediction remains fundamentally limited by market reflexivity (Soros) and the observer effect.

### TSCG Layer Dependencies

```
M3  Genesis Space  (ASFID ⊗ REVOI dimensions)
 ↓
M2  GenericConcepts v15.9.0
    m2:Propagation  ⊗⇒(Cascade, Duplication, Network)
    m2:Narration    ⊗⇒(Transformation, Representation, Relation)
    m2:Bifurcation  (Minsky Moment)
    + 10 secondary concepts
 ↓
M1  M1_Economics.jsonld
    ExogenousShock · CreditExpansion · LeverageCycle · SpeculativePremium
    MarketSentiment · AssetBubble · FundamentalValue · MinskyCrisis
    SystemicRisk · CreditCrunch · DebtDeflation · FinancialContagion
 ↓
M0  M0_KindlebergerMinsky.jsonld  ← THIS FILE
    5 poles × 6 historical instances × 4 simulation marker objects
```

---

## Related Files

| File | Layer | Relation |
|------|-------|---------|
| `M3_GenesisSpace.jsonld` | M3 | ASFID ⊗ REVOI dimensional space |
| `M2_GenericConcepts.jsonld` | M2 | All M2 patterns used; Propagation + Narration introduced here |
| `M1_Economics.jsonld` | M1 | Domain extension — all M1 concepts used in poles |
| `M1_CoreConcepts.jsonld` | M1 | Core transdisciplinary concepts |
| `M2_GenericConcepts_README.md` | docs | Narration + Propagation + Duplication documentation |
| `TSCG_Smart_Prompt_v15_8_0.md` | docs | TSCG session context |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
