# TSCG M2 MetaConcepts Framework

Framework de modélisation systémique basé sur une algèbre tensorielle à 5 dimensions.

## Structure du Framework

### M3 - Genesis Space (Dimensions fondamentales)
- **A** (Attractor): Bassin d'attraction, état d'équilibre
- **D** (Dynamics): Évolution temporelle, changement
- **F** (Flow): Transfert de matière, énergie, information
- **I** (Information): Donnée, sens, représentation
- **S** (Structure): Topologie, organisation, arrangement spatial

### M2 - MetaConcepts (Tenseurs)


#### Famille Other

**Network**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_F.jsonld#F", "math:symbol": "F"}], "math:arity": 3, "math:latex": "S \\otimes  I \\otimes  F", "math:ascii": "S (x) I (x) F"}$
- Description: Set of nodes connected by edges enabling distributed interactions.
- Exemples:
  - Neural networks
  - Internet

**Constraint**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}], "math:arity": 2, "math:latex": "S \\otimes  I", "math:ascii": "S (x) I"}$
- Description: Restriction on possible system states or trajectories, limiting degrees of freedom.
- Exemples:
  - Physical conservation laws
  - Budget limits

**Signature**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) S", "math:latex": "I (x) S"}$
- Description: Characteristic pattern enabling unique identification.
- Exemples:
  - Spectral signature
  - Fingerprint

**Bifurcation**
- Formule: ${"@type": "math:RawString", "math:value": "dD/dF", "math:latex": "dD/dF"}$
- Description: Qualitative change in system behavior at critical parameter threshold.
- Exemples:
  - Ecosystem regime shifts
  - Phase transitions

**Step**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}], "math:arity": 3, "math:latex": "S \\otimes  I \\otimes  D", "math:ascii": "S (x) I (x) D"}$
- Description: Node specialized for sequential/temporal contexts.
- Exemples:
  - Butterfly egg stage
  - Recipe step

**Threshold**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}], "math:arity": 2, "math:latex": "A \\otimes  I", "math:ascii": "A (x) I"}$
- Description: Critical value triggering qualitative change in system behavior.
- Exemples:
  - Tipping point
  - Activation threshold

**Composition**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes A", "math:latex": "S \\otimes I \\otimes A"}$
- Description: Bidirectional structural operation forming the fundamental duality of assembly and disassembly.
- Exemples:
  - LEGO bricks → construction
  - Atoms → molecule

**Imbrication**
- Formule: ${"@type": "math:RawString", "math:value": "S → S", "math:latex": "S → S"}$
- Description: Structural relation where a system contains subsystems that reproduce the parent system's structure.
- Exemples:
  - Mandelbrot set
  - Bronchial tree
  - VSM recursive viability

**LocalActivationLateralInhibition**
- Formule: ${"@type": "math:Equation", "math:left": {"@type": "math:RawString", "math:value": "(x)", "math:latex": "(x)"}, "math:right": {"@type": "math:RawString", "math:value": ">(Amplification, Regulation) | range(F_A) << range(F_R)", "math:latex": ">(Amplification, Regulation) | range(F_A) << range(F_R)"}, "math:latex": "(x)=>(Amplification, Regulation) | range(F_A) << range(F_R)"}$
- Description: Binary MetaconceptCombo in which a local self-reinforcing process (Amplification, short range) is structurally coupled to a longer-range inhibitory process (Regulation), producing stable periodic spatial or functional patterns.
- Exemples:
  - Lateral inhibition in neuroscience
  - Turing morphogenesis

**Segmentation**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) D", "math:latex": "S (x) I (x) D"}$
- Description: Partition of a whole into homogeneous segments according to similarity, continuity, or structural criteria.
- Exemples:
  - Market segmentation
  - Image segmentation

**Resilience**
- Formule: ${"@type": "math:RawString", "math:value": "A \\otimes S", "math:latex": "A \\otimes S"}$
- Description: Capacity to absorb disturbances while retaining fundamental structure and function.
- Exemples:
  - Bridge withstanding earthquake
  - Ecosystem recovery after wildfire

**System**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) F", "math:latex": "S (x) F"}$
- Description: Organized set of interacting components with defined boundary.
- Exemples:
  - Living cell
  - Computer system

**Symmetry**
- Formule: ${"@type": "math:Variable", "math:symbol": "S", "math:reference": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S"}$
- Description: Invariance under transformation.
- Exemples:
  - Crystal lattice symmetries
  - Conservation laws (Noether)

**Modularity**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I", "math:latex": "S \\otimes I"}$
- Description: Decomposition into semi-independent functional units.
- Exemples:
  - Software modules
  - Organ systems

**Topology**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I", "math:latex": "S \\otimes I"}$
- Description: Classification of structural properties preserved under continuous deformations.
- Exemples:
  - Network topology types
  - Topological invariants

**Action**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}], "math:arity": 2, "math:latex": "D \\otimes  I", "math:ascii": "D (x) I"}$
- Description: Atomic operation triggered by a Step.
- Exemples:
  - HTTP tokenize
  - Cell division

**Gradient**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "math:Unknown", "math:name": ""}, {"@type": "math:Unknown", "math:name": "₂F or"}, {"@type": "math:Unknown", "math:name": "₂I"}], "math:arity": 3, "math:latex": "\\otimes  ₂F or \\otimes  ₂I", "math:ascii": "(x) ₂F or (x) ₂I"}$
- Description: Spatial or temporal variation creating driving force for flows.
- Exemples:
  - Temperature gradient
  - Concentration gradient

**Convergence**
- Formule: ${"@type": "math:RawString", "math:value": "-\\nabla \\cdot D / \\nabla \\cdot D", "math:latex": "-\\nabla \\cdot D / \\nabla \\cdot D"}$
- Description: Focusing or dispersing of flows, trajectories, or information.
- Exemples:
  - Beam focusing/spreading
  - Convergent/divergent evolution

**Transformation**
- Formule: ${"@type": "math:RawString", "math:value": "D (x) S (x) I", "math:latex": "D (x) S (x) I"}$
- Description: Fundamental change in system state, structure, or identity.
- Exemples:
  - Chemical reactions
  - Metamorphosis

**Adaptation**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) F (x) D", "math:latex": "I (x) F (x) D"}$
- Description: Progressive modification of structure or behavior in response to environmental changes.
- Exemples:
  - Bacterial antibiotic resistance
  - Neural plasticity

**Dissipation**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_F.jsonld#F", "math:symbol": "F"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}], "math:arity": 2, "math:latex": "F \\otimes  D", "math:ascii": "F (x) D"}$
- Description: Irreversible energy degradation and entropy production.
- Exemples:
  - Heat loss in engines
  - Friction

**State**
- Formule: ${"@type": "math:Variable", "math:symbol": "I", "math:reference": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I"}$
- Description: Instantaneous configuration of system variables.
- Exemples:
  - System state vector
  - Configuration

**Trade-off**
- Formule: ${"@type": "math:RawString", "math:value": "A \\otimes I \\otimes F", "math:latex": "A \\otimes I \\otimes F"}$
- Description: Deliberate exchange where improving one desirable property necessarily degrades another due to inherent constraints.
- Exemples:
  - Speed-Precision trade-off
  - Bias-Variance trade-off

**Environment**
- Formule: ${"@type": "math:RawString", "math:value": "F \\otimes I", "math:latex": "F \\otimes I"}$
- Description: External context with which system exchanges matter, energy, information.
- Exemples:
  - Ecological niche
  - Market context

**MetaconceptCombo**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "math:Unknown", "math:name": ""}, {"@type": "math:Unknown", "math:name": "ᵢ₌₁ⁿ Mᵢ ⇒ M_result"}], "math:arity": 2, "math:latex": "\\otimes  ᵢ₌₁ⁿ Mᵢ ⇒ M_result", "math:ascii": "(x) ᵢ₌₁ⁿ Mᵢ ⇒ M_result"}$
- Description: Parameterized metaconcept produced by synergistic combination of N parent metaconcepts (N ≥ 2) via n-ary tensor assembly and emergence morphism.
- Exemples:
  - VarietyAmplification = ValueSpace ⊗ Amplification
  - AdaptiveRegulatedLearning = Regulation ⊗ Adaptation ⊗ Memory

**Signal**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) F", "math:latex": "I (x) F"}$
- Description: Carrier of information through space or time, enabling communication.
- Exemples:
  - Radio wave
  - Neural action potential

**Polarity**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) A", "math:latex": "S (x) I (x) A"}$
- Description: Configuration of N distinct, mutually exclusive value poles or orientational axes organized in structured opposition or complementarity.
- Exemples:
  - Political Compass (N=4)
  - Magic Color Wheel (N=5)
  - Wu Xing (N=5)

**KnowledgeFieldMetaCombo**
- Formule: ${"@type": "math:Equation", "math:left": {"@type": "math:RawString", "math:value": "KnowledgeField (o) (x)_i", "math:latex": "KnowledgeField (o) (x)_i"}, "math:right": {"@type": "math:RawString", "math:value": "1^n M_i", "math:latex": "1^n M_i"}, "math:latex": "KnowledgeField (o) (x)_i=1^n M_i"}$
- Description: Factorization metaconcept coupling a KnowledgeField (disciplinary tag) with one or more universal Metaconcepts to create domain-specific specializations.
- Exemples:
  - BiologicalProcessor = Biological ⊙ Processor
  - ChemicalLink = Chemical ⊙ Link

**Pattern**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) A", "math:latex": "S (x) I (x) A"}$
- Description: Recurring structural motif identifiable across instances and reusable as template.
- Exemples:
  - Branching pattern in biology
  - Design patterns in software

**Path**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) D", "math:latex": "S (x) I (x) D"}$
- Description: Planned or conceptual route through network structure.
- Exemples:
  - Shortest path algorithm
  - Metabolic pathway diagram

**Role**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I", "math:latex": "S (x) I"}$
- Description: Functional position or responsibility within system structure.
- Exemples:
  - Server/client role
  - Social role

**Processor**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes D \\otimes F \\otimes V \\otimes R", "math:latex": "S \\otimes I \\otimes D \\otimes F \\otimes V \\otimes R"}$
- Description: Generic system with inputs and outputs that transforms/processes incoming resources, signals, or matter into outputs.
- Exemples:
  - Microprocessor
  - Digestive System

**Tropism**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_F.jsonld#F", "math:symbol": "F"}], "math:arity": 4, "math:latex": "A \\otimes  S \\otimes  D \\otimes  F", "math:ascii": "A (x) S (x) D (x) F"}$
- Description: Specialized Behavior directed by external gradient stimulus.
- Exemples:
  - Phototropism
  - Chemotaxis

**Mediator**
- Formule: ${"@type": "math:RawString", "math:value": "F \\otimes I \\otimes S", "math:latex": "F \\otimes I \\otimes S"}$
- Description: Intermediary entity or mechanism enabling interaction between components.
- Exemples:
  - Catalyst
  - API gateway

**Event**
- Formule: ${"@type": "math:RawString", "math:value": "D (x) I", "math:latex": "D (x) I"}$
- Description: Discrete occurrence with temporal localization.
- Exemples:
  - Action potential spike
  - Transaction

**Capacity**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}], "math:arity": 2, "math:latex": "S \\otimes  I", "math:ascii": "S (x) I"}$
- Description: Upper structural limit or maximal potential of system.
- Exemples:
  - Channel bandwidth
  - Carrying capacity

**Behavior**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes D \\otimes F", "math:latex": "S \\otimes D \\otimes F"}$
- Description: Network of coordinated Steps that can be decomposed and analyzed.
- Exemples:
  - HTTP request handling
  - Predator hunting sequence

**Hierarchy**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}], "math:arity": 2, "math:latex": "S \\otimes  A", "math:ascii": "S (x) A"}$
- Description: Nested levels of organization with vertical control relations.
- Exemples:
  - Biological organization
  - Corporate org chart

**Homeostasis**
- Formule: ${"@type": "math:RawString", "math:value": "A \\otimes S \\otimes F", "math:latex": "A \\otimes S \\otimes F"}$
- Description: Self-regulation maintaining stable internal state despite external perturbations.
- Exemples:
  - pH balance in cells
  - Body temperature regulation

**Identity**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) A (x) V (x) E", "math:latex": "S (x) I (x) A (x) V (x) E"}$
- Description: Persistent property that makes an entity distinguishable and self-restoring across transformations.
- Exemples:
  - Molecular identity
  - Genetic identity
  - Object identity (UUID)

**Code**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) S", "math:latex": "I (x) S"}$
- Description: System of rules for systematic transformation between domains.
- Exemples:
  - Genetic code
  - Morse code

**Self-Organization**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}], "math:arity": 3, "math:latex": "A \\otimes  I \\otimes  D", "math:ascii": "A (x) I (x) D"}$
- Description: Spontaneous emergence of ordered patterns without external direction.
- Exemples:
  - Flocking behavior
  - Crystal formation

**Invariant**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}], "math:arity": 2, "math:latex": "S \\otimes  A", "math:ascii": "S (x) A"}$
- Description: Property unchanged under specific transformations or operations.
- Exemples:
  - Conservation laws
  - Topological invariants

**Channel**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes F", "math:latex": "S \\otimes I \\otimes F"}$
- Description: Structured conduit for signal transmission. Isolates one dimension, filters content, has finite capacity.
- Exemples:
  - Ion channels
  - RGB color channels

**Trajectory**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_F.jsonld#F", "math:symbol": "F"}], "math:arity": 3, "math:latex": "A \\otimes  D \\otimes  F", "math:ascii": "A (x) D (x) F"}$
- Description: Observable path through state space traced by system evolution over time.
- Exemples:
  - Projectile trajectory
  - Blood pressure trajectory

**Relation**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}], "math:arity": 2, "math:latex": "S \\otimes  I", "math:ascii": "S (x) I"}$
- Description: Abstract connection or association between entities, identified through analysis or modeling.
- Exemples:
  - Semantic relation
  - Causal relation

**Activation**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_A.jsonld#A", "math:symbol": "A"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}], "math:arity": 2, "math:latex": "A \\otimes  D", "math:ascii": "A (x) D"}$
- Description: Enabling or blocking of processes or pathways.
- Exemples:
  - Lateral inhibition in neuroscience
  - Turing morphogenesis
  - Lateral inhibition in neuroscience

**ValueSpace**
- Formule: ${"@type": "math:RawString", "math:value": "It → V → O → R → Im", "math:latex": "It → V → O → R → Im"}$
- Description: Space of possible values for a property or object.
- Exemples:
  - RGB color [0,255]³
  - Temperature [0,100]°C

**Link**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes F", "math:latex": "S \\otimes I \\otimes F"}$
- Description: Concrete physical connection between nodes enabling actual information or resource transfer.
- Exemples:
  - Network edge
  - Synaptic connection

**Amplification**
- Formule: ${"@type": "math:RawString", "math:value": "F_t \\otimes D \\otimes I_t \\otimes R \\otimes O", "math:latex": "F_t \\otimes D \\otimes I_t \\otimes R \\otimes O"}$
- Description: Bidirectional process: increase (amplification) or decrease (attenuation) of signal, flow, quantity, or variety.
- Exemples:
  - Enzymatic cascade
  - Electronic amplifier

**Language**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) S (x) F", "math:latex": "I (x) S (x) F"}$
- Description: Structured system for information exchange and meaning construction.
- Exemples:
  - Programming language
  - Natural language

**Coding**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}], "math:arity": 3, "math:latex": "I \\otimes  S \\otimes  D", "math:ascii": "I (x) S (x) D"}$
- Description: Bidirectional transformation between information and coded representation.
- Exemples:
  - DNA transcription/translation
  - Encryption/Decryption

**Trigger**
- Formule: ${"@type": "math:RawString", "math:value": "D (x) I", "math:latex": "D (x) I"}$
- Description: Initiating stimulus for process activation.
- Exemples:
  - Signal transduction trigger
  - Interrupt handler

**Domain**
- Formule: ${"@type": "math:RawString", "math:value": "sum_i sigma_i |u_i> (x) |v_i>", "math:latex": "sum_i sigma_i |u_i> (x) |v_i>"}$
- Description: Structured field of knowledge where Territory phenomena (ASFID) and Map frameworks (REVOI) are coupled through epistemic practices.
- Exemples:
  - Biology (σ_mean=0.75)
  - Nuclear Engineering (σ_mean=0.86)
  - Optics (σ_mean=0.80)

**Space**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I", "math:latex": "S \\otimes I"}$
- Description: Dimensional framework in which system states and trajectories exist (state space, phase space).
- Exemples:
  - State space
  - RGB color [0,255]³
  - Phase space

**Workflow**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_D.jsonld#D", "math:symbol": "D"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_F.jsonld#F", "math:symbol": "F"}], "math:arity": 3, "math:latex": "S \\otimes  D \\otimes  F", "math:ascii": "S (x) D (x) F"}$
- Description: Structured network implementation of a Process.
- Exemples:
  - Manufacturing process workflow
  - CI/CD pipeline

**ButterflyEffect**
- Formule: ${"@type": "math:EmergentCombo", "math:type": "metaconcept_combo", "math:factors": ["Amplification", "Trajectory"], "math:arity": 2, "math:semantics": "synergistic_combination", "math:emergence": true, "math:latex": "\\otimes\\Rightarrow(Amplification, Trajectory)"}$
- Description: Binary MetaconceptCombo in which unconstrained local positive feedback (Amplification) is coupled with a chaotic system trajectory, producing exponential divergence of initially nearby system trajectories.
- Exemples:
  - Lorenz system
  - Double pendulum

**Node**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I", "math:latex": "S \\otimes I"}$
- Description: Elementary entity or point in a network structure, serving as connection endpoint.
- Exemples:
  - Vertex in graph
  - Server in network

**Synergy**
- Formule: $(-1)^{p} (I ⊗ D)$
- Description: Combined effect differing from sum of individual effects (enhancement or inhibition).
- Exemples:
  - Drug synergy
  - Interference patterns

**Component**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I", "math:latex": "S \\otimes I"}$
- Description: Elementary constitutive part of a system with functional role in the whole.
- Exemples:
  - RGB primaries
  - Fire Triangle: Fuel, Oxygen, Heat

**Emergence**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) S (x) D", "math:latex": "I (x) S (x) D"}$
- Description: Appearance of novel properties at system level not predictable from components alone.
- Exemples:
  - Traffic jams from individual drivers
  - Consciousness from neural interactions

**Scope**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes A \\otimes R", "math:latex": "S \\otimes I \\otimes A \\otimes R"}$
- Description: Domain of validity or applicability where an entity, rule, or authority has effect. Defines a positive boundary of what is permitted or possible.
- Exemples:
  - Jurisdiction boundaries
  - Variable scope in programming

**Balance**
- Formule: ${"@type": "math:RawString", "math:value": "A (x) S (x) F", "math:latex": "A (x) S (x) F"}$
- Description: State of equilibrium between multiple interacting factors where variations compensate to maintain system stability.
- Exemples:
  - Photographic exposure
  - Chemical equilibrium

**Hub**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) F", "math:latex": "S (x) F"}$
- Description: Highly connected node serving as central routing point for flow redistribution, without active processing.
- Exemples:
  - Nerve plexus
  - Airport hub

**KnowledgeField**
- Formule: ${"@type": "math:RawString", "math:value": "sum_i sigma_i |u_i> (x) |v_i>", "math:latex": "sum_i sigma_i |u_i> (x) |v_i>"}$
- Description: Structured field of knowledge where Territory phenomena (ASFID) and Map frameworks (REVOI) are coupled through epistemic practices.
- Exemples:
  - BiologicalProcessor = Biological ⊙ Processor
  - ChemicalLink = Chemical ⊙ Link
  - BiologicalProcessor = Biological ⊙ Processor

**Memory**
- Formule: ${"@type": "math:Integral", "math:integrand": {"@type": "math:RawString", "math:value": "D−F", "math:latex": "D−F"}, "math:variable": "τ", "math:latex": "\\int (D−F)\\,d\\tau"}$
- Description: Retention of past states influencing current behavior through temporal integration.
- Exemples:
  - Material hysteresis
  - Neural synaptic weights

**Fusion**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes D", "math:latex": "S \\otimes D"}$
- Description: Union or separation of entities.
- Exemples:
  - Nuclear fusion/fission
  - Cell fusion/fission

**Regulation**
- Formule: ${"@type": "math:RawString", "math:value": "A \\otimes S \\otimes F", "math:latex": "A \\otimes S \\otimes F"}$
- Description: Control mechanisms maintaining system parameters within acceptable ranges.
- Exemples:
  - Traffic light systems
  - Hormonal feedback loops

**Observer**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) A", "math:latex": "I (x) A"}$
- Description: Entity performing measurement or interpretation of system state.
- Exemples:
  - Scientific measurement apparatus
  - Sensor

**FeedbackLoop**
- Formule: ${"@type": "math:RawString", "math:value": "A \\otimes S \\otimes F \\otimes I \\otimes D", "math:latex": "A \\otimes S \\otimes F \\otimes I \\otimes D"}$
- Description: Cyclic regulatory process where a system compares its current state to a target, reduces the discrepancy, and evolves over time.
- Exemples:
  - Thermostat
  - Insulin-glucose regulation

**Substrate**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes F", "math:latex": "S \\otimes F"}$
- Description: Material or informational support enabling system existence.
- Exemples:
  - Physical medium
  - Hardware platform

**Agent**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) I (x) D", "math:latex": "S (x) I (x) D"}$
- Description: Active entity capable of autonomous action and interaction.
- Exemples:
  - Software agent
  - Autonomous robot

**M2_MetaConcepts**
- Formule: ${"@type": "math:Equation", "math:left": {"@type": "math:RawString", "math:value": "δ(M)", "math:latex": "δ(M)"}, "math:right": {"@type": "math:RawString", "math:value": "||P(Reality) - Model|| ∈ [0,1]", "math:latex": "||P(Reality) - Model|| ∈ [0,1]"}, "math:latex": "δ(M) = ||P(Reality) - Model|| ∈ [0,1]"}$
- Description: Atomic operation triggered by a Step.
- Exemples:
  - Transaction
  - Chemical reactions
  - Radio wave

**Process**
- Formule: ${"@type": "math:RawString", "math:value": "D (x) F", "math:latex": "D (x) F"}$
- Description: Sequence of state changes over time.
- Exemples:
  - Metabolic pathway
  - Digestive System
  - Microprocessor

**Storage**
- Formule: ${"@type": "math:RawString", "math:value": "S (x) F", "math:latex": "S (x) F"}$
- Description: Function of retaining and accumulating matter, energy, or information.
- Exemples:
  - Data warehouse
  - Battery storage

**Cascade**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes A \\otimes D \\otimes F", "math:latex": "S \\otimes I \\otimes A \\otimes D \\otimes F"}$
- Description: Sequential multi-stage process where output of each step becomes input of next step, following a trajectory toward goal state.
- Exemples:
  - Compiler pipeline
  - Blood coagulation cascade
  - RAAS hormonal cascade

**Representation**
- Formule: ${"@type": "math:TensorProduct", "math:factors": [{"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_I.jsonld#I", "math:symbol": "I"}, {"@type": "m3:Dimension", "@id": "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/m3_S.jsonld#S", "math:symbol": "S"}], "math:arity": 2, "math:latex": "I \\otimes  S", "math:ascii": "I (x) S"}$
- Description: Mapping between domains preserving structural relationships.
- Exemples:
  - Mental schemas
  - Mathematical models

**Cluster**
- Formule: ${"@type": "math:RawString", "math:value": "S \\otimes I \\otimes A", "math:latex": "S \\otimes I \\otimes A"}$
- Description: Dense local grouping of nodes exhibiting synergistic cooperation and emergent functional properties.
- Exemples:
  - Enteric nervous system
  - Innovation clusters

**Alignment**
- Formule: ${"@type": "math:RawString", "math:value": "I (x) A (x) S", "math:latex": "I (x) A (x) S"}$
- Description: Bidirectional dynamic process by which two entities, representations, or systems progressively reduce their mutual discrepancy toward a coherent correspondence.
- Exemples:
  - Wheel alignment
  - DNA sequence alignment
