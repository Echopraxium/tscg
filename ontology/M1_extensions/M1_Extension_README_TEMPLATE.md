# M1_<Domain>.jsonld — README

**Author**: Echopraxium with the collaboration of Claude AI
**Version**: <version>
**Date**: <date>
**Layer**: M1 — Domain Extension
**Status**: Active

---

## 🎯 Role

**M1_<Domain>** is the M1-level extension for the **<Domain>** knowledge field.
It defines domain-specific `KnowledgeFieldConceptCombo` instances reusable across
`<Domain>` poclets and systemic frameworks.

---

## 📐 Namespace

```
m1:extension:<domain>:  →  M1_extensions/<domain>/M1_<Domain>.jsonld#
```

All concepts use the `Fm1m2(<Domain>, ...)` formula notation:

```json
"@type": ["owl:Class", "m2:KnowledgeFieldConceptCombo"],
"rdfs:subClassOf": "m2:KnowledgeFieldConceptCombo",
"m2:knowledgeField": {"@id": "m1:extension:<domain>:<Domain>"},
"m1:structuralGrammarFormula": "Fm1m2(<Domain>, <ASFID-formula> | <REVOI-formula>)"
```

---

## 🧩 Concepts (<N> KnowledgeFieldConceptCombos)

| Concept | Formula | Description |
|---|---|---|
| `m1:extension:<domain>:ConceptA` | `Fm1m2(<Domain>, A × S × F)` | ... |
| `m1:extension:<domain>:ConceptB` | `Fm1m2(<Domain>, D × It | V + O)` | ... |

---

## 🏗️ Architecture

```
m2:KnowledgeFieldConceptCombo   ← M2 (parent class)
  ↓ rdfs:subClassOf
  m1:extension:<domain>:ConceptA   ← this file
  m1:extension:<domain>:ConceptB
```

**Imports:**
- `M1_CoreConcepts.jsonld` — M1 umbrella (m1: prefix)
- `M2_GenericConcepts.jsonld` — GenericConcepts (m2: prefix)

---

## 📚 Key Takeaways

1. All concepts typed as `m2:KnowledgeFieldConceptCombo`
2. All formulas use `Fm1m2(<Domain>, ...)` notation
3. No `m2:characterizedBy`, no `asfidSignature` (deprecated)

---

## 🔗 Related

- `M1_CoreConcepts.jsonld` — M1 base layer
- `M1_Domains.jsonld` — domain registry (`m1:domain:<Domain>`)
- `M0_<Instance>.jsonld` — concrete poclet instances
