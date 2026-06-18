// transformations.js - Simulation FEM simplifiée avec propagation visible
// NE PAS redéclarer CONFIG (déjà dans config.js)

// Paramètres physiques augmentés pour une meilleure visibilité
const STRESS_PERTURBATION = 0.8;
const STRESS_DIFFUSIVITY_BASE = 0.45;
const NON_NEWTONIAN_EXP = 2;
const MAX_STRESS = 1.0;

// Récupère les voisins d'une cellule
function getNeighbors(cell) {
  const neighbors = [];
  const dirs = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]];
  for (let [dx,dy,dz] of dirs) {
    const nr = cell.row + dy;
    const nc = cell.col + dx;
    const nd = cell.dep + dz;
    if (nr >= 0 && nr < CONFIG.MROWS && nc >= 0 && nc < CONFIG.MCOLS && nd >= 0 && nd < CONFIG.MZDEPTHS) {
      const neighbor = cells.find(c => c.row === nr && c.col === nc && c.dep === nd);
      if (neighbor) neighbors.push(neighbor);
    }
  }
  return neighbors;
}

// Diffusion de contrainte avec effet visible
function computeStressDiffusion(dt) {
  let newStress = cells.map(c => c.stress || 0);
  let maxChange = 0;
  
  for (let i = 0; i < cells.length; i++) {
    let cell = cells[i];
    let neighbors = getNeighbors(cell);
    if (neighbors.length === 0) continue;
    let avgNeighbor = neighbors.reduce((sum, n) => sum + (n.stress || 0), 0) / neighbors.length;
    let stressMag = Math.max(0.01, cell.stress || 0);
    let diffusivity = STRESS_DIFFUSIVITY_BASE * Math.pow(stressMag, NON_NEWTONIAN_EXP - 1);
    let delta = diffusivity * dt * (avgNeighbor - (cell.stress || 0));
    let change = Math.abs(delta);
    if (change > maxChange) maxChange = change;
    newStress[i] = Math.min(MAX_STRESS, Math.max(0, (cell.stress || 0) + delta));
  }
  
  for (let i = 0; i < cells.length; i++) {
    let cell = cells[i];
    cell.stress = newStress[i];
    
    // Mise à jour visuelle immédiate
    let s = cell.stress;
    let scale = 1 + s * 0.5;
    cell.mesh.scaling = new BABYLON.Vector3(scale, scale, scale);
    
    // Couleur : orange (faible) → rouge (forte)
    let r = 0.78 + s * 0.22;
    let g = 0.14 - s * 0.04;
    let b = 0.02;
    cell.mat.diffuseColor = new BABYLON.Color3(r, g, b);
    
    if (s > 0.1) {
      cell.mat.emissiveColor = new BABYLON.Color3(s * 0.5, s * 0.15, 0);
    } else {
      cell.mat.emissiveColor = new BABYLON.Color3(0, 0, 0);
    }
    
    // Mettre à jour les bâtiments associés
    if (typeof updateBuildingsHeight !== 'undefined') {
      updateBuildingsHeight(cell);
    }
  }
  
  return maxChange;
}

// Forçages globaux
function applyGlobalForcing(dt) {
  for (let cell of cells) {
    // Slab pull
    if (cell.col >= CONFIG.MCOLS - 2 && cell.row === 0) {
      let intensity = SIM.slabDensity * 0.15;
      cell.stress = Math.min(MAX_STRESS, (cell.stress || 0) + intensity * dt);
    }
    // Ridge push
    if (Math.abs(cell.col - CONFIG.MCOLS/2) < 2 && cell.row === CONFIG.MROWS-1) {
      let intensity = SIM.convection * 0.12;
      cell.stress = Math.min(MAX_STRESS, (cell.stress || 0) + intensity * dt);
    }
    // Convection
    let convFactor = SIM.convection * 0.08 * Math.sin(cell.row * Math.PI / CONFIG.MROWS);
    cell.stress = Math.min(MAX_STRESS, (cell.stress || 0) + convFactor * dt);
  }
}

// Injection de perturbation
function injectStressPerturbation(cell, amount = STRESS_PERTURBATION) {
  if (!cell) return;
  cell.stress = Math.min(MAX_STRESS, (cell.stress || 0) + amount);
  
  // Mise à jour visuelle immédiate
  let s = cell.stress;
  let scale = 1 + s * 0.5;
  cell.mesh.scaling = new BABYLON.Vector3(scale, scale, scale);
  let r = 0.78 + s * 0.22;
  let g = 0.14 - s * 0.04;
  cell.mat.diffuseColor = new BABYLON.Color3(r, g, 0.02);
  
  setStatus('info', `💥 Stress: ${(s*100).toFixed(0)}% in cell (${cell.row+1},${cell.col+1},${cell.dep+1})`);
  
  // Vérifier si seuil de séisme local atteint
  if (cell.stress >= 0.9) {
    setStatus('warn', '⚠️ Local stress threshold reached!');
  }
}

// Propagation forcée (bouton Propagate)
function propagateFromSelectedCell(steps = 25) {
  if (!SIM.selCell) {
    setStatus('warn', 'No cell selected. Click on a cell first.');
    return;
  }
  
  setStatus('info', '🌀 Propagating stress...');
  
  // Injection forte
  injectStressPerturbation(SIM.selCell, 0.6);
  
  // Itérations de diffusion
  for (let i = 0; i < steps; i++) {
    applyGlobalForcing(0.1);
    let maxChange = computeStressDiffusion(0.1);
    
    // Afficher la progression
    if (i % 5 === 0) {
      let totalStress = cells.reduce((s,c) => s + (c.stress || 0), 0);
      let avg = totalStress / cells.length;
      setStatus('info', `🌀 Propagation step ${i+1}/${steps} - Avg stress: ${(avg*100).toFixed(0)}%`);
    }
  }
  
  if (typeof updateStatusText !== 'undefined') updateStatusText();
  
  let totalStress = cells.reduce((s,c) => s + (c.stress || 0), 0);
  let avgStress = totalStress / cells.length;
  let currentThreshold = SIM.quakeThreshold || 0.70;
  setStatus('info', `✅ Propagation complete! Avg stress: ${(avgStress*100).toFixed(0)}% (threshold: ${(currentThreshold*100).toFixed(0)}%)`);
  
  if (avgStress >= currentThreshold && !SIM.quakeActive) {
    triggerGlobalQuake();
  }
}

// Déclencher un séisme global
function triggerGlobalQuake() {
  SIM.quakeActive = true;
  SIM.quakeTimer = 1.6;
  setStatus('warn', '⚠️⚠️⚠️ GLOBAL EARTHQUAKE TRIGGERED ⚠️⚠️⚠️');
  
  // Effet domino sur tous les bâtiments
  for (let building of buildings) {
    let intensity = Math.random() * 0.8 + 0.3;
    let tiltAngle = intensity * 30;
    building.mesh.rotation = new BABYLON.Vector3(
      (Math.random() - 0.5) * tiltAngle * Math.PI / 180,
      0,
      (Math.random() - 0.5) * tiltAngle * Math.PI / 180
    );
    setTimeout(() => {
      if (building.mesh) building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
    }, 2000);
  }
}

// Mise à jour du champ de contrainte (appelée dans renderLoop)
function updateStressField(dt) {
  if (SIM.viewMode !== 'layer') return;
  applyGlobalForcing(dt);
  let maxChange = computeStressDiffusion(dt);
  
  let totalStress = cells.reduce((s, c) => s + (c.stress || 0), 0);
  let avgStress = totalStress / cells.length;  // ← Définir avgStress
  SIM.stress = avgStress;
  
  // Utiliser le seuil configurable
  let currentThreshold = SIM.quakeThreshold || 0.70;
  
  // Déclencher séisme si seuil atteint
  if (SIM.stress >= currentThreshold && !SIM.quakeActive && SIM.quakeCooldown <= 0) {
    triggerGlobalQuake();
  }
}

// Initialisation des champs de stress
function initStressFields() {
  if (!cells) return;
  for (let cell of cells) {
    cell.stress = 0;
  }
  console.log('Stress fields initialized for', cells.length, 'cells');
}

// =============================================================
// FONCTIONS DE DÉBOGAGE (uniquement pour la console)
// =============================================================
function debugStressState() {
  console.log("=== STRESS DEBUG ===");
  console.log("Global stress:", SIM.stress);
  console.log("Quake active:", SIM.quakeActive);
  console.log("Quake cooldown:", SIM.quakeCooldown);
  
  let stressedCells = cells.filter(c => (c.stress || 0) > 0.1);
  console.log(`Cells with stress > 0.1: ${stressedCells.length}/${cells.length}`);
  
  stressedCells.slice(0, 10).forEach(c => {
    console.log(`  Cell R${c.row+1}C${c.col+1}D${c.dep+1}: stress=${(c.stress||0).toFixed(3)}`);
  });
  
  if (stressedCells.length === 0) {
    console.warn("⚠️ No stressed cells found! Propagation may not be working.");
  }
}

function testStressInjection() {
  if (!SIM.selCell) {
    console.warn("No cell selected. Click on a cell first.");
    return;
  }
  console.log("=== TEST INJECTION ===");
  console.log("Before injection - stress:", SIM.selCell.stress);
  SIM.selCell.stress = 0.9;
  computeStressDiffusion(0.1);
  console.log("After injection - stress:", SIM.selCell.stress);
  debugStressState();
}

// Exposer les fonctions globalement
window.getNeighbors = getNeighbors;
window.injectStressPerturbation = injectStressPerturbation;
window.updateStressField = updateStressField;
window.initStressFields = initStressFields;
window.propagateFromSelectedCell = propagateFromSelectedCell;
window.debugStressState = debugStressState;
window.testStressInjection = testStressInjection;