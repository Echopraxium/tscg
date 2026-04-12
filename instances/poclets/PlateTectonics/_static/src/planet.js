// src/planet.js - Mode planète avec cellules cliquables, highlight, sélection et mise à jour du Layer Cake

let gridLinesList = [];
let selectedGridCell = null;
let gridSelectionMarker = null;
let cellMeshes = [];
let sampleMarkers = [];
let gridCreated = false;
let currentHoverCell = null;

// =============================================================
// CONSTRUCTION DE LA PLANÈTE
// =============================================================

function buildPlanetEarth() {
  console.log("buildPlanetEarth called");
  
  const earthMat = new BABYLON.StandardMaterial("earthMat", scene);
  
  const textureUrl = "https://threejs.org/examples/textures/planets/earth_atmos_2048.jpg";
  const earthTexture = new BABYLON.Texture(textureUrl, scene);
  earthMat.diffuseTexture = earthTexture;
  earthMat.ambientColor = new BABYLON.Color3(0.6, 0.6, 0.6);
  earthMat.specularColor = new BABYLON.Color3(0.2, 0.2, 0.2);
  earthMat.emissiveColor = new BABYLON.Color3(0.15, 0.15, 0.15);
  
  planetEarth = BABYLON.MeshBuilder.CreateSphere("earth", { diameter: 12, segments: 256 }, scene);
  planetEarth.material = earthMat;
  planetEarth.position = new BABYLON.Vector3(0, 0, 0);
  planetEarth.rotation.x = Math.PI;
  planetEarth.isPickable = false;
  
  const atmosMat = new BABYLON.StandardMaterial("atmos", scene);
  atmosMat.diffuseColor = new BABYLON.Color3(0.4, 0.6, 0.9);
  atmosMat.alpha = 0.08;
  atmosMat.backFaceCulling = false;
  planetAtmosphere = BABYLON.MeshBuilder.CreateSphere("atmosphere", { diameter: 12.2, segments: 128 }, scene);
  planetAtmosphere.material = atmosMat;
  planetAtmosphere.rotation.x = Math.PI;
  planetAtmosphere.isPickable = false;
  
  if (planetGroup) {
    planetEarth.parent = planetGroup;
    planetAtmosphere.parent = planetGroup;
  }
  
  createClickableCells();
  
  setTimeout(() => {
    createLatLongGrid();
  }, 100);
  
  console.log("Planet Earth created successfully");
  
  return { earth: planetEarth, atmosphere: planetAtmosphere };
}

// =============================================================
// CRÉATION DES CELLULES CLIQUABLES
// =============================================================

function createClickableCells() {
  console.log("createClickableCells called");
  
  cellMeshes.forEach(mesh => { if (mesh) mesh.dispose(); });
  cellMeshes = [];
  
  const radius = 6.05;
  const latStep = 7.5;
  const lonStep = 7.5;
  
  let cellCount = 0;
  
  for (let lat = -90; lat < 90; lat += latStep) {
    for (let lon = -180; lon < 180; lon += lonStep) {
      createCellMesh(lat, lon, radius);
      cellCount++;
    }
  }
  
  console.log(`Created ${cellCount} clickable transparent cells`);
}

function createCellMesh(lat, lon, radius) {
  const latStep = 7.5;
  const lonStep = 7.5;
  const latStart = lat;
  const latEnd = lat + latStep;
  const lonStart = lon;
  const lonEnd = lon + lonStep;
  
  const positions = [];
  const indices = [];
  
  const subLat = 4;
  const subLon = 4;
  
  for (let i = 0; i <= subLat; i++) {
    const tLat = i / subLat;
    const currentLat = latStart + tLat * latStep;
    const phi = (90 - currentLat) * Math.PI / 180;
    const sinPhi = Math.sin(phi);
    const cosPhi = Math.cos(phi);
    
    for (let j = 0; j <= subLon; j++) {
      const tLon = j / subLon;
      let currentLon = lonStart + tLon * lonStep;
      if (currentLon > 180) currentLon -= 360;
      const theta = currentLon * Math.PI / 180;
      
      const x = radius * sinPhi * Math.cos(theta);
      const y = radius * cosPhi;
      const z = radius * sinPhi * Math.sin(theta);
      
      positions.push(x, y, z);
    }
  }
  
  for (let i = 0; i < subLat; i++) {
    for (let j = 0; j < subLon; j++) {
      const idx = i * (subLon + 1) + j;
      const nextIdx = (i + 1) * (subLon + 1) + j;
      indices.push(idx, idx + 1, nextIdx);
      indices.push(nextIdx, idx + 1, nextIdx + 1);
    }
  }
  
  const vertexData = new BABYLON.VertexData();
  vertexData.positions = positions;
  vertexData.indices = indices;
  BABYLON.VertexData.ComputeNormals(positions, indices, vertexData.normals = []);
  
  const mesh = new BABYLON.Mesh(`cell_${lat}_${lon}`, scene);
  vertexData.applyToMesh(mesh);
  
  const mat = new BABYLON.StandardMaterial(`mat_cell_${lat}_${lon}`, scene);
  mat.alpha = 0;
  mat.backFaceCulling = false;
  mesh.material = mat;
  mesh.parent = planetGroup;
  mesh.isPickable = true;
  mesh.metadata = { lat: lat, lon: lon, type: 'grid_cell' };
  
  mesh.actionManager = new BABYLON.ActionManager(scene);
  
  mesh.actionManager.registerAction(
    new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, () => {
      if (mesh === selectedGridCell?.mesh) return;
      if (currentHoverCell && currentHoverCell !== mesh) {
        if (currentHoverCell.material) {
          currentHoverCell.material.alpha = 0;
        }
      }
      currentHoverCell = mesh;
      if (mesh.material) {
        mesh.material.alpha = 0.4;
        mesh.material.diffuseColor = new BABYLON.Color3(1, 0.85, 0);
      }
    })
  );
  
  mesh.actionManager.registerAction(
    new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, () => {
      if (mesh === currentHoverCell) {
        if (mesh === selectedGridCell?.mesh) {
          if (mesh.material) {
            mesh.material.alpha = 0.5;
            mesh.material.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
          }
        } else {
          if (mesh.material) {
            mesh.material.alpha = 0;
          }
        }
        currentHoverCell = null;
      }
    })
  );
  
  mesh.actionManager.registerAction(
    new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPickTrigger, () => {
      console.log(`Cell clicked: lat=${lat}, lon=${lon}`);
      selectGridCell(lat, lon, mesh);
    })
  );
  
  cellMeshes.push(mesh);
}

// =============================================================
// GRILLE MÉRIDIENS/PARALLÈLES
// =============================================================

function createLatLongGrid(radius = 6.08) {
  console.log("createLatLongGrid called");
  
  if (!planetGroup) {
    setTimeout(() => createLatLongGrid(radius), 100);
    return;
  }
  
  if (gridLinesList.length > 0) {
    gridLinesList.forEach(line => { if (line) line.dispose(); });
    gridLinesList = [];
  }

  const step = 7.5;
  const gridColor = new BABYLON.Color3(0.4, 0.7, 0.9);
  const gridAlpha = 0.6;
  
  for (let lat = -82.5; lat <= 82.5; lat += step) {
    const phi = (90 - lat) * Math.PI / 180;
    const r = radius * Math.sin(phi);
    const y = radius * Math.cos(phi);
    const points = [];
    for (let lon = 0; lon <= 360; lon += 5) {
      const theta = lon * Math.PI / 180;
      points.push(new BABYLON.Vector3(r * Math.cos(theta), y, r * Math.sin(theta)));
    }
    const line = BABYLON.MeshBuilder.CreateLines(`lat_${lat}`, { points: points }, scene);
    line.color = gridColor;
    line.alpha = gridAlpha;
    line.parent = planetGroup;
    line.isPickable = false;
    gridLinesList.push(line);
  }
  
  for (let lon = -180; lon < 180; lon += step) {
    const points = [];
    for (let lat = -87.5; lat <= 87.5; lat += 2.5) {
      const phi = (90 - lat) * Math.PI / 180;
      const theta = lon * Math.PI / 180;
      points.push(new BABYLON.Vector3(radius * Math.sin(phi) * Math.cos(theta), radius * Math.cos(phi), radius * Math.sin(phi) * Math.sin(theta)));
    }
    const line = BABYLON.MeshBuilder.CreateLines(`lon_${lon}`, { points: points }, scene);
    line.color = gridColor;
    line.alpha = gridAlpha;
    line.parent = planetGroup;
    line.isPickable = false;
    gridLinesList.push(line);
  }
  
  const equatorPoints = [];
  for (let lon = 0; lon <= 360; lon += 3) {
    const theta = lon * Math.PI / 180;
    equatorPoints.push(new BABYLON.Vector3(radius * Math.cos(theta), 0, radius * Math.sin(theta)));
  }
  const equatorLine = BABYLON.MeshBuilder.CreateLines("equator", { points: equatorPoints }, scene);
  equatorLine.color = new BABYLON.Color3(0.3, 0.9, 1.0);
  equatorLine.alpha = 0.9;
  equatorLine.parent = planetGroup;
  equatorLine.isPickable = false;
  gridLinesList.push(equatorLine);
  
  console.log(`Grid created with ${gridLinesList.length} lines`);
}

function toggleGrid(visible) {
  console.log(`toggleGrid called with visible=${visible}`);
  gridLinesList.forEach(line => {
    if (line) line.setEnabled(visible);
  });
}

// =============================================================
// SÉLECTION D'UNE CELLULE
// =============================================================

function selectGridCell(lat, lon, clickedMesh) {
  console.log(`=== selectGridCell called: lat=${lat}, lon=${lon}`);
  
  if (selectedGridCell) {
    const oldMesh = selectedGridCell.mesh;
    if (oldMesh && oldMesh.material) {
      oldMesh.material.alpha = 0;
    }
  }
  
  selectedGridCell = { lat, lon, mesh: clickedMesh };
  
  if (clickedMesh && clickedMesh.material) {
    clickedMesh.material.alpha = 0.5;
    clickedMesh.material.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
  }
  
  if (gridSelectionMarker) {
    gridSelectionMarker.dispose();
    gridSelectionMarker = null;
  }
  
  const phi = (90 - lat) * Math.PI / 180;
  const theta = lon * Math.PI / 180;
  const r = 6.08;
  const x = r * Math.sin(phi) * Math.cos(theta);
  const y = r * Math.cos(phi);
  const z = r * Math.sin(phi) * Math.sin(theta);
  
  const markerMat = new BABYLON.StandardMaterial("gridSelectMat", scene);
  markerMat.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
  markerMat.emissiveColor = new BABYLON.Color3(0.1, 0.4, 0.1);
  markerMat.backFaceCulling = false;
  
  gridSelectionMarker = BABYLON.MeshBuilder.CreateSphere("gridSelect", { diameter: 0.35 }, scene);
  gridSelectionMarker.position = new BABYLON.Vector3(x, y, z);
  gridSelectionMarker.material = markerMat;
  gridSelectionMarker.parent = planetGroup;
  
  let geologyData = {
    crustType: 'oceanic',
    crustThickness: 7,
    mantleTemperature: 1300,
    activity: 'stable',
    description: 'Deep ocean basin',
    isLand: false,
    landName: null,
    layerCakeType: 'oceanic'
  };
  
  if (typeof window.getGeologyData !== 'undefined') {
    geologyData = window.getGeologyData(lat, lon);
    console.log("Geology data:", geologyData);
  }
  
  // TEST VISIBLE : Changer la couleur du fond de la scène
  if (geologyData.crustType === 'continental') {
    scene.clearColor = new BABYLON.Color4(0.2, 0.1, 0.05, 1);
    setStatus('warn', '🌍 CONTINENTAL crust selected');
  } else {
    scene.clearColor = new BABYLON.Color4(0.02, 0.03, 0.06, 1);
    setStatus('warn', '💧 OCEANIC crust selected');
  }
  
  const typeIcons = { 
    oceanic: '💧', continental: '🏔️', ridge: '🌊', 
    subduction: '⬇️', hotspot: '🌋', rift: '🔴', craton: '🗻' 
  };
  
  document.getElementById('cp-info').innerHTML = `
    ${geologyData.isLand ? '🏝️' : '💧'} <strong style="color:#4aff4a">✓ SELECTED</strong><br>
    📍 ${lat}°, ${lon}°<br>
    ${typeIcons[geologyData.crustType] || '🌍'} Type: ${geologyData.crustType}<br>
    📏 Crust: ${geologyData.crustThickness} km<br>
    🔥 Mantle: ${geologyData.mantleTemperature}°C<br>
    ${geologyData.activity === 'active' ? '🌋 Active' : '✓ Stable'}
  `;
  document.getElementById('cell-panel').classList.remove('hide');
  document.getElementById('cp-propagation').innerHTML = `Click "Sample" to extract core sample`;
  
  if (typeof updateStatusText !== 'undefined') {
    updateStatusText();
  }
  
  setStatus('info', `✅ Cell selected: ${lat}°, ${lon}° - ${geologyData.crustType} crust`);
  
  // 🔴 METTRE À JOUR LE LAYER CAKE
  if (typeof window.updateLayerCakeFromGeology !== 'undefined') {
    window.updateLayerCakeFromGeology(geologyData);
    console.log("Layer Cake update called");
  } else {
    console.warn("updateLayerCakeFromGeology not defined");
  }
  
  const sampleBtn = document.getElementById('btn-sample');
  if (sampleBtn) {
    sampleBtn.style.display = 'block';
    const newBtn = sampleBtn.cloneNode(true);
    sampleBtn.parentNode.replaceChild(newBtn, sampleBtn);
    newBtn.addEventListener('click', () => {
      const data = typeof window.getGeologyData !== 'undefined' ? window.getGeologyData(lat, lon) : geologyData;
      setStatus('info', `🔬 Core sample: ${data.crustType} crust, ${data.crustThickness}km thick, ${data.mantleTemperature}°C mantle`);
      console.log("Sample data:", data);
    });
  }
}

function clearGridSelection() {
  if (selectedGridCell) {
    const oldMesh = selectedGridCell.mesh;
    if (oldMesh && oldMesh.material) {
      oldMesh.material.alpha = 0;
    }
    selectedGridCell = null;
  }
  
  if (gridSelectionMarker) {
    gridSelectionMarker.dispose();
    gridSelectionMarker = null;
  }
  
  if (typeof updateStatusText !== 'undefined') {
    updateStatusText();
  }
}

function addSampleMarker(lat, lon) {
  if (!planetEarth) return null;
  
  const phi = (90 - lat) * Math.PI / 180;
  const theta = lon * Math.PI / 180;
  const radius = 6;
  const x = radius * Math.sin(phi) * Math.cos(theta);
  const y = radius * Math.cos(phi);
  const z = radius * Math.sin(phi) * Math.sin(theta);
  
  const markerMat = new BABYLON.StandardMaterial("markerMat", scene);
  markerMat.diffuseColor = new BABYLON.Color3(1, 0.65, 0.2);
  markerMat.emissiveColor = new BABYLON.Color3(0.5, 0.3, 0);
  markerMat.backFaceCulling = false;
  
  const marker = BABYLON.MeshBuilder.CreateSphere("sampleMarker", { diameter: 0.25 }, scene);
  marker.position = new BABYLON.Vector3(x, y, z);
  marker.material = markerMat;
  marker.parent = planetGroup;
  sampleMarkers.push(marker);
  
  let scale = 1;
  const interval = setInterval(() => {
    if (marker && marker.scaling) {
      scale = scale === 1 ? 1.5 : 1;
      marker.scaling = new BABYLON.Vector3(scale, scale, scale);
    } else {
      clearInterval(interval);
    }
  }, 500);
  
  setTimeout(() => {
    if (marker) {
      marker.dispose();
      clearInterval(interval);
    }
  }, 5000);
  
  return marker;
}

function clearSampleMarkers() {
  for (let m of sampleMarkers) {
    if (m) m.dispose();
  }
  sampleMarkers = [];
}

function getSelectedGridCell() {
  return selectedGridCell;
}

function testPicking() {
  console.log("=== TEST PICKING ===");
  console.log(`Number of clickable cells: ${cellMeshes.length}`);
  console.log("Selected cell:", selectedGridCell);
}

window.buildPlanetEarth = buildPlanetEarth;
window.createLatLongGrid = createLatLongGrid;
window.toggleGrid = toggleGrid;
window.selectGridCell = selectGridCell;
window.clearGridSelection = clearGridSelection;
window.addSampleMarker = addSampleMarker;
window.clearSampleMarkers = clearSampleMarkers;
window.testPicking = testPicking;
window.getSelectedGridCell = getSelectedGridCell;