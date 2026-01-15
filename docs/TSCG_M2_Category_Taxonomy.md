# TSCG M2 - Taxonomie des Catégories de Métaconcepts

## 🎯 Objectif
Classifier les métaconcepts M2 selon leur nature fonctionnelle pour faciliter :
- Navigation dans l'ontologie
- Patterns de composition
- Mapping vers domaines applicatifs

---

## 📊 Taxonomie proposée

### 1. **Structural** (Structurels)
Concepts concernant l'organisation spatiale, la topologie, l'architecture.
- Hierarchy
- Network
- Modularity
- Symmetry
- Boundary
- Interface
- Component
- Scale
- Redundancy

**Signature typique** : S élevé (0.6-0.9), D faible (0.0-0.3)
**Tenseur dominant** : S⊗S, S⊗I

---

### 2. **Dynamic** (Dynamiques)
Concepts concernant le changement temporel, les transformations, les processus.
- Bifurcation
- Transformation
- Trajectory
- Event
- Behavior
- Catalysis
- Gradient
- Interaction

**Signature typique** : D élevé (0.5-0.9), I variable
**Tenseur dominant** : D⊗I, F⊗D, S⊗D

---

### 3. **Regulatory** (Régulatoires)
Concepts concernant le contrÎle, la stabilisation, la gouvernance.
- Homeostasis
- Regulation
- Feedback
- Constraint
- Threshold
- Filter
- Gain
- Rule
- Protocol

**Signature typique** : A élevé (0.5-0.8), tenseurs ordre 2+
**Tenseur dominant** : A⊗I, A⊗S⊗F, I⊗F

---

### 4. **Adaptive** (Adaptatifs)
Concepts concernant l'apprentissage, la modification, la résilience.
- Adaptation
- Resilience
- Memory
- Tropism
- Emergence

**Signature typique** : I élevé (0.5-0.8), F moyen-élevé (0.4-0.7)
**Tenseur dominant** : F⊗I⊗D, D⊗I⊗S, A⊗I⊗S

---

### 5. **Energetic** (Énergétiques)
Concepts concernant les flux, les échanges, la dissipation.
- Dissipation
- Resource
- Gradient
- Transduction

**Signature typique** : F élevé (0.6-0.9), D élevé (0.5-0.8)
**Tenseur dominant** : F⊗D, A⊗F⊗D, S⊗F⊗D

---

### 6. **Informational** (Informationnels)
Concepts concernant les données, les signaux, les représentations.
- Signal
- Language
- Representation
- Identity
- Coherence
- Relation

**Signature typique** : I élevé (0.7-0.9), S variable
**Tenseur dominant** : I⊗I, S⊗I, I⊗F

---

### 7. **Ontological** (Ontologiques)
Concepts concernant l'existence, l'identité, les fondements.
- System
- Environment
- Substrate
- State
- Boundary

**Signature typique** : Variable (concepts primitifs)
**Tenseur dominant** : Variable

---

### 8. **Teleonomic** (Téléonomiques)
Concepts concernant les buts, la direction, la finalité (sans anthropomorphisme).
- Autopoiesis
- Stability
- Robustness
- Synergy

**Signature typique** : A élevé (0.6-0.9)
**Tenseur dominant** : A⊗S, A⊗S⊗D, A⊗S⊗F

---

### 9. **Relational** (Relationnels)
Concepts concernant les rÎles, les interactions, les médiations.
- Agent
- Role
- Mediator
- Observer
- Interaction

**Signature typique** : I moyen-élevé (0.4-0.7), F moyen (0.3-0.6)
**Tenseur dominant** : S⊗I, F⊗I, I⊗D

---

## 🔄 Métaconcepts multi-catégories

Certains métaconcepts appartiennent à plusieurs catégories :

- **Homeostasis** : Regulatory + Energetic + Teleonomic
- **Emergence** : Adaptive + Dynamic + Informational
- **Network** : Structural + Relational
- **Bifurcation** : Dynamic + Regulatory
- **Memory** : Adaptive + Informational

---

## 📋 Mapping complet (53 → catégories)

### Structural (9)
1. Hierarchy
2. Network
3. Modularity
4. Symmetry
5. Boundary
6. Interface
7. Component
8. Scale
9. Redundancy

### Dynamic (8)
10. Bifurcation
11. Transformation
12. Trajectory
13. Event
14. Behavior
15. Catalysis
16. Gradient
17. Interaction

### Regulatory (9)
18. Homeostasis
19. Regulation
20. Feedback
21. Constraint
22. Threshold
23. Filter
24. Gain
25. Rule
26. Protocol

### Adaptive (5)
27. Adaptation
28. Resilience
29. Memory
30. Tropism
31. Emergence

### Energetic (4)
32. Dissipation
33. Resource
34. Gradient (aussi Dynamic)
35. Transduction

### Informational (6)
36. Signal
37. Language
38. Representation
39. Identity
40. Coherence
41. Relation

### Ontological (5)
42. System
43. Environment
44. Substrate
45. State
46. Capacity

### Teleonomic (4)
47. Autopoiesis
48. Stability
49. Robustness
50. Synergy

### Relational (5)
51. Agent
52. Role
53. Mediator
54. Observer
55. Facet

---

## 🎨 Encodage JSON-LD

```json
"m2:metaConceptCategory": {
  "@type": "rdf:Bag",
  "categories": ["Regulatory", "Energetic", "Teleonomic"]
}
```

Ou plus simple :

```json
"m2:metaConceptCategory": "Regulatory",
"m2:secondaryCategories": ["Energetic", "Teleonomic"]
```

---

## 🔍 Utilisation

### Requête SPARQL exemple
```sparql
SELECT ?concept WHERE {
  ?concept m2:metaConceptCategory "Regulatory" .
}
```

### Navigation hiérarchique
```
M2 Metaconcepts
├── Structural
│   ├── Hierarchy
│   ├── Network
│   └── ...
├── Dynamic
│   ├── Bifurcation
│   └── ...
└── ...
```

---

## ✅ Validation

Chaque métaconcept doit avoir :
- **1 catégorie primaire** (obligatoire)
- **0-2 catégories secondaires** (optionnel)

Total : 9 catégories couvrant les ~50 métaconcepts finaux.
