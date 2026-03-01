# Kindleberger-Minsky Financial Crisis Cycle — TSCG Simulation

**File**: `kindleberger_minsky_sim.py`  
**Version**: 1.11.0  
**Date**: 2026-03-01  
**Author**: Echopraxium with the collaboration of Claude AI  
**Poclet**: `M0_KindlebergerMinsky.jsonld`  
**M2 GenericConcepts**: v15.9.0  
**Framework**: TSCG (Transdisciplinary System Construction Game)

---

## Table of Contents

1. [Overview](#overview)
2. [Theoretical Foundation](#theoretical-foundation)
3. [The 5-Pole Kindleberger-Minsky Structure](#the-5-pole-kindleberger-minsky-structure)
4. [7 Historical Instances](#7-historical-instances)
5. [TSCG Mapping — M2 GenericConcepts](#tscg-mapping--m2-genericconcepts)
6. [ASFID / REVOI Scores](#asfid--revoi-scores)
7. [Interface Layout](#interface-layout)
8. [Controls Reference](#controls-reference)
9. [Visual Language](#visual-language)
10. [Requirements & Installation](#requirements--installation)
11. [Architecture Notes](#architecture-notes)

---

## Overview

This simulation is a **TSCG M0 Poclet visualization** of the Kindleberger-Minsky model of financial crises. It renders 7 historical speculative bubbles as interactive animated sequences, mapping each phase of the cycle onto the TSCG bicephalous ontology (ASFID Territory + REVOI Map).

The simulation demonstrates how a single abstract pattern — the five-phase speculative cycle — recurs with structural isomorphism across 3 centuries, 5 asset classes, and 4 continents.

### Key Characteristics

| Dimension | Value |
|-----------|-------|
| ASFID mean score | 0.91 |
| REVOI mean score | 0.82 |
| Epistemic gap δΘ | 0.09 |
| Historical instances | 7 |
| Phases per instance | 5 |
| Primary M2 patterns | Propagation, Narration |
| Date range covered | 1711 – 2022 |

---

## Theoretical Foundation

### Kindleberger-Minsky Model

The model originates in Hyman Minsky's financial instability hypothesis (1970s) and was systematized by Charles Kindleberger in *Manias, Panics and Crashes* (1978). The core insight: speculative bubbles follow a deterministic five-phase sequence driven by the interaction of credit expansion, narrative propagation, and leverage unwinding.

### TSCG Mapping

In TSCG terms, the Kindleberger-Minsky cycle is a **temporal Attractor** (A) whose basin of attraction is defined by the intersection of:

- **Information dynamics** (I ⊗ D) — displacement event and narrative formation
- **Flow amplification** (F ⊗ D ⊗ A) — credit expansion and leverage cascade
- **Structural crystallization** (A ⊗ S) — peak consensus, zero dissent
- **Bifurcation** (I ⊗ D → threshold crossing) — Minsky Moment, R₀ > 1
- **Cascade dissipation** (F ⊗ D) — debt deflation, institutional collapse

The M3 bicephalous perspective reveals an important asymmetry: Territory (ASFID) scores are consistently high (measurable physical flows of capital), while Map (REVOI) scores degrade at peak Euphoria — the moment when the narrative most completely displaces empirical reality.

---

## The 5-Pole Kindleberger-Minsky Structure

| # | Phase | TSCG Formula | Primary M2 | Dominant Force |
|---|-------|-------------|------------|----------------|
| 1 | **DISPLACEMENT** | `I ⊗ D` | m2:Event | Exogenous shock creates new profit opportunity |
| 2 | **BOOM** | `F ⊗ D ⊗ A` | m2:Amplification | Credit expansion + leverage cascade |
| 3 | **EUPHORIA** | `A ⊗ S` | m2:Narration | Peak consensus, "this time is different" narrative |
| 4 | **DISTRESS** | `I ⊗ D` (threshold) | m2:Bifurcation | Minsky Moment — R₀ > 1, insider selling |
| 5 | **REVULSION** | `F ⊗ D` | m2:Propagation | Debt deflation, contagion, institutional collapse |

### Phase Colour Code

| Phase | Colour | Hex |
|-------|--------|-----|
| DISPLACEMENT | Blue | `#4A90E2` |
| BOOM | Green | `#22C97A` |
| EUPHORIA | Amber | `#F5A623` |
| DISTRESS | Red | `#E64141` |
| REVULSION | Purple | `#A855F7` |

---

## 7 Historical Instances

Listed in chronological order (as displayed in the interface):

| # | Label | Asset | Period | Peak | Drawdown | Multiplier |
|---|-------|-------|--------|------|----------|------------|
| 1 | S.SEA 1720 | South Sea Company stock | ~10 yrs (1711–1720) | £1,050/share | −90.5% | ×10.5 |
| 2 | RUBBER 1912 | Pará rubber (Hevea brasiliensis) | ~20 yrs (1895–1915) | £12/long ton | −96.3% | ×26.7 |
| 3 | NYSE 1929 | Dow Jones Industrial Average | ~11 yrs (1922–1932) | 381.2 pts | −89.2% | ×4.0 |
| 4 | NIKKEI 1989 | Nikkei 225 Index | ~8 yrs (1984–1992) | 38,915 pts | −63.2% | ×3.8 |
| 5 | NASDAQ 2000 | NASDAQ Composite | ~9 yrs (1993–2002) | 5,132.5 pts | −78.3% | ×7.3 |
| 6 | GFC 2008 | S&P 500 Index | ~9 yrs (2001–2009) | 1,565.0 pts | −57.4% | ×1.8 |
| 7 | BTC 2021 | Bitcoin (BTC) | ~4 yrs (2019–2022) | $69,044 | −77.5% | ×19.7 |

### Key Observations

**Amplitude paradox**: The most extreme multipliers (Rubber ×26.7, South Sea ×10.5) occurred in pre-industrial economies with limited information infrastructure, suggesting that narrative propagation velocity — not credit volume — is the dominant amplifier.

**Drawdown floor**: Five of seven instances show drawdowns exceeding 75%, consistent with Minsky's prediction that leverage-driven cycles overshoot on the downside.

**Duration compression**: Cycle length has shortened from ~20 years (Rubber) to ~4 years (Crypto), reflecting accelerating information propagation (R₀ narrative).

---

## TSCG Mapping — M2 GenericConcepts

### Primary Patterns

| M2 Concept | Phase | Role |
|------------|-------|------|
| `m2:Event` | DISPLACEMENT | Exogenous shock that opens the profit opportunity |
| `m2:Amplification` | BOOM | Credit-driven positive feedback loop |
| `m2:Narration` | EUPHORIA | Self-reinforcing belief system, R₀ >> 1 |
| `m2:Bifurcation` | DISTRESS | Phase transition — system crosses instability threshold |
| `m2:Propagation` | REVULSION | Contagion cascade across institutions and geographies |

### Secondary Patterns (selected)

`m2:Cascade` · `m2:Network` · `m2:LeverageCycle` · `m2:Threshold` · `m2:Trigger` · `m2:Oscillator` · `m2:Emergence` · `m2:Memory` · `m2:Identity` · `m2:Dissipation` · `m2:Regulation` · `m2:DebtDeflation` · `m2:FinancialContagion`

### R₀ Propagation Regime by Phase

| Phase | R₀ (panic) | R₀ (narrative) | Regime |
|-------|-----------|----------------|--------|
| DISPLACEMENT | 0.05–0.1 | 0.5–0.8 | SubThreshold |
| BOOM | 0.08–0.1 | 1.7–2.5 | Supercritical (narrative) |
| EUPHORIA | 0.1 | 4.0–5.0 | Supercritical — peak |
| DISTRESS | 3.0–5.0 | 0.1–0.2 | **MINSKY MOMENT** R₀ > 1 |
| REVULSION | 0.2–0.3 | 0.05 | Saturated → SubThreshold |

---

## ASFID / REVOI Scores

Scores sourced from `M0_KindlebergerMinsky.jsonld` and `M1_Economics.jsonld`.

### By Phase (mean across all instances)

| Phase | A | S | F | I | D | ASFID mean |
|-------|---|---|---|---|---|-----------|
| DISPLACEMENT | 0.69 | 0.64 | 0.73 | 0.92 | 0.88 | 0.77 |
| BOOM | 0.83 | 0.79 | 0.93 | 0.84 | 0.92 | 0.86 |
| EUPHORIA | 0.97 | 0.91 | 0.84 | 0.87 | 0.84 | 0.89 |
| DISTRESS | 0.94 | 0.84 | 0.87 | 0.94 | 0.97 | 0.91 |
| REVULSION | 0.87 | 0.81 | 0.97 | 0.87 | 0.97 | 0.90 |

**ASFID global mean**: 0.91 — high Territory measurability across all phases.  
**REVOI global mean**: 0.82 — Map quality degrades at Euphoria peak (Verifiability V collapses).  
**Epistemic gap δΘ**: 0.09 — indicates the framework captures the system well despite the qualitative nature of narrative dynamics.

---

## Interface Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│  TSCG  KINDLEBERGER-MINSKY          [S.SEA][RUBBER][NYSE]…  ← bubble tabs │
├──────────────────────────────────────┬─────────────────────────────────────┤
│ PHASE  [DISPLACEMENT][BOOM][EUPH]…   │  TSCG  MAPPING          M2 v15.9.0 │
├──────────────────────────────────────┤  ─ current phase formula            │
│                                      │  ─ primary / secondary M2           │
│   ASSET PRICE  (75% height)          │  ─ ASFID score bars                 │
│   • dim white  = full history        │  ─ R₀ regime                        │
│   • bright white = played            │  ─ narrative arc                    │
│   • thick white  = current phase     ├─────────────────────────────────────┤
│                                      │  EPISODE                            │
├──────────────────────────────────────┤  ─ asset name & period              │
│   TRANSACTION VOLUME  (25% height)   │  ─ context paragraph                │
│   • dim pastels  = other phases      │  ─ driver                           │
│   • bright pastels = current phase   │  ─ Wikipedia links [↗]             │
├──────────────────────────────────────├─────────────────────────────────────┤
│  [▶PLAY][RESET][1][2][3][4][5]  ×0.5 ×1 ×2 ×4  ████░░ progress           │  METRICS
└────────────────────────────────────────────────────────────────────────────┘  ─ price start/peak/trough
                                                                                 ─ drawdown, velocity
                                                                                 ─ TSCG scores
```

### Left Panel — Charts (≈63% of window width)

- **Header bar**: Title + 7 bubble selection tabs (chronological order)
- **Phase bar**: Colour-coded phase segments — clickable to jump phases
- **Price chart** (75% of chart height): Asset price curve, peak-scaled and normalised
- **Volume chart** (25% of chart height): Transaction volume, normalised

### Right Panel — Information (≈37% of window width)

Three resizable panels separated by draggable splitters:

- **TSCG MAPPING**: Phase formula, M2 primary/secondary concepts, ASFID score bars, R₀ regime label, narrative arc quote
- **EPISODE**: Asset name, period, cycle duration, phase date, context description, driving force, Wikipedia reference links
- **METRICS**: Asset price statistics (start/peak/trough/current), cycle statistics (drawdown, multiplier, total cycle), current phase dynamics (velocity, volume normalised, volatility, acceleration)

---

## Controls Reference

### Navigation

| Control | Action |
|---------|--------|
| Bubble tabs (header) | Select historical instance — cursor positions at end of DISPLACEMENT |
| Phase bar segments | Click any phase segment → jump to that phase |
| Buttons `[1]` `[2]` `[3]` `[4]` `[5]` | Jump to phase 1–5 |
| `[RESET]` | Return to start of current bubble |
| Click on chart | Immediately set time cursor to that position |
| Click + drag on chart | Scrub timeline interactively |

### Playback

| Control | Action |
|---------|--------|
| `[▶ PLAY]` / `[⏸ PAUSE]` | Toggle animation |
| `[×0.5]` `[×1]` `[×2]` `[×4]` | Animation speed multiplier |
| `SPACE` | Toggle play/pause |

### Other

| Control | Action |
|---------|--------|
| Mouse hover on chart | Crosshair tooltip: price, phase, date, ahead/played status |
| Drag splitters (right panel) | Resize TSCG Mapping / Episode / Metrics panels |
| Click `[↗ link]` | Open Wikipedia article in browser |
| Window resize / drag | Fully responsive layout — all panels recompute |
| `ESC` or `Q` | Quit |

---

## Visual Language

### Price Curve

| Visual | Meaning |
|--------|---------|
| Very dim white (1px) | Future — not yet reached by playhead |
| Dim white (2px) | Played — phases before the current active phase |
| **Bright white (3px)** | **Current active phase** |
| Coloured dot | Playhead position (dot colour = current phase colour) |
| Yellow vertical tick + label | Historical event marker |

### Volume Bars

| Visual | Meaning |
|--------|---------|
| Very dim pastel (≈20%) | Future — beyond playhead |
| Mid pastel (≈78%) | Played phases other than the current |
| **Full bright pastel** | **Current active phase** |

Each phase has a distinct pastel colour: sky blue (DISPLACEMENT) · mint green (BOOM) · gold (EUPHORIA) · coral (DISTRESS) · lavender (REVULSION).

### Phase Bar

The phase bar sits between the header and the price chart. The active phase is rendered at full brightness; all others are dimmed. Hovering over a segment highlights it. Full phase names are shown when segment width allows; abbreviated names otherwise.

---

## Requirements & Installation

```bash
# Minimum requirement
pip install pygame

# Run
python kindleberger_minsky_sim.py
```

**Python**: 3.8+  
**Pygame**: 2.0+  
**Screen**: Recommended minimum 1280 × 760 (default window size). Fully resizable.  
**OS**: Linux, macOS, Windows (any platform supporting pygame)

No other dependencies. All data is embedded in the script via the `BUBBLES` list.

---

## Architecture Notes

### Data Architecture

All historical data lives in the `BUBBLES` list — a list of 7 dicts, one per historical instance. Each bubble contains:

- Metadata: `id`, `name`, `short`, `color`, `asset`, `unit`, `peak`, `trough`, `drawdown_pct`, `multiplier`, `total_cycle`, `description`, `wiki`
- `phases`: list of 5 dicts, one per Kindleberger-Minsky phase, each containing `date`, `months`, `v_pct` (velocity %/month), `vol_norm`, `volatility` (0–3), `formula`, `primary_m2`, `secondary_m2`, `narrative`, `asfid` (A/S/F/I/D scores), `r0_panic`, `r0_narr`, `r0_regime`, `force`, `events`

### Curve Generation

Synthetic price and volume curves are generated by `generate_curves(bubble)` using `STEPS_PER_MONTH = 8` points per month. Price evolution is velocity-driven (`v_pct` per phase) with Gaussian noise scaled by `volatility` level (0=Low → 3=Extreme). A fixed seed (`VOL_NOISE_SEED = 42`) ensures reproducibility. All bubbles are pre-generated at startup and cached in `self.curves`.

### Layout System

A `Layout` singleton (`L`) holds all derived geometry and is recalculated on every `VIDEORESIZE` event. Module-level globals (`CHART_W`, `PRICE_TOP`, etc.) are updated in place so all drawing code remains unmodified.

### Phase State Management

The authoritative phase index is stored in `self._selected_phase` (never inferred from the float playhead, which would produce off-by-one errors at phase boundaries). It is updated:
- On `_jump_phase(i)` — set explicitly
- During playback — synced each frame via `phase_at_point()`
- On `_select_bubble()` and `RESET` — reset to 0

### File Relationships

```
kindleberger_minsky_sim.py
  ├── driven by:  M0_KindlebergerMinsky.jsonld
  ├── M2 layer:   M2_GenericConcepts.jsonld  (v15.9.0)
  │     └── uses: Narration, Propagation, Duplication, Bifurcation, Amplification, …
  └── M1 layer:   M1_Economics.jsonld
        └── concepts: ExogenousShock, CreditExpansion, LeverageCycle,
                      MarketSentiment, MinskyCrisis, SystemicRisk, FinancialContagion
```

---

*Generated for TSCG framework — Echopraxium with the collaboration of Claude AI*
