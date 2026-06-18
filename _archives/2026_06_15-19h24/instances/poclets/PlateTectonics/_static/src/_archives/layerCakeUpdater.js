// src/layerCakeUpdater.js - Met à jour le Layer Cake selon les données géologiques

function updateLayerCakeFromGeology(geologyData) {
  console.log("Updating Layer Cake for:", geologyData);
  
  // Modifier les couleurs et épaisseurs selon le type de croûte
  switch(geologyData.crustType) {
    case 'continental':
      // Croûte continentale : plus épaisse, couleur marron
      updateCrustColor('#8B6914', '#CD9B1D');
      updateCrustThickness(1.2, 0.15);
      break;
      
    case 'oceanic':
      // Croûte océanique : plus fine, couleur bleu foncé
      updateCrustColor('#1a2d5a', '#0d40b3');
      updateCrustThickness(0.6, 0.10);
      break;
      
    case 'ridge':
      // Dorsale : croûte fine, rouge/orange (magma)
      updateCrustColor('#ff5533', '#ff8866');
      updateCrustThickness(0.4, 0.08);
      break;
      
    case 'subduction':
      // Zone de subduction : croûte épaisse, bleu/gris
      updateCrustColor('#2266cc', '#4488ee');
      updateCrustThickness(1.0, 0.12);
      break;
      
    case 'hotspot':
      // Point chaud : croûte normale, rouge vif
      updateCrustColor('#ff3300', '#ff6644');
      updateCrustThickness(0.8, 0.10);
      break;
  }
  
  // Modifier la température du manteau (couleur des cellules mantelliques)
  updateMantleTemperature(geologyData.mantleTemperature);
  
  // Modifier l'activité (émission de particules)
  updateVolcanicActivity(geologyData.activity === 'active');
}

function updateCrustColor(continentalColor, oceanicColor) {
  // Mettre à jour les matériaux des plaques
  for (let plate of continentalPlates) {
    if (plate.material) {
      plate.material.diffuseColor = BABYLON.Color3.FromHexString(continentalColor);
    }
  }
  for (let plate of oceanicPlates) {
    if (plate.material) {
      plate.material.diffuseColor = BABYLON.Color3.FromHexString(oceanicColor);
    }
  }
}

function updateCrustThickness(continentalHeight, oceanicHeight) {
  // Ajuster la hauteur des plaques
  for (let i = 0; i < continentalPlates.length; i++) {
    const plate = continentalPlates[i];
    const idx = i;
    const origY = 0.25 + (idx % 3) * 0.05;
    plate.position.y = origY + continentalHeight;
    plate.scaling.y = continentalHeight / 0.9;
  }
}

function updateMantleTemperature(temperature) {
  // La température influence la couleur des cellules mantelliques
  const heatFactor = (temperature - 1000) / 800; // 1000°C -> 0, 1800°C -> 1
  const r = 0.68 + heatFactor * 0.3;
  const g = 0.03 + heatFactor * 0.1;
  const b = 0.01;
  
  for (let cell of cells) {
    if (cell.mat) {
      cell.mat.diffuseColor = new BABYLON.Color3(r, g, b);
    }
  }
}

function updateVolcanicActivity(active) {
  // Activer/désactiver les particules volcaniques
  if (active) {
    if (psVol && !psVol.isStarted) psVol.start();
  } else {
    if (psVol && psVol.isStarted) psVol.stop();
  }
}

// Exposer la fonction globalement
window.updateLayerCakeFromGeology = updateLayerCakeFromGeology;