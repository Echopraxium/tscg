"""
poclet_parser.py
================
TSCG Poclet Parser - Generic JSON-LD to Simulation Data
Author: Echopraxium with the collaboration of Claude AI

Reads a TSCG M0 poclet (JSON-LD) and extracts all data needed
to drive a Pygame simulation:
  - Components + thresholds (from constraints)
  - ASFID base scores (territorySpace)
  - REVOI scores (revoi / mapSpace)
  - Synergy principle
  - Epistemic gap (ΔΘ)
  - Metaconcepts mobilized

Usage:
    # Direct path
    from poclet_parser import PocletParser
    p = PocletParser("M0_FireTriangle.jsonld")
    sim_data = p.parse()

    # Auto-discovery from repository root
    from poclet_parser import PocletRepository
    repo = PocletRepository("/path/to/tscg")         # explicit root
    repo = PocletRepository()                         # auto-detect
    sim_data = repo.load("FireTriangle")              # by name (case-insensitive)
    names    = repo.list()                            # all available poclets
"""

import json
import math
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Repository discovery
# ---------------------------------------------------------------------------

# Standard TSCG path for poclets inside the repository
POCLETS_RELATIVE_PATH = Path("system-models") / "poclets"


class PocletRepository:
    """
    Discovers and loads TSCG M0 poclet JSON-LD files from a repository tree.

    Search strategy:
      1. Use the provided root if given.
      2. Otherwise walk upward from this file's directory until a folder
         containing 'system-models/poclets' is found.
      3. Scan recursively under <root>/system-models/poclets for all
         files matching 'M0_*.jsonld'.

    Usage:
        repo = PocletRepository()                   # auto-detect root
        repo = PocletRepository("/path/to/tscg")    # explicit root

        names = repo.list()                         # ['FireTriangle', 'RAAS', ...]
        data  = repo.load("FireTriangle")           # PocletSimData
        path  = repo.find("FireTriangle")           # Path object or None
    """

    def __init__(self, root=None):
        if root is not None:
            self.root = Path(root)
        else:
            self.root = self._auto_detect_root()

        self._poclets_dir = self.root / POCLETS_RELATIVE_PATH if self.root else None
        self._index = {}   # name (lower) -> path

        if self._poclets_dir and self._poclets_dir.exists():
            self._build_index()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def list(self):
        """Return canonical names of all discovered poclets (sorted)."""
        return sorted(self._index.keys())

    def find(self, name):
        """
        Resolve a poclet by name (case-insensitive, partial match allowed).
        Examples: "FireTriangle", "fire_triangle", "fire" all match M0_FireTriangle.jsonld
        """
        key = name.lower().replace(" ", "_").replace("-", "_")
        if key in self._index:
            return self._index[key]
        # Prefix / substring match
        for k, v in self._index.items():
            if key in k or k in key:
                return v
        return None

    def load(self, name):
        """
        Find and parse a poclet by name.
        Raises FileNotFoundError if not found.
        """
        path = self.find(name)
        if path is None:
            available = ", ".join(self.list()) or "(none)"
            raise FileNotFoundError(
                f"Poclet '{name}' not found under '{self._poclets_dir}'.\n"
                f"Available: {available}"
            )
        return PocletParser(path).parse()

    def __repr__(self):
        return (f"<PocletRepository root='{self.root}' "
                f"poclets_found={len(self._index)}>")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _auto_detect_root(self):
        """
        Walk upward from this file's location until we find a directory
        that contains 'system-models/poclets'.
        """
        candidate = Path(__file__).resolve().parent
        for _ in range(10):   # max 10 levels up
            if (candidate / POCLETS_RELATIVE_PATH).exists():
                return candidate
            parent = candidate.parent
            if parent == candidate:
                break
            candidate = parent
        return Path.cwd()     # last resort: current working directory

    def _build_index(self):
        """Recursively index all M0_*.jsonld files under the poclets directory."""
        self._index.clear()
        for path in sorted(self._poclets_dir.rglob("M0_*.jsonld")):
            stem = path.stem          # e.g. "M0_FireTriangle"
            name = stem[3:] if stem.upper().startswith("M0_") else stem
            key  = name.lower()
            if key in self._index:
                # Prefer validated files over _to_be_fixed
                existing = str(self._index[key])
                if "_to_be_fixed" in existing and "_to_be_fixed" not in str(path):
                    self._index[key] = path
            else:
                self._index[key] = path

# ---------------------------------------------------------------------------
# Data classes (plain dicts kept simple for Pygame friendliness)
# ---------------------------------------------------------------------------

class ComponentData:
    def __init__(self, cid, label, role, function, asfid_contribution,
                 threshold=None, threshold_label=None, examples=None):
        self.id               = cid
        self.label            = label
        self.role             = role
        self.function         = function
        self.asfid_contribution = asfid_contribution   # dict {dim: description}
        self.threshold        = threshold              # float or None
        self.threshold_label  = threshold_label        # str description
        self.examples         = examples or []

    def __repr__(self):
        return f"<Component {self.label} threshold={self.threshold}>"


class ASFIDVector:
    """5-dimensional Eagle Eye (Territory) measurement."""
    DIMS = ["A", "S", "F", "I", "D"]

    def __init__(self, A=0.0, S=0.0, F=0.0, I=0.0, D=0.0):
        self.A = A
        self.S = S
        self.F = F
        self.I = I
        self.D = D

    def as_dict(self):
        return {"A": self.A, "S": self.S, "F": self.F, "I": self.I, "D": self.D}

    def norm(self):
        return math.sqrt(self.A**2 + self.S**2 + self.F**2 + self.I**2 + self.D**2)

    def __sub__(self, other):
        return ASFIDVector(
            self.A - other.A, self.S - other.S, self.F - other.F,
            self.I - other.I, self.D - other.D
        )

    def __repr__(self):
        return (f"ASFID(A={self.A:.2f}, S={self.S:.2f}, F={self.F:.2f}, "
                f"I={self.I:.2f}, D={self.D:.2f})")


class REVOIVector:
    """5-dimensional Sphinx Eye (Map) evaluation."""
    DIMS = ["R", "E", "V", "O", "I"]

    def __init__(self, R=0.0, E=0.0, V=0.0, O=0.0, I=0.0):
        self.R = R
        self.E = E
        self.V = V
        self.O = O
        self.I = I

    def mean(self):
        return (self.R + self.E + self.V + self.O + self.I) / 5.0

    def as_dict(self):
        return {"R": self.R, "E": self.E, "V": self.V, "O": self.O, "I": self.I}

    def __repr__(self):
        return (f"REVOI(R={self.R:.2f}, E={self.E:.2f}, V={self.V:.2f}, "
                f"O={self.O:.2f}, I={self.I:.2f})")


class EpistemicGap:
    def __init__(self, norm, delta_vector, interpretation, assessment):
        self.norm          = norm
        self.delta_vector  = delta_vector   # list of floats [A,S,F,I,D]
        self.interpretation = interpretation
        self.assessment    = assessment

    def __repr__(self):
        return f"<EpistemicGap ΔΘ={self.norm:.3f} ({self.interpretation})>"


class PocletSimData:
    """
    All simulation-relevant data extracted from a poclet JSON-LD.
    This is the contract between the parser and the Pygame simulation.
    """
    def __init__(self):
        self.id               = ""
        self.label            = ""
        self.comment          = ""
        self.domain           = ""
        self.poclet_type      = ""
        self.synergy_formula  = ""
        self.synergy_emergent = ""
        self.components       = []        # list of ComponentData
        self.asfid_base       = ASFIDVector()
        self.revoi            = REVOIVector()
        self.epistemic_gap    = None      # EpistemicGap or None
        self.metaconcepts     = []        # list of str (critical names)
        self.metaconcept_count = 0
        self.extinguishment   = []        # list of {target, action, mechanism}
        self.observer         = ""

    def __repr__(self):
        return (f"<PocletSimData '{self.label}' "
                f"components={len(self.components)} "
                f"asfid={self.asfid_base} "
                f"revoi={self.revoi}>")


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class PocletParser:
    """
    Generic parser for TSCG M0 poclet JSON-LD files.

    Design principles:
      - Namespace-agnostic: detects the m0 prefix from @context automatically
      - Graceful degradation: missing fields yield defaults, not exceptions
      - Pure extraction: no simulation logic here
    """

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self._raw = None
        self._node = None
        self._m0_prefix = None   # e.g. "m0:fire_triangle"
        self._ns = {}            # resolved namespace map

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self) -> PocletSimData:
        self._load()
        self._detect_namespace()
        self._find_main_node()
        return self._extract()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            self._raw = json.load(f)

    def _detect_namespace(self):
        """
        Identify the m0 prefix from @context.
        e.g. "m0:fire_triangle" -> self._m0_prefix = "m0:fire_triangle"
        """
        ctx = self._raw.get("@context", {})
        for key, val in ctx.items():
            if key.startswith("m0:"):
                self._m0_prefix = key
                break
        if not self._m0_prefix:
            # Fallback: try plain "m0"
            self._m0_prefix = "m0"
        self._ns = ctx

    def _find_main_node(self):
        """Find the principal @graph node (NamedIndividual / Poclet)."""
        graph = self._raw.get("@graph", [])
        # Prefer the node whose @id starts with our m0 prefix
        for node in graph:
            nid = node.get("@id", "")
            if self._m0_prefix and nid.startswith(self._m0_prefix):
                self._node = node
                return
        # Fallback: first node
        if graph:
            self._node = graph[0]

    def _k(self, key: str) -> str:
        """Build full prefixed key: 'm0:fire_triangle:components'."""
        return f"{self._m0_prefix}:{key}"

    def _get(self, key, default=None):
        """Get a field from the main node using our m0 prefix."""
        return self._node.get(self._k(key), default)

    def _extract(self) -> PocletSimData:
        sim = PocletSimData()
        node = self._node

        # --- Identity ---
        sim.id      = node.get("@id", "")
        sim.label   = node.get("rdfs:label", "Unknown Poclet")
        sim.comment = node.get("rdfs:comment", "")
        sim.domain  = self._get("domain", "")
        sim.poclet_type = self._get("pocletType", "")
        sim.observer    = self._get("observer", "")

        # --- Synergy ---
        synergy = self._get("synergyPrinciple", {})
        sim.synergy_formula  = synergy.get("formula", "")
        sim.synergy_emergent = synergy.get("emergentProperty", "")

        # --- Components ---
        sim.components = self._extract_components()

        # --- ASFID (Territory / Eagle Eye) ---
        territory = self._get("territorySpace", {})
        asfid_raw = territory.get("asfidState", {})
        sim.asfid_base = ASFIDVector(
            A=float(asfid_raw.get("A", 0.0)),
            S=float(asfid_raw.get("S", 0.0)),
            F=float(asfid_raw.get("F", 0.0)),
            I=float(asfid_raw.get("I", 0.0)),
            D=float(asfid_raw.get("D", 0.0)),
        )

        # --- REVOI (Map / Sphinx Eye) ---
        revoi_section = self._get("revoi", {})
        # Key may be "reviState" or "oriveState" (legacy)
        revoi_raw = (revoi_section.get("reviState")
                     or revoi_section.get("oriveState")
                     or {})
        # Also try mapSpace fallback
        if not revoi_raw:
            map_space = self._get("mapSpace", {})
            revoi_raw = map_space.get("reviState", {})

        sim.revoi = REVOIVector(
            R=float(revoi_raw.get("R", 0.0)),
            E=float(revoi_raw.get("E", 0.0)),
            V=float(revoi_raw.get("V", 0.0)),
            O=float(revoi_raw.get("O", 0.0)),
            I=float(revoi_raw.get("I", 0.0)),
        )

        # --- Epistemic Gap ---
        eg = self._get("epistemicGap", {})
        if eg:
            delta_raw = eg.get("deltaVector", "(0,0,0,0,0)")
            # Parse "(+0.10, -0.20, +0.30, -0.15, +0.25)" -> list of floats
            delta_floats = [float(x) for x in
                            re.findall(r"[+-]?\d+\.?\d*", delta_raw)]
            sim.epistemic_gap = EpistemicGap(
                norm=float(eg.get("norm", 0.0)),
                delta_vector=delta_floats,
                interpretation=eg.get("interpretation", ""),
                assessment=eg.get("assessment", ""),
            )

        # --- Metaconcepts ---
        mc = self._get("metaconceptsMobilized", {})
        sim.metaconcept_count = int(mc.get("total", 0))
        critical = mc.get("criticalMetaconcepts", [])
        sim.metaconcepts = [m.get("name", "") for m in critical if m.get("name")]

        # --- Extinguishment ---
        ext = self._get("extinguishmentStrategies", {})
        sim.extinguishment = ext.get("methods", [])

        return sim

    def _extract_components(self) -> list:
        """
        Extract components with thresholds inferred from constraints.
        Returns list of ComponentData.
        """
        raw_components = self._get("components", [])
        constraints    = self._get("constraints", [])

        # Build a threshold map: parameter_name -> {value, label}
        threshold_map = {}
        for c in constraints:
            param     = c.get("parameter", "").lower()
            condition = c.get("condition", "")
            ctype     = c.get("type", "")
            # Extract numeric value from condition string
            nums = re.findall(r"\d+\.?\d*", condition)
            value = float(nums[0]) if nums else None
            threshold_map[param] = {
                "value": value,
                "label": condition,
                "type":  ctype,
            }

        components = []
        for raw in raw_components:
            label = raw.get("rdfs:label", "Unknown")
            cid   = raw.get("@id", "")
            role  = raw.get(self._k("role"), "")
            func  = raw.get(self._k("function"), "")
            asfid = raw.get(self._k("asfidContribution"), {})
            examples = raw.get(self._k("examples"), [])

            # Match threshold by label keyword
            threshold_val   = None
            threshold_label = None
            label_lower = label.lower()
            for param_key, t in threshold_map.items():
                if param_key in label_lower or label_lower in param_key:
                    threshold_val   = t["value"]
                    threshold_label = t["label"]
                    break

            components.append(ComponentData(
                cid=cid,
                label=label,
                role=role,
                function=func,
                asfid_contribution=asfid,
                threshold=threshold_val,
                threshold_label=threshold_label,
                examples=examples,
            ))

        return components


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "M0_FireTriangle.jsonld"
    parser = PocletParser(path)
    data   = parser.parse()

    print(f"\n{'='*60}")
    print(f"  POCLET: {data.label}")
    print(f"{'='*60}")
    print(f"  Domain   : {data.domain}")
    print(f"  Observer : {data.observer}")
    print(f"  Synergy  : {data.synergy_formula}")
    print(f"  Emergent : {data.synergy_emergent}")
    print(f"\n  ASFID (Territory): {data.asfid_base}")
    print(f"  REVOI  (Map)     : {data.revoi}  mean={data.revoi.mean():.2f}")
    if data.epistemic_gap:
        print(f"  ΔΘ (Epistemic Gap): {data.epistemic_gap}")
    print(f"\n  Components ({len(data.components)}):")
    for c in data.components:
        print(f"    - {c.label}")
        print(f"        role      : {c.role}")
        print(f"        threshold : {c.threshold} ({c.threshold_label})")
        print(f"        ASFID     : {c.asfid_contribution}")
    print(f"\n  Critical Metaconcepts: {data.metaconcepts}")
    print(f"  Total mobilized     : {data.metaconcept_count}")
