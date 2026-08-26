#!/usr/bin/env python3
"""
FireTriangle README alignment — bring M0_FireTriangle_README.md in line with the
v2.0.0 conformant instance. Applies the same decisions as the instance rewrite:
  D1 = canonical M2 formulas (read from HEAD)
  D2 = structural-grammar alignment (drop ket/Hilbert vectors + norms; canonical gap)
Each replacement is asserted: if a source string is not found, the script fails loud.

Run from repo root. Markdown only — no ORIVE/score write-path risk.
"""
import sys

SRC = "instances/poclets/FireTriangle/M0_FireTriangle_README.md"
DST = SRC  # in-place

with open(SRC, encoding="utf-8") as f:
    t = f.read()

# (old, new) — order-independent; every old must be present exactly once
REPL = [
    # --- Signature formula (D1 canonical) ---
    ("Signature** (GenericConcept **I\u2297F**)",
     "Signature** (GenericConcept **It \u00d7 Ss | V**)"),
    ("**Signature** GenericConcept (I\u2297F)",
     "**Signature** GenericConcept (It \u00d7 Ss | V)"),

    # --- Synergy principle (⊕ -> ×) ---
    ("`Fuel \u2295 O\u2082 \u2295 Heat \u2192 Fire (emergent)`",
     "`Fuel \u00d7 O\u2082 \u00d7 Heat \u2192 Fire (emergent)`"),

    # --- Territory ket vector + norm (D2) ---
    ("**ASFID State Vector**: `|\u03a9_fire\u27e9 = 0.85|A\u27e9 + 0.70|S\u27e9 + 0.90|F\u27e9 + 0.65|It\u27e9 + 0.75|D\u27e9`",
     "**ASFID scores** (Territory / Eagle Eye): A=0.85 \u00b7 S=0.70 \u00b7 F=0.90 \u00b7 It=0.65 \u00b7 D=0.75"),
    ("\n\n**Norm**: 1.734\n", "\n"),

    # --- Map ket vector (D2) ---
    ("**REVOI State Vector**: `|M_triangle\u27e9_REVOI = 0.80|O\u27e9 + 0.90|R\u27e9 + 0.90|Im\u27e9 + 0.95|V\u27e9 + 0.70|E\u27e9`",
     "**REVOI scores** (Map / Sphinx Eye): R=0.90 \u00b7 E=0.70 \u00b7 V=0.95 \u00b7 O=0.80 \u00b7 Im=0.90"),

    # --- REVOI 5th dimension mislabel It -> Im ---
    ("| **It_score** (Interoperability) | 0.90 | Highly shareable",
     "| **Im_score** (Interoperability) | 0.90 | Highly shareable"),

    # --- Comparison table: rename row, drop Hilbert norm row ---
    ("| **State Vector** | ASFID: (0.85, 0.70, 0.90, 0.65, 0.75) | REVOI: (0.90, 0.70, 0.95, 0.80, 0.90) \u00b7 Map ASFID: (0.75, 0.90, 0.60, 0.80, 0.50) |\n| **Norm** | 1.734 | (calculated from REVOI) |\n",
     "| **Scores** | ASFID: (0.85, 0.70, 0.90, 0.65, 0.75) | REVOI: (0.90, 0.70, 0.95, 0.80, 0.90) \u00b7 Map ASFID: (0.75, 0.90, 0.60, 0.80, 0.50) |\n"),

    # --- Epistemic Gap section (D2: canonical gap + keep per-dim divergence) ---
    ("**Formula**: `\u0394\u0398 = \u2016|\u03a9_fire\u27e9 - |M_triangle\u27e9\u2016`\n\n"
     "**Delta Vector (Territory - Map)**: `(+0.10, -0.20, +0.30, -0.15, +0.25)`\n\n"
     "**Gap Norm**: **0.474**\n\n"
     "**Interpretation**: **Moderate gap** (0 < \u0394\u0398 < 0.5)\n\n"
     "**Assessment**: Model is reasonably good - captures essence but simplifies reality\n",
     "**Canonical gap (root)**: `m0:epistemicGap = |asfidMean \u2212 revoiMean| / \u221a2 = |0.71 \u2212 0.85| / \u221a2 = 0.099`\n\n"
     "**Interpretation**: **Small gap** \u2014 the model's Territory-competence (asfidMean 0.71) and Map-competence (revoiMean 0.85) are close.\n\n"
     "### Territory-vs-Map per-dimension divergence\n\n"
     "Beyond the scalar gap, the model ASFID profile diverges from the observed-fire ASFID profile per dimension.\n\n"
     "**Delta (observed \u2212 model)**: `(A +0.10, S \u22120.20, F +0.30, It \u22120.15, D +0.25)`\n\n"
     "**Assessment**: Model captures the essence but simplifies reality (largest divergences on F, D, S).\n"),

    # --- Critical GenericConcepts formulas (D1 canonical; | escaped for md table) ---
    ("| **Component** | Identifies Fuel, O\u2082, Heat as elementary parts | S\u2297I |",
     "| **Component** | Identifies Fuel, O\u2082, Heat as elementary parts | St \u00d7 It \\| L |"),
    ("| **Synergy** | Explains emergence (1+1+1 = Fire, not 3) | A\u2297S\u2297I |",
     "| **Synergy** | Explains emergence (1+1+1 = Fire, not 3) | It \u00d7 D \\| _^ |"),
    ("| **Composition** | Bottom-up assembly of components into system | S\u2297I\u2297A |",
     "| **Composition** | Bottom-up assembly of components into system | St \u00d7 It \u00d7 A \\| _^ |"),
    ("| **Trigger** | Heat initiates process when threshold crossed | D\u2297I |",
     "| **Trigger** | Heat initiates process when threshold crossed | D \u00d7 It |"),
    ("| **Process** | Combustion as dynamic transformation | D\u2297F |",
     "| **Process** | Combustion as dynamic transformation | D \u00d7 F |"),

    # --- Firefighter observer: It->Im in REVOI state, drop ket ---
    ("(R_score:0.80, E_score:0.75, V_score:0.85, O_score:0.85, It_score:0.60)",
     "(R_score:0.80, E_score:0.75, V_score:0.85, O_score:0.85, Im_score:0.60)"),
    ("- **State Vector**: |M_firefighter\u27e9_REVOI = 0.80|R\u27e9 + 0.75|E\u27e9 + 0.85|V\u27e9 + 0.85|O\u27e9 + 0.60|Im\u27e9\n",
     ""),

    # --- Validation summary gap ---
    ("**Epistemic Gap**: **\u0394\u0398 = 0.474** (Moderate - acceptable)",
     "**Epistemic Gap**: **0.099** (Small - well-balanced)"),

    # --- Layer diagram synergy line ---
    ("  \u2514\u2500 Fire Triangle: Fuel \u2295 O\u2082 \u2295 Heat \u2192 Fire",
     "  \u2514\u2500 Fire Triangle: Fuel \u00d7 O\u2082 \u00d7 Heat \u2192 Fire"),

    # --- Footer: version, date, URI path fix ---
    ("**Version**: 1.1  ", "**Version**: 2.0.0  "),
    ("**Last Updated**: 2026-02-24", "**Last Updated**: 2026-08-21"),
    ("**URI**: `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/poclets/FireTriangle/M0_FireTriangle.jsonld`",
     "**URI**: `https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/poclets/FireTriangle/M0_FireTriangle.jsonld`"),
]

missing = []
for old, new in REPL:
    n = t.count(old)
    if n != 1:
        missing.append((old[:60], n))
    else:
        t = t.replace(old, new)

if missing:
    print("ABORT — these source strings were not found exactly once:")
    for frag, n in missing:
        print(f"  count={n}  «{frag}...»")
    sys.exit(1)

with open(DST, "w", encoding="utf-8") as f:
    f.write(t)

print("Patched", DST)
for glyph, name in [("\u2297", "otimes"), ("\u2295", "oplus"),
                    ("\u27e9", "ket"), ("\u2016", "norm"), ("0.474", "old-gap")]:
    print(f"  residual {name}: {t.count(glyph)}")
