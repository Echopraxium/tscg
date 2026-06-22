# Business Model Canvas (BMC) — TSCG SystemicFramework

**Author:** Echopraxium with the collaboration of Claude AI
**Version:** 1.0.0 — 2026-06-20
**Type:** `m3:SystemicFramework`
**File:** `instances/systemic-frameworks/Bmc/M0_Bmc.jsonld`
**M1 Extension:** `ontology/M1_extensions/business-modeling/M1_BusinessModeling.jsonld`

---

## Overview

The Business Model Canvas (Osterwalder & Pigneur, 2010) is a strategic management framework that describes how an organization **creates, delivers, and captures value** through 9 interconnected building blocks. It is the most widely adopted business modeling tool in the world, with 5M+ registered canvases on Strategyzer and adoption across 45+ languages.

As a TSCG SystemicFramework, the BMC is analyzed through the **bicephalous lens**:
- **Eagle Eye (ASFID / Territory):** captures the operational dynamics of real business systems
- **Sphinx Eye (REVOI / Map):** evaluates the BMC canvas itself as a representational and analytical tool

**SpectralClass:** `Coherent` (δ₁ = 0.031 — deep interior of Coherent zone)
**FocalClass:** `SlightlyHyperopic` (SFE = 0.813) — the BMC is **map-dominant**: its Sphinx Eye strength (REVOI = 0.874) slightly exceeds its Territory coverage (ASFID = 0.830), reflecting its nature as a visual strategic canvas rather than a dynamic simulation tool.

---

## System Description

The BMC organizes any business system into **9 building blocks** arranged in a canonical topology:

```
┌─────────────────────────────────────────────────────────────────────┐
│  KEY           │  KEY          │ VALUE        │ CUSTOMER   │ CUSTOMER│
│  PARTNERS      │  ACTIVITIES   │ PROPOSITION  │ RELATIONS  │ SEGMENTS│
│  (KP)          │  (KA)         │    (VP)      │   (CR)     │  (CS)   │
│                ├───────────────┤              ├────────────┤         │
│                │  KEY          │              │ CHANNELS   │         │
│                │  RESOURCES    │              │   (CH)     │         │
│                │  (KR)         │              │            │         │
├────────────────┴───────────────┴──────────────┴────────────┴─────────┤
│         COST STRUCTURE (C$)          │    REVENUE STREAMS (RS)       │
└──────────────────────────────────────┴───────────────────────────────┘
```

**Left side (Infrastructure):** KP + KA + KR + C$ — *how* value is produced
**Center (Value):** VP — *what* value is created
**Right side (Customer):** CS + CR + CH + RS — *for whom* and *how* value is captured

The BMC's fundamental equation: **Value Created = Value Delivered = Value Captured** (when the model is coherent). Any misalignment between the three zones signals a strategic tension or model inconsistency.

---

## TSCG Analysis

### ASFID State (Territory / Eagle Eye)

| Dimension | Score | BMC Block Mapping | Justification |
|---|---|---|---|
| **A** Attractor | 0.85 | Value Proposition | VP defines the convergence state toward which customers and revenues are attracted. Network effects in platform models create super-attractor dynamics. |
| **S** Structure | 0.90 | 9-block architecture | Formal canonical topology with explicit directional relationships (infrastructure → value → customer). Highest ASFID score: the BMC IS structural. |
| **F** Flow | 0.78 | Channels + Revenue Streams + Cost Structure | Value flow (VP → CH → RS) and cost flow (KR + KA + KP → C$) well-articulated. Slightly lower: quantification requires domain-specific metrics not native to the canvas. |
| **It** Information | 0.82 | Value Proposition + Customer Segments | VP is an informational construct by definition. Customer Segments define the perceptual map. Less formalized than VSM's variety calculus. |
| **D** Dynamics | 0.80 | Customer Relationships + Business Model Mutations | Mutations (Netflix×3, AWS×2, Michelin×2) demonstrate rich temporal dynamics. BMC is primarily a static snapshot tool — dynamic evolution requires external scenario analysis. |
| **ASFID Mean** | **0.830** | | |

### REVOI State (Map / Sphinx Eye)

| Dimension | Score | Justification |
|---|---|---|
| **R** Representability | 0.90 | Universal visual standard: single-page canvas layout reproduced identically across 45+ languages, thousands of publications, and 5M+ registered canvases. Highest REVOI score. |
| **E** Evolvability | 0.88 | Highly extensible: Lean Canvas (Ash Maurya), Value Proposition Canvas (Osterwalder), BMC+ (social enterprise), Digital Twin BMC. Compatible with adjacent frameworks (TRIZ, VSM, OKR, Balanced Scorecard). |
| **V** Verifiability | 0.85 | Validated across thousands of companies (Strategyzer database, HBS case studies). BMC pre-analysis correlates with startup success in Y Combinator cohorts. Causal validation remains correlational, not experimental. |
| **O** Observability | 0.87 | 9 blocks directly observable and instrumentable via customer interviews, financial data, and partner contracts. BMC workshops are a standard observation methodology. |
| **Im** Interoperability | 0.87 | Compatible with TRIZ (innovation trigger), VSM (viability check), Lean Startup (pivot = block replacement), OKR, Balanced Scorecard. No W3C standard but de-facto universal adoption achieved. |
| **REVOI Mean** | **0.874** | |

### Epistemic Gap

| Metric | Value | Interpretation |
|---|---|---|
| δ₁ = \|ASFID − REVOI\| / √2 | **0.031** | Deep Coherent zone — Eagle Eye and Sphinx Eye are well-balanced |
| SpectralClass | **Coherent** | δ₁ ∈ [0, 0.05) |
| focalBias | **+0.044** | Positive = Map slightly dominant (Hyperopic) |
| stereopsicDepth | **0.85** | T=0.90, K=0.85, Ss=0.80, L=0.85 |
| SFE (focalScore) | **0.813** | `stereopsicDepth × (1 − |focalBias|)` |
| FocalClass | **SlightlyHyperopic** | REVOI > ASFID by a small margin |

**Interpretation:** The BMC's slight REVOI dominance is a **designed feature, not a gap**. The canvas was intentionally created as a Map tool (Sphinx Eye): it was designed for strategic *representation* rather than operational *simulation*. This distinguishes it from VSM (more Territory-balanced, δ₁=0.057, OnCriticalLine) and TRIZ (strongly Map-dominant, REVOI=0.96). The BMC sits in the optimal zone for a strategic communication and alignment tool.

---

## Components

The BMC has 9 building blocks, each mappable to primary ASFID dimensions:

| Block | Acronym | ASFID Primary | TSCG Role | M1 KFCC |
|---|---|---|---|---|
| Value Propositions | VP | A + It | Attractor center — convergence point of the entire system | `ValueProposition` |
| Customer Segments | CS | It + S | Information boundary — defines which signals are relevant | `CustomerSegment` |
| Channels | CH | F | Structural flow paths — VP delivery infrastructure | — |
| Customer Relationships | CR | D + A | Temporal dynamics — acquisition/retention/churn cycles | — |
| Revenue Streams | RS | F + A | Economic flow capture — quantified VP attractor pull | `RevenueStream` |
| Key Activities | KA | F + D | Internal operational flows — resource-to-VP transformation | — |
| Key Resources | KR | S + A | Structural substrate — assets on which KA operates | — |
| Key Partnerships | KP | S + It | Extended structure — boundary-crossing capabilities | — |
| Cost Structure | C$ | F + A | Cost flows + sustainability attractor | — |

**Fundamental StrategicTension:** VP (maximize value) ↔ C$ (minimize cost) — the primary creative antagonism that drives business model innovation.

---

## M1 KnowledgeFieldConceptCombos (M1_BusinessModeling.jsonld)

9 KFCCs were created for the BMC analysis:

| KFCC | Structural Grammar | Description |
|---|---|---|
| `ValueProposition` | `A × It` | VP as attractor + informational construct |
| `CustomerSegment` | `It × St` | Information boundary + structural coupling |
| `RevenueStream` | `F × A` | Economic flow + attractor pull |
| `CrossSubsidy` | `A × F × D` | Dual-polarity amplification — one segment funds another |
| `PlatformDuality` | `St × F × D \| Im` | Two-sided network — synergy between interdependent segments |
| `BusinessModelPattern` | `St × It \| R` | Structural invariant — reusable business archetype |
| `StrategicTension` | `D × A \| St` | Productive antagonism between BMC blocks |
| `BusinessModelMutation` | `D × F × St` | Non-incremental reconfiguration — bifurcation point |
| `VerticalIntegration` | `F × St × A` | Value chain internalization — KP → KA + KR |

**Key distinctions:**
- `CrossSubsidy` ≠ `Cascade` — requires explicit dual-polarity amplification, not simple sequential flow
- `PlatformDuality` = M1 instantiation of `m2:Synergy` — platform value exceeds sum of individual sides
- `BusinessModelMutation` requires ≥3 BMC blocks reconfigured simultaneously

---

## GenericConcepts Mobilized

**Total: 12 GenericConcepts** across 4 ASFID families + cross-dimensional

| Family | GenericConcepts |
|---|---|
| Attractor | `m2:Attractor`, `m2:Equilibrium` |
| Structure | `m2:Structure`, `m2:Modularity`, `m2:Boundary` |
| Flow | `m2:Flow`, `m2:Cascade`, `m2:Propagation`, `m2:Process` |
| Information | `m2:Information` |
| Dynamics | `m2:Dynamics`, `m2:Transformation`, `m2:Feedback` |
| Cross-dimensional | `m2:Amplification`, `m2:Synergy`, `m2:Polarity`, `m2:Emergence` |

**Stereopsic GenericConcepts (3):** `m2:Synergy`, `m2:Emergence`, `m2:Amplification`
These require simultaneous Eagle Eye + Sphinx Eye activation:
- `m2:Synergy` → PlatformDuality: the two-sided network IS different from the operator's perspective vs. the analyst's canvas
- `m2:Emergence` → Network effects: platform lock-in is not predictable from individual block analysis
- `m2:Amplification` → CrossSubsidy: dual-polarity amplification visible only when both Territory and Map views are active simultaneously

---

## Real-World Case Studies (15)

### Business Model Mutations

**Netflix — 3 successive mutations (1997→2007→2013):**

| State | Year | Model | VP | Revenue | Blocks Changed |
|---|---|---|---|---|---|
| 0 | 1997 | DVD-by-mail | No late fees, large catalog, home delivery | Monthly subscription $15.99 | — |
| 1 | 2007 | Streaming platform | Instant unlimited, any device | Tiered subscription $8.99-$22.99 | VP, KA, KP, RS, KR |
| 2 | 2013 | Content studio + streaming | Original exclusive content + catalog | Global subscription (190 countries) | VP, KA, KP, RS, KR |

Each mutation changes ≥4 blocks and shifts the attractor state qualitatively. The 2013 mutation introduces VerticalIntegration (content production internalized).

**AWS — cost center to profit center (2000→2006):**
Internal IT infrastructure for amazon.com → elastic public cloud utility. The most radical mutation in the corpus: transforms a cost center into a profit center. CrossSubsidy inverted: AWS profits now subsidize Amazon retail's logistics.

**Michelin — product to outcome service (pre-1999→1999+):**
Tire asset sale → Pay-Per-Km fleet contract. VP shifts from asset to outcome. VerticalIntegration downstream into IoT fleet analytics. Classic `BusinessModelMutation` + `VerticalIntegration` combination.

### Platform and CrossSubsidy Patterns

| Company | Pattern | Key Mechanism |
|---|---|---|
| **Spotify** | CrossSubsidy + PlatformDuality | Free tier (ads) subsidized by €10.99/month premium (~30% conversion). Listeners ↔ Artists/Labels. |
| **Airbnb** | PlatformDuality | Hosts ↔ Guests. No real estate KeyResources — pure trust infrastructure orchestration. 3%+12-14% fees. |
| **Visa** | PlatformDuality + CrossSubsidy | Cardholders (free, subsidized) ↔ Merchants (interchange ~1.8%). 4.3B cards × 100M+ merchant locations. |
| **Apple** | VerticalIntegration + Ecosystem | Apple Silicon (chip design), 500+ retail stores, App Store 30% commission. Multi-attractor basin via ecosystem lock-in. |
| **Google** | CrossSubsidy (attention economy) | Free search subsidized by $224B/year advertising (2023). Users = product; advertisers = customers. |
| **Amazon** | PlatformDuality + VerticalIntegration | Buyers ↔ Third-party sellers (58% of units). FBA (Fulfillment by Amazon) + Amazon Ads: vertical capture at 3 stages. |
| **IKEA** | BusinessModelPattern (cost innovation) | Customer self-assembly = free labor subsidy. StrategicTension resolved: low cost + high design via flat-pack. Vertical integration into forestry. |
| **Uber** | PlatformDuality + StrategicTension | Drivers ↔ Riders. StrategicTension mediated by dynamic pricing (surge). Network density effect: more drivers → shorter waits → more riders. |

---

## Key Insights

**1. The BMC as structural grammar**
The 9 blocks are not arbitrary categories — they correspond to the fundamental ASFID/REVOI dimensions with remarkable precision. Structure (S) maps to the 9-block architecture itself. Attractor (A) maps to the VP. Flow (F) maps to Channels + Revenue Streams + Cost flows. Information (It) maps to the VP signal + Customer Segment perception. Dynamics (D) maps to Customer Relationships + mutation timelines.

**2. Platform duality as the signature of Synergy**
The most economically significant business models in the corpus (Visa, Google, Amazon, Airbnb, Apple, Spotify, Uber) are all multi-sided platforms. This is not coincidental: `m2:Synergy` — value that exceeds the sum of individual components — is most powerfully expressed when two distinct customer populations interact through a shared infrastructure. The BMC's strength is making this invisible synergy visible.

**3. CrossSubsidy as designed asymmetry**
CrossSubsidy (`m2:Amplification` with dual polarity) is the mechanism by which platforms bootstrap network effects. The subsidized side attracts volume; the volume creates value for the capture side; the capture revenue funds the subsidy. This is a designed self-reinforcing loop — the inverse of vicious cycles.

**4. BusinessModelMutation as phase transition**
The Netflix case illustrates that business model mutations are not gradual evolutions but **phase transitions**: the system crosses a bifurcation point beyond which the previous attractor basin is no longer accessible. After 2007, Netflix could not return to DVD-only. After 2013, returning to a pure licensing model would require dismantling production infrastructure worth billions. Mutations are **irreversible structural transformations** — exactly the dynamics described by `m2:Transformation`.

**5. SlightlyHyperopic as designed feature**
The BMC's slight Map dominance (SFE = 0.813, FocalClass = SlightlyHyperopic) reflects its design intent: it is a **canvas for strategic alignment**, not a dynamic simulator. This distinguishes it from VSM (designed for operational viability diagnosis, more Territory-balanced) and TRIZ (designed for systematic innovation, strongly Map-dominant). Each framework's focal class reflects its epistemic purpose.

---

## Transdisciplinary Analogies

| Business Concept | TSCG Analog | Domain |
|---|---|---|
| Value Proposition | Attractor basin | Physics / Dynamical Systems |
| Platform Network Effects | Emergence | Complex Systems |
| Business Model Mutation | Phase Transition | Thermodynamics |
| CrossSubsidy | Amplification with dual polarity | Signal Processing / Electronics |
| Key Partnerships extending firm boundary | Symbiosis | Biology / Ecology |
| Revenue Stream recurring vs transactional | Limit cycle vs pulse dynamics | Nonlinear Dynamics |
| Customer Segment boundary | Ecological niche boundary | Ecology |
| Strategic Tension (VP vs C$) | Polarity / Yin-Yang | Philosophy / Systems Theory |

The BMC's transdisciplinary depth is validated by the fact that each of its 9 blocks maps cleanly to a TSCG GenericConcept family — a feature shared only by the most epistemically robust frameworks in the corpus (VSM, TRIZ, Fire Triangle).

---

## Comparison with Other SystemicFrameworks

| Framework | ASFID | REVOI | δ₁ | SpectralClass | FocalClass | Note |
|---|---|---|---|---|---|---|
| **BMC** | 0.830 | 0.874 | 0.031 | Coherent | SlightlyHyperopic | Map-dominant by design |
| **VSM** | 0.928 | 0.848 | 0.057 | OnCriticalLine | SlightlyMyopic | Territory-dominant — operational simulator |
| **TRIZ** | 0.880 | 0.960 | 0.057 | OnCriticalLine | Hyperopic | Strongly Map-dominant — systematic innovation |

The three SystemicFrameworks cover complementary epistemic positions: TRIZ (innovation generation), BMC (business design), VSM (organizational viability). Together they form a complete strategic toolkit.

---

## References

**Primary:**
- Osterwalder, A. & Pigneur, Y. (2010). *Business Model Generation*. Wiley.
- Osterwalder, A., Pigneur, Y., Bernarda, G. & Smith, A. (2014). *Value Proposition Design*. Wiley.

**Case Studies:**
- Netflix: Hastings, R. & Meyer, E. (2020). *No Rules Rules*. Penguin.
- AWS: Bryar, C. & Carr, B. (2021). *Working Backwards*. St. Martin's Press.
- Michelin: Vargo, S.L. & Lusch, R.F. (2004). "Evolving to a New Dominant Logic for Marketing." *Journal of Marketing*, 68(1), 1–17.
- Platform Economics: Parker, G., Van Alstyne, M. & Choudary, S. (2016). *Platform Revolution*. Norton.

**TSCG:**
- `ontology/M1_extensions/business-modeling/M1_BusinessModeling.jsonld` — 9 KFCCs
- `ontology/M1_Domains.jsonld` — BusinessModeling domain entry (v1.4.0)
- `instances/systemic-frameworks/Bmc/M0_Bmc.jsonld` — this instance
