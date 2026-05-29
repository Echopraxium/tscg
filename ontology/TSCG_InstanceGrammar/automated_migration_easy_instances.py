#!/usr/bin/env python3
"""
TSCG Automated Realignment Script - All Instance Types (v3.0.0)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19 (v2.5.0), 2026-04-20 (v2.6.0, v2.7.0), 2026-05-29 (v3.0.0)
Version: 3.0.0 - Fix @base missing, M3_GenesisSpace → M3_GenesisGrammar migration

FIXES:
- Modifies @graph[0] instead of root level
- Renames m2:ontologyType → m3:ontologyType
- Renames m0:domain → m1:domain
- Adds missing m1:/m3: namespaces to @context (v2.1.0)
- Stop-on-error by default with --continue-on-error option (v2.1.0)
- FIX: add_ontology_type() now handles @type correctly (v2.2.0)
- FIX: Removes m1:Poclet from @type array (v2.2.0)
- NEW: add_domain() extracts domain from m1:pocletCharacteristics (v2.2.0)
- CRITICAL: Converts relative namespace URLs to ABSOLUTE URLs for pyshacl (v2.3.0)
- NEW: Supports federated instances - migrates m0:federatedInstances automatically (v2.4.0)
- FIX: Removes m3:ontologyCategory (not just m2:ontologyCategory) (v2.4.1)
- NEW: Reorders properties (m3:ontologyType right after owl:imports) (v2.4.2)
- FIX: Removes rdf:type when it's an object {"@id": "m3:Poclet"} (v2.4.3)
- FIX: Property ordering works even without owl:imports (v2.4.3)
- NEW: Migrates m0:domain from @graph[1+] to @graph[0] as m1:domain (v2.5.0)
- NEW: Supports SymbolicSystemGrammars (Iching) and SystemicFrameworks (Vsm) (v2.6.0)
- NEW: Includes manually fixed poclets (BloodPressureControl, ButterflyMetamorphosis, CellSignalingModes) (v2.7.0)
"""

import json
import re
import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")

# Instance type directories
POCLETS_DIR = REPO_ROOT / "instances/poclets"
SYMBOLIC_GRAMMARS_DIR = REPO_ROOT / "instances/symbolic-system-grammars"
SYSTEMIC_FRAMEWORKS_DIR = REPO_ROOT / "instances/systemic-frameworks"

ONTOLOGY_DIR = REPO_ROOT / "ontology"
BACKUP_DIR = REPO_ROOT / "migration_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
# v3.0.0: Updated path — SHACL schema is in TSCG_InstanceGrammar/ folder
SHACL_SCHEMA = ONTOLOGY_DIR / "TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl"
if not SHACL_SCHEMA.exists():
    # Fallback: search common locations
    for candidate in [
        ONTOLOGY_DIR / "TSCG_Grammar/M0_Instances_Schema.shacl.ttl",
        ONTOLOGY_DIR / "M0_Instances_Schema.shacl.ttl",
        REPO_ROOT / "ontology/TSCG_InstanceGrammar/M0_Instances_Schema.shacl.ttl",
    ]:
        if candidate.exists():
            SHACL_SCHEMA = candidate
            break

# Instance types configuration
INSTANCE_TYPES = {
    "poclet": {
        "dir": POCLETS_DIR,
        "ontology_type": "m3:Poclet",
        "prefix": "M0_"
    },
    "symbolic_grammar": {
        "dir": SYMBOLIC_GRAMMARS_DIR,
        "ontology_type": "m3:SymbolicSystemGrammar",
        "prefix": "M0_"
    },
    "systemic_framework": {
        "dir": SYSTEMIC_FRAMEWORKS_DIR,
        "ontology_type": "m3:SystemicFramework",
        "prefix": "M0_"
    },
    "tscg_tool": {
        "dir": REPO_ROOT / "instances" / "tscg-tools",
        "ontology_type": "m3:TscgTool",
        "prefix": "M0_"
    }
}

# Instances to EXCLUDE (require manual intervention)
# v2.7.0: All problematic instances have been manually fixed with specialized scripts
# v3.0.0: Theremin excluded — M0_Theremin.jsonld stub not yet created
MANUAL_INSTANCES = {
    # BloodPressureControl - FIXED with fix_bloodpressure_namespace.py (141 tscg: → m0:)
    # ButterflyMetamorphosis - FIXED with fix_butterfly_classes.py (custom classes removed)
    # CellSignalingModes - FIXED with fix_cellsignaling_inline.py (inline components extracted)
}

# Instances already fully compliant (skip migration)
# v3.0.0: AdaptativeImmuneResponse removed — still contains M3_GenesisSpace + m1:Poclet in @type
COMPLIANT_INSTANCES = {
    # Empty — all instances need v3.0.0 migration
}

# ============================================================================
# TRANSFORMATION RULES (CORRECTED)
# ============================================================================

class TransformationRules:
    """Defines all automated transformations - operates on @graph[0]."""
    
    @staticmethod
    def migrate_domain_from_graph_objects(data):
        """Search for m0:domain in ALL @graph objects and migrate to @graph[0] as m1:domain.
        
        Some poclets have m0:domain in @graph[1] (instance data) instead of @graph[0] (ontology metadata).
        This function:
        1. Searches @graph[1], @graph[2], etc. for m0:domain
        2. Extracts its value
        3. Adds it to @graph[0] as m1:domain
        4. Removes m0:domain from the source object
        
        Returns: (modified, domain_value) tuple
        """
        if "@graph" not in data or len(data["@graph"]) == 0:
            return False, None
        
        ontology = data["@graph"][0]
        
        # If m1:domain already exists in @graph[0], do nothing
        if "m1:domain" in ontology:
            return False, None
        
        # Search for m0:domain in @graph[1], @graph[2], etc.
        domain_value = None
        source_index = None
        
        for i in range(1, len(data["@graph"])):
            obj = data["@graph"][i]
            if "m0:domain" in obj:
                domain_value = obj["m0:domain"]
                source_index = i
                break
        
        if domain_value is None:
            return False, None
        
        # Add m1:domain to @graph[0]
        ontology["m1:domain"] = domain_value
        
        # Remove m0:domain from source object
        del data["@graph"][source_index]["m0:domain"]
        
        return True, domain_value
    
    @staticmethod
    def fix_type_ontology(ontology):
        """Fix @type:
        - owl:NamedIndividual → owl:Ontology
        - m0:Poclet → owl:Ontology
        - ["owl:Ontology", "m1:Poclet", ...] → "owl:Ontology" (remove forbidden types)
        """
        if "@type" not in ontology:
            return False
        t = ontology["@type"]
        FORBIDDEN = {"owl:NamedIndividual", "m0:Poclet", "m1:Poclet",
                     "m1:core:Poclet", "m3:Poclet"}
        if isinstance(t, list):
            cleaned = [x for x in t if x not in FORBIDDEN]
            if "owl:Ontology" not in cleaned:
                cleaned.insert(0, "owl:Ontology")
            # Flatten to string if only one element
            result = cleaned[0] if len(cleaned) == 1 else cleaned
            if result != t:
                ontology["@type"] = result
                return True
        elif t in FORBIDDEN:
            ontology["@type"] = "owl:Ontology"
            return True
        return False
    
    @staticmethod
    def fix_version_property(ontology):
        """m0:version → owl:versionInfo"""
        if "m0:version" in ontology:
            ontology["owl:versionInfo"] = ontology.pop("m0:version")
            return True
        return False
    
    @staticmethod
    def remove_ontology_category(ontology):
        """Remove obsolete m2:ontologyCategory and m3:ontologyCategory"""
        modified = False
        
        if "m2:ontologyCategory" in ontology:
            del ontology["m2:ontologyCategory"]
            modified = True
        
        if "m3:ontologyCategory" in ontology:
            del ontology["m3:ontologyCategory"]
            modified = True
        
        return modified
    
    @staticmethod
    def reorder_ontology_properties(ontology):
        """Reorder ontology properties with m3:ontologyType in early position.
        
        Preferred order:
        1. @id
        2. @type
        3. owl:imports (if present)
        4. m3:ontologyType (right after owl:imports, or after @type if no imports)
        5. rdfs:label
        6. rdfs:comment
        7. dcterms:creator
        8. dcterms:created
        9. owl:versionInfo
        10. m1:domain
        11. ... rest in original order
        """
        # Define base preferred order
        base_order = ["@id", "@type"]
        
        # If owl:imports exists, add it and m3:ontologyType after it
        # If owl:imports doesn't exist, add m3:ontologyType directly after @type
        if "owl:imports" in ontology:
            preferred_order = base_order + ["owl:imports", "m3:ontologyType"]
        else:
            preferred_order = base_order + ["m3:ontologyType"]
        
        # Add remaining standard properties
        preferred_order.extend([
            "rdfs:label",
            "rdfs:comment",
            "dcterms:creator",
            "dcterms:created",
            "owl:versionInfo",
            "m1:domain",
        ])
        
        # Create reordered dict
        reordered = {}
        
        # Add properties in preferred order (if they exist)
        for key in preferred_order:
            if key in ontology:
                reordered[key] = ontology[key]
        
        # Add remaining properties in their original order
        for key, value in ontology.items():
            if key not in reordered:
                reordered[key] = value
        
        # Replace ontology dict content
        ontology.clear()
        ontology.update(reordered)
        
        return True  # Always return True since we always reorder
    
    @staticmethod
    def fix_ontology_type_namespace(ontology):
        """m2:ontologyType → m3:ontologyType"""
        if "m2:ontologyType" in ontology:
            ontology["m3:ontologyType"] = ontology.pop("m2:ontologyType")
            return True
        return False
    
    @staticmethod
    def fix_domain_namespace(ontology):
        """m0:domain → m1:domain"""
        if "m0:domain" in ontology:
            ontology["m1:domain"] = ontology.pop("m0:domain")
            return True
        return False
    
    @staticmethod
    def fix_title_to_label(ontology):
        """dcterms:title → rdfs:label (if rdfs:label absent)"""
        if "dcterms:title" in ontology and "rdfs:label" not in ontology:
            ontology["rdfs:label"] = ontology.pop("dcterms:title")
            return True
        elif "dcterms:title" in ontology and "rdfs:label" in ontology:
            # Both present - remove dcterms:title (keep rdfs:label)
            del ontology["dcterms:title"]
            return True
        return False
    
    @staticmethod
    def fix_description_to_comment(ontology):
        """dcterms:description → rdfs:comment (if rdfs:comment absent)"""
        if "dcterms:description" in ontology and "rdfs:comment" not in ontology:
            ontology["rdfs:comment"] = ontology.pop("dcterms:description")
            return True
        elif "dcterms:description" in ontology and "rdfs:comment" in ontology:
            # Both present - remove dcterms:description
            del ontology["dcterms:description"]
            return True
        return False
    
    @staticmethod
    def add_ontology_type(ontology, ontology_type_value="m3:Poclet"):
        """Add m3:ontologyType if absent. Supports Poclet, SymbolicSystemGrammar, SystemicFramework"""
        if "m3:ontologyType" not in ontology:
            # Clean up incorrect @type values (m1:Poclet should not be in @type)
            if "@type" in ontology:
                if isinstance(ontology["@type"], list):
                    # Remove m1:Poclet from list if present
                    ontology["@type"] = [t for t in ontology["@type"] if t != "m1:Poclet"]
                elif ontology["@type"] == "m1:Poclet":
                    # Replace single m1:Poclet with owl:Ontology
                    ontology["@type"] = "owl:Ontology"
            
            # Check for incorrect rdf:type variants
            if "rdf:type" in ontology:
                rdf_type_value = ontology["rdf:type"]
                
                # Case 1: String value "m3:Poclet" (or other types)
                if rdf_type_value in ["m3:Poclet", "m3:SymbolicSystemGrammar", "m3:SystemicFramework"]:
                    del ontology["rdf:type"]
                
                # Case 2: Object value {"@id": "m3:Poclet"} (or other types)
                elif isinstance(rdf_type_value, dict) and rdf_type_value.get("@id") in ["m3:Poclet", "m3:SymbolicSystemGrammar", "m3:SystemicFramework"]:
                    del ontology["rdf:type"]
                
                # Case 3: Any other rdf:type pointing to a Poclet-like IRI
                elif isinstance(rdf_type_value, dict) and "@id" in rdf_type_value:
                    if any(t in rdf_type_value["@id"] for t in ["Poclet", "SymbolicSystemGrammar", "SystemicFramework"]):
                        del ontology["rdf:type"]
            
            # Add correct m3:ontologyType
            ontology["m3:ontologyType"] = {"@id": ontology_type_value}
            return True
        return False
    
    @staticmethod
    def add_domain(ontology):
        """Add m1:domain if absent, extracting from m1:pocletCharacteristics.domain"""
        if "m1:domain" not in ontology and "m0:domain" not in ontology:
            # Try to extract from m1:pocletCharacteristics.domain
            if "m1:pocletCharacteristics" in ontology:
                chars = ontology["m1:pocletCharacteristics"]
                if isinstance(chars, dict) and "domain" in chars:
                    domain_str = chars["domain"]
                    # Parse domain string (e.g., "Immunology / Biology" → "Biology")
                    if "/" in domain_str:
                        # Take the most specific domain (last part)
                        domain = domain_str.split("/")[-1].strip()
                    else:
                        domain = domain_str.strip()
                    
                    ontology["m1:domain"] = domain
                    return True
            
            # If no domain found in characteristics, cannot add automatically
            # This will still fail SHACL but user will see the error
            return False
        return False
    
    @staticmethod
    def fix_base_url(context):
        """Fix @base URL: aladas-org/cryptocalc → Echopraxium/tscg"""
        if "@base" in context:
            base = context["@base"]
            if "aladas-org/cryptocalc" in base:
                context["@base"] = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
                return True
        return False
    
    @staticmethod
    def add_missing_namespaces(context):
        """Add m1: and m3: namespaces to @context if absent (with ABSOLUTE URLs)"""
        modified = False
        
        # Add m1: if absent (ABSOLUTE URL)
        if "m1" not in context:
            context["m1"] = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#"
            modified = True
        
        # Add m3: if absent (ABSOLUTE URL)
        if "m3" not in context:
            context["m3"] = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#"
            modified = True
        
        return modified
    
    @staticmethod
    def fix_relative_namespaces(context):
        """Convert relative namespace URLs to absolute URLs for pyshacl compatibility"""
        modified = False
        
        # Mapping of relative → absolute URLs
        # All known relative → absolute mappings (including already-renamed GenesisGrammar)
        namespace_mappings = {
            "m1": [
                ("M1_CoreConcepts.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#"),
            ],
            "m3": [
                ("M3_GenesisSpace.jsonld#",   "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#"),
                ("M3_GenesisGrammar.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#"),
            ],
            "m2": [
                ("M2_GenericConcepts.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#"),
            ],
        }

        for ns_key, mappings in namespace_mappings.items():
            if ns_key in context:
                for relative_url, absolute_url in mappings:
                    if context[ns_key] == relative_url:
                        context[ns_key] = absolute_url
                        modified = True
                        break
        
        return modified
    
    @staticmethod
    def fix_genesis_space_to_grammar(context):
        """Migrate M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld in @context. (v3.0.0)"""
        modified = False
        OLD_FULL = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#"
        NEW_FULL = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#"
        OLD_REL  = "M3_GenesisSpace.jsonld#"
        NEW_REL  = "M3_GenesisGrammar.jsonld#"
        for key in list(context.keys()):
            val = context[key]
            if not isinstance(val, str): continue
            if OLD_FULL in val:
                context[key] = val.replace(OLD_FULL, NEW_FULL)
                modified = True
            elif OLD_REL in val and not val.startswith("http"):
                context[key] = val.replace(OLD_REL, NEW_REL)
                modified = True
        return modified

    @staticmethod
    def fix_genesis_space_in_body(data):
        """Migrate M3_GenesisSpace.jsonld references in the full @graph body. (v3.0.0)
        Uses full JSON serialization for safety — covers all nested occurrences.
        """
        OLD = "M3_GenesisSpace.jsonld"
        NEW = "M3_GenesisGrammar.jsonld"
        serialized = json.dumps(data, ensure_ascii=False)
        if OLD in serialized:
            return True, json.loads(serialized.replace(OLD, NEW))
        return False, data

    @staticmethod
    def add_base_if_missing(context):
        """Add canonical @base to @context if absent or incorrect. (v3.0.0)
        Required for pyoxigraph/TscgOntologyAPIServer: without @base, relative @id
        values resolve to file:///local/path instead of the canonical GitHub IRI.
        """
        BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
        if "@base" not in context:
            context["@base"] = BASE
            return True
        current = context.get("@base", "")
        if current and "raw.githubusercontent.com/Echopraxium/tscg" not in current:
            context["@base"] = BASE
            return True
        return False

    @staticmethod
    def fix_changelog_format(ontology):
        """Convert m2:changelog from object to array format"""
        if "m2:changelog" in ontology and isinstance(ontology["m2:changelog"], dict):
            # Convert object format to array
            changelog_array = []
            for key, value in ontology["m2:changelog"].items():
                if isinstance(value, dict):
                    entry = {
                        "version": key.replace("v", "").replace("_", "."),
                        "date": value.get("date", ""),
                        "changes": value.get("description", value.get("changes", ""))
                    }
                    changelog_array.append(entry)
            
            # Keep only 3 most recent
            ontology["m2:changelog"] = changelog_array[:3]
            return True
        return False

# ============================================================================
# MIGRATION ENGINE (CORRECTED)
# ============================================================================

class InstanceMigrator:
    """Handles migration of a single instance (JSON-LD + README + HTML)."""
    
    def __init__(self, instance_name, instance_type="poclet"):
        self.instance_name = instance_name
        self.instance_type = instance_type
        self.type_config = INSTANCE_TYPES[instance_type]
        self.instance_dir = self.type_config["dir"] / instance_name
        self.modifications = []
        self.errors = []
        
        # File paths
        file_prefix = self.type_config["prefix"]
        self.jsonld_path = self.instance_dir / f"{file_prefix}{instance_name}.jsonld"
        self.readme_path = self.instance_dir / f"{file_prefix}{instance_name}_README.md"
        self.html_path = self.instance_dir / f"{file_prefix}{instance_name}.html"
        self.html_static_path = self.instance_dir / "static" / f"{file_prefix}{instance_name}.html"
        
        # Determine actual HTML location
        if self.html_static_path.exists():
            self.html_path = self.html_static_path
        elif not self.html_path.exists():
            self.html_path = None
    
    def backup_files(self):
        """Create backup of all instance files (including federated instances)."""
        backup_instance_dir = BACKUP_DIR / self.instance_name
        backup_instance_dir.mkdir(parents=True, exist_ok=True)
        
        # DEBUG for NakamotoConsensus
        if self.instance_name == "NakamotoConsensus":
            print(f"\n🔍 DEBUG NakamotoConsensus:")
            print(f"   jsonld_path: {self.jsonld_path}")
            print(f"   exists(): {self.jsonld_path.exists()}")
            print(f"   is_file(): {self.jsonld_path.is_file()}")
            print(f"   absolute(): {self.jsonld_path.absolute()}")
        
        # Backup main files
        if self.jsonld_path.exists():
            shutil.copy2(self.jsonld_path, backup_instance_dir / self.jsonld_path.name)
        if self.readme_path.exists():
            shutil.copy2(self.readme_path, backup_instance_dir / self.readme_path.name)
        if self.html_path and self.html_path.exists():
            shutil.copy2(self.html_path, backup_instance_dir / self.html_path.name)
        
        # Backup federated instances if any
        if self.jsonld_path.exists():
            try:
                with open(self.jsonld_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if "@graph" in data and len(data["@graph"]) > 0:
                    ontology = data["@graph"][0]
                    
                    if "m0:federatedInstances" in ontology:
                        federated_files = ontology["m0:federatedInstances"]
                        
                        if isinstance(federated_files, list):
                            for fed_item in federated_files:
                                # Extract filename from federated instance object
                                fed_filename = None
                                
                                if isinstance(fed_item, str):
                                    fed_filename = fed_item
                                elif isinstance(fed_item, dict) and "@id" in fed_item:
                                    fed_id = fed_item["@id"]
                                    if ":" in fed_id:
                                        fed_id = fed_id.split(":")[-1]
                                    fed_filename = f"M0_{fed_id}.jsonld"
                                elif isinstance(fed_item, dict) and "rdfs:seeAlso" in fed_item:
                                    url = fed_item["rdfs:seeAlso"]
                                    fed_filename = url.split("/")[-1]
                                
                                if fed_filename:
                                    fed_path = self.instance_dir / fed_filename
                                    if fed_path.exists():
                                        shutil.copy2(fed_path, backup_instance_dir / fed_filename)
            except:
                pass  # If we can't parse federated instances, skip backup (main file will still be backed up)
        
        return backup_instance_dir
    
    def apply_transformations_to_data(self, data, filepath_for_logging):
        """Apply all transformations to a JSON-LD data structure.
        
        Args:
            data: Parsed JSON-LD data
            filepath_for_logging: Path for logging purposes
            
        Returns:
            tuple: (success, modifications_list)
        """
        modifications = []
        
        # CRITICAL: All M0 files have @graph structure
        if "@graph" not in data or len(data["@graph"]) == 0:
            return False, ["No @graph array found in JSON-LD"]
        
        # Get the ontology object (first item in @graph)
        ontology = data["@graph"][0]
        context = data.get("@context", {})
        
        # Apply transformations
        rules = TransformationRules()
        
        # Fix @context
        if rules.fix_base_url(context):
            modifications.append("@context: Fixed @base URL (aladas-org → Echopraxium)")

        if rules.add_base_if_missing(context):
            modifications.append("@context: Added missing @base (canonical https://raw.githubusercontent.com/...)")

        if rules.fix_genesis_space_to_grammar(context):
            modifications.append("@context: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld")

        if rules.add_missing_namespaces(context):
            modifications.append("@context: Added missing m1:/m3: namespaces")
        
        if rules.fix_relative_namespaces(context):
            modifications.append("@context: Converted relative URLs to absolute")
        
        # Fix ontology properties
        if rules.fix_type_ontology(ontology):
            modifications.append("JSON-LD: Fixed @type → owl:Ontology")
        
        if rules.fix_version_property(ontology):
            modifications.append("JSON-LD: m0:version → owl:versionInfo")
        
        if rules.remove_ontology_category(ontology):
            modifications.append("JSON-LD: Removed m2/m3:ontologyCategory")
        
        if rules.fix_ontology_type_namespace(ontology):
            modifications.append("JSON-LD: m2:ontologyType → m3:ontologyType")
        
        if rules.fix_domain_namespace(ontology):
            modifications.append("JSON-LD: m0:domain → m1:domain")
        
        if rules.fix_title_to_label(ontology):
            modifications.append("JSON-LD: dcterms:title → rdfs:label")
        
        if rules.fix_description_to_comment(ontology):
            modifications.append("JSON-LD: dcterms:description → rdfs:comment")
        
        if rules.add_ontology_type(ontology, self.type_config["ontology_type"]):
            modifications.append(f"JSON-LD: Added {self.type_config['ontology_type']}")
        
        if rules.add_domain(ontology):
            modifications.append("JSON-LD: Added m1:domain")
        
        if rules.fix_changelog_format(ontology):
            modifications.append("JSON-LD: Converted m2:changelog to array")
        
        # Reorder properties for consistency (m3:ontologyType after owl:imports)
        rules.reorder_ontology_properties(ontology)
        
        return True, modifications
    
    def migrate_single_jsonld_file(self, filepath):
        """Migrate a single JSON-LD file (main or federated).
        
        Args:
            filepath: Path to JSON-LD file
            
        Returns:
            tuple: (success, modifications_list)
        """
        if not filepath.exists():
            return False, [f"JSON-LD not found: {filepath}"]
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            # Fallback: try with cp1252 then re-encode to utf-8
            try:
                with open(filepath, 'r', encoding='cp1252') as f:
                    raw = f.read()
                data = json.loads(raw)
                # Re-write as clean UTF-8 immediately
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write(chr(10))
            except Exception as e2:
                return False, [f"Encoding error in {filepath}: {str(e2)}"]
        except Exception as e:
            return False, [f"Failed to read {filepath}: {str(e)}"]
        
        modifications = []
        
        # STEP 0 (v3.0.0): Full-body replacement of M3_GenesisSpace → M3_GenesisGrammar
        body_changed, data = TransformationRules.fix_genesis_space_in_body(data)
        if body_changed:
            modifications.append("JSON-LD body: M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld")

        # STEP 0b (v3.0.0): Remove stray root-level properties (outside @graph)
        # Some files have m3:ontologyType at root level — invalid, must be in @graph[0]
        root_stray = []
        for key in list(data.keys()):
            if key not in ("@context", "@graph", "@id", "@type"):
                root_stray.append(key)
                del data[key]
        if root_stray:
            modifications.append(f"Removed stray root-level properties: {', '.join(root_stray)}")

        # STEP 1: Migrate m0:domain from @graph[1+] to @graph[0] as m1:domain
        # (Must happen BEFORE other transformations that operate on @graph[0])
        migrated, domain_value = TransformationRules.migrate_domain_from_graph_objects(data)
        if migrated:
            modifications.append(f"JSON-LD: Migrated m0:domain → m1:domain ('{domain_value}' from @graph[1+] to @graph[0])")
        
        # STEP 2: Apply transformations to @graph[0]
        success, trans_mods = self.apply_transformations_to_data(data, filepath)
        
        if not success:
            return False, trans_mods
        
        modifications.extend(trans_mods)
        
        # Write back
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            return False, [f"Failed to write {filepath}: {str(e)}"]
        
        return True, modifications
    
    def migrate_jsonld(self):
        """Apply all transformations to JSON-LD file + federated instances."""
        if not self.jsonld_path.exists():
            self.errors.append(f"JSON-LD not found: {self.jsonld_path}")
            return False
        
        try:
            # First, migrate the main file
            success, modifications = self.migrate_single_jsonld_file(self.jsonld_path)
            
            if not success:
                self.errors.extend(modifications)
                return False
            
            self.modifications.extend(modifications)
            
            # Check for federated instances
            with open(self.jsonld_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            ontology = data["@graph"][0]
            
            if "m0:federatedInstances" in ontology:
                federated_files = ontology["m0:federatedInstances"]
                
                if isinstance(federated_files, list):
                    self.modifications.append(f"Federated: Found {len(federated_files)} sub-instances")
                    
                    for fed_item in federated_files:
                        # Extract filename from federated instance object
                        fed_filename = None
                        
                        # Case 1: Simple string (direct filename)
                        if isinstance(fed_item, str):
                            fed_filename = fed_item
                        
                        # Case 2: Object with @id (e.g., "m0:RGB_Additive" → "M0_RGB_Additive.jsonld")
                        elif isinstance(fed_item, dict) and "@id" in fed_item:
                            fed_id = fed_item["@id"]
                            # Remove namespace prefix (e.g., "m0:RGB_Additive" → "RGB_Additive")
                            if ":" in fed_id:
                                fed_id = fed_id.split(":")[-1]
                            # Construct filename: RGB_Additive → M0_RGB_Additive.jsonld
                            fed_filename = f"M0_{fed_id}.jsonld"
                        
                        # Case 3: Extract from rdfs:seeAlso URL
                        elif isinstance(fed_item, dict) and "rdfs:seeAlso" in fed_item:
                            url = fed_item["rdfs:seeAlso"]
                            fed_filename = url.split("/")[-1]  # Extract filename from URL
                        
                        if not fed_filename:
                            self.errors.append(f"Could not extract filename from federated item: {fed_item}")
                            continue
                        
                        fed_path = self.instance_dir / fed_filename
                        
                        if not fed_path.exists():
                            self.errors.append(f"Federated file not found: {fed_path}")
                            continue
                        
                        # Migrate federated instance
                        fed_success, fed_mods = self.migrate_single_jsonld_file(fed_path)
                        
                        if fed_success:
                            self.modifications.append(f"Federated: {fed_filename} → {len(fed_mods)} changes")
                        else:
                            self.errors.append(f"Federated {fed_filename} failed: {fed_mods}")
                            return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"JSON-LD migration failed: {str(e)}")
            return False
    
    def validate_jsonld(self):
        """Validate JSON-LD with SHACL."""
        try:
            result = subprocess.run(
                [
                    "pyshacl",
                    "-s", str(SHACL_SCHEMA),
                    "-df", "json-ld",
                    str(self.jsonld_path)
                ],
                capture_output=True,
                text=True,
                cwd=str(ONTOLOGY_DIR)
            )
            
            if "Conforms: True" in result.stdout:
                return True, "SHACL validation passed"
            elif result.returncode != 0 and not result.stdout:
                return False, f"pyshacl error (returncode={result.returncode}):\n{result.stderr[:500]}"
            else:
                # Show only first violation message for brevity
                lines = result.stdout.split("\n")
                msgs = [l for l in lines if "Message:" in l or "Constraint Violation" in l]
                summary = "\n".join(msgs[:3]) if msgs else result.stdout[:300]
                return False, f"SHACL validation failed:\n{summary}"
                
        except Exception as e:
            return False, f"SHACL validation error: {str(e)}"
    
    def migrate_readme(self):
        """Migrate README (placeholder - extend if needed)."""
        if not self.readme_path.exists():
            return True  # Not an error if README doesn't exist
        
        # For now, README migration is minimal
        # Extend here if specific README patterns need fixing
        return True
    
    def validate_html(self):
        """Basic HTML validation - check for broken structure."""
        if not self.html_path:
            return True, "No HTML file to validate"
        
        try:
            with open(self.html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Basic checks
            checks = []
            
            # Check for unclosed tags
            if html_content.count('<div>') != html_content.count('</div>'):
                checks.append("WARNING: Mismatched <div> tags")
            
            # Check for basic structure
            if '<html' not in html_content or '</html>' not in html_content:
                checks.append("ERROR: Missing <html> tags")
            
            if checks:
                return False, "\n".join(checks)
            
            return True, "HTML structure OK"
            
        except Exception as e:
            return False, f"HTML validation error: {str(e)}"
    
    def dry_run(self):
        """Simulate migration — read and analyse without writing any file."""
        if not self.jsonld_path.exists():
            print(f"  ⚠ {self.instance_name}: JSON-LD not found ({self.jsonld_path})")
            return False

        try:
            with open(self.jsonld_path, 'r', encoding='utf-8') as f:
                import copy
                data = copy.deepcopy(json.load(f))
        except Exception as e:
            print(f"  ✗ {self.instance_name}: read error — {e}")
            return False

        # Run STEP 0
        body_changed, data2 = TransformationRules.fix_genesis_space_in_body(data)

        # Run context + graph[0] transformations on a deep copy
        context  = data2.get("@context", {})
        ontology = data2.get("@graph", [{}])[0] if "@graph" in data2 else {}
        rules    = TransformationRules()
        mods = []

        if rules.fix_base_url(context):           mods.append("@context: Fixed @base URL")
        if rules.add_base_if_missing(context):    mods.append("@context: Added missing @base")
        if rules.fix_genesis_space_to_grammar(context): mods.append("@context: GenesisSpace → GenesisGrammar")
        if rules.add_missing_namespaces(context): mods.append("@context: Added missing namespaces")
        if rules.fix_relative_namespaces(context):mods.append("@context: Relative → absolute URLs")
        if rules.fix_type_ontology(ontology):     mods.append("@type → owl:Ontology")
        if rules.fix_version_property(ontology):  mods.append("m0:version → owl:versionInfo")
        if rules.remove_ontology_category(ontology): mods.append("Removed ontologyCategory")
        if rules.fix_ontology_type_namespace(ontology): mods.append("m2:ontologyType → m3:ontologyType")
        if rules.fix_domain_namespace(ontology):  mods.append("m0:domain → m1:domain")
        if rules.fix_title_to_label(ontology):    mods.append("dcterms:title → rdfs:label")
        if rules.fix_description_to_comment(ontology): mods.append("dcterms:description → rdfs:comment")
        if rules.add_ontology_type(ontology, self.type_config["ontology_type"]): mods.append(f"Added {self.type_config['ontology_type']}")
        if rules.fix_changelog_format(ontology):  mods.append("changelog → array format")
        if body_changed: mods.insert(0, "JSON-LD body: GenesisSpace → GenesisGrammar")

        if mods:
            print(f"  🔧 {self.instance_name}: {len(mods)} change(s) would be applied:")
            for m in mods:
                print(f"     • {m}")
        else:
            print(f"  ✅ {self.instance_name}: already compliant — no changes needed")

        self.modifications = mods
        return True

    def migrate(self):
        """Execute full migration pipeline with checkpoints."""
        print(f"\n{'='*70}")
        print(f"MIGRATING: {self.instance_name}")
        print(f"{'='*70}")
        
        # Checkpoint 1: Backup
        print("\n📦 Checkpoint 1: Creating backup...")
        backup_dir = self.backup_files()
        print(f"   ✓ Backup created: {backup_dir}")
        
        # Checkpoint 2: Migrate JSON-LD
        print("\n🔧 Checkpoint 2: Migrating JSON-LD...")
        if not self.migrate_jsonld():
            print(f"   ❌ Migration failed: {self.errors}")
            return False
        
        if self.modifications:
            for mod in self.modifications:
                print(f"   • {mod}")
        else:
            print("   ℹ️  No modifications needed")
        
        # Checkpoint 3: Validate JSON-LD
        print("\n✅ Checkpoint 3: Validating JSON-LD with SHACL...")
        valid, message = self.validate_jsonld()
        if not valid:
            print(f"   ❌ {message}")
            self.errors.append(f"SHACL: {message}")
            print("\n⚠️  ROLLBACK: Restoring from backup...")
            self.rollback(backup_dir)
            return False
        print(f"   ✓ {message}")
        
        # Checkpoint 4: Migrate README (if exists)
        print("\n📝 Checkpoint 4: Migrating README...")
        if not self.migrate_readme():
            print(f"   ❌ README migration failed")
        else:
            print("   ✓ README processed")
        
        # Checkpoint 5: Validate HTML (if exists)
        if self.html_path:
            print("\n🌐 Checkpoint 5: Validating HTML structure...")
            valid, message = self.validate_html()
            if not valid:
                print(f"   ⚠️  {message}")
                print("   ⚠️  Review HTML manually before testing simulation")
            else:
                print(f"   ✓ {message}")
        
        print(f"\n{'='*70}")
        print(f"✅ MIGRATION COMPLETE: {self.instance_name}")
        print(f"{'='*70}")
        
        return True
    
    def rollback(self, backup_dir):
        """Restore files from backup."""
        for backup_file in backup_dir.glob("*"):
            target = self.instance_dir / backup_file.name
            if backup_file.name.startswith("M0_"):
                # Check if original was in static/ subdirectory
                if "static" in str(self.html_path):
                    target = self.instance_dir / "static" / backup_file.name
            shutil.copy2(backup_file, target)
        print(f"   ✓ Rollback complete")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def _has_jsonld(base_dir, name, instance_type):
    """Check if the expected JSON-LD file exists for an instance."""
    type_dirs = {
        "poclet":          POCLETS_DIR,
        "symbolic_grammar": SYMBOLIC_GRAMMARS_DIR,
        "systemic_framework": SYSTEMIC_FRAMEWORKS_DIR,
        "tscg_tool":       REPO_ROOT / "instances" / "tscg-tools",
    }
    base = type_dirs.get(instance_type, base_dir)
    jsonld = base / name / f"M0_{name}.jsonld"
    return jsonld.exists()


def get_easy_instances():
    """Get list of instances suitable for automated migration.
    Returns list of tuples: (instance_name, instance_type)
    Automatically excludes directories without a M0_<Name>.jsonld file.
    """
    instances = []

    def _collect(base_dir, instance_type):
        if not base_dir.exists():
            return
        for d in sorted(base_dir.iterdir()):
            if not d.is_dir() or d.name.startswith('_'):
                continue
            name = d.name
            if name in MANUAL_INSTANCES or name in COMPLIANT_INSTANCES:
                continue
            if not _has_jsonld(base_dir, name, instance_type):
                print(f"  ⚠ Skipping {name} ({instance_type}): no M0_{name}.jsonld found")
                continue
            instances.append((name, instance_type))

    _collect(POCLETS_DIR,            "poclet")
    _collect(SYMBOLIC_GRAMMARS_DIR,  "symbolic_grammar")
    _collect(SYSTEMIC_FRAMEWORKS_DIR, "systemic_framework")
    _collect(REPO_ROOT / "instances" / "tscg-tools", "tscg_tool")

    return instances

def generate_report(results):
    """Generate migration summary report."""
    report_path = BACKUP_DIR / "MIGRATION_REPORT.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# TSCG Automated Migration Report (v3.0.0 - GenesisGrammar + @base)\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Backup Location:** {BACKUP_DIR}\n\n")
        
        f.write("## Summary\n\n")
        success = sum(1 for r in results.values() if r['status'] == 'success')
        failed = sum(1 for r in results.values() if r['status'] == 'failed')
        
        f.write(f"- ✅ **Successful:** {success}\n")
        f.write(f"- ❌ **Failed:** {failed}\n")
        f.write(f"- 📊 **Total:** {len(results)}\n\n")
        
        f.write("## Detailed Results\n\n")
        for instance, result in results.items():
            instance_type = result.get('type', 'unknown')
            f.write(f"### {instance} ({instance_type})\n")
            f.write(f"**Status:** {'✅ Success' if result['status'] == 'success' else '❌ Failed'}\n\n")
            
            if result['modifications']:
                f.write("**Modifications:**\n")
                for mod in result['modifications']:
                    f.write(f"- {mod}\n")
                f.write("\n")
            
            if result['errors']:
                f.write("**Errors:**\n")
                for err in result['errors']:
                    f.write(f"- {err}\n")
                f.write("\n")
        
        f.write("## Fixes Applied in v3.0.0\n\n")
        f.write("1. ✅ Added missing @base in @context (required for TscgOntologyAPIServer/pyoxigraph)\n")
        f.write("2. ✅ Migrated M3_GenesisSpace.jsonld → M3_GenesisGrammar.jsonld throughout\n")
        f.write("3. ✅ All v2.7.0 features maintained (multi-type support, domain migration)\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. Review this report\n")
        f.write("2. Test HTML simulations manually (see TEST_CHECKLIST.md)\n")
        f.write("3. If issues found, restore from backup\n")
        f.write("4. Manually add m1:domain values for instances without domain\n")
    
    print(f"\n📄 Report generated: {report_path}")
    return report_path

def generate_test_checklist(migrated_instances):
    """Generate HTML testing checklist.
    
    Args:
        migrated_instances: List of (instance_name, instance_type) tuples
    """
    checklist_path = BACKUP_DIR / "TEST_CHECKLIST.md"
    
    # Filter instances that have HTML files
    html_instances = []
    for instance_name, instance_type in migrated_instances:
        migrator = InstanceMigrator(instance_name, instance_type)
        if migrator.html_path and migrator.html_path.exists():
            html_instances.append((instance_name, instance_type))
    
    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write("# HTML Simulation Testing Checklist\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Testing Instructions\n\n")
        f.write("For each instance below, open the HTML file in your browser and verify:\n\n")
        f.write("1. ✅ Page loads without errors\n")
        f.write("2. ✅ No JavaScript console errors\n")
        f.write("3. ✅ All UI elements visible (sidebar tabs, controls, canvas)\n")
        f.write("4. ✅ ASFID/REVOI scores display correctly\n")
        f.write("5. ✅ Interactive features work (sliders, buttons, animations)\n")
        f.write("6. ✅ Visual simulation renders correctly\n\n")
        
        f.write("## Instances to Test\n\n")
        for i, (instance_name, instance_type) in enumerate(html_instances, 1):
            migrator = InstanceMigrator(instance_name, instance_type)
            f.write(f"### {i}. {instance_name} ({instance_type})\n\n")
            f.write(f"**File:** `{migrator.html_path.relative_to(REPO_ROOT)}`\n\n")
            f.write("**Test results:**\n")
            f.write("- [ ] Page loads\n")
            f.write("- [ ] No JS errors\n")
            f.write("- [ ] UI complete\n")
            f.write("- [ ] Scores OK\n")
            f.write("- [ ] Interactive OK\n")
            f.write("- [ ] Simulation OK\n\n")
            f.write("**Notes:** _[Add any issues found]_\n\n")
            f.write("---\n\n")
    
    print(f"📋 Test checklist generated: {checklist_path}")
    return checklist_path

def main():
    """Main execution flow."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TSCG Automated Migration v3.0.0 - GenesisGrammar + @base migration"
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue migration even if errors occur (default: stop on first error)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate migration without modifying any file — shows what would be changed"
    )
    args = parser.parse_args()
    
    print("="*70)
    print("TSCG AUTOMATED MIGRATION v3.0.0 - GenesisGrammar + @base migration")
    print("="*70)
    
    # Get instances to migrate
    easy_instances = get_easy_instances()
    
    print(f"\n📊 Found {len(easy_instances)} instances for automated migration")
    print(f"   Excluding {len(MANUAL_INSTANCES)} manual instances: {', '.join(MANUAL_INSTANCES)}")
    print(f"   Excluding {len(COMPLIANT_INSTANCES)} compliant instances: {', '.join(COMPLIANT_INSTANCES)}")
    
    # Confirm
    if args.dry_run:
        print(f"\n🔍 DRY-RUN MODE — no files will be modified")
        print(f"   Simulating migration of {len(easy_instances)} instances...")
    else:
        print(f"\n⚠️  This will modify {len(easy_instances)} instances.")
        print(f"   Backups will be created in: {BACKUP_DIR}")

    if args.continue_on_error:
        print(f"   ⚠️  MODE: Continue on error (--continue-on-error)")
    else:
        print(f"   🛡️  MODE: Stop on first error (default)")

    if not args.dry_run:
        response = input("\nProceed? [y/N]: ")
        if response.lower() != 'y':
            print("❌ Migration cancelled")
            return 1
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Migrate each instance
    results = {}
    for instance_name, instance_type in easy_instances:
        migrator = InstanceMigrator(instance_name, instance_type)
        if args.dry_run:
            success = migrator.dry_run()
        else:
            success = migrator.migrate()
        
        results[instance_name] = {
            'status': 'success' if success else 'failed',
            'type': instance_type,
            'modifications': migrator.modifications,
            'errors': migrator.errors
        }
        
        # Stop on error (unless --continue-on-error flag set)
        if not success and not args.continue_on_error:
            print(f"\n❌ MIGRATION STOPPED: {instance_name} ({instance_type}) failed")
            print(f"   Errors: {migrator.errors}")
            print(f"\n💡 To continue despite errors, use: --continue-on-error")
            break
    
    # Generate reports
    print("\n" + "="*70)
    if args.dry_run:
        print("DRY-RUN SUMMARY")
    else:
        print("GENERATING REPORTS")
    print("="*70)

    if args.dry_run:
        report_path = None
        checklist_path = None
        print("\n(No files written — dry-run mode)")
    else:
        report_path = generate_report(results)
        checklist_path = generate_test_checklist(easy_instances)
    
    # Summary
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("="*70)
    if args.dry_run:
        print(f"\n🔍 Would migrate: {success_count}/{len(easy_instances)} instances")
        print(f"   (no files written — use without --dry-run to apply)")
    else:
        print(f"\n✅ Successfully migrated: {success_count}/{len(easy_instances)} instances")
        print(f"\n📁 Backups: {BACKUP_DIR}")
        print(f"📄 Report: {report_path}")
        print(f"📋 Test checklist: {checklist_path}")
    
    print("\n🧪 NEXT STEPS:")
    print("1. Review the migration report")
    print("2. Test HTML simulations using the checklist")
    print("3. If issues found, use backups to rollback")
    print("4. Manually add m1:domain values where needed")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
