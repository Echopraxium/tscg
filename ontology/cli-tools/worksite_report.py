#!/usr/bin/env python3
"""
worksite_report.py — render the TSCG worksite status table from worksite.yaml.

Author : Echopraxium with the collaboration of Claude AI
Version: 0.1.0
Home   : ontology/cli-tools/worksite_report.py

Reads the structured state layer (ontology/docs/_01_Worksite/worksite.yaml) and
prints the roadmap table on demand — the "table at any time" the worksite map's
prose could only give by hand. Two renderings from the SAME source:

  --text       (default) terminal table
  --markdown   the .md derivation (YAML is source of truth, .md is generated)

Later lot: a --measure switch will refresh the reliably-measurable gauges (e.g.
SC-6/DCC006 via check_M1, ⊗ via validator/FRB) instead of trusting the YAML's
`current`. For now the report reflects the declared state; gauges with
`current: null` are shown as `?` and annotated with the family that will measure them.

Usage
-----
  python worksite_report.py                     # all worksites, text
  python worksite_report.py --worksite WS-0     # one worksite
  python worksite_report.py --markdown          # .md derivation to stdout
  python worksite_report.py --markdown -o roadmap.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml --break-system-packages")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tscg_paths import REPO_ROOT  # noqa: E402

YAML_PATH = REPO_ROOT / "ontology/docs/_01_Worksite/worksite.yaml"

_ICON = {"done": "✅", "design-decided": "◐", "scoped": "○", "staged": "▣",
         "todo": "☐", "partial": "◑", "blocked": "✕"}


def _gauge_cell(item: dict) -> str:
    if "gauge" not in item:
        return ""
    cur = item.get("current")
    tgt = item.get("target")
    shown = "?" if cur is None else str(cur)
    by = item.get("measured_by", "")
    tail = f" [{by}]" if cur is None and by else ""
    return f"{item['gauge']}: {shown}→{tgt}{tail}"


def load() -> dict:
    """Aggregate the central worksite.yaml (meta + inline worksites) with any
    distributed per-worksite files at _01_Worksite/WS-*/worksite.yaml.

    A worksite lives in EXACTLY ONE place (central inline OR its WS-n/ file); a
    duplicate id is a hard error so the two sources never drift silently.
    """
    if not YAML_PATH.exists():
        sys.exit(f"not found: {YAML_PATH}")
    doc = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8")) or {}
    worksites = list(doc.get("worksites", []))
    seen = {w["id"] for w in worksites if isinstance(w, dict) and "id" in w}

    ws_dir = YAML_PATH.parent
    for wf in sorted(ws_dir.glob("WS-*/worksite.yaml")):
        sub = yaml.safe_load(wf.read_text(encoding="utf-8"))
        # a distributed file may be: a bare LIST of worksites (the delivered block
        # format), a dict with a `worksites:` list, or a single bare mapping.
        if isinstance(sub, list):
            entries = sub
        elif isinstance(sub, dict) and "worksites" in sub:
            entries = sub["worksites"]
        elif isinstance(sub, dict) and "id" in sub:
            entries = [sub]
        else:
            entries = []
        for w in entries:
            wid = w.get("id")
            if wid in seen:
                sys.exit(f"duplicate worksite {wid!r}: in central AND {wf}")
            seen.add(wid)
            worksites.append(w)

    doc["worksites"] = sorted(
        worksites,
        key=lambda w: int(str(w.get("id", "WS-999")).split("-")[-1])
        if str(w.get("id", "")).split("-")[-1].isdigit() else 999,
    )
    return doc


def render_text(doc: dict, only: str | None) -> str:
    out = []
    meta = doc.get("meta", {})
    out.append(f"TSCG worksites — map v{meta.get('mirrors_map_version','?')} "
               f"| HEAD {meta.get('head','?')} | schema {meta.get('schema_version','?')}")
    out.append("=" * 72)
    for ws in doc.get("worksites", []):
        if only and ws["id"] != only:
            continue
        icon = _ICON.get(ws.get("status", ""), "·")
        pr = ws.get("priority", "")
        out.append(f"{icon} {ws['id']:<6} {ws['title']}   (status={ws.get('status')}"
                   f"{', prio=' + str(pr) if pr else ''})")
        if ws.get("note"):
            out.append(f"        · {ws['note']}")
        for it in ws.get("items", []):
            ic = _ICON.get(it.get("status", ""), "·")
            g = _gauge_cell(it)
            line = f"     {ic} {it['id']:<10} {it['title']:<40} {it.get('status','')}"
            if g:
                line += f"   {g}"
            out.append(line)
            for k in ("residual", "note", "record", "commit", "grave_after"):
                if it.get(k):
                    out.append(f"          {k}: {it[k]}")
        out.append("-" * 72)
    return "\n".join(out)


def render_markdown(doc: dict, only: str | None) -> str:
    meta = doc.get("meta", {})
    out = [f"# TSCG Worksite Roadmap (generated from worksite.yaml)",
           "",
           f"*map v{meta.get('mirrors_map_version','?')} · HEAD "
           f"`{meta.get('head','?')}` · schema {meta.get('schema_version','?')} · "
           f"generated {meta.get('generated','?')}*", ""]
    for ws in doc.get("worksites", []):
        if only and ws["id"] != only:
            continue
        icon = _ICON.get(ws.get("status", ""), "·")
        pr = ws.get("priority", "")
        out.append(f"## {icon} {ws['id']} — {ws['title']}  "
                   f"({ws.get('status')}{', prio ' + str(pr) if pr else ''})")
        if ws.get("note"):
            out.append(f"> {ws['note']}")
        out.append("")
        if ws.get("items"):
            out.append("| | item | title | status | gauge |")
            out.append("|---|---|---|---|---|")
            for it in ws["items"]:
                ic = _ICON.get(it.get("status", ""), "·")
                note = it.get("note") or it.get("residual") or ""
                title = it["title"] + (f" — {note}" if note else "")
                out.append(f"| {ic} | {it['id']} | {title} | {it.get('status','')} "
                           f"| {_gauge_cell(it)} |")
            out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="render the TSCG worksite table")
    ap.add_argument("--markdown", action="store_true", help="emit the .md derivation")
    ap.add_argument("--worksite", default=None, help="filter to one worksite id")
    ap.add_argument("-o", "--out", default=None, help="write to a file instead of stdout")
    args = ap.parse_args(argv)

    doc = load()
    text = render_markdown(doc, args.worksite) if args.markdown \
        else render_text(doc, args.worksite)

    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
