#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reasoner.py - TSCG Metaconcept Reasoner

Given a ClassificationResult from MetaconceptClassifier, produces a
ReasoningResult that adds three layers of systemic inference:

  1. ASFID Profile     — aggregate dominant M3 dimensions across all candidates
                         (score-weighted) → dimension fingerprint + suggested
                         tensor formula for the system under analysis.
  2. Family Grouping   — cluster candidates into M2 semantic families
                         (Structural, Dynamic, Regulatory, Adaptive, …).
  3. Composite Inference — detect when all component metaconcepts of a known
                         composite (FeedbackLoop, Cascade, LALI, ButterflyEffect)
                         appear in the candidates and flag the composite.

The reasoner is pure in-process logic: it requires no RAG database, no model
loading, and no external I/O.  It operates solely on ClassificationResult data.

Usage (CLI):
  python reasoner.py "A thermostat maintains temperature via negative feedback"
  python reasoner.py "..." --top-k 10 --verbose
  python reasoner.py "..." --json

Usage (API):
  from tscg.engine.classifier import MetaconceptClassifier
  from tscg.engine.reasoner import MetaconceptReasoner

  clf    = MetaconceptClassifier()
  result = clf.classify("A thermostat maintains temperature via negative feedback")

  rsn    = MetaconceptReasoner()
  report = rsn.reason(result)
  rsn.display(report)

Author: Echopraxium with the collaboration of Claude AI
"""

import re
import sys
import json
import argparse
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Force UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# ==============================================================================
# STATIC KNOWLEDGE BASE
# ==============================================================================

# M3 ASFID dimensions (Eagle Eye / Territory)
_ASFID_DIMS = {"A", "S", "F", "I", "D"}

# M2 label → semantic family
_LABEL_TO_FAMILY: Dict[str, str] = {
    # Structural
    "Hierarchy": "Structural",
    "Network": "Structural",
    "Symmetry": "Structural",
    "Modularity": "Structural",
    "Topology": "Structural",
    "Segmentation": "Structural",
    "Invariant": "Structural",
    "Capacity": "Structural",
    "Storage": "Structural",
    "Substrate": "Structural",
    "Node": "Structural",
    "Path": "Structural",
    # Dynamic
    "Transformation": "Dynamic",
    "Process": "Dynamic",
    "Trajectory": "Dynamic",
    "Event": "Dynamic",
    "Bifurcation": "Dynamic",
    "Behavior": "Dynamic",
    "Workflow": "Dynamic",
    "Synergy": "Dynamic",
    "Step": "Dynamic",
    "Action": "Dynamic",
    # Regulatory
    "Homeostasis": "Regulatory",
    "Regulation": "Regulatory",
    "Constraint": "Regulatory",
    "Scope": "Regulatory",
    "Threshold": "Regulatory",
    "Trigger": "Regulatory",
    "Activation": "Regulatory",
    # Adaptive
    "Resilience": "Adaptive",
    "Adaptation": "Adaptive",
    "Emergence": "Adaptive",
    "Memory": "Adaptive",
    # Energetic
    "Dissipation": "Energetic",
    "Convergence": "Energetic",
    "Divergence": "Energetic",
    "Flow": "Energetic",
    # Regulatory (additional variants found in DB)
    "Balance": "Regulatory",            # synonym/variant of Homeostasis
    # Informational
    "Code": "Informational",
    "Coding": "Informational",
    "Representation": "Informational",
    "Language": "Informational",
    "Pattern": "Informational",
    "Signal": "Informational",
    "Signature": "Informational",
    # Ontological
    "System": "Ontological",
    "Environment": "Ontological",
    "Observer": "Ontological",
    "State": "Ontological",
    "Gradient": "Ontological",
    "Self-Organization": "Ontological",
    "Imbrication": "Ontological",
    "Component": "Ontological",
    "Space": "Ontological",
    "Cluster": "Ontological",
    # Teleonomic
    "Tropism": "Teleonomic",
    "Alignment": "Teleonomic",
    "Identity": "Teleonomic",
    "ValueSpace": "Teleonomic",
    # Relational
    "Agent": "Relational",
    "Role": "Relational",
    "Mediator": "Relational",
    "Link": "Relational",
    "Relation": "Relational",
    "Channel": "Relational",
    "Hub": "Relational",
    # Composite / Special (handled separately, but listed for completeness)
    "FeedbackLoop": "Composite",
    "Feedback Loop": "Composite",       # label variant with space
    "Cascade": "Composite",
    "LALI": "Composite",
    "LocalActivationLateralInhibition": "Composite",
    "ButterflyEffect": "Composite",
    "Butterfly Effect": "Composite",    # label variant with space
    "Processor": "Composite",
    # Hybrid / Complex
    "Domain": "Complex",
    "KnowledgeField": "Complex",
    "Amplification": "Complex",
    "Attenuation": "Complex",
    "Composition": "Complex",
    "Decomposition": "Complex",
    "Fusion": "Complex",
    "Fission": "Complex",
    "Encoding": "Complex",
    "Decoding": "Complex",
    "Positive": "Complex",
    "Negative": "Complex",
    "Resource": "Complex",
}

# Composite metaconcepts and their required component labels
_COMPOSITE_COMPONENTS: Dict[str, List[str]] = {
    "FeedbackLoop": ["Process", "Alignment", "Homeostasis"],
    "Cascade": ["Process", "Step", "Trajectory"],
    "LALI": ["Amplification", "Regulation"],
    "ButterflyEffect": ["Amplification", "Trajectory"],
    "Processor": ["Transformation", "Representation"],
}

# Human-readable description of each composite
_COMPOSITE_DESC: Dict[str, str] = {
    "FeedbackLoop":    "Closed-loop regulation: Process + Alignment + Homeostasis → A ⊗ S ⊗ F ⊗ I ⊗ D",
    "Cascade":         "Staged sequential flow: Process + Step + Trajectory → S ⊗ I ⊗ D ⊗ F",
    "LALI":            "Local Activation / Lateral Inhibition: Amplification + Regulation → self-organizing patterns",
    "ButterflyEffect": "Deterministic chaos: Amplification + Trajectory[chaotic] → sensitive dependence",
    "Processor":       "Transformation unit: Transformation + Representation → multi-domain processing",
}

# ASFID dimension full names (for display)
_DIM_NAMES: Dict[str, str] = {
    "A": "Attractor",
    "S": "Structure",
    "F": "Flow",
    "I": "Information",
    "D": "Dynamics",
}


# ==============================================================================
# DATA CLASSES
# ==============================================================================

@dataclass
class DimensionProfile:
    """Score-weighted ASFID dimension fingerprint of the analysed system."""
    weights: Dict[str, float]   # {A: 0.42, S: 0.31, F: 0.18, I: 0.05, D: 0.04}
    dominant: List[str]         # dims above 0.15 weight threshold, sorted desc
    suggested_formula: str      # e.g. "A ⊗ S ⊗ F"


@dataclass
class FamilyGroup:
    """A cluster of metaconcept candidates sharing the same semantic family."""
    category: str
    labels: List[str]           # metaconcept labels in this family
    avg_score: float            # mean cosine similarity of members


@dataclass
class CompositeHint:
    """Indication that a composite metaconcept may apply."""
    composite: str              # e.g. "FeedbackLoop"
    description: str
    components_found: List[str]
    components_missing: List[str]
    completeness: float         # fraction of required components present [0, 1]


@dataclass
class ReasoningResult:
    """Full output of MetaconceptReasoner.reason()."""
    query: str
    dimension_profile: DimensionProfile
    family_groups: List[FamilyGroup]           # non-empty families, sorted by avg_score desc
    composite_hints: List[CompositeHint]       # ordered by completeness desc
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ==============================================================================
# REASONER
# ==============================================================================

class MetaconceptReasoner:
    """
    Derives systemic insight from a MetaconceptClassifier result.

    Three reasoning stages run in sequence (no external I/O required):

      1. ASFID Profile     — parse tensor formulas to compute a score-weighted
                             dimension fingerprint and suggest a formula.
      2. Family Grouping   — group candidates into M2 semantic families.
      3. Composite Inference — flag known composite metaconcepts whose components
                             all (or partially) appear in the candidates.

    Example:
        >>> clf = MetaconceptClassifier()
        >>> clf_result = clf.classify("A thermostat maintains temperature ...")
        >>> rsn = MetaconceptReasoner()
        >>> report = rsn.reason(clf_result)
        >>> rsn.display(report)
    """

    def __init__(
        self,
        dim_threshold: float = 0.10,
        composite_min_completeness: float = 0.50,
    ):
        """
        Args:
            dim_threshold: Minimum normalised weight for a dimension to be
                           counted as dominant in the ASFID profile.
            composite_min_completeness: Minimum fraction of components found
                           for a composite hint to be included in the result.
        """
        self.dim_threshold = dim_threshold
        self.composite_min_completeness = composite_min_completeness

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def reason(self, classification_result) -> ReasoningResult:
        """
        Run all three reasoning stages on a ClassificationResult.

        Args:
            classification_result: Output of MetaconceptClassifier.classify().

        Returns:
            ReasoningResult with dimension profile, family groups, and
            composite hints.
        """
        candidates = classification_result.metaconcept_candidates

        return ReasoningResult(
            query=classification_result.query,
            dimension_profile=self._build_dimension_profile(candidates),
            family_groups=self._build_family_groups(candidates),
            composite_hints=self._detect_composites(candidates),
        )

    # ------------------------------------------------------------------
    # Stage 1 — ASFID Profile
    # ------------------------------------------------------------------

    def _build_dimension_profile(self, candidates) -> DimensionProfile:
        """
        Parse tensor formulas from candidates and build a score-weighted
        ASFID dimension fingerprint.

        Each candidate contributes its cosine-similarity score to the weight
        of every ASFID dimension found in its tensor formula.  Weights are
        then L1-normalised so they sum to 1.
        """
        accumulated: Dict[str, float] = {d: 0.0 for d in _ASFID_DIMS}

        for cand in candidates:
            formula = cand.tensor_formula or ""
            dims = _extract_dims(formula)
            if not dims:
                continue
            # Distribute the candidate score equally among its dimensions
            per_dim = cand.score / len(dims)
            for d in dims:
                accumulated[d] += per_dim

        total = sum(accumulated.values())
        if total == 0.0:
            weights = {d: 0.0 for d in _ASFID_DIMS}
            dominant: List[str] = []
            suggested = "?"
        else:
            weights = {d: round(v / total, 4) for d, v in accumulated.items()}
            dominant = sorted(
                [d for d, w in weights.items() if w >= self.dim_threshold],
                key=lambda d: weights[d],
                reverse=True,
            )
            suggested = " ⊗ ".join(dominant) if dominant else "?"

        return DimensionProfile(
            weights=weights,
            dominant=dominant,
            suggested_formula=suggested,
        )

    # ------------------------------------------------------------------
    # Stage 2 — Family Grouping
    # ------------------------------------------------------------------

    def _build_family_groups(self, candidates) -> List[FamilyGroup]:
        """
        Group candidates by their M2 semantic family and compute the mean
        cosine-similarity score for each group.
        """
        groups: Dict[str, List] = {}

        for cand in candidates:
            family = _resolve_family(cand.label)
            groups.setdefault(family, []).append(cand)

        result: List[FamilyGroup] = []
        for category, members in groups.items():
            avg = sum(m.score for m in members) / len(members)
            result.append(FamilyGroup(
                category=category,
                labels=[m.label for m in members],
                avg_score=round(avg, 4),
            ))

        result.sort(key=lambda g: g.avg_score, reverse=True)
        return result

    # ------------------------------------------------------------------
    # Stage 3 — Composite Inference
    # ------------------------------------------------------------------

    def _detect_composites(self, candidates) -> List[CompositeHint]:
        """
        Check whether the component metaconcepts of known composite
        metaconcepts appear among the candidates.

        Two detection paths:
        - Direct: the composite label itself appears among candidates
          (e.g. "Feedback Loop" is directly returned by the classifier).
        - Component-based: the required sub-components are all (or mostly)
          present (e.g. Process + Alignment + Homeostasis → FeedbackLoop).
        """
        candidate_labels = {_normalise_label(c.label) for c in candidates}

        # Normalised aliases: "feedback loop" -> "FeedbackLoop", etc.
        _composite_aliases = {
            _normalise_label(k): k
            for k in list(_COMPOSITE_COMPONENTS.keys()) + [
                "feedback loop", "butterfly effect",
                "local activation lateral inhibition",
            ]
        }
        # Map alias → canonical composite name
        _alias_to_canonical = {
            "feedback loop": "FeedbackLoop",
            "butterfly effect": "ButterflyEffect",
            "local activation lateral inhibition": "LALI",
            "lali": "LALI",
            "cascade": "Cascade",
            "processor": "Processor",
            "feedbackloop": "FeedbackLoop",
            "butterflyeffect": "ButterflyEffect",
        }

        hints_by_composite: Dict[str, CompositeHint] = {}

        # ── Direct detection ──────────────────────────────────────────
        for norm_label in candidate_labels:
            canonical = _alias_to_canonical.get(norm_label)
            if canonical and canonical in _COMPOSITE_COMPONENTS:
                if canonical not in hints_by_composite:
                    hints_by_composite[canonical] = CompositeHint(
                        composite=canonical,
                        description=_COMPOSITE_DESC.get(canonical, ""),
                        components_found=["(direct match)"],
                        components_missing=[],
                        completeness=1.0,
                    )

        # ── Component-based detection ─────────────────────────────────
        for composite, components in _COMPOSITE_COMPONENTS.items():
            if composite in hints_by_composite:
                continue  # already found by direct match
            found = [c for c in components if _normalise_label(c) in candidate_labels]
            missing = [c for c in components if _normalise_label(c) not in candidate_labels]
            completeness = len(found) / len(components)
            if completeness >= self.composite_min_completeness:
                hints_by_composite[composite] = CompositeHint(
                    composite=composite,
                    description=_COMPOSITE_DESC.get(composite, ""),
                    components_found=found,
                    components_missing=missing,
                    completeness=round(completeness, 4),
                )

        hints = list(hints_by_composite.values())
        hints.sort(key=lambda h: h.completeness, reverse=True)
        return hints

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    def display(self, report: ReasoningResult, verbose: bool = False):
        """Pretty-print a ReasoningResult to stdout."""
        print("\n" + "=" * 70)
        print("  TSCG Metaconcept Reasoner")
        print("=" * 70)
        print(f"Input : {report.query[:120]}")
        print(f"Time  : {report.timestamp}")

        # ── ASFID Profile ──────────────────────────────────────────────
        prof = report.dimension_profile
        print(f"\n{'─' * 70}")
        print("  ASFID Dimension Profile")
        print(f"{'─' * 70}")
        if not prof.dominant:
            print("  No dominant dimensions detected (no formulas available).")
        else:
            for dim in ["A", "S", "F", "I", "D"]:
                w = prof.weights.get(dim, 0.0)
                bar = _score_bar(w, width=16)
                mark = " ◀" if dim in prof.dominant else ""
                print(f"  {dim} ({_DIM_NAMES[dim]:<13}) {bar} {w:.3f}{mark}")
            print(f"\n  Suggested formula : {prof.suggested_formula}")

        # ── Family Groups ──────────────────────────────────────────────
        print(f"\n{'─' * 70}")
        print(f"  Semantic Family Groups  ({len(report.family_groups)})")
        print(f"{'─' * 70}")
        for grp in report.family_groups:
            labels_str = ", ".join(grp.labels)
            bar = _score_bar(grp.avg_score, width=10)
            print(f"\n  {grp.category:<14} {bar} {grp.avg_score:.3f}")
            print(f"               → {labels_str}")

        # ── Composite Hints ────────────────────────────────────────────
        if report.composite_hints:
            print(f"\n{'─' * 70}")
            print(f"  Composite Metaconcept Hints  ({len(report.composite_hints)})")
            print(f"{'─' * 70}")
            for hint in report.composite_hints:
                bar = _score_bar(hint.completeness, width=10)
                print(f"\n  {hint.composite}")
                print(f"    Completeness : {bar} {hint.completeness:.0%}")
                print(f"    Found        : {', '.join(hint.components_found) or '—'}")
                if hint.components_missing:
                    print(f"    Missing      : {', '.join(hint.components_missing)}")
                if verbose:
                    print(f"    Description  : {hint.description}")
        else:
            print(f"\n{'─' * 70}")
            print("  Composite Hints  — none detected above threshold.")

        print(f"\n{'=' * 70}\n")

    def to_dict(self, report: ReasoningResult) -> dict:
        """Serialize a ReasoningResult to a JSON-serialisable dict."""
        return {
            "query": report.query,
            "timestamp": report.timestamp,
            "dimension_profile": {
                "weights": report.dimension_profile.weights,
                "dominant": report.dimension_profile.dominant,
                "suggested_formula": report.dimension_profile.suggested_formula,
            },
            "family_groups": [
                {
                    "category": g.category,
                    "labels": g.labels,
                    "avg_score": g.avg_score,
                }
                for g in report.family_groups
            ],
            "composite_hints": [
                {
                    "composite": h.composite,
                    "description": h.description,
                    "components_found": h.components_found,
                    "components_missing": h.components_missing,
                    "completeness": h.completeness,
                }
                for h in report.composite_hints
            ],
        }


# ==============================================================================
# UTILITIES
# ==============================================================================

# Regex to capture single uppercase dimension letters (A, S, F, I, D)
# anchored by non-alpha characters so "DA" doesn't match "D" twice.
_DIM_RE = re.compile(r"(?<![A-Z])([ASFID])(?![A-Z])")

# Also match dimension letters that appear adjacent to operators or brackets
_DIM_TOKEN_RE = re.compile(r"\b([ASFID])\b")


def _extract_dims(formula: str) -> List[str]:
    """
    Extract ASFID dimension letters from a tensor formula string.

    Handles standard tensor notation (A ⊗ S ⊗ F), arrow chains (S → I → A),
    differential forms (∂D/∂F), integral forms (∫(D−F)dτ), parametric
    forms ((-1)^p (I ⊗ D)), and any other Unicode notation.

    A dimension letter is counted when it is not immediately adjacent to
    another uppercase ASCII letter (to avoid false matches in identifiers).

    Returns a deduplicated list of ASFID dimension characters, in order of
    first appearance.
    """
    if not formula:
        return []
    dims: List[str] = []
    seen: set = set()
    # Match any ASFID letter not flanked by another uppercase ASCII letter.
    # Works regardless of surrounding Unicode operators (⊗ ∂ ∫ − → …).
    for m in re.finditer(r"(?<![A-Z])([ASFID])(?![A-Z])", formula):
        d = m.group(1)
        if d not in seen:
            dims.append(d)
            seen.add(d)
    return dims


def _resolve_family(label: str) -> str:
    """
    Return the semantic family for a metaconcept label.
    Falls back to 'Unknown' for labels not in the knowledge base.
    """
    # Direct lookup
    if label in _LABEL_TO_FAMILY:
        return _LABEL_TO_FAMILY[label]
    # Case-insensitive fallback
    lower = label.lower()
    for key, family in _LABEL_TO_FAMILY.items():
        if key.lower() == lower:
            return family
    return "Unknown"


def _normalise_label(label: str) -> str:
    """Lower-case and strip a label for comparison."""
    return label.strip().lower()


def _score_bar(score: float, width: int = 12) -> str:
    """ASCII progress bar for a [0, 1] value."""
    filled = round(max(0.0, min(1.0, score)) * width)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TSCG Metaconcept Reasoner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python reasoner.py "A thermostat maintains temperature via negative feedback"
  python reasoner.py "The immune system neutralises pathogens" --top-k 8
  python reasoner.py "VSM recursively embeds viable systems" --verbose
  python reasoner.py "..." --json
        """,
    )
    parser.add_argument("description", help="Natural language system description")
    parser.add_argument(
        "--db",
        default=None,
        help="ChromaDB path for the upstream classifier (default: auto-detect)",
    )
    parser.add_argument(
        "--top-k", type=int, default=7,
        help="Number of metaconcept candidates passed to the classifier (default: 7)",
    )
    parser.add_argument(
        "--min-score", type=float, default=0.30,
        help="Minimum cosine similarity for classifier candidates (default: 0.30)",
    )
    parser.add_argument(
        "--composite-threshold", type=float, default=0.50,
        help="Minimum component completeness to report a composite hint (default: 0.50)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Show composite descriptions and additional detail",
    )
    parser.add_argument(
        "--json", dest="as_json", action="store_true",
        help="Output both classification and reasoning as JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    # Import here so the module can be imported without chromadb being present
    try:
        from tscg.engine.classifier import MetaconceptClassifier
    except ImportError:
        # Fallback: try relative path when run as script from the engine dir
        import importlib.util, pathlib
        spec = importlib.util.spec_from_file_location(
            "metaconcept_classifier",
            pathlib.Path(__file__).parent.parent / "classifier" / "metaconcept_classifier.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        MetaconceptClassifier = mod.MetaconceptClassifier

    clf_kwargs = {"top_k_metaconcepts": args.top_k, "min_score": args.min_score}
    if args.db:
        clf_kwargs["db_path"] = args.db

    clf = MetaconceptClassifier(**clf_kwargs)
    clf_result = clf.classify(args.description)

    rsn = MetaconceptReasoner(composite_min_completeness=args.composite_threshold)
    report = rsn.reason(clf_result)

    if args.as_json:
        output = {
            "classification": clf.to_dict(clf_result),
            "reasoning": rsn.to_dict(report),
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        clf.display(clf_result)
        rsn.display(report, verbose=args.verbose)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
