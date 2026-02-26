# TSCG Documentation Index
## Complete Guide to ValueSpace Attributes and Framework Extensions

**Version**: 14.4.0  
**Date**: 2026-02-05  
**Author**: Echopraxium with the collaboration of Claude AI

---

## 📚 Documentation Overview

This documentation set covers the systematic enrichment of TSCG M2 GenericConcepts with ValueSpace attributes (Phases 1-4), architectural extensions (N-ary GenericConceptCombo), and practical user guides.

**Total deliverables**: 7 documents + 1 ontology file

---

## 🎯 Quick Navigation

### For New Users
1. Start with **Quick Reference** (cheat sheet)
2. Read **User Guide** for practical examples
3. Consult **Attribute Reference** when needed

### For System Analysts
1. **Poclet Analysis Methodology** (how to discover GenericConcepts)
2. **User Guide** (how to instantiate with attributes)
3. **Architectural Extensions** (advanced patterns)

### For Framework Developers
1. **Final Report** (complete summary)
2. **Architectural Extensions** (N-ary combos, ValueSpace pattern)
3. **Attribute Candidates Analysis** (selection methodology)

---

## 📄 Document Descriptions

### 1. M2_GenericConcepts.jsonld ⭐ CORE ONTOLOGY

**File**: `M2_GenericConcepts.jsonld` (v14.4.0)  
**Type**: JSON-LD ontology  
**Size**: 5530 lines  
**Content**:
- 71 M2 GenericConcepts (stable)
- 11 GenericConcepts enriched with attributes
- 13 attributes (ValueSpace)
- 72 discrete values with full documentation

**Use for**:
- Authoritative reference for all attribute definitions
- Valid value lookup (`possibleValues`)
- Formula details, examples, characteristics
- OWL/RDF reasoning and semantic web applications

**Key sections**:
- Lines 1-100: Context and metadata
- Search for `"m2:hasAttribute"` to find enriched GenericConcepts
- Each attribute has complete ValueSpace definition

---

### 2. TSCG_ValueSpace_Quick_Reference.md ⭐ START HERE

**Type**: Cheat sheet (2 pages)  
**Audience**: Everyone  
**Purpose**: Fast lookup of attribute values

**Content**:
- All 13 attributes in table format
- Decision trees for common choices
- Usage examples (RAAS, PID, Network)
- Common mistakes to avoid
- Validation checklist

**Use when**:
- Need quick reminder of valid values
- Choosing attribute value for system
- Validating instantiation

**Highlights**:
- One-page reference per attribute
- Decision trees (e.g., "Does system overshoot? → convergence_pattern")
- Complete value lists with examples

---

### 3. TSCG_ValueSpace_User_Guide.md ⭐ PRACTICAL GUIDE

**Type**: User manual (35 pages)  
**Audience**: Poclet creators, system modelers  
**Purpose**: How to use attributes in practice

**Content**:
1. **Quick Start** (3-step workflow)
2. **Understanding ValueSpace** (what attributes are)
3. **Attribute Reference** (detailed guide for each)
4. **Instantiation Patterns** (5 common patterns)
5. **Complete Examples** (RAAS, Thermostat, Social Network, Pendulum)
6. **Templates** (ready-to-use JSON snippets)
7. **Common Pitfalls** (mistakes and solutions)
8. **FAQs** (20+ questions answered)

**Use when**:
- Creating new poclet (M0)
- Annotating existing system
- Need JSON syntax examples
- Troubleshooting validation errors

**Highlights**:
- 4 complete worked examples
- 3 ready-to-use templates (Biology, Control, Network)
- Decision guides for each attribute
- Rationale best practices

---

### 4. ValueSpace_Enrichment_Final_Report.md 📊 COMPLETE SUMMARY

**Type**: Technical report (40 pages)  
**Audience**: Framework developers, researchers  
**Purpose**: Comprehensive summary of Phases 1-4

**Content**:
1. **Executive Summary** (mission, results, impact)
2. **Complete Attribute Catalog** (all 11 GenericConcepts)
3. **Phase-by-Phase Breakdown** (4 phases detailed)
4. **RAAS Complete Annotation** (full example)
5. **Statistics** (before/after comparison)
6. **Architectural Validation** (proliferation avoided)
7. **Insights & Lessons Learned**
8. **Recommendations** (future work)

**Use when**:
- Understanding overall project scope
- Presenting TSCG to stakeholders
- Planning future extensions
- Academic/research context

**Highlights**:
- Statistics: 71 GenericConcepts (stable) + 13 attributes + 72 values
- Architecture validation (no ontology explosion)
- Complete RAAS JSON annotation
- Phase-by-phase progression

---

### 5. Poclet_Analysis_Methodology.md 🔍 DISCOVERY PROCESS

**Type**: Methodological guide (30 pages)  
**Audience**: System analysts, researchers  
**Purpose**: How to analyze systems to discover GenericConcepts

**Content**:
1. **Core Principle** (poclet = active discovery)
2. **Architectural Flow** (M0 → M1 → M2)
3. **Decision Tree** (M2 vs M1_Core vs M1_Domain)
4. **M2 Validation Criteria** (transdisciplinary, tensor formula, etc.)
5. **Analysis Phases** (5-phase process)
6. **RAAS Case Study** (complete analysis)
7. **Best Practices & Anti-patterns**

**Use when**:
- Starting new system analysis
- Deciding if pattern is M2 or M1
- Need validation criteria for GenericConcept
- Creating poclet from scratch

**Highlights**:
- Decision tree for M2 vs M1 classification
- 5-phase analysis process (ASFID → gaps → formalization)
- Complete RAAS walkthrough
- ✅/❌ best practices list

---

### 6. TSCG_Architectural_Extensions.md 🏗️ ADVANCED PATTERNS

**Type**: Architecture specification (25 pages)  
**Audience**: Framework architects, advanced users  
**Purpose**: N-ary GenericConceptCombo & attribute architecture

**Content**:
1. **Extension 1: N-ary GenericConceptCombo** (n ≥ 2 parents)
   - Theoretical foundation (tensor associativity)
   - Coupling algorithm
   - Cascade example (3 parents)
2. **Extension 2: Typed Attributes via ValueSpace**
   - Mechanism (leverage existing m2:ValueSpace)
   - Attribute schema
   - Trajectory.shape example
3. **Implementation Status** (v14.3.6-14.4.0)
4. **Case Study: Cascade Evolution** (3 iterations)
5. **Future Directions**

**Use when**:
- Designing new GenericConceptCombo
- Understanding N-ary composition
- Creating new attribute for GenericConcept
- Architecture discussions

**Highlights**:
- Cascade = ⊗⇒(Process, Step, Trajectory) → S⊗I⊗A⊗D⊗F
- Mathematical validation (tensor associativity)
- Complete attribute schema
- Future extension patterns

---

### 7. M2_Attribute_Candidates_Analysis.md 🎯 SELECTION PROCESS

**Type**: Analysis document (20 pages)  
**Audience**: Framework developers  
**Purpose**: How attributes were selected (methodology)

**Content**:
1. **Selection Criteria** (5 criteria for candidates)
2. **Priority 1: High-Value Candidates** (immediate implementation)
   - Amplification, Regulation, Process, Bifurcation, Convergence, Symmetry
3. **Priority 2-3: Medium/Lower Priority** (future phases)
4. **Implementation Roadmap** (Phases 1-4)
5. **Validation Criteria** (checklist)

**Use when**:
- Proposing new attribute
- Understanding why attribute was chosen
- Planning Phase 5+ extensions
- Evaluating candidate attributes

**Highlights**:
- 5 selection criteria (natural variations, avoids proliferation, etc.)
- 4-phase roadmap (completed)
- Validation checklist for each attribute
- Priority ranking

---

## 🗂️ Document Relationships

```
Quick Reference ────┬──► User Guide ────┬──► Final Report
                    │                   │
                    │                   └──► Architectural Extensions
                    │
                    └──► Poclet Methodology
                         │
                         └──► Attribute Candidates Analysis
                              │
                              └──► M2_GenericConcepts.jsonld (authoritative source)
```

---

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| **M2 GenericConcepts** | 71 (stable) |
| **Enriched GenericConcepts** | 11 |
| **Total Attributes** | 13 |
| **Discrete Values** | 72 |
| **JSON-LD Lines** | 5530 |
| **Documentation Pages** | ~200 (total) |
| **Versions** | v14.3.5 → v14.4.0 |
| **Phases** | 4 (complete) |

---

## 🎓 Learning Paths

### Path 1: Quick User (30 minutes)
1. Quick Reference (10 min)
2. User Guide Quick Start (10 min)
3. Pick a template and modify (10 min)

### Path 2: System Analyst (2 hours)
1. Quick Reference (10 min)
2. Poclet Methodology (45 min)
3. User Guide complete (45 min)
4. Try RAAS example (20 min)

### Path 3: Framework Developer (4+ hours)
1. Final Report (60 min)
2. Architectural Extensions (60 min)
3. Attribute Candidates Analysis (45 min)
4. M2_GenericConcepts.jsonld study (60 min+)

---

## 🔑 Key Concepts

### ValueSpace
GenericConcept (M2) defining space of possible values with epistemic quality measures. Used as mechanism for typed attributes.

**Formula**: It ⊗ V ⊗ O ⊗ R ⊗ Im

### Attribute
Configurable property of GenericConcept with predefined discrete values from ValueSpace.

**Example**: `Trajectory.shape ∈ {Linear, Circular, Spiral, ...}`

### GenericConcept Enrichment
Adding attributes to existing M2 GenericConcepts without creating subtype proliferation.

**Result**: 71 stable GenericConcepts + 72 configurations

### N-ary GenericConceptCombo
Generalization from binary (M_A ⊗⇒ M_B) to N-ary composition (⊗⇒(M₁, ..., Mₙ)).

**Example**: Cascade = ⊗⇒(Process, Step, Trajectory)

---

## 📞 Support & Contribution

### Questions?
- Check FAQ in User Guide
- Consult Quick Reference for valid values
- Review M2_GenericConcepts.jsonld for details

### Found an Issue?
- Document in poclet with `"note"` field
- Propose new value with justification
- File issue with TSCG project

### Want to Contribute?
- Create poclets using attributes
- Propose new attributes (use selection criteria)
- Share domain-specific insights
- Improve documentation

---

## 🎯 Success Criteria

### For Using Attributes
- ✅ Valid values from `possibleValues`
- ✅ Rationale provided for choices
- ✅ Only relevant attributes used
- ✅ JSON-LD valid and parseable
- ✅ Transdisciplinary validation possible

### For Proposing New Attributes
- ✅ Natural variations identified (≥3 values)
- ✅ Avoids subtype proliferation
- ✅ Transdisciplinary examples (≥3 domains)
- ✅ Semantic significance demonstrated
- ✅ Fits ValueSpace pattern

---

## 📅 Version History

| Version | Date | Changes |
|---------|------|---------|
| v14.3.6 | 2026-02-05 | Phase 1a: Trajectory.shape |
| v14.3.7 | 2026-02-05 | Phase 1b: Amplification, Regulation, Process (3 attrs) |
| v14.3.8 | 2026-02-05 | Phase 2: Regulation.2, Convergence, Process.2 (3 attrs) |
| v14.3.9 | 2026-02-05 | Phase 3: Bifurcation, Symmetry, Threshold (3 attrs) |
| v14.4.0 | 2026-02-05 | Phase 4: Network, Signal, Gradient (3 attrs) ✅ COMPLETE |

---

## 🚀 Next Steps

### Immediate (v14.4.x)
- Create M0_RAAS.jsonld (complete poclet with all attributes)
- Populate M1_Biology.jsonld (HormonalCascade, EndocrineAxis, etc.)
- User testing and feedback

### Near-term (v14.5.0)
- Implement N-ary GenericConceptCombo
- Cascade = ⊗⇒(Process, Step, Trajectory)
- Additional poclets for validation

### Long-term (v15.0+)
- Phase 5+ attributes (if needed)
- M1 domain extensions with attributes
- Tool support (validators, generators)

---

## 📖 Citation

If using TSCG ValueSpace attributes in research or projects:

```
Echopraxium with the collaboration of Claude AI (2026).
TSCG ValueSpace Attributes: Systematic Enrichment of
Transdisciplinary GenericConcepts (Version 14.4.0).
GitHub: https://github.com/Echopraxium/tscg
```

---

## 📧 Contact

For questions, suggestions, or contributions, please contact:
- **Project**: TSCG (Transdisciplinary System Construction Game)
- **GitHub**: https://github.com/Echopraxium/tscg
- **Version**: 14.4.0
- **Date**: 2026-02-05

---

**End of Documentation Index**

*Last updated: 2026-02-05*
