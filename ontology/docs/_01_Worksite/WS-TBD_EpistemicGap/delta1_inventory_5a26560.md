# delta_1 inventory at 5a26560

## A. git grep hits by area and role

Command: `git grep -n -I -i -E "δ₁|δ1|δ\(M\)|epistemicGap|EpistemicGap|epistemic.gap|spectralClass|SpectralClass|spectral_class|delta_?1\b" -- . :(exclude)*migration_backups* :(exclude)*_backups* :(exclude)ontology/docs/_01_Worksite/WS-TBD_EpistemicGap/*`

| area | role | files | lines |
|---|---|---|---|
| M0 | use (see C) | 45 | 194 |
| M0_Common | ontology (see B) | 1 | 35 |
| M1 | ontology (see B) | 1 | 1 |
| M2 | ontology (see B) | 1 | 5 |
| M3 | ontology (see B) | 5 | 24 |
| archive | archive (Ref snapshot) | 3 | 171 |
| code | code | 46 | 142 |
| code | code (page) | 29 | 55 |
| data | data snapshot | 3 | 52 |
| docs | narrative | 134 | 522 |
| gate | check (SHACL) | 2 | 39 |
| gate/tooling | code | 3 | 9 |
| historical | narrative (historical) | 26 | 171 |
| narrative | narrative | 6 | 46 |
| skills | producer (instructions) | 6 | 33 |

Total: 311 files, 1499 lines.

## B. Ontology files: every JSON path mentioning the family

| file | node | key path | role | value (start) |
|---|---|---|---|---|
| M3_EagleEye.jsonld | `m3:eagle_eye:EagleEye` | `/dcterms:description` | doctrine | Territory Grammar Gt — the Territory perspective of TSCG (what a syste |
| M3_EagleEye.jsonld | `m3:eagle_eye:EagleEye` | `/coupling_with_MapGrammar/epistemic_gap` | definition (formula) | {"symbol": "δ₁", "formula": "\|\|ASFID_mean − REVOI_mean\|\| / √2", "meani |
| M3_EagleEye.jsonld | `m3:eagle_eye:EagleEye` | `/coupling_with_MapGrammar/epistemic_gap/symbol` | definition (formula) | δ₁ |
| M3_EagleEye.jsonld | `m3:eagle_eye:EagleEye` | `/coupling_with_MapGrammar/korzybski` | doctrine | The map is not the territory — Gt ≠ Gm structurally, δ₁ > 0 in all rea |
| M3_GenesisGrammar.jsonld | `m3:GenesisGrammar` | `/dcterms:description` | doctrine | M3 — the most abstract layer of the TSCG Layer Cake (M3 → M0), numbere |
| M3_GenesisGrammar.jsonld | `m3:GenesisGrammar` | `/grammar_foundation/connection/epistemic_gap` | definition (formula) | δ₁ = \|\|ASFID_mean − REVOI_mean\|\| / √2 |
| M3_GenesisGrammar.jsonld | `m3:GenesisGrammar` | `/three_perspectives/complementarity/feedback_loop/convergence` | doctrine | δ₁ → 0 represents epistemic equilibrium (Map ≈ Territory) |
| M3_GenesisGrammar.jsonld | `m3:GenesisGrammar` | `/m3:changelog[2]/adms:versionNotes` | history | WS-5 DEBT LOT (A), decision Michel 2026-10-08 (Debt Overview §8.0): th |
| M3_GenesisGrammar.jsonld | `m3:SystemicFramework` | `/m3:integrationGuidelines/step5` | doctrine | Document epistemic gaps and alignment scores |
| M3_GenesisGrammar.jsonld | `m3:CouplingStructure` | `/m3:mathematicalForm` | definition (formula) | Φ : Gt → Gm, Ψ : Gm → Gt (natural transformations), δ₁ = \|\|ASFID_mean  |
| M3_GenesisGrammar.jsonld | `m3:AlignmentLoop` | `/m3:iteration` | doctrine | iterative refinement via Φ/Ψ until δ₁ converges toward epistemic equil |
| M3_GenesisGrammar.jsonld | `m3:KorzybskiPrinciple` | `/m3:formalization` | doctrine | Φ : Gt → Gm is never a perfect isomorphism — δ₁ > 0 for all real syste |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:TypeSystem` | `/m3:grammar_foundation:levels/M0/curry_howard` | doctrine | Poclet = proof term. δ₁ = degree of proof (Curry-Howard correspondence |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:intersubjectiveBenchmark` | `/m3:grammar_foundation:structure/epistemicScore/property` | definition (formula) | m0:epistemicGap |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:SpecialElements` | `/StereopsisEmptySet/rdfs:comment` | doctrine | Neutral element of \|. Defined as EmptyTerritory \| EmptyMap. Divergent  |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:SpecialElements` | `/StereopsisEmptySet/m3:grammar_foundation:epistemicGap` | doctrine | δ₁ = max |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:SpecialElements` | `/StereopsisUniversalSet/rdfs:comment` | doctrine | Pseudo-absorbent of \|. Defined as 𝕋₀(×) ∪ 𝕋₀(+) ∪ 𝕋₀(\|) = 𝕋₀ (16 primi |
| M3_GrammarFoundation.jsonld | `m3:grammar_foundation:SpecialElements` | `/StereopsisUniversalSet/m3:grammar_foundation:epistemicGap` | doctrine | δ₁ = 0 |
| M3_OdinsWisdom.jsonld | `m3:odins_wisdom.StereopsisEmptySet` | `/rdfs:comment` | doctrine | Neutral element of \|. Defined as EmptyTerritory \| EmptyMap. x \| Stereo |
| M3_OdinsWisdom.jsonld | `m3:odins_wisdom.StereopsisEmptySet` | `/m3:epistemicGap` | doctrine | δ₁ = max |
| M3_SphinxEye.jsonld | `m3:sphinx_eye:SphinxEye` | `/dcterms:description` | doctrine | Map Grammar Gm — the Map perspective of TSCG (how a system is known; m |
| M3_SphinxEye.jsonld | `m3:sphinx_eye:SphinxEye` | `/coupling_with_TerritoryGrammar/epistemic_gap` | definition (formula) | {"symbol": "δ₁", "formula": "\|\|ASFID_mean − REVOI_mean\|\| / √2", "meani |
| M3_SphinxEye.jsonld | `m3:sphinx_eye:SphinxEye` | `/coupling_with_TerritoryGrammar/epistemic_gap/symbol` | definition (formula) | δ₁ |
| M3_SphinxEye.jsonld | `m3:sphinx_eye:SphinxEye` | `/coupling_with_TerritoryGrammar/korzybski` | doctrine | The map is not the territory — Gm ≠ Gt structurally, δ₁ > 0 in all rea |
| M2_GenericConcepts.jsonld | `m2:M2_GenericConcepts` | `/dcterms:description` | doctrine | Second layer of the TSCG Layer Cake: transdisciplinary GenericConcepts |
| M2_GenericConcepts.jsonld | `m2:M2_GenericConcepts` | `/m2:epistemicGapFormula` | definition (formula) | δ(M) = \|\|P(Reality) - Model\|\| ∈ [0,1] |
| M2_GenericConcepts.jsonld | `m2:hasEpistemicGap` | `/@id` | definition | m2:hasEpistemicGap |
| M2_GenericConcepts.jsonld | `m2:hasEpistemicGap` | `/rdfs:label` | definition | has epistemic gap |
| M2_GenericConcepts.jsonld | `m2:hasEpistemicGap` | `/@type` | definition | owl:DatatypeProperty |
| M2_GenericConcepts.jsonld | `m2:Modelisation` | `/m2:korzybskiConnection` | doctrine | Modelisation is the formal M2 instantiation of Korzybski's map-making  |
| M1_Optics.jsonld | `m1:MapTerritory_Optics` | `/m1:epistemicGap` | doctrine | ÃŽâ€ÃŽËœ = Ã¢â‚¬â€“Territory_ASFID - Map_REVOIÃ¢â‚¬â€“ quantifies mod |
| M0_Common.jsonld | `M0_Common.jsonld` | `/m3:changelog[0]/adms:versionNotes` | history | owl:oneOf of m0:SpectralClass, m0:FocalClass and m0:ScoringStatus writ |
| M0_Common.jsonld | `M0_Common.jsonld` | `/m0:namespaceConvention/shared/usage` | doctrine | m0:scoreA, m0:epistemicGap, m0:focalScore... |
| M0_Common.jsonld | `m0:epistemicGap` | `/@id` | definition | m0:epistemicGap |
| M0_Common.jsonld | `m0:epistemicGap` | `/rdfs:label` | definition | Epistemic Gap (δ₁) |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:spectralClassThresholds` | derived | {"Coherent": "δ₁ < 0.05", "OnCriticalLine": "0.05 ≤ δ₁ < 0.15", "Limin |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:spectralClassThresholds/Coherent` | derived | δ₁ < 0.05 |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:spectralClassThresholds/OnCriticalLine` | derived | 0.05 ≤ δ₁ < 0.15 |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:spectralClassThresholds/Liminal` | derived | 0.15 ≤ δ₁ < 0.30 |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:spectralClassThresholds/Enigmatic` | derived | δ₁ ≥ 0.30 |
| M0_Common.jsonld | `m0:epistemicGap` | `/@type` | definition | owl:DatatypeProperty |
| M0_Common.jsonld | `m0:epistemicGap` | `/rdfs:comment` | definition | Normalized distance between ASFID mean and REVOI mean: \|asfidMean − re |
| M0_Common.jsonld | `m0:epistemicGap` | `/m0:formula` | definition | \|m0:asfidMean − m0:revoiMean\| / √2 |
| M0_Common.jsonld | `m0:epistemicGap` | `/dcterms:creator` | definition | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:epistemicGap` | `/dcterms:created` | definition | 2026-06-19 |
| M0_Common.jsonld | `m0:SpectralClass` | `/@id` | derived | m0:SpectralClass |
| M0_Common.jsonld | `m0:SpectralClass` | `/rdfs:comment` | derived | Enumeration of epistemic gap (δ₁) qualitative classifications. Derived |
| M0_Common.jsonld | `m0:SpectralClass` | `/owl:oneOf/@list[0]/@id` | derived | m0:spectralClass.Coherent |
| M0_Common.jsonld | `m0:SpectralClass` | `/owl:oneOf/@list[1]/@id` | derived | m0:spectralClass.OnCriticalLine |
| M0_Common.jsonld | `m0:SpectralClass` | `/owl:oneOf/@list[2]/@id` | derived | m0:spectralClass.Liminal |
| M0_Common.jsonld | `m0:SpectralClass` | `/owl:oneOf/@list[3]/@id` | derived | m0:spectralClass.Enigmatic |
| M0_Common.jsonld | `m0:SpectralClass` | `/@type` | derived | owl:Class |
| M0_Common.jsonld | `m0:SpectralClass` | `/rdfs:label` | derived | Spectral Class |
| M0_Common.jsonld | `m0:SpectralClass` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:SpectralClass` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/@id` | derived | m0:spectralClass.Coherent |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/rdfs:comment` | derived | δ₁ < 0.05 — excellent Map/Territory alignment, strong epistemic cohere |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/m0:threshold` | derived | δ₁ < 0.05 |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/rdfs:label` | derived | Coherent |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:spectralClass.Coherent` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/@id` | derived | m0:spectralClass.OnCriticalLine |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/rdfs:comment` | derived | 0.05 ≤ δ₁ < 0.15 — good alignment with notable gap, on the epistemic b |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/m0:threshold` | derived | 0.05 ≤ δ₁ < 0.15 |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/rdfs:label` | derived | OnCriticalLine |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:spectralClass.OnCriticalLine` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/@id` | derived | m0:spectralClass.Liminal |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/rdfs:comment` | derived | 0.15 ≤ δ₁ < 0.30 — significant gap, Map and Territory partially misali |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/m0:threshold` | derived | 0.15 ≤ δ₁ < 0.30 |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/rdfs:label` | derived | Liminal |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:spectralClass.Liminal` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/@id` | derived | m0:spectralClass.Enigmatic |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/rdfs:comment` | derived | δ₁ ≥ 0.30 — large gap, Map and Territory strongly divergent |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/m0:threshold` | derived | δ₁ ≥ 0.30 |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/rdfs:label` | derived | Enigmatic |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:spectralClass.Enigmatic` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:spectralClass` | `/@id` | derived | m0:spectralClass |
| M0_Common.jsonld | `m0:spectralClass` | `/rdfs:comment` | derived | Qualitative classification of the epistemic gap δ₁ between ASFID and R |
| M0_Common.jsonld | `m0:spectralClass` | `/rdfs:range/@id` | derived | m0:SpectralClass |
| M0_Common.jsonld | `m0:spectralClass` | `/@type` | derived | owl:ObjectProperty |
| M0_Common.jsonld | `m0:spectralClass` | `/rdfs:label` | derived | spectral Class |
| M0_Common.jsonld | `m0:spectralClass` | `/dcterms:creator` | derived | Echopraxium with the collaboration of Claude AI |
| M0_Common.jsonld | `m0:spectralClass` | `/dcterms:created` | derived | 2026-06-19 |
| M0_Common.jsonld | `m0:scoringStatus.Complete` | `/rdfs:comment` | doctrine | All 10 ASFID+REVOI scores present. m0:asfidMean, m0:revoiMean, m0:epis |

Counts by file and role:

| file | role | paths |
|---|---|---|
| M0_Common.jsonld | definition | 7 |
| M0_Common.jsonld | derived | 46 |
| M0_Common.jsonld | doctrine | 2 |
| M0_Common.jsonld | history | 1 |
| M1_Optics.jsonld | doctrine | 1 |
| M2_GenericConcepts.jsonld | definition | 3 |
| M2_GenericConcepts.jsonld | definition (formula) | 1 |
| M2_GenericConcepts.jsonld | doctrine | 2 |
| M3_EagleEye.jsonld | definition (formula) | 2 |
| M3_EagleEye.jsonld | doctrine | 2 |
| M3_GenesisGrammar.jsonld | definition (formula) | 2 |
| M3_GenesisGrammar.jsonld | doctrine | 5 |
| M3_GenesisGrammar.jsonld | history | 1 |
| M3_GrammarFoundation.jsonld | definition (formula) | 1 |
| M3_GrammarFoundation.jsonld | doctrine | 5 |
| M3_OdinsWisdom.jsonld | doctrine | 2 |
| M3_SphinxEye.jsonld | definition (formula) | 2 |
| M3_SphinxEye.jsonld | doctrine | 2 |

## C. M0 instances: m0:epistemicGap on the owl:Ontology node

| instance | form | stored | stored class | class from thresholds | recomputed from means | note |
|---|---|---|---|---|---|---|
| M0_ButterflyMetamorphosis | float | 0.22 | - | Liminal | 0.0778 | stored != recomputed |
| M0_TscgCanopyGraphVizProto | float | 0.016 | Coherent | Coherent | 0.0113 |  |
| M0_CellSignalingModes | object | {'formula': 'ΔΘ = ‖|Ω_signalin | - | - | - |  |
| M0_CMYK_Subtractive | float | 0.27 | - | Liminal | - |  |
| M0_CMY_Subtractive | float | 0.28 | - | Liminal | - |  |
| M0_HSL_Additive | float | 0.37 | - | Enigmatic | - |  |
| M0_RGB_Additive | object | {'formula': 'ΔΘ = ‖|Ω_color⟩ - | - | - | - |  |
| M0_ComplexChemicalSynapse | float | 0.24 | - | Liminal | - |  |
| M0_Counterpoint | str | 0.016 | Coherent [0, 0.05) | Coherent | - |  |
| M0_ExposureTriangle | object | {'formula': 'ΔΘ = ‖|Ω_exposure | - | - | - |  |
| M0_FireTriangle | float | 0.099 | - | OnCriticalLine | 0.0990 |  |
| M0_FourStrokeEngine | float | 0.132 | - | OnCriticalLine | - |  |
| M0_NakamotoConsensus | object | {'norm': 0.072, 'deltaVector': | - | - | - |  |
| M0_NuclearReactorsTypology | float | 0.01 | - | Coherent | 0.0071 |  |
| M0_Ptoe | float | 0.057 | - | OnCriticalLine | 0.0566 |  |
| M0_QRCodeToPocketCity | float | 0.08 | OnCriticalLine | OnCriticalLine | - |  |
| M0_Thermostat | float | 0.014 | Coherent | Coherent | 0.0141 |  |
| M0_Transistor | float | 0.01 | - | Coherent | - |  |
| M0_World2DProjection | float | 0.17 | Liminal | Liminal | 0.1697 |  |
| M0_Kidneys | float | 0.01 | - | Coherent | - |  |
| M0_RAAS | float | 0.04 | - | Coherent | - |  |
| M0_TPACK | object | {'formula': 'Delta_Theta = ||O | - | - | - |  |
| M0_Bmc | float | 0.031 | Coherent | Coherent | 0.0311 |  |
| M0_Triz | float | 0.057 | OnCriticalLine | OnCriticalLine | 0.0566 |  |
| M0_VSM | typed literal | 0.08 | Coherent | OnCriticalLine | 0.0566 | class != thresholds, stored != recomputed |
| M0_TriskeleToolchain | float | 0.0255 | Coherent | Coherent | 0.0255 |  |
| M0_IChing | typed literal | 0.0339 | Coherent | Coherent | 0.0339 |  |
| M0_TscgOntologyAPIServer | float | 0.0339 | Coherent | Coherent | 0.0339 |  |
| M0_TscgOntologyExplorer | float | 0.0316 | Coherent | Coherent | 0.0000 | stored != recomputed |
| M0_TscgPocletGenerator | float | 0.136 | Coherent | OnCriticalLine | 0.0028 | class != thresholds, stored != recomputed |
| M0_TscgPocletMiner | float | 0.06 | Coherent | OnCriticalLine | 0.0410 | class != thresholds, stored != recomputed |

Forms on the owl:Ontology node: {'absent': 11, 'float': 23, 'object': 5, 'str': 1, 'no owl:Ontology node': 1, 'typed literal': 2}

m0:epistemicGap on another node of @graph (not the owl:Ontology node):
- M0_BloodPressureControl.jsonld @graph[1] (float)
- M0_ButterflyMetamorphosis.jsonld @graph[31] (float)
- M0_KindlebergerMinsky.jsonld @graph[1] (float)
- M0_MtgColorWheel.jsonld @graph[1] (dict)
- M0_PhaseTransition.jsonld @graph[1] (float)
- M0_PlateTectonics.jsonld @graph[1] (dict)
- M0_TrophicPyramid.jsonld @graph[1] (dict)
- M0_TVTestPattern.jsonld @graph[1] (dict)

## D. Formula census (gap formulas written in ontology and instance files)

| occurrences | formula (numbers -> N) |
|---|---|
| 2 | `δ₁ = ¦¦ASFID_mean − REVOI_mean¦¦ / √2` |
| 1 | `ΔΘ = ‖ ¦Ω_disc⟩ − ¦M_perceived⟩ ‖` |
| 1 | `δ₁ = ¦asfidMean − revoiMean¦ / √2` |
| 1 | `δ₁ = ¦N − N¦ / √2 = N → OnCriticalLine** (N ≤ δ₁ < 0` |
| 1 | `δ₁ = ¦N − N¦/√2 = N → OnCriticalLine.**` |
| 1 | `ΔΘ = ‖¦Ω_signaling⟩ - ¦M_4modes⟩‖` |
| 1 | `ΔΘ = ‖¦Ω_color⟩ - ¦M_RGB⟩‖` |
| 1 | `ΔΘ = ‖¦Ω_exposure⟩ - ¦M_triangle⟩‖` |
| 1 | `δ = ¦¦ASFID − REVOI¦¦ = sqrt((-N)² + (N)² + (N)² + (-0.` |
| 1 | `δ₁ = ¦¦ASFID_norm - REVOI_norm¦¦ / max_possible` |
| 1 | `delta1 = ¦¦ASFID - REVOI¦¦ / sqrt(5) = sqrt(N) / N ≈ N` |
| 1 | `δ₁ = ¦¦ASFID_mean - REVOI_mean¦¦ / √2` |
| 1 | `δ = 1 − (ASFID_mean + REVOI_mean) / 2 = 1 − (N + N) / 2` |
| 1 | `Delta_Theta = ¦¦Omega_teaching> - ¦M_tpack>¦¦` |
| 1 | `δ₁ = ¦N − N¦ / √2 = N. High S_score (N) reflects t` |
| 1 | `δ₁ = ¦N−N¦ / √2 = N. The intentional V_score=N (sy` |
| 1 | `δ(M) = ¦¦P(Reality) - Model¦¦ ∈ [0` |

## E. check_m0 PASS instances that carry the family on their owl:Ontology node

check_m0 statuses: {'FAIL': 25, 'PASS': 18}
PASS instances carrying the family: 14

- TscgCanopyGraphVizProto: m0:epistemicGap, m0:spectralClass
- FireTriangle: m0:epistemicGap, m0.fireTriangle:epistemicGap
- NuclearReactorsTypology: m0:epistemicGap
- Ptoe: epistemicGap, m0:epistemicGap
- QRCodeToPocketCity: m0:epistemicGap, m0:spectralClass
- Thermostat: m0:epistemicGap, m0:spectralClass, m0.thermostat:epistemicGap
- World2DProjection: m0:epistemicGap, m0:spectralClass, m0.world2DProjection:epistemicGap
- Bmc: m0:epistemicGap, m0:spectralClass
- Triz: m0:epistemicGap, m0:spectralClass
- TriskeleToolchain: m0:epistemicGap, m0:spectralClass, m0:spectralClassNote
- TscgOntologyAPIServer: m0:epistemicGap, m0:spectralClass
- TscgOntologyExplorer: m0:epistemicGap, m0:spectralClass
- TscgPocletGenerator: m0:epistemicGap, m0:spectralClass
- TscgPocletMiner: m0:epistemicGap, m0:spectralClass
