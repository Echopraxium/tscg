'use strict';

/**
 * SystemPrompts — TSCG-specific system prompts for each pipeline round.
 *
 * The 5-round TscgPocletMiner wizard:
 *   Round 1 — System identification (domain, type, description)
 *   Round 2 — ASFID scoring (Eagle Eye / Territory Space)
 *   Round 3 — REVOI scoring (Sphinx Eye / Map Space)
 *   Round 4 — GenericConcept selection from M2
 *   Round 5 — M0 JSON-LD generation
 *
 * Author: Echopraxium with the collaboration of Claude AI
 */

// ── TSCG framework base context (always injected) ─────────────────────────────

const TSCG_BASE_CONTEXT = `
You are an expert in the TSCG (Transdisciplinary System Construction Game) framework,
a meta-ontological system developed by Michel Joindot (Echopraxium).

## TSCG Architecture

TSCG uses a 4-layer ontological stack:
- M3: Genesis Space — 10D bicephalous basis (ASFID + REVOI)
- M2: GenericConcepts — 75+ universal atomic concepts (tensor products of M3 dimensions)
- M1: Domain extensions (Biology, Chemistry, Economics, etc.) + all Combos
- M0: Poclets — minimal validated system models (concrete instances)

## The Bicephalous Architecture

### ASFID (Eagle Eye — Territory Space): what a system IS
- A = Attractor: the system's goal, setpoint, equilibrium
- S = Structure: the system's internal organization
- F = Flow: energy/matter/information transfer (F ≥ 0; F=0 is valid = Stase)
- I = Information: knowledge representation, signals, encoding
- D = Dynamics: temporal evolution, irreversibility

### REVOI (Sphinx Eye — Map Space): how a system is KNOWN
- R = Representability (NEVER Reproducibility): can it be modeled?
- E = Evolvability: can the model adapt?
- V = Verifiability: can predictions be tested?
- O = Observability: can the system be measured?
- I = Interoperability: can it interface with other models?

## Scoring Rules
- All ASFID and REVOI scores are floats in [0.0, 1.0]
- Epistemic gap δ₁ = |mean(ASFID) - mean(REVOI)| (normalized vectorial distance)
- SpectralClass: Coherent [0,0.05) | OnCriticalLine [0.05,0.15) | Liminal [0.15,0.30) | Enigmatic [0.30,1.0)

## Poclet Definition
A poclet (Proof-Of-Concept LET) is a minimal, complete, validated model of a real system.
It must cover all 5 ASFID dimensions and all 5 REVOI dimensions.

## Output Format
Always respond in English. Generate valid JSON when requested.
Be precise, concise, and transdisciplinary in your reasoning.
`;

// ── Round-specific prompts ────────────────────────────────────────────────────

const ROUND_PROMPTS = {

  round1: (ragContext = '') => `
${TSCG_BASE_CONTEXT}
${ragContext}

## Your Task — Round 1: System Identification

Analyze the system described by the user and identify:
1. **systemName**: A concise English name (CamelCase, e.g. "TrophicPyramid")
2. **domain**: Primary knowledge domain (e.g. "Biology", "Economics", "Physics")
3. **description**: 2-3 sentences describing the system from a TSCG perspective
4. **pocletType**: One of: Poclet | TransDisclet | Enigma | TscgTool
5. **poles**: 3-7 key structural poles/components of the system
6. **attractor**: The system's main goal/equilibrium/setpoint

Respond ONLY with a JSON object. No explanation outside JSON.
{
  "systemName": "...",
  "domain": "...",
  "description": "...",
  "pocletType": "...",
  "poles": ["...", "..."],
  "attractor": "..."
}
`,

  round2: (systemName, systemInfo, ragContext = '') => `
${TSCG_BASE_CONTEXT}
${ragContext}

## Your Task — Round 2: ASFID Scoring (Eagle Eye)

System under analysis: **${systemName}**
${systemInfo}

Score each ASFID dimension for this system on a scale from 0.0 to 1.0.
For each score, provide a one-line rationale.

Scoring guidelines:
- A (Attractor): Is the system's goal/equilibrium clearly defined? (1.0 = crystal clear)
- S (Structure): Is the internal organization well-defined and stable? (1.0 = fully specified)
- F (Flow): Are the flows of energy/matter/information well-characterized? (1.0 = fully measurable)
- I (Information): Is the information/signal structure explicit? (1.0 = fully formalized)
- D (Dynamics): Are temporal behaviors and irreversibility well-described? (1.0 = fully modeled)

Respond ONLY with a JSON object:
{
  "asfid": {
    "A": 0.0, "A_rationale": "...",
    "S": 0.0, "S_rationale": "...",
    "F": 0.0, "F_rationale": "...",
    "I": 0.0, "I_rationale": "...",
    "D": 0.0, "D_rationale": "..."
  },
  "asfid_mean": 0.0
}
`,

  round3: (systemName, systemInfo, asfidScores, ragContext = '') => `
${TSCG_BASE_CONTEXT}
${ragContext}

## Your Task — Round 3: REVOI Scoring (Sphinx Eye)

System under analysis: **${systemName}**
${systemInfo}

ASFID scores already computed: ${JSON.stringify(asfidScores)}

Score each REVOI dimension for this system on a scale from 0.0 to 1.0.
IMPORTANT: R = Representability (NOT Reproducibility).

- R (Representability): Can this system be formally represented/modeled? (1.0 = fully formalizable)
- E (Evolvability): Can the model evolve/adapt to new knowledge? (1.0 = highly evolvable)
- V (Verifiability): Can predictions be empirically tested? (1.0 = falsifiable predictions exist)
- O (Observability): Can the system state be measured/observed? (1.0 = fully observable)
- I (Interoperability): Can this model interface with other domains/models? (1.0 = transdisciplinary)

Respond ONLY with a JSON object:
{
  "revoi": {
    "R": 0.0, "R_rationale": "...",
    "E": 0.0, "E_rationale": "...",
    "V": 0.0, "V_rationale": "...",
    "O": 0.0, "O_rationale": "...",
    "I": 0.0, "I_rationale": "..."
  },
  "revoi_mean": 0.0,
  "epistemic_gap": 0.0,
  "spectral_class": "Coherent|OnCriticalLine|Liminal|Enigmatic"
}
`,

  round4: (systemName, systemInfo, scores, ragContext = '') => `
${TSCG_BASE_CONTEXT}
${ragContext}

## Your Task — Round 4: GenericConcept Selection (M2)

System under analysis: **${systemName}**
${systemInfo}
Scores: ASFID mean = ${scores.asfid_mean?.toFixed(2)}, REVOI mean = ${scores.revoi_mean?.toFixed(2)}

From the M2 GenericConcepts available in the TSCG corpus (provided in context above),
select the 4-8 most relevant concepts for modeling this system.

For each selected concept provide:
- its exact M2 name (e.g. "Attractor", "Transducer", "Cascade")
- its tensor formula (e.g. "A", "F⊗S⊗I")
- why it applies to this system (one sentence)

Also propose any relevant KnowledgeFieldConceptCombo (domain-qualified combinations).

Respond ONLY with a JSON object:
{
  "genericConcepts": [
    {
      "name": "...",
      "formula": "...",
      "rationale": "..."
    }
  ],
  "knowledgeFieldCombos": [
    {
      "name": "...",
      "formula": "...",
      "domain": "...",
      "rationale": "..."
    }
  ]
}
`,

  round5: (systemName, allRoundData, ragContext = '') => `
${TSCG_BASE_CONTEXT}
${ragContext}

## Your Task — Round 5: M0 JSON-LD Generation

Generate a complete M0 JSON-LD poclet file for **${systemName}**.

Use this TSCG data collected in previous rounds:
${JSON.stringify(allRoundData, null, 2)}

## JSON-LD Requirements

- Use @base: "https://raw.githubusercontent.com/Echopraxium/tscg/main/ontology/"
- Author: "Echopraxium with the collaboration of Claude AI"
- Include m0:asfidScore, m0:revoiScore, m0:epistemicGap, m0:spectralClass
- Reference M1 extensions as: "M1_extensions/domain_name/M1_DomainName.jsonld"
- Include m2:changelog with max 3 entries (most recent first)
- All string values in English

Respond ONLY with the JSON-LD object (no markdown fences, no explanation).
`,
};

/**
 * Build the user prompt for a given pipeline round.
 *
 * @param {number} round          1-5
 * @param {object} [context]      Round-specific data
 * @param {string} [ragContext]   Retrieved RAG chunks (from RagBuilder.retrieve())
 * @returns {{ systemPrompt: string, userPrompt: string }}
 */
function buildPrompt(round, context = {}, ragContext = '') {
  const { systemName, systemInfo, asfidScores, scores, allRoundData, userInput } = context;

  switch (round) {
    case 1:
      return {
        systemPrompt: ROUND_PROMPTS.round1(ragContext),
        userPrompt:   `Analyze this system and identify it for TSCG modeling:\n\n${userInput}`,
      };
    case 2:
      return {
        systemPrompt: ROUND_PROMPTS.round2(systemName, systemInfo, ragContext),
        userPrompt:   `Compute the ASFID scores for: ${systemName}`,
      };
    case 3:
      return {
        systemPrompt: ROUND_PROMPTS.round3(systemName, systemInfo, asfidScores, ragContext),
        userPrompt:   `Compute the REVOI scores for: ${systemName}`,
      };
    case 4:
      return {
        systemPrompt: ROUND_PROMPTS.round4(systemName, systemInfo, scores, ragContext),
        userPrompt:   `Select the most relevant M2 GenericConcepts for: ${systemName}`,
      };
    case 5:
      return {
        systemPrompt: ROUND_PROMPTS.round5(systemName, allRoundData, ragContext),
        userPrompt:   `Generate the complete M0 JSON-LD poclet for: ${systemName}`,
      };
    default:
      throw new Error(`buildPrompt: invalid round ${round} (must be 1-5)`);
  }
}

module.exports = { buildPrompt, TSCG_BASE_CONTEXT };
