// src/geologyData.js - Données géologiques et formes SVG par cellule (résolution 7.5°)

const GEOLOGY_DATA = {};
const CELL_SHAPES = {};

// Types de croûte possibles
const CRUST_TYPES = {
  OCEANIC: 'oceanic',
  CONTINENTAL: 'continental',
  RIDGE: 'ridge',
  SUBDUCTION: 'subduction',
  HOTSPOT: 'hotspot',
  RIFT: 'rift',
  CRATON: 'craton'
};

// Couleurs pour l'affichage
const CRUST_COLORS = {
  oceanic: '#1a5d8c',
  continental: '#5a8c5a',
  ridge: '#ff5533',
  subduction: '#2266cc',
  hotspot: '#ff3300',
  rift: '#e3b341',
  craton: '#8B6914'
};

// =============================================================
// GÉNÉRATION DE FORME SVG PAR CELLULE
// =============================================================

function generateCellSVG(lat, lon, isLand, shapeType, crustType) {
  const svgNS = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(svgNS, "svg");
  svg.setAttribute("width", "256");
  svg.setAttribute("height", "256");
  svg.setAttribute("viewBox", "0 0 256 256");
  
  let bgColor;
  switch(crustType) {
    case 'continental': bgColor = '#5a8c5a'; break;
    case 'ridge': bgColor = '#ff5533'; break;
    case 'subduction': bgColor = '#2266cc'; break;
    case 'hotspot': bgColor = '#ff3300'; break;
    case 'rift': bgColor = '#e3b341'; break;
    case 'craton': bgColor = '#8B6914'; break;
    default: bgColor = '#1a4d8c';
  }
  
  const bg = document.createElementNS(svgNS, "rect");
  bg.setAttribute("width", "256");
  bg.setAttribute("height", "256");
  bg.setAttribute("fill", bgColor);
  svg.appendChild(bg);
  
  if (isLand && shapeType) {
    const path = document.createElementNS(svgNS, "path");
    let d = "";
    
    switch(shapeType) {
      case "northAmerica":
        d = "M40,30 Q70,20 110,35 T150,60 Q160,85 140,115 Q110,135 80,125 Q50,115 35,90 Q25,65 40,30Z";
        break;
      case "southAmerica":
        d = "M100,70 Q125,60 150,80 Q165,115 145,160 Q120,185 95,165 Q80,130 90,100Z";
        break;
      case "eurasia":
        d = "M100,30 Q140,15 190,35 T230,80 Q220,115 185,130 Q150,145 125,120 Q105,95 110,60Z";
        break;
      case "africa":
        d = "M90,90 Q125,75 155,95 Q170,130 150,170 Q120,190 95,170 Q75,140 90,105Z";
        break;
      case "australia":
        d = "M170,170 Q205,155 225,180 Q220,210 195,225 Q170,215 175,185Z";
        break;
      case "greenland":
        d = "M100,20 Q130,10 160,25 Q165,50 140,65 Q110,60 100,40Z";
        break;
      case "antarctica":
        d = "M30,210 Q80,195 130,200 T200,205 Q220,220 200,235 Q150,240 80,235 Q30,230 30,210Z";
        break;
      default:
        d = "M80,80 Q120,65 150,90 Q160,125 130,150 Q95,160 75,135 Q60,105 80,80Z";
    }
    
    path.setAttribute("d", d);
    path.setAttribute("fill", "#4a7a4a");
    path.setAttribute("stroke", "#3a6a3a");
    path.setAttribute("stroke-width", "2");
    svg.appendChild(path);
    
    if (shapeType === "eurasia") {
      const mountain = document.createElementNS(svgNS, "circle");
      mountain.setAttribute("cx", "160");
      mountain.setAttribute("cy", "65");
      mountain.setAttribute("r", "10");
      mountain.setAttribute("fill", "#8B6914");
      svg.appendChild(mountain);
    }
    if (shapeType === "northAmerica") {
      const mountain = document.createElementNS(svgNS, "circle");
      mountain.setAttribute("cx", "100");
      mountain.setAttribute("cy", "60");
      mountain.setAttribute("r", "8");
      mountain.setAttribute("fill", "#8B6914");
      svg.appendChild(mountain);
    }
    if (shapeType === "southAmerica") {
      const mountain = document.createElementNS(svgNS, "circle");
      mountain.setAttribute("cx", "120");
      mountain.setAttribute("cy", "100");
      mountain.setAttribute("r", "8");
      mountain.setAttribute("fill", "#8B6914");
      svg.appendChild(mountain);
    }
  }
  
  if (crustType === 'ridge') {
    const line = document.createElementNS(svgNS, "line");
    line.setAttribute("x1", "80");
    line.setAttribute("y1", "128");
    line.setAttribute("x2", "176");
    line.setAttribute("y2", "128");
    line.setAttribute("stroke", "#ff8888");
    line.setAttribute("stroke-width", "4");
    svg.appendChild(line);
  }
  
  if (crustType === 'hotspot') {
    const hotspot = document.createElementNS(svgNS, "circle");
    hotspot.setAttribute("cx", "128");
    hotspot.setAttribute("cy", "128");
    hotspot.setAttribute("r", "12");
    hotspot.setAttribute("fill", "#ff6666");
    hotspot.setAttribute("stroke", "#ff0000");
    hotspot.setAttribute("stroke-width", "2");
    svg.appendChild(hotspot);
  }
  
  if (crustType === 'subduction') {
    const arrow = document.createElementNS(svgNS, "path");
    arrow.setAttribute("d", "M128,80 L128,176 M120,160 L128,176 L136,160");
    arrow.setAttribute("stroke", "#4488ff");
    arrow.setAttribute("stroke-width", "3");
    arrow.setAttribute("fill", "none");
    svg.appendChild(arrow);
  }
  
  return new XMLSerializer().serializeToString(svg);
}

// =============================================================
// INITIALISATION DES DONNÉES GÉOLOGIQUES (résolution 7.5°)
// =============================================================

function initGeologyData() {
  for (let lat = -90; lat <= 90; lat += 7.5) {
    for (let lon = -180; lon <= 180; lon += 7.5) {
      const key = `${lat},${lon}`;
      GEOLOGY_DATA[key] = {
        crustType: CRUST_TYPES.OCEANIC,
        crustThickness: 7,
        mantleTemperature: 1300,
        activity: 'stable',
        description: 'Deep ocean basin',
        isLand: false,
        landName: null,
        elevation: -4000,
        layerCakeType: 'oceanic'
      };
    }
  }
}

// =============================================================
// DÉFINITION DES CONTINENTS (résolution 7.5°)
// =============================================================

const CONTINENTS = {
  'North America': {
    cells: [
      { lat: 45, lon: -105 }, { lat: 45, lon: -97.5 }, { lat: 45, lon: -90 }, { lat: 45, lon: -82.5 }, { lat: 45, lon: -75 },
      { lat: 37.5, lon: -105 }, { lat: 37.5, lon: -97.5 }, { lat: 37.5, lon: -90 }, { lat: 37.5, lon: -82.5 }, { lat: 37.5, lon: -75 },
      { lat: 30, lon: -105 }, { lat: 30, lon: -97.5 }, { lat: 30, lon: -90 }, { lat: 30, lon: -82.5 }, { lat: 30, lon: -75 },
      { lat: 52.5, lon: -112.5 }, { lat: 52.5, lon: -105 }, { lat: 52.5, lon: -97.5 }, { lat: 52.5, lon: -90 },
      { lat: 60, lon: -120 }, { lat: 60, lon: -112.5 }, { lat: 60, lon: -105 }, { lat: 60, lon: -97.5 }, { lat: 60, lon: -90 },
      { lat: 22.5, lon: -97.5 }, { lat: 22.5, lon: -90 }, { lat: 15, lon: -90 }, { lat: 15, lon: -82.5 }
    ],
    type: CRUST_TYPES.CONTINENTAL,
    thickness: 38,
    shape: 'northAmerica'
  },
  'South America': {
    cells: [
      { lat: 0, lon: -60 }, { lat: 0, lon: -52.5 }, { lat: 0, lon: -45 }, { lat: 0, lon: -37.5 },
      { lat: -7.5, lon: -60 }, { lat: -7.5, lon: -52.5 }, { lat: -7.5, lon: -45 }, { lat: -7.5, lon: -37.5 },
      { lat: -15, lon: -60 }, { lat: -15, lon: -52.5 }, { lat: -15, lon: -45 }, { lat: -15, lon: -37.5 },
      { lat: -22.5, lon: -60 }, { lat: -22.5, lon: -52.5 }, { lat: -22.5, lon: -45 },
      { lat: -30, lon: -60 }, { lat: -30, lon: -52.5 }
    ],
    type: CRUST_TYPES.CONTINENTAL,
    thickness: 36,
    shape: 'southAmerica'
  },
  'Eurasia': {
    cells: [
      { lat: 45, lon: 0 }, { lat: 45, lon: 7.5 }, { lat: 45, lon: 15 }, { lat: 45, lon: 22.5 }, { lat: 45, lon: 30 },
      { lat: 45, lon: 37.5 }, { lat: 45, lon: 45 }, { lat: 45, lon: 52.5 }, { lat: 45, lon: 60 }, { lat: 45, lon: 67.5 },
      { lat: 45, lon: 75 }, { lat: 45, lon: 82.5 }, { lat: 45, lon: 90 },
      { lat: 37.5, lon: 7.5 }, { lat: 37.5, lon: 15 }, { lat: 37.5, lon: 22.5 }, { lat: 37.5, lon: 30 },
      { lat: 37.5, lon: 37.5 }, { lat: 37.5, lon: 45 }, { lat: 37.5, lon: 52.5 }, { lat: 37.5, lon: 60 },
      { lat: 37.5, lon: 67.5 }, { lat: 37.5, lon: 75 }, { lat: 37.5, lon: 82.5 }, { lat: 37.5, lon: 90 },
      { lat: 52.5, lon: 0 }, { lat: 52.5, lon: 7.5 }, { lat: 52.5, lon: 15 }, { lat: 52.5, lon: 22.5 },
      { lat: 52.5, lon: 30 }, { lat: 52.5, lon: 37.5 }, { lat: 52.5, lon: 45 }, { lat: 52.5, lon: 52.5 },
      { lat: 52.5, lon: 60 }, { lat: 52.5, lon: 67.5 }, { lat: 52.5, lon: 75 }, { lat: 60, lon: 0 },
      { lat: 60, lon: 7.5 }, { lat: 60, lon: 15 }, { lat: 60, lon: 22.5 }, { lat: 60, lon: 30 },
      { lat: 60, lon: 37.5 }, { lat: 60, lon: 45 }, { lat: 60, lon: 52.5 }, { lat: 60, lon: 60 }
    ],
    type: CRUST_TYPES.CONTINENTAL,
    thickness: 40,
    shape: 'eurasia'
  },
  'Africa': {
    cells: [
      { lat: 15, lon: 0 }, { lat: 15, lon: 7.5 }, { lat: 15, lon: 15 }, { lat: 15, lon: 22.5 }, { lat: 15, lon: 30 },
      { lat: 7.5, lon: 0 }, { lat: 7.5, lon: 7.5 }, { lat: 7.5, lon: 15 }, { lat: 7.5, lon: 22.5 }, { lat: 7.5, lon: 30 },
      { lat: 0, lon: 0 }, { lat: 0, lon: 7.5 }, { lat: 0, lon: 15 }, { lat: 0, lon: 22.5 }, { lat: 0, lon: 30 },
      { lat: -7.5, lon: 0 }, { lat: -7.5, lon: 7.5 }, { lat: -7.5, lon: 15 }, { lat: -7.5, lon: 22.5 }, { lat: -7.5, lon: 30 },
      { lat: -15, lon: 0 }, { lat: -15, lon: 7.5 }, { lat: -15, lon: 15 }, { lat: -15, lon: 22.5 }
    ],
    type: CRUST_TYPES.CONTINENTAL,
    thickness: 35,
    shape: 'africa'
  },
  'Australia': {
    cells: [
      { lat: -15, lon: 112.5 }, { lat: -15, lon: 120 }, { lat: -15, lon: 127.5 }, { lat: -15, lon: 135 }, { lat: -15, lon: 142.5 }, { lat: -15, lon: 150 },
      { lat: -22.5, lon: 112.5 }, { lat: -22.5, lon: 120 }, { lat: -22.5, lon: 127.5 }, { lat: -22.5, lon: 135 }, { lat: -22.5, lon: 142.5 }, { lat: -22.5, lon: 150 },
      { lat: -30, lon: 120 }, { lat: -30, lon: 127.5 }, { lat: -30, lon: 135 }, { lat: -30, lon: 142.5 }
    ],
    type: CRUST_TYPES.CONTINENTAL,
    thickness: 32,
    shape: 'australia'
  },
  'Antarctica': {
    cells: [
      { lat: -75, lon: -180 }, { lat: -75, lon: -172.5 }, { lat: -75, lon: -165 }, { lat: -75, lon: -157.5 },
      { lat: -75, lon: -150 }, { lat: -75, lon: -142.5 }, { lat: -75, lon: -135 }, { lat: -75, lon: -127.5 },
      { lat: -75, lon: -120 }, { lat: -75, lon: -112.5 }, { lat: -75, lon: -105 }, { lat: -75, lon: -97.5 },
      { lat: -75, lon: -90 }, { lat: -75, lon: -82.5 }, { lat: -75, lon: -75 }, { lat: -75, lon: -67.5 },
      { lat: -75, lon: -60 }, { lat: -75, lon: -52.5 }, { lat: -75, lon: -45 }, { lat: -75, lon: -37.5 },
      { lat: -75, lon: -30 }, { lat: -75, lon: -22.5 }, { lat: -75, lon: -15 }, { lat: -75, lon: -7.5 },
      { lat: -75, lon: 0 }, { lat: -75, lon: 7.5 }, { lat: -75, lon: 15 }, { lat: -75, lon: 22.5 },
      { lat: -75, lon: 30 }, { lat: -75, lon: 37.5 }, { lat: -75, lon: 45 }, { lat: -75, lon: 52.5 },
      { lat: -75, lon: 60 }, { lat: -75, lon: 67.5 }, { lat: -75, lon: 75 }, { lat: -75, lon: 82.5 },
      { lat: -75, lon: 90 }, { lat: -75, lon: 97.5 }, { lat: -75, lon: 105 }, { lat: -75, lon: 112.5 },
      { lat: -75, lon: 120 }, { lat: -75, lon: 127.5 }, { lat: -75, lon: 135 }, { lat: -75, lon: 142.5 },
      { lat: -75, lon: 150 }, { lat: -75, lon: 157.5 }
    ],
    type: CRUST_TYPES.CRATON,
    thickness: 35,
    shape: 'antarctica'
  }
};

// =============================================================
// ZONES ACTIVES
// =============================================================

const RIDGES = [
  { lat: 0, lon: -30, range: 12, name: 'Mid-Atlantic Ridge', type: CRUST_TYPES.RIDGE },
  { lat: 45, lon: -40, range: 10, name: 'North Atlantic Ridge', type: CRUST_TYPES.RIDGE },
  { lat: -30, lon: -110, range: 12, name: 'East Pacific Rise', type: CRUST_TYPES.RIDGE },
  { lat: 20, lon: 70, range: 10, name: 'Indian Ocean Ridge', type: CRUST_TYPES.RIDGE },
  { lat: 65, lon: -20, range: 8, name: 'Iceland Ridge', type: CRUST_TYPES.RIDGE }
];

const SUBDUCTIONS = [
  { lat: 35, lon: 140, range: 14, name: 'Japan Trench', type: CRUST_TYPES.SUBDUCTION },
  { lat: -20, lon: -70, range: 12, name: 'Peru-Chile Trench', type: CRUST_TYPES.SUBDUCTION },
  { lat: -30, lon: 180, range: 12, name: 'Tonga Trench', type: CRUST_TYPES.SUBDUCTION },
  { lat: 40, lon: 25, range: 10, name: 'Hellenic Arc', type: CRUST_TYPES.SUBDUCTION },
  { lat: 10, lon: 125, range: 10, name: 'Philippine Trench', type: CRUST_TYPES.SUBDUCTION }
];

const HOTSPOTS = [
  { lat: 19, lon: -155, range: 7, name: 'Hawaii Hotspot', type: CRUST_TYPES.HOTSPOT },
  { lat: 44, lon: -110, range: 7, name: 'Yellowstone Hotspot', type: CRUST_TYPES.HOTSPOT },
  { lat: -20, lon: -175, range: 7, name: 'Tonga Hotspot', type: CRUST_TYPES.HOTSPOT },
  { lat: 37, lon: 14, range: 6, name: 'Etna Hotspot', type: CRUST_TYPES.HOTSPOT }
];

const RIFTS = [
  { lat: 10, lon: 40, range: 8, name: 'East African Rift', type: CRUST_TYPES.RIFT },
  { lat: 50, lon: 100, range: 8, name: 'Baikal Rift', type: CRUST_TYPES.RIFT },
  { lat: 35, lon: -110, range: 7, name: 'Rio Grande Rift', type: CRUST_TYPES.RIFT }
];

// =============================================================
// APPLICATION DES DONNÉES AUX CELLULES
// =============================================================

function applyToCell(lat, lon, data) {
  const latStep = 7.5, lonStep = 7.5;
  for (let latCell = -90; latCell <= 90; latCell += latStep) {
    for (let lonCell = -180; lonCell <= 180; lonCell += lonStep) {
      const latDist = Math.abs(latCell - lat);
      const lonDist = Math.abs(lonCell - lon);
      const range = data.range || 12;
      if (latDist <= range && lonDist <= range) {
        const key = `${latCell},${lonCell}`;
        if (GEOLOGY_DATA[key]) {
          GEOLOGY_DATA[key].crustType = data.type;
          GEOLOGY_DATA[key].crustThickness = data.thickness || (data.type === CRUST_TYPES.CONTINENTAL ? 38 : 8);
          GEOLOGY_DATA[key].mantleTemperature = data.type === CRUST_TYPES.RIDGE ? 1500 : (data.type === CRUST_TYPES.HOTSPOT ? 1600 : 1300);
          GEOLOGY_DATA[key].activity = 'active';
          GEOLOGY_DATA[key].description = data.name;
          GEOLOGY_DATA[key].isLand = data.type === CRUST_TYPES.CONTINENTAL || data.type === CRUST_TYPES.CRATON;
          GEOLOGY_DATA[key].landName = data.name || null;
          GEOLOGY_DATA[key].layerCakeType = data.type;
          GEOLOGY_DATA[key].shapeType = data.shape || null;
        }
      }
    }
  }
}

// =============================================================
// CHARGEMENT DE TOUTES LES DONNÉES
// =============================================================

function loadGeologyData() {
  initGeologyData();
  
  for (const [name, continent] of Object.entries(CONTINENTS)) {
    for (const cell of continent.cells) {
      const key = `${cell.lat},${cell.lon}`;
      if (GEOLOGY_DATA[key]) {
        GEOLOGY_DATA[key].crustType = continent.type;
        GEOLOGY_DATA[key].crustThickness = continent.thickness;
        GEOLOGY_DATA[key].isLand = true;
        GEOLOGY_DATA[key].landName = name;
        GEOLOGY_DATA[key].description = `${name} continental crust`;
        GEOLOGY_DATA[key].elevation = 500;
        GEOLOGY_DATA[key].layerCakeType = 'continental';
        GEOLOGY_DATA[key].shapeType = continent.shape;
      }
    }
  }
  
  for (const ridge of RIDGES) applyToCell(ridge.lat, ridge.lon, ridge);
  for (const sub of SUBDUCTIONS) applyToCell(sub.lat, sub.lon, sub);
  for (const hot of HOTSPOTS) applyToCell(hot.lat, hot.lon, hot);
  for (const rift of RIFTS) applyToCell(rift.lat, rift.lon, rift);
  
  console.log("Geology data loaded for", Object.keys(GEOLOGY_DATA).length, "cells (7.5° resolution)");
}

// =============================================================
// FONCTIONS D'ACCÈS AUX DONNÉES
// =============================================================

function getGeologyData(lat, lon) {
  const latStep = 7.5, lonStep = 7.5;
  const latCell = Math.round(lat / latStep) * latStep;
  let lonCell = Math.round(lon / lonStep) * lonStep;
  if (lonCell > 180) lonCell -= 360;
  if (lonCell < -180) lonCell += 360;
  
  const key = `${latCell},${lonCell}`;
  const data = GEOLOGY_DATA[key];
  
  if (data) {
    return {
      latitude: latCell,
      longitude: lonCell,
      crustType: data.crustType,
      crustThickness: data.crustThickness,
      mantleTemperature: data.mantleTemperature,
      activity: data.activity,
      description: data.description,
      isLand: data.isLand,
      landName: data.landName,
      elevation: data.elevation || (data.isLand ? 500 : -4000),
      layerCakeType: data.layerCakeType,
      shapeType: data.shapeType,
      color: CRUST_COLORS[data.crustType] || '#1a5d8c'
    };
  }
  
  return {
    latitude: latCell,
    longitude: lonCell,
    crustType: CRUST_TYPES.OCEANIC,
    crustThickness: 7,
    mantleTemperature: 1300,
    activity: 'stable',
    description: 'Deep ocean basin',
    isLand: false,
    landName: null,
    elevation: -4000,
    layerCakeType: 'oceanic',
    shapeType: null,
    color: CRUST_COLORS.oceanic
  };
}

function getCellColor(lat, lon) {
  const data = getGeologyData(lat, lon);
  return data.color;
}

function getCellShape(lat, lon) {
  const data = getGeologyData(lat, lon);
  return { svg: null, isLand: data.isLand, shapeType: data.shapeType, crustType: data.crustType };
}

// =============================================================
// INITIALISATION
// =============================================================

loadGeologyData();

// =============================================================
// EXPOSITION GLOBALE
// =============================================================

window.getGeologyData = getGeologyData;
window.getCellColor = getCellColor;
window.getCellShape = getCellShape;
window.CRUST_TYPES = CRUST_TYPES;