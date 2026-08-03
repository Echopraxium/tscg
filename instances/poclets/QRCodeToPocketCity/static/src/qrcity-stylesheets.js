/* ══════════════════════════════════════════════════════════════
   QRCodeToPocketCity — STYLE LAYER
   Author: Echopraxium with the collaboration of Claude AI
   Version: 1.0.0

   Declarative stylesheet registry. Following the CanopyGraphViz
   convention, STYLE is a separate file from CORE and holds every
   appearance value AND every generation rule.

   A stylesheet is NOT a colour theme. Its `rules` block drives
   geometry — heights, arch budget, fenestration density, sign
   frequency — so switching stylesheet re-interprets the same seed
   into a different city. Layout is a style channel.

   Schema
   ──────
   sky, fog          scene background, optional exponential fog
   light             ambient + sun + fill
   ground/plate/roof flat surfaces (roof also drives chimney caps)
   facade.flat[]     opaque facade colours
   facade.brick[]    procedural brick specs   (or [] to disable)
   facade.stone[]    procedural stone specs   (or [])
   facade.glass[]    procedural curtain walls (or [])
   window            lit/dark colours + emissive
   chimney/door/frame/step   detail colours
   landmark          finder-pattern colours + civic names
   logo              corporate sign palette + size ratio
   inverted          full palette override for inverted polarity
   rules             GEOMETRY: heights, densities, arch and sign budget
   ══════════════════════════════════════════════════════════════ */
'use strict';

const QRCITY_STYLESHEETS = {

  /* ── Daylight: neutral reference. Plaster, concrete, brick, stone ── */
  daylight: {
    name: 'Daylight',
    sky:  '#7eb8d4',
    fog:  null,
    light: {
      ambient: { color: '#ffffff', intensity: 0.66 },
      sun:     { color: '#fff8e0', intensity: 0.92, dir: [-0.35, -0.85, -0.28] },
      fill:    { color: '#d0e8ff', intensity: 0.30, dir: [ 0.45, -0.55,  0.40] }
    },
    ground: '#f1f3f6',
    plate:  '#14171c',
    roof:   '#14171c',
    surround: { color:'#b9c4cc' },
    facade: {
      flat: ['#aaafb6','#999ea5','#868b93','#b6ab99',
             '#9f9688','#c4b089','#af9a72','#ccc3b4'],
      brick: [
        { brick:'#a86f59', mortar:'#cec5b6', jitter:0.22, seed:0x5EED01 },
        { brick:'#8d6857', mortar:'#bfb4a6', jitter:0.20, seed:0x5EED02 }
      ],
      stone: [
        { stone:'#bbb6aa', mortar:'#9e998e', jitter:0.18, seed:0x570E01 },
        { stone:'#aaa59a', mortar:'#8f8b81', jitter:0.20, seed:0x570E02 },
        { stone:'#cbc5b9', mortar:'#aaa59a', jitter:0.16, seed:0x570E03 }
      ],
      glass: [
        { tint:'#7c98ad', mullion:'#46525e', litTint:'#fff6dc', litProb:0.22, seed:0x5EED11 },
        { tint:'#6a8a9a', mullion:'#46525e', litTint:'#fff6dc', litProb:0.22, seed:0x5EED12 },
        { tint:'#88a8bb', mullion:'#46525e', litTint:'#fff6dc', litProb:0.22, seed:0x5EED13 }
      ]
    },
    window:  { lit:'#fef3c7', litGlow:'#6b4800', glow:0.70, dark:'#1e293b' },
    chimney: '#c9cdd4',
    door:    '#5b3410',
    frame:   '#c9cdd4',
    step:    '#b0b8c4',
    landmark: {
      colors: ['#dc2626','#1d4ed8','#16a34a','#7c3aed','#d97706'],
      names:  ['Town Hall','University','Hospital','Market Hall','Library']
    },
    logo: {
      size: 0.75,
      palette: ['#c0392b','#1f4e79','#1d7a4c','#2c3e50',
                '#d68910','#7d3c98','#f4f6f7','#17202a']
    },
    inverted: {
      ground: '#1c6b33',
      plate:  '#ffffff',
      roof:   '#ffffff',
      facadeFlat: ['#d9a05b','#c98d4a','#e2b878','#b87a3e',
                   '#d4a267','#c08850','#eac68f','#a96f38'],
      chimney:'#b8b4ab', door:'#4a2410', frame:'#ffffff', step:'#cfcbc2'
    },
    rules: {
      height:       { min:0.6, max:4.4 },
      landmarkKeep: { min:3.0, max:5.2 },
      landmarkRing: { min:1.2, max:2.0 },
      glassProb:0.28, glassMinHeight:3.0, landmarkGlassProb:0.30,
      windowsPerFace:{ min:2, max:3 },
      windowAbsentProb:0.15, windowLitProb:0.55, bayProb:0.20,
      chimneyMax:3, landmarkChimneyProb:0.55,
      archCap:{ small:5, mid:8, large:12 }, archProb:0.16,
      logoProb:0.10, logoMinHeight:2.4
    }
  },

  /* ── Night: the stylesheet that makes lit windows meaningful ── */
  night: {
    name: 'Night',
    sky:  '#0a1020',
    fog:  { color:'#0a1020', density:0.016 },
    light: {
      ambient: { color:'#4a5a80', intensity:0.34 },
      sun:     { color:'#8fa6d8', intensity:0.28, dir:[-0.30,-0.85,-0.38] },
      fill:    { color:'#2a3a5c', intensity:0.22, dir:[ 0.50,-0.50, 0.42] }
    },
    // Ground must contrast strongly with the roofs or the code stops being
    // scannable — the poclet's whole claim. Moonlit pavement, not black.
    ground:'#7c8494', plate:'#05070c', roof:'#05070c',
    surround: { color:'#2a3140' },
    facade: {
      flat: ['#3e4455','#363c4b','#2f3543','#433c4d',
             '#3a4351','#48403c','#404753','#333a47'],
      brick: [ { brick:'#5a3428', mortar:'#3d372f', jitter:0.18, seed:0x5EED21 } ],
      stone: [
        { stone:'#4a4c54', mortar:'#35373d', jitter:0.16, seed:0x570E11 },
        { stone:'#565962', mortar:'#3e4148', jitter:0.18, seed:0x570E12 }
      ],
      glass: [
        { tint:'#1e2c3a', mullion:'#0f1620', litTint:'#ffe9a8', litProb:0.52, seed:0x5EED31 },
        { tint:'#243342', mullion:'#0f1620', litTint:'#fff0c0', litProb:0.46, seed:0x5EED32 }
      ]
    },
    // Strong glow: at night the windows are the primary light source
    window:  { lit:'#fff0b4', litGlow:'#ffd166', glow:1.55, dark:'#0d1220' },
    // A bloom pass turns lit windows into light sources rather than bright
    // rectangles. Hundreds of real point lights would be unaffordable; this
    // buys the same read for one post-process.
    glowLayer: { intensity: 0.85, blurKernel: 42 },
    chimney:'#555d6b', door:'#8a6a3a', frame:'#6b7280', step:'#3f4654',
    landmark: {
      colors: ['#ef4444','#3b82f6','#22c55e','#a855f7','#f59e0b'],
      names:  ['Town Hall','University','Hospital','Market Hall','Library']
    },
    logo: {
      size: 0.75,
      palette: ['#e0345a','#1f6fd0','#14b37d','#f0b429',
                '#b14aed','#ff6b35','#0d1220','#e8eaf0']
    },
    inverted: {
      ground:'#123f22', plate:'#ffffff', roof:'#ffffff',
      facadeFlat: ['#a8794a','#96683c','#ba8c5e','#855c34',
                   '#a07348','#b08055','#8f6540','#c29464'],
      chimney:'#8a90a0', door:'#3a1c0c', frame:'#dfe3ec', step:'#9aa0b0'
    },
    rules: {
      height:       { min:0.8, max:5.2 },   // taller: more lit floors
      landmarkKeep: { min:3.4, max:6.0 },
      landmarkRing: { min:1.4, max:2.2 },
      glassProb:0.42, glassMinHeight:2.6, landmarkGlassProb:0.45,
      windowsPerFace:{ min:2, max:3 },
      windowAbsentProb:0.08, windowLitProb:0.72, bayProb:0.34,
      chimneyMax:2, landmarkChimneyProb:0.35,
      archCap:{ small:5, mid:8, large:12 }, archProb:0.16,
      logoProb:0.20, logoMinHeight:2.3
    }
  },

  /* ── Blueprint: technical draft. No textures, geometry legible ── */
  blueprint: {
    name: 'Blueprint',
    sky:  '#0b3a6f',
    fog:  null,
    light: {
      ambient: { color:'#ffffff', intensity:0.85 },
      sun:     { color:'#dceeff', intensity:0.45, dir:[-0.38,-0.86,-0.30] },
      fill:    { color:'#9fc4ff', intensity:0.35, dir:[ 0.52,-0.52, 0.40] }
    },
    // Same reason as Night: #11498a on #08284f was blue-on-blue and barely
    // readable. Ink-on-paper contrast, still unmistakably a draft.
    ground:'#4f9ae6', plate:'#04162c', roof:'#04162c',
    surround: { color:'#0b3a6f' },
    facade: {
      flat: ['#17518f','#1b5c9e','#134780','#1f66aa',
             '#195496','#215f9f','#0f3f74','#1d5aa0'],
      brick: [], stone: [], glass: []      // draft mode: no texture at all
    },
    window:  { lit:'#bfe0ff', litGlow:'#2a6fae', glow:0.45, dark:'#0d3c6e' },
    chimney:'#9fc4ff', door:'#bfe0ff', frame:'#dceeff', step:'#7fa9d8',
    landmark: {
      colors: ['#ffffff','#dceeff','#bfe0ff','#a5d0f5','#8cc0ee'],
      names:  ['Civic A','Civic B','Civic C','Civic D','Civic E']
    },
    logo: { size:0.75, palette:['#08284f','#ffffff','#1d5fa8','#dceeff'] },
    inverted: {
      ground:'#175c31', plate:'#ffffff', roof:'#ffffff',
      facadeFlat: ['#d0a878','#c09865','#dcb88a','#b08a58',
                   '#c8a070','#d8b080','#b89460','#e2c297'],
      chimney:'#c2d8f0', door:'#50301a', frame:'#ffffff', step:'#d2e2f4'
    },
    rules: {
      height:       { min:1.0, max:3.6 },   // flatter: reads as a plan
      landmarkKeep: { min:2.8, max:4.2 },
      landmarkRing: { min:1.2, max:1.8 },
      glassProb:0, glassMinHeight:99, landmarkGlassProb:0,
      windowsPerFace:{ min:1, max:2 },
      windowAbsentProb:0.25, windowLitProb:0.30, bayProb:0.10,
      chimneyMax:1, landmarkChimneyProb:0.15,
      archCap:{ small:8, mid:14, large:20 }, archProb:0.30,  // arches emphasised
      logoProb:0.08, logoMinHeight:2.2
    }
  },

  /* ── Winter: white roofs on mid-grey ground. Snow-capped low town ── */
  winter: {
    name: 'Winter',
    sky:  '#c3ced9',
    fog:  { color:'#c3ced9', density:0.013 },
    light: {
      ambient: { color:'#eef4fb', intensity:0.78 },
      sun:     { color:'#ffffff', intensity:0.72, dir:[-0.30,-0.88,-0.36] },
      fill:    { color:'#c8d8ec', intensity:0.34, dir:[ 0.46,-0.50, 0.44] }
    },
    // Polarity is deliberately reversed here: built modules are the WHITE
    // ones (snow-covered roofs) against mid-grey ground. The QR still reads,
    // because contrast is what matters, not which side is dark.
    ground: '#4a4f57',
    plate:  '#fbfdff',
    roof:   '#fbfdff',
    surround: { color:'#6f7680' },        // open snowfield beyond the town
    facade: {
      flat: ['#6d7079','#7a7d86','#5f636c','#858892',
             '#71757e','#8e919a','#666a73','#7e828b'],
      brick: [ { brick:'#8a6a5e', mortar:'#b9b4ae', jitter:0.16, seed:0x5EED51 } ],
      stone: [
        { stone:'#9aa0a8', mortar:'#7d838b', jitter:0.14, seed:0x570E31 },
        { stone:'#878d95', mortar:'#6e747c', jitter:0.16, seed:0x570E32 }
      ],
      glass: [
        { tint:'#7f95a8', mullion:'#4a525c', litTint:'#ffeec2', litProb:0.30, seed:0x5EED61 }
      ]
    },
    window:  { lit:'#ffeec2', litGlow:'#8a6320', glow:0.85, dark:'#2b323c' },
    chimney: '#d8dee6',
    door:    '#4a3428',
    frame:   '#e8edf3',
    step:    '#9aa0a8',
    landmark: {
      colors: ['#a83232','#2f5d9c','#2c7a52','#6b4a9c','#b8792a'],
      names:  ['Town Hall','University','Hospital','Market Hall','Library']
    },
    logo: {
      size: 0.75,
      palette: ['#a83232','#2f5d9c','#2c7a52','#3d434c','#f0f4f8','#1d2229']
    },
    inverted: {
      ground:'#2e6b46', plate:'#ffffff', roof:'#ffffff',
      facadeFlat: ['#c9a878','#b89865','#d4b88a','#a88a58',
                   '#c0a070','#ccb080','#b09460','#d8c297'],
      chimney:'#dfe4ea', door:'#4a2c18', frame:'#ffffff', step:'#c4cad2'
    },
    rules: {
      height:       { min:0.5, max:3.0 },   // low town under snow
      landmarkKeep: { min:2.8, max:4.4 },
      landmarkRing: { min:1.0, max:1.7 },
      glassProb:0.14, glassMinHeight:2.4, landmarkGlassProb:0.15,
      windowsPerFace:{ min:1, max:3 },
      windowAbsentProb:0.12, windowLitProb:0.68, bayProb:0.16,
      chimneyMax:4, landmarkChimneyProb:0.70,   // chimneys matter in winter
      archCap:{ small:5, mid:9, large:14 }, archProb:0.18,
      logoProb:0.10, logoMinHeight:2.2
    }
  },

  /* ── Cycladic: blue domes over whitewash, on ochre earth ── */
  cycladic: {
    name: 'Cycladic',
    sky:  '#0d2b52',                     // navy: continuous with the sea
    fog:  null,
    light: {
      ambient: { color:'#fff8ec', intensity:0.80 },
      sun:     { color:'#fffdf4', intensity:0.88, dir:[-0.42,-0.84,-0.26] },
      fill:    { color:'#bfe4ff', intensity:0.30, dir:[ 0.44,-0.48, 0.46] }
    },
    // Roofs are the Aegean blue of the island churches; the ground is the
    // dry ochre earth between the houses.
    ground: '#e09d45',
    plate:  '#014FB5',
    roof:   '#014FB5',
    // #014FB5 sits at luminance 0.27; the ground had to rise to 0.65 to keep
    // the roof/street contrast above the scannable threshold.
    surround: {
      color: '#0d2b52',                    // deep navy Aegean
      waves: { crest:'#7fb8e8', count:220, seed:0x5EA001 }
    },
    facade: {
      flat: ['#f7f4ee','#efeae1','#fbf8f3','#e8e2d8',
             '#f3efe7','#faf6f0','#ece6dc','#f6f2ea'],
      brick: [],                                   // whitewash, never brick
      stone: [],                                   // no visible courses here
      // Hand-applied render in sand tones: mottled, jointless, faintly
      // swept by the trowel.
      plaster: [
        { base:'#e8dcc2', jitter:0.13, mottle:150, sweeps:40, seed:0x51A001 },
        { base:'#ddceb0', jitter:0.14, mottle:160, sweeps:44, seed:0x51A002 },
        { base:'#f0e6d2', jitter:0.11, mottle:140, sweeps:36, seed:0x51A003 }
      ],
      glass: []
    },
    // Only the roofs are Aegean blue. Making the joinery blue too made every
    // opening disappear into the roofline, so windows and doors are timber.
    window:  { lit:'#ffeeb8', litGlow:'#7a5a18', glow:0.60, dark:'#4a3b28' },
    chimney: '#ffffff',
    door:    '#6b4423',
    frame:   '#f4efe4',
    step:    '#c98f4e',
    landmark: {
      colors: ['#013b88','#014FB5','#0263d6','#012a63','#2a7fd4'],
      names:  ['Dimarcheio','Panepistimio','Nosokomeio','Agora','Vivliothiki']
    },
    logo: {
      size: 0.75,
      palette: ['#0d3f7a','#1d5fa8','#ffffff','#c07423','#6b4423']
    },
    inverted: {
      ground:'#2f7a45', plate:'#ffffff', roof:'#ffffff',
      facadeFlat: ['#e0a24e','#cf9040','#eab370','#bd7f36',
                   '#d99a48','#e5aa60','#c78838','#edbb7e'],
      chimney:'#f0e8d8', door:'#15498c', frame:'#ffffff', step:'#dcd2c0'
    },
    rules: {
      height:       { min:0.5, max:2.4 },   // cubic houses, very low-rise
      landmarkKeep: { min:2.6, max:3.8 },
      landmarkRing: { min:0.9, max:1.5 },
      glassProb:0, glassMinHeight:99, landmarkGlassProb:0,
      windowsPerFace:{ min:1, max:2 },      // few, small openings
      windowAbsentProb:0.30, windowLitProb:0.35, bayProb:0.06,
      // No chimneys on the islands: flat whitewashed terraces, not hearths
      chimneyMax:0, landmarkChimneyProb:0,
      // Roughly one roof in six carries a blue hemispherical dome
      domeProb:0.17,
      archCap:{ small:9, mid:15, large:22 }, archProb:0.34,  // passages everywhere
      logoProb:0.06, logoMinHeight:1.9
    }
  },

  /* ── Terracotta: Mediterranean old town, brick and stone, low-rise ── */
  terracotta: {
    name: 'Terracotta',
    sky:  '#e8c89a',
    fog:  { color:'#e8c89a', density:0.010 },
    light: {
      ambient: { color:'#fff2e0', intensity:0.70 },
      sun:     { color:'#ffe0b0', intensity:1.00, dir:[-0.48,-0.80,-0.22] },
      fill:    { color:'#ffd9b8', intensity:0.26, dir:[ 0.42,-0.55, 0.48] }
    },
    ground:'#f0e2cc', plate:'#2a1a12', roof:'#2a1a12',
    surround: { color:'#c9a878' },
    facade: {
      flat: ['#d9a066','#c98f5a','#e0b183','#bf7f4f',
             '#d4a878','#c79060','#e8c39a','#b87848'],
      brick: [
        { brick:'#b5563a', mortar:'#e0cbb0', jitter:0.26, seed:0x5EED41 },
        { brick:'#a04b32', mortar:'#d8c0a4', jitter:0.24, seed:0x5EED42 },
        { brick:'#c46748', mortar:'#e8d6bd', jitter:0.22, seed:0x5EED43 }
      ],
      stone: [
        { stone:'#d6c9a8', mortar:'#b8a888', jitter:0.20, seed:0x570E21 },
        { stone:'#c4b593', mortar:'#a89878', jitter:0.22, seed:0x570E22 }
      ],
      glass: []                                   // no curtain walls here
    },
    window:  { lit:'#fff0c4', litGlow:'#7a5218', glow:0.55, dark:'#4a3524' },
    chimney:'#e0cbb0', door:'#5d3a1f', frame:'#efe0c8', step:'#d8c4a4',
    landmark: {
      colors: ['#8c2f24','#2f5d7c','#4a7c3f','#6b3f7c','#c2761f'],
      names:  ['Ayuntamiento','Universidad','Hospital','Mercado','Biblioteca']
    },
    logo: {
      size: 0.75,
      palette: ['#8c2f24','#2f5d7c','#4a7c3f','#c2761f','#fff3dd','#3d2a18']
    },
    inverted: {
      ground:'#2a5e26', plate:'#ffffff', roof:'#ffffff',
      facadeFlat: ['#d98c4a','#c47a38','#eaa068','#b56a2e',
                   '#d28450','#c07040','#e2975e','#aa6030'],
      chimney:'#d8ccb4', door:'#5a2a12', frame:'#fff8ec', step:'#e4d8c0'
    },
    rules: {
      height:       { min:0.5, max:2.8 },   // low-rise old town
      landmarkKeep: { min:3.2, max:5.0 },   // landmarks dominate the skyline
      landmarkRing: { min:1.0, max:1.6 },
      glassProb:0, glassMinHeight:99, landmarkGlassProb:0,
      windowsPerFace:{ min:1, max:2 },
      windowAbsentProb:0.18, windowLitProb:0.40, bayProb:0.12,
      chimneyMax:3, landmarkChimneyProb:0.60,
      archCap:{ small:7, mid:12, large:18 }, archProb:0.26,  // arcaded streets
      logoProb:0.16, logoMinHeight:2.1
    }
  }
};

const QRCITY_STYLE_IDS = Object.keys(QRCITY_STYLESHEETS);
