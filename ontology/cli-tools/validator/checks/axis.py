"""
checks/axis.py — AXIS family: Facet-mechanism conformance (gates SC-3).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/cli-tools/validator/checks/axis.py

The measuring family for WS-0 / SC-3 (see SC-3 draft v2). It makes the graving of
the M3 Facet mechanism + the Audience facet FALSIFIABLE: it is RED until M3 carries
a well-formed facet registry AND every M0 instance has migrated off the old
m0:facet.* apparatus. Gauge for SC-3: ERROR count -> 0.

DETECTION ONLY (spec §1). Never writes. Findings may carry a proposed_diff.

Scope is decided per file by relpath:

  M0 instances (instances/**/M0_*.jsonld)
    AXIS-1  m3:hasFacetValue value is a bare string, not an IRI      -> ERROR
    AXIS-2  m3:hasFacetValue IRI is not a registered m3:FacetValue   -> ERROR
    AXIS-3  legacy m0:facet.* apparatus still present (unmigrated)   -> ERROR

  M3 registry (ontology/M3_GenesisGrammar.jsonld)
    AXIS-4  m3:FacetValue individual has no m3:valueOf               -> ERROR
    AXIS-5  m3:valueOf target is not a declared m3:Facet individual  -> ERROR

REGISTRY NOTE
-------------
_FACET_VALUES mirrors SC-3 draft v2 §2 (Audience: KitArchitect/KitCrafter/KitUser).
It is held here in the same spirit as ctx.py's _CANON — a small, ratified, stable
set verified against the draft/HEAD. The SOURCE OF TRUTH is the M3 registry once
graved; a later lot should replace this literal with a load from M3_GenesisGrammar
(the same file AXIS-4/AXIS-5 already parse), so the two can never drift.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Tuple

# Ratified facet-value local names (SC-3 draft v2 §2). Local name = part after the
# last ':' or '#'. Absolute or prefixed IRI forms both reduce to these.
_FACET_VALUES = {
    "audience.KitArchitect",
    "audience.KitCrafter",
    "audience.KitUser",
}

# Legacy apparatus removed by SC-3 (draft v2 §3). Any USE in an instance = unmigrated.
_LEGACY_KEYS = {
    "m0:hasFacet",
    "m0:illustratesConcept",
    "m0:roleGrounding",
}
# Legacy IRIs that must no longer appear as values.
_LEGACY_VALUE_RE = re.compile(r"(?:^|[:#])(?:facet\.Democratization|roleGrounding\.[A-Za-z]+)$")

_PREFIXED = re.compile(r"^([A-Za-z][\w.\-]*):(?!//)(.*)$")
_URI_SCHEMES = {"http", "https", "urn", "mailto", "file", "ftp", "tag", "did", "data"}

_FACETVALUE_TYPE_LOCALS = {"FacetValue"}   # m3:FacetValue
_FACET_TYPE_LOCALS = {"Facet"}             # m3:Facet


def _finding(cid: str, severity: str, relpath: str, node: str, message: str,
             proposed_diff: str | None = None) -> Dict[str, Any]:
    f = {"id": cid, "severity": severity, "file": relpath,
         "node": node, "message": message}
    if proposed_diff:
        f["proposed_diff"] = proposed_diff
    return f


def _local_name(iri: str) -> str:
    """Local name = substring after the last '#', else after the first ':' prefix."""
    if "#" in iri:
        return iri.rsplit("#", 1)[-1]
    m = _PREFIXED.match(iri)
    if m:
        return m.group(2)
    if "/" in iri:
        return iri.rsplit("/", 1)[-1]
    return iri


def _as_iri(value: Any) -> Tuple[bool, str | None]:
    """(is_iri, iri) for a single JSON-LD value.

    IRI = an @id object, or a string that is a prefixed name / absolute URL.
    A bare string ('KitUser') is a literal -> not an IRI (AXIS-1 territory).
    """
    if isinstance(value, dict):
        vid = value.get("@id")
        if isinstance(vid, str):
            return True, vid
        return False, None
    if isinstance(value, str):
        if value.startswith("http://") or value.startswith("https://"):
            return True, value
        m = _PREFIXED.match(value)
        if m and m.group(1) not in _URI_SCHEMES:
            return True, value
        return False, None
    return False, None


def _iter_nodes(doc: Any) -> List[Dict[str, Any]]:
    """All dict nodes anywhere in the document (handles @graph or flat)."""
    nodes: List[Dict[str, Any]] = []

    def walk(n: Any) -> None:
        if isinstance(n, dict):
            nodes.append(n)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for item in n:
                walk(item)

    walk(doc)
    return nodes


def _types_of(node: Dict[str, Any]) -> List[str]:
    t = node.get("@type")
    if t is None:
        return []
    return [t] if isinstance(t, str) else [x for x in t if isinstance(x, str)]


# --------------------------------------------------------------------------- M0

def _run_m0_instance(relpath: str, doc: Any) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    nodes = _iter_nodes(doc)

    for node in nodes:
        node_id = node.get("@id", "-")

        # AXIS-1 / AXIS-2 : m3:hasFacetValue values
        if "m3:hasFacetValue" in node:
            raw = node["m3:hasFacetValue"]
            vals = raw if isinstance(raw, list) else [raw]
            for v in vals:
                is_iri, iri = _as_iri(v)
                if not is_iri:
                    findings.append(_finding(
                        "AXIS-1", "ERROR", relpath, node_id,
                        f"m3:hasFacetValue carries a bare value {v!r}; must be an IRI "
                        f"of a registered m3:FacetValue (e.g. m3:audience.KitUser)."))
                    continue
                if _local_name(iri) not in _FACET_VALUES:
                    findings.append(_finding(
                        "AXIS-2", "ERROR", relpath, node_id,
                        f"m3:hasFacetValue -> {iri!r} is not a registered m3:FacetValue "
                        f"(known: {', '.join(sorted(_FACET_VALUES))})."))

        # AXIS-3 : legacy apparatus (unmigrated). One finding per legacy property.
        for key in sorted(_LEGACY_KEYS & set(node.keys())):
            findings.append(_finding(
                "AXIS-3", "ERROR", relpath, node_id,
                f"legacy facet apparatus '{key}' still present; SC-3 removes it "
                f"(migrate m0:hasFacet facet.Democratization -> m3:hasFacetValue "
                f"m3:audience.KitUser; drop illustratesConcept/roleGrounding)."))
        # legacy IRIs referenced under a NON-legacy property. A legacy key is already
        # reported above; an @id is the node's own identity, not an outbound reference
        # (skipping both avoids the triple-count on one Democratization link).
        for key, val in node.items():
            if key in _LEGACY_KEYS or key.startswith("@"):
                continue
            for item in (val if isinstance(val, list) else [val]):
                _, iri = _as_iri(item)
                if iri and _LEGACY_VALUE_RE.search(iri):
                    findings.append(_finding(
                        "AXIS-3", "ERROR", relpath, node_id,
                        f"legacy facet IRI {iri!r} (under '{key}') still referenced; "
                        f"removed by SC-3."))
    return findings


# --------------------------------------------------------------------------- M3

def _run_m3_registry(relpath: str, doc: Any) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    nodes = _iter_nodes(doc)

    declared_facets = {
        node.get("@id") for node in nodes
        if node.get("@id") and any(_local_name(t) in _FACET_TYPE_LOCALS
                                   for t in _types_of(node))
    }

    for node in nodes:
        if not any(_local_name(t) in _FACETVALUE_TYPE_LOCALS for t in _types_of(node)):
            continue
        vid = node.get("@id", "-")
        vo = node.get("m3:valueOf")
        if vo is None:
            findings.append(_finding(
                "AXIS-4", "ERROR", relpath, vid,
                "m3:FacetValue has no m3:valueOf; every value must belong to an axis."))
            continue
        _, target = _as_iri(vo)
        if target is None or target not in declared_facets:
            findings.append(_finding(
                "AXIS-5", "ERROR", relpath, vid,
                f"m3:valueOf -> {target!r} is not a declared m3:Facet individual in "
                f"this file (axis is a phantom)."))
    return findings


# ------------------------------------------------------------------------ entry

def run(relpath: str, text: str) -> List[Dict[str, Any]]:
    """Run the AXIS family on one file's raw JSON-LD text. Returns findings."""
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        return [_finding("AXIS-000", "ERROR", relpath, "-",
                         f"file is not parseable JSON: {exc}")]

    name = relpath.rsplit("/", 1)[-1]
    if name.startswith("M0_") and relpath.startswith("instances/"):
        return _run_m0_instance(relpath, doc)
    if name == "M3_GenesisGrammar.jsonld":
        return _run_m3_registry(relpath, doc)
    return []
