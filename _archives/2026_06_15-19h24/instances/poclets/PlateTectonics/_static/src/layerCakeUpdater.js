// src/layerCakeUpdater.js - Reconstruit le Layer Cake selon les données géologiques

function updateLayerCakeFromGeology(geologyData) {
  console.log("=== RECONSTRUCTING LAYER CAKE ===");
  console.log("Geology data:", geologyData);
  
  // Déterminer les paramètres selon le type de croûte
  let plateColor, mantleColor, oceanColor, buildingColor, crustHeight;
  
  switch(geologyData.crustType) {
    case 'continental':
      plateColor = new BABYLON.Color3(0.8, 0.5, 0.3);   // Marron/orange
      mantleColor = new BABYLON.Color3(0.9, 0.2, 0.1);   // Rouge vif
      oceanColor = new BABYLON.Color3(0.2, 0.4, 0.6);
      buildingColor = new BABYLON.Color3(0.9, 0.6, 0.3);
      crustHeight = 1.3;
      console.log("🔴 RECONSTRUCTING CONTINENTAL LAYER CAKE");
      break;
    case 'oceanic':
    default:
      plateColor = new BABYLON.Color3(0.2, 0.4, 0.7);     // Bleu moyen
      mantleColor = new BABYLON.Color3(0.6, 0.1, 0.05);  // Rouge-brun
      oceanColor = new BABYLON.Color3(0.1, 0.3, 0.5);
      buildingColor = new BABYLON.Color3(0.4, 0.4, 0.5);
      crustHeight = 0.8;
      console.log("🔵 RECONSTRUCTING OCEANIC LAYER CAKE");
      break;
  }
  
  // 1. Supprimer tous les éléments du Layer Cake
  console.log("  → Removing existing Layer Cake elements...");
  
  // Supprimer les plaques continentales
  if (typeof continentalPlates !== 'undefined') {
    for (let plate of continentalPlates) {
      if (plate) plate.dispose();
    }
    continentalPlates.length = 0;
  }
  
  // Supprimer les plaques océaniques
  if (typeof oceanicPlates !== 'undefined') {
    for (let plate of oceanicPlates) {
      if (plate) plate.dispose();
    }
    oceanicPlates.length = 0;
  }
  
  // Supprimer les bâtiments
  if (typeof buildings !== 'undefined') {
    for (let building of buildings) {
      if (building && building.mesh) building.mesh.dispose();
    }
    buildings.length = 0;
  }
  
  // Supprimer les cellules du manteau
  if (typeof cells !== 'undefined') {
    for (let cell of cells) {
      if (cell && cell.mesh) cell.mesh.dispose();
      if (cell && cell.wires) cell.wires.forEach(w => w.dispose());
    }
    cells.length = 0;
  }
  
  console.log("  → Existing elements removed");
  
  // 2. Recréer le Layer Cake avec les nouvelles couleurs
  console.log("  → Rebuilding Layer Cake with new colors...");
  
  // Recréer la grille mantellique
  if (typeof buildMantleGrid !== 'undefined') {
    buildMantleGrid();
  }
  
  // Recréer les bâtiments
  if (typeof buildBuildings !== 'undefined') {
    buildBuildings();
  }
  
  // 3. Appliquer les couleurs après reconstruction
  setTimeout(() => {
    // Appliquer les couleurs aux plaques continentales
    if (typeof continentalPlates !== 'undefined') {
      for (let plate of continentalPlates) {
        if (plate && plate.material) {
          plate.material.diffuseColor = plateColor;
          plate.material.emissiveColor = new BABYLON.Color3(plateColor.r * 0.2, plateColor.g * 0.05, 0);
          plate.scaling.y = crustHeight;
        }
      }
      console.log(`  → Colored ${continentalPlates.length} continental plates`);
    }
    
    // Appliquer les couleurs aux plaques océaniques
    if (typeof oceanicPlates !== 'undefined') {
      for (let plate of oceanicPlates) {
        if (plate && plate.material) {
          plate.material.diffuseColor = oceanColor;
        }
      }
      console.log(`  → Colored ${oceanicPlates.length} oceanic plates`);
    }
    
    // Appliquer les couleurs aux cellules du manteau
    if (typeof cells !== 'undefined') {
      for (let cell of cells) {
        if (cell && cell.mat) {
          cell.mat.diffuseColor = mantleColor;
          cell.mat.emissiveColor = new BABYLON.Color3(mantleColor.r * 0.3, mantleColor.g * 0.1, 0);
        }
      }
      console.log(`  → Colored ${cells.length} mantle cells`);
    }
    
    // Appliquer les couleurs aux bâtiments
    if (typeof buildings !== 'undefined') {
      for (let building of buildings) {
        if (building && building.mesh && building.mesh.material) {
          building.mesh.material.diffuseColor = buildingColor;
        }
      }
      console.log(`  → Colored ${buildings.length} buildings`);
    }
    
    setStatus('success', `🌋 Layer Cake rebuilt with ${geologyData.crustType} crust`);
    console.log("=== RECONSTRUCTION COMPLETE ===");
  }, 100);
}

window.updateLayerCakeFromGeology = updateLayerCakeFromGeology;