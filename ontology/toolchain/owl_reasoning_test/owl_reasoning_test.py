#!/usr/bin/env python3
"""
owl_reasoning_test.py — OWL reasoning (Pellet via Owlready2) on a TSCG ontology file.

Author : Echopraxium with the collaboration of Claude AI
Version: 2.0.0 (2026-10-10)
Home   : ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py

Usage (from anywhere inside the repository; paths are relative to the repo root):
    python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M3_GenesisGrammar.jsonld
    python ... --file ontology/M2_GenericConcepts.jsonld --isolated     # ignore owl:imports
    python ... --file ontology/M3_GenesisGrammar.jsonld --list-imports # resolve imports only, no Java

2.0.0 (2026-10-10)
- owl:imports are RESOLVED LOCALLY. Since WS-1 lot 1i (2026-09-30) imports are real IRIs;
  Owlready2 followed them, downloaded raw JSON-LD from GitHub and failed ("NTriples parsing
  error … line 1"), so any file with imports could not be reasoned. Now every import whose
  IRI is inside the repository (https://raw.githubusercontent.com/Echopraxium/tscg/main/…)
  is read from the working copy, transitively, and merged into ONE graph; the owl:imports
  triples are then removed so that Owlready2 does not fetch anything. An import that cannot
  be resolved locally is an ERROR (exit 2), never a silent skip.
- A globally INCONSISTENT ontology is reported as FAILED (exit 1). Before, Owlready2's
  OwlReadyInconsistentOntologyError fell into the generic handler and was printed as
  "Java not installed / JAVA_HOME not set" — a logical defect disguised as a setup issue.
- The temporary RDF/XML file goes to the system temp directory (was temp_ontology.rdf at
  the repository root).
- Exit codes: 0 consistent · 1 inconsistent (global or unsatisfiable classes) · 2 input or
  import error · 3 reasoner/environment error.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

REPO_BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main/"
OWL_IMPORTS = "http://www.w3.org/2002/07/owl#imports"


def find_tscg_root(start: Path):
    """The repository root: the nearest ancestor holding an 'ontology/' directory."""
    current = start.resolve()
    for _ in range(12):
        if (current / "ontology").is_dir():
            return current
        if current == current.parent:
            return None
        current = current.parent
    return None


def iri_to_local(iri: str, root: Path):
    """Map an import IRI to a file of the working copy, or None if it is outside the repo."""
    if iri.startswith(REPO_BASE):
        return root / iri[len(REPO_BASE):].split("#", 1)[0]
    return None


def load_with_imports(path: Path, root: Path, follow_imports: bool = True):
    """Parse `path` (JSON-LD) and, transitively, its owl:imports from the working copy.

    Returns (graph, merged_files, unresolved): the merged rdflib Graph WITHOUT owl:imports
    triples, the list of files merged (first = `path`), and the list of import IRIs that
    could not be resolved locally (empty when everything was found)."""
    from rdflib import Graph, URIRef

    root = root.resolve()
    merged, unresolved, seen = [], [], set()
    g = Graph()
    todo = [path.resolve()]
    while todo:
        f = todo.pop(0)
        if f in seen:
            continue
        seen.add(f)
        part = Graph()
        part.parse(str(f), format="json-ld", base=REPO_BASE + f.relative_to(root).as_posix())
        merged.append(f)
        imports = [str(o) for o in part.objects(None, URIRef(OWL_IMPORTS))]
        for s, p, o in part:
            if str(p) != OWL_IMPORTS:
                g.add((s, p, o))
        if not follow_imports:
            continue
        for iri in imports:
            local = iri_to_local(iri, root)
            if local is None or not local.is_file():
                unresolved.append(iri)
            elif local.resolve() not in seen:
                todo.append(local.resolve())
    return g, merged, unresolved


def main(argv=None):
    parser = argparse.ArgumentParser(description="OWL reasoning (Pellet) on a TSCG ontology file")
    parser.add_argument("--file", default="ontology/M2_GenericConcepts.jsonld",
                        help="path relative to the repository root (default: ontology/M2_GenericConcepts.jsonld)")
    parser.add_argument("--isolated", action="store_true",
                        help="reason on the file alone: ignore its owl:imports")
    parser.add_argument("--list-imports", action="store_true",
                        help="resolve and list the imports, then stop (no Java needed)")
    args = parser.parse_args(argv)

    print("=" * 70)
    print("TSCG OWL REASONING — owl_reasoning_test 2.0.0")
    print("=" * 70)

    root = find_tscg_root(Path.cwd())
    if root is None:
        print("❌ Could not find the TSCG repository root (a directory holding 'ontology/').")
        return 2
    print(f"Repository root: {root}")

    path = root / args.file
    if not path.is_file():
        print(f"❌ File not found: {args.file}  (paths are relative to the repository root)")
        return 2

    try:
        import rdflib  # noqa: F401
    except ImportError:
        print("❌ rdflib is not installed: python -m pip install -r ontology/toolchain/requirements.txt")
        return 3

    mode = "isolated: owl:imports ignored" if args.isolated else "+ owl:imports, resolved locally"
    print(f"\n📥 Loading {args.file}  ({mode})")
    try:
        graph, merged, unresolved = load_with_imports(path, root, follow_imports=not args.isolated)
    except Exception as e:  # a parse error is an input error, not an environment error
        print(f"❌ Cannot parse the input as JSON-LD: {type(e).__name__}: {e}")
        return 2
    for f in merged:
        print(f"   • {f.relative_to(root.resolve()).as_posix()}")
    print(f"   {len(merged)} file(s) merged, {len(graph)} triples, owl:imports removed")
    if unresolved:
        print("❌ Imports that cannot be resolved in the working copy:")
        for iri in unresolved:
            print(f"   • {iri}")
        print("   Fix the import, or run with --isolated to reason on the file alone.")
        return 2
    if args.list_imports:
        return 0

    try:
        from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError
    except ImportError:
        print("❌ owlready2 is not installed: python -m pip install owlready2")
        return 3

    tmpdir = tempfile.mkdtemp(prefix="tscg_owl_")
    tmp = Path(tmpdir) / "merged.rdf"
    try:
        graph.serialize(destination=str(tmp), format="xml")
        onto = get_ontology(f"file://{tmp.absolute()}").load()
        print(f"\n📊 Classes: {len(list(onto.classes()))}   Properties: {len(list(onto.properties()))}"
              f"   Individuals: {len(list(onto.individuals()))}")

        print("\n🧠 Running Pellet (10–30 s)…")
        try:
            with onto:
                sync_reasoner_pellet(infer_property_values=True, debug=1)
        except OwlReadyInconsistentOntologyError as e:
            print("\n❌ THE ONTOLOGY IS INCONSISTENT (global inconsistency found by Pellet)")
            print(f"   {e}")
            print(f"\nStatus: ❌ FAILED — {args.file}")
            return 1
        except Exception as e:
            print(f"\n❌ Reasoner / environment error: {type(e).__name__}: {e}")
            print("   Check: 'java -version' works (Java 17+); owlready2 is installed.")
            return 3

        unsat = list(onto.inconsistent_classes())
        print("\n" + "=" * 70)
        print(f"File      : {args.file}  ({len(merged)} file(s) merged)")
        print("Reasoner  : Pellet (via Owlready2)")
        if unsat:
            print(f"Status    : ❌ FAILED — {len(unsat)} unsatisfiable class(es):")
            for c in unsat:
                print(f"   • {c.iri}")
            print("=" * 70)
            return 1
        print("Status    : ✅ PASSED — no inconsistency, no unsatisfiable class")
        print("=" * 70)
        return 0
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
