const fs=require('fs'),vm=require('vm');
// --- stubs DOM + Babylon assez complets pour executer l'initialisation ---
const noop=()=>{};
const mkEl=()=>new Proxy({style:{},dataset:{},classList:{add:noop,remove:noop,toggle:noop},
  children:[],value:'',textContent:'',innerHTML:'',checked:false,width:236,height:188,offsetWidth:190,offsetHeight:150,
  selectedOptions:[{text:'X'}],
  getContext:()=>new Proxy({},{get:()=>()=>({addColorStop:noop})}),
  appendChild:noop,addEventListener:noop,querySelectorAll:()=>[],querySelector:()=>mkEl(),closest:()=>null,
  getBoundingClientRect:()=>({left:0,top:0})},
  {get:(t,k)=>k in t?t[k]:noop,set:(t,k,v)=>{t[k]=v;return true;}});
const V3=class{constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;}
  add(o){return new V3(this.x+o.x,this.y+o.y,this.z+o.z);}
  subtract(o){return new V3(this.x-o.x,this.y-o.y,this.z-o.z);}
  scale(s){return new V3(this.x*s,this.y*s,this.z*s);}
  length(){return Math.hypot(this.x,this.y,this.z);}
  normalize(){const n=this.length()||1;return new V3(this.x/n,this.y/n,this.z/n);}
  static Zero(){return new V3();} static Dot(a,b){return a.x*b.x+a.y*b.y+a.z*b.z;}
  static TransformCoordinates(){return new V3(0,0,1);} static Project(){return new V3(10,10,0.5);}};
const mesh=()=>new Proxy({position:new V3(),rotation:{x:0,y:0,z:0},scaling:{x:1,setAll:noop},
  metadata:{},material:{},name:'m',isPickable:true,
  getBoundingInfo:()=>({boundingBox:{maximum:{y:0.5}}}),
  setEnabled:noop,isEnabled:()=>true,dispose:noop,addChild:noop,enableEdgesRendering:noop},
  {get:(t,k)=>k in t?t[k]:noop,set:(t,k,v)=>{t[k]=v;return true;}});
const B={Vector3:V3,Color3:class{constructor(r,g,b){this.r=r;this.g=g;this.b=b;}
   scale(s){return new B.Color3(this.r*s,this.g*s,this.b*s);}
   static FromHexString(){return new B.Color3(1,1,1);}},
  Color4:class{constructor(r,g,b,a){Object.assign(this,{r,g,b,a});}},
  Matrix:{Identity:()=>({})},Mesh:{BACKSIDE:1,NO_CAP:0,CAP_END:1},
  Engine:class{constructor(){}runRenderLoop(f){this._f=f;}getRenderWidth(){return 1200;}
    getRenderHeight(){return 800;}resize(){}},
  Scene:class{constructor(){this.onBeforeRenderObservable={add:noop};this.onPointerObservable={add:noop};}
    render(){}getViewMatrix(){return{};}getTransformMatrix(){return{};}pick(){return{hit:false};}},
  FreeCamera:class{constructor(){this.position=new V3(0,0,0.0001);this.fov=1.05;
    this.viewport={toGlobal:()=>({})};}
    getForwardRay(){return{direction:new V3(0,0,1)};}setTarget(){}},
  HemisphericLight:class{constructor(){this.intensity=1;}},
  DirectionalLight:class{constructor(){this.intensity=1;}},
  GlowLayer:class{constructor(){this.intensity=1;}},
  DynamicTexture:class{constructor(){}getContext(){return new Proxy({},{get:()=>()=>({addColorStop:noop})});}update(){}},
  StandardMaterial:class{constructor(){}},
  MeshBuilder:new Proxy({},{get:()=>()=>mesh()}),
  Texture:{WRAP_ADDRESSMODE:1,CLAMP_ADDRESSMODE:0},
  PointsCloudSystem:class{constructor(){}addPoints(){}buildMeshAsync(){}}};
const sandbox={BABYLON:B,console,performance:{now:()=>0},Math,JSON,Set,Map,Object,Array,
  document:{getElementById:()=>mkEl(),createElement:()=>mkEl(),
    addEventListener:noop,body:mkEl()},
  window:{},addEventListener:noop,innerWidth:1200,innerHeight:800};
sandbox.window=sandbox;
vm.createContext(sandbox);
try{
  for(const f of ['src/canopy-data.js','src/canopy-stylesheet.js','src/canopy-core.js'])
    vm.runInContext(fs.readFileSync(f,'utf8'),sandbox,{filename:f});
  vm.runInContext(`console.log('  focus      :',state.focus);
console.log('  arrangement:',state.arrangement);
console.log('  noeuds positionnes :',Object.keys(pos).length,'/',N.length);
console.log('  pliables   :',N.filter(x=>(treeChildren[x.id]||[]).length).length);`,sandbox);
  console.log('\nBOOT OK — initialisation complete sans erreur');
}catch(e){ console.log('\nBOOT ECHEC :',e.message,'\n',(e.stack||'').split('\n')[1]); process.exit(1); }
vm.runInContext(`
console.log('\\n=== tous les arrangements ===');
['canopy','clusters','cone','nautilus'].forEach(a=>{
  state.arrangement=a;
  if(a==='cone'||a==='nautilus') state.radial='meta'; else state.radial='tree';
  try{ relayout();
    console.log('  '+a.padEnd(10)+' OK  positions='+Object.keys(pos).length
      +(coneSlices.length?('  tranches='+coneSlices.length):''));
  }catch(e){ console.log('  '+a.padEnd(10)+' ECHEC: '+e.message); }
});
console.log('\\n=== tranche isolee + amorces ===');
state.arrangement='cone'; state.radial='meta'; relayout();
try{ setSlice(coneSlices[3]?coneSlices[3].k:0); console.log('  setSlice OK'); }
catch(e){ console.log('  setSlice ECHEC: '+e.message); }
console.log('\\n=== repliement ===');
state.arrangement='canopy'; state.radial='tree'; state.slice=null; relayout();
try{ toggleFold('GenericConceptFamily'); console.log('  toggleFold OK  masques='+collapsedHidden.size); }
catch(e){ console.log('  toggleFold ECHEC: '+e.message); }
`,sandbox);
vm.runInContext(`
console.log('\\n=== noeud observateur (sous les pieds) ===');
['canopy','clusters','cone','nautilus'].forEach(a=>{
  state.arrangement=a; state.radial=(a==='cone'||a==='nautilus')?'meta':'tree';
  relayout();
  const p=pos[state.focus];
  const vis=nodeVisible(byId[state.focus]);
  console.log('  '+a.padEnd(10)+' position='+(p?('('+p.x.toFixed(1)+','+p.y.toFixed(1)+','+p.z.toFixed(1)+')'):'∅')
    +'  visible='+vis+'  distance='+(p?p.length().toFixed(1):'-'));
});
`,sandbox);
