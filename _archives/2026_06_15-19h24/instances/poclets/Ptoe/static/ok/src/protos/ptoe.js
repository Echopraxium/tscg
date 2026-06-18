/* ═══════════════════════════════════════════════════════════════════
   TSCG Ptoe Simulation - JavaScript
   Author: Echopraxium with the collaboration of Claude AI
   ═══════════════════════════════════════════════════════════════════ */

console.log('🚀 Ptoe JavaScript loaded');

'use strict';

'use strict';

/* ══════════════════════════════════════════════
   DATA
══════════════════════════════════════════════ */
const CAT_HEX = {
  am:'#FF4422', ae:'#FF9900', tm:'#FFD030', pt:'#55CC33',
  md:'#3399FF', nm:'#66EEFF', ha:'#CC33FF', ng:'#FF44BB',
  ln:'#22FFCC', ac:'#44AAFF'
};
const CAT_NAME = {
  am:'Alkali Metal', ae:'Alkaline Earth Metal', tm:'Transition Metal',
  pt:'Post-Transition Metal', md:'Metalloid', nm:'Nonmetal',
  ha:'Halogen', ng:'Noble Gas', ln:'Lanthanide', ac:'Actinide'
};
const CAT_DESC = {
  am:'Highly reactive metals in Group 1 with one valence electron. They form +1 cations and react vigorously with water. Examples: Li, Na, K.',
  ae:'Reactive metals in Group 2 with two valence electrons. They form +2 cations and are less reactive than alkali metals. Examples: Be, Mg, Ca.',
  tm:'Metals in Groups 3-12 with variable oxidation states. They have partially filled d-orbitals and often form colored compounds. Examples: Fe, Cu, Zn.',
  pt:'Metals in Groups 13-15 that are softer and have lower melting points than transition metals. Examples: Al, Sn, Pb.',
  md:'Elements with properties intermediate between metals and nonmetals. They are semiconductors. Examples: B, Si, Ge.',
  nm:'Elements that lack metallic properties. They gain electrons in reactions and form covalent bonds. Examples: C, N, O, S.',
  ha:'Highly reactive nonmetals in Group 17 with seven valence electrons. They form -1 anions and diatomic molecules. Examples: F, Cl, Br.',
  ng:'Inert gases in Group 18 with full valence shells. They rarely form compounds due to their stability. Examples: He, Ne, Ar.',
  ln:'Rare earth metals in the f-block (atomic numbers 57-71). They have similar chemical properties and are used in magnets and electronics.',
  ac:'Radioactive elements in the f-block (atomic numbers 89-103). Many are synthetic and unstable. Examples: U, Pu, Am.'
};
const BLOCK = {am:'s',ae:'s',nm:'p',ha:'p',ng:'p',md:'p',pt:'p',tm:'d',ln:'f',ac:'f'};

const EL = [
  [1,'H','Hydrogen',1,1,'nm','1.008'],[2,'He','Helium',1,18,'ng','4.003'],
  [3,'Li','Lithium',2,1,'am','6.941'],[4,'Be','Beryllium',2,2,'ae','9.012'],
  [5,'B','Boron',2,13,'md','10.81'],[6,'C','Carbon',2,14,'nm','12.01'],
  [7,'N','Nitrogen',2,15,'nm','14.01'],[8,'O','Oxygen',2,16,'nm','16.00'],
  [9,'F','Fluorine',2,17,'ha','19.00'],[10,'Ne','Neon',2,18,'ng','20.18'],
  [11,'Na','Sodium',3,1,'am','22.99'],[12,'Mg','Magnesium',3,2,'ae','24.31'],
  [13,'Al','Aluminum',3,13,'pt','26.98'],[14,'Si','Silicon',3,14,'md','28.09'],
  [15,'P','Phosphorus',3,15,'nm','30.97'],[16,'S','Sulfur',3,16,'nm','32.07'],
  [17,'Cl','Chlorine',3,17,'ha','35.45'],[18,'Ar','Argon',3,18,'ng','39.95'],
  [19,'K','Potassium',4,1,'am','39.10'],[20,'Ca','Calcium',4,2,'ae','40.08'],
  [21,'Sc','Scandium',4,3,'tm','44.96'],[22,'Ti','Titanium',4,4,'tm','47.87'],
  [23,'V','Vanadium',4,5,'tm','50.94'],[24,'Cr','Chromium',4,6,'tm','52.00'],
  [25,'Mn','Manganese',4,7,'tm','54.94'],[26,'Fe','Iron',4,8,'tm','55.85'],
  [27,'Co','Cobalt',4,9,'tm','58.93'],[28,'Ni','Nickel',4,10,'tm','58.69'],
  [29,'Cu','Copper',4,11,'tm','63.55'],[30,'Zn','Zinc',4,12,'tm','65.38'],
  [31,'Ga','Gallium',4,13,'pt','69.72'],[32,'Ge','Germanium',4,14,'md','72.63'],
  [33,'As','Arsenic',4,15,'md','74.92'],[34,'Se','Selenium',4,16,'nm','78.97'],
  [35,'Br','Bromine',4,17,'ha','79.90'],[36,'Kr','Krypton',4,18,'ng','83.80'],
  [37,'Rb','Rubidium',5,1,'am','85.47'],[38,'Sr','Strontium',5,2,'ae','87.62'],
  [39,'Y','Yttrium',5,3,'tm','88.91'],[40,'Zr','Zirconium',5,4,'tm','91.22'],
  [41,'Nb','Niobium',5,5,'tm','92.91'],[42,'Mo','Molybdenum',5,6,'tm','95.95'],
  [43,'Tc','Technetium',5,7,'tm','[98]'],[44,'Ru','Ruthenium',5,8,'tm','101.1'],
  [45,'Rh','Rhodium',5,9,'tm','102.9'],[46,'Pd','Palladium',5,10,'tm','106.4'],
  [47,'Ag','Silver',5,11,'tm','107.9'],[48,'Cd','Cadmium',5,12,'tm','112.4'],
  [49,'In','Indium',5,13,'pt','114.8'],[50,'Sn','Tin',5,14,'pt','118.7'],
  [51,'Sb','Antimony',5,15,'md','121.8'],[52,'Te','Tellurium',5,16,'md','127.6'],
  [53,'I','Iodine',5,17,'ha','126.9'],[54,'Xe','Xenon',5,18,'ng','131.3'],
  [55,'Cs','Cesium',6,1,'am','132.9'],[56,'Ba','Barium',6,2,'ae','137.3'],
  [57,'La','Lanthanum',5.55,1,'ln','138.9'],[58,'Ce','Cerium',5.55,2,'ln','140.1'],
  [59,'Pr','Praseodymium',5.55,3,'ln','140.9'],[60,'Nd','Neodymium',5.55,4,'ln','144.2'],
  [61,'Pm','Promethium',5.55,5,'ln','[145]'],[62,'Sm','Samarium',5.55,6,'ln','150.4'],
  [63,'Eu','Europium',5.55,7,'ln','152.0'],[64,'Gd','Gadolinium',5.55,8,'ln','157.3'],
  [65,'Tb','Terbium',5.55,9,'ln','158.9'],[66,'Dy','Dysprosium',5.55,10,'ln','162.5'],
  [67,'Ho','Holmium',5.55,11,'ln','164.9'],[68,'Er','Erbium',5.55,12,'ln','167.3'],
  [69,'Tm','Thulium',5.55,13,'ln','168.9'],[70,'Yb','Ytterbium',5.55,14,'ln','173.0'],
  [71,'Lu','Lutetium',5.55,15,'ln','175.0'],[72,'Hf','Hafnium',6,4,'tm','178.5'],
  [73,'Ta','Tantalum',6,5,'tm','180.9'],[74,'W','Tungsten',6,6,'tm','183.8'],
  [75,'Re','Rhenium',6,7,'tm','186.2'],[76,'Os','Osmium',6,8,'tm','190.2'],
  [77,'Ir','Iridium',6,9,'tm','192.2'],[78,'Pt','Platinum',6,10,'tm','195.1'],
  [79,'Au','Gold',6,11,'tm','197.0'],[80,'Hg','Mercury',6,12,'pt','200.6'],
  [81,'Tl','Thallium',6,13,'pt','204.4'],[82,'Pb','Lead',6,14,'pt','207.2'],
  [83,'Bi','Bismuth',6,15,'pt','209.0'],[84,'Po','Polonium',6,16,'md','[209]'],
  [85,'At','Astatine',6,17,'ha','[210]'],[86,'Rn','Radon',6,18,'ng','[222]'],
  [87,'Fr','Francium',7,1,'am','[223]'],[88,'Ra','Radium',7,2,'ae','[226]'],
  [89,'Ac','Actinium',6.55,1,'ac','[227]'],[90,'Th','Thorium',6.55,2,'ac','232.0'],
  [91,'Pa','Protactinium',6.55,3,'ac','231.0'],[92,'U','Uranium',6.55,4,'ac','238.0'],
  [93,'Np','Neptunium',6.55,5,'ac','[237]'],[94,'Pu','Plutonium',6.55,6,'ac','[244]'],
  [95,'Am','Americium',6.55,7,'ac','[243]'],[96,'Cm','Curium',6.55,8,'ac','[247]'],
  [97,'Bk','Berkelium',6.55,9,'ac','[247]'],[98,'Cf','Californium',6.55,10,'ac','[251]'],
  [99,'Es','Einsteinium',6.55,11,'ac','[252]'],[100,'Fm','Fermium',6.55,12,'ac','[257]'],
  [101,'Md','Mendelevium',6.55,13,'ac','[258]'],[102,'No','Nobelium',6.55,14,'ac','[259]'],
  [103,'Lr','Lawrencium',6.55,15,'ac','[266]'],[104,'Rf','Rutherfordium',7,4,'tm','[267]'],
  [105,'Db','Dubnium',7,5,'tm','[268]'],[106,'Sg','Seaborgium',7,6,'tm','[271]'],
  [107,'Bh','Bohrium',7,7,'tm','[272]'],[108,'Hs','Hassium',7,8,'tm','[270]'],
  [109,'Mt','Meitnerium',7,9,'tm','[278]'],[110,'Ds','Darmstadtium',7,10,'tm','[281]'],
  [111,'Rg','Roentgenium',7,11,'tm','[282]'],[112,'Cn','Copernicium',7,12,'pt','[285]'],
  [113,'Nh','Nihonium',7,13,'pt','[286]'],[114,'Fl','Flerovium',7,14,'pt','[289]'],
  [115,'Mc','Moscovium',7,15,'pt','[290]'],[116,'Lv','Livermorium',7,16,'pt','[293]'],
  [117,'Ts','Tennessine',7,17,'ha','[294]'],[118,'Og','Oganesson',7,18,'ng','[294]']
];

/* ══════════════════════════════════════════════
   NAUTILUS MATH
══════════════════════════════════════════════ */
const A=2.0, B=0.048, TF=0.110, HSCL=2.0, TURNS=7;
const sR=t=>A*Math.exp(B*2*Math.PI*t);
const tR=t=>TF*sR(t);

/* ══════════════════════════════════════════════
   NACRE SHADER
══════════════════════════════════════════════ */
BABYLON.Effect.ShadersStore['nacreVertexShader']=`
  precision highp float;
  attribute vec3 position; attribute vec3 normal; attribute vec2 uv;
  uniform mat4 worldViewProjection; uniform mat4 world; uniform mat4 view;
  varying vec2 vUV; varying vec3 vN; varying vec3 vViewDir;
  void main(){
    vec4 wPos=world*vec4(position,1.0); vec4 vPos=view*wPos;
    vN=normalize(mat3(world)*normal); vViewDir=normalize(-vPos.xyz);
    vUV=uv; gl_Position=worldViewProjection*vec4(position,1.0);
  }`;
BABYLON.Effect.ShadersStore['nacreFragmentShader']=`
  precision highp float;
  varying vec2 vUV; varying vec3 vN; varying vec3 vViewDir;
  uniform float uTime;
  vec3 hsv2rgb(vec3 c){
    vec4 K=vec4(1.0,2.0/3.0,1.0/3.0,3.0);
    vec3 p=abs(fract(c.xxx+K.xyz)*6.0-K.www);
    return c.z*mix(K.xxx,clamp(p-K.xxx,0.0,1.0),c.y);
  }
  void main(){
    vec3 N=normalize(vN); vec3 V=normalize(vViewDir);
    float NdotV=max(dot(N,V),0.0); float graz=1.0-NdotV;
    vec3 base=mix(vec3(0.97,0.90,0.86),vec3(0.82,0.70,0.65),graz*0.70);
    float hue=mod(graz*2.0+vUV.x*2.5+uTime*0.022,1.0);
    vec3 iri=hsv2rgb(vec3(hue,0.50,0.85));
    float str=smoothstep(0.30,0.62,graz)*(1.0-smoothstep(0.62,0.94,graz))*0.40;
    vec3 col=mix(base,iri,str);
    vec3 L=normalize(vec3(0.55,0.75,0.35)); vec3 H=normalize(V+L);
    float sp=pow(max(dot(N,H),0.0),140.0)*0.28;
    col+=vec3(0.90,0.88,0.80)*sp;
    gl_FragColor=vec4(col,0.97);
  }`;

/* ══════════════════════════════════════════════
   DOM REFS
══════════════════════════════════════════════ */
const canvasA=document.getElementById('canvas-a');
const canvasB=document.getElementById('canvas-b');
const viewMain=document.getElementById('view-main');
const viewNE=document.getElementById('view-ne');
let swapped=false;

/* ══════════════════════════════════════════════
   ENGINE A — NAUTILUS
══════════════════════════════════════════════ */
const engA=new BABYLON.Engine(canvasA,true,{antialias:true,stencil:true});
const nauScene=new BABYLON.Scene(engA);
nauScene.clearColor=new BABYLON.Color4(0.012,0.030,0.060,1.0);

const CAM_ALPHA=-0.15, CAM_BETA=0.82, CAM_RADIUS=54;
const camA=new BABYLON.ArcRotateCamera('camA',CAM_ALPHA,CAM_BETA,CAM_RADIUS,BABYLON.Vector3.Zero(),nauScene);
camA.lowerRadiusLimit=8; camA.upperRadiusLimit=130;
camA.lowerBetaLimit=0.04; camA.upperBetaLimit=Math.PI*0.80;
camA.wheelDeltaPercentage=0.012; camA.minZ=0.2;
camA.attachControl(canvasA,true);
camA.useAutoRotationBehavior=true;
camA.autoRotationBehavior.idleRotationSpeed=0.20;
camA.autoRotationBehavior.idleRotationWaitTime=500;
camA.useAutoRotationBehavior=false;

/* Lighting */
const sunA=new BABYLON.DirectionalLight('sunA',new BABYLON.Vector3(0.5,-0.55,0.3),nauScene);
sunA.diffuse=new BABYLON.Color3(1.0,0.92,0.72); sunA.intensity=0.80;
const hemiA=new BABYLON.HemisphericLight('hemiA',new BABYLON.Vector3(0,1,0),nauScene);
hemiA.diffuse=new BABYLON.Color3(0.18,0.22,0.35);
hemiA.groundColor=new BABYLON.Color3(0.02,0.02,0.04); hemiA.intensity=0.22;

/* Nacre material */
const nacreMat=new BABYLON.ShaderMaterial('nacre',nauScene,'nacre',{
  attributes:['position','normal','uv'],
  uniforms:['worldViewProjection','world','view','uTime'],
  needAlphaBlending:true  // Enable transparency
});
nacreMat.setFloat('uTime',0); nacreMat.backFaceCulling=false;
nacreMat.alpha = 1.0; // Default: fully opaque

/* Shell */
(function buildShell(){
  const NU=380,NV=48,pos=[],nor=[],uvA=[],idx=[];
  for(let j=0;j<=NU;j++){
    const t=TURNS*j/NU,th=-2*Math.PI*t,r=sR(t),tr=tR(t),nx=Math.cos(th),nz=Math.sin(th);
    for(let i=0;i<=NV;i++){
      const phi=2*Math.PI*i/NV,cp=Math.cos(phi),sp=Math.sin(phi);
      pos.push(r*nx+tr*cp*nx,tr*sp*HSCL,r*nz+tr*cp*nz);
      const enx=cp*nx,eny=sp*HSCL,enz=cp*nz,el=Math.sqrt(enx*enx+eny*eny+enz*enz)+1e-8;
      nor.push(enx/el,eny/el,enz/el); uvA.push(j/NU,i/NV);
    }
  }
  for(let j=0;j<NU;j++) for(let i=0;i<NV;i++){
    const a=j*(NV+1)+i,b=a+1,c=a+NV+1,d=c+1; idx.push(a,b,d,a,d,c);
  }
  const vd=new BABYLON.VertexData();
  vd.positions=pos; vd.normals=nor; vd.uvs=uvA; vd.indices=idx;
  const m=new BABYLON.Mesh('shell',nauScene); vd.applyToMesh(m);
  m.material=nacreMat; m.isPickable=false;
})();

/* Growth rings */
const ringMat=new BABYLON.StandardMaterial('gringMat',nauScene);
ringMat.diffuseColor=new BABYLON.Color3(0.22,0.15,0.06);
ringMat.emissiveColor=new BABYLON.Color3(0.04,0.025,0.005);
ringMat.specularPower=80;
/* Growth rings removed — no visible utility */

/* Septa */
const septaMat=new BABYLON.StandardMaterial('septa',nauScene);
septaMat.diffuseColor=new BABYLON.Color3(0.82,0.74,0.52);
septaMat.emissiveColor=new BABYLON.Color3(0.10,0.07,0.02);
septaMat.alpha=0.45; septaMat.backFaceCulling=false;
for(let p=1;p<=6;p++){
  const t=p,th=-2*Math.PI*t,r=sR(t),tr=tR(t),nx=Math.cos(th),nz=Math.sin(th),cx=r*nx,cz=r*nz;
  const NS=40,pos2=[],nor2=[],uvB=[],idx2=[];
  pos2.push(cx,0,cz); nor2.push(0,1,0); uvB.push(0.5,0.5);
  for(let i=0;i<=NS;i++){
    const phi=2*Math.PI*i/NS,cp=Math.cos(phi),sp=Math.sin(phi);
    pos2.push(cx+tr*cp*nx,tr*sp*HSCL,cz+tr*cp*nz);
    nor2.push(0,1,0); uvB.push(0.5+cp*0.5,0.5+sp*0.5);
    if(i>0) idx2.push(0,i,i+1);
  }
  const vd2=new BABYLON.VertexData(); vd2.positions=pos2; vd2.normals=nor2; vd2.uvs=uvB; vd2.indices=idx2;
  const sm=new BABYLON.Mesh(`septa${p}`,nauScene); vd2.applyToMesh(sm); sm.material=septaMat; sm.isPickable=false;
  const rpts=[]; for(let i=0;i<=NS;i++){ const phi=2*Math.PI*i/NS,cp=Math.cos(phi),sp=Math.sin(phi); rpts.push(new BABYLON.Vector3(cx+tr*cp*nx,tr*sp*HSCL,cz+tr*cp*nz)); }
  const sr=BABYLON.MeshBuilder.CreateTube(`sring${p}`,{path:rpts,radius:0.022,tessellation:5,cap:BABYLON.Mesh.NO_CAP},nauScene);
  const rm=new BABYLON.StandardMaterial(`srm${p}`,nauScene); rm.emissiveColor=new BABYLON.Color3(0.80,0.60,0.18); rm.alpha=0.55; sr.material=rm; sr.isPickable=false;
  const dot=BABYLON.MeshBuilder.CreateSphere(`dot${p}`,{diameter:0.11,segments:6},nauScene);
  dot.position=new BABYLON.Vector3((r+tr)*nx,0,(r+tr)*nz);
  const dm=new BABYLON.StandardMaterial(`dm${p}`,nauScene); dm.emissiveColor=new BABYLON.Color3(1.0,0.82,0.22); dot.material=dm; dot.isPickable=false;
}

/* Umbilicus */
(function(){
  const pts=[]; for(let i=0;i<=180;i++){ const t=i/180,th=-t*2*Math.PI*2.5,r=0.35*Math.exp(B*th); pts.push(new BABYLON.Vector3(r*Math.cos(th),0,r*Math.sin(th))); }
  const u=BABYLON.MeshBuilder.CreateTube('umb',{path:pts,radius:0.025,tessellation:6,cap:BABYLON.Mesh.NO_CAP},nauScene);
  const um=new BABYLON.StandardMaterial('umM',nauScene); um.emissiveColor=new BABYLON.Color3(0.80,0.55,0.12); um.alpha=0.50; u.material=um; u.isPickable=false;
})();

/* Stars */
const pcs0=new BABYLON.PointsCloudSystem('stars',1,nauScene);
pcs0.addPoints(2200,p=>{
  const rd=80+Math.random()*260,th=Math.random()*Math.PI*2,ph=Math.random()*Math.PI*2;
  p.position=new BABYLON.Vector3(rd*Math.sin(ph)*Math.cos(th),rd*Math.cos(ph)*0.18,rd*Math.sin(ph)*Math.sin(th));
  const br=0.15+Math.random()*0.42; p.color=new BABYLON.Color4(br,br,br+0.05,0.38);
});
pcs0.buildMeshAsync().then(m=>{m.isPickable=false;});

/* ── Family ring system ── */
const HL=new BABYLON.HighlightLayer('hl',nauScene,{blurHorizontalSize:0.7,blurVerticalSize:0.7});
const elemMeshes=[];
const catMats={},catMatsSel={};
function getCatMat(cat,sel=false){
  const store=sel?catMatsSel:catMats;
  if(!store[cat]){
    const m=new BABYLON.StandardMaterial(`cm_${cat}_${sel}`,nauScene);
    const c=BABYLON.Color3.FromHexString(CAT_HEX[cat]);
    m.diffuseColor=c.scale(sel?0.50:0.22);
    m.emissiveColor=c.scale(sel?1.80:0.65);
    m.specularColor=new BABYLON.Color3(0.06,0.06,0.06);
    store[cat]=m;
  }
  return store[cat];
}

const RING_RAD_NORMAL=0.096, RING_RAD_SEL=0.096*4;
const ringPathMap=new Map(), ringMeshMap=new Map();

function recreateRing(z,radius,useSel){
  const old=ringMeshMap.get(z); if(!old) return null;
  const meta=old.metadata, vis=old.visibility, pick=old.isPickable;
  const idx=elemMeshes.indexOf(old); /* BEFORE dispose — BabylonJS nulls metadata on dispose */
  old.dispose();
  const pts=ringPathMap.get(z);
  const ring=BABYLON.MeshBuilder.CreateTube(`er${z}`,{path:pts,radius,tessellation:7,cap:BABYLON.Mesh.NO_CAP},nauScene);
  ring.material=getCatMat(meta.cat,useSel);
  ring.metadata=meta; ring.visibility=vis; ring.isPickable=pick;
  ringMeshMap.set(z,ring);
  if(idx>=0) elemMeshes[idx]=ring; else elemMeshes.push(ring);
  return ring;
}

let selectedElemZ=null;
function setSelectedElemRing(z){
  if(selectedElemZ!==null && selectedElemZ!==z){
    const cat=EL[selectedElemZ-1][5];
    const ring=recreateRing(selectedElemZ,RING_RAD_NORMAL,selectedCat===cat);
    if(ring&&selectedCat===cat) try{HL.addMesh(ring,BABYLON.Color3.FromHexString(CAT_HEX[cat]));}catch(e){}
  }
  selectedElemZ=z;
  if(z!==null){
    const cat=EL[z-1][5];
    const ring=recreateRing(z,RING_RAD_SEL,true);
    if(ring&&selectedCat&&cat===selectedCat) try{HL.addMesh(ring,BABYLON.Color3.FromHexString(CAT_HEX[cat]));}catch(e){}
  }
}

EL.forEach(([z,sym,name,period,group,cat,mass])=>{
  const isFA=(cat==='ln'||cat==='ac'), tg=isFA?15:18;
  const t=(period-1)+(group-1)/tg, th=-2*Math.PI*t, r=sR(t), tr=tR(t);
  const nx=Math.cos(th), nz=Math.sin(th), PROT=1.028, NS=26, pts=[];
  for(let i=0;i<=NS;i++){
    const phi=2*Math.PI*i/NS,cp=Math.cos(phi),sp=Math.sin(phi);
    pts.push(new BABYLON.Vector3(r*nx+tr*PROT*cp*nx,tr*PROT*sp*HSCL,r*nz+tr*PROT*cp*nz));
  }
  ringPathMap.set(z,pts);
  const ring=BABYLON.MeshBuilder.CreateTube(`er${z}`,{path:pts,radius:RING_RAD_NORMAL,tessellation:7,cap:BABYLON.Mesh.NO_CAP},nauScene);
  ring.material=getCatMat(cat,false);
  ring.metadata={isElem:true,z,sym,name,cat,mass,period,group};
  elemMeshes.push(ring); ringMeshMap.set(z,ring);
});

/* ══════════════════════════════════════════════
   ENGINE B — ORBITAL / BOHR SCENE
══════════════════════════════════════════════ */
const engB=new BABYLON.Engine(canvasB,true,{antialias:true,stencil:true});
const orbScene=new BABYLON.Scene(engB);
orbScene.clearColor=new BABYLON.Color4(0.010,0.012,0.025,1.0);

/* camB: equatorial view (beta=PI/2) → nucleus at y=0 appears perfectly centered on rings */
const CAM_B_ALPHA=-Math.PI*0.3, CAM_B_BETA=0.960, CAM_B_RADIUS=10.7;
const camB=new BABYLON.ArcRotateCamera('camB',CAM_B_ALPHA,CAM_B_BETA,CAM_B_RADIUS,BABYLON.Vector3.Zero(),orbScene);
camB.lowerRadiusLimit=4; camB.upperRadiusLimit=40;
camB.wheelDeltaPercentage=0.015; camB.minZ=0.1;
camB.attachControl(canvasB,true);

/* Lighting for orbital/bohr */
const orbSun=new BABYLON.DirectionalLight('os',new BABYLON.Vector3(0.7,-0.8,0.4),orbScene);
orbSun.diffuse=new BABYLON.Color3(0.8,0.85,1.0); orbSun.intensity=0.90;
const orbAmb=new BABYLON.HemisphericLight('oa',new BABYLON.Vector3(0,1,0),orbScene);
orbAmb.diffuse=new BABYLON.Color3(0.20,0.20,0.35); orbAmb.groundColor=new BABYLON.Color3(0.05,0.05,0.10);
orbAmb.intensity=0.60;
const nucLight=new BABYLON.PointLight('nl',BABYLON.Vector3.Zero(),orbScene);
nucLight.diffuse=new BABYLON.Color3(1.0,0.78,0.32); nucLight.intensity=1.6; nucLight.range=12;

/* ── Orbital mat helper ── */
function mkOrbMat(hexColor,alpha){
  const mat=new BABYLON.StandardMaterial('om_'+Math.random().toString(36).slice(2),orbScene);
  const c=BABYLON.Color3.FromHexString(hexColor);
  mat.diffuseColor=c.scale(0.35); mat.emissiveColor=c.scale(0.55);
  mat.alpha=alpha; mat.transparencyMode=BABYLON.Material.MATERIAL_ALPHABLEND;
  mat.backFaceCulling=false; return mat;
}

/* ══════════════════════════════════════════════
   ORBITAL VISUALIZATION — Orbitron-accurate
   Shows the OUTERMOST electron's orbital shape.
   Color convention: + lobe warm (red/yellow), - lobe cool (blue/teal)
══════════════════════════════════════════════ */
/* lobe builder: elongated sphere along given axis */
function mkLobe(name, axis, sign, scale, color, alpha){
  const m=BABYLON.MeshBuilder.CreateSphere(name,{diameter:3.0,segments:12},orbScene);
  /* axis: 'x','y','z' */
  const sc = axis==='x' ? new BABYLON.Vector3(1.0,0.50,0.50)
           : axis==='y' ? new BABYLON.Vector3(0.50,1.0,0.50)
           :               new BABYLON.Vector3(0.50,0.50,1.0);
  m.scaling=sc.clone();
  m.scaling.x*=scale; m.scaling.y*=scale; m.scaling.z*=scale;
  const off=2.05*sign;
  m.position= axis==='x'?new BABYLON.Vector3(off,0,0)
            : axis==='y'?new BABYLON.Vector3(0,off,0)
            :             new BABYLON.Vector3(0,0,off);
  m.material=mkOrbMat(color,alpha);
  return m;
}
/* diagonal lobe for dxy/dxz/dyz */
function mkDiagLobe(name,ax1,ax2,sign1,sign2,color,alpha){
  const m=BABYLON.MeshBuilder.CreateSphere(name,{diameter:2.6,segments:10},orbScene);
  m.scaling=new BABYLON.Vector3(0.62,0.38,0.62);
  m.position=new BABYLON.Vector3(sign1*1.7, 0, sign2*1.7);
  if(ax1==='x'&&ax2==='z') m.position=new BABYLON.Vector3(sign1*1.7,sign2*1.7,0);
  if(ax1==='y'&&ax2==='z') m.position=new BABYLON.Vector3(0,sign1*1.7,sign2*1.7);
  m.material=mkOrbMat(color,alpha);
  return m;
}

/* Format config string like "1s² 2s² 2p³" */
function configStr(z){
const order=[
{t:'1s',c:2},{t:'2s',c:2},{t:'2p',c:6},{t:'3s',c:2},{t:'3p',c:6},
{t:'4s',c:2},{t:'3d',c:10},{t:'4p',c:6},{t:'5s',c:2},{t:'4d',c:10},
{t:'5p',c:6},{t:'6s',c:2},{t:'4f',c:14},{t:'5d',c:10},{t:'6p',c:6},
{t:'7s',c:2},{t:'5f',c:14},{t:'6d',c:10},{t:'7p',c:6}
];
const sup=['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹','¹⁰','¹¹','¹²','¹³','¹⁴'];
let parts=[],rem=z;
for(const {t,c} of order){
if(rem<=0)break;
const e=Math.min(rem,c);
parts.push(t+(sup[e]||e));
rem-=e;
}
return parts.join(' ');
}

/* ── Build orbital meshes — all filled orbitals, Orbitron proportions ── *//* ── Electron shell config (Bohr) ── */
function getElectronShells(z){
  const caps=[2,8,18,32,32,18,8]; const shells=[]; let rem=z;
  for(const cap of caps){ if(rem<=0)break; const n=Math.min(rem,cap); shells.push(n); rem-=n; }
  return shells;
}


/* ── Build Bohr model meshes — fused-cell nucleus ── */
function buildBohrMeshes(z, protons, neutrons, yOff=0){
  const meshes=[];
  const total=protons+neutrons;
  const nucR=Math.cbrt(total)*0.34+0.12;
  const show=Math.min(total,56);
  const particleDiam=Math.min(1.20, (2*nucR / Math.cbrt(Math.max(1,show))) * 1.55);

  const goldenAngle=Math.PI*(3-Math.sqrt(5));

  /* Step 1: pre-compute all positions */
  const positions=[];
  for(let i=0;i<show;i++){
    if(show===1){ positions.push([0,0,0]); continue; }
    const tNorm=(i+0.5)/show;
    const rad=nucR*Math.cbrt(tNorm);
    const y2=1-tNorm*2;
    const rxy=Math.sqrt(Math.max(0,1-y2*y2));
    const theta=goldenAngle*i;
    positions.push([rad*rxy*Math.cos(theta), rad*y2, rad*rxy*Math.sin(theta)]);
  }

  /* Step 2: Center nucleus using geometric center (min/max Y) */
  /* This ensures the visual "equator" aligns with orbital plane at Y=0 */
  /* Particularly important for large nuclei (Z >= 61) where Fibonacci */
  /* distribution creates visual asymmetry if using centroid */
  let minY = Infinity, maxY = -Infinity;
  positions.forEach(p => {
    if (p[1] < minY) minY = p[1];
    if (p[1] > maxY) maxY = p[1];
  });
  const geometricCenterY = (minY + maxY) / 2;
  positions.forEach(p => { p[1] -= geometricCenterY; });

  for(let i=0;i<show;i++){
    const [px,py,pz]=positions[i];
    const s=BABYLON.MeshBuilder.CreateSphere(`nc${i}`,
      {diameter:particleDiam, segments:9}, orbScene);
    s.position=new BABYLON.Vector3(px, py+yOff, pz);

    const isProton = (protons===0) ? false
                   : (neutrons===0) ? true
                   : Math.floor(i*protons/show) < Math.floor((i+1)*protons/show);
    const nm=new BABYLON.StandardMaterial(`ncm${i}`,orbScene);
    if(isProton){
      nm.diffuseColor  =new BABYLON.Color3(0.82,0.12,0.10);
      nm.specularColor =new BABYLON.Color3(1.0, 0.55,0.50);
      nm.emissiveColor =new BABYLON.Color3(0.22,0.02,0.01);
    } else {
      nm.diffuseColor  =new BABYLON.Color3(0.12,0.20,0.85);
      nm.specularColor =new BABYLON.Color3(0.55,0.62,1.0);
      nm.emissiveColor =new BABYLON.Color3(0.01,0.02,0.22);
    }
    nm.specularPower=14;
    s.material=nm; meshes.push(s);
  }

  // Electron shells — all centered at yOff on Y axis
  const shells=getElectronShells(z);
  const shellColors=['#44FF88','#44CCFF','#FFDD44','#FF8844','#CC44FF','#FF4488','#88FFCC'];
  const shellParents = []; // Store parent nodes for rotation
  
  /* First shell radius proportional to nucleus size (prevents collision for large nuclei) */
  /* Using 2.0× multiplier to ensure sufficient clearance, especially from K (Z=19) onwards */
  const firstShellRadius = Math.max(1.5, nucR * 2.0);
  
  shells.forEach((eCount,si)=>{
    const rad = firstShellRadius + si * 2.0; // Evenly spaced from first shell
    
    // Create parent node for this shell (ring + electrons)
    const shellParent = new BABYLON.TransformNode(`shell${si}`, orbScene);
    shellParent.position.y = yOff;
    shellParent.metadata = { shellIndex: si, radius: rad }; // Store metadata for rotation speed
    shellParents.push(shellParent);
    
    // Create ring and parent it to shellParent
    const ring=BABYLON.MeshBuilder.CreateTorus(`shring${si}`,{
      diameter:rad*2, thickness:0.035, tessellation:80
    },orbScene);
    ring.position.y = 0; // Relative to parent (parent already at yOff)
    ring.parent = shellParent;
    const rm=new BABYLON.StandardMaterial(`shringm${si}`,orbScene);
    rm.emissiveColor=BABYLON.Color3.FromHexString(shellColors[si%shellColors.length]).scale(0.55);
    rm.alpha=0.50; ring.material=rm; meshes.push(ring);

    // Create electrons and parent them to shellParent
    const eShow=Math.min(eCount,20);
    for(let e=0;e<eShow;e++){
      const ang=(e/eShow)*Math.PI*2;
      const el=BABYLON.MeshBuilder.CreateSphere(`el${si}_${e}`,{diameter:0.20,segments:6},orbScene);
      el.position=new BABYLON.Vector3(rad*Math.cos(ang), 0, rad*Math.sin(ang)); // Relative to parent
      el.parent = shellParent;
      const em=new BABYLON.StandardMaterial(`elm${si}_${e}`,orbScene);
      em.emissiveColor=BABYLON.Color3.FromHexString(shellColors[si%shellColors.length]);
      el.material=em; meshes.push(el);
    }
  });
  
  // Return both meshes and shellParents for rotation
  return { meshes, shellParents };
}

/* ── Scene switcher ── */
let orbMeshes=[], shellParents=[], fadeObs=null;
function clearOrbitalScene(){
  /* Cancel fade animation first */
  if(fadeObs){ orbScene.onBeforeRenderObservable.remove(fadeObs); fadeObs=null; }
  /* Dispose ALL non-system meshes in the orbital scene to avoid ghost meshes */
  const toDispose=orbScene.meshes.slice(); /* copy — array mutates during dispose */
  toDispose.forEach(m=>{
    if(m.name==='BackgroundHelper'||m.name==='BackgroundPlane'||m.name==='BackgroundSkybox') return;
    if(m.material){ m.material.dispose(false,true); }
    m.dispose();
  });
  orbMeshes=[];
}

function getOrbitalMode(){ return 'bohr'; }


function showVisualization(elem){
  clearOrbitalScene();
  const mode=getOrbitalMode();
  if(mode==='bohr'){
    const neutrons = elem.z===1 ? 0
                   : elem.z<=20 ? elem.z
                   : Math.round(elem.z * (1 + (elem.z-20)*0.006));
    const nShells=getElectronShells(elem.z).length;
    const yOff = 0; /* nucleus at origin — geometrically correct */
    const result = buildBohrMeshes(elem.z, elem.z, neutrons, yOff);
    orbMeshes = result.meshes;
    shellParents = result.shellParents;
    camB.radius=Math.max(6.7, (nShells*2.6+2.5)*1.333);
    camB.target=BABYLON.Vector3.Zero(); /* orbit around atom center */
  }
  const targets=orbMeshes.map(m=>({mesh:m,target:m.material?.alpha||1}));
  targets.forEach(({mesh})=>{if(mesh.material)mesh.material.alpha=0;});
  let e2=0;
  fadeObs=orbScene.onBeforeRenderObservable.add(()=>{
    e2+=engB.getDeltaTime()/1000;
    const f=Math.min(1,e2/0.50);
    targets.forEach(({mesh,target})=>{
      if(mesh&&!mesh.isDisposed()&&mesh.material) mesh.material.alpha=target*f;
    });
    if(f>=1){orbScene.onBeforeRenderObservable.remove(fadeObs);fadeObs=null;}
  });
}

/* ── Sync both orbital-mode selectors ── */
/* orbital mode selector sync removed — Bohr only */

/* ══════════════════════════════════════════════
   FAMILY SELECTION
══════════════════════════════════════════════ */
let selectedCat=null, hlRings=[];

function populateSelect(filterCat=null){
  const sel=document.getElementById('elem-select'); if(!sel)return;
  sel.innerHTML='';
  const items=filterCat?EL.filter(e=>e[5]===filterCat):EL;
  items.forEach(([z,sym,name])=>{
    const opt=document.createElement('option');
    opt.value=z; opt.textContent=`${z}: ${sym} - ${name}`; /* format: "1: H - Hydrogen" */
    if(z===currentZ) opt.selected=true;
    sel.appendChild(opt);
  });
}

function selectFamily(cat){
  hlRings.forEach(r=>{try{HL.removeMesh(r);}catch(e){}});
  hlRings=[];
  selectedCat=cat;
  const col=BABYLON.Color3.FromHexString(CAT_HEX[cat]);
  
  // Keep ALL rings visible and unchanged - only highlight family rings
  elemMeshes.forEach(ring=>{
    if(!ring.metadata) return;
    if(ring.metadata.cat===cat){
      ring.visibility=1.0; ring.isPickable=true;
      ring.material=getCatMat(cat,true);
      HL.addMesh(ring,col); hlRings.push(ring);
    } else {
      // Keep other rings completely unchanged
      ring.visibility=1.0;
      ring.isPickable=true;
      ring.material=getCatMat(ring.metadata.cat,false);
    }
  });
  populateSelect(cat);
  const first=EL.find(e=>e[5]===cat);
  if(first) showElement(first[0]);
  
  // Update Description tab - scroll to family section
  const descPanel = document.querySelectorAll('.tab-panel')[0];
  activateTab(0); // Switch to Description tab
  const familySection = document.getElementById(`family-${cat}`);
  if (familySection) {
    // Smooth scroll to family section
    setTimeout(() => {
      familySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }
  
  // FAMILY SELECTION MODE VISUALS
  // 1. Make shell highly translucent with wireframe
  if (shellMesh && shellMesh.material) {
    shellMesh.material.wireframe = true;
    shellMesh.material.alpha = 0.05; // Very translucent - almost invisible
  }
  
  // 2. Create luminous connection lines between family ring centers
  // Clean up old lines first
  familyConnectionLines.forEach(line => {
    try { line.dispose(); } catch(e) {}
  });
  familyConnectionLines.length = 0;
  
  // Get family rings sorted by atomic number
  const familyRings = elemMeshes
    .filter(ring => ring.metadata && ring.metadata.cat === cat)
    .sort((a, b) => a.metadata.z - b.metadata.z);
  
  // Create luminous path connecting ring centers
  if (familyRings.length > 1) {
    const points = familyRings.map(ring => ring.position.clone());
    
    // Use CreateTube for thick, highly visible lines
    const line = BABYLON.MeshBuilder.CreateTube(`familyPath_${cat}`, {
      path: points,
      radius: 0.15,  // Thicker for high visibility
      tessellation: 12,
      cap: BABYLON.Mesh.CAP_ALL,
      updatable: false
    }, nauScene);
    
    // Create bright glowing material
    const lineMat = new BABYLON.StandardMaterial(`familyPathMat_${cat}`, nauScene);
    lineMat.emissiveColor = col.scale(1.5); // Brighter emission
    lineMat.diffuseColor = col;
    lineMat.alpha = 1.0; // Fully opaque
    line.material = lineMat;
    line.isPickable = false;
    
    // Add very strong glow
    HL.addMesh(line, col.scale(1.2));
    
    familyConnectionLines.push(line);
  }
}

function clearFamilySelection(){
  hlRings.forEach(r=>{try{HL.removeMesh(r);}catch(e){}});
  hlRings=[]; selectedCat=null;
  elemMeshes.forEach(ring=>{
    if(!ring.metadata) return;
    ring.visibility=1.0; ring.isPickable=true;
    ring.material=getCatMat(ring.metadata.cat,false);
  });
  populateSelect();
  
  // Scroll Description tab back to top
  const descPanel = document.querySelectorAll('.tab-panel')[0];
  if (descPanel) {
    descPanel.scrollTop = 0;
  }
  
  // RESTORE NORMAL VISUALS
  // 1. Restore shell to normal (opaque with no wireframe)
  if (shellMesh && shellMesh.material) {
    shellMesh.material.wireframe = false;
    shellMesh.material.alpha = 1.0; // Fully opaque
  }
  
  // 2. Remove connection lines (including from highlight layer)
  familyConnectionLines.forEach(line => {
    try {
      HL.removeMesh(line);
      line.dispose();
    } catch(e) {}
  });
  familyConnectionLines.length = 0;
}

/* ── Build families legend ── */
const famList=document.getElementById('families-list');
Object.entries(CAT_NAME).forEach(([k,v])=>{
  const d=document.createElement('div'); d.className='leg';
  d.innerHTML=`<div class="ld" style="background:${CAT_HEX[k]}"></div>${v}`;
  d.addEventListener('click',()=>{
    const already=(selectedCat===k);
    document.querySelectorAll('.leg').forEach(l=>l.classList.remove('leg-sel'));
    if(already) clearFamilySelection();
    else { selectFamily(k); d.classList.add('leg-sel'); }
  });
  famList.appendChild(d);
});

document.getElementById('legend-clear').addEventListener('click',()=>{
  clearFamilySelection();
  document.querySelectorAll('.leg').forEach(l=>l.classList.remove('leg-sel'));
});

/* ══════════════════════════════════════════════
   ATOMIC CARD — tile style
══════════════════════════════════════════════ */
const atTile=document.getElementById('atomic-tile');
const atZ=document.getElementById('at-z');
const atSym=document.getElementById('at-sym');
const atName=document.getElementById('at-name');
const atMass=document.getElementById('at-mass');
const atCatRow=document.getElementById('at-cat-row');
const atBlkRow=document.getElementById('at-blk-row');
const acZLabel=document.getElementById('ac-z-label');
const acLeft=document.getElementById('ac-left');
const acRight=document.getElementById('ac-right');
const chipElem=document.getElementById('chip-elem');

let currentZ=1, hovMesh=null;

function hexToRgb(hex){
  const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
  return [r,g,b];
}

function showElement(z){
  currentZ=Math.max(1,Math.min(118,z));
  const [ez,sym,name,period,group,cat,mass]=EL[currentZ-1];
  const hex=CAT_HEX[cat];
  const [r,g,b]=hexToRgb(hex);

  // Tile background: category color, semi-transparent over dark bg
  atTile.style.background=`rgba(${r},${g},${b},0.70)`;
  atTile.style.borderColor=`rgba(${r},${g},${b},0.88)`;

  atZ.textContent=currentZ;
  atSym.textContent=sym;
  atName.textContent=name;
  atMass.textContent=mass;
  atCatRow.textContent=CAT_NAME[cat];
  atCatRow.style.color=`rgba(${Math.max(0,r-60)},${Math.max(0,g-60)},${Math.max(0,b-60)},0.90)`;
  atBlkRow.textContent=`Block-${BLOCK[cat]} · Period ${Math.floor(period+0.05)} · Group ${group}`;

  acZLabel.textContent=`Z = ${currentZ}`;
  acLeft.disabled=(currentZ<=1); acLeft.style.opacity=(currentZ<=1)?'0.22':'1';
  acRight.disabled=(currentZ>=118); acRight.style.opacity=(currentZ>=118)?'0.22':'1';

  chipElem.textContent=`${sym} — ${name}`;
  chipElem.style.borderColor=`rgba(${r},${g},${b},0.45)`;
  chipElem.style.color=`rgba(${Math.min(255,r+80)},${Math.min(255,g+80)},${Math.min(255,b+80)},0.88)`;

  const sel=document.getElementById('elem-select');
  if(sel) sel.value=currentZ;

  setSelectedElemRing(currentZ);
  showVisualization({z:ez,sym,name,period,group,cat,mass});
}

/* Wikipedia link on symbol click */
atSym.addEventListener('click',()=>{
  const name=EL[currentZ-1][2].replace(/ /g,'_');
  window.open(`https://en.wikipedia.org/wiki/${name}`,'_blank');
});

acLeft.addEventListener('click',()=>showElement(currentZ-1));
acRight.addEventListener('click',()=>showElement(currentZ+1));
document.getElementById('elem-select').addEventListener('change',function(){ showElement(parseInt(this.value)); });
document.getElementById('ac-clear-sel').addEventListener('click',()=>showElement(1));
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowLeft'||e.key==='ArrowDown') showElement(currentZ-1);
  if(e.key==='ArrowRight'||e.key==='ArrowUp')  showElement(currentZ+1);
});

/* ══════════════════════════════════════════════
   HOVER / PICK on Nautilus
══════════════════════════════════════════════ */
const hoveredVal=document.getElementById('hovered-val');
let isDragging=false;
canvasA.addEventListener('pointerdown',()=>{isDragging=false;});
canvasA.addEventListener('pointermove',e=>{if(e.buttons===1)isDragging=true;});
canvasA.addEventListener('pointerup',()=>{isDragging=false;});

nauScene.onPointerObservable.add(pi=>{
  if(pi.type===BABYLON.PointerEventTypes.POINTERMOVE){
    const hit=nauScene.pick(nauScene.pointerX,nauScene.pointerY,m=>m.metadata?.isElem&&m.isPickable);
    if(hit.hit&&hit.pickedMesh){
      const d=hit.pickedMesh.metadata;
      hoveredVal.textContent=`${d.z}: ${d.sym} - ${d.name}`;
      canvasA.style.cursor='pointer'; hovMesh=hit.pickedMesh;
    } else {
      hoveredVal.textContent='—'; canvasA.style.cursor='default'; hovMesh=null;
    }
    return;
  }
  if(pi.type===BABYLON.PointerEventTypes.POINTERUP){
    if(isDragging) return;
    const hit=nauScene.pick(nauScene.pointerX,nauScene.pointerY,m=>m.metadata?.isElem&&m.isPickable);
    if(hit.hit&&hit.pickedMesh) showElement(hit.pickedMesh.metadata.z);
  }
});

/* ══════════════════════════════════════════════
   ACTIVE VIEW TOGGLE — capture phase
══════════════════════════════════════════════ */
viewNE.addEventListener('pointerdown',e=>{
  if(e.isPrimary&&e.button===0) viewNE.classList.add('ne-active');
},{capture:true});
viewMain.addEventListener('pointerdown',e=>{
  if(e.isPrimary&&e.button===0) viewNE.classList.remove('ne-active');
},{capture:true});

/* ══════════════════════════════════════════════
   BOTTOM BUTTONS
══════════════════════════════════════════════ */
let autoRotating=false;
let bohrBetaDir=1; /* oscillation direction for Bohr YZ rotation */
const btnAuto=document.getElementById('btn-autorot');

btnAuto.addEventListener('click',()=>{
  autoRotating=!autoRotating;
  /* Apply auto-rotation to the CURRENTLY ACTIVE view */
  const neActive=viewNE.classList.contains('ne-active');
  if(neActive){
    /* NE is active → rotate orbital/Bohr (handled in engB render loop) */
    // Rotation logic is in engB.runRenderLoop
  } else {
    /* Main view is active → rotate Nautilus */
    camA.useAutoRotationBehavior=autoRotating;
    if(autoRotating&&camA.autoRotationBehavior){
      camA.autoRotationBehavior.idleRotationSpeed=0.20;
      camA.autoRotationBehavior.idleRotationWaitTime=0;
    }
  }
  btnAuto.classList.toggle('on',autoRotating);
  btnAuto.textContent=autoRotating?'⟳ Auto Rotate ON':'⟳ Auto Rotate';
});

const NE_DEFAULT_W=192, NE_DEFAULT_H=290;

document.getElementById('btn-reset').addEventListener('click',()=>{
  /* Main Nautilus camera */
  camA.alpha=CAM_ALPHA; camA.beta=CAM_BETA; camA.radius=CAM_RADIUS;
  camA.target=BABYLON.Vector3.Zero();
  /* Orbital camera */
  camB.alpha=CAM_B_ALPHA; camB.beta=CAM_B_BETA; camB.radius=CAM_B_RADIUS;
  camB.target=BABYLON.Vector3.Zero();
  /* NE panel: restore default size + expand if collapsed */
  viewNE.style.width=NE_DEFAULT_W+'px';
  viewNE.style.height=NE_DEFAULT_H+'px';
  if(neCollapsed){
    neCollapsed=false;
    neBodyEl.style.display='';
    neTitlebarEl.style.borderRadius='0';
    neToggle.textContent='-';
    setTimeout(()=>engB.resize(),12);
  } else {
    neSavedH=NE_DEFAULT_H;
    setTimeout(()=>engB.resize(),12);
  }
  /* Stop auto-rotate */
  autoRotating=false;
  camA.useAutoRotationBehavior=false;
  btnAuto.classList.remove('on');
  btnAuto.textContent='⟳ Auto Rotate';
  /* Family + element reset, set Bohr as default mode */
  clearFamilySelection();
  document.querySelectorAll('.leg').forEach(l=>l.classList.remove('leg-sel'));
  document.getElementById('orbital-mode-sel').value='bohr';
  populateSelect(); showElement(7);
  
  /* Reset splitter position (sidebar width) */
  document.documentElement.style.setProperty('--sidebar-w', '360px');
  updateNEPosition(); // Update NE panel position based on new sidebar width
  resizeEngines(); // Resize both engines
});

/* ══════════════════════════════════════════════
   SWAP
══════════════════════════════════════════════ */
const swapBtn=document.getElementById('swap-btn');
const orbModeSel=document.getElementById('orbital-mode-sel');
const orbModeInline=document.getElementById('orbital-mode-inline');

function applyLayout(){
  console.log(`🔧 applyLayout() called - swapped=${swapped}`);
  const neBody=document.getElementById('ne-body');
  const resH=document.getElementById('ne-resize-handle');
  const mainOrbBar=document.getElementById('main-orb-bar');
  if(!swapped){
    /* A=nautilus=main, B=orbital=NE */
    viewMain.appendChild(canvasA);
    neBody.insertBefore(canvasB,resH);
    orbModeSel.style.display=''; orbModeInline.style.display='none';
    if(mainOrbBar) mainOrbBar.style.display='none';
  } else {
    /* B=orbital=main, A=nautilus=NE */
    viewMain.appendChild(canvasB);
    neBody.insertBefore(canvasA,resH);
    orbModeSel.style.display='none'; orbModeInline.style.display='none';
    if(mainOrbBar) mainOrbBar.style.display='block';
  }
  setTimeout(()=>{
    engA.resize();
    engB.resize();
    console.log('🔧 applyLayout() resize completed');
  },12);
}
applyLayout();
swapBtn.addEventListener('click',()=>{ 
  swapped=!swapped; 
  applyLayout();
  console.log('🔄 SWAP triggered');
  setTimeout(() => logAspectRatioDiagnostic('After SWAP'), 50);
});

/* ══════════════════════════════════════════════
   NE PANEL — EXPAND / COLLAPSE
══════════════════════════════════════════════ */
const neToggle=document.getElementById('ne-toggle');
const neBodyEl=document.getElementById('ne-body');
const neTitlebarEl=document.getElementById('ne-titlebar');
let neCollapsed=false, neSavedH=280;

neToggle.addEventListener('click',e=>{
  neCollapsed=!neCollapsed;
  if(neCollapsed){
    console.log('📦 NE PANEL collapsed');
    neSavedH=viewNE.offsetHeight;
    neBodyEl.style.display='none';
    viewNE.style.height='34px';
    neTitlebarEl.style.borderRadius='0 0 0 8px';
    neToggle.textContent='+';
  } else {
    console.log('📦 NE PANEL expanded');
    neBodyEl.style.display='';
    viewNE.style.height=neSavedH+'px';
    neTitlebarEl.style.borderRadius='0';
    neToggle.textContent='-';
    setTimeout(()=>{
      engB.resize();
      logAspectRatioDiagnostic('After NE EXPAND');
    },50);
  }
  e.stopPropagation();
});

/* ══════════════════════════════════════════════
   NE PANEL — RESIZE (bottom-left handle)
   Panel is anchored top-right.
   Dragging left → wider; dragging down → taller.
══════════════════════════════════════════════ */
const resHandle=document.getElementById('ne-resize-handle');
let resizing=false,rsX,rsY,rsW,rsH;
let lastDiagnosticTime = 0;

resHandle.addEventListener('pointerdown',e=>{
  if(e.button!==0)return;
  resizing=true; rsX=e.clientX; rsY=e.clientY;
  rsW=viewNE.offsetWidth; rsH=viewNE.offsetHeight;
  resHandle.setPointerCapture(e.pointerId);
  e.stopPropagation(); e.preventDefault();
  console.log('🔧 SPLITTER RESIZE started');
},{capture:true});
window.addEventListener('pointermove',e=>{
  if(!resizing)return;
  const dw=rsX-e.clientX;
  const dh=e.clientY-rsY;
  viewNE.style.width =Math.max(160,Math.min(720,rsW+dw))+'px';
  viewNE.style.height=Math.max(80, Math.min(860,rsH+dh))+'px';
  
  // Resize BOTH engines (not just B)
  // A might be in Main and affected by NE size change
  if (window.engA) engA.resize();
  if (window.engB) engB.resize();
  
  // Log diagnostic every 500ms to avoid console spam
  const now = Date.now();
  if (now - lastDiagnosticTime > 500) {
    logAspectRatioDiagnostic('During SPLITTER RESIZE');
    lastDiagnosticTime = now;
  }
});
window.addEventListener('pointerup',()=>{
  if(resizing) {
    resizing=false;
    console.log('🔧 SPLITTER RESIZE ended');
    setTimeout(() => logAspectRatioDiagnostic('After SPLITTER RESIZE'), 50);
  }
});

/* ══════════════════════════════════════════════
   RENDER LOOPS
══════════════════════════════════════════════ */
let elapsed=0;
const BOHR_BETA_MIN=Math.PI*0.18, BOHR_BETA_MAX=Math.PI*0.82;

engA.runRenderLoop(()=>{
  const dt=engA.getDeltaTime()/1000; elapsed+=dt;
  nacreMat.setFloat('uTime',elapsed);
  /* Auto-rotate Nautilus when it's in active view */
  const neActive = viewNE.classList.contains('ne-active');
  // A rotates if: in main and main active, OR in NE and NE active
  if(autoRotating && ((!swapped && !neActive) || (swapped && neActive))){
    camA.alpha-=0.0022;
  }
  nauScene.render();
});

engB.runRenderLoop(()=>{
  nucLight.intensity=1.5+Math.sin(Date.now()*0.002)*0.22;
  /* Auto-rotate orbital/Bohr when it's in active view */
  const neActive = viewNE.classList.contains('ne-active');
  // B rotates if: in main and main active, OR in NE and NE active
  if(autoRotating && ((swapped && !neActive) || (!swapped && neActive))){
    const mode=document.getElementById('orbital-mode-sel').value;
    if(mode==='bohr'){
      /* Rotate each shell around X axis with speed inversely proportional to radius */
      const speedSlider = document.getElementById('rotation-speed-slider');
      const speedMultiplier = speedSlider ? parseFloat(speedSlider.value) : 1.17;
      shellParents.forEach(parent => {
        const baseSpeed = 0.01 * speedMultiplier; // Base speed × slider value (+17% default)
        const radius = parent.metadata.radius; // Stored in metadata
        const speed = baseSpeed / radius; // Inversely proportional
        parent.rotation.x += speed;
      });
    } else {
      /* Orbital: spin around Y axis */
      camB.alpha+=0.0025;
    }
  }
  orbScene.render();
});
/* ══════════════════════════════════════════════
   DIAGNOSTIC ASPECT RATIO
══════════════════════════════════════════════ */
function logAspectRatioDiagnostic(context) {
  console.group(`🔍 ASPECT RATIO DIAGNOSTIC - ${context}`);
  
  // Window dimensions
  console.log('🖥️ Window:');
  console.log(`  - innerWidth: ${window.innerWidth}px`);
  console.log(`  - innerHeight: ${window.innerHeight}px`);
  
  // Canvas dimensions
  console.log('📐 Canvas A (Nautilus):');
  console.log(`  - canvas.width: ${canvasA.width}px`);
  console.log(`  - canvas.height: ${canvasA.height}px`);
  console.log(`  - clientWidth: ${canvasA.clientWidth}px`);
  console.log(`  - clientHeight: ${canvasA.clientHeight}px`);
  console.log(`  - aspect ratio: ${(canvasA.width / canvasA.height).toFixed(3)}`);
  
  console.log('📐 Canvas B (Orbital):');
  console.log(`  - canvas.width: ${canvasB.width}px`);
  console.log(`  - canvas.height: ${canvasB.height}px`);
  console.log(`  - clientWidth: ${canvasB.clientWidth}px`);
  console.log(`  - clientHeight: ${canvasB.clientHeight}px`);
  console.log(`  - aspect ratio: ${(canvasB.width / canvasB.height).toFixed(3)}`);
  
  // Container dimensions
  const viewMainRect = viewMain.getBoundingClientRect();
  const viewNERect = viewNE.getBoundingClientRect();
  console.log('📦 View Main Container:');
  console.log(`  - width: ${viewMainRect.width}px`);
  console.log(`  - height: ${viewMainRect.height}px`);
  console.log(`  - aspect ratio: ${(viewMainRect.width / viewMainRect.height).toFixed(3)}`);
  
  console.log('📦 View NE Container:');
  console.log(`  - width: ${viewNERect.width}px`);
  console.log(`  - height: ${viewNERect.height}px`);
  console.log(`  - aspect ratio: ${(viewNERect.width / viewNERect.height).toFixed(3)}`);
  console.log(`  - ne-active: ${viewNE.classList.contains('ne-active')}`);
  
  // Camera parameters
  console.log('📷 Camera A (Nautilus):');
  console.log(`  - fov: ${camA.fov}`);
  console.log(`  - alpha: ${camA.alpha.toFixed(3)}`);
  console.log(`  - beta: ${camA.beta.toFixed(3)}`);
  console.log(`  - radius: ${camA.radius.toFixed(3)}`);
  
  console.log('📷 Camera B (Orbital):');
  console.log(`  - fov: ${camB.fov}`);
  console.log(`  - alpha: ${camB.alpha.toFixed(3)}`);
  console.log(`  - beta: ${camB.beta.toFixed(3)}`);
  console.log(`  - radius: ${camB.radius.toFixed(3)}`);
  
  // Swap state
  console.log('🔄 Swap State:');
  console.log(`  - swapped: ${swapped}`);
  console.log(`  - A in: ${!swapped ? 'MAIN' : 'NE'}`);
  console.log(`  - B in: ${swapped ? 'MAIN' : 'NE'}`);
  
  // CSS Variables
  console.log('🎨 CSS Variables:');
  const sidebarW = getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w');
  console.log(`  - --sidebar-w: ${sidebarW}`);
  
  // Grid calculation
  const leftPanel = 203;
  const splitterWidth = 5;
  const sidebarWidth = parseInt(sidebarW) || 360;
  const totalFixed = leftPanel + splitterWidth + sidebarWidth;
  const availableForMain = window.innerWidth - totalFixed;
  console.log('📏 Grid Calculation:');
  console.log(`  - Left panel: ${leftPanel}px`);
  console.log(`  - Splitter: ${splitterWidth}px`);
  console.log(`  - Sidebar: ${sidebarWidth}px`);
  console.log(`  - Total fixed: ${totalFixed}px`);
  console.log(`  - Available for Main: ${availableForMain}px`);
  console.log(`  - Main actual: ${viewMain.getBoundingClientRect().width.toFixed(1)}px`);
  
  console.groupEnd();
}

// Window resize with diagnostic and loop protection
let resizeTimeout;
let isResizing = false;

window.addEventListener('resize',()=>{
  if (isResizing) {
    console.warn('⚠️ Resize loop detected - skipping');
    return;
  }
  
  isResizing = true;
  
  // Check if --sidebar-w is too large for current window
  const currentSidebarW = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w')) || 360;
  const maxSafeWidth = Math.floor(window.innerWidth * 0.5);
  if (currentSidebarW > maxSafeWidth) {
    const newWidth = Math.max(180, maxSafeWidth); // 180 = MIN_W
    document.documentElement.style.setProperty('--sidebar-w', newWidth+'px');
    console.log(`📐 Auto-adjusted sidebar: ${currentSidebarW}px → ${newWidth}px (window too narrow)`);
  }
  
  engA.resize();
  engB.resize();
  
  // Debounce diagnostic logging
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    logAspectRatioDiagnostic('After WINDOW RESIZE');
    isResizing = false;
  }, 300);
});

// Log initial state after page load
setTimeout(() => logAspectRatioDiagnostic('INITIAL STATE'), 500);

/* ══════════════════════════════════════════════
   TAB SWITCHING
══════════════════════════════════════════════ */
function activateTab(index) {
  const btns = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');
  
  btns.forEach((btn, i) => {
    if (i === index) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
  
  panels.forEach((panel, i) => {
    if (i === index) {
      panel.classList.add('active');
    } else {
      panel.classList.remove('active');
    }
  });
}

/* ── Init ── */
populateSelect();
showElement(7);

// ═══════════════════════════════════════════════════════════════════
// SPLITTER (drag to resize sidebar)
// Tested and working (mousedown pattern from NuclearReactorsTypology)
// ═══════════════════════════════════════════════════════════════════
(function() {
  const splitter = document.getElementById('splitter');
  const viewNE = document.getElementById('view-ne');
  
  if (!splitter) {
    console.warn('⚠️ Splitter element not found');
    return;
  }
  
  let draggingSp = false, startX = 0, startW = 0;
  const MIN_W = 180, MAX_W = 640;

  // Helper function to update NE panel position
  function updateNEPosition() {
    if (!viewNE) return;
    const sidebarW = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w')) || 360;
    const splitterRect = splitter.getBoundingClientRect();
    const neWidth = viewNE.offsetWidth;
    // Position NE panel: X_splitter - width_NE
    const rightPos = window.innerWidth - splitterRect.left + neWidth;
    viewNE.style.right = sidebarW + 5 + 'px'; // sidebar width + splitter width
  }

  // Helper function to resize BabylonJS engines
  function resizeEngines() {
    if (window.engA) {
      window.engA.resize();
      // Force camera aspect ratio update for Nautilus scene
      if (camA) {
        camA.getProjectionMatrix(true);
      }
    }
    if (window.engB) {
      window.engB.resize();
      // Force camera aspect ratio update for Orbital scene
      if (camB) {
        camB.getProjectionMatrix(true);
      }
    }
  }

  splitter.addEventListener('mousedown', function(e) {
    draggingSp = true;
    startX = e.clientX;
    startW = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sidebar-w')) || 360;
    splitter.classList.add('dragging');
    e.preventDefault();
  });

  window.addEventListener('mousemove', function(e) {
    if (!draggingSp) return;
    const dx = startX - e.clientX;
    let nw = Math.min(MAX_W, Math.max(MIN_W, startW + dx));
    
    // CRITICAL: Limit sidebar to 50% of window width to prevent collapse
    const maxSafeWidth = Math.floor(window.innerWidth * 0.5);
    if (nw > maxSafeWidth) {
      nw = maxSafeWidth;
      console.warn(`⚠️ Sidebar limited to ${maxSafeWidth}px (50% of window)`);
    }
    
    document.documentElement.style.setProperty('--sidebar-w', nw+'px');
    updateNEPosition();
    // Use requestAnimationFrame + setTimeout for CSS Grid to finish
    if (!window.splitterResizePending) {
      window.splitterResizePending = true;
      requestAnimationFrame(() => {
        // Wait for CSS Grid recalculation
        setTimeout(() => {
          resizeEngines();
          window.splitterResizePending = false;
        }, 16); // ~1 frame delay
      });
    }
  });

  window.addEventListener('mouseup', function() {
    if (draggingSp) {
      draggingSp = false;
      splitter.classList.remove('dragging');
      updateNEPosition();
      resizeEngines();
    }
  });

  // Initial positioning
  updateNEPosition();
  
  // Update on window resize
  window.addEventListener('resize', function() {
    updateNEPosition();
  });

  console.log('✅ Splitter initialized (mousedown/mousemove/mouseup + NE repositioning)');
})();

console.log('✅ All JavaScript loaded successfully');
