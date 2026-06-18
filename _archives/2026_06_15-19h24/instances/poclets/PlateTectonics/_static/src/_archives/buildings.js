// Bâtiments et effet domino
function buildBuildings() {
  for (let x = -6.5; x <= -1.5; x += 0.22) {
    for (let z = -2.2; z <= 2.2; z += 0.25) {
      if (Math.random() > 0.2) continue;
      const heightLevels = Math.floor(Math.random() * 15) + 1;
      const height = 0.03 + heightLevels * 0.012;
      const width = 0.07;
      const depth = 0.07;
      const r = 0.4 + (heightLevels / 15) * 0.5;
      const g = 0.4 + (heightLevels / 15) * 0.3;
      const b = 0.5 + (heightLevels / 15) * 0.2;
      const buildingMat = mat(r, g, b, 1, 0.03, 0.03, 0.05);
      const mesh = BABYLON.MeshBuilder.CreateBox(`building_${x}_${z}`, { width: width, height: height, depth: depth }, scene);
      mesh.position = new BABYLON.Vector3(x, 0.78 + height / 2, z);
      mesh.material = buildingMat;
      mesh.isPickable = false;
      buildings.push({ mesh, cell: null, origHeight: height, heightLevels, originalY: 0.78 + height / 2 });
    }
  }
  
  setTimeout(() => {
    for (let building of buildings) {
      let minDist = Infinity;
      for (let cell of cells) {
        const dist = Math.hypot(building.mesh.position.x - cell.mesh.position.x, building.mesh.position.z - cell.mesh.position.z);
        if (dist < minDist && dist < 0.8) {
          minDist = dist;
          building.cell = cell;
        }
      }
    }
  }, 200);
}

function applyDominoEffect(epicenterCell, intensity) {
  if (!epicenterCell) return;
  const epicenterX = epicenterCell.mesh.position.x;
  const epicenterZ = epicenterCell.mesh.position.z;
  for (let building of buildings) {
    if (!building.cell) continue;
    const dx = building.mesh.position.x - epicenterX;
    const dz = building.mesh.position.z - epicenterZ;
    const distance = Math.hypot(dx, dz);
    const effectIntensity = intensity * (1 - Math.min(1, distance / 6)) * (0.6 + Math.random() * 0.6);
    if (effectIntensity > 0.1) {
      const tiltAngle = effectIntensity * 35 * (building.heightLevels / 20);
      const angle = Math.atan2(dz, dx);
      const tiltX = Math.cos(angle) * tiltAngle * Math.PI / 180;
      const tiltZ = Math.sin(angle) * tiltAngle * Math.PI / 180;
      building.mesh.rotation = new BABYLON.Vector3(tiltZ, 0, -tiltX);
      setTimeout(() => {
        if (building.mesh && !SIM.quakeActive) building.mesh.rotation = new BABYLON.Vector3(0, 0, 0);
      }, 2000);
    }
  }
}