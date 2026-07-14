// ──────────────────────────────────────────────────────────────
// Butterfly Metamorphosis Poclet — Simulation Data
// Author: Echopraxium with the collaboration of Claude AI
// Framework: TSCG (Transdisciplinary System Construction Game)
//
// Design: generic 6-pole "trunk" (shared parametric keyframes)
//         + per-species overlay (palette, morphology flags, durations).
// This keeps the model DRY: an egg is an egg across species; only
// colour + a few distinctive geometric traits vary.
// ──────────────────────────────────────────────────────────────

(function (global) {
  'use strict';

  // ═══ 1. GENERIC POLES (shared trunk) ═══
  // Each pole is a parametric vector. The morph = interpolation of
  // these vectors between adjacent poles. Fields:
  //   bodyLength  : Z extent of the segmented body
  //   bodyRadius  : base segment radius
  //   taper       : 0 = sausage, 1 = strongly tapered ends
  //   legLen      : 0 hidden .. 1 full articulated legs
  //   wingExtent  : 0 no wings .. 1 fully deployed (grows like embryonic wings)
  //   antenna     : 0 hidden .. 1 full antennae
  //   chrysalisA  : chrysalis shell opacity (0 = no shell, >0 = visible/translucent)
  //   headSize    : head sphere scale
  //   form        : semantic tag (for idle-animation dispatch)
  const POLES = [
    { key: 'egg',       label: 'Egg',              bodyLength: 0.70, bodyRadius: 0.46, taper: 0.10, legLen: 0.00, wingExtent: 0.00, antenna: 0.00, chrysalisA: 0.00, headSize: 0.0, form: 'egg' },
    { key: 'larva',     label: 'Larva',            bodyLength: 3.40, bodyRadius: 0.34, taper: 0.12, legLen: 0.45, wingExtent: 0.00, antenna: 0.12, chrysalisA: 0.00, headSize: 1.1, form: 'larva' },
    { key: 'prepupa',   label: 'Pre-Pupa',         bodyLength: 2.00, bodyRadius: 0.50, taper: 0.45, legLen: 0.10, wingExtent: 0.00, antenna: 0.00, chrysalisA: 0.35, headSize: 0.6, form: 'prepupa' },
    { key: 'pupa',      label: 'Pupa (Chrysalis)', bodyLength: 1.65, bodyRadius: 0.55, taper: 0.60, legLen: 0.00, wingExtent: 0.20, antenna: 0.10, chrysalisA: 0.52, headSize: 0.5, form: 'pupa' },
    { key: 'emergence', label: 'Emergence',        bodyLength: 1.80, bodyRadius: 0.40, taper: 0.55, legLen: 0.60, wingExtent: 0.62, antenna: 0.70, chrysalisA: 0.12, headSize: 0.9, form: 'emergence' },
    { key: 'imago',     label: 'Imago',            bodyLength: 1.70, bodyRadius: 0.32, taper: 0.58, legLen: 0.95, wingExtent: 1.00, antenna: 1.00, chrysalisA: 0.00, headSize: 1.0, form: 'imago' }
  ];

  // ═══ 2. SPECIES OVERLAY ═══
  // Each species reuses the generic poles; it only overrides colours,
  // a handful of geometric flags, wingspan scale, and stage durations.
  const SPECIES = {
    monarch: {
      id: 'monarch',
      common: 'Monarch',
      latin: 'Danaus plexippus',
      hostPlant: 'Milkweed (Asclepias)',
      wingspanScale: 1.00,
      flags: { wingTails: false, eyespots: false, iridescent: false, chrysalisGoldSpots: true, caterpillarFilaments: true, caterpillarHorn: false },
      palette: {
        egg: '#f4e7a1', caterpillar: '#f4d03f', caterpillarBand: '#1c1c1c',
        body: '#2b1a0f', wingPrimary: '#e07b1a', wingVein: '#1a1a1a', wingSpot: '#fefefe',
        chrysalis: '#3f7d4e', chrysalisAccent: '#ffd23f'
      },
      durations: { egg: 4, larva: 24, prepupa: 1.5, pupa: 12, emergence: 0.15, imago: 30 }
    },
    swallowtail: {
      id: 'swallowtail',
      common: 'Old World Swallowtail',
      latin: 'Papilio machaon',
      hostPlant: 'Fennel, carrot (Apiaceae)',
      wingspanScale: 1.05,
      flags: { wingTails: true, eyespots: false, iridescent: false, chrysalisGoldSpots: false, caterpillarFilaments: false, caterpillarHorn: true },
      palette: {
        egg: '#e9e2c4', caterpillar: '#7bc36a', caterpillarBand: '#1c1c1c',
        body: '#241d10', wingPrimary: '#f2c200', wingVein: '#101010', wingSpot: '#2a5cff',
        chrysalis: '#8a8f5c', chrysalisAccent: '#5b6b34'
      },
      durations: { egg: 6, larva: 28, prepupa: 2, pupa: 15, emergence: 0.15, imago: 28 }
    },
    morpho: {
      id: 'morpho',
      common: 'Blue Morpho',
      latin: 'Morpho peleides',
      hostPlant: 'Fabaceae (legumes)',
      wingspanScale: 1.35,
      flags: { wingTails: false, eyespots: false, iridescent: true, chrysalisGoldSpots: false, caterpillarFilaments: true, caterpillarHorn: false },
      palette: {
        egg: '#dce6c8', caterpillar: '#b5532e', caterpillarBand: '#e8d24a',
        body: '#0e0f1a', wingPrimary: '#2b6bff', wingVein: '#0a1030', wingSpot: '#8fb4ff',
        chrysalis: '#9ad1b0', chrysalisAccent: '#4c8f6a'
      },
      durations: { egg: 7, larva: 30, prepupa: 2, pupa: 14, emergence: 0.15, imago: 40 }
    },
    peacock: {
      id: 'peacock',
      common: 'European Peacock',
      latin: 'Aglais io',
      hostPlant: 'Stinging nettle (Urtica)',
      wingspanScale: 0.95,
      flags: { wingTails: false, eyespots: true, iridescent: false, chrysalisGoldSpots: true, caterpillarFilaments: false, caterpillarHorn: false },
      palette: {
        egg: '#cdd98f', caterpillar: '#1c1c1c', caterpillarBand: '#e6e6e6',
        body: '#2a0f12', wingPrimary: '#b3232a', wingVein: '#2a0d10', wingSpot: '#2f6fb0',
        chrysalis: '#7d7a5a', chrysalisAccent: '#c9b24a'
      },
      durations: { egg: 5, larva: 26, prepupa: 1.5, pupa: 13, emergence: 0.15, imago: 32 }
    },
    paintedlady: {
      id: 'paintedlady',
      common: 'Painted Lady',
      latin: 'Vanessa cardui',
      hostPlant: 'Thistle, mallow',
      wingspanScale: 0.82,
      flags: { wingTails: false, eyespots: false, iridescent: false, chrysalisGoldSpots: true, caterpillarFilaments: false, caterpillarHorn: false },
      palette: {
        egg: '#d6e0a8', caterpillar: '#6b5a34', caterpillarBand: '#d9c56a',
        body: '#3a2410', wingPrimary: '#d98a2b', wingVein: '#241206', wingSpot: '#ffffff',
        chrysalis: '#8a7d63', chrysalisAccent: '#b8a05a'
      },
      durations: { egg: 4, larva: 21, prepupa: 1, pupa: 10, emergence: 0.15, imago: 21 }
    }
  };

  const SPECIES_ORDER = ['monarch', 'swallowtail', 'morpho', 'peacock', 'paintedlady'];

  // ═══ 3. TSCG ONTOLOGY METADATA (from M0_ButterflyMetamorphosis.jsonld) ═══
  const META = {
    title: 'Butterfly Metamorphosis — Complete Holometabolous Lifecycle',
    version: '1.1.1',
    domain: 'M1_Biology / Developmental Biology',
    status: 'VALIDATED',
    description:
      'Six-pole model of butterfly metamorphosis from egg to adult imago, ' +
      'including the critical emergence phase that distinguishes complete ' +
      'metamorphosis from simpler 5-pole developmental processes. The chrysalis ' +
      'is not a single state but spans three poles: it forms at the Pre-Pupa, ' +
      'transforms internally at the Pupa (histolysis / histogenesis from imaginal ' +
      'discs), and splits open at Emergence.',
    asfid: { A: 0.95, S: 0.98, F: 0.92, I: 0.96, D: 0.94, mean: 0.95 },
    // REVOI (Sphinx Eye / Map) per M2 v16.16.0 = Representability, Evolvability,
    // Verifiability, Observability, Interoperability. NOTE: values PROVISIONAL —
    // re-derived onto the new axes (old ORIVE Validity/Expressiveness/Reproducibility
    // were obsolete), pending Michel's validation (Phase 4).
    revoi: { R: 0.90, E: 0.74, V: 0.92, O: 0.85, Im: 0.78, mean: 0.84 },
    epistemicGap: 0.22, // provisional — recompute δ₁ after REVOI values are fixed
    m2: [
      { name: 'Transformation',   formula: 'D × S × I',       dominance: 0.96, note: 'Irreversible change of structure, function and identity.' },
      { name: 'Emergence',        formula: 'I × S × D',       dominance: 0.94, note: 'Adult structures emerge from imaginal discs.' },
      { name: 'Regulation',       formula: 'A × S × F',       dominance: 0.93, note: 'JH / Ecdysone hormonal cascade controls transitions.' },
      { name: 'Behavior',         formula: 'S × D × F',       dominance: 0.92, note: 'Ordered network of Steps (the 6 poles). M2 discoveryContext cites butterfly metamorphosis.' },
      { name: 'Threshold',        formula: 'A × I',           dominance: 0.89, note: 'Hormonal thresholds trigger all-or-nothing commitment (ex-Switch).' },
      { name: 'Layer',            formula: 'St × It × A | R', dominance: 0.87, note: 'Nested levels: molecular -> cellular -> tissue -> organism.' },
      { name: 'Step',             formula: 'S × I × D',       dominance: 0.86, note: 'Each pole is a Step. M2 example: "Butterfly egg stage".' },
      { name: 'Stase',            formula: 'S × A',           dominance: 0.82, note: 'Imaginal discs dormant, reversible (replaces candidate Latency).' },
      { name: 'Potentialization', formula: 'A × D × F | _^',  dominance: 0.80, note: 'Activation of dormant discs at emergence (replaces candidate Latency).' },
      { name: 'Memory',           formula: '∫(D−F)dτ',        dominance: 0.75, note: 'Larval learning retained through CNS continuity.' }
    ]
  };

  global.TSCG_BUTTERFLY = { POLES: POLES, SPECIES: SPECIES, SPECIES_ORDER: SPECIES_ORDER, META: META };

})(window);
