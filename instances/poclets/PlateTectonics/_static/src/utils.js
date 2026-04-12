// Fonctions utilitaires globales
function mkDot() {
  const c = document.createElement('canvas');
  c.width = c.height = 32;
  const g = c.getContext('2d'), r = g.createRadialGradient(16, 16, 0, 16, 16, 14);
  r.addColorStop(0, 'rgba(255,255,255,1)');
  r.addColorStop(.6, 'rgba(255,255,255,.55)');
  r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r;
  g.beginPath();
  g.arc(16, 16, 14, 0, Math.PI * 2);
  g.fill();
  return c.toDataURL();
}

function mat(r, g, b, al, er, eg, eb) {
  const m = new BABYLON.StandardMaterial(`mat_${Date.now()}`, scene);
  m.diffuseColor = new BABYLON.Color3(r, g, b);
  if (al != null && al < 1) { m.alpha = al; m.backFaceCulling = false; }
  if (er != null) m.emissiveColor = new BABYLON.Color3(er, eg, eb);
  return m;
}

function box(nm, w, h, d, x, y, z, m) {
  const mesh = BABYLON.MeshBuilder.CreateBox(nm, { width: w, height: h, depth: d }, scene);
  mesh.position = new BABYLON.Vector3(x, y, z);
  mesh.isPickable = false;
  if (m) mesh.material = m;
  return mesh;
}

function setStatus(type, msg) {
  const dot = document.getElementById('sdot'), lbl = document.getElementById('slbl');
  dot.className = 'sdot';
  if (type === 'run') dot.classList.add('run');
  else if (type === 'warn') dot.classList.add('warn');
  else if (type === 'info') dot.classList.add('info');
  if (msg) lbl.textContent = msg;
}

function togglePanel(panelId) {
  const content = document.getElementById(panelId);
  const toggle = document.getElementById(panelId.replace('-content', '-toggle'));
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    content.classList.add('collapsed');
    if (toggle) toggle.textContent = '▼';
  } else {
    content.classList.remove('collapsed');
    content.classList.add('expanded');
    if (toggle) toggle.textContent = '▲';
  }
}

function toggleSection(sectionId) {
  const content = document.getElementById(sectionId);
  if (content.classList.contains('expanded')) {
    content.classList.remove('expanded');
    content.classList.add('collapsed');
  } else {
    content.classList.remove('collapsed');
    content.classList.add('expanded');
  }
}

// Exposer les fonctions globalement
window.togglePanel = togglePanel;
window.toggleSection = toggleSection;
window.setStatus = setStatus;