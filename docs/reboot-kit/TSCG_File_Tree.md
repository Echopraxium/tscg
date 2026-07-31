# TSCG — File Tree

**Version**: 17.0.1
**Date**: 2026-07-30
**Author**: Echopraxium with the collaboration of Claude AI
**Project**: TSCG (Transdisciplinary System Construction Game)
**Anchor**: repo HEAD `d92ded2` (origin/main), regenerated from the actual tree — not
a snapshot. Excludes `node_modules`, `_archives`, `*_backups`, vendored `pyshacl`,
and binary simulation assets (images/audio/fonts). Instance dirs are shown at the M0
level (sim assets omitted).

**Regeneration**: this file drifts every commit. To refresh, list HEAD and prune noise
(e.g. `git ls-files | grep -vE 'node_modules|_archives|_backups|\.(png|jpg|mp3|woff)'`).

---

## Meaningful tree (curated)

```
ontology/
  HANDOVER_2026-06-19 (1).md
  M0_Common.jsonld
  M1_CoreConcepts.jsonld
  M1_CoreConcepts_README.md
  M1_Domains.jsonld
  M1_Domains_README.md
  M2_GenericConcepts.jsonld
  M2_GenericConcepts_README.md
  M3_BicephalousPerspective.jsonld
  M3_BicephalousPerspective_README.md
  M3_EagleEye.jsonld
  M3_EagleEye_README.md
  M3_GenesisGrammar.jsonld
  M3_GenesisGrammar_README.md
  M3_GrammarFoundation.jsonld
  M3_GrammarFoundation_README.md
  M3_SphinxEye.jsonld
  M3_SphinxEye_README.md
  M1_extensions/
    biology/  M1_Biology.jsonld
    business_modeling/  M1_BusinessModeling.jsonld
    chemistry/  M1_Chemistry.jsonld
    economics/  M1_Economics.jsonld
    education/  M1_Education.jsonld
    electronics/  M1_Electronics.jsonld
    energy_generators/  M1_EnergyGenerators.jsonld
    geology/  M1_Geology.jsonld
    music/  M1_music.jsonld
    mythology/  M1_Mythology.jsonld
    optics/  M1_Optics.jsonld
    photography/  M1_Photography.jsonld
    physics/  M1_Physics.jsonld
    systemic_modeling/  M1_SystemicModeling.jsonld
  InstanceSimulations/
    M0_InstanceSimulation_UXControls.jsonld
    M0_InstanceSimulation_UXControls_README.md
    M0_InstanceSimulations.jsonld
    M0_InstanceSimulations_README.md
  StructuralGrammar/
    Braille_StructuralGrammar.pdf
    Functional_Grammar_Model.md
    HANDOVER_tscg_base16_session.md
    PotentialRefinements_MonoidalOperators.md
    StructuralGrammar_MonoidalOperators_README.md
    Structural_Grammar_Foundation.md
    Structural_Grammar_Foundation_README.md
    TSCG_IntersubjectiveBenchmark_for_DefeasibleKnowledge_README.md
    TSCG_Mathematical_Legitimacy_Summary.md
    TSCG_StructuralGrammar_as_Mathematical_Foundation_README.md
    _00_Session_Claude_GrammaireStructurelle.md
  docs/_01_Worksite/
      TSCG_OntologyValidator_Worksite_README.md
      TSCG_VocabularyConsolidation_Worksite_README.md
      WS-3/
        M2_Formulas_Review_with_Gs_README.md
      WS-8/
        Until_Further_Notice_WorksiteEntry.md
      WS-0/
        Functional_Grammar_Model.md
        M2_FeedbackLoop_Reclassification_README.md
        README.md
        SC-1_FunctionalGrammar_Handover.md
        TSCG_File_Tree.md
        TSCG_Session_Handover_2026-07-25.md
        _00_TSCG_Worksite_Map.md
        _01_Facet_as_M3_Principle_ArchitectureNote.md
        SC-1/
          SC-1_Completion_Report.md
          SC-1_FunctionalGrammar_Handover.md
          _00_TSCG_Worksite_Map_SC1-9.md
        Next Conversation_2026_07_30/
          SC-3_Facet_Decision_Record.md
instances/
  poclets/
    AdaptativeImmuneResponse/  M0_AdaptativeImmuneResponse.jsonld
    BloodPressureControl/  M0_BloodPressureControl.jsonld
    ButterflyMetamorphosis/  M0_ButterflyMetamorphosis.jsonld
    CanopyGraphVizProto/  M0_TscgCanopyGraphVizProto.jsonld
    CellSignalingModes/  M0_CellSignalingModes.jsonld
    ColorSynthesis/  M0_CMYK_Subtractive.jsonld M0_CMY_Subtractive.jsonld M0_ColorSynthesis.jsonld M0_HSL_Additive.jsonld
    ComplexChemicalSynapse/  M0_ComplexChemicalSynapse.jsonld complex_chemical_synapse_sim.py
    CounterPoint/  M0_Counterpoint.jsonld
    ExposureTriangle/  M0_ExposureTriangle.jsonld
    FireTriangle/  M0_FireTriangle.jsonld
    FourStrokeEngine/  M0_FourStrokeEngine.jsonld
    KindlebergerMinsky/  M0_KindlebergerMinsky.jsonld
    MtgColorWheel/  M0_MtgColorWheel.jsonld
    NakamotoConsensus/  M0_NakamotoConsensus.jsonld
    NuclearReactorsTypology/  M0_NuclearReactorsTypology.jsonld
    PhaseTransition/  M0_PhaseTransition.jsonld
    PlateTectonics/  M0_PlateTectonics.jsonld
    Ptoe/  M0_Ptoe.jsonld
    Theremin/  
    Transistor/  M0_Transistor.jsonld
    TrophicPyramid/  M0_TrophicPyramid.jsonld
    TvTestPattern/  M0_TVTestPattern.jsonld tv_test_pattern_sim.py
    Vco/  M0_VCO.jsonld
    kidneys/  M0_Kidneys.jsonld
    raas/  M0_RAAS.jsonld
    tpack/  M0_TPACK.jsonld tpack_sim.py
    yggdrasil/  M0_Yggdrasil.jsonld
  systemic-frameworks/
    Bmc/  M0_Bmc.jsonld M0_BmcSimulation.jsonld
    Triz/  M0_Triz.jsonld M0_Triz_Examples.jsonld
    vsm/  M0_VSM.jsonld
  symbolic-system-grammars/
    TriskeleToolchain/  M0_TriskeleToolchain.jsonld reorganize_projects.py run_all_tests.py run_pipeline.py
    TscgFoundationGrammar/  
    iching/  M0_IChing.jsonld
  tscg-tools/
    TscgLayerCakeMCPServer/  tscg_layercake_mcp_server.py
    TscgLittleBigBrain/  M0_Triz_Examples.jsonld TRIZ_vs_TSCG.py detect_scores.py diagnostic_scores.py
    TscgOntologyAPIServer/  M0_TscgOntologyAPIServer.jsonld
    TscgOntologyExplorer/  M0_TscgOntologyExplorer.jsonld
    TscgPocletGenerator/  M0_TscgPocletGenerator.jsonld tscg_poclet_generator.py tscg_rag_augmentor.py
    TscgPocletMiner/  M0_TscgPocletMiner.jsonld
    _archives/  
cli_tools/
  check-corpus-updates/  check-corpus-updates.py
  flexible-graphRAG/  
  generate_index-html/  Correction_Parsing_GraphZero.md README_Modifications.md
  migrate_properties/  migrate_properties.py migrate_properties_README.md
  ontology-linter/  AI_OntologyEngineering_Pitfalls_and_Solutions_README.md Prerequisites_Setup_README.md ontology_linter.py ontology_linter_README.md
  owl_reasoning_test/  TSCG_OWL_Validation_Session_Summary.md TSCG_Validation_Handoff_M1_M0.md convert_jsonld_to_turtle.py fix_owl_literals.py owl_reasoning_test.py owl_reasoning_test_README.md rdfs_diagnostic.py
  verify_migration/  verify_migration.py verify_migration_README.md```

---

## Notes on structure (vs the v16.1.0 tree)

- **`ontology/M0_Common.jsonld`** now exists (shared M0 vocabulary incl. the
  `m0:Facet` / `m0:hasFacet` mechanism — see SC-3 Decision Record).
- **M1 extensions = 14** under `ontology/M1_extensions/<domain>/` (added
  `business_modeling`).
- **Worksites reorganized to the WS-n scheme** under `ontology/docs/_01_Worksite/`:
  `WS-0` (Structural Cleanup, incl. `SC-1/` and dated `Next Conversation_*` opening
  packets), `WS-3` (Gs review), `WS-8` (Until Further Notice). Two loose worksite
  READMEs (OntologyValidator, VocabularyConsolidation) sit at the `_01_Worksite/` root.
- **Canopy** moved from `_protos/` to `instances/poclets/CanopyGraphVizProto/`
  (typed `m3:Poclet`).
- **New instances since v16.1.0**: `systemic-frameworks/Bmc` (Business Model Canvas),
  `symbolic-system-grammars/TriskeleToolchain`, `tscg-tools/TscgLayerCakeMCPServer`,
  `tscg-tools/TscgLittleBigBrain`.
- **`cli_tools/`** (underscore) is the tooling home: `ontology-linter/`,
  `owl_reasoning_test/`, `migrate_properties/`, `verify_migration/`,
  `check-corpus-updates/`. Note: the worksite map also references `cli-tools/` (hyphen)
  and `check-M2/`/`check-M3/`; confirm the canonical spelling before scripting (a known
  SC-1 tooling-path hazard).

- **Case divergence (local vs versioned)**: some instance dirs/files differ in case
  between the working tree and git (`Kidneys`↔`kidneys`, `Vsm`↔`vsm`, `M0_Vco`↔`M0_VCO`,
  `M1_Music`↔`M1_music`, etc.). This tree shows the **versioned** case (from the HEAD
  tarball). Raw GitHub URLs are case-sensitive — generate URL lists from `git ls-files`.
  (Worksite map §8.)

---

## CHANGELOG

- **17.0.1** (2026-07-30) — Added a note on local-vs-versioned case divergence.
- **17.0.0** (2026-07-30) — Full regeneration from HEAD `d92ded2`. Reflects the WS-n
  worksite reorganization, Canopy→poclets, M0_Common, 14 M1 extensions, and the new
  Bmc / TriskeleToolchain / MCP-server / LittleBigBrain instances. Version renumbered
  17.0.0 to break from the stale 16.1.0 lineage (the 2026-05-23 tree predated SC-1/SC-2
  and the Structural Grammar migration).
