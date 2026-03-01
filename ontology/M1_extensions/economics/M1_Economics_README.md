# M1_Economics_README.md

**File:** `M1_extensions/economics/M1_Economics.jsonld`  
**Version:** 1.0.0 · **Date:** 2026-02-28  
**Author:** Echopraxium with the collaboration of Claude AI  
**Domain:** Finance / Economics — Financial economics, Behavioral finance, Macroeconomics, Systemic risk  
**Status:** ACTIVE — First TSCG domain extension in the Finance / Economics field

---

## Overview

`M1_Economics.jsonld` is the domain-specific extension of the TSCG framework for **financial and economic systems**. It contains 14 concepts extracted from the systematic analysis of the `M0_KindlebergerMinsky` poclet, covering the full 5-phase speculative cycle from Displacement to Revulsion.

Every concept in this file:
- Is **domain-specific** — valid in Finance / Economics but not claimed to be universal
- **Characterizes** one or more M2 GenericConcepts (`m2:characterizedBy`)
- Is **anchored** to one or more Kindleberger-Minsky phases (`m1econ:minskyPhase`)
- Carries a **tensor formula** inherited or refined from its M2 parent(s)

### Architectural Position

```
M3  Genesis Space  (ASFID ⊗ REVOI — 10 fundamental dimensions)
 ↓
M2  GenericConcepts  (81 universal patterns — m2:Propagation, m2:Narration, m2:Bifurcation…)
 ↓
M1  M1_Economics.jsonld  ← THIS FILE
    KnowledgeField: Economics (NOUN) + Financial (ADJECTIVE)
    14 domain concepts across 5 concept families
 ↓
M0  M0_KindlebergerMinsky.jsonld  (5 poles × 6 historical instances)
```

### Discovery Context

All 14 concepts were identified during the `M0_KindlebergerMinsky` poclet analysis (2026-02-28). The poclet simultaneously triggered the creation of two new M2 GenericConcepts — `m2:Propagation` and `m2:Narration` — which became the primary M2 patterns that M1 Economics concepts characterize. See `M0_KindlebergerMinsky_README.md` for the full poclet documentation.

---

## KnowledgeField

### `m1econ:Economics` (NOUN)

`Economics` is registered as a `m2:KnowledgeField` NOUN instance — the complete epistemic field.

| Property | Value |
|----------|-------|
| σ_mean | **0.72** |
| Alignment angle θ | ~35° |
| Maturity level | **Developing** |
| ASFID dominant | Dynamics · Flow · Attractor |
| REVOI dominant | Observability · Representability |

**Maturity breakdown:** Microeconomics and financial metrics are mature (σ~0.85). Macroeconomic prediction and systemic risk forecasting remain contested (σ~0.45). The fundamental epistemic constraint is **market reflexivity** (Soros): the observer affects the observed market, creating an irreducible forecasting limit.

### `m1econ:Financial` (ADJECTIVE)

Disciplinary qualifier derived from `m1econ:Economics`, used in `KnowledgeFieldMetaCombo` patterns. Example:

```
Financial ⊙ Propagation  →  m1econ:FinancialContagion
Financial ⊙ Narration    →  m1econ:MarketSentiment
Financial ⊙ Bifurcation  →  m1econ:MinskyCrisis
```

---

## Concept Families

### Concept Map by Minsky Phase

```
DISPLACEMENT          BOOM                 EUPHORIA              DISTRESS              REVULSION
─────────────         ──────────────────   ──────────────────    ──────────────────    ──────────────────
ExogenousShock   →    CreditExpansion  →   SpeculativePremium →  InformationAsymmetry→ CreditCrunch
ProfitOpportunity     LeverageCycle        FundamentalValue      MinskyCrisis          DebtDeflation
                       MarketSentiment      AssetBubble           SystemicRisk          FinancialContagion
```

### Family 1 — Cycle Concepts (2 concepts)

Domain-generic concepts spanning all phases.

---

### Family 2 — Credit Dynamics (3 concepts)

Concepts governing the credit expansion mechanism of the Boom phase.

---

### Family 3 — Valuation (3 concepts)

Concepts governing asset pricing, speculative premium, and the Euphoria peak.

---

### Family 4 — Crisis Mechanics (3 concepts)

Concepts governing the Distress phase and systemic fragility.

---

### Family 5 — Collapse Dynamics (3 concepts)

Concepts governing the Revulsion phase, panic propagation, and macro amplification.

---

## Concept Reference

### `m1econ:ExogenousShock`
**Family:** Cycle · **Phase:** Displacement  
**M2:** `m2:Event` · `m2:Trigger` · `m2:Bifurcation`  
**Formula:** `I ⊗ D`

An external event that displaces an economic system from equilibrium by creating new information or changing the opportunity structure. Not predictable from within the system. Must be significant enough to alter profit expectations for a large class of assets.

**Typology:**

| Type | Example |
|------|---------|
| Technological | Railways, internet, blockchain |
| Financial | Deregulation, new instruments (MBS, CDO) |
| Geopolitical | War end, trade opening |
| Monetary | Central bank rate change |

**Historical instances:** Tulip (Dutch luxury speculation, 1634) · South Sea (monopoly grant, 1711) · Wall St (post-WWI industrialization, 1922) · Dot-com (WWW commercialization, 1993) · GFC (Fed 1% + securitization, 2001) · Crypto (DeFi + Bitcoin halving, 2019)

---

### `m1econ:ProfitOpportunity`
**Family:** Cycle · **Phase:** Displacement → Boom  
**M2:** `m2:Attractor` · `m2:Gradient` · `m2:Information`  
**Formula:** `A ⊗ I ⊗ D`

The new or underexploited configuration that offers expected returns above equilibrium. The attractor activating the Displacement phase. Early movers capture genuine value; late movers arrive when speculative premium has already exceeded it.

**Lifecycle:**

| Stage | Condition |
|-------|-----------|
| Genuine | Displacement: real economic value exists |
| Amplified | Boom: value amplified by narrative beyond fundamentals |
| Fictitious | Euphoria: pure speculative game |
| Exposed | Revulsion: value reassessed, often below genuine level |

---

### `m1econ:CreditExpansion`
**Family:** Credit · **Phase:** Boom  
**M2:** `m2:Flow` · `m2:Amplification` · `m2:FeedbackLoop`  
**Formula:** `F ⊗ D ⊗ A`

Rapid growth in credit volume, primarily driven by low interest rates, financial innovation, or reduced lending standards. The primary fuel of the Boom phase. Pro-cyclical positive feedback: asset prices rise → collateral rises → borrowing capacity rises → more purchases → prices rise.

**Minsky finance types:**

| Type | Condition | Stability |
|------|-----------|-----------|
| Hedge | Cash flows cover debt service + principal | Stable |
| Speculative | Cash flows cover interest only — must refinance | Fragile |
| Ponzi | Cash flows cover neither — needs rising prices | Unstable |

**Key metrics:** Credit growth > GDP growth · Private credit/GDP ratio · Bank leverage ratios · Loan-to-value ratios · Commercial paper outstanding

---

### `m1econ:LeverageCycle`
**Family:** Credit · **Phase:** Boom → Revulsion  
**M2:** `m2:Amplification` · `m2:FeedbackLoop` · `m2:Oscillator`  
**Formula:** `F ⊗ D ⊗ A`  
**Theoretical basis:** Geanakoplos (2010), Adrian & Shin (2010)

The pro-cyclical dynamic in which leverage ratios expand during booms and contract violently during busts. `Leverage = Asset Value / Equity`. A 10:1 leveraged position loses all equity on a 10% price decline.

**Amplification mechanisms:**

```
Upswing:   Price↑ → Collateral↑ → Borrowing↑ → Purchases↑ → Price↑  (accelerator)
Downswing: Price↓ → Margin call → Forced sale → Price↓ → Margin call (cascade)
```

**Historical leverage ratios at peak:**
- 1929: Margin accounts 10:1
- 2007: Investment banks 30:1–40:1 (Bear Stearns, Lehman)
- 2021: Crypto DeFi platforms offering 100:1 on perpetual futures

---

### `m1econ:MarketSentiment`
**Family:** Credit · **Phase:** Boom → Euphoria → Distress → Revulsion  
**M2:** `m2:Narration` · `m2:Signal` · `m2:Propagation`  
**Formula:** `S ⊗ I ⊗ D ⊗ F ⊗ V ⊗ R ⊗ A ⊗ Im`

The aggregate psychological disposition of market participants toward an asset class — the primary carrier of `m2:Narration` in financial markets. Shiller (2019): sentiment narratives are **causal**, not merely epiphenomenal, in driving market prices.

**Sentiment spectrum:**

| Sentiment | Minsky Phase | Narrative |
|-----------|-------------|-----------|
| Extreme Greed | Euphoria | "This time is different" |
| Greed | Boom | "Don't miss the opportunity — FOMO" |
| Neutral | Pre-Displacement | Equilibrium |
| Fear | Distress | "This is serious — de-risking" |
| Extreme Fear | Revulsion | "Never again" |

**Measurable indicators:** CNN Fear & Greed Index · AAII Survey · Put/Call ratio · Google Trends (Shiller methodology) · Social media sentiment · VIX

---

### `m1econ:SpeculativePremium`
**Family:** Valuation · **Phase:** Boom → Euphoria (peak) → Revulsion (collapse)  
**M2:** `m2:Gradient` · `m2:Threshold` · `m2:Attractor`  
**Formula:** `A ⊗ I ⊗ D`

```
SpeculativePremium = MarketPrice − FundamentalValue
```

Zero at equilibrium; grows monotonically during Boom and Euphoria; collapses during Revulsion. Keynes *beauty contest*: investors buy what others will buy, independent of fundamentals — a self-referential game inflating the premium beyond any fundamental anchor.

**Historical peak premiums:**

| Instance | Metric | Value |
|----------|--------|-------|
| Tulip 1637 | Price vs annual income | 10× skilled craftsman annual income |
| Dot-com 2000 | Shiller CAPE | 44× (historical mean ~16×) |
| Housing 2006 | Price/Rent | 3σ above 1975-2000 baseline |
| Crypto 2021 | Price vs production cost | $69K vs ~$10K cost-of-mining |

---

### `m1econ:FundamentalValue`
**Family:** Valuation · **Phase:** Reference across all phases  
**M2:** `m2:Attractor` · `m2:Invariant`  
**Formula:** `A ⊗ I`

The intrinsic value derived from expected future cash flows, discounted at a risk-adjusted rate. The *true long-run attractor* from which SpeculativePremium is measured. Empirically, market prices mean-revert toward fundamental value over 7–10 year horizons (Shiller CAPE data 1871–present).

**Valuation methods:** DCF · Gordon Growth Model · Comparable Multiples (P/E, EV/EBITDA) · Asset-based (NAV)

**Epistemic note:** Fundamental value is itself uncertain and model-dependent. This uncertainty is exploited by speculative narratives ("traditional metrics don't apply in a new paradigm") — a key mechanism of the Euphoria phase.

---

### `m1econ:AssetBubble`
**Family:** Valuation · **Phase:** Euphoria + retrospective identification in Revulsion  
**M2:** `m2:Attractor` · `m2:Emergence` · `m2:Oscillator`  
**Formula:** `A ⊗ S ⊗ F ⊗ D`

A sustained, self-reinforcing deviation of asset prices above fundamental value — an **emergent property** irreducible to any single market participant. Definitively identified only after its collapse: a fundamental observability limitation (REVOI V=0.75 in the Kindleberger-Minsky poclet).

**Diagnostic thresholds:**

| Metric | Bubble signal |
|--------|--------------|
| Shiller CAPE | > 30 (2000: 44; 1929: 32) |
| Housing Price/Rent | > 2σ above long-run mean |
| NYSE Margin Debt | > 3% of GDP |
| Tobin's Q | > 1.5 (equities > physical replacement cost) |

**Observability paradox:** Clearly visible in retrospect; cannot be identified with certainty in real time. Central bank interventions to "prick the bubble" carry their own crash risk.

---

### `m1econ:InformationAsymmetry`
**Family:** Crisis · **Phase:** Displacement (maximal) · Distress (counterparty opacity)  
**M2:** `m2:Information` · `m2:Observer` · `m2:Gradient`  
**Formula:** `I ⊗ S ⊗ A`  
**Theoretical basis:** Akerlof (1970 Nobel, "lemons problem")

A condition in which different market participants have access to different information about asset values, risks, or system state. Maximal at Displacement (insiders aware, majority not) and during Distress (banks cannot assess counterparty solvency — the 2008 LIBOR freeze: "who is solvent?").

**Phase-specific manifestations:**

| Phase | Form |
|-------|------|
| Displacement | Insiders vs uninformed majority |
| Boom/Euphoria | Sophisticated investors quietly exiting while retail enters |
| Distress | Counterparty solvency unknown ("lemons" problem in interbank market) |
| Revulsion | Fraud revelations — Ponzi schemes exposed ("when the tide goes out" — Buffett) |

---

### `m1econ:MinskyCrisis`
**Family:** Crisis · **Phase:** Distress  
**M2:** `m2:Bifurcation` · `m2:Threshold` · `m2:Propagation`  
**Formula:** `I ⊗ D ⊗ A`

The critical phase transition — the *Minsky Moment* — in which the financial system bifurcates from speculative equilibrium to crash dynamics. Term coined by Paul McCulley (PIMCO, 1998). At this moment, panic Propagation R₀ crosses 1.

**Trigger typology:**

| Type | Examples |
|------|---------|
| Internal | Ponzi unit exposure (rising prices needed to service debt) |
| Institutional default | Lehman 2008, LTCM 1998 |
| Regulatory action | Bubble Act 1720, margin rule changes 1929 |
| Geopolitical | Oil embargo, war |
| Fraud revelation | Ponzi scheme collapse |

**Physics analogy:** First-order phase transition (discontinuous) — liquid → gas at boiling point. The financial system crosses a critical threshold from stable (speculative) to unstable (crash) phase.

**Historical Minsky Moments:**

| Date | Event |
|------|-------|
| Feb 3, 1637 | Haarlem tulip auction fails — first buyers refuse contracts |
| Oct 24, 1929 | Black Thursday — 12.9M NYSE shares, margin call cascade |
| Sep 15, 2008 | Lehman bankruptcy → money market funds "break the buck" |
| May 9–12, 2022 | Terra UST depeg → $40B destroyed in 72h |

---

### `m1econ:SystemicRisk`
**Family:** Crisis · **Phase:** Distress → Revulsion  
**M2:** `m2:Emergence` · `m2:Propagation` · `m2:Network`  
**Formula:** `S ⊗ I ⊗ A ⊗ D ⊗ F ⊗ V ⊗ Im`

The risk of collapse of an **entire financial system** — an emergent property of network interconnectedness and correlated exposures, **irreducible** to the sum of individual institution risks.

**Transmission channels:**

| Channel | Mechanism |
|---------|-----------|
| Direct exposure | Bank A defaults → Bank B holds Bank A bonds → Bank B weakened |
| Common asset | All banks hold MBS → MBS price falls → all simultaneously weakened |
| Funding contagion | Bank A run → depositors fear Bank B → Bank B run (pure panic) |
| Liquidity spiral | Price fall → margin call → fire sale → price fall (Adrian & Shin 2010) |

**Measurable indicators:** SRISK (NYU Stern) · CoVaR · TED spread (LIBOR − T-bill) · LIBOR-OIS spread · CDS spreads on major banks

**Regulatory response:** G-SIB surcharges (Basel III) · Stress testing (CCAR/DFAST) · Resolution planning (living wills) · Central clearing (CCPs)

---

### `m1econ:CreditCrunch`
**Family:** Collapse · **Phase:** Distress → Revulsion  
**M2:** `m2:Flow` · `m2:Propagation` · `m2:Regulation`  
**Formula:** `F ⊗ D ⊗ Im`

A sudden and severe reduction in credit availability — the financial market manifestation of `m2:Propagation` in the Revulsion phase. Panic about creditworthiness spreads through the interbank network (Im), causing credit collapse even for creditworthy borrowers (V degrades: panic fidelity deteriorates — legitimate borrowers confused with defaulters).

**Interaction with LeverageCycle:** Credit crunch → firms cannot refinance → forced asset sales → price falls → collateral falls → more credit denied → vicious cycle.

**Indicators:**

| Indicator | Crisis threshold |
|-----------|-----------------|
| TED spread | > 100bps (2008 peak: 460bps) |
| LIBOR-OIS spread | > 50bps (2008 peak: 360bps) |
| Senior Loan Officer Survey | % tightening > 50% |
| Bank lending growth | Negative |

**LOLR response:** Bagehot principle — Central Bank lends freely at penalty rate against good collateral to break the credit crunch.

---

### `m1econ:DebtDeflation`
**Family:** Collapse · **Phase:** Revulsion  
**M2:** `m2:Cascade` · `m2:Dissipation` · `m2:FeedbackLoop`  
**Formula:** `F ⊗ D ⊗ A`  
**Theoretical basis:** Irving Fisher (1933)

A self-reinforcing economic contraction in which falling asset prices increase the real burden of debt, leading to further defaults, more sales, further price falls, and deeper contraction. The primary amplification mechanism transforming a financial crisis into a prolonged depression.

**Fisher's 9-step mechanism:**

```
1. Over-indebtedness → distress selling
2. Credit money contraction (bank money destroyed)
3. Price level falls (deflation)
4. Net worth falls → business failures
5. Profits fall → output and trade decline
6. Pessimism and loss of confidence
7. Hoarding → velocity slows → further deflation
8. Real interest rate rises → further distress
9. → Back to step 1 (vicious cycle)
```

**Fisher's paradox:** The more debtors repay, the more they owe in real terms if prices fall faster than debt is liquidated.

**Historical instances:**

| Instance | Outcome |
|----------|---------|
| USA 1929-33 | CPI -25%, DJIA -89%, 25% unemployment |
| Japan 1990-2010 | "Lost Decade" — zombie banks, balance sheet recession |
| 2008-09 | Near-deflation averted by QE + TARP |

**Policy response:** QE (Bernanke's "printing press") · Debt restructuring (Brady bonds) · Fiscal stimulus (Keynesian multiplier)

---

### `m1econ:FinancialContagion`
**Family:** Collapse · **Phase:** Distress → Revulsion  
**M2:** `m2:Propagation`  
**Formula:** `S ⊗ I ⊗ A ⊗ D ⊗ F ⊗ V ⊗ Im`

The M1 Economics instantiation of `m2:Propagation`. Cross-institutional or cross-market spread of financial distress through a financial network: each node that "receives" the panic signal becomes a new emitter.

**TSCG Propagation mapping:**

| Dimension | Financial meaning |
|-----------|------------------|
| S | Interbank exposure network (bilateral credit, CDS, repo) |
| I | Distress signal content (counterparty default risk) |
| A | Minsky Moment threshold R₀=1 (below: contained; above: systemic) |
| D | Contagion velocity (hours to days in acute phase) |
| F | Capital withdrawal, margin calls, repo non-renewal |
| V | Signal fidelity (high: legitimate risk; low: pure panic) |
| Im | Bilateral exposure compatibility (credit lines, CDS contracts) |

**Distinction from DebtDeflation:**

| | FinancialContagion | DebtDeflation |
|--|-------------------|---------------|
| Mechanism | Network-level spread (who infects whom) | Macro-level amplification (all simultaneously) |
| Speed | Hours to days | Months to years |
| Role | Ignites the crisis | Sustains and deepens it |
| M2 | `m2:Propagation` | `m2:Cascade` + `m2:Dissipation` |

**Historical cascade chains:**

| Crisis | Contagion sequence |
|--------|-------------------|
| 1997-98 Asian crisis | Thai baht → Korean won → Russian default → LTCM |
| 2008 GFC | Lehman → money market funds → commercial paper → global credit freeze (24h) |
| 2022 Crypto | Terra/LUNA → Celsius → Three Arrows → Voyager → FTX |

---

## M2 Coverage Summary

| M2 GenericConcept | M1 Economics instances |
|-------------------|----------------------|
| `m2:Propagation` | FinancialContagion · SystemicRisk · MarketSentiment |
| `m2:Narration` | MarketSentiment |
| `m2:Bifurcation` | MinskyCrisis |
| `m2:Amplification` | CreditExpansion · LeverageCycle |
| `m2:FeedbackLoop` | CreditExpansion · LeverageCycle · DebtDeflation |
| `m2:Attractor` | FundamentalValue · AssetBubble · ProfitOpportunity · SpeculativePremium |
| `m2:Emergence` | SystemicRisk · AssetBubble |
| `m2:Flow` | CreditExpansion · CreditCrunch |
| `m2:Cascade` | DebtDeflation |
| `m2:Event` + `m2:Trigger` | ExogenousShock |
| `m2:Information` | InformationAsymmetry |
| `m2:Oscillator` | LeverageCycle · AssetBubble |

---

## Minsky Phase Coverage Matrix

| Concept | Disp. | Boom | Euph. | Dist. | Revuls. |
|---------|:-----:|:----:|:-----:|:-----:|:-------:|
| ExogenousShock | ● | | | | |
| ProfitOpportunity | ● | ● | | | |
| CreditExpansion | | ● | | | |
| LeverageCycle | | ● | | | ● |
| MarketSentiment | | ● | ● | ● | ● |
| SpeculativePremium | | ● | ● | | ● |
| FundamentalValue | ● | ● | ● | ● | ● |
| AssetBubble | | | ● | | ● |
| InformationAsymmetry | ● | | | ● | |
| MinskyCrisis | | | | ● | |
| SystemicRisk | | | | ● | ● |
| CreditCrunch | | | | ● | ● |
| DebtDeflation | | | | | ● |
| FinancialContagion | | | | ● | ● |

---

## Related Files

| File | Layer | Relation |
|------|-------|---------|
| `M3_GenesisSpace.jsonld` | M3 | ASFID ⊗ REVOI dimensional space |
| `M3_EagleEye.jsonld` | M3 | ASFID dimension definitions |
| `M3_SphinxEye.jsonld` | M3 | REVOI dimension definitions |
| `M2_GenericConcepts.jsonld` | M2 | All M2 patterns characterized by M1 Economics |
| `M2_GenericConcepts_README.md` | docs | Narration, Propagation, Duplication documentation |
| `M1_CoreConcepts.jsonld` | M1 | Core transdisciplinary concepts |
| `M0_KindlebergerMinsky.jsonld` | M0 | Discovery context poclet — 5 poles × 6 instances |
| `M0_KindlebergerMinsky_README.md` | docs | Full poclet documentation with simulation markers |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| **v1.0.0** | 2026-02-28 | Initial version. 14 concepts extracted from M0_KindlebergerMinsky poclet. KnowledgeField Economics (NOUN) + Financial (ADJECTIVE). Discovery context: M2 Propagation + Narration + Duplication (M2 v15.9.0). |

---

*TSCG Framework — Transdisciplinary System Construction Game*  
*Author: Echopraxium with the collaboration of Claude AI*
