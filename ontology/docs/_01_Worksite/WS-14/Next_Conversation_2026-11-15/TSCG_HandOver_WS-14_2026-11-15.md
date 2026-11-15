# TSCG HandOver — WS-14 Simulation convergence, and the Worksites dependency graph (2026-11-14 / 15)

**Date**: 2026-11-15 (evening) · **Author**: Echopraxium with the collaboration of Claude AI
**Kind**: HandOver (Smart Prompt v17 §4). It only loads and points; it holds no authoritative
framework content. This is the "other conversation" that the evening HandOver
`_02_housekeeping/2026_11_15/TSCG_HandOver_2026-11-15_evening.md` mentions for WS-14.

---

## 1. Load first — by name

- **`head-over-memory`**: every verifiable fact below is a *pointer to check at HEAD*.
- **`tscg-ontology-diagnosis-pipeline`**: before any SIM-13 lot (it changes ontology files).
- **`tscg-m2-candidate-filter`**: before any new M2 term (R / I elements, effort / flow, a facet).
- For Kit work: `kit/README.md`, then `kit/ENGINE_SCOPE.md`.

Then read at HEAD:
1. `ontology/docs/_01_Worksite/WS-14/worksite.yaml` — items SIM-0 … SIM-13, their state.
2. `ontology/docs/_01_Worksite/WS-14/WS-14_Simulation_Convergence.md` — origin, direction, invariants.
3. `ontology/docs/_01_Worksite/WS-14/WS-14_SIM-13_M1_SimulationEngine_Scoping.md` — the open decisions D1–D8.
4. `lib/simulation/README.md`, then `FourLegs/README.md` (migration backlog) and `TwoLegs/README.md` (page inventory).

---

## 2. Session state (perishable — verify, do not trust)

- Pushed by Michel: 16 commits on top of `3425171`, the last ones "Compendium: sub-worksites
  nested under their worksite (WS-0 > SC-3)" and "Compendium: cross-links between the
  worksites graph and the health map". *Check with `git log --oneline -17`.*
- Checks run before the push: acceptance gate `GATE: PASS` (incl. PATH_CHECK 0 finding),
  `node kit/tools/check_laws.js` PASS (0 FAIL, 5 WARN),
  `python ontology/toolchain/worksite_graph.py --check` (0 error). Re-run them, do not
  copy their counts from here.
- The first GitHub Actions run with the new `checks` job was not observed from the session:
  look at the Actions tab, and at the Project management page of the published Compendium.
- Not done: `docs/reboot-kit/TSCG_FileTree.md` still shows the old paths (regenerate with
  `tscg_generate_filetree.py`).

---

## 3. What was built (pointers)

| What | Where |
|---|---|
| Kit laws as data (`K.LAWS`, `K.ENGINE`), shown "under the hood" | `lib/simulation/ThreeLegs/engine/sim.js` |
| Synoptic (node editor), independent of the laws (`law` option) | `lib/simulation/ThreeLegs/synoptics/synoptic.js` |
| Rule "no physics outside K.LAWS", as a check that fails | `kit/tools/check_laws.js` |
| What the engine can / cannot simulate (tiers A–D, draft) | `kit/ENGINE_SCOPE.md` |
| Three generations of simulations; PyGame moved out of `src/` | `lib/simulation/` (FourLegs, TwoLegs, ThreeLegs) |
| Worksites dependency graph (field `depends_on`, clusters, checks) | `ontology/toolchain/worksite_graph.py` |
| Graph in the Compendium: first item of Project management, foldable, open by default; Worksites folder right under it, SC-n nested under their WS-n; cross-links with the LayerCake Health Map | `cli_tools/compendium/` (template, `build_compendium.py`, `compendium_folders.yaml`) |
| CI job `checks` (graph integrity, check_laws), never blocks the deployment | `.github/workflows/pages.yml` |

---

## 4. What Michel decided (non-verifiable, 2026-11-14 / 15)

- The Kit's "black box" (electronic-piano syndrome: the demo plays by itself) is a defect;
  the model must be explicit, in the spirit of LTspice. Physics hard-coded in a page is the
  thing to remove.
- Library layout: `lib/simulation/` with **FourLegs** (PyGame, obsolete, to migrate),
  **TwoLegs** (one page per poclet, legacy), **ThreeLegs** (the Kit, the future). All
  PyGame is obsolete and must be migrated. Everything converges to ThreeLegs.
- `lib/` holds code only; the simulation *knowledge* (laws) belongs in the ontology:
  an **M1 extension** (`simulation_engine`, the formalism) plus the laws in the domain M1,
  the netlist in M0; an M0 may use several domains. **No "M1.5" layer**: the extension is
  filed by an **m3:Facet** (value `Formalism`), under the SC-3 Facet record.
- Equations: SHACL as the guard rail (it checks, it does not simulate); syntax inspired by
  XMILE; BPML rejected.
- Worksites dependency graph: inline, foldable, **open by default**; "N/A" (not
  "unavailable") when it cannot be generated; routing solved by clustering; the Worksites
  folder right under it; a link each way with the health map.

---

## 5. Open — choose with Michel

1. Validate the 13 `depends_on` entries (12 extracted from the worksites' notes + WS-14 → WS-0).
2. Priority of WS-14 (null).
3. **SIM-2**: validate `kit/ENGINE_SCOPE.md`, incl. `source` / `sink` / `clock` having no M2 class.
4. **SIM-13**: decisions D1–D3, D5–D8 (D4 resolved). Pilot: Thermostat.
5. **SIM-3**: the 5 WARN of check_laws (direct state writes: tutorial initial conditions,
   window click in the scale model, attenuation in Larsen); check_laws in the acceptance gate?
6. Pending proposal (not applied): `lib/` should hold logic only, so the whole PyGame
   scripts could go back to their poclets (4 of 8 are exact duplicates already there;
   `tpack_sim.py` differs from the poclet copy, which is richer). Linked to D4.
7. Element-level links between the two diagrams (health-map node ↔ worksite that repairs
   it): needs the owning worksite as a structured field in the health-map generator.
8. Mobile ergonomics of the graph (tap a box for its card, "real size" with scrolling):
   shown in a mock-up, not applied.

---

## 6. Lesson of the session

The defect was visible in the code but nothing flagged it: the purpose (pedagogical
transparency) was not a checked rule. Turn a purpose into a check that can fail
(`check_laws.js`, `worksite_graph.py --check`), rather than relying on someone noticing.
