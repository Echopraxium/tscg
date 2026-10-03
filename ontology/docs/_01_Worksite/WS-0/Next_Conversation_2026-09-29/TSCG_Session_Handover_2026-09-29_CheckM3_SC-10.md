# TSCG Session HandOver — 2026-09-29 — Check-M3 (SC-10) + Application type & facets

**Author**: Echopraxium with the collaboration of Claude AI
**Purpose**: open a dedicated session to (A) implement `check-M3` (WS-0 / SC-10 "M3 grammar"),
then (B) grave the M3/M1 additions decided on 2026-09-29, gated by that new check.
**Where to put this**: `ontology/docs/_01_Worksite/WS-0/Next_Conversation_2026-09-29/`

---

## 1. Load first — by name

- **`head-over-memory`** — authority discipline.
- **`tscg-ontology-diagnosis-pipeline`** — every ontology change goes through its 6 phases.
- **`tscg-generate-mn-grammars`** — SHACL grammar generation for M3 (Part A).

## 2. Governing rule

HEAD is the only authority. Every fact tagged *observed 2026-09-29* below was read on
HEAD that day but is **perishable**: re-verify before relying on it. This HandOver
carries decisions and pointers, not framework content.

## 3. Fresh session state

- **Current HEAD**: not measured in the originating session — measure at start.
- **Active worksite**: WS-0 / **SC-10 "M3 grammar"** — `scoped`, rank 8,
  note "prerequisites met; plumbing, not arbitration" *(observed in `worksite.yaml`)*.
- **Staleness to fix**: `ontology/docs/_01_Worksite/worksite.yaml` meta says
  `head: f0daa1a`, `generated: 2026-08-08`, and still shows SC-3 as `design-decided`
  although SC-3 was graved on 2026-09-01. Resync as part of this session.
- **Working copy in flight**: none.
- **Origin**: decisions came from the Ship Builder design session (a modular 3D ship
  editor in Godot for a dogfight game team). Its spec lives in a Claude doc:
  https://claude.ai/code/artifact/ce45932f-525a-4506-b1df-42c1a9b30058

---

## 4. Part A — implement `check-M3` (do this FIRST)

**Why first**: Part B modifies M3. Like SC-3 waited for its gate (`grave_after: WS-5`),
the M3 additions should be graved *under* a gate that can fail.

**Deliverables** (mirror `check-M1`; re-read its structure on HEAD before coding):
- `ontology/cli-tools/check-M3/M3_Schema_shacl.ttl`
- `ontology/cli-tools/check-M3/check_M3.py` (run from `ontology/cli-tools/`, like `check_M1.py`)
- Wiring into `ontology/cli-tools/run_all_layers.py` + a baseline in `golden_values.json`
- `check_M3_README.md`

**Proposed check families** (target = the M3 files imported by `M3_GenesisGrammar.jsonld`):
1. **Headers**: `owl:versionInfo` semver, `dcterms:creator` exact string,
   `m3:ontologyType` ∈ {Genesis, GenesisExtension}, changelog ≤ 7 entries (M3 exception).
2. **Notation**: no `⊗` anywhere; R = Representability (never Reproducibility).
3. **Alphabet**: exactly 16 primitives (Gt 5 + Gm 5 + Gs 6), unique type symbols —
   read the actual alphabets from the three grammar files, do not hard-code from memory.
4. **Type scheme**: every `skos:hasTopConcept` of `m3:TscgOntologyTypeScheme` is
   `owl:Class` + `skos:Concept`, `rdfs:subClassOf m3:TscgOntologyType`, `skos:inScheme` the scheme.
5. **Facets**: every `m3:FacetValue` has exactly one `m3:valueOf` → an `m3:Facet`;
   `hasFacetValue` targets are IRIs. After Part B: every `m3:Facet` has a `m3:facetTarget`.

**Verify before writing**:
- The Bootstrap states the "≤ 7 changelog entries" M3 rule is "documented in the M3 SHACL
  shape", yet no M3 SHACL appears in the file tree. Find it or confirm the Bootstrap anticipates.
- The WS-5 validator's **AXIS** family already checks part of the facet registry.
  Decide the split (SHACL vs AXIS) to avoid duplicate findings.

**Done when**: check-M3 passes on current HEAD (or its findings are triaged by Michel),
baseline recorded in `golden_values.json`, `run_all_layers` green, SC-10 set to `done`.

---

## 5. Part B — decisions locked by Michel (2026-09-29) — do NOT relitigate

**M3 (`M3_GenesisGrammar.jsonld`, observed v4.6.0)**
- New instance type **`m3:Application`** in `m3:TscgOntologyTypeScheme`
  (nature = software application; *not* reflexive, unlike `m3:TscgTool`).
  "Prototype" is NOT part of the type name — maturity is a facet.
- New global facet **Maturity**: values `Prototype`, `Released`.
- New global facet **Purpose**: value `Editor` (only value for now; extensible).
- New property **`m3:facetTarget`** on `m3:Facet`, values **Instance** and **Domain**
  (what the facet classifies). **No `facetScope`**: a facet's scope is read from the
  file/namespace that declares it (M3 = global; an M1 extension = that domain) —
  redundant data rejected to avoid Layer Cake heaviness.
- Suggested IRIs (to confirm against existing naming, e.g. `m3:audience.KitUser`):
  `m3:Maturity`, `m3:maturity.Prototype`, `m3:maturity.Released`, `m3:Purpose`,
  `m3:purpose.Editor`, `m3:facetTarget`, `m3:facetTarget.Instance`, `m3:facetTarget.Domain`.
- Existing facet `m3:Audience` must receive `m3:facetTarget` = Instance.

**M1**
- `m1:domain` stays a **property** (not a facet). Register **`m1:domain:VideoGame`**
  in `M1_Domains.jsonld` (observed v1.5.0, 22 domains) with `m1:subdomains`:
  **Simulation, Space, MMO, RPG**. *(relatedDomains ComputerScience / GameTheory /
  Physics were only a proposal — confirm with Michel.)*
- New extension `M1_extensions/<video_game>/M1_VideoGame.jsonld` (check folder-naming
  convention on HEAD) declaring **instance facets** (`facetTarget` = Instance):
  **Genre** {Simulation, RPG}, **Setting** {Space}, **PlayerScale** {MMO}.
  Precedent: `M1_Cartography.jsonld` domain facets.

**SHACL M0** (`ontology/cli-tools/check-M0/M0_Instances_Schema_shacl.ttl`, observed v1.7)
- Add `m3:Application` to the closed `sh:in` list of `m3:ontologyType`.
- Add a `facetTarget` coherence constraint (Instance-targeted facet values carried only
  by M0 instances).

**Records**: `facetTarget` extends the SC-3 mechanism → update the SC-3 Decision Record
(new version or addendum). Version bumps + changelog entries on every touched file.

---

## 6. Open decisions for Michel (batch them)

1. SHACL-vs-AXIS split for facet checks (Part A).
2. `m3:TransDisclet` is in the type scheme but absent from the M0 SHACL `sh:in` list,
   and `instances/transdisclet/` is empty — include, or leave as is?
3. `relatedDomains` for VideoGame.
4. Folder for Application instances (proposal: `instances/applications/`), for the
   future `M0_ShipBuilder.jsonld` (Maturity = Prototype, Purpose = Editor, domain VideoGame).

## 7. Out of scope for this session

The Ship Builder M0 instance itself, its Godot implementation, and the Ship Builder spec.

## 8. Gates

Claude: rdflib parse, pyshacl, check-M3 / check-M0 / AXIS on a fresh HEAD clone.
Michel (Windows): Pellet, `check_M1.py`, `run_all_layers`. Nothing is committed without
Michel's sign-off at each pipeline gate.
