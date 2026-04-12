// src/main.js - Point d'entrée principal (version FEM)

function initScene() {
  const canvas = document.getElementById('renderCanvas');
  engine = new BABYLON.Engine(canvas, true, { antialias: true });
  scene = new BABYLON.Scene(engine);
  scene.clearColor = new BABYLON.Color4(.02, .03, .06, 1);
  
  initWireColors();
  setupCamera(canvas);
  setupLights();
  buildScene();
  buildMantleGrid();
  buildParticles();
  buildBuildings();
  
  // Initialiser les champs de stress APRÈS que les cellules existent
  if (typeof initStressFields !== 'undefined') {
    initStressFields();
  }
  
  createLayerGroups();
  attachAllToLayerCake();
  
  const planet = buildPlanetEarth();
  planetEarth = planet.earth;
  planetAtmosphere = planet.atmosphere;
  attachPlanetToGroup();
  
  createLatLongGrid(scene);
  
  if (typeof createPickerSphere !== 'undefined') createPickerSphere();
  
  // Par défaut : mode Layer Cake
  if (layerCakeGroup) layerCakeGroup.setEnabled(true);
  if (planetGroup) planetGroup.setEnabled(false);
  
  camera.alpha = -Math.PI * 0.28;
  camera.beta = Math.PI * 0.30;
  camera.radius = 26;
  camera.target = new BABYLON.Vector3(0, -.5, 0);
  
  quakeFlash = document.getElementById('quake-flash');
  
  let _rg, _mg;
  
  function renderLoop() {
    if (!_rg) { _rg = scene.getLightByName('rg'); _mg = scene.getLightByName('mg'); }
    const dt = Math.min(engine.getDeltaTime() * .001, .05);
    if (!SIM.running) return;
    SIM.t += dt;
    const cv = SIM.convection;
    
    // Animation des lumières
    if (_rg) _rg.intensity = 1.8 + Math.sin(SIM.t * 2) * .8 * cv;
    if (_mg) _mg.intensity = 3.5 + Math.sin(SIM.t * .7) * 1.0;
    
    // Mise à jour du champ de contrainte (FEM simplifiée)
    updateStressField(dt);
    
    // Gestion des particules (seulement en mode Layer Cake)
    if (psConv && SIM.viewMode === 'layer') psConv.emitRate = Math.round(14 + cv * 55);
    if (psRidge && SIM.viewMode === 'layer') psRidge.emitRate = Math.round(7 + cv * 35);
    
    // Mise à jour de l'affichage de la barre de stress
    const pct = Math.round(SIM.stress * 100);
    document.getElementById('sfl').style.width = pct + '%';
    document.getElementById('sfl').style.background = SIM.stress < .5 ? 'var(--accent)' : SIM.stress < .80 ? 'var(--warn)' : 'var(--eagle)';
    document.getElementById('val-stress').textContent = pct + '%';
    
    // Couleur des failles
    faultMats.forEach(fm => {
      const sr = Math.max(.15, SIM.stress * .95 + .05), sg = Math.max(0, .65 - SIM.stress * .65);
      fm.diffuseColor = new BABYLON.Color3(sr, sg, .06);
    });
    
    // Déclenchement d'un séisme si stress >= 90%
    if (SIM.stress >= 0.90 && !SIM.quakeActive && SIM.quakeCooldown <= 0 && SIM.viewMode === 'layer') {
      SIM.quakeActive = true;
      SIM.quakeTimer = 1.6;
      SIM.stress = Math.max(0, SIM.stress - 0.6);
      if (psQuake) { psQuake.start(); setTimeout(() => psQuake.stop(), 900); }
      if (quakeFlash) { quakeFlash.style.display = 'block'; setTimeout(() => { quakeFlash.style.display = 'none'; }, 500); }
      applyDominoEffect(SIM.selCell, 1.0);
      setStatus('warn', '⚠️ FAULT RUPTURE - DOMINO EFFECT ⚠️');
    }
    
    // Animation du séisme
    if (SIM.quakeActive) {
      SIM.quakeTimer -= dt;
      const shk = (Math.random() - .5) * 0.06;
      camera.target.x += shk;
      camera.target.y += shk * .3;
      if (SIM.quakeTimer <= 0) {
        SIM.quakeActive = false;
        SIM.quakeCooldown = 2.0;
        camera.target = new BABYLON.Vector3(0, -.5, 0);
        for (let building of buildings) building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
        setStatus('run', 'Running');
      }
    }
    
    // Angle de subduction
    if (SIM.viewMode === 'layer' && slabMeshes[0]) {
      slabMeshes[0].rotation.z = -Math.PI * (.12 + SIM.slabDensity * .20);
      slabMeshes[1].rotation.z = -Math.PI * (.16 + SIM.slabDensity * .26);
    }
    
    // Animation du panache mantellique
    if (SIM.plumeActive && SIM.viewMode === 'layer') {
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
    
    // Rotation de la planète
    if (SIM.viewMode === 'planet' && planetEarth) {
      // planetEarth.rotation.y += 0.002;
      // if (planetAtmosphere) planetAtmosphere.rotation.y += 0.002;
    }
  }
  
  scene.registerBeforeRender(renderLoop);
  engine.runRenderLoop(() => { scene.render(); });
  new ResizeObserver(() => engine.resize()).observe(document.getElementById('cv'));
}

// Démarrage
document.addEventListener('DOMContentLoaded', () => {
  initScene();
  wireControls();
  wireSplitter();
  wireTabs();
  setStatus('run', 'Running');
});