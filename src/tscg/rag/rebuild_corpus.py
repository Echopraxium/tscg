#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_corpus.py — TSCG Poclet Corpus Builder
Author: Echopraxium with the collaboration of Claude AI
v2.0.0

Scans instances/poclets/ for M0_*.jsonld files and writes
poclet_corpus_profile.json — the exact same format as rebuild_corpus.js.

PocletMiner (Electron) reads this JSON file via the 'load-corpus' IPC handler
and rag_engine.js uses it for semantic embedding.

Usage:
  python rebuild_corpus.py                        # auto-detect repo root
  python rebuild_corpus.py --repo /path/to/tscg  # explicit repo root
  python rebuild_corpus.py --out /path/to/out/poclet_corpus_profile.json
  python rebuild_corpus.py --verbose              # print extracted entries

Output: poclet_corpus_profile.json (next to this script unless --out is given)
"""

import os
import sys
import json
import re
import argparse
import hashlib
import datetime
from pathlib import Path
from collections import Counter
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ─── Repo detection ───────────────────────────────────────────────────────────

_SCRIPT_DIR = Path(__file__).resolve().parent

def find_repo_root(start: Path) -> Optional[Path]:
    """Walk up from start looking for instances/poclets/."""
    for p in [start, *start.parents]:
        if (p / "instances" / "poclets").is_dir():
            return p
    return None

# ─── Field extraction helpers ─────────────────────────────────────────────────

def strip_ns(s: str) -> str:
    """'m2:Cascade (ternary 5D)' → 'Cascade', 'm1:biology:DevelopmentalBiology' → 'DevelopmentalBiology'"""
    if not isinstance(s, str):
        return str(s)
    # Remove trailing parenthetical
    s = re.sub(r'\s*\(.*?\)\s*$', '', s).strip()
    # Strip last namespace prefix
    parts = s.split(':')
    return parts[-1].strip() if len(parts) > 1 else s.strip()

def safe_str(v) -> str:
    if isinstance(v, str):   return v
    if isinstance(v, list):  return v[0] if v else ''
    if isinstance(v, dict):  return v.get('@id', v.get('@value', ''))
    return str(v) if v is not None else ''

def safe_list(v) -> list:
    if isinstance(v, list): return v
    if v is not None:       return [v]
    return []

def safe_num(v) -> Optional[float]:
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, str):
        try:   return float(v)
        except ValueError: return None
    return None

def extract_asfid(entry: dict) -> Optional[dict]:
    """Extract ASFID scores from various field naming conventions."""
    # Convention 1: m0:asfidScores { A, S, F, I, D, mean }
    raw = entry.get('m0:asfidScores')
    if isinstance(raw, dict):
        scores = {
            'A':    safe_num(raw.get('A')),
            'S':    safe_num(raw.get('S')),
            'F':    safe_num(raw.get('F')),
            'I':    safe_num(raw.get('I')),
            'D':    safe_num(raw.get('D')),
            'mean': safe_num(raw.get('mean'))
        }
        # Also handle verbose keys with justification siblings (M0_Kidneys pattern)
        if scores['A'] is None: scores['A'] = safe_num(raw.get('A_score'))
        if scores['S'] is None: scores['S'] = safe_num(raw.get('S_score'))
        if scores['F'] is None: scores['F'] = safe_num(raw.get('F_score'))
        if scores['I'] is None: scores['I'] = safe_num(raw.get('I_score'))
        if scores['D'] is None: scores['D'] = safe_num(raw.get('D_score'))
        # Auto-compute mean if missing
        if scores['mean'] is None:
            vals = [v for v in [scores['A'], scores['S'], scores['F'], scores['I'], scores['D']] if v is not None]
            scores['mean'] = round(sum(vals) / len(vals), 3) if vals else None
        return scores

    # Convention 2: m1:core:asfidScoring { attractor, structure, flow, information, dynamics, overall }
    raw = entry.get('m1:core:asfidScoring')
    if isinstance(raw, dict):
        a = safe_num(raw.get('attractor'))
        s = safe_num(raw.get('structure'))
        f = safe_num(raw.get('flow'))
        i = safe_num(raw.get('information'))
        d = safe_num(raw.get('dynamics'))
        mean = safe_num(raw.get('overall') or raw.get('mean'))
        if mean is None:
            vals = [v for v in [a, s, f, i, d] if v is not None]
            mean = round(sum(vals) / len(vals), 3) if vals else None
        return {'A': a, 'S': s, 'F': f, 'I': i, 'D': d, 'mean': mean}

    # Convention 3: m0:asfidMean (scalar only)
    mean = safe_num(entry.get('m0:asfidMean'))
    if mean is not None:
        return {'A': None, 'S': None, 'F': None, 'I': None, 'D': None, 'mean': mean}
    return None

def extract_revoi(entry: dict) -> Optional[dict]:
    """Extract REVOI scores — also handles deprecated 'orive' field names."""
    # Convention 1: m0:revoiScores { R, E, V, O, I, mean }
    raw = entry.get('m0:revoiScores') or entry.get('m0:oriveScores')
    if isinstance(raw, dict):
        return {
            'R':    safe_num(raw.get('R')),
            'E':    safe_num(raw.get('E')),
            'V':    safe_num(raw.get('V')),
            'O':    safe_num(raw.get('O')),
            'I':    safe_num(raw.get('I')),
            'mean': safe_num(raw.get('mean'))
        }
    # Convention 2: m0:oriveMean / m0:revoiMean (scalar only)
    mean = (safe_num(entry.get('m0:oriveMean')) or
            safe_num(entry.get('m0:revoiMean')))
    if mean is not None:
        return {'R': None, 'E': None, 'V': None, 'O': None, 'I': None, 'mean': mean}
    return None

def extract_domain(entry: dict) -> str:
    """Extract domain string, stripping namespace prefix if present."""
    raw = safe_str(entry.get('m0:domain', ''))
    if raw:
        return strip_ns(raw)
    # Fallback: m1:core:pocletCharacteristics { domain / mainDomain }
    chars = entry.get('m1:core:pocletCharacteristics')
    if isinstance(chars, dict):
        d = chars.get('domain') or chars.get('mainDomain') or ''
        if d:
            return safe_str(d)
    return 'Unknown'

def extract_subdomains(entry: dict) -> list:
    return [strip_ns(safe_str(s)) for s in safe_list(entry.get('m0:subdomains', []))]

def extract_ontology_type(entry: dict) -> str:
    ot = entry.get('m3:ontologyType') or entry.get('m2:ontologyCategory', '')
    if isinstance(ot, dict):
        ot = ot.get('@id', '')
    return strip_ns(safe_str(ot)) or 'Poclet'

def extract_validates(entry: dict) -> list:
    """Collect validated metaconcepts from all known field names."""
    fields = [
        'm0:validatesMetaconcepts',
        'm0:validatedMetaconcepts',
        'm0:primaryGenericConcepts',
        'm0:instantiatesM2',
        'm0:mobilisedGenericConcepts',
        'm0:genericConceptsUsed',
    ]
    result = []
    for f in fields:
        for v in safe_list(entry.get(f, [])):
            name = strip_ns(safe_str(v))
            if name and name not in result:
                result.append(name)
    return result

def extract_primary_metaconcept(entry: dict) -> str:
    raw = (entry.get('m0:primaryMetaconcept') or
           entry.get('m0:primaryGenericConcept') or '')
    return strip_ns(safe_str(raw))

def extract_epistemic_gap(entry: dict) -> Optional[float]:
    raw = entry.get('m0:epistemicGap')
    if isinstance(raw, dict):
        return safe_num(raw.get('delta') or raw.get('value'))
    return safe_num(raw)

# ─── JSON-LD file parser ──────────────────────────────────────────────────────

def find_system_entry(graph: list) -> Optional[dict]:
    """Return the primary system node from a @graph array.

    Priority:
      1. Entry with m0:domain (explicit domain tag)
      2. Entry with m1:core:pocletCharacteristics (new-style metadata)
      3. Entry with m1:core:asfidScoring
      4. Entry typed owl:Ontology (header node, often carries metadata)
      5. First NamedIndividual
      6. First entry
    """
    for e in graph:
        if 'm0:domain' in e:
            return e
    for e in graph:
        if 'm1:core:pocletCharacteristics' in e or 'm1:core:asfidScoring' in e:
            return e
    for e in graph:
        types = safe_list(e.get('@type', []))
        if any('Ontology' in t for t in types):
            return e
    for e in graph:
        types = safe_list(e.get('@type', []))
        if any('NamedIndividual' in t for t in types):
            return e
    return graph[0] if graph else None

def parse_poclet_file(file_path: Path, verbose: bool = False) -> Optional[dict]:
    try:
        with open(file_path, encoding='utf-8') as f:
            doc = json.load(f)
    except Exception as e:
        if verbose:
            print(f"  [skip] {file_path.name}: parse error — {e}")
        return None

    graph = doc.get('@graph', [])
    if not graph:
        if verbose:
            print(f"  [skip] {file_path.name}: no @graph")
        return None

    entry = find_system_entry(graph)
    if entry is None:
        if verbose:
            print(f"  [skip] {file_path.name}: empty @graph")
        return None

    ontology_type = extract_ontology_type(entry)

    # Only Poclets (skip TransDisclet, TscgTool, CaseStudy, etc.)
    if ontology_type not in ('Poclet', ''):
        if verbose:
            print(f"  [skip] {file_path.name}: type={ontology_type}")
        return None

    filename    = file_path.stem                                     # M0_RAAS
    label_raw   = entry.get('rdfs:label', '')
    label       = safe_str(label_raw) or filename

    domain      = extract_domain(entry)
    subdomains  = extract_subdomains(entry)
    asfid       = extract_asfid(entry)
    revoi       = extract_revoi(entry)
    gap         = extract_epistemic_gap(entry)
    primary     = extract_primary_metaconcept(entry)
    validates   = extract_validates(entry)

    # Rich description for RAG embedding (same logic as rebuild_corpus.js)
    desc_parts = [
        label,
        f"Domain: {domain}",
        f"Subdomains: {', '.join(subdomains)}" if subdomains else '',
        f"Primary concept: {primary}" if primary else '',
        f"Validates: {', '.join(validates)}" if validates else '',
        f"ASFID mean: {asfid['mean']}" if asfid and asfid['mean'] is not None else '',
        f"REVOI mean: {revoi['mean']}" if revoi and revoi['mean'] is not None else '',
    ]
    description = '. '.join(p for p in desc_parts if p)

    poclet = {
        'id':                    filename,
        'label':                 label,
        'domain':                domain,
        'subdomains':            subdomains,
        'ontologyType':          'Poclet',
        'asfidScores':           asfid,
        'revoiScores':           revoi,
        'epistemicGap':          gap,
        'primaryMetaconcept':    primary,
        'validatesMetaconcepts': validates,
        'description':           description,
        'sourceFile':            str(file_path)
    }

    if verbose:
        print(f"  [ok]   {filename}  domain={domain}  "
              f"asfid={asfid['mean'] if asfid else '?'}  "
              f"revoi={revoi['mean'] if revoi else '?'}")
    return poclet

# ─── Directory scanner ────────────────────────────────────────────────────────

def walk_jsonld(directory: Path) -> list:
    result = []
    if not directory.is_dir():
        return result
    for root, dirs, files in os.walk(directory):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in files:
            if fname.endswith('.jsonld'):
                result.append(Path(root) / fname)
    return sorted(result)

# ─── Static corpus data ───────────────────────────────────────────────────────

# invariants.criteria — shape expected by renderer.js buildInvariantChecklist()
INVARIANT_CRITERIA = [
    {
        'id': 'real_observable',
        'weight': 2,
        'question': 'Is this a real, observable system (not a pure abstraction)?',
        'examples_ok': ['RAAS', 'Transistor', 'Fire Triangle']
    },
    {
        'id': 'asfid_complete',
        'weight': 2,
        'question': 'Can you identify at least A + S + F ASFID dimensions?',
        'examples_ok': ['ButterflyMetamorphosis', 'BloodPressureControl']
    },
    {
        'id': 'domain_delimited',
        'weight': 1,
        'question': 'Is the domain clearly delimited (biology, electronics, …)?',
        'examples_ok': ['Yggdrasil (mythology)', 'Transistor (electronics)']
    },
    {
        'id': 'non_trivial_dynamics',
        'weight': 2,
        'question': 'Does the system exhibit non-trivial regulation or dynamics?',
        'examples_ok': ['RAAS (cascade)', 'ExposureTriangle (trade-off)']
    },
    {
        'id': 'web_documented',
        'weight': 1,
        'question': 'Is it well-documented on the web (Wikipedia, papers)?',
        'examples_ok': ['Kidneys', 'AdaptiveImmuneResponse']
    },
    {
        'id': 'corpus_gap',
        'weight': 2,
        'question': 'Does it fill a domain gap in the current corpus?',
        'examples_ok': ['SIR model (epidemiology)', 'Peirce triangle (semiotics)']
    },
    {
        'id': 'type_discriminated',
        'weight': 1,
        'question': 'Can you determine the type: Poclet vs TransDisclet vs SystemicFramework?',
        'examples_ok': ['Transistor (Poclet)', 'Oscillator (TransDisclet)']
    },
]

# screening_criteria — legacy flat list (kept for rebuild_corpus.js compatibility)
SCREENING_CRITERIA = [
    {'id': c['id'], 'label': c['question'], 'weight': c['weight']}
    for c in INVARIANT_CRITERIA
]

SCORING_THRESHOLDS = {
    'verdict': {
        'strong_candidate': {'invariants_min': 6, 'asfid_min': 0.75},
        'candidate':        {'invariants_min': 4, 'asfid_min': 0.60},
        'weak_candidate':   {'invariants_min': 2, 'asfid_min': 0.45},
    }
}

WEB_SEARCH_TEMPLATES = {
    'wikipedia':      'https://en.wikipedia.org/wiki/{SYSTEM}',
    'google':         'https://www.google.com/search?q={SYSTEM}+{DOMAIN}+system+model',
    'duckduckgo':     'https://duckduckgo.com/?q={SYSTEM}+{DOMAIN}+system+model',
    'scholar':        'https://scholar.google.com/scholar?q={SYSTEM}+system+model',
    'gemini_verify':  'https://gemini.google.com/app?q=Is+{SYSTEM}+a+minimal+complete+system+in+{DOMAIN}%3F+Does+it+have+ASFID+dimensions%3F',
    'gemini_suggest': 'https://gemini.google.com/app?q=Suggest+5+minimal+complete+systems+in+{DOMAIN}+suitable+for+TSCG+poclet+modeling',
}

GAP_ANALYSIS_CANDIDATES = [
    {'system': 'SIR Epidemiological Model',     'domain': 'Epidemiology',     'type': 'Poclet',       'priority': 'high'},
    {'system': "Peirce's Semiotic Triangle",    'domain': 'Semiotics',        'type': 'Poclet',       'priority': 'high'},
    {'system': 'Harmonic Oscillator',           'domain': 'Physics',          'type': 'TransDisclet', 'priority': 'high'},
    {'system': "Rogers' Innovation Diffusion",  'domain': 'Social Sciences',  'type': 'Poclet',       'priority': 'medium'},
    {'system': 'Neural Network (Perceptron)',    'domain': 'Computer Science', 'type': 'Poclet',       'priority': 'medium'},
    {'system': 'Krebs Cycle',                   'domain': 'Biochemistry',     'type': 'Poclet',       'priority': 'medium'},
    {'system': 'Supply & Demand Equilibrium',   'domain': 'Economics',        'type': 'Poclet',       'priority': 'medium'},
    {'system': 'Predator-Prey (Lotka-Volterra)','domain': 'Ecology',          'type': 'Poclet',       'priority': 'medium'},
]

# ─── Corpus assembly ──────────────────────────────────────────────────────────

def build_corpus_stats(poclets: list, domains: list) -> dict:
    return {
        'total':           len(poclets),
        'domains_covered': len([d for d in domains if d != 'Unknown']),
        'validated':       len([p for p in poclets if p.get('asfidScores')]),
    }

def build_domain_coverage(poclets: list) -> dict:
    coverage: dict = {}
    for p in poclets:
        coverage.setdefault(p['domain'], []).append(p['id'])
    return coverage

def build_gap_analysis(poclets: list) -> dict:
    covered = {p['domain'].lower() for p in poclets if p['domain'] != 'Unknown'}
    uncovered = sorted({
        c['domain'] for c in GAP_ANALYSIS_CANDIDATES
        if c['domain'].lower() not in covered
    })
    return {
        'description': 'Domains and systems not yet covered in the corpus',
        'uncovered_domains': uncovered,
        'priority_candidates': GAP_ANALYSIS_CANDIDATES,
    }

def build_invariants(poclets: list) -> dict:
    domains = sorted({p['domain'] for p in poclets})

    all_concepts = [c for p in poclets for c in p['validatesMetaconcepts']]
    freq = Counter(all_concepts)
    top_concepts = [{'concept': c, 'freq': f}
                    for c, f in freq.most_common(20)]

    def dim_mean(dim_key, scores_key):
        vals = [p[scores_key][dim_key]
                for p in poclets
                if p.get(scores_key) and p[scores_key].get(dim_key) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    asfid_means = {d: dim_mean(d, 'asfidScores') for d in 'ASFID'}
    revoi_means = {d: dim_mean(d, 'revoiScores')  for d in 'REVOI'}

    return {
        'description':        'Statistical invariants distilled from the validated corpus',
        'domains':            domains,
        'topValidatedConcepts': top_concepts,
        'corpusMeanASFID':    asfid_means,
        'corpusMeanREVOI':    revoi_means,
        'criteria':           INVARIANT_CRITERIA,   # ← renderer.js buildInvariantChecklist()
    }

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Rebuild poclet_corpus_profile.json for TscgPocletMiner'
    )
    parser.add_argument('--repo',    type=str, help='Path to TSCG repo root')
    parser.add_argument('--out',     type=str, help='Output JSON path (default: next to this script)')
    parser.add_argument('--verbose', action='store_true', help='Print each parsed poclet')
    args = parser.parse_args()

    # ── Locate poclets directory ──────────────────────────────────────────────
    if args.repo:
        repo_root = Path(args.repo)
    else:
        repo_root = find_repo_root(_SCRIPT_DIR)
        if repo_root is None:
            print(f"ERROR: Could not find instances/poclets/ relative to {_SCRIPT_DIR}")
            print("Use --repo /path/to/tscg to specify the repo root explicitly.")
            sys.exit(1)

    poclets_dir = repo_root / 'instances' / 'poclets'
    print(f"Scanning: {poclets_dir}")

    # ── Parse all .jsonld files ───────────────────────────────────────────────
    all_files = walk_jsonld(poclets_dir)
    print(f"Found {len(all_files)} .jsonld file(s)")

    poclets = []
    skipped = []

    for f in all_files:
        result = parse_poclet_file(f, verbose=args.verbose)
        if result:
            poclets.append(result)
        else:
            skipped.append(f.name)

    print(f"Extracted {len(poclets)} poclet(s), skipped {len(skipped)}")
    if skipped and args.verbose:
        print(f"Skipped: {', '.join(skipped)}")

    # ── Build output document ─────────────────────────────────────────────────
    now_iso  = datetime.datetime.now(datetime.timezone.utc).isoformat()
    now_date = now_iso[:10]

    invariants = build_invariants(poclets)
    domains    = invariants['domains']

    output = {
        '_meta': {
            'title':        'TSCG Poclet Corpus Profile — Auto-generated by rebuild_corpus.py',
            'version':      '2.1.0',
            'generatedAt':  now_iso,
            'date':         now_date,
            'authors':      ['Echopraxium with the collaboration of Claude AI'],
            'purpose':      'Profiling reference used by TscgPocletMiner to score new candidates against the validated corpus.',
            'pocletsDir':   str(poclets_dir),
            'pocletCount':  len(poclets),
            'skippedFiles': skipped,
            'hash':         ''
        },
        'corpus_stats':       build_corpus_stats(poclets, domains),
        'domain_coverage':    build_domain_coverage(poclets),
        'invariants':         invariants,
        'gap_analysis':       build_gap_analysis(poclets),
        'scoring_thresholds': SCORING_THRESHOLDS,
        'web_search_templates': WEB_SEARCH_TEMPLATES,
        'screening_criteria': SCREENING_CRITERIA,
        'poclets':            poclets,
    }

    # ── Hash ──────────────────────────────────────────────────────────────────
    content = json.dumps(output, ensure_ascii=False, indent=2)
    h = hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    output['_meta']['hash'] = h

    # ── Write ─────────────────────────────────────────────────────────────────
    out_path = Path(args.out) if args.out else _SCRIPT_DIR / 'poclet_corpus_profile.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)

    final_content = json.dumps(output, ensure_ascii=False, indent=2)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Written: {out_path}  ({len(poclets)} poclets, hash={h})")

    # ── Console summary ───────────────────────────────────────────────────────
    print(f"\nDomains covered ({len(invariants['domains'])}):")
    for d in invariants['domains']:
        count = sum(1 for p in poclets if p['domain'] == d)
        print(f"  {d:30s}  {count} poclet(s)")

    if invariants['topValidatedConcepts']:
        print(f"\nTop GenericConcepts:")
        for entry in invariants['topValidatedConcepts'][:10]:
            print(f"  {entry['concept']:30s}  freq={entry['freq']}")


if __name__ == '__main__':
    main()
