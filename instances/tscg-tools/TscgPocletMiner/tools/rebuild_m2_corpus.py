#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_m2_corpus.py — TSCG M2 GenericConcepts Corpus Builder
Author: Echopraxium with the collaboration of Claude AI
v1.0.0

Reads M2_GenericConcepts.jsonld and writes m2_concepts_corpus.json
consumed by rag_engine.js for semantic embedding.

Each output entry:
  {
    "id":      "Composition",
    "label":   "Composition (Composition/Decomposition)",
    "formula": "S ⊗ I ⊗ A",
    "family":  "Structural",
    "text":    "<rich text for embedding>"
  }

Usage:
  python rebuild_m2_corpus.py                        # auto-detect repo root
  python rebuild_m2_corpus.py --repo /path/to/tscg
  python rebuild_m2_corpus.py --out /path/to/m2_concepts_corpus.json
  python rebuild_m2_corpus.py --verbose
"""

import os
import sys
import json
import re
import argparse
import hashlib
import datetime
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ─── Repo detection ───────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).resolve().parent

def find_repo_root(start: Path) -> Optional[Path]:
    """Walk up from start looking for M2_GenericConcepts.jsonld or ontology/."""
    for p in [start, *start.parents]:
        if (p / "ontology" / "M2_GenericConcepts.jsonld").exists():
            return p
        if (p / "M2_GenericConcepts.jsonld").exists():
            return p
    return None

def find_m2_file(repo_root: Path) -> Optional[Path]:
    candidates = [
        repo_root / "ontology" / "M2_GenericConcepts.jsonld",
        repo_root / "M2_GenericConcepts.jsonld",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

# ─── Field helpers ────────────────────────────────────────────────────────────

def safe_str(v) -> str:
    if isinstance(v, str):  return v
    if isinstance(v, list): return v[0] if v else ''
    if isinstance(v, dict): return v.get('@id', v.get('@value', ''))
    return str(v) if v is not None else ''

def strip_prefix(s: str) -> str:
    """'m2:Composition' → 'Composition', 'm2:Structural' → 'Structural'"""
    if ':' in s:
        return s.split(':')[-1]
    return s

# ─── Entry extraction ─────────────────────────────────────────────────────────

# Classes that are meta-classes, not actual GenericConcepts
_SKIP_IDS = {
    'm2:GenericConcept',
    'm2:GenericConceptCombo',
    'm2:DomainSpecificConcept',
    'm2:M2_GenericConcepts',
    'm2:KnowledgeField',
    'm2:KnowledgeFieldConcept',
    'm2:KnowledgeFieldGenericCombo',
}

def is_generic_concept(entry: dict) -> bool:
    """True if this graph entry is a concrete M2 GenericConcept."""
    eid = entry.get('@id', '')
    if eid in _SKIP_IDS:
        return False
    if not eid.startswith('m2:'):
        return False
    if entry.get('@type') != 'owl:Class':
        return False
    # Must be subclass of m2:GenericConcept (directly or transitively via label)
    parent = safe_str(entry.get('rdfs:subClassOf', ''))
    if 'GenericConcept' not in parent and 'GenericConceptCombo' not in parent:
        return False
    # Must have at least a label
    if not entry.get('rdfs:label'):
        return False
    return True

def extract_concept(entry: dict, verbose: bool = False) -> dict:
    """Extract a structured concept record from a @graph entry."""
    raw_id   = entry['@id']                         # e.g. "m2:Composition"
    concept_id = strip_prefix(raw_id)               # e.g. "Composition"

    label    = safe_str(entry.get('rdfs:label', concept_id))
    comment  = safe_str(entry.get('rdfs:comment', ''))

    # Short name / full name
    short_name = safe_str(entry.get('m2:shortName', '')) or concept_id
    full_name  = safe_str(entry.get('m2:fullName',  '')) or label

    # Tensor formula — prefer Unicode version
    formula = (
        safe_str(entry.get('m2:hasTensorFormula', '')) or
        safe_str(entry.get('m2:tensorFormula', '')) or
        ''
    )
    formula_ascii = safe_str(entry.get('m2:hasTensorFormulaASCII', ''))
    formula_exp   = safe_str(entry.get('m2:hasTensorFormulaExpanded', ''))

    # Family / category
    family_raw = safe_str(entry.get('m2:hasFamily', ''))
    family     = strip_prefix(family_raw) if family_raw else ''

    # Epistemic gap
    gap = entry.get('m2:hasEpistemicGap')
    if isinstance(gap, (int, float)):
        gap = float(gap)
    else:
        gap = None

    # Polarity
    polarity = safe_str(entry.get('m2:hasPolarity', ''))

    # Dominant M3 dimensions
    dom_raw  = entry.get('m2:hasDominantM3', [])
    dominant = [strip_prefix(safe_str(d)) for d in (dom_raw if isinstance(dom_raw, list) else [dom_raw])]

    # Examples (for richer embedding)
    examples_raw = entry.get('m2:hasExample', [])
    if isinstance(examples_raw, str):
        examples_raw = [examples_raw]
    examples = [safe_str(e) for e in examples_raw[:3]]  # limit to 3 for embedding

    # ConceptContract (Triggerable / Observable / Composable / Stateful)
    contract = entry.get('m2:conceptContract', {})
    contract_parts = []
    if isinstance(contract, dict):
        for k, v in contract.items():
            contract_parts.append(f"{strip_prefix(k)}: {safe_str(v)}")

    # Build rich text for RAG embedding
    text_parts = [
        f"GenericConcept: {full_name}",
        f"Short name: {short_name}",
        f"Formula: {formula}" if formula else '',
        f"Formula expanded: {formula_exp}" if formula_exp else '',
        f"Family: {family}" if family else '',
        f"Polarity: {polarity}" if polarity else '',
        f"Dominant dimensions: {', '.join(dominant)}" if dominant else '',
        # First ~300 chars of comment (avoid token overload)
        comment[:300] if comment else '',
        f"Examples: {' | '.join(examples)}" if examples else '',
    ]
    text = '. '.join(p for p in text_parts if p)

    record = {
        'id':        concept_id,
        'label':     label,
        'formula':   formula,
        'family':    family,
        'polarity':  polarity,
        'gap':       gap,
        'dominant':  dominant,
        'text':      text,
    }

    if verbose:
        print(f"  [ok] {concept_id:30s}  formula={formula or '—':20s}  family={family}")

    return record

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Rebuild m2_concepts_corpus.json for TscgPocletMiner RAG engine'
    )
    parser.add_argument('--repo',    type=str, help='Path to TSCG repo root')
    parser.add_argument('--m2',      type=str, help='Direct path to M2_GenericConcepts.jsonld')
    parser.add_argument('--out',     type=str, help='Output JSON path (default: next to this script)')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    # ── Locate M2_GenericConcepts.jsonld ──────────────────────────────────────
    if args.m2:
        m2_path = Path(args.m2)
    else:
        repo_root = Path(args.repo) if args.repo else find_repo_root(_SCRIPT_DIR)
        if repo_root is None:
            print(f"ERROR: Cannot find M2_GenericConcepts.jsonld relative to {_SCRIPT_DIR}")
            print("Use --repo /path/to/tscg or --m2 /direct/path/M2_GenericConcepts.jsonld")
            sys.exit(1)
        m2_path = find_m2_file(repo_root)
        if m2_path is None:
            print(f"ERROR: M2_GenericConcepts.jsonld not found under {repo_root}")
            sys.exit(1)

    print(f"Reading: {m2_path}")

    with open(m2_path, encoding='utf-8') as f:
        doc = json.load(f)

    graph = doc.get('@graph', [])
    print(f"Graph entries: {len(graph)}")

    # ── Extract all GenericConcepts ───────────────────────────────────────────
    concepts = []
    skipped  = []

    for entry in graph:
        if is_generic_concept(entry):
            concepts.append(extract_concept(entry, verbose=args.verbose))
        else:
            eid = entry.get('@id', '')
            if eid.startswith('m2:') and entry.get('@type') == 'owl:Class':
                skipped.append(strip_prefix(eid))

    print(f"Extracted {len(concepts)} GenericConcept(s), skipped {len(skipped)} meta-class(es)")
    if skipped and args.verbose:
        print(f"Skipped meta-classes: {', '.join(skipped)}")

    # Sort by id for stable output
    concepts.sort(key=lambda c: c['id'])

    # ── Build output ──────────────────────────────────────────────────────────
    now_iso  = datetime.datetime.now(datetime.timezone.utc).isoformat()

    output = {
        '_meta': {
            'title':        'TSCG M2 GenericConcepts Corpus — Auto-generated by rebuild_m2_corpus.py',
            'version':      '1.0.0',
            'generatedAt':  now_iso,
            'date':         now_iso[:10],
            'authors':      ['Echopraxium with the collaboration of Claude AI'],
            'source':       str(m2_path),
            'conceptCount': len(concepts),
            'hash':         '',
        },
        'concepts': concepts,
    }

    # Hash
    content = json.dumps(output, ensure_ascii=False, indent=2)
    h = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    output['_meta']['hash'] = h

    # ── Write ─────────────────────────────────────────────────────────────────
    out_path = Path(args.out) if args.out else _SCRIPT_DIR / 'm2_concepts_corpus.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nWritten: {out_path}  ({len(concepts)} concepts, hash={h})")

    # ── Summary ───────────────────────────────────────────────────────────────
    families = {}
    for c in concepts:
        families[c['family'] or 'Unknown'] = families.get(c['family'] or 'Unknown', 0) + 1
    print(f"\nBy family:")
    for fam, count in sorted(families.items(), key=lambda x: -x[1]):
        print(f"  {fam:30s}  {count}")

    no_formula = [c['id'] for c in concepts if not c['formula']]
    if no_formula:
        print(f"\nConcepts without formula ({len(no_formula)}): {', '.join(no_formula)}")


if __name__ == '__main__':
    main()
