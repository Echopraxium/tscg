"""
kindleberger_minsky_sim.py
==========================
TSCG Poclet Simulation — Kindleberger-Minsky Financial Crisis Cycle
Author: Echopraxium with the collaboration of Claude AI
Version: 1.11.0  (2026-02-28)

Driven by the M0_KindlebergerMinsky poclet (M2 GenericConcepts v15.9.0).

7 historical instances:
  1. Brazilian Rubber Boom   (1895–1915)
  2. Japanese Asset Bubble   (1984–1992)
  3. South Sea Bubble        (1711–1720)
  4. Wall Street 1929        (1922–1932)
  5. Dot-com Bubble          (1993–2002)
  6. Global Financial Crisis (2001–2009)
  7. Crypto 2019-2022        (2019–2022)

Layout (1500 × 880):
  LEFT (~940px): Bubble tabs | Phase bar | Price chart (75%) | Volume chart (25%) | Controls
  RIGHT (~560px): 3 panels with draggable splitters
    Panel 1 — TSCG MAPPING   : phase formula, M2 concepts, ASFID scores, R0, narrative arc
    Panel 2 — EPISODE         : asset, period, context, key events, Wikipedia links
    Panel 3 — METRICS         : price start/peak/trough, drawdown, velocity, vol norm, acceleration

Controls:
  Bubble tabs        — select historical instance
  [▶ / ⏸]           — play / pause animation
  [◀] [1][2][3][4][5]— jump to start or specific phase
  [×0.5][×1][×2][×4] — animation speed
  [RESET]            — restart
  Mouse hover chart  — crosshair with price + date tooltip
  Drag splitters     — resize right panels
  Click [WIKI] links — open in browser
  ESC / Q            — quit

Requirements: pip install pygame
Run:          python kindleberger_minsky_sim.py
"""

import math
import random
import webbrowser
import pygame
import pygame.gfxdraw

# ─────────────────────────────────────────────────────────────────────────────
# Window & layout  — dynamic (recalculated on resize)
# ─────────────────────────────────────────────────────────────────────────────
WIN_W, WIN_H = 1280, 760
FPS          = 60

HEADER_H    = 44
CTRL_H      = 42
PHASE_BAR_H = 26
PAD         = 10
Y_AXIS_W    = 62

class Layout:
    """Singleton that holds all derived geometry.
    Call L.update(w, h) after any resize to refresh module-level globals."""

    def __init__(self, w, h):
        self.update(w, h)

    def update(self, w, h):
        global WIN_W, WIN_H
        global CHART_W, RIGHT_X, RIGHT_W
        global CHART_TOP, CHART_BOT, CHART_H
        global PRICE_H, VOL_H
        global PRICE_TOP, PRICE_BOT, VOL_TOP, VOL_BOT

        WIN_W   = w
        WIN_H   = h

        CHART_W  = max(600, int(w * 0.627))
        RIGHT_X  = CHART_W
        RIGHT_W  = w - CHART_W

        CHART_TOP = HEADER_H + PHASE_BAR_H
        CHART_BOT = h - CTRL_H
        CHART_H   = CHART_BOT - CHART_TOP

        PRICE_H  = int(CHART_H * 0.75)
        VOL_H    = CHART_H - PRICE_H

        PRICE_TOP = CHART_TOP
        PRICE_BOT = CHART_TOP + PRICE_H
        VOL_TOP   = PRICE_BOT
        VOL_BOT   = CHART_BOT

L = Layout(WIN_W, WIN_H)

# ─────────────────────────────────────────────────────────────────────────────
# Colour palette  (dark terminal / financial terminal theme)
# ─────────────────────────────────────────────────────────────────────────────
BG       = ( 10,  13,  22)
PANEL    = ( 18,  22,  36)
PANEL2   = ( 24,  28,  44)
BORDER   = ( 48,  56,  90)
BORDER2  = ( 34,  42,  68)
TEXT     = (210, 220, 240)
DIM      = (110, 125, 155)
DIM2     = ( 58,  70,  96)
GOLD     = (255, 205,  55)
GREEN    = ( 55, 210, 110)
RED_C    = (230,  65,  65)
ACCENT   = ( 60, 165, 255)
SLIDER_BG= ( 32,  38,  60)
SLIDER_FG= ( 55, 145, 230)
WHITE    = (230, 235, 250)

# Phase colours
PH_COL = [
    ( 74, 144, 226),   # 0 DISPLACEMENT – blue
    ( 34, 201, 122),   # 1 BOOM         – green
    (245, 166,  35),   # 2 EUPHORIA     – amber
    (230,  65,  65),   # 3 DISTRESS     – red
    (168,  85, 247),   # 4 REVULSION    – purple
]
PH_DIM = [tuple(max(0,c-110) for c in col) for col in PH_COL]
PH_BG  = [tuple(c//6 for c in col) for col in PH_COL]

PHASE_NAMES = ["DISPLACEMENT", "BOOM", "EUPHORIA", "DISTRESS", "REVULSION"]
PHASE_SHORT = ["DISP", "BOOM", "EUPH", "DIST", "REVULS"]
PHASE_KEYS  = ["displacement", "boom", "euphoria", "distress", "revulsion"]

# ─────────────────────────────────────────────────────────────────────────────
# Bubble data  — all values sourced from M0_KindlebergerMinsky.jsonld
# ─────────────────────────────────────────────────────────────────────────────
# Phase schema keys:
#   date       – human-readable date range
#   months     – duration in months (float ok for short phases)
#   v_pct      – price velocity %/month (signed)
#   vol_norm   – volume normalised (1.0 = Displacement baseline)
#   volatility – 0=Low 1=Medium 2=High 3=Extreme
#   formula    – TSCG ASFID formula
#   primary_m2 – primary M2 GenericConcept
#   secondary_m2 – list of secondary M2
#   narrative  – dominant narrative text (quoted)
#   asfid      – dict A S F I D scores
#   r0_panic   – propagation R0 equivalent for panic
#   r0_narr    – propagation R0 for opportunity narrative
#   r0_regime  – regime label
#   force      – dominant driving force (short label)
#   events     – list of (month_offset_from_phase_start, label)

BUBBLES = [
  # ── 0  BRAZILIAN RUBBER BOOM ─────────────────────────────────────────────
  { "id":    "rubber",
    "name":  "Brazilian Rubber Boom",
    "short": "RUBBER 1912",
    "color": ( 80, 200, 100),
    "asset": "Pará rubber (Hevea brasiliensis)",
    "unit":  "GBP / long ton",
    "peak":  12.0,  "trough": 0.45,
    "drawdown_pct": -96.3,  "multiplier": 26.7,
    "total_cycle": "~20 years (1895–1915)",
    "description": (
        "The Amazon basin held a near-monopoly on Hevea brasiliensis, the only "
        "commercial rubber source. Demand from bicycle and automobile tyre "
        "industries (Dunlop 1888, Benz 1886) created a global supply crisis. "
        "Manaus became one of the wealthiest cities on Earth — the Teatro Amazonas "
        "opera house (1896) shipped Italian marble and Venetian glass to the jungle. "
        "British botanist Henry Wickham had secretly exported 70,000 Hevea seeds "
        "to Kew Gardens in 1876. Plantations in Malaya and Ceylon, organised by "
        "the colonial system, reached productive scale in 1912. Asian rubber, "
        "produced at 1/10th the Brazilian cost, instantly collapsed world prices. "
        "Manaus was abandoned; the Amazonian rubber economy never recovered."
    ),
    "wiki": [
        ("Amazon rubber boom", "https://en.wikipedia.org/wiki/Amazon_rubber_boom"),
        ("Hevea brasiliensis", "https://en.wikipedia.org/wiki/Hevea_brasiliensis"),
        ("Teatro Amazonas", "https://en.wikipedia.org/wiki/Amazon_Theatre"),
    ],
    "phases": [
      { "date":"1895 – 1904", "months":108, "v_pct":+1.0, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Information"],
        "narrative":'"Amazon rubber — the empire of the tyre age"',
        "asfid":{"A":0.68,"S":0.62,"F":0.72,"I":0.90,"D":0.85},
        "r0_panic":0.05,"r0_narr":0.6,"r0_regime":"SubThreshold",
        "force":"Bicycle + automobile tyre demand creates global rubber shortage",
        "events":[(0,"Dunlop pneumatic tyre 1888"),(48,"Benz mass production 1901"),(96,"Manaus opera house built 1896")]},
      { "date":"1905 – 1909", "months":60, "v_pct":+3.5, "vol_norm":4.0,
        "volatility":1, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation","m2:Narration"],
        "narrative":'"Brazilian monopoly — no alternative source possible"',
        "asfid":{"A":0.82,"S":0.76,"F":0.90,"I":0.84,"D":0.90},
        "r0_panic":0.08,"r0_narr":1.8,"r0_regime":"Supercritical (narrative)",
        "force":"Seringalistas (rubber barons) debt-bond indigenous tappers; Ford investment",
        "events":[(0,"Rubber prices double 1905"),(36,"Ford Motor buys Amazon concession"),(48,"London rubber futures market opens")]},
      { "date":"1910 – mid 1912", "months":30, "v_pct":+8, "vol_norm":10.0,
        "volatility":1, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Identity"],
        "narrative":'"Amazon rubber is irreplaceable — monopoly forever"',
        "asfid":{"A":0.95,"S":0.88,"F":0.84,"I":0.86,"D":0.83},
        "r0_panic":0.1,"r0_narr":4.0,"r0_regime":"Supercritical — peak",
        "force":"Peak price £12/long ton; London exchange speculation; Manaus luxury peak",
        "events":[(0,"Peak £12/ton 1910"),(18,"Malayan plantations reach full production 1912")]},
      { "date":"Jul – Dec 1912", "months":6, "v_pct":-25, "vol_norm":8.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Asian supply flooding market — Amazon cannot compete"',
        "asfid":{"A":0.90,"S":0.82,"F":0.85,"I":0.92,"D":0.93},
        "r0_panic":3.5,"r0_narr":0.1,"r0_regime":"MINSKY MOMENT — R0>1",
        "force":"Malayan plantation rubber at 1/10th Amazon cost hits London exchange",
        "events":[(0,"Malayan rubber price undercuts Amazon Jul 1912"),(4,"London exchange panic selling Nov 1912")]},
      { "date":"1913 – 1915", "months":24, "v_pct":-15, "vol_norm":0.5,
        "volatility":1, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:DebtDeflation"],
        "narrative":'"Amazon rubber is finished — Manaus is a ghost city"',
        "asfid":{"A":0.85,"S":0.80,"F":0.94,"I":0.85,"D":0.95},
        "r0_panic":0.2,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"Prices collapse to £0.45/ton; seringalistas bankrupt; indigenous debt-slaves released",
        "events":[(0,"Seringalistas mass bankruptcy 1913"),(12,"Manaus luxury economy collapses 1914"),(24,"WW1 briefly revives demand 1915")]},
    ],
  },

  # ── 1  JAPANESE ASSET BUBBLE ──────────────────────────────────────────────
  { "id":    "japan",
    "name":  "Japanese Asset Bubble",
    "short": "NIKKEI 1989",
    "color": (255, 100, 100),
    "asset": "Nikkei 225 Index",
    "unit":  "JPY (index points)",
    "peak":  38915,  "trough": 14309,
    "drawdown_pct": -63.2,  "multiplier": 3.8,
    "total_cycle": "~8 years (1984–1992)",
    "description": (
        "Japan in the 1980s was the world's second-largest economy, running "
        "massive trade surpluses. The 1985 Plaza Accord forced yen appreciation "
        "(USD/JPY: 240→120), threatening exports. The Bank of Japan cut rates "
        "to 2.5% (1987) to offset the impact, flooding the economy with credit. "
        "Easy money poured into equities and real estate. The Imperial Palace "
        "grounds were theoretically worth more than all California real estate. "
        "Nikkei 225 peaked at 38,915 on December 29, 1989. Bank of Japan "
        "raised rates sharply from 1989. The Nikkei lost 63% by 1992 and never "
        "recovered to its 1989 peak. Japan entered a 30-year deflationary "
        "stagnation — zombie banks, balance-sheet recession, the 'Lost Decade'."
    ),
    "wiki": [
        ("Japanese asset price bubble", "https://en.wikipedia.org/wiki/Japanese_asset_price_bubble"),
        ("Plaza Accord", "https://en.wikipedia.org/wiki/Plaza_Accord"),
        ("Lost Decade (Japan)", "https://en.wikipedia.org/wiki/Lost_Decade_(Japan)"),
    ],
    "phases": [
      { "date":"1984 – 1986", "months":36, "v_pct":+1.8, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Information"],
        "narrative":'"Japan Inc. — world champion exporter, unstoppable economy"',
        "asfid":{"A":0.70,"S":0.65,"F":0.74,"I":0.92,"D":0.87},
        "r0_panic":0.05,"r0_narr":0.7,"r0_regime":"SubThreshold",
        "force":"Plaza Accord 1985: yen doubles vs USD; BoJ cuts rates to offset",
        "events":[(0,"Plaza Accord Sep 1985"),(12,"BoJ cuts to 2.5% 1986"),(24,"Zaitech corporate speculation begins")]},
      { "date":"1987 – mid 1988", "months":18, "v_pct":+3.5, "vol_norm":3.5,
        "volatility":1, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:LeverageCycle","m2:Propagation"],
        "narrative":'"Japanese banks and real estate — permanently appreciating"',
        "asfid":{"A":0.84,"S":0.80,"F":0.93,"I":0.85,"D":0.92},
        "r0_panic":0.08,"r0_narr":2.0,"r0_regime":"Supercritical (narrative)",
        "force":"Zaitech: Japanese corporations use equity as collateral to buy more equity",
        "events":[(0,"Black Monday Oct 1987: Japan barely affected"),(12,"Imperial Palace > California real estate value")]},
      { "date":"mid 1988 – Dec 29, 1989", "months":18, "v_pct":+4.5, "vol_norm":8.0,
        "volatility":1, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Identity","m2:Memory"],
        "narrative":'"Japan will overtake America — the 21st century belongs to Japan"',
        "asfid":{"A":0.96,"S":0.91,"F":0.84,"I":0.87,"D":0.83},
        "r0_panic":0.1,"r0_narr":4.5,"r0_regime":"Supercritical — peak",
        "force":"Nikkei: 10K→38,915; Tokyo land = 4× all US land; golf club memberships $3M",
        "events":[(0,"Nikkei crosses 30,000 pts"),(15,"Peak: Nikkei 38,915 Dec 29, 1989")]},
      { "date":"Jan 1990 – Dec 1990", "months":12, "v_pct":-4.5, "vol_norm":6.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"BoJ hiking — land prices falling — bank collateral worthless"',
        "asfid":{"A":0.93,"S":0.84,"F":0.87,"I":0.94,"D":0.96},
        "r0_panic":3.0,"r0_narr":0.15,"r0_regime":"MINSKY MOMENT — R0>1",
        "force":"BoJ raises rates 5 times in 15 months (2.5%→6%); real estate lending capped",
        "events":[(0,"BoJ raises rates Jan 1990"),(6,"Nikkei -30% by Jun 1990"),(10,"Real estate crash begins 1990")]},
      { "date":"1991 – 1992", "months":24, "v_pct":-5.0, "vol_norm":1.5,
        "volatility":2, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:DebtDeflation","m2:Regulation"],
        "narrative":'"Zombie banks — bad loans impossible to write off — Lost Decade"',
        "asfid":{"A":0.86,"S":0.81,"F":0.96,"I":0.86,"D":0.97},
        "r0_panic":0.25,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"¥87T non-performing loans; zombie banks; Jusen housing lenders collapse",
        "events":[(0,"Nikkei trough 14,309 Aug 1992"),(12,"Jusen scandal 1992"),(20,"Big Bang bank reform proposed")]},
    ],
  },

  # ── 2  SOUTH SEA BUBBLE ──────────────────────────────────────────────────────
  { "id":    "southsea",
    "name":  "South Sea Bubble",
    "short": "S.SEA 1720",
    "color": ( 80, 200, 180),
    "asset": "South Sea Company stock",
    "unit":  "GBP / share",
    "peak":  1050,  "trough": 100,
    "drawdown_pct": -90.5,  "multiplier": 10.5,
    "total_cycle": "~10 years (1711–1720)",
    "description": (
        "The South Sea Company was granted a British government monopoly on trade "
        "with Spanish South America in 1711. In 1720 it proposed to absorb the "
        "national debt, fuelling massive speculation. Directors bribed officials, "
        "created installment plans enabling leverage, and promoted the stock "
        "publicly. King George I served as governor. Isaac Newton lost £20,000 "
        "('I can calculate the movement of stars, but not the madness of men'). "
        "The Bubble Act of June 1720 restricted competing companies, ironically "
        "accelerating the crash as capital sought exit. Parliament launched an "
        "inquiry; directors fled or were jailed."
    ),
    "wiki": [
        ("South Sea Company", "https://en.wikipedia.org/wiki/South_Sea_Company"),
        ("South Sea bubble", "https://en.wikipedia.org/wiki/South_Sea_bubble"),
        ("Bubble Act", "https://en.wikipedia.org/wiki/Bubble_Act"),
    ],
    "phases": [
      { "date":"1711 – Jan 1719", "months":96, "v_pct":+0.3, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration"],
        "narrative":'"Colonial trade monopoly — guaranteed returns"',
        "asfid":{"A":0.65,"S":0.60,"F":0.70,"I":0.90,"D":0.85},
        "r0_panic":0.05,"r0_narr":0.5,"r0_regime":"SubThreshold",
        "force":"Parliamentary monopoly grant on South American trade",
        "events":[(0,"Company chartered 1711"),(60,"Debt conversion talks begin")]},
      { "date":"Jan 1719 – Mar 1720", "months":15, "v_pct":+10, "vol_norm":5.0,
        "volatility":1, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation"],
        "narrative":'"National debt will be absorbed — guaranteed profit"',
        "asfid":{"A":0.82,"S":0.78,"F":0.92,"I":0.85,"D":0.90},
        "r0_panic":0.1,"r0_narr":1.8,"r0_regime":"Supercritical (narrative)",
        "force":"Installment purchase plan + director insider buying",
        "events":[(0,"Debt conversion plan announced"),(8,"King George I as governor")]},
      { "date":"Apr – Jun 24, 1720", "months":3, "v_pct":+60, "vol_norm":10.0,
        "volatility":2, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Identity"],
        "narrative":'"This is the greatest investment of the century"',
        "asfid":{"A":0.96,"S":0.90,"F":0.85,"I":0.87,"D":0.88},
        "r0_panic":0.1,"r0_narr":5.0,"r0_regime":"Supercritical — peak",
        "force":"Aristocracy publicly invested; 'bubble companies' proliferate",
        "events":[(0,"300→1050 in 3 months"),(2.5,"Peak: £1050, Jun 24")]},
      { "date":"Jun 24 – Sep 1720", "months":3, "v_pct":-15, "vol_norm":5.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Insider selling — something is wrong"',
        "asfid":{"A":0.93,"S":0.85,"F":0.88,"I":0.94,"D":0.96},
        "r0_panic":2.0,"r0_narr":0.3,"r0_regime":"Supercritical (panic)",
        "force":"Bubble Act (Jun 1720) triggers capital repatriation",
        "events":[(0,"Bubble Act restricts competitors"),(1,"Director selling revealed")]},
      { "date":"Sep – Dec 1720", "months":4, "v_pct":-30, "vol_norm":0.1,
        "volatility":2, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:Regulation"],
        "narrative":'"Fraud — Parliament to investigate"',
        "asfid":{"A":0.86,"S":0.82,"F":0.96,"I":0.87,"D":0.97},
        "r0_panic":0.3,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"Parliamentary inquiry; directors flee; Newton loses £20K",
        "events":[(0,"Directors flee country"),(2,"Parliamentary inquiry opens")]},
    ],
  },

  # ── 3  WALL STREET 1929 ──────────────────────────────────────────────────────
  { "id":    "wall1929",
    "name":  "Wall St / Great Depression",
    "short": "NYSE 1929",
    "color": (255, 140,  60),
    "asset": "Dow Jones Industrial Average",
    "unit":  "USD (index points)",
    "peak":  381.2,  "trough": 41.22,
    "drawdown_pct": -89.2,  "multiplier": 4.0,
    "total_cycle": "~11 years (1922–1932)",
    "description": (
        "Post-WWI prosperity, electrification, and automobile mass production "
        "drove the Roaring Twenties boom. Millions of Americans bought stocks "
        "on margin (10:1 leverage). Investment trusts created additional leverage. "
        "Irving Fisher declared a 'permanently high plateau' one week before the "
        "crash. Black Thursday (Oct 24, 1929): 12.9 million NYSE shares traded. "
        "Black Monday & Tuesday (Oct 28-29): DJIA -25% in two days. "
        "The subsequent Great Depression saw 9,000 US bank failures, 25% "
        "unemployment, and a -89% DJIA decline over 33 months."
    ),
    "wiki": [
        ("Wall Street Crash of 1929", "https://en.wikipedia.org/wiki/Wall_Street_Crash_of_1929"),
        ("Great Depression", "https://en.wikipedia.org/wiki/Great_Depression"),
        ("Roaring Twenties", "https://en.wikipedia.org/wiki/Roaring_Twenties"),
    ],
    "phases": [
      { "date":"1922 – 1925", "months":48, "v_pct":+1.2, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Amplification"],
        "narrative":'"Industrial revolution — prosperity for all"',
        "asfid":{"A":0.70,"S":0.65,"F":0.75,"I":0.95,"D":0.90},
        "r0_panic":0.05,"r0_narr":0.7,"r0_regime":"SubThreshold",
        "force":"Post-WWI boom: Ford, electrification, Fed easy money",
        "events":[(0,"Fed eases post-WWI"),(24,"Radio stocks surge")]},
      { "date":"1926 – 1928", "months":36, "v_pct":+2.0, "vol_norm":2.5,
        "volatility":1, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation","m2:LeverageCycle"],
        "narrative":'"Margin accounts for everyone — stocks only go up"',
        "asfid":{"A":0.85,"S":0.80,"F":0.95,"I":0.85,"D":0.95},
        "r0_panic":0.1,"r0_narr":2.0,"r0_regime":"Supercritical (narrative)",
        "force":"10:1 margin accounts; investment trusts; broker call money",
        "events":[(0,"NYSE volume doubles"),(18,"Investment trusts proliferate")]},
      { "date":"Jan – Sep 3, 1929", "months":8, "v_pct":+1.5, "vol_norm":4.0,
        "volatility":1, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Memory"],
        "narrative":'"Permanently high plateau" — Irving Fisher, Sep 1929',
        "asfid":{"A":0.98,"S":0.92,"F":0.85,"I":0.88,"D":0.85},
        "r0_panic":0.1,"r0_narr":4.0,"r0_regime":"Supercritical — peak",
        "force":"DJIA peak Sep 3, 381.17 pts; margin debt at record high",
        "events":[(0,"DJIA 300 pts"),(7,"Peak: Sep 3, 381.17 pts")]},
      { "date":"Sep 4 – Oct 24, 1929", "months":2, "v_pct":-4.0, "vol_norm":6.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Margin calls — forced liquidations cascade"',
        "asfid":{"A":0.95,"S":0.85,"F":0.88,"I":0.95,"D":0.98},
        "r0_panic":3.0,"r0_narr":0.2,"r0_regime":"MINSKY MOMENT — R0>1",
        "force":"Margin calls → broker loan recalls → bank strain",
        "events":[(0,"Selling pressure starts"),(1.7,"Black Thu Oct 24: 12.9M shares")]},
      { "date":"Oct 1929 – Jul 1932", "months":33, "v_pct":-3.0, "vol_norm":0.5,
        "volatility":2, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:DebtDeflation"],
        "narrative":'"Banks collapsing — Great Depression"',
        "asfid":{"A":0.88,"S":0.82,"F":0.98,"I":0.88,"D":0.98},
        "r0_panic":0.3,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"9000 bank failures; Smoot-Hawley tariffs; debt deflation spiral",
        "events":[(0,"Black Mon-Tue: -25% in 2 days"),(6,"Hoover: 'Prosperity is near'"),(33,"DJIA trough: 41.22 pts")]},
    ],
  },

  # ── 4  DOT-COM ───────────────────────────────────────────────────────────────
  { "id":    "dotcom",
    "name":  "Dot-com Bubble",
    "short": "NASDAQ 2000",
    "color": ( 55, 200, 255),
    "asset": "NASDAQ Composite",
    "unit":  "USD (index points)",
    "peak":  5132.52,  "trough": 1114.11,
    "drawdown_pct": -78.3,  "multiplier": 7.3,
    "total_cycle": "~9 years (1993–2002)",
    "description": (
        "The commercialisation of the World Wide Web (Netscape IPO 1995) created "
        "a 'new economy' narrative: traditional valuation metrics (P/E, profit) "
        "were declared obsolete. Companies with '.com' in their name saw IPOs "
        "soar regardless of revenues. PE ratios of 200-500x for unprofitable "
        "companies. Day trading democratised by online brokers (E*Trade, Schwab). "
        "NASDAQ peak: 5,132 on March 10, 2000. Pets.com, Webvan, Kozmo went "
        "bankrupt. WorldCom and Enron frauds compounded the collapse. "
        "$5 trillion market cap destroyed. Amazon and Google survived."
    ),
    "wiki": [
        ("Dot-com bubble", "https://en.wikipedia.org/wiki/Dot-com_bubble"),
        ("NASDAQ Composite", "https://en.wikipedia.org/wiki/Nasdaq_Composite"),
        ("Netscape", "https://en.wikipedia.org/wiki/Netscape"),
    ],
    "phases": [
      { "date":"1993 – 1996", "months":48, "v_pct":+1.5, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Information"],
        "narrative":'"Internet will transform commerce"',
        "asfid":{"A":0.68,"S":0.62,"F":0.72,"I":0.95,"D":0.88},
        "r0_panic":0.05,"r0_narr":0.6,"r0_regime":"SubThreshold",
        "force":"Netscape IPO Aug 1995 — $2.9B for unprofitable browser company",
        "events":[(0,"Mosaic browser released 1993"),(24,"Netscape IPO Aug 1995"),(36,"Amazon IPO May 1997")]},
      { "date":"1997 – 1998", "months":24, "v_pct":+3.5, "vol_norm":10.0,
        "volatility":1, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation","m2:Narration"],
        "narrative":'"New economy — eyeballs replace revenue"',
        "asfid":{"A":0.83,"S":0.79,"F":0.94,"I":0.84,"D":0.93},
        "r0_panic":0.1,"r0_narr":2.2,"r0_regime":"Supercritical (narrative)",
        "force":"Online brokers democratise day trading; VC funding $50B/yr",
        "events":[(0,"Day trading explosion"),(12,"eBay IPO Sep 1998"),(20,"AOL-Time Warner merger talks")]},
      { "date":"Jan 1999 – Mar 10, 2000", "months":14, "v_pct":+6.0, "vol_norm":25.0,
        "volatility":2, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Memory","m2:Identity"],
        "narrative":'"This time is different — PE ratios irrelevant online"',
        "asfid":{"A":0.98,"S":0.91,"F":0.84,"I":0.87,"D":0.85},
        "r0_panic":0.1,"r0_narr":5.0,"r0_regime":"Supercritical — peak",
        "force":"AOL-Time Warner $165B merger (Jan 2000); NASDAQ 2.5B shares/day",
        "events":[(0,"NASDAQ 2500→4000"),(12,"AOL-Time Warner Jan 2000"),(14,"Peak Mar 10: 5132")]},
      { "date":"Mar 11 – Jun 2000", "months":4, "v_pct":-8.0, "vol_norm":20.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Earnings misses — these companies have no future"',
        "asfid":{"A":0.94,"S":0.84,"F":0.87,"I":0.94,"D":0.97},
        "r0_panic":3.5,"r0_narr":0.2,"r0_regime":"MINSKY MOMENT — R0>1",
        "force":"Institutional sell orders Mar 13; Microsoft antitrust ruling",
        "events":[(0,"Mar 13: massive institutional sell"),(2,"Microsoft antitrust Apr 2000")]},
      { "date":"Jul 2000 – Oct 9, 2002", "months":28, "v_pct":-3.0, "vol_norm":8.0,
        "volatility":2, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:Convergence"],
        "narrative":'"Fraud and bankruptcy — dot-com is dead"',
        "asfid":{"A":0.87,"S":0.81,"F":0.97,"I":0.87,"D":0.97},
        "r0_panic":0.3,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"Pets.com, Webvan, Kozmo bankrupt; WorldCom/Enron frauds; 9/11",
        "events":[(2,"Pets.com bankrupt Jul 2000"),(8,"9/11 Sep 2001"),(14,"WorldCom fraud Jun 2002"),(28,"Trough Oct 9, 2002: 1114")]},
    ],
  },

  # ── 5  GFC 2008 ─────────────────────────────────────────────────────────────
  { "id":    "gfc",
    "name":  "Global Financial Crisis",
    "short": "GFC 2008",
    "color": (230, 100, 100),
    "asset": "S&P 500 Index",
    "unit":  "USD (index points)",
    "peak":  1565.0,  "trough": 666.79,
    "drawdown_pct": -57.4,  "multiplier": 1.8,
    "total_cycle": "~9 years (2001–2009)",
    "description": (
        "Post-dot-com crash and 9/11, the Fed cut rates to 1% (2003-2004). "
        "Financial innovation created MBS, CDO, and CDO-squared instruments. "
        "Subprime mortgages were extended to NINJA borrowers (No Income, No Job "
        "or Assets). Investment banks ran at 30:1-40:1 leverage. "
        "Bernanke: 'Subprime is contained' (March 2007). "
        "Lehman Brothers filed for bankruptcy September 15, 2008. Money market "
        "funds 'broke the buck'. TED spread hit 460 bps. "
        "$700B TARP bailout; Fed QE1 November 2008. The VIX reached 89.53."
    ),
    "wiki": [
        ("2007-2008 financial crisis", "https://en.wikipedia.org/wiki/2007%E2%80%932008_financial_crisis"),
        ("Lehman Brothers", "https://en.wikipedia.org/wiki/Lehman_Brothers"),
        ("Subprime mortgage crisis", "https://en.wikipedia.org/wiki/Subprime_mortgage_crisis"),
    ],
    "phases": [
      { "date":"2001 – 2004", "months":48, "v_pct":+0.6, "vol_norm":1.0,
        "volatility":0, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Information"],
        "narrative":'"Housing always appreciates — safe as houses"',
        "asfid":{"A":0.68,"S":0.62,"F":0.73,"I":0.92,"D":0.88},
        "r0_panic":0.05,"r0_narr":0.6,"r0_regime":"SubThreshold",
        "force":"Fed Funds Rate at 1% (2003-04); FSMA 1999; MBS innovation",
        "events":[(0,"Fed cuts to 1% after 9/11"),(36,"Subprime lending explodes")]},
      { "date":"2005 – 2006", "months":24, "v_pct":+1.1, "vol_norm":2.5,
        "volatility":0, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation","m2:LeverageCycle"],
        "narrative":'"CDOs rated AAA — risk has been eliminated"',
        "asfid":{"A":0.82,"S":0.78,"F":0.93,"I":0.83,"D":0.92},
        "r0_panic":0.08,"r0_narr":1.7,"r0_regime":"Supercritical (narrative)",
        "force":"MBS/CDO $2.5T/yr issuance; shadow banking leverage 30:1",
        "events":[(0,"CDO-squared invented"),(20,"Case-Shiller index peaks")]},
      { "date":"Jan – Jul 2007", "months":7, "v_pct":+0.3, "vol_norm":1.3,
        "volatility":0, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Memory"],
        "narrative":'"Subprime is contained" — Bernanke, Mar 2007',
        "asfid":{"A":0.97,"S":0.91,"F":0.84,"I":0.87,"D":0.84},
        "r0_panic":0.2,"r0_narr":2.5,"r0_regime":"Supercritical — peak",
        "force":"S&P 500 peak Oct 2007 at 1565; VIX deceptively low (<15)",
        "events":[(0,"Case-Shiller peaks Jul 2007"),(5,"Bear Stearns hedge funds collapse")]},
      { "date":"Aug 2007 – Sep 15, 2008", "months":14, "v_pct":-2.0, "vol_norm":2.0,
        "volatility":2, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Counterparty risk unknown — who is solvent?"',
        "asfid":{"A":0.94,"S":0.84,"F":0.87,"I":0.95,"D":0.97},
        "r0_panic":4.0,"r0_narr":0.1,"r0_regime":"MINSKY MOMENT — R0>1",
        "force":"BNP Paribas freeze → Bear Stearns → Fannie/Freddie → Lehman",
        "events":[(0,"BNP freezes funds Aug 9, 2007"),(7,"Bear Stearns rescued Mar 2008"),(14,"LEHMAN Sep 15, 2008")]},
      { "date":"Sep 2008 – Mar 9, 2009", "months":6, "v_pct":-8.0, "vol_norm":0.3,
        "volatility":3, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:Regulation","m2:DebtDeflation"],
        "narrative":'"Global recession — Great Recession"',
        "asfid":{"A":0.87,"S":0.81,"F":0.98,"I":0.87,"D":0.98},
        "r0_panic":0.3,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"VIX: 89.53; TARP $700B; Fed QE1 Nov 2008; 8.7M jobs lost",
        "events":[(0,"Money market 'breaks buck'"),(1,"TARP $700B approved"),(6,"S&P trough Mar 9: 666")]},
    ],
  },

  # ── 6  CRYPTO 2021 ───────────────────────────────────────────────────────────
  { "id":    "crypto",
    "name":  "Crypto Bubble 2019-2022",
    "short": "BTC 2021",
    "color": (255, 165,  40),
    "asset": "Bitcoin (BTC)",
    "unit":  "USD / BTC",
    "peak":  69044.0,  "trough": 15599.0,
    "drawdown_pct": -77.5,  "multiplier": 19.7,
    "total_cycle": "~4 years (2019–2022)",
    "description": (
        "DeFi emergence (Uniswap, Compound 2019), Bitcoin halving (May 2020), "
        "and institutional adoption (MicroStrategy, Tesla, PayPal) drove a "
        "supercycle. NFT boom (Beeple: $69M March 2021), Coinbase IPO, and "
        "El Salvador BTC legal tender. Bitcoin peaked at $69,044 November 10, 2021. "
        "The Fed's rate hike cycle (risk-off), Terra/LUNA collapse ($40B in 72h), "
        "Celsius freeze, Three Arrows insolvency, and FTX collapse ($32B, Nov 2022) "
        "created a cascading crypto contagion destroying $2T in market cap."
    ),
    "wiki": [
        ("Cryptocurrency bubble", "https://en.wikipedia.org/wiki/Cryptocurrency_bubble"),
        ("Terra (blockchain)", "https://en.wikipedia.org/wiki/Terra_(blockchain)"),
        ("FTX (company)", "https://en.wikipedia.org/wiki/FTX_(company)"),
    ],
    "phases": [
      { "date":"Jan 2019 – Oct 2020", "months":22, "v_pct":+7, "vol_norm":1.0,
        "volatility":1, "formula":"I ⊗ D", "primary_m2":"m2:Event",
        "secondary_m2":["m2:Trigger","m2:Narration","m2:Information"],
        "narrative":'"DeFi will replace traditional finance"',
        "asfid":{"A":0.71,"S":0.66,"F":0.76,"I":0.92,"D":0.91},
        "r0_panic":0.1,"r0_narr":0.8,"r0_regime":"SubThreshold",
        "force":"DeFi protocols launch; Bitcoin halving May 2020; PayPal crypto",
        "events":[(0,"Uniswap V1 launch Nov 2018"),(12,"Bitcoin halving May 2020"),(18,"PayPal crypto support Oct 2020")]},
      { "date":"Nov 2020 – Mar 2021", "months":5, "v_pct":+50, "vol_norm":5.0,
        "volatility":2, "formula":"F ⊗ D ⊗ A", "primary_m2":"m2:Amplification",
        "secondary_m2":["m2:Cascade","m2:Network","m2:Propagation","m2:Narration"],
        "narrative":'"Institutional adoption — BTC is digital gold"',
        "asfid":{"A":0.84,"S":0.80,"F":0.95,"I":0.86,"D":0.94},
        "r0_panic":0.1,"r0_narr":2.5,"r0_regime":"Supercritical (narrative)",
        "force":"MicroStrategy $1B BTC; Tesla $1.5B; Coinbase IPO April 2021",
        "events":[(0,"MicroStrategy buys $1B BTC"),(3,"Tesla $1.5B BTC Feb 2021"),(5,"BTC first peak: $64K Apr 2021")]},
      { "date":"Apr – Nov 10, 2021", "months":8, "v_pct":+4, "vol_norm":20.0,
        "volatility":3, "formula":"A ⊗ S", "primary_m2":"m2:Narration",
        "secondary_m2":["m2:Oscillator","m2:Emergence","m2:Duplication","m2:Identity"],
        "narrative":'"Crypto is the future — HODL everything"',
        "asfid":{"A":0.97,"S":0.90,"F":0.84,"I":0.87,"D":0.85},
        "r0_panic":0.1,"r0_narr":5.0,"r0_regime":"Supercritical — peak",
        "force":"Beeple NFT $69M; El Salvador legal tender; meme coins",
        "events":[(0,"Beeple NFT $69M Mar 2021"),(2,"Coinbase IPO Apr 2021"),(4,"El Salvador legal tender Jun 2021"),(8,"Peak: $69,044, Nov 10, 2021")]},
      { "date":"Nov 2021 – May 12, 2022", "months":6, "v_pct":-10, "vol_norm":10.0,
        "volatility":3, "formula":"I ⊗ D ⊗ A", "primary_m2":"m2:Bifurcation",
        "secondary_m2":["m2:Trigger","m2:Threshold","m2:Propagation"],
        "narrative":'"Stablecoin depeg — systemic contagion"',
        "asfid":{"A":0.94,"S":0.84,"F":0.87,"I":0.95,"D":0.97},
        "r0_panic":5.0,"r0_narr":0.1,"r0_regime":"MINSKY MOMENT — R0>>1",
        "force":"Terra/LUNA collapse May 9-12 2022: $40B destroyed in 72h",
        "events":[(0,"Fed begins rate hikes Mar 2022"),(5,"LUNA/UST collapse May 9-12: $40B")]},
      { "date":"May – Nov 2022", "months":6, "v_pct":-8, "vol_norm":2.0,
        "volatility":3, "formula":"F ⊗ D", "primary_m2":"m2:Propagation",
        "secondary_m2":["m2:Cascade","m2:Dissipation","m2:FinancialContagion"],
        "narrative":'"FTX fraud — the whole industry is rotten"',
        "asfid":{"A":0.87,"S":0.81,"F":0.97,"I":0.87,"D":0.97},
        "r0_panic":0.3,"r0_narr":0.05,"r0_regime":"Saturated → SubThreshold",
        "force":"Celsius freeze Jun; 3AC insolvency Jun; Voyager Jul; FTX Nov 8-11",
        "events":[(0,"Celsius Network freezes Jun 2022"),(1,"3 Arrows Capital insolvent"),(2,"Voyager bankrupt Jul"),(5,"FTX collapse Nov 8-11: $32B→$0"),(6,"BTC trough: $15,599")]},
    ],
  },
]


# Chronological order
_BUBBLE_ORDER = ["southsea", "rubber", "wall1929", "japan", "dotcom", "gfc", "crypto"]
BUBBLES.sort(key=lambda b: _BUBBLE_ORDER.index(b["id"]) if b["id"] in _BUBBLE_ORDER else 99)

# ─────────────────────────────────────────────────────────────────────────────
# Curve generation
# ─────────────────────────────────────────────────────────────────────────────
STEPS_PER_MONTH = 8
VOL_NOISE_SEED  = 42

def _volatility_sigma(vol_level):
    return [0.004, 0.010, 0.022, 0.045][vol_level]

def generate_curves(bubble):
    """Return (price_pts, vol_pts, phase_boundaries, event_pts).
    price_pts: list of float (absolute price)
    vol_pts:   list of float (0-1 normalised for display)
    phase_boundaries: list of int (point index where each phase starts)
    event_pts: list of (pt_index, label)
    """
    rng = random.Random(2026)
    price_pts  = []
    vol_pts    = []
    ph_bounds  = []
    evt_pts    = []
    phases     = bubble["phases"]

    price = phases[0]["v_pct"] > 0 and bubble["peak"] / \
            (sum(max(0, p["v_pct"]/100 * p["months"]) for p in phases) + 1) * 0.1
    # Simpler: just start from 100 (normalised) and let velocity drive it
    price = 100.0

    for ph_i, ph in enumerate(phases):
        ph_bounds.append(len(price_pts))
        n_months = ph["months"]
        n_steps  = max(6, int(n_months * STEPS_PER_MONTH))
        sigma    = _volatility_sigma(ph["volatility"])
        v_step   = ph["v_pct"] / 100.0 / STEPS_PER_MONTH  # per step fraction
        vol_base = ph["vol_norm"]

        for ev_month, ev_label in ph.get("events", []):
            ev_step = ph_bounds[-1] + int(ev_month * STEPS_PER_MONTH)
            evt_pts.append((ev_step, ev_label))

        for i in range(n_steps):
            noise = rng.gauss(0, sigma)
            price = price * (1.0 + v_step + noise)
            price = max(price, 0.5)
            price_pts.append(price)
            # Volume: sine ripple + trend
            t = i / max(1, n_steps)
            vol = vol_base * (0.7 + 0.5 * rng.random() + 0.3 * math.sin(t * 4))
            vol_pts.append(vol)

    return price_pts, vol_pts, ph_bounds, evt_pts

def phase_at_point(pt_idx, ph_bounds):
    """Return phase index (0-4) for a given point index."""
    ph = 0
    for i, b in enumerate(ph_bounds):
        if pt_idx >= b:
            ph = i
    return ph

# ─────────────────────────────────────────────────────────────────────────────
# Text helpers
# ─────────────────────────────────────────────────────────────────────────────

def wrap_text(text, font, max_w):
    """Return list of lines fitting within max_w pixels."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fmt_price(p, unit):
    """Format price for display."""
    if p >= 10000:
        return f"{p:,.0f}"
    elif p >= 100:
        return f"{p:,.1f}"
    else:
        return f"{p:.2f}"

# ─────────────────────────────────────────────────────────────────────────────
# Draggable splitter
# ─────────────────────────────────────────────────────────────────────────────

class Splitter:
    H = 5
    def __init__(self, y, y_min, y_max):
        self.y     = y
        self.y_min = y_min
        self.y_max = y_max
        self.drag  = False

    def rect(self):
        return pygame.Rect(RIGHT_X, self.y, RIGHT_W, self.H)

    def handle_event(self, ev):
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if self.rect().inflate(0, 8).collidepoint(ev.pos):
                self.drag = True
        elif ev.type == pygame.MOUSEBUTTONUP:
            self.drag = False
        elif ev.type == pygame.MOUSEMOTION and self.drag:
            self.y = max(self.y_min, min(self.y_max, ev.pos[1]))

    def draw(self, surf):
        r = self.rect()
        col = (65, 75, 110) if self.drag else (40, 48, 80)
        pygame.draw.rect(surf, col, r)
        cx = r.centerx; cy = r.centery
        for dx in (-8, 0, 8):
            pygame.draw.circle(surf, (80, 95, 140), (cx + dx, cy), 2)

# ─────────────────────────────────────────────────────────────────────────────
# Main simulation class
# ─────────────────────────────────────────────────────────────────────────────

class KindlebergerSim:

    SPEEDS = [0.5, 1.0, 2.0, 4.0]
    SPEED_LABELS = ["×0.5", "×1", "×2", "×4"]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
        pygame.display.set_caption(
            "TSCG — Kindleberger-Minsky Financial Crisis Cycle Simulator  v1.1.0"
        )
        self.clock = pygame.time.Clock()

        # Fonts
        self.F = {}
        for key, size, bold in [
            ("title", 18, True), ("lg", 15, True), ("md", 13, True),
            ("sm", 12, False), ("xs", 10, False), ("xxs", 9, False),
            ("mono_lg", 14, True), ("mono_md", 12, True), ("mono_sm", 11, False),
            ("mono_xs", 10, False),
        ]:
            self.F[key]  = pygame.font.SysFont("DejaVuSans", size, bold)
        for key, size, bold in [
            ("mono_lg", 14, True), ("mono_md", 12, True),
            ("mono_sm", 11, False), ("mono_xs", 10, False),
        ]:
            self.F[key] = pygame.font.SysFont("DejaVuSansMono", size, bold)

        # State
        self.bubble_idx      = 0
        self.playhead        = 0.0   # 0.0 → 1.0 of total points
        self.playing         = False
        self.speed_idx       = 1     # ×1
        self.mouse_pos       = (0, 0)
        self.crosshair_x     = -1
        self._selected_phase = 0     # authoritative phase index (no float ambiguity)
        self._scrubbing      = False  # True while dragging timeline in chart

        # Splitters (y positions within window — updated on resize)
        self._init_splitters()

        # Pre-generate all bubble curves
        self.curves = {}
        for b in BUBBLES:
            self.curves[b["id"]] = generate_curves(b)

        # Position cursor at end of phase 0 on startup
        self._jump_phase(0)

        # Buttons — bubble tabs
        self.tab_rects  = []
        self.wiki_rects = []
        self._rebuild_ctrl_rects()

    def _init_splitters(self):
        sp1_y = HEADER_H + (WIN_H - HEADER_H) // 3
        sp2_y = HEADER_H + 2 * (WIN_H - HEADER_H) // 3
        if not hasattr(self, 'sp1'):
            self.sp1 = Splitter(sp1_y, HEADER_H + 80, WIN_H - CTRL_H - 80)
            self.sp2 = Splitter(sp2_y, HEADER_H + 160, WIN_H - CTRL_H - 40)
        else:
            # Re-clamp splitters to new window bounds
            self.sp1.y_min = HEADER_H + 80
            self.sp1.y_max = WIN_H - CTRL_H - 80
            self.sp1.y = max(self.sp1.y_min, min(self.sp1.y_max, sp1_y))
            self.sp2.y_min = HEADER_H + 160
            self.sp2.y_max = WIN_H - CTRL_H - 40
            self.sp2.y = max(self.sp2.y_min, min(self.sp2.y_max, sp2_y))

    def _rebuild_ctrl_rects(self):
        ctrl_y = WIN_H - CTRL_H + 6
        bh = 28; x = 8
        self.btn_play   = pygame.Rect(x, ctrl_y, 82, bh); x += 90
        self.btn_reset  = pygame.Rect(x, ctrl_y, 60, bh); x += 68
        self.btn_phases = []
        for i in range(5):
            self.btn_phases.append(pygame.Rect(x, ctrl_y, 36, bh)); x += 42
        x += 52   # extra gap so "SPEED:" label clears phase button 5
        self.speed_btns = []
        for i in range(4):
            self.speed_btns.append(pygame.Rect(x, ctrl_y, 44, bh)); x += 50

    # ── Accessors ────────────────────────────────────────────────────────────
    @property
    def bubble(self):
        return BUBBLES[self.bubble_idx]

    @property
    def curve_data(self):
        return self.curves[self.bubble["id"]]

    @property
    def price_pts(self):   return self.curve_data[0]
    @property
    def vol_pts(self):     return self.curve_data[1]
    @property
    def ph_bounds(self):   return self.curve_data[2]
    @property
    def evt_pts(self):     return self.curve_data[3]
    @property
    def n_pts(self):       return len(self.price_pts)

    @property
    def current_pt(self):
        return max(1, int(self.playhead * self.n_pts))

    @property
    def current_phase_idx(self):
        return self._selected_phase

    @property
    def current_phase(self):
        return self.bubble["phases"][self.current_phase_idx]

    def _select_bubble(self, idx):
        self.bubble_idx      = idx
        self.playing         = False
        self._selected_phase = 0
        self._jump_phase(0)   # cursor at end of phase 0 for new bubble

    def _scrub_to_x(self, mx):
        """Set playhead from a mouse x position inside the price chart."""
        cw = CHART_W - Y_AXIS_W - 4
        xi = (mx - Y_AXIS_W) / cw
        xi = max(0.0, min(1.0, xi))
        self.playhead = xi
        self.playing  = False
        real_pt = max(0, int(xi * self.n_pts) - 1)
        self._selected_phase = phase_at_point(real_pt, self.ph_bounds)

    def _jump_phase(self, ph_idx):
        self._selected_phase = ph_idx
        bds = self.ph_bounds
        # Jump playhead to the LAST point of the selected phase
        ph_end   = bds[ph_idx + 1] if ph_idx + 1 < len(bds) else self.n_pts
        end_pt   = ph_end - 2        # last index firmly inside the phase
        self.playhead = min(1.0, max(0.0, end_pt / self.n_pts))
        self.playing  = False

    # ── Main loop ────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            if self.playing:
                speed = self.SPEEDS[self.speed_idx]
                advance = speed * dt / (self.n_pts / FPS)
                self.playhead = min(1.0, self.playhead + advance)
                if self.playhead >= 1.0:
                    self.playing = False
                # Keep _selected_phase in sync during playback
                real_pt = max(0, int(self.playhead * self.n_pts) - 1)
                self._selected_phase = phase_at_point(real_pt, self.ph_bounds)
            self._draw()

    def _handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit(); raise SystemExit
                if ev.key == pygame.K_SPACE:
                    self.playing = not self.playing
            if ev.type == pygame.VIDEORESIZE:
                new_w = max(900, ev.w)
                new_h = max(600, ev.h)
                self.screen = pygame.display.set_mode(
                    (new_w, new_h), pygame.RESIZABLE)
                L.update(new_w, new_h)
                self._init_splitters()
                self._rebuild_ctrl_rects()

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self._scrubbing = False

            self.sp1.handle_event(ev)
            self.sp2.handle_event(ev)
            # Ensure sp2 > sp1
            if self.sp2.y < self.sp1.y + 60:
                self.sp2.y = self.sp1.y + 60

            if ev.type == pygame.MOUSEMOTION:
                self.mouse_pos = ev.pos
                mx, my = ev.pos
                if Y_AXIS_W < mx < CHART_W:
                    self.crosshair_x = mx
                else:
                    self.crosshair_x = -1
                # Drag-to-scrub on price chart
                if self._scrubbing and Y_AXIS_W <= mx <= CHART_W:
                    self._scrub_to_x(mx)

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos
                # Click on price/volume chart area → scrub timeline
                in_chart = (Y_AXIS_W <= mx <= CHART_W and
                            PRICE_TOP <= my <= VOL_BOT)
                if in_chart:
                    self._scrubbing = True
                    self._scrub_to_x(mx)
                # Bubble tabs
                for i, r in enumerate(self.tab_rects):
                    if r.collidepoint(mx, my):
                        self._select_bubble(i); break
                # Phase bar segments
                for i, r in enumerate(self.phase_bar_rects):
                    if r.collidepoint(mx, my):
                        self._jump_phase(i); break
                # Play/pause
                if self.btn_play.collidepoint(mx, my):
                    if self.playhead >= 1.0:
                        self.playhead = 0.0
                    self.playing = not self.playing
                # Reset
                if self.btn_reset.collidepoint(mx, my):
                    self.playhead = 0.0; self.playing = False
                    self._selected_phase = 0
                # Phase jump
                for i, r in enumerate(self.btn_phases):
                    if r.collidepoint(mx, my):
                        self._jump_phase(i); break
                # Speed
                for i, r in enumerate(self.speed_btns):
                    if r.collidepoint(mx, my):
                        self.speed_idx = i; break
                # Wiki links
                for r, url in self.wiki_rects:
                    if r.collidepoint(mx, my):
                        webbrowser.open(url); break

    # ── Draw ─────────────────────────────────────────────────────────────────
    def _draw(self):
        s = self.screen
        s.fill(BG)
        self._draw_header()
        self._draw_phase_bar()
        self._draw_price_chart()
        self._draw_vol_chart()
        self._draw_controls()
        self._draw_right_panel()
        # Splitters on top
        self.sp1.draw(s)
        self.sp2.draw(s)
        pygame.display.flip()

    # ── Header ───────────────────────────────────────────────────────────────
    def _draw_header(self):
        s = self.screen
        pygame.draw.rect(s, PANEL, (0, 0, WIN_W, HEADER_H))
        pygame.draw.line(s, BORDER, (0, HEADER_H - 1), (WIN_W, HEADER_H - 1))

        # Logo
        logo = self.F["title"].render("TSCG  KINDLEBERGER-MINSKY", True, GOLD)
        s.blit(logo, (10, 12))
        sub = self.F["xs"].render("M0 Poclet Simulation  ·  M2 v15.9.0  ·  7 Historical Instances", True, DIM)
        s.blit(sub, (10, 30))

        # Bubble tabs
        tab_x = 320
        self.tab_rects = []
        for i, b in enumerate(BUBBLES):
            label  = b["short"]
            tw, th = self.F["mono_sm"].size(label)
            r      = pygame.Rect(tab_x, 8, tw + 18, HEADER_H - 14)
            self.tab_rects.append(r)
            col  = b["color"]
            if i == self.bubble_idx:
                pygame.draw.rect(s, tuple(c // 5 for c in col), r, border_radius=4)
                pygame.draw.rect(s, col, r, 2, border_radius=4)
                tc = col
            else:
                pygame.draw.rect(s, PANEL2, r, border_radius=4)
                pygame.draw.rect(s, BORDER2, r, 1, border_radius=4)
                tc = DIM
            ls = self.F["mono_sm"].render(label, True, tc)
            s.blit(ls, ls.get_rect(center=r.center))
            tab_x += r.w + 6

    # ── Phase bar ────────────────────────────────────────────────────────────
    def _draw_phase_bar(self):
        s     = self.screen
        b     = self.bubble
        total = self.n_pts
        cur   = self.current_phase_idx
        x0    = Y_AXIS_W
        w_bar = CHART_W - Y_AXIS_W
        ph_bounds = self.ph_bounds
        mx_now, my_now = self.mouse_pos

        LBL_WHITE  = (245, 248, 255)
        LBL_NORMAL = (185, 195, 220)

        self.phase_bar_rects = []
        bar_y = HEADER_H
        bar_h = PHASE_BAR_H

        # Track occupied label x-ranges to prevent overlap
        occupied = []   # list of (x_left, x_right) already drawn

        for i, ph_name in enumerate(PHASE_NAMES):
            p_start = ph_bounds[i]
            p_end   = ph_bounds[i + 1] if i + 1 < len(ph_bounds) else total
            seg_w   = int((p_end - p_start) / total * w_bar)
            rx      = x0 + int(p_start / total * w_bar)
            r       = pygame.Rect(rx, bar_y, seg_w - 1, bar_h)
            self.phase_bar_rects.append(r)

            hovered = r.collidepoint(mx_now, my_now)
            if i == cur:
                bg_col = PH_COL[i]
            elif hovered:
                bg_col = tuple(min(255, c + 40) for c in PH_DIM[i])
            else:
                bg_col = PH_DIM[i]

            pygame.draw.rect(s, bg_col, r)

            # Thin separator
            pygame.draw.line(s, (0, 0, 0), (rx, bar_y), (rx, bar_y + bar_h), 1)

            lbl_col = LBL_WHITE if i == cur else LBL_NORMAL

            # Choose label: full name if fits, short if fits, else nothing
            # Also check that it won't collide with already-drawn labels
            for candidate in (PHASE_NAMES[i], PHASE_SHORT[i]):
                lbl = self.F["mono_xs"].render(candidate, True, lbl_col)
                lw = lbl.get_width()
                margin = 8
                if lw > seg_w - margin * 2:
                    continue
                # Center of segment
                cx = rx + seg_w // 2
                lx_left  = cx - lw // 2
                lx_right = cx + lw // 2
                # Check collision with already-drawn labels
                collision = any(lx_left < ox_r + 2 and lx_right > ox_l - 2
                                for ox_l, ox_r in occupied)
                if not collision:
                    s.blit(lbl, lbl.get_rect(center=(cx, bar_y + bar_h // 2)))
                    occupied.append((lx_left, lx_right))
                break

        # Left y-axis area label
        pygame.draw.rect(s, PANEL2, (0, bar_y, Y_AXIS_W, bar_h))
        t = self.F["xxs"].render("PHASE", True, DIM2)
        s.blit(t, (4, bar_y + 7))

    # ── Price chart ──────────────────────────────────────────────────────────
    def _draw_price_chart(self):
        s     = self.screen
        pts   = self.price_pts
        total = self.n_pts
        cp    = self.current_pt
        bds   = self.ph_bounds

        pygame.draw.rect(s, PANEL, (0, PRICE_TOP, CHART_W, PRICE_H))
        pygame.draw.line(s, BORDER, (Y_AXIS_W, PRICE_TOP), (Y_AXIS_W, PRICE_BOT))

        # Y-axis scale uses FULL history so ghost and played share same axis
        p_min = min(pts) * 0.94
        p_max = max(pts) * 1.06
        if p_max == p_min: p_max = p_min + 1

        cw = CHART_W - Y_AXIS_W - 4   # drawable chart width

        def py(price):
            t = (price - p_min) / (p_max - p_min)
            return int(PRICE_BOT - 8 - t * (PRICE_H - 16))
        def px(idx):
            return Y_AXIS_W + int(idx / max(1, total - 1) * cw)

        # Phase background bands
        for i in range(len(PHASE_NAMES)):
            ps = bds[i]
            pe = bds[i + 1] if i + 1 < len(bds) else total
            x1 = px(ps); x2 = px(pe)
            if x2 > x1:
                pygame.draw.rect(s, PH_BG[i], (x1, PRICE_TOP, x2 - x1, PRICE_H))

        # Horizontal grid + y-axis labels
        for tick in range(6):
            t = tick / 5
            price_tick = p_min + t * (p_max - p_min)
            yg = py(price_tick)
            if PRICE_TOP < yg < PRICE_BOT:
                pygame.draw.line(s, BORDER2, (Y_AXIS_W, yg), (CHART_W, yg))
                label = fmt_price(price_tick, "")
                ls = self.F["mono_xs"].render(label, True, DIM)
                s.blit(ls, (2, yg - 7))

        # Phase boundary vertical lines
        for i, pb in enumerate(bds[1:], 1):
            xv = px(pb)
            pygame.draw.line(s, PH_DIM[i], (xv, PRICE_TOP), (xv, PRICE_BOT), 1)

        # ── Colour constants ──────────────────────────────────────────────────────
        WHITE_FULL = (255, 255, 255)   # pure white — current phase (3px)
        WHITE_DIM  = (175, 182, 205)   # dim white  — rest of history (2px)
        WHITE_GHOST= (88,  96, 125)    # very dim   — future / ghost (1px)

        cur_ph_start = bds[self.current_phase_idx]
        cur_ph_end   = bds[self.current_phase_idx + 1] if self.current_phase_idx + 1 < len(bds) else total

        # ── Full historical ghost (future of playhead) — very dim white 1px ───
        for j in range(max(cp, 1), total):
            xa = px(j - 1); ya = py(pts[j - 1])
            xb = px(j);     yb = py(pts[j])
            ya = max(PRICE_TOP, min(PRICE_BOT, ya))
            yb = max(PRICE_TOP, min(PRICE_BOT, yb))
            pygame.draw.line(s, WHITE_GHOST, (xa, ya), (xb, yb), 1)

        # ── Ghost event ticks (future) ────────────────────────────────────────
        for ev_idx, ev_label in self.evt_pts:
            if ev_idx >= cp:
                xv = px(ev_idx)
                pygame.draw.line(s, (38, 45, 68), (xv, PRICE_TOP + 2), (xv, PRICE_BOT - 2), 1)

        # ── Played curve — draw in 3 segments by thickness ────────────────────
        if cp > 1:
            # a) Before current phase — dim white 2px
            for j in range(1, min(cp, cur_ph_start)):
                xa = px(j-1); ya = py(pts[j-1])
                xb = px(j);   yb = py(pts[j])
                ya = max(PRICE_TOP, min(PRICE_BOT, ya))
                yb = max(PRICE_TOP, min(PRICE_BOT, yb))
                pygame.draw.line(s, WHITE_DIM, (xa, ya), (xb, yb), 2)
            # b) Current phase — pure white 3px
            for j in range(max(1, cur_ph_start), cp):
                xa = px(j-1); ya = py(pts[j-1])
                xb = px(j);   yb = py(pts[j])
                ya = max(PRICE_TOP, min(PRICE_BOT, ya))
                yb = max(PRICE_TOP, min(PRICE_BOT, yb))
                pygame.draw.line(s, WHITE_FULL, (xa, ya), (xb, yb), 3)

            # Playhead dot — phase colour
            ph_col = PH_COL[self.current_phase_idx]
            cx_ = px(cp - 1); cy_ = py(pts[cp - 1])
            cy_ = max(PRICE_TOP + 5, min(PRICE_BOT - 5, cy_))
            pygame.draw.circle(s, ph_col,      (cx_, cy_), 7)
            pygame.draw.circle(s, WHITE_FULL,  (cx_, cy_), 7, 2)

        # ── Event markers (played) ─────────────────────────────────────────────
        EV_COL      = (165, 160, 75)
        ROW_H       = 11                    # pixel height per row
        N_ROWS      = 5                     # max stagger rows
        row_next_x  = [Y_AXIS_W] * N_ROWS  # next free x per row
        max_row_used = -1                   # highest row index actually drawn

        for ev_idx, ev_label in self.evt_pts:
            if ev_idx < cp:
                xv = px(ev_idx)
                pygame.draw.line(s, EV_COL, (xv, PRICE_TOP + 2), (xv, PRICE_BOT - 2), 1)
                abbr = ev_label[:22]
                ms   = self.F["xxs"].render(abbr, True, EV_COL)
                lw   = ms.get_width()
                for row in range(N_ROWS):
                    if xv + 3 >= row_next_x[row]:
                        yoff = PRICE_TOP + 4 + row * ROW_H
                        s.blit(ms, (xv + 3, yoff))
                        row_next_x[row] = xv + 3 + lw + 4
                        if row > max_row_used:
                            max_row_used = row
                        break
                # If no row fits, tick line already drawn, skip label

        # ── Crosshair + tooltip ───────────────────────────────────────────────
        if self.crosshair_x > 0 and Y_AXIS_W < self.crosshair_x < CHART_W:
            xi = int((self.crosshair_x - Y_AXIS_W) / cw * (total - 1))
            xi = max(0, min(total - 1, xi))
            cross_price = pts[xi]
            cxp = px(xi)
            cyp = py(cross_price)
            cyp = max(PRICE_TOP + 1, min(PRICE_BOT - 1, cyp))
            pygame.draw.line(s, (70, 90, 130), (cxp, PRICE_TOP), (cxp, PRICE_BOT), 1)
            pygame.draw.line(s, (70, 90, 130), (Y_AXIS_W, cyp),  (CHART_W, cyp),   1)
            b_data  = self.bubble
            ph_idx  = phase_at_point(xi, bds)
            ph_info = b_data["phases"][ph_idx]
            scaled  = cross_price * b_data["peak"] / max(pts)
            ahead   = xi >= cp
            tip_lines = [
                fmt_price(scaled, "") + "  " + b_data["unit"],
                PHASE_NAMES[ph_idx],
                ph_info["date"],
                ">> ahead" if ahead else "OK played",
            ]
            tip_w = max(self.F["mono_sm"].size(l)[0] for l in tip_lines) + 16
            tip_h = len(tip_lines) * 18 + 10
            tip_x = min(cxp + 8, CHART_W - tip_w - 4)
            tip_y = max(PRICE_TOP + 4, cyp - tip_h - 4)
            pygame.draw.rect(s, PANEL2, (tip_x, tip_y, tip_w, tip_h), border_radius=4)
            pygame.draw.rect(s, BORDER,  (tip_x, tip_y, tip_w, tip_h), 1, border_radius=4)
            for li, line in enumerate(tip_lines):
                c = (PH_COL[ph_idx] if li == 1
                     else ((180, 150, 60) if (li == 0 and ahead) else
                           (DIM if li >= 2 else TEXT)))
                ls = self.F["mono_sm"].render(line, True, c)
                s.blit(ls, (tip_x + 8, tip_y + 6 + li * 18))

        # Title — placed just below the last event label row actually drawn
        t = self.F["xs"].render(
            "ASSET PRICE (peak-scaled)   dim=history   white=played   thick=current phase",
            True, DIM)
        rows_used = max_row_used + 1 if max_row_used >= 0 else 0
        legend_y  = PRICE_TOP + 4 + rows_used * ROW_H + 4
        s.blit(t, (Y_AXIS_W + 4, legend_y))

    # ── Volume chart ─────────────────────────────────────────────────────────
    def _draw_vol_chart(self):
        s     = self.screen
        pts   = self.vol_pts
        total = self.n_pts
        cp    = self.current_pt
        bds   = self.ph_bounds

        pygame.draw.rect(s, PANEL2, (0, VOL_TOP, CHART_W, VOL_H))
        pygame.draw.line(s, BORDER, (0, VOL_TOP), (CHART_W, VOL_TOP))
        pygame.draw.line(s, BORDER, (Y_AXIS_W, VOL_TOP), (Y_AXIS_W, VOL_BOT))

        # Scale on FULL history
        v_max = max(pts) * 1.1 if pts else 1.0
        if v_max == 0: v_max = 1.0

        bar_w = max(1, int((CHART_W - Y_AXIS_W) / total))
        x0    = Y_AXIS_W
        usable_h = VOL_H - 16

        def vx(i): return x0 + int(i / max(1, total) * (CHART_W - Y_AXIS_W))

        # Bright pastels for each phase
        PH_PASTEL_FULL = [
            (175, 215, 255),   # DISPLACEMENT — sky blue
            (140, 255, 190),   # BOOM         — mint green
            (255, 230, 100),   # EUPHORIA     — gold
            (255, 145, 145),   # DISTRESS     — coral
            (220, 165, 255),   # REVULSION    — lavender
        ]
        # Mid-brightness: ~55% of full — clearly visible but secondary
        PH_PASTEL_MID  = [tuple(int(c * 0.78) for c in col) for col in PH_PASTEL_FULL]
        # Ghost (future): per-phase very dim — ~20%
        PH_PASTEL_GHOST= [tuple(int(c * 0.35) for c in col) for col in PH_PASTEL_FULL]

        cur_ph = self.current_phase_idx

        # ── GHOST bars: future (beyond playhead) — very dim per-phase ─────────
        for i in range(min(cp, total), total):
            ph_i = phase_at_point(i, bds)
            bx   = vx(i)
            bh   = max(1, int(pts[i] / v_max * usable_h))
            by   = VOL_BOT - bh
            pygame.draw.rect(s, PH_PASTEL_GHOST[ph_i], (bx, by, max(1, bar_w - 1), bh))

        # ── PLAYED bars: current phase = full bright, others = mid ────────────
        for i in range(min(cp, total)):
            ph_i     = phase_at_point(i, bds)
            draw_col = PH_PASTEL_FULL[ph_i] if ph_i == cur_ph else PH_PASTEL_MID[ph_i]
            bx   = vx(i)
            bh   = max(1, int(pts[i] / v_max * usable_h))
            by   = VOL_BOT - bh
            pygame.draw.rect(s, draw_col, (bx, by, max(1, bar_w - 1), bh))

        # Y axis grid + tick labels
        for tick_v in [0.25, 0.5, 0.75, 1.0]:
            yg = int(VOL_BOT - tick_v * usable_h)
            pygame.draw.line(s, BORDER2, (Y_AXIS_W, yg), (CHART_W, yg))
            ls = self.F["xxs"].render(f"{tick_v:.0%}", True, DIM2)
            s.blit(ls, (2, yg - 7))

        # Title
        t = self.F["xs"].render(
            "TRANSACTION VOLUME  (normalised)   ghost = full history   bright = played",
            True, DIM)
        s.blit(t, (Y_AXIS_W + 4, VOL_TOP + 3))

    def _draw_controls(self):
        s = self.screen
        pygame.draw.rect(s, PANEL, (0, WIN_H - CTRL_H, CHART_W, CTRL_H))
        pygame.draw.line(s, BORDER, (0, WIN_H - CTRL_H), (CHART_W, WIN_H - CTRL_H))

        def btn(rect, label, active=False, col=None):
            if col is None:
                col = tuple(min(255, c + 30) for c in PH_COL[self.current_phase_idx]) if active else PANEL2
            pygame.draw.rect(s, col, rect, border_radius=4)
            pygame.draw.rect(s, BORDER if not active else PH_COL[self.current_phase_idx], rect, 1, border_radius=4)
            ls = self.F["mono_sm"].render(label, True, TEXT if active else DIM)
            s.blit(ls, ls.get_rect(center=rect.center))

        # Play/Pause
        play_lbl = "⏸ PAUSE" if self.playing else "▶ PLAY"
        btn(self.btn_play, play_lbl, active=self.playing)
        btn(self.btn_reset, "RESET")

        # Phase jump
        s.blit(self.F["xs"].render("PHASE:", True, DIM2),
               (self.btn_phases[0].x - 42, self.btn_phases[0].y + 7))
        for i, r in enumerate(self.btn_phases):
            is_cur = (i == self.current_phase_idx)
            c = PH_COL[i] if is_cur else PANEL2
            pygame.draw.rect(s, c, r, border_radius=3)
            pygame.draw.rect(s, PH_COL[i], r, 1, border_radius=3)
            ls = self.F["mono_xs"].render(str(i + 1), True, TEXT if is_cur else PH_DIM[i])
            s.blit(ls, ls.get_rect(center=r.center))

        # Speed
        x_sp = self.speed_btns[0].x - 50
        s.blit(self.F["xs"].render("SPEED:", True, DIM2),
               (x_sp, self.speed_btns[0].y + 7))
        for i, r in enumerate(self.speed_btns):
            btn(r, self.SPEED_LABELS[i], active=(i == self.speed_idx))

        # Progress bar
        prog_x = self.speed_btns[-1].right + 12
        prog_w = CHART_W - prog_x - 10
        prog_r = pygame.Rect(prog_x, WIN_H - CTRL_H + 14, prog_w, 10)
        pygame.draw.rect(s, SLIDER_BG, prog_r, border_radius=3)
        fill_w = int(prog_w * self.playhead)
        col = PH_COL[self.current_phase_idx]
        pygame.draw.rect(s, col, pygame.Rect(prog_x, prog_r.y, fill_w, 10), border_radius=3)
        pygame.draw.rect(s, BORDER, prog_r, 1, border_radius=3)

        # Current phase text
        ph = self.current_phase
        t  = self.F["mono_xs"].render(
            f"▶  {PHASE_NAMES[self.current_phase_idx]}  |  {ph['date']}",
            True, PH_COL[self.current_phase_idx])
        s.blit(t, (prog_x, WIN_H - CTRL_H + 28))

    # ── Right panel ──────────────────────────────────────────────────────────
    def _draw_right_panel(self):
        s  = self.screen
        b  = self.bubble
        ph = self.current_phase
        pi = self.current_phase_idx
        col = PH_COL[pi]

        # Panel background
        pygame.draw.rect(s, PANEL, (RIGHT_X, HEADER_H, RIGHT_W, WIN_H - HEADER_H))
        pygame.draw.line(s, BORDER, (RIGHT_X, HEADER_H), (RIGHT_X, WIN_H))

        sp1y = self.sp1.y
        sp2y = self.sp2.y

        # Clip regions
        self._draw_tscg_panel(RIGHT_X, HEADER_H, RIGHT_W, sp1y - HEADER_H, ph, pi, col)
        self._draw_episode_panel(RIGHT_X, sp1y + Splitter.H, RIGHT_W,
                                 sp2y - sp1y - Splitter.H, b, ph, pi, col)
        self._draw_metrics_panel(RIGHT_X, sp2y + Splitter.H, RIGHT_W,
                                 WIN_H - sp2y - Splitter.H, b, ph, pi, col)

    def _panel_header(self, x, y, w, label, badge, col):
        s = self.screen
        pygame.draw.rect(s, tuple(c // 6 for c in col), (x, y, w, 22))
        pygame.draw.line(s, tuple(c // 2 for c in col), (x, y + 22), (x + w, y + 22))
        t = self.F["mono_sm"].render(label, True, col)
        s.blit(t, (x + 8, y + 3))
        bs = self.F["mono_xs"].render(badge, True, col)
        s.blit(bs, (x + w - bs.get_width() - 8, y + 4))
        return y + 26

    def _draw_tscg_panel(self, px, py, pw, ph_h, ph, pi, col):
        s  = self.screen
        clip = pygame.Rect(px, py, pw, ph_h)
        s.set_clip(clip)

        y = self._panel_header(px, py, pw, "TSCG  MAPPING", f"M2  v15.9.0", col)
        lm = px + 10

        # Phase name + formula
        name_surf = self.F["lg"].render(PHASE_NAMES[pi], True, col)
        s.blit(name_surf, (lm, y + 2))
        formula_surf = self.F["mono_lg"].render(f"  {ph['formula']}", True, col)
        s.blit(formula_surf, (lm + name_surf.get_width() + 6, y + 4))
        y += name_surf.get_height() + 4

        # Primary M2
        pm2 = ph["primary_m2"]
        pm2_s = self.F["mono_md"].render(f"PRIMARY:  {pm2}", True, col)
        pygame.draw.rect(s, tuple(c // 7 for c in col), (lm - 4, y, pw - 14, 20), border_radius=3)
        pygame.draw.rect(s, tuple(c // 2 for c in col), (lm - 4, y, pw - 14, 20), 1, border_radius=3)
        s.blit(pm2_s, (lm + 2, y + 1))
        y += 24

        # Secondary M2 chips
        sec = ph.get("secondary_m2", [])
        cx = lm; chip_y = y
        for m2 in sec:
            short = m2.replace("m2:", "")
            cs    = self.F["mono_xs"].render(short, True, DIM)
            cw    = cs.get_width() + 10
            if cx + cw > px + pw - 8:
                cx = lm; chip_y += 18
            pygame.draw.rect(s, PANEL2, (cx, chip_y, cw, 15), border_radius=2)
            pygame.draw.rect(s, BORDER2, (cx, chip_y, cw, 15), 1, border_radius=2)
            s.blit(cs, (cx + 5, chip_y + 1))
            cx += cw + 4
        y = chip_y + 20

        # Narrative
        narr = ph.get("narrative", "")
        pygame.draw.rect(s, (16, 20, 36), (lm - 4, y, pw - 14, 1))
        y += 2
        ns  = self.F["sm"].render("NARRATIVE:", True, DIM2)
        s.blit(ns, (lm, y)); y += 16
        for line in wrap_text(narr, self.F["sm"], pw - 24):
            ls = self.F["sm"].render(line, True, (200, 185, 120))
            s.blit(ls, (lm, y)); y += 16
        y += 4

        # ASFID bars
        asfid = ph["asfid"]
        asfid_label = self.F["mono_xs"].render("ASFID  SCORES:", True, DIM2)
        s.blit(asfid_label, (lm, y)); y += 15
        bar_w = pw - 60
        for dim in ["A", "S", "F", "I", "D"]:
            val = asfid[dim]
            dl  = self.F["mono_md"].render(dim, True, col)
            s.blit(dl, (lm, y))
            bx  = lm + 18
            pygame.draw.rect(s, SLIDER_BG, (bx, y + 2, bar_w, 10), border_radius=3)
            fill = int(bar_w * val)
            pygame.draw.rect(s, col, (bx, y + 2, fill, 10), border_radius=3)
            vl  = self.F["mono_xs"].render(f"{val:.2f}", True, TEXT)
            s.blit(vl, (bx + bar_w + 4, y + 1))
            y += 16

        # R0
        r0p  = ph.get("r0_panic", 0)
        r0n  = ph.get("r0_narr", 0)
        reg  = ph.get("r0_regime", "")
        y   += 4
        r0l  = self.F["mono_xs"].render(
            f"R₀ panic={r0p:.1f}   R₀ narrative={r0n:.1f}", True, DIM)
        s.blit(r0l, (lm, y)); y += 14
        reg_col = RED_C if "MINSKY" in reg else (GREEN if "Supra" in reg else DIM)
        rs  = self.F["mono_xs"].render(reg, True, reg_col)
        s.blit(rs, (lm, y))

        s.set_clip(None)

    def _draw_episode_panel(self, px, py, pw, ph_h, b, ph, pi, col):
        s  = self.screen
        clip = pygame.Rect(px, py, pw, ph_h)
        s.set_clip(clip)

        y = self._panel_header(px, py, pw, "EPISODE", b["short"], col)
        lm = px + 10

        # Asset + period
        asset_s = self.F["md"].render(b["asset"], True, TEXT)
        s.blit(asset_s, (lm, y)); y += 18
        period_s = self.F["mono_xs"].render(
            f"{b['total_cycle']}  ·  {b['unit']}", True, DIM)
        s.blit(period_s, (lm, y)); y += 16

        # Phase date
        ph_date_s = self.F["mono_xs"].render(
            f"Phase: {ph['date']}", True, col)
        s.blit(ph_date_s, (lm, y)); y += 18

        # Description — wrapped
        desc_label = self.F["xxs"].render("CONTEXT:", True, DIM2)
        s.blit(desc_label, (lm, y)); y += 13
        for line in wrap_text(b["description"], self.F["xs"], pw - 22):
            if y + 13 > py + ph_h - 60:
                break
            ls = self.F["xs"].render(line, True, DIM)
            s.blit(ls, (lm, y)); y += 13
        y += 4

        # Dominant force of current phase
        force = ph.get("force", "")
        pygame.draw.rect(s, tuple(c // 7 for c in col), (lm - 4, y, pw - 14, 1))
        y += 3
        fl = self.F["xxs"].render("DRIVER:", True, DIM2)
        s.blit(fl, (lm, y)); y += 13
        for line in wrap_text(force, self.F["xs"], pw - 22):
            if y + 13 > py + ph_h - 44:
                break
            ls = self.F["xs"].render(line, True, (180, 200, 160))
            s.blit(ls, (lm, y)); y += 13
        y += 4

        # Wikipedia links
        self.wiki_rects = []
        wl_label = self.F["xxs"].render("REFERENCES:", True, DIM2)
        s.blit(wl_label, (lm, y)); y += 13
        for link_label, url in b.get("wiki", []):
            if y + 18 > py + ph_h - 2:
                break
            r = pygame.Rect(lm, y, pw - 22, 16)
            pygame.draw.rect(s, PANEL2, r, border_radius=2)
            pygame.draw.rect(s, BORDER2, r, 1, border_radius=2)
            mx, my_ = self.mouse_pos
            hov = r.collidepoint(mx, my_)
            link_col = ACCENT if hov else (80, 140, 220)
            ls = self.F["xs"].render(f"↗  {link_label}", True, link_col)
            s.blit(ls, (lm + 4, y + 1))
            self.wiki_rects.append((r, url))
            y += 20

        s.set_clip(None)

    def _draw_metrics_panel(self, px, py, pw, ph_h, b, ph, pi, col):
        s  = self.screen
        clip = pygame.Rect(px, py, pw, min(ph_h, WIN_H - py))
        s.set_clip(clip)

        y = self._panel_header(px, py, pw, "METRICS", f"Phase {pi+1}/5", col)
        lm = px + 10

        def metric_row(label, value, vc=TEXT):
            nonlocal y
            if y + 16 > py + ph_h - 2:
                return
            ls = self.F["mono_xs"].render(label.ljust(20), True, DIM)
            vs = self.F["mono_sm"].render(str(value), True, vc)
            s.blit(ls, (lm, y))
            s.blit(vs, (lm + 160, y))
            y += 16

        def section(title):
            nonlocal y
            y += 4
            pygame.draw.line(s, BORDER2, (lm, y), (px + pw - 14, y))
            y += 2
            ts = self.F["xxs"].render(title, True, DIM2)
            s.blit(ts, (lm, y)); y += 14

        # Price metrics
        section("ASSET PRICE")
        max_pts = max(self.price_pts) if self.price_pts else 1
        scale   = b["peak"] / max_pts
        cur_scaled = self.price_pts[self.current_pt - 1] * scale if self.current_pt > 0 else 0
        metric_row("Start (Displ.)",    fmt_price(b["peak"] / b["multiplier"], "") + f" {b['unit']}")
        metric_row("Peak (Euphoria)",   fmt_price(b["peak"], "") + f" {b['unit']}", col)
        metric_row("Trough (Revulsion)",fmt_price(b["trough"], "") + f" {b['unit']}", RED_C)
        metric_row("Current (scaled)",  fmt_price(cur_scaled, "") + f" {b['unit']}", col)

        section("CYCLE STATISTICS")
        metric_row("Drawdown from peak", f"{b['drawdown_pct']:.1f}%", RED_C)
        metric_row("Multiplier (×base)", f"×{b['multiplier']:.1f}", GREEN)
        metric_row("Total cycle",        b["total_cycle"])

        section("CURRENT PHASE DYNAMICS")
        vels = {
            0: "+15%", 1: "+35%", 2: "+100%", 3: "-500%", 4: "-90%"
        }
        acc_signs = {0: "+", 1: "++", 2: "+→0", 3: "−−−", 4: "−−−→0"}
        vol_table = {
            0: "1.0×", 1: "5.0×", 2: "20.0×", 3: "0.5×", 4: "0.01×"
        }
        volatility_map = ["Low", "Medium", "High", "Extreme"]

        metric_row("Phase velocity",     ph["v_pct"] and f"{ph['v_pct']:+.0f}%/month" or "–")
        metric_row("Acceleration",       acc_signs.get(pi, "?"),
                   RED_C if pi == 3 else (GREEN if pi == 1 else TEXT))
        metric_row("Vol. normalised",    f"{ph['vol_norm']:.1f}×  baseline")
        metric_row("Volatility",         volatility_map[ph["volatility"]],
                   RED_C if ph["volatility"] >= 2 else TEXT)
        metric_row("R₀ panic",           f"{ph.get('r0_panic',0):.2f}",
                   RED_C if ph.get('r0_panic', 0) > 1 else GREEN)
        metric_row("R₀ narrative",       f"{ph.get('r0_narr',0):.2f}")
        metric_row("Regime",             ph.get("r0_regime", "–"),
                   RED_C if "MINSKY" in ph.get("r0_regime","") else TEXT)

        section("TSCG SCORES  (M0 Poclet)")
        asfid = ph["asfid"]
        mean_asfid = sum(asfid.values()) / len(asfid)
        metric_row("ASFID mean",         f"{mean_asfid:.2f}", col)
        metric_row("REVOI mean",         "0.82", DIM)
        metric_row("Epistemic gap δΘ",   "0.09", DIM)

        s.set_clip(None)


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sim = KindlebergerSim()
    sim.run()
