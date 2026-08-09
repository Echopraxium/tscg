# PEPITE-013 fix — xsd:float coercion on prose (score justifications)

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-08-09
**Base**: repo HEAD `d5e81a7` (after the API-server fixes)
**Golden**: M0-only change → the M1 golden gate (16/151/3) is NOT affected.

## The defect (KitArchitect-KitArchitect-01-01's PEPITE-KitArchitect-01-013)

The `@context` of 6 M0 files coerces every `X_score` term to `@type: xsd:float`
GLOBALLY. On numeric scores that is redundant (the data already carries
`{"@value": "0.95", "@type": "xsd:float"}`). But the same `X_score` keys are reused
inside `scoreJustification` to hold PROSE — so the coercion casts prose to `xsd:float`.
Loaded in RDF, those become invalid float literals (rdflib raises
`could not convert string to float: 'VSM defines clear viable equilibrium states…'`).

## The fix

Remove the `@type: xsd:float` coercion from the `X_score` term DEFS in the `@context`,
keeping the `@id`. Numeric scores keep their type (via their own local `@value`/`@type`);
the justification prose stops being cast.

Scope: exactly the **6 files** with the active defect (numeric scores + prose
justification): M0_VSM, M0_Kidneys, M0_TscgCanopyGraphVizProto, and the 3 tscg-tools
(APIServer, Explorer, PocletMiner). NOT the 29-file `M0_Poclet#` rebrand — that is a
separate lot.

## Proven in a VM before delivery

- 6 files still parse as JSON.
- The diff removes ONLY `@type: xsd:float` from score DEFS in `@context`; **0 `@value`
  data nodes touched** (numeric scores untouched).
- JSON-LD expansion of M0_VSM: **before = 13 numeric-float + 10 prose-as-float**
  (10 rdflib cast failures); **after = 13 numeric-float + 0 prose-as-float**. Defect gone.
- M0_VSM contains a deprecated-term (`ORIVE`) changelog line — the script edits in place
  on your machine, so that literal is NOT corrupted (verified: count unchanged).

## How to apply (LOCAL script — not delivered files)

Because M0_VSM carries the `ORIVE` literal, the fix is delivered as a script you run,
never as whole files.

```
# from the repo root
python fix_pepite_KitArchitect-01-013.py .
git diff        # confirm: only '@type: xsd:float' removed from @context score DEFS,
                #          no @value touched, no ORIVE line altered in M0_VSM
```

The script is transactional (validates all 6 files in memory, writes only if all pass)
and guarded (re-parses JSON; asserts no `_score` def keeps `xsd:float`). It handles both
one-line and multi-line def formats.

Then commit scoped to the 6 files.

## Next (separate lots)

1. **Rebrand `M0_Poclet#` → `M0_Common.jsonld#`** (29 files) — the phantom-namespace
   backlog. The WS-5 validator, extended to scan M0 and flag `M0_Poclet#` (which does
   not exist) vs `M0_Common` (which does), gives the 29→0 gauge and verifies it.
2. **Validator TYP family** — detect "xsd:float coercion on a prose field" as the
   durable guardian against KitArchitect-01-013 recurring (the corpus counterpart of the API regression
   tests).
