#!/usr/bin/env python3
"""
test_m1_domains.py — negative tests for SC-5 (domains are classes, Michel 2026-10-11/12).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/tests/test_m1_domains.py

A domain is an owl:Class rdfs:subClassOf m1:Domain (or of a parent domain), never an
individual. Checked by M1 SHACL 1.8.0 SHAPE 11 DomainClassShape and SHAPE 13
NoDomainIndividualShape, and by check_M1 1.8.0 DCC010 (the Fm1m2 first argument must be
a class descending from m1:Domain, transitively, possibly through several parents).

Each SHACL test mutates a real file IN MEMORY and asserts the exact move of exactly one
shape, relative to the unmutated file (deltas; frozen values belong to the gate).

Run:  python ontology/toolchain/validator/tests/test_m1_domains.py
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_m1_combo_punning as base  # noqa: E402  (shared loaders, run as check_M1 runs pyshacl)

check_M1 = base.check_M1
REPO = base.REPO
REGISTRY = REPO / "ontology" / "M1_Domains.jsonld"
GEOLOGY = REPO / "ontology" / "M1_extensions" / "geology" / "M1_Geology.jsonld"


def _node(d, nid):
    return next(n for n in d["@graph"] if n.get("@id") == nid)


def _delta(path, mutate):
    return base._delta(path, mutate)


# -- SHAPE 11 / 13 on HEAD -----------------------------------------------------------
def test_domain_shapes_clean_on_head():
    for path in (REGISTRY, GEOLOGY):
        counts, _g = base._shapes(path, base._load(path))
        assert counts.get("DomainClassShape", 0) == 0, (path.name, counts)
        assert counts.get("NoDomainIndividualShape", 0) == 0, (path.name, counts)


# -- SHAPE 13 ---------------------------------------------------------------------------
def test_shape13_domain_class_punned_as_individual():
    def m(d):
        _node(d, "m1:domain:Ecology")["@type"] = ["owl:Class", "m1:Domain"]
    assert _delta(REGISTRY, m) == {"NoDomainIndividualShape": 1}


def test_shape13_obsolete_knowledgefield_individual():
    def m(d):
        n = _node(d, "m1:extension:geology:Geological")
        n["@type"] = ["owl:Class", "m2:KnowledgeField"]
    assert _delta(GEOLOGY, m) == {"NoDomainIndividualShape": 1}


# -- SHAPE 11 ---------------------------------------------------------------------------
def test_shape11_missing_label():
    # SHAPE 5 PlainDomainClassShape (every rdfs:subClassOf subject) requires a label too
    assert _delta(REGISTRY, lambda d: _node(d, "m1:domain:Ecology").pop("rdfs:label")) \
        == {"DomainClassShape": 1, "PlainDomainClassShape": 1}


def test_shape11_related_domain_as_string():
    def m(d):
        _node(d, "m1:domain:Ecology")["m1:relatedDomains"] = ["m1:domain:Biology"]
    assert _delta(REGISTRY, m) == {"DomainClassShape": 1}


def test_shape11_retired_knowledgefield_role_on_adjective_subdomain():
    # Geological is a subclass of Geology: reached through rdfs:subClassOf+ (transitive)
    def m(d):
        _node(d, "m1:extension:geology:Geological")["m2:knowledgeFieldRole"] = "ADJECTIVE"
    assert _delta(GEOLOGY, m) == {"DomainClassShape": 1}


# -- check_M1 DCC010 --------------------------------------------------------------------
def _registry(ontology_dir):
    check_M1._DOMAIN_REGISTRY = None
    try:
        return check_M1.load_domain_registry(ontology_dir)
    finally:
        check_M1._DOMAIN_REGISTRY = None


def test_dcc010_reads_the_class_hierarchy_on_head():
    names = _registry(REPO / "ontology")
    # extension domain classes (Music / EnergyGenerators / SystemicModeling were missed
    # until 1.7.0), an adjective subdomain, a registry class
    for n in ("music", "energygenerators", "systemicmodeling", "geological", "ecology"):
        assert n in names, n
    for n in ("cascade", "oscillator", "domain"):          # not domains
        assert n not in names, n


def test_dcc010_multiple_parents_and_non_domain():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "M1_extensions").mkdir()
        graph = [
            {"@id": "m1:domain:A", "@type": "owl:Class", "rdfs:subClassOf": {"@id": "m1:Domain"}},
            {"@id": "m1:domain:B", "@type": "owl:Class", "rdfs:subClassOf": {"@id": "m1:Domain"}},
            {"@id": "m1:domain:AB", "@type": "owl:Class",
             "rdfs:subClassOf": [{"@id": "m1:domain:A"}, {"@id": "m1:domain:B"}]},
            {"@id": "m1:NotADomain", "@type": "owl:Class", "rdfs:subClassOf": {"@id": "m1:Other"}},
            {"@id": "m1:domain:Ind", "@type": "m1:Domain"},          # an individual: not a domain
        ]
        (root / "M1_Domains.jsonld").write_text(json.dumps({"@graph": graph}), encoding="utf-8")
        names = _registry(root)
    assert {"a", "b", "ab"} <= names
    assert "notadomain" not in names and "ind" not in names


def test_dcc010_flags_a_domainless_fm1m2():
    path = GEOLOGY
    d = base._load(path)
    c = check_M1.M1Checker(path, dry_run=True)
    c.data = copy.deepcopy(d)
    check_M1._DOMAIN_REGISTRY = None
    try:
        c._check_signature("m1:test:X", "Fm1m2(Cascade, Duplication, Network)", "Fm1m2", "DCC")
        c._check_signature("m1:test:Y", "Fm1m2(Geological, Duplication)", "Fm1m2", "DCC")
    finally:
        check_M1._DOMAIN_REGISTRY = None
    dcc010 = [i.message for i in c.issues if i.code == "DCC010"]
    assert len(dcc010) == 1 and "m1:test:X" in dcc010[0], dcc010


def main() -> int:
    tests = [(n, fn) for n, fn in sorted(globals().items())
             if n.startswith("test_") and callable(fn)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL {name}: {e!r}")
    print(f"{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
