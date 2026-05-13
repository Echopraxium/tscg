#!/usr/bin/env python3
"""
TSCG Automated Realignment Script - Easy Instances (CORRECTED)
Author: Echopraxium with the collaboration of Claude AI
Date: 2026-04-19
Version: 2.5.0 - m0:domain cross-object migration (@graph[1+] → @graph[0])

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
INSTANCES_DIR = REPO_ROOT / "instances/poclets"
ONTOLOGY_DIR = REPO_ROOT / "ontology"
BACKUP_DIR = REPO_ROOT / "migration_backups" / datetime.now().strftime("%Y%m%d_%H%M%S")
SHACL_SCHEMA = ONTOLOGY_DIR / "TSCG_Grammar/M0_Instances_Schema.shacl.ttl"

# Instances to EXCLUDE (require manual intervention)
MANUAL_INSTANCES = {
    "BloodPressureControl",  # 50+ tscg:* namespace violations
    "ButterflyMetamorphosis",  # 10+ custom classes to reclassify
    "CellSignalingModes",  # Inline components restructuring
    "VSM_Metaconcepts",  # ORIVE → REVOI terminology change
}

# Instances already fully compliant (skip migration)
COMPLIANT_INSTANCES = {
    "AdaptiveImmuneResponse",  # 100% compliant reference
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
        """@type: owl:NamedIndividual → owl:Ontology"""
        if "@type" in ontology:
            if ontology["@type"] == "owl:NamedIndividual":
                ontology["@type"] = "owl:Ontology"
                return True
            elif ontology["@type"] == "m0:Poclet":
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
    def add_ontology_type(ontology):
        """Add m3:ontologyType: {"@id": "m3:Poclet"} if absent"""
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
                
                # Case 1: String value "m3:Poclet"
                if rdf_type_value == "m3:Poclet":
                    del ontology["rdf:type"]
                
                # Case 2: Object value {"@id": "m3:Poclet"}
                elif isinstance(rdf_type_value, dict) and rdf_type_value.get("@id") == "m3:Poclet":
                    del ontology["rdf:type"]
                
                # Case 3: Any other rdf:type pointing to a Poclet-like IRI
                elif isinstance(rdf_type_value, dict) and "@id" in rdf_type_value:
                    if "Poclet" in rdf_type_value["@id"]:
                        del ontology["rdf:type"]
            
            # Add correct m3:ontologyType
            ontology["m3:ontologyType"] = {"@id": "m3:Poclet"}
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
            context["m3"] = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#"
            modified = True
        
        return modified
    
    @staticmethod
    def fix_relative_namespaces(context):
        """Convert relative namespace URLs to absolute URLs for pyshacl compatibility"""
        modified = False
        
        # Mapping of relative → absolute URLs
        namespace_mappings = {
            "m1": ("M1_CoreConcepts.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#"),
            "m3": ("M3_GenesisSpace.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisSpace.jsonld#"),
            "m2": ("M2_GenericConcepts.jsonld#", "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#"),
        }
        
        for ns_key, (relative_url, absolute_url) in namespace_mappings.items():
            if ns_key in context and context[ns_key] == relative_url:
                context[ns_key] = absolute_url
                modified = True
        
        return modified
    
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
    
    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.instance_dir = INSTANCES_DIR / instance_name
        self.modifications = []
        self.errors = []
        
        # File paths
        self.jsonld_path = self.instance_dir / f"M0_{instance_name}.jsonld"
        self.readme_path = self.instance_dir / f"M0_{instance_name}_README.md"
        self.html_path = self.instance_dir / f"M0_{instance_name}.html"
        self.html_static_path = self.instance_dir / "static" / f"M0_{instance_name}.html"
        
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
            modifications.append("@context: Fixed @base URL")
        
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
        
        if rules.add_ontology_type(ontology):
            modifications.append("JSON-LD: Added m3:ontologyType")
        
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
        except Exception as e:
            return False, [f"Failed to read {filepath}: {str(e)}"]
        
        modifications = []
        
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
            else:
                return False, f"SHACL validation failed:\n{result.stdout}"
                
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

def get_easy_instances():
    """Get list of instances suitable for automated migration."""
    all_instances = [d.name for d in INSTANCES_DIR.iterdir() if d.is_dir()]
    
    easy_instances = [
        name for name in all_instances 
        if name not in MANUAL_INSTANCES and name not in COMPLIANT_INSTANCES
    ]
    
    return easy_instances

def generate_report(results):
    """Generate migration summary report."""
    report_path = BACKUP_DIR / "MIGRATION_REPORT.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# TSCG Automated Migration Report (v2.0 - CORRECTED)\n\n")
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
            f.write(f"### {instance}\n")
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
        
        f.write("## Fixes Applied in v2.0\n\n")
        f.write("1. ✅ Modifications now target @graph[0] (ontology level)\n")
        f.write("2. ✅ Added m2:ontologyType → m3:ontologyType rename\n")
        f.write("3. ✅ Added m0:domain → m1:domain rename\n")
        f.write("4. ✅ All transformations working at correct JSON level\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. Review this report\n")
        f.write("2. Test HTML simulations manually (see TEST_CHECKLIST.md)\n")
        f.write("3. If issues found, restore from backup\n")
        f.write("4. Manually add m1:domain values for instances without domain\n")
    
    print(f"\n📄 Report generated: {report_path}")
    return report_path

def generate_test_checklist(migrated_instances):
    """Generate HTML testing checklist."""
    checklist_path = BACKUP_DIR / "TEST_CHECKLIST.md"
    
    # Filter instances that have HTML files
    html_instances = []
    for instance in migrated_instances:
        migrator = InstanceMigrator(instance)
        if migrator.html_path and migrator.html_path.exists():
            html_instances.append(instance)
    
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
        for i, instance in enumerate(html_instances, 1):
            migrator = InstanceMigrator(instance)
            f.write(f"### {i}. {instance}\n\n")
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
        description="TSCG Automated Migration v2.5.0"
    )
    parser.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Continue migration even if errors occur (default: stop on first error)"
    )
    args = parser.parse_args()
    
    print("="*70)
    print("TSCG AUTOMATED MIGRATION v2.5.0 - @graph cross-object migration")
    print("="*70)
    
    # Get instances to migrate
    easy_instances = get_easy_instances()
    
    print(f"\n📊 Found {len(easy_instances)} instances for automated migration")
    print(f"   Excluding {len(MANUAL_INSTANCES)} manual instances: {', '.join(MANUAL_INSTANCES)}")
    print(f"   Excluding {len(COMPLIANT_INSTANCES)} compliant instances: {', '.join(COMPLIANT_INSTANCES)}")
    
    # Confirm
    print(f"\n⚠️  This will modify {len(easy_instances)} instances.")
    print(f"   Backups will be created in: {BACKUP_DIR}")
    
    if args.continue_on_error:
        print(f"   ⚠️  MODE: Continue on error (--continue-on-error)")
    else:
        print(f"   🛡️  MODE: Stop on first error (default)")
    
    response = input("\nProceed? [y/N]: ")
    if response.lower() != 'y':
        print("❌ Migration cancelled")
        return 1
    
    # Create backup directory
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Migrate each instance
    results = {}
    for instance in easy_instances:
        migrator = InstanceMigrator(instance)
        success = migrator.migrate()
        
        results[instance] = {
            'status': 'success' if success else 'failed',
            'modifications': migrator.modifications,
            'errors': migrator.errors
        }
        
        # Stop on error (unless --continue-on-error flag set)
        if not success and not args.continue_on_error:
            print(f"\n❌ MIGRATION STOPPED: {instance} failed")
            print(f"   Errors: {migrator.errors}")
            print(f"\n💡 To continue despite errors, use: --continue-on-error")
            break
    
    # Generate reports
    print("\n" + "="*70)
    print("GENERATING REPORTS")
    print("="*70)
    
    report_path = generate_report(results)
    checklist_path = generate_test_checklist(easy_instances)
    
    # Summary
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    
    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("="*70)
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
