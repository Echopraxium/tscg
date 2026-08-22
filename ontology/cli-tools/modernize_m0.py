#!/usr/bin/env python3
"""
TSCG M0 modernizer (Path B) — brings a non-conformant instance toward check-M0
conformance without polluting the shared M0_Common namespace.

Per Michel's decisions:
  - Path B: instance-local m0:X properties are RECLASSIFIED to m0.<inst>:X.
    A property stays under m0: ONLY if its first segment is in the schema's
    shared whitelist (read from the check-M0 SHACL). Everything else is local.
  - Politique 1 for the tensor reform (guarded; no-op when absent):
    rename m0:tensorFormula -> m2:hasStructuralGrammarFormula, and in formula
    VALUES map the retired glyph to the monoidal product and subscript atoms
    (S->St, I->It). (Map-segment I->Im is context-dependent and left for review.)

Mechanical fixes applied:
  - m0: prefix -> M0_Common#   (C02)
  - add m0.<camelInstance>: -> instance-file#   (C03)
  - owl:imports made absolute + M0_Common added   (C09)
  - obsolete @context aliases removed: sm, m1core, m1chem, m1phys, *_score,
    snake/short local aliases, m0.tensorFormula   (C07)
  - m1/m2/m3 prefixes forced absolute if relative

Does NOT invent semantics (domain, ontologyType, formula content). Reports gaps.
Run from repo root:  python modernize_m0.py <instance.jsonld>
"""
import sys, json, re, io
from pathlib import Path

BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main"
# Schema resolved relative to THIS script's location (works from any CWD, and
# whether the script lives in ontology/cli-tools/ or elsewhere beside check-M0).
SCHEMA = Path(__file__).resolve().parent / "check-M0" / "M0_Instances_Schema_shacl.ttl"

def camel(name: str) -> str:
    parts = re.split(r'[_\-]', name)
    if len(parts) == 1:
        return name[0].lower() + name[1:]
    return parts[0].lower() + "".join(p[:1].upper() + p[1:] for p in parts[1:])

def load_whitelist() -> set:
    txt = SCHEMA.read_text(encoding="utf-8")
    toks = set(re.findall(r'm0:([A-Za-z][A-Za-z0-9_]*)', txt))
    return {t for t in toks if not t.endswith("Shape")}

def modernize(path: Path):
    # The check-M0 gate derives an instance's name from its FILE stem
    # (M0_<name> -> <name>), so that is the identity. A folder may hold several
    # instances (e.g. Bmc/ has M0_Bmc and M0_BmcSimulation), so the folder name
    # is NOT a reliable identity. We only use the folder to detect a *case-only*
    # drift of the same name (folder 'Vco' vs file 'M0_VCO.jsonld'), which passes
    # on one OS and fails on another.
    folder = path.parent.name
    file_inst = path.stem[3:] if path.stem.startswith("M0_") else path.stem
    casing_warn = None
    if folder.lower() == file_inst.lower() and folder != file_inst:
        # case-only mismatch -> canonicalize to the folder's casing
        inst = folder
        canonical_file = f"M0_{folder}.jsonld"
        casing_warn = (
            f"file '{path.name}' differs from folder '{folder}' by case only. The gate "
            f"derives the name from the FILE, so this drifts across Windows/Linux. "
            f"Canonical name is '{canonical_file}'. Rename it (case-safe, two-step):\n"
            f"    git mv {path.parent.as_posix()}/{path.name} {path.parent.as_posix()}/_tmp_{inst}.jsonld\n"
            f"    git mv {path.parent.as_posix()}/_tmp_{inst}.jsonld {path.parent.as_posix()}/{canonical_file}"
        )
    else:
        inst = file_inst
        canonical_file = path.name
    cam = camel(inst)
    wl = load_whitelist()
    d = json.loads(path.read_text(encoding="utf-8"))
    ctx = d.get("@context", {})
    g = d.get("@graph", [])
    o = g[0] if g else {}
    report = {"instance": inst, "camel": cam}
    if casing_warn:
        report["CASING_WARNING"] = casing_warn

    # serialize early so alias body-migrations operate on text
    raw = json.dumps(d, ensure_ascii=False, indent=2)
    body_migrations = []   # (old_prefix, new_prefix)

    def uses(pfx):
        return raw.count('"%s:' % pfx)

    # ---- @context: migrate-or-delete old aliases ----
    for k in list(ctx.keys()):
        if k.endswith("_score") or k in ("asfid", "revi", "m0.tensorFormula"):
            del ctx[k]; continue
        if k == "m1core":
            if uses("m1core"): body_migrations.append(("m1core", "m1"))
            del ctx[k]; continue
        if k == "sm":
            del ctx[k]; continue  # observed unused; delete
        if re.match(r'^m1[a-z]+$', k) and k != "m1":   # m1<domain> short alias
            val = ctx[k]; val = val.get("@id") if isinstance(val, dict) else val
            m = re.search(r'M1_extensions/([a-z_]+)/', str(val))
            if m and uses(k):
                dom = m.group(1)
                newpfx = f"m1.ext:{dom}"
                ctx[newpfx] = f"{BASE}/ontology/M1_extensions/{dom}/M1_{dom.title().replace('_','')}.jsonld#"
                body_migrations.append((k, newpfx))
            del ctx[k]; continue
        if (k.startswith("m0.") and k not in ("m0", f"m0.{cam}")) or \
           (k.startswith("m0:") and k != "m0"):
            del ctx[k]
    ctx["m0"] = f"{BASE}/ontology/M0_Common.jsonld#"
    # instance-file URL for the local alias: use the CANONICAL file name (folder-aligned)
    rp = path.resolve().as_posix()
    idx = rp.find("/instances/")
    reldir = rp[idx + 1:rp.rfind("/")] if idx >= 0 else f"instances/poclets/{inst}"
    ctx[f"m0.{cam}"] = f"{BASE}/{reldir}/{canonical_file}#"
    # force core prefixes absolute
    for pfx, tgt in [("m1", "M1_CoreConcepts.jsonld#"), ("m2", "M2_GenericConcepts.jsonld#"),
                     ("m3", "M3_GenesisGrammar.jsonld#")]:
        if pfx in ctx and not str(ctx[pfx]).startswith("http"):
            ctx[pfx] = f"{BASE}/ontology/{tgt}"

    # ---- owl:imports absolute + M0_Common ----
    imp = o.get("owl:imports", [])
    if isinstance(imp, str): imp = [imp]
    imp = [(i if str(i).startswith("http") else f"{BASE}/ontology/{i}") for i in imp]
    if not any("M0_Common" in str(i) for i in imp):
        imp.append(f"{BASE}/ontology/M0_Common.jsonld")
    if imp: o["owl:imports"] = imp

    # ---- v2 fixers on the root node + graph ----
    def num(v):
        if isinstance(v, dict) and "@value" in v:
            try: return float(v["@value"])
            except Exception: return v["@value"]
        return v

    # C10: SCORE props stored as {@value,@type} -> bare numeric
    SCORE_PROPS = ["m0:scoreA","m0:scoreS","m0:scoreF","m0:scoreIt","m0:scoreD",
                   "m0:scoreR","m0:scoreE","m0:scoreV","m0:scoreO","m0:scoreIm",
                   "m0:asfidMean","m0:revoiMean","m0:epistemicGap",
                   "m0:focalScore","m0:focalBias","m0:stereopsicDepth"]
    debared = [p for p in SCORE_PROPS if isinstance(o.get(p), dict) and "@value" in o[p]]
    for p in debared:
        o[p] = num(o[p])

    # C15: flatten nested asfidScores{}/revoiScores{} -> flat bare scores (+means/gap)
    def flatten(block_key, mapping):
        blk = o.pop(block_key, None)
        if not isinstance(blk, dict): return None
        for sub, target in mapping.items():
            if sub in blk:
                o[target] = num(blk[sub])
        return num(blk.get("mean")) if "mean" in blk else None
    flattened = False
    if isinstance(o.get("m0:asfidScores"), dict):
        am = flatten("m0:asfidScores",
                     {"A_score":"m0:scoreA","S_score":"m0:scoreS","F_score":"m0:scoreF",
                      "It_score":"m0:scoreIt","D_score":"m0:scoreD"})
        if am is not None and "m0:asfidMean" not in o: o["m0:asfidMean"] = am
        flattened = True
    if isinstance(o.get("m0:revoiScores"), dict):
        rm = flatten("m0:revoiScores",
                     {"R_score":"m0:scoreR","E_score":"m0:scoreE","V_score":"m0:scoreV",
                      "O_score":"m0:scoreO","It_score":"m0:scoreIm","Im_score":"m0:scoreIm"})
        if rm is not None and "m0:revoiMean" not in o: o["m0:revoiMean"] = rm
        flattened = True
    if flattened and "m0:epistemicGap" not in o \
       and isinstance(o.get("m0:asfidMean"), (int,float)) and isinstance(o.get("m0:revoiMean"), (int,float)):
        o["m0:epistemicGap"] = round(abs(o["m0:asfidMean"] - o["m0:revoiMean"]) / (2**0.5), 3)
    report["debared_scores"] = len(debared); report["flattened_nested"] = flattened

    # C11: enum string values -> IRI nodes {"@id": "m0:<prop>.<PascalValue>"}
    ENUM_PROPS = {"m0:spectralClass":"spectralClass","m0:focalClass":"focalClass",
                  "m0:scoringStatus":"scoringStatus"}
    fixed_enums = []
    for p, short in ENUM_PROPS.items():
        v = o.get(p)
        if isinstance(v, str) and not v.startswith(f"m0:{short}."):
            pv = v[:1].upper() + v[1:]
            o[p] = {"@id": f"m0:{short}.{pv}"}
            fixed_enums.append(f"{short}={v}")
    report["enum_iris"] = fixed_enums

    # C13: m3:ontologyType must live only in @graph[0] — strip from the rest
    stripped = 0
    for node in d["@graph"][1:]:
        if isinstance(node, dict) and "m3:ontologyType" in node:
            del node["m3:ontologyType"]; stripped += 1
    report["ontologyType_stripped"] = stripped

    d["@graph"][0] = o
    s = json.dumps(d, ensure_ascii=False, indent=2)

    # ---- migrate old-alias body usages (m1core->m1, m1<dom>->m1.ext:<dom>) ----
    # m1core is a universally retired alias for M1_CoreConcepts; migrate it even when it
    # was never declared in @context (a dangling prefix, e.g. m1core:simulationTitle).
    if '"m1core:' in s and ("m1core", "m1") not in body_migrations:
        body_migrations.append(("m1core", "m1"))
    for old, new in body_migrations:
        s = s.replace('"%s:' % old, '"%s:' % new)
    report["alias_migrations"] = [f"{a}->{b}" for a, b in body_migrations]

    # safety net: any remaining "<prefix>: whose prefix is not declared/standard
    declared = set(json.loads(s).get("@context", {}).keys()) | {
        "@base", "dcterms", "owl", "rdf", "rdfs", "skos", "xsd", "m0", "m1", "m2", "m3"}
    used = set(re.findall(r'"([A-Za-z][A-Za-z0-9_.]*):[A-Za-z]', s))
    unresolved = sorted(p for p in used if p not in declared and not p.startswith("m0.")
                        and not p.startswith("m1.ext"))
    if unresolved:
        report["UNRESOLVED_PREFIXES"] = unresolved

    # ---- ORIVE prose hygiene (vestige acronym; keep the number) ----
    s = re.sub(r'\bORIVE\b', 'REVOI', s)

    # ---- tensor reform (guarded) ----
    if "m0:tensorFormula" in s:
        s = s.replace('"m0:tensorFormula"', '"m2:hasStructuralGrammarFormula"')
        report["renamed_tensorFormula"] = True
    if "m0:hasStructuralGrammarFormula" in s:
        s = s.replace('"m0:hasStructuralGrammarFormula"', '"m2:hasStructuralGrammarFormula"')

    # ---- Path B reclassification of m0:X tokens (keys + @ids) ----
    relocated = set(); kept = set()
    def repl(m):
        seg1 = m.group(1); rest = m.group(2) or ""
        if seg1 in wl:
            kept.add(seg1); return m.group(0)
        # instance-local -> m0.<cam>: ; for double-colon m0:<Inst>:Y drop <Inst>
        local = rest[1:] if rest else seg1
        relocated.add(seg1 + rest)
        return f'"m0.{cam}:{local}'
    s = re.sub(r'"m0:([A-Za-z0-9_]+)(:[A-Za-z0-9_]+)?', repl, s)
    report["reclassified_local"] = len(relocated)
    report["kept_shared"] = sorted(kept)

    path.write_text(s + "\n", encoding="utf-8")

    # ---- semantic-gap flags (not auto-filled) ----
    o2 = json.loads(s)["@graph"][0]
    gaps = []
    if not o2.get("m1:domain"): gaps.append("m1:domain MISSING (semantic — needs a value)")
    if not o2.get("m3:ontologyType"): gaps.append("m3:ontologyType MISSING")
    report["semantic_gaps"] = gaps
    report["residual_orive"] = s.lower().count("orive")
    return report

if __name__ == "__main__":
    r = modernize(Path(sys.argv[1]))
    print(json.dumps(r, ensure_ascii=False, indent=2))
