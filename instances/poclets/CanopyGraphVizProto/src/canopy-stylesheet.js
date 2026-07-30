/* Canopée — STYLESHEET. The single declarative encoding, and the source the
   on-screen legend is generated from. Editing this file changes both the render
   and its reading guide. See Canopee_Stylesheet_and_Legend_Spec.md. */
'use strict';

const REL_COLORS={subClassOf:'#6ea8ff',hasFamily:'#e0a94b',hasDominantM3:'#b96be0',
  comboOf:'#59d6a2',appliesToDomains:'#48b6e8',illustratesConcept:'#d98cae',
  ontologyType:'#8fa2c8',imports:'#4a5a80',a:'#39466a',authoredBy:'#39466a'};
const PAL9=['#e0a94b','#48b6e8','#b96be0','#59d6a2','#d98cae','#e8734a','#7f9cf5','#c7d24a','#4ac7c7','#9aa6c0'];

// ============================================================================
//  STYLESHEET  —  the single declarative encoding = the map legend (spec v1.0).
//  One source of truth: node point-symbols, edge line-symbols, hue palettes.
//  The on-screen legend (buildLegend) is generated FROM this object; editing here
//  changes both the render and the legend. Runtime toggles live in `state`.
// ============================================================================
const STYLESHEET={
  nodes:{
    shapeBy:'kind', size:'magnitude',
    // point symbol per kind: shape (channel) · hue (default) · ring (relational flag)
    kinds:{
      foundation:   {shape:'ico',    hue:'#e6c65b', ring:null,     label:'M3 foundation'},
      root:         {shape:'dodeca', hue:'#8fa2c8', ring:null,     label:'root class'},
      concept:      {shape:'tetra',  hue:'#e6c94b', ring:null,     label:'GenericConcept'},
      combo:        {shape:'octa',   hue:'#59d6a2', ring:null,     label:'GenericConceptCombo'},
      domainCombo:  {shape:'octa',   hue:'#59d6a2', ring:'square', label:'DomainConceptCombo'},
      family:       {shape:'cube',   hue:'#6ea8ff', ring:null,     label:'family'},
      domainConcept:{shape:'cube',   hue:'#59d6a2', ring:'round',  label:'M1 domain concept'},
      instance:     {shape:'sphere', hue:'#d98cae', ring:null,     label:'M0 instance (fruit)'},
      vocab:        {shape:'octa',   hue:'#5a6b8c', ring:null,     label:'imported vocabulary'},
      other:        {shape:'sphere', hue:'#8fa2c8', ring:null,     label:'other'},
    },
    // hue palettes used when hue is bound to a facet/computed field instead of kind
    huePalettes:{
      dominantM3:{Territory:'#e6a94b',Map:'#48b6e8',Stereopsis:'#b96be0','—':'#5a6b8c'},
      layer:{m3:'#e6c65b',m2:'#6ea8ff',m1:'#59d6a2',m0:'#d98cae',VOCAB:'#5a6b8c'},
      categorical:PAL9,
    },
  },
  edges:{ colors:REL_COLORS },   // opacity is live in state.edgeAlpha (scaffolding)
  frame:{},                      // radialAxis + instrument are live in state
};
const GLYPHS=STYLESHEET.nodes.kinds;   // alias for the mesh/legend code paths

const SHAPE_GLYPH={sphere:'●',cube:'■',tetra:'▲',octa:'◆',ico:'⬢',dodeca:'⬟'};
const ORBIT_TESS={sphere:36,ico:36,dodeca:5,cube:4,octa:4,tetra:3};
