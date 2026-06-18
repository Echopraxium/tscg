// src/sceneBuilder.js - Construction de la scène Layer Cake
// Version avec double-face (DOUBLESIDE) pour voir les couches par le dessus

// Fonction pour créer un mesh avec double-face et wireframe
function createBoxWithEdgesTwoSided(nm, w, h, d, x, y, z, color, edgeColor = new BABYLON.Color3(0, 1, 1), alpha = 1.0) {
  const mat = new BABYLON.StandardMaterial(`mat_${nm}`, scene);
  mat.diffuseColor = color;
  mat.specularColor = new BABYLON.Color3(0.25, 0.25, 0.25);
  mat.specularPower = 40;
  mat.alpha = alpha;
  mat.backFaceCulling = false;
  mat.twoSidedLighting = true;
  
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { 
    width: w, height: h, depth: d, 
    sideOrientation: BABYLON.Mesh.DOUBLESIDE 
  }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  mesh.material = mat;
  
  mesh.enableEdgesRendering();
  mesh.edgesWidth = 2.0;
  mesh.edgesColor = edgeColor;
  
  return mesh;
}

// Version sans wireframe avec double-face
function createBoxNoEdgesTwoSided(nm, w, h, d, x, y, z, color, alpha = 1.0) {
  const mat = new BABYLON.StandardMaterial(`mat_${nm}`, scene);
  mat.diffuseColor = color;
  mat.specularColor = new BABYLON.Color3(0.2, 0.2, 0.2);
  mat.specularPower = 40;
  mat.alpha = alpha;
  mat.backFaceCulling = false;
  mat.twoSidedLighting = true;
  
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { 
    width: w, height: h, depth: d, 
    sideOrientation: BABYLON.Mesh.DOUBLESIDE 
  }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  mesh.material = mat;
  
  return mesh;
}

// Version simple pour compatibilité (avec double-face)
function mat(r, g, b, al, er, eg, eb) {
  const m = new BABYLON.StandardMaterial(`mat_${Date.now()}`, scene);
  m.diffuseColor = new BABYLON.Color3(r, g, b);
  if (al != null && al < 1) m.alpha = al;
  if (er != null) m.emissiveColor = new BABYLON.Color3(er, eg, eb);
  m.backFaceCulling = false;
  m.twoSidedLighting = true;
  return m;
}

function box(nm, w, h, d, x, y, z, m) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { 
    width: w, height: h, depth: d, 
    sideOrientation: BABYLON.Mesh.DOUBLESIDE 
  }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  return mesh;
}

function buildScene() {
  // Manteau inférieur - double-face
  const mantleColor = new BABYLON.Color3(0.68, 0.03, 0.01);
  const mantle = createBoxNoEdgesTwoSided('mantle', 14, 3.5, 5, 0, -2.8, 0, mantleColor, 1.0);
  
  // Lithosphère - double-face avec wireframe cyan
  const lithoColor = new BABYLON.Color3(0.55, 0.40, 0.25);
  const lithoBase = createBoxWithEdgesTwoSided('lithoBase', 14, 1.00, 5, 0, -0.40, 0, lithoColor, new BABYLON.Color3(0, 1, 1), 1.0);
  
  const GAP2 = 0.06;
  const PW = (7 - GAP2 * 2) / 3;
  const PD = (5 - GAP2 * 2) / 3;
  
  // Couleurs pour les croûtes continentales
  const continentColors = [
    new BABYLON.Color3(0.65, 0.52, 0.34), new BABYLON.Color3(0.60, 0.48, 0.30), new BABYLON.Color3(0.58, 0.46, 0.28),
    new BABYLON.Color3(0.62, 0.50, 0.32), new BABYLON.Color3(0.64, 0.51, 0.33), new BABYLON.Color3(0.56, 0.44, 0.27),
    new BABYLON.Color3(0.63, 0.50, 0.31), new BABYLON.Color3(0.61, 0.49, 0.30), new BABYLON.Color3(0.59, 0.47, 0.29)
  ];

  // Plaques continentales (gauche) - double-face avec wireframe cyan
  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const cx = -7 + GAP2 + PW * .5 + c2 * (PW + GAP2);
      const cz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      // Croûte continentale
      const contPlate = createBoxWithEdgesTwoSided(`cc_${idx}`, PW, 1.20, PD, cx, 0.60, cz, continentColors[idx], new BABYLON.Color3(0, 1, 1), 1.0);
      continentalPlates.push(contPlate);
      
      // Sol continental
      const soilColor = new BABYLON.Color3(
        continentColors[idx].r * 0.85,
        continentColors[idx].g * 0.85,
        continentColors[idx].b * 0.85
      );
      const soilPlate = createBoxWithEdgesTwoSided(`cs_${idx}`, PW, 0.15, PD, cx, 1.25, cz, soilColor, new BABYLON.Color3(0, 1, 1), 1.0);
      
      if (c2 < 2) {
        const faultColor = new BABYLON.Color3(0.25, 0.65, 0.15);
        const faultMesh = createBoxWithEdgesTwoSided(`fh_${idx}`, .05, 0.15, PD, cx + PW * .5 + GAP2 * .5, 1.30, cz, faultColor, new BABYLON.Color3(1, 0.5, 0), 1.0);
        faultMats.push(faultMesh.material);
      }
    }
  }
  
  // Couche continentale supérieure - double-face
  const topColor = new BABYLON.Color3(0.47, 0.40, 0.26);
  const contTop = createBoxWithEdgesTwoSided('contTop', 7, 0.12, 5, -3.5, 1.50, 0, topColor, new BABYLON.Color3(0, 1, 1), 1.0);

  // Couleurs pour les plaques océaniques
  const oceanColors = [
    new BABYLON.Color3(0.12, 0.19, 0.38), new BABYLON.Color3(0.14, 0.21, 0.40), new BABYLON.Color3(0.11, 0.18, 0.36),
    new BABYLON.Color3(0.13, 0.20, 0.39), new BABYLON.Color3(0.15, 0.22, 0.41), new BABYLON.Color3(0.10, 0.17, 0.35),
    new BABYLON.Color3(0.12, 0.19, 0.37), new BABYLON.Color3(0.13, 0.20, 0.38), new BABYLON.Color3(0.11, 0.18, 0.36)
  ];
  
  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const ox = GAP2 + PW * .5 + c2 * (PW + GAP2);
      const oz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      // Lithosphère océanique
      const lithoOceanColor = new BABYLON.Color3(0.20, 0.18, 0.30);
      const oceanLitho = createBoxWithEdgesTwoSided(`rlitho_${idx}`, PW, 0.80, PD, ox, -0.30, oz, lithoOceanColor, new BABYLON.Color3(0, 1, 1), 1.0);
      
      // Croûte océanique
      const oceanCrust = createBoxWithEdgesTwoSided(`rcrust_${idx}`, PW, 0.40, PD, ox, 0.30, oz, oceanColors[idx], new BABYLON.Color3(0, 1, 1), 1.0);
      
      // Océan - légèrement transparent
      const oceanColor = new BABYLON.Color3(0.04, 0.22, 0.68);
      const oceanWater = createBoxWithEdgesTwoSided(`rocean_${idx}`, PW, 0.60, PD, ox, 0.85, oz, oceanColor, new BABYLON.Color3(0, 1, 1), 0.85);
    }
  }

  // Dorsale médio-océanique
  const ch = BABYLON.MeshBuilder.CreateSphere('ch', { diameter: 2.0, segments: 8 }, scene);
  ch.scaling.y = 0.60;
  ch.position = new BABYLON.Vector3(0, -0.10, 0);
  const chMat = new BABYLON.StandardMaterial('chMat', scene);
  chMat.diffuseColor = new BABYLON.Color3(1, 0.45, 0.06);
  chMat.emissiveColor = new BABYLON.Color3(0.55, 0.14, 0);
  chMat.backFaceCulling = false;
  chMat.twoSidedLighting = true;
  ch.material = chMat;
  
  const rc = BABYLON.MeshBuilder.CreateSphere('rc', { diameter: 2.2, segments: 8 }, scene);
  rc.scaling.y = 0.45;
  rc.position = new BABYLON.Vector3(0, 0.70, 0);
  const rcMat = new BABYLON.StandardMaterial('rcMat', scene);
  rcMat.diffuseColor = new BABYLON.Color3(0.88, 0.38, 0.08);
  rcMat.emissiveColor = new BABYLON.Color3(0.30, 0.10, 0);
  rcMat.backFaceCulling = false;
  rcMat.twoSidedLighting = true;
  rc.material = rcMat;

  // Bandes magnétiques
  const stripeColors = [
    new BABYLON.Color3(0.12, 0.20, 0.34),
    new BABYLON.Color3(0.22, 0.30, 0.46)
  ];
  for (let i = 1; i <= 5; i++) {
    for (let s of [-1, 1]) {
      const st = createBoxNoEdgesTwoSided(`st${s}${i}`, .50, 0.06, 5, s * (1.0 + i * .65), 1.20, 0, stripeColors[i % 2], 1.0);
    }
  }

  // Montagne
  const mt = BABYLON.MeshBuilder.CreateCylinder('mt', { 
    diameterTop: 0.04, diameterBottom: 2.5, height: 2.2, tessellation: 8 
  }, scene);
  mt.position = new BABYLON.Vector3(-5.5, 2.10, 0.3);
  const mtMat = new BABYLON.StandardMaterial('mtMat', scene);
  mtMat.diffuseColor = new BABYLON.Color3(0.58, 0.52, 0.46);
  mtMat.backFaceCulling = false;
  mtMat.twoSidedLighting = true;
  mt.material = mtMat;
  
  const snow = BABYLON.MeshBuilder.CreateSphere('snow', { diameter: 0.70, segments: 6 }, scene);
  snow.scaling.y = 0.50;
  snow.position = new BABYLON.Vector3(-5.5, 3.20, 0.3);
  const snowMat = new BABYLON.StandardMaterial('snowMat', scene);
  snowMat.diffuseColor = new BABYLON.Color3(0.94, 0.96, 1.0);
  snowMat.emissiveColor = new BABYLON.Color3(0.08, 0.08, 0.08);
  snowMat.backFaceCulling = false;
  snowMat.twoSidedLighting = true;
  snow.material = snowMat;

  // Zone de subduction
  const trench = createBoxNoEdgesTwoSided('trench', 1.8, 0.50, 5, 5.5, -0.10, 0, new BABYLON.Color3(0.06, 0.08, 0.16), 1.0);
  
  const sl1 = createBoxNoEdgesTwoSided('slab1', 4.5, 0.45, 5, 5.5, -1.80, 0, new BABYLON.Color3(0.18, 0.20, 0.30), 0.90);
  sl1.rotation.z = -Math.PI * 0.20;
  slabMeshes.push(sl1);
  
  const sl2 = createBoxNoEdgesTwoSided('slab2', 3.0, 0.40, 5, 6.2, -2.80, 0, new BABYLON.Color3(0.14, 0.16, 0.26), 0.78);
  sl2.rotation.z = -Math.PI * 0.28;
  slabMeshes.push(sl2);

  // Volcan
  const vc = BABYLON.MeshBuilder.CreateCylinder('vc', { 
    diameterTop: 0.08, diameterBottom: 1.5, height: 2.0, tessellation: 7 
  }, scene);
  vc.position = new BABYLON.Vector3(3.8, 1.90, 0.3);
  const vcMat = new BABYLON.StandardMaterial('vcMat', scene);
  vcMat.diffuseColor = new BABYLON.Color3(0.24, 0.20, 0.22);
  vcMat.backFaceCulling = false;
  vcMat.twoSidedLighting = true;
  vc.material = vcMat;
  
  const ld = BABYLON.MeshBuilder.CreateSphere('ld', { diameter: 0.35, segments: 5 }, scene);
  ld.position = new BABYLON.Vector3(3.8, 2.90, 0.3);
  const ldMat = new BABYLON.StandardMaterial('ldMat', scene);
  ldMat.diffuseColor = new BABYLON.Color3(1.0, 0.25, 0.03);
  ldMat.emissiveColor = new BABYLON.Color3(0.60, 0.10, 0);
  ldMat.backFaceCulling = false;
  ldMat.twoSidedLighting = true;
  ld.material = ldMat;

  // Point chaud (hotspot)
  hotspotMesh = BABYLON.MeshBuilder.CreateSphere('hs', { diameter: 0.70, segments: 7 }, scene);
  hotspotMesh.position = new BABYLON.Vector3(-3, 1.20, 0);
  const hsMat = new BABYLON.StandardMaterial('hsMat', scene);
  hsMat.diffuseColor = new BABYLON.Color3(1.0, 0.45, 0.06);
  hsMat.emissiveColor = new BABYLON.Color3(0.60, 0.18, 0);
  hsMat.backFaceCulling = false;
  hsMat.twoSidedLighting = true;
  hotspotMesh.material = hsMat;
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
  glassMat.twoSidedLighting = true;
  
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
  
  // Contours des murs (arêtes)
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
  // Lumière ambiante
  const ambient = new BABYLON.HemisphericLight('amb', new BABYLON.Vector3(0, 1, 0), scene);
  ambient.intensity = 0.50;
  ambient.groundColor = new BABYLON.Color3(0.10, 0.05, 0);
  
  // Lumière directionnelle (soleil)
  const sun = new BABYLON.DirectionalLight('sun', new BABYLON.Vector3(-1, -1.2, -0.5), scene);
  sun.intensity = 1.0;
  
  // Lumières ponctuelles pour les effets
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
  
  // Lumière arrière
  const backLight = new BABYLON.PointLight('bk', new BABYLON.Vector3(0, 0, -6), scene);
  backLight.diffuse = new BABYLON.Color3(0.65, 0.55, 0.48);
  backLight.intensity = 1.6;
  backLight.range = 16;
  
  // Lumière supplémentaire par dessus
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