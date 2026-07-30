# Migration note — `knowledgeField` → `domain`

*Echopraxium with the collaboration of Claude AI.*

Status: **in progress, not complete.** Both names are live in the corpus at the time of
writing. Any consumer of the ontology (parsers, validators, the Canopée data adapter) must
handle both until the migration is sealed.

---

## 1. Scope

Measured on a working snapshot (not `git HEAD` — the repository remains the only authority,
so re-measure before acting):

- `knowledgeField` — **66 occurrences across 14 files**, spanning M0, M1 and M1 extensions
  (M0_TrophicPyramid, M1_Biology, M1_BusinessModeling, M1_Chemistry, M1_Economics,
  M1_Electronics, M1_EnergyGenerators, M1_Geology, …).
- `m1:domain` — 112 occurrences (the target name, already in use).
- `m0:domain` — 7 occurrences.

So the corpus currently carries **both** the old and the new name, in different files. Until
the rename is finished, a consumer that recognises only one of them will silently drop
relations.

---

## 2. Hazard: `domain` is an overloaded local name

This is the part most likely to cause a silent, hard-to-diagnose bug.

`rdfs:domain` appears **101 times** and means something entirely different: it is the OWL/RDFS
declaration of *which class a property applies to*. It is schema plumbing, not a knowledge
domain.

| Property | Occurrences | Meaning |
|---|---|---|
| `m1:domain` | 112 | knowledge domain of a concept — **a real relation** |
| `rdfs:domain` | 101 | class a property is declared on — **schema, not a relation** |
| `m0:domain` | 7 | knowledge domain at M0 |

**Rule for any consumer: key properties on the full prefixed IRI, never on the local name.**
A parser that splits on `:` and matches `domain` will conflate the two and fabricate ~101
spurious edges between concepts and property definitions.

The same caution applies to any other local name shared across vocabularies (`range`,
`member`, `type`, `label`).

---

## 3. Cardinality, and why it matters here

`knowledgeField`/`domain` is **single-valued** (max 1 observed), which classifies it as a
*containment* relation rather than a *contract* under the criterion below:

> A relation that may carry several values cannot define a single parent, so it is a
> **contract** the node satisfies, not a **container** it sits in.

Contrast with `relatedDomains` (up to 4 values) and `appliesToDomains`, which are contracts: an
M0 instance may honour several domains, so they must **not** create parent/child links in any
hierarchy or folding tree.

If the migration changes the cardinality of `domain` (e.g. allowing several domains per
concept), it changes its classification too — it would become a contract, and every consumer
that treats it as containment must be revisited. **Preserving single-valuedness is therefore
part of the migration contract, not an incidental detail.**

---

## 4. Checklist to seal the migration

- [ ] Re-measure occurrences against `git HEAD`, not a snapshot.
- [ ] Rename `knowledgeField` → `domain` across the 14 files, with version bumps and
      changelog entries (rolling 3, except M3 files which keep up to 7).
- [ ] Confirm the prefix is consistent (`m1:domain` vs `m0:domain` — decide whether both
      remain or converge).
- [ ] Confirm cardinality stays 1; add or update a SHACL shape asserting `sh:maxCount 1`.
- [ ] Add a SHACL shape forbidding `knowledgeField` once the rename is done, so it cannot
      creep back.
- [ ] Update `run_all_layers` golden values (the relation rename will move counts).
- [ ] Update the Canopée data adapter's containment map (`HIERARCHY_PARENT`) to use the
      final name.

---

## 5. Consumer guidance in the interim

Until the migration is sealed, treat the two names as synonyms **and key on full IRIs**:

```
containment (single-valued) : m1:domain, m0:domain, <legacy> knowledgeField,
                              hasFamily, ontologyType, parentCombo, skos:broader
contract   (multi-valued)   : relatedDomains, appliesToDomains, comboOf, mobilizes,
                              imports, validatesGenericConcepts, skos:member
schema, not a relation      : rdfs:domain, rdfs:range
```
