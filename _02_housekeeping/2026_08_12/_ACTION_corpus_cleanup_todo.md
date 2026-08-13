> **THROWAWAY ACTION LIST — not corpus content.**
> This file is a one-time to-do: which project-knowledge files to keep vs remove.
> Do the removals in the project UI, then discard this file. It never goes into the corpus.
> (The permanent anchors are `TSCG_CorpusReference_Bootstrap.md` + `TSCG_CorpusReference.md`.)

# TSCG Cyclop v0 — Corpus Cleanup List

Generated from the actual project files (98 total). **KEEP = 27**, **REMOVE = 71**, orphans = 0.

Rule: a file is REMOVED from project knowledge when it has a live authority (HEAD) or is transient/superseded; it is KEPT only when it carries durable conceptual rationale with no fast-moving live source. Removing a file from the project does not delete it from the repo — HEAD remains the authority.

## KEEP (27) — durable conceptual essays + ontology READMEs with rationale

- `Archetypes_as_CrossCultural_Artifacts.md`
- `CredibilityAccretion_Process.md`
- `Functional_Grammar_Model.md`
- `LegoTechnic_Modularity.md`
- `M1_CoreConcepts_README.md`
- `M2_GenericConcepts_README.md`
- `M3_BicephalousPerspective_README.md`
- `M3_EagleEye_README.md`
- `M3_GenesisGrammar_README.md`
- `M3_GrammarFoundation_README.md`
- `M3_SphinxEye_README.md`
- `MultisubjectiveScoreEvaluationProtocol.md`
- `OntologicalOverfitting.md`
- `OntologyModeling_Guidelines.md`
- `Poclet_Analysis_Methodology.md`
- `Structural_Grammar_Foundation.md`
- `Structural_Grammar_Foundation_README.md`
- `SystemicEsperanto.md`
- `TSCG_Architectural_Extensions.md`
- `TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md`
- `TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md`
- `TerritoryMap_Dichotomy.md`
- `_00_TSCG_as_StereoscopicGlasses.md`
- `_01_Facet_as_M3_Principle_ArchitectureNote.md`
- `_01_Narcissus_and_Icarus_as_Safeguards.md`
- `poclet_terminology.md`
- `tscg_metrics_README.md`

## REMOVE (71)

### A. Live ontologies (.jsonld) — read from HEAD  (54)

- `M0_AdaptativeImmuneResponse.jsonld`
- `M0_BloodPressureControl.jsonld`
- `M0_ButterflyMetamorphosis.jsonld`
- `M0_CellSignalingModes.jsonld`
- `M0_ColorSynthesis.jsonld`
- `M0_Common.jsonld`
- `M0_ComplexChemicalSynapse.jsonld`
- `M0_Counterpoint.jsonld`
- `M0_ExposureTriangle.jsonld`
- `M0_FireTriangle.jsonld`
- `M0_FourStrokeEngine.jsonld`
- `M0_IChing.jsonld`
- `M0_Kidneys.jsonld`
- `M0_KindlebergerMinsky.jsonld`
- `M0_MtgColorWheel.jsonld`
- `M0_NakamotoConsensus.jsonld`
- `M0_NuclearReactorsTypology.jsonld`
- `M0_PhaseTransition.jsonld`
- `M0_PlateTectonics.jsonld`
- `M0_Ptoe.jsonld`
- `M0_RGB_Additive.jsonld`
- `M0_Raas.jsonld`
- `M0_Tpack.jsonld`
- `M0_Transistor.jsonld`
- `M0_Triz.jsonld`
- `M0_TrophicPyramid.jsonld`
- `M0_TscgOntologyAPIServer.jsonld`
- `M0_TscgOntologyExplorer.jsonld`
- `M0_TscgPocletMiner.jsonld`
- `M0_TvTestPattern.jsonld`
- `M0_Vco.jsonld`
- `M0_Vsm.jsonld`
- `M1_Biology.jsonld`
- `M1_BusinessModeling.jsonld`
- `M1_Chemistry.jsonld`
- `M1_CoreConcepts.jsonld`
- `M1_Domains.jsonld`
- `M1_Economics.jsonld`
- `M1_Education.jsonld`
- `M1_Electronics.jsonld`
- `M1_EnergyGenerators.jsonld`
- `M1_Geology.jsonld`
- `M1_Music.jsonld`
- `M1_Mythology.jsonld`
- `M1_Optics.jsonld`
- `M1_Photography.jsonld`
- `M1_Physics.jsonld`
- `M1_SystemicModeling.jsonld`
- `M2_GenericConcepts.jsonld`
- `M3_BicephalousPerspective.jsonld`
- `M3_EagleEye.jsonld`
- `M3_GenesisGrammar.jsonld`
- `M3_GrammarFoundation.jsonld`
- `M3_SphinxEye.jsonld`

### B. Live SHACL (.ttl) — read from HEAD  (2)

- `M0_Instances_Schema_shacl.ttl`
- `M1_Schema_shacl.ttl`

### C. Live code (.py) — read from HEAD  (1)

- `tscg_metrics.py`

### D. Live/transient state — read from HEAD  (5)

- `CLAUDE.md`
- `README.md`
- `TO_DO.txt`
- `TSCG_File_Tree.md`
- `_00_TSCG_Worksite_Map.md`

### E. Meta-index / superseded prompt  (3)

- `TSCG_Project_Corpus.md`
- `TSCG_Reference_Corpus.md`
- `TSCG_Smart_Prompt_v16_3_0.md`

### F. Instance/registry README mirrors (stale)  (3)

- `M0_PlateTectonics_README.md`
- `M0_TrophicPyramid_README.md`
- `M1_Domains_README.md`

### G. Completed/transient worksite docs -> git  (3)

- `M2_FeedbackLoop_Reclassification_README.md`
- `SC-1_Completion_Report.md`
- `SC-1_FunctionalGrammar_Handover.md`

---
*The two new anchor files replace what these removals take away:*
*`TSCG_CorpusReference_Bootstrap.md` (invariants) and `TSCG_CorpusReference.md` (folder→HEAD routing table).*