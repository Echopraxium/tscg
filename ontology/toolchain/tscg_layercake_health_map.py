#!/usr/bin/env python3
"""
tscg_layercake_health_map.py — LayerCake Health Map: concentric hexagonal map of the
TSCG technical debt (snapshot). Renamed from tscg_debt_map.py (Michel, 2026-10-06).

Author : Echopraxium with the collaboration of Claude AI
Version: 0.4.0
Date   : 2026-10-06
Home   : ontology/toolchain/tscg_layercake_health_map.py

WHAT IT DRAWS
-------------
The Layer Cake seen from above, as an onion: M3 at the centre, then M2, M1, and M0
on the periphery (radius = layer, centre = abstract, periphery = concrete).
  * one HEX CELL per node (a top-level @graph node; one cell per instance in M0);
  * one META-HEXAGON per cluster of nodes (Michel, 2026-10-06):
      M3  Eagle Eye (Gt), Sphinx Eye (Gm), Bicephalous (Gs) on three axes 120° apart,
          Genesis (types / classes / properties) between them, the apex
          Grammar Foundation at the centre;
      M2  one cluster per m2:hasFamily, plus "meta-schema" (classes without family,
          ontology header) and "properties";
      M1  one cluster per file (CoreConcepts, Domains, one per extension domain);
      M0  one cell per instance (its checks are file-level), grouped by category;
  * cells keep a stable order (sorted by IRI) from one snapshot to the next, so a
    repaired node turns green IN PLACE; holes in a meta-hexagon are normal.

Colours (Michel, 2026-10-06):
  green   no finding on this node
  bright orange  the node's ONLY finding is bare keys (D1, the WS-1 vocabulary
          backlog): content dropped on JSON-LD expansion; shown apart so that it
          does not drown the other debt
  magenta other measured, frozen technical debt on this node (SHACL result, header gap,
          check_M1 / check_m0 failure, changelog vestige…) — contained, cannot grow
          silently
  red     the node is INVISIBLE or MISREAD by the tools, because of a FILE-level
          defect: @vocab (bare keys turned into fake standard terms), a root named
          graph, a file that a strict JSON-LD processor rejects, or a file with no
          owl:Ontology node (invisible to its grammar)
  grey    not measured

WHERE THE FINDINGS COME FROM (no new check is defined here; the map only ATTRIBUTES
the findings of the existing instruments to nodes):
  validator/checks/doc.py      D1 bare keys (per owner node), D2–D7
  validator/checks/shacl_runner + the grammars registered per layer (focus nodes)
  validator/checks/ext.py      G1b, G5 (G6 is the consequence of D2: file-level red)
  check-M1/check_M1.py         per-file issues; the node is named in the message
  check-M0/check_m0_instances  per-instance checks C01–C15
LINKS (0.2.0) — drawn only where the data carries a relation (Michel, 2026-10-06):
  M0 -> M1  an instance -> the M1 domain files it imports or cites (CoreConcepts,
            shared by every instance, is implied and not drawn)
  M1 -> M2  a domain -> the families of the M2 concepts it MOBILISES
            (m2:mobilizes, m1:comboOf, m1:instantiatesGenericConcept). Typing
            (@type / rdfs:subClassOf to m2:DomainConceptCombo …) is NOT usage.
  M2 -> M3  a family -> the three Eyes, weighted by the share of Gt / Gm / Gs
            primitives in its formulas (Eagle Eye = Gt, Sphinx Eye = Gm,
            Bicephalous = Gs) — the monoidal composition (WS-3)
  Stroke width = weight; hover a link for its detail.
  PLACEMENT (0.3.0): each ring is ordered by the weighted circular mean of the angles
  of what its clusters link to in the ring INSIDE it (barycentre ordering, the
  classic crossing reduction for layered graphs): M2 by the Eyes, M1 by its
  families, M0 by its domains. Clusters without an inward link go last. An M1
  domain with NO link to M2 gets a dashed outline: its combos do not name M2
  concepts (they still carry monoidal formulas — SC-6 / DCC006).
DETECTION ONLY: nothing is written to the corpus. The numbers printed in the footer
are read from golden_values.json (the authority), never typed in.

USAGE
-----
  python tscg_layercake_health_map.py            # snapshot into ontology/docs/_01_Worksite/LayerCakeHealthMap/
  python tscg_layercake_health_map.py --out DIR --no-png
"""

from __future__ import annotations

import argparse
import collections
import datetime
import html
import json
import logging
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "validator"))
sys.path.insert(0, str(HERE / "check-M1"))
from tscg_paths import REPO_ROOT  # noqa: E402
from sources import Source, classify_layer  # noqa: E402
from checks import doc as doc_check, shacl_runner, ext as ext_check  # noqa: E402

logging.getLogger("rdflib").setLevel(logging.ERROR)

__version__ = "0.4.0"
GREEN, PALE, ORANGE, RED, GREY = "green", "pale", "orange", "red", "grey"
# Palette (Michel, 2026-10-06): bright orange = bare keys, magenta = other technical debt.
COLOR = {GREEN: "#3f9e5a", PALE: "#ff8a00", ORANGE: "#c4268f", RED: "#d8322a", GREY: "#b9b9b9"}
FILE_RED = {"D2": "@vocab: bare keys become fake standard terms",
            "D3": "root named graph: invisible to the default graph",
            "D7": "rejected by a strict JSON-LD 1.1 processor"}

M3_CLUSTER_OF_FILE = {
    "M3_EagleEye.jsonld": "Eagle Eye · Gt",
    "M3_SphinxEye.jsonld": "Sphinx Eye · Gm",
    "M3_BicephalousPerspective.jsonld": "Bicephalous · Gs",
    "M3_GrammarFoundation.jsonld": "Grammar Foundation (apex)",
}


# ── data model ─────────────────────────────────────────────────────────────────────

class Node:
    def __init__(self, nid: str, iri: str, layer: str, cluster: str, file: str):
        self.id, self.iri, self.layer, self.cluster, self.file = nid, iri, layer, cluster, file
        self.findings: List[str] = []
        self.file_red: List[str] = []

    @property
    def status(self) -> str:
        if self.file_red:
            return RED
        if not self.findings:
            return GREEN
        return PALE if all(f.startswith("D1 ") for f in self.findings) else ORANGE


def _types(n: Dict[str, Any]) -> List[str]:
    t = n.get("@type", [])
    return [x for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)]


def expand(cid: str, ctx: Dict[str, Any]) -> str:
    """Compact id -> IRI with the file's own prefixes (prefix = text before 1st ':')."""
    if re.match(r"^[a-z][a-z0-9+.-]*://", cid):
        return cid
    if ":" in cid:
        pfx, local = cid.split(":", 1)
        base = ctx.get(pfx)
        base = base.get("@id") if isinstance(base, dict) else base
        if isinstance(base, str):
            return base + local
    b = ctx.get("@base")
    return (b or "") + cid


# ── clustering ─────────────────────────────────────────────────────────────────────

def m3_cluster(fname: str, node: Dict[str, Any]) -> str:
    if fname in M3_CLUSTER_OF_FILE:
        return M3_CLUSTER_OF_FILE[fname]
    ts = _types(node)
    if "skos:Concept" in ts or "skos:ConceptScheme" in ts or "skos:inScheme" in node:
        return "Genesis · types"
    if any("Property" in t for t in ts):
        return "Genesis · properties"
    return "Genesis · classes"


def m2_cluster(node: Dict[str, Any]) -> str:
    ts = _types(node)
    if any("Property" in t for t in ts):
        return "properties"
    fam = node.get("m2:hasFamily")
    if isinstance(fam, list):
        fam = fam[0] if fam else None
    if isinstance(fam, dict):
        fam = fam.get("@id")
    if isinstance(fam, str):
        return fam.split(":", 1)[-1]
    return "meta-schema"


def m1_cluster(fname: str) -> str:
    return fname[3:-7] if fname.startswith("M1_") else fname


# ── attribution of findings ────────────────────────────────────────────────────────

def bare_keys_per_node(node: Dict[str, Any], terms: set) -> int:
    count = [0]

    def cb(k, _v, _nid):
        if not (k.startswith("@") or ":" in k or k in terms):
            count[0] += 1

    doc_check._walk(node, cb)
    return count[0]


def collect_ontology_layer(src: Source, layer: str, files: List[str]) -> List[Node]:
    nodes: List[Node] = []
    by_iri: Dict[str, Node] = {}
    for rel in files:
        text = src.read(rel)
        d = json.loads(text)
        ctx = d.get("@context", {}) if isinstance(d.get("@context"), dict) else {}
        terms = {k for k in ctx if not k.startswith("@")}
        fname = rel.rsplit("/", 1)[-1]
        file_nodes: List[Node] = []
        header: Optional[Node] = None
        for n in d.get("@graph", []):
            if not (isinstance(n, dict) and isinstance(n.get("@id"), str)):
                continue
            cl = (m3_cluster(fname, n) if layer == "M3" else
                  m2_cluster(n) if layer == "M2" else m1_cluster(fname))
            node = Node(n["@id"], expand(n["@id"], ctx), layer, cl, rel)
            if "owl:Ontology" in _types(n):
                header = node
                if layer == "M2":
                    node.cluster = "meta-schema"
            k = bare_keys_per_node(n, terms)
            if k:
                node.findings.append(f"D1 bare keys x{k}")
            file_nodes.append(node)
            by_iri[node.iri] = node
        if header is None and file_nodes:
            for x in file_nodes:
                x.file_red.append("no owl:Ontology node: invisible to its grammar")
        # document plane, file- and node-level
        for f in doc_check.run(rel, text, layer):
            cid = f["id"]
            if cid == "D1":
                continue
            if cid in FILE_RED or cid == "D0":
                for x in file_nodes:
                    x.file_red.append(f"{cid}: {FILE_RED.get(cid, f['message'][:80])}")
                continue
            target = next((x for x in file_nodes if x.id == f["node"]), header)
            if target is not None:
                target.findings.append(f"{cid}: {f['message'][:90]}")
        nodes.extend(file_nodes)

    # SHACL: grammars registered for the layer
    for g in shacl_runner.GRAMMARS.get(layer, []):
        pairs = [(rel, src.read(rel)) for rel in files]
        findings, _s = shacl_runner.run(g, src.read(g), pairs, layer)
        for f in findings:
            if f["id"] != "SHACL-V":
                continue
            target = by_iri.get(f["node"])
            if target is None:   # blank node (e.g. a changelog entry): file header
                target = next((x for x in nodes if x.file == f["file"]
                               and x.cluster in ("meta-schema",) or x.file == f["file"]), None)
            if target is not None:
                target.findings.append(f"SHACL {f.get('shape', '?')}: {f['message'][:90]}")

    # EXT (G1b, G5). G6 is the consequence of @vocab (D2) and already makes the file red.
    if layer in ("M3", "M2"):
        triples = [(rel, src.read(rel), layer) for rel in files]
        ef, _ = ext_check.run(triples, src.read(ext_check.SCHEME_HOST), src.read(ext_check.APEX))
        for f in ef:
            if f["id"] in ("G1b",):
                t = by_iri.get(f["node"])
                if t:
                    t.findings.append(f"G1b: {f['message'][:90]}")
    return nodes


def attach_check_m1(nodes: List[Node]) -> None:
    import check_M1  # noqa: E402
    by_file = collections.defaultdict(list)
    for n in nodes:
        by_file[n.file].append(n)
    for rel, fnodes in by_file.items():
        checker = check_M1.M1Checker(REPO_ROOT / rel, dry_run=True)
        try:
            import contextlib, io
            with contextlib.redirect_stdout(io.StringIO()):
                checker.run()
        except Exception as exc:
            for x in fnodes:
                x.findings.append(f"check_M1 crashed: {exc}")
            continue
        ids = {x.id: x for x in fnodes}
        header = next((x for x in fnodes if "Ontology" in x.cluster), None) or fnodes[0]
        for issue in checker.issues:
            if issue.severity == "INFO":
                continue
            m = re.search(r"(m[0-3]:[\w:.\-]+)", issue.message)
            target = ids.get(m.group(1).rstrip(".:")) if m else None
            (target or header).findings.append(f"{issue.code}: {issue.message[:90]}")


def collect_m0(src: Source, files: List[str]) -> List[Node]:
    tmp = Path(tempfile.mkdtemp()) / "m0.json"
    script = HERE / "check-M0" / "check_m0_instances.py"
    subprocess.run([sys.executable, str(script), "--json", str(tmp)], cwd=script.parent,
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    reports = {}
    if tmp.exists():
        for r in json.loads(tmp.read_text(encoding="utf-8")).get("instances", []):
            reports[Path(r["path"]).name] = r
    nodes: List[Node] = []
    for rel in files:
        fname = rel.rsplit("/", 1)[-1]
        parts = rel.split("/")
        category = parts[1] if len(parts) > 2 else "?"
        n = Node(fname[3:-7], rel, "M0", f"{category}/{fname[3:-7]}", rel)
        text = src.read(rel)
        for f in doc_check.run(rel, text, "M0"):
            if f["id"] in FILE_RED:
                n.file_red.append(f"{f['id']}: {FILE_RED[f['id']]}")
        try:
            d = json.loads(text)
            if not any("owl:Ontology" in _types(x) for x in d.get("@graph", []) if isinstance(x, dict)):
                n.file_red.append("no owl:Ontology node: invisible to its grammar")
        except Exception:
            n.file_red.append("not parseable JSON")
        r = reports.get(fname)
        if r is None:
            n.findings.append("not reported by check_m0_instances (not measured)")
        else:
            for c in r["checks"]:
                if c["status"] in ("FAIL", "WARN"):
                    n.findings.append(f"{c['code']} {c['name']}: {str(c['detail'])[:80]}")
        nodes.append(n)
    return nodes


# ── relations between clusters ─────────────────────────────────────────────────────

USES_KEYS = ("m2:mobilizes", "m1:comboOf", "m1:instantiatesGenericConcept")
GRAMMAR_ALPHABET = {"Gt": {"A", "St", "F", "It", "D"},
                    "Gm": {"R", "E", "V", "O", "Im"},
                    "Gs": {"T", "K", "Ss", "L", "_^", "_$", "_0"}}
EYE_OF = {"Gt": "Eagle Eye · Gt", "Gm": "Sphinx Eye · Gm", "Gs": "Bicephalous · Gs"}


def compute_edges(src: Source, by_layer: Dict[str, List[str]]) -> List[Tuple[tuple, tuple, float, str]]:
    edges: List[Tuple[tuple, tuple, float, str]] = []
    m2 = json.loads(src.read("ontology/M2_GenericConcepts.jsonld"))
    family: Dict[str, str] = {}
    formulas: Dict[str, List[str]] = collections.defaultdict(list)
    for n in m2.get("@graph", []):
        if not (isinstance(n, dict) and isinstance(n.get("@id"), str)):
            continue
        fam = n.get("m2:hasFamily")
        fam = fam[0] if isinstance(fam, list) and fam else fam
        fam = fam.get("@id") if isinstance(fam, dict) else fam
        if isinstance(fam, str) and not any("Property" in x for x in _types(n)):
            family[n["@id"]] = fam.split(":", 1)[-1]
            f = n.get("m2:hasStructuralGrammarFormula")
            for x in (f if isinstance(f, list) else [f] if f else []):
                if isinstance(x, str):
                    formulas[family[n["@id"]]].append(x)

    # M2 -> M3: monoidal composition of each family's formulas
    tok2g = {tok: g for g, toks in GRAMMAR_ALPHABET.items() for tok in toks}
    for fam, fs in formulas.items():
        c: collections.Counter = collections.Counter()
        for f in fs:
            for tok in re.findall(r"_\^|_\$|_0|[A-Z][a-z]?", f):
                if tok in tok2g:
                    c[tok2g[tok]] += 1
        tot = sum(c.values())
        for g, k in c.items():
            edges.append((("M2", fam), ("M3", EYE_OF[g]), k / tot * len(fs),
                          f"M2 {fam} -> {EYE_OF[g]}: {k}/{tot} primitives of {len(fs)} formula(s) are {g}"))

    # M1 -> M2: concepts mobilised, by family
    for rel in by_layer["M1"]:
        d = json.loads(src.read(rel))
        c = collections.Counter()

        def walk(o, key=None):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k != "@context":
                        walk(v, k)
            elif isinstance(o, list):
                for v in o:
                    walk(v, key)
            else:
                val = o if isinstance(o, str) else None
                if val in family and (key in USES_KEYS or (key or "").endswith(":comboOf")):
                    c[family[val]] += 1

        for n in d.get("@graph", []):
            if isinstance(n, dict):
                for k, v in n.items():
                    if k in USES_KEYS or k.endswith(":comboOf"):
                        for x in (v if isinstance(v, list) else [v]):
                            x = x.get("@id") if isinstance(x, dict) else x
                            if x in family:
                                c[family[x]] += 1
        stem = m1_cluster(rel.rsplit("/", 1)[-1])
        for fam, k in c.items():
            edges.append((("M1", stem), ("M2", fam), float(k),
                          f"M1 {stem} -> M2 {fam}: mobilises {k} concept reference(s)"))

    # M0 -> M1: domain files imported or cited (CoreConcepts implied)
    m1_files = {rel.rsplit("/", 1)[-1]: m1_cluster(rel.rsplit("/", 1)[-1]) for rel in by_layer["M1"]}
    slug = {re.sub(r"[^a-z]", "", v.lower()): v for v in m1_files.values()}
    for rel in by_layer["M0"]:
        text = src.read(rel)
        fname = rel.rsplit("/", 1)[-1]
        parts = rel.split("/")
        key = ("M0", f"{parts[1] if len(parts) > 2 else '?'}/{fname[3:-7]}")
        targets = {v for f, v in m1_files.items() if f in text}
        for s in re.findall(r"m1:extension:([a-z_]+):", text):
            if re.sub(r"[^a-z]", "", s) in slug:
                targets.add(slug[re.sub(r"[^a-z]", "", s)])
        for tgt in sorted(targets - {"CoreConcepts"}):
            edges.append((key, ("M1", tgt), 1.0, f"M0 {fname[3:-7]} -> M1 {tgt}"))
    return edges


# ── hex geometry ───────────────────────────────────────────────────────────────────

def spiral(n: int) -> List[Tuple[int, int]]:
    """Axial coordinates of n cells, centre first, then ring by ring."""
    cells = [(0, 0)]
    dirs = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    k = 1
    while len(cells) < n:
        q, r = -k, k                      # start of ring k (direction 4 * k)
        for d in range(6):
            for _ in range(k):
                cells.append((q, r))
                q, r = q + dirs[d][0], r + dirs[d][1]
        k += 1
    return cells[:n]


def ring_of(n: int) -> int:
    k = 0
    while 1 + 3 * k * (k + 1) < n:
        k += 1
    return k


def hex_points(cx: float, cy: float, s: float) -> str:
    return " ".join(f"{cx + s * math.cos(math.radians(60 * i + 30)):.1f},"
                    f"{cy + s * math.sin(math.radians(60 * i + 30)):.1f}" for i in range(6))


def axial_to_xy(q: int, r: int, s: float) -> Tuple[float, float]:
    return s * math.sqrt(3) * (q + r / 2), s * 1.5 * r


# ── rendering ──────────────────────────────────────────────────────────────────────

def render(nodes: List[Node], golden: Dict[str, Any], head: str, out_svg: Path,
           edges: Optional[List[Tuple[tuple, tuple, float, str]]] = None) -> Dict[str, Any]:
    S = 6.0                                     # cell circumradius
    clusters: Dict[Tuple[str, str], List[Node]] = collections.OrderedDict()
    for n in sorted(nodes, key=lambda x: (x.layer, x.cluster, x.iri)):
        clusters.setdefault((n.layer, n.cluster), []).append(n)

    def radius(members: List[Node], layer: str) -> float:
        if layer == "M0":
            return S * 2.2
        return (ring_of(len(members)) + 0.6) * S * math.sqrt(3) + 4

    placed: List[Tuple[Tuple[str, str], float, float, float]] = []
    # M3: apex at the centre, 6 around it (3 eyes on the 3 axes, Genesis in between)
    m3_order = ["Eagle Eye · Gt", "Genesis · types", "Sphinx Eye · Gm",
                "Genesis · classes", "Bicephalous · Gs", "Genesis · properties"]
    m3 = {k[1]: v for k, v in clusters.items() if k[0] == "M3"}
    apex = "Grammar Foundation (apex)"
    r_apex = radius(m3.get(apex, []), "M3")
    placed.append((("M3", apex), 0.0, 0.0, r_apex))
    r_sat = max(radius(m3[c], "M3") for c in m3_order if c in m3)
    ring_r = max(r_apex + r_sat + 44, 2 * r_sat + 24)
    for i, c in enumerate(m3_order):
        if c not in m3:
            continue
        a = math.radians(-90 + 60 * i)
        placed.append((("M3", c), ring_r * math.cos(a), ring_r * math.sin(a), radius(m3[c], "M3")))
    outer = ring_r + max(radius(m3[c], "M3") for c in m3_order if c in m3)

    ring_meta = {"M3": (0.0, outer)}
    for layer in ("M2", "M1", "M0"):
        items = [(k, v) for k, v in clusters.items() if k[0] == layer]
        placed_angle = {k: math.atan2(y, x) for k, x, y, _r in placed}

        def bary(k):
            sx = sy = 0.0
            for a, b, w, _l in (edges or []):
                if a == k and b in placed_angle:
                    sx += w * math.cos(placed_angle[b])
                    sy += w * math.sin(placed_angle[b])
            if sx == 0 and sy == 0:
                return None
            return math.atan2(sy, sx) % (2 * math.pi)

        keyed = [(bary(k), k, v) for k, v in items]
        linked = sorted([x for x in keyed if x[0] is not None], key=lambda x: x[0])
        unlinked = sorted([x for x in keyed if x[0] is None],
                          key=lambda x: (x[2][0].cluster if layer == "M0" else -len(x[2])))
        items = [(k, v) for _b, k, v in linked + unlinked]
        start_angle = linked[0][0] if linked else -math.pi / 2
        rads = [radius(v, layer) for _k, v in items]
        gap = 10 if layer != "M0" else 6
        need = sum(2 * x + gap for x in rads) / (2 * math.pi)
        R = max(outer + max(rads) + 34, need)
        total = sum(2 * x + gap for x in rads)
        ang = start_angle - (2 * rads[0] + gap) / total * math.pi
        for (k, v), rad in zip(items, rads):
            step = (2 * rad + gap) / total * 2 * math.pi
            a = ang + step / 2
            placed.append((k, R * math.cos(a), R * math.sin(a), rad))
            ang += step
        ring_meta[layer] = (R - max(rads), R + max(rads))
        outer = R + max(rads)

    W = 2 * (outer + 150)
    cx0 = cy0 = W / 2
    out: List[str] = []
    H = W + 170
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" '
               f'viewBox="0 0 {W:.0f} {H:.0f}" font-family="Helvetica, Arial, sans-serif">')
    out.append(f'<rect width="100%" height="100%" fill="#fbfaf7"/>')
    # layer rings (guides)
    for layer, (r0, r1) in ring_meta.items():
        rm = (r0 + r1) / 2 if layer != "M3" else r1 / 2
        out.append(f'<circle cx="{cx0:.0f}" cy="{cy0:.0f}" r="{(r1 + 8 if layer != "M3" else r1 + 8):.0f}" '
                   f'fill="none" stroke="#d9d5cc" stroke-dasharray="3 5"/>')
        out.append(f'<text x="{cx0 + 6:.0f}" y="{cy0 - (r1 + 12):.0f}" font-size="13" '
                   f'fill="#8a857a" font-weight="bold">{layer}</text>')

    # links, drawn UNDER the bricks
    pos = {k: (cx0 + x, cy0 + y, rad) for k, x, y, rad in placed}
    if edges:
        wmax = max(w for *_x, w, _l in edges) or 1.0
        colour = {"M0": "#6f8fb3", "M1": "#7d74a8", "M2": "#4f9a9a"}
        out.append('<g fill="none" stroke-linecap="round">')
        for a, b, w, label in edges:
            if a not in pos or b not in pos:
                continue
            (x1, y1, _r1), (x2, y2, _r2) = pos[a], pos[b]
            # control point pulled toward the centre: links follow the onion inward
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            qx, qy = mx + (cx0 - mx) * 0.25, my + (cy0 - my) * 0.25
            sw = 0.6 + 4.0 * math.sqrt(w / wmax)
            out.append(f'<path d="M{x1:.1f},{y1:.1f} Q{qx:.1f},{qy:.1f} {x2:.1f},{y2:.1f}" '
                       f'stroke="{colour.get(a[0], "#888")}" stroke-width="{sw:.2f}" '
                       f'stroke-opacity="0.32"><title>{html.escape(label)}</title></path>')
        out.append('</g>')

    stats: Dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for (layer, name), x, y, rad in placed:
        members = clusters[(layer, name)]
        px, py = cx0 + x, cy0 + y
        if layer == "M0":
            n = members[0]
            tip = html.escape(f"{n.file}\n" + "\n".join(n.file_red + n.findings or ["no finding"]))
            out.append(f'<polygon points="{hex_points(px, py, S * 2.1)}" fill="{COLOR[n.status]}" '
                       f'stroke="#fbfaf7" stroke-width="1"><title>{tip}</title></polygon>')
            stats[layer][n.status] += 1
            a = math.atan2(y, x)
            lx, ly = cx0 + (math.hypot(x, y) + S * 3.2) * math.cos(a), cy0 + (math.hypot(x, y) + S * 3.2) * math.sin(a)
            deg = math.degrees(a)
            flip = 90 < deg % 360 < 270
            anchor = "end" if flip else "start"
            rot = deg + 180 if flip else deg
            out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="7.5" fill="#55524b" '
                       f'text-anchor="{anchor}" dominant-baseline="middle" '
                       f'transform="rotate({rot:.1f} {lx:.1f} {ly:.1f})">{html.escape(n.id)}</text>')
            continue
        # M1_Domains is the domain REGISTRY, not a domain with combos: no M2 link expected.
        no_down = (layer == "M1" and name != "Domains" and edges is not None
                   and not any(a == (layer, name) and b[0] == "M2" for a, b, _w, _l in edges))
        dash = ' stroke-dasharray="4 3" stroke-width="1.6"' if no_down else ""
        out.append(f'<polygon points="{hex_points(px, py, rad)}" fill="#efece4" '
                   f'stroke="{"#8a857a" if no_down else "#cfcabd"}"{dash}>'
                   + (f'<title>{html.escape(name)}: no link to any M2 concept — its combos still '
                      f'carry monoidal formulas instead of named concepts (SC-6 / DCC006)</title>'
                      if no_down else "") + '</polygon>')
        for (q, r), n in zip(spiral(len(members)), members):
            dx, dy = axial_to_xy(q, r, S)
            tip = html.escape(f"{n.id}\n" + "\n".join(n.file_red + n.findings or ["no finding"]))
            out.append(f'<polygon points="{hex_points(px + dx, py + dy, S * 0.93)}" '
                       f'fill="{COLOR[n.status]}"><title>{tip}</title></polygon>')
            stats[layer][n.status] += 1
        g = sum(1 for n in members if n.status == GREEN)
        out.append(f'<text x="{px:.1f}" y="{py + rad + 11:.1f}" font-size="9" text-anchor="middle" '
                   f'fill="#3b3934">{html.escape(name)}</text>')
        out.append(f'<text x="{px:.1f}" y="{py + rad + 21:.1f}" font-size="8" text-anchor="middle" '
                   f'fill="#77736a">{g}/{len(members)} green</text>')

    # legend + footer
    y0 = W + 10
    out.append(f'<text x="30" y="{y0 + 10:.0f}" font-size="18" font-weight="bold" fill="#2b2a26">'
               f'TSCG — LayerCake Health Map (snapshot)</text>')
    out.append(f'<text x="30" y="{y0 + 30:.0f}" font-size="11" fill="#55524b">'
               f'{datetime.date.today()} · HEAD {head} · tscg_layercake_health_map {__version__} · centre = M3 '
               f'(abstract), periphery = M0 (concrete) · one cell per node (one per instance in M0) · '
               f'hover a cell for its findings, a link for its detail</text>')
    out.append(f'<text x="30" y="{y0 + 76:.0f}" font-size="10.5" fill="#55524b">links: '
               f'<tspan fill="#6f8fb3">M0 → M1 domain files used</tspan> (CoreConcepts implied) · '
               f'<tspan fill="#7d74a8">M1 → M2 families of the concepts mobilised</tspan> · '
               f'<tspan fill="#4f9a9a">M2 → M3 Eyes by Gt / Gm / Gs share of the formulas</tspan> · '
               f'width = weight · dashed M1 outline = no link to M2 (SC-6)</text>')
    lx = 30
    for st, label in ((GREEN, "no finding"), (PALE, "bare keys only (WS-1 vocabulary)"),
                      (ORANGE, "other technical debt (measured, frozen)"),
                      (RED, "invisible / misread by the tools (file-level)"), (GREY, "not measured")):
        out.append(f'<polygon points="{hex_points(lx + 7, y0 + 52, 7)}" fill="{COLOR[st]}"/>')
        out.append(f'<text x="{lx + 18}" y="{y0 + 56:.0f}" font-size="11" fill="#3b3934">{label}</text>')
        lx += 18 + 6 * len(label) + 22
    yy = y0 + 100
    for layer in ("M3", "M2", "M1", "M0"):
        gv = golden.get(layer, {})
        c = stats[layer]
        tot = sum(c.values())
        out.append(f'<text x="30" y="{yy:.0f}" font-size="11" fill="#3b3934">'
                   f'<tspan font-weight="bold">{layer}</tspan>  cells {tot}: '
                   f'{c[GREEN]} green · {c[PALE]} bare keys · {c[ORANGE]} other debt · {c[RED]} red'
                   f'    |    gate (golden_values.json): files {gv.get("files", "?")} · errors '
                   f'{gv.get("errors", "?")} · warnings {gv.get("warnings", "?")} · SHACL '
                   f'{gv.get("shacl_violations", "?")}</text>')
        yy += 16
    out.append("</svg>")
    # no trailing blanks (truncated messages inside tooltips): clean diffs and patches
    out_svg.write_text("\n".join("\n".join(x.rstrip() for x in s.split("\n")) for s in out) + "\n",
                       encoding="utf-8")
    return {k: dict(v) for k, v in stats.items()}


def to_png(svg: Path, png: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    import re as _re
    m = _re.search(r'width="(\d+)" height="(\d+)"', svg.read_text(encoding="utf-8")[:300])
    w, h = (int(m.group(1)), int(m.group(2))) if m else (1600, 1700)
    page = ("<!doctype html><html><body style='margin:0;background:#fbfaf7'>"
            + svg.read_text(encoding="utf-8") + "</body></html>")
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--disable-gpu"])
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1.5)
        pg.set_content(page, wait_until="domcontentloaded")
        pg.locator("svg").first.screenshot(path=str(png), animations="disabled", timeout=120000)
        b.close()
    return True


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="TSCG LayerCake Health Map (concentric hex snapshot)")
    ap.add_argument("--out", default=str(REPO_ROOT / "ontology/docs/_01_Worksite/LayerCakeHealthMap"))
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args(argv)

    src = Source("local")
    manifest = src.manifest()
    by_layer = collections.defaultdict(list)
    for rel in manifest:
        lay = classify_layer(rel)
        if lay:
            by_layer[lay].append(rel)

    nodes: List[Node] = []
    for layer in ("M3", "M2", "M1"):
        ln = collect_ontology_layer(src, layer, sorted(by_layer[layer]))
        if layer == "M1":
            attach_check_m1(ln)
        nodes += ln
    nodes += collect_m0(src, sorted(by_layer["M0"]))

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO_ROOT,
                          capture_output=True, text=True).stdout.strip() or "?"
    golden = json.loads((HERE / "golden_values.json").read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = f"TSCG_LayerCake_Health_Map_{datetime.date.today()}_{head}"
    svg = out / f"{stem}.svg"
    edges = compute_edges(src, by_layer)
    stats = render(nodes, golden, head, svg, edges)
    print(f"links: {len(edges)}")
    print(f"SVG: {svg}")
    for layer in ("M3", "M2", "M1", "M0"):
        print(f"  {layer}: {stats.get(layer, {})}")
    if not args.no_png:
        png = out / f"{stem}.png"
        print(f"PNG: {png}" if to_png(svg, png) else "PNG: skipped (playwright not installed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
