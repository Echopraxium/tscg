# TSCG — Session Handover (2026-07-23)

**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Context**: session opened on SC-2. The detour that followed was diagnostic, not
accidental: it found that three SC-1 rules
were enforced on **no M1 extension at all**, that CTX-4 is active breakage rather
than a latent fragility, and that the corpus carries ~4300 keys that never reach
RDF. Everything found was measured, fixed or scoped, committed and pushed. **SC-2 steps 1
and 2 were then executed** (see §2.4); steps 3–5 remain.

**Authority reminder (golden rule)**: the only authority is `git show HEAD:<file>`.
Project snapshots and prior uploads are NOT authorities. This session verified
against HEAD at every step and **the discipline paid twice** (see §7).

Conventions unchanged: English files / French conversation; `@base` short IRIs;
base URI `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/`;
changelog 3 entries (M3: up to 7); no `⊗`/`⊗⇒` (`×`=Gt, `+`=Gm, `|`=Gs);
Fm2/Fm1m2 are functions (comma-args). **NEW**: only `m3:`/`m2:`/`m1:`/`m0:`
prefixes — no `tscg:`, and never a lower-layer prefix inside a higher-layer file.

---

## 0. COMMITTED AND PUSHED (nothing left pending)

Unlike the two previous sessions, **all deliverables are in the public repo**.

| Commit | Content |
|---|---|
| `839257e` | tools: add `tscg_metrics.py` v1.0.0 + README |
| `35e19e3` | tools: rename `_open_cmd_window.bat` → `_00_open_cmd_window.bat` |
| `aac3a05` | **SHACL v1.4.0**: SHAPE 9 dual targetClass (+ golden 468→680) |
| `14e403d` | **M3 ×5**: define `m3:changelog`, adopt it, fix CTX-4, declare 19 props |
| `dd96555` | docs: VOC worksite scoping note |
| `0168207` | docs: rename validator design spec to worksite convention |
| (+1) | docs: rename VOC note to worksite convention |

Naming convention settled for `ontology/docs/_01_Worksite/`:
`TSCG_<Subject>_Worksite_README.md` for scoping notes; `M0_*` reserved for real
TSCG instances (this frees `M0_TscgOntologyValidator_README.md` for the day the
tool actually exists as an `M0_*.jsonld` peer of PocletMiner/Explorer/APIServer).

---

## 1. THE THREE FINDINGS (why this session mattered)

### 1.1 CTX-4 is ACTIVE BREAKAGE, not a fragility

A relative prefix (`"m3": "M3_GenesisGrammar.jsonld#"`) resolves against `@base`
in **identifier** position but **NOT** in **predicate** position. Consequence:
`m3:MonoidalType` (a class) expanded correctly while **every `m3:*` property in the
same file expanded to an unresolved IRI**.

Measured: `M3_GenesisGrammar` had **52 unresolved predicates → 0** after the fix.
`M3_EagleEye` and `M3_SphinxEye`: 4 → 0 each.

**This corrects the 2026-07-18 conclusion.** That session compared `MonoidalType`
— an identifier — across the 5 M3 files, found one IRI, and reported alignment.
The alignment did not hold for properties. CTX-4 was catalogued as "fragile,
resolves today"; it does not resolve today, in the rdflib/pyshacl stack that
`run_all_layers` itself uses.

**Still open: 21 CTX-4 occurrences**, including `M2_GenericConcepts` (relative on
both `m2` and `m3`) and 12 M1 extensions.

### 1.2 SHAPE 9 enforced the SC-1 rules on NOTHING

`M1_Schema_shacl.ttl` SHAPE 9 `ComboFormulaShape` correctly encodes Michel's three
rules (no monoidal operator in a signature; no bare primitive as argument; arity
`Fm2` ≥ 2 concepts, `Fm1m2` ≥ 1 Domain AND ≥ 1 GenericConcept). But it carried a
single `sh:targetClass m2:GenericConceptCombo` with the comment
`# inherited by m2:DomainConceptCombo`.

**That inheritance assumption is false in practice.** Every M1 extension combo is
typed `m2:DomainConceptCombo`, so the shape fired on `M1_CoreConcepts` only.
Verified empirically on `M1_Geology`: 17 violations reported, **zero** from
SHAPE 9, against formulas that plainly violate rule 1.

Fixed by a dual `sh:targetClass` (v1.4.0). Result: SC-1 violations **8 → 114**.
The 8 were all in CoreConcepts; the 14 extensions produced zero.

**The SC-6 perimeter is now measured for the first time**: 114 violation messages
= 109 rule-1 (monoidal operator inside a signature) + 5 arity, over **155 combo
formulas** carrying a monoidal operator. Worst: Chemistry 15, Economics 14,
Mythology 11, Photography 11, CoreConcepts 10, Education 10.
**`M1_Physics` and `M1_Electronics` are already conformant** — use them as
reference forms when repairing the others.

### 1.3 ~4300 keys never reach RDF (the VOC family)

A **bare key** (declared in no `@context`) is not a badly-named property: it is
JSON that never crosses into RDF. In files without `@vocab` it is **dropped on
expansion**; in files with `@vocab` it maps onto a foreign namespace (two M3 files
were minting bogus `owl:role`, `owl:status`).

Census: **4281 occurrences / 1301 distinct** over 26 canonical files
(M2 1781, M1 1572, M3 756, M0 172). Of these, **693 have a standard equivalent**
and **303 are false friends** (see §4 of the VOC note).

Concretely: `M3_EagleEye`'s root node carries eight bare keys — `metadata`,
`parent_ontology`, `grammar_properties`, `coupling_with_MapGrammar`, `metaphor`,
`dual_axes_position`, `independence_matrix`, `complementary_grammar`. The entire
semantic payload of the Eagle Eye ontology is invisible to any reasoner.

This is δ₁ applied to the files themselves: the gap between what the file
*displays* and what the graph *contains*.

---

## 2. WHAT WAS ACTUALLY CHANGED

### 2.1 `m3:changelog` defined (apex) and adopted

The `changelog` property was **used corpus-wide but declared NOWHERE**, in three
competing spellings. The five M3 files used `m2:changelog` — an M3 file referencing
an M2 property (**layer inversion**), compounded by the `m2` prefix being
**undeclared** in those `@context`s (CTX-1), so the key resolved to an opaque `m2:`
URI scheme.

Now defined once in `M3_GrammarFoundation` (2.5.0) as `owl:AnnotationProperty`
— legal downward from every layer, since M2/M1/M0 all import M3. Aligned **in
intent** with `adms:versionNotes`; **no `rdfs:subPropertyOf` asserted**, pending a
decision on whether the corpus accepts external vocabulary beyond
rdfs/owl/skos/dcterms.

Gauge: `STR layer inversion` **5 → 0** (first gauge in the corpus to reach target).
Changelog forms: `m2:` 22→17, `m1:` 3, `m3:` 0→5, bare `metadata.changelog` 4.

### 2.2 B1 — 19 property declarations

`M3_BicephalousPerspective` used **24 `m3:*` keys with 0 declared**. Nineteen are
now declared as `owl:AnnotationProperty` (declaration only — no usage, no data
changed): `role`, `semantics`, `symbol`, `grammar`, `visual`, `usage`,
`derivation`, `formula_role`, `independence`, `analogyInGt`, `analogyInGs`,
`pairWith`, `triadicPattern`, `theoretical_basis`, `transcendentalQuestion`,
`openQuestion`, `rejected_names`, `notation_note`, `notation_disambiguation`.

- **HELD** (decide separately): `definition`, `examples` (Family-A candidates →
  `skos:definition`/`skos:example`), `epistemicGap` (δ₁ measurement, SC-6 sensitivity).
- **EXCLUDED**: `typeSymbol`, `typeIndex` — already defined in `M3_GenesisGrammar`.
  Redefining them would have created an STR-1 duplicate; the scope check caught it.
- **FLAGGED, not fixed**: `pairWith` carries a string
  (`"m3:bicephalous:NegativePole"`) where an `@id` is expected — latent reference
  defect, candidate `owl:ObjectProperty`. **Michel's call.**

### 2.3 The honest negative result

**Zero bare keys were fixed. Eighteen were added** (`VOC 4263 → 4281`): the 6 new
changelog entries each carry 3 undeclared bare keys (`version`, `date`, `changes`).
The gauge revealed this; no manual review would have. The VOC debt is untouched
and the worksite has not started.

### 2.4 SC-2 STEPS 1 & 2 EXECUTED (end of session)

The notation reform finally started. Both steps are **at the source** — they change
the convention and the symbols, not yet the 43 M2 formulas.

**Step 2 — `M3_EagleEye.jsonld` 2.9.0 -> 2.10.0** (done first, on request):
- `m3:typeSymbol` `S` -> `St`, `I` -> `It`; matching `rdfs:label` updates;
  alphabet listings `{A,S,F,I,D}` -> `{A,St,F,It,D}` (3 sites).
- Class `@id` values (`m3:eagle_eye:typeS`/`typeI`) **unchanged** — only the symbol
  moves, so no cross-file reference breaks.
- Example formula `A x S x It x F = Homeostasis` (already half-migrated) completed.
- **Defect found while checking residues**: this file described Sphinx Eye's alphabet
  as `{R,E,V,O,I}` — the fifth REVOI primitive is **`Im`** (Interoperability), never a
  bare `I`. Corrected to `{R,E,V,O,Im}`; it contradicted GrammarFoundation and SphinxEye.
- Historical changelog entries left untouched (history, not defect).

**Step 1 — `M3_BicephalousPerspective.jsonld` 1.4.0 -> 1.5.0**:
- `m3:notation_disambiguation` no longer states the retired hybrid-only rule.
- **New rule graved**: `S` and `I` are ALWAYS monoid-subscripted in EVERY atom formula
  (`St`/`Ss`, `It`/`Im`); `A`/`F`/`D` stay bare. Scope: **atoms only** — combo
  signatures take named concepts, not primitives.
- Rationale recorded: the old rule gave one primitive **two spellings depending on its
  neighbours** — ambiguous to read, and impossible to check mechanically. That is
  precisely what makes step 3 (SHACL `FormulaShape`) possible at all.
- `m2:Balance` usage example `A x S x F | _0` -> `A x St x F | _0`.

**Ordering note**: step 2 shipped before step 1, which left the two M3 files
contradicting each other for one turn. Step 1 closed it. **Commit all four files as
one lot** — a repo state with only step 2 applied is inconsistent.

**READMEs updated in step**: `M3_EagleEye_README` 2.10.0,
`M3_BicephalousPerspective_README` 1.5.0 (stale-rule warning removed, retired rule
kept visible in a "Retired rule" callout with its reason).

**No golden impact**: neither M2 formulas nor M1 data were touched. Gauge `NOT-1`
stays at **43** — it moves only at step 4.


---

## 3. NEW INSTRUMENT — `tscg_metrics.py` v1.0.0

`ontology/cli-tools/tscg_metrics.py` + `tscg_metrics_README.md`.

Read-only metric board over the four layers. **Why it exists**: three manual
censuses of the same defect produced **three different numbers** (1661, 6444, 4263)
because each applied a different notion of "canonical file". Hand-counting is not
reproducible, so no worksite could prove progress. The selection rule is now frozen
(26 canonical files). **Every count produced by hand before 2026-07-23 is superseded.**

```
python ontology/cli-tools/tscg_metrics.py --root ontology --shacl
python ontology/cli-tools/tscg_metrics.py --root ontology --save baseline.json
python ontology/cli-tools/tscg_metrics.py --root ontology --baseline baseline.json
```

No dependency for the core gauges; `rdflib`+`pyshacl` only for `--shacl`.

### Baseline after this session (HEAD, 2026-07-23)

| Family | Gauge | Value | Target | Owning worksite |
|---|---|---:|---:|---|
| VOC | bare keys (occurrences) | 4281 | 0 | VOC |
| VOC | bare keys (distinct) | 1301 | 0 | VOC |
| VOC | standard-replaceable | 693 | — | VOC family A |
| VOC | false friends | 303 | — | (native, keep) |
| VOC | prefixed but undefined | 853 | 0 | VOC family B1 |
| CTX | undeclared prefix | 1 | 0 | CTX |
| CTX | relative `mN` prefix | 21 | 0 | CTX-4 |
| CTX | term name with `:` | 31 | 0 | CTX-5 |
| FRB | tensor operator (live) | 89 | 0 | SC-9 |
| FRB | legacy arrow | 5 | 0 | SC-9 |
| DUP | retired D8 triad | 8 | 0 | SC-6 slice (Geology) |
| NOT | bare S/I in atom formula | 43 | 0 | **SC-2** |
| STR | layer inversion | **0** | 0 | ✅ DONE |
| SC-1 | combo signature violations | 114 | 0 | **SC-6** |

**`run_all_layers` counts each violation twice** (golden 468 = 2 × 234 measured;
680 = 2 × 340). Not a defect introduced here — the doubling pre-existed and is
self-consistent, so deltas remain valid. Worth confirming and documenting.
Its prose message also has stale hard-coded numbers ("476 violations", "163
errors") that no longer match its own golden.

---

## 4. BACKLOG (surfaced, NOT done)

- **README ⇄ jsonld drift — introduced by this session, 5 files.** The M3 READMEs
  were not updated with their `.jsonld`:

  | README | states | jsonld is |
  |---|---|---|
  | `M3_GrammarFoundation_README.md` | 2.4.1 | **2.5.0** |
  | `M3_GenesisGrammar_README.md` | 4.3.0 | **4.5.0** |
  | `M3_EagleEye_README.md` | 2.8.0 | **2.9.0** |
  | `M3_SphinxEye_README.md` | 3.5.0 | **3.6.0** |
  | `M3_BicephalousPerspective_README.md` | 1.3.1 | **1.4.0** |

  Note `M3_GenesisGrammar_README` was already 2 versions behind before this session.
  Rule (from 2026-07-18): `README.version == jsonld.owl:versionInfo`.
- **M1_Geology**: 8 residual `m1:structuralGrammarFormulaRawText`. Content verified:
  `S (x) I (x) A (x) D` — the ASCII transliteration of the retired `⊗`. The canonical
  formula survives alongside, so **deletion is safe** (guard-before-delete satisfied).
  `TeX` and `Expanded` have **zero occurrences corpus-wide** — dead fields.
  **No morphism depends on the D8 family** (verified); `m3:Morphism` lives in M3 and
  does not use it.
- **21 CTX-4** + **31 CTX-5** + **1 CTX-1** remaining.
- **Changelog migration lot 2**: 17 `m2:changelog` + 3 `m1:changelog` files left.
  Unblocked now the apex property exists. Also 4 files with a bare
  `metadata.changelog` — and `metadata` is itself undeclared everywhere (VOC).
- **`M3_GrammarFoundation` still declares `@vocab = owl#`**, projecting its bare
  terms into the OWL namespace.
- **Source typo (still there)**: `M3_GrammarFoundation.jsonld` changelog 2.3.0 reads
  `DomainConceptCombo → DomainConceptCombo` (should be `KnowledgeFieldConceptCombo → …`).
- **`_00_TSCG_Worksite_Map.md` §1.1 is stale**: it still writes
  `Fm2 : GenericConcept⁺ → ConceptCombo`. Per SC-1, `m2:ConceptCombo` does not exist;
  the class is `m2:GenericConceptCombo`, and `Fm2` takes **≥ 2** arguments.

---

## 5. OPEN DECISIONS (Michel's, blocking their worksites)

1. **VOC data-vs-documentation** — for each `eagleView`/`sphinxView` sub-field:
   data (reify: `m2:EagleView` class with `m2:hasFormula`, `m2:hasBasis`…, visible
   and SHACL-checkable) or documentation (single declared container
   `m3:documentation`, where invisibility becomes *intended and verifiable*)?
   Intuition to confirm: **mixed** — `formula` is data (it is the object of SC-2),
   `pros`/`cons`/`mechanism` is documentation. The frontier runs *inside* the block.
2. **VOC family A** — approve the 15-entry standard-replacement table (693 occ).
3. **`m3:changelog` alignment** — assert `rdfs:subPropertyOf adms:versionNotes`,
   or keep zero external dependency?
4. **`pairWith`** — promote to `owl:ObjectProperty` with a real `@id`?
5. **M3 citing M2 examples** — `M3_GenesisGrammar` cites `m2:Stase` /
   `m2:AbsorbingState` as *string values* under `m2Reference` (documentary, not
   triples). Legitimate pedagogy or layer leak?
6. **`definition`/`examples`/`epistemicGap`** — B1 declaration or Family-A standard?

---

## 6. WHEN TO GENERATE THE M2/M3 SHACL GRAMMARS

Asked this session. Answer, measured:

- **M3 prerequisite is MET**: all 5 M3 files now carry an absolute `m3` prefix,
  0 unresolved predicates. The 2026-07-18 trap ("do not generate before CTX is
  fixed") no longer applies to M3.
- **M2 is NOT**: `M2_GenericConcepts` is still relative on both `m2` and `m3`.
- **But a deeper blocker applies to both**: a SHACL grammar validates **the graph**.
  With 1781 bare keys in M2 and 756 in M3, the shapes would validate a largely
  **empty** graph and pass — not because the corpus is correct, but because there is
  nothing to check. That is the worst outcome: an instrument showing green on an
  unmeasured layer.

⇒ **VOC is not parallel to the grammar work; it is its prerequisite.**
Proposed order: VOC decisions → CTX-4 on `M2_GenericConcepts` → M3 grammar →
M2 grammar. Defensible alternative: generate a **restricted** M3 grammar now,
covering only what is already in the graph (classes, `MonoidalType`, the 19 newly
declared properties), as an immediate safety net on the foundational layer.

---

## 7. METHOD — what the discipline caught

The commit sequence was run step by step against HEAD, and **stopped twice**:

1. **Step 0 caught a moved HEAD**: measurements were taken on `5dcd8e9`, the local
   repo was at `cce7678`, and the tree was dirty. `git diff --stat 5dcd8e9 HEAD --
   ontology/` proved only `golden_values.json` and one README had changed — no
   `.jsonld`, no `.ttl` — so the baseline held. **Without that check the lots would
   have been applied against an unverified corpus.**
2. **The gate caught an unexplained delta**: predicted +106, `run_all_layers`
   reported +212. Committing on "close enough" would have been wrong; the factor 2
   turned out to be run_all_layers' own double-counting (§3). **The rule held: an
   unexplained movement blocks the commit until it is explained.**

Two of my own detector bugs were also found by cross-checking, and both are
recorded in the metrics README: DUP-1 read 0 because the pattern ignored the `m1:`
prefix (8 real occurrences); and a SHACL shape was reported as "not firing" because
property shapes are blank nodes, so the shape *name* never appears in the report.
**Rule adopted: a gauge reading 0 is a claim, and claims get tested.**

Lot 3 could not be verified by `run_all_layers` at all (**M2 and M3 remain
NOT_INSTRUMENTED**). It was validated by three independent means: git hash
(5/5 exact), metric board delta (4/4 predicted), and IRI resolution (52 → 0).
That improvised triple-check is the strongest concrete argument for building the
validator.

---

## 8. NEXT ACTIONS (recommended order)

1. **Fix the 5 M3 README versions** (§4) — small, and it is drift *this* session
   introduced. Do it before it compounds.
2. **SC-2 steps 3-5** — steps 1 and 2 are DONE (§2.4). Remaining:
   - **step 3**: SHACL `FormulaShape` forbidding bare `S`/`I` in **atom** formulas
     (`m2:hasStructuralGrammarFormula`), NOT in `Fm2`/`Fm1m2` signatures. This is what
     turns the 43 into an enforced counter rather than a manual audit.
   - **step 4**: migrate the **43** M2 atom formulas. Gauge `NOT-1` must reach **0**.
     Fully mechanical (measured: 0 sit in a Map `+` segment, 0 already use `Ss`/`Im`).
     `Balance = A × S × F | _0` -> `A × St × F | _0`.
   - **step 5**: `M2_GenericConcepts_README` — the "Notation Convention" section still
     states the OLD hybrid-only rule; plus Key Takeaways and Statistics.
   **Verified: SC-2 edits formula VALUES (literals), not keys — so the residual CTX-4
   in `M2_GenericConcepts` does NOT compromise it.**
3. **M1_Geology `RawText`** (8) — safe, small, DUP-1 → 0.
4. **VOC decisions** (§5) — they unblock both the grammar work and family A.
5. **SC-6** — 114/155, now measured. Heavy and semantic: each formula needs the
   right **named** M2 concept recovered, not a mechanical substitution.
6. **Build `M0_TscgOntologyValidator`** in a fresh session, from
   `TSCG_OntologyValidator_Worksite_README.md`, starting with CTX + the `--source`
   switch. `tscg_metrics.py` is its metric front-end and a working prototype of the
   hash check.

**Maturity note (endorsed)**: ontology engineering here still lacks the safety nets
of software engineering. This session added one — a reproducible metric board — and
proved why: every number that mattered had been wrong at least once.
