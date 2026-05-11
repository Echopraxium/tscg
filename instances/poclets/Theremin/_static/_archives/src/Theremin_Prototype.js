/* Theremin Prototype - JavaScript
 * Author: Echopraxium with the collaboration of Claude AI
 * Framework: TSCG
 * 
 * This prototype simulates a Theremin using:
 * - BabylonJS for 3D visualization
 * - Web Audio API for sound synthesis
 * - Interactive 3D cursors for pitch and volume control
 */

/* globals BABYLON */

// ======================================
// Global State
// ======================================
let engine, scene, camera;
let thereminBody, pitchAntenna, volumeAntenna;
let pitchCursor, volumeCursor;
let groundGrid;

// Electromagnetic field visualization
let pitchFieldMesh, volumeFieldMesh;
let fieldsVisible = true;

// Demo mode
let demoMode = false;
let demoSequence = [];
let demoCurrentNote = 0;
let demoStartTime = 0;

// Audio system
let audioContext, oscillator, gainNode, reverbNode;
let isAudioInitialized = false;
let isPlaying = false;

// Cursor dragging state
let isDraggingPitch = false;
let isDraggingVolume = false;
let dragStartY = 0;
let dragStartCursorY = 0;

// Theremin parameters
const PITCH_MIN = 200;  // Hz (low G3)
const PITCH_MAX = 1200; // Hz (high D6)
const PITCH_CURSOR_MIN_Y = 0.5;
const PITCH_CURSOR_MAX_Y = 4.0;

const VOLUME_MIN = 0;
const VOLUME_MAX = 0.8;
const VOLUME_CURSOR_MIN_Y = 0.5;
const VOLUME_CURSOR_MAX_Y = 3.5;

let currentPitch = 440; // A4
let currentVolume = 0.5;

// ======================================
// Initialization
// ======================================
document.addEventListener('DOMContentLoaded', init);

function init() {
  console.log('Initializing Theremin Prototype...');
  
  setupBabylonJS();
  setupUI();
  setupAudioSystem();
  
  console.log('Initialization complete!');
}

// ======================================
// BabylonJS Setup
// ======================================
function setupBabylonJS() {
  const canvas = document.getElementById('canvas-main');
  engine = new BABYLON.Engine(canvas, true);
  
  scene = new BABYLON.Scene(engine);
  scene.clearColor = new BABYLON.Color3(0.05, 0.05, 0.08);
  
  // Camera (ArcRotateCamera)
  camera = new BABYLON.ArcRotateCamera(
    'camera',
    -Math.PI / 2,  // alpha (horizontal rotation)
    Math.PI / 3,   // beta (vertical angle)
    12,            // radius (distance)
    new BABYLON.Vector3(0, 2, 0),  // target
    scene
  );
  camera.attachControl(canvas, true);
  camera.lowerRadiusLimit = 5;
  camera.upperRadiusLimit = 20;
  camera.lowerBetaLimit = 0.1;
  camera.upperBetaLimit = Math.PI / 2;
  
  // Lights
  const hemisphericLight = new BABYLON.HemisphericLight(
    'hemiLight',
    new BABYLON.Vector3(0, 1, 0),
    scene
  );
  hemisphericLight.intensity = 0.6;
  
  const directionalLight = new BABYLON.DirectionalLight(
    'dirLight',
    new BABYLON.Vector3(-1, -2, -1),
    scene
  );
  directionalLight.intensity = 0.5;
  
  // Ground grid
  createGroundGrid();
  
  // Theremin model
  createThereminModel();
  
  // Interactive cursors
  createPitchCursor();
  createVolumeCursor();
  
  // Electromagnetic field visualization
  createElectromagneticFields();
  
  // Setup picking
  setupPicking();
  
  // Render loop
  engine.runRenderLoop(() => {
    updateFieldIntensity();
    updateDemoMode();
    scene.render();
  });
  
  // Resize handler
  window.addEventListener('resize', () => {
    engine.resize();
  });
}

function createGroundGrid() {
  groundGrid = BABYLON.MeshBuilder.CreateGround(
    'ground',
    { width: 20, height: 20, subdivisions: 20 },
    scene
  );
  
  const gridMaterial = new BABYLON.StandardMaterial('gridMat', scene);
  gridMaterial.wireframe = true;
  gridMaterial.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.1);
  gridMaterial.alpha = 0.3;
  groundGrid.material = gridMaterial;
  groundGrid.position.y = 0;
}

function createThereminModel() {
  // Base platform (elegant wood base - longer and lower profile)
  const base = BABYLON.MeshBuilder.CreateBox(
    'base',
    { width: 4.5, height: 0.12, depth: 2.2 },
    scene
  );
  base.position.y = 0.06;
  
  const baseMat = new BABYLON.StandardMaterial('baseMat', scene);
  // Rich cherry/mahogany wood tone
  baseMat.diffuseColor = new BABYLON.Color3(0.48, 0.28, 0.18);
  baseMat.specularColor = new BABYLON.Color3(0.35, 0.2, 0.15);
  baseMat.specularPower = 64; // Semi-gloss wood finish
  base.material = baseMat;
  
  // Main body (control unit - professional cabinet)
  thereminBody = BABYLON.MeshBuilder.CreateBox(
    'body',
    { width: 4.0, height: 0.7, depth: 2.0 },
    scene
  );
  thereminBody.position = new BABYLON.Vector3(0, 0.47, 0);
  
  const bodyMat = new BABYLON.StandardMaterial('bodyMat', scene);
  // Warm natural wood (maple/birch tone)
  bodyMat.diffuseColor = new BABYLON.Color3(0.65, 0.48, 0.32);
  bodyMat.specularColor = new BABYLON.Color3(0.45, 0.35, 0.25);
  bodyMat.specularPower = 60;
  thereminBody.material = bodyMat;
  
  // Front control panel (black anodized aluminum look)
  const panel = BABYLON.MeshBuilder.CreateBox(
    'panel',
    { width: 3.6, height: 0.55, depth: 0.08 },
    scene
  );
  panel.position = new BABYLON.Vector3(0, 0.47, 1.04);
  
  const panelMat = new BABYLON.StandardMaterial('panelMat', scene);
  panelMat.diffuseColor = new BABYLON.Color3(0.08, 0.08, 0.1);
  panelMat.specularColor = new BABYLON.Color3(0.25, 0.25, 0.28);
  panelMat.specularPower = 96; // Brushed metal look
  panel.material = panelMat;
  
  // Control knobs (6 knobs - professional layout)
  const knobMat = new BABYLON.StandardMaterial('knobMat', scene);
  knobMat.diffuseColor = new BABYLON.Color3(0.25, 0.25, 0.28);
  knobMat.specularColor = new BABYLON.Color3(0.5, 0.5, 0.5);
  knobMat.specularPower = 80;
  
  for (let i = 0; i < 6; i++) {
    const knob = BABYLON.MeshBuilder.CreateCylinder(
      `knob_${i}`,
      { height: 0.12, diameterTop: 0.14, diameterBottom: 0.18 },
      scene
    );
    knob.position = new BABYLON.Vector3(
      -1.5 + (i * 0.6),
      0.47,
      1.12
    );
    knob.rotation.x = Math.PI / 2;
    knob.material = knobMat;
    
    // Pointer line on knob
    const pointer = BABYLON.MeshBuilder.CreateBox(
      `pointer_${i}`,
      { width: 0.02, height: 0.06, depth: 0.01 },
      scene
    );
    pointer.position = new BABYLON.Vector3(
      -1.5 + (i * 0.6),
      0.47,
      1.18
    );
    
    const pointerMat = new BABYLON.StandardMaterial(`pointerMat_${i}`, scene);
    pointerMat.emissiveColor = new BABYLON.Color3(0.9, 0.9, 0.9);
    pointer.material = pointerMat;
  }
  
  // LED indicators above knobs
  for (let i = 0; i < 6; i++) {
    const led = BABYLON.MeshBuilder.CreateSphere(
      `led_${i}`,
      { diameter: 0.06 },
      scene
    );
    led.position = new BABYLON.Vector3(
      -1.5 + (i * 0.6),
      0.68,
      1.08
    );
    
    const ledMat = new BABYLON.StandardMaterial(`ledMat_${i}`, scene);
    ledMat.emissiveColor = new BABYLON.Color3(0.9, 0.3, 0.2); // Warm red glow
    ledMat.alpha = 0.9;
    led.material = ledMat;
  }
  
  // Rubber feet (4 corners)
  const footPositions = [
    [-2.1, 0, 1.0],
    [2.1, 0, 1.0],
    [-2.1, 0, -1.0],
    [2.1, 0, -1.0]
  ];
  
  const footMat = new BABYLON.StandardMaterial('footMat', scene);
  footMat.diffuseColor = new BABYLON.Color3(0.12, 0.12, 0.12);
  
  footPositions.forEach((pos, i) => {
    const foot = BABYLON.MeshBuilder.CreateCylinder(
      `foot_${i}`,
      { height: 0.06, diameter: 0.25 },
      scene
    );
    foot.position = new BABYLON.Vector3(pos[0], pos[1], pos[2]);
    foot.material = footMat;
  });
  
  // Pitch antenna (right, vertical - polished chrome)
  pitchAntenna = BABYLON.MeshBuilder.CreateCylinder(
    'pitchAntenna',
    { height: 4.2, diameter: 0.055 },
    scene
  );
  pitchAntenna.position = new BABYLON.Vector3(1.8, 2.54, 0);
  
  const chromeMat = new BABYLON.StandardMaterial('chromeMat', scene);
  chromeMat.diffuseColor = new BABYLON.Color3(0.88, 0.88, 0.92);
  chromeMat.specularColor = new BABYLON.Color3(1, 1, 1);
  chromeMat.specularPower = 256; // Mirror-like chrome
  pitchAntenna.material = chromeMat;
  
  // Pitch antenna ball tip (decorative)
  const pitchTip = BABYLON.MeshBuilder.CreateSphere(
    'pitchTip',
    { diameter: 0.18 },
    scene
  );
  pitchTip.position = new BABYLON.Vector3(1.8, 4.64, 0);
  pitchTip.material = chromeMat;
  
  // Pitch antenna base mount (tapered cylinder)
  const pitchMount = BABYLON.MeshBuilder.CreateCylinder(
    'pitchMount',
    { height: 0.22, diameterTop: 0.14, diameterBottom: 0.22 },
    scene
  );
  pitchMount.position = new BABYLON.Vector3(1.8, 0.93, 0);
  
  const mountMat = new BABYLON.StandardMaterial('mountMat', scene);
  mountMat.diffuseColor = new BABYLON.Color3(0.18, 0.18, 0.2);
  mountMat.specularColor = new BABYLON.Color3(0.4, 0.4, 0.42);
  mountMat.specularPower = 90;
  pitchMount.material = mountMat;
  
  // Volume antenna (left, horizontal loop - chrome)
  volumeAntenna = createProfessionalLoopAntenna();
  
  // Volume antenna mount
  const volumeMount = BABYLON.MeshBuilder.CreateCylinder(
    'volumeMount',
    { height: 0.22, diameterTop: 0.14, diameterBottom: 0.22 },
    scene
  );
  volumeMount.position = new BABYLON.Vector3(-1.8, 0.93, 0);
  volumeMount.material = mountMat;
}

function createProfessionalLoopAntenna() {
  // Professional loop antenna with chrome finish
  const loop = BABYLON.MeshBuilder.CreateTorus(
    'volumeAntenna',
    { diameter: 1.6, thickness: 0.05, tessellation: 64 },
    scene
  );
  loop.position = new BABYLON.Vector3(-1.8, 2.3, 0);
  loop.rotation.z = Math.PI / 2;
  
  const chromeMat = new BABYLON.StandardMaterial('loopChromeMat', scene);
  chromeMat.diffuseColor = new BABYLON.Color3(0.88, 0.88, 0.92);
  chromeMat.specularColor = new BABYLON.Color3(1, 1, 1);
  chromeMat.specularPower = 256; // Mirror chrome
  loop.material = chromeMat;
  
  return loop;
}

function createPitchCursor() {
  // Green sphere for pitch control
  pitchCursor = BABYLON.MeshBuilder.CreateSphere(
    'pitchCursor',
    { diameter: 0.4 },
    scene
  );
  pitchCursor.position = new BABYLON.Vector3(
    1.8, // Aligned with new pitch antenna position
    2.5, // Middle height
    0.8  // In front
  );
  
  const pitchCursorMat = new BABYLON.StandardMaterial('pitchCursorMat', scene);
  pitchCursorMat.diffuseColor = new BABYLON.Color3(0.3, 0.8, 0.3);
  pitchCursorMat.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.1);
  pitchCursorMat.specularColor = new BABYLON.Color3(0.5, 0.5, 0.5);
  pitchCursor.material = pitchCursorMat;
  
  // Add glow layer effect
  const gl = new BABYLON.GlowLayer('pitchGlow', scene);
  gl.addIncludedOnlyMesh(pitchCursor);
  gl.intensity = 0.5;
  
  // Visual guide line (dashed, yellow, thicker)
  createDashedGuideLine(
    'pitchGuideLine',
    new BABYLON.Vector3(1.8, 0, 0.8),
    PITCH_CURSOR_MIN_Y,
    PITCH_CURSOR_MAX_Y,
    new BABYLON.Color3(1.0, 0.9, 0.0) // Yellow
  );
}

function createVolumeCursor() {
  // Blue cylinder for volume control
  volumeCursor = BABYLON.MeshBuilder.CreateCylinder(
    'volumeCursor',
    { height: 0.3, diameter: 0.5 },
    scene
  );
  volumeCursor.position = new BABYLON.Vector3(
    -1.8, // Aligned with new volume antenna position
    2.0,  // Middle height
    0.8   // In front
  );
  
  const volumeCursorMat = new BABYLON.StandardMaterial('volumeCursorMat', scene);
  volumeCursorMat.diffuseColor = new BABYLON.Color3(0.2, 0.6, 0.9);
  volumeCursorMat.emissiveColor = new BABYLON.Color3(0.1, 0.2, 0.3);
  volumeCursorMat.specularColor = new BABYLON.Color3(0.5, 0.5, 0.5);
  volumeCursor.material = volumeCursorMat;
  
  // Add glow layer effect
  const gl = new BABYLON.GlowLayer('volumeGlow', scene);
  gl.addIncludedOnlyMesh(volumeCursor);
  gl.intensity = 0.5;
  
  // Visual guide line (dashed, yellow, thicker)
  createDashedGuideLine(
    'volumeGuideLine',
    new BABYLON.Vector3(-1.8, 0, 0.8),
    VOLUME_CURSOR_MIN_Y,
    VOLUME_CURSOR_MAX_Y,
    new BABYLON.Color3(1.0, 0.9, 0.0) // Yellow
  );
}

// Helper function to create dashed guide lines
function createDashedGuideLine(name, basePosition, minY, maxY, color) {
  const totalHeight = maxY - minY;
  const dashLength = 0.15;   // Length of each dash
  const gapLength = 0.10;    // Gap between dashes
  const diameter = 0.03;     // Thickness (reduced 50% from 0.06)
  
  const segmentLength = dashLength + gapLength;
  const numSegments = Math.floor(totalHeight / segmentLength);
  
  for (let i = 0; i < numSegments; i++) {
    const segment = BABYLON.MeshBuilder.CreateCylinder(
      `${name}_segment_${i}`,
      { height: dashLength, diameter: diameter },
      scene
    );
    
    const yPos = minY + (i * segmentLength) + (dashLength / 2);
    segment.position = new BABYLON.Vector3(
      basePosition.x,
      yPos,
      basePosition.z
    );
    
    const segmentMat = new BABYLON.StandardMaterial(`${name}_mat_${i}`, scene);
    segmentMat.diffuseColor = color;
    segmentMat.emissiveColor = color.scale(0.3); // Slight glow
    segmentMat.alpha = 0.8;
    segment.material = segmentMat;
  }
}

// ======================================
// Electromagnetic Field Visualization
// ======================================
function createElectromagneticFields() {
  // Pitch antenna field (vertical, green)
  createPitchField();
  
  // Volume antenna field (horizontal loop, blue)
  createVolumeField();
}

function createPitchField() {
  // Volumetric field mesh (ellipsoid around antenna)
  pitchFieldMesh = BABYLON.MeshBuilder.CreateSphere(
    'pitchFieldMesh',
    { diameterX: 2.5, diameterY: 4.0, diameterZ: 2.5, segments: 16 },
    scene
  );
  pitchFieldMesh.position = new BABYLON.Vector3(1.8, 2.3, 0);
  
  const pitchFieldMat = new BABYLON.StandardMaterial('pitchFieldMat', scene);
  pitchFieldMat.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
  pitchFieldMat.emissiveColor = new BABYLON.Color3(0.1, 0.4, 0.1);
  pitchFieldMat.alpha = 0.15;
  pitchFieldMat.wireframe = false;
  pitchFieldMesh.material = pitchFieldMat;
  
  // CRITICAL: Disable picking to avoid blocking cursor selection
  pitchFieldMesh.isPickable = false;
  
  // Ellipsoidal field lines (arcs) instead of particles
  createEllipsoidalFieldLines(
    'pitchFieldLines',
    pitchAntenna.position,
    2.5, 4.0, 2.5, // radiusX, radiusY, radiusZ
    new BABYLON.Color3(0.2, 0.8, 0.2),
    12 // number of arc lines
  );
}

function createVolumeField() {
  // Volumetric field mesh (torus around loop antenna)
  volumeFieldMesh = BABYLON.MeshBuilder.CreateTorus(
    'volumeFieldMesh',
    { diameter: 2.5, thickness: 0.8, tessellation: 24 },
    scene
  );
  volumeFieldMesh.position = new BABYLON.Vector3(-1.8, 2.3, 0);
  volumeFieldMesh.rotation.z = Math.PI / 2;
  
  const volumeFieldMat = new BABYLON.StandardMaterial('volumeFieldMat', scene);
  volumeFieldMat.diffuseColor = new BABYLON.Color3(0.2, 0.6, 0.9);
  volumeFieldMat.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.5);
  volumeFieldMat.alpha = 0.15;
  volumeFieldMat.wireframe = false;
  volumeFieldMesh.material = volumeFieldMat;
  
  // CRITICAL: Disable picking to avoid blocking cursor selection
  volumeFieldMesh.isPickable = false;
  
  // Toroidal field lines (arcs) instead of particles
  createToroidalFieldLines(
    'volumeFieldLines',
    volumeAntenna.position,
    1.5, 0.8, // major radius, minor radius
    new BABYLON.Color3(0.2, 0.6, 0.9),
    16 // number of arc lines
  );
}

// Create ellipsoidal field lines (arcs)
function createEllipsoidalFieldLines(namePrefix, center, radiusX, radiusY, radiusZ, color, numLines) {
  const fieldLines = [];
  
  for (let i = 0; i < numLines; i++) {
    const angle = (i / numLines) * Math.PI * 2;
    const points = [];
    
    // Create arc from bottom to top following ellipsoid surface
    for (let t = 0; t <= 1; t += 0.05) {
      const theta = t * Math.PI; // 0 to PI (bottom to top)
      const phi = angle;
      
      const x = center.x + (radiusX / 2) * Math.sin(theta) * Math.cos(phi);
      const y = center.y + (radiusY / 2) * Math.cos(theta);
      const z = center.z + (radiusZ / 2) * Math.sin(theta) * Math.sin(phi);
      
      points.push(new BABYLON.Vector3(x, y, z));
    }
    
    const line = BABYLON.MeshBuilder.CreateLines(
      `${namePrefix}_${i}`,
      { points: points },
      scene
    );
    
    line.color = color;
    line.alpha = 0.4;
    line.isPickable = false;
    
    fieldLines.push(line);
  }
  
  return fieldLines;
}

// Create toroidal field lines (circular arcs)
function createToroidalFieldLines(namePrefix, center, majorRadius, minorRadius, color, numLines) {
  const fieldLines = [];
  
  // Meridian lines (going around the tube)
  for (let i = 0; i < numLines / 2; i++) {
    const angle = (i / (numLines / 2)) * Math.PI * 2;
    const points = [];
    
    for (let t = 0; t <= 1; t += 0.05) {
      const theta = t * Math.PI * 2;
      
      const r = (majorRadius / 2) + (minorRadius / 2) * Math.cos(theta);
      const x = center.x + r * Math.cos(angle);
      const y = center.y + (minorRadius / 2) * Math.sin(theta);
      const z = center.z + r * Math.sin(angle);
      
      points.push(new BABYLON.Vector3(x, y, z));
    }
    
    const line = BABYLON.MeshBuilder.CreateLines(
      `${namePrefix}_meridian_${i}`,
      { points: points },
      scene
    );
    
    line.color = color;
    line.alpha = 0.4;
    line.isPickable = false;
    
    fieldLines.push(line);
  }
  
  // Parallel lines (going around the major circle)
  for (let i = 0; i < numLines / 2; i++) {
    const offset = ((i / (numLines / 2)) - 0.5) * minorRadius;
    const points = [];
    
    for (let t = 0; t <= 1; t += 0.05) {
      const angle = t * Math.PI * 2;
      
      const r = (majorRadius / 2);
      const x = center.x + r * Math.cos(angle);
      const y = center.y + offset;
      const z = center.z + r * Math.sin(angle);
      
      points.push(new BABYLON.Vector3(x, y, z));
    }
    
    const line = BABYLON.MeshBuilder.CreateLines(
      `${namePrefix}_parallel_${i}`,
      { points: points },
      scene
    );
    
    line.color = color;
    line.alpha = 0.4;
    line.isPickable = false;
    
    fieldLines.push(line);
  }
  
  // Rotate to match antenna orientation (Z-axis rotation)
  fieldLines.forEach(line => {
    line.rotation.z = Math.PI / 2;
  });
  
  return fieldLines;
}

function updateFieldIntensity() {
  // Animate field intensity based on cursor activity
  if (pitchFieldMesh && fieldsVisible) {
    // Pulse effect when pitch is being modified
    if (isDraggingPitch) {
      pitchFieldMesh.material.alpha = 0.25 + Math.sin(Date.now() * 0.01) * 0.05;
    } else {
      pitchFieldMesh.material.alpha = 0.15;
    }
  }
  
  if (volumeFieldMesh && fieldsVisible) {
    // Pulse effect when volume is being modified
    if (isDraggingVolume) {
      volumeFieldMesh.material.alpha = 0.25 + Math.sin(Date.now() * 0.01) * 0.05;
    } else {
      volumeFieldMesh.material.alpha = 0.15;
    }
  }
}

function toggleElectromagneticFields(visible) {
  fieldsVisible = visible;
  
  if (pitchFieldMesh) {
    pitchFieldMesh.setEnabled(visible);
  }
  if (volumeFieldMesh) {
    volumeFieldMesh.setEnabled(visible);
  }
  
  // Toggle field lines visibility
  scene.meshes.forEach(mesh => {
    if (mesh.name.startsWith('pitchFieldLines_') || 
        mesh.name.startsWith('volumeFieldLines_')) {
      mesh.setEnabled(visible);
    }
  });
}

// ======================================
// Picking & Interaction
// ======================================
function setupPicking() {
  const canvas = document.getElementById('canvas-main');
  
  // Mouse down
  canvas.addEventListener('pointerdown', (evt) => {
    const pickResult = scene.pick(evt.clientX, evt.clientY);
    
    if (pickResult.hit) {
      if (pickResult.pickedMesh === pitchCursor) {
        isDraggingPitch = true;
        dragStartY = evt.clientY;
        dragStartCursorY = pitchCursor.position.y;
        camera.detachControl(canvas);
        canvas.style.cursor = 'ns-resize';
      } else if (pickResult.pickedMesh === volumeCursor) {
        isDraggingVolume = true;
        dragStartY = evt.clientY;
        dragStartCursorY = volumeCursor.position.y;
        camera.detachControl(canvas);
        canvas.style.cursor = 'ns-resize';
      }
    }
  });
  
  // Mouse move
  canvas.addEventListener('pointermove', (evt) => {
    if (isDraggingPitch) {
      const deltaY = (dragStartY - evt.clientY) * 0.01; // Inverted and scaled
      let newY = dragStartCursorY + deltaY;
      newY = Math.max(PITCH_CURSOR_MIN_Y, Math.min(PITCH_CURSOR_MAX_Y, newY));
      pitchCursor.position.y = newY;
      
      // Update pitch
      const t = (newY - PITCH_CURSOR_MIN_Y) / (PITCH_CURSOR_MAX_Y - PITCH_CURSOR_MIN_Y);
      currentPitch = PITCH_MIN + t * (PITCH_MAX - PITCH_MIN);
      updateAudioPitch();
      updateFrequencyDisplay();
      
      // Start audio if not playing
      if (!isPlaying && isAudioInitialized) {
        startSound();
      }
    } else if (isDraggingVolume) {
      const deltaY = (dragStartY - evt.clientY) * 0.01;
      let newY = dragStartCursorY + deltaY;
      newY = Math.max(VOLUME_CURSOR_MIN_Y, Math.min(VOLUME_CURSOR_MAX_Y, newY));
      volumeCursor.position.y = newY;
      
      // Update volume
      const t = (newY - VOLUME_CURSOR_MIN_Y) / (VOLUME_CURSOR_MAX_Y - VOLUME_CURSOR_MIN_Y);
      currentVolume = VOLUME_MIN + t * (VOLUME_MAX - VOLUME_MIN);
      updateAudioVolume();
      updateVolumeDisplay();
      
      // Start audio if not playing
      if (!isPlaying && isAudioInitialized) {
        startSound();
      }
    }
  });
  
  // Mouse up
  canvas.addEventListener('pointerup', () => {
    if (isDraggingPitch || isDraggingVolume) {
      isDraggingPitch = false;
      isDraggingVolume = false;
      camera.attachControl(canvas, true);
      canvas.style.cursor = 'default';
    }
  });
}

// ======================================
// Web Audio API
// ======================================
function setupAudioSystem() {
  // Audio context will be created on first user interaction
  // (browsers require user gesture to start audio)
  document.getElementById('play-sound-btn').addEventListener('click', () => {
    if (!isAudioInitialized) {
      initAudioContext();
    }
    
    if (isPlaying) {
      stopSound();
    } else {
      startSound();
    }
  });
  
  // Waveform selector
  document.getElementById('waveform-select').addEventListener('change', (e) => {
    if (oscillator && isAudioInitialized) {
      oscillator.type = e.target.value;
    }
  });
  
  // Reverb checkbox
  document.getElementById('reverb-cb').addEventListener('change', (e) => {
    if (isAudioInitialized) {
      toggleReverb(e.target.checked);
    }
  });
}

function initAudioContext() {
  if (isAudioInitialized) return;
  
  console.log('Initializing Web Audio API...');
  
  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  
  // Create oscillator
  oscillator = audioContext.createOscillator();
  oscillator.type = document.getElementById('waveform-select').value;
  oscillator.frequency.setValueAtTime(currentPitch, audioContext.currentTime);
  
  // Create gain node (volume control)
  gainNode = audioContext.createGain();
  gainNode.gain.setValueAtTime(currentVolume, audioContext.currentTime);
  
  // Simple reverb (convolver with impulse response)
  reverbNode = audioContext.createConvolver();
  
  // Connect: oscillator -> gain -> destination
  oscillator.connect(gainNode);
  gainNode.connect(audioContext.destination);
  
  isAudioInitialized = true;
  console.log('Audio system initialized!');
}

function startSound() {
  if (!isAudioInitialized) {
    initAudioContext();
  }
  
  if (isPlaying) return;
  
  // Recreate oscillator (they can only be started once)
  oscillator = audioContext.createOscillator();
  oscillator.type = document.getElementById('waveform-select').value;
  oscillator.frequency.setValueAtTime(currentPitch, audioContext.currentTime);
  
  oscillator.connect(gainNode);
  oscillator.start();
  
  isPlaying = true;
  document.getElementById('play-sound-btn').textContent = 'Stop Sound';
  console.log('Sound started');
}

function stopSound() {
  if (!isPlaying || !oscillator) return;
  
  oscillator.stop();
  oscillator.disconnect();
  
  isPlaying = false;
  document.getElementById('play-sound-btn').textContent = 'Start Sound';
  console.log('Sound stopped');
}

function updateAudioPitch() {
  if (oscillator && isPlaying && isAudioInitialized) {
    oscillator.frequency.setValueAtTime(currentPitch, audioContext.currentTime);
  }
}

function updateAudioVolume() {
  if (gainNode && isAudioInitialized) {
    gainNode.gain.setValueAtTime(currentVolume, audioContext.currentTime);
  }
}

function toggleReverb(enabled) {
  // Simple reverb toggle (would need impulse response for real reverb)
  // This is a placeholder for future implementation
  console.log('Reverb toggle:', enabled, '(not yet implemented)');
}

// ======================================
// UI Controls
// ======================================
function setupUI() {
  // Tab switching
  window.activateTab = function(index) {
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');
    
    tabs.forEach((tab, i) => {
      if (i === index) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
    
    contents.forEach((content, i) => {
      if (i === index) {
        content.classList.add('active');
      } else {
        content.classList.remove('active');
      }
    });
  };
  
  // Reset button
  document.getElementById('reset-btn').addEventListener('click', () => {
    resetScene();
  });
  
  // Auto rotate checkbox
  document.getElementById('auto-rotate-cb').addEventListener('change', (e) => {
    if (e.target.checked) {
      scene.registerBeforeRender(() => {
        camera.alpha += 0.005;
      });
    } else {
      scene.unregisterBeforeRender();
    }
  });
  
  // Show grid checkbox
  document.getElementById('show-grid-cb').addEventListener('change', (e) => {
    groundGrid.setEnabled(e.target.checked);
  });
  
  // Show electromagnetic fields checkbox
  document.getElementById('show-fields-cb').addEventListener('change', (e) => {
    toggleElectromagneticFields(e.target.checked);
  });
  
  // Home button
  document.getElementById('home-btn').addEventListener('click', () => {
    window.location.href = 'https://github.com/Echopraxium/tscg';
  });
  
  // Play demo button
  document.getElementById('play-demo-btn').addEventListener('click', () => {
    if (demoMode) {
      stopDemo();
    } else {
      playDemo();
    }
  });
}

function resetScene() {
  // Reset cursors to default positions
  pitchCursor.position.y = 2.5;
  volumeCursor.position.y = 2.0;
  
  // Reset audio parameters
  currentPitch = 440;
  currentVolume = 0.5;
  
  updateAudioPitch();
  updateAudioVolume();
  updateFrequencyDisplay();
  updateVolumeDisplay();
  
  // Reset camera
  camera.alpha = -Math.PI / 2;
  camera.beta = Math.PI / 3;
  camera.radius = 12;
  camera.target = new BABYLON.Vector3(0, 2, 0);
  
  // Stop sound
  if (isPlaying) {
    stopSound();
  }
  
  console.log('Scene reset');
}

// ======================================
// Demo Mode - Classical Melodies Library
// ======================================

// Get melody sequence by name
function getMelodySequence(melodyName) {
  const melodies = {
    bumblebee: getBumblebeeMelody(),
    clair: getClairDeLuneMelody(),
    fur_elise: getFurEliseMelody(),
    gymnopédie: getGymnopedieMelody(),
    canon: getCanonMelody(),
    turkish: getTurkishMarchMelody(),
    prelude: getPreludeMelody(),
    clair_lune: getAuClairDeLaLuneMelody(),
    ode: getOdeToJoyMelody(),
    swan: getSwanMelody()
  };
  
  return melodies[melodyName] || melodies.bumblebee;
}

// 1. Flight of the Bumblebee - Rimsky-Korsakov
function getBumblebeeMelody() {
  return [
    // First phrase (ascending chromatic run)
    [440, 100, 0.4],   // A4
    [466, 100, 0.4],   // A#4
    [494, 100, 0.5],   // B4
    [523, 100, 0.5],   // C5
    [554, 100, 0.5],   // C#5
    [587, 100, 0.6],   // D5
    [622, 100, 0.6],   // D#5
    [659, 100, 0.6],   // E5
    [622, 100, 0.5],   // D#5
    [587, 100, 0.5],   // D5
    [554, 100, 0.5],   // C#5
    [523, 100, 0.4],   // C5
    [494, 100, 0.4],   // B4
    [523, 100, 0.5],   // C5
    [554, 100, 0.5],   // C#5
    [587, 100, 0.6],   // D5
    [622, 100, 0.6],   // D#5
    [659, 100, 0.7],   // E5
    [698, 100, 0.7],   // F5
    [740, 100, 0.7],   // F#5
    [698, 80, 0.6],    // F5
    [740, 80, 0.6],    // F#5
    [698, 80, 0.6],    // F5
    [659, 80, 0.5],    // E5
    [622, 80, 0.5],    // D#5
    [659, 80, 0.5],    // E5
    [622, 80, 0.5],    // D#5
    [587, 80, 0.4],    // D5
    [784, 120, 0.7],   // G5
    [740, 120, 0.7],   // F#5
    [698, 120, 0.6],   // F5
    [659, 120, 0.6],   // E5
    [622, 120, 0.5],   // D#5
    [587, 120, 0.5],   // D5
    [554, 120, 0.4],   // C#5
    [523, 120, 0.4],   // C5
    [494, 100, 0.5],   // B4
    [466, 100, 0.5],   // A#4
    [440, 100, 0.5],   // A4
    [415, 100, 0.4],   // G#4
    [392, 100, 0.4],   // G4
    [370, 100, 0.3],   // F#4
    [349, 100, 0.3],   // F4
    [330, 150, 0.2],   // E4
  ];
}

// 2. Clair de Lune - Debussy (opening phrase)
function getClairDeLuneMelody() {
  return [
    [523, 300, 0.3],   // C5
    [587, 300, 0.3],   // D5
    [659, 300, 0.4],   // E5
    [698, 600, 0.4],   // F5
    [659, 300, 0.3],   // E5
    [587, 300, 0.3],   // D5
    [523, 600, 0.3],   // C5
    [494, 300, 0.3],   // B4
    [523, 300, 0.3],   // C5
    [587, 600, 0.4],   // D5
    [659, 300, 0.4],   // E5
    [698, 300, 0.4],   // F5
    [784, 600, 0.5],   // G5
    [698, 300, 0.4],   // F5
    [659, 300, 0.4],   // E5
    [587, 900, 0.3],   // D5
  ];
}

// 3. Für Elise - Beethoven (famous opening)
function getFurEliseMelody() {
  return [
    [659, 200, 0.4],   // E5
    [622, 200, 0.4],   // D#5
    [659, 200, 0.4],   // E5
    [622, 200, 0.4],   // D#5
    [659, 200, 0.4],   // E5
    [494, 200, 0.4],   // B4
    [587, 200, 0.4],   // D5
    [523, 200, 0.4],   // C5
    [440, 400, 0.4],   // A4
    [262, 200, 0.2],   // C4
    [330, 200, 0.3],   // E4
    [440, 200, 0.4],   // A4
    [494, 400, 0.4],   // B4
    [330, 200, 0.3],   // E4
    [415, 200, 0.3],   // G#4
    [494, 200, 0.4],   // B4
    [523, 400, 0.4],   // C5
    [330, 200, 0.3],   // E4
    [659, 200, 0.4],   // E5
    [622, 200, 0.4],   // D#5
    [659, 200, 0.4],   // E5
    [622, 200, 0.4],   // D#5
    [659, 200, 0.4],   // E5
    [494, 200, 0.4],   // B4
    [587, 200, 0.4],   // D5
    [523, 200, 0.4],   // C5
    [440, 600, 0.4],   // A4
  ];
}

// 4. Gymnopédie No.1 - Satie (slow, dreamy)
function getGymnopedieMelody() {
  return [
    [392, 600, 0.3],   // G4
    [494, 600, 0.4],   // B4
    [523, 600, 0.4],   // C5
    [587, 1200, 0.4],  // D5
    [523, 600, 0.4],   // C5
    [494, 600, 0.4],   // B4
    [440, 1200, 0.4],  // A4
    [392, 600, 0.3],   // G4
    [440, 600, 0.4],   // A4
    [494, 1200, 0.4],  // B4
    [523, 600, 0.4],   // C5
    [587, 600, 0.4],   // D5
    [523, 1200, 0.4],  // C5
  ];
}

// 5. Canon in D - Pachelbel (famous progression)
function getCanonMelody() {
  return [
    [587, 400, 0.5],   // D5
    [440, 400, 0.4],   // A4
    [494, 400, 0.4],   // B4
    [370, 400, 0.3],   // F#4
    [392, 400, 0.4],   // G4
    [587, 400, 0.5],   // D5
    [392, 400, 0.4],   // G4
    [440, 400, 0.4],   // A4
    [587, 400, 0.5],   // D5
    [440, 400, 0.4],   // A4
    [494, 400, 0.4],   // B4
    [370, 400, 0.3],   // F#4
    [392, 400, 0.4],   // G4
    [587, 400, 0.5],   // D5
    [392, 400, 0.4],   // G4
    [440, 800, 0.4],   // A4
  ];
}

// 6. Turkish March - Mozart (energetic)
function getTurkishMarchMelody() {
  return [
    [494, 150, 0.5],   // B4
    [440, 150, 0.4],   // A4
    [415, 150, 0.4],   // G#4
    [440, 300, 0.4],   // A4
    [523, 150, 0.5],   // C5
    [494, 150, 0.5],   // B4
    [440, 150, 0.4],   // A4
    [494, 300, 0.5],   // B4
    [659, 150, 0.6],   // E5
    [622, 150, 0.5],   // D#5
    [587, 150, 0.5],   // D5
    [622, 300, 0.5],   // D#5
    [494, 150, 0.5],   // B4
    [440, 150, 0.4],   // A4
    [415, 150, 0.4],   // G#4
    [440, 600, 0.4],   // A4
  ];
}

// 7. Prelude in C Major - Bach (arpeggios)
function getPreludeMelody() {
  return [
    [262, 150, 0.3],   // C4
    [330, 150, 0.3],   // E4
    [392, 150, 0.4],   // G4
    [523, 150, 0.4],   // C5
    [330, 150, 0.3],   // E4
    [392, 150, 0.4],   // G4
    [523, 150, 0.4],   // C5
    [330, 150, 0.3],   // E4
    [294, 150, 0.3],   // D4
    [349, 150, 0.3],   // F4
    [440, 150, 0.4],   // A4
    [587, 150, 0.4],   // D5
    [349, 150, 0.3],   // F4
    [440, 150, 0.4],   // A4
    [587, 150, 0.4],   // D5
    [349, 150, 0.3],   // F4
    [262, 150, 0.3],   // C4
    [330, 150, 0.3],   // E4
    [392, 150, 0.4],   // G4
    [523, 150, 0.4],   // C5
    [330, 150, 0.3],   // E4
    [392, 150, 0.4],   // G4
    [523, 150, 0.4],   // C5
    [330, 150, 0.3],   // E4
  ];
}

// 8. Au Clair de la Lune - Traditional (simple, folk)
function getAuClairDeLaLuneMelody() {
  return [
    [523, 400, 0.4],   // C5
    [523, 400, 0.4],   // C5
    [523, 400, 0.4],   // C5
    [587, 400, 0.4],   // D5
    [659, 800, 0.5],   // E5
    [587, 800, 0.4],   // D5
    [523, 400, 0.4],   // C5
    [659, 400, 0.5],   // E5
    [587, 400, 0.4],   // D5
    [587, 400, 0.4],   // D5
    [523, 800, 0.4],   // C5
    [523, 400, 0.4],   // C5
    [523, 400, 0.4],   // C5
    [523, 400, 0.4],   // C5
    [587, 400, 0.4],   // D5
    [659, 800, 0.5],   // E5
    [587, 800, 0.4],   // D5
  ];
}

// 9. Ode to Joy - Beethoven (triumphant)
function getOdeToJoyMelody() {
  return [
    [659, 300, 0.5],   // E5
    [659, 300, 0.5],   // E5
    [698, 300, 0.5],   // F5
    [784, 300, 0.6],   // G5
    [784, 300, 0.6],   // G5
    [698, 300, 0.5],   // F5
    [659, 300, 0.5],   // E5
    [587, 300, 0.5],   // D5
    [523, 300, 0.4],   // C5
    [523, 300, 0.4],   // C5
    [587, 300, 0.5],   // D5
    [659, 300, 0.5],   // E5
    [659, 450, 0.5],   // E5
    [587, 150, 0.5],   // D5
    [587, 600, 0.5],   // D5
    [659, 300, 0.5],   // E5
    [659, 300, 0.5],   // E5
    [698, 300, 0.5],   // F5
    [784, 300, 0.6],   // G5
    [784, 300, 0.6],   // G5
    [698, 300, 0.5],   // F5
    [659, 300, 0.5],   // E5
    [587, 300, 0.5],   // D5
    [523, 300, 0.4],   // C5
    [523, 300, 0.4],   // C5
    [587, 300, 0.5],   // D5
    [659, 300, 0.5],   // E5
    [587, 450, 0.5],   // D5
    [523, 150, 0.4],   // C5
    [523, 600, 0.4],   // C5
  ];
}

// 10. The Swan - Saint-Saëns (lyrical, flowing)
function getSwanMelody() {
  return [
    [392, 600, 0.4],   // G4
    [523, 600, 0.5],   // C5
    [494, 300, 0.5],   // B4
    [440, 300, 0.4],   // A4
    [392, 600, 0.4],   // G4
    [440, 600, 0.4],   // A4
    [494, 600, 0.5],   // B4
    [523, 1200, 0.5],  // C5
    [587, 600, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [494, 300, 0.5],   // B4
    [440, 300, 0.4],   // A4
    [392, 600, 0.4],   // G4
    [349, 600, 0.4],   // F4
    [392, 1200, 0.4],  // G4
  ];
}

function playDemo() {
  if (!isAudioInitialized) {
    initAudioContext();
  }
  
  // Get selected melody
  const melodySelect = document.getElementById('melody-select');
  const selectedMelody = melodySelect.value;
  
  demoMode = true;
  demoSequence = getMelodySequence(selectedMelody);
  demoCurrentNote = 0;
  demoStartTime = Date.now();
  
  // Update button
  const btn = document.getElementById('play-demo-btn');
  btn.textContent = '⏹ Stop Demo';
  btn.classList.add('playing');
  
  // Start audio if not playing
  if (!isPlaying) {
    startSound();
  }
  
  console.log('Demo mode started - ' + melodySelect.options[melodySelect.selectedIndex].text);
}

function stopDemo() {
  demoMode = false;
  demoCurrentNote = 0;
  
  // Update button
  const btn = document.getElementById('play-demo-btn');
  btn.textContent = '▶ Play Demo';
  btn.classList.remove('playing');
  
  // Stop sound
  if (isPlaying) {
    stopSound();
  }
  
  // Reset cursors to default
  resetScene();
  
  console.log('Demo mode stopped');
}

function updateDemoMode() {
  if (!demoMode || demoSequence.length === 0) return;
  
  // Calculate elapsed time
  const elapsed = Date.now() - demoStartTime;
  
  // Find current note based on elapsed time
  let cumulativeTime = 0;
  let targetNote = -1;
  
  for (let i = 0; i < demoSequence.length; i++) {
    cumulativeTime += demoSequence[i][1]; // duration
    if (elapsed < cumulativeTime) {
      targetNote = i;
      break;
    }
  }
  
  // If sequence finished, restart
  if (targetNote === -1) {
    demoStartTime = Date.now();
    return;
  }
  
  // Animate cursors to current note
  if (targetNote !== demoCurrentNote) {
    const [freq, duration, vol] = demoSequence[targetNote];
    
    // Update pitch cursor
    const pitchT = (freq - PITCH_MIN) / (PITCH_MAX - PITCH_MIN);
    const pitchY = PITCH_CURSOR_MIN_Y + pitchT * (PITCH_CURSOR_MAX_Y - PITCH_CURSOR_MIN_Y);
    pitchCursor.position.y = pitchY;
    currentPitch = freq;
    
    // Update volume cursor
    const volumeT = vol / VOLUME_MAX;
    const volumeY = VOLUME_CURSOR_MIN_Y + volumeT * (VOLUME_CURSOR_MAX_Y - VOLUME_CURSOR_MIN_Y);
    volumeCursor.position.y = volumeY;
    currentVolume = vol;
    
    // Update audio
    updateAudioPitch();
    updateAudioVolume();
    updateFrequencyDisplay();
    updateVolumeDisplay();
    
    demoCurrentNote = targetNote;
  }
}

function updateFrequencyDisplay() {
  const note = frequencyToNote(currentPitch);
  document.getElementById('freq-display').textContent = 
    `${Math.round(currentPitch)} Hz (${note})`;
}

function updateVolumeDisplay() {
  const volumePercent = Math.round((currentVolume / VOLUME_MAX) * 100);
  document.getElementById('volume-display').textContent = `${volumePercent}%`;
}

// ======================================
// Utility Functions
// ======================================
function frequencyToNote(freq) {
  const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  const a4 = 440;
  const c0 = a4 * Math.pow(2, -4.75);
  
  if (freq === 0) return '---';
  
  const halfSteps = 12 * Math.log2(freq / c0);
  const octave = Math.floor(halfSteps / 12);
  const noteIndex = Math.round(halfSteps % 12);
  
  return noteNames[noteIndex] + octave;
}

// Initialize displays
updateFrequencyDisplay();
updateVolumeDisplay();
