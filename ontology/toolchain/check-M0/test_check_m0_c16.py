#!/usr/bin/env python3
"""
test_check_m0_c16.py — negative tests for check_m0 C16 (no use of a deprecated M0 term)
and for the C03 alias rule (1.8.1).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0 (2026-11-15)
Home   : ontology/toolchain/check-M0/test_check_m0_c16.py

Every check must be able to FAIL. C16 reads the deprecated set from M0_Common.jsonld;
these tests assert that (1) the set is read from the file (non-empty, contains a
known deprecated term), (2) a real instance with no deprecated term passes, and (3)
each form of use is caught: a graph key, a nested key, an @context entry, an
{"@id": ...} value and a bare string value.

Run:  python ontology/toolchain/check-M0/test_check_m0_c16.py   (exit 0 iff all pass)
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_m0_instances import (  # noqa: E402
    load_deprecated_terms, find_deprecated_uses, discover_instances,
)

FAILURES = []


def check(name, cond, detail=""):
    print(f"  [{'OK' if cond else 'XX'}] {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def main() -> int:
    dep = load_deprecated_terms()
    check("deprecated set read from M0_Common (non-empty)", len(dep) > 0, f"{len(dep)}")
    check("m0:scoreA is in the deprecated set", "m0:scoreA" in dep)
    check("m0:InstanceProperty is NOT deprecated", "m0:InstanceProperty" not in dep)

    path, name, _ = next(iter(discover_instances(only_name="Thermostat")))
    base = json.loads(Path(path).read_text(encoding="utf-8"))
    check("Thermostat at HEAD has no deprecated use", find_deprecated_uses(base, dep) == [],
          str(find_deprecated_uses(base, dep)[:3]))

    def mutated(fn):
        d = copy.deepcopy(base)
        fn(d)
        return len(find_deprecated_uses(d, dep))

    check("graph key caught", mutated(lambda d: d["@graph"][0].__setitem__("m0:scoreA", 0.5)) == 1)
    check("nested key caught",
          mutated(lambda d: d["@graph"][0].__setitem__("x", {"y": {"m0:epistemicGap": 0.1}})) == 1)
    check("@context entry caught",
          mutated(lambda d: d["@context"].__setitem__("m0:focalScore", {"@type": "xsd:float"})) == 1)
    check("@id value caught",
          mutated(lambda d: d["@graph"][0].__setitem__("z", {"@id": "m0:spectralClass.Coherent"})) == 1)
    check("bare string value caught",
          mutated(lambda d: d["@graph"][0].__setitem__("z", ["m0:scoringStatus.Complete"])) == 1)

    # C03 alias rule (1.8.1): an acronym name gives an all-lowercase alias
    from check_m0_instances import InstanceChecker
    def alias(n):
        return InstanceChecker(Path("."), n, "")._camel()
    check("C03 alias of VCO is vco", alias("VCO") == "vco", alias("VCO"))
    check("C03 alias of RAAS is raas", alias("RAAS") == "raas", alias("RAAS"))
    check("C03 alias of Vco is vco", alias("Vco") == "vco", alias("Vco"))
    check("C03 alias of QRCodeToPocketCity unchanged",
          alias("QRCodeToPocketCity") == "qRCodeToPocketCity", alias("QRCodeToPocketCity"))
    check("C03 alias of Fire_Triangle is fireTriangle", alias("Fire_Triangle") == "fireTriangle",
          alias("Fire_Triangle"))

    print(f"\n{'PASS' if not FAILURES else 'FAIL'}: {len(FAILURES)} failure(s)")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
