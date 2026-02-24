# Liste complète des 86 métaconcepts (à utiliser pour génération)
METACONCEPTS = {
    # Structural Family (12)
    "Hierarchy": {"formula": "S ⊗ A", "family": "Structural", "polarity": "neutral"},
    "Network": {"formula": "S ⊗ I ⊗ F", "family": "Structural", "polarity": "neutral"},
    "Symmetry": {"formula": "S", "family": "Structural", "polarity": "neutral"},
    "Modularity": {"formula": "S ⊗ I", "family": "Structural", "polarity": "neutral"},
    "Topology": {"formula": "S ⊗ I", "family": "Structural", "polarity": "neutral"},
    "Segmentation": {"formula": "S ⊗ I ⊗ D", "family": "Structural", "polarity": "neutral"},
    "Node": {"formula": "S ⊗ I", "family": "Structural", "polarity": "neutral"},
    "Hub": {"formula": "S ⊗ F", "family": "Structural", "polarity": "neutral"},
    "Space": {"formula": "S ⊗ I", "family": "Ontological", "polarity": "neutral"},
    "Composition": {"formula": "S ⊗ I ⊗ A", "family": "Structural", "polarity": "dual"},
    "Polarity": {"formula": "S ⊗ I ⊗ A", "family": "Structural", "polarity": "nary"},
    "Invariant": {"formula": "S ⊗ A", "family": "Structural", "polarity": "neutral"},
    
    # Dynamic Family (12)
    "Bifurcation": {"formula": "∂D/∂F", "family": "Dynamic", "polarity": "neutral"},
    "Transformation": {"formula": "D ⊗ S ⊗ I", "family": "Dynamic", "polarity": "neutral"},
    "Process": {"formula": "D ⊗ F", "family": "Dynamic", "polarity": "neutral"},
    "Trajectory": {"formula": "A ⊗ D ⊗ F", "family": "Dynamic", "polarity": "neutral"},
    "Event": {"formula": "D ⊗ I", "family": "Dynamic", "polarity": "neutral"},
    "Cascade": {"formula": "S ⊗ I ⊗ A ⊗ D ⊗ F", "family": "Dynamic", "polarity": "dual"},
    "Behavior": {"formula": "S ⊗ D ⊗ F", "family": "Dynamic", "polarity": "dual"},
    "Tropism": {"formula": "A ⊗ S ⊗ D ⊗ F", "family": "Dynamic", "polarity": "dual"},
    "Workflow": {"formula": "S ⊗ D ⊗ F", "family": "Structural", "polarity": "dual"},
    "Step": {"formula": "S ⊗ I ⊗ D", "family": "Structural", "polarity": "dual"},
    "Action": {"formula": "D ⊗ I", "family": "Dynamic", "polarity": "dual"},
    "Convergence": {"formula": "-∇·D / ∇·D", "family": "Dynamic", "polarity": "dual"},
    
    # Regulatory Family (10)
    "Homeostasis": {"formula": "A ⊗ S ⊗ F", "family": "Regulatory", "polarity": "neutral"},
    "Regulation": {"formula": "A ⊗ S ⊗ F", "family": "Regulatory", "polarity": "neutral"},
    "Constraint": {"formula": "S ⊗ I", "family": "Regulatory", "polarity": "neutral"},
    "Scope": {"formula": "S → I → A → R", "family": "Regulatory", "polarity": "neutral"},
    "Threshold": {"formula": "A ⊗ I", "family": "Regulatory", "polarity": "neutral"},
    "Trigger": {"formula": "D ⊗ I", "family": "Regulatory", "polarity": "neutral"},
    "Balance": {"formula": "A ⊗ S ⊗ F", "family": "Regulatory", "polarity": "neutral"},
    "Trade-off": {"formula": "A ⊗ I ⊗ F", "family": "Regulatory", "polarity": "neutral"},
    "FeedbackLoop": {"formula": "A ⊗ S ⊗ F ⊗ I ⊗ D", "family": "Dynamic", "polarity": "dual"},
    "Alignment": {"formula": "I ⊗ A ⊗ S", "family": "Dynamic", "polarity": "neutral"},
    
    # Adaptive Family (5)
    "Resilience": {"formula": "A ⊗ S", "family": "Adaptive", "polarity": "neutral"},
    "Adaptation": {"formula": "I ⊗ F ⊗ D", "family": "Adaptive", "polarity": "neutral"},
    "Emergence": {"formula": "I ⊗ S ⊗ D", "family": "Adaptive", "polarity": "neutral"},
    "Memory": {"formula": "∫(D−F)dτ", "family": "Adaptive", "polarity": "neutral"},
    "Self-Organization": {"formula": "A ⊗ I ⊗ D", "family": "Teleonomic", "polarity": "neutral"},
    
    # Energetic Family (2)
    "Dissipation": {"formula": "F ⊗ D", "family": "Energetic", "polarity": "neutral"},
    "Storage": {"formula": "S ⊗ F", "family": "Energetic", "polarity": "neutral"},
    
    # Informational Family (10)
    "Code": {"formula": "I ⊗ S", "family": "Informational", "polarity": "neutral"},
    "Coding": {"formula": "I ⊗ S ⊗ D", "family": "Informational", "polarity": "dual"},
    "Representation": {"formula": "I ⊗ S", "family": "Informational", "polarity": "neutral"},
    "Language": {"formula": "I ⊗ S ⊗ F", "family": "Informational", "polarity": "neutral"},
    "Pattern": {"formula": "S → I → A", "family": "Informational", "polarity": "dual"},
    "Signal": {"formula": "I ⊗ F", "family": "Informational", "polarity": "neutral"},
    "Signature": {"formula": "I ⊗ S", "family": "Informational", "polarity": "neutral"},
    "ValueSpace": {"formula": "It → V → O → R → Im", "family": "Informational", "polarity": "hybrid"},
    "Synergy": {"formula": "I ⊗ D", "family": "Dynamic", "polarity": "dual"},
    "Activation": {"formula": "A ⊗ D", "family": "Regulatory", "polarity": "dual"},
    
    # Ontological Family (15)
    "System": {"formula": "S ⊗ F", "family": "Ontological", "polarity": "neutral"},
    "Environment": {"formula": "F ⊗ I", "family": "Ontological", "polarity": "neutral"},
    "Observer": {"formula": "I ⊗ A", "family": "Ontological", "polarity": "neutral"},
    "State": {"formula": "I", "family": "Ontological", "polarity": "neutral"},
    "Substrate": {"formula": "S ⊗ F", "family": "Ontological", "polarity": "neutral"},
    "Gradient": {"formula": "⊗ ₂F or ⊗ ₂I", "family": "Ontological", "polarity": "neutral"},
    "Imbrication": {"formula": "S → S", "family": "Ontological", "polarity": "dual"},
    "Domain": {"formula": "∑ᵢ σᵢ |uᵢ⟩ ⊗ |vᵢ⟩", "family": "Ontological", "polarity": "hybrid"},
    "Identity": {"formula": "S → I → A → V → E", "family": "Structural", "polarity": "dual"},
    "Processor": {"formula": "S ⊗ I ⊗ D ⊗ F ⊗ V ⊗ R", "family": "Ontological", "polarity": "dual"},
    "Amplification": {"formula": "Ft → D → It → R → O", "family": "Dynamic", "polarity": "hybrid"},
    "KnowledgeField": {"formula": "∑ᵢ σᵢ |uᵢ⟩ ⊗ |vᵢ⟩", "family": "Ontological", "polarity": "hybrid"},
    "KnowledgeFieldMetaCombo": {"formula": "KnowledgeField ⊙ Metaconcept(s)", "family": "Compositional", "polarity": "neutral"},
    "LocalActivationLateralInhibition": {"formula": "⊗⇒(Amplification, Regulation) | range(F_A) << range(F_R)", "family": "Dynamic", "polarity": "dual"},
    "ButterflyEffect": {"formula": "⊗⇒(Amplification, Trajectory) | λ > 0", "family": "Dynamic", "polarity": "dual"},
    
    # Relational Family (12)
    "Agent": {"formula": "S ⊗ I ⊗ D", "family": "Relational", "polarity": "neutral"},
    "Role": {"formula": "S ⊗ I", "family": "Relational", "polarity": "neutral"},
    "Mediator": {"formula": "F ⊗ I ⊗ S", "family": "Relational", "polarity": "neutral"},
    "Link": {"formula": "S ⊗ I ⊗ F", "family": "Relational", "polarity": "neutral"},
    "Relation": {"formula": "S ⊗ I", "family": "Relational", "polarity": "neutral"},
    "Path": {"formula": "S ⊗ I ⊗ D", "family": "Structural", "polarity": "neutral"},
    "Channel": {"formula": "S ⊗ I ⊗ F", "family": "Structural", "polarity": "neutral"},
    "Cluster": {"formula": "S ⊗ I ⊗ A", "family": "Structural", "polarity": "neutral"},
    "Component": {"formula": "S ⊗ I", "family": "Structural", "polarity": "neutral"},
    "Fusion": {"formula": "S ⊗ D", "family": "Dynamic", "polarity": "dual"},
    "Capacity": {"formula": "S ⊗ I", "family": "Structural", "polarity": "neutral"},
    
    # Metaconcept Families (5)
    "MetaConcept": {"formula": None, "family": "Meta", "polarity": None},
    "MetaconceptFamily": {"formula": None, "family": "Meta", "polarity": None},
    "MetaconceptPair": {"formula": None, "family": "Meta", "polarity": None},
    "DimensionPair": {"formula": None, "family": "Meta", "polarity": None},
    "SignPair": {"formula": None, "family": "Meta", "polarity": None},
    "StructuralPair": {"formula": None, "family": "Meta", "polarity": None},
    
    # MetaconceptCombos (2)
    "MetaconceptCombo": {"formula": "⊗ ᵢ₌₁ⁿ Mᵢ ⇒ M_result", "family": "Ontological", "polarity": "neutral"},
    # Cascade déjà compté dans Dynamic
}