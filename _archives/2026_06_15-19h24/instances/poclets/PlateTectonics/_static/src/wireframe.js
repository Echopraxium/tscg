// Gestion des wireframes
function boxWireframe(nm, x, y, z, w, h, d, col, alpha) {
  const e = .005;
  const x1 = x - w / 2 - e, x2 = x + w / 2 + e;
  const y1 = y - h / 2 - e, y2 = y + h / 2 + e;
  const z1 = z - d / 2 - e, z2 = z + d / 2 + e;
  const edges = [
    [[x1, y1, z1], [x2, y1, z1]], [[x2, y1, z1], [x2, y1, z2]], [[x2, y1, z2], [x1, y1, z2]], [[x1, y1, z2], [x1, y1, z1]],
    [[x1, y2, z1], [x2, y2, z1]], [[x2, y2, z1], [x2, y2, z2]], [[x2, y2, z2], [x1, y2, z2]], [[x1, y2, z2], [x1, y2, z1]],
    [[x1, y1, z1], [x1, y2, z1]], [[x2, y1, z1], [x2, y2, z1]], [[x2, y1, z2], [x2, y2, z2]], [[x1, y1, z2], [x1, y2, z2]]
  ];
  return edges.map((e2, i) => {
    const l = BABYLON.MeshBuilder.CreateLines(`${nm}_w${i}`,
      { points: [new BABYLON.Vector3(...e2[0]), new BABYLON.Vector3(...e2[1])] }, scene);
    l.color = col;
    l.alpha = alpha;
    return l;
  });
}