# TSCG HandOver — WS-5 debt lots, 2026-10-12: class/instance separation done, domains are classes; next SC-5b

**Author**: Echopraxium with the collaboration of Claude AI
**Date**: 2026-10-12
**Follows**: `../Next_Conversation_2026-10-11/TSCG_HandOver_WS-5_2026-10-11_session2.md`
(and, through it, the 2026-10-06 HandOver: working method, push path).

> Thin loader, not a content snapshot (Smart Prompt §4). Every volatile fact below
> (SHAs, counts, versions) is **session state at handover time**: re-verify against
> HEAD before use.

---

## 0. Load first — by name

1. **`head-over-memory`** — authority discipline (HEAD > corpus > memory).
2. **`tscg-ontology-diagnosis-pipeline`** — every lot touches the gate or ontologies.
3. **`tscg-generate-mn-grammars`** — only if a lot touches a SHACL grammar (the M0 lot does).
4. Then read from HEAD:
   - `ontology/docs/_01_Worksite/TSCG_Debt_Overview.md` **1.14.0** — §8.0f is the record
     of this session (lots C2, C1b, S, SC-5 and everything left open).
   - `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` — invariants "Classes and
     instances are separated" and "A domain is a class too" (both new).

---

## 1. Fresh session state (at handover — re-verify)

- **HEAD**: the commit carrying this HandOver, on top of `e9beb47` (Lot SC-5), pushed
  2026-10-12. Confirm with `git log --oneline -8`.
- **Gate**: `cd ontology/toolchain && python run_all_layers.py` → `GATE: PASS`:

  | Layer | files | errors | warnings | shacl_violations |
  |---|---|---|---|---|
  | M3 | 5 | 141 | 604 | 3 |
  | M2 | 1 | 1 | 1368 | 7 |
  | M1 | 17 | 133 | 1 | 296 (one result counted twice — `check_M1` double count, still open) |
  | M0 | 43 | 124 | 0 | 22 |

- **Tests**: `python -m pytest -q` → 62 passed on Michel's machine (Pellet tests skipped in
  Claude's sandbox: Java too old → 60 + 2 skipped there).
- **Push path** unchanged: Claude → `format-patch` → `git am` + gate on a fresh clone →
  Michel `git am`, gate, tests, push. Patches named `1_…`, `2_…`.

### Shipped 2026-10-11 → 10-12 (this session)

| Commit | Lot | Content |
|---|---|---|
| `a4ee738` | **C2** | combo punning removed from 139 M1 combos and forbidden (M1 SHACL SHAPE 12, `check_M1` CMB001) |
| `c021697` | **C1b** | 69 non-combo `subClassOf` strings → IRIs; phantom parents resolved; `m1:Domain` declared |
| `b1f0669` | **S** | `m2:State ⊑ m2:Node` (statecharts), formula/family aligned on Node |
| `e9beb47` | **SC-5** | domains are classes ⊑ `m1:Domain`; registry, DCC010, M1 SHACL 1.8.0; KnowledgeField purged, `m2:knowledgeField` → `m1:domain`; golden M1 149/1/446 → 133/1/296 |

### Decisions taken (Michel, 2026-10-11/12) — recorded in Debt Overview §8.0f

- Classes in M2/M1, instances in M0; no punning (a name is a class OR an individual).
- A domain is an `owl:Class` ⊑ `m1:Domain` (extension class `m1:extension:<ext>:<Name>`,
  or `m1:domain:<Name>` in `M1_Domains`); a subdomain may have several parents
  (intersection); "il n'y a plus de KnowledgeField, c'est Domain".
- **What can be inferred is not stored**: `m1:subdomains` (→ `rdfs:subClassOf`),
  `m1:instanceCount` / `m1:instanceExamples` (→ from the M0 instances).
- An M0 instance designates its domain by the **IRI** of a domain class, never a string.
- Links between classes that are documentation are annotations (`m1:relatedDomains`,
  `m1:domain`: `owl:AnnotationProperty`, IRI values).
- `m2:State ⊑ m2:Node`; Protocol = attribute of `m2:Workflow` (use cases of a workflow in a
  UML swimlane, on a statechart: State, Event); `biology:CellularCommunication` will
  specialise it.

---

## 2. Next goal — lot SC-5b: subdomains become classes

Decision (a), Michel 2026-10-12: `m1:subdomains` is deleted **in the same lot** as the
subdomain classes are created, so nothing is lost.

1. **Measure** on HEAD: `m1:subdomains` holds **139 strings on 22 domain classes**
   (registry + extensions; re-measure).
2. **Table for Michel, line by line** — for each string: keep as a subdomain class
   (`m1:domain:<Name>` or `m1:extension:<ext>:<Name>`), parent domain(s) (several allowed),
   merge with an existing domain (e.g. "Physiology", "Neuroscience" vs `Neurobiology`),
   or drop (a theme, not a domain: "Thermodynamics of Ecosystems"?). Duplicates across
   domains (the same string under two parents) = one class with two parents.
3. Michel validates the table; then create the classes, delete `m1:subdomains`, update
   the registry README / Debt Overview. DCC010 already reads the transitive hierarchy;
   SHAPE 11 `DomainClassShape` already targets `rdfs:subClassOf+ m1:Domain`.
4. Settle at the same time the **name pairs**: registry `MusicTheory` vs `music:Music`,
   `SystemsTheory` vs `systemic_modeling:SystemicModeling` (same? subclass?), and the
   dangling `relatedDomains` targets `m1:domain:Mathematics` (5), `m1:domain:Anthropology` (1).
5. Expected gate: M1 counts unchanged unless a new class lacks a label (SHAPE 5/11).

## 3. Then — lot M0: domain IRIs

- `m1:domain` in **41 M0 instance files** (re-measure) is free text ("Biology",
  "Optics / Color Science", "Thermodynamics", "TSCG", "Virtual machine design", lists, one
  `m1.ext:biology:DevelopmentalBiology`) → mapping table (string → domain/subdomain class
  IRI), validated by Michel; after SC-5b so subdomains exist.
- Add the rule to the M0 checks (M0 SHACL `M0_Instances_Schema_shacl.ttl` and/or
  `check_m0_instances.py`) with a negative test; expect M0 counts to move (show first).
- Then delete `m1:instanceCount`, `m1:instanceExamples` and the `M1_Domains` header counts
  (`m1:domainCount`, `m1:totalInstances`, `m1:otherInstances`) after checking the query
  gives the same lists; TscgOntologyExplorer reads `M1_Domains` (check it).

## 4. Other lots queued (Debt Overview)

- **Protocol** (M2 candidate / attribute of `m2:Workflow`), then
  `biology:CellularCommunication` (its parent `m1:CommunicationPattern` is still a phantom
  string).
- **Part (a), M2** (WS-1 B2): 1110 uses of data/object properties on M2 classes → the
  documenting ones as `owl:AnnotationProperty`; Pellet observations of §8.0f as input.
- **Engine `advanced=False`** (`validator/checks/shacl_runner.py`): the `sh:SPARQLTarget`
  shapes (combo shapes since C1, `DomainClassShape` since SC-5) are not run on the engine
  path → the engine and the LayerCake Health Map under-report M1. Fix = `advanced=True`;
  moves the engine's M1 numbers (not the gate's).
- KnowledgeField still in tools/old docs: `src/` (reasoner.py, Metaconcepts_List.py),
  TscgPocletMiner (`knowledgeFieldCombos` JSON key, SystemPrompts.js), CanopyGraphVizProto,
  `ontology/docs/*KnowledgeField*`, old Smart Prompts, published papers (leave those).
- the comments of the domain classes BusinessModeling / Economics / Geology still say "bicephalous"
  (lot R2, ~45 adjectives); `Fm1m2(Education, Trade-off)` uses the M2 id `m2:Trade-off`.
- Still queued from 2026-10-11: one role one property batch 3, lot R2, lot-NSRESOLVE,
  S5-1/S5-1b/S5-2/S5-3, `typeS/typeI` renaming, `check_M1` double count, WS-13 priority.

## 5. Decisions waiting for Michel

1. SC-5b table (line by line) and the name pairs (§2.4).
2. M0 mapping table (§3).
3. Still open from 2026-10-11: WS-13 priority; Compendium tab visibility; M0 bare-key gauge
   owner.

## 6. Outside git — Project Knowledge to refresh

- Reload `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` into the Project
  "TSCG Workshop v1" (two new invariants: class/instance separation, domains are classes).
- Re-upload `TSCG_FileTree.md` / `TSCG_ReferenceCorpus.md` from HEAD if they changed.
