#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_corpus.py - TSCG Poclet Corpus Analyser

Scans all M0 poclet JSON-LD files in the repository and produces:
  1. Typical poclet profile (ASFID/REVOI scores, epistemic gap δ)
  2. GenericConcept frequency ranking (which M2 concepts are most mobilised)
  3. Domain coverage map + gap analysis (under-represented domains)
  4. Per-poclet detail table
  5. Optional JSON export (--json)

Handles all score field naming variants found across the corpus:
  m0:asfidScores / m0:territorySpace.asfidState / m0:asfidProfile /
  m0:asfidMean / tscg:asfidScore  →  normalised to A,S,F,I,D means
  m0:revoiScores / m0:mapSpace.reviState              →  R,E,V,O,I means
  m0:epistemicGap (float or {delta: …})               →  δ float
  m0:validatesMetaconcepts / m0:primaryGenericConcepts /
  m0:instantiatesM2 / m0:mobilisedGenericConcepts / …  →  concept set

Usage:
  python rebuild_corpus.py                   # scan repo relative to script
  python rebuild_corpus.py --repo /path/to/tscg
  python rebuild_corpus.py --json report.json
  python rebuild_corpus.py --verbose

Author: Echopraxium with the collaboration of Claude AI
"""

import os
import sys
import json
import re
import argparse
import datetime
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Repo root: script lives at src/tscg/rag/rebuild_corpus.py
_SCRIPT_DIR  = Path(__file__).resolve().parent
_REPO_ROOT   = _SCRIPT_DIR.parent.parent.parent.parent
DEFAULT_REPO = str(_REPO_ROOT)

# Known domains → broader category  (for gap analysis)
DOMAIN_TAXONOMY = {
    # Biology & Life Sciences
    "biology": "Life Sciences",
    "ecology": "Life Sciences",
    "endocrinology": "Life Sciences",
    "developmental biology": "Life Sciences",
    "renal physiology": "Life Sciences",
    "cardiovascular": "Life Sciences",
    "immunology": "Life Sciences",
    "neuroscience": "Life Sciences",
    "cell biology": "Life Sciences",
    # Physics & Engineering
    "electronics": "Physics & Engineering",
    "semiconductor physics": "Physics & Engineering",
    "signal processing": "Physics & Engineering",
    "thermodynamics": "Physics & Engineering",
    "mechanics": "Physics & Engineering",
    "nuclear engineering": "Physics & Engineering",
    "optics": "Physics & Engineering",
    # Mathematics & Formal Sciences
    "mathematics": "Mathematics & Formal Sciences",
    "logic": "Mathematics & Formal Sciences",
    "information theory": "Mathematics & Formal Sciences",
    # Humanities & Culture
    "mythology": "Humanities & Culture",
    "comparative religion": "Humanities & Culture",
    "cosmology": "Humanities & Culture",
    "linguistics": "Humanities & Culture",
    "philosophy": "Humanities & Culture",
    # Social Sciences & Economics
    "economics": "Social Sciences & Economics",
    "finance": "Social Sciences & Economics",
    "sociology": "Social Sciences & Economics",
    "political science": "Social Sciences & Economics",
    # Education & Cognitive Sciences
    "education": "Education & Cognitive Sciences",
    "cognitive science": "Education & Cognitive Sciences",
    "psychology": "Education & Cognitive Sciences",
    # Design & Creative Arts
    "game design": "Design & Creative Arts",
    "photography": "Design & Creative Arts",
    "music": "Design & Creative Arts",
    "architecture": "Design & Creative Arts",
    # Chemistry
    "chemistry": "Chemistry",
    "biochemistry": "Chemistry",
}

DESIRED_DOMAINS = [
    "Life Sciences", "Physics & Engineering", "Chemistry",
    "Mathematics & Formal Sciences", "Humanities & Culture",
    "Social Sciences & Economics", "Education & Cognitive Sciences",
    "Design & Creative Arts",
]

# ==============================================================================
# ARGUMENT PARSING
# ==============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="TSCG Poclet Corpus Analyser — profile, coverage, concept frequencies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python rebuild_corpus.py
  python rebuild_corpus.py --repo /path/to/tscg
  python rebuild_corpus.py --json corpus_report.json
  python rebuild_corpus.py --verbose
        """
    )
    parser.add_argument("--repo",    default=DEFAULT_REPO,
                        help=f"Repository root (default: {DEFAULT_REPO})")
    parser.add_argument("--json",    metavar="PATH",
                        help="Export full report as JSON to this path")
    parser.add_argument("--top",     type=int, default=15,
                        help="Number of top GenericConcepts to display (default: 15)")
    parser.add_argument("--verbose", action="store_true",
                        help="Show per-file parsing details")
    return parser.parse_args()

# ==============================================================================
# JSON-LD POCLET PARSER
# ==============================================================================

def _strip_prefix(value: str) -> str:
    """Remove 'm2:', 'm0:', 'tscg:' etc. prefixes, keep the local name."""
    if isinstance(value, str):
        return value.split(":")[-1].split("#")[-1].strip()
    return str(value)


def _extract_concept_ref(item) -> Optional[str]:
    """
    Normalise a concept reference to its local name.
    Handles:  "m2:Cascade"  |  {"@id": "m2:Cascade"}  |  {"@id": "m2:Cascade", "role": "…"}
    """
    if isinstance(item, str):
        name = _strip_prefix(item)
        # Strip trailing parenthetical annotations like "(ternary 5D)"
        name = re.sub(r'\s*\(.*\)$', '', name).strip()
        return name if name else None
    if isinstance(item, dict):
        ref = item.get("@id") or item.get("id", "")
        name = _strip_prefix(ref)
        name = re.sub(r'\s*\(.*\)$', '', name).strip()
        return name if name else None
    return None


def _extract_concepts_from_entry(entry: dict) -> List[str]:
    """
    Collect all M2 GenericConcept references from a single @graph entry.
    Handles all field name variants found in the corpus.
    """
    CONCEPT_FIELDS = [
        "m0:validatesMetaconcepts", "m0:primaryMetaconcept",
        "m0:primaryGenericConcepts", "m0:secondaryGenericConcepts",
        "m0:mobilisedGenericConcepts", "m0:mobilizedGenericConcepts",
        "m0:instantiatesM2", "m0:metaconceptsMobilized",
        "tscg:mobilizesMetaconcept", "m0:instantiatesMetaconcept",
        "m0:m2_metaconcepts", "m0:metaconcept",
        "m2:metaconceptUsage",
    ]
    concepts = []
    for field in CONCEPT_FIELDS:
        val = entry.get(field)
        if val is None:
            continue
        if isinstance(val, (str, dict)):
            val = [val]
        if isinstance(val, list):
            for item in val:
                name = _extract_concept_ref(item)
                if name and name.lower() not in ("none", ""):
                    concepts.append(name)
    # Also scrape nested objects for mobilisedGenericConcepts lists
    for key, val in entry.items():
        if isinstance(val, dict):
            nested = val.get("m0:mobilisedGenericConcepts") or val.get("m0:mobilizedGenericConcepts")
            if nested:
                if isinstance(nested, str):
                    nested = [nested]
                for item in nested:
                    name = _extract_concept_ref(item)
                    if name:
                        concepts.append(name)
    return concepts


def _extract_asfid(entry: dict) -> Optional[Dict[str, float]]:
    """
    Extract ASFID scores {A, S, F, I, D, mean} from all known field variants.
    Returns None if no scores found.
    """
    DIM_MAP = {
        "a": "A", "attractor": "A",
        "s": "S", "structure": "S",
        "f": "F", "flow": "F",
        "i": "I", "information": "I",
        "d": "D", "dynamics": "D",
    }

    def _parse_score_dict(raw: dict) -> Optional[Dict[str, float]]:
        scores = {}
        for k, v in raw.items():
            mapped = DIM_MAP.get(k.lower())
            if mapped and isinstance(v, (int, float)):
                scores[mapped] = float(v)
        if len(scores) == 5:
            scores["mean"] = round(sum(scores[d] for d in "ASFID") / 5, 4)
            return scores
        mean = raw.get("mean") or raw.get("score")
        if mean and isinstance(mean, (int, float)):
            return {"mean": float(mean)}
        return None

    # Variant 1: m0:asfidScores
    raw = entry.get("m0:asfidScores")
    if isinstance(raw, dict):
        result = _parse_score_dict(raw)
        if result:
            return result

    # Variant 2: m0:territorySpace → m0:asfidState
    ts = entry.get("m0:territorySpace")
    if isinstance(ts, dict):
        state = ts.get("m0:asfidState")
        if isinstance(state, dict):
            result = _parse_score_dict(state)
            if result:
                return result

    # Variant 3: m0:asfidProfile  (long-form key names: attractor, structure, …)
    raw = entry.get("m0:asfidProfile")
    if isinstance(raw, dict):
        result = _parse_score_dict(raw)
        if result:
            return result

    # Variant 4: m0:asfidMean  (only mean available)
    mean_val = entry.get("m0:asfidMean") or entry.get("tscg:asfidScore")
    if isinstance(mean_val, (int, float)):
        return {"mean": float(mean_val)}

    return None


def _extract_revoi(entry: dict) -> Optional[Dict[str, float]]:
    """
    Extract REVOI scores {R, E, V, O, I, mean} from all known field variants.
    """
    DIM_MAP = {
        "r": "R", "representability": "R", "representable": "R",
        "e": "E", "evolvability": "E",    "evolvable": "E",
        "v": "V", "verifiability": "V",   "verifiable": "V",
        "o": "O", "observability": "O",   "observable": "O",
        "i": "I", "interoperability": "I","interoperable": "I",
    }

    def _parse_score_dict(raw: dict) -> Optional[Dict[str, float]]:
        scores = {}
        for k, v in raw.items():
            mapped = DIM_MAP.get(k.lower())
            if mapped and isinstance(v, (int, float)):
                scores[mapped] = float(v)
        if len(scores) == 5:
            scores["mean"] = round(sum(scores[d] for d in "REVOI") / 5, 4)
            return scores
        mean = raw.get("mean") or raw.get("score")
        if mean and isinstance(mean, (int, float)):
            return {"mean": float(mean)}
        return None

    # Variant 1: m0:revoiScores
    raw = entry.get("m0:revoiScores")
    if isinstance(raw, dict):
        result = _parse_score_dict(raw)
        if result:
            return result

    # Variant 2: m0:mapSpace → m0:reviState
    ms = entry.get("m0:mapSpace")
    if isinstance(ms, dict):
        state = ms.get("m0:reviState")
        if isinstance(state, dict):
            result = _parse_score_dict(state)
            if result:
                return result

    return None


def _extract_epistemic_gap(entry: dict) -> Optional[float]:
    """Extract δ (epistemic gap) as a float from all known variants."""
    for field in ("m0:epistemicGap", "tscg:epistemicGap"):
        val = entry.get(field)
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, dict):
            delta = val.get("delta") or val.get("value")
            if isinstance(delta, (int, float)):
                return float(delta)
    return None


def _extract_domain(entry: dict) -> Optional[str]:
    """Extract the primary domain string."""
    for field in ("m0:domain", "tscg:domain"):
        val = entry.get(field)
        if isinstance(val, str) and val:
            return val.strip()
    # Nested in pocletMetadata
    meta = entry.get("m0:pocletMetadata")
    if isinstance(meta, dict):
        val = meta.get("domain")
        if isinstance(val, str):
            return val.strip()
    return None


def _extract_label(entry: dict) -> str:
    lbl = entry.get("rdfs:label", "")
    if isinstance(lbl, dict):
        lbl = lbl.get("@value", "")
    return str(lbl).strip()


def _is_main_entry(entry: dict) -> bool:
    """
    Heuristic: the main poclet entry is typically the first NamedIndividual
    with an @id containing 'm0:' and carrying domain / score fields.
    """
    entry_id = entry.get("@id", "")
    types = entry.get("@type", [])
    if isinstance(types, str):
        types = [types]

    # Ontology header entries
    if "owl:Ontology" in types:
        return True

    # NamedIndividual at poclet level
    has_m0_id = "m0:" in str(entry_id) and "/" not in str(entry_id).replace("m0:", "")
    if "owl:NamedIndividual" in types and has_m0_id:
        return True

    # Any entry with score or domain fields
    score_keys = {"m0:asfidScores", "m0:revoiScores", "m0:asfidMean",
                  "m0:territorySpace", "m0:mapSpace", "m0:asfidProfile"}
    if score_keys & set(entry.keys()):
        return True

    return False


# ==============================================================================
# POCLET DATA CLASS
# ==============================================================================

class PocletProfile:
    def __init__(self, path: str):
        self.path     = path
        self.name     = Path(path).stem          # e.g. M0_RAAS
        self.label    = ""
        self.domain   = "Unknown"
        self.asfid    : Optional[Dict[str, float]] = None
        self.revoi    : Optional[Dict[str, float]] = None
        self.delta    : Optional[float] = None
        self.concepts : List[str] = []           # all M2 GenericConcept names
        self.parse_errors : List[str] = []

    @property
    def asfid_mean(self) -> Optional[float]:
        return self.asfid.get("mean") if self.asfid else None

    @property
    def revoi_mean(self) -> Optional[float]:
        return self.revoi.get("mean") if self.revoi else None


# ==============================================================================
# CORPUS SCANNER
# ==============================================================================

def scan_corpus(repo_path: str, verbose: bool = False) -> List[PocletProfile]:
    """
    Walk the repository and parse all M0_*.jsonld poclet files.
    Returns a list of PocletProfile objects.
    """
    repo  = Path(repo_path)
    poclets: List[PocletProfile] = []

    # Collect files — exclude archived / sparql / docs directories
    SKIP_DIRS = {"_archives", "_archive", "sparql", "docs", "node_modules",
                 ".git", "__pycache__", "tools"}

    m0_files = []
    for f in repo.rglob("M0_*.jsonld"):
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        m0_files.append(f)

    m0_files.sort()

    if verbose:
        print(f"  Found {len(m0_files)} M0 poclet files")

    for fpath in m0_files:
        profile = PocletProfile(str(fpath))

        try:
            data = json.loads(fpath.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError as e:
            profile.parse_errors.append(f"JSON parse error: {e}")
            poclets.append(profile)
            continue

        graph = data.get("@graph", [])
        if not isinstance(graph, list):
            graph = []

        all_concepts: List[str] = []

        for entry in graph:
            if not isinstance(entry, dict):
                continue

            # Concepts from ALL entries (sub-entries also mobilise M2 concepts)
            all_concepts.extend(_extract_concepts_from_entry(entry))

            # Scores and domain — only from the main entry
            if _is_main_entry(entry):
                if not profile.label:
                    profile.label = _extract_label(entry)
                if profile.domain == "Unknown":
                    d = _extract_domain(entry)
                    if d:
                        profile.domain = d
                if profile.asfid is None:
                    profile.asfid = _extract_asfid(entry)
                if profile.revoi is None:
                    profile.revoi = _extract_revoi(entry)
                if profile.delta is None:
                    profile.delta = _extract_epistemic_gap(entry)

        # Deduplicate concepts (preserve frequency across the whole poclet)
        profile.concepts = all_concepts

        if verbose:
            print(f"  {profile.name}: domain={profile.domain}, "
                  f"asfid={profile.asfid_mean}, revoi={profile.revoi_mean}, "
                  f"δ={profile.delta}, concepts={len(set(all_concepts))}")

        poclets.append(profile)

    return poclets


# ==============================================================================
# ANALYSIS
# ==============================================================================

def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return round(sum(values) / len(values), 4)


def _classify_domain(raw_domain: str) -> str:
    """Map a raw domain string to a broad DOMAIN_TAXONOMY category."""
    d = raw_domain.lower()
    for keyword, category in DOMAIN_TAXONOMY.items():
        if keyword in d:
            return category
    return "Other"


def analyse_corpus(poclets: List[PocletProfile], top_n: int = 15) -> Dict:
    """
    Compute corpus-level statistics from a list of PocletProfile objects.
    """
    n = len(poclets)

    # ── ASFID distribution ────────────────────────────────────────────────────
    dims_asfid = defaultdict(list)
    for p in poclets:
        if p.asfid:
            for dim in "ASFID":
                val = p.asfid.get(dim)
                if val is not None:
                    dims_asfid[dim].append(val)

    asfid_profile = {
        dim: {"mean": mean(dims_asfid[dim]),
              "min":  min(dims_asfid[dim], default=None),
              "max":  max(dims_asfid[dim], default=None),
              "n":    len(dims_asfid[dim])}
        for dim in "ASFID"
    }
    asfid_means = [p.asfid_mean for p in poclets if p.asfid_mean is not None]

    # ── REVOI distribution ────────────────────────────────────────────────────
    dims_revoi = defaultdict(list)
    for p in poclets:
        if p.revoi:
            for dim in "REVOI":
                val = p.revoi.get(dim)
                if val is not None:
                    dims_revoi[dim].append(val)

    revoi_profile = {
        dim: {"mean": mean(dims_revoi[dim]),
              "min":  min(dims_revoi[dim], default=None),
              "max":  max(dims_revoi[dim], default=None),
              "n":    len(dims_revoi[dim])}
        for dim in "REVOI"
    }
    revoi_means = [p.revoi_mean for p in poclets if p.revoi_mean is not None]

    # ── Epistemic gap ─────────────────────────────────────────────────────────
    deltas = [p.delta for p in poclets if p.delta is not None]

    # ── GenericConcept frequencies ────────────────────────────────────────────
    concept_counter: Counter = Counter()
    for p in poclets:
        # Count distinct concept mentions per poclet (avoid double-counting
        # when the same entry is referenced many times in one poclet)
        for concept in set(p.concepts):
            concept_counter[concept] += 1

    top_concepts = concept_counter.most_common(top_n)

    # ── Domain coverage ───────────────────────────────────────────────────────
    domain_counter: Counter = Counter()
    category_map: Dict[str, List[str]] = defaultdict(list)

    for p in poclets:
        category = _classify_domain(p.domain)
        domain_counter[category] += 1
        if p.domain not in category_map[category]:
            category_map[category].append(p.domain)

    covered    = {cat for cat in domain_counter if domain_counter[cat] > 0}
    gaps       = [cat for cat in DESIRED_DOMAINS if cat not in covered]

    return {
        "generated_at":    datetime.datetime.now().isoformat(),
        "poclet_count":    n,
        "asfid_profile":   asfid_profile,
        "asfid_mean_dist": {
            "mean": mean(asfid_means),
            "min":  min(asfid_means, default=None),
            "max":  max(asfid_means, default=None),
            "n":    len(asfid_means),
        },
        "revoi_profile":   revoi_profile,
        "revoi_mean_dist": {
            "mean": mean(revoi_means),
            "min":  min(revoi_means, default=None),
            "max":  max(revoi_means, default=None),
            "n":    len(revoi_means),
        },
        "epistemic_gap": {
            "mean":   mean(deltas),
            "min":    min(deltas, default=None),
            "max":    max(deltas, default=None),
            "n":      len(deltas),
            "values": {p.name: p.delta for p in poclets if p.delta is not None},
        },
        "top_concepts":    top_concepts,
        "all_concepts":    dict(concept_counter.most_common()),
        "domain_coverage": {
            "by_category":       dict(domain_counter),
            "by_category_detail": {k: v for k, v in category_map.items()},
            "covered_categories": sorted(covered),
            "gap_categories":    gaps,
        },
        "poclets": [
            {
                "name":       p.name,
                "label":      p.label,
                "domain":     p.domain,
                "asfid_mean": p.asfid_mean,
                "revoi_mean": p.revoi_mean,
                "delta":      p.delta,
                "asfid":      p.asfid,
                "revoi":      p.revoi,
                "top_concepts": list(dict(Counter(p.concepts).most_common(5)).keys()),
                "concept_count": len(set(p.concepts)),
                "parse_errors": p.parse_errors,
            }
            for p in poclets
        ],
    }


# ==============================================================================
# DISPLAY
# ==============================================================================

def _bar(value: Optional[float], width: int = 20) -> str:
    """Render a 0–1 value as a text progress bar."""
    if value is None:
        return "─" * width
    filled = round(value * width)
    return "█" * filled + "░" * (width - filled)


def _fmt(value: Optional[float]) -> str:
    return f"{value:.3f}" if value is not None else "  n/a "


def display_report(report: Dict, top_n: int = 15) -> None:
    n  = report["poclet_count"]
    W  = 72

    print("\n" + "=" * W)
    print("  TSCG POCLET CORPUS — PROFILE REPORT")
    print("=" * W)
    print(f"  Generated : {report['generated_at'][:19]}")
    print(f"  Poclets   : {n}")
    print("=" * W)

    # ── 1. Typical poclet ASFID profile ───────────────────────────────────────
    ap  = report["asfid_profile"]
    adm = report["asfid_mean_dist"]
    print(f"\n{'─'*W}")
    print("  1. TYPICAL ASFID PROFILE  (Eagle Eye — Territory)")
    print(f"{'─'*W}")
    print(f"  {'Dim':<5} {'Mean':>6}  {'Min':>6}  {'Max':>6}  {'n':>3}  Distribution")
    print(f"  {'─'*5} {'─'*6}  {'─'*6}  {'─'*6}  {'─'*3}  {'─'*22}")
    DIM_NAMES = {"A":"Attractor","S":"Structure","F":"Flow","I":"Information","D":"Dynamics"}
    for dim in "ASFID":
        d = ap[dim]
        print(f"  {dim} ({DIM_NAMES[dim][0:1]+')':<4} {_fmt(d['mean'])}  {_fmt(d['min'])}  {_fmt(d['max'])}  {d['n']:>3}  {_bar(d['mean'])}")
    print(f"\n  Overall ASFID mean : {_fmt(adm['mean'])}  {_bar(adm['mean'])}  (n={adm['n']})")

    # ── 2. Typical poclet REVOI profile ───────────────────────────────────────
    rp  = report["revoi_profile"]
    rdm = report["revoi_mean_dist"]
    print(f"\n{'─'*W}")
    print("  2. TYPICAL REVOI PROFILE  (Sphinx Eye — Map)")
    print(f"{'─'*W}")
    print(f"  {'Dim':<5} {'Mean':>6}  {'Min':>6}  {'Max':>6}  {'n':>3}  Distribution")
    print(f"  {'─'*5} {'─'*6}  {'─'*6}  {'─'*6}  {'─'*3}  {'─'*22}")
    REVOI_NAMES = {"R":"Representab.","E":"Evolvability","V":"Verifiability",
                   "O":"Observability","I":"Interoperab."}
    for dim in "REVOI":
        d = rp[dim]
        print(f"  {dim} ({REVOI_NAMES[dim][0:1]+')':<4} {_fmt(d['mean'])}  {_fmt(d['min'])}  {_fmt(d['max'])}  {d['n']:>3}  {_bar(d['mean'])}")
    print(f"\n  Overall REVOI mean : {_fmt(rdm['mean'])}  {_bar(rdm['mean'])}  (n={rdm['n']})")

    # ── 3. Epistemic gap δ ────────────────────────────────────────────────────
    eg = report["epistemic_gap"]
    print(f"\n{'─'*W}")
    print("  3. EPISTEMIC GAP δ  (Map-Territory divergence)")
    print(f"{'─'*W}")
    print(f"  Corpus mean δ : {_fmt(eg['mean'])}  (n={eg['n']})")
    print(f"  Min           : {_fmt(eg['min'])}")
    print(f"  Max           : {_fmt(eg['max'])}")
    print()
    if eg["values"]:
        for pname, delta in sorted(eg["values"].items(), key=lambda x: (x[1] or 99)):
            bar = _bar(delta, 15)
            print(f"    {pname:<35} δ={_fmt(delta)}  {bar}")

    # ── 4. GenericConcept frequencies ─────────────────────────────────────────
    print(f"\n{'─'*W}")
    print(f"  4. TOP {top_n} GENERIC CONCEPTS  (by poclet count)")
    print(f"{'─'*W}")
    print(f"  {'Rank':<5} {'GenericConcept':<28} {'Poclets':>7}  Frequency bar")
    print(f"  {'─'*5} {'─'*28} {'─'*7}  {'─'*22}")
    max_freq = report["top_concepts"][0][1] if report["top_concepts"] else 1
    for rank, (concept, count) in enumerate(report["top_concepts"], 1):
        bar = "█" * round(22 * count / max(max_freq, 1))
        print(f"  {rank:<5} {concept:<28} {count:>7}  {bar}")

    # ── 5. Domain coverage ────────────────────────────────────────────────────
    dc = report["domain_coverage"]
    print(f"\n{'─'*W}")
    print("  5. DOMAIN COVERAGE")
    print(f"{'─'*W}")
    print(f"  {'Category':<32} {'Poclets':>7}")
    print(f"  {'─'*32} {'─'*7}")
    for cat in DESIRED_DOMAINS:
        count = dc["by_category"].get(cat, 0)
        domains = ", ".join(dc["by_category_detail"].get(cat, []))
        flag = "  " if count > 0 else "⚠ "
        print(f"  {flag}{cat:<30} {count:>7}   {domains[:38]}")
    other = dc["by_category"].get("Other", 0)
    if other:
        print(f"    {'Other':<30} {other:>7}")

    if dc["gap_categories"]:
        print(f"\n  ⚠  GAPS — no poclet yet in:")
        for cat in dc["gap_categories"]:
            print(f"       • {cat}")
    else:
        print("\n  ✓  All target domain categories covered")

    # ── 6. Per-poclet summary table ───────────────────────────────────────────
    print(f"\n{'─'*W}")
    print("  6. PER-POCLET SUMMARY")
    print(f"{'─'*W}")
    print(f"  {'Poclet':<32} {'ASFID':>6}  {'REVOI':>6}  {'δ':>6}  Domain")
    print(f"  {'─'*32} {'─'*6}  {'─'*6}  {'─'*6}  {'─'*20}")
    for p in report["poclets"]:
        dom = (p["domain"] or "?")[:22]
        print(f"  {p['name']:<32} {_fmt(p['asfid_mean'])}  {_fmt(p['revoi_mean'])}  "
              f"{_fmt(p['delta'])}  {dom}")

    print(f"\n{'='*W}\n")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    args = parse_arguments()

    print("\n" + "=" * 70)
    print("  TSCG Poclet Corpus Analyser")
    print("=" * 70)
    print(f"  Repository : {args.repo}")
    print("=" * 70)

    # 1. Scan
    print("\n📁 Scanning poclets...")
    poclets = scan_corpus(args.repo, verbose=args.verbose)
    if not poclets:
        print("❌ No M0 poclet files found.")
        return 1
    print(f"✓ Found {len(poclets)} poclets")

    # 2. Analyse
    print("📊 Analysing corpus...")
    report = analyse_corpus(poclets, top_n=args.top)

    # 3. Display
    display_report(report, top_n=args.top)

    # 4. Optional JSON export
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"📄 Report saved → {args.json}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)
