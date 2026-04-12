// Configuration globale
const CONFIG = {
  MCOLS: 16,
  MROWS: 3,
  MZDEPTHS: 4,
  TOTAL_W: 13.6,
  TOTAL_H: 1.45,
  TOTAL_D: 4.6,
  GAP: 0.03,
  DEFAULT_CONVECTION: 0.5,
  DEFAULT_SLAB_DENSITY: 0.6,
  DEFAULT_ASYMMETRY: 0,
  DEFAULT_PROPAGATION_STRENGTH: 0.8,
  DEFAULT_PROPAGATION_RADIUS: 1.88,
  CELL_COLORS: {
    normal: { r: .78, g: .14, b: .02, em_r: .12, em_g: .015, em_b: 0, al: .68 },
    hover: { r: .95, g: .55, b: .15, em_r: .35, em_g: .12, em_b: 0, al: .88 },
    select: { r: 1.0, g: 0.85, b: 0.0, em_r: 0.5, em_g: 0.4, em_b: 0, al: 1.0 },  // JAUNE D'OR
    deformed: { r: 1.0, g: .55, b: .18, em_r: .55, em_g: .18, em_b: 0, al: .92 },
    propagated: { r: .85, g: .35, b: .10, em_r: .25, em_g: .08, em_b: 0, al: .78 }
  },
  WIRE_COLORS: {
    normal: { c: null, al: .55 },
    hover: { c: null, al: .90 },
    select: { c: null, al: 1.0 },
    deformed: { c: null, al: .85 },
    propagated: { c: null, al: .70 }
  },
  LAYER_CAKE: 0x1,
  LAYER_PLANET: 0x2
};

function initWireColors() {
  if (typeof BABYLON !== 'undefined') {
    CONFIG.WIRE_COLORS.normal.c = new BABYLON.Color3(.50, .55, .65);
    CONFIG.WIRE_COLORS.hover.c = new BABYLON.Color3(.95, .75, .30);
    CONFIG.WIRE_COLORS.select.c = new BABYLON.Color3(1.0, 1.0, 1.0);
    CONFIG.WIRE_COLORS.deformed.c = new BABYLON.Color3(1.0, .70, .25);
    CONFIG.WIRE_COLORS.propagated.c = new BABYLON.Color3(.85, .55, .20);
  }
}