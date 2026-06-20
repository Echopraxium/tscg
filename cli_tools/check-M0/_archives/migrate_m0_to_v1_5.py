#!/usr/bin/env python3
"""
TSCG M0 Migration Script — v1.5.0
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-06-20

Migrates all M0 instance JSON-LD files from legacy conventions to v1.5:

Changes applied:
  @context:
    • m0: → M0_Common.jsonld# (shared, canonical)
    • m0.<instance>: → instances/.../M0_<Name>.jsonld# (local)
    • m1.extensions.<domain>: → ontology/M1_extensions/<domain>/M1_<Domain>.jsonld#
    • Removes obsolete aliases: A_score, S_score, ... Im_score, m1core:, m0bmc:, etc.
    • Adds owl:imports M0_Common.jsonld

  @graph[0] (ontology node):
    • m2:hasTensorFormula → m2:hasStructuralGrammarFormula
    • Score values bare numeric:  {"@value": "0.85", "@type": "xsd:float"} → 0.85
    • Enum values as IRI:  "Coherent" → {"@id": "m0:spectralClass.Coherent"}
    • m3:ontologyType removed from sub-nodes (kept only in @graph[0])
    • m2:changelog truncated to 3 most recent entries

  Does NOT change:
    • @base (must already be canonical https://raw.githubusercontent.com/...)
    • m3:ontologyType value in @graph[0]
    • Any domain-specific sub-nodes (@graph[1+])
    • HTML simulation files
    • README files

Usage:
    python migrate_m0_to_v1_5.py [--dry-run] [--instance NAME] [--continue-on-error]

    --dry-run           Show what would change, do not modify files
    --instance NAME     Process only this instance (e.g. FireTriangle)
    --continue-on-error Keep going even if one instance fails
    --no-backup         Skip backup creation (not recommended)
"""

import json
import shutil
import sys
import argparse
from pathlib import Path
from datetime import datetime
from copy import deepcopy

# ============================================================================
# CONFIGURATION — adjust REPO_ROOT to your local path
# ============================================================================

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")

INSTANCES_ROOT   = REPO_ROOT / "instances"
ONTOLOGY_DIR     = REPO_ROOT / "ontology"
SCRIPT_DIR       = Path(__file__).parent.resolve()

# SHACL schema — v1.5 expected alongside this script
SHACL_SCHEMA = SCRIPT_DIR / "M0_Instances_Schema_shacl_v1.5.ttl"
if not SHACL_SCHEMA.exists():
    for candidate in [
        SCRIPT_DIR / "M0_Instances_Schema.shacl.ttl",
        ONTOLOGY_DIR / "M0_Instances_Schema.shacl.ttl",
    ]:
        if candidate.exists():
            SHACL_SCHEMA = candidate
            break

# Canonical URLs
BASE_ONTOLOGY    = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
BASE_INSTANCES   = "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/"
M0_COMMON_URL    = BASE_ONTOLOGY + "M0_Common.jsonld#"
M0_COMMON_SHORT  = "M0_Common.jsonld"   # short form for owl:imports

# Instance sub-directories mapped to their m3:ontologyType
INSTANCE_DIRS = {
    "poclet":            (INSTANCES_ROOT / "poclets",                 "m3:Poclet"),
    "systemic_framework":(INSTANCES_ROOT / "systemic-frameworks",     "m3:SystemicFramework"),
    "symbolic_grammar":  (INSTANCES_ROOT / "symbolic-system-grammar","m3:SymbolicSystemGrammar"),
    "tscg_tool":         (INSTANCES_ROOT / "tscg-tools",              "m3:TscgTool"),
    "transdisclet":      (INSTANCES_ROOT / "transdisclet",            "m3:TransDisclet"),
}

# ============================================================================
# TRANSFORMATION RULES — v1.5
# ============================================================================

# Old @context aliases that must be removed or replaced
OBSOLETE_ALIASES = {
    # Old score aliases (pre-M0_Common era)
    "A_score", "S_score", "F_score", "It_score", "D_score",
    "R_score", "E_score", "V_score", "O_score", "Im_score",
    # Old m1 alias (before m1: became canonical)
    "m1core",
    # sm: (old instance namespace shortcut)
    "sm",
}

# Enum property names that must have IRI values (not string literals)
ENUM_PROPERTIES = {
    "m0:spectralClass",
    "m0:focalClass",
    "m0:scoringStatus",
}

# Known enum prefixes per property
ENUM_PREFIXES = {
    "m0:spectralClass": "m0:spectralClass.",
    "m0:focalClass":    "m0:focalClass.",
    "m0:scoringStatus": "m0:scoringStatus.",
}


class V15Transformer:
    """All v1.5 transformations — stateless static methods."""

    # ── @context ──────────────────────────────────────────────────────────────

    @staticmethod
    def fix_m0_namespace(context, instance_name, instance_type_dir):
        """
        Split old monolithic m0: into:
          m0:             → M0_Common.jsonld#  (shared)
          m0.<instance>:  → instances/.../M0_<Name>.jsonld#  (local)

        Also cleans up:
          - Old m0vsm:, m0bmc: etc. → replaced by m0.vsm:, m0.bmc:
          - Legacy m0:propertyName context entries (values are strings or dicts)
            e.g. "m0:epistemicGap": {"@id": "M0_Poclet#epistemicGap"} → removed
          - m1core: → removed (already handled by remove_obsolete_aliases but also here)
          - eagle_eye:*, sphinx_eye:* as context aliases → removed
        """
        mods = []
        old_m0 = context.get("m0", "")

        # Always set canonical shared m0:
        if old_m0 != M0_COMMON_URL:
            context["m0"] = M0_COMMON_URL
            if old_m0:
                mods.append("@context: m0: → M0_Common.jsonld# (shared canonical)")
            else:
                mods.append("@context: m0: added → M0_Common.jsonld#")

        # Build camelCase local alias
        # Handles acronym names: RGB_Additive → rgbAdditive, CMYK_Subtractive → cmykSubtractive
        # Standard names: FireTriangle → fireTriangle
        import re as _re
        parts = _re.split(r'[_\-]', instance_name)
        if len(parts) > 1:
            # Has underscore/hyphen separator — join with camelCase
            camel = parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
        else:
            # No separator — just lowercase the first char
            camel = instance_name[0].lower() + instance_name[1:]
        local_alias = f"m0.{camel}"

        # Build expected local IRI
        local_iri = (
            BASE_INSTANCES
            + instance_type_dir + "/"
            + instance_name + "/"
            + "M0_" + instance_name + ".jsonld#"
        )

        # Add local alias if not already present (any variant)
        if local_alias not in context:
            context[local_alias] = local_iri
            mods.append(f"@context: Added {local_alias}:")

        # Remove old m0<Name>: dot-less aliases (e.g. m0vsm, m0bmc, m0triz)
        camel_lower = camel.lower()
        for old_alias in [f"m0{camel_lower}", f"m0{instance_name}"]:
            if old_alias in context:
                del context[old_alias]
                mods.append(f"@context: Removed legacy alias {old_alias}:")

        # Remove legacy context entries whose KEY looks like "m0:something"
        # These are old inline property definitions from the M0_Poclet# era
        # e.g. "m0:epistemicGap": {"@id": "M0_Poclet#epistemicGap", "@type": "xsd:float"}
        legacy_keys = [
            k for k in list(context.keys())
            if (k.startswith("m0:") or k.startswith("m0.") and ":" in k
                or k.startswith("eagle_eye:") or k.startswith("sphinx_eye:")
                or k.startswith("m3:eagle_eye") or k.startswith("m3:sphinx_eye")
                or k == "m1core")
            and k != local_alias
            and k != "m0"
        ]
        for k in legacy_keys:
            del context[k]
            mods.append(f"@context: Removed legacy entry {k!r}")

        return mods

    @staticmethod
    def fix_m1_extensions(context):
        """
        Convert old m1 extension aliases to canonical dot-separated pattern:
          "m1bio":   "M1_extensions/biology/M1_Biology.jsonld#"
          "m1chem":  "M1_extensions/chemistry/M1_Chemistry.jsonld#"
          "m1.ext:biology": ...  (old variant)
        → "m1.extensions.biology": "https://.../M1_extensions/biology/M1_Biology.jsonld#"
        """
        mods = []
        # Map known shorthand aliases to their canonical domain
        KNOWN_EXT_ALIASES = {
            "m1bio":        "biology",
            "m1chem":       "chemistry",
            "m1phys":       "physics",
            "m1elec":       "electronics",
            "m1mus":        "music",
            "m1myth":       "mythology",
            "m1econ":       "economics",
            "m1opt":        "optics",
            "m1photo":      "photography",
            "m1sysmod":     "systemic-modeling",
            "m1geo":        "geology",
            "m1edu":        "education",
            "m1energy":     "energy-generators",
            "m1biz":        "business-modeling",
        }

        def canonical_ext_alias(domain):
            """e.g. 'biology' → 'm1.extensions.biology'"""
            return f"m1.extensions.{domain}"

        def canonical_ext_iri(domain):
            """e.g. 'biology' → full IRI"""
            domain_title = domain.replace("-", " ").title().replace(" ", "")
            return BASE_ONTOLOGY + f"M1_extensions/{domain}/M1_{domain_title}.jsonld#"

        for old_alias, domain in KNOWN_EXT_ALIASES.items():
            if old_alias in context:
                new_alias = canonical_ext_alias(domain)
                new_iri   = canonical_ext_iri(domain)
                old_iri   = context.pop(old_alias)
                context[new_alias] = new_iri
                mods.append(f"@context: {old_alias} → {new_alias}: {new_iri}")

        # Also fix "m1.ext:<domain>" old pattern
        for key in list(context.keys()):
            if key.startswith("m1.ext:"):
                domain = key.split(":", 1)[1]
                new_alias = canonical_ext_alias(domain)
                new_iri   = canonical_ext_iri(domain)
                context.pop(key)
                context[new_alias] = new_iri
                mods.append(f"@context: {key} → {new_alias}: {new_iri}")

        return mods

    @staticmethod
    def remove_obsolete_aliases(context):
        """Remove old score aliases (A_score, ...) and deprecated prefixes."""
        mods = []
        for alias in OBSOLETE_ALIASES:
            if alias in context:
                del context[alias]
                mods.append(f"@context: Removed obsolete alias '{alias}'")
        return mods

    @staticmethod
    def ensure_m0_common_import(ontology):
        """Add M0_Common.jsonld to owl:imports if not already present."""
        imports = ontology.get("owl:imports", [])
        if isinstance(imports, str):
            imports = [imports]

        # Check any form: short "M0_Common.jsonld" or full URL
        already = any(
            "M0_Common" in str(imp) for imp in imports
        )
        if already:
            return False

        imports.insert(0, M0_COMMON_SHORT)
        ontology["owl:imports"] = imports
        return True

    # ── @graph[0] body ───────────────────────────────────────────────────────

    @staticmethod
    def flatten_nested_scores(ontology):
        """
        Convert nested m1:asfidScoring{} / m1:revoiScoring{} objects to flat m0:scoreX properties.

        Pattern (legacy — AdaptativeImmuneResponse):
          "m1:asfidScoring": {"attractor": 0.95, "structure": 0.9, "flow": 0.85,
                               "information": 0.95, "dynamics": 0.9, "overall": 0.91}
          "m1:revoiScoring": {"representability": 0.9, "evolvability": 0.85, ...}

        Produces:
          "m0:scoreA": 0.95, "m0:scoreS": 0.9, "m0:scoreF": 0.85,
          "m0:scoreIt": 0.95, "m0:scoreD": 0.9, "m0:asfidMean": 0.91
          "m0:scoreR": 0.9, "m0:scoreE": 0.85, ...
        """
        ASFID_MAP = {
            "attractor":   "m0:scoreA",
            "structure":   "m0:scoreS",
            "flow":        "m0:scoreF",
            "information": "m0:scoreIt",
            "dynamics":    "m0:scoreD",
            "overall":     "m0:asfidMean",
        }
        REVOI_MAP = {
            "representability": "m0:scoreR",
            "evolvability":     "m0:scoreE",
            "verifiability":    "m0:scoreV",
            "observability":    "m0:scoreO",
            "interoperability": "m0:scoreIm",
            "overall":          "m0:revoiMean",
        }
        mods = []

        if "m1:asfidScoring" in ontology:
            obj = ontology.pop("m1:asfidScoring")
            if isinstance(obj, dict):
                for key, prop in ASFID_MAP.items():
                    if key in obj and isinstance(obj[key], (int, float)):
                        ontology[prop] = obj[key]
                # Preserve interpretation as rdfs:comment if present
                if "interpretation" in obj and "m0:scoringJustification" not in ontology:
                    ontology["m0:scoringJustification"] = obj["interpretation"]
                mods.append("Flattened m1:asfidScoring{} → m0:scoreA/S/F/It/D + m0:asfidMean")

        if "m1:revoiScoring" in ontology:
            obj = ontology.pop("m1:revoiScoring")
            if isinstance(obj, dict):
                for key, prop in REVOI_MAP.items():
                    if key in obj and isinstance(obj[key], (int, float)):
                        ontology[prop] = obj[key]
                if "interpretation" in obj and "m0:scoringJustification" not in ontology:
                    ontology["m0:scoringJustification"] = obj["interpretation"]
                mods.append("Flattened m1:revoiScoring{} → m0:scoreR/E/V/O/Im + m0:revoiMean")

        return mods

    @staticmethod
    def _extract_score_value(val):
        """Convert any score value representation to bare float, or return None."""
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, dict) and "@value" in val:
            try:
                return float(val["@value"])
            except (ValueError, TypeError):
                pass
        return None

    @staticmethod
    def flatten_asfid_scores_object(node):
        """
        Convert m0:asfidScores{} / m0:revoiScores{} objects to flat m0:scoreX properties.
        Removes the objects once flattened.

        Handles all sub-variants of key names found in the corpus:
          A_score / S_score / F_score / It_score / D_score  (ASFID)
          R_score / E_score / V_score / O_score / Im_score  (REVOI)
        Values may be bare numerics OR {"@value":"0.75","@type":"xsd:float"}.

        Also handles bare 'asfidScores' / 'revoiScores' (NakamotoConsensus — no prefix).

        Applied to ANY node (graph[0] AND graph[1+] — KindlebergerMinsky per-phase scores).
        The extracted flat scores are added to the SAME node, then the object is removed.
        """
        ASFID_KEY_MAP = {
            "A_score":    "m0:scoreA",
            "S_score":    "m0:scoreS",
            "F_score":    "m0:scoreF",
            "It_score":   "m0:scoreIt",
            "D_score":    "m0:scoreD",
            # Single-letter variants (NakamotoConsensus)
            "A": "m0:scoreA",
            "S": "m0:scoreS",
            "F": "m0:scoreF",
            "I": "m0:scoreIt",   # In ASFID context: I = Information
            "D": "m0:scoreD",
            # Already-prefixed keys still inside a nested object (CounterPoint)
            "m0:scoreA":  "m0:scoreA",
            "m0:scoreS":  "m0:scoreS",
            "m0:scoreF":  "m0:scoreF",
            "m0:scoreIt": "m0:scoreIt",
            "m0:scoreD":  "m0:scoreD",
        }
        REVOI_KEY_MAP = {
            "R_score":    "m0:scoreR",
            "E_score":    "m0:scoreE",
            "V_score":    "m0:scoreV",
            "O_score":    "m0:scoreO",
            "Im_score":   "m0:scoreIm",
            # Single-letter variants (NakamotoConsensus)
            "R": "m0:scoreR",
            "E": "m0:scoreE",
            "V": "m0:scoreV",
            "O": "m0:scoreO",
            "I": "m0:scoreIm",   # In REVOI context: I = Interoperability
            # Already-prefixed keys (CounterPoint)
            "m0:scoreR":  "m0:scoreR",
            "m0:scoreE":  "m0:scoreE",
            "m0:scoreV":  "m0:scoreV",
            "m0:scoreO":  "m0:scoreO",
            "m0:scoreIm": "m0:scoreIm",
            # Mixed alias in revoiScores (CounterPoint: "It_score" used for Im)
            "It_score":   "m0:scoreIm",
        }

        mods = []
        ev = V15Transformer._extract_score_value

        for src_key, key_map, mean_prop in [
            ("m0:asfidScores",  ASFID_KEY_MAP, "m0:asfidMean"),
            ("m0:revoiScores",  REVOI_KEY_MAP, "m0:revoiMean"),
            ("asfidScores",     ASFID_KEY_MAP, "m0:asfidMean"),   # NakamotoConsensus
            ("revoiScores",     REVOI_KEY_MAP, "m0:revoiMean"),   # NakamotoConsensus
        ]:
            if src_key not in node:
                continue
            obj = node.pop(src_key)
            if not isinstance(obj, dict):
                continue

            extracted = []
            for old_k, new_k in key_map.items():
                v = ev(obj.get(old_k))
                if v is not None:
                    node[new_k] = v
                    extracted.append(old_k)

            # overall / mean
            for mean_key in ("overall", "mean", "asfidMean", "revoiMean"):
                v = ev(obj.get(mean_key))
                if v is not None and mean_prop not in node:
                    node[mean_prop] = v
                    break

            if extracted:
                mods.append(f"Flattened {src_key}{{}} → {', '.join(extracted)}")

        # NakamotoConsensus deep-nested: m0:territorySpace.asfidScores / m0:mapSpace.revoiScores
        ev = V15Transformer._extract_score_value
        for container_key, scores_key, key_map, mean_prop in [
            ("m0:territorySpace", "asfidScores", ASFID_KEY_MAP, "m0:asfidMean"),
            ("m0:mapSpace",       "revoiScores", REVOI_KEY_MAP, "m0:revoiMean"),
        ]:
            container = node.get(container_key)
            if not isinstance(container, dict):
                continue
            obj = container.get(scores_key)
            if not isinstance(obj, dict):
                continue
            extracted = []
            for old_k, new_k in key_map.items():
                v = ev(obj.get(old_k))
                if v is not None and new_k not in node:
                    node[new_k] = v
                    extracted.append(old_k)
            # Remove the scores sub-object from the container
            del container[scores_key]
            if extracted:
                mods.append(f"Flattened {container_key}.{scores_key}{{}} → {', '.join(extracted)}")

        return mods

    @staticmethod
    def rename_alias_score_keys(ontology, context):
        """
        Rename score keys that used @context aliases to their canonical m0: form.

        When @context declared:  "A_score": {"@id": "...M0_Poclet#scoreA", "@type": "xsd:float"}
        the @graph[0] node contains keys like:  "A_score": 0.85

        After remove_obsolete_aliases() strips the alias from @context, these keys
        become unresolvable strings. This method renames them to m0:scoreX BEFORE
        the alias is removed, so the values are preserved.

        Must be called BEFORE remove_obsolete_aliases().
        """
        ALIAS_TO_PROP = {
            "A_score":   "m0:scoreA",
            "S_score":   "m0:scoreS",
            "F_score":   "m0:scoreF",
            "It_score":  "m0:scoreIt",
            "D_score":   "m0:scoreD",
            "R_score":   "m0:scoreR",
            "E_score":   "m0:scoreE",
            "V_score":   "m0:scoreV",
            "O_score":   "m0:scoreO",
            "Im_score":  "m0:scoreIm",
        }
        mods = []
        for old_key, new_key in ALIAS_TO_PROP.items():
            if old_key in ontology:
                val = ontology.pop(old_key)
                # Convert typed value to bare numeric if needed
                if isinstance(val, dict) and "@value" in val:
                    try:
                        val = float(val["@value"])
                    except (ValueError, TypeError):
                        pass
                ontology[new_key] = val
                mods.append(old_key)

        if mods:
            return [f"Renamed score aliases → m0:scoreX: {', '.join(mods)}"]
        return []

    @staticmethod
    def rename_prefixed_keys_in_graph(graph, context):
        """
        Rename legacy-prefixed keys inside ALL graph nodes.

        Problems solved:
          "m1core:simulationTitle" → "m1:simulationTitle"
              (m1core: alias removed from @context but key survives in node body)
          "m1energy:coolantType" → "m1.extensions.energy-generators:coolantType"
              (old short extension alias renamed in @context but not in body)

        Strategy: build a mapping {old_prefix → new_prefix} from what was renamed
        in @context, plus hardcoded legacy patterns. Then walk all nodes and rename
        any key whose prefix matches.
        """
        # Hardcoded legacy prefix → canonical prefix
        PREFIX_MAP = {
            "m1core:":       "m1:",
            "m1bio:":        "m1.extensions.biology:",
            "m1chem:":       "m1.extensions.chemistry:",
            "m1phys:":       "m1.extensions.physics:",
            "m1elec:":       "m1.extensions.electronics:",
            "m1mus:":        "m1.extensions.music:",
            "m1myth:":       "m1.extensions.mythology:",
            "m1econ:":       "m1.extensions.economics:",
            "m1opt:":        "m1.extensions.optics:",
            "m1photo:":      "m1.extensions.photography:",
            "m1sysmod:":     "m1.extensions.systemic-modeling:",
            "m1geo:":        "m1.extensions.geology:",
            "m1edu:":        "m1.extensions.education:",
            "m1energy:":     "m1.extensions.energy-generators:",
            "m1biz:":        "m1.extensions.business-modeling:",
        }

        mods = []

        def rename_node_keys(node):
            to_rename = []
            for key in list(node.keys()):
                for old_pfx, new_pfx in PREFIX_MAP.items():
                    if key.startswith(old_pfx):
                        new_key = new_pfx + key[len(old_pfx):]
                        to_rename.append((key, new_key, old_pfx))
                        break
            for old_key, new_key, pfx in to_rename:
                node[new_key] = node.pop(old_key)
                mods.append(f"Key rename: {old_key} → {new_key}")

        for node in graph:
            if isinstance(node, dict):
                rename_node_keys(node)

        return mods

    @staticmethod
    def fix_tensor_formula(node):
        """m2:hasTensorFormula → m2:hasStructuralGrammarFormula (anywhere in graph)"""
        if "m2:hasTensorFormula" in node:
            node["m2:hasStructuralGrammarFormula"] = node.pop("m2:hasTensorFormula")
            return True
        return False

    @staticmethod
    def fix_score_values(ontology):
        """
        Convert any score value to a bare Python float:
          {"@value": "0.85", "@type": "xsd:float"} → 0.85
          "0.016"  (string numeric — Counterpoint)   → 0.016
          {"norm": 0.072, ...} (object — NakamotoConsensus epistemicGap) → 0.072

        Applies to all m0:scoreX, m0:asfidMean, m0:revoiMean, m0:epistemicGap, etc.
        """
        SCORE_PROPS = {
            "m0:scoreA", "m0:scoreS", "m0:scoreF", "m0:scoreIt", "m0:scoreD",
            "m0:scoreR", "m0:scoreE", "m0:scoreV", "m0:scoreO", "m0:scoreIm",
            "m0:asfidMean", "m0:revoiMean", "m0:epistemicGap",
            "m0:focalScore", "m0:focalBias", "m0:stereopsicDepth",
        }
        mods = []
        for prop in SCORE_PROPS:
            if prop not in ontology:
                continue
            val = ontology[prop]
            converted = None

            if isinstance(val, (int, float)):
                # Already bare numeric — ensure it's a float (not int)
                converted = float(val)
            elif isinstance(val, dict) and "@value" in val:
                # {"@value": "0.85", "@type": "xsd:float"} pattern
                try:
                    converted = float(val["@value"])
                except (ValueError, TypeError):
                    pass
            elif isinstance(val, str):
                # String numeric: "0.016" → 0.016 (Counterpoint epistemicGap)
                try:
                    converted = float(val)
                except (ValueError, TypeError):
                    pass
            elif isinstance(val, dict) and "norm" in val:
                # Complex epistemicGap object: extract norm
                # Handles: {"norm": 0.072} AND {"norm": "≈ 0.30"} AND {"norm": "approx 0.17"}
                import re as _re
                norm_raw = val["norm"]
                if isinstance(norm_raw, (int, float)):
                    converted = float(norm_raw)
                elif isinstance(norm_raw, str):
                    # Extract first float-like number from string
                    m = _re.search(r'(\d+\.\d+|\d+)', norm_raw)
                    if m:
                        converted = float(m.group(1))

            if converted is not None and converted != val:
                ontology[prop] = converted
                mods.append(f"Score bare numeric: {prop}")

        return mods

    @staticmethod
    def fix_enum_values(ontology):
        """
        Convert string enum values to IRI objects:
          "m0:spectralClass": "Coherent"       → {"@id": "m0:spectralClass.Coherent"}
          "m0:spectralClass": "Coherent [0, 0.05)" → {"@id": "m0:spectralClass.Coherent"}
          "m0:spectralClass": {"@id": "m0:spectralClass.Coherent [0, 0.05)"}
                              → {"@id": "m0:spectralClass.Coherent"}
        """
        import re as _re
        mods = []
        for prop, prefix in ENUM_PREFIXES.items():
            if prop not in ontology:
                continue
            val = ontology[prop]
            if isinstance(val, dict) and "@id" in val:
                # Already IRI — but may contain interval suffix
                iri = val["@id"]
                if iri.startswith(prefix) and not any(iri == prefix + v for v in
                        ("Coherent","OnCriticalLine","Liminal","Enigmatic",
                         "Emmetropic","SlightlyMyopic","SlightlyHyperopic",
                         "Myopic","Hyperopic","Astigmatic",
                         "Complete","Partial","Pending")):
                    # Strip suffix after the valid part
                    clean_iri = _re.sub(r'(\s*[\[\(].*)$', '', iri).strip()
                    if clean_iri != iri:
                        ontology[prop] = {"@id": clean_iri}
                        mods.append(f"Enum IRI cleaned: {prop} interval suffix removed")
            elif isinstance(val, str) and not val.startswith("m0:"):
                # Strip interval notation: "Coherent [0, 0.05)" → "Coherent"
                clean = _re.split(r'\s*[\[\(]', val)[0].strip()
                ontology[prop] = {"@id": prefix + clean}
                mods.append(f"Enum IRI: {prop} → {{@id: {prefix}{clean}}}")
        return mods

    @staticmethod
    def remove_subnode_ontology_type(data):
        """
        m3:ontologyType must only appear in @graph[0].
        Remove it from @graph[1+] if present.
        """
        mods = []
        graph = data.get("@graph", [])
        for i, node in enumerate(graph[1:], start=1):
            if "m3:ontologyType" in node:
                del node["m3:ontologyType"]
                label = node.get("rdfs:label", node.get("@id", f"node[{i}]"))
                mods.append(f"Removed m3:ontologyType from sub-node: {label}")
        return mods

    @staticmethod
    def fix_changelog(ontology):
        """Keep only the 3 most recent changelog entries."""
        cl = ontology.get("m2:changelog")
        if isinstance(cl, list) and len(cl) > 3:
            ontology["m2:changelog"] = cl[:3]
            return True
        return False

    @staticmethod
    def fix_tensor_formula_in_all_nodes(data):
        """Apply hasTensorFormula → hasStructuralGrammarFormula across all @graph nodes."""
        mods = []
        for node in data.get("@graph", []):
            if V15Transformer.fix_tensor_formula(node):
                label = node.get("rdfs:label", node.get("@id", "?"))
                mods.append(f"hasStructuralGrammarFormula in node: {label}")
        return mods


# ============================================================================
# MIGRATOR
# ============================================================================

def _instance_type_dir(instance_type):
    """Returns the sub-path fragment used in instance IRIs (e.g. 'poclets')."""
    mapping = {
        "poclet":            "poclets",
        "systemic_framework":"systemic-frameworks",
        "symbolic_grammar":  "symbolic-system-grammar",
        "tscg_tool":         "tscg-tools",
        "transdisclet":      "transdisclet",
    }
    return mapping.get(instance_type, instance_type)


class InstanceMigratorV15:
    """Applies v1.5 transformations to a single M0 instance JSON-LD file."""

    def __init__(self, jsonld_path: Path, instance_name: str, instance_type: str):
        self.path          = jsonld_path
        self.instance_name = instance_name
        self.instance_type = instance_type
        self.type_dir      = _instance_type_dir(instance_type)
        self.modifications = []
        self.errors        = []

    def _apply(self, data):
        """Apply all v1.5 transformations. Returns (success, modifications)."""
        mods = []
        t    = V15Transformer

        if "@graph" not in data or not data["@graph"]:
            return False, ["No @graph array found"]

        context  = data.get("@context", {})
        ontology = data["@graph"][0]

        # ── Score keys rename — BEFORE aliases are removed from @context ──────
        # Aliases still present in @context → we can safely rename the keys
        mods += t.rename_alias_score_keys(ontology, context)
        mods += t.flatten_nested_scores(ontology)

        # ── asfidScores{} / revoiScores{} objects — all graph nodes ──────────
        for node in data["@graph"]:
            sub_mods = t.flatten_asfid_scores_object(node)
            if sub_mods:
                label = node.get("rdfs:label", node.get("@id", "?"))
                mods += [f"{label}: {m}" for m in sub_mods]

        # ── @context ──────────────────────────────────────────────────────────
        mods += t.fix_m0_namespace(context, self.instance_name, self.type_dir)
        mods += t.fix_m1_extensions(context)
        mods += t.remove_obsolete_aliases(context)

        # ── Rename m1core: / extension aliases in ALL graph node keys ─────────
        # Must run AFTER fix_m1_extensions() so we know the canonical mappings
        mods += t.rename_prefixed_keys_in_graph(data["@graph"], context)

        # Ensure standard namespaces are present and absolute
        STD = {
            "m1": BASE_ONTOLOGY + "M1_CoreConcepts.jsonld#",
            "m2": BASE_ONTOLOGY + "M2_GenericConcepts.jsonld#",
            "m3": BASE_ONTOLOGY + "M3_GenesisGrammar.jsonld#",
            "rdf":     "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs":    "http://www.w3.org/2000/01/rdf-schema#",
            "owl":     "http://www.w3.org/2002/07/owl#",
            "xsd":     "http://www.w3.org/2001/XMLSchema#",
            "dcterms": "http://purl.org/dc/terms/",
            "skos":    "http://www.w3.org/2004/02/skos/core#",
        }
        for alias, iri in STD.items():
            if alias not in context:
                context[alias] = iri
                mods.append(f"@context: Added missing {alias}:")
            elif context[alias] != iri and alias in ("m1","m2","m3"):
                # Fix relative to absolute
                context[alias] = iri
                mods.append(f"@context: Fixed {alias}: → absolute URL")

        # Ensure @base
        if "@base" not in context:
            context["@base"] = BASE_ONTOLOGY
            mods.append("@context: Added @base")

        # ── owl:imports ───────────────────────────────────────────────────────
        if t.ensure_m0_common_import(ontology):
            mods.append("owl:imports: Added M0_Common.jsonld")

        # ── Score values ──────────────────────────────────────────────────────
        score_mods = t.fix_score_values(ontology)
        if score_mods:
            mods.append(f"Bare numerics: {len(score_mods)} score(s) converted")

        # ── Enum values ───────────────────────────────────────────────────────
        enum_mods = t.fix_enum_values(ontology)
        mods += enum_mods

        # ── hasStructuralGrammarFormula ───────────────────────────────────────
        formula_mods = t.fix_tensor_formula_in_all_nodes(data)
        mods += formula_mods

        # ── Sub-node ontologyType ─────────────────────────────────────────────
        subnode_mods = t.remove_subnode_ontology_type(data)
        mods += subnode_mods

        # ── Changelog ─────────────────────────────────────────────────────────
        if t.fix_changelog(ontology):
            mods.append("m2:changelog: Truncated to 3 entries")

        return True, mods

    def dry_run(self):
        """Analyse without writing. Returns True (always non-destructive)."""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ✗ {self.instance_name}: read error — {e}")
            return False

        data_copy = deepcopy(data)
        success, mods = self._apply(data_copy)

        if not success:
            print(f"  ✗ {self.instance_name}: {mods}")
            return False

        if mods:
            print(f"  🔧 {self.instance_name}: {len(mods)} change(s) would be applied:")
            for m in mods:
                print(f"     • {m}")
        else:
            print(f"  ✅ {self.instance_name}: already v1.5 compliant — no changes needed")

        self.modifications = mods
        return True

    def migrate(self, backup_dir: Path = None):
        """Apply transformations and write file. Returns True on success."""
        # Read
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.errors.append(f"Read error: {e}")
            return False

        # Backup
        if backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.path, backup_dir / self.path.name)

        # Apply
        success, mods = self._apply(data)
        if not success:
            self.errors += mods
            return False
        self.modifications = mods

        # Write
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            self.errors.append(f"Write error: {e}")
            # Restore backup
            if backup_dir:
                backup_file = backup_dir / self.path.name
                if backup_file.exists():
                    shutil.copy2(backup_file, self.path)
                    self.errors.append("Backup restored after write failure")
            return False

        return True

    def validate_shacl(self):
        """Run pyshacl. Returns (passed: bool, message: str)."""
        import subprocess
        if not SHACL_SCHEMA.exists():
            return None, f"SHACL schema not found: {SHACL_SCHEMA}"
        try:
            result = subprocess.run(
                ["pyshacl", "-s", str(SHACL_SCHEMA), "-df", "json-ld", str(self.path)],
                capture_output=True, text=True, cwd=str(ONTOLOGY_DIR)
            )
            if "Conforms: True" in result.stdout:
                return True, "SHACL PASS"
            lines  = result.stdout.split("\n")
            msgs   = [l for l in lines if "Message:" in l or "Constraint Violation" in l]
            summary = "\n".join(msgs[:5]) if msgs else result.stdout[:400]
            return False, f"SHACL FAIL:\n{summary}"
        except Exception as e:
            return None, f"pyshacl error: {e}"


# ============================================================================
# DISCOVERY
# ============================================================================

def discover_instances(only_name=None):
    """
    Yield (jsonld_path, instance_name, instance_type) for every M0 instance.

    Supports two layouts:
      Layout A (sub-folder per instance):
        instances/poclets/FireTriangle/M0_FireTriangle.jsonld

      Layout A+ (federated poclet — multiple JSON-LD in one folder):
        instances/poclets/ColorSynthesis/M0_ColorSynthesis.jsonld   ← main
        instances/poclets/ColorSynthesis/M0_CMYK_Subtractive.jsonld ← satellite
        instances/poclets/ColorSynthesis/M0_RGB_Additive.jsonld     ← satellite
        All files in the folder are migrated.

      Layout B (flat):
        instances/poclets/M0_FireTriangle.jsonld

    Folders with no M0_*.jsonld are silently skipped (not considered instances).
    If only_name is given, filter to instances whose name matches.
    """
    seen = set()

    for itype, (base_dir, _) in INSTANCE_DIRS.items():
        if not base_dir.exists():
            continue

        # Layout A / A+ — sub-folder(s) per instance
        for d in sorted(base_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_"):
                continue
            folder_name = d.name

            # Collect ALL M0_*.jsonld in this folder
            jsonld_files = sorted(d.glob("M0_*.jsonld"))
            if not jsonld_files:
                continue  # no .jsonld → not an instance folder

            for jsonld in jsonld_files:
                name = jsonld.stem[3:]  # strip "M0_"
                if only_name and name != only_name and folder_name != only_name:
                    continue
                key = str(jsonld)
                if key not in seen:
                    seen.add(key)
                    yield jsonld, name, itype

        # Layout B — flat (M0_*.jsonld directly in base_dir)
        for jsonld in sorted(base_dir.glob("M0_*.jsonld")):
            name = jsonld.stem[3:]
            if only_name and name != only_name:
                continue
            key = str(jsonld)
            if key not in seen:
                seen.add(key)
                yield jsonld, name, itype


# ============================================================================
# REPORTING
# ============================================================================

def generate_report(results, report_path):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ok  = sum(1 for r in results.values() if r["status"] == "success")
    ko  = sum(1 for r in results.values() if r["status"] == "failed")

    lines = [
        "# TSCG M0 Migration Report — v1.5.0",
        f"\n**Date:** {now}",
        f"**Summary:** ✅ {ok} success  ❌ {ko} failed  📊 {len(results)} total\n",
        "---\n",
        "## Changes applied\n",
        "- `m0:` → `M0_Common.jsonld#` (shared canonical)",
        "- `m0.<instance>:` added (local namespace)",
        "- `m1.extensions.<domain>:` (canonical dot-separated)",
        "- Obsolete score aliases removed (A_score...)",
        "- `owl:imports M0_Common.jsonld` added",
        "- Score values → bare numerics",
        "- Enum values → IRI objects (`{@id: m0:spectralClass.Coherent}`)",
        "- `m2:hasTensorFormula` → `m2:hasStructuralGrammarFormula`",
        "- `m3:ontologyType` removed from sub-nodes",
        "- `m2:changelog` truncated to 3 entries",
        "\n---\n",
        "## Detailed Results\n",
    ]

    for name, r in results.items():
        status = "✅ Success" if r["status"] == "success" else "❌ Failed"
        shacl  = r.get("shacl", "—")
        lines.append(f"### {name} ({r.get('type','?')})")
        lines.append(f"**Status:** {status}  |  **SHACL:** {shacl}\n")
        if r["modifications"]:
            lines.append("**Modifications:**")
            for m in r["modifications"]:
                lines.append(f"- {m}")
            lines.append("")
        if r["errors"]:
            lines.append("**Errors:**")
            for e in r["errors"]:
                lines.append(f"- {e}")
            lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n📄 Report: {report_path}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="TSCG M0 Migration to v1.5 — M0_Common namespace, bare numerics, enum IRIs"
    )
    parser.add_argument("--dry-run",          action="store_true",
                        help="Show changes without modifying files")
    parser.add_argument("--instance",         metavar="NAME",
                        help="Process only one instance (e.g. FireTriangle)")
    parser.add_argument("--continue-on-error", action="store_true",
                        help="Keep going if an instance fails")
    parser.add_argument("--no-backup",        action="store_true",
                        help="Skip backup creation")
    parser.add_argument("--no-shacl",         action="store_true",
                        help="Skip SHACL validation after migration")
    args = parser.parse_args()

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = REPO_ROOT / "migration_backups" / f"v1_5_{timestamp}"

    print("=" * 70)
    print("TSCG M0 MIGRATION — v1.5.0  (M0_Common + bare numerics + enum IRIs)")
    print("=" * 70)

    if args.dry_run:
        print("\n🔍 DRY-RUN MODE — no files will be modified\n")
    else:
        print(f"\n⚠️  Files will be modified. Backups → {backup_root}")
        if not args.instance:
            resp = input("Proceed with full corpus migration? [y/N]: ")
            if resp.lower() != "y":
                print("❌ Cancelled")
                return 1

    instances = list(discover_instances(only_name=args.instance))
    if not instances:
        target = args.instance or "any instance"
        print(f"⚠️  No JSON-LD files found for: {target}")
        return 1

    print(f"\n📊 Found {len(instances)} instance(s) to process\n")

    results = {}
    for jsonld_path, name, itype in instances:
        migrator = InstanceMigratorV15(jsonld_path, name, itype)

        print(f"\n{'─'*60}")
        print(f"  {name}  [{itype}]")
        print(f"{'─'*60}")

        if args.dry_run:
            migrator.dry_run()
            results[name] = {
                "status": "dry-run",
                "type":   itype,
                "modifications": migrator.modifications,
                "errors":        migrator.errors,
                "shacl": "—",
            }
            continue

        # Real migration
        backup_dir = None if args.no_backup else (backup_root / name)
        success = migrator.migrate(backup_dir=backup_dir)

        shacl_result = "—"
        if success and not args.no_shacl:
            passed, msg = migrator.validate_shacl()
            if passed is True:
                shacl_result = "✅ PASS"
                print(f"  ✅ SHACL: PASS")
            elif passed is False:
                shacl_result = "❌ FAIL"
                print(f"  ❌ SHACL: {msg}")
                migrator.errors.append(msg)
                success = False
                # Rollback
                if backup_dir:
                    bk = backup_dir / jsonld_path.name
                    if bk.exists():
                        shutil.copy2(bk, jsonld_path)
                        print(f"  ↩️  Rolled back from backup")
            else:
                shacl_result = f"⚠️  {msg}"
                print(f"  ⚠️  SHACL skipped: {msg}")

        if success:
            n = len(migrator.modifications)
            print(f"  ✅ Done — {n} modification(s)")
            for m in migrator.modifications:
                print(f"     • {m}")
        else:
            print(f"  ❌ FAILED — {migrator.errors}")
            if not args.continue_on_error:
                print("\n💡 Use --continue-on-error to keep going despite failures")
                return 1

        results[name] = {
            "status": "success" if success else "failed",
            "type":   itype,
            "modifications": migrator.modifications,
            "errors":        migrator.errors,
            "shacl":         shacl_result,
        }

    # Summary
    print("\n" + "=" * 70)
    if args.dry_run:
        print("DRY-RUN COMPLETE")
        ok = sum(1 for r in results.values() if r["modifications"] or True)
        print(f"  {len(instances)} instance(s) analysed — run without --dry-run to apply")
    else:
        ok = sum(1 for r in results.values() if r["status"] == "success")
        ko = sum(1 for r in results.values() if r["status"] == "failed")
        print(f"MIGRATION COMPLETE: ✅ {ok} success  ❌ {ko} failed")
        if not args.no_backup:
            print(f"📁 Backups: {backup_root}")
        report_path = backup_root / "MIGRATION_REPORT.md" if not args.no_backup else Path("migration_report_v1_5.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        generate_report(results, report_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
