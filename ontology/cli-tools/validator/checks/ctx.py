"""
checks/ctx.py — CTX family: @context / IRI-resolution hygiene.

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/cli-tools/validator/checks/ctx.py

The highest-value family (design spec §2). DETECTION ONLY — every finding may carry
a proposed_diff, but the validator never writes. All checks are deterministic and
need no human in the loop; the *policy* calls (e.g. is the CTX-5 coercion idiom a
defect?) are surfaced as advisories for the human to rule on, never auto-decided.

Checks
------
CTX-1  prefix USED but not DECLARED           -> ERROR for mN, WARNING otherwise
CTX-2  relative mN prefix + @vocab present    -> ERROR (resolves against owl#)
CTX-3  @base malformed (no trailing ontology/) -> ERROR
CTX-4  relative mN prefix (fragile, @base-dep) -> ERROR
CTX-5  @context term whose NAME contains ':'
         - value is a string IRI (alias attempt) -> WARNING (real defect)
         - value is an object (coercion idiom)    -> INFO   (benign, NOT a defect)
CTX-CANON  declared mN prefix not pointing at its canonical file -> INFO (advisory)
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List

# Well-known non-mN prefixes: an undeclared use is still a bug, but lower severity.
_STANDARD = {"rdf", "rdfs", "owl", "xsd", "dcterms", "skos", "dc",
             "sh", "vann", "prov", "foaf", "schema"}
# URL schemes / JSON-LD keywords that look like `prefix:...` but are NOT prefixed names.
_URI_SCHEMES = {"http", "https", "urn", "mailto", "file", "ftp", "tag", "did", "data"}
_MN = {"m0", "m1", "m2", "m3"}

# Canonical absolute targets for the mN prefixes (design spec §2 "Canonical rule";
# the four layer roots ratified by Michel 2026-08-08 and verified against HEAD:
# every mN prefix in the governed corpus declares exactly one of these).
_CANON = {
    "m3": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M3_GenesisGrammar.jsonld#",
    "m2": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M2_GenericConcepts.jsonld#",
    "m1": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M1_CoreConcepts.jsonld#",
    "m0": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/M0_Common.jsonld#",
}

_PREFIXED = re.compile(r"^([A-Za-z][\w.\-]*):(?!//)(.*)$")


def _finding(cid: str, severity: str, relpath: str, node: str, message: str,
             proposed_diff: str | None = None) -> Dict[str, Any]:
    f = {"id": cid, "severity": severity, "file": relpath,
         "node": node, "message": message}
    if proposed_diff:
        f["proposed_diff"] = proposed_diff
    return f


def _is_relative(iri: str) -> bool:
    return not (iri.startswith("http://") or iri.startswith("https://"))


def _collect_declared(context: Dict[str, Any]) -> Dict[str, str]:
    """key -> IRI for simple prefix declarations (colon-free key, string value)."""
    declared = {}
    for k, v in context.items():
        if k.startswith("@"):
            continue
        if ":" in k:
            continue  # colon-named term, handled by CTX-5
        if isinstance(v, str):
            declared[k] = v
    return declared


# Values under these keys are IRIs and DO get expanded (undeclared prefix = real bug).
_IRI_VALUE_KEYS = {"@id", "@type"}


def _prefix_of(s: str) -> str | None:
    m = _PREFIXED.match(s)
    if m and m.group(1) not in _URI_SCHEMES:
        return m.group(1)
    return None


def _iter_iri_position_prefixes(obj: Any) -> List[str]:
    """Prefixes appearing in a REAL IRI-expansion position only.

    Deterministic proxy for JSON-LD expansion (spec §4: 'expansion is where
    relative-IRI bugs surface'), without a full expander in lot 1:
      * a prefixed KEY (predicate position) is always expanded;
      * a prefixed value under @id / @type is expanded.
    A prefixed string sitting in a prose/definition/data value (changes,
    rdfs:comment, skos:definition, an arbitrary property, a plain list item) is a
    LITERAL, never expanded — flagging it re-reports changelog history and
    definition text, the exact false-positive class the spec warns about.
    """
    used: List[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                if not k.startswith("@"):
                    p = _prefix_of(k)
                    if p:
                        used.append(p)
                if k in _IRI_VALUE_KEYS:
                    vals = v if isinstance(v, list) else [v]
                    for item in vals:
                        if isinstance(item, str):
                            p = _prefix_of(item)
                            if p:
                                used.append(p)
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(obj)
    return used


def run(relpath: str, text: str) -> List[Dict[str, Any]]:
    """Run the CTX family on one file's raw JSON-LD text. Returns findings."""
    findings: List[Dict[str, Any]] = []

    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        return [_finding("CTX-000", "ERROR", relpath, "@context",
                         f"file is not parseable JSON: {exc}")]

    context = doc.get("@context")
    if context is None:
        return [_finding("CTX-000", "WARNING", relpath, "@context",
                         "no @context block")]
    if isinstance(context, list):
        return [_finding("CTX-000", "WARNING", relpath, "@context",
                         "@context is a list; lot-1 CTX analyses dict contexts only")]
    if not isinstance(context, dict):
        return [_finding("CTX-000", "ERROR", relpath, "@context",
                         f"@context is a {type(context).__name__}, expected object")]

    declared = _collect_declared(context)
    base = context.get("@base")
    has_vocab = "@vocab" in context

    # -- CTX-1: used but not declared ---------------------------------------
    # Only STRUCTURAL prefixes are in scope: the mN family and well-known vocab
    # prefixes. An arbitrary capitalised data string like "Mythology:" in a
    # reference table is data, not a namespace defect — flagging it is noise. The
    # attested CTX-1 defect is `m3:` used without declaration; that is what this
    # catches, without crying wolf on 400 data strings.
    used = set(_iter_iri_position_prefixes(doc))
    colon_heads = {k.split(":", 1)[0] for k in context if ":" in k and not k.startswith("@")}
    structural = _MN | _STANDARD
    for pfx in sorted(used):
        if pfx not in structural:
            continue
        if pfx in declared or pfx in colon_heads:
            continue
        sev = "ERROR" if pfx in _MN else "WARNING"
        findings.append(_finding(
            "CTX-1", sev, relpath, f"{pfx}:",
            f"prefix '{pfx}:' is used but not declared in @context "
            f"(expands to an opaque/bogus IRI, invisible to reasoner/SHACL)"))

    # -- CTX-2 / CTX-4: relative mN prefixes --------------------------------
    for pfx in sorted(p for p in declared if p in _MN):
        iri = declared[pfx]
        if _is_relative(iri):
            findings.append(_finding(
                "CTX-4", "ERROR", relpath, f"{pfx}:",
                f"mN prefix '{pfx}' is relative ({iri!r}); resolves via @base and is "
                f"one bad edit from breaking. Canonical form is absolute."))
            if has_vocab:
                findings.append(_finding(
                    "CTX-2", "ERROR", relpath, f"{pfx}:",
                    f"relative prefix '{pfx}' with @vocab present -> resolves against "
                    f"'{context['@vocab']}', silently misplacing every {pfx}: term."))

    # -- CTX-CANON: declared but non-canonical mN target --------------------
    for pfx in sorted(p for p in declared if p in _CANON):
        iri = declared[pfx]
        if not _is_relative(iri) and iri != _CANON[pfx]:
            findings.append(_finding(
                "CTX-CANON", "INFO", relpath, f"{pfx}:",
                f"'{pfx}' points at {iri!r}, not the canonical {_CANON[pfx]!r}"))

    # -- CTX-3: @base malformed ---------------------------------------------
    if isinstance(base, str) and not base.rstrip("/").endswith("/ontology"):
        findings.append(_finding(
            "CTX-3", "ERROR", relpath, "@base",
            f"@base {base!r} does not end in '.../ontology/'; relative IRIs mint "
            f"under the wrong root."))

    # -- CTX-5: colon-named terms -------------------------------------------
    for k, v in context.items():
        if k.startswith("@") or ":" not in k:
            continue
        if isinstance(v, str):
            findings.append(_finding(
                "CTX-5", "WARNING", relpath, k,
                f"@context term {k!r} contains ':' and maps to an IRI string "
                f"(alias attempt; JSON-LD will not use it as a prefix)."))
        else:
            findings.append(_finding(
                "CTX-5i", "INFO", relpath, k,
                f"@context term {k!r} contains ':' but maps to a coercion object "
                f"({json.dumps(v, ensure_ascii=False)}); standard JSON-LD idiom, "
                f"NOT a defect — flagged for policy confirmation."))

    return findings
