# vco_sim.py — VCO Simulation README

**TSCG Poclet Simulation · Voltage Controlled Oscillator**  
*Author: Echopraxium with the collaboration of Claude AI · TSCG v15.8.0*

---

## Description

Simulation interactive d'un **VCO (Voltage Controlled Oscillator)**, module de base d'un synthétiseur modulaire. Le VCO génère un signal audio périodique dont la fréquence est contrôlée par une tension d'entrée suivant la loi **V/Oct** (1 volt par octave).

Cette simulation est le premier outil à instancier `m2:Oscillator` (GenericConceptCombo introduit en M2 v15.8.0).

---

## Prérequis

```bash
pip install pygame numpy
```

Python 3.8 ou supérieur requis.

---

## Lancement

```bash
python vco_sim.py
```

---

## Interface

```
┌─────────────────┬──────────────────────────────┬──────────────────┐
│   LEFT (320px)  │       CENTER (620px)          │   RIGHT (340px)  │
│                 │                               │                  │
│  Sliders :      │  Oscilloscope                 │  Scores ASFID    │
│  • Frequency    │  (fenêtre 20 ms — n cycles)   │  Scores REVOI    │
│  • Amplitude    │                               │                  │
│  • Fine Tune    │  Courbe V/Oct                 │  Paramètres      │
│                 │  (loi exponentielle f=f₀×2^CV)│  live            │
│  Tabs Waveform  │  + marqueur fréquence courante│                  │
│  Bouton AUDIO   │                               │                  │
└─────────────────┴──────────────────────────────┴──────────────────┘
```

---

## Contrôles

### Sliders (panneau gauche)

| Slider | Plage | Description |
|---|---|---|
| **Frequency** | 20 – 2 000 Hz (échelle log) | Fréquence de base. Glisser vers le haut = monter en fréquence. Échelle logarithmique : chaque octave occupe la même hauteur visuelle. |
| **Amplitude** | 0 – 100 % | Volume du signal audio généré. |
| **Fine Tune** | ±100 cents | Accordage fin en centièmes de demi-ton. +100 ¢ = +1 demi-ton. |

> Les sliders se **draggent verticalement** : cliquer-glisser le curseur rond.

### Sélecteur de forme d'onde

Cliquer sur un des 4 onglets pour changer la forme d'onde :

| Forme | Harmoniques | Timbre |
|---|---|---|
| **Sine** | Fondamentale seule | Pur, flûte |
| **Square** | Impaires (1/n) | Creux, clarinette |
| **Triangle** | Impaires (1/n²) | Doux, entre sinus et carré |
| **Sawtooth** | Toutes (1/n) | Brillant, cordes/cuivres |

### Bouton AUDIO

Cliquer sur **◉ AUDIO** pour activer/désactiver la sortie sonore.

- **Vert / allumé** → son actif
- **Gris / éteint** → simulation muette (oscilloscope actif)

> ⚠️ Le son démarre muet par défaut. Penser à régler le volume système au préalable.

### Quitter

`ESC` ou fermer la fenêtre.

---

## Panneau central

### Oscilloscope
Affiche le signal sur une **fenêtre temporelle fixe de 20 ms** — comme un oscilloscope réel avec un timebase fixé. Le nombre de cycles visibles dépend directement de la fréquence :

| Fréquence | Cycles visibles |
|---|---|
| 20 Hz | 0.4 cycle (vue partielle) |
| 100 Hz | 2 cycles |
| 440 Hz (A4) | 8.8 cycles |
| 1 000 Hz | 20 cycles |
| 2 000 Hz | 40 cycles |

Les lignes verticales de la grille marquent chaque cycle complet. Le label en bas à gauche indique le nombre de cycles visibles et la fréquence ; celui de droite rappelle la fenêtre (20 ms) et l'amplitude.

### Courbe V/Oct
Visualise la **loi exponentielle** du VCO :

```
f(CV) = f₀ × 2^(CV)

f₀ = 440 Hz (A4) à CV = 0V
```

Un marqueur indique la position de la fréquence courante sur la courbe. Chaque graduation verticale représente 1 volt = 1 octave.

---

## Panneau droit

### Scores ASFID (Eagle Eye — Territory)

| Dimension | Score | Signification pour le VCO |
|---|---|---|
| **A** Attractor | 0.90 | Fréquence cible `f = f₀ × 2^CV` |
| **S** Structure | 0.75 | Circuit : intégrateur, convertisseur V/Oct, mise en forme |
| **F** Flow | 0.85 | Signal audio en sortie (±5V Eurorack) |
| **I** Information | 0.80 | Phase instantanée φ(t), sélection de forme d'onde |
| **D** Dynamics | 0.90 | Loi V/Oct — dynamique fréquentielle |

### Scores REVOI (Sphinx Eye — Map)

| Dimension | Score | Signification |
|---|---|---|
| **R** Representability | 0.90 | Formule fermée `f = f₀ × 2^CV`, séries de Fourier connues |
| **E** Evolvability | 0.85 | Extensions : FM, sync, PWM, wavetable… |
| **V** Verifiability | 0.95 | Mesurable directement : fréquencemètre, oscilloscope, FFT |
| **O** Observability | 0.95 | Signal entièrement visible sur oscilloscope |
| **I** Interoperability | 0.95 | Standard V/Oct universel (Eurorack) |

### Paramètres live
Affiche en temps réel : forme d'onde, fréquence exacte, amplitude, nom de la note (avec cents d'écart), état audio.

---

## Architecture audio

Le moteur audio utilise un **accumulateur de phase** numpy :

```
φ(t) = φ₀ + 2π × f × t / Fe
x(t) = waveform(φ(t)) × amplitude
```

Paramètres audio :
- Fréquence d'échantillonnage : **44 100 Hz**
- Résolution : **16 bits signé**
- Mode : **stéréo**
- Buffer : **2 048 frames** (~46 ms de latence)

La phase est **continue entre chunks** : pas de clics ni de discontinuités lors du changement de fréquence ou de forme d'onde.

L'oscilloscope utilise une **fenêtre temporelle fixe de 20 ms** (timebase fixe) : augmenter la fréquence fait apparaître davantage de cycles, exactement comme sur un oscilloscope réel.

---

## Contexte TSCG

```
m2:Oscillator
  ⊗⇒(Component, Process, Trajectory | trajectoryShape=Circular)
  = S ⊗ A ⊗ I ⊗ D ⊗ F

m0:VCO  rdfs:subClassOf  m2:Oscillator
```

Le VCO est le **premier poclet M0** à instancier `m2:Oscillator`, validant ce GenericConceptCombo dans le domaine Électronique / Synthèse sonore.

### Analogies transdisciplinaires

| Domaine | Analogue | Équivalent du CV |
|---|---|---|
| Biologie | Pacemaker cardiaque (nœud SA) | Tonus autonomique |
| Mécanique | Pendule à longueur variable | Contrôle de la gravité effective |
| Économie | Cycle conjoncturel | Taux d'intérêt directeur |
| Chimie | Réaction Belousov-Zhabotinsky | Débit d'injection de réactif |

---

## Fichiers associés

| Fichier | Description |
|---|---|
| `vco_sim.py` | Cette simulation |
| `M0_VCO.jsonld` | Ontologie du poclet (JSON-LD) |
| `M0_VCO_README.md` | Documentation du poclet TSCG |
| `VCO_SIM_README.md` | Ce fichier |

---

*TSCG v15.8.0 · 2026-02-27*
