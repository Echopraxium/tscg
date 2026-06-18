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

// Vibrato (bouton droit sur curseur pitch)
let vibratoActive = false;
let vibratoSpeed = 5.5;    // Hz - vitesse d'oscillation
let vibratoDepth = 8;      // Hz - amplitude de l'oscillation
let vibratoTime = 0;

// Mode Piano Key (notes détachées)
let pianoKeyMode = false;

// Keyboard control for volume cursor
let volumeKeyUp = false;    // Arrow Up or W
let volumeKeyDown = false;  // Arrow Down or S
const volumeKeySpeed = 0.02; // Speed of volume cursor movement with keyboard

// Waveform selector (4-position knob)
let currentWaveform = 0; // 0=sine, 1=triangle, 2=square, 3=sawtooth
const waveformNames = ['sine', 'triangle', 'square', 'sawtooth'];
let waveformKnob = null;
let waveformIndicator = null;

// Pitch control circle (appears during drag)
let pitchControlCircle = null;
let pitchRadiusLine = null;  // Visual radius from antenna to circle edge
let isPitchDragging = false;
const pitchCircleBaseRadius = 0.3;  // Base radius
const pitchCircleRadiusRange = 0.6; // Max additional radius
let isKeyPressed = false;  // Track si on est en train de drag
let fadeOutActive = false;
let fadeOutStartTime = 0;
let fadeOutDuration = 0.2; // secondes

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
  camera.upperBetaLimit = Math.PI - 0.1;  // Allow looking from below (almost vertical up)
  camera.wheelPrecision = 50;  // Higher = slower/smoother zoom (default is 3)
  
  // Lights
  const hemisphericLight = new BABYLON.HemisphericLight(
    'hemiLight',
    new BABYLON.Vector3(0, 1, 0),
    scene
  );
  hemisphericLight.intensity = 0.8;  // Increased for better top illumination
  
  const directionalLight = new BABYLON.DirectionalLight(
    'dirLight',
    new BABYLON.Vector3(-1, -0.5, -1),  // Less downward angle for better top lighting
    scene
  );
  directionalLight.intensity = 0.6;  // Slightly increased
  
  // Ground grid
  createGroundGrid();
  
  // Theremin model
  createThereminModel();
  
  // Interactive cursors
  createPitchCursor();
  createVolumeCursor();
  
  // XYZ Axis Helper (for debugging orientation)
  createAxisHelper();
  
  // Electromagnetic field visualization
  createElectromagneticFields();
  
  // Setup picking
  setupPicking();
  updateWaveform(); // Initialize waveform knob position
  
  // Render loop
  engine.runRenderLoop(() => {
    // Keyboard control for volume cursor
    if (volumeKeyUp && volumeCursor) {
      volumeCursor.position.y = Math.min(volumeCursor.position.y + volumeKeySpeed, VOLUME_CURSOR_MAX_Y);
      // Calculate volume from cursor position
      const t = (volumeCursor.position.y - VOLUME_CURSOR_MIN_Y) / (VOLUME_CURSOR_MAX_Y - VOLUME_CURSOR_MIN_Y);
      currentVolume = VOLUME_MIN + t * (VOLUME_MAX - VOLUME_MIN);
      updateAudioVolume();
    }
    if (volumeKeyDown && volumeCursor) {
      volumeCursor.position.y = Math.max(volumeCursor.position.y - volumeKeySpeed, VOLUME_CURSOR_MIN_Y);
      // Calculate volume from cursor position
      const t = (volumeCursor.position.y - VOLUME_CURSOR_MIN_Y) / (VOLUME_CURSOR_MAX_Y - VOLUME_CURSOR_MIN_Y);
      currentVolume = VOLUME_MIN + t * (VOLUME_MAX - VOLUME_MIN);
      updateAudioVolume();
    }
    
    updateFieldIntensity();
    updateDemoMode();
    
    // Continuous audio updates (vibrato + piano key fade out)
    if (vibratoActive) {
      updateAudioPitch();
    }
    if (fadeOutActive) {
      updateAudioVolume();
    }
    
    scene.render();
  });
  
  // Resize handler
  window.addEventListener('resize', () => {
    engine.resize();
  });
}

function createGroundGrid() {
  // Create discrete grid with light gray dashed lines
  const gridSize = 20;
  const divisions = 20;
  const step = gridSize / divisions;
  
  const lines = [];
  
  // Horizontal lines (along X axis)
  for (let i = 0; i <= divisions; i++) {
    const z = -gridSize / 2 + i * step;
    lines.push([
      new BABYLON.Vector3(-gridSize / 2, 0, z),
      new BABYLON.Vector3(gridSize / 2, 0, z)
    ]);
  }
  
  // Vertical lines (along Z axis)
  for (let i = 0; i <= divisions; i++) {
    const x = -gridSize / 2 + i * step;
    lines.push([
      new BABYLON.Vector3(x, 0, -gridSize / 2),
      new BABYLON.Vector3(x, 0, gridSize / 2)
    ]);
  }
  
  groundGrid = BABYLON.MeshBuilder.CreateLineSystem(
    'ground',
    { lines: lines },
    scene
  );
  
  // Light gray color, more discrete
  groundGrid.color = new BABYLON.Color3(0.3, 0.3, 0.3);  // Light gray
  groundGrid.alpha = 0.25;  // More transparent
  
  // Enable dashed lines for discrete appearance
  groundGrid.enableEdgesRendering();
  groundGrid.edgesWidth = 1.0;
  groundGrid.edgesColor = new BABYLON.Color4(0.3, 0.3, 0.3, 0.25);
}

function createThereminModel() {
  // Trapezoidal body created manually with vertices and faces
  // CORRECTED PROPORTIONS (accounting for -PI/2 rotation around Y):
  // After rotation: X→depth, Z→width, Y→height
  // 
  // Original: width=5.0, depth=3.0, height=0.6
  // Target: width +15%, depth -40%, height +65%
  // Visual: width=3.45, depth=3.0, height=0.99
  // 
  // In code BEFORE rotation:
  // X (becomes depth after rotation): 3.0
  // Z (becomes width after rotation): 3.45
  // Y (height, unchanged): 0.99
  
  const halfX = 3.0 / 2;      // 1.5 (will be depth after rotation)
  const halfZ = 3.45 / 2;     // 1.725 (will be width after rotation)
  const height = 0.99;        // Height increased by 65%
  
  // Bottom trapezoid (Y=0): wider
  const bottomLeft = new BABYLON.Vector3(-halfX, 0, -halfZ);
  const bottomRight = new BABYLON.Vector3(halfX, 0, -halfZ);
  const bottomFrontRight = new BABYLON.Vector3(halfX, 0, halfZ);
  const bottomFrontLeft = new BABYLON.Vector3(-halfX, 0, halfZ);
  
  // Top trapezoid (Y=height): narrower, asymmetric (matching provided image)
  // Left side more inclined: ratio 0.8
  // Right side less inclined: ratio 0.6
  const topLeftRatio = 0.8;
  const topRightRatio = 0.6;
  const topLeft = new BABYLON.Vector3(-halfX * topLeftRatio, height, -halfZ);
  const topRight = new BABYLON.Vector3(halfX * topRightRatio, height, -halfZ);
  const topFrontRight = new BABYLON.Vector3(halfX * topRightRatio, height, halfZ);
  const topFrontLeft = new BABYLON.Vector3(-halfX * topLeftRatio, height, halfZ);
  
  // Define vertices (8 corners)
  const positions = [
    // Bottom 4 vertices (0-3)
    ...bottomLeft.asArray(),
    ...bottomRight.asArray(),
    ...bottomFrontRight.asArray(),
    ...bottomFrontLeft.asArray(),
    // Top 4 vertices (4-7)
    ...topLeft.asArray(),
    ...topRight.asArray(),
    ...topFrontRight.asArray(),
    ...topFrontLeft.asArray()
  ];
  
  // Define faces (triangles, counter-clockwise for outward normals)
  const indices = [
    // Bottom face (looking from below)
    0, 2, 1,  0, 3, 2,
    // Top face (looking from above)  
    4, 5, 6,  4, 6, 7,
    // Front face (toward positive Z)
    3, 6, 2,  3, 7, 6,
    // Back face (toward negative Z)
    0, 1, 5,  0, 5, 4,
    // Left face (more inclined, toward negative X)
    0, 4, 7,  0, 7, 3,
    // Right face (less inclined, toward positive X)
    1, 2, 6,  1, 6, 5
  ];
  
  // Create custom mesh
  thereminBody = new BABYLON.Mesh('body', scene);
  const vertexData = new BABYLON.VertexData();
  vertexData.positions = positions;
  vertexData.indices = indices;
  
  // IMPROVED UV COORDINATES using normalized positions
  // Calculate bounding box for normalization
  const minX = -halfX, maxX = halfX;
  const minY = 0, maxY = height;
  const minZ = -halfZ, maxZ = halfZ;
  
  // IMPROVED UV COORDINATES using cylindrical mapping
  // This works better for trapezoidal shapes with vertical faces
  const uvs = [];
  for (let i = 0; i < positions.length; i += 3) {
    const x = positions[i];
    const y = positions[i + 1];
    const z = positions[i + 2];
    
    // Cylindrical mapping: angle for U, height for V
    const angle = Math.atan2(z, x);
    const u = (angle + Math.PI) / (2 * Math.PI);  // 0 to 1 around perimeter
    const v = (y - minY) / (maxY - minY);  // 0 to 1 from bottom to top
    
    uvs.push(u, v);
  }
  
  vertexData.uvs = uvs;
  
  // Compute normals for proper lighting
  const normals = [];
  BABYLON.VertexData.ComputeNormals(positions, indices, normals);
  vertexData.normals = normals;
  
  vertexData.applyToMesh(thereminBody);
  
  // Position at Y=0.35 (above grid)
  thereminBody.position = new BABYLON.Vector3(0, 0.35, 0);
  
  // Rotate PI/2 around Y
  thereminBody.rotation.y = Math.PI / 2;
  
  // MATTE OAK WOOD MATERIAL with provided texture
  const bodyMat = new BABYLON.StandardMaterial('bodyMat', scene);
  
  // Oak wood texture from assets folder
  const woodTexture = new BABYLON.Texture(
    'src/assets/oak-texture.jpg',
    scene,
    false,  // noMipmap
    true,   // invertY
    BABYLON.Texture.TRILINEAR_SAMPLINGMODE,  // samplingMode
    () => console.log('✓ Oak texture loaded successfully'),  // onLoad
    (message) => console.error('✗ Oak texture load error:', message)  // onError
  );
  woodTexture.uScale = 3;  // Increased repeat for better lateral face coverage
  woodTexture.vScale = 3;
  woodTexture.hasAlpha = false;
  woodTexture.wrapU = BABYLON.Texture.WRAP_ADDRESSMODE;  // Repeat mode
  woodTexture.wrapV = BABYLON.Texture.WRAP_ADDRESSMODE;
  
  bodyMat.diffuseTexture = woodTexture;
  bodyMat.ambientTexture = woodTexture;  // Also set ambient for better visibility
  
  // LIGHTEN the texture to match test rectangle
  bodyMat.emissiveColor = new BABYLON.Color3(0.15, 0.10, 0.05);  // Slight warm glow
  bodyMat.ambientColor = new BABYLON.Color3(0.3, 0.3, 0.3);  // Ambient light contribution
  
  // MATTE finish - very low specular
  bodyMat.specularColor = new BABYLON.Color3(0.05, 0.05, 0.05);  // Almost no reflection
  bodyMat.specularPower = 3;  // Very low = matte finish
  
  bodyMat.backFaceCulling = false;
  bodyMat.alpha = 0;  // INVISIBLE - only textured faces are visible
  thereminBody.material = bodyMat;
  thereminBody.isVisible = false;  // Hide solid body completely
  
  // ===== 6 TEXTURED FACES WITH EXACT VERTICES =====
  // Using exact trapezoid vertices to ensure perfect edge alignment
  
  // Helper to create wood material
  function createWoodMaterial(name, brightness = 'medium', uScale = 2, vScale = 1) {
    const mat = new BABYLON.StandardMaterial(name, scene);
    const tex = new BABYLON.Texture('src/assets/oak-texture.jpg', scene, 
      false, // noMipmap
      false, // invertY
      BABYLON.Texture.TRILINEAR_SAMPLINGMODE,
      () => { console.log(`✓ Texture loaded for ${name}`); },
      (message) => { console.error(`✗ Texture failed for ${name}:`, message); }
    );
    tex.uScale = uScale;
    tex.vScale = vScale;
    mat.diffuseTexture = tex;
    
    const levels = {
      medium: { e: [0.20, 0.13, 0.08], a: [0.35, 0.35, 0.35] },
      light: { e: [0.25, 0.17, 0.10], a: [0.45, 0.45, 0.45] }
    };
    
    const l = levels[brightness];
    mat.emissiveColor = new BABYLON.Color3(...l.e);
    mat.ambientColor = new BABYLON.Color3(...l.a);
    mat.specularColor = new BABYLON.Color3(0.05, 0.05, 0.05);
    mat.specularPower = 3;
    mat.backFaceCulling = true;
    return mat;
  }
  
  // Base position offset
  const baseY = 0.35;
  
  // Define 8 vertices of trapezoid (in local coordinates, before body rotation)
  const v1_BL_Back = new BABYLON.Vector3(-halfX, 0, -halfZ);           // Bottom-Left-Back
  const v2_BR_Back = new BABYLON.Vector3(halfX, 0, -halfZ);            // Bottom-Right-Back
  const v3_BL_Front = new BABYLON.Vector3(-halfX, 0, halfZ);           // Bottom-Left-Front
  const v4_BR_Front = new BABYLON.Vector3(halfX, 0, halfZ);            // Bottom-Right-Front
  const v5_TL_Back = new BABYLON.Vector3(-halfX * 0.8, height, -halfZ); // Top-Left-Back
  const v6_TR_Back = new BABYLON.Vector3(halfX * 0.6, height, -halfZ);  // Top-Right-Back
  const v7_TL_Front = new BABYLON.Vector3(-halfX * 0.8, height, halfZ); // Top-Left-Front
  const v8_TR_Front = new BABYLON.Vector3(halfX * 0.6, height, halfZ);  // Top-Right-Front
  
  // === FACE 1: BOTTOM (rectangle) ===
  const bottomVerts = [...v1_BL_Back.asArray(), ...v2_BR_Back.asArray(), ...v4_BR_Front.asArray(), ...v3_BL_Front.asArray()];
  const bottomIndices = [0, 2, 1, 0, 3, 2];  // Reversed winding
  const bottomUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const bottomFace = new BABYLON.Mesh('bottomFace', scene);
  const bottomVD = new BABYLON.VertexData();
  bottomVD.positions = bottomVerts;
  bottomVD.indices = bottomIndices;
  bottomVD.uvs = bottomUVs;
  const bottomNormals = [];
  BABYLON.VertexData.ComputeNormals(bottomVerts, bottomIndices, bottomNormals);
  bottomVD.normals = bottomNormals;
  bottomVD.applyToMesh(bottomFace);
  bottomFace.position = new BABYLON.Vector3(0, baseY, 0);
  bottomFace.rotation.y = Math.PI / 2;
  bottomFace.material = createWoodMaterial('bottomMat', 'medium', 1.5, 1.5);
  
  // === FACE 2: TOP (rectangle - smaller) ===
  const topVerts = [...v5_TL_Back.asArray(), ...v6_TR_Back.asArray(), ...v8_TR_Front.asArray(), ...v7_TL_Front.asArray()];
  const topIndices = [0, 1, 2, 0, 2, 3];
  const topUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const topFace = new BABYLON.Mesh('topFace', scene);
  const topVD = new BABYLON.VertexData();
  topVD.positions = topVerts;
  topVD.indices = topIndices;
  topVD.uvs = topUVs;
  const topNormals = [];
  BABYLON.VertexData.ComputeNormals(topVerts, topIndices, topNormals);
  topVD.normals = topNormals;
  topVD.applyToMesh(topFace);
  topFace.position = new BABYLON.Vector3(0, baseY, 0);
  topFace.rotation.y = Math.PI / 2;
  topFace.material = createWoodMaterial('topMat', 'light', 1.0, 1.5);
  
  // === FACE 3: LEFT/VOLUME (trapezoid) ===
  const leftVerts = [...v1_BL_Back.asArray(), ...v3_BL_Front.asArray(), ...v7_TL_Front.asArray(), ...v5_TL_Back.asArray()];
  const leftIndices = [0, 2, 1, 0, 3, 2];
  const leftUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const leftFace = new BABYLON.Mesh('leftFace', scene);
  const leftVD = new BABYLON.VertexData();
  leftVD.positions = leftVerts;
  leftVD.indices = leftIndices;
  leftVD.uvs = leftUVs;
  const leftNormals = [];
  BABYLON.VertexData.ComputeNormals(leftVerts, leftIndices, leftNormals);
  leftVD.normals = leftNormals;
  leftVD.applyToMesh(leftFace);
  leftFace.position = new BABYLON.Vector3(0, baseY, 0);
  leftFace.rotation.y = Math.PI / 2;
  leftFace.material = createWoodMaterial('leftMat', 'light', 1.5, 0.5);
  
  // === FACE 4: RIGHT/PITCH (trapezoid) ===
  const rightVerts = [...v2_BR_Back.asArray(), ...v4_BR_Front.asArray(), ...v8_TR_Front.asArray(), ...v6_TR_Back.asArray()];
  const rightIndices = [0, 1, 2, 0, 2, 3];
  const rightUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const rightFace = new BABYLON.Mesh('rightFace', scene);
  const rightVD = new BABYLON.VertexData();
  rightVD.positions = rightVerts;
  rightVD.indices = rightIndices;
  rightVD.uvs = rightUVs;
  const rightNormals = [];
  BABYLON.VertexData.ComputeNormals(rightVerts, rightIndices, rightNormals);
  rightVD.normals = rightNormals;
  rightVD.applyToMesh(rightFace);
  rightFace.position = new BABYLON.Vector3(0, baseY, 0);
  rightFace.rotation.y = Math.PI / 2;
  rightFace.material = createWoodMaterial('rightMat', 'light', 1.5, 0.5);
  
  // === FACE 5: BACK (rectangle) ===
  const backVerts = [...v1_BL_Back.asArray(), ...v2_BR_Back.asArray(), ...v6_TR_Back.asArray(), ...v5_TL_Back.asArray()];
  const backIndices = [0, 1, 2, 0, 2, 3];
  const backUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const backFace = new BABYLON.Mesh('backFace', scene);
  const backVD = new BABYLON.VertexData();
  backVD.positions = backVerts;
  backVD.indices = backIndices;
  backVD.uvs = backUVs;
  const backNormals = [];
  BABYLON.VertexData.ComputeNormals(backVerts, backIndices, backNormals);
  backVD.normals = backNormals;
  backVD.applyToMesh(backFace);
  backFace.position = new BABYLON.Vector3(0, baseY, 0);
  backFace.rotation.y = Math.PI / 2;
  backFace.material = createWoodMaterial('backMat', 'light', 1.5, 0.5);
  
  // === FACE 6: FRONT (rectangle) ===
  const frontVerts = [...v3_BL_Front.asArray(), ...v4_BR_Front.asArray(), ...v8_TR_Front.asArray(), ...v7_TL_Front.asArray()];
  const frontIndices = [0, 2, 1, 0, 3, 2];  // Reversed winding
  const frontUVs = [0, 0, 1, 0, 1, 1, 0, 1];
  
  const frontFace = new BABYLON.Mesh('frontFace', scene);
  const frontVD = new BABYLON.VertexData();
  frontVD.positions = frontVerts;
  frontVD.indices = frontIndices;
  frontVD.uvs = frontUVs;
  const frontNormals = [];
  BABYLON.VertexData.ComputeNormals(frontVerts, frontIndices, frontNormals);
  frontVD.normals = frontNormals;
  frontVD.applyToMesh(frontFace);
  frontFace.position = new BABYLON.Vector3(0, baseY, 0);
  frontFace.rotation.y = Math.PI / 2;
  frontFace.material = createWoodMaterial('frontMat', 'light', 1.5, 0.5);
  
  console.log('✓ All 6 textured faces created with exact vertices');
  
  // Inclined control panel (moved further outward)
  const panel = BABYLON.MeshBuilder.CreateBox(
    'panel',
    { width: 2.5, height: 0.6, depth: 0.12 },
    scene
  );
  const panelBaseZ = -halfZ + 0.30;
  panel.position = new BABYLON.Vector3(0, 0.65, panelBaseZ * 0.9);  // 10% toward positive Z (less negative)
  // Rotations in LOCAL space
  panel.rotate(BABYLON.Axis.Y, -Math.PI, BABYLON.Space.LOCAL);
  panel.rotate(BABYLON.Axis.X, -(3 * Math.PI / 32 + 13.65 * Math.PI / 180), BABYLON.Space.LOCAL);  // ~30.525° clockwise
  
  // LOCAL AXES for panel (X=red, Y=green, Z=blue)
  const panelAxes = new BABYLON.AxesViewer(scene, 0.5);  // 0.5 = axis length
  panelAxes.xAxis.parent = panel;
  panelAxes.yAxis.parent = panel;
  panelAxes.zAxis.parent = panel;
  
  const panelMat = new BABYLON.StandardMaterial('panelMat', scene);
  panelMat.diffuseColor = new BABYLON.Color3(0.12, 0.12, 0.15);
  panelMat.specularColor = new BABYLON.Color3(0.3, 0.3, 0.35);
  panelMat.specularPower = 100; // Glossy black panel
  panel.material = panelMat;
  
  // === THEREMINI-STYLE CONTROLS (as children of panel) ===
  
  // Knob material
  const knobMat = new BABYLON.StandardMaterial('knobMat', scene);
  knobMat.diffuseColor = new BABYLON.Color3(0.2, 0.2, 0.22);
  knobMat.specularColor = new BABYLON.Color3(0.4, 0.4, 0.45);
  knobMat.specularPower = 80;
  
  // Button material
  const buttonMat = new BABYLON.StandardMaterial('buttonMat', scene);
  buttonMat.diffuseColor = new BABYLON.Color3(0.15, 0.15, 0.18);
  buttonMat.specularColor = new BABYLON.Color3(0.3, 0.3, 0.35);
  
  // LCD Display material
  const lcdMat = new BABYLON.StandardMaterial('lcdMat', scene);
  lcdMat.diffuseColor = new BABYLON.Color3(0.05, 0.15, 0.1);
  lcdMat.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.2);
  
  // Orange indicator material
  const indicatorMat = new BABYLON.StandardMaterial('indicatorMat', scene);
  indicatorMat.emissiveColor = new BABYLON.Color3(0.9, 0.5, 0.1);
  
  // All positions are RELATIVE to panel (local coordinates)
  const controlDepth = 0.08;  // Distance from panel surface
  
  // LEFT SIDE: Volume Knob
  const volumeKnob = BABYLON.MeshBuilder.CreateCylinder(
    'volumeKnob',
    { height: 0.18, diameterTop: 0.15, diameterBottom: 0.18, tessellation: 32 },
    scene
  );
  volumeKnob.position = new BABYLON.Vector3(-1.0, 0.15, controlDepth);
  volumeKnob.rotation.x = Math.PI / 2;
  volumeKnob.material = knobMat;
  volumeKnob.parent = panel;
  
  // Volume indicator
  const volIndicator = BABYLON.MeshBuilder.CreateBox(
    'volIndicator',
    { width: 0.03, height: 0.08, depth: 0.01 },
    scene
  );
  volIndicator.position = new BABYLON.Vector3(-1.0, 0.15, controlDepth + 0.1);
  volIndicator.material = indicatorMat;
  volIndicator.parent = panel;
  
  // Pitch Correction Knob
  const pitchCorrKnob = BABYLON.MeshBuilder.CreateCylinder(
    'pitchCorrKnob',
    { height: 0.18, diameterTop: 0.15, diameterBottom: 0.18, tessellation: 32 },
    scene
  );
  pitchCorrKnob.position = new BABYLON.Vector3(-0.5, 0.15, controlDepth);
  pitchCorrKnob.rotation.x = Math.PI / 2;
  pitchCorrKnob.material = knobMat;
  pitchCorrKnob.parent = panel;
  
  // Pitch correction indicator
  const pitchIndicator = BABYLON.MeshBuilder.CreateBox(
    'pitchIndicator',
    { width: 0.03, height: 0.08, depth: 0.01 },
    scene
  );
  pitchIndicator.position = new BABYLON.Vector3(-0.5, 0.15, controlDepth + 0.1);
  pitchIndicator.material = indicatorMat;
  pitchIndicator.parent = panel;
  
  // CENTER: LCD Display
  const lcdDisplay = BABYLON.MeshBuilder.CreateBox(
    'lcdDisplay',
    { width: 0.5, height: 0.25, depth: 0.02 },
    scene
  );
  lcdDisplay.position = new BABYLON.Vector3(0, 0.1, controlDepth);
  lcdDisplay.material = lcdMat;
  lcdDisplay.parent = panel;
  
  // BUTTONS (below LCD)
  const buttonNames = ['SCALE', 'ROOT', 'EFFECT', 'SETUP'];
  for (let i = 0; i < 4; i++) {
    const button = BABYLON.MeshBuilder.CreateCylinder(
      `button_${buttonNames[i]}`,
      { height: 0.04, diameter: 0.08, tessellation: 16 },
      scene
    );
    const xPos = -0.18 + (i * 0.12);
    button.position = new BABYLON.Vector3(xPos, -0.12, controlDepth);
    button.rotation.x = Math.PI / 2;
    button.material = buttonMat;
    button.parent = panel;
  }
  
  // RIGHT SIDE: Effect Amount Knob
  const effectKnob = BABYLON.MeshBuilder.CreateCylinder(
    'effectKnob',
    { height: 0.18, diameterTop: 0.15, diameterBottom: 0.18, tessellation: 32 },
    scene
  );
  effectKnob.position = new BABYLON.Vector3(0.5, 0.15, controlDepth);
  effectKnob.rotation.x = Math.PI / 2;
  effectKnob.material = knobMat;
  effectKnob.parent = panel;
  
  // Effect indicator
  const effectIndicator = BABYLON.MeshBuilder.CreateBox(
    'effectIndicator',
    { width: 0.03, height: 0.08, depth: 0.01 },
    scene
  );
  effectIndicator.position = new BABYLON.Vector3(0.5, 0.15, controlDepth + 0.1);
  effectIndicator.material = indicatorMat;
  effectIndicator.parent = panel;
  
  // Presets Knob
  const presetsKnob = BABYLON.MeshBuilder.CreateCylinder(
    'presetsKnob',
    { height: 0.18, diameterTop: 0.15, diameterBottom: 0.18, tessellation: 32 },
    scene
  );
  presetsKnob.position = new BABYLON.Vector3(1.0, 0.15, controlDepth);
  presetsKnob.rotation.x = Math.PI / 2;
  presetsKnob.material = knobMat;
  presetsKnob.parent = panel;
  
  // Presets indicator
  const presetsIndicator = BABYLON.MeshBuilder.CreateBox(
    'presetsIndicator',
    { width: 0.03, height: 0.08, depth: 0.01 },
    scene
  );
  presetsIndicator.position = new BABYLON.Vector3(1.0, 0.15, controlDepth + 0.1);
  presetsIndicator.material = indicatorMat;
  presetsIndicator.parent = panel;
  
  // === WAVEFORM SELECTOR (bottom center) ===
  // Invisible picking zone (larger for easier clicking)
  const waveformPickingZone = BABYLON.MeshBuilder.CreateCylinder(
    'waveformKnob',  // SAME NAME as visible knob for click detection
    { height: 0.25, diameter: 0.35, tessellation: 32 },
    scene
  );
  waveformPickingZone.position = new BABYLON.Vector3(0, -0.22, controlDepth);
  waveformPickingZone.rotation.x = Math.PI / 2;
  waveformPickingZone.isVisible = false;  // Invisible but pickable
  waveformPickingZone.parent = panel;
  
  // Main knob (visible)
  const waveformKnobVisible = BABYLON.MeshBuilder.CreateCylinder(
    'waveformKnobVisible',
    { height: 0.22, diameterTop: 0.20, diameterBottom: 0.24, tessellation: 32 },
    scene
  );
  waveformKnobVisible.position = new BABYLON.Vector3(0, -0.22, controlDepth);
  waveformKnobVisible.rotation.x = Math.PI / 2;
  waveformKnobVisible.material = knobMat;
  waveformKnobVisible.parent = panel;
  waveformKnob = waveformPickingZone;  // Reference for positioning
  
  // Waveform indicator (white line pointing to current position)
  waveformIndicator = BABYLON.MeshBuilder.CreateBox(
    'waveformIndicator',
    { width: 0.03, height: 0.10, depth: 0.01 },
    scene
  );
  waveformIndicator.position = new BABYLON.Vector3(0, -0.22, controlDepth + 0.12);
  const whiteIndicatorMat = new BABYLON.StandardMaterial('whiteIndicatorMat', scene);
  whiteIndicatorMat.emissiveColor = new BABYLON.Color3(0.9, 0.9, 0.9);
  waveformIndicator.material = whiteIndicatorMat;
  waveformIndicator.parent = panel;
  
  // 4 waveform decals around the knob
  const waveformDecals = [
    { angle: -135, text: '~', color: new BABYLON.Color3(0.3, 0.7, 1.0) },  // Sine (wavy)
    { angle: -45, text: '△', color: new BABYLON.Color3(0.7, 0.3, 1.0) },   // Triangle
    { angle: 45, text: '⊓', color: new BABYLON.Color3(1.0, 0.7, 0.3) },    // Square
    { angle: 135, text: '⊿', color: new BABYLON.Color3(1.0, 0.3, 0.7) }    // Sawtooth
  ];
  
  const decalRadius = 0.18;
  waveformDecals.forEach((decal, i) => {
    const angleRad = decal.angle * Math.PI / 180;
    const x = decalRadius * Math.cos(angleRad);
    const y = decalRadius * Math.sin(angleRad);
    
    // Create text plane for waveform symbol
    const textPlane = BABYLON.MeshBuilder.CreatePlane(
      `waveformDecal${i}`,
      { width: 0.10, height: 0.10 },
      scene
    );
    textPlane.position = new BABYLON.Vector3(x, -0.22 + y, controlDepth + 0.08);
    
    // Create dynamic texture for text
    const textTexture = new BABYLON.DynamicTexture(`waveformText${i}`, 128, scene);
    const textMat = new BABYLON.StandardMaterial(`waveformTextMat${i}`, scene);
    textMat.diffuseTexture = textTexture;
    textMat.emissiveColor = decal.color;
    textMat.backFaceCulling = false;
    textMat.alpha = 0.9;
    textPlane.material = textMat;
    textPlane.parent = panel;
    
    // Draw text on texture
    const ctx = textTexture.getContext();
    ctx.fillStyle = 'white';
    ctx.font = 'bold 80px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(decal.text, 64, 64);
    textTexture.update();
  });
  
  // 4 position markers around the knob
  const markerMat = new BABYLON.StandardMaterial('markerMat', scene);
  markerMat.emissiveColor = new BABYLON.Color3(0.5, 0.5, 0.6);
  
  const markerRadius = 0.12;
  const markerPositions = [
    { angle: -135, label: 'SIN' },  // Sine (bottom-left)
    { angle: -45, label: 'TRI' },   // Triangle (bottom-right)
    { angle: 45, label: 'SQR' },    // Square (top-right)
    { angle: 135, label: 'SAW' }    // Sawtooth (top-left)
  ];
  
  markerPositions.forEach((pos, i) => {
    const angleRad = pos.angle * Math.PI / 180;
    const marker = BABYLON.MeshBuilder.CreateSphere(
      `waveMarker_${i}`,
      { diameter: 0.015 },
      scene
    );
    marker.position = new BABYLON.Vector3(
      Math.cos(angleRad) * markerRadius,
      -0.22 + Math.sin(angleRad) * markerRadius,
      controlDepth + 0.12
    );
    marker.material = markerMat;
    marker.parent = panel;
  });
  
  // Support feet (3 points for stability)
  const footPositions = [
    [-1.8, 0, 1.0],   // Left front
    [1.8, 0, 1.0],    // Right front
    [0, 0, -1.2]      // Center back
  ];
  
  const footMat = new BABYLON.StandardMaterial('footMat', scene);
  footMat.diffuseColor = new BABYLON.Color3(0.15, 0.15, 0.15);
  
  footPositions.forEach((pos, i) => {
    const foot = BABYLON.MeshBuilder.CreateCylinder(
      `foot_${i}`,
      { height: 0.08, diameter: 0.3 },
      scene
    );
    foot.position = new BABYLON.Vector3(pos[0], pos[1] + 0.04, pos[2]);
    foot.material = footMat;
  });
  
  // ===== VOLUME ANTENNA (LEFT, horizontal loop - chrome) =====
  // Like real Moog Etherwave Pro
  volumeAntenna = createProfessionalLoopAntenna();
  
  // Volume antenna mount  
  const volumeMount = BABYLON.MeshBuilder.CreateCylinder(
    'volumeMount',
    { height: 0.22, diameterTop: 0.14, diameterBottom: 0.22 },
    scene
  );
  volumeMount.position = new BABYLON.Vector3(-2.09, 0.35, 0);  // Aligned with loop
  
  const mountMat = new BABYLON.StandardMaterial('mountMat', scene);
  mountMat.diffuseColor = new BABYLON.Color3(0.18, 0.18, 0.2);
  mountMat.specularColor = new BABYLON.Color3(0.4, 0.4, 0.42);
  mountMat.specularPower = 90;
  volumeMount.material = mountMat;
  
  // ===== PITCH ANTENNA SECTION (RIGHT side with horizontal arm) =====
  // Like real Moog Etherwave Pro
  
  // Horizontal arm (chrome) extending to the right - Moog style
  const pitchArm = BABYLON.MeshBuilder.CreateCylinder(
    'pitchArm',
    { height: 1.2, diameter: 0.08, tessellation: 16 },
    scene
  );
  pitchArm.rotation.z = Math.PI / 2; // Rotate to horizontal
  pitchArm.position = new BABYLON.Vector3(1.2, 0.35, 0); // Same height as body center
  
  const armChromeMat = new BABYLON.StandardMaterial('armChromeMat', scene);
  armChromeMat.diffuseColor = new BABYLON.Color3(0.88, 0.88, 0.92);
  armChromeMat.specularColor = new BABYLON.Color3(1, 1, 1);
  armChromeMat.specularPower = 256;
  pitchArm.material = armChromeMat;
  
  // Pitch antenna (RIGHT, vertical - chrome)
  pitchAntenna = BABYLON.MeshBuilder.CreateCylinder(
    'pitchAntenna',
    { height: 4.2, diameter: 0.055 },
    scene
  );
  pitchAntenna.position = new BABYLON.Vector3(1.8, 2.45, 0); // Rises from arm at body height
  pitchAntenna.isVisible = false; // HIDDEN: replaced by yellow field line
  
  const chromeMat = new BABYLON.StandardMaterial('chromeMat', scene);
  chromeMat.diffuseColor = new BABYLON.Color3(0.88, 0.88, 0.92);
  chromeMat.specularColor = new BABYLON.Color3(1, 1, 1);
  chromeMat.specularPower = 256; // Mirror-like chrome
  pitchAntenna.material = chromeMat;
  
  // Pitch antenna ball tip (decorative) - KEPT VISIBLE
  const pitchTip = BABYLON.MeshBuilder.CreateSphere(
    'pitchTip',
    { diameter: 0.18 },
    scene
  );
  pitchTip.position = new BABYLON.Vector3(1.8, 4.0, 0);  // Top of yellow line (PITCH_CURSOR_MAX_Y)
  pitchTip.material = chromeMat;
  
  // Pitch antenna base mount (tapered cylinder)
  const pitchMount = BABYLON.MeshBuilder.CreateCylinder(
    'pitchMount',
    { height: 0.22, diameterTop: 0.14, diameterBottom: 0.22 },
    scene
  );
  pitchMount.position = new BABYLON.Vector3(1.8, 0.35, 0);  // At body height
  pitchMount.material = mountMat;
}

function createProfessionalLoopAntenna() {
  // Professional loop antenna for VOLUME (LEFT side)
  // Horizontal orientation like Moog Etherwave Pro
  const loop = BABYLON.MeshBuilder.CreateTorus(
    'volumeAntenna',  // Now volume, not pitch!
    { diameter: 1.6, thickness: 0.075, tessellation: 64 },  // 50% thicker tube
    scene
  );
  loop.position = new BABYLON.Vector3(-2.09, 0.845, 0);  // Centered on body height (0.35 + 0.99/2)
  // No rotation - loop stays flat/horizontal, extending the body laterally
  
  const chromeMat = new BABYLON.StandardMaterial('loopChromeMat', scene);
  chromeMat.diffuseColor = new BABYLON.Color3(0.88, 0.88, 0.92);
  chromeMat.specularColor = new BABYLON.Color3(1, 1, 1);
  chromeMat.specularPower = 256; // Mirror chrome
  loop.material = chromeMat;
  
  return loop;
}

function createPitchCursor() {
  // Green disc for pitch control (RIGHT side - vertical antenna)
  pitchCursor = BABYLON.MeshBuilder.CreateCylinder(
    'pitchCursor',
    { 
      height: 0.12,      // Flat disc
      diameter: 0.6,
      tessellation: 32 
    },
    scene
  );
  pitchCursor.position = new BABYLON.Vector3(
    1.8,   // RIGHT side - ALIGNED with pitch antenna X
    2.5,   // Middle height
    0      // ALIGNED with pitch antenna Z
  );
  pitchCursor.isVisible = false; // HIDDEN: replaced by pitch control circle
  
  const pitchCursorMat = new BABYLON.StandardMaterial('pitchCursorMat', scene);
  pitchCursorMat.diffuseColor = new BABYLON.Color3(0.3, 0.8, 0.3);  // Green
  pitchCursorMat.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.1);
  pitchCursorMat.specularColor = new BABYLON.Color3(0.5, 0.5, 0.5);
  pitchCursor.material = pitchCursorMat;
  
  // Enlarged picking zone (invisible sphere for easier selection)
  const pickingSphere = BABYLON.MeshBuilder.CreateSphere(
    'pitchPickingZone',
    { diameter: 2.0 },  // Reasonable size for good picking
    scene
  );
  pickingSphere.position = new BABYLON.Vector3(0, 0.3, 0);  // Offset upward for better coverage
  pickingSphere.isVisible = false;  // Invisible in production
  pickingSphere.isPickable = false; // DISABLED: now using yellow line for picking
  pickingSphere.parent = pitchCursor;  // Follows cursor automatically
  
  pitchCursor.isPickable = true;
  
  // Add glow layer effect
  const gl = new BABYLON.GlowLayer('pitchGlow', scene);
  gl.addIncludedOnlyMesh(pitchCursor);
  gl.intensity = 0.5;
  
  // Visual guide line (dashed, yellow) - REPLACES vertical rod antenna
  createDashedGuideLine(
    'pitchGuideLine',
    new BABYLON.Vector3(1.8, 0, 0),  // ALIGNED with pitch antenna position
    PITCH_CURSOR_MIN_Y,
    PITCH_CURSOR_MAX_Y,
    new BABYLON.Color3(1.0, 0.9, 0.0) // Yellow
  );
  
  // Large picking cylinder around pitch line (easier to click than thin dashed line)
  const pitchPickingCylinder = BABYLON.MeshBuilder.CreateCylinder(
    'pitchPickingCylinder',
    {
      height: PITCH_CURSOR_MAX_Y - PITCH_CURSOR_MIN_Y,
      diameter: 0.4  // Large enough to click easily
    },
    scene
  );
  const centerY = (PITCH_CURSOR_MIN_Y + PITCH_CURSOR_MAX_Y) / 2;
  pitchPickingCylinder.position = new BABYLON.Vector3(1.8, centerY, 0);
  pitchPickingCylinder.isPickable = true;
  
  // Visible semi-transparent for easier targeting
  const pickCylMat = new BABYLON.StandardMaterial('pitchPickCylMat', scene);
  pickCylMat.diffuseColor = new BABYLON.Color3(1, 1, 0);  // Yellow
  pickCylMat.alpha = 0.15;  // Very transparent
  pitchPickingCylinder.material = pickCylMat;
  pitchPickingCylinder.isVisible = true;
  
  // Pitch control circle (appears during drag, radius changes with X/Z distance)
  pitchControlCircle = BABYLON.MeshBuilder.CreateDisc(
    'pitchControlCircle',
    { radius: pitchCircleBaseRadius, tessellation: 64 },
    scene
  );
  pitchControlCircle.position = new BABYLON.Vector3(1.8, 2.5, 0); // On pitch line
  // NO rotation - CreateDisc is horizontal by default (XZ plane, parallel to grid)
  pitchControlCircle.isVisible = false; // Hidden by default
  
  // Green semi-transparent material with green outline
  const pitchCircleMat = new BABYLON.StandardMaterial('pitchCircleMat', scene);
  pitchCircleMat.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);
  pitchCircleMat.emissiveColor = new BABYLON.Color3(0.1, 0.4, 0.1);
  pitchCircleMat.alpha = 0.4;  // Semi-transparent
  pitchCircleMat.wireframe = false;
  pitchCircleMat.backFaceCulling = false; // Visible from both sides
  pitchControlCircle.material = pitchCircleMat;
  
  // Green outline (torus around circle)
  const pitchCircleOutline = BABYLON.MeshBuilder.CreateTorus(
    'pitchCircleOutline',
    { diameter: pitchCircleBaseRadius * 2, thickness: 0.02, tessellation: 64 },
    scene
  );
  pitchCircleOutline.position = new BABYLON.Vector3(0, 0, 0);
  // NO rotation - CreateTorus is also horizontal by default (XZ plane)
  pitchCircleOutline.parent = pitchControlCircle; // Follows circle
  
  const outlineMat = new BABYLON.StandardMaterial('pitchOutlineMat', scene);
  outlineMat.emissiveColor = new BABYLON.Color3(0.3, 1.0, 0.3);
  pitchCircleOutline.material = outlineMat;
  
  // Visual radius line (from antenna center to circle edge)
  // Hidden by default, shown during drag
  pitchRadiusLine = BABYLON.MeshBuilder.CreateLines(
    'pitchRadiusLine',
    {
      points: [
        new BABYLON.Vector3(0, 0, 0),  // Start at antenna (will be updated)
        new BABYLON.Vector3(0, 0, 0)   // End at circle edge (will be updated)
      ],
      updatable: true  // Can be updated during drag
    },
    scene
  );
  pitchRadiusLine.color = new BABYLON.Color3(0.3, 1.0, 0.3);  // Green
  pitchRadiusLine.isVisible = false;  // Hidden by default
}

function createVolumeCursor() {
  // Blue cylinder for volume control (LEFT side - horizontal loop)
  volumeCursor = BABYLON.MeshBuilder.CreateCylinder(
    'volumeCursor',
    { height: 0.3, diameter: 0.5 },
    scene
  );
  volumeCursor.position = new BABYLON.Vector3(
    -2.09,  // LEFT side - ALIGNED with volume antenna X
    2.0,    // Middle height
    0       // ALIGNED with volume antenna Z
  );
  
  const volumeCursorMat = new BABYLON.StandardMaterial('volumeCursorMat', scene);
  volumeCursorMat.diffuseColor = new BABYLON.Color3(0.2, 0.6, 0.9);
  volumeCursorMat.emissiveColor = new BABYLON.Color3(0.1, 0.2, 0.3);
  volumeCursorMat.specularColor = new BABYLON.Color3(0.5, 0.5, 0.5);
  volumeCursor.material = volumeCursorMat;
  
  // Enlarged invisible picking zone for better usability
  const volumePickingZone = BABYLON.MeshBuilder.CreateSphere(
    'volumePickingZone',
    { diameter: 2.0 },  // Reasonable size for good picking
    scene
  );
  volumePickingZone.position = new BABYLON.Vector3(0, 0.3, 0);  // Offset upward for better coverage
  volumePickingZone.isVisible = false;  // Invisible in production
  volumePickingZone.isPickable = true;
  volumePickingZone.parent = volumeCursor;  // Follows cursor automatically
  
  volumeCursor.isPickable = true;
  
  // Add glow layer effect
  const gl = new BABYLON.GlowLayer('volumeGlow', scene);
  gl.addIncludedOnlyMesh(volumeCursor);
  gl.intensity = 0.5;
  
  // Visual guide line (dashed, yellow) - starts at volume antenna bottom
  const volumeAntennaBottomY = 0.845 - 0.075/2;  // Antenna center - half thickness
  createDashedGuideLine(
    'volumeGuideLine',
    new BABYLON.Vector3(-2.09, 0, 0),  // ALIGNED with volume antenna
    volumeAntennaBottomY,  // Start at antenna bottom
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
// ===== XYZ AXIS HELPER =====
function createAxisHelper() {
  const axisLength = 3;
  const axisThickness = 0.05;
  const arrowLength = 0.3;
  const arrowThickness = 0.15;
  
  // X Axis (RED) - HIDDEN
  const xAxis = BABYLON.MeshBuilder.CreateCylinder(
    'xAxis',
    { height: axisLength, diameter: axisThickness },
    scene
  );
  xAxis.position = new BABYLON.Vector3(axisLength / 2, 0, 0);
  xAxis.rotation.z = -Math.PI / 2;
  xAxis.isVisible = false;  // HIDDEN
  
  const xAxisMat = new BABYLON.StandardMaterial('xAxisMat', scene);
  xAxisMat.diffuseColor = new BABYLON.Color3(1, 0, 0);
  xAxisMat.emissiveColor = new BABYLON.Color3(0.3, 0, 0);
  xAxis.material = xAxisMat;
  
  const xArrow = BABYLON.MeshBuilder.CreateCylinder(
    'xArrow',
    { height: arrowLength, diameterTop: 0, diameterBottom: arrowThickness },
    scene
  );
  xArrow.position = new BABYLON.Vector3(axisLength, 0, 0);
  xArrow.rotation.z = -Math.PI / 2;
  xArrow.material = xAxisMat;
  xArrow.isVisible = false;  // HIDDEN
  
  // Y Axis (GREEN) - HIDDEN
  const yAxis = BABYLON.MeshBuilder.CreateCylinder(
    'yAxis',
    { height: axisLength, diameter: axisThickness },
    scene
  );
  yAxis.position = new BABYLON.Vector3(0, axisLength / 2, 0);
  yAxis.isVisible = false;  // HIDDEN
  
  const yAxisMat = new BABYLON.StandardMaterial('yAxisMat', scene);
  yAxisMat.diffuseColor = new BABYLON.Color3(0, 1, 0);
  yAxisMat.emissiveColor = new BABYLON.Color3(0, 0.3, 0);
  yAxis.material = yAxisMat;
  
  const yArrow = BABYLON.MeshBuilder.CreateCylinder(
    'yArrow',
    { height: arrowLength, diameterTop: 0, diameterBottom: arrowThickness },
    scene
  );
  yArrow.position = new BABYLON.Vector3(0, axisLength, 0);
  yArrow.material = yAxisMat;
  yArrow.isVisible = false;  // HIDDEN
  
  // Z Axis (BLUE) - HIDDEN
  const zAxis = BABYLON.MeshBuilder.CreateCylinder(
    'zAxis',
    { height: axisLength, diameter: axisThickness },
    scene
  );
  zAxis.position = new BABYLON.Vector3(0, 0, axisLength / 2);
  zAxis.rotation.x = Math.PI / 2;
  zAxis.isVisible = false;  // HIDDEN
  
  const zAxisMat = new BABYLON.StandardMaterial('zAxisMat', scene);
  zAxisMat.diffuseColor = new BABYLON.Color3(0, 0, 1);
  zAxisMat.emissiveColor = new BABYLON.Color3(0, 0, 0.3);
  zAxis.material = zAxisMat;
  
  const zArrow = BABYLON.MeshBuilder.CreateCylinder(
    'zArrow',
    { height: arrowLength, diameterTop: 0, diameterBottom: arrowThickness },
    scene
  );
  zArrow.position = new BABYLON.Vector3(0, 0, axisLength);
  zArrow.rotation.x = Math.PI / 2;
  zArrow.material = zAxisMat;
  zArrow.isVisible = false;  // HIDDEN
}

// ===== ELECTROMAGNETIC FIELDS =====
function createElectromagneticFields() {
  // Pitch antenna field (horizontal loop, LEFT, green)
  createPitchField();
  
  // Volume antenna field (vertical rod, RIGHT, blue)
  createVolumeField();
}

function createPitchField() {
  // Volumetric field mesh around PITCH antenna (RIGHT, vertical rod - GREEN)
  pitchFieldMesh = BABYLON.MeshBuilder.CreateSphere(
    'pitchFieldMesh',
    { diameterX: 2.5, diameterY: 4.0, diameterZ: 2.5, segments: 16 },
    scene
  );
  pitchFieldMesh.position = new BABYLON.Vector3(1.8, 2.3, 0);  // RIGHT side - matches pitch cursor
  
  const pitchFieldMat = new BABYLON.StandardMaterial('pitchFieldMat', scene);
  pitchFieldMat.diffuseColor = new BABYLON.Color3(0.2, 0.8, 0.2);  // GREEN
  pitchFieldMat.emissiveColor = new BABYLON.Color3(0.1, 0.4, 0.1);
  pitchFieldMat.alpha = 0.15;
  pitchFieldMat.wireframe = false;
  pitchFieldMesh.material = pitchFieldMat;
  
  // CRITICAL: Disable picking to avoid blocking cursor selection
  pitchFieldMesh.isPickable = false;
}

function createVolumeField() {
  // Volumetric field mesh around VOLUME antenna (LEFT, horizontal loop - BLUE)
  volumeFieldMesh = BABYLON.MeshBuilder.CreateTorus(
    'volumeFieldMesh',
    { diameter: 2.5, thickness: 0.8, tessellation: 24 },
    scene
  );
  volumeFieldMesh.position = new BABYLON.Vector3(-2.09, 0.845, 0);  // Aligned with volume antenna height
  // No rotation needed - torus is naturally horizontal (XZ plane), aligned with loop antenna
  
  const volumeFieldMat = new BABYLON.StandardMaterial('volumeFieldMat', scene);
  volumeFieldMat.diffuseColor = new BABYLON.Color3(0.2, 0.6, 0.9);  // BLUE
  volumeFieldMat.emissiveColor = new BABYLON.Color3(0.1, 0.3, 0.5);
  volumeFieldMat.alpha = 0.15;
  volumeFieldMat.wireframe = false;
  volumeFieldMesh.material = volumeFieldMat;
  
  // CRITICAL: Disable picking to avoid blocking cursor selection
  volumeFieldMesh.isPickable = false;
  
  // NOTE: Ellipsoidal field lines removed - they don't match horizontal loop antenna geometry
  // The torus field mesh is sufficient for volume antenna visualization
}

// Update waveform from knob selector
function updateWaveform() {
  const waveformType = waveformNames[currentWaveform];
  
  // Update oscillator if it exists
  if (oscillator) {
    oscillator.type = waveformType;
  }
  
  // Update HTML select (if exists)
  const waveformSelect = document.getElementById('waveform-select');
  if (waveformSelect) {
    waveformSelect.value = waveformType;
  }
  
  // Update knob indicator rotation (4 positions: -135°, -45°, 45°, 135°)
  if (waveformIndicator) {
    const angles = [-135, -45, 45, 135];
    const angleRad = angles[currentWaveform] * Math.PI / 180;
    // Rotate indicator around Z axis (in panel's local space)
    waveformIndicator.rotation.z = angleRad;
  }
  
  console.log('Waveform changed to:', waveformType);
}

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
      // Click on PITCH cursor, guide line, or picking cylinder
      if (pickResult.pickedMesh === pitchCursor || 
          pickResult.pickedMesh.name === 'pitchPickingZone' || 
          pickResult.pickedMesh.name === 'pitchPickingCylinder' ||
          pickResult.pickedMesh.name.startsWith('pitchGuideLine_')) {
        
        // Show pitch control circle
        if (pitchControlCircle) {
          pitchControlCircle.isVisible = true;
          pitchControlCircle.position.y = pickResult.pickedPoint.y;
          
          // Show radius line
          if (pitchRadiusLine) {
            pitchRadiusLine.isVisible = true;
          }
        }
        
        // RIGHT button = Vibrato + Drag
        if (evt.button === 2) {
          evt.preventDefault();
          vibratoActive = true;
          vibratoTime = 0;
          isDraggingPitch = true;  // Allow drag with right button too
          isPitchDragging = true;
          isKeyPressed = true;
          dragStartY = evt.clientY;
          dragStartCursorY = pickResult.pickedPoint.y;
          camera.detachControl(canvas);
          canvas.style.cursor = 'ns-resize';
          console.log('Vibrato + Drag activated!');
        } 
        // LEFT button = Normal drag
        else if (evt.button === 0) {
          isDraggingPitch = true;
          isPitchDragging = true;
          isKeyPressed = true;
          dragStartY = evt.clientY;
          dragStartCursorY = pickResult.pickedPoint.y;
          camera.detachControl(canvas);
          canvas.style.cursor = 'ns-resize';
          
          // Cancel fade out if Piano Key mode active
          if (pianoKeyMode) {
            fadeOutActive = false;
          }
        }
      } 
      // Click on VOLUME cursor - NOW CONTROLLED BY KEYBOARD
      else if (pickResult.pickedMesh === volumeCursor || pickResult.pickedMesh.name === 'volumePickingZone') {
        // Volume control now uses keyboard only (Arrow Up/Down or W/S)
        console.log('Volume cursor: use keyboard controls (↑↓ or W/S)');
      }
      // Click on WAVEFORM KNOB - cycle through 4 positions
      else if (pickResult.pickedMesh && pickResult.pickedMesh.name === 'waveformKnob') {
        currentWaveform = (currentWaveform + 1) % 4; // Cycle: 0→1→2→3→0
        updateWaveform();
      }
    }
  });
  
  // Disable context menu on right-click
  canvas.addEventListener('contextmenu', (evt) => {
    evt.preventDefault();
    return false;
  });
  
  // Mouse move
  canvas.addEventListener('pointermove', (evt) => {
    if (isDraggingPitch) {
      // Get 3D position of mouse in world space using raypicking
      // Pick against all objects to get smooth continuous 3D position
      const pickResult = scene.pick(evt.clientX, evt.clientY, null, false, camera);
      
      if (pickResult.hit && pitchControlCircle) {
        const pickedPoint = pickResult.pickedPoint;
        
        // Circle stays at initial Y position from first click
        // Calculate distance from antenna position in XZ plane
        const antennaX = 1.8;
        const antennaZ = 0;
        const dx = pickedPoint.x - antennaX;
        const dz = pickedPoint.z - antennaZ;
        const distance = Math.sqrt(dx * dx + dz * dz);
        
        // Calculate ellipsoid radius at current Y height for max radius
        // Ellipsoid: diameterX=2.5, diameterY=4.0, center at Y=2.3
        const ellipsoidCenterY = 2.3;
        const ellipsoidRadiusX = 1.25;  // diameterX / 2
        const ellipsoidRadiusY = 2.0;   // diameterY / 2
        const dy = pitchControlCircle.position.y - ellipsoidCenterY;
        const normalizedY = dy / ellipsoidRadiusY;
        const ellipsoidRadiusAtY = ellipsoidRadiusX * Math.sqrt(Math.max(0, 1 - normalizedY * normalizedY));
        
        // Max radius = 2.5 × ellipsoid radius at this Y
        const maxRadiusAtY = 2.5 * ellipsoidRadiusAtY;
        
        // Clamp distance to reasonable range
        const minDist = 0.2;
        const maxDist = Math.max(0.5, maxRadiusAtY);  // Dynamic max based on Y
        const clampedDist = Math.max(minDist, Math.min(maxDist, distance));
        
        // Update circle radius based on distance - SMOOTH continuous update
        const radius = pitchCircleBaseRadius + (clampedDist / maxDist) * pitchCircleRadiusRange * 3;  // Increased range
        const scale = radius / pitchCircleBaseRadius;
        pitchControlCircle.scaling = new BABYLON.Vector3(scale, 1, scale);  // Scale in XZ plane (horizontal)
        
        // Update radius line: from antenna center to projected point on circle edge IN XZ PLANE
        if (pitchRadiusLine) {
          pitchRadiusLine.dispose();  // Remove old line
        }
        
        const antennaCenter = new BABYLON.Vector3(antennaX, pitchControlCircle.position.y, antennaZ);
        
        // Project raypicking onto circle edge in XZ plane (same Y as circle)
        const projDx = pickedPoint.x - antennaX;
        const projDz = pickedPoint.z - antennaZ;
        const projDist2D = Math.sqrt(projDx * projDx + projDz * projDz);
        
        // Normalize and scale to circle radius
        const projEdgeX = antennaX + (projDx / projDist2D) * radius;
        const projEdgeZ = antennaZ + (projDz / projDist2D) * radius;
        const edgePoint = new BABYLON.Vector3(projEdgeX, pitchControlCircle.position.y, projEdgeZ);
        
        pitchRadiusLine = BABYLON.MeshBuilder.CreateLines(
          'pitchRadiusLine',
          { points: [antennaCenter, edgePoint] },
          scene
        );
        pitchRadiusLine.color = new BABYLON.Color3(0.3, 1.0, 0.3);  // Green
        
        // Update pitch based on distance
        // Larger distance = lower pitch (grave) - INVERTED
        // Smaller distance = higher pitch (aiguë) - INVERTED
        const t = (clampedDist - minDist) / (maxDist - minDist);
        currentPitch = PITCH_MAX - t * (PITCH_MAX - PITCH_MIN); // INVERTED
        updateAudioPitch();
        updateFrequencyDisplay();
        
        // Update cursor position for other systems
        pitchCursor.position.y = pitchControlCircle.position.y;
      }
      
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
  canvas.addEventListener('pointerup', (evt) => {
    // RIGHT button release = stop vibrato + drag
    if (evt.button === 2) {
      if (vibratoActive) {
        vibratoActive = false;
        console.log('Vibrato stopped');
      }
      if (isDraggingPitch || isDraggingVolume) {  // Also check volume drag
        isDraggingPitch = false;
        isDraggingVolume = false;  // Reset volume drag too
        isPitchDragging = false;
        isKeyPressed = false;
        camera.attachControl(canvas, true);
        canvas.style.cursor = 'default';
        
        // Hide pitch control circle
        if (pitchControlCircle) {
          pitchControlCircle.isVisible = false;
        }
        
        // Hide radius line
        if (pitchRadiusLine) {
          pitchRadiusLine.isVisible = false;
        }
        
        // Piano Key mode: trigger fade out
        if (pianoKeyMode && isPlaying) {
          fadeOutActive = true;
          fadeOutStartTime = Date.now();
          console.log('Piano Key: fade out started');
        } else {
          // Normal mode: stop sound immediately when releasing mouse
          if (isPlaying) {
            stopSound();
            console.log('Sound stopped (mouse released)');
          }
        }
      }
    }
    
    // LEFT button release = end drag only
    if (evt.button === 0 && (isDraggingPitch || isDraggingVolume)) {
      isDraggingPitch = false;
      isDraggingVolume = false;
      isPitchDragging = false;
      isKeyPressed = false;
      camera.attachControl(canvas, true);
      canvas.style.cursor = 'default';
      
      // Hide pitch control circle
      if (pitchControlCircle) {
        pitchControlCircle.isVisible = false;
      }
      
      // Hide radius line
      if (pitchRadiusLine) {
        pitchRadiusLine.isVisible = false;
      }
      
      // Piano Key mode: trigger fade out
      if (pianoKeyMode && isPlaying) {
        fadeOutActive = true;
        fadeOutStartTime = Date.now();
        console.log('Piano Key: fade out started');
      } else {
        // Normal mode: stop sound immediately when releasing mouse
        if (isPlaying) {
          stopSound();
          console.log('Sound stopped (mouse released)');
        }
      }
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
  
  // Piano Key mode checkbox
  document.getElementById('piano-key-cb').addEventListener('change', (e) => {
    pianoKeyMode = e.target.checked;
    console.log('Piano Key Mode:', pianoKeyMode ? 'ON' : 'OFF');
    
    // Stop sound when activating Piano Key mode
    if (pianoKeyMode && gainNode) {
      gainNode.gain.setValueAtTime(0, audioContext.currentTime);
      isKeyPressed = false;
      console.log('Sound stopped (Piano Key mode activated)');
    }
  });
  
  // Vibrato speed slider
  document.getElementById('vibrato-speed').addEventListener('input', (e) => {
    vibratoSpeed = parseFloat(e.target.value);
    document.getElementById('vibrato-speed-val').textContent = vibratoSpeed.toFixed(1) + ' Hz';
  });
  
  // Vibrato depth slider
  document.getElementById('vibrato-depth').addEventListener('input', (e) => {
    vibratoDepth = parseFloat(e.target.value);
    document.getElementById('vibrato-depth-val').textContent = vibratoDepth.toFixed(0) + ' Hz';
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
    let finalPitch = currentPitch;
    
    // Ajouter vibrato si actif
    if (vibratoActive) {
      vibratoTime += 0.016; // ~60fps
      const vibratoOffset = Math.sin(vibratoTime * vibratoSpeed * Math.PI * 2) * vibratoDepth;
      finalPitch = currentPitch + vibratoOffset;
    }
    
    oscillator.frequency.setValueAtTime(finalPitch, audioContext.currentTime);
  }
}

function updateAudioVolume() {
  if (gainNode && isAudioInitialized) {
    let finalVolume = currentVolume;
    
    // Mode Piano Key : fade out après relâchement
    if (fadeOutActive) {
      const elapsed = (Date.now() - fadeOutStartTime) / 1000;
      if (elapsed < fadeOutDuration) {
        // Fade out linéaire
        const fadeProgress = elapsed / fadeOutDuration;
        finalVolume = currentVolume * (1 - fadeProgress);
      } else {
        // Fade out terminé
        finalVolume = 0;
        fadeOutActive = false;
        if (isPlaying) {
          stopSound();
          console.log('Piano Key: note terminée');
        }
      }
    }
    
    gainNode.gain.setValueAtTime(finalVolume, audioContext.currentTime);
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
  
  // Style selector - populate melodies when style changes
  document.getElementById('style-select').addEventListener('change', () => {
    populateMelodySelect();
  });
  
  // Initialize melody select with first category (Classical)
  populateMelodySelect();
  
  // === KEYBOARD CONTROL FOR VOLUME CURSOR ===
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'z' || e.key === 'Z') {
      volumeKeyUp = true;
      e.preventDefault(); // Prevent camera rotation
    }
    if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
      volumeKeyDown = true;
      e.preventDefault(); // Prevent camera rotation
    }
  });
  
  document.addEventListener('keyup', (e) => {
    if (e.key === 'ArrowUp' || e.key === 'z' || e.key === 'Z') {
      volumeKeyUp = false;
    }
    if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') {
      volumeKeyDown = false;
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
// Demo Mode - Melody Library (3 Categories)
// ======================================

// Melody categories structure
const MELODY_CATEGORIES = {
  classical: {
    label: "Classique",
    melodies: {
      bumblebee: "Vol du Bourdon (Rimsky-Korsakov)",
      clair: "Clair de Lune (Debussy)",
      fur_elise: "Für Elise (Beethoven)",
      gymnopédie: "Gymnopédie No.1 (Satie)",
      canon: "Canon en Ré (Pachelbel)",
      turkish: "Marche Turque (Mozart)",
      prelude: "Prélude en Do (Bach)",
      clair_lune: "Au Clair de la Lune (Trad.)",
      ode: "Ode à la Joie (Beethoven)",
      swan: "Le Cygne (Saint-Saëns)"
    }
  },
  jazz: {
    label: "Jazz",
    melodies: {
      take_five: "Take Five (Dave Brubeck)",
      autumn_leaves: "Autumn Leaves",
      blue_bossa: "Blue Bossa",
      all_blues: "All Blues (Miles Davis)",
      so_what: "So What (Miles Davis)",
      summertime: "Summertime (Gershwin)",
      fly_me: "Fly Me to the Moon",
      girl_ipanema: "Girl from Ipanema (Jobim)"
    }
  },
  brazil: {
    label: "Brazil",
    melodies: {
      ipanema: "Girl from Ipanema",
      wave: "Wave (Jobim)",
      desafinado: "Desafinado",
      mas_que_nada: "Mas Que Nada",
      aguas: "Águas de Março",
      chega: "Chega de Saudade",
      corcovado: "Corcovado (Quiet Nights)",
      samba_nota: "Samba de Uma Nota Só",
      triste: "Triste (Jobim)"
    }
  }
};

// Get melody sequence by name
function getMelodySequence(melodyName) {
  const melodies = {
    // Classical
    bumblebee: getBumblebeeMelody(),
    clair: getClairDeLuneMelody(),
    fur_elise: getFurEliseMelody(),
    gymnopédie: getGymnopedieMelody(),
    canon: getCanonMelody(),
    turkish: getTurkishMarchMelody(),
    prelude: getPreludeMelody(),
    clair_lune: getAuClairDeLaLuneMelody(),
    ode: getOdeToJoyMelody(),
    swan: getSwanMelody(),
    // Jazz
    take_five: getTakeFiveMelody(),
    autumn_leaves: getAutumnLeavesMelody(),
    blue_bossa: getBlueBossaMelody(),
    all_blues: getAllBluesMelody(),
    so_what: getSoWhatMelody(),
    summertime: getSummertimeMelody(),
    fly_me: getFlyMeMelody(),
    girl_ipanema: getGirlIpanemaMelody(),
    // Brazil
    ipanema: getGirlIpanemaMelody(),  // Same as Jazz version
    wave: getWaveMelody(),
    desafinado: getDesafinadoMelody(),
    mas_que_nada: getMasQueNadaMelody(),
    aguas: getAguasMelody(),
    chega: getChegaMelody(),
    corcovado: getCorcovadoMelody(),
    samba_nota: getSambaNotaMelody(),
    triste: getTristeMelody()
  };
  
  return melodies[melodyName] || melodies.bumblebee;
}

// Populate melody select based on selected style
function populateMelodySelect() {
  const styleSelect = document.getElementById('style-select');
  const melodySelect = document.getElementById('melody-select');
  const selectedStyle = styleSelect.value;
  
  // Clear current options
  melodySelect.innerHTML = '';
  
  // Get melodies for selected style
  const category = MELODY_CATEGORIES[selectedStyle];
  if (category) {
    Object.keys(category.melodies).forEach(key => {
      const option = document.createElement('option');
      option.value = key;
      option.textContent = category.melodies[key];
      melodySelect.appendChild(option);
    });
  }
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

// ======================================
// Jazz Repertoire
// ======================================

// 1. Take Five - Dave Brubeck (iconic 5/4 time signature theme)
function getTakeFiveMelody() {
  return [
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 400, 0.6],   // F5
    [784, 400, 0.6],   // G5
    [659, 800, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 400, 0.6],   // F5
    [784, 400, 0.6],   // G5
    [659, 800, 0.5],   // E5
    [784, 400, 0.6],   // G5
    [880, 400, 0.6],   // A5
    [784, 400, 0.6],   // G5
    [698, 400, 0.5],   // F5
    [659, 800, 0.5],   // E5
  ];
}

// 2. Autumn Leaves (Les Feuilles Mortes)
function getAutumnLeavesMelody() {
  return [
    [659, 400, 0.5],   // E5
    [698, 400, 0.5],   // F5
    [784, 600, 0.6],   // G5
    [523, 400, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 800, 0.6],   // E5
    [440, 400, 0.4],   // A4
    [494, 400, 0.5],   // B4
    [523, 800, 0.5],   // C5
    [392, 400, 0.4],   // G4
    [440, 600, 0.4],   // A4
    [494, 400, 0.5],   // B4
    [523, 800, 0.5],   // C5
  ];
}

// 3. Blue Bossa
function getBlueBossaMelody() {
  return [
    [523, 600, 0.5],   // C5
    [587, 300, 0.5],   // D5
    [659, 300, 0.6],   // E5
    [698, 600, 0.6],   // F5
    [784, 600, 0.6],   // G5
    [698, 300, 0.6],   // F5
    [659, 300, 0.5],   // E5
    [587, 600, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [440, 400, 0.4],   // A4
    [494, 400, 0.5],   // B4
    [523, 800, 0.5],   // C5
  ];
}

// 4. All Blues - Miles Davis
function getAllBluesMelody() {
  return [
    [392, 600, 0.4],   // G4
    [466, 600, 0.5],   // A#4
    [523, 600, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [523, 400, 0.5],   // C5
    [466, 600, 0.5],   // A#4
    [392, 800, 0.4],   // G4
    [392, 600, 0.4],   // G4
    [466, 600, 0.5],   // A#4
    [523, 600, 0.5],   // C5
    [587, 800, 0.5],   // D5
  ];
}

// 5. So What - Miles Davis
function getSoWhatMelody() {
  return [
    [587, 800, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 800, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.6],   // E5
    [698, 800, 0.6],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 800, 0.5],   // C5
  ];
}

// 6. Summertime - Gershwin
function getSummertimeMelody() {
  return [
    [659, 600, 0.4],   // E5
    [659, 300, 0.4],   // E5
    [698, 300, 0.5],   // F5
    [784, 600, 0.6],   // G5
    [698, 300, 0.5],   // F5
    [659, 300, 0.5],   // E5
    [587, 800, 0.5],   // D5
    [523, 600, 0.4],   // C5
    [587, 300, 0.5],   // D5
    [659, 300, 0.5],   // E5
    [698, 600, 0.5],   // F5
    [659, 300, 0.5],   // E5
    [587, 900, 0.5],   // D5
  ];
}

// 7. Fly Me to the Moon
function getFlyMeMelody() {
  return [
    [440, 600, 0.5],   // A4
    [523, 600, 0.5],   // C5
    [494, 600, 0.5],   // B4
    [440, 600, 0.5],   // A4
    [392, 800, 0.4],   // G4
    [349, 600, 0.4],   // F4
    [392, 600, 0.4],   // G4
    [440, 800, 0.5],   // A4
    [494, 600, 0.5],   // B4
    [523, 600, 0.5],   // C5
    [587, 800, 0.6],   // D5
  ];
}

// 8. Girl from Ipanema - Jobim (also in Brazil category)
function getGirlIpanemaMelody() {
  return [
    [698, 400, 0.5],   // F5
    [659, 400, 0.5],   // E5
    [698, 400, 0.5],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 800, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 600, 0.6],   // F5
    [784, 400, 0.6],   // G5
    [698, 400, 0.5],   // F5
    [659, 800, 0.5],   // E5
  ];
}

// ======================================
// Brazil / Bossa Nova Repertoire
// ======================================

// 1. Wave - Jobim
function getWaveMelody() {
  return [
    [587, 600, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 400, 0.6],   // F5
    [784, 600, 0.6],   // G5
    [880, 600, 0.6],   // A5
    [784, 400, 0.6],   // G5
    [698, 400, 0.6],   // F5
    [659, 600, 0.5],   // E5
    [587, 600, 0.5],   // D5
    [523, 800, 0.5],   // C5
  ];
}

// 2. Desafinado
function getDesafinadoMelody() {
  return [
    [523, 400, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 600, 0.6],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [494, 400, 0.5],   // B4
    [523, 400, 0.5],   // C5
    [587, 600, 0.5],   // D5
    [659, 800, 0.6],   // E5
  ];
}

// 3. Mas Que Nada
function getMasQueNadaMelody() {
  return [
    [587, 300, 0.6],   // D5
    [659, 300, 0.6],   // E5
    [698, 300, 0.6],   // F5
    [784, 300, 0.7],   // G5
    [784, 300, 0.7],   // G5
    [698, 300, 0.6],   // F5
    [659, 300, 0.6],   // E5
    [587, 300, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [587, 600, 0.5],   // D5
    [659, 800, 0.6],   // E5
  ];
}

// 4. Águas de Março
function getAguasMelody() {
  return [
    [523, 400, 0.5],   // C5
    [523, 400, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 600, 0.6],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [494, 400, 0.5],   // B4
    [440, 600, 0.4],   // A4
    [494, 800, 0.5],   // B4
  ];
}

// 5. Chega de Saudade
function getChegaMelody() {
  return [
    [659, 600, 0.5],   // E5
    [698, 400, 0.6],   // F5
    [784, 400, 0.6],   // G5
    [880, 600, 0.6],   // A5
    [784, 400, 0.6],   // G5
    [698, 400, 0.5],   // F5
    [659, 600, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 800, 0.5],   // C5
  ];
}

// 6. Corcovado (Quiet Nights)
function getCorcovadoMelody() {
  return [
    [698, 800, 0.5],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 600, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 800, 0.6],   // F5
    [784, 600, 0.6],   // G5
    [698, 400, 0.5],   // F5
    [659, 800, 0.5],   // E5
  ];
}

// 7. Samba de Uma Nota Só (One Note Samba)
function getSambaNotaMelody() {
  return [
    [587, 400, 0.5],   // D5 (the "one note")
    [587, 400, 0.5],   // D5
    [587, 400, 0.5],   // D5
    [587, 400, 0.5],   // D5
    [523, 400, 0.5],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.6],   // E5
    [698, 600, 0.6],   // F5
    [659, 400, 0.5],   // E5
    [587, 400, 0.5],   // D5
    [523, 800, 0.5],   // C5
  ];
}

// 8. Triste - Jobim
function getTristeMelody() {
  return [
    [523, 800, 0.4],   // C5
    [587, 400, 0.5],   // D5
    [659, 400, 0.5],   // E5
    [698, 800, 0.6],   // F5
    [784, 400, 0.6],   // G5
    [698, 400, 0.5],   // F5
    [659, 600, 0.5],   // E5
    [587, 600, 0.5],   // D5
    [523, 1000, 0.4],  // C5
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
  
  // If sequence finished, STOP (don't restart)
  if (targetNote === -1) {
    stopDemo();  // Stop demo instead of restarting
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
