"""
checks/doc.py — DOC family: document-plane checks D1–D7 (WS-5, step 2).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/toolchain/validator/checks/doc.py

WHY A DOCUMENT PLANE
--------------------
SHACL sees only the expanded graph: a bare JSON key (declared in no @context) is
dropped on expansion, so no shape can ever see it. These checks read the JSON AS
WRITTEN. Specification: ontology/docs/_01_Worksite/WS-5/
WS-5_M3M2_Instrumentation_Scoping.md §3.1 (decisions Q1–Q4, D5 option (a)).
DETECTION ONLY — nothing is written to the corpus.

Checks
------
D1  bare key (VOC): a key with no ':' , not a JSON-LD keyword, not a term of the
    file's @context. ONE finding per (file, key) carrying `count` = occurrences
    (the gate counts occurrences). WARNING: frozen backlog owned by WS-1.
D2  `@vocab` in @context (bare keys silently become <vocab><key> terms). ERROR.
D3  root object with both `@id` and `@graph`: a JSON-LD NAMED graph, invisible to
    pyshacl's default graph. ERROR.
D4  `owl:imports` value that is not an IRI reference ({"@id": ...}): a string is a
    literal, nothing is imported. ERROR.
D5  changelog (decision D5(a), Michel 2026-10-04: the ONLY changelog is
    `m3:changelog`, on the owl:Ontology node):
      D5  any key whose name contains "changelog" (case-insensitive) other than
          `m3:changelog` — legacy `metadata.changelog` maps, `m2:changelog`,
          per-concept `m2:changeLog` …;
      D5  the owl:Ontology node has no `m3:changelog`, or it is not a list;
      D5  an entry whose keys are not exactly {owl:versionInfo, dcterms:date,
          adms:versionNotes};
      D5  retention exceeded: more than 7 entries in an M3 file, 3 elsewhere.
    ERROR.
D6  layer inversion: a term of a LOWER layer (m2: in an M3 file, …) used as a KEY,
    or as an IRI value (@id, @type, {"@id": ...}). Mentions in prose are not
    references and are not counted. ERROR.
D7  the file does not expand under a strict JSON-LD 1.1 processor (pyld), remote
    contexts blocked (an offline check must not depend on the network). ERROR.
    A missing pyld is reported as D7 ERROR "not run", never as a pass.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any, Dict, List, Optional

CHANGELOG_KEY = "m3:changelog"
ENTRY_KEYS = {"owl:versionInfo", "dcterms:date", "adms:versionNotes"}
RETENTION = {"M3": 7}
RETENTION_DEFAULT = 3

_MN = re.compile(r"^m([0-3]):")


def _finding(cid: str, severity: str, relpath: str, node: str, message: str,
             **extra: Any) -> Dict[str, Any]:
    f = {"id": cid, "severity": severity, "file": relpath, "node": node,
         "message": message}
    f.update({k: v for k, v in extra.items() if v is not None})
    return f


def _layer_num(relpath: str) -> Optional[int]:
    m = re.match(r"M([0-3])_", relpath.rsplit("/", 1)[-1])
    return int(m.group(1)) if m else None


def _types(node: Dict[str, Any]) -> List[str]:
    t = node.get("@type", [])
    return [x for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)]


def _walk(obj: Any, cb, node_id: str = "-") -> None:
    """cb(key, value, owner_node_id) for every key outside @context."""
    if isinstance(obj, dict):
        nid = obj.get("@id", node_id) if isinstance(obj.get("@id"), str) else node_id
        for k, v in obj.items():
            if k == "@context":
                continue
            cb(k, v, nid)
            _walk(v, cb, nid)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, cb, node_id)


# -- individual checks -------------------------------------------------------------

def d1_bare_keys(relpath: str, doc: Dict[str, Any], terms: set) -> List[Dict[str, Any]]:
    counts: Counter = Counter()

    def cb(k, _v, _nid):
        if k.startswith("@") or ":" in k or k in terms:
            return
        counts[k] += 1

    _walk(doc, cb)
    return [_finding("D1", "WARNING", relpath, key,
                     f"bare key '{key}' x{n}: declared in no @context, dropped on "
                     f"JSON-LD expansion (invisible to SHACL and to any reasoner)",
                     count=n)
            for key, n in sorted(counts.items())]


def d2_vocab(relpath: str, ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "@vocab" not in ctx:
        return []
    return [_finding("D2", "ERROR", relpath, "@context",
                     f"@vocab = {ctx['@vocab']!r}: every bare key silently becomes a "
                     f"term in that namespace (gauge EXT-2). Remove @vocab and declare "
                     f"the terms.")]


def d3_named_graph(relpath: str, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "@id" in doc and "@graph" in doc:
        return [_finding("D3", "ERROR", relpath, str(doc["@id"]),
                         "root object has both @id and @graph: the whole file is a "
                         "NAMED graph, invisible to pyshacl's default graph. Move @id "
                         "onto the owl:Ontology node inside @graph.")]
    return []


def d4_imports(relpath: str, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def cb(k, v, nid):
        if k != "owl:imports":
            return
        for x in (v if isinstance(v, list) else [v]):
            if not (isinstance(x, dict) and isinstance(x.get("@id"), str)):
                out.append(_finding("D4", "ERROR", relpath, nid,
                                    f"owl:imports value {json.dumps(x, ensure_ascii=False)[:80]} "
                                    f"is not an IRI reference: write {{\"@id\": \"<iri>\"}}"))

    _walk(doc, cb)
    return out


def d5_changelog(relpath: str, doc: Dict[str, Any], layer: Optional[str]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    # (1) any other changelog-like key, anywhere
    def cb(k, _v, nid):
        if "changelog" in k.lower() and k != CHANGELOG_KEY:
            out.append(_finding("D5", "ERROR", relpath, nid,
                                f"key '{k}': the only changelog is '{CHANGELOG_KEY}' on the "
                                f"owl:Ontology node (decision D5(a)). Fold its content "
                                f"there or drop it.", key=k))

    _walk(doc, cb)

    # (2) the ontology node and its m3:changelog
    graph = doc.get("@graph", [])
    nodes = [n for n in (graph if isinstance(graph, list) else []) if isinstance(n, dict)]
    onto = [n for n in nodes if "owl:Ontology" in _types(n)]
    if len(onto) != 1:
        out.append(_finding("D5", "ERROR", relpath, "-",
                            f"{len(onto)} owl:Ontology node(s) in @graph, expected 1: "
                            f"the changelog has no unique home."))
        return out
    o = onto[0]
    oid = str(o.get("@id", "-"))
    log = o.get(CHANGELOG_KEY)
    if log is None:
        out.append(_finding("D5", "ERROR", relpath, oid,
                            f"owl:Ontology node has no '{CHANGELOG_KEY}'."))
        return out
    if not isinstance(log, list):
        out.append(_finding("D5", "ERROR", relpath, oid,
                            f"'{CHANGELOG_KEY}' is a {type(log).__name__}, expected a list "
                            f"of entries."))
        return out
    for i, e in enumerate(log):
        keys = set(e) if isinstance(e, dict) else set()
        if keys != ENTRY_KEYS:
            missing = sorted(ENTRY_KEYS - keys)
            extra = sorted(keys - ENTRY_KEYS)
            out.append(_finding("D5", "ERROR", relpath, f"{oid} {CHANGELOG_KEY}[{i}]",
                                f"entry keys must be exactly {sorted(ENTRY_KEYS)}; "
                                f"missing {missing}, extra {extra}"))
    limit = RETENTION.get(layer or "", RETENTION_DEFAULT)
    if len(log) > limit:
        out.append(_finding("D5", "ERROR", relpath, oid,
                            f"'{CHANGELOG_KEY}' holds {len(log)} entries; retention for "
                            f"{layer} is {limit}. Older entries belong in git history."))
    return out


def d6_layer_inversion(relpath: str, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    layer = _layer_num(relpath)
    if layer is None:
        return []
    out: List[Dict[str, Any]] = []

    def lower(term: Any) -> bool:
        m = _MN.match(term) if isinstance(term, str) else None
        return bool(m) and int(m.group(1)) < layer

    def cb(k, v, nid):
        if lower(k):
            out.append(_finding("D6", "ERROR", relpath, nid,
                                f"key '{k}' belongs to a lower layer than M{layer}: a layer "
                                f"may only use terms of its own layer or above."))
        # @id covers node identities AND references {"@id": ...} (the walk descends
        # into them): one finding per occurrence, never two.
        if k in ("@id", "@type"):
            for x in (v if isinstance(v, list) else [v]):
                if lower(x):
                    out.append(_finding("D6", "ERROR", relpath, nid,
                                        f"{k} '{x}' belongs to a lower layer than M{layer}."))

    _walk(doc, cb)
    return out


def d7_expand(relpath: str, doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
        from pyld import jsonld
    except ImportError as exc:
        return [_finding("D7", "ERROR", relpath, "-",
                         f"pyld not installed ({exc}): strict expansion NOT run. "
                         f"This is not a pass.")]

    def offline(url, options=None):
        raise jsonld.JsonLdError(f"remote document blocked (offline check): {url}",
                                 "jsonld.LoadDocumentError", {"url": url},
                                 code="loading document failed")

    try:
        jsonld.expand(doc, {"documentLoader": offline})
    except Exception as exc:
        return [_finding("D7", "ERROR", relpath, "-",
                         f"strict JSON-LD 1.1 expansion (pyld) fails: {_root_cause(exc)}")]
    return []


def _root_cause(exc: BaseException) -> str:
    """pyld wraps errors several levels deep; the useful text is the innermost one."""
    cur, last = exc, exc
    while cur is not None:
        last = cur
        cur = getattr(cur, "cause", None)
    args = getattr(last, "args", None)
    msg = args[0] if args and isinstance(args[0], str) else str(last)
    details = getattr(last, "details", None)
    hint = ""
    if isinstance(details, dict):
        for k in ("term", "iri", "url"):
            if details.get(k):
                hint = f" [{k}: {str(details[k])[:110]}]"
                break
    return (str(msg).splitlines()[0] + hint)[:260]


# -- family entry point --------------------------------------------------------------

def run(relpath: str, text: str, layer: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        return [_finding("D0", "ERROR", relpath, "-", f"not parseable JSON: {exc}")]
    if not isinstance(doc, dict):
        return [_finding("D0", "ERROR", relpath, "-", "root is not a JSON object")]
    ctx = doc.get("@context", {})
    ctx = ctx if isinstance(ctx, dict) else {}
    terms = {k for k in ctx if not k.startswith("@")}

    findings: List[Dict[str, Any]] = []
    findings += d1_bare_keys(relpath, doc, terms)
    findings += d2_vocab(relpath, ctx)
    findings += d3_named_graph(relpath, doc)
    findings += d4_imports(relpath, doc)
    findings += d5_changelog(relpath, doc, layer)
    findings += d6_layer_inversion(relpath, doc)
    findings += d7_expand(relpath, doc)
    return findings


def occurrences(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    """Occurrence count per check id (D1 findings carry `count`)."""
    c: Counter = Counter()
    for f in findings:
        if re.fullmatch(r"D\d", f["id"]):
            c[f["id"]] += int(f.get("count", 1))
    return dict(sorted(c.items()))
