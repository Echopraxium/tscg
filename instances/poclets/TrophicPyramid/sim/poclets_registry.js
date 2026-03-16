/**
 * TSCG Poclet Registry
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Central index of all simulations available in the TSCG repository.
 * Place this file at the ROOT of the tscg/ repository.
 * The Poclet Explorer reads this file to populate its list.
 *
 * Path convention: relative to the tscg/ repository root.
 * Status values: 'ACTIVE' | 'WIP' | 'PLANNED'
 */

'use strict';

const POCLETS_REGISTRY = [

  // ── Poclets ────────────────────────────────────────────────────
  {
    id:       'trophic-pyramid',
    label:    'Trophic Pyramid',
    type:     'Poclet',
    domain:   'Ecology / Biology',
    engine:   'BabylonJS 3D',
    synergy:  'StratifiedDissipation = Biology ⊙ (Layer ⊗ Dissipation)',
    asfid:    { A:0.95, S:0.90, F:0.95, I:0.80, D:0.85, mean:0.89 },
    revoi:    { R:0.95, E:0.70, V:0.90, O:0.80, I:0.85, mean:0.84 },
    delta:    0.05,
    path:     'instances/poclets/trophic-pyramid/sim',
    version:  '1.0.0',
    status:   'ACTIVE',
    desc:     '5-level trophic pyramid with StratifiedDissipation combo. 3D BabylonJS simulation with trophic cascade scenario.'
  },
  {
    id:       'phase-transition',
    label:    'Phase Transition',
    type:     'Poclet',
    domain:   'Physics / Thermodynamics',
    engine:   'P5.js (pending migration)',
    synergy:  'OrderDisorderTransition = Physics ⊙ (Bifurcation ⊗ Threshold)',
    asfid:    { A:0.90, S:0.85, F:0.85, I:0.75, D:0.95, mean:0.86 },
    revoi:    { R:0.90, E:0.75, V:0.95, O:0.85, I:0.80, mean:0.85 },
    delta:    0.01,
    path:     'instances/poclets/phase-transition/sim',
    version:  '1.0.0',
    status:   'WIP',
    desc:     'Phase transitions (solid/liquid/gas) modelled as Bifurcation events at thermodynamic thresholds.'
  },
  {
    id:       'vco',
    label:    'Voltage-Controlled Oscillator',
    type:     'Poclet',
    domain:   'Electronics',
    engine:   'P5.js (pending migration)',
    synergy:  'ControlledOscillation = Electronics ⊙ (Oscillator ⊗ Regulation)',
    asfid:    { A:0.90, S:0.80, F:0.95, I:0.85, D:0.90, mean:0.88 },
    revoi:    { R:0.90, E:0.80, V:0.95, O:0.90, I:0.85, mean:0.88 },
    delta:    0.00,
    path:     'instances/poclets/vco/sim',
    version:  '1.0.0',
    status:   'WIP',
    desc:     'VCO oscilloscope simulation. Frequency modulated by control voltage. Validates Oscillator TransDisclet candidate.'
  },
  {
    id:       'raas',
    label:    'RAAS — Renin-Angiotensin-Aldosterone',
    type:     'Poclet',
    domain:   'Biology / Endocrinology',
    engine:   'Planned',
    synergy:  'Cascade = ⊗⇒(Process, Step, Trajectory)',
    asfid:    { A:0.90, S:0.80, F:0.70, I:0.80, D:0.90, mean:0.82 },
    revoi:    { R:0.90, E:0.80, V:0.70, O:0.90, I:0.80, mean:0.86 },
    delta:    0.04,
    path:     'instances/poclets/raas/sim',
    version:  '1.0.0',
    status:   'PLANNED',
    desc:     'Hormonal cascade regulating blood pressure. First poclet demonstrating complete 5D ASFID coverage.'
  },
  {
    id:       'butterfly-metamorphosis',
    label:    'Butterfly Metamorphosis',
    type:     'Poclet',
    domain:   'Biology / Developmental Biology',
    engine:   'Planned',
    synergy:  'HolometabolousTransformation = Biology ⊙ (Bifurcation ⊗ Process)',
    asfid:    { A:0.95, S:0.98, F:0.95, I:0.90, D:0.85, mean:0.95 },
    revoi:    { R:0.90, E:0.75, V:0.85, O:0.80, I:0.85, mean:0.88 },
    delta:    0.07,
    path:     'instances/poclets/butterfly-metamorphosis/sim',
    version:  '1.0.0',
    status:   'PLANNED',
    desc:     '6-pole model of holometabolous lifecycle from egg to imago. Complete structural reorganisation via Bifurcation.'
  },
  {
    id:       'kindleberger-minsky',
    label:    'Kindleberger-Minsky Cycle',
    type:     'Poclet',
    domain:   'Finance / Economics',
    engine:   'Planned',
    synergy:  'SpeculativeCycle = Economics ⊙ (Propagation ⊗ Narration)',
    asfid:    { A:0.75, S:0.70, F:0.85, I:0.80, D:0.90, mean:0.80 },
    revoi:    { R:0.80, E:0.60, V:0.55, O:0.70, I:0.75, mean:0.68 },
    delta:    0.12,
    path:     'instances/poclets/kindleberger-minsky/sim',
    version:  '1.0.0',
    status:   'PLANNED',
    desc:     '5-phase speculative cycle (Displacement → Boom → Euphoria → Distress → Revulsion). M1_Economics.jsonld.'
  },
  {
    id:       'yggdrasil',
    label:    'Yggdrasil — Norse Cosmology',
    type:     'Poclet',
    domain:   'Mythology / Comparative Religion',
    engine:   'Planned',
    synergy:  'CyclicCosmology = Mythology ⊙ (CyclicTension ⊗ CatastrophicBifurcation)',
    asfid:    { A:0.85, S:0.90, F:0.75, I:0.90, D:0.80, mean:0.84 },
    revoi:    { R:0.85, E:0.65, V:0.60, O:0.75, I:0.80, mean:0.73 },
    delta:    0.11,
    path:     'instances/poclets/yggdrasil/sim',
    version:  '2.0.0',
    status:   'PLANNED',
    desc:     'Norse cosmology: 7-pole multipolar network (9 worlds) with Ragnarök CatastrophicBifurcation. M1_Mythology.jsonld.'
  },

  // ── TSCG Tools ─────────────────────────────────────────────────
  {
    id:       'tscg-explorer',
    label:    'TSCG Explorer',
    type:     'TscgTool',
    domain:   'TSCG Framework',
    engine:   'Pygame (pending migration)',
    synergy:  'Reflexive meta-tool — models itself via m3:TscgTool',
    asfid:    null,
    revoi:    null,
    delta:    null,
    path:     'instances/tscg-tools/tscg-explorer/sim',
    version:  '1.0.0',
    status:   'WIP',
    desc:     'Interactive 2D network visualisation of the 81 M2 GenericConcepts with IS-A tree, concept profiles, and 3 projection modes.'
  }
];

if (typeof module !== 'undefined') module.exports = { POCLETS_REGISTRY };
