# MTGWheel 3D — Documentation

## Concept

Représentation visuelle 3D interactive du **Color Pie** de Magic: The Gathering, construite avec **Three.js**. Le projet modélise les 5 couleurs de mana, leurs 10 combinaisons bicolores (5 adjacentes + 5 diagonales) et la pseudo-couleur Artifact.

---

## Structure de la scène

### Couleurs de mana primaires

| Lettre | Couleur | Hex      |
|--------|---------|----------|
| W      | White   | #C8A87A  |
| B      | Blue    | #3A7FD5  |
| K      | Black   | #2A1F28  |
| R      | Red     | #C82020  |
| G      | Green   | #1A7A40  |

> La lettre **K** est utilisée pour Black (évite la confusion avec Blue = B).

---

### Géométrie

#### Anneau principal (prisme pentagonal)
- 5 **sphères monochromes** aux sommets du pentagone (rayon R1 = 1.5) — couleurs primaires
- 5 **tubes courbes** (arcs de cercle, `TubeGeometry` + `ArcCurve`) entre chaque paire adjacente, coupés en 2 moitiés colorées
- 5 **tubes droits** (`LineCurve3`) entre chaque paire diagonale, coupés en 2 moitiés colorées
- 10 **sphères bicolores** aux milieux des arcs et des diagonales (texture canvas split gauche/droite)

#### Dodécaèdre central
- Représente la pseudo-couleur **Artifact** (incolore)
- Couleur ivoire/nacre (`#e8e4d8`)
- Positionné au centre du pentagone dans le même plan (Y1)
- Arêtes gris foncé

---

### Tailles des objets

| Objet | Taille |
|---|---|
| Sphères primaires | `0.23 × 1.08 × 1.05 ≈ 0.260` |
| Sphères bicolores | `0.23 × 0.85 × 0.91 × 0.91 ≈ 0.160` |
| Dodécaèdre Artifact | `0.22 × 0.85 ≈ 0.187` |
| Tubes arcs adjacents | rayon 0.035 |
| Tubes droits diagonaux | rayon 0.028 |

---

### Arêtes (wireframe)

La couleur des arêtes suit le **contraste de luminance** :
- Couleur sombre (Black, Blue, Red, Green) → arêtes **blanches**
- Couleur claire (White/beige) → arêtes **noires**

Formule : `lum = 0.299·R + 0.587·G + 0.114·B` → seuil à 0.45

---

### Sphères bicolores — orientation de la séparation

La ligne de séparation de chaque sphère bicolore est orientée **perpendiculairement** à la ligne reliant ses deux couleurs parentes :
- Arcs : direction `p1[i] → p1[i+1]`
- Diagonales : direction `p1[i] → p1[(i+2)%5]`

Rotation appliquée : `mesh.rotation.y = atan2(-dz/l, dx/l) + PI/2`

---

## Étapes de développement

| Étape | Description |
|---|---|
| 1 | Prisme pentagonal extrudé, 5 faces colorées, fond noir, cadre blanc |
| 2 | Deuxième prisme inscrit (milieux des arêtes), faces bicolores adjacentes |
| 3 | Troisième prisme inscrit (diagonales), faces bicolores diagonales |
| 4 | Passage aux sphères sur les sommets, arcs de cercle entre les pôles |
| 5 | Tubes courbes (arcs) pour les adjacentes, tubes droits pour les diagonales |
| 6 | Sphères bicolores aux midpoints, dodécaèdre Artifact central |
| 7 | Ajustements tailles, wireframe contrasté, orientation des séparations |

---

## Interaction

- **Drag souris / touch** → rotation libre du groupe 3D
- Pas d'auto-rotation — le modèle reste statique jusqu'à interaction

---

## Dépendances

- [Three.js r128](https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js)
- Aucune autre dépendance

---

## Fichiers

| Fichier | Description |
|---|---|
| `MTGWheel_3D_README.md` | Ce document |
| `MTGWheel_3D.js` | Code source Three.js complet (standalone, à intégrer dans une page HTML) |
