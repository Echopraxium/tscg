// src/sceneBuilder.js - Construction de la scène Layer Cake

// Fonction pour créer un mesh avec wireframe
function createBoxWithEdges(nm, w, h, d, x, y, z, m, edgeColor = new BABYLON.Color3(0, 1, 1), alpha = 1.0) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { width: w, height: h, depth: d }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  
  mesh.enableEdgesRendering();
  mesh.edgesWidth = 2.0;
  mesh.edgesColor = edgeColor;
  
  return mesh;
}

function createBoxNoEdges(nm, w, h, d, x, y, z, m) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { width: w, height: h, depth: d }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  return mesh;
}

function mat(r, g, b, al, er, eg, eb) {
  const m = new BABYLON.StandardMaterial(`mat_${Date.now()}`, scene);
  m.diffuseColor = new BABYLON.Color3(r, g, b);
  if (al != null && al < 1) { m.alpha = al; }
  if (er != null) m.emissiveColor = new BABYLON.Color3(er, eg, eb);
  m.backFaceCulling = false;
  return m;
}

function box(nm, w, h, d, x, y, z, m) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { width: w, height: h, depth: d }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  return mesh;
}

function buildScene() {
  // Manteau inférieur
  const mantle = createBoxNoEdges('mantle', 14, 3.5, 5, 0, -2.8, 0, mat(.68, .03, .01, 1.0));
  
  // Lithosphère
  const lithoBase = createBoxWithEdges('lithoBase', 14, 1.00, 5, 0, -0.40, 0, mat(.55, .40, .25, 1.0), new BABYLON.Color3(0, 1, 1), 1.0);
  
  const GAP2 = 0.06;
  const PW = (7 - GAP2 * 2) / 3;
  const PD = (5 - GAP2 * 2) / 3;
  
  const cc = [
    [.65, .52, .34], [.60, .48, .30], [.58, .46, .28],
    [.62, .50, .32], [.64, .51, .33], [.56, .44, .27],
    [.63, .50, .31], [.61, .49, .30], [.59, .47, .29]
  ];

  // Plaques continentales
  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const cx = -7 + GAP2 + PW * .5 + c2 * (PW + GAP2);
      const cz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      const contPlate = createBoxWithEdges(`cc_${idx}`, PW, 1.20, PD, cx, 0.60, cz, mat(...cc[idx], 1.0), new BABYLON.Color3(0, 1, 1), 1.0);
      continentalPlates.push(contPlate);
      
      const soilPlate = createBoxWithEdges(`cs_${idx}`, PW, 0.15, PD, cx, 1.25, cz, mat(...cc[idx].map(v => v * .85), 1.0), new BABYLON.Color3(0, 1, 1), 1.0);
      
      if (c2 < 2) {
        const fm = mat(.25, .65, .15, 1, .05, .15, 0);
        faultMats.push(fm);
        const faultMesh = createBoxWithEdges(`fh_${idx}`, .05, 0.15, PD, cx + PW * .5 + GAP2 * .5, 1.30, cz, fm, new BABYLON.Color3(1, 0.5, 0), 1.0);
      }
    }
  }
  
  // Couche continentale supérieure
  const contTop = createBoxWithEdges('contTop', 7, 0.12, 5, -3.5, 1.50, 0, mat(.47, .40, .26, 1.0), new BABYLON.Color3(0, 1, 1), 1.0);

  // Plaques océaniques
  const oc = [
    [.12, .19, .38], [.14, .21, .40], [.11, .18, .36],
    [.13, .20, .39], [.15, .22, .41], [.10, .17, .35],
    [.12, .19, .37], [.13, .20, .38], [.11, .18, .36]
  ];
  
  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const ox = GAP2 + PW * .5 + c2 * (PW + GAP2);
      const oz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      const oceanLitho = createBoxWithEdges(`rlitho_${idx}`, PW, 0.80, PD, ox, -0.30, oz, mat(.20, .18, .30, 1.0), new BABYLON.Color3(0, 1, 1), 1.0);
      const oceanCrust = createBoxWithEdges(`rcrust_${idx}`, PW, 0.40, PD, ox, 0.30, oz, mat(...oc[idx], 1.0), new BABYLON.Color3(0, 1, 1), 1.0);
      const oceanWater = createBoxWithEdges(`rocean_${idx}`, PW, 0.60, PD, ox, 0.85, oz, mat(.04, .22, .68, 0.85), new BABYLON.Color3(0, 1, 1), 0.85);
    }
  }

  // Dorsale
  const ch = BABYLON.MeshBuilder.CreateSphere('ch', { diameter: 2.0, segments: 8 }, scene);
  ch.scaling.y = 0.60;
  ch.position = new BABYLON.Vector3(0, -0.10, 0);
  ch.material = mat(1, .45, .06, 1, .55, .14, 0);
  
  const rc = BABYLON.MeshBuilder.CreateSphere('rc', { diameter: 2.2, segments: 8 }, scene);
  rc.scaling.y = 0.45;
  rc.position = new BABYLON.Vector3(0, 0.70, 0);
  rc.material = mat(.88, .38, .08, 1, .30, .10, 0);

  // Bandes magnétiques
  const stripeColors = [[.12, .20, .34], [.22, .30, .46]];
  for (let i = 1; i <= 5; i++) {
    for (let s of [-1, 1]) {
      const st = createBoxNoEdges(`st${s}${i}`, .50, 0.06, 5, s * (1.0 + i * .65), 1.20, 0);
      const sm = new BABYLON.StandardMaterial(`smm${s}${i}`, scene);
      sm.diffuseColor = new BABYLON.Color3(...stripeColors[i % 2]);
      sm.backFaceCulling = false;
      st.material = sm;
    }
  }

  // Montagne
  const mt = BABYLON.MeshBuilder.CreateCylinder('mt', { diameterTop: 0.04, diameterBottom: 2.5, height: 2.2, tessellation: 8 }, scene);
  mt.position = new BABYLON.Vector3(-5.5, 2.10, 0.3);
  mt.material = mat(.58, .52, .46, 1);
  
  const snow = BABYLON.MeshBuilder.CreateSphere('snow', { diameter: 0.70, segments: 6 }, scene);
  snow.scaling.y = 0.50;
  snow.position = new BABYLON.Vector3(-5.5, 3.20, 0.3);
  snow.material = mat(.94, .96, 1, 1, .08, .08, .08);

  // Subduction
  const trench = createBoxNoEdges('trench', 1.8, 0.50, 5, 5.5, -0.10, 0, mat(.06, .08, .16, 1));
  
  const sl1 = createBoxNoEdges('slab1', 4.5, 0.45, 5, 5.5, -1.80, 0, mat(.18, .20, .30, 0.90));
  sl1.rotation.z = -Math.PI * 0.20;
  slabMeshes.push(sl1);
  
  const sl2 = createBoxNoEdges('slab2', 3.0, 0.40, 5, 6.2, -2.80, 0, mat(.14, .16, .26, 0.78));
  sl2.rotation.z = -Math.PI * 0.28;
  slabMeshes.push(sl2);

  // Volcan
  const vc = BABYLON.MeshBuilder.CreateCylinder('vc', { diameterTop: 0.08, diameterBottom: 1.5, height: 2.0, tessellation: 7 }, scene);
  vc.position = new BABYLON.Vector3(3.8, 1.90, 0.3);
  vc.material = mat(.24, .20, .22, 1);
  
  const ld = BABYLON.MeshBuilder.CreateSphere('ld', { diameter: 0.35, segments: 5 }, scene);
  ld.position = new BABYLON.Vector3(3.8, 2.90, 0.3);
  ld.material = mat(1, .25, .03, 1, .60, .10, 0);

  // Point chaud
  hotspotMesh = BABYLON.MeshBuilder.CreateSphere('hs', { diameter: 0.70, segments: 7 }, scene);
  hotspotMesh.position = new BABYLON.Vector3(-3, 1.20, 0);
  hotspotMesh.material = mat(1, .45, .06, 1, .60, .18, 0);
  hotspotMesh.isVisible = false;

  // Flèches de convection
  const arrowColor = new BABYLON.Color3(0.98, 0.55, 0.10);
  
  function addArrow(points, name) {
    const l = BABYLON.MeshBuilder.CreateLines(name, {
      points: points.map(p => new BABYLON.Vector3(p[0], p[1], p[2]))
    }, scene);
    l.color = arrowColor;
    l.alpha = 0.55;
    convArrows.push(l);
  }
  
  addArrow([[-6.2, -2.0, 2.1], [-2.5, -2.3, 2.1], [-0.3, -0.8, 2.1], [-0.3, 0.4, 2.1]], 'cvL1');
  addArrow([[-0.3, 0.4, 2.1], [-0.3, 0.6, 2.1]], 'cvL2');
  addArrow([[-0.3, 0.6, 2.1], [-3.8, 0.4, 2.1], [-6.2, -0.6, 2.1], [-6.2, -2.0, 2.1]], 'cvL3');
  addArrow([[-6.2, -2.0, 2.1], [-5.9, -1.6, 2.1]], 'cvLa1');
  addArrow([[-6.2, -2.0, 2.1], [-6.5, -1.6, 2.1]], 'cvLa2');
  addArrow([[6.2, -2.0, -2.1], [2.5, -2.3, -2.1], [0.3, -0.8, -2.1], [0.3, 0.4, -2.1]], 'cvR1');
  addArrow([[0.3, 0.4, -2.1], [0.3, 0.6, -2.1]], 'cvR2');
  addArrow([[0.3, 0.6, -2.1], [3.8, 0.4, -2.1], [6.2, -0.6, -2.1], [6.2, -2.0, -2.1]], 'cvR3');
  addArrow([[6.2, -2.0, -2.1], [5.9, -1.6, -2.1]], 'cvRa1');
  addArrow([[6.2, -2.0, -2.1], [6.5, -1.6, -2.1]], 'cvRa2');

  // Murs en verre
  const glassMat = new BABYLON.StandardMaterial('glass', scene);
  glassMat.diffuseColor = new BABYLON.Color3(0.35, 0.55, 0.90);
  glassMat.emissiveColor = new BABYLON.Color3(0.05, 0.08, 0.15);
  glassMat.alpha = 0.10;
  glassMat.backFaceCulling = false;
  
  function addWall(name, w, h, pos, ry) {
    const p = BABYLON.MeshBuilder.CreatePlane(name, { width: w, height: h }, scene);
    p.position = pos;
    p.rotation.y = ry;
    p.material = glassMat;
  }
  
  addWall('wF', 14, 9.0, new BABYLON.Vector3(0, -0.5, 2.58), 0);
  addWall('wB', 14, 9.0, new BABYLON.Vector3(0, -0.5, -2.58), Math.PI);
  addWall('wL', 5, 9.0, new BABYLON.Vector3(-7, -0.5, 0), Math.PI * 0.5);
  addWall('wR', 5, 9.0, new BABYLON.Vector3(7, -0.5, 0), -Math.PI * 0.5);
  
  // Contours des murs
  const edgeColor = new BABYLON.Color3(0.28, 0.48, 0.80);
  const EX = 7, EYt = 3.5, EYb = -4.5, EZ = 2.58;
  const edges = [
    [[-EX, EYt, -EZ], [EX, EYt, -EZ]], [[EX, EYt, -EZ], [EX, EYt, EZ]], [[EX, EYt, EZ], [-EX, EYt, EZ]], [[-EX, EYt, EZ], [-EX, EYt, -EZ]],
    [[-EX, EYb, -EZ], [EX, EYb, -EZ]], [[EX, EYb, -EZ], [EX, EYb, EZ]], [[EX, EYb, EZ], [-EX, EYb, EZ]], [[-EX, EYb, EZ], [-EX, EYb, -EZ]],
    [[-EX, EYt, -EZ], [-EX, EYb, -EZ]], [[EX, EYt, -EZ], [EX, EYb, -EZ]], [[EX, EYt, EZ], [EX, EYb, EZ]], [[-EX, EYt, EZ], [-EX, EYb, EZ]]
  ];
  
  edges.forEach((e, i) => {
    const l = BABYLON.MeshBuilder.CreateLines(`edge${i}`, {
      points: [new BABYLON.Vector3(e[0][0], e[0][1], e[0][2]), new BABYLON.Vector3(e[1][0], e[1][1], e[1][2])]
    }, scene);
    l.color = edgeColor;
    l.alpha = 0.30;
  });
}

function setupLights() {
  const ambient = new BABYLON.HemisphericLight('amb', new BABYLON.Vector3(0, 1, 0), scene);
  ambient.intensity = 0.50;
  ambient.groundColor = new BABYLON.Color3(0.10, 0.05, 0);
  
  const sun = new BABYLON.DirectionalLight('sun', new BABYLON.Vector3(-1, -1.2, -0.5), scene);
  sun.intensity = 1.0;
  
  const mantleLight = new BABYLON.PointLight('mg', new BABYLON.Vector3(0, -1.2, 0), scene);
  mantleLight.diffuse = new BABYLON.Color3(1, 0.35, 0.05);
  mantleLight.intensity = 4.0;
  mantleLight.range = 18;
  
  const ridgeLight = new BABYLON.PointLight('rg', new BABYLON.Vector3(0, 0.5, 0), scene);
  ridgeLight.diffuse = new BABYLON.Color3(1, 0.60, 0.15);
  ridgeLight.intensity = 2.5;
  ridgeLight.range = 7;
  
  const volcanoLight = new BABYLON.PointLight('vg', new BABYLON.Vector3(4.5, 2, 0), scene);
  volcanoLight.diffuse = new BABYLON.Color3(1, 0.30, 0.04);
  
  const backLight = new BABYLON.PointLight('bk', new BABYLON.Vector3(0, 0, -6), scene);
  backLight.diffuse = new BABYLON.Color3(0.65, 0.55, 0.48);
  backLight.intensity = 1.6;
  backLight.range = 16;
  
  const topLight = new BABYLON.PointLight('top', new BABYLON.Vector3(0, 3, 0), scene);
  topLight.diffuse = new BABYLON.Color3(0.8, 0.7, 0.6);
  topLight.intensity = 0.8;
  topLight.range = 20;
}

function setupCamera(canvas) {
  camera = new BABYLON.ArcRotateCamera('cam', -Math.PI * 0.28, Math.PI * 0.30, 26, new BABYLON.Vector3(0, -0.5, 0), scene);
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 4;
  camera.upperRadiusLimit = 50;
  camera.lowerBetaLimit = 0.01;
  camera.upperBetaLimit = Math.PI - 0.01;
  camera.wheelDeltaPercentage = 0.01;
  camera.minZ = 0.1;
}