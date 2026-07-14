# FeedbackLoop Reclassification (M2 → M1_CoreConcepts)

**Version**: 1.0.0
**Date**: 2026-07-07
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Change type**: Ontological correction — anti-overfitting migration
**Status**: PROPOSITION (pending validation before graving)

---

## 1. Summary

`m2:FeedbackLoop` is **misclassified as an atomic M2 GenericConcept**. Its own
fiche already declares it as a product of three existing M2 concepts, which is a
textbook decomposability signal. This document specifies its migration to
`M1_CoreConcepts` as a combo, the corrected (non-circular) decomposition, and two
notation residues to purge in the same operation.

This correction is an instance of the **Ontological Overfitting** remedy: a
concept admitted before the Triple Filter was formalized, never re-audited against
Test 1 (Decomposability) and Test 3 (Atomicity).

---

## 2. Diagnosis

### 2.1 Current (erroneous) M2 fiche

```
m2:FeedbackLoop
  m2:hasStructuralGrammarFormula : "m2:Process × m2:Alignment × m2:Homeostasis"
  m2:structuralExpansion         : "(D × F) × (I × A × S) × (A × S × F) = A × S × F × I × D"
```

### 2.2 Triple Filter results

| Test | Question | Result |
|------|----------|--------|
| **Test 1 — Decomposability** | Expressible as `Fm2(C1, C2, …)` of existing M2 concepts? | **FAIL** — the fiche itself writes it as `Process × Alignment × Homeostasis` |
| **Test 2 — Transdisciplinarity** | Validated in ≥6 unrelated domains? | Pass (thermostat, insulin regulation, PID, ecology, economics…) — but irrelevant once Test 1 fails |
| **Test 3 — Atomicity** | Adds an M3 dimension absent from all components? | **FAIL** — see below |

**Test 3 detail.** The expansion covers all five ASFID dimensions
(`A × S × F × I × D`). The union of the components already covers all five:

```
Process     : D × F
Alignment   : I × A × S
Homeostasis : A × St × F
─────────────────────────
Union       : A, S, F, I, D   (complete)
```

FeedbackLoop introduces **no dimension** absent from its components →
non-atomic → not an M2 concept.

**Verdict:** two independent hard-test failures. Migration M2 → M1_CoreConcepts
is warranted.

---

## 3. The circularity issue (why the 3-factor formula is wrong)

The stored decomposition uses **three** factors, but the third one is both
circular and redundant.

- **Circular.** `m2:Homeostasis` (`A × St × F`, *"self-regulation maintaining a
  stable internal state"*) **is itself a feedback loop** — specifically the
  negative-polarity, fixed-setpoint case. Defining FeedbackLoop *by means of*
  Homeostasis inverts the natural subsumption:

  ```
  Homeostasis  ⊂  FeedbackLoop        (correct: Homeostasis is a specialization)
  FeedbackLoop = f(Homeostasis)       (wrong: circular — presupposes what it defines)
  ```

- **Redundant.** The "compare to a target and reduce the discrepancy" semantics
  is already carried by `m2:Alignment` (`I × A × S`: error detection toward an
  attractor). Adding Homeostasis merely re-injects `A × S × F`, already supplied
  by `Process + Alignment`. It contributes no new dimension.

A decomposition must be expressed through **generative mechanism**, not through
**effect**. Homeostasis is the *effect* (a maintained stable state); the
*mechanism* is a discrepancy-driven cyclic process.

---

## 4. Corrected decomposition

```
m1:FeedbackLoop  (M1_CoreConcepts)
  m1:comboOf                            : [ m2:Process, m2:Alignment ]
  m1:structuralGrammarFormula           : "Fm2(Process, Alignment)"
  m1:structuralGrammarFormulaExpanded   : "(D × F) × (I × A × S) = A × S × F × I × D"
```

**Reading.** A temporal cycle (`Process`) driven by discrepancy reduction
(`Alignment`) — the essence of feedback, mechanism rather than effect. Dual
polarity (negative = stabilizing, positive = amplifying) is preserved as an
attribute on the combo, exactly as it was on the former M2 fiche.

**Emergent property.** Cyclic self-reference: the output of the process becomes
an input to its own error signal. Absent from `Process` (linear unfolding, no
comparison) and from `Alignment` (single discrepancy reduction, no temporal
recurrence) taken individually.

---

## 5. Downstream: the Homeostasis domino (flagged, not resolved)

Once FeedbackLoop is an M1 combo `Fm2(Process, Alignment)`, `m2:Homeostasis`
must be **re-audited on its own**. "Self-regulation maintaining a stable state"
presupposes a regulatory loop, which suggests Homeostasis may itself be an M1
specialization of the same combo (negative polarity + fixed attractor) rather
than an atomic M2 concept.

Arguments **for** retained atomicity: `hasPolarity = neutral`, a distinct
REVOI/Sphinx signature (`O + R + V`), and a clean attractor-maintenance role.

**Decision deferred.** This README does not rule on Homeostasis. It only records
that the FeedbackLoop migration makes the Homeostasis audit the logical next
step. Resolving Homeostasis before graving FeedbackLoop is optional; the two are
architecturally independent.

---

## 6. Notation residues to purge in the same edit

Independent of the reclassification, the current FeedbackLoop fiche violates two
active conventions:

1. **⊗ residue.** `m2:expressionTeX` contains `\otimes` (U+2297). Forbidden since
   the 2026-07-06 operator rule. Structural formulas use `×`, `+`, `|` only.

2. **Scalar-coefficient residue.** `m2:expression` and `m2:poleMapping` carry a
   scalar coefficient (`k ·`, `−k ·`, `+k ·`). This is leftover scalar-algebra
   semantics, incompatible with the monoidal structural product. Polarity must be
   expressed as a qualitative attribute (`feedback_polarity`), not as a signed
   scalar weight.

---

## 7. Migration checklist

```
□  Remove m2:FeedbackLoop entry from M2_GenericConcepts.jsonld
□  Add m1:FeedbackLoop to M1_CoreConcepts.jsonld as Fm2(Process, Alignment)
     - m1:comboOf, m1:parentGenericConcepts (Process, Alignment)
     - m1:structuralGrammarFormulaExpanded = A × S × F × I × D
     - carry over: dual polarity, examples, negative/positive aspects
     - m1:migrationNote referencing this README
□  Purge \otimes and scalar k· residues (do not re-introduce in the M1 entry)
□  Update references to m2:FeedbackLoop across M0 instances → m1:FeedbackLoop
□  Update m2:changelog (M2_GenericConcepts) — keep 3 most recent entries
□  Update m2:changelog (M1_CoreConcepts) — keep 3 most recent entries
□  Re-run SHACL validation (pyshacl) on M1_CoreConcepts and affected M0 files
□  (Optional, separate change request) Audit m2:Homeostasis atomicity
```

---

## 8. Rationale note (anti-metric-gaming)

This migration lowers the M2 count by one, but the count is **not** the reason
for the change. The justification is the two hard-test failures (Section 2). The
migration is legitimate only because a genuine `Fm2(Process, Alignment)`
decomposition exists. Reclassifying a concept merely to reduce a number — hiding
a true atomic under a combo label — would be the mirror pathology (ontological
underfitting) and is explicitly out of scope here.

---

## 9. References

- `OntologicalOverfitting.md` — Triple Filter (Decomposability / Transdisciplinarity / Atomicity), M1 Safety Valve.
- `M1_CoreConcepts.jsonld` — `m1:ConstraintBalance` triad; overfitting = OverConstrained (`_$`) pole.
- `M2_GenericConcepts.jsonld` — current `m2:FeedbackLoop`, `m2:Process`, `m2:Alignment`, `m2:Homeostasis` fiches.
- Base URI (all ontology IRIs): `https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/` (via `@base`).
