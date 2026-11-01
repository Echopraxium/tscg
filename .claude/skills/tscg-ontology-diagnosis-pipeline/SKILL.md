---
name: tscg-ontology-diagnosis-pipeline
description: >
  Orchestrates Human, LLM, and Formal Tools for safe ontology engineering through
  a 6-phase validation pipeline. Solves the Ouroboros paradox (LLMs need oversight
  but lack ontological intuition) with explicit role boundaries: Human for semantic
  architecture, LLM for technical execution, Formal Tools for logical validation.
  Covers initialization, pre-diagnosis, change execution, technical validation
  (linter/reasoner/SHACL), semantic validation, and documentation. Use this skill
  EVERY TIME you modify TSCG ontologies to ensure systematic validation and prevent
  semantic drift. Includes decision trees, validation checklists, and concrete
  scenarios (property renaming, architectural changes, notation cleanup, migrations,
  bare-key reduction) and the debt-honesty rule: never lower a counter by moving the
  debt where no tool counts (D1 down => G8 not up).
---

# TSCG Ontology Diagnosis & Validation Pipeline

**Purpose:** Orchestrate Human, LLM, and Formal Tools for safe ontology engineering  
**Problem:** Ouroboros paradox - LLMs need oversight but lack ontological intuition  
**Solution:** Explicit multi-agent workflow with clear role boundaries

---

## Three Agents

### 👤 **Human (Michel)**
**Expertise:** Semantic architecture, domain knowledge, conceptual modeling  
**Responsibilities:**
- Define architectural decisions (It vs Im, ASFID/REVOI structure)
- Validate semantic coherence ("does this make sense in TSCG?")
- Approve/reject structural changes
- Resolve ambiguous cases
- Make final go/no-go decisions

**Should NOT:** Execute repetitive technical tasks, manual renaming, boilerplate

---

### 🤖 **LLM (Claude)**
**Expertise:** Pattern application, systematic transformations, technical execution  
**Responsibilities:**
- Execute documented patterns
- Systematic transformations (renaming, migration)
- Generate boilerplate code
- Detect syntactic inconsistencies
- Apply formal rules mechanically

**Should NOT:** Invent semantic structures, make architectural decisions, improvise patterns

---

### 🛠️ **Formal Tools**
**Expertise:** Mathematical guarantees, formal logic validation  
**Responsibilities:**
- Syntactic validation (JSON-LD, RDF parsing)
- Logical consistency (OWL reasoning)
- Constraint enforcement (SHACL)
- Regression testing (SPARQL queries)

**Should NOT:** Interpret semantics, understand domain context

**Available Tools** (all under `ontology/toolchain/`; prerequisites:
`python -m pip install -r ontology/toolchain/requirements.txt`):
- `run_all_layers.py` — **the acceptance gate**: exact frozen counts on M3, M2, M1, M0
  (`golden_values.json`), plus, for M1 and M0, a separate `engine` section (document plane
  + cross-file checks, lot K0). The final word on every change.
- `validator/tscg_validator.py` — the validation engine: `--doc` (document plane
  D1–D7: bare keys, `@vocab`, changelog, strict JSON-LD expansion…), `--ext`
  (cross-file G1b/G5/G6 and **G8 phantom predicates**: a TSCG predicate used but declared
  as a property nowhere), `--shacl` (the SHACL grammars registered per layer)
- `check-M1/check_M1.py`, `check-M0/check_m0_instances.py` — M1 / M0 checkers
- `ontology-linter/ontology_linter.py` — TSCG conventions + syntax
- `owl_reasoning_test/rdfs_diagnostic.py` — RDFS/OWL modeling errors
- `owl_reasoning_test/fix_owl_literals.py` — automated OWL literal fixes
- `owl_reasoning_test/owl_reasoning_test.py` — reasoner (logical consistency; owlready2's
  bundled Jena needs Java 25)
- `tscg_metrics.py` — gauges (VOC, CTX, FRB, DUP, EXT…)
- `tscg_layercake_health_map.py` — the LayerCake Health Map (where the debt is)

---

## The debt-honesty rule (Michel, 2026-11-01)

**Never lower a counter by moving the debt to a place no tool counts.** A repair is a
repair only if the debt disappears; if it merely changes form, the matching counter must
rise, and the gate must see it. When a lot reveals hidden debt, the counts go UP — that is
progress, not regression (freeze it with a written reason).

The reference case, vocabulary debt (OWL 2: an entity's type comes from its declaration):
- a **bare key** (D1, declared in no `@context`) is dropped on JSON-LD expansion;
- a key mapped in `@context` but declared as a property nowhere is a **phantom
  predicate** (G8);
- a bare key is repaired ONLY by **deleting** it (redundant / derivable), **mapping** it to
  an existing property (`rdfs:comment`, `dcterms:…`, an existing TSCG property), or
  **declaring** it for real (property type + `rdfs:label`, in the file that owns it);
- **D1 down ⇒ G8 must not go up.** A `@context` entry alone is not a repair.

The same reflex applies to any check: before celebrating a drop, ask "did the defect
disappear, or did it move out of the instrument's sight?" If a defect class is not
measured, measure it first (instrumentation lot), then reduce it.

The rule lives on HEAD in `docs/reboot-kit/TSCG_ReferenceCorpus_Bootstrap.md` (hard
invariants) — read it there; this section is the operational reminder.

---

## Workflow Pipeline

### Phase 0: Initialization
**Trigger:** New ontology work or modification needed

**Steps:**
1. 👤 **Human:** Define the change request
   - What needs to change? (architecture, notation, properties)
   - Why? (rationale)
   - Scope? (M0/M1/M2/M3, single file or multiple)

2. 🤖 **LLM:** Acknowledge and clarify
   - Confirm understanding
   - Ask clarifying questions if ambiguous
   - Propose approach outline

3. 👤 **Human:** Approve approach or refine

**Exit criteria:** Clear, documented change request

---

### Phase 1: Pre-Diagnosis
**Goal:** Establish baseline state before changes

**Steps:**
1. 🛠️ **Gate:** the baseline is the frozen reference
   ```bash
   cd ontology/toolchain && python run_all_layers.py      # must end with GATE: PASS
   ```
   **Output:** the exact counts per layer before the change. A change that must
   lower a count is announced HERE (which counter, by how much, why).

2. 🛠️ **Engine + linter** on the layer(s) concerned
   ```bash
   python ontology/toolchain/validator/tscg_validator.py --layers M2 --doc --ext --shacl --report pre.json
   python ontology/toolchain/ontology-linter/ontology_linter.py ontology/ --layer M2 --format markdown --output pre_diagnosis.md
   ```

3. 🛠️ **Reasoner:** logical consistency
   ```bash
   python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M2_GenericConcepts.jsonld
   ```

4. 🤖 **LLM:** Summarize baseline
   - Parse tool outputs
   - Highlight critical issues
   - Present to human

5. 👤 **Human:** Review baseline
   - Note known issues to preserve or fix
   - Identify regression risks

**Exit criteria:** Documented baseline + human approval

---

### Phase 2: Change Execution
**Goal:** Implement the change with LLM

**Steps:**
1. 🤖 **LLM:** Execute change
   - Apply documented patterns from skills
   - Make systematic modifications
   - Document each step

2. 🤖 **LLM:** Self-check
   - Review changes against requirements
   - Check for obvious errors
   - Apply the debt-honesty rule: no repair that only moves a defect out of sight
   - Prepare summary

3. 👤 **Human:** Quick review (optional)
   - Spot-check critical changes
   - Flag anything unexpected

**Exit criteria:** Change implemented, ready for validation

---

### Phase 3: Technical Validation
**Goal:** Formal tools verify correctness

**Sequential execution with failure gates:**

**3.1 🛠️ Ontology Linter** - Syntax & TSCG conventions
```bash
python ontology/toolchain/ontology-linter/ontology_linter.py <modified_files> --strict
```
**Pass:** No new errors  
**Fail:** → Fix issues → Retry

**Exit gate:** Must pass before 3.2

---

**3.2 🛠️ RDFS Diagnostic** ⭐ NEW - OWL modeling errors
```bash
python ontology/toolchain/owl_reasoning_test/rdfs_diagnostic.py
```
**Checks:**
- Literal values vs URI references (rdfs:subClassOf, domain, range)
- Invalid property declarations (@owl:functionalProperty)
- Undefined class references

**Pass:** 0 errors  
**Fail:** → Apply automated fixes:
```bash
# Preview fixes
python ontology/toolchain/owl_reasoning_test/fix_owl_literals.py --dry-run

# Apply if preview OK
python ontology/toolchain/owl_reasoning_test/fix_owl_literals.py

# Re-validate
python ontology/toolchain/owl_reasoning_test/rdfs_diagnostic.py
```

**Exit gate:** Must pass with 0 errors before 3.3

---

**3.3 🛠️ OWL Reasoning** - Logical consistency
```bash
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file <modified_file>
```
**Checks:**
- Logical consistency
- Inconsistent classes
- OWL axiom validation

**Pass:** No inconsistencies found  
**Fail:** → Review Pellet output → Fix logical issues → Retry

**Note:** "Reparenting" warnings are normal (Pellet optimizing hierarchy). An
`UnsupportedClassVersionError … class file version 69.0` is an environment fault (Java
older than 25), not an ontology result: report "not run", never "passed".

**Exit gate:** Must pass before 3.4

---

**3.4 🛠️ SHACL + document plane** - the grammars registered for the layer
```bash
python ontology/toolchain/validator/tscg_validator.py --layers <M3|M2|M1|M0> --doc --ext --shacl
```
(M1/M0 are also covered by `check_M1.py --shacl` and `check_m0_instances.py`.)
**Pass:** no NEW finding compared with Phase 1 (the frozen backlog may remain)  
**Fail:** → Fix → Retry

---

**3.5 🛠️ Acceptance gate** - exact frozen counts, the final check
```bash
cd ontology/toolchain && python run_all_layers.py
```
**Pass:** `GATE: PASS`  
**Up** = a new defect → fix it — OR a lot that deliberately reveals hidden debt (a new
check): show the move, freeze it with `--update-golden`, write why. **Down** = a
deliberate repair → check it against the debt-honesty rule (did the defect disappear, or
did another counter have to rise — e.g. D1 down with G8 up?), show the move to the human,
then `python run_all_layers.py --update-golden` and write the reason in the commit — OR a
check that stopped biting → investigate. Never loosen a check to pass.
If a tool or grammar changed: its negative tests (`ontology/toolchain/validator/tests/`).

---

**3.6 🤖 LLM:** Aggregate results & report
- Parse all tool outputs
- Identify error patterns
- Suggest fixes if failures
- Generate Phase 3 summary

**Exit criteria:** All formal tools pass (3.1 → 3.2 → 3.3 → 3.4 → 3.5)

---

### Phase 4: Semantic Validation
**Goal:** Human validates semantic correctness

**Steps:**
1. 🤖 **LLM:** Prepare semantic report
   - Summarize what changed
   - Explain rationale for each change
   - Highlight semantic implications
   - Flag any assumptions made

2. 👤 **Human:** Review semantics
   - Does this align with TSCG architecture?
   - Are there unintended semantic consequences?
   - Do the names/labels make sense?
   - Is the formalism appropriate?

3. 👤 **Human:** Decision
   - ✅ **APPROVE** → Phase 5
   - ⚠️ **REVISE** → Back to Phase 2 with feedback
   - ❌ **REJECT** → Revert, restart from Phase 0

**Exit criteria:** Human approves semantic correctness

---

### Phase 5: Documentation & Finalization
**Goal:** Document and integrate changes

**Steps:**
1. 🤖 **LLM:** Generate documentation
   - Update version numbers
   - Write changelog entries
   - Update READMEs if needed
   - Document architectural decisions

2. 👤 **Human:** Review documentation
   - Accuracy check
   - Completeness check
   - Approve or request edits

3. 🤖 **LLM:** Present final files
   - Show all modified files
   - Provide commit message suggestion

4. 👤 **Human:** Commit decision
   - Ready to commit?
   - Need further changes?

**Exit criteria:** Changes committed to repository

---

## Common Scenarios

### Scenario 1: Property Renaming
**Example:** `hasTensorFormula` → `hasStructuralGrammarFormula`

| Phase | Agent | Action |
|-------|-------|--------|
| 0 | 👤 | "Rename all tensor properties to structural grammar" |
| 1 | 🛠️ | Baseline linter report |
| 2 | 🤖 | Execute systematic renaming |
| 3 | 🛠️ | Linter + Reasoner validation (G8 must not rise: a rename that breaks a declaration/use pair shows up as +G8) |
| 4 | 👤 | Semantic approval |
| 5 | 🤖 | Update docs, present files |

**Time:** ~15 minutes  
**Risk:** Low (mechanical transformation)

---

### Scenario 2: Architectural Change
**Example:** Add new M3 dimension to ASFID

| Phase | Agent | Action |
|-------|-------|--------|
| 0 | 👤 | "Add dimension X to ASFID with semantics Y" |
| 1 | 🛠️ | Baseline state (reasoner critical) |
| 2 | 🤖 | Add dimension, update dependent structures |
| 3 | 🛠️ | **CRITICAL** - Reasoner must pass |
| 4 | 👤 | **CRITICAL** - Deep semantic review |
| 5 | 🤖 | Extensive documentation |

**Time:** ~1-2 hours  
**Risk:** High (architectural impact)

---

### Scenario 3: Notation Cleanup
**Example:** Fix ambiguous `I` in formulas

| Phase | Agent | Action |
|-------|-------|--------|
| 0 | 👤 | "Replace bare I with It/Im based on context" |
| 1 | 🛠️ | Linter detects all I occurrences |
| 2 | 🤖 | **ASK HUMAN** for each ambiguous case |
| 4 | 👤 | Provide It/Im decisions |
| 2 | 🤖 | Execute replacements |
| 3 | 🛠️ | Linter validates |
| 4 | 👤 | Spot-check critical formulas |
| 5 | 🤖 | Document pattern |

**Time:** ~30 minutes  
**Risk:** Medium (semantic distinction critical)

---

### Scenario 4: Migration Pipeline
**Example:** M3 structural grammar migration

| Phase | Agent | Action |
|-------|-------|--------|
| 0 | 👤 | "Migrate all M3/M2 to structural grammar" |
| 1 | 🛠️ | Baseline ALL layers |
| 2 | 🤖 | **M3 first** (foundation) |
| 3 | 🛠️ | Validate M3 |
| 4 | 👤 | Approve M3 |
| 2 | 🤖 | **M2 next** (depends on M3) |
| 3 | 🛠️ | Validate M2 |
| 4 | 👤 | Approve M2 |
| ... | ... | Continue M1, M0 |

**Time:** ~2-4 hours (incremental)  
**Risk:** High (cascading changes)  
**Strategy:** Layer-by-layer with validation

---

### Scenario 5: Bare-key reduction (vocabulary debt)
**Example:** the bare keys of `m2:eagleView` (lot K1)

| Phase | Agent | Action |
|-------|-------|--------|
| 0 | 👤 | "Reduce the bare keys of X" |
| 1 | 🛠️ | Baseline D1 and G8 for the layer(s) |
| 2 | 🤖 | Decision table per key: delete / map / declare — **ASK HUMAN** for each key's meaning |
| 4 | 👤 | Decide each key |
| 2 | 🤖 | Apply; every declared key gets a property type + `rdfs:label` in the owning file |
| 3 | 🛠️ | Gate: D1 down, **G8 not up** |
| 5 | 🤖 | Freeze with reason, document |

**Risk:** Medium (semantic: the meaning of each key is Michel's call)

---

## Decision Trees

### When LLM Should Ask Human

```
┌─────────────────────────────────┐
│ Does pattern exist in skills?   │
└────────┬────────────────────────┘
         │
    ┌────▼────┐
    │ YES  NO │
    │  ↓   ↓  │
    │  ✓   ? │
    └─────────┘
         │ NO
         ├→ Is it purely mechanical?
         │    ├→ YES: Ask for pattern first
         │    └→ NO: Ask for guidance
         │
         └→ Does it affect semantics?
              ├→ YES: **ASK HUMAN**
              └→ NO: Proceed but flag

**Rule:** When in doubt, ASK. Never improvise semantics.
```

### When to Use Which Tool

```
Issue Type          → Tool
──────────────────────────────────
Syntax error        → Linter
Structural problem  → Linter
Logic inconsistency → Reasoner
Constraint violation→ SHACL
Undeclared term     → validator --ext (G5 standard, G8 TSCG)
Bare key            → validator --doc (D1)
Regression          → SPARQL tests
Semantic ambiguity  → Human
```

---

## Validation Checklist

### Pre-Commit Checklist
- [ ] 🛠️ Linter passes (no new errors)
- [ ] 🛠️ Reasoner passes (consistent)
- [ ] 🛠️ SHACL validates (if applicable)
- [ ] 🛠️ Tests pass (no regressions)
- [ ] 🛠️ Every counter that dropped was checked against the debt-honesty rule (D1 down ⇒ G8 not up)
- [ ] 🤖 Documentation updated
- [ ] 👤 Human semantic approval
- [ ] 👤 Commit message reviewed

### Post-Commit Checklist
- [ ] CI/CD passes
- [ ] Documentation deployed
- [ ] Changes logged in project journal

---

## Tool Configuration

### Linter Configuration
```bash
# Standard validation
python ontology_linter.py ontology/ --layer M2

# Strict (pre-commit)
python ontology_linter.py ontology/ --strict

# Report generation
python ontology_linter.py ontology/ --format markdown --output report.md
```

### Reasoner Configuration
```bash
python ontology/toolchain/owl_reasoning_test/owl_reasoning_test.py --file ontology/M2_GenericConcepts.jsonld
```

### SHACL Configuration
Grammars are data, registered per layer in
`ontology/toolchain/validator/checks/shacl_runner.py` (`GRAMMARS`); new grammars live
in `ontology/toolchain/grammars/` (see `tscg-generate-mn-grammars`).
```bash
python ontology/toolchain/validator/tscg_validator.py --layers M2 --shacl
python ontology/toolchain/validator/tscg_validator.py --shapes grammars/<file>.ttl --layers M3
```

---

## Integration with Existing Skills

This skill **orchestrates** other skills:

- `tscg-instance-pipeline` → Uses this for M0 validation
- `tscg-generate-mn-grammars` → Uses Phase 3 (Technical Validation)
- `tscg-tensor-to-structural-grammar-migration` → Follows this entire pipeline

**Relationship:** This is the **meta-skill** that defines HOW to use other skills safely.

---

## Exit Criteria Summary

| Phase | Human | LLM | Tools | Can Proceed If... |
|-------|-------|-----|-------|-------------------|
| 0 | ✅ | ✅ | - | Change request clear |
| 1 | ✅ | ✅ | ✅ | Baseline documented |
| 2 | - | ✅ | - | Change implemented |
| 3 | - | ✅ | ✅ | All tools pass |
| 4 | ✅ | ✅ | - | Human approves semantics |
| 5 | ✅ | ✅ | - | Docs complete, ready to commit |

**Golden Rule:** Every phase must pass before proceeding to the next.

---

## Anti-Patterns to Avoid

❌ **LLM improvising architecture**
- LLM creates new metaconcept without human approval
- **FIX:** Always Phase 4 for architectural changes

❌ **Human doing mechanical tasks**
- Human manually renaming 249 properties
- **FIX:** Let LLM do Phase 2 (execution)

❌ **Skipping formal validation**
- Commit without running reasoner
- **FIX:** Phase 3 is mandatory

❌ **Tools interpreting semantics**
- Linter flags "tensor" as error vs warning
- **FIX:** Tools report, humans decide

❌ **Circular reasoning**
- LLM validates its own work without tools
- **FIX:** Phase 3 uses independent tools

❌ **Masking debt by relocation**
- Adding `"role": "m2:role"` to a `@context` so that D1 drops, while `m2:role` is declared nowhere
- Any change that makes a counter fall by moving the defect where no instrument looks
- **FIX:** the debt-honesty rule — delete / map / declare; measure the hidden form first (G8 exists for this)

---

## Success Metrics

### Process Metrics
- **Time to validation:** How long Phase 1-5?
- **Tool pass rate:** % of changes passing Phase 3 first try
- **Human approval rate:** % of changes approved in Phase 4 first review
- **Regression rate:** Post-commit issues found

### Quality Metrics
- **Ontology consistency:** Reasoner always passes
- **Convention compliance:** Linter warnings decreasing
- **Vocabulary debt:** D1 and G8 decreasing together, never one at the other's expense
- **Test coverage:** % of ontology covered by SPARQL tests

---

## Future Enhancements

### Short Term
- [ ] Automate Phase 1 (baseline reporting)
- [x] Create SHACL shapes for M2/M3 (structural grammar, WS-5, 2026-10-05)
- [x] Phantom-predicate check G8 + M1/M0 engine plane in the gate (lot K0, 2026-11-01)
- [ ] Build SPARQL test suite

### Medium Term
- [ ] CI/CD integration (GitHub Actions)
- [ ] Automated rollback on Phase 3 failures
- [ ] Performance metrics dashboard

### Long Term
- [ ] Machine learning for semantic validation (Phase 4 assist)
- [ ] Automated pattern extraction from approved changes
- [ ] Predictive risk assessment

---

## Usage Examples

### Example 1: Using this skill for property rename

**Human triggers:**
```
Michel: "I want to rename hasStructuralGrammarFormulaASCII to 
hasStructuralGrammarFormulaRawText across all M2"
```

**Claude follows pipeline:**
```
[Phase 0] ✅ Confirmed: systematic rename in M2 layer
[Phase 1] 🛠️ Running baseline...
          → 26 occurrences detected
[Phase 2] 🤖 Executing rename...
          → 84 replacements made
[Phase 3] 🛠️ Validating...
          → Linter: PASS
          → Reasoner: PASS
[Phase 4] 👤 Awaiting your semantic approval...
```

### Example 2: Human catches improvisation

**Claude attempts:**
```
[Phase 2] 🤖 Creating new m2:hasFormulaVariant property...
```

**Human rejects:**
```
Michel: ❌ Stop. This property wasn't in the requirements.
        Don't invent new properties.
```

**Claude course-corrects:**
```
[Phase 4] 🤖 You're right. Reverting improvisation.
          Using existing m2:hasStructuralGrammarFormulaRawText instead.
```

---

## Conclusion

This skill **breaks the Ouroboros** by:
1. ✅ Explicit role boundaries (Human ≠ LLM ≠ Tools)
2. ✅ Formal validation gates (Phase 3)
3. ✅ Human semantic authority (Phase 4)
4. ✅ Systematic workflow (Phases 0-5)
5. ✅ Debt honesty: a counter falls only when the defect disappears

**Use this skill EVERY TIME you modify TSCG ontologies.**

---

**Status:** Active skill  
**Version:** 1.2.0

**Last Updated:** 2026-11-01 (lot K0: debt-honesty rule, G8 phantom predicates, M1/M0
engine section of the gate, Scenario 5 bare-key reduction, Java 25 note for the reasoner)

**Maintainer:** Michel (Echopraxium)