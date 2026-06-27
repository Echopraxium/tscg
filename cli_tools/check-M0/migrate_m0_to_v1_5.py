#!/usr/bin/env python3
"""
TSCG M0 Migration Script — v1.5.1
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-06-26

Changes vs v1.5.0:
  fix_tensor_formula_in_all_nodes() now calls:
    (a) fix_tensor_formula()               — m2:hasTensorFormula → m2:hasStructuralGrammarFormula
    (b) fix_tensor_formula_in_nested_objects() — "tensorFormula" key in nested objects (NakamotoConsensus)
    (c) fix_tensor_operator_in_formulas()  — ⊗ → × in all formula string values
  
  New methods added to V15Transformer:
    - fix_tensor_formula_in_nested_objects(data)
    - fix_tensor_operator_in_formulas(data)

[Full script — identical to v1.5.0 except patched methods]
"""

import json
import shutil
import sys
import argparse
from pathlib import Path
from datetime import datetime
from copy import deepcopy

REPO_ROOT        = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
INSTANCES_ROOT   = REPO_ROOT / "instances"
ONTOLOGY_DIR     = REPO_ROOT / "ontology"
SCRIPT_DIR       = Path(__file__).parent.resolve()

SHACL_SCHEMA = SCRIPT_DIR / "M0_Instances_Schema_shacl_v1.5.ttl"
if not SHACL_SCHEMA.exists():
    for candidate in [
        SCRIPT_DIR / "M0_Instances_Schema.shacl.ttl",
        ONTOLOGY_DIR / "M0_Instances_Schema.shacl.ttl",
    ]:
        if candidate.exists():
            SHACL_SCHEMA = candidate
            break

BASE_ONTOLOGY    = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
BASE_INSTANCES   = "https://raw.githubusercontent.com/Echopraxium/tscg/main/instances/"
M0_COMMON_URL    = BASE_ONTOLOGY + "M0_Common.jsonld#"
M0_COMMON_SHORT  = "M0_Common.jsonld"

INSTANCE_DIRS = {
    "poclet":            (INSTANCES_ROOT / "poclets",                 "m3:Poclet"),
    "systemic_framework":(INSTANCES_ROOT / "systemic-frameworks",     "m3:SystemicFramework"),
    "symbolic_grammar":  (INSTANCES_ROOT / "symbolic-system-grammar","m3:SymbolicSystemGrammar"),
    "tscg_tool":         (INSTANCES_ROOT / "tscg-tools",              "m3:TscgTool"),
    "transdisclet":      (INSTANCES_ROOT / "transdisclet",            "m3:TransDisclet"),
}

OBSOLETE_ALIASES = {
    "A_score","S_score","F_score","It_score","D_score",
    "R_score","E_score","V_score","O_score","Im_score",
    "m1core","sm",
}

ENUM_PROPERTIES = {"m0:spectralClass","m0:focalClass","m0:scoringStatus"}
ENUM_PREFIXES   = {
    "m0:spectralClass": "m0:spectralClass.",
    "m0:focalClass":    "m0:focalClass.",
    "m0:scoringStatus": "m0:scoringStatus.",
}


class V15Transformer:

    @staticmethod
    def fix_m0_namespace(context, instance_name, instance_type_dir):
        mods = []
        old_m0 = context.get("m0", "")
        if old_m0 != M0_COMMON_URL:
            context["m0"] = M0_COMMON_URL
            mods.append("@context: m0: -> M0_Common.jsonld# (shared canonical)")

        import re as _re
        parts = _re.split(r'[_\-]', instance_name)
        camel = parts[0].lower() + "".join(p.capitalize() for p in parts[1:]) if len(parts) > 1 \
                else instance_name[0].lower() + instance_name[1:]
        local_alias = f"m0.{camel}"
        local_iri   = (BASE_INSTANCES + instance_type_dir + "/" + instance_name + "/M0_" + instance_name + ".jsonld#")

        if local_alias not in context:
            context[local_alias] = local_iri
            mods.append(f"@context: Added {local_alias}:")

        camel_lower = camel.lower()
        for old_alias in [f"m0{camel_lower}", f"m0{instance_name}"]:
            if old_alias in context:
                del context[old_alias]
                mods.append(f"@context: Removed legacy alias {old_alias}:")

        legacy_keys = [
            k for k in list(context.keys())
            if (k.startswith("m0:") or k.startswith("eagle_eye:") or k.startswith("sphinx_eye:") or k == "m1core")
            and k != local_alias and k != "m0"
        ]
        for k in legacy_keys:
            del context[k]
            mods.append(f"@context: Removed legacy entry {k!r}")

        return mods

    @staticmethod
    def fix_m1_extensions(context):
        mods = []
        KNOWN_EXT_ALIASES = {
            "m1bio":"biology","m1chem":"chemistry","m1phys":"physics","m1elec":"electronics",
            "m1mus":"music","m1myth":"mythology","m1econ":"economics","m1opt":"optics",
            "m1photo":"photography","m1sysmod":"systemic-modeling","m1geo":"geology",
            "m1edu":"education","m1energy":"energy-generators","m1biz":"business-modeling",
        }
        def canonical_ext_alias(domain): return f"m1.extensions.{domain}"
        def canonical_ext_iri(domain):
            domain_title = domain.replace("-"," ").title().replace(" ","")
            return BASE_ONTOLOGY + f"M1_extensions/{domain}/M1_{domain_title}.jsonld#"

        for old_alias, domain in KNOWN_EXT_ALIASES.items():
            if old_alias in context:
                context[canonical_ext_alias(domain)] = canonical_ext_iri(domain)
                context.pop(old_alias)
                mods.append(f"@context: {old_alias} -> {canonical_ext_alias(domain)}")

        for key in list(context.keys()):
            if key.startswith("m1.ext:"):
                domain = key.split(":",1)[1]
                context[canonical_ext_alias(domain)] = canonical_ext_iri(domain)
                context.pop(key)
                mods.append(f"@context: {key} -> {canonical_ext_alias(domain)}")
        return mods

    @staticmethod
    def remove_obsolete_aliases(context):
        mods = []
        for alias in OBSOLETE_ALIASES:
            if alias in context:
                del context[alias]
                mods.append(f"@context: Removed obsolete alias '{alias}'")
        return mods

    @staticmethod
    def ensure_m0_common_import(ontology):
        imports = ontology.get("owl:imports", [])
        if isinstance(imports, str): imports = [imports]
        if any("M0_Common" in str(i) for i in imports):
            return False
        imports.insert(0, M0_COMMON_SHORT)
        ontology["owl:imports"] = imports
        return True

    @staticmethod
    def flatten_nested_scores(ontology):
        ASFID_MAP = {"attractor":"m0:scoreA","structure":"m0:scoreS","flow":"m0:scoreF",
                     "information":"m0:scoreIt","dynamics":"m0:scoreD","overall":"m0:asfidMean"}
        REVOI_MAP = {"representability":"m0:scoreR","evolvability":"m0:scoreE",
                     "verifiability":"m0:scoreV","observability":"m0:scoreO",
                     "interoperability":"m0:scoreIm","overall":"m0:revoiMean"}
        mods = []
        for src, mapping, label in [("m1:asfidScoring",ASFID_MAP,"ASFID"),("m1:revoiScoring",REVOI_MAP,"REVOI")]:
            if src in ontology:
                obj = ontology.pop(src)
                if isinstance(obj, dict):
                    for k, p in mapping.items():
                        if k in obj and isinstance(obj[k],(int,float)): ontology[p] = obj[k]
                    mods.append(f"Flattened {src}{{}} -> m0:score* + m0:{label.lower()}Mean")
        return mods

    @staticmethod
    def _extract_score_value(val):
        if isinstance(val, (int,float)): return float(val)
        if isinstance(val, dict) and "@value" in val:
            try: return float(val["@value"])
            except: pass
        return None

    @staticmethod
    def flatten_asfid_scores_object(node):
        ASFID_KEY_MAP = {"A_score":"m0:scoreA","S_score":"m0:scoreS","F_score":"m0:scoreF",
                         "It_score":"m0:scoreIt","D_score":"m0:scoreD","A":"m0:scoreA",
                         "S":"m0:scoreS","F":"m0:scoreF","I":"m0:scoreIt","D":"m0:scoreD",
                         "m0:scoreA":"m0:scoreA","m0:scoreS":"m0:scoreS","m0:scoreF":"m0:scoreF",
                         "m0:scoreIt":"m0:scoreIt","m0:scoreD":"m0:scoreD"}
        REVOI_KEY_MAP = {"R_score":"m0:scoreR","E_score":"m0:scoreE","V_score":"m0:scoreV",
                         "O_score":"m0:scoreO","Im_score":"m0:scoreIm","R":"m0:scoreR",
                         "E":"m0:scoreE","V":"m0:scoreV","O":"m0:scoreO","I":"m0:scoreIm",
                         "m0:scoreR":"m0:scoreR","m0:scoreE":"m0:scoreE","m0:scoreV":"m0:scoreV",
                         "m0:scoreO":"m0:scoreO","m0:scoreIm":"m0:scoreIm","It_score":"m0:scoreIm"}
        mods = []
        ev = V15Transformer._extract_score_value
        for src_key, key_map, mean_prop in [
            ("m0:asfidScores",ASFID_KEY_MAP,"m0:asfidMean"),
            ("m0:revoiScores",REVOI_KEY_MAP,"m0:revoiMean"),
            ("asfidScores",ASFID_KEY_MAP,"m0:asfidMean"),
            ("revoiScores",REVOI_KEY_MAP,"m0:revoiMean"),
        ]:
            if src_key not in node: continue
            obj = node.pop(src_key)
            if not isinstance(obj, dict): continue
            extracted = []
            for old_k, new_k in key_map.items():
                v = ev(obj.get(old_k))
                if v is not None:
                    node[new_k] = v
                    extracted.append(old_k)
            for mk in ("overall","mean","asfidMean","revoiMean"):
                v = ev(obj.get(mk))
                if v is not None and mean_prop not in node:
                    node[mean_prop] = v
                    break
            if extracted:
                mods.append(f"Flattened {src_key}{{}}")
        return mods

    @staticmethod
    def rename_alias_score_keys(ontology, context):
        ALIAS_TO_PROP = {"A_score":"m0:scoreA","S_score":"m0:scoreS","F_score":"m0:scoreF",
                         "It_score":"m0:scoreIt","D_score":"m0:scoreD","R_score":"m0:scoreR",
                         "E_score":"m0:scoreE","V_score":"m0:scoreV","O_score":"m0:scoreO",
                         "Im_score":"m0:scoreIm"}
        mods = []
        for old_key, new_key in ALIAS_TO_PROP.items():
            if old_key in ontology:
                val = ontology.pop(old_key)
                if isinstance(val, dict) and "@value" in val:
                    try: val = float(val["@value"])
                    except: pass
                ontology[new_key] = val
                mods.append(old_key)
        if mods: return [f"Renamed score aliases: {', '.join(mods)}"]
        return []

    @staticmethod
    def rename_prefixed_keys_in_graph(graph, context):
        PREFIX_MAP = {
            "m1core:":"m1:","m1bio:":"m1.extensions.biology:","m1chem:":"m1.extensions.chemistry:",
            "m1phys:":"m1.extensions.physics:","m1elec:":"m1.extensions.electronics:",
            "m1mus:":"m1.extensions.music:","m1myth:":"m1.extensions.mythology:",
            "m1econ:":"m1.extensions.economics:","m1opt:":"m1.extensions.optics:",
            "m1photo:":"m1.extensions.photography:","m1sysmod:":"m1.extensions.systemic-modeling:",
            "m1geo:":"m1.extensions.geology:","m1edu:":"m1.extensions.education:",
            "m1energy:":"m1.extensions.energy-generators:","m1biz:":"m1.extensions.business-modeling:",
        }
        mods = []
        def rename_node_keys(node):
            for key in list(node.keys()):
                for old_pfx, new_pfx in PREFIX_MAP.items():
                    if key.startswith(old_pfx):
                        node[new_pfx + key[len(old_pfx):]] = node.pop(key)
                        mods.append(f"Key rename: {key}")
                        break
        for node in graph:
            if isinstance(node, dict): rename_node_keys(node)
        return mods

    @staticmethod
    def fix_tensor_formula(node):
        """m2:hasTensorFormula -> m2:hasStructuralGrammarFormula on direct node property."""
        if "m2:hasTensorFormula" in node:
            node["m2:hasStructuralGrammarFormula"] = node.pop("m2:hasTensorFormula")
            return True
        return False

    @staticmethod
    def fix_tensor_formula_in_nested_objects(data):
        """
        Rename "tensorFormula" -> "structuralGrammarFormula" in nested objects.

        Pattern (NakamotoConsensus):
          "m0:genericConceptsMobilized": {
            "concepts": [
              {"name": "Dissipation", "tensorFormula": "F x D", "role": "..."},
            ]
          }
        """
        mods = []

        def _rename_in_obj(obj, path=""):
            if isinstance(obj, dict):
                keys_to_rename = [k for k in obj if k == "tensorFormula"]
                for k in keys_to_rename:
                    obj["structuralGrammarFormula"] = obj.pop(k)
                    mods.append(f"tensorFormula -> structuralGrammarFormula at {path}")
                for k, v in list(obj.items()):
                    _rename_in_obj(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    _rename_in_obj(item, f"{path}[{i}]")

        for i, node in enumerate(data.get("@graph", [])):
            _rename_in_obj(node, f"@graph[{i}]")

        return mods

    @staticmethod
    def fix_tensor_operator_in_formulas(data):
        """
        Replace all ⊗ (U+2297) with × (U+00D7) in string values across @graph.

        NOTE: Automatic grammar detection is fragile. All ⊗ become × by default.
        Formulas crossing Map/Stereopsic grammars may need manual review to use + or |.
        """
        count = [0]

        def _fix_in_obj(obj):
            if isinstance(obj, dict):
                for k in list(obj.keys()):
                    v = obj[k]
                    if isinstance(v, str) and "⊗" in v:
                        obj[k] = v.replace("⊗", "×")
                        count[0] += 1
                    else:
                        _fix_in_obj(v)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, str) and "⊗" in item:
                        obj[i] = item.replace("⊗", "×")
                        count[0] += 1
                    else:
                        _fix_in_obj(item)

        for node in data.get("@graph", []):
            _fix_in_obj(node)

        if count[0] > 0:
            return [
                f"⊗ -> × operator: {count[0]} occurrence(s) replaced. "
                f"NOTE: review formulas crossing Map/Stereopsic grammars (may need + or |)"
            ]
        return []

    @staticmethod
    def fix_score_values(ontology):
        SCORE_PROPS = {
            "m0:scoreA","m0:scoreS","m0:scoreF","m0:scoreIt","m0:scoreD",
            "m0:scoreR","m0:scoreE","m0:scoreV","m0:scoreO","m0:scoreIm",
            "m0:asfidMean","m0:revoiMean","m0:epistemicGap",
            "m0:focalScore","m0:focalBias","m0:stereopsicDepth",
        }
        mods = []
        import re as _re
        for prop in SCORE_PROPS:
            if prop not in ontology: continue
            val = ontology[prop]
            converted = None
            if isinstance(val, (int,float)): converted = float(val)
            elif isinstance(val, dict) and "@value" in val:
                try: converted = float(val["@value"])
                except: pass
            elif isinstance(val, str):
                try: converted = float(val)
                except: pass
            elif isinstance(val, dict) and "norm" in val:
                norm_raw = val["norm"]
                if isinstance(norm_raw,(int,float)): converted = float(norm_raw)
                elif isinstance(norm_raw, str):
                    m = _re.search(r'(\d+\.\d+|\d+)', norm_raw)
                    if m: converted = float(m.group(1))
            if converted is not None and converted != val:
                ontology[prop] = converted
                mods.append(prop)
        if mods: return [f"Bare numerics: {len(mods)} score(s) converted"]
        return []

    @staticmethod
    def fix_enum_values(ontology):
        import re as _re
        mods = []
        for prop, prefix in ENUM_PREFIXES.items():
            if prop not in ontology: continue
            val = ontology[prop]
            if isinstance(val, dict) and "@id" in val:
                iri = val["@id"]
                clean_iri = _re.sub(r'(\s*[\[\(].*)$','',iri).strip()
                if clean_iri != iri:
                    ontology[prop] = {"@id": clean_iri}
                    mods.append(f"Enum IRI cleaned: {prop}")
            elif isinstance(val, str) and not val.startswith("m0:"):
                clean = _re.split(r'\s*[\[\(]', val)[0].strip()
                ontology[prop] = {"@id": prefix + clean}
                mods.append(f"Enum IRI: {prop} -> {{@id: {prefix}{clean}}}")
        return mods

    @staticmethod
    def remove_subnode_ontology_type(data):
        mods = []
        for i, node in enumerate(data.get("@graph",[])[1:], start=1):
            if "m3:ontologyType" in node:
                del node["m3:ontologyType"]
                label = node.get("rdfs:label", node.get("@id", f"node[{i}]"))
                mods.append(f"Removed m3:ontologyType from: {label}")
        return mods

    @staticmethod
    def fix_changelog(ontology):
        cl = ontology.get("m2:changelog")
        if isinstance(cl, list) and len(cl) > 3:
            ontology["m2:changelog"] = cl[:3]
            return True
        return False

    @staticmethod
    def fix_tensor_formula_in_all_nodes(data):
        """
        Apply all tensor formula migrations across @graph:
          (a) m2:hasTensorFormula -> m2:hasStructuralGrammarFormula  (direct property)
          (b) tensorFormula -> structuralGrammarFormula              (nested objects — NakamotoConsensus)
          (c) ⊗ -> × in all formula string values                    (both files)
        """
        mods = []

        # (a) Direct property on each graph node
        for node in data.get("@graph", []):
            if V15Transformer.fix_tensor_formula(node):
                label = node.get("rdfs:label", node.get("@id", "?"))
                mods.append(f"m2:hasTensorFormula -> m2:hasStructuralGrammarFormula: {label}")

        # (b) Nested "tensorFormula" key (NakamotoConsensus pattern)
        mods += V15Transformer.fix_tensor_formula_in_nested_objects(data)

        # (c) ⊗ operator replacement
        mods += V15Transformer.fix_tensor_operator_in_formulas(data)

        return mods


# ============================================================================
# MIGRATOR (identique à v1.5.0)
# ============================================================================

def _instance_type_dir(instance_type):
    return {
        "poclet":"poclets","systemic_framework":"systemic-frameworks",
        "symbolic_grammar":"symbolic-system-grammar","tscg_tool":"tscg-tools",
        "transdisclet":"transdisclet",
    }.get(instance_type, instance_type)


class InstanceMigratorV15:

    def __init__(self, jsonld_path, instance_name, instance_type):
        self.path          = jsonld_path
        self.instance_name = instance_name
        self.instance_type = instance_type
        self.type_dir      = _instance_type_dir(instance_type)
        self.modifications = []
        self.errors        = []

    def _apply(self, data):
        mods = []
        t    = V15Transformer

        if "@graph" not in data or not data["@graph"]:
            return False, ["No @graph array found"]

        context  = data.get("@context", {})
        ontology = data["@graph"][0]

        mods += t.rename_alias_score_keys(ontology, context)
        mods += t.flatten_nested_scores(ontology)

        for node in data["@graph"]:
            sub_mods = t.flatten_asfid_scores_object(node)
            if sub_mods:
                label = node.get("rdfs:label", node.get("@id", "?"))
                mods += [f"{label}: {m}" for m in sub_mods]

        mods += t.fix_m0_namespace(context, self.instance_name, self.type_dir)
        mods += t.fix_m1_extensions(context)
        mods += t.remove_obsolete_aliases(context)
        mods += t.rename_prefixed_keys_in_graph(data["@graph"], context)

        STD = {
            "m1": BASE_ONTOLOGY + "M1_CoreConcepts.jsonld#",
            "m2": BASE_ONTOLOGY + "M2_GenericConcepts.jsonld#",
            "m3": BASE_ONTOLOGY + "M3_GenesisGrammar.jsonld#",
            "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
            "owl":"http://www.w3.org/2002/07/owl#",
            "xsd":"http://www.w3.org/2001/XMLSchema#",
            "dcterms":"http://purl.org/dc/terms/",
            "skos":"http://www.w3.org/2004/02/skos/core#",
        }
        for alias, iri in STD.items():
            if alias not in context:
                context[alias] = iri
                mods.append(f"@context: Added {alias}:")
            elif context[alias] != iri and alias in ("m1","m2","m3"):
                context[alias] = iri
                mods.append(f"@context: Fixed {alias}:")

        if "@base" not in context:
            context["@base"] = BASE_ONTOLOGY
            mods.append("@context: Added @base")

        if t.ensure_m0_common_import(ontology):
            mods.append("owl:imports: Added M0_Common.jsonld")

        mods += t.fix_score_values(ontology)
        mods += t.fix_enum_values(ontology)
        mods += t.fix_tensor_formula_in_all_nodes(data)  # (a)+(b)+(c)
        mods += t.remove_subnode_ontology_type(data)

        if t.fix_changelog(ontology):
            mods.append("m2:changelog: Truncated to 3 entries")

        return True, mods

    def dry_run(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  X {self.instance_name}: read error — {e}")
            return False

        data_copy = deepcopy(data)
        success, mods = self._apply(data_copy)
        if not success:
            print(f"  X {self.instance_name}: {mods}")
            return False
        if mods:
            print(f"  ~ {self.instance_name}: {len(mods)} change(s) would be applied:")
            for m in mods: print(f"     * {m}")
        else:
            print(f"  OK {self.instance_name}: already v1.5 compliant")
        self.modifications = mods
        return True

    def migrate(self, backup_dir=None):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.errors.append(f"Read error: {e}")
            return False

        if backup_dir:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.path, backup_dir / self.path.name)

        success, mods = self._apply(data)
        if not success:
            self.errors += mods
            return False
        self.modifications = mods

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
        except Exception as e:
            self.errors.append(f"Write error: {e}")
            if backup_dir:
                bk = backup_dir / self.path.name
                if bk.exists():
                    shutil.copy2(bk, self.path)
                    self.errors.append("Backup restored")
            return False

        return True

    def validate_shacl(self):
        import subprocess
        if not SHACL_SCHEMA.exists():
            return None, f"SHACL schema not found: {SHACL_SCHEMA}"
        try:
            result = subprocess.run(
                ["pyshacl","-s",str(SHACL_SCHEMA),"-df","json-ld",str(self.path)],
                capture_output=True, text=True, cwd=str(ONTOLOGY_DIR)
            )
            if "Conforms: True" in result.stdout: return True, "SHACL PASS"
            lines = result.stdout.split("\n")
            msgs  = [l for l in lines if "Message:" in l or "Constraint Violation" in l]
            return False, "\n".join(msgs[:5]) if msgs else result.stdout[:400]
        except Exception as e:
            return None, f"pyshacl error: {e}"


# ============================================================================
# DISCOVERY
# ============================================================================

def discover_instances(only_name=None):
    seen = set()
    for itype, (base_dir, _) in INSTANCE_DIRS.items():
        if not base_dir.exists(): continue
        for d in sorted(base_dir.iterdir()):
            if not d.is_dir() or d.name.startswith("_"): continue
            jsonld_files = sorted(d.glob("M0_*.jsonld"))
            if not jsonld_files: continue
            for jsonld in jsonld_files:
                name = jsonld.stem[3:]
                if only_name and name != only_name and d.name != only_name: continue
                key = str(jsonld)
                if key not in seen:
                    seen.add(key)
                    yield jsonld, name, itype
        for jsonld in sorted(base_dir.glob("M0_*.jsonld")):
            name = jsonld.stem[3:]
            if only_name and name != only_name: continue
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
        "# TSCG M0 Migration Report — v1.5.1",
        f"**Date:** {now}",
        f"**Summary:** OK {ok} success  XX {ko} failed  {len(results)} total\n",
        "## Changes applied\n",
        "- m0: -> M0_Common.jsonld# (shared canonical)",
        "- m0.<instance>: added (local namespace)",
        "- m1.extensions.<domain>: (canonical dot-separated)",
        "- Obsolete score aliases removed",
        "- owl:imports M0_Common.jsonld added",
        "- Score values -> bare numerics",
        "- Enum values -> IRI objects",
        "- m2:hasTensorFormula -> m2:hasStructuralGrammarFormula (direct property)",
        "- tensorFormula -> structuralGrammarFormula (nested objects)",
        "- ⊗ -> × operator (all formula string values)",
        "- m3:ontologyType removed from sub-nodes",
        "- m2:changelog truncated to 3 entries\n",
        "## Detailed Results\n",
    ]
    for name, r in results.items():
        status = "OK Success" if r["status"] == "success" else "XX Failed"
        lines.append(f"### {name} ({r.get('type','?')})")
        lines.append(f"**Status:** {status}  |  **SHACL:** {r.get('shacl','—')}\n")
        for m in r.get("modifications",[]): lines.append(f"- {m}")
        for e in r.get("errors",[]): lines.append(f"- ERROR: {e}")
        lines.append("")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nReport: {report_path}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="TSCG M0 Migration v1.5.1")
    parser.add_argument("--dry-run",           action="store_true")
    parser.add_argument("--instance",          metavar="NAME")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--no-backup",         action="store_true")
    parser.add_argument("--no-shacl",          action="store_true")
    args = parser.parse_args()

    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = REPO_ROOT / "migration_backups" / f"v1_5_1_{timestamp}"

    print("=" * 70)
    print("TSCG M0 MIGRATION — v1.5.1")
    print("Extended tensor fix: hasTensorFormula + tensorFormula key + ⊗ operator")
    print("=" * 70)

    if args.dry_run:
        print("\nDRY-RUN MODE — no files will be modified\n")
    else:
        print(f"\nFiles will be modified. Backups -> {backup_root}")
        if not args.instance:
            resp = input("Proceed? [y/N]: ")
            if resp.lower() != "y":
                print("Cancelled")
                return 1

    instances = list(discover_instances(only_name=args.instance))
    if not instances:
        print(f"No JSON-LD files found for: {args.instance or 'any instance'}")
        return 1

    print(f"\nFound {len(instances)} instance(s)\n")

    results = {}
    for jsonld_path, name, itype in instances:
        migrator = InstanceMigratorV15(jsonld_path, name, itype)
        print(f"\n{'─'*60}")
        print(f"  {name}  [{itype}]")
        print(f"{'─'*60}")

        if args.dry_run:
            migrator.dry_run()
            results[name] = {"status":"dry-run","type":itype,
                             "modifications":migrator.modifications,"errors":migrator.errors,"shacl":"—"}
            continue

        backup_dir = None if args.no_backup else (backup_root / name)
        success = migrator.migrate(backup_dir=backup_dir)

        shacl_result = "—"
        if success and not args.no_shacl:
            passed, msg = migrator.validate_shacl()
            if passed is True:
                shacl_result = "PASS"
                print(f"  SHACL: PASS")
            elif passed is False:
                shacl_result = "FAIL"
                print(f"  SHACL FAIL: {msg}")
                migrator.errors.append(msg)
                success = False
                if backup_dir:
                    bk = backup_dir / jsonld_path.name
                    if bk.exists():
                        shutil.copy2(bk, jsonld_path)
                        print(f"  Rolled back from backup")
            else:
                shacl_result = f"WARN: {msg}"

        if success:
            print(f"  OK Done — {len(migrator.modifications)} modification(s)")
            for m in migrator.modifications: print(f"     * {m}")
        else:
            print(f"  XX FAILED — {migrator.errors}")
            if not args.continue_on_error:
                return 1

        results[name] = {"status":"success" if success else "failed","type":itype,
                         "modifications":migrator.modifications,"errors":migrator.errors,"shacl":shacl_result}

    print("\n" + "="*70)
    if args.dry_run:
        print(f"DRY-RUN COMPLETE — {len(instances)} instance(s) analysed")
    else:
        ok = sum(1 for r in results.values() if r["status"]=="success")
        ko = sum(1 for r in results.values() if r["status"]=="failed")
        print(f"MIGRATION COMPLETE: OK {ok} success  XX {ko} failed")
        report_path = backup_root / "MIGRATION_REPORT.md" if not args.no_backup else Path("migration_report_v1_5_1.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        generate_report(results, report_path)

    return 0

if __name__ == "__main__":
    sys.exit(main())
