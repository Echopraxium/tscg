// État global de la simulation
const SIM = {
  running: true, t: 0, convection: 0.5,
  slabDensity: 0.6, asymmetry: 0,
  stress: 0, quakeActive: false, quakeTimer: 0, quakeCooldown: 0,
  wilsonActive: false, wilsonT: 0, wilsonPhase: -1,
  showLegend: true,
  hovCell: null, selCell: null,
  vol: { x: 0, y: 0, z: 0 }, trans: { x: 0, y: 0, z: 0 }, rot: { alpha: 0, phi: 0, omega: 0 },
  realtimeMode: true, propagationStrength: 0.8, propagationRadius: 1.88, viewMode: 'layer',
  quakeThreshold: 0.70  // Seuil de déclenchement par défaut (70%)
};

// Éléments globaux
let engine = null;
let scene = null;
let camera = null;
let psConv = null, psRidge = null, psVol = null, psQuake = null;
let slabMeshes = [], convArrows = [], faultMats = [];
let hotspotMesh = null, quakeFlash = null;
let continentalPlates = [], oceanicPlates = [], buildings = [];
let cells = [], origCellPositions = [];
let planetEarth = null, planetAtmosphere = null;
let currentVolAxis = 'x', currentTransAxis = 'x', currentRotAxis = 'alpha';