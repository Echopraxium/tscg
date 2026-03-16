/**
 * TSCG Poclet Metadata — Trophic Pyramid
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Data module: mirrors M0_TrophicPyramid.jsonld for use in the renderer.
 * Each simulation has its own metadata.js — the renderer.js reads this.
 */

'use strict';

const POCLET_METADATA = {
  id: 'M0_TrophicPyramid',
  label: 'Trophic Pyramid',
  version: '1.0.0',
  domain: 'Ecology / Biology',
  type: 'Poclet',
  date: '2026-03-13',
  author: 'Echopraxium with the collaboration of Claude AI',
  reference: 'Lindeman (1942) — The Trophic-Dynamic Aspect of Ecology',

  synergy: {
    formula: 'StratifiedDissipation = Biology ⊙ (Layer ⊗ Dissipation)',
    compiledTensor: 'S ⊗ I ⊗ A ⊗ R ⊗ F ⊗ D',
    emergentProperty: 'Pyramidal biomass structure — universal conical shape of ecosystems',
    empiricalLaw: "Lindeman's 10% rule: η ≈ 0.1 at each trophic boundary"
  },

  asfid: { A: 0.95, S: 0.90, F: 0.95, I: 0.80, D: 0.85, mean: 0.89 },
  revoi: { R: 0.95, E: 0.70, V: 0.90, O: 0.80, I: 0.85, mean: 0.84 },
  epistemicGap: 0.05,
  epistemicGapDesc: 'Exceptionally low — one of ecology\'s best-characterised laws',

  primaryGenericConcepts: [
    { name: 'm2:Layer',       formula: 'S⊗I⊗A⊗R', role: 'Structural backbone — each trophic level IS a Layer' },
    { name: 'm2:Dissipation', formula: 'F⊗D',       role: '~90% energy lost at each trophic boundary' },
    { name: 'm2:Context',     formula: 'O⊗R⊗Im⊗E',  role: 'Biome determines which species fill each Level' }
  ],

  secondaryGenericConcepts: [
    { name: 'm2:Hierarchy',   formula: 'A⊗S',         role: 'Positional ordering base→apex' },
    { name: 'm2:Flow',        formula: 'F',            role: 'Energy/biomass transfer between levels' },
    { name: 'm2:Gradient',    formula: '⊗₂F',          role: 'Energy density gradient from base to apex' },
    { name: 'm2:Homeostasis', formula: 'A⊗S⊗F⊗I⊗D',  role: 'Ecosystem equilibrium' },
    { name: 'm2:Regulation',  formula: 'A⊗S⊗F',       role: 'Predator-prey feedback loops' },
    { name: 'm2:Cascade',     formula: '⊗⇒(P,St,Tr)', role: 'Trophic cascade: apex removal → destabilisation' },
    { name: 'm2:Threshold',   formula: 'A⊗I⊗F',       role: 'Minimum viable population triggers' },
    { name: 'm2:Network',     formula: 'S⊗F⊗I',       role: 'Food web underlying the pyramid' },
    { name: 'm2:Emergence',   formula: '—',            role: 'Ecosystem services from level interactions' }
  ],

  // Trophic levels — simulation poles
  levels: [
    {
      id: 'decomposers',
      rank: 0,
      label: 'Decomposers',
      sublabel: 'Saprotrophs / Detritivores',
      organisms: 'Fungi, Bacteria, Earthworms',
      energyKj: 4000,       // cross-cutting channel (~40% of flux)
      biomassRelative: 0.3,  // relative display unit (not trophic biomass)
      color: '#6e7681',
      colorDark: '#3d444f',
      isDecomposer: true,
      asfid: { A: 0.80, S: 0.85, F: 0.95, I: 0.85, D: 0.90 },
      role: 'Nutrient recycling — completes biogeochemical cycle',
      info: 'Cross-cutting: receive detritus from ALL levels. Return inorganic nutrients (N, P, K) to soil/water. ~40–60% of all ecosystem energy passes through the decomposer channel.'
    },
    {
      id: 'producers',
      rank: 1,
      label: 'Primary Producers',
      sublabel: 'Autotrophs',
      organisms: 'Plants, Phytoplankton, Algae',
      energyKj: 10000,
      biomassRelative: 10,
      color: '#56d364',
      colorDark: '#1f6331',
      isDecomposer: false,
      asfid: { A: 0.95, S: 0.95, F: 0.85, I: 0.75, D: 0.70 },
      role: 'Solar energy capture (photosynthesis)',
      info: 'Capture ~1–2% of incident solar radiation. Provide the entire energetic base of the pyramid. Biomass ≈ 99% of ecosystem total (terrestrial). Basis of Layer rank = 1.'
    },
    {
      id: 'herbivores',
      rank: 2,
      label: 'Primary Consumers',
      sublabel: 'Herbivores',
      organisms: 'Insects, Ungulates, Zooplankton',
      energyKj: 1000,
      biomassRelative: 5,
      color: '#79c0ff',
      colorDark: '#1b3a5c',
      isDecomposer: false,
      asfid: { A: 0.90, S: 0.85, F: 0.90, I: 0.80, D: 0.85 },
      role: 'Primary biomass consumers',
      info: 'Receive 10% of producer energy. ~90% lost as heat + faeces. Regulated top-down by Level 3 carnivores. Herbivore irruption occurs when Level 3 is removed (trophic cascade).'
    },
    {
      id: 'carnivores',
      rank: 3,
      label: 'Secondary Consumers',
      sublabel: 'Carnivores / Omnivores',
      organisms: 'Foxes, Snakes, Predatory Fish',
      energyKj: 100,
      biomassRelative: 2,
      color: '#d2a8ff',
      colorDark: '#3d1f6b',
      isDecomposer: false,
      asfid: { A: 0.90, S: 0.80, F: 0.85, I: 0.85, D: 0.90 },
      role: 'Mesopredator regulation',
      info: 'Receive 10% of herbivore energy. Regulate Level 2 populations via predation pressure. Released from apex control during trophic cascade → irruption → herbivore collapse.'
    },
    {
      id: 'apex',
      rank: 4,
      label: 'Apex Predators',
      sublabel: 'Tertiary Consumers',
      organisms: 'Wolves, Sharks, Eagles',
      energyKj: 10,
      biomassRelative: 0.8,
      color: '#f78166',
      colorDark: '#6b1f1f',
      isDecomposer: false,
      asfid: { A: 0.95, S: 0.75, F: 0.75, I: 0.90, D: 0.95 },
      role: 'Keystone species — top-down ecosystem control',
      info: 'Only 10 kJ/m²/yr available. Smallest biomass — energetically barely sustainable. Removal triggers full trophic cascade. Empirical example: wolves in Yellowstone (1995) — changed river courses.'
    }
  ]
};

// Export for Node.js (Electron renderer with nodeIntegration)
if (typeof module !== 'undefined') module.exports = { POCLET_METADATA };
