/* Canopée — DATA ADAPTER. Emits the {nodes, edges} shape canopy-core consumes.
   Swap this file for a real M0–M3 parser, a Neo4j/Bolt reader, or a GEXF loader:
   nothing else needs to change. */
'use strict';

/* ---- 1. DATA ADAPTER: a synthetic-but-faithful TSCG layer cake ------------ */
const M3='m3',M2='m2',M1='m1',M0='m0';
const N=[]; const E=[];
function n(id,label,layer,vocab,extra={}){N.push(Object.assign({id,label,layer,vocab},extra));}
function e(s,t,type){E.push({s,t,type});}

/* --- M3 : foundations (the fixed, brightest stars) --- */
n('GrammarFoundation','GrammarFoundation',M3,'m3',{ontologyType:'—'});
['GenesisGrammar','EagleEye','SphinxEye','BicephalousPerspective'].forEach(x=>{
  n(x,x,M3,'m3'); e(x,'GrammarFoundation','imports');});
n('MonoidalType','MonoidalType',M3,'m3'); e('MonoidalType','GrammarFoundation','subClassOf');
['Territory','Map','Stereopsis'].forEach(x=>{n(x,x,M3,'m3'); e(x,'MonoidalType','subClassOf');});
['Poclet','TscgTool','SystemicFramework','SymbolicSystemGrammar'].forEach(x=>{
  n(x,x,M3,'m3',{ontologyType:x});});
n('Facet','Facet',M3,'m3'); e('Facet','GrammarFoundation','subClassOf');

/* --- M2 : GenericConcepts + families --- */
n('GenericConcept','GenericConcept',M2,'m2');
n('GenericConceptFamily','GenericConceptFamily',M2,'m2');
const fams=['Structural','Dynamic','Regulatory','Adaptive','Energetic',
            'Informational','Ontological','Teleonomic','Relational','Combo'];
fams.forEach(f=>{n(f,f+' Family',M2,'m2',{family:f}); e(f,'GenericConceptFamily','subClassOf');});
// concept, family, dominant grammar
const concepts=[
 ['Composition','Structural','Territory'],['Hierarchy','Structural','Territory'],
 ['Modularity','Structural','Territory'],['Imbrication','Structural','Territory'],
 ['Layer','Structural','Territory'],['Segmentation','Structural','Territory'],
 ['Transformation','Dynamic','Territory'],['Flow','Energetic','Territory'],
 ['FeedbackLoop','Regulatory','Territory'],['Homeostasis','Regulatory','Territory'],
 ['Balance','Regulatory','Stereopsis'],['Adaptation','Adaptive','Territory'],
 ['Representation','Informational','Map'],['Interoperability','Informational','Map'],
 ['Observability','Informational','Map'],['Verifiability','Informational','Map'],
 ['Emergence','Ontological','Territory'],['Boundary','Ontological','Territory'],
 ['Role','Relational','Stereopsis'],['Symbol','Relational','Stereopsis'],
 ['Optimization','Teleonomic','Stereopsis'],
];
concepts.forEach(([c,f,d])=>{
  n(c,c,M2,'m2',{family:f,dominantM3:d});
  e(c,'GenericConcept','subClassOf'); e(c,f,'hasFamily'); e(c,d,'hasDominantM3');});
// combos
[['GenericConceptCombo',['Composition','Emergence']],
 ['DomainConceptCombo',['GenericConceptCombo']]].forEach(([c,parents])=>{
  n(c,c,M2,'m2',{family:'Combo'}); e(c,'Combo','hasFamily'); e(c,'GenericConcept','subClassOf');
  parents.forEach(p=>e(c,p,'comboOf'));});

// family cohesion — concepts of one family are mutually related (real TSCG intra-family links,
// e.g. the M2 'distinctionFromRelated' web: Composition vs Modularity vs Hierarchy …).
(function(){const g={};
  N.filter(x=>x.layer===M2&&x.dominantM3).forEach(x=>{(g[x.family]=g[x.family]||[]).push(x.id);});
  Object.values(g).forEach(a=>{ if(a.length<2)return;
    for(let i=0;i<a.length;i++) e(a[i],a[(i+1)%a.length],'relatedTo');   // ring
    if(a.length>3) e(a[0],a[2],'relatedTo');                            // one chord for density
  });})();

/* --- M1 : core concepts, domains, extensions --- */
n('CoreConcepts','CoreConcepts',M1,'m1');
const domains=['Biology','Optics','Chemistry','Music','Economics','Physics'];
domains.forEach(d=>n(d,d,M1,'m1',{family:'—'}));
[['Refraction','Optics','Transformation'],['Catalysis','Chemistry','Transformation'],
 ['CounterpointRule','Music','Balance'],['Cascade','Physics','Flow'],
 ['Metabolism','Biology','Flow']].forEach(([c,dom,parent])=>{
  n(c,c,M1,'m1'); e(c,parent,'subClassOf'); e(c,dom,'appliesToDomains');});

/* --- M0 : instances (the many faint stars) --- */
const insts=[
 ['FireTriangle','Poclet',['Composition','Emergence'],['Physics'],'Democratization'],
 ['ExposureTriangle','Poclet',['Balance'],['Optics'],'Democratization'],
 ['Counterpoint','SymbolicSystemGrammar',['Balance','Layer'],['Music'],null],
 ['IChing','SymbolicSystemGrammar',['Segmentation'],[],null],
 ['Kidneys','SystemicFramework',['Homeostasis','Flow'],['Biology'],null],
 ['Vsm','SystemicFramework',['FeedbackLoop','Hierarchy'],[],null],
 ['Triz','TscgTool',['Transformation'],[],null],
 ['NakamotoConsensus','SystemicFramework',['FeedbackLoop'],['Economics'],null],
 ['PhaseTransition','Poclet',['Transformation','Emergence'],['Physics'],null],
 ['TrophicPyramid','SystemicFramework',['Hierarchy','Flow'],['Biology'],null],
 ['PlateTectonics','SystemicFramework',['Transformation'],['Physics'],null],
 ['CellSignaling','SystemicFramework',['Interoperability'],['Biology'],null],
 ['ColorSynthesis','Poclet',['Composition'],['Optics'],'Democratization'],
 ['FourStrokeEngine','Poclet',['Transformation','FeedbackLoop'],['Physics'],null],
];
insts.forEach(([id,otype,ill,doms,facet])=>{
  n(id,id,M0,'m0',{ontologyType:otype});
  e(id,otype,'ontologyType');
  ill.forEach(c=>e(id,c,'illustratesConcept'));
  doms.forEach(d=>e(id,d,'appliesToDomains'));
  if(facet) N[N.length-1].facet=facet;
});

/* --- imported vocabulary (hidden by default; the hairball magnets) --- */
[['owl:Class','owl'],['owl:Ontology','owl'],['rdfs:subClassOf','rdfs'],
 ['rdfs:label','rdfs'],['dcterms:creator','dcterms'],['xsd:string','xsd'],
 ['skos:example','skos']].forEach(([id,v])=>n(id,id,'VOCAB',v,{}));
// every concept "is a" owl:Class, every instance authored by dcterms:creator ...
N.filter(x=>x.layer===M2||x.layer===M1).forEach(x=>e(x.id,'owl:Class','a'));
N.filter(x=>x.layer===M0).forEach(x=>{e(x.id,'owl:Ontology','a');e(x.id,'dcterms:creator','authoredBy');});
