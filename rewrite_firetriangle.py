#!/usr/bin/env python3
"""
FireTriangle Conformance Pass — surgical rewrite to SHACL v1.6.
Author: Echopraxium with the collaboration of Claude AI

Reads the current M0_FireTriangle.jsonld, applies:
  - @context cleanup (drop dead aliases; fix relative m0:epistemicGap def; drop *_score)
  - flat bare-numeric scores m0:scoreA..m0:scoreIm (drop nested asfid/revoiScores)
  - owl:imports M0_Common.jsonld (+ M3/M2/M1)
  - namespace fixes (m1core: -> m1:)
  - notation reform: canonical M2 formulas (read from HEAD), no ⊗/⊕
  - structural-grammar alignment: remove ket/Hilbert state-vectors + norms
  - recomputed canonical epistemicGap = |asfidMean-revoiMean|/√2
  - version bump + rolling changelog (3 objects)

NOTE: does NOT go through any server write-path (ORIVE trap). Michel runs this locally.
"""
import json, io

SRC = "instances/poclets/FireTriangle/M0_FireTriangle.jsonld"
DST = "instances/poclets/FireTriangle/M0_FireTriangle.jsonld"  # overwrite in working copy

BASE = "https://raw.githubusercontent.com/Echopraxium/tscg/main"

with open(SRC, encoding="utf-8") as f:
    doc = json.load(f)

# ---------- 1. @context ----------
M0C = f"{BASE}/ontology/M0_Common.jsonld#"
# xsd:float coercion so bare JSON numbers parse as xsd:float (not xsd:double),
# satisfying the schema's sh:datatype xsd:float. @id kept ABSOLUTE to stay
# clear of the CanonicalNamespace shape. Term key kept as canonical m0:scoreX (v1.5).
def coerce(local):
    return {"@id": M0C + local, "@type": "xsd:float"}

ctx = {
    "dcterms": "http://purl.org/dc/terms/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "m3": f"{BASE}/ontology/M3_GenesisGrammar.jsonld#",
    "m2": f"{BASE}/ontology/M2_GenericConcepts.jsonld#",
    "m1": f"{BASE}/ontology/M1_CoreConcepts.jsonld#",
    "m0": M0C,
    "m1.ext:chemistry": f"{BASE}/ontology/M1_extensions/M1_Chemistry.jsonld#",
}
for local in ("scoreA", "scoreS", "scoreF", "scoreIt", "scoreD",
              "scoreR", "scoreE", "scoreV", "scoreO", "scoreIm",
              "asfidMean", "revoiMean", "epistemicGap"):
    ctx["m0:" + local] = coerce(local)
ctx["@base"] = f"{BASE}/ontology/"
doc["@context"] = ctx

onto = doc["@graph"][0]

# ---------- 2. owl:imports ----------
onto["owl:imports"] = [
    f"{BASE}/ontology/M3_GenesisGrammar.jsonld",
    f"{BASE}/ontology/M2_GenericConcepts.jsonld",
    f"{BASE}/ontology/M1_CoreConcepts.jsonld",
    f"{BASE}/ontology/M0_Common.jsonld",
]

# ---------- 3. version + changelog ----------
onto["owl:versionInfo"] = "2.0.0"
onto["m2:changelog"] = [
    {
        "version": "2.0.0",
        "date": "2026-08-21",
        "changes": ("SHACL v1.6 conformance pass. Flat bare-numeric scores "
                    "m0:scoreA..m0:scoreIm (dropped m0:asfidScores/m0:revoiScores sub-objects "
                    "and *_score aliases). Added owl:imports M0_Common.jsonld. Namespace fixes: "
                    "removed relative m0:epistemicGap @context def; m1core: -> m1:. Notation reform: "
                    "retired tensor/sum glyphs removed (now \u00d7 / + / | only); formulas aligned to "
                    "canonical M2 read from HEAD (Signature It\u00d7Ss|V, Component St\u00d7It|L, "
                    "Synergy It\u00d7D|_^, Composition St\u00d7It\u00d7A|_^, Trigger D\u00d7It, Process D\u00d7F). "
                    "Removed ket/Hilbert state-vectors and norms (structural-grammar alignment). "
                    "epistemicGap recomputed = |asfidMean-revoiMean|/\u221a2 = 0.099 (was 0.474, old Hilbert norm).")
    },
    {
        "version": "1.2.1", "date": "2026-06-26",
        "changes": "ACTION3: Added m0:focalApplicable=true."
    },
    {
        "version": "1.2.0", "date": "2026-04-18",
        "changes": ("SHACL v1.1 realignment: @type owl:Ontology, m3:ontologyType m3:Poclet, "
                    "m1:domain migrated from m0:domain, scores extracted from mapSpace, epistemicGap added.")
    },
]

# ---------- 4. flat scores (bare numerics) + means + canonical gap ----------
for k in ("m0:asfidScores", "m0:revoiScores"):
    onto.pop(k, None)

scores = {
    "m0:scoreA": 0.75, "m0:scoreS": 0.90, "m0:scoreF": 0.60, "m0:scoreIt": 0.80, "m0:scoreD": 0.50,
    "m0:scoreR": 0.90, "m0:scoreE": 0.70, "m0:scoreV": 0.95, "m0:scoreO": 0.80, "m0:scoreIm": 0.90,
}
asfid_mean = round((0.75 + 0.90 + 0.60 + 0.80 + 0.50) / 5, 3)   # 0.71
revoi_mean = round((0.90 + 0.70 + 0.95 + 0.80 + 0.90) / 5, 3)   # 0.85
gap = round(abs(asfid_mean - revoi_mean) / (2 ** 0.5), 3)        # 0.099

# rebuild onto dict with scores inserted right after m1:domain, in a clean order
new_onto = {}
for k, v in onto.items():
    if k == "m0:epistemicGap":
        continue  # re-added below as bare numeric
    new_onto[k] = v
    if k == "m1:domain":
        for sk, sv in scores.items():
            new_onto[sk] = sv
        new_onto["m0:asfidMean"] = asfid_mean
        new_onto["m0:revoiMean"] = revoi_mean
        new_onto["m0:epistemicGap"] = gap
onto = new_onto
doc["@graph"][0] = onto

# ---------- 5. m1core: -> m1: ----------
if "m1core:simulationTitle" in onto:
    onto["m1:simulationTitle"] = onto.pop("m1core:simulationTitle")

# ---------- 6. notation reform in nested string values ----------
# 6a. flameColorByTemperature.m2GenericConcept -> canonical Signature
comps = onto.get("m0:FireTriangle:components", [])
for c in comps:
    fcbt = c.get("m0:FireTriangle:flameColorByTemperature")
    if isinstance(fcbt, dict) and "m2GenericConcept" in fcbt:
        fcbt["m2GenericConcept"] = "Signature (It \u00d7 Ss | V)"

# 6b. synergyPrinciple.formula  (⊕ -> ×, Territory product of physical components)
sp = onto.get("m0:FireTriangle:synergyPrinciple")
if isinstance(sp, dict) and "formula" in sp:
    sp["formula"] = "Fuel \u00d7 O\u2082 \u00d7 Heat \u2192 Fire (emergent)"

# 6c. criticalGenericConcepts -> canonical M2 formulas (read from HEAD)
CANON = {
    "Component":   "St \u00d7 It | L",
    "Synergy":     "It \u00d7 D | _^",
    "Composition": "St \u00d7 It \u00d7 A | _^",
    "Trigger":     "D \u00d7 It",
    "Process":     "D \u00d7 F",
}
gcm = onto.get("m0:FireTriangle:GenericConceptsMobilized", {})
for item in gcm.get("criticalGenericConcepts", []):
    nm = item.get("name")
    if nm in CANON:
        item["formula"] = CANON[nm]
    if nm == "Component" and "status" in item:
        # Component now exists in M2 (verified at HEAD) — the "gap identified" note is stale
        item["status"] = "Present in M2 (m2:Component)"

# ---------- 7. structural-grammar alignment: drop ket/Hilbert vestiges ----------
def strip_ket(block, keys):
    if isinstance(block, dict):
        for k in keys:
            block.pop(k, None)

# territorySpace: drop ket stateVector + Hilbert norm
strip_ket(onto.get("m0:FireTriangle:territorySpace"),
          ["stateVector", "norm"])

# mapSpace: drop ket state-vectors + Hilbert norms (keep numeric states + justifications)
strip_ket(onto.get("m0:FireTriangle:mapSpace"),
          ["reviStateVector", "reviNorm", "asfidStateVector", "asfidNorm"])

# revoi block: drop ket stateVector
strip_ket(onto.get("m0:FireTriangle:revoi"),
          ["stateVector"])

# alternativeObservers: drop each ket stateVector
for obs in onto.get("m0:FireTriangle:alternativeObservers", []):
    strip_ket(obs, ["stateVector"])

# epistemicGap descriptive block: replace Hilbert ‖·‖ formula, drop Hilbert norm,
# reframe as structural-grammar Territory-vs-Map ASFID divergence (keep per-dim analysis)
eg = onto.get("m0:FireTriangle:epistemicGap")
if isinstance(eg, dict):
    eg.pop("norm", None)
    eg["formula"] = ("Per-dimension ASFID divergence between Territory profile "
                     "(observed fire) and Map profile (triangle model). "
                     "Canonical scalar gap at root: m0:epistemicGap = |asfidMean \u2212 revoiMean| / \u221a2.")
    eg["interpretation"] = ("Model captures the essence but simplifies reality; "
                            "largest divergences on S, F, D (see below).")
    # deltaVector kept as descriptive per-dimension (A,S,F,It,D) difference

# ---------- write ----------
with io.open(DST, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")

# report residual forbidden operators
txt = open(DST, encoding="utf-8").read()
print("Rewrote", DST)
print("Residual \u2297:", txt.count("\u2297"), " Residual \u2295:", txt.count("\u2295"))
print("Residual ket '\u27e9':", txt.count("\u27e9"), " Residual norm '\u2016':", txt.count("\u2016"))
print("asfidMean/revoiMean/gap =", asfid_mean, revoi_mean, gap)
