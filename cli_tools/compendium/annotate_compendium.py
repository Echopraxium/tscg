#!/usr/bin/env python3
"""annotate_compendium.py - semi-automatic Compendium classification.
kind = what the file IS ; audience = who it is FOR (KitArchitect/KitCrafter/KitUser).
M0 *.jsonld instances SKIPPED (they carry the real m3:Audience facet).
Convention does the work; an existing @tscg block wins. dry-run default;
--apply writes the block in-place, idempotently. RULES ordered, first match wins."""
import os, re, csv, argparse
from collections import Counter, defaultdict

A, C, U = "KitArchitect", "KitCrafter", "KitUser"

OUT = [
    r"(^|/)\.git/", r"(^|/)node_modules/", r"(^|/)migration_backups/",
    r"(^|/)domain_format_fix_backups/", r"(^|/)_archives/",
    r"(^|/)_02_housekeeping/", r"(^|/)_sim/", r"(^|/)src/tscg/",
    r"(^|/)projects/Doom-Generic/", r"(^|/)crates/",
    r"\.(rs|c|h|ll|tasm|inc|o|a)$",
    r"\.(url|bat|lnk|png|jpe?g|gif|mid|sf2|pdf|docx?|ico|nt|oxg|tvm[xl]|tob|wad|zip|pptx)$",
    r"(package-lock|Cargo)\.lock$", r"(_bak($|\.)|_Previous|M3_GenesisSpace)",
]

RULES = [
    (r"(^|/)instances/.*M0_[^/]*\.jsonld$", "instance", None, "stable"),
    (r"(^|/)ontology/M3_[^/]*\.jsonld$",    "layer", [A]),
    (r"(^|/)ontology/M2_[^/]*\.jsonld$",    "layer", [A]),
    (r"(^|/)ontology/(M1_|M0_Common)[^/]*\.jsonld$", "layer", [C,A]),
    (r"(^|/)ontology/cli-tools/.*\.(py|ttl)$", "gate", [A]),
    (r"(^|/)cli_tools/",                    "tool",  [A]),
    (r"(^|/)\.claude/skills/",              "skill", [A]),
    # Worksite / handover rules MUST stay before every "doc" rule: all worksites live
    # under ontology/docs/_01_Worksite/, so "ontology/docs/.*\.md" used to win and
    # their notes and HandOvers landed in "doc" instead of Project management
    # (11 worksite files instead of 39 — fixed 2026-10-03).
    (r"(^|/)_01_Worksite/",                 "worksite", [A], "draft"),
    (r"(^|/)worksite\.yaml$",               "worksite", [A], "draft"),
    (r"(?i)handover.*\.md$",                "handover", [A], "draft"),
    (r"(^|/)ontology/TSCG_InstanceGrammar/.*\.py$", "tool", [A]),
    (r"(^|/)ontology/TSCG_InstanceGrammar/.*\.md$", "doc",  [C,A]),
    (r"(^|/)ontology/StructuralGrammar/.*\.md$", "doc", [A]),
    (r"(^|/)ontology/.*_README\.md$",       "doc",   [C,A]),
    (r"(^|/)ontology/M1_extensions/.*\.md$", "doc",  [A]),
    (r"(^|/)ontology/docs/.*\.(md|html)$",  "doc",   [A]),
    (r"(^|/)ontology/sparql/.*\.py$",       "tool",  [A]),
    (r"(^|/)docs/CoreHypotheses/.*\.md$",   "epistemology", [U,C,A]),
    (r"(^|/)docs/papers/",                  "epistemology", [C,A], "draft"),
    (r"(^|/)docs/methodology/.*\.md$",      "doc",   [C,A]),
    (r"(^|/)docs/reboot-kit/",              "infra", [A]),
    (r"(^|/)docs/.*\.md$",                  "doc",   [A]),
    (r"(^|/)_00_UserGuide/UserGuide\.md$",  "guide", [U]),
    (r"(^|/)_00_UserGuide/exercises/.*/workflow_run_sample/", "simulation", [U]),
    (r"(^|/)_00_UserGuide/exercises/.*\.md$", "exercise", [U]),
    (r"(^|/)instances/symbolic-system-grammars/.*\.md$", "doc", [U,C,A]),
    (r"(^|/)instances/systemic-frameworks/.*\.md$",      "doc", [C,A]),
    (r"(^|/)instances/.*\.html$",           "simulation", [U]),
    (r"(^|/)instances/.*/(sim|static|src)/.*\.(js|css)$", "simulation-src", [C,A]),
    (r"(POCLET_CREATION_GUIDE|M0_TEMPLATES|_00_template|M0_INSTANCE_TEMPLATE|M0_CONTEXT_TEMPLATE)", "template", [C]),
    (r"(^|/)instances/.*_README\.md$",      "doc",   [U]),
    (r"(^|/)src/[^/]+\.py$",                "tool",  [A]),
    (r"(^|/)src/[^/]+\.md$",                "doc",   [A]),
    (r"(^|/)index\.html$",                  "landing", [U]),
    (r"(^|/)README\.md$",                   "landing", [U]),
    (r"(^|/)CLAUDE\.md$",                   "infra", [A]),
    (r"^[^/]+\.(py|js)$",                   "tool",  [A]),
    (r"(^|/)instances/poclets/",                  "poclet-asset",    [U]),
    (r"(^|/)instances/tscg-tools/",               "tool-asset",      [C,A]),
    (r"(^|/)instances/systemic-frameworks/",      "framework-asset", [C,A]),
    (r"(^|/)instances/symbolic-system-grammars/", "ssg-asset",       [C,A]),
]

CURATED = (".py",".js",".html",".yaml",".yml",".md")

def rel_paths(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d != ".git"]
        for fn in fns:
            full = os.path.join(dp, fn)
            yield full, os.path.relpath(full, root).replace(os.sep, "/")

def has_block(full):
    try:
        with open(full, encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
        return "@tscg" in head or "tscg-kind" in head
    except Exception:
        return False

def classify(rp):
    for pat in OUT:
        if re.search(pat, rp): return ("__OUT__", None, None)
    ext = os.path.splitext(rp)[1].lower()
    if ext not in CURATED and not re.search(r"(^|/)instances/.*M0_[^/]*\.jsonld$", rp):
        return ("__OUT__", None, None)
    for r in RULES:
        pat, kind, aud = r[0], r[1], r[2]
        status = r[3] if len(r) > 3 else "stable"
        if re.search(pat, rp): return (kind, aud, status)
    if rp.endswith(CURATED): return ("__UNCLASSIFIED__", None, None)
    return ("__OUT__", None, None)

def build_block(ext, kind, aud, status):
    rows = [("kind", kind), ("audience", "[" + ", ".join(aud) + "]"), ("status", status)]
    if ext == ".md":
        return "top", "---\n" + "".join(f"tscg-{k}: {v}\n" for k,v in rows) + "---\n\n"
    if ext in (".py",".yaml",".yml"):
        return "hash", "# @tscg\n" + "".join(f"# {k}: {v}\n" for k,v in rows) + "# @tscg-end\n\n"
    if ext == ".js":
        return "top", "/* @tscg\n" + "".join(f"   {k}: {v}\n" for k,v in rows) + "   @tscg-end */\n\n"
    if ext == ".html":
        return "html", "<!-- @tscg\n" + "".join(f"     {k}: {v}\n" for k,v in rows) + "-->\n"
    return None, None

def write_block(full, kind, aud, status):
    if has_block(full): return False
    ext = os.path.splitext(full)[1].lower()
    mode, block = build_block(ext, kind, aud, status)
    if not block: return False
    with open(full, encoding="utf-8", errors="ignore") as f: c = f.read()
    if mode == "hash" and c.startswith("#!"):
        i = c.find("\n") + 1; c = c[:i] + block + c[i:]
    elif mode == "html":
        m = re.search(r"<!doctype[^>]*>\s*|<html[^>]*>\s*", c, re.I)
        c = (c[:m.end()] + block + c[m.end():]) if m else block + c
    else:
        c = block + c
    with open(full, "w", encoding="utf-8") as f: f.write(c)
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    proposed, unclassified, to_write = [], [], []
    counts = Counter(); bka = defaultdict(Counter); out_n = 0
    for full, rp in rel_paths(a.root):
        kind, aud, status = classify(rp)
        if kind == "__OUT__": out_n += 1; continue
        if has_block(full): counts["existing-override"] += 1; continue
        if kind == "instance": counts["instance (facet owns)"] += 1; continue
        if kind == "__UNCLASSIFIED__": unclassified.append(rp); counts["ARBITRATE"] += 1; continue
        aud_s = "|".join(aud)
        proposed.append((rp, kind, aud_s, status)); to_write.append((full, kind, aud, status))
        counts["auto"] += 1; bka[kind][aud_s] += 1
    with open(os.path.join(a.out, "compendium_annotations_proposed.tsv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["path","kind","audience","status"]); w.writerows(sorted(proposed))
    with open(os.path.join(a.out, "compendium_arbitration.md"), "w", encoding="utf-8") as f:
        f.write(f"# Compendium - unclassified ({len(unclassified)})\n\n")
        for rp in sorted(unclassified): f.write(f"- `{rp}`\n")
    written = 0
    if a.apply:
        for full, kind, aud, status in to_write:
            if write_block(full, kind, aud, status): written += 1
    print("=== summary ===")
    for k, v in counts.most_common(): print(f"  {v:5d}  {k}")
    print(f"  {out_n:5d}  out")
    if a.apply: print(f"\n  APPLIED: {written} blocks written")
    print("\n=== auto by kind x audience ===")
    for kind in sorted(bka):
        print(f"  {kind:16s} " + "  ".join(f"{x}={n}" for x,n in bka[kind].items()))

if __name__ == "__main__": main()
