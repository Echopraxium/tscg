/**
 * TSCG Poclet Metadata — Fire Triangle
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Data module: mirrors M0_FireTriangle.jsonld for use in the renderer.
 * Each simulation has its own metadata.js — the renderer.js reads this.
 */

'use strict';

const POCLET_METADATA = {
  id:        'M0_FireTriangle',
  label:     'Fire Triangle',
  version:   '1.0.0',
  domain:    'Chemistry / Physics',
  type:      'Poclet',
  date:      '2026-03-15',
  author:    'Echopraxium with the collaboration of Claude AI',
  reference: 'Lavoisier (1777) — Combustion theory; Fire Triangle (classical ternary model)',

  synergy: {
    formula:           'CombustionEquilibrium = Chemistry \u2299 (Balance \u2297 Threshold)',
    compiledTensor:    'A \u2297 S \u2297 F \u2297 I \u2297 D',
    emergentProperty:  'Self-sustaining exothermic reaction \u2014 fire exists only as the synergy of three co-present conditions',
    empiricalLaw:      'Extinction law: removing any one component immediately terminates combustion'
  },

  asfid: { A: 0.90, S: 0.85, F: 0.85, I: 0.80, D: 0.90, mean: 0.86 },
  revoi: { R: 0.90, E: 0.70, V: 0.95, O: 0.85, I: 0.85, mean: 0.85 },
  epistemicGap:     0.01,
  epistemicGapDesc: 'Near-zero gap \u2014 the Fire Triangle is an almost perfect Map of combustion Territory',

  primaryGenericConcepts: [
    { name: 'm2:Balance',   formula: 'A\u2297S\u2297I',   role: 'Ternary equilibrium \u2014 all 3 components must co-exist above threshold' },
    { name: 'm2:Threshold', formula: 'A\u2297I\u2297F',   role: 'Each component has a minimum viable value (ignition threshold)' },
    { name: 'm2:Synergy',   formula: 'I\u2297S\u2297D',   role: 'Fire emerges only from the co-presence of all 3 \u2014 not from any subset' }
  ],

  secondaryGenericConcepts: [
    { name: 'm2:Flow',           formula: 'F',                 role: 'Heat transfer + mass flow (fuel vapour, O\u2082) to reaction zone' },
    { name: 'm2:Dissipation',    formula: 'F\u2297D',          role: '~70% of combustion energy lost as thermal radiation + convection' },
    { name: 'm2:Regulation',     formula: 'A\u2297S\u2297F',   role: 'Positive feedback: heat \u2192 pyrolysis \u2192 more fuel vapour \u2192 more heat' },
    { name: 'm2:Cascade',        formula: '\u2297\u21d2(P,St,Tr)', role: 'Fire spread as spatial cascade (wildfire dynamics)' },
    { name: 'm2:Transformation', formula: 'S\u2297D',          role: 'Fuel \u2192 CO\u2082 + H\u2082O + \u0394H (irreversible chemical transformation)' },
    { name: 'm2:Context',        formula: 'O\u2297R\u2297Im\u2297E', role: 'Environment (humidity, altitude, fuel type) conditions combustion' }
  ],

  // Ternary poles — the three vertices of the Fire Triangle
  poles: [
    {
      id:               'heat',
      label:            'Heat',
      sublabel:         'Activation Energy',
      emoji:            '\uD83D\uDD25',
      color:            '#f78166',
      threshold:        0.25,
      defaultValue:     0.65,
      extinctionMethod: 'Cooling \u2014 water spray, CO\u2082 extinguisher, heat-absorbing powder',
      description:      'Ignition source providing the activation energy to initiate the oxidation chain reaction. Sources: spark, friction, pilot flame. Minimum = ignition temperature of the specific fuel (wood ~300\u00b0C, methane ~580\u00b0C).',
      asfid: { A: 0.90, S: 0.75, F: 0.85, I: 0.90, D: 0.95 }
    },
    {
      id:               'fuel',
      label:            'Fuel',
      sublabel:         'Combustible Matter',
      emoji:            '\uD83E\uDEB5',
      color:            '#56d364',
      threshold:        0.30,
      defaultValue:     0.75,
      extinctionMethod: 'Fuel removal \u2014 fire breaks, closing gas valve, clearing brush',
      description:      'Reducing agent providing carbon-hydrogen bonds for oxidation. Must exceed stoichiometric minimum. Sources: cellulose, hydrocarbons, metals. Extinction: fuel starvation (fire breaks, gas valve closure, water curtain).',
      asfid: { A: 0.85, S: 0.90, F: 0.90, I: 0.75, D: 0.85 }
    },
    {
      id:               'oxygen',
      label:            'O\u2082',
      sublabel:         'Oxidizer',
      emoji:            '\uD83D\uDCA8',
      color:            '#79c0ff',
      threshold:        0.16,
      defaultValue:     0.70,
      extinctionMethod: 'Smothering \u2014 CO\u2082 extinguisher, foam, fire blanket (O\u2082 exclusion)',
      description:      'Atmospheric oxidizer (O\u2082 \u2265 16% required). Accepts electrons in the redox reaction. Standard air: 21% O\u2082. Fire smothers at <16%. Extinction: CO\u2082 blanket, foam, fire blanket \u2014 all displace O\u2082 below threshold.',
      asfid: { A: 0.90, S: 0.85, F: 0.85, I: 0.80, D: 0.85 }
    }
  ]
};

// Export for Node.js (Electron renderer with nodeIntegration)
if (typeof module !== 'undefined') module.exports = { POCLET_METADATA };
