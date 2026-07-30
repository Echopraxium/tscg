#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tscg_layercake_mcp_server.py — TscgLayerCakeMCPServer

A local-first MCP (Model Context Protocol) server that exposes the TSCG
ontology corpus as a small set of task-shaped tools, so an MCP client
(e.g. Claude Desktop) can pull only what a query needs instead of loading
the whole corpus into its context window.

Design principles
-----------------
* Stateless on the corpus. By default every read fetches LIVE from git HEAD
  (raw.githubusercontent.com/.../main/ontology/). Nothing is persisted to
  disk, so nothing can go stale relative to HEAD. This makes "run it locally"
  a valid distribution model, not just a budget fallback.
* source = "head" (authority, default) | "local" (your working copy while editing).
* Task-shaped tools over a raw SPARQL endpoint: get_file / search / get_concept /
  list_* / resolve_iri keep each call short and reliable. SPARQL is an optional
  last-resort escape hatch.
* The business logic is pure functions (no MCP dependency) so it is testable
  and usable via  `python tscg_layercake_mcp_server.py --selftest`.

Author: Echopraxium with the collaboration of Claude AI
"""

from __future__ import annotations

import os
import sys
import json
import urllib.request
import urllib.error
from functools import lru_cache
from pathlib import Path
from typing import Optional

# ==============================================================================
# CONFIGURATION
# ==============================================================================

OWNER = "Echopraxium"
REPO = "tscg"
DEFAULT_REF = os.environ.get("TSCG_REF", "main")

# Everything the tools talk about is relative to this directory inside the repo.
# It matches the ontologies' own  "@base": ".../main/ontology/"  convention,
# so tool paths look exactly like the IRIs you already use, e.g.
#   "M2_GenericConcepts.jsonld"
#   "M1_extensions/biology/M1_Biology.jsonld"
ONTOLOGY_PREFIX = "ontology/"

RAW_BASE = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{DEFAULT_REF}/"
GITHUB_TREE_API = f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees/{DEFAULT_REF}?recursive=1"

# A tiny committed file listing every corpus path (ontology-relative), served
# from the raw CDN. Preferred over the GitHub API because the CDN is NOT
# rate-limited, so the listing works everywhere with zero config. Regenerate
# and commit it whenever files are added/removed:
#   python tscg_layercake_mcp_server.py --emit-manifest > ontology/_manifest.json
MANIFEST_PATH = "_manifest.json"

# source = "head"  -> live from GitHub  (authoritative)
# source = "local" -> your working copy (set TSCG_LOCAL_REPO to the repo root)
DEFAULT_SOURCE = os.environ.get("TSCG_SOURCE", "head")
LOCAL_REPO = os.environ.get("TSCG_LOCAL_REPO", "")

# Optional: lifts the unauthenticated GitHub API limit (60 req/h -> 5000 req/h).
# Only the tree listing hits the API; file contents come from the raw CDN,
# which is not rate-limited. A token is therefore rarely necessary.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Known compact-prefix table for resolve_iri (Strategy 2 of the IRIExpander).
# Order matters: multi-segment prefixes are checked before their parents.
_PREFIX_TABLE = [
    ("m3:eagle_eye:", "M3_EagleEye.jsonld#"),
    ("m3:sphinx_eye:", "M3_SphinxEye.jsonld#"),
    ("m3:", "M3_GenesisGrammar.jsonld#"),
    ("m2:", "M2_GenericConcepts.jsonld#"),
    ("m1:", "M1_CoreConcepts.jsonld#"),
]

# In-session caches. In-memory only — they die with the process, so they can
# never become a stale on-disk snapshot of HEAD.
_TREE_CACHE: dict[str, list[str]] = {}
_FILE_CACHE: dict[tuple[str, str], str] = {}


# ==============================================================================
# LOW-LEVEL I/O
# ==============================================================================

def _http_get(url: str, api: bool = False) -> str:
    """GET a URL as text. `api=True` adds GitHub API headers (UA + optional token)."""
    headers = {"User-Agent": "TscgLayerCakeMCPServer"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _resolve_source(source: Optional[str]) -> str:
    src = (source or DEFAULT_SOURCE).lower()
    if src not in ("head", "local"):
        raise ValueError(f"source must be 'head' or 'local', got {source!r}")
    if src == "local" and not LOCAL_REPO:
        raise ValueError("source='local' requires TSCG_LOCAL_REPO to point at the repo root")
    return src


# ==============================================================================
# PURE-FUNCTION CORE  (no MCP dependency — testable, reusable)
# ==============================================================================

def list_tree(source: Optional[str] = None) -> list[str]:
    """
    Return every corpus file path, RELATIVE TO ontology/ (e.g.
    'M2_GenericConcepts.jsonld', 'M1_extensions/biology/M1_Biology.jsonld').
    Cached per source for the session.
    """
    src = _resolve_source(source)
    if src in _TREE_CACHE:
        return _TREE_CACHE[src]

    paths: list[str] = []
    if src == "head":
        # Strategy 1 — committed manifest on the raw CDN (no API, no rate limit).
        try:
            paths = json.loads(_http_get(RAW_BASE + ONTOLOGY_PREFIX + MANIFEST_PATH))
        except Exception:
            paths = []
        # Strategy 2 — GitHub tree API (live, needs the 60 req/h budget or a token).
        if not paths:
            try:
                data = json.loads(_http_get(GITHUB_TREE_API, api=True))
                if data.get("truncated"):
                    sys.stderr.write("[warn] GitHub tree response truncated; listing is partial.\n")
                paths = [
                    node["path"][len(ONTOLOGY_PREFIX):]
                    for node in data.get("tree", [])
                    if node.get("type") == "blob" and node.get("path", "").startswith(ONTOLOGY_PREFIX)
                ]
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    raise RuntimeError(
                        "Corpus listing failed: no _manifest.json on HEAD and the GitHub API "
                        "is rate-limited (60 req/h unauthenticated). Fix by committing a manifest "
                        "(python tscg_layercake_mcp_server.py --emit-manifest > ontology/_manifest.json) "
                        "or by setting GITHUB_TOKEN."
                    ) from e
                raise
    else:  # local
        root = Path(LOCAL_REPO) / "ontology"
        for f in root.rglob("*"):
            if f.is_file() and f.name != MANIFEST_PATH:
                paths.append(str(f.relative_to(root)).replace("\\", "/"))

    paths.sort()
    _TREE_CACHE[src] = paths
    return paths


def read_file(path: str, source: Optional[str] = None) -> str:
    """Return the raw text of one corpus file, given its ontology-relative path."""
    src = _resolve_source(source)
    path = path.strip().lstrip("/")
    key = (src, path)
    if key in _FILE_CACHE:
        return _FILE_CACHE[key]

    if src == "head":
        text = _http_get(RAW_BASE + ONTOLOGY_PREFIX + path)
    else:
        text = (Path(LOCAL_REPO) / "ontology" / path).read_text(encoding="utf-8")

    _FILE_CACHE[key] = text
    return text


def _layer_of(path: str) -> str:
    stem = Path(path).name.upper()
    for n in ("M3", "M2", "M1", "M0"):
        if stem.startswith(n + "_"):
            return n
    return "?"


def _source_priority(path: str) -> int:
    """Higher = more canonical (used as a search tiebreak)."""
    layer = {"M3": 40, "M2": 30, "M1": 20, "M0": 10}.get(_layer_of(path), 0)
    ext = {".jsonld": 2, ".json": 2, ".md": 1}.get(Path(path).suffix.lower(), 0)
    return layer + ext


def search(query: str, layer: Optional[str] = None, max_results: int = 8,
           source: Optional[str] = None) -> list[dict]:
    """
    Full-text search over .jsonld/.md corpus files. Returns a ranked list of
    {path, layer, matches, snippet} — paths + snippets, never whole files.
    That snippet-only return is the point: it is the lazy-loading win.

    NOTE: the first search of a session warms the file cache (fetches the
    candidate files once); subsequent searches are near-instant.
    """
    q = query.strip().lower()
    if not q:
        return []
    want_layer = layer.upper() if layer else None

    candidates = [
        p for p in list_tree(source)
        if Path(p).suffix.lower() in (".jsonld", ".json", ".md")
        and (want_layer is None or _layer_of(p) == want_layer)
    ]

    hits: list[dict] = []
    for p in candidates:
        try:
            text = read_file(p, source)
        except Exception:
            continue
        lines = text.splitlines()
        matched = [(i + 1, ln.strip()) for i, ln in enumerate(lines) if q in ln.lower()]
        if not matched:
            continue
        snippet = "\n".join(f"  L{n}: {ln[:200]}" for n, ln in matched[:3])
        hits.append({
            "path": p,
            "layer": _layer_of(p),
            "matches": len(matched),
            "snippet": snippet,
        })

    hits.sort(key=lambda h: (h["matches"], _source_priority(h["path"])), reverse=True)
    return hits[:max_results]


def _first_str(value) -> str:
    """Coerce an rdfs:label / rdfs:comment (str | {'@value':..} | list) to a string."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return value.get("@value", "")
    if isinstance(value, list) and value:
        return _first_str(value[0])
    return ""


def get_concept(name: str, source: Optional[str] = None) -> Optional[dict]:
    """
    Return a compact record for one M2 GenericConcept:
    {label, formula, definition, family, polarity, perspective, examples, id}.
    Matches on rdfs:label (case-insensitive) or on the @id suffix. Compact by
    design — the caller gets the concept, not the whole 143-entry file.
    """
    n = name.strip().lower()
    data = json.loads(read_file("M2_GenericConcepts.jsonld", source))
    for e in data.get("@graph", []):
        label = _first_str(e.get("rdfs:label", ""))
        cid = e.get("@id", "")
        suffix = cid.split(":")[-1] if cid else ""
        if label.lower() == n or suffix.lower() == n:
            fam = e.get("m2:hasFamily", "")
            examples = e.get("m2:hasExample", [])
            if isinstance(examples, str):
                examples = [examples]
            return {
                "id": cid,
                "label": label,
                # Live property name in the corpus (subscripted structural grammar):
                "formula": e.get("m2:hasStructuralGrammarFormula", ""),
                "definition": _first_str(e.get("rdfs:comment", "")),
                "family": fam,
                "polarity": e.get("m2:hasPolarity", ""),
                "perspective": e.get("m2:perspective", ""),
                "examples": [str(x) for x in examples[:5]],
            }
    return None


def list_extensions(source: Optional[str] = None) -> list[str]:
    """Return the M1 extension files (ontology-relative paths under M1_extensions/)."""
    return [
        p for p in list_tree(source)
        if p.startswith("M1_extensions/") and p.lower().endswith(".jsonld")
        and Path(p).name.upper().startswith("M1_")
    ]


def list_poclets(source: Optional[str] = None) -> list[str]:
    """Return the M0 instance/poclet files (M0_*.jsonld under instances/)."""
    return [
        p for p in list_tree(source)
        if "instances/" in p and Path(p).name.upper().startswith("M0_")
        and p.lower().endswith(".jsonld")
    ]


def resolve_iri(compact: str, source: Optional[str] = None) -> str:
    """
    Expand a compact TSCG IRI to a full absolute URI (IRIExpander logic).
    Strategies, in order:
      1. m1:extension:<domain>:<Local>  -> M1_extensions/<domain>/M1_<Domain>.jsonld#<Local>
      2. known-prefix table (m3:eagle_eye:, m3:sphinx_eye:, m3:, m2:, m1:)
      3. base-relative fallback
    Everything resolves against  .../main/ontology/ .
    """
    base = RAW_BASE + ONTOLOGY_PREFIX
    c = compact.strip()

    # Strategy 1 — M1 extension pattern
    if c.startswith("m1:extension:"):
        rest = c[len("m1:extension:"):]
        parts = rest.split(":", 1)
        if len(parts) == 2:
            domain, local = parts
            dom_cap = domain[:1].upper() + domain[1:]
            return f"{base}M1_extensions/{domain}/M1_{dom_cap}.jsonld#{local}"

    # Strategy 2 — known prefixes
    for prefix, target in _PREFIX_TABLE:
        if c.startswith(prefix):
            return base + target + c[len(prefix):]

    # Strategy 3 — base-relative fallback
    return base + c.lstrip(":")


def sparql(query: str, graphs: list[str], source: Optional[str] = None) -> str:
    """
    OPTIONAL / EXPERIMENTAL escape hatch. Loads the named JSON-LD files into a
    temporary rdflib graph and runs a SPARQL query. Prefer the task-shaped
    tools above; SPARQL is only worth it for structured queries they can't express.

    `graphs` is a list of ontology-relative paths to load, e.g.
    ["M2_GenericConcepts.jsonld", "M1_CoreConcepts.jsonld"].
    """
    try:
        import rdflib  # noqa: F401
    except ImportError:
        return ("[sparql unavailable] Install the optional dependency:\n"
                "    pip install rdflib\n"
                "(The production version can swap in pyoxigraph to match TscgStore.)")
    from rdflib import Graph
    g = Graph()
    for p in graphs:
        g.parse(data=read_file(p, source), format="json-ld")
    rows = g.query(query)
    out = [" | ".join(str(v) for v in row) for row in rows]
    return "\n".join(out) if out else "(no results)"


# ==============================================================================
# MCP WRAPPERS  (thin — all real work is in the pure functions above)
# ==============================================================================

def build_mcp():
    """Construct the FastMCP server. Imported lazily so --selftest needs no mcp install."""
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("TscgLayerCakeMCPServer")

    @mcp.tool()
    def tscg_get_file(path: str, source: str = "") -> str:
        """Return the raw text of one TSCG corpus file. `path` is relative to
        ontology/, e.g. 'M2_GenericConcepts.jsonld' or
        'M1_extensions/biology/M1_Biology.jsonld'. source: 'head' (default,
        authoritative) or 'local' (your working copy)."""
        return read_file(path, source or None)

    @mcp.tool()
    def tscg_search(query: str, layer: str = "", max_results: int = 8, source: str = "") -> str:
        """Full-text search the corpus. Returns paths + snippets (not whole files).
        Optional layer filter: 'M0'|'M1'|'M2'|'M3'."""
        hits = search(query, layer or None, max_results, source or None)
        if not hits:
            return "(no matches)"
        return "\n\n".join(
            f"[{h['layer']}] {h['path']}  ({h['matches']} match(es))\n{h['snippet']}"
            for h in hits
        )

    @mcp.tool()
    def tscg_get_concept(name: str, source: str = "") -> str:
        """Return a compact record for one M2 GenericConcept (formula, definition,
        family, examples). Matches on label or @id suffix, e.g. 'Layer'."""
        c = get_concept(name, source or None)
        if c is None:
            return f"(no GenericConcept named {name!r})"
        return json.dumps(c, ensure_ascii=False, indent=2)

    @mcp.tool()
    def tscg_list_extensions(source: str = "") -> str:
        """List the M1 domain extension files (paths under M1_extensions/)."""
        return "\n".join(list_extensions(source or None)) or "(none)"

    @mcp.tool()
    def tscg_list_poclets(source: str = "") -> str:
        """List the M0 instance / poclet files."""
        return "\n".join(list_poclets(source or None)) or "(none)"

    @mcp.tool()
    def tscg_resolve_iri(compact: str, source: str = "") -> str:
        """Expand a compact TSCG IRI (e.g. 'm3:eagle_eye:Attractor',
        'm1:extension:biology:CellularCommunication') to a full absolute URI."""
        return resolve_iri(compact, source or None)

    @mcp.tool()
    def tscg_sparql(query: str, graphs: list[str], source: str = "") -> str:
        """OPTIONAL last-resort. Run SPARQL over the named JSON-LD files.
        Prefer the task-shaped tools above for everyday use."""
        return sparql(query, graphs, source or None)

    return mcp


# ==============================================================================
# ENTRY POINT
# ==============================================================================

def _selftest() -> int:
    """Exercise the pure-function core against the configured source. No MCP needed."""
    print(f"Self-test — source={_resolve_source(None)}  ref={DEFAULT_REF}")
    tree = list_tree()
    print(f"  list_tree            : {len(tree)} files")
    exts = list_extensions()
    print(f"  list_extensions      : {len(exts)}  e.g. {exts[:2]}")
    pocs = list_poclets()
    print(f"  list_poclets         : {len(pocs)}  e.g. {[Path(p).name for p in pocs[:2]]}")
    print(f"  resolve_iri(m3:eagle_eye:Attractor):\n      {resolve_iri('m3:eagle_eye:Attractor')}")
    print(f"  resolve_iri(m1:extension:biology:CellularCommunication):\n      {resolve_iri('m1:extension:biology:CellularCommunication')}")
    c = get_concept("Layer")
    print(f"  get_concept('Layer') : {c['label'] if c else None}  formula={c['formula'] if c else None!r}")
    hits = search("attractor", layer="M2", max_results=3)
    print(f"  search('attractor', M2): {len(hits)} hit(s)  top={hits[0]['path'] if hits else None}")
    print("OK")
    return 0


def _emit_manifest() -> int:
    """Print the ontology-relative file list as JSON, for committing to ontology/_manifest.json.
    Uses the local working copy if TSCG_LOCAL_REPO is set (recommended — no API),
    otherwise the GitHub tree API."""
    src = "local" if LOCAL_REPO else "head"
    if src == "local":
        root = Path(LOCAL_REPO) / "ontology"
        paths = sorted(
            str(f.relative_to(root)).replace("\\", "/")
            for f in root.rglob("*")
            if f.is_file() and f.name != MANIFEST_PATH
        )
    else:
        data = json.loads(_http_get(GITHUB_TREE_API, api=True))
        paths = sorted(
            node["path"][len(ONTOLOGY_PREFIX):]
            for node in data.get("tree", [])
            if node.get("type") == "blob" and node.get("path", "").startswith(ONTOLOGY_PREFIX)
        )
    print(json.dumps(paths, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    if "--emit-manifest" in sys.argv:
        return _emit_manifest()
    if "--selftest" in sys.argv:
        return _selftest()
    build_mcp().run()  # stdio transport by default
    return 0


if __name__ == "__main__":
    sys.exit(main())
