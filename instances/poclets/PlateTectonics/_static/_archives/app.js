'use strict';

const SIM = {
  running: true, t: 0, convection: .5, slabDensity: .6, asymmetry: 0, stress: 0,
  quakeActive: false, quakeTimer: 0, quakeCooldown: 0,
  wilsonActive: false, wilsonT: 0, wilsonPhase: -1,
  plumeActive: false, plumeTimer: 0, showLegend: true,
  hovCell: null, selCell: null,
  vol: { x: 0, y: 0, z: 0 }, trans: { x: 0, y: 0, z: 0 }, rot: { alpha: 0, phi: 0, omega: 0 },
  realtimeMode: true, propagationStrength: 0.8, propagationRadius: 2.5, viewMode: 'layer'
};

let engine, scene, camera;
let psConv, psRidge, psVol, psPlume, psQuake;
let slabMeshes = [], convArrows = [], faultMats = [];
let hotspotMesh = null, quakeFlash = null;
let continentalPlates = [], oceanicPlates = [], buildings = [], magmaSpots = [], planetEarth = null;
let cells = [], origCellPositions = [];
let quakeDirection = { x: 0, z: 0 };

let currentVolAxis = 'x', currentTransAxis = 'x', currentRotAxis = 'alpha';

// ═══════════════════════════════════════════════════════════════
//  MANTLE GRID with Ray Picking
// ═══════════════════════════════════════════════════════════════
const MCOLS = 8, MROWS = 3, MZDEPTHS = 4;
const TOTAL_W = 13.6, TOTAL_H = 1.45, TOTAL_D = 4.6;
const CW = TOTAL_W / MCOLS, CH = TOTAL_H / MROWS, CZ_full = TOTAL_D / MZDEPTHS;
const GAP = 0.05;
const CW_g = CW - GAP, CH_g = CH - GAP, CD_g = CZ_full - GAP;

const CELL_COLORS = {
  normal: { r: .78, g: .14, b: .02, em_r: .12, em_g: .015, em_b: 0, al: .68 },
  hover: { r: .95, g: .55, b: .15, em_r: .35, em_g: .12, em_b: 0, al: .88 },
  select: { r: 1.0, g: .80, b: .20, em_r: .45, em_g: .25, em_b: 0, al: 1.0 },
  deformed: { r: 1.0, g: .55, b: .18, em_r: .55, em_g: .18, em_b: 0, al: .92 },
  propagated: { r: .85, g: .35, b: .10, em_r: .25, em_g: .08, em_b: 0, al: .78 }
};
const WIRE_COLORS = {
  normal: { c: new BABYLON.Color3(.50, .55, .65), al: .55 },
  hover: { c: new BABYLON.Color3(.95, .75, .30), al: .90 },
  select: { c: new BABYLON.Color3(1.0, 1.0, 1.0), al: 1.0 },
  deformed: { c: new BABYLON.Color3(1.0, .70, .25), al: .85 },
  propagated: { c: new BABYLON.Color3(.85, .55, .20), al: .70 }
};

function buildMantleGrid() {
  cells = [];
  origCellPositions = [];
  const startX = -6.8 + CW / 2;
  const startY = -2.0 + CH / 2;
  const startZ = -TOTAL_D / 2 + CZ_full / 2;

  for (let row = 0; row < MROWS; row++) {
    for (let col = 0; col < MCOLS; col++) {
      for (let dep = 0; dep < MZDEPTHS; dep++) {
        const cx = startX + col * CW;
        const cy = startY + row * CH;
        const cz = startZ + dep * CZ_full;
        const heatT = 1 - ((MROWS - 1 - row) / (MROWS - 1)) * .25;

        const cellMat = new BABYLON.StandardMaterial(`cm_${row}_${col}_${dep}`, scene);
        cellMat.diffuseColor = new BABYLON.Color3(.78 * heatT, .14, .02);
        cellMat.emissiveColor = new BABYLON.Color3(.14 * heatT, .018, 0);
        cellMat.alpha = CELL_COLORS.normal.al;
        cellMat.separateCullingPass = true;
        cellMat.backFaceCulling = false;

        const mesh = BABYLON.MeshBuilder.CreateBox(`cell_${row}_${col}_${dep}`,
          { width: CW_g, height: CH_g, depth: CD_g }, scene);
        mesh.position = new BABYLON.Vector3(cx, cy, cz);
        mesh.material = cellMat;
        mesh.renderingGroupId = 1;
        mesh.isPickable = true;

        const wires = boxWireframe(`cw_${row}_${col}_${dep}`, cx, cy, cz, CW_g, CH_g, CD_g,
          new BABYLON.Color3(.50, .55, .65), .55);
        wires.forEach(w => { w.renderingGroupId = 2; w.isPickable = false; });

        const cell = {
          row, col, dep, cx, cy, cz, mesh, mat: cellMat, wires, state: 'normal', heatT,
          origPos: { x: cx, y: cy, z: cz },
          origRot: { alpha: 0, phi: 0, omega: 0 },
          origScale: { x: 1, y: 1, z: 1 },
          volume: { x: 0, y: 0, z: 0 }, trans: { x: 0, y: 0, z: 0 }, rot: { alpha: 0, phi: 0, omega: 0 }
        };

        origCellPositions.push({ x: cx, y: cy, z: cz });
        cells.push(cell);
      }
    }
  }

  // Ray picking
  scene.onPointerObservable.add((evt) => {
    if (evt.type === BABYLON.PointerEventTypes.POINTERMOVE) {
      const pickInfo = scene.pick(scene.pointerX, scene.pointerY, (m) => {
        return m.isPickable && m.name && m.name.startsWith('cell_');
      });
      if (pickInfo && pickInfo.hit && pickInfo.pickedMesh) {
        const pickedCell = cells.find(c => c.mesh === pickInfo.pickedMesh);
        if (pickedCell && pickedCell !== SIM.selCell) {
          hoverCell(pickedCell);
        } else if (!pickedCell && SIM.hovCell && SIM.hovCell !== SIM.selCell) {
          applyCellState(SIM.hovCell, 'normal');
          SIM.hovCell = null;
        }
      } else if (SIM.hovCell && SIM.hovCell !== SIM.selCell) {
        applyCellState(SIM.hovCell, 'normal');
        SIM.hovCell = null;
      }
    }
    else if (evt.type === BABYLON.PointerEventTypes.POINTERPICK) {
      const pickInfo = scene.pick(scene.pointerX, scene.pointerY, (m) => {
        return m.isPickable && m.name && m.name.startsWith('cell_');
      });
      if (pickInfo && pickInfo.hit && pickInfo.pickedMesh) {
        const pickedCell = cells.find(c => c.mesh === pickInfo.pickedMesh);
        if (pickedCell) clickCell(pickedCell);
      } else {
        deselectCell();
      }
    }
  });
}

function boxWireframe(nm, x, y, z, w, h, d, col, alpha) {
  const e = .005;
  const x1 = x - w / 2 - e, x2 = x + w / 2 + e;
  const y1 = y - h / 2 - e, y2 = y + h / 2 + e;
  const z1 = z - d / 2 - e, z2 = z + d / 2 + e;
  const edges = [
    [[x1, y1, z1], [x2, y1, z1]], [[x2, y1, z1], [x2, y1, z2]], [[x2, y1, z2], [x1, y1, z2]], [[x1, y1, z2], [x1, y1, z1]],
    [[x1, y2, z1], [x2, y2, z1]], [[x2, y2, z1], [x2, y2, z2]], [[x2, y2, z2], [x1, y2, z2]], [[x1, y2, z2], [x1, y2, z1]],
    [[x1, y1, z1], [x1, y2, z1]], [[x2, y1, z1], [x2, y2, z1]], [[x2, y1, z2], [x2, y2, z2]], [[x1, y1, z2], [x1, y2, z2]]
  ];
  return edges.map((e2, i) => {
    const l = BABYLON.MeshBuilder.CreateLines(`${nm}_w${i}`,
      { points: [new BABYLON.Vector3(...e2[0]), new BABYLON.Vector3(...e2[1])] }, scene);
    l.color = col;
    l.alpha = alpha;
    return l;
  });
}

function applyCellState(cell, state) {
  if (!cell) return;
  cell.state = state;
  const col = CELL_COLORS[state] || CELL_COLORS.normal;
  const wc = WIRE_COLORS[state] || WIRE_COLORS.normal;
  if (col) {
    cell.mat.diffuseColor = new BABYLON.Color3(col.r * cell.heatT, col.g, col.b);
    cell.mat.emissiveColor = new BABYLON.Color3(col.em_r * cell.heatT, col.em_g, col.em_b);
    cell.mat.alpha = col.al;
  }
  if (wc) cell.wires.forEach(w => { w.color = wc.c; w.alpha = wc.al; });
}

function hoverCell(cell) {
  if (cell === SIM.selCell) return;
  if (SIM.hovCell && SIM.hovCell !== cell && SIM.hovCell !== SIM.selCell)
    applyCellState(SIM.hovCell, 'normal');
  SIM.hovCell = cell;
  applyCellState(cell, 'hover');
}

function clickCell(cell) {
  if (SIM.selCell === cell) { deselectCell(); return; }
  if (SIM.selCell) {
    applyCellState(SIM.selCell, SIM.selCell.volume.x !== 0 || SIM.selCell.volume.y !== 0 || SIM.selCell.volume.z !== 0 ? 'deformed' : 'normal');
  }
  SIM.selCell = cell;
  applyCellState(cell, 'select');
  SIM.vol = { ...cell.volume };
  SIM.trans = { ...cell.trans };
  SIM.rot = { ...cell.rot };
  updateAllDisplays();
  showCellInfo(cell);
}

function deselectCell() {
  if (SIM.selCell) {
    applyCellState(SIM.selCell, SIM.selCell.volume.x !== 0 || SIM.selCell.volume.y !== 0 || SIM.selCell.volume.z !== 0 ? 'deformed' : 'normal');
    SIM.selCell = null;
  }
  document.getElementById('cell-panel').classList.add('hide');
}

function showCellInfo(cell) {
  document.getElementById('cp-info').innerHTML = `Row ${cell.row + 1} · Col ${cell.col + 1} · Slice: ${cell.dep + 1}/4`;
  document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength * 100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`;
  document.getElementById('cell-panel').classList.remove('hide');
}

function updateAllDisplays() {
  document.getElementById('vol-values').textContent = `${SIM.vol.x.toFixed(1)},${SIM.vol.y.toFixed(1)},${SIM.vol.z.toFixed(1)}`;
  document.getElementById('trans-values').textContent = `${SIM.trans.x.toFixed(1)},${SIM.trans.y.toFixed(1)},${SIM.trans.z.toFixed(1)}`;
  document.getElementById('rot-values').textContent = `${SIM.rot.alpha}°,${SIM.rot.phi}°,${SIM.rot.omega}°`;

  if (currentVolAxis === 'x') document.getElementById('vol-value').textContent = SIM.vol.x.toFixed(2);
  else if (currentVolAxis === 'y') document.getElementById('vol-value').textContent = SIM.vol.y.toFixed(2);
  else document.getElementById('vol-value').textContent = SIM.vol.z.toFixed(2);
  document.getElementById('vol-slider').value = SIM.vol[currentVolAxis];

  if (currentTransAxis === 'x') document.getElementById('trans-value').textContent = SIM.trans.x.toFixed(2);
  else if (currentTransAxis === 'y') document.getElementById('trans-value').textContent = SIM.trans.y.toFixed(2);
  else document.getElementById('trans-value').textContent = SIM.trans.z.toFixed(2);
  document.getElementById('trans-slider').value = SIM.trans[currentTransAxis];

  if (currentRotAxis === 'alpha') document.getElementById('rot-value').textContent = SIM.rot.alpha + '°';
  else if (currentRotAxis === 'phi') document.getElementById('rot-value').textContent = SIM.rot.phi + '°';
  else document.getElementById('rot-value').textContent = SIM.rot.omega + '°';
  document.getElementById('rot-slider').value = SIM.rot[currentRotAxis];
}

// Propagation avec tous les DOF et rayon configurable
function propagateToNeighbors(sourceCell, vol, trans, rot, intensity) {
  if (intensity <= 0.02) return;
  for (let cell of cells) {
    if (cell === sourceCell) continue;
    const rowDist = Math.abs(cell.row - sourceCell.row);
    const colDist = Math.abs(cell.col - sourceCell.col);
    const depDist = Math.abs(cell.dep - sourceCell.dep);
    const distance = Math.sqrt(rowDist * rowDist + colDist * colDist + depDist * depDist);
    if (distance <= SIM.propagationRadius && distance > 0) {
      const propIntensity = intensity * (1 - distance / SIM.propagationRadius) * SIM.propagationStrength;
      if (propIntensity > 0.02) {
        const scaledVol = {
          x: vol.x * propIntensity, y: vol.y * propIntensity, z: vol.z * propIntensity
        };
        const scaledTrans = {
          x: trans.x * propIntensity, y: trans.y * propIntensity, z: trans.z * propIntensity
        };
        const scaledRot = {
          alpha: rot.alpha * propIntensity, phi: rot.phi * propIntensity, omega: rot.omega * propIntensity
        };
        cell.volume = { x: cell.volume.x + scaledVol.x, y: cell.volume.y + scaledVol.y, z: cell.volume.z + scaledVol.z };
        cell.trans = { x: cell.trans.x + scaledTrans.x, y: cell.trans.y + scaledTrans.y, z: cell.trans.z + scaledTrans.z };
        cell.rot = { alpha: cell.rot.alpha + scaledRot.alpha, phi: cell.rot.phi + scaledRot.phi, omega: cell.rot.omega + scaledRot.omega };
        applyTransformationsToCell(cell, cell.volume, cell.trans, cell.rot, true);
        applyCellState(cell, 'propagated');
        updateBuildingsHeight(cell);
        if (propIntensity > 0.1) {
          propagateToNeighbors(cell, scaledVol, scaledTrans, scaledRot, propIntensity * 0.5);
        }
      }
    }
  }
}

function applyTransformationsToCell(cell, vol, trans, rot, isPropagation = false) {
  if (!cell) return;
  
  if (!isPropagation) {
    cell.volume = { ...vol };
    cell.trans = { ...trans };
    cell.rot = { ...rot };
  }
  
  cell.mesh.position = new BABYLON.Vector3(cell.origPos.x, cell.origPos.y, cell.origPos.z);
  cell.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
  cell.mesh.scaling = new BABYLON.Vector3(1, 1, 1);
  
  const scaleX = 1 + vol.x * 0.25;
  const scaleY = 1 + vol.y * 0.25;
  const scaleZ = 1 + vol.z * 0.25;
  cell.mesh.scaling = new BABYLON.Vector3(scaleX, scaleY, scaleZ);
  
  cell.mesh.position.x += trans.x * 0.3;
  cell.mesh.position.y += trans.y * 0.2;
  cell.mesh.position.z += trans.z * 0.3;
  
  const radAlpha = rot.alpha * Math.PI / 180;
  const radPhi = rot.phi * Math.PI / 180;
  const radOmega = rot.omega * Math.PI / 180;
  cell.mesh.rotation = new BABYLON.Vector3(radAlpha, radPhi, radOmega);
  
  if (!isPropagation) {
    const volMag = Math.sqrt(vol.x * vol.x + vol.y * vol.y + vol.z * vol.z);
    const transMag = Math.sqrt(trans.x * trans.x + trans.y * trans.y + trans.z * trans.z);
    const rotMag = (Math.abs(rot.alpha) + Math.abs(rot.phi) + Math.abs(rot.omega)) / 45;
    const totalMag = (volMag + transMag + rotMag) / 3;
    
    const stressIncrement = totalMag * 0.3;
    if (stressIncrement > 0) SIM.stress = Math.min(1, SIM.stress + stressIncrement);
    
    if (totalMag > 0.01) {
      applyCellState(cell, 'deformed');
      propagateToNeighbors(cell, vol, trans, rot, 0.7);
      updateBuildingsHeight(cell);
      updateBuildingsTilt(cell, rot);
    } else if (cell !== SIM.selCell) applyCellState(cell, 'normal');
  }
}

function updateBuildingsHeight(cell) {
  const stressFactor = Math.abs(cell.volume.x) + Math.abs(cell.volume.y) + Math.abs(cell.volume.z) +
                       Math.abs(cell.trans.x) + Math.abs(cell.trans.y) + Math.abs(cell.trans.z);
  const building = buildings.find(b => b.cell === cell);
  if (building && building.origHeight) {
    const newHeight = building.origHeight * (1 + stressFactor * 2);
    building.mesh.scaling.y = Math.max(0.5, Math.min(2.5, newHeight / building.origHeight));
    building.mesh.position.y = cell.mesh.position.y + cell.mesh.scaling.y * CH_g / 2 + building.mesh.scaling.y * 0.1;
  }
}

function updateBuildingsTilt(cell, rot) {
  const building = buildings.find(b => b.cell === cell);
  if (building) {
    const tiltX = (rot.phi * 0.5) * Math.PI / 180;
    const tiltZ = (rot.alpha * 0.5) * Math.PI / 180;
    building.mesh.rotation = new BABYLON.Vector3(tiltX, 0, tiltZ);
  }
}

function resetBuildingsTilt() {
  for (let building of buildings) {
    if (building.mesh) {
      building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
    }
  }
}

function onXYZChange() {
  if (!SIM.selCell) return;
  if (SIM.realtimeMode) {
    if (currentVolAxis === 'x') SIM.vol.x = parseFloat(document.getElementById('vol-slider').value);
    else if (currentVolAxis === 'y') SIM.vol.y = parseFloat(document.getElementById('vol-slider').value);
    else SIM.vol.z = parseFloat(document.getElementById('vol-slider').value);
    
    if (currentTransAxis === 'x') SIM.trans.x = parseFloat(document.getElementById('trans-slider').value);
    else if (currentTransAxis === 'y') SIM.trans.y = parseFloat(document.getElementById('trans-slider').value);
    else SIM.trans.z = parseFloat(document.getElementById('trans-slider').value);
    
    if (currentRotAxis === 'alpha') SIM.rot.alpha = parseFloat(document.getElementById('rot-slider').value);
    else if (currentRotAxis === 'phi') SIM.rot.phi = parseFloat(document.getElementById('rot-slider').value);
    else SIM.rot.omega = parseFloat(document.getElementById('rot-slider').value);
    
    updateAllDisplays();
    applyTransformationsToCell(SIM.selCell, SIM.vol, SIM.trans, SIM.rot);
    
    let msg = '';
    if (SIM.vol.y > 0.3) msg = '⬇️ Subsidence → slab pull';
    else if (SIM.vol.y < -0.3) msg = '🌋 Uplift → upwelling';
    else if (SIM.vol.x > 0.3) msg = '↔️ Compression → convergence';
    else if (SIM.vol.x < -0.3) msg = '↔️ Dilation → divergence';
    else if (SIM.trans.x !== 0 || SIM.trans.z !== 0) msg = '🔄 Translation → plate shift';
    else if (SIM.rot.alpha !== 0 || SIM.rot.phi !== 0) msg = '🔄 Rotation → plate rotation';
    if (msg) setStatus('info', msg);
    setTimeout(() => { if (!SIM.quakeActive) setStatus('run', 'Running'); }, 1500);
  }
}

function applyTransformConfig() {
  if (!SIM.selCell) return;
  applyTransformationsToCell(SIM.selCell, SIM.vol, SIM.trans, SIM.rot);
  setStatus('info', '✅ Transformations applied');
  setTimeout(() => { if (!SIM.quakeActive) setStatus('run', 'Running'); }, 1500);
}

// ═══════════════════════════════════════════════════════════════
//  BUILDINGS (80% plus nombreux, hauteurs 1-15, effet domino)
// ═══════════════════════════════════════════════════════════════
function buildBuildings() {
  const buildingPositions = [];
  for (let x = -6.5; x <= -1.5; x += 0.22) {
    for (let z = -2.2; z <= 2.2; z += 0.25) {
      if (Math.random() > 0.2) continue;
      buildingPositions.push({ x: x + (Math.random() - 0.5) * 0.1, z: z + (Math.random() - 0.5) * 0.1 });
    }
  }
  
  const maxBuildings = Math.min(buildingPositions.length, 120);
  
  for (let i = 0; i < maxBuildings; i++) {
    const bp = buildingPositions[i];
    const heightLevels = Math.floor(Math.random() * 15) + 1;
    const height = 0.03 + heightLevels * 0.012;
    const width = 0.07;
    const depth = 0.07;
    
    const r = 0.4 + (heightLevels / 15) * 0.5;
    const g = 0.4 + (heightLevels / 15) * 0.3;
    const b = 0.5 + (heightLevels / 15) * 0.2;
    const buildingMat = new BABYLON.StandardMaterial(`building_${i}`, scene);
    buildingMat.diffuseColor = new BABYLON.Color3(r, g, b);
    buildingMat.emissiveColor = new BABYLON.Color3(0.03, 0.03, 0.05);
    
    const mesh = BABYLON.MeshBuilder.CreateBox(`building_${i}`,
      { width: width, height: height, depth: depth }, scene);
    mesh.position = new BABYLON.Vector3(bp.x, 0.78 + height / 2, bp.z);
    mesh.material = buildingMat;
    mesh.isPickable = false;
    
    buildings.push({ 
      mesh, cell: null, origHeight: height, heightLevels, 
      origPos: { x: bp.x, z: bp.z }, originalY: 0.78 + height / 2,
      tiltX: 0, tiltZ: 0
    });
  }
  
  console.log(`Built ${buildings.length} buildings (height range: 1-15 levels)`);
  
  setTimeout(() => {
    for (let building of buildings) {
      let minDist = Infinity;
      for (let cell of cells) {
        const dist = Math.hypot(building.mesh.position.x - cell.mesh.position.x, building.mesh.position.z - cell.mesh.position.z);
        if (dist < minDist && dist < 0.8) {
          minDist = dist;
          building.cell = cell;
        }
      }
      if (building.cell) updateBuildingsHeight(building.cell);
    }
  }, 200);
}

function applyDominoEffect(epicenterCell, intensity) {
  if (!epicenterCell) return;
  
  const epicenterX = epicenterCell.mesh.position.x;
  const epicenterZ = epicenterCell.mesh.position.z;
  
  for (let building of buildings) {
    if (!building.cell) continue;
    
    const dx = building.mesh.position.x - epicenterX;
    const dz = building.mesh.position.z - epicenterZ;
    const distance = Math.hypot(dx, dz);
    
    const effectIntensity = intensity * (1 - Math.min(1, distance / 6)) * (0.6 + Math.random() * 0.6);
    
    if (effectIntensity > 0.1) {
      const tiltAngle = effectIntensity * 35 * (building.heightLevels / 20);
      const angle = Math.atan2(dz, dx);
      const tiltX = Math.cos(angle) * tiltAngle * Math.PI / 180;
      const tiltZ = Math.sin(angle) * tiltAngle * Math.PI / 180;
      
      building.mesh.rotation = new BABYLON.Vector3(tiltZ, 0, -tiltX);
      building.tiltX = tiltZ;
      building.tiltZ = -tiltX;
      
      if (building.mesh.material) {
        building.mesh.material.emissiveIntensity = 0.3;
        setTimeout(() => {
          if (building.mesh && building.mesh.material) {
            building.mesh.material.emissiveIntensity = 0;
          }
        }, 800);
      }
      
      setTimeout(() => {
        if (building.mesh && !SIM.quakeActive) {
          building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
          building.tiltX = 0;
          building.tiltZ = 0;
        }
      }, 2500);
    }
  }
}

// ═══════════════════════════════════════════════════════════════
//  PLANET EARTH (True Sphere Mode)
// ═══════════════════════════════════════════════════════════════
function buildPlanetEarth() {
  const earthMat = new BABYLON.StandardMaterial("earthMat", scene);
  
  const textureSize = 1024;
  const canvas = document.createElement("canvas");
  canvas.width = textureSize;
  canvas.height = textureSize;
  const ctx = canvas.getContext("2d");
  
  ctx.fillStyle = "#1a4d8c";
  ctx.fillRect(0, 0, textureSize, textureSize);
  
  ctx.fillStyle = "#5a8c5a";
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.25, textureSize * 0.35, textureSize * 0.12, textureSize * 0.1, 0, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.28, textureSize * 0.55, textureSize * 0.08, textureSize * 0.12, 0, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.65, textureSize * 0.4, textureSize * 0.18, textureSize * 0.12, 0, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.55, textureSize * 0.55, textureSize * 0.1, textureSize * 0.1, 0, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.75, textureSize * 0.45, textureSize * 0.1, textureSize * 0.08, 0, 0, 2 * Math.PI);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(textureSize * 0.8, textureSize * 0.7, textureSize * 0.07, textureSize * 0.06, 0, 0, 2 * Math.PI);
  ctx.fill();
  
  ctx.strokeStyle = "#ff6644";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(textureSize * 0.45, textureSize * 0.3);
  ctx.lineTo(textureSize * 0.5, textureSize * 0.5);
  ctx.lineTo(textureSize * 0.48, textureSize * 0.7);
  ctx.stroke();
  
  ctx.strokeStyle = "#3388ff";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(textureSize * 0.2, textureSize * 0.6);
  ctx.lineTo(textureSize * 0.25, textureSize * 0.75);
  ctx.lineTo(textureSize * 0.35, textureSize * 0.8);
  ctx.stroke();
  
  ctx.strokeStyle = "#88ff88";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(textureSize * 0.3, textureSize * 0.4);
  ctx.lineTo(textureSize * 0.35, textureSize * 0.45);
  ctx.lineTo(textureSize * 0.32, textureSize * 0.52);
  ctx.stroke();
  
  earthMat.diffuseTexture = new BABYLON.Texture(canvas.toDataURL(), scene);
  earthMat.specularColor = new BABYLON.Color3(0.1, 0.1, 0.1);
  
  planetEarth = BABYLON.MeshBuilder.CreateSphere("earth", { diameter: 5, segments: 64 }, scene);
  planetEarth.material = earthMat;
  planetEarth.position = new BABYLON.Vector3(0, 0, 0);
  planetEarth.isVisible = false;
  
  const atmosMat = new BABYLON.StandardMaterial("atmos", scene);
  atmosMat.diffuseColor = new BABYLON.Color3(0.3, 0.5, 0.9);
  atmosMat.alpha = 0.15;
  atmosMat.backFaceCulling = false;
  const atmosphere = BABYLON.MeshBuilder.CreateSphere("atmosphere", { diameter: 5.1, segments: 64 }, scene);
  atmosphere.material = atmosMat;
  atmosphere.isVisible = false;
  planetEarth.atmosphere = atmosphere;
}

function switchViewMode(mode) {
  SIM.viewMode = mode;
  if (mode === 'planet') {
    for (let cell of cells) cell.mesh.isVisible = false;
    for (let building of buildings) building.mesh.isVisible = false;
    for (let plate of continentalPlates) plate.isVisible = false;
    for (let plate of oceanicPlates) plate.isVisible = false;
    for (let arrow of convArrows) if(arrow) arrow.isVisible = false;
    if (hotspotMesh) hotspotMesh.isVisible = false;
    for (let slab of slabMeshes) if(slab) slab.isVisible = false;
    
    if (planetEarth) {
      planetEarth.isVisible = true;
      if (planetEarth.atmosphere) planetEarth.atmosphere.isVisible = true;
    }
    
    camera.alpha = 0;
    camera.beta = Math.PI / 2.5;
    camera.radius = 8;
    camera.target = new BABYLON.Vector3(0, 0, 0);
    setStatus('info', '🌍 Planet Mode - Spherical Earth with tectonic features');
  } else {
    for (let cell of cells) cell.mesh.isVisible = true;
    for (let building of buildings) building.mesh.isVisible = true;
    for (let plate of continentalPlates) plate.isVisible = true;
    for (let plate of oceanicPlates) plate.isVisible = true;
    for (let arrow of convArrows) if(arrow) arrow.isVisible = true;
    if (hotspotMesh) hotspotMesh.isVisible = SIM.plumeActive;
    for (let slab of slabMeshes) if(slab) slab.isVisible = true;
    
    if (planetEarth) {
      planetEarth.isVisible = false;
      if (planetEarth.atmosphere) planetEarth.atmosphere.isVisible = false;
    }
    
    camera.alpha = -Math.PI * 0.28;
    camera.beta = Math.PI * 0.30;
    camera.radius = 26;
    camera.target = new BABYLON.Vector3(0, -.5, 0);
    setStatus('info', '🍰 Layer Cake Mode - Classic cross-section view');
  }
  setTimeout(() => { if (!SIM.quakeActive) setStatus('run', 'Running'); }, 1500);
}

// ═══════════════════════════════════════════════════════════════
//  SCENE BUILDING
// ═══════════════════════════════════════════════════════════════
function mat(nm, r, g, b, al, er, eg, eb) {
  const m = new BABYLON.StandardMaterial(nm, scene);
  m.diffuseColor = new BABYLON.Color3(r, g, b);
  if (al != null && al < 1) { m.alpha = al; m.backFaceCulling = false; }
  if (er != null) m.emissiveColor = new BABYLON.Color3(er, eg, eb);
  return m;
}

function box(nm, w, h, d, x, y, z, m, p) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { width: w, height: h, depth: d }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  if (p) mesh.parent = p;
  return mesh;
}

function mkDot() {
  const c = document.createElement('canvas');
  c.width = c.height = 32;
  const g = c.getContext('2d'), r = g.createRadialGradient(16, 16, 0, 16, 16, 14);
  r.addColorStop(0, 'rgba(255,255,255,1)');
  r.addColorStop(.6, 'rgba(255,255,255,.55)');
  r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r;
  g.beginPath();
  g.arc(16, 16, 14, 0, Math.PI * 2);
  g.fill();
  return c.toDataURL();
}

function ps(nm, cap, tex, ex, ey, ez, mBx, mBy, mBz, MBx, MBy, MBz, c1, c2, d1, d2, mS, MS, mL, ML, rate) {
  const p = new BABYLON.ParticleSystem(nm, cap, scene);
  p.particleTexture = new BABYLON.Texture(tex, scene);
  p.emitter = new BABYLON.Vector3(ex, ey, ez);
  p.minEmitBox = new BABYLON.Vector3(mBx, mBy, mBz);
  p.maxEmitBox = new BABYLON.Vector3(MBx, MBy, MBz);
  p.color1 = new BABYLON.Color4(...c1);
  p.color2 = new BABYLON.Color4(...c2);
  p.colorDead = new BABYLON.Color4(0, 0, 0, 0);
  p.minSize = mS;
  p.maxSize = MS;
  p.minLifeTime = mL;
  p.maxLifeTime = ML;
  p.emitRate = rate;
  p.direction1 = new BABYLON.Vector3(...d1);
  p.direction2 = new BABYLON.Vector3(...d2);
  p.minEmitPower = .15;
  p.maxEmitPower = .65;
  p.gravity = new BABYLON.Vector3(0, -.04, 0);
  return p;
}

function buildScene() {
  box('mantle', 14, 2.4, 5, 0, -3.2, 0, mat('mM', .68, .03, .01));
  box('lithoBase', 14, .75, 5, 0, -.60, 0, mat('lbM', .55, .40, .25, 0.96));

  const GAP2 = 0.06, PW = (7 - GAP2 * 2) / 3, PD = (5 - GAP2 * 2) / 3;
  const cc = [[.65, .52, .34], [.60, .48, .30], [.58, .46, .28], [.62, .50, .32], [.64, .51, .33], [.56, .44, .27], [.63, .50, .31], [.61, .49, .30], [.59, .47, .29]];

  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const cx = -7 + GAP2 + PW * .5 + c2 * (PW + GAP2);
      const cz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      const contPlate = box(`cc_${idx}`, PW, .90, PD, cx, .25, cz, mat(`ccm${idx}`, ...cc[idx], 0.98));
      continentalPlates.push(contPlate);
      box(`cs_${idx}`, PW, .07, PD, cx, .72, cz, mat(`csm${idx}`, ...cc[idx].map(v => v * .85), 0.95));
      
      if (c2 < 2) {
        const fm = mat(`fm_h${idx}`, .25, .65, .15, 1, .05, .15, 0);
        faultMats.push(fm);
        box(`fh_${idx}`, .05, .07, PD, cx + PW * .5 + GAP2 * .5, .75, cz, fm);
      }
    }
  }
  box('contTop', 7, .06, 5, -3.5, .74, 0, mat('ctm', .47, .40, .26, 0.95));

  const oc = [[.12, .19, .38], [.14, .21, .40], [.11, .18, .36], [.13, .20, .39], [.15, .22, .41], [.10, .17, .35], [.12, .19, .37], [.13, .20, .38], [.11, .18, .36]];
  
  for (let r = 0; r < 3; r++) {
    for (let c2 = 0; c2 < 3; c2++) {
      const idx = r * 3 + c2;
      const ox = GAP2 + PW * .5 + c2 * (PW + GAP2);
      const oz = -2.5 + GAP2 + PD * .5 + r * (PD + GAP2);
      
      box(`rlitho_${idx}`, PW, .55, PD, ox, -.70, oz, mat(`rlm${idx}`, .20, .18, .30, 0.94));
      box(`rcrust_${idx}`, PW, .30, PD, ox, -.08, oz, mat(`rcm${idx}`, ...oc[idx], 0.96));
      box(`rocean_${idx}`, PW, .55, PD, ox, .42, oz, mat(`ocm${idx}`, .04, .22, .68, 0.88));
    }
  }

  const ch = BABYLON.MeshBuilder.CreateSphere('ch', { diameter: 1.8, segments: 8 }, scene);
  ch.scaling.y = .44;
  ch.position = new BABYLON.Vector3(0, -.46, 0);
  ch.material = mat('chm', 1, .45, .06, 1, .55, .14, 0);
  
  const rc = BABYLON.MeshBuilder.CreateSphere('rc', { diameter: 2.0, segments: 8 }, scene);
  rc.scaling.y = .32;
  rc.position = new BABYLON.Vector3(0, .22, 0);
  rc.material = mat('rcm', .88, .38, .08, 1, .30, .10, 0);

  const mt = BABYLON.MeshBuilder.CreateCylinder('mt', { diameterTop: .04, diameterBottom: 2.2, height: 1.9, tessellation: 8 }, scene);
  mt.position = new BABYLON.Vector3(-5.5, 1.68, .3);
  mt.material = mat('mtm', .58, .52, .46);
  
  const snow = BABYLON.MeshBuilder.CreateSphere('snow', { diameter: .58, segments: 6 }, scene);
  snow.scaling.y = .44;
  snow.position = new BABYLON.Vector3(-5.5, 2.55, .3);
  snow.material = mat('snm', .94, .96, 1, 1, .08, .08, .08);

  box('trench', 1.4, .40, 5, 5.5, -.22, 0, mat('tm', .06, .08, .16));
  
  const sl1 = box('slab1', 4.2, .35, 5, 5.5, -2.0, 0, mat('slm', .18, .20, .30, .90));
  sl1.rotation.z = -Math.PI * .20;
  slabMeshes.push(sl1);
  
  const sl2 = box('slab2', 2.8, .32, 5, 6.2, -3.2, 0, mat('slm2', .14, .16, .26, .78));
  sl2.rotation.z = -Math.PI * .28;
  slabMeshes.push(sl2);

  const vc = BABYLON.MeshBuilder.CreateCylinder('vc', { diameterTop: .06, diameterBottom: 1.3, height: 1.8, tessellation: 7 }, scene);
  vc.position = new BABYLON.Vector3(3.8, 1.55, .3);
  vc.material = mat('vcm', .24, .20, .22);
  
  const ld = BABYLON.MeshBuilder.CreateSphere('ld', { diameter: .30, segments: 5 }, scene);
  ld.position = new BABYLON.Vector3(3.8, 2.42, .3);
  ld.material = mat('ldm', 1, .25, .03, 1, .60, .10, 0);

  hotspotMesh = BABYLON.MeshBuilder.CreateSphere('hs', { diameter: .55, segments: 7 }, scene);
  hotspotMesh.position = new BABYLON.Vector3(-3, .76, 0);
  hotspotMesh.material = mat('hm', 1, .45, .06, 1, .60, .18, 0);
  hotspotMesh.isVisible = false;

  const gm = new BABYLON.StandardMaterial('gls', scene);
  gm.diffuseColor = new BABYLON.Color3(.35, .55, .90);
  gm.emissiveColor = new BABYLON.Color3(.05, .08, .15);
  gm.alpha = 0.15;
  gm.backFaceCulling = false;
  
  function wall(nm, w, h, pos, ry) {
    const p = BABYLON.MeshBuilder.CreatePlane(nm, { width: w, height: h }, scene);
    p.position = pos;
    p.rotation.y = ry;
    p.material = gm;
  }
  wall('wF', 14, 8.4, new BABYLON.Vector3(0, -.8, 2.58), 0);
  wall('wB', 14, 8.4, new BABYLON.Vector3(0, -.8, -2.58), Math.PI);
  wall('wL', 5, 8.4, new BABYLON.Vector3(-7, -.8, 0), Math.PI * .5);
  wall('wR', 5, 8.4, new BABYLON.Vector3(7, -.8, 0), -Math.PI * .5);
}

function buildParticles() {
  const dot = mkDot();
  psConv = ps('psC', 180, dot, 0, -2, 0, -6.5, -.7, -2.2, 6.5, .7, 2.2, [1, .52, .10, .70], [.80, .20, .04, .45], [-0.3, .9, .2], [.3, .9, -.2], .10, .35, 3, 7, 28);
  psRidge = ps('psR', 100, dot, 0, -.1, 0, -.4, 0, -2.2, .4, 0, 2.2, [1, .65, .12, .92], [1, .30, .04, .72], [-.04, 1, .04], [.04, 1, -.04], .07, .16, 1, 2.5, 18);
  psVol = ps('psV', 60, dot, 3.8, 2.3, .3, -.08, 0, -.08, .08, 0, .08, [1, .40, .05, .92], [.85, .18, .02, .65], [-.5, 1, -.5], [.5, 1, .5], .06, .14, 1.4, 2.8, 10);
  psQuake = ps('psQ', 80, dot, 0, .80, 0, -.1, 0, -2, .1, 0, 2, [1, .80, .20, .92], [1, .40, .10, .70], [-.7, 1, -.7], [.7, 1, .7], .08, .20, .6, 1.6, 0);
  psQuake.targetStopDuration = .7;
  psPlume = ps('psPl', 120, dot, -3, -3.8, 0, -.18, 0, -.18, .18, 0, .18, [1, .70, .15, .90], [1, .35, .05, .65], [-.04, 1, -.04], [.04, 1, .04], .06, .16, 2.5, 5, 0);
  psPlume.gravity = new BABYLON.Vector3(0, .12, 0);
  psConv.start();
  psRidge.start();
  psVol.start();
}

function initScene() {
  const canvas = document.getElementById('renderCanvas');
  engine = new BABYLON.Engine(canvas, true, { antialias: true });
  scene = new BABYLON.Scene(engine);
  scene.clearColor = new BABYLON.Color4(.02, .03, .06, 1);

  camera = new BABYLON.ArcRotateCamera('cam', -Math.PI * .28, Math.PI * .30, 26, new BABYLON.Vector3(0, -.5, 0), scene);
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 4;
  camera.upperRadiusLimit = 50;
  camera.lowerBetaLimit = 0.01;
  camera.upperBetaLimit = Math.PI - 0.01;
  camera.wheelDeltaPercentage = .01;

  const amb = new BABYLON.HemisphericLight('amb', new BABYLON.Vector3(0, 1, 0), scene);
  amb.intensity = .40;
  const sun = new BABYLON.DirectionalLight('sun', new BABYLON.Vector3(-1, -1.2, -.5), scene);
  sun.intensity = .82;
  const mg = new BABYLON.PointLight('mg', new BABYLON.Vector3(0, -1.2, 0), scene);
  mg.diffuse = new BABYLON.Color3(1, .35, .05);
  mg.intensity = 4.0;
  mg.range = 18;
  const rg = new BABYLON.PointLight('rg', new BABYLON.Vector3(0, .5, 0), scene);
  rg.diffuse = new BABYLON.Color3(1, .60, .15);
  rg.intensity = 2.0;
  rg.range = 7;
  new BABYLON.PointLight('vg', new BABYLON.Vector3(4.5, 2, 0), scene).diffuse = new BABYLON.Color3(1, .30, .04);
  const backLight = new BABYLON.PointLight('bk', new BABYLON.Vector3(0, 0, -6), scene);
  backLight.diffuse = new BABYLON.Color3(.55, .45, .38);
  backLight.intensity = 1.4;

  buildScene();
  buildMantleGrid();
  buildParticles();
  buildBuildings();
  buildPlanetEarth();

  quakeFlash = document.getElementById('quake-flash');

  scene.registerBeforeRender(renderLoop);
  engine.runRenderLoop(() => scene.render());
  new ResizeObserver(() => engine.resize()).observe(document.getElementById('cv'));
}

let _rg, _mg;
function renderLoop() {
  if (!_rg) { _rg = scene.getLightByName('rg'); _mg = scene.getLightByName('mg'); }
  const dt = Math.min(engine.getDeltaTime() * .001, .05);
  if (!SIM.running) return;
  SIM.t += dt;
  const cv = SIM.convection;
  if (_rg) _rg.intensity = 1.8 + Math.sin(SIM.t * 2) * .8 * cv;
  if (_mg) _mg.intensity = 3.5 + Math.sin(SIM.t * .7) * 1.0;
  if (psConv) psConv.emitRate = Math.round(14 + cv * 55);
  if (psRidge) psRidge.emitRate = Math.round(7 + cv * 35);

  const stressRate = dt * .025 * cv * (1 + SIM.asymmetry * 0.3);
  SIM.stress = Math.min(1, SIM.stress + stressRate);
  if (SIM.quakeCooldown > 0) SIM.quakeCooldown -= dt;

  const pct = Math.round(SIM.stress * 100);
  document.getElementById('sfl').style.width = pct + '%';
  document.getElementById('sfl').style.background = SIM.stress < .5 ? 'var(--accent)' : SIM.stress < .80 ? 'var(--warn)' : 'var(--eagle)';
  document.getElementById('val-stress').textContent = pct + '%';

  faultMats.forEach(fm => {
    const sr = Math.max(.15, SIM.stress * .95 + .05), sg = Math.max(0, .65 - SIM.stress * .65);
    fm.diffuseColor = new BABYLON.Color3(sr, sg, .06);
  });

  if (SIM.stress >= 0.90 && !SIM.quakeActive && SIM.quakeCooldown <= 0) triggerQuake();

  if (SIM.quakeActive) {
    SIM.quakeTimer -= dt;
    const shk = (Math.random() - .5) * 0.06;
    camera.target.x += shk;
    camera.target.y += shk * .3;
    if (SIM.quakeTimer <= 0) {
      SIM.quakeActive = false;
      SIM.quakeCooldown = 2.0;
      camera.target = new BABYLON.Vector3(0, -.5, 0);
      resetBuildingsTilt();
      setStatus('run', 'Running');
    }
  }

  if (slabMeshes[0]) {
    slabMeshes[0].rotation.z = -Math.PI * (.12 + SIM.slabDensity * .20);
    slabMeshes[1].rotation.z = -Math.PI * (.16 + SIM.slabDensity * .26);
  }

  if (SIM.plumeActive) {
    SIM.plumeTimer -= dt;
    const sc = Math.sin(SIM.plumeTimer * Math.PI / 6);
    if (hotspotMesh) {
      hotspotMesh.isVisible = true;
      hotspotMesh.scaling = new BABYLON.Vector3(sc, sc, sc);
    }
    if (SIM.plumeTimer <= 0) {
      SIM.plumeActive = false;
      if (hotspotMesh) hotspotMesh.isVisible = false;
      if (psPlume) psPlume.stop();
      document.getElementById('btn-plume').classList.remove('active');
    }
  }

  if (SIM.viewMode === 'planet' && planetEarth) {
    planetEarth.rotation.y += 0.002;
    if (planetEarth.atmosphere) planetEarth.atmosphere.rotation.y += 0.002;
  }
}

function triggerQuake() {
  SIM.quakeActive = true;
  SIM.quakeTimer = 1.6;
  SIM.stress = Math.max(0, SIM.stress - 0.6);
  if (psQuake) { psQuake.start(); setTimeout(() => psQuake.stop(), 900); }
  if (quakeFlash) { quakeFlash.style.display = 'block'; setTimeout(() => { quakeFlash.style.display = 'none'; }, 500); }
  
  applyDominoEffect(SIM.selCell, 1.0);
  
  setStatus('warn', '⚠️ FAULT RUPTURE - DOMINO EFFECT ⚠️');
}

function setStatus(type, msg) {
  const dot = document.getElementById('sdot'), lbl = document.getElementById('slbl');
  dot.className = 'sdot';
  if (type === 'run') dot.classList.add('run');
  else if (type === 'warn') dot.classList.add('warn');
  else if (type === 'info') dot.classList.add('info');
  if (msg) lbl.textContent = msg;
}

function togglePanel(panelId) {
  const content = document.getElementById(panelId);
  const toggle = document.getElementById(panelId.replace('-content', '-toggle'));
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    content.classList.add('collapsed');
    if (toggle) toggle.textContent = '▼';
  } else {
    content.classList.remove('collapsed');
    content.classList.add('expanded');
    if (toggle) toggle.textContent = '▲';
  }
}

function toggleSection(sectionId) {
  const content = document.getElementById(sectionId);
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    content.classList.add('collapsed');
  } else {
    content.classList.remove('collapsed');
    content.classList.add('expanded');
  }
}

function wireControls() {
  document.getElementById('btn-play').addEventListener('click', () => {
    SIM.running = !SIM.running;
    const b = document.getElementById('btn-play');
    b.textContent = SIM.running ? '⏸ Pause' : '▶ Play';
    b.classList.toggle('active', SIM.running);
    if (SIM.running) { if (psConv) psConv.start(); if (psRidge) psRidge.start(); if (psVol) psVol.start(); }
    else { if (psConv) psConv.stop(); if (psRidge) psRidge.stop(); if (psVol) psVol.stop(); }
  });

  document.getElementById('btn-reset').addEventListener('click', () => {
    SIM.running = true; SIM.t = 0; SIM.stress = 0; SIM.quakeActive = false; SIM.quakeCooldown = 0;
    SIM.wilsonActive = false; SIM.plumeActive = false;
    SIM.convection = .5; SIM.slabDensity = .6; SIM.asymmetry = 0; SIM.propagationStrength = 0.8; SIM.propagationRadius = 2.5;
    document.getElementById('sl-conv').value = .5; document.getElementById('val-conv').textContent = '50%';
    document.getElementById('sl-slab').value = .6; document.getElementById('val-slab').textContent = '60%';
    document.getElementById('sl-asym').value = 0; document.getElementById('val-asym').textContent = '0';
    document.getElementById('sl-propagation').value = 0.8; document.getElementById('val-propagation').textContent = '80%';
    document.getElementById('sl-radius').value = 2.5; document.getElementById('val-radius').textContent = '2.5';
    camera.alpha = -Math.PI * .28; camera.beta = Math.PI * .30; camera.radius = 26;
    camera.target = new BABYLON.Vector3(0, -.5, 0);
    if (hotspotMesh) hotspotMesh.isVisible = false;
    if (psPlume && psPlume.isStarted()) psPlume.stop();
    cells.forEach((c, idx) => {
      c.mesh.position = new BABYLON.Vector3(origCellPositions[idx].x, origCellPositions[idx].y, origCellPositions[idx].z);
      c.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
      c.mesh.scaling = new BABYLON.Vector3(1, 1, 1);
      c.volume = { x: 0, y: 0, z: 0 }; c.trans = { x: 0, y: 0, z: 0 }; c.rot = { alpha: 0, phi: 0, omega: 0 };
      applyCellState(c, 'normal');
    });
    for (let building of buildings) {
      building.mesh.position.y = building.originalY;
      building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
      if (building.cell) updateBuildingsHeight(building.cell);
    }
    if (SIM.selCell) { applyCellState(SIM.selCell, 'normal'); SIM.selCell = null; }
    SIM.hovCell = null;
    document.getElementById('cell-panel').classList.add('hide');
    SIM.vol = { x: 0, y: 0, z: 0 }; SIM.trans = { x: 0, y: 0, z: 0 }; SIM.rot = { alpha: 0, phi: 0, omega: 0 };
    updateAllDisplays();
    document.getElementById('btn-play').textContent = '⏸ Pause';
    document.getElementById('btn-play').classList.add('active');
    document.getElementById('btn-wilson').classList.remove('active');
    document.getElementById('btn-plume').classList.remove('active');
    if (psConv && !psConv.isStarted()) { psConv.start(); psRidge.start(); psVol.start(); }
    setStatus('run', 'Running');
  });

  document.getElementById('btn-plume').addEventListener('click', () => {
    if (SIM.plumeActive) return;
    SIM.plumeActive = true; SIM.plumeTimer = 6; if (psPlume) psPlume.start();
    document.getElementById('btn-plume').classList.add('active');
    setStatus('orange', '🌋 Mantle Plume rising 🌋');
  });

  document.getElementById('btn-wilson').addEventListener('click', () => {
    SIM.wilsonActive = !SIM.wilsonActive;
    document.getElementById('btn-wilson').classList.toggle('active', SIM.wilsonActive);
    setStatus('info', SIM.wilsonActive ? 'Wilson Cycle...' : '');
  });

  document.getElementById('btn-labels').addEventListener('click', () => {
    SIM.showLegend = !SIM.showLegend;
    document.getElementById('legend-panel').style.display = SIM.showLegend ? 'block' : 'none';
    document.getElementById('btn-labels').classList.toggle('active', SIM.showLegend);
  });

  document.getElementById('sl-conv').addEventListener('input', e => { SIM.convection = parseFloat(e.target.value); document.getElementById('val-conv').textContent = Math.round(SIM.convection * 100) + '%'; });
  document.getElementById('sl-slab').addEventListener('input', e => { SIM.slabDensity = parseFloat(e.target.value); document.getElementById('val-slab').textContent = Math.round(SIM.slabDensity * 100) + '%'; });
  document.getElementById('sl-asym').addEventListener('input', e => { SIM.asymmetry = parseFloat(e.target.value); document.getElementById('val-asym').textContent = (SIM.asymmetry >= 0 ? '+' : '') + SIM.asymmetry.toFixed(2); });
  document.getElementById('sl-propagation').addEventListener('input', e => { SIM.propagationStrength = parseFloat(e.target.value); document.getElementById('val-propagation').textContent = Math.round(SIM.propagationStrength * 100) + '%'; document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength * 100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`; });
  document.getElementById('sl-radius').addEventListener('input', e => { SIM.propagationRadius = parseFloat(e.target.value); document.getElementById('val-radius').textContent = SIM.propagationRadius.toFixed(1); document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength * 100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`; });

  document.getElementById('vol-axis').addEventListener('change', e => {
    currentVolAxis = e.target.value;
    document.getElementById('vol-slider').value = SIM.vol[currentVolAxis];
    document.getElementById('vol-value').textContent = SIM.vol[currentVolAxis].toFixed(2);
  });
  document.getElementById('trans-axis').addEventListener('change', e => {
    currentTransAxis = e.target.value;
    document.getElementById('trans-slider').value = SIM.trans[currentTransAxis];
    document.getElementById('trans-value').textContent = SIM.trans[currentTransAxis].toFixed(2);
  });
  document.getElementById('rot-axis').addEventListener('change', e => {
    currentRotAxis = e.target.value;
    document.getElementById('rot-slider').value = SIM.rot[currentRotAxis];
    document.getElementById('rot-value').textContent = SIM.rot[currentRotAxis] + '°';
  });

  document.getElementById('vol-slider').addEventListener('input', e => { onXYZChange(); });
  document.getElementById('trans-slider').addEventListener('input', e => { onXYZChange(); });
  document.getElementById('rot-slider').addEventListener('input', e => { onXYZChange(); });

  const modeRealtime = document.getElementById('mode-realtime');
  const modeConfigure = document.getElementById('mode-configure');
  const applyBtn = document.getElementById('xyz-apply');
  modeRealtime.addEventListener('click', () => {
    SIM.realtimeMode = true;
    modeRealtime.classList.add('realtime');
    modeConfigure.classList.remove('active');
    modeRealtime.classList.remove('active');
    modeConfigure.classList.remove('realtime');
    applyBtn.style.display = 'none';
    setStatus('info', '🎬 Real Time mode: immediate deformation + propagation');
    setTimeout(() => { if (!SIM.quakeActive) setStatus('run', 'Running'); }, 1500);
  });
  modeConfigure.addEventListener('click', () => {
    SIM.realtimeMode = false;
    modeConfigure.classList.add('active');
    modeRealtime.classList.remove('realtime');
    modeConfigure.classList.remove('realtime');
    modeRealtime.classList.remove('active');
    applyBtn.style.display = 'block';
    setStatus('info', '⚙️ Configure mode: adjust then Apply');
    setTimeout(() => { if (!SIM.quakeActive) setStatus('run', 'Running'); }, 1500);
  });
  modeRealtime.classList.add('realtime');
  applyBtn.style.display = 'none';
  document.getElementById('xyz-apply').addEventListener('click', applyTransformConfig);
  document.getElementById('cp-close').addEventListener('click', () => { deselectCell(); });

  document.getElementById('mode-layer').addEventListener('click', () => {
    document.getElementById('mode-layer').classList.add('active');
    document.getElementById('mode-planet').classList.remove('active');
    switchViewMode('layer');
  });
  document.getElementById('mode-planet').addEventListener('click', () => {
    document.getElementById('mode-planet').classList.add('active');
    document.getElementById('mode-layer').classList.remove('active');
    switchViewMode('planet');
  });

  document.getElementById('btn-play').classList.add('active');
  document.getElementById('btn-labels').classList.add('active');
}

function wireSplitter() {
  const sp = document.getElementById('sp'), app = document.getElementById('app');
  let drag = false, sx = 0, sw = 0;
  sp.addEventListener('mousedown', e => { drag = true; sx = e.clientX; sw = document.getElementById('sb').getBoundingClientRect().width; sp.classList.add('drag'); document.body.style.cursor = 'col-resize'; e.preventDefault(); });
  document.addEventListener('mousemove', e => { if (!drag) return; app.style.setProperty('--sidebar-w', Math.max(180, Math.min(640, sw + (sx - e.clientX))) + 'px'); });
  document.addEventListener('mouseup', () => { drag = false; sp.classList.remove('drag'); document.body.style.cursor = ''; });
}

function wireTabs() {
  document.querySelectorAll('.tab-btn').forEach(b => {
    b.addEventListener('click', () => {
      const t = b.dataset.tab;
      document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      document.getElementById('panel-' + t).classList.add('active');
    });
  });
  document.querySelector('[data-tab="desc"]').classList.add('active');
  document.getElementById('panel-desc').classList.add('active');
}

window.addEventListener('DOMContentLoaded', () => {
  initScene();
  wireControls();
  wireSplitter();
  wireTabs();
  setStatus('run', 'Running');
});