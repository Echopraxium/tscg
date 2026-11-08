#!/usr/bin/env python3
"""
test_fm2_notation.py — the Fm2 notation: grammar, parser, SHACL pattern, checker.

Author : Echopraxium with the collaboration of Claude AI
Version: 1.0.0 (2026-11-08)
Home   : ontology/toolchain/validator/tests/test_fm2_notation.py

The grammar (grammars/Fm2_notation.ebnf) is the single source. These tests fail
when one of the things derived from it drifts:
  T1  every example written in the EBNF parses;
  T2  the sh:pattern of SHAPE 14 in M1_Schema_shacl.ttl IS the generated pattern;
  T3  parser and pattern agree (accept / reject) on the examples, on malformed
      formulas and on every formula of M1_CoreConcepts;
  T4  SHAPE 9 (primitive argument, arity) reads a block as one unit;
  T5  check_M1: GCC011 / GCC012 / GCC013 bite, and a well-formed block passes.

Run:  python ontology/toolchain/validator/tests/test_fm2_notation.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLCHAIN = HERE.parent.parent
ONTOLOGY = TOOLCHAIN.parent
sys.path.insert(0, str(TOOLCHAIN / "grammars"))
sys.path.insert(0, str(TOOLCHAIN / "check-M1"))
import fm2_notation as f  # noqa: E402

EBNF = TOOLCHAIN / "grammars" / "Fm2_notation.ebnf"
SHACL = TOOLCHAIN / "check-M1" / "M1_Schema_shacl.ttl"

MALFORMED = [
    "Fm2(Component, Process, Trajectory) | shape=Circular",          # guard
    "Fm2(A × B)",                                                    # operator
    "Fm2(Trajectory { foo: [a: b] })",                               # unknown section
    "Fm2(Trajectory { properties: [shape: Circular, final: maybe] })",
    "Fm2(X, Y { constraints: [range(Q) << range(F)] })",             # not a dimension
    "Fm2(X, Y { constraints: [range(F) <<< range(F)] })",            # not a relation
    "Fm2(X, Y { constraints: [range(F) << range(F)], properties: [a: b] })",  # order
]

FAILS = []


def check(name, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def ebnf_examples():
    return [l.strip() for l in EBNF.read_text(encoding="utf-8").splitlines()
            if l.strip().startswith("Fm2(")]


def accepts(s):
    try:
        f.parse(s)
        return True
    except f.NotationError:
        return False


def shacl_patterns():
    import rdflib
    g = rdflib.Graph()
    g.parse(SHACL, format="turtle")
    sh = rdflib.Namespace("http://www.w3.org/ns/shacl#")
    m1 = rdflib.Namespace("https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#")
    def pats(shape):
        out = []
        for p in g.objects(m1[shape], sh.property):
            out += [str(o) for o in g.objects(p, sh.pattern)]
            for n in g.objects(p, getattr(sh, "not")):
                out += ["NOT:" + str(o) for o in g.objects(n, sh.pattern)]
        return out
    return pats("Fm2NotationShape"), pats("ComboFormulaShape")


def main():
    ex = ebnf_examples()
    print("T1 — the examples of the EBNF parse")
    check("EBNF has examples", len(ex) >= 5, f"{len(ex)}")
    for e in ex:
        check(f"parse: {e[:60]}", accepts(e))

    print("T2 — SHAPE 14's pattern is the generated one")
    p14, p9 = shacl_patterns()
    check("SHAPE 14 carries exactly the generated pattern", p14 == [f.shacl_pattern()], str(p14)[:120])

    print("T3 — parser and pattern agree")
    pat = re.compile(f.shacl_pattern())
    core = json.loads((ONTOLOGY / "M1_CoreConcepts.jsonld").read_text(encoding="utf-8"))
    corpus = [n["m1:structuralGrammarFormula"] for n in core["@graph"]
              if isinstance(n.get("m1:structuralGrammarFormula"), str)
              and n["m1:structuralGrammarFormula"].startswith("Fm")]
    for s in ex + MALFORMED + corpus:
        check(f"agree: {s[:60]}", accepts(s) == bool(pat.match(s)))
    for s in MALFORMED:
        check(f"reject: {s[:60]}", not accepts(s))

    print("T4 — SHAPE 9 reads a block as one unit")
    prim = [re.compile(x[4:]) for x in p9 if x.startswith("NOT:") and "St|Ss" in x]
    arity = [re.compile(x) for x in p9 if not x.startswith("NOT:") and x.startswith("^(Fm2|Fm1m2)")]
    check("SHAPE 9 patterns found", len(prim) == 1 and len(arity) == 1)
    if prim and arity:
        for e in ex:
            check(f"no primitive seen in: {e[:50]}", not prim[0].search(e))
            check(f"arity ok: {e[:50]}", bool(arity[0].match(e)) == (len(f.parse(e).arguments) >= 2))
        check("primitive still caught", bool(prim[0].search("Fm2(F, Memory)")))
        check("primitive caught next to a block", bool(prim[0].search("Fm2(Trajectory { properties: [shape: Circular] }, F)")))

    print("T5 — check_M1 bites on the meaning")
    sys.argv = ["check_M1"]
    import check_M1  # noqa: E402
    k = check_M1.M1Checker(ONTOLOGY / "M1_CoreConcepts.jsonld")
    cases = [
        ("Fm2(Component, Process, Trajectory { properties: [shape: Circular, final: true] })", []),
        ("Fm2(Amplification, Regulation { constraints: [range(Amplification.F) << range(F)] })", []),
        ("Fm2(Component, Process, Trajectory { properties: [trajectoryShape: Circular] })", ["GCC012"]),
        ("Fm2(Component, Process, Trajectory { properties: [shape: Square] })", ["GCC012"]),
        ("Fm2(Amplification, Regulation { constraints: [range(Memory.F) << range(F)] })", ["GCC013"]),
        ("Fm2(Amplification, Regulation { constraints: [range(Amplification.K) << range(F)] })", ["GCC013"]),
        ("Fm2(Amplification, Regulation { constraints: [range(F) <<< range(F)] })", ["GCC011"]),
        ("Fm2(Component, Process, Trajectory) | shape=Circular", ["GCC009"]),
    ]
    for formula, expected in cases:
        k.issues = []
        k._check_signature("m1:Test", formula, "Fm2", "GCC")
        got = sorted(i.code for i in k.issues)
        check(f"{expected or 'clean'}: {formula[:55]}", got == sorted(expected), str(got))

    print()
    print("FAILED: " + ", ".join(FAILS) if FAILS else "ALL PASS")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
