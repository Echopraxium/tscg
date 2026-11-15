#!/usr/bin/env python3
"""delta1_inventory.py -- read-only inventory of the epistemic gap (delta_1) family at HEAD.

Author: Echopraxium with the collaboration of Claude AI
Feasibility study, 2026-11-15. Standard library only; changes no file.

Usage (repo root, clean clone at HEAD):
    python ontology/docs/_01_Worksite/WS-15/delta1_inventory.py

Sections printed (Markdown):
  A. git grep hits by area and by role (role from path/extension; see ROLE_RULES)
  B. every JSON path of the M3 / M2 / M1 / M0_Common ontology files that mentions
     the family, with a role (definition / derived / doctrine / use)
  C. the value of m0:epistemicGap on the owl:Ontology node of each M0 instance
     (same discovery as check_m0), the stored class, the class the M0_Common
     thresholds give, and |asfidMean - revoiMean| / sqrt(2) recomputed
  D. the formulas found for the gap (string census)
  E. the check_m0 PASS instances carrying the family (impact of a FAIL vs WARN check)
  F. the whole scoring family (scope of 'no scores', 2026-11-15)
"""
import json, math, re, subprocess, sys, collections
from pathlib import Path

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
PATTERN = (r"δ₁|δ1|δ\(M\)|epistemicGap|EpistemicGap|epistemic.gap|spectralClass|SpectralClass"
           r"|spectral_class|delta_?1\b")
HERE = Path(__file__).resolve().parent.relative_to(ROOT).as_posix()
# this study's own folder is excluded, so that the counts do not include the note itself
EXCLUDE = [":(exclude)*migration_backups*", ":(exclude)*_backups*", f":(exclude){HERE}/*"]
FAMILY = re.compile(PATTERN, re.I)


def git_grep():
    out = subprocess.run(["git", "grep", "-n", "-I", "-i", "-E", PATTERN, "--", "."] + EXCLUDE,
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    return [l.split(":", 2) for l in out.splitlines() if l.count(":") >= 2]


def area_role(path):
    p = path
    if p.startswith("ontology/Ref/"):
        return "archive", "archive (Ref snapshot)"
    if re.match(r"ontology/M3_.*\.jsonld$", p):
        return "M3", "ontology (see B)"
    if re.match(r"ontology/M2_.*\.jsonld$", p):
        return "M2", "ontology (see B)"
    if re.match(r"ontology/(M1_|M1_extensions/).*\.jsonld$", p):
        return "M1", "ontology (see B)"
    if p == "ontology/M0_Common.jsonld":
        return "M0_Common", "ontology (see B)"
    if re.match(r"(instances|_00_UserGuide)/.*M0_[^/]*\.jsonld$", p) or p.endswith(".jsonld"):
        return "M0", "use (see C)"
    if p.endswith(".ttl") and "toolchain" in p:
        return "gate", "check (SHACL)"
    if p.startswith("ontology/toolchain/") and p.endswith(".py"):
        return "gate/tooling", "code"
    if p.startswith(".claude/skills/"):
        return "skills", "producer (instructions)"
    if re.search(r"\.(py|js|ts|css)$", p):
        return "code", "code"
    if p.endswith(".html"):
        return "code" if "/static/" in p or "/sim/" in p or p in ("index.html",) else "narrative", \
               "code (page)" if "/static/" in p or "/sim/" in p or p == "index.html" else "narrative"
    if p.endswith(".json"):
        return "data", "data snapshot"
    if p.startswith(("docs/papers/", "docs/reboot-kit/SmartPrompts/")):
        return "historical", "narrative (historical)"
    return "docs", "narrative"


def section_a(hits):
    print("## A. git grep hits by area and role\n")
    print("Command: `git grep -n -I -i -E \"%s\" -- . %s`\n" % (PATTERN, " ".join(EXCLUDE)))
    files = collections.defaultdict(set)
    lines = collections.Counter()
    for f, _, _ in hits:
        k = area_role(f)
        files[k].add(f)
        lines[k] += 1
    print("| area | role | files | lines |\n|---|---|---|---|")
    for k in sorted(files):
        print(f"| {k[0]} | {k[1]} | {len(files[k])} | {lines[k]} |")
    print(f"\nTotal: {len({h[0] for h in hits})} files, {len(hits)} lines.\n")


def walk(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}/{k}"
            if FAMILY.search(k) or (isinstance(v, str) and FAMILY.search(v)):
                out.append((p, v))
            walk(v, p, out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]", out)


def role_b(fname, node_id, path, value):
    key = path.rsplit("/", 1)[-1]
    if "changelog" in path or "versionNotes" in path:
        return "history"
    if fname == "M0_Common.jsonld" and re.search("spectral|threshold", node_id + path, re.I):
        return "derived"
    if node_id and FAMILY.search(node_id) and path.count("/") == 1:
        return "definition"
    if re.search(r"formula|epistemic_gap|epistemicGapFormula|mathematicalForm|epistemicScore", path):
        return "definition (formula)"
    if isinstance(value, (int, float)):
        return "use"
    return "doctrine"


def section_b():
    print("## B. Ontology files: every JSON path mentioning the family\n")
    files = sorted(ROOT.glob("ontology/M3_*.jsonld")) + sorted(ROOT.glob("ontology/M2_*.jsonld")) \
        + sorted(ROOT.glob("ontology/M1_*.jsonld")) + sorted(ROOT.glob("ontology/M1_extensions/**/*.jsonld")) \
        + [ROOT / "ontology/M0_Common.jsonld"]
    print("| file | node | key path | role | value (start) |\n|---|---|---|---|---|")
    counts = collections.Counter()
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        graph = d.get("@graph", [d])
        for node in graph:
            out = []
            walk(node, "", out)
            if FAMILY.search(node.get("@id", "")):
                seen = {p for p, _ in out}
                out += [(f"/{k}", v) for k, v in node.items()
                        if isinstance(v, str) and f"/{k}" not in seen]
            for p, v in out:
                r = role_b(f.name, node.get("@id", ""), p, v)
                counts[(f.name, r)] += 1
                s = (json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v)[:70].replace("|", "\\|")
                print(f"| {f.name} | `{node.get('@id', '?')}` | `{p}` | {r} | {s} |")
    print("\nCounts by file and role:\n\n| file | role | paths |\n|---|---|---|")
    for (f, r), c in sorted(counts.items()):
        print(f"| {f} | {r} | {c} |")
    print()


def num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, dict) and "@value" in v:
        try:
            return float(v["@value"])
        except ValueError:
            return None
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def klass(x):
    return "Coherent" if x < .05 else "OnCriticalLine" if x < .15 else "Liminal" if x < .30 else "Enigmatic"


def section_c():
    sys.path.insert(0, str(ROOT / "ontology/toolchain"))
    sys.path.insert(0, str(ROOT / "ontology/toolchain/check-M0"))
    from check_m0_instances import discover_instances  # same discovery as the gate
    print("## C. M0 instances: m0:epistemicGap on the owl:Ontology node\n")
    print("| instance | form | stored | stored class | class from thresholds | recomputed from means | note |")
    print("|---|---|---|---|---|---|---|")
    forms = collections.Counter()
    nested = []
    for path, name, _ in discover_instances():
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        graph = d.get("@graph", [d])
        onts = [n for n in graph if isinstance(n, dict) and "owl:Ontology" in
                (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])]
        for i, n in enumerate(graph):
            if isinstance(n, dict) and "m0:epistemicGap" in n and (not onts or n is not onts[0]):
                nested.append((Path(path).name, i, type(n["m0:epistemicGap"]).__name__))
        if not onts:
            forms["no owl:Ontology node"] += 1
            continue
        o = onts[0]
        v = o.get("m0:epistemicGap", None)
        if v is None:
            form = "absent"
        elif isinstance(v, dict):
            form = "typed literal" if "@value" in v else "object"
        else:
            form = type(v).__name__
        forms[form] += 1
        if form == "absent":
            continue
        g = num(v)
        sc = o.get("m0:spectralClass")
        sc = (sc.get("@id") if isinstance(sc, dict) else sc) or "-"
        exp = klass(g) if g is not None else "-"
        am, rm = num(o.get("m0:asfidMean")), num(o.get("m0:revoiMean"))
        rec = f"{abs(am - rm) / math.sqrt(2):.4f}" if am is not None and rm is not None else "-"
        note = []
        if sc != "-" and g is not None and exp not in sc:
            note.append("class != thresholds")
        if rec != "-" and g is not None and abs(float(rec) - g) > 0.005:
            note.append("stored != recomputed")
        print(f"| {Path(path).stem} | {form} | {g if g is not None else str(v)[:30]} | {sc.split('spectralClass.')[-1]} | {exp} | {rec} | {', '.join(note)} |")
    print("\nForms on the owl:Ontology node:", dict(forms))
    print("\nm0:epistemicGap on another node of @graph (not the owl:Ontology node):")
    for f, i, t in nested:
        print(f"- {f} @graph[{i}] ({t})")
    print()


def section_d():
    print("## D. Formula census (gap formulas written in ontology and instance files)\n")
    pat = r"(δ₁|δ\(M\)|δ|delta_?1|ΔΘ|Delta_Theta) ?= ?[^\",;]{3,60}"
    out = subprocess.run(["git", "grep", "-h", "-o", "-I", "-E", pat, "--", "ontology/*.jsonld",
                          "instances/**/*.jsonld", "_00_UserGuide", ":(exclude)ontology/Ref/*"] + EXCLUDE,
                         cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()
    c = collections.Counter(re.sub(r"\d\.\d+", "N", l).strip() for l in out)
    print("| occurrences | formula (numbers -> N) |\n|---|---|")
    for k, v in c.most_common():
        if re.match(r"^\S+ ?= ?(¦?N|max|0\b)", k) or "degree of proof" in k:
            continue  # a computed value or a gloss, not a formula
        print(f"| {v} | `{k.replace('|', '¦')}` |")
    print()


def section_e():
    """FAIL-vs-WARN impact: which check_m0 PASS instances carry the family on their owl:Ontology node."""
    import tempfile, os
    print("## E. check_m0 PASS instances that carry the family on their owl:Ontology node\n")
    tmp = os.path.join(tempfile.mkdtemp(), "m0.json")
    subprocess.run([sys.executable, "check-M0/check_m0_instances.py", "--json", tmp],
                   cwd=ROOT / "ontology/toolchain", capture_output=True)
    d = json.loads(Path(tmp).read_text(encoding="utf-8"))
    reps = d if isinstance(d, list) else next(v for v in d.values() if isinstance(v, list))
    status = collections.Counter(r["status"] for r in reps)
    carrying = []
    for r in reps:
        if r["status"] != "PASS":
            continue
        doc = json.loads(Path(r["path"]).read_text(encoding="utf-8"))
        g = doc.get("@graph", [doc])
        o = [n for n in g if isinstance(n, dict) and "owl:Ontology" in
             (n.get("@type") if isinstance(n.get("@type"), list) else [n.get("@type")])]
        keys = [k for k in (o[0] if o else {}) if FAMILY.search(k)]
        if keys:
            carrying.append((r["name"], keys))
    print(f"check_m0 statuses: {dict(status)}")
    print(f"PASS instances carrying the family: {len(carrying)}\n")
    for n, k in carrying:
        print(f"- {n}: {', '.join(k)}")
    print()


SCORES = re.compile(r"\bscore(A|S|St|F|I|It|D|R|E|V|O|Im)\b|asfidScores|revoiScores|asfidMean|revoiMean"
                    r"|scoreJustification|scoringStatus|ScoringStatus|focalScore|focalBias|focalClass"
                    r"|FocalClass|stereopsicDepth|focalApplicable|FocalProperty|ScoringProperty|epistemicGap|spectralClass"
                    r"|SpectralClass")


def section_f():
    """Scope of 'no scores at all' (Michel, 2026-11-15): the whole scoring family."""
    print("## F. The scoring family (scores, means, gap, classes, focal family, status)\n")
    d = json.loads((ROOT / "ontology/M0_Common.jsonld").read_text(encoding="utf-8"))
    declared = [n.get("@id") for n in d.get("@graph", []) if SCORES.search(n.get("@id", ""))]
    print(f"M0_Common nodes of the family: {len(declared)} of {len(d.get('@graph', []))}\n")
    print(", ".join(f"`{x}`" for x in declared) + "\n")
    sys.path.insert(0, str(ROOT / "ontology/toolchain"))
    sys.path.insert(0, str(ROOT / "ontology/toolchain/check-M0"))
    from check_m0_instances import discover_instances
    with_keys, total = 0, 0
    for path, name, _ in discover_instances():
        total += 1
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        out = []
        walk_keys(doc.get("@graph", [doc]), out)
        if out:
            with_keys += 1
    print(f"M0 instances with at least one key of the family in @graph: {with_keys} of {total}\n")
    print("M3 / M2 string values mentioning a score (word 'score'):\n")
    for f in sorted(ROOT.glob("ontology/M3_*.jsonld")) + sorted(ROOT.glob("ontology/M2_*.jsonld")):
        doc = json.loads(f.read_text(encoding="utf-8"))
        hits = []
        for node in doc.get("@graph", [doc]):
            o = []
            walk_strings(node, "", o)
            hits += [(node.get("@id"), p, v) for p, v in o if re.search(r"\bscor(e|es|ed|ing)\b", v, re.I)
                     and "changelog" not in p]
        for nid, p, v in hits:
            m = re.search(r".{0,60}\bscor\w*.{0,60}", v, re.I)
            print(f"- {f.name} `{nid}` `{p}`: …{m.group(0).replace('|', '¦')}…")
    print()


def walk_keys(o, out):
    if isinstance(o, dict):
        for k, v in o.items():
            if SCORES.search(k):
                out.append(k)
            walk_keys(v, out)
    elif isinstance(o, list):
        for v in o:
            walk_keys(v, out)


def walk_strings(o, path, out):
    if isinstance(o, dict):
        for k, v in o.items():
            walk_strings(v, f"{path}/{k}", out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk_strings(v, f"{path}[{i}]", out)
    elif isinstance(o, str):
        out.append((path, o))


if __name__ == "__main__":
    head = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    print(f"# delta_1 inventory at {head}\n")
    hits = git_grep()
    section_a(hits)
    section_b()
    section_c()
    section_d()
    section_e()
    section_f()
