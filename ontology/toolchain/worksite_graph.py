#!/usr/bin/env python3
"""
worksite_graph.py — the Worksites dependency graph, as an SVG, from worksite.yaml.

Author : Echopraxium with the collaboration of Claude AI
Version: 0.2.0
Home   : ontology/toolchain/worksite_graph.py

Reads the worksite state layer (worksite.yaml + _01_Worksite/WS-*/worksite.yaml, through
worksite_report.load()) and draws one box per worksite and one arrow per declared
dependency. Only the structured field `depends_on` is read, never the prose notes: a
dependency that is not declared is not drawn.

    depends_on:
      - { ws: WS-5, kind: hard, why: "..." }   # hard | soft | batched

Layout: one horizontal band per cluster (connected worksites; those with no dependency
form a last "Independent" band), so no edge crosses another cluster. Inside a band,
columns by depth (one column right of the deepest prerequisite, `batched` does not
count), rows by barycentre of the prerequisites then priority (1 first; unset, mixed,
done last); an edge that skips a column runs in the corridor between two rows.
Arrows go from the prerequisite to the worksite that waits for it.

Checks (exit 1, nothing written): a `depends_on` naming an unknown worksite, an unknown
kind, or a cycle among hard / soft dependencies.

Usage
-----
  python worksite_graph.py                       # writes worksites_dependency_graph.svg here
  python worksite_graph.py --out <dir>           # into <dir>
  python worksite_graph.py --check               # checks only
"""

from __future__ import annotations

import argparse
import datetime
import html
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worksite_report  # noqa: E402  (shares the loader: one source of truth)

KINDS = ("hard", "soft", "batched")
STATUS_FILL = {   # light fill, dark stroke per status
    "done": ("#e3efe3", "#5b8a5b"), "partial": ("#fdf0d8", "#b07d1e"),
    "scoped": ("#e6eef8", "#4a6f9c"), "design-decided": ("#e6eef8", "#4a6f9c"),
    "staged": ("#efe6f6", "#7a5596"), "todo": ("#f1f1ef", "#77756f"),
    "blocked": ("#f8e3e1", "#a8473d"),
}
BOX_W, BOX_H, COL_GAP, ROW_GAP, MARGIN = 230, 64, 96, 30, 30


def prio_key(ws: dict):
    p = ws.get("priority")
    if isinstance(p, int):
        return (0, p, ws["id"])
    return (1, 0 if p is None else 1 if p == "mixed" else 2, ws["id"])


def edges_of(doc: dict) -> tuple[list, list]:
    ids = {w["id"] for w in doc["worksites"]}
    edges, errors = [], []
    for w in doc["worksites"]:
        for d in w.get("depends_on") or []:
            pre, kind = d.get("ws"), d.get("kind", "hard")
            if pre not in ids:
                errors.append(f"{w['id']}: depends_on names an unknown worksite {pre!r}")
            elif kind not in KINDS:
                errors.append(f"{w['id']}: unknown dependency kind {kind!r} (allowed: {', '.join(KINDS)})")
            else:
                edges.append((pre, w["id"], kind, d.get("why", "")))
    return edges, errors


def depths(doc: dict, edges: list) -> tuple[dict, list]:
    """Column of each worksite = 1 + depth of its deepest hard/soft prerequisite."""
    pre = {w["id"]: [a for a, b, k, _ in edges if b == w["id"] and k != "batched"] for w in doc["worksites"]}
    depth, state, errors = {}, {}, []

    def visit(n, path):
        if state.get(n) == "done":
            return depth[n]
        if state.get(n) == "open":
            errors.append("cycle: " + " -> ".join(path + [n]))
            return 0
        state[n] = "open"
        depth[n] = 1 + max((visit(p, path + [n]) for p in pre[n]), default=-1)
        state[n] = "done"
        return depth[n]

    for n in pre:
        visit(n, [])
    return depth, errors


def wrap(text: str, width: int = 30) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    return lines[:2] if len(lines) <= 2 else [lines[0], lines[1][: width - 1] + "…"]


def head_sha() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                              cwd=Path(__file__).resolve().parent).stdout.strip() or "?"
    except Exception:
        return "?"


def clusters_of(doc: dict, edges: list) -> list[list[dict]]:
    """Weakly connected components (any kind of edge). Worksites with no dependency at all
    form one last cluster, "Independent". Clusters ordered by their best priority."""
    parent = {w["id"]: w["id"] for w in doc["worksites"]}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b, _, _ in edges:
        parent[find(a)] = find(b)
    groups: dict[str, list] = {}
    for w in doc["worksites"]:
        groups.setdefault(find(w["id"]), []).append(w)
    linked = [g for g in groups.values() if len(g) > 1]
    alone = [g[0] for g in groups.values() if len(g) == 1]
    linked.sort(key=lambda g: min(prio_key(w) for w in g))
    return linked + ([sorted(alone, key=prio_key)] if alone else [])


def render(doc: dict, edges: list, depth: dict) -> str:
    """Clusters are horizontal bands: no edge ever crosses another cluster. Inside a band,
    columns by depth, rows by barycentre of the prerequisites (then priority), and an edge
    that skips a column runs in the empty corridor between two rows, never behind a box."""
    ncols = max(depth.values()) + 1
    width = MARGIN * 2 + ncols * BOX_W + (ncols - 1) * COL_GAP
    pre = {}
    for a, b, k, _ in edges:
        if k != "batched":
            pre.setdefault(b, []).append(a)
    pos, bands, y = {}, [], MARGIN + 62
    for ci, group in enumerate(clusters_of(doc, edges)):
        ids = {w["id"] for w in group}
        independent = not any(a in ids or b in ids for a, b, _, _ in edges)
        cells: dict[tuple, str] = {}
        if independent:          # no edge: a plain grid, by priority
            for i, w in enumerate(group):
                cells[(i % ncols, i // ncols)] = w["id"]
        else:
            row = {}
            for c in range(ncols):
                col = [w for w in group if depth[w["id"]] == c]

                def bary(w):
                    ps = [row[p] for p in pre.get(w["id"], []) if p in row]
                    return (sum(ps) / len(ps) if ps else 1e9, prio_key(w))
                col.sort(key=bary if c else prio_key)
                for r, w in enumerate(col):
                    row[w["id"]] = r
                    cells[(c, r)] = w["id"]
        nrows = max(r for _, r in cells) + 1
        label = "Independent (no declared dependency)" if independent else f"Cluster {ci + 1}"
        bands.append((y, nrows, label))
        for (c, r), wid in cells.items():
            pos[wid] = (MARGIN + c * (BOX_W + COL_GAP), y + 26 + r * (BOX_H + ROW_GAP), c, r)
        y += 26 + nrows * (BOX_H + ROW_GAP) + 18
    height = y + 50
    e = html.escape
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
           '<defs>'
           '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker></defs>',
           f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
           f'<text x="{MARGIN}" y="{MARGIN + 6}" font-size="17" font-weight="600" fill="#222">Worksites dependency graph</text>',
           f'<text x="{MARGIN}" y="{MARGIN + 26}" font-size="11.5" fill="#666">Generated from worksite.yaml (field depends_on) at HEAD '
           f'{e(head_sha())}, {datetime.date.today().isoformat()}.</text>',
           f'<text x="{MARGIN}" y="{MARGIN + 42}" font-size="11.5" fill="#666">Arrow: prerequisite → worksite that waits for it. '
           f'One band per cluster of connected worksites; inside a band, columns by depth.</text>']
    for by, nrows, label in bands:
        out.append(f'<rect x="{MARGIN - 12}" y="{by}" width="{width - 2 * MARGIN + 24}" '
                   f'height="{26 + nrows * (BOX_H + ROW_GAP) - ROW_GAP + 12}" rx="10" fill="#fafaf8" stroke="#e2e0da"/>'
                   f'<text x="{MARGIN}" y="{by + 17}" font-size="11.5" font-weight="600" fill="#888">{e(label)}</text>')
    # edges first, under the boxes
    def corridor(yb, rb):           # the empty lane just above the target's row
        return yb - ROW_GAP / 2

    for a, b, kind, why in edges:
        (xa, ya, ca, ra), (xb, yb, cb, rb) = pos[a], pos[b]
        if kind == "batched" and cb < ca:
            (xa, ya, ca, ra), (xb, yb, cb, rb) = (xb, yb, cb, rb), (xa, ya, ca, ra)
        x1, y1, x2, y2 = xa + BOX_W, ya + BOX_H / 2, xb - (0 if kind == "batched" else 2), yb + BOX_H / 2
        if cb == ca:                # same column (batched): bottom to bottom, below the boxes
            x1, x2 = xa + BOX_W / 2, xb + BOX_W / 2
            d = f"M{x1},{ya + BOX_H} C{x1},{ya + BOX_H + 30} {x2},{yb + BOX_H + 30} {x2},{yb + BOX_H}"
        elif cb - ca == 1:          # neighbour column: direct curve through the column gap
            m = COL_GAP * 0.6
            d = f"M{x1},{y1} C{x1 + m},{y1} {x2 - m},{y2} {x2},{y2}"
        else:                       # skips columns: out into the gap, along the corridor, back in
            yc = corridor(yb, rb) if rb > 0 else yb - ROW_GAP / 2
            gx1, gx2 = x1 + COL_GAP / 2, x2 - COL_GAP / 2
            d = (f"M{x1},{y1} C{x1 + COL_GAP * 0.4},{y1} {gx1},{y1} {gx1},{(y1 + yc) / 2} "
                 f"S{gx1},{yc} {gx1 + 12},{yc} L{gx2 - 12},{yc} "
                 f"C{gx2},{yc} {gx2},{y2} {x2},{y2}")
        if kind == "batched":
            style = 'stroke="#9a7bb8" stroke-width="1.6" stroke-dasharray="2 4" fill="none"'
        elif kind == "hard":
            style = 'stroke="#555" stroke-width="1.8" fill="none" marker-end="url(#ah)"'
        else:
            style = 'stroke="#888" stroke-width="1.4" stroke-dasharray="6 4" fill="none" marker-end="url(#ah)"'
        out.append(f'<path d="{d}" {style}><title>{e(a)} → {e(b)} ({kind}): {e(why)}</title></path>')
    for w in doc["worksites"]:
        x, y = pos[w["id"]][:2]
        status = str(w.get("status") or "todo")
        fill, stroke = STATUS_FILL.get(status, STATUS_FILL["todo"])
        prio = w.get("priority")
        ptxt = f"P{prio}" if isinstance(prio, int) else ("P?" if prio is None else str(prio))
        tip = f"{w['id']} — {w.get('title', '')}\nstatus: {status} · priority: {prio}"
        out.append(f'<g><title>{e(tip)}</title>'
                   f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
                   f'<text x="{x + 10}" y="{y + 19}" font-size="13" font-weight="700" fill="#222">{e(w["id"])}</text>'
                   f'<text x="{x + BOX_W - 10}" y="{y + 19}" font-size="11.5" text-anchor="end" fill="{stroke}">'
                   f'{e(ptxt)} · {e(status)}</text>')
        for i, line in enumerate(wrap(str(w.get("title", "")))):
            out.append(f'<text x="{x + 10}" y="{y + 38 + i * 15}" font-size="12" fill="#333">{e(line)}</text>')
        out.append("</g>")
    ly = height - 34
    out.append(
        f'<g font-size="11.5" fill="#444">'
        f'<path d="M{MARGIN},{ly} h40" stroke="#555" stroke-width="1.8" marker-end="url(#ah)"/><text x="{MARGIN + 48}" y="{ly + 4}">hard</text>'
        f'<path d="M{MARGIN + 100},{ly} h40" stroke="#888" stroke-width="1.4" stroke-dasharray="6 4" marker-end="url(#ah)"/><text x="{MARGIN + 148}" y="{ly + 4}">soft (defer / measure)</text>'
        f'<path d="M{MARGIN + 290},{ly} h40" stroke="#9a7bb8" stroke-width="1.6" stroke-dasharray="2 4"/><text x="{MARGIN + 338}" y="{ly + 4}">batched (same files)</text>'
        f'<text x="{MARGIN + 480}" y="{ly + 4}">P? = priority not set · hover a box or an arrow for details</text></g>')
    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent), help="output directory")
    ap.add_argument("--check", action="store_true", help="checks only, write nothing")
    a = ap.parse_args()
    doc = worksite_report.load()
    edges, errors = edges_of(doc)
    depth, cyc = depths(doc, edges) if not errors else ({}, [])
    errors += cyc
    for msg in errors:
        print("ERROR", msg)
    print(f"worksite_graph: {len(doc['worksites'])} worksites, {len(edges)} dependencies, {len(errors)} error(s)")
    if errors:
        return 1
    if a.check:
        return 0
    out = Path(a.out) / "worksites_dependency_graph.svg"
    out.write_text(render(doc, edges, depth), encoding="utf-8")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
