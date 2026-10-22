# HandOver — SC-3 "Facet as an M3 principle" — 2026-09-01

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: resume SC-3 in a fresh, HEAD-anchored **graving session**. Paste this as the
opening message of a new conversation in the TSCG project.
**Governing rule**: HEAD is the only authority. Load the skills, re-measure HEAD, and grave
one isolated lot at a time (Record §8). Nothing in SC-3 is graved yet.

---

## 0. Reprise checklist (do first)

1. Fetch and follow the Smart Prompt: `docs/reboot-kit/TSCG_SmartPrompt.md` (loads skills:
   `head-over-memory`, `tscg-ontology-diagnosis-pipeline`, `tscg-instance-pipeline`).
2. **Re-measure HEAD** — the numbers below are perishable (baseline 2026-08-28). Confirm
   layer versions and that `m3:Facet` is still absent before graving.
3. Carry the three produced artifacts (see §4) into the repo.

---

## 1. What SC-3 is now — RE-SCOPED this session (read carefully)

SC-3 is an item of **WS-0 "Structural Cleanup"** (`grave_after: WS-5`).

**The ratified Record `SC-3_Facet_Decision_Record.md` v1.0.0 is now PARTLY OBSOLETE.**
It describes a **4-axis decomposition of `ontologyType`** (SCALE / NATURE / AUDIENCE /
DOMAIN). **That whole decomposition was ABANDONED this session**, by Head Chef decision:

- **NATURE is the backbone**, not a facet. A facet (per the graved `m0:Facet` doctrine) is a
  *conferred, contingent, Map-perspective role*. NATURE (SystemModel/Framework/Grammar/Tool)
  is *what the artifact essentially is* — Territory, exactly-one — i.e. the backbone tree.
  Typing it as a facet is the "fabricate an orthogonality" abuse the Record's own §5 warns of.
- **SCALE** (Poclet/CaseStudy/RealWorldSystem) is a **refinement of the SystemModel branch of
  the backbone**, not an orthogonal facet.
- Only **AUDIENCE** passes the conferred/contingent/Map test → the single genuine facet.

**New SC-3 scope**: grave the **Facet mechanism** + the **Audience facet** only.
**`ontologyType` is left entirely untouched.** No SCALE, no NATURE, no DOMAIN (DOMAIN was
always deferred to SC-5).

➡ **A Record v2.0.0 is DUE** to capture this re-scope (see §7). Do not grave against v1.0.0.

---

## 2. HEAD baseline (re-measured 2026-08-28, sha 7da58af)

| file | version | note |
|---|---|---|
| ontology/M3_GenesisGrammar.jsonld | 4.5.0 | target of the graving; `skos` already in @context |
| ontology/M2_GenericConcepts.jsonld | 16.19.0 | untouched |
| ontology/M0_Common.jsonld | 1.1.0 | holds `m0:facet.*` apparatus to remove |
| ontology/M3_GrammarFoundation.jsonld | 2.5.0 | untouched |

- `m3:Facet` / `m3:FacetValue` / `m3:valueOf` / `m3:hasFacetValue` / `m3:Audience` /
  `m3:audience.*` : **all ABSENT at HEAD** (collision-free, re-verify).
- `m0:Facet`, `m0:hasFacet`, `m0:facet.Democratization`, `m0:illustratesConcept`,
  `m0:RoleGrounding`+`roleGrounding.{Reused,Designed}` : **present** in M0_Common.

---

## 3. The FROZEN model (all decisions closed)

Three levels + two links (full JSON-LD fragment in `SC-3_M3_Facet_Draft_v2.md` §2 — the
single source; do not retype it from here):

| level | construct | example |
|---|---|---|
| mechanism class | `m3:Facet` (owl:Class) | — |
| an axis (a facet) | *individual* `a m3:Facet` = `skos:ConceptScheme` | `m3:Audience` |
| a value | `m3:FacetValue` (owl:Class) = `skos:Concept` | `m3:audience.KitUser` |
| value → axis | `m3:valueOf` (⊑ `skos:inScheme`) | `audience.KitUser valueOf Audience` |
| carrier → value | `m3:hasFacetValue` (multi, IRI-only) | `inst hasFacetValue audience.KitUser` |

**Closed decisions:**
- **Doctrine**: narrow (kept from HEAD `m0:Facet`) — facet value = conferred/contingent/
  Map-perspective role, anchored `m2:Role` Ss|K, distinct from ScoringProperty/FocalProperty.
- **Contract = the value itself** (no separate contract object). A `m3:FacetValue` carries its
  obligations as its own properties; none for AUDIENCE. Contracts are compositional (union of
  the values a carrier holds), each a conditional SHACL shape. *(Sieve/EpistemicResidue will
  later be a FacetValue WITH a contract — the mechanism will be in place.)*
- **#1** carrier property = generic **`m3:hasFacetValue`** (axis is an individual, so no
  per-axis property).
- **#2** Audience is **optional** (no "≥1 Audience" obligation).
- **#3** inter-value relations **deferred** — produce→consume chain (Architect→Crafter→User)
  documented in prose in `Audience`'s comment; **no** relation property graved
  (no broader/narrower/related/precedes/consumes). SKOS only if/when a 2nd ordered facet needs it.
- **Names (WS-4)** frozen: convention **(A) per-axis** — `m3:audience.<Value>` (not `facet.<Value>`).
- **Democratization → `audience.KitUser`**; its old contract (illustratesConcept/roleGrounding)
  is **dropped**, not carried over.

---

## 4. Artifacts produced this session (carry into the repo)

1. **`SC-3_M3_Facet_Draft_v2.md`** — the frozen model: M3 fragment (§2), M0 removals (§3),
   SHACL edits (§4), migration (§5), locks (§6). **The graving spec.**
2. **`axis.py`** — the WS-5 **AXIS** check family that gates SC-3. Destination:
   `ontology/cli-tools/validator/checks/axis.py` (sibling of `ctx.py`). Tested 7/7 in isolation.
   Registry `_FACET_VALUES` held in-file (mirrors §2; a later lot should load it from M3).
3. **`M0_QRCodeToPocketCity.jsonld`** — the single migrated instance (Democratization →
   `hasFacetValue audience.KitUser`; changelog 1.1.0). `axis.run` → **gate-green**.
   Apply **after** the M3 fragment is graved (it references `m3:audience.KitUser`).

---

## 5. Gauge & locks

- **Gauge X = 1.** Only `QRCodeToPocketCity` carried Democratization (of 42 in-scope M0
  instances). FireTriangle / ExposureTriangle are *cited in doctrine* but do **not** declare
  the facet. → M0 migration is one file.
- **Lock 1 — Pellet punning: LIFTED by construction.** The v2 model has no punning (rdflib
  overlap-check: zero class/individual/property overlap; dotted local names parse). Final
  reasoner confirmation deferred to the repo `cli_tools/owl_reasoning_test/` on project Java
  (this session's Java was too old for owlready2's Pellet jar — tooling, not the model).
- **Lock 2 — names WS-4: FROZEN**, convention (A). WS-4 formal worksite not yet opened;
  this is the de-facto convention to formalise there.
- **Lock 3 — migration: READY**, gate-green.

---

## 6. Graving steps (the remaining work — a fresh isolated session, Record §8)

1. Re-measure HEAD (§0.2); confirm `m3:Facet` still absent.
2. Insert the M3 fragment (draft v2 §2) into `M3_GenesisGrammar.jsonld`; bump its version.
3. Remove the `m0:facet.*` apparatus from `M0_Common.jsonld` (draft v2 §3); bump its version.
4. Edit the M0 SHACL (draft v2 §4): drop the 3 Democratization/roleGrounding shapes; rename
   `ForbidStringHasFacetShape` → `ForbidStringHasFacetValueShape`.
5. Apply `M0_QRCodeToPocketCity.jsonld` (the migrated file).
6. Integrate `axis.py` (2 lines in `tscg_validator.py`): `from checks import axis as axis_check`
   and `_IMPLEMENTED = {"CTX": ctx_check, "AXIS": axis_check}`. Run `--layers M3,M0` → **0 ERROR**.
7. Head Chef's formal gates: linter · Pellet (owl_reasoning_test) · SHACL CONFORMS:True ·
   run_all_layers · golden diff. Then commit (M3 + M0_Common + SHACL + QRCode + axis.py together).

---

## 7. Record v2.0.0 — DUE

Write `SC-3_Facet_Decision_Record.md` **v2.0.0** capturing the re-scope: mechanism + Audience
only, `ontologyType` untouched, NATURE=backbone / SCALE=backbone-refinement, contract-on-value,
decisions #1–#3, convention (A). Mark v1.0.0's 4-axis model as superseded.

---

## 8. On hold (NOT SC-3 — do not lose)

- **Phase-shift oscillator poclet** — the *original topic of the session that spawned all this*.
  Reading **C**: "round-trip as a fidelity test" (encode → decode → redraw; the un-redrawable
  part = the epistemic residue). Support circuit = **phase-shift oscillator** (transistor + 3×RC),
  chosen sinusoidal. Étape 2 (analysis) never started — it was paused when SC-3 opened.
- **EpistemicResidue / Sieve** — diagnosed as a `FacetValue` **with a contract** (round-trip +
  residue delta), NOT a new `ontologyType`. Waits for the Facet mechanism to be graved.

---

*State: SC-3 model frozen, gate built & tested (axis.py 7/7), gauge measured (X=1), migration
ready (gate-green), punning cleared, names fixed (A). Ready to grave; not graved. Resume here.*
