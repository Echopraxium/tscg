/* Canopée — CORE. Domain-agnostic: layout strategies, structure recovery,
   rendering, radar, explorer, interaction, legend generation.
   Depends on: canopy-data.js (N, E) and canopy-stylesheet.js (STYLESHEET…). */
'use strict';

/* ============================================================================
   CANOPY-CORE  —  host-agnostic star-map renderer for typed graphs.
   Consumes: nodes[{id,label,layer,vocab,family,dominantM3,ontologyType}]
             edges[{s,t,type}]   (typed, directed s→t)
   Everything visual is a configurable projection of a declared attribute:
     radial  ← subClassOf-depth | meta-level | hops     (pluggable)
     sector+colour ← a chosen facet                     (pluggable)
     magnitude ← degree
   The TSCG data below is one *adapter*. Neo4j/Bolt, Obsidian/MetadataCache or a
   real M0–M3 parser would each emit the same {nodes,edges} shape.
============================================================================ */

/* ---- 2. GRAPH UTILITIES --------------------------------------------------- */
const byId=Object.fromEntries(N.map(x=>[x.id,x]));
const REL_TYPES=[...new Set(E.map(x=>x.type))];
const LAYER_ORDER={m3:0,m2:1,m1:2,m0:3,VOCAB:4};

const deg={}; N.forEach(x=>deg[x.id]=0);
E.forEach(x=>{deg[x.s]++;deg[x.t]++;});
const maxDeg=Math.max(...N.filter(x=>x.layer!=='VOCAB').map(x=>deg[x.id]));
// Magnitude by RANK (percentile), not by degree ratio: degree is heavily skewed, so a linear
// ratio piles almost every node into one magnitude and the instrument then culls all-or-nothing.
const magOf={};
(function computeMagnitudes(){
  const rank=N.slice().sort((a,b)=>deg[a.id]-deg[b.id]);
  rank.forEach((x,i)=>{ magOf[x.id]=Math.round(9*i/Math.max(1,rank.length-1)); });
})();

function adjacency(types){ // undirected adjacency over a subset of edge types
  const a={}; N.forEach(x=>a[x.id]=[]);
  E.forEach(({s,t,type})=>{ if(!types||types.has(type)){a[s].push(t);a[t].push(s);} });
  return a;
}
function bfsDist(focus,types){
  const a=adjacency(types),d={},q=[focus]; d[focus]=0;
  while(q.length){const u=q.shift();a[u].forEach(v=>{if(d[v]===undefined){d[v]=d[u]+1;q.push(v);}});}
  return d;
}
// graph barycentre: the node minimising total shortest-path distance (closeness centre),
// over the non-vocabulary graph. This is the default observer position.
function graphBarycenter(){
  const a=adjacency(null), ids=N.filter(x=>x.layer!=='VOCAB').map(x=>x.id);
  const idset=new Set(ids); let best=ids[0], bestTot=Infinity;
  ids.forEach(src=>{
    const d={[src]:0},q=[src]; let sum=0,reached=0;
    while(q.length){const u=q.shift();(a[u]||[]).forEach(v=>{
      if(idset.has(v)&&d[v]===undefined){d[v]=d[u]+1;q.push(v);sum+=d[v];reached++;}});}
    const tot=sum+(ids.length-1-reached)*ids.length;   // penalise unreached
    if(tot<bestTot){bestTot=tot;best=src;}
  });
  return best;
}

/* ---- 3. STATE ------------------------------------------------------------- */
const state={
  focus:'GenericConcept',
  radial:'tree',
  facet:'dominantM3',
  coneDeg:40, depth:7, magFloor:0,
  showVocab:false,
  showAll:false,
  selectCenter:false,
  arrangement:'canopy',
  edgeAlpha:0.15,
  colorBy:'facet',
  collapsed:new Set(),        // DERIVED each layout from the expansion policy below
  expandLimit:5,              // 1 (exclusive) | 3 | 5 | 10 | Infinity
  autoOpenDepth:2,            // anything shallower than this starts open
  expandOrder:[],             // LRU queue of explicitly opened nodes
  forcedClosed:new Set(),     // explicitly closed, overrides autoOpenDepth
  slice:null,
  spectral:{on:false,k:3},
  rels:Object.fromEntries(REL_TYPES.map(t=>[t,!['a','authoredBy'].includes(t)])),
};
let specLabels={};   // nodeId -> 'C0'.. , filled by runSpectral()

/* facet value + colour palettes */
function facetVal(node){
  if(state.spectral.on) return specLabels[node.id]||'·';   // spectral is just another facet provider
  switch(state.facet){
    case 'dominantM3': return node.dominantM3||'—';
    case 'family':     return node.family||'—';
    case 'layer':      return node.layer;
    case 'ontologyType':return node.ontologyType||'—';
    case 'vocab':      return node.vocab;
  }
}
let facetColorMap={};
function rebuildFacetColors(){
  facetColorMap={};
  const HP=STYLESHEET.nodes.huePalettes;
  if(state.spectral.on){
    for(let i=0;i<state.spectral.k;i++) facetColorMap['C'+i]=HP.categorical[i%HP.categorical.length];
    facetColorMap['·']='#5a6b8c'; return;
  }
  if(state.facet==='dominantM3'){ facetColorMap={...HP.dominantM3}; }
  else if(state.facet==='layer'){ facetColorMap={...HP.layer}; }
  else{
    const vals=[...new Set(N.map(facetVal))];
    vals.forEach((v,i)=>facetColorMap[v]=HP.categorical[i%HP.categorical.length]);
  }
}
function colorOf(node){
  if(state.colorBy==='kind') return (STYLESHEET.nodes.kinds[kindOf(node)]||STYLESHEET.nodes.kinds.other).hue;
  return facetColorMap[facetVal(node)]||'#5a6b8c';
}

/* ---- 4. LAYOUT : spherical (r,θ,φ) --------------------------------------- */
const SHELL=9, R0=6;
function hash(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return((h>>>0)%10000)/10000;}
let radialOf={};
function computeRadial(){
  radialOf={};
  if(state.radial==='meta'){
    N.forEach(x=>radialOf[x.id]=LAYER_ORDER[x.layer]);
  }else if(state.radial==='trophic'){
    // directed flow → height (MacKay/Johnson/Sansom). Honours triple direction s→t.
    const ids=N.map(x=>x.id);
    const types=new Set(REL_TYPES.filter(t=>state.rels[t]));
    const h=trophicLevels(ids,types);            // already normalised to [0,6]
    N.forEach(x=>radialOf[x.id]=h[x.id]);
  }else{
    const types=state.radial==='subclass'
      ? new Set(['subClassOf','hasFamily'])
      : new Set(REL_TYPES.filter(t=>state.rels[t]));
    const d=bfsDist(state.focus,types);
    const far=Math.max(0,...Object.values(d))+1;
    N.forEach(x=>radialOf[x.id]=(d[x.id]===undefined?far:d[x.id]));
  }
}

/* ---- 4b. STRUCTURE RECOVERY (pure JS, no deps) --------------------------- */
function dot(a,b){let s=0;for(let i=0;i<a.length;i++)s+=a[i]*b[i];return s;}
function mulberry32(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;
  let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;
  return((t^t>>>14)>>>0)/4294967296;};}

/* Trophic levels: solve the weighted-Laplacian system Λh = (w_in − w_out) by CG.
   Λ = diag(w_in+w_out) − (W+Wᵀ); regularised to SPD; result rescaled to [0,6]. */
function trophicLevels(ids,useTypes){
  const idx={}; ids.forEach((id,i)=>idx[id]=i); const n=ids.length;
  const win=new Float64Array(n),wout=new Float64Array(n),adj=Array.from({length:n},()=>[]);
  E.forEach(({s,t,type})=>{ if(useTypes&&!useTypes.has(type))return;
    if(!(s in idx)||!(t in idx)||s===t)return;
    const i=idx[s],j=idx[t]; wout[i]++; win[j]++; adj[i].push(j); adj[j].push(i);});
  const diag=new Float64Array(n),v=new Float64Array(n),eps=1e-6;
  for(let i=0;i<n;i++){diag[i]=win[i]+wout[i]; v[i]=win[i]-wout[i];}
  const Lmul=x=>{const y=new Float64Array(n);
    for(let i=0;i<n;i++){let s=(diag[i]+eps)*x[i]; for(const j of adj[i])s-=x[j]; y[i]=s;} return y;};
  let h=new Float64Array(n),r=v.slice(),p=r.slice(),rs=dot(r,r);
  for(let it=0;it<400&&Math.sqrt(rs)>1e-9;it++){
    const Ap=Lmul(p),al=rs/(dot(p,Ap)||1e-12);
    for(let i=0;i<n;i++){h[i]+=al*p[i];r[i]-=al*Ap[i];}
    const rs2=dot(r,r),be=rs2/(rs||1e-12);
    for(let i=0;i<n;i++)p[i]=r[i]+be*p[i]; rs=rs2;
  }
  let mn=Infinity,mx=-Infinity; for(const x of h){if(x<mn)mn=x;if(x>mx)mx=x;}
  const rng=(mx-mn)||1,out={}; ids.forEach((id,i)=>out[id]=(h[i]-mn)/rng*6); return out;
}

/* Normalized-Laplacian spectral clustering: top-k modes of M=D^-1/2 A D^-1/2
   via deflated power iteration, then row-normalised k-means (Ng–Jordan–Weiss). */
// Usage/relational edges only. The classificatory edges (hasFamily, hasDominantM3,
// ontologyType) ARE the labels — feeding them would leak the answer. So spectral must
// recover the grouping from how concepts are *related and used*, not how they're filed.
const SPECTRAL_EDGES=new Set(['relatedTo','illustratesConcept','comboOf','appliesToDomains','imports']);
function spectralClusters(ids,k){
  const idx={}; ids.forEach((id,i)=>idx[id]=i); const n=ids.length;
  const A=Array.from({length:n},()=>[]),deg=new Float64Array(n);
  E.forEach(({s,t,type})=>{ if(!SPECTRAL_EDGES.has(type))return;
    if(!(s in idx)||!(t in idx)||s===t)return;
    const i=idx[s],j=idx[t]; A[i].push(j); A[j].push(i); deg[i]++; deg[j]++;});
  const isq=new Float64Array(n); for(let i=0;i<n;i++)isq[i]=deg[i]>0?1/Math.sqrt(deg[i]):0;
  const Mmul=x=>{const y=new Float64Array(n);
    for(let i=0;i<n;i++){let s=0;for(const j of A[i])s+=isq[i]*isq[j]*x[j];y[i]=s;}return y;};
  const rnd=mulberry32(12345), eigs=[];
  for(let e=0;e<k;e++){
    let v=new Float64Array(n); for(let i=0;i<n;i++)v[i]=rnd()-0.5;
    for(let it=0;it<220;it++){
      let w=Mmul(v);
      for(const u of eigs){const d=dot(w,u);for(let i=0;i<n;i++)w[i]-=d*u[i];}
      const nr=Math.sqrt(dot(w,w))||1; for(let i=0;i<n;i++)w[i]/=nr; v=w;
    }
    eigs.push(v);
  }
  // embedding rows (n×k), row-normalised
  const rows=Array.from({length:n},(_,i)=>{
    const r=eigs.map(u=>u[i]); const nr=Math.hypot(...r)||1; return r.map(z=>z/nr);});
  // k-means with restarts
  let best=null,bestJ=Infinity;
  for(let rs=0;rs<8;rs++){
    const rr=mulberry32(7*rs+1); let C=[];
    const first=Math.floor(rr()*n); C.push(rows[first].slice());
    while(C.length<k){ // k-means++
      const D=rows.map(p=>Math.min(...C.map(c=>dist2(p,c))));
      let sum=D.reduce((a,b)=>a+b,0)||1, thr=rr()*sum, acc=0, pick=0;
      for(let i=0;i<n;i++){acc+=D[i]; if(acc>=thr){pick=i;break;}}
      C.push(rows[pick].slice());
    }
    let lab=new Array(n).fill(0);
    for(let it=0;it<30;it++){
      for(let i=0;i<n;i++){let bd=Infinity,bi=0;
        for(let c=0;c<k;c++){const d=dist2(rows[i],C[c]);if(d<bd){bd=d;bi=c;}} lab[i]=bi;}
      const sums=Array.from({length:k},()=>new Float64Array(k)),cnt=new Float64Array(k);
      for(let i=0;i<n;i++){cnt[lab[i]]++;for(let d=0;d<k;d++)sums[lab[i]][d]+=rows[i][d];}
      for(let c=0;c<k;c++)if(cnt[c])for(let d=0;d<k;d++)C[c][d]=sums[c][d]/cnt[c];
    }
    let J=0; for(let i=0;i<n;i++)J+=dist2(rows[i],C[lab[i]]);
    if(J<bestJ){bestJ=J;best=lab.slice();}
  }
  const out={}; ids.forEach((id,i)=>out[id]='C'+best[i]); return out;
}
function dist2(a,b){let s=0;for(let i=0;i<a.length;i++){const d=a[i]-b[i];s+=d*d;}return s;}

/* purity of spectral clusters against the declared 'dominantM3' facet */
function grammarRecovery(labels){
  const groups={}; N.forEach(x=>{ if(!x.dominantM3)return; const c=labels[x.id];
    (groups[c]=groups[c]||[]).push(x.dominantM3);});
  let hit=0,tot=0;
  for(const c in groups){const arr=groups[c],cnt={};
    arr.forEach(g=>cnt[g]=(cnt[g]||0)+1);
    hit+=Math.max(...Object.values(cnt)); tot+=arr.length;}
  return tot?Math.round(100*hit/tot):0;
}

function runSpectral(){
  const ids=N.filter(x=>x.layer!=='VOCAB').map(x=>x.id);   // structure lives below the vocabulary
  specLabels={}; N.forEach(x=>specLabels[x.id]='·');
  const lab=spectralClusters(ids,state.spectral.k);
  ids.forEach(id=>specLabels[id]=lab[id]);
  const pur=grammarRecovery(specLabels);
  document.getElementById('specReadout').innerHTML=
    `<b style="color:#cfe0ff">${state.spectral.k}</b> clusters found from usage/relational edges only `+
    `(classificatory edges hidden — they'd leak the answer). Match to declared grammar: `+
    `<b style="color:#9fe0b0">${pur}%</b>. <span style="color:var(--dim)">Slide k up to sharpen. `+
    `High = grammar is real in the topology (Territory); the gap is a δ₁ Map/Territory signal.</span>`;
}
const pos={};
// CANOPY arrangement: a spanning forest rooted at the observer. Each subtree grows radially
// outward as a "tree" — children placed near their parent's direction with a spread that
// tightens with depth (so a trunk forms, leaves fan at the tip). Top-level trees are spread
// over the whole sphere (Fibonacci). Radial distance = height along the trunk.
/* Containment for the fold tree. In these triples the OBJECT is the container and the
   SUBJECT is the contained: `TrophicPyramid appliesToDomains Biology` means the M0
   instance *uses* the M1 extension, so Biology is the parent, never the child. The tree
   is therefore walked against the arrow. Relations absent from this map are lateral
   (relatedTo, hasDominantM3…) and create no parent/child link at all. */
/* Containment vs. contract. The test is CARDINALITY, measured on the corpus: a relation
   that may carry several values cannot define a single parent, so it is a *contract* the
   node satisfies, not a container it sits in. `M0 appliesToDomains M1_Biology` is such a
   contract — an instance may honour several domains — so it creates no parent/child link.
   Single-valued classification relations (hasFamily, ontologyType, knowledgeField,
   parentCombo) do. subClassOf is kept despite occasional multiple inheritance (≈90% single),
   with HIERARCHY_PRIORITY breaking ties. Everything else is lateral. */
const HIERARCHY_PARENT = {
  subClassOf:'object', hasFamily:'object', ontologyType:'object',
  // Real-corpus equivalents, single-valued: m1:domain / m0:domain (legacy name
  // `knowledgeField`, rename in progress — see MIGRATION_knowledgeField_to_domain.md),
  // parentCombo, skos:broader.
  // WARNING for the future parser: key on the FULL prefixed IRI, never the local name —
  // `rdfs:domain` (101 uses) is schema plumbing, unrelated to `m1:domain` (112 uses).
};
const HIERARCHY_PRIORITY = ['subClassOf','hasFamily','ontologyType'];
// Shared spanning forest rooted at the observer. Also yields, per node, how many
// descendants it holds (descCount) and which nodes are hidden behind a collapsed one.
let treeParent={}, treeChildren={}, treeDepth={}, treeOrder=[], descCount={}, collapsedHidden=new Set();
/* Expansion policy. A node with children is open only if it was explicitly opened, or
   sits above autoOpenDepth. When the user's limit is exceeded the OLDEST expansion is
   evicted (LRU) rather than refusing the click — a refusal leaves the user stuck without
   knowing why. Ancestors of the node just opened are never evicted, otherwise opening a
   deep node would hide the node itself. */
function isExpanded(id){
  if(state.forcedClosed.has(id)) return false;
  if(state.expandOrder.indexOf(id)>=0) return true;
  return (treeDepth[id]||0) < state.autoOpenDepth;
}
function ancestorsOf(id){
  const out=new Set(); let p=treeParent[id];
  while(p!==undefined&&p!==null){ out.add(p); p=treeParent[p]; }
  return out;
}
function enforceExpandLimit(justOpened){
  if(!isFinite(state.expandLimit))return;
  const prot=ancestorsOf(justOpened); prot.add(justOpened);
  while(state.expandOrder.length>state.expandLimit){
    const i=state.expandOrder.findIndex(id=>!prot.has(id));
    if(i<0)break;
    state.forcedClosed.add(state.expandOrder[i]);
    state.expandOrder.splice(i,1);
  }
}
function buildSpanningTree(){
  // 1. every node picks ONE container, by declared relation priority (not traversal luck)
  const best={};   // child -> {parent, rank}
  E.forEach(({s,t,type})=>{
    const role=HIERARCHY_PARENT[type]; if(!role)return;
    const parent = role==='object'? t : s;
    const child  = role==='object'? s : t;
    if(parent===child||!byId[parent]||!byId[child])return;
    const rank=HIERARCHY_PRIORITY.indexOf(type); if(rank<0)return;
    if(!best[child]||rank<best[child].rank) best[child]={parent,rank};
  });
  const kidsOf={}; N.forEach(x=>kidsOf[x.id]=[]);
  Object.entries(best).forEach(([child,b])=>{ if(child!==state.focus) kidsOf[b.parent].push(child); });
  // 2. the observer is the view's root: every containment ROOT hangs off it, so chains
  //    that run outside the observer's own subtree are preserved instead of orphaned
  const roots=N.filter(x=>x.id!==state.focus && (!best[x.id]||best[x.id].parent===state.focus))
               .map(x=>x.id);
  treeParent={[state.focus]:null}; treeChildren={[state.focus]:roots.slice()};
  treeDepth={[state.focus]:0}; treeOrder=[state.focus];
  const q=[]; roots.forEach(r=>{ treeParent[r]=state.focus; treeDepth[r]=1; treeOrder.push(r); q.push(r); });
  while(q.length){const u=q.shift();(kidsOf[u]||[]).forEach(v=>{
    if(treeDepth[v]===undefined){treeDepth[v]=treeDepth[u]+1;treeParent[v]=u;
      (treeChildren[u]=treeChildren[u]||[]).push(v);treeOrder.push(v);q.push(v);}});}
  // 3. anything still unreached (a containment cycle) becomes a top-level neighbour
  N.forEach(x=>{ if(treeDepth[x.id]===undefined){treeDepth[x.id]=1;treeParent[x.id]=state.focus;
    treeChildren[state.focus].push(x.id);treeOrder.push(x.id);}});
  descCount={};
  treeOrder.slice().reverse().forEach(u=>{ let c=0;
    (treeChildren[u]||[]).forEach(v=>c+=1+(descCount[v]||0)); descCount[u]=c; });
  // Folding is DERIVED from the expansion policy, never stored — so the user's limit
  // can't be silently exceeded by an earlier action.
  state.collapsed=new Set();
  N.forEach(x=>{ if((treeChildren[x.id]||[]).length && !isExpanded(x.id)) state.collapsed.add(x.id); });
  collapsedHidden=new Set();
  treeOrder.forEach(u=>{ if(!state.collapsed.has(u))return;
    const s=[...(treeChildren[u]||[])];
    while(s.length){const v=s.pop(); collapsedHidden.add(v); (treeChildren[v]||[]).forEach(w=>s.push(w));}});
}
function canopyLayout(){
  buildSpanningTree();
  const depth=treeDepth, childrenOf=treeChildren, order=treeOrder;
  const dir={}; dir[state.focus]=new BABYLON.Vector3(0,1,0);
  const top=childrenOf[state.focus]||[], GA=Math.PI*(3-Math.sqrt(5));
  top.forEach((id,i)=>{ const y=1-(i+0.5)/top.length*2, rad=Math.sqrt(Math.max(0,1-y*y)), th=GA*i;
    dir[id]=new BABYLON.Vector3(Math.cos(th)*rad,y,Math.sin(th)*rad); });
  order.forEach(id=>{ if(dir[id])return;
    const pd=dir[treeParent[id]]||new BABYLON.Vector3(0,1,0), spread=0.6/Math.max(1,depth[id]);
    const off=new BABYLON.Vector3(hash(id+'x')-0.5,hash(id+'y')-0.5,hash(id+'z')-0.5).scale(spread*2);
    dir[id]=pd.add(off).normalize(); });
  radialOf={}; N.forEach(x=>radialOf[x.id]=depth[x.id]);
  if(state.radial!=='tree'){ computeRadial(); }   // canopy gives DIRECTION; radial axis gives DISTANCE
  N.forEach(x=>{ const r=R0+radialOf[x.id]*SHELL*0.85; pos[x.id]=dir[x.id].scale(r); });
}
/* Stratified cone (the "genesis" view): the observer stands at the apex — inside M3 —
   looking down the axis toward M0. Each slice is a disc; the cone widens because
   cardinality grows with depth (few foundations → many instances), which is the same
   b^d vs r² pressure that saturates concentric shells. Works with any radial axis:
   the axis chooses what a slice *is*, the cone only stacks and widens them. */
let coneSlices=[];
function coneLayout(){
  buildSpanningTree();
  if(state.radial==='tree'){ radialOf={}; N.forEach(x=>radialOf[x.id]=treeDepth[x.id]); }
  else computeRadial();
  const groups={};
  N.forEach(x=>{ const k=Math.max(0,Math.round(radialOf[x.id]||0)); (groups[k]=groups[k]||[]).push(x); });
  const GA=Math.PI*(3-Math.sqrt(5));
  coneSlices=[];
  let prevRad=0;
  Object.keys(groups).map(Number).sort((a,b)=>a-b).forEach((k,ki)=>{
    const arr=groups[k].slice().sort((a,b)=>String(facetVal(a)).localeCompare(String(facetVal(b)))
      || a.label.localeCompare(b.label));
    const n=arr.length, z=R0+4+ki*SHELL*1.6;
    const rad=Math.max(prevRad*1.15, 3.5+ki*4.2, 2.6*Math.sqrt(n));
    prevRad=rad;
    // a stratum is one giant cluster made of sub-clusters (keyed by the active facet):
    // on real data M0's sub-clusters are the individual instance files.
    const sub={}; arr.forEach(x=>{ const k=String(facetVal(x)); (sub[k]=sub[k]||[]).push(x); });
    const keys=Object.keys(sub).sort(), m=keys.length;
    keys.forEach((key,ci)=>{
      const cl=sub[key], cn=cl.length;
      const cR=(m===1)?0:rad*0.60*Math.sqrt((ci+0.5)/m), cT=GA*ci;
      const cx=cR*Math.cos(cT), cy=cR*Math.sin(cT);
      const sr=Math.min(rad*0.33,Math.max(1.5,1.45*Math.sqrt(cn)));
      cl.forEach((x,i)=>{
        const rr=(cn===1)?0:sr*Math.sqrt((i+0.5)/cn), th=GA*i;
        pos[x.id]=new BABYLON.Vector3(cx+rr*Math.cos(th),cy+rr*Math.sin(th),z);
      });
    });
    coneSlices.push({k,z,rad,n,clusters:m,label:sliceLabel(k,arr)});
  });
}
function sliceLabel(k,arr){
  if(state.radial==='meta'){ const L=['M3','M2','M1','M0','vocab']; return L[k]||('L'+k); }
  const c={}; arr.forEach(x=>c[x.layer]=(c[x.layer]||0)+1);
  const dom=Object.entries(c).sort((a,b)=>b[1]-a[1])[0];
  return (state.radial==='tree'?'depth ':'level ')+k+(dom?' · mostly '+dom[0]:'');
}
/* Nautilus shell (borrowed from the M0_Ptoe poclet). Each stratum is one coil of a
   logarithmic spiral r = A·e^(B·2πt). Unlike concentric shells — whose perimeter grows
   only linearly in r — a log spiral's perimeter grows by a constant FACTOR per turn
   (~×1.6 here), i.e. geometrically, which is exactly the b^d growth of a branching
   hierarchy. It absorbs saturation the way hyperbolic space does, by other means. */
const NAU_A=6, NAU_B=0.075, NAU_TF=0.30, NAU_H=1.5;
const nauR=t=>NAU_A*Math.exp(NAU_B*2*Math.PI*t);
function nautilusLayout(){
  buildSpanningTree();
  if(state.radial==='tree'){ radialOf={}; N.forEach(x=>radialOf[x.id]=treeDepth[x.id]); }
  else computeRadial();
  const groups={};
  N.forEach(x=>{ const k=Math.max(0,Math.round(radialOf[x.id]||0)); (groups[k]=groups[k]||[]).push(x); });
  const GA=Math.PI*(3-Math.sqrt(5));
  coneSlices=[];
  Object.keys(groups).map(Number).sort((a,b)=>a-b).forEach((k,ki)=>{
    const arr=groups[k].slice().sort((a,b)=>String(facetVal(a)).localeCompare(String(facetVal(b)))
      || a.label.localeCompare(b.label));
    const n=arr.length;
    arr.forEach((x,i)=>{
      const t=ki+(i+0.5)/n;                       // position along the coil
      const th=-2*Math.PI*t, r=nauR(t), tr=NAU_TF*r;
      const nx=Math.cos(th), nz=Math.sin(th);
      const phi=GA*i;                             // wrap around the tube cross-section
      pos[x.id]=new BABYLON.Vector3(
        r*nx+tr*Math.cos(phi)*nx, tr*Math.sin(phi)*NAU_H, r*nz+tr*Math.cos(phi)*nz);
    });
    const rm=nauR(ki+0.5);
    coneSlices.push({k,z:0,rad:rm,n,clusters:new Set(arr.map(x=>String(facetVal(x)))).size,
      label:sliceLabel(k,arr),coil:ki});
  });
}
function layout(){
  if(state.arrangement==='canopy'){ canopyLayout(); return; }
  if(state.arrangement==='cone'){ coneLayout(); return; }
  if(state.arrangement==='nautilus'){ nautilusLayout(); return; }
  buildSpanningTree();          // collapse works in both arrangements
  computeRadial();
  // sector centres from distinct facet values
  const vals=[...new Set(N.map(facetVal))];
  const secIdx={}; vals.forEach((v,i)=>secIdx[v]=i);
  const nSec=vals.length, secW=2*Math.PI/nSec;
  N.forEach(x=>{
    const r=R0+radialOf[x.id]*SHELL;
    const sc=secIdx[facetVal(x)]*secW + secW/2;
    const theta=sc + (hash(x.id)-0.5)*secW*0.82;
    const phi=0.10*Math.PI + hash(x.id+'φ')*0.80*Math.PI;   // full sphere: nodes all around you
    pos[x.id]=new BABYLON.Vector3(
      r*Math.sin(phi)*Math.cos(theta), r*Math.cos(phi), r*Math.sin(phi)*Math.sin(theta));
  });
}

/* ---- 5. BABYLON SCENE ----------------------------------------------------- */
const canvas=document.getElementById('c');
const engine=new BABYLON.Engine(canvas,true,{preserveDrawingBuffer:true,stencil:true},true);
const scene=new BABYLON.Scene(engine);
scene.clearColor=new BABYLON.Color4(0,0,0,0);
// ASTRONAUT observer: a first-person camera fixed AT the centre, no horizon. Dragging turns
// the head in place (a node you turn away from passes behind you); look up, down, or behind.
// The jetpack (Teleport) jumps the vantage to any star. Scroll narrows the solid angle.
const cam=new BABYLON.FreeCamera('cam',new BABYLON.Vector3(0,0,0.0001),scene);
cam.minZ=0.01; cam.maxZ=2400; cam.fov=1.05;
let yaw=0.6, pitch=0.0;                         // free look: azimuth + pitch, full sphere, no horizon
function applyCam(){
  const cp=Math.cos(pitch),sp=Math.sin(pitch);
  const dir=new BABYLON.Vector3(cp*Math.sin(yaw),sp,cp*Math.cos(yaw));
  cam.setTarget(cam.position.add(dir));
}
applyCam();
new BABYLON.HemisphericLight('h',new BABYLON.Vector3(0,1,0),scene).intensity=0.55;
// key light: gives each face of a polyhedron a different brightness, so solids read as solids
(function(){ const k=new BABYLON.DirectionalLight('key',new BABYLON.Vector3(-0.5,-0.75,0.42),scene);
  k.intensity=1.15; k.diffuse=new BABYLON.Color3(1,0.97,0.9); })();
const glow=new BABYLON.GlowLayer('glow',scene); glow.intensity=0.9;

// Procedural galactic backdrop — drawn to a DynamicTexture (no external asset, stays
// serverless) and mapped inside a sky dome. infiniteDistance keeps it centred on the
// observer, so flying with the jetpack never reaches it.
(function skydome(){
  const W=2048,H=1024;
  const dt=new BABYLON.DynamicTexture('skyTex',{width:W,height:H},scene,false);
  const c=dt.getContext();
  c.fillStyle='#04060d'; c.fillRect(0,0,W,H);
  const bandY=x=>H*0.5+Math.sin(x/W*Math.PI*2)*H*0.13;
  // draw everything three times across the UV wrap so no hard seam runs down the sky
  const wrap=(x,fn)=>{ fn(x); fn(x-W); fn(x+W); };
  // The background must NOT borrow the nodes' visual vocabulary — no disc large enough or
  // warm enough to read as a concept glyph. So: stars are POINTS only, never tinted warm;
  // nebulae are broad, faint, edgeless washes, never crisp coloured blobs.
  const wash=(x,y,r,rgb,a)=>wrap(x,px=>{
    const g=c.createRadialGradient(px,y,0,px,y,r);
    g.addColorStop(0,'rgba('+rgb+','+a+')'); g.addColorStop(1,'rgba('+rgb+',0)');
    c.fillStyle=g; c.beginPath(); c.arc(px,y,r,0,7); c.fill(); });
  // Milky Way band — a broad diffuse glow, cool blue-grey only
  for(let i=0;i<460;i++){
    const x=Math.random()*W, y=bandY(x)+(Math.random()-0.5)*H*0.18;
    wash(x,y,60+Math.random()*160,'120,140,200',0.04);
  }
  // dust lanes threading the band (dark, subtractive)
  for(let i=0;i<110;i++){
    const x=Math.random()*W, y=bandY(x)+(Math.random()-0.5)*H*0.08;
    wash(x,y,40+Math.random()*110,'4,6,13',0.28);
  }
  // a couple of faint "pillars of creation"-style nebulae — very large, very soft, low alpha,
  // muted teal/rose so they never approach the saturated hues of the glyphs
  [[W*0.30,H*0.36,'92,150,150'],[W*0.74,H*0.66,'150,110,140']].forEach(([nx,ny,rgb])=>{
    for(let i=0;i<90;i++){
      const a=Math.random()*7, d=Math.random()*150;
      wash(nx+Math.cos(a)*d, ny+Math.sin(a)*d*0.8, 30+Math.random()*70, rgb, 0.022);
    }
  });
  // stars: points only. Radius ≤ 1.3px, never warm — cool white to faint blue, so none can
  // be mistaken for a body. Denser along the band.
  for(let i=0;i<5200;i++){
    let x=Math.random()*W,y;
    if(Math.random()<0.6) y=bandY(x)+(Math.random()-0.5)*H*0.22; else y=Math.random()*H;
    const b=Math.random(), rad=b>0.992?1.3:b>0.9?0.9:0.55;
    const tint=b>0.95?'210,224,255':'255,255,255';   // white or faint blue, never yellow
    c.fillStyle=`rgba(${tint},${0.20+b*0.55})`;
    wrap(x,px=>{ c.beginPath(); c.arc(px,y,rad,0,7); c.fill(); });
  }
  dt.update();
  dt.wrapU=BABYLON.Texture.WRAP_ADDRESSMODE;
  dt.wrapV=BABYLON.Texture.CLAMP_ADDRESSMODE;
  const sky=BABYLON.MeshBuilder.CreateSphere('sky',
    {diameter:900,segments:64,sideOrientation:BABYLON.Mesh.BACKSIDE},scene);
  const sm=new BABYLON.StandardMaterial('skyM',scene);
  sm.disableLighting=true; sm.emissiveTexture=dt;
  sm.diffuseColor=new BABYLON.Color3(0,0,0); sm.specularColor=new BABYLON.Color3(0,0,0);
  sky.material=sm; sky.isPickable=false; sky.infiniteDistance=true; sky.renderingGroupId=0;
  scene.skyMesh=sky;
})();

/* ---- node GLYPHS: shape = kind, colour = facet-or-kind, ring = a relational flag ---- */
function kindOf(x){
  if(x.layer==='VOCAB') return 'vocab';
  if(x.layer==='m3') return 'foundation';
  if(x.id==='GenericConcept'||x.id==='GenericConceptFamily') return 'root';
  if(x.family==='Combo') return /Domain/.test(x.id) ? 'domainCombo' : 'combo';
  if(x.layer==='m2' && x.dominantM3) return 'concept';
  if(x.layer==='m2') return 'family';
  if(x.layer==='m1') return 'domainConcept';
  if(x.layer==='m0') return 'instance';
  return 'other';
}
const SHAPE_OPTIONS=['sphere','cube','tetra','octa','ico','dodeca'];
function makeShape(shape){
  switch(shape){
    case 'cube':   return BABYLON.MeshBuilder.CreateBox('g',{size:0.95},scene);
    case 'tetra':  return BABYLON.MeshBuilder.CreatePolyhedron('g',{type:0,size:0.62},scene);
    case 'octa':   return BABYLON.MeshBuilder.CreatePolyhedron('g',{type:1,size:0.66},scene);
    case 'ico':    return BABYLON.MeshBuilder.CreateIcoSphere('g',{radius:0.6,subdivisions:1},scene);
    case 'dodeca': return BABYLON.MeshBuilder.CreatePolyhedron('g',{type:2,size:0.55},scene);
    default:       return BABYLON.MeshBuilder.CreateSphere('g',{segments:10,diameter:1},scene);
  }
}
// Globe wireframe for spheres: one equator + four polar great circles (= 8 meridians).
// A sphere has no sharp edges for edge-rendering to find (tessellation facets are near
// coplanar), so the wireframe is emulated with explicit lines.
function sphereGuides(id,radius,col){
  const SEG=44, lines=[];
  const eq=[]; for(let i=0;i<=SEG;i++){ const a=2*Math.PI*i/SEG;
    eq.push(new BABYLON.Vector3(radius*Math.cos(a),0,radius*Math.sin(a))); }
  lines.push(eq);
  [0,Math.PI/4,Math.PI/2,3*Math.PI/4].forEach(az=>{ const mer=[];
    for(let i=0;i<=SEG;i++){ const a=2*Math.PI*i/SEG;
      mer.push(new BABYLON.Vector3(radius*Math.sin(a)*Math.cos(az),radius*Math.cos(a),radius*Math.sin(a)*Math.sin(az))); }
    lines.push(mer); });
  const ls=BABYLON.MeshBuilder.CreateLineSystem('gw_'+id,{lines},scene);
  ls.color=col; ls.alpha=0.8; ls.isPickable=false;
  return ls;
}
const meshes={};
function buildNodeMeshes(){
  Object.values(meshes).forEach(m=>m.dispose());   // disposes child rings too
  for(const k in meshes) delete meshes[k];
  N.forEach(x=>{
    const g=GLYPHS[kindOf(x)]||GLYPHS.other;
    const m=makeShape(g.shape); m.name='n_'+x.id;
    const mat=new BABYLON.StandardMaterial('m_'+x.id,scene);
    // lit, not flat-emissive: with lighting off a tetrahedron just reads as a flat triangle
    mat.disableLighting=false;
    mat.specularColor=new BABYLON.Color3(0.14,0.14,0.16); mat.specularPower=24;
    m.material=mat; m.metadata={id:x.id}; meshes[x.id]=m;
    const ec=BABYLON.Color3.FromHexString(g.hue);
    const wire=new BABYLON.Color4(Math.min(1,ec.r+0.4),Math.min(1,ec.g+0.4),Math.min(1,ec.b+0.4),0.8);
    if(g.shape==='sphere'){
      // a sphere has no edges to render — give it a globe wireframe: equator + 4 meridians
      m.addChild(sphereGuides(x.id,0.5,new BABYLON.Color3(wire.r,wire.g,wire.b)));
    }else{
      m.enableEdgesRendering(); m.edgesWidth=1.6; m.edgesColor=wire;
    }
    if(g.ring){
      const ring=BABYLON.MeshBuilder.CreateTorus('ring_'+x.id,
        {diameter:1.9,thickness:0.09,tessellation:g.ring==='square'?4:28},scene);
      ring.parent=m; ring.rotation.x=Math.PI/2; ring.isPickable=false;
      const rmat=new BABYLON.StandardMaterial('rm_'+x.id,scene);
      rmat.disableLighting=true; rmat.emissiveColor=BABYLON.Color3.FromHexString('#cfe0ff'); rmat.alpha=0.9;
      ring.material=rmat;
    }
  });
}
buildNodeMeshes();

/* edge lines (built once, toggled) */
let edgeMeshes=[];
function buildEdges(){
  edgeMeshes.forEach(l=>l.dispose()); edgeMeshes=[];
  E.forEach(ed=>{
    const l=BABYLON.MeshBuilder.CreateLines('e',{points:[pos[ed.s],pos[ed.t]]},scene);
    l.color=BABYLON.Color3.FromHexString(REL_COLORS[ed.type]||'#39466a');
    l.alpha=0.5; l.isPickable=false; l.metadata=ed; edgeMeshes.push(l);
  });
}

/* ---- 6. VISIBILITY / MAGNITUDE / CONE ------------------------------------ */
let hoverId=null;
function nodeVisible(x){
  if(x.id===state.focus) return false;          // the observer is standing on this node
  if(collapsedHidden.has(x.id)) return false;   // folded away behind a collapsed ancestor
  if(state.slice!==null && state.arrangement==='cone'
     && Math.max(0,Math.round(radialOf[x.id]||0))!==state.slice) return false;
  if(x.layer==='VOCAB' && !state.showVocab) return false;
  if(radialOf[x.id] > state.depth) return false;
  if(magnitude(x) < state.magFloor) return false;
  return true;
}
function magnitude(x){
  // a collapsed node is a dense body: its brightness announces how much it holds
  if(state.collapsed.has(x.id)&&descCount[x.id])
    return Math.min(9,4+Math.round(Math.log2(1+descCount[x.id])*1.4));
  return magOf[x.id]||0;
}
function inCone(p){
  if(!p) return false;
  const fwd=cam.getForwardRay().direction;
  const dir=p.subtract(cam.position).normalize();
  const ang=Math.acos(Math.max(-1,Math.min(1,BABYLON.Vector3.Dot(fwd,dir))))*180/Math.PI;
  return ang <= state.coneDeg/2;
}
function applyVisual(){
  const neigh=hoverId?new Set(E.filter(x=>x.s===hoverId||x.t===hoverId).flatMap(x=>[x.s,x.t])):null;
  N.forEach(x=>{
    const m=meshes[x.id]; if(!m)return;
    const vis=nodeVisible(x) && !!pos[x.id];
    m.setEnabled(vis); if(!vis)return;
    const cone=inCone(pos[x.id]);
    const mg=magnitude(x);
    const d=0.34 + 0.9*(mg/9);           // size by magnitude
    m.scaling.setAll(d * (x.id===state.focus?1.5:1));
    const col=BABYLON.Color3.FromHexString(colorOf(x));
    const emph=hoverId? (x.id===hoverId?1.35:(neigh.has(x.id)?1.0:0.14))
                      : (cone?1.0:0.5);
    const folded=state.collapsed.has(x.id);
    m.material.diffuseColor=col.scale(0.55+0.45*Math.min(1,emph));
    m.material.emissiveColor=col.scale((folded?0.34:0.12)+0.30*emph);
    m.material.alpha=cone?1:0.62;
    m.position=pos[x.id];
  });
  // edges: type enabled + both ends visible + (in cone OR incident to hover)
  edgeMeshes.forEach(l=>{
    const ed=l.metadata, a=byId[ed.s], b=byId[ed.t];
    let on=state.rels[ed.type] && nodeVisible(a) && nodeVisible(b);
    if(on){
      const local=inCone(pos[ed.s])||inCone(pos[ed.t]);
      const hl=hoverId&&(ed.s===hoverId||ed.t===hoverId);
      on = local||hl;
      l.alpha = hl?0.85:(local?state.edgeAlpha:0);
    }
    l.setEnabled(on);
  });
}


/* ---- 8. INTERACTION ------------------------------------------------------- */
const tip=document.getElementById('tip');
let lastClickId=null, lastClickT=0;
function setCenter(id){ state.focus=id;
  document.getElementById('focusName').textContent=byId[id].label;
  const o=document.getElementById('obsName'); if(o)o.textContent=byId[id].label;
  cam.position=new BABYLON.Vector3(0,0,0.0001); applyCam();  // stand ON the new centre
  if(typeof updateDolly==='function') updateDolly();
  relayout();
  // teleport is a one-shot: uncheck it so the next click doesn't teleport again
  if(state.selectCenter){ state.selectCenter=false;
    const cb=document.getElementById('selCenter'); if(cb)cb.checked=false;
    canvas.style.cursor='default'; }
}
function pickMeshAt(e){ const r=canvas.getBoundingClientRect();
  const hit=scene.pick(e.clientX-r.left,e.clientY-r.top,m=>m.metadata&&m.metadata.id);
  return hit&&hit.hit?hit.pickedMesh:null; }
function pickAt(e){ const m=pickMeshAt(e); return m?m.metadata.id:null; }
// tolerant pick: the exact ray can miss a small distant glyph, so fall back to the nearest
// visible node within a few pixels of the cursor. Used for right-click, which must not miss.
function pickNear(e,px=16){
  const direct=pickAt(e); if(direct)return direct;
  const r=canvas.getBoundingClientRect(), sx=e.clientX-r.left, sy=e.clientY-r.top;
  const W=engine.getRenderWidth(),H=engine.getRenderHeight();
  let best=null,bd=px*px;
  N.forEach(x=>{ const m=meshes[x.id]; if(!m||!m.isEnabled()||!pos[x.id])return;
    const p=BABYLON.Vector3.Project(pos[x.id],BABYLON.Matrix.Identity(),
      scene.getTransformMatrix(),cam.viewport.toGlobal(W,H));
    const v=BABYLON.Vector3.TransformCoordinates(pos[x.id],scene.getViewMatrix());
    if(v.z<=0)return;
    const dx=p.x-sx,dy=p.y-sy,d=dx*dx+dy*dy;
    if(d<bd){bd=d;best=x.id;} });
  return best;
}
function toggleFold(id){
  if(!id||!(treeChildren[id]||[]).length)return false;
  const i=state.expandOrder.indexOf(id);
  if(isExpanded(id)){
    state.forcedClosed.add(id);
    if(i>=0) state.expandOrder.splice(i,1);
  }else{
    state.forcedClosed.delete(id);
    if(i>=0) state.expandOrder.splice(i,1);
    state.expandOrder.push(id);
    enforceExpandLimit(id);
  }
  relayout(); return true;
}

(function firstPersonControls(){
  let drag=false,lx=0,ly=0,moved=0;
  canvas.addEventListener('pointerdown',e=>{
    if(e.button===2){                          // right button → context menu, here (button is reliable)
      const id = hoverId || pickNear(e);
      tip.style.display='none';
      // TEMP DIAGNOSTIC — surfaced on screen because the console shows nothing
      const dbg=$('tip');
      dbg.style.display='block'; dbg.style.left=(e.clientX+14)+'px'; dbg.style.top=(e.clientY-40)+'px';
      dbg.innerHTML=`<b style="color:#e6c94b">right-click debug</b><br>hoverId: ${hoverId||'∅'}<br>`
        +`pickNear: ${pickNear(e)||'∅'}<br>resolved: ${id||'∅'} → ${id?'OPEN':'no target, aborted'}`;
      if(id){ ctxJustOpened=true; openCtxMenu(e,id); }
      return;
    }
    const pm=pickMeshAt(e);
    if(pm && pm.metadata.stub){ jumpToSlice(pm.metadata.id); return; }        // hypertext jump
    drag=true; lx=e.clientX; ly=e.clientY; moved=0;
    const id=pm?pm.metadata.id:null, now=performance.now();
    if(id && state.selectCenter && id===lastClickId && now-lastClickT<340) setCenter(id); // double-click
    lastClickId=id; lastClickT=now;
  });
  addEventListener('pointerup',()=>{drag=false;});
  addEventListener('pointermove',e=>{
    if($('ctxmenu') && $('ctxmenu').style.display==='block') return;  // menu open: freeze hover
    if(drag){ const dx=e.clientX-lx,dy=e.clientY-ly; lx=e.clientX; ly=e.clientY; moved+=Math.abs(dx)+Math.abs(dy);
      yaw-=dx*0.0042; pitch-=dy*0.0042; pitch=Math.max(-1.52,Math.min(1.52,pitch)); applyCam();
      hoverId=null; tip.style.display='none'; return; }
    // hover / inspect (only when not dragging)
    const id=pickAt(e);
    if(id!==hoverId){ hoverId=id; applyVisual(); }
    if(id){ const x=byId[id], rels=E.filter(z=>z.s===id||z.t===id);
      tip.style.display='block';
      tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+12)+'px';
      tip.innerHTML=`<div class="t">${x.label}</div><div class="m">`+
        `<i>layer</i> ${x.layer} &nbsp; <i>vocab</i> ${x.vocab}<br>`+
        (x.family?`<i>family</i> ${x.family}<br>`:'')+
        (x.dominantM3?`<i>grammar</i> ${x.dominantM3}<br>`:'')+
        (x.ontologyType&&x.ontologyType!=='—'?`<i>type</i> ${x.ontologyType}<br>`:'')+
        `<i>links</i> ${rels.length} &nbsp; <i>magnitude</i> ${magnitude(x)}`+
        ((treeChildren[id]||[]).length
          ? (isExpanded(id)
              ? `<br><i style="color:#7f8ca8">${descCount[id]} descendants, open</i>`
              : `<br><i style="color:#e6c94b">◆ folded · ${descCount[id]} hidden</i>`)
          : '')+
        `<br><i style="color:#9fb0d0">right-click for actions</i></div>`;
    } else tip.style.display='none';
  });
  // right-click folds / unfolds a subtree (sober expand-collapse)
  // suppress the native browser menu; our menu opens on the right-button pointerdown above
  canvas.addEventListener('contextmenu',e=>e.preventDefault());
  // WHEEL = ZOOM (the instrument's field of view). Movement belongs to the keyboard:
  // changing focal length and changing position are not the same act.
  canvas.addEventListener('wheel',e=>{
    cam.fov=Math.max(0.35,Math.min(1.9,cam.fov+(e.deltaY>0?0.08:-0.08)));
    updateInstrument(); e.preventDefault(); },{passive:false});
})();

/* ---- 9. CONTROL PANEL WIRING --------------------------------------------- */
function relayout(){ rebuildFacetColors(); layout(); buildEdges(); buildSlices(); buildStubs(); buildLegend(); applyVisual();
  if(typeof updateFoldReadout==='function') updateFoldReadout(); }
const $=id=>document.getElementById(id);
$('radial').onchange=e=>{state.radial=e.target.value;
  $('vRadial').textContent={tree:'tree depth',subclass:'specialization',meta:'meta-level',hops:'hops',trophic:'trophic flow'}[state.radial]; relayout();};
$('facet').onchange=e=>{state.facet=e.target.value;
  $('vFacet').textContent=e.target.selectedOptions[0].text.split(' (')[0].toLowerCase(); relayout();};
$('colorBy').onchange=e=>{state.colorBy=e.target.value;
  $('vColorBy').textContent=e.target.value; relayout();};
$('spectralT').onchange=e=>{state.spectral.on=e.target.checked;
  $('kclusters').disabled=!e.target.checked;
  $('facet').disabled=e.target.checked;
  if(state.spectral.on){ $('vFacet').textContent='spectral clusters';
    state.colorBy='facet'; $('colorBy').value='facet'; $('vColorBy').textContent='facet'; runSpectral(); }
  else{ state.facet=$('facet').value; $('vFacet').textContent=$('facet').selectedOptions[0].text.split(' (')[0].toLowerCase();
    $('specReadout').innerHTML='Ignores declared facets. Builds the normalized graph Laplacian, '+
      'power-iterates its low modes, k-means on the embedding — then colours by the clusters it '+
      '<i>finds on its own</i>.'; }
  relayout();};
$('kclusters').oninput=e=>{state.spectral.k=+e.target.value;$('vK').textContent=state.spectral.k;
  if(state.spectral.on){runSpectral();relayout();}};
function updateInstrument(){
  const fov=cam.fov;
  state.coneDeg=fov*180/Math.PI;                       // the emphasis cone IS the field of view
  const t=(fov-0.35)/(1.9-0.35);                        // 0 = telescope … 1 = naked eye
  state.magFloor=state.showAll?0:Math.round(t*4);       // naked eye: bright only; telescope: reveal faint
  $('vInstr').textContent = fov>1.4?'naked eye':fov>0.8?'binoculars':'telescope';
  const sl=$('instr'); if(sl) sl.value=Math.round(fov*100);
  $('instrReadout').textContent =
    `field ${Math.round(state.coneDeg)}° · seeing mag ≥ ${state.magFloor}${state.magFloor===0?' (all)':''}`
    + ` · showing ${N.filter(nodeVisible).length}/${N.length} nodes`;
  applyVisual(); buildLegend();
}
$('arr').onchange=e=>{state.arrangement=e.target.value;
  $('vArr').textContent={canopy:'canopy',clusters:'clusters',cone:'cone',nautilus:'nautilus'}[e.target.value];
  if(e.target.value!=='canopy' && state.radial==='tree'){ state.radial='hops'; $('radial').value='hops'; $('vRadial').textContent='hops'; }
  if(e.target.value==='cone'){                   // stand at the apex, look down the axis
    state.radial='meta'; $('radial').value='meta'; $('vRadial').textContent='meta-level';
    yaw=0; pitch=0; cam.position=new BABYLON.Vector3(0,0,0.0001); applyCam(); updateDolly();
  } else { state.slice=null; }
  if(e.target.value==='nautilus'){               // start at the umbilicus, looking outward
    state.radial='meta'; $('radial').value='meta'; $('vRadial').textContent='meta-level';
    yaw=0; pitch=0.25; cam.position=new BABYLON.Vector3(0,0,0.0001); applyCam(); updateDolly();
  }
  $('coneGrp').style.display=(e.target.value==='cone')?'':'none';
  relayout();};
$('scaf').oninput=e=>{state.edgeAlpha=(+e.target.value)/100;$('vScaf').textContent=e.target.value+'%';applyVisual();};
$('instr').oninput=e=>{ cam.fov=(+e.target.value)/100; updateInstrument(); };
$('depth').oninput=e=>{state.depth=+e.target.value;
  $('vDepth').textContent=state.depth>=7?'all':'≤ '+state.depth;applyVisual();buildLegend();};
$('expandLimit').onchange=e=>{
  state.expandLimit = e.target.value==='inf'?Infinity:+e.target.value;
  if(state.expandOrder.length) enforceExpandLimit(state.expandOrder[state.expandOrder.length-1]);
  relayout(); };
$('foldDepth').onclick=()=>{ state.expandOrder=[]; state.forcedClosed=new Set();
  state.autoOpenDepth=1; relayout(); };
$('foldClear').onclick=()=>{ state.expandOrder=[]; state.forcedClosed=new Set();
  state.autoOpenDepth=99; state.expandLimit=Infinity; $('expandLimit').value='inf'; relayout(); };
function updateFoldReadout(){
  const open=N.filter(x=>(treeChildren[x.id]||[]).length&&isExpanded(x.id)).length;
  const lim=isFinite(state.expandLimit)?state.expandLimit:'∞';
  $('vFold').textContent=`${open} open / ${lim} · ${collapsedHidden.size} hidden`;
}
$('slicePrev').onclick=()=>shiftSlice(-1);
$('sliceNext').onclick=()=>shiftSlice(1);
$('sliceAll').onclick=()=>setSlice(null);
$('travelBack').onclick=()=>travel(-1);
$('travelFwd').onclick=()=>travel(1);
$('showAll').onchange=e=>{state.showAll=e.target.checked;updateInstrument();relayout();};
$('vocabT').onchange=e=>{state.showVocab=e.target.checked;relayout();};
$('selCenter').onchange=e=>{state.selectCenter=e.target.checked;
  canvas.style.cursor=e.target.checked?'crosshair':'default';};

// relation-type checkboxes
const relsEl=$('rels');
REL_TYPES.filter(t=>!['a','authoredBy'].includes(t)).forEach(t=>{
  const l=document.createElement('label'); l.className='chk';
  l.innerHTML=`<input type="checkbox" ${state.rels[t]?'checked':''}>`+
    `<span class="sw" style="background:${REL_COLORS[t]||'#39466a'}"></span>${t}`;
  l.querySelector('input').onchange=ev=>{state.rels[t]=ev.target.checked;
    if(state.radial==='hops')relayout(); else applyVisual();};
  relsEl.appendChild(l);
});
const FACET_NAME={dominantM3:'grammar',family:'family',layer:'layer',ontologyType:'type',vocab:'vocabulary'};
function buildLegend(){
  const box=$('legendBox'); if(!box)return;
  const present=new Set(N.filter(nodeVisible).map(kindOf));
  let h='';
  // point symbols: shape = kind
  h+='<div class="lgh">bodies · shape = kind</div>';
  Object.entries(STYLESHEET.nodes.kinds).forEach(([k,g])=>{ if(!present.has(k))return;
    const ring=g.ring?` <span style="color:#7f8ca8">+${g.ring} ring</span>`:'';
    h+=`<div class="lgy"><span class="gl" style="color:${g.hue}">${SHAPE_GLYPH[g.shape]||'●'}</span>${g.label}${ring}</div>`;
  });
  // colour binding
  const cby=state.spectral.on?('spectral clusters (k='+state.spectral.k+')')
           :(state.colorBy==='kind'?'node kind':(FACET_NAME[state.facet]||state.facet));
  h+=`<div class="lgh">colour = ${cby}</div>`;
  if(state.spectral.on || state.colorBy==='facet'){
    [...new Set(N.filter(nodeVisible).map(facetVal))].forEach(v=>{
      h+=`<div class="lgy"><span class="dot" style="color:${facetColorMap[v]||'#5a6b8c'}"></span>${v}</div>`;});
  } else {
    h+='<div class="lg2">hue matches the shapes above</div>';
  }
  // line symbols: relations
  h+='<div class="lgh">relations · lines</div>';
  REL_TYPES.filter(t=>state.rels[t]&&!['a','authoredBy'].includes(t)).forEach(t=>{
    h+=`<div class="lgy"><span class="sw" style="background:${STYLESHEET.edges.colors[t]||'#39466a'}"></span>${t}</div>`;});
  // reference frame
  const rax=state.arrangement==='canopy'?'canopy · trunk height'
    :({subclass:'specialization',meta:'meta-level',hops:'hops from you',trophic:'trophic flow'}[state.radial]||state.radial);
  h+='<div class="lgh">frame</div>';
  h+=`<div class="lg2">radial: ${rax}</div>`;
  h+=`<div class="lg2">instrument: ${($('vInstr')||{}).textContent||''} · seeing mag ≥ ${state.magFloor}</div>`;
  box.innerHTML=h;
}

/* ---- 9b. 3D RADAR (Elite-style): egocentric disc + elevation stems ---------
   Pure 2D projection of the already-computed pos{} — no second engine.
   Azimuth is relative to the gaze (straight ahead = top), radial position = distance,
   vertical stem = elevation above/below the observer's horizontal plane. */
const radarCv=$('radar-canvas'), rctx=radarCv.getContext('2d');
let radarCollapsed=false;
$('radar-toggle').onclick=()=>{
  radarCollapsed=!radarCollapsed;
  $('radar-body').style.display=radarCollapsed?'none':'';
  $('radar-bar').classList.toggle('collapsed',radarCollapsed);
  $('radar-toggle').textContent=radarCollapsed?'+':'−';
  if(!radarCollapsed) drawRadar();
};
function drawRadar(){
  if(radarCollapsed)return;
  const W=radarCv.width,H=radarCv.height,cx=W/2,cy=H*0.56;
  const RX=W*0.41, RY=RX*0.40, STEM=H*0.30;
  rctx.clearRect(0,0,W,H);
  // range rings
  rctx.lineWidth=1;
  [1,0.66,0.33].forEach(f=>{ rctx.strokeStyle='rgba(110,168,255,'+(f===1?0.30:0.16)+')';
    rctx.beginPath(); rctx.ellipse(cx,cy,RX*f,RY*f,0,0,Math.PI*2); rctx.stroke(); });
  // field-of-view wedge (where you are actually looking)
  const half=state.coneDeg*Math.PI/360;
  rctx.fillStyle='rgba(110,168,255,0.11)'; rctx.beginPath(); rctx.moveTo(cx,cy);
  for(let a=-half;a<=half;a+=0.04) rctx.lineTo(cx+Math.sin(a)*RX, cy-Math.cos(a)*RY);
  rctx.closePath(); rctx.fill();
  // observer
  rctx.fillStyle='#cfe0ff'; rctx.beginPath(); rctx.arc(cx,cy,2,0,Math.PI*2); rctx.fill();
  // contacts
  let maxR=1;
  N.forEach(x=>{ if(nodeVisible(x)&&pos[x.id]) maxR=Math.max(maxR,pos[x.id].subtract(cam.position).length()); });
  let count=0, observed=0;
  N.forEach(x=>{
    if(!nodeVisible(x)||!pos[x.id])return;
    const p=pos[x.id].subtract(cam.position), dist=p.length();
    const rel=Math.atan2(p.x,p.z)-yaw;                       // azimuth relative to gaze
    const elev=Math.atan2(p.y,Math.hypot(p.x,p.z));          // −π/2 … +π/2
    const f=Math.min(1,dist/maxR);
    const px=cx+Math.sin(rel)*RX*f, py=cy-Math.cos(rel)*RY*f;
    const ty=py-(elev/(Math.PI/2))*STEM;
    const mg=magnitude(x), hot=(x.id===hoverId), aim=(x.id===aimedId);
    const inFov=inCone(pos[x.id]); if(inFov) observed++;     // caught by the instrument's cone
    rctx.strokeStyle=aim?'rgba(159,224,176,0.9)':(hot?'rgba(255,255,255,0.75)':'rgba(150,175,220,0.28)');
    rctx.beginPath(); rctx.moveTo(px,py); rctx.lineTo(px,ty); rctx.stroke();
    rctx.fillStyle=aim?'#9fe0b0':(hot?'#ffffff':colorOf(x));
    rctx.beginPath(); rctx.arc(px,ty,(aim?2.6:1.2)+mg*0.22,0,Math.PI*2); rctx.fill();
    count++;
  });
  $('radar-count').textContent=`Visible ${count} · Observed ${observed}`;
  const vt=$('vtCount'); if(vt) vt.textContent=N.length;
}
/* ---- 9c. OBJECT EXPLORER + GAZE GUIDANCE ---------------------------------- */
let aimedId=null;
function updateDolly(){
  const d=cam.position.length();
  $('vDolly').textContent = d<1?'at centre':(d.toFixed(0)+' out');
}
function buildExplorer(){
  const layer=$('expLayer').value, q=$('expSearch').value.trim().toLowerCase();
  const items=N.filter(x=>(layer==='all'||x.layer===layer) && (!q||x.label.toLowerCase().includes(q)))
               .sort((a,b)=>a.label.localeCompare(b.label));
  $('vExpCount').textContent=items.length;
  const el=$('expList'); el.innerHTML='';
  items.forEach(x=>{
    const g=STYLESHEET.nodes.kinds[kindOf(x)]||STYLESHEET.nodes.kinds.other;
    const d=document.createElement('div');
    d.className='exp'+(x.id===aimedId?' sel':'');
    d.innerHTML=`<span class="g" style="color:${g.hue}">${SHAPE_GLYPH[g.shape]||'●'}</span>${x.label}`;
    d.onclick=()=>{ aimedId=x.id; buildExplorer(); $('expCentre').disabled=false; };
    el.appendChild(d);
  });
}
$('expLayer').onchange=buildExplorer;
$('expSearch').oninput=buildExplorer;
$('expCentre').onclick=()=>{ if(!aimedId)return;
  setCenter(aimedId); cam.position=new BABYLON.Vector3(0,0,0.0001); applyCam(); updateDolly();
  aimedId=null; $('expCentre').disabled=true; buildExplorer(); };

// HUD arrow: when the aimed node is off-screen or behind you, an arrow at the screen edge
// points which way to turn your head; when it is in view, a ring marks it.
function renderGuide(){
  const g=$('guide'),gl=$('guideLbl'),gr=$('guideRing');
  if(!aimedId||!pos[aimedId]||aimedId===state.focus){g.style.display=gl.style.display=gr.style.display='none';return;}
  const W=engine.getRenderWidth(),H=engine.getRenderHeight();
  const v=BABYLON.Vector3.TransformCoordinates(pos[aimedId],scene.getViewMatrix());
  const p=BABYLON.Vector3.Project(pos[aimedId],BABYLON.Matrix.Identity(),
    scene.getTransformMatrix(),cam.viewport.toGlobal(W,H));
  const onScreen = v.z>0 && p.x>10 && p.x<W-10 && p.y>10 && p.y<H-10;
  if(onScreen){
    g.style.display='none';
    gr.style.display='block'; gr.style.left=p.x+'px'; gr.style.top=p.y+'px';
    gl.style.display='block'; gl.style.left=(p.x+22)+'px'; gl.style.top=(p.y-8)+'px';
    gl.textContent=byId[aimedId].label;
  }else{
    gr.style.display='none';
    // direction on screen toward the target, in view space (flip when behind)
    let dx=v.x,dy=-v.y; if(v.z<=0){dx=-dx;dy=-dy;}
    const n=Math.hypot(dx,dy)||1; dx/=n; dy/=n;
    const R=Math.min(W,H)*0.34, cx=W/2+dx*R, cy=H/2+dy*R;
    g.style.display='block'; g.style.left=cx+'px'; g.style.top=cy+'px';
    g.style.transform=`translate(-50%,-50%) rotate(${Math.atan2(dy,dx)*180/Math.PI+90}deg)`;
    gl.style.display='block'; gl.style.left=(cx+14)+'px'; gl.style.top=(cy+10)+'px';
    gl.textContent=byId[aimedId].label+(v.z<=0?' · behind you':'');
  }
}

/* ---- 9f. CONTEXT MENU ------------------------------------------------------
   Right-click a star. Actions state their consequence in numbers ("reveals 121"),
   because a fold whose effect you can't predict feels broken — which is exactly what
   happened with the earlier pole-cube widgets on a shallow subtree. */
function closeCtxMenu(){ const m=$('ctxmenu'); if(m) m.style.display='none'; }
let ctxJustOpened=false;
addEventListener('pointerdown',e=>{
  if(e.button===2)return;                       // right-click: handled by the canvas opener
  if(ctxJustOpened){ ctxJustOpened=false; return; }
  if(!e.target.closest||!e.target.closest('#ctxmenu')) closeCtxMenu();
},true);
addEventListener('keydown',e=>{ if(e.code==='Escape') closeCtxMenu(); });
function openCtxMenu(ev,id){
  const box=$('ctxmenu'); if(!box)return;
  if(!id){ closeCtxMenu(); return; }
  const x=byId[id]; if(!x)return;
  const g=STYLESHEET.nodes.kinds[kindOf(x)]||STYLESHEET.nodes.kinds.other;
  const kids=(treeChildren[id]||[]).length, desc=descCount[id]||0;
  const open=isExpanded(id);
  const rows=[];
  rows.push(`<div class="hd"><span class="g" style="color:${g.hue}">${SHAPE_GLYPH[g.shape]||'●'}</span>`
    +`<span>${x.label}<br><small>${g.label}</small></span></div>`);
  if(kids){
    rows.push(open
      ? `<button data-a="fold">Collapse — hides <b>${desc}</b></button>`
      : `<button data-a="fold">Expand — reveals <b>${desc}</b></button>`);
  } else {
    rows.push(`<button disabled>No subtree to fold</button>`);
  }
  rows.push('<div class="sep"></div>');
  rows.push(`<button data-a="centre">Observe from here</button>`);
  rows.push(`<button data-a="aim">Aim at this${aimedId===id?' ✓':''}</button>`);
  if(state.arrangement==='cone')
    rows.push(`<button data-a="slice">Isolate its stratum</button>`);
  box.innerHTML=rows.join('');
  box.style.display='block';
  const w=box.offsetWidth||190, h=box.offsetHeight||150;
  box.style.left=Math.min(ev.clientX+8, innerWidth-w-8)+'px';
  box.style.top =Math.min(ev.clientY+8, innerHeight-h-8)+'px';
  box.querySelectorAll('button[data-a]').forEach(b=>{
    b.onclick=()=>{
      const a=b.dataset.a; closeCtxMenu();
      if(a==='fold') toggleFold(id);
      else if(a==='centre'){ setCenter(id);
        cam.position=new BABYLON.Vector3(0,0,0.0001); applyCam(); updateDolly(); }
      else if(a==='aim'){ aimedId=(aimedId===id?null:id); buildExplorer();
        $('expCentre').disabled=!aimedId; }
      else if(a==='slice') jumpToSlice(id);
    };
  });
}

/* Cross-slice stubs: when a stratum is isolated, links leaving it are not erased — they
   become short directional stubs. The layer cake is exactly its inter-layer edges, so
   hiding them would turn four strata into four disconnected catalogues. Click = jump. */
let stubMeshes=[];
function buildStubs(){
  stubMeshes.forEach(m=>m.dispose()); stubMeshes=[];
  if(state.slice===null||state.arrangement!=='cone')return;
  const seen=new Set();
  E.forEach(ed=>{
    if(!state.rels[ed.type])return;
    const a=byId[ed.s],b=byId[ed.t]; if(!a||!b)return;
    const av=nodeVisible(a), bv=nodeVisible(b);
    if(av===bv)return;                               // both in, or both out
    const from=av?ed.s:ed.t, to=av?ed.t:ed.s;
    if(!pos[from]||!pos[to])return;
    const key=from+'>'+to+':'+ed.type; if(seen.has(key))return; seen.add(key);
    const dir=pos[to].subtract(pos[from]).normalize();
    const p0=pos[from].add(dir.scale(1.0)), p1=pos[from].add(dir.scale(3.4));
    const l=BABYLON.MeshBuilder.CreateTube('stub',
      {path:[p0,p1],radius:0.13,tessellation:5,cap:BABYLON.Mesh.CAP_END},scene);
    const mt=new BABYLON.StandardMaterial('stubM',scene); mt.disableLighting=true;
    mt.emissiveColor=BABYLON.Color3.FromHexString(STYLESHEET.edges.colors[ed.type]||'#39466a');
    mt.alpha=0.85; l.material=mt;
    l.metadata={id:to,stub:true,type:ed.type}; stubMeshes.push(l);
  });
}
/* cone scaffolding: one ring per slice + generatrices along the surface */
let sliceMeshes=[];
function buildSlices(){
  sliceMeshes.forEach(m=>m.dispose()); sliceMeshes=[];
  if(state.arrangement==='nautilus'){
    if(!coneSlices.length)return;
    const col=new BABYLON.Color3(0.42,0.46,0.62), turns=coneSlices.length;
    // the spiral curve itself
    const pts=[]; for(let i=0;i<=turns*90;i++){ const t=i/90;
      const th=-2*Math.PI*t, r=nauR(t); pts.push(new BABYLON.Vector3(r*Math.cos(th),0,r*Math.sin(th))); }
    const sp=BABYLON.MeshBuilder.CreateLines('spiral',{points:pts},scene);
    sp.color=col; sp.alpha=0.30; sp.isPickable=false; sliceMeshes.push(sp);
    // septa: a ring at each coil boundary, like the chambers of a real shell
    for(let k=0;k<=turns;k++){
      const th=-2*Math.PI*k, r=nauR(k), tr=NAU_TF*r, nx=Math.cos(th), nz=Math.sin(th), rp=[];
      for(let i=0;i<=48;i++){ const p=2*Math.PI*i/48;
        rp.push(new BABYLON.Vector3(r*nx+tr*Math.cos(p)*nx,tr*Math.sin(p)*NAU_H,r*nz+tr*Math.cos(p)*nz)); }
      const rr=BABYLON.MeshBuilder.CreateLines('septum'+k,{points:rp},scene);
      rr.color=col; rr.alpha=0.24; rr.isPickable=false; sliceMeshes.push(rr);
    }
    return;
  }
  if(state.arrangement!=='cone'||!coneSlices.length)return;
  // translucent cone surface between consecutive strata — this is what makes the
  // cosmic-history diagram read as a cone rather than as a stack of loose rings
  for(let i=0;i<coneSlices.length;i++){
    const a=coneSlices[i], b=coneSlices[i+1];
    const z0=(i===0)?R0*0.5:a.z, r0=(i===0)?0.4:a.rad;
    const z1=b?b.z:a.z+SHELL*0.9, r1=b?b.rad:a.rad*1.05;
    const h=z1-z0;
    const f=BABYLON.MeshBuilder.CreateCylinder('cone'+i,
      {height:h,diameterTop:r1*2,diameterBottom:r0*2,tessellation:48,cap:BABYLON.Mesh.NO_CAP},scene);
    f.rotation.x=Math.PI/2; f.position=new BABYLON.Vector3(0,0,z0+h/2);
    const fm=new BABYLON.StandardMaterial('coneM'+i,scene);
    fm.disableLighting=true; fm.emissiveColor=new BABYLON.Color3(0.10,0.14,0.30);
    fm.alpha=0.10; fm.backFaceCulling=false; f.material=fm; f.isPickable=false;
    sliceMeshes.push(f);
  }
  const SEG=72, col=new BABYLON.Color3(0.36,0.50,0.78);
  coneSlices.forEach(s=>{
    const pts=[]; for(let i=0;i<=SEG;i++){ const a=2*Math.PI*i/SEG;
      pts.push(new BABYLON.Vector3(s.rad*Math.cos(a),s.rad*Math.sin(a),s.z)); }
    const r=BABYLON.MeshBuilder.CreateLines('slice_'+s.k,{points:pts},scene);
    r.color=col; r.alpha=0.34; r.isPickable=false; sliceMeshes.push(r);
  });
  for(let g=0;g<8;g++){ const a=2*Math.PI*g/8, pts=[new BABYLON.Vector3(0,0,R0*0.6)];
    coneSlices.forEach(s=>pts.push(new BABYLON.Vector3(s.rad*Math.cos(a),s.rad*Math.sin(a),s.z)));
    const l=BABYLON.MeshBuilder.CreateLines('gen_'+g,{points:pts},scene);
    l.color=col; l.alpha=0.16; l.isPickable=false; sliceMeshes.push(l);
  }
}
function renderSliceLabels(){
  const box=document.getElementById('sliceLabels'); if(!box)return;
  const naut=state.arrangement==='nautilus';
  if(state.arrangement!=='cone'&&!naut){ box.innerHTML=''; return; }
  const W=engine.getRenderWidth(),H=engine.getRenderHeight();
  let html='';
  coneSlices.forEach(s=>{
    const wp = naut
      ? (()=>{ const t=(s.coil||0)+0.5, th=-2*Math.PI*t, r=nauR(t);
               return new BABYLON.Vector3(r*Math.cos(th),NAU_TF*r*NAU_H*1.5,r*Math.sin(th)); })()
      : new BABYLON.Vector3(0,s.rad*1.04,s.z);
    const v=BABYLON.Vector3.TransformCoordinates(wp,scene.getViewMatrix());
    if(v.z<=0)return;
    const p=BABYLON.Vector3.Project(wp,BABYLON.Matrix.Identity(),
      scene.getTransformMatrix(),cam.viewport.toGlobal(W,H));
    if(p.x<0||p.x>W||p.y<0||p.y>H)return;
    html+=`<div class="slbl" style="left:${p.x}px;top:${p.y}px">${s.label}<span>${s.n}</span></div>`;
  });
  box.innerHTML=html;
}
/* keyboard flight: ↑/↓ or Z/X or W/S for thrust along the gaze, ←/→ to swing the head.
   Held keys give continuous motion, which reads far better than discrete steps. */
const keysDown={};
addEventListener('keydown',e=>{
  const t=e.target.tagName; if(t==='INPUT'||t==='SELECT'||t==='TEXTAREA')return;
  keysDown[e.code]=true;
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)) e.preventDefault();
});
addEventListener('keyup',e=>{ keysDown[e.code]=false; });
addEventListener('blur',()=>{ for(const k in keysDown) keysDown[k]=false; });
function stepKeys(){
  let thrust=0, turn=0;
  if(keysDown['ArrowUp']||keysDown['KeyZ']||keysDown['KeyW']) thrust+=1;
  if(keysDown['ArrowDown']||keysDown['KeyX']||keysDown['KeyS']) thrust-=1;
  if(keysDown['ArrowLeft']||keysDown['KeyA']) turn-=1;
  if(keysDown['ArrowRight']||keysDown['KeyD']) turn+=1;
  if(turn){ yaw+=turn*0.022; applyCam(); }
  if(thrust){
    glideTarget=null;                                  // manual control overrides travel
    const fwd=cam.getForwardRay().direction;
    const np=cam.position.add(fwd.scale(thrust*0.62));
    if(np.length()<=170){ cam.position=np; applyCam(); updateDolly(); }
  }
  if(turn||thrust) applyCam();
}

/* ---- 9e. SLICE NAVIGATION · HYPERTEXT JUMP · CONTINUUM TRAVEL ------------- */
function sliceIndexOf(id){ return Math.max(0,Math.round(radialOf[id]||0)); }
function setSlice(k){
  state.slice=k;
  const s=(k===null)?null:coneSlices.find(z=>z.k===k);
  $('vSlice').textContent = (k===null)?'all strata'
    : (s?`${s.label} · ${s.n} in ${s.clusters} clusters`:'stratum '+k);
  relayout();
  if(s){ glideTo(s.z-Math.max(8,s.rad*0.9)); }
}
function jumpToSlice(id){                       // follow a stub to the other layer
  if(!pos[id])return;
  aimedId=id; buildExplorer(); $('expCentre').disabled=false;
  setSlice(sliceIndexOf(id));
}
function shiftSlice(d){
  const ks=coneSlices.map(s=>s.k);
  if(!ks.length)return;
  if(state.slice===null){ setSlice(ks[0]); return; }
  const i=ks.indexOf(state.slice); if(i<0){ setSlice(ks[0]); return; }
  const j=Math.max(0,Math.min(ks.length-1,i+d));
  setSlice(ks[j]);
}
// smooth travel along the cone axis — chronological (toward M0) or retro (toward M3)
let glideTarget=null;
function glideTo(z){ glideTarget=z; }
function travel(dir){
  const zs=coneSlices.map(s=>s.z); if(!zs.length)return;
  const lo=-6, hi=zs[zs.length-1]+10;
  glideTo(Math.max(lo,Math.min(hi,(glideTarget!==null?glideTarget:cam.position.z)+dir*18)));
}
function stepGlide(){
  if(glideTarget===null)return;
  const p=cam.position, dz=glideTarget-p.z;
  if(Math.abs(dz)<0.15){ p.z=glideTarget; glideTarget=null; }
  else p.z+=dz*0.09;
  cam.position=new BABYLON.Vector3(p.x,p.y,p.z); applyCam(); updateDolly();
}

/* ---- 9d. SELECTION ORBIT (polygon matches the glyph's own geometry) -------- */
let orbitMesh=null, orbitFor=null;
function updateOrbit(){
  const id=aimedId||hoverId;
  if(!id||!pos[id]||!meshes[id]||!meshes[id].isEnabled()){
    if(orbitMesh)orbitMesh.setEnabled(false); orbitFor=null; return; }
  const g=STYLESHEET.nodes.kinds[kindOf(byId[id])]||STYLESHEET.nodes.kinds.other;
  if(orbitFor!==id){
    if(orbitMesh)orbitMesh.dispose();
    orbitMesh=BABYLON.MeshBuilder.CreateTorus('orbit',
      {diameter:2.5,thickness:0.075,tessellation:ORBIT_TESS[g.shape]||36},scene);
    const om=new BABYLON.StandardMaterial('orbitM',scene);
    om.disableLighting=true;
    om.emissiveColor=BABYLON.Color3.FromHexString(aimedId?'#9fe0b0':'#ffffff');
    om.alpha=0.92; orbitMesh.material=om; orbitMesh.isPickable=false;
    orbitFor=id;
  }
  orbitMesh.setEnabled(true);
  orbitMesh.position=pos[id];
  orbitMesh.scaling.setAll(meshes[id].scaling.x*1.35);
  orbitMesh.rotation.y+=0.012;
  orbitMesh.rotation.x=0.42;
}

/* ---- 10. RUN -------------------------------------------------------------- */
state.focus=graphBarycenter();
document.getElementById('focusName').textContent=byId[state.focus].label;
document.getElementById('obsName').textContent=byId[state.focus].label;
state.radial='tree'; $('radial').value='tree'; $('vRadial').textContent='tree depth';
cam.fov=1.5;
relayout();            // positions must exist before any applyVisual/inCone call
updateInstrument();
buildExplorer(); updateDolly(); $('expCentre').disabled=true;
scene.onBeforeRenderObservable.add(()=>{ applyCone(); });
let coneTick=0;
function applyCone(){ if(++coneTick%2===0){/* cone depends on camera; refresh lightly */ applyVisualCheap();} }
function applyVisualCheap(){ // update only cone-driven alpha each frame (cheap path)
  N.forEach(x=>{const m=meshes[x.id]; if(!m||!m.isEnabled()||!pos[x.id])return;
    if(hoverId)return; const cone=inCone(pos[x.id]);
    m.material.alpha=cone?1:0.62;
    const c=BABYLON.Color3.FromHexString(colorOf(x));
    m.material.diffuseColor=c.scale(cone?1:0.6);
    m.material.emissiveColor=c.scale(cone?0.42:0.16);});
}
let radarTick=0;
engine.runRenderLoop(()=>{stepKeys();stepGlide();scene.render();renderGuide();updateOrbit();renderSliceLabels();
  if(++radarTick%3===0) drawRadar();});
addEventListener('resize',()=>engine.resize());
