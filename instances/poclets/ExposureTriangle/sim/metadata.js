/**
 * TSCG Poclet Metadata — Exposure Triangle
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Data module: mirrors M0_ExposureTriangle.jsonld for use in the renderer.
 */

'use strict';

const POCLET_METADATA = {
  id:        'M0_ExposureTriangle',
  label:     'Exposure Triangle (Photography)',
  version:   '1.1.0',
  domain:    'Photography / Optics / Image Formation',
  type:      'Poclet',
  date:      '2026-01-20',
  author:    'Echopraxium with the collaboration of Claude AI',
  reference: 'Adams (1981) — The Negative; Peterson (2016) — Understanding Exposure',

  synergy: {
    formula:          'ExposureBalance = Photography ⊙ (Balance ⊗ Trade-off)',
    compiledTensor:   'A ⊗ S ⊗ F ⊗ I ⊗ D',
    emergentProperty: 'Correct exposure — infinite combinations yield the same EV, each with different image qualities',
    empiricalLaw:     'Reciprocity law: EV = log₂(ISO/f²/t) = constant for a given scene'
  },

  asfid: { A: 0.80, S: 0.85, F: 0.95, I: 0.75, D: 0.60, mean: 0.79 },
  revoi: { R: 0.90, E: 0.70, V: 0.90, O: 0.85, I: 0.80, mean: 0.83 },
  epistemicGap:     0.32,
  epistemicGapDesc: 'Moderate gap — triangle omits scene luminance, metering, diffraction, reciprocity failure',

  primaryGenericConcepts: [
    { name: 'm2:Balance',   formula: 'A⊗S⊗F', role: 'Correct exposure: ISO × Aperture_Area × Time = constant (scene-dependent)' },
    { name: 'm2:Trade-off', formula: 'R⊗V⊗E', role: 'Cannot simultaneously maximize DoF, freeze motion and minimize noise' },
    { name: 'm2:Invariant', formula: 'S⊗A',   role: 'EV = log₂(ISO/f²/t) stays constant across equivalent settings' }
  ],

  secondaryGenericConcepts: [
    { name: 'm2:Amplification', formula: 'Ft⊗D⊗It', role: 'ISO sensor gain: each stop = 2× signal amplification' },
    { name: 'm2:FeedbackLoop',  formula: 'P⊗Al⊗H',  role: 'Camera metering: negative feedback loop correcting toward target EV' },
    { name: 'm2:Threshold',     formula: 'A⊗I',      role: '1/focal_length rule (shake), ISO≥1600 (noise), f/16+ (diffraction)' },
    { name: 'm2:Regulation',    formula: 'A⊗S⊗F',   role: 'Auto-exposure modes (Av, Tv, P) maintain target EV' },
    { name: 'm2:Polarity',      formula: 'S⊗I⊗A',   role: 'Stops scale: +EV=over, 0=correct, -EV=under' },
    { name: 'm2:Transformation',formula: 'D⊗I⊗S',   role: 'Equivalent settings: ISO400/f4/1/250 ↔ ISO800/f5.6/1/250' },
    { name: 'm2:Component',     formula: 'S⊗I',      role: 'ISO, Aperture, Shutter as distinct elementary parameters' },
    { name: 'm2:Signal',        formula: 'I⊗F',      role: 'Photon flux as information carrier (scene luminance, color, spatial data)' }
  ],

  // Three poles — the vertices of the Exposure Triangle
  // COMP [0,1]: always 0=min light contribution, 1=max light contribution
  poles: [
    {
      id:           'iso',
      label:        'ISO',
      sublabel:     'Sensor Gain / Sensitivity',
      emoji:        '🎮',
      color:        '#50d2d2',
      description:  'Amplifies the electrical signal from photons. Higher ISO = brighter image in low light, but more grain/noise. Each stop = 2× gain. Digital cameras adjust per frame; film is fixed per roll.',
      tradeoff:     'Sensitivity ↔ Image Quality (grain/noise)',
      examples:     'ISO 100: bright sunlight (clean) · ISO 400: overcast · ISO 1600: indoor · ISO 6400: concert/astro',
      compMin:      100,    // COMP=0
      compMax:      6400,   // COMP=1
      baselineComp: 0.333,  // ISO 400
      asfid: { A: 0.75, S: 0.80, F: 0.85, I: 0.90, D: 0.60 }
    },
    {
      id:           'aperture',
      label:        'Aperture',
      sublabel:     'f-number / Lens Opening',
      emoji:        '🔬',
      color:        '#ffaf2d',
      description:  'Controls light flux entering the lens (Area ∝ 1/f²). Wider aperture (lower f-number) = more light + shallow depth of field. Narrow = less light + deep focus. Full stops: f/1.4, f/2, f/2.8, f/4, f/5.6, f/8, f/11, f/16, f/22.',
      tradeoff:     'Light gathering (wide) ↔ Depth of Field (narrow)',
      examples:     'f/1.4: portrait bokeh · f/5.6: street · f/11: landscape · f/22: macro (max DoF)',
      compMin:      22,     // COMP=0 → f/22 (narrow, dark)
      compMax:      1.4,    // COMP=1 → f/1.4 (wide, bright)
      baselineComp: 0.497,  // f/5.6
      asfid: { A: 0.80, S: 0.90, F: 0.95, I: 0.75, D: 0.55 }
    },
    {
      id:           'shutter',
      label:        'Shutter',
      sublabel:     'Exposure Time / Duration',
      emoji:        '⏱',
      color:        '#c86eff',
      description:  'Duration the sensor is exposed to light (temporal integration). Fast shutter freezes motion. Slow shutter accumulates light but introduces motion blur and camera shake. Rule: min speed = 1/focal_length.',
      tradeoff:     'Motion freeze (fast) ↔ Light gathering (slow)',
      examples:     '1/8000s: hummingbird · 1/250s: general · 1/30s: handheld limit · 20s: Milky Way',
      compMin:      1/4000, // COMP=0 → 1/4000s (fast, dark)
      compMax:      30,     // COMP=1 → 30s (slow, bright)
      baselineComp: 0.237,  // 1/250s
      asfid: { A: 0.80, S: 0.75, F: 0.95, I: 0.70, D: 0.85 }
    }
  ],

  // Presets — each designed to achieve EV ≈ 0 with a specific trade-off emphasis
  presets: [
    { id:'portrait',  label:'👤 Portrait',  iso:400,   f:2.8,  t:1/1000, note:'Wide aperture → shallow DoF. Fast shutter freezes subtle motion.' },
    { id:'landscape', label:'🏔 Landscape', iso:100,   f:11,   t:1/16,   note:'Narrow aperture → deep DoF. Low ISO for cleanest image. Tripod required.' },
    { id:'sport',     label:'🏃 Sport',     iso:1600,  f:4,    t:1/2000, note:'Fast shutter freezes action. Accept higher ISO noise.' },
    { id:'astro',     label:'🌌 Astro',     iso:3200,  f:2.8,  t:20,     note:'Wide + high ISO + very long shutter for dark sky. High EV offset vs daylight.' }
  ]
};

if (typeof module !== 'undefined') module.exports = { POCLET_METADATA };
