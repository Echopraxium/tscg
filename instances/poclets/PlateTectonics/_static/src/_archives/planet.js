// src/planet.js - Version avec highlight au survol (jaune) et sélection (vert)

let gridLinesList = [];
let selectedGridCell = null;
let gridSelectionMarker = null;
let cellMeshes = [];
let sampleMarkers = [];
let gridCreated = false;
let currentHoverCell = null;
let originalCellColors = new Map(); // Stocke les couleurs originales des cellules

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
  
  createClickableCells();
  createLatLongGrid();
  
  console.log("Planet Earth created successfully");
  
  return { earth: planetEarth, atmosphere: planetAtmosphere };
}

// =============================================================
// CRÉATION DES CELLULES CLIQUABLES AVEC HIGHLIGHT
// =============================================================

function createClickableCells() {
  console.log("createClickableCells called");
  
  cellMeshes.forEach(mesh => { if (mesh) mesh.dispose(); });
  cellMeshes = [];
  originalCellColors.clear();
  
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
  
  console.log(`Created ${cellCount} clickable cells`);
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
  
  // Récupérer la couleur géologique pour la cellule
  let geologyColor = new BABYLON.Color3(0.2, 0.3, 0.5); // Couleur par défaut
  if (typeof window.getGeologyData !== 'undefined') {
    const geoData = window.getGeologyData(lat, lon);
    switch(geoData.crustType) {
      case 'continental': geologyColor = new BABYLON.Color3(0.55, 0.45, 0.35); break;
      case 'ridge': geologyColor = new BABYLON.Color3(1.0, 0.35, 0.2); break;
      case 'subduction': geologyColor = new BABYLON.Color3(0.2, 0.4, 0.7); break;
      case 'hotspot': geologyColor = new BABYLON.Color3(1.0, 0.2, 0.1); break;
      case 'rift': geologyColor = new BABYLON.Color3(0.9, 0.5, 0.1); break;
      default: geologyColor = new BABYLON.Color3(0.1, 0.35, 0.55);
    }
  }
  
  // Stocker la couleur originale
  originalCellColors.set(mesh, geologyColor.clone());
  
  const mat = new BABYLON.StandardMaterial(`mat_cell_${lat}_${lon}`, scene);
  mat.diffuseColor = geologyColor;
  mat.alpha = 0.7;  // Semi-transparent pour voir la texture en dessous
  mat.backFaceCulling = false;
  mesh.material = mat;
  mesh.parent = planetGroup;
  mesh.isPickable = true;
  mesh.metadata = { lat: lat, lon: lon, type: 'grid_cell' };
  
  // ActionManager pour les interactions
  mesh.actionManager = new BABYLON.ActionManager(scene);
  
  // Survol - Highlight en jaune
  mesh.actionManager.registerAction(
    new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, () => {
      if (mesh === selectedGridCell?.mesh) return; // Ne pas modifier la cellule sélectionnée
      if (currentHoverCell) {
        // Restaurer la couleur précédente
        const prevColor = originalCellColors.get(currentHoverCell);
        if (prevColor && currentHoverCell.material) {
          currentHoverCell.material.diffuseColor = prevColor;
        }
      }
      currentHoverCell = mesh;
      // Highlight en jaune
      if (mesh.material) {
        mesh.material.diffuseColor = new BABYLON.Color3(1, 0.85, 0);
      }
      document.getElementById('cp-info').innerHTML = `📍 Survol: ${lat}°, ${lon}°`;
    })
  );
  
  // Sortie du survol - Restauration
  mesh.actionManager.registerAction(
    new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, () => {
      if (mesh === currentHoverCell) {
        if (mesh === selectedGridCell?.mesh) {
          // Si c'est la cellule sélectionnée, garder la couleur verte
          if (mesh.material) {
            mesh.material.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
          }
        } else {
          // Restaurer la couleur originale
          const origColor = originalCellColors.get(mesh);
          if (origColor && mesh.material) {
            mesh.material.diffuseColor = origColor;
          }
        }
        currentHoverCell = null;
      }
    })
  );
  
  // Clic - Sélection en vert
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
  const gridAlpha = 0.45;
  
  for (let lat = -82.5; lat <= 82.5; lat += step) {
    const phi = (90 - lat) * Math.PI / 180;
    const r = radius * Math.sin(phi);
    const y = radius * Math.cos(phi);
    const points = [];
    for (let lon = 0; lon <= 360; lon += 10) {
      const theta = lon * Math.PI / 180;
      points.push(new BABYLON.Vector3(r * Math.cos(theta), y, r * Math.sin(theta)));
    }
    const line = BABYLON.MeshBuilder.CreateLines(`lat_${lat}`, { points: points }, scene);
    line.color = gridColor;
    line.alpha = gridAlpha;
    line.parent = planetGroup;
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
    gridLinesList.push(line);
  }
  
  const equatorPoints = [];
  for (let lon = 0; lon <= 360; lon += 5) {
    const theta = lon * Math.PI / 180;
    equatorPoints.push(new BABYLON.Vector3(radius * Math.cos(theta), 0, radius * Math.sin(theta)));
  }
  const equatorLine = BABYLON.MeshBuilder.CreateLines("equator", { points: equatorPoints }, scene);
  equatorLine.color = new BABYLON.Color3(0.3, 0.9, 1.0);
  equatorLine.alpha = 0.7;
  equatorLine.parent = planetGroup;
  gridLinesList.push(equatorLine);
  
  console.log(`Grid created with ${gridLinesList.length} lines`);
}

function toggleGrid(visible) {
  gridLinesList.forEach(line => line.setEnabled(visible));
}

// =============================================================
// SÉLECTION D'UNE CELLULE (couleur VERTE)
// =============================================================

function selectGridCell(lat, lon, clickedMesh) {
  // Restaurer la couleur de l'ancienne cellule sélectionnée
  if (selectedGridCell) {
    const oldMesh = selectedGridCell.mesh;
    if (oldMesh && oldMesh.material) {
      const origColor = originalCellColors.get(oldMesh);
      if (origColor) {
        oldMesh.material.diffuseColor = origColor;
      }
    }
  }
  
  // Définir la nouvelle cellule sélectionnée
  selectedGridCell = { lat, lon, mesh: clickedMesh };
  
  // Colorer en VERT la cellule sélectionnée
  if (clickedMesh && clickedMesh.material) {
    clickedMesh.material.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
  }
  
  // Supprimer l'ancien marqueur sphérique
  if (gridSelectionMarker) {
    gridSelectionMarker.dispose();
    gridSelectionMarker = null;
  }
  
  // Créer un petit marqueur à la surface
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
  
  // Récupérer les données géologiques
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
  }
  
  const typeIcons = { oceanic: '💧', continental: '🏔️', ridge: '🌊', subduction: '⬇️', hotspot: '🌋', rift: '🔴', craton: '🗻' };
  
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
  
  if (typeof window.updateLayerCakeFromGeology !== 'undefined') {
    window.updateLayerCakeFromGeology(geologyData);
  }
  
  const sampleBtn = document.getElementById('btn-sample');
  if (sampleBtn) {
    sampleBtn.style.display = 'block';
    const newBtn = sampleBtn.cloneNode(true);
    sampleBtn.parentNode.replaceChild(newBtn, sampleBtn);
    newBtn.addEventListener('click', () => {
      const data = typeof window.getGeologyData !== 'undefined' ? window.getGeologyData(lat, lon) : geologyData;
      setStatus('info', `🔬 Core sample: ${data.crustType} crust, ${data.crustThickness}km thick`);
      console.log("Sample data:", data);
    });
  }
  
  setStatus('info', `✅ Cell selected: ${lat}°, ${lon}° - ${geologyData.crustType} crust`);
}

function clearGridSelection() {
  if (selectedGridCell) {
    const oldMesh = selectedGridCell.mesh;
    if (oldMesh && oldMesh.material) {
      const origColor = originalCellColors.get(oldMesh);
      if (origColor) {
        oldMesh.material.diffuseColor = origColor;
      }
    }
    selectedGridCell = null;
  }
  
  if (gridSelectionMarker) {
    gridSelectionMarker.dispose();
    gridSelectionMarker = null;
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

function testPicking() {
  console.log("=== TEST PICKING ===");
  console.log(`Number of clickable cells: ${cellMeshes.length}`);
  console.log("Hover: yellow highlight | Click: green selection");
}

// =============================================================
// EXPOSITION GLOBALE
// =============================================================

window.buildPlanetEarth = buildPlanetEarth;
window.createLatLongGrid = createLatLongGrid;
window.toggleGrid = toggleGrid;
window.selectGridCell = selectGridCell;
window.clearGridSelection = clearGridSelection;
window.addSampleMarker = addSampleMarker;
window.clearSampleMarkers = clearSampleMarkers;
window.testPicking = testPicking;