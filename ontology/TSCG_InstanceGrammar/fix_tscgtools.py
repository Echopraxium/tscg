import json
from pathlib import Path

REPO_ROOT = Path("E:/_00_Michel/_00_Lab/_00_GitHub/tscg")
BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
TOOLS = [
    "TscgOntologyAPIServer",
    "TscgOntologyExplorer", 
    "TscgPocletGenerator",
    "TscgPocletMiner",
]

for tool in TOOLS:
    path = REPO_ROOT / "instances" / "tscg-tools" / tool / f"M0_{tool}.jsonld"
    print(f"\n{tool}:")
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    ctx = data.get('@context', {})
    modified = False
    
    # Fix relative namespaces
    fixes = {
        'm3': ('M3_GenesisGrammar.jsonld#', f'{BASE}M3_GenesisGrammar.jsonld#'),
        'm2': ('M2_GenericConcepts.jsonld#', f'{BASE}M2_GenericConcepts.jsonld#'),
        'm1': ('M1_CoreConcepts.jsonld#', f'{BASE}M1_CoreConcepts.jsonld#'),
    }
    
    for prefix, (rel, absolute) in fixes.items():
        if ctx.get(prefix) == rel:
            ctx[prefix] = absolute
            print(f"  Fixed {prefix}: {rel} → absolute")
            modified = True
    
    # Add @base if missing
    if '@base' not in ctx:
        ctx['@base'] = BASE
        print(f"  Added @base")
        modified = True
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f"  ✅ Saved")
    else:
        print(f"  ✓ Already correct")

print("\nDone")
