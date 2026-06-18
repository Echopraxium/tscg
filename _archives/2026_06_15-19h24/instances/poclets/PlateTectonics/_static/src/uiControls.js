// src/uiControls.js - Contrôles UI et gestion des modes d'affichage

let layerCakeGroup = null;
let planetGroup = null;
let gridVisible = false;

// Crée les groupes racines
function createLayerGroups() {
  if (!layerCakeGroup) {
    layerCakeGroup = new BABYLON.TransformNode("layerCakeGroup", scene);
  }
  if (!planetGroup) {
    planetGroup = new BABYLON.TransformNode("planetGroup", scene);
  }
}

// Attache TOUS les éléments du Layer Cake au groupe racine
function attachAllToLayerCake() {
  if (!layerCakeGroup) {
    layerCakeGroup = new BABYLON.TransformNode("layerCakeGroup", scene);
  }

  const attach = (obj) => {
    if (obj && obj.parent !== layerCakeGroup) obj.parent = layerCakeGroup;
  };

  for (let cell of cells) {
    if (cell && cell.mesh) attach(cell.mesh);
    if (cell && cell.wires) cell.wires.forEach(w => attach(w));
  }
  for (let b of buildings) if (b && b.mesh) attach(b.mesh);
  for (let p of continentalPlates) attach(p);
  for (let p of oceanicPlates) attach(p);
  for (let a of convArrows) attach(a);
  if (hotspotMesh) attach(hotspotMesh);
  for (let s of slabMeshes) attach(s);
  
  scene.meshes.forEach(mesh => {
    if (mesh === layerCakeGroup || mesh === planetGroup) return;
    if (mesh === planetEarth || mesh === planetAtmosphere) return;
    if (mesh.parent === planetGroup) return;
    if (mesh.parent !== layerCakeGroup) mesh.parent = layerCakeGroup;
  });
}

// Attache la planète et son atmosphère au groupe planète
function attachPlanetToGroup() {
  if (!planetGroup) {
    planetGroup = new BABYLON.TransformNode("planetGroup", scene);
  }
  if (planetEarth && planetEarth.parent !== planetGroup) {
    planetEarth.parent = planetGroup;
  }
  if (planetAtmosphere && planetAtmosphere.parent !== planetGroup) {
    planetAtmosphere.parent = planetGroup;
  }
}

// Change le mode d'affichage en activant/désactivant les groupes racines
// Dans uiControls.js, trouvez la fonction switchViewMode et remplacez-la par celle-ci :
function switchViewMode(mode) {
  SIM.viewMode = mode;
  
  if (mode === 'planet') {
    // ==================== MODE PLANÈTE ====================
    
    // 1. Désactiver le groupe du Layer Cake (le plus important !)
    if (layerCakeGroup) {
      layerCakeGroup.setEnabled(false);
      console.log("Layer Cake group DISABLED");
    }
    
    // 2. Activer le groupe de la planète
    if (planetGroup) {
      planetGroup.setEnabled(true);
      console.log("Planet group ENABLED");
    }
    
    // 3. Arrêter les particules
    if (psConv) psConv.stop();
    if (psRidge) psRidge.stop();
    if (psVol) psVol.stop();
    
    // 4. Désactiver TOUTES les cellules une par une (sécurité)
    if (typeof cells !== 'undefined' && cells) {
      for (let cell of cells) {
        if (cell && cell.mesh) {
          cell.mesh.setEnabled(false);
        }
        if (cell && cell.wires) {
          cell.wires.forEach(w => { if (w) w.setEnabled(false); });
        }
      }
      console.log(`  → Disabled ${cells.length} mantle cells`);
    }
    
    // 5. Désactiver les bâtiments
    if (typeof buildings !== 'undefined' && buildings) {
      for (let building of buildings) {
        if (building && building.mesh) building.mesh.setEnabled(false);
      }
    }
    
    // 6. Désactiver les plaques
    if (typeof continentalPlates !== 'undefined' && continentalPlates) {
      for (let plate of continentalPlates) {
        if (plate) plate.setEnabled(false);
      }
    }
    if (typeof oceanicPlates !== 'undefined' && oceanicPlates) {
      for (let plate of oceanicPlates) {
        if (plate) plate.setEnabled(false);
      }
    }
    
    // 7. Désactiver les flèches
    if (typeof convArrows !== 'undefined' && convArrows) {
      for (let arrow of convArrows) {
        if (arrow) arrow.setEnabled(false);
      }
    }
    
    // 8. Désactiver les murs statiques
    const staticNames = ['wF', 'wB', 'wL', 'wR', 'mantle', 'lithoBase', 'contTop', 
                         'trench', 'vc', 'ld', 'ch', 'rc', 'mt', 'snow'];
    for (let name of staticNames) {
      const mesh = scene.getMeshByName(name);
      if (mesh) mesh.setEnabled(false);
    }
    
    // 9. Ajuster la caméra
    camera.alpha = 0;
    camera.beta = Math.PI / 2.5;
    camera.radius = 14;
    camera.target = new BABYLON.Vector3(0, 0, 0);
    
    // 10. Réinitialiser le panneau d'info
    document.getElementById('cp-info').innerHTML = 'Click on the grid to select a cell';
    document.getElementById('cp-propagation').innerHTML = 'Latitude / Longitude';
    document.getElementById('cell-panel').classList.remove('hide');
    
    // 11. Cacher le bouton Sample
    const sampleBtn = document.getElementById('btn-sample');
    if (sampleBtn) sampleBtn.style.display = 'none';
    
    // 12. Créer la grille et le picker
    if (typeof createLatLongGrid !== 'undefined') {
      createLatLongGrid(6.08);
    }
    if (typeof createGridPicker !== 'undefined') {
      createGridPicker();
    }
    
    setStatus('info', '🌍 Planet Mode - Click on the grid to select a cell');
    
    // 13. Ajouter des marqueurs
    setTimeout(() => {
      if (typeof addSampleMarker !== 'undefined') {
        addSampleMarker(0, -30);
        addSampleMarker(45, -40);
        addSampleMarker(-30, -110);
        addSampleMarker(20, 70);
        addSampleMarker(65, -20);
      }
    }, 1000);
    
  } else {
    // ==================== MODE LAYER CAKE ====================
    
    // 1. Désactiver la planète
    if (planetGroup) planetGroup.setEnabled(false);
    
    // 2. Activer le groupe du Layer Cake
    if (layerCakeGroup) {
      layerCakeGroup.setEnabled(true);
      console.log("Layer Cake group ENABLED");
    }
    
    // 3. Redémarrer les particules
    if (psConv) psConv.start();
    if (psRidge) psRidge.start();
    if (psVol) psVol.start();
    
    // 4. Réactiver TOUTES les cellules
    if (typeof cells !== 'undefined' && cells) {
      for (let cell of cells) {
        if (cell && cell.mesh) cell.mesh.setEnabled(true);
        if (cell && cell.wires) cell.wires.forEach(w => { if (w) w.setEnabled(true); });
      }
      console.log(`  → Enabled ${cells.length} mantle cells`);
    }
    
    // 5. Réactiver les bâtiments
    if (typeof buildings !== 'undefined' && buildings) {
      for (let building of buildings) {
        if (building && building.mesh) building.mesh.setEnabled(true);
      }
    }
    
    // 6. Réactiver les plaques
    if (typeof continentalPlates !== 'undefined' && continentalPlates) {
      for (let plate of continentalPlates) {
        if (plate) plate.setEnabled(true);
      }
    }
    if (typeof oceanicPlates !== 'undefined' && oceanicPlates) {
      for (let plate of oceanicPlates) {
        if (plate) plate.setEnabled(true);
      }
    }
    
    // 7. Réactiver les flèches
    if (typeof convArrows !== 'undefined' && convArrows) {
      for (let arrow of convArrows) {
        if (arrow) arrow.setEnabled(true);
      }
    }
    
    // 8. Réactiver les murs statiques
    const staticNames = ['wF', 'wB', 'wL', 'wR', 'mantle', 'lithoBase', 'contTop', 
                         'trench', 'vc', 'ld', 'ch', 'rc', 'mt', 'snow'];
    for (let name of staticNames) {
      const mesh = scene.getMeshByName(name);
      if (mesh) mesh.setEnabled(true);
    }
    
    // 9. Ajuster la caméra
    camera.alpha = -Math.PI * 0.28;
    camera.beta = Math.PI * 0.30;
    camera.radius = 26;
    camera.target = new BABYLON.Vector3(0, -0.5, 0);
    
    // 10. Réinitialiser le panneau d'info
    if (SIM.selCell) {
      let stressVal = (SIM.selCell.stress || 0).toFixed(2);
      document.getElementById('cp-info').innerHTML = `Row ${SIM.selCell.row+1} · Col ${SIM.selCell.col+1} · Slice: ${SIM.selCell.dep+1}/4<br>Stress: ${stressVal}`;
      document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength*100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`;
    } else {
      document.getElementById('cp-info').innerHTML = 'No cell selected';
      document.getElementById('cp-propagation').innerHTML = 'Click on a cell to select';
    }
    document.getElementById('cell-panel').classList.remove('hide');
    
    // 11. Cacher le bouton Sample
    const sampleBtn = document.getElementById('btn-sample');
    if (sampleBtn) sampleBtn.style.display = 'none';
    
    // 12. Nettoyer les marqueurs
    if (typeof clearSampleMarkers !== 'undefined') clearSampleMarkers();
    if (typeof clearGridSelection !== 'undefined') clearGridSelection();
    
    setStatus('info', '🍰 Layer Cake Mode');
  }
  
  // Mettre à jour le texte du panneau de contrôle
  updateStatusText();
  
  setTimeout(() => { 
    if (!SIM.quakeActive) setStatus('run', 'Running'); 
  }, 1500);
}

// Met à jour le texte dans le panneau de contrôle
// Dans uiControls.js, modifier updateStatusText :
function updateStatusText() {
  const statusDiv = document.getElementById('xyz-status');
  if (!statusDiv) return;
  
  if (SIM.viewMode === 'planet') {
    // Récupérer la cellule sélectionnée depuis planet.js
    if (typeof window.getSelectedGridCell !== 'undefined') {
      const selected = window.getSelectedGridCell();
      if (selected) {
        statusDiv.innerHTML = `Planet: ${selected.lat}°, ${selected.lon}° selected`;
        return;
      }
    }
    statusDiv.innerHTML = 'Click on a grid cell to select';
  } else {
    if (SIM.selCell) {
      let stressVal = (SIM.selCell.stress || 0).toFixed(2);
      statusDiv.innerHTML = `Selected: R${SIM.selCell.row+1} C${SIM.selCell.col+1} D${SIM.selCell.dep+1} | Stress: ${stressVal}`;
    } else {
      statusDiv.innerHTML = 'No cell selected — click on any cell face';
    }
  }
}

// Charge le README dans l'onglet Description
function loadReadme() {
  fetch('../M0_PlateTectonics_README.md')
    .then(response => {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.text();
    })
    .then(md => {
      document.getElementById('panel-desc').innerHTML = `<pre style="white-space:pre-wrap; font-family:monospace; font-size:11px;">${md}</pre>`;
    })
    .catch(err => {
      console.warn('README non trouvé:', err);
      document.getElementById('panel-desc').innerHTML = '<p>README.md introuvable.</p>';
    });
}

// --------------------------------------------------------------
// wireControls : tous les écouteurs d'événements de l'interface
// --------------------------------------------------------------
function wireControls() {
  // Play/Pause
  document.getElementById('btn-play').addEventListener('click', () => {
    SIM.running = !SIM.running;
    const b = document.getElementById('btn-play');
    b.textContent = SIM.running ? '⏸ Pause' : '▶ Play';
    b.classList.toggle('active', SIM.running);
    if (SIM.running && SIM.viewMode === 'layer') {
      if (psConv) psConv.start();
      if (psRidge) psRidge.start();
      if (psVol) psVol.start();
    } else {
      if (psConv) psConv.stop();
      if (psRidge) psRidge.stop();
      if (psVol) psVol.stop();
    }
  });

  // Reset
  document.getElementById('btn-reset').addEventListener('click', () => {
    SIM.running = true; SIM.t = 0; SIM.stress = 0; SIM.quakeActive = false; SIM.quakeCooldown = 0;
    SIM.wilsonActive = false; SIM.plumeActive = false;
    SIM.convection = 0.5; SIM.slabDensity = 0.6; SIM.asymmetry = 0;
    SIM.propagationStrength = 0.8; SIM.propagationRadius = 1.88;
    SIM.quakeThreshold = 0.70;
    
    document.getElementById('sl-conv').value = 0.5; document.getElementById('val-conv').textContent = '50%';
    document.getElementById('sl-slab').value = 0.6; document.getElementById('val-slab').textContent = '60%';
    document.getElementById('sl-asym').value = 0; document.getElementById('val-asym').textContent = '0';
    document.getElementById('sl-propagation').value = 0.8; document.getElementById('val-propagation').textContent = '80%';
    document.getElementById('sl-radius').value = 1.88; document.getElementById('val-radius').textContent = '1.88';
    
    const thresholdSlider = document.getElementById('sl-threshold');
    if (thresholdSlider) {
      thresholdSlider.value = 0.70;
      document.getElementById('val-threshold').textContent = '70%';
    }
    
    if (SIM.viewMode === 'layer') {
      camera.alpha = -Math.PI * 0.28; camera.beta = Math.PI * 0.30; camera.radius = 26; camera.target = new BABYLON.Vector3(0, -0.5, 0);
      if (hotspotMesh) hotspotMesh.isVisible = false;
      if (psPlume && psPlume.isStarted()) psPlume.stop();
      for (let cell of cells) {
        const idx = cells.indexOf(cell);
        if (origCellPositions[idx]) cell.mesh.position = new BABYLON.Vector3(origCellPositions[idx].x, origCellPositions[idx].y, origCellPositions[idx].z);
        cell.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
        cell.mesh.scaling = new BABYLON.Vector3(1, 1, 1);
        cell.stress = 0;
        cell.volume = { x: 0, y: 0, z: 0 }; cell.trans = { x: 0, y: 0, z: 0 }; cell.rot = { alpha: 0, phi: 0, omega: 0 };
        applyCellState(cell, 'normal');
      }
      for (let building of buildings) {
        building.mesh.position.y = building.originalY;
        building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
      }
      if (SIM.selCell) { applyCellState(SIM.selCell, 'normal'); SIM.selCell = null; }
    } else {
      camera.alpha = 0; camera.beta = Math.PI / 2.5; camera.radius = 14; camera.target = new BABYLON.Vector3(0, 0, 0);
    }
    SIM.hovCell = null;
    document.getElementById('cell-panel').classList.add('hide');
    updateAllDisplays();
    updateStatusText();
    document.getElementById('btn-play').textContent = '⏸ Pause';
    document.getElementById('btn-play').classList.add('active');
    document.getElementById('btn-wilson').classList.remove('active');
    if (psConv && !psConv.isStarted() && SIM.viewMode === 'layer') { psConv.start(); psRidge.start(); psVol.start(); }
    setStatus('run', 'Running');
  });

  // Wilson Cycle
  document.getElementById('btn-wilson').addEventListener('click', () => {
    if (SIM.viewMode !== 'layer') {
      setStatus('warn', 'Wilson Cycle only available in Layer Cake mode.');
      return;
    }
    SIM.wilsonActive = !SIM.wilsonActive;
    document.getElementById('btn-wilson').classList.toggle('active', SIM.wilsonActive);
    setStatus('info', SIM.wilsonActive ? 'Wilson Cycle...' : '');
  });

  // Legend toggle
  document.getElementById('btn-labels').addEventListener('click', () => {
    SIM.showLegend = !SIM.showLegend;
    document.getElementById('legend-panel').style.display = SIM.showLegend ? 'block' : 'none';
    document.getElementById('btn-labels').classList.toggle('active', SIM.showLegend);
  });

  // Sliders
  document.getElementById('sl-conv').addEventListener('input', e => { SIM.convection = parseFloat(e.target.value); document.getElementById('val-conv').textContent = Math.round(SIM.convection * 100) + '%'; });
  document.getElementById('sl-slab').addEventListener('input', e => { SIM.slabDensity = parseFloat(e.target.value); document.getElementById('val-slab').textContent = Math.round(SIM.slabDensity * 100) + '%'; });
  document.getElementById('sl-asym').addEventListener('input', e => { SIM.asymmetry = parseFloat(e.target.value); document.getElementById('val-asym').textContent = (SIM.asymmetry >= 0 ? '+' : '') + SIM.asymmetry.toFixed(2); });
  document.getElementById('sl-propagation').addEventListener('input', e => { SIM.propagationStrength = parseFloat(e.target.value); document.getElementById('val-propagation').textContent = Math.round(SIM.propagationStrength * 100) + '%'; if (SIM.viewMode === 'layer') document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength * 100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`; });
  document.getElementById('sl-radius').addEventListener('input', e => { SIM.propagationRadius = parseFloat(e.target.value); document.getElementById('val-radius').textContent = SIM.propagationRadius.toFixed(1); if (SIM.viewMode === 'layer') document.getElementById('cp-propagation').innerHTML = `Propagation: ${Math.round(SIM.propagationStrength * 100)}% | Radius: ${SIM.propagationRadius.toFixed(1)}`; });

  const thresholdSlider = document.getElementById('sl-threshold');
  const thresholdVal = document.getElementById('val-threshold');
  if (thresholdSlider) {
    thresholdSlider.addEventListener('input', (e) => {
      SIM.quakeThreshold = parseFloat(e.target.value);
      thresholdVal.textContent = Math.round(SIM.quakeThreshold * 100) + '%';
      setStatus('info', `⚠️ Quake threshold set to ${Math.round(SIM.quakeThreshold * 100)}%`);
    });
  }

  // View mode buttons
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

  // Bouton Propagate Stress
  const propagateBtn = document.getElementById('btn-propagate');
  if (propagateBtn) {
    propagateBtn.addEventListener('click', () => {
      if (SIM.viewMode !== 'layer') {
        setStatus('warn', 'Propagation only available in Layer Cake mode.');
        return;
      }
      if (typeof propagateFromSelectedCell !== 'undefined') {
        propagateFromSelectedCell(25);
      } else {
        setStatus('warn', 'propagateFromSelectedCell not defined.');
      }
    });
  }

  // Bouton Toggle Grid
  const gridBtn = document.getElementById('btn-grid');
  if (gridBtn) {
    gridBtn.addEventListener('click', () => {
      if (SIM.viewMode !== 'planet') {
        setStatus('warn', 'Grid only available in Planet Mode');
        return;
      }
      if (typeof toggleGrid !== 'undefined') {
        gridVisible = !gridVisible;
        toggleGrid(gridVisible);
        setStatus('info', gridVisible ? 'Grid ON' : 'Grid OFF');
      }
    });
  }

  document.getElementById('btn-play').classList.add('active');
  document.getElementById('btn-labels').classList.add('active');
}

// Redimensionnement du splitter
function wireSplitter() {
  const sp = document.getElementById('sp'), app = document.getElementById('app');
  let drag = false, sx = 0, sw = 0;
  sp.addEventListener('mousedown', e => { drag = true; sx = e.clientX; sw = document.getElementById('sb').getBoundingClientRect().width; sp.classList.add('drag'); document.body.style.cursor = 'col-resize'; e.preventDefault(); });
  document.addEventListener('mousemove', e => { if (!drag) return; app.style.setProperty('--sidebar-w', Math.max(180, Math.min(640, sw + (sx - e.clientX))) + 'px'); });
  document.addEventListener('mouseup', () => { drag = false; sp.classList.remove('drag'); document.body.style.cursor = ''; });
}

// Onglets de la barre latérale
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

// Exposer les fonctions globalement
window.createLayerGroups = createLayerGroups;
window.attachAllToLayerCake = attachAllToLayerCake;
window.attachPlanetToGroup = attachPlanetToGroup;
window.switchViewMode = switchViewMode;
window.wireControls = wireControls;
window.wireSplitter = wireSplitter;
window.wireTabs = wireTabs;
window.updateStatusText = updateStatusText;
window.loadReadme = loadReadme;