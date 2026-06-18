// src/mantleGrid.js - Grille mantellique interactive

// Dimensions calculées à partir de CONFIG
const CW = CONFIG.TOTAL_W / CONFIG.MCOLS;
const CH = CONFIG.TOTAL_H / CONFIG.MROWS;
const CZ_full = CONFIG.TOTAL_D / CONFIG.MZDEPTHS;
const CW_g = CW - CONFIG.GAP;
const CH_g = CH - CONFIG.GAP;
const CD_g = CZ_full - CONFIG.GAP;

// Applique un état visuel à une cellule
function applyCellState(cell, state) {
  if (!cell) return;
  cell.state = state;
  const col = CONFIG.CELL_COLORS[state] || CONFIG.CELL_COLORS.normal;
  const wc = CONFIG.WIRE_COLORS[state] || CONFIG.WIRE_COLORS.normal;
  if (col) {
    cell.mat.diffuseColor = new BABYLON.Color3(col.r * cell.heatT, col.g, col.b);
    cell.mat.emissiveColor = new BABYLON.Color3(col.em_r * cell.heatT, col.em_g, col.em_b);
    cell.mat.alpha = col.al;
  }
  if (wc && wc.c) {
    cell.wires.forEach(w => { w.color = wc.c; w.alpha = wc.al; });
  }
}

// Construit la grille de cellules
function buildMantleGrid() {
  cells = [];
  origCellPositions = [];
  const startX = -6.8 + CW / 2;
  const startY = -2.0 + CH / 2;
  const startZ = -CONFIG.TOTAL_D / 2 + CZ_full / 2;

  for (let row = 0; row < CONFIG.MROWS; row++) {
    for (let col = 0; col < CONFIG.MCOLS; col++) {
      for (let dep = 0; dep < CONFIG.MZDEPTHS; dep++) {
        const cx = startX + col * CW;
        const cy = startY + row * CH;
        const cz = startZ + dep * CZ_full;
        const heatT = 1 - ((CONFIG.MROWS - 1 - row) / (CONFIG.MROWS - 1)) * .25;

        const cellMat = new BABYLON.StandardMaterial(`cm_${row}_${col}_${dep}`, scene);
        cellMat.diffuseColor = new BABYLON.Color3(.78 * heatT, .14, .02);
        cellMat.emissiveColor = new BABYLON.Color3(.14 * heatT, .018, 0);
        cellMat.alpha = CONFIG.CELL_COLORS.normal.al;
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
          stress: 0,
          volume: { x: 0, y: 0, z: 0 }, trans: { x: 0, y: 0, z: 0 }, rot: { alpha: 0, phi: 0, omega: 0 }
        };

        origCellPositions.push({ x: cx, y: cy, z: cz });
        cells.push(cell);
      }
    }
  }

  setupRayPicking();
}

// Gestion du ray picking pour hover et clic
// Modifier setupRayPicking pour vérifier le mode
function setupRayPicking() {
  scene.onPointerObservable.add((evt) => {
    // NE RIEN FAIRE EN MODE PLANÈTE - RETOUR IMMÉDIAT
    if (SIM.viewMode === 'planet') return;
    
    if (evt.type === BABYLON.PointerEventTypes.POINTERMOVE) {
      const pickInfo = scene.pick(scene.pointerX, scene.pointerY, (m) => {
        return m.isPickable && m.name && m.name.startsWith('cell_');
      });
      if (pickInfo && pickInfo.hit && pickInfo.pickedMesh) {
        const pickedCell = cells.find(c => c.mesh === pickInfo.pickedMesh);
        if (pickedCell && pickedCell !== SIM.selCell) {
          if (SIM.hovCell && SIM.hovCell !== pickedCell && SIM.hovCell !== SIM.selCell)
            applyCellState(SIM.hovCell, 'normal');
          SIM.hovCell = pickedCell;
          applyCellState(pickedCell, 'hover');
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
        if (pickedCell) {
          clickCell(pickedCell);
        }
      } else {
        deselectCell();
      }
    }
  });
}

// Gestion du clic sur une cellule
function clickCell(cell) {
  // Désélectionner si même cellule
  if (SIM.selCell === cell) {
    deselectCell();
    return;
  }
  
  // Restaurer l'état précédent
  if (SIM.selCell) {
    applyCellState(SIM.selCell, 'normal');
  }
  
  // Sélectionner la nouvelle cellule
  SIM.selCell = cell;
  applyCellState(cell, 'select');
  
  // Injection de perturbation de contrainte (déclenche la déformation)
  if (typeof injectStressPerturbation !== 'undefined') {
    injectStressPerturbation(cell, 0.6);
  }
  
  // Mise à jour visuelle immédiate
  let stressVal = (cell.stress || 0).toFixed(2);
  let scale = 1 + (cell.stress || 0) * 0.5;
  cell.mesh.scaling = new BABYLON.Vector3(scale, scale, scale);
  
  // Mettre à jour la couleur en fonction du stress
  let s = cell.stress || 0;
  let r = 0.78 + s * 0.22;
  let g = 0.14 - s * 0.04;
  cell.mat.diffuseColor = new BABYLON.Color3(r, g, 0.02);
  
  // Afficher les informations
  document.getElementById('cp-info').innerHTML = `Row ${cell.row+1} · Col ${cell.col+1} · Slice: ${cell.dep+1}/4<br>Stress: ${stressVal}`;
  document.getElementById('cell-panel').classList.remove('hide');
  
  // Mettre à jour le statut
  if (typeof updateStatusText !== 'undefined') updateStatusText();
  
  // Message de confirmation
  setStatus('info', `🎯 Cell selected - Stress: ${(cell.stress*100).toFixed(0)}% - Click "Propagate" to spread`);
}

// Désélectionne la cellule courante
function deselectCell() {
  if (SIM.selCell) {
    applyCellState(SIM.selCell, 'normal');
    SIM.selCell = null;
  }
  document.getElementById('cell-panel').classList.add('hide');
  if (typeof updateStatusText !== 'undefined') updateStatusText();
}

// Exposer les fonctions globalement
window.buildMantleGrid = buildMantleGrid;
window.applyCellState = applyCellState;
window.clickCell = clickCell;
window.deselectCell = deselectCell;