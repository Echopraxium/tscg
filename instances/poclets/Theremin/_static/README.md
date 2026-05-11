# Theremin Prototype - Interactive 3D Simulation

**Author:** Echopraxium with the collaboration of Claude AI  
**Framework:** TSCG (Transdisciplinary System Construction Game)  
**Status:** Technical Prototype

## Description

This prototype demonstrates the feasibility of simulating a Theremin electronic musical instrument using web technologies. The simulation features:

- **BabylonJS 3D engine** for visualization
- **Web Audio API** for real-time sound synthesis
- **Interactive 3D cursors** for intuitive control of pitch and volume
- **Electromagnetic field visualization** (particles + volumetric meshes)
- **Standard TSCG UI layout** (header, canvas, sidebar, bottom bar)

## What is a Theremin?

The theremin is one of the earliest electronic musical instruments, invented in 1920 by Léon Theremin. It is unique because it is played without physical contact - the performer's hand movements near two antennas control the pitch and volume of the sound.

- **Right antenna (vertical):** Controls pitch (frequency) - closer hand = higher notes
- **Left antenna (horizontal loop):** Controls volume (amplitude) - hand height adjusts loudness

## Technical Implementation

### 3D Visualization (BabylonJS)

- **Theremin model:** Simplified 3D representation with base, body, and two antennas
- **Pitch cursor (green sphere):** Vertical movement controls frequency (200-1200 Hz)
- **Volume cursor (blue cylinder):** Vertical movement controls amplitude (0-80%)
- **Visual guides:** Semi-transparent vertical lines showing cursor movement range
- **Glow effects:** Applied to cursors for better visibility

#### Electromagnetic Field Visualization 🌊

**Pedagogical Feature:** The simulation visualizes the capacitive fields that make the theremin work.

**Pitch Field (Green):**
- **Volumetric mesh:** Semi-transparent ellipsoid (2.5×4.0×2.5 units) around vertical antenna
- **Particle system:** 300 particles emanating outward from antenna
- **Behavior:** Pulses and intensifies (emitRate: 80 → 150) when pitch cursor is dragged
- **Physics:** Represents the heterodyne oscillator's electromagnetic field

**Volume Field (Blue):**
- **Volumetric mesh:** Semi-transparent torus (Ø 2.5 units) around loop antenna
- **Particle system:** 300 particles flowing in circular patterns
- **Behavior:** Pulses and intensifies when volume cursor is dragged
- **Physics:** Represents the amplitude detector's capacitive field

**Implementation Details:**
- Particle texture: Glow flare with additive blending for luminous effect
- Dynamic emission rate: 80 particles/sec (idle) → 150 particles/sec (active)
- Alpha animation: Sinusoidal pulse (α = 0.15 → 0.30) during interaction
- Particle lifetime: 0.8-1.5 seconds with gradual fade-out
- Gravity simulation: Slight downward drift (-0.3 to -0.5 units/sec)

**Toggle Control:** Bottom bar "EM Fields" checkbox enables/disables visualization

### Audio Synthesis (Web Audio API)

- **OscillatorNode:** Generates the base sound wave
- **GainNode:** Controls volume/amplitude
- **Waveform types:** Sine (pure), Triangle (soft), Sawtooth (bright), Square (harsh)
- **Frequency range:** 200 Hz (G3) to 1200 Hz (D6) - approximately 2.5 octaves
- **Note detection:** Real-time conversion of frequency to musical notes (e.g., "440 Hz → A4")

### Interaction Model

Unlike a real theremin where hand proximity is detected by electromagnetic fields, this simulation uses:

1. **Click & Drag on 3D cursors:** Direct manipulation for precise control
2. **Visual feedback:** Real-time display of frequency and volume values
3. **Automatic sound start:** Audio begins when cursors are moved

**Rationale:** 3D picking without visual references is challenging, so the cursors act as both:
- Physical interaction targets (easy to click/drag)
- Visual indicators of current parameter values

## How to Use

### Prerequisites

- Modern web browser (Chrome, Firefox, Edge, Safari)
- Python 3.x installed (for local server)

### Running the Prototype

1. **Start the local server:**
   ```bash
   # On Windows
   _00_serve_theremin.bat
   
   # On Linux/Mac
   python3 -m http.server 8000
   ```

2. **Open in browser:**
   - Navigate to: `http://localhost:8000/Theremin_Prototype.html`

3. **Interact with the theremin:**
   - Click "Start Sound" button (required for browsers to enable audio)
   - Click and drag the **green sphere** (pitch cursor) up/down
   - Click and drag the **blue cylinder** (volume cursor) up/down
   - Experiment with different waveforms in the "Audio" tab

### Controls

**Camera (3D view):**
- Left click + drag: Rotate camera
- Right click + drag: Pan camera
- Scroll wheel: Zoom in/out

**Theremin:**
- Click + drag pitch cursor (green): Change note frequency
- Click + drag volume cursor (blue): Adjust volume
- Start/Stop Sound button: Toggle audio playback

**Bottom bar:**
- Reset: Return to default positions and parameters
- Auto Rotate: Automatic camera rotation around the scene
- Show Grid: Toggle ground grid visibility
- EM Fields: Toggle electromagnetic field visualization (particles + volumetric meshes)
- Start/Stop Sound: Toggle audio playback

**Audio parameters (sidebar):**
- Waveform selector: Choose sound character
- Reverb: Experimental feature (not yet implemented)

## File Structure

```
Theremin_Prototype/
├── Theremin_Prototype.html         # Main HTML structure
├── src/
│   ├── Theremin_Prototype.css      # Styling and layout
│   └── Theremin_Prototype.js       # BabylonJS scene + Web Audio logic
├── .eslintrc.json                  # ESLint configuration
├── _00_serve_theremin.bat          # Windows server script
└── README.md                       # This file
```

**Note:** CSS and JS files are in the `src/` subdirectory following TSCG standard architecture (v1.0.0+).

## Technical Details

### Audio Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Pitch | 200-1200 Hz | 440 Hz (A4) | Controlled by green cursor Y position |
| Volume | 0-80% | 50% | Controlled by blue cursor Y position |
| Waveform | 4 types | Sine | Determines timbre/sound character |

### Cursor Mappings

**Pitch Cursor (Green Sphere):**
- Y position range: 0.5 to 4.0 units
- Maps to: 200 Hz (bottom) → 1200 Hz (top)
- Musical range: ~G3 to D6

**Volume Cursor (Blue Cylinder):**
- Y position range: 0.5 to 3.5 units
- Maps to: 0% (bottom) → 80% (top)
- Note: Maximum kept at 80% to avoid distortion

### Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| BabylonJS | ✅ | ✅ | ✅ | ✅ |
| Web Audio API | ✅ | ✅ | ✅ | ✅ |
| Glow effects | ✅ | ✅ | ⚠️ (degraded) | ✅ |

⚠️ Safari may have slightly reduced visual quality for glow effects

## Known Limitations

1. **No gestural control:** Real theremins detect hand proximity; this simulation uses mouse dragging
2. **Simplified timbre:** Lacks the nuanced sound characteristics of analog theremins
3. **Latency:** ~10-50ms audio latency depending on browser and system
4. **Reverb placeholder:** Reverb checkbox is present but not yet implemented (requires impulse response)
5. **Single oscillator:** Real theremins use heterodyning (two oscillators); this uses one

## Future Enhancements (Post-Prototype)

If the prototype is validated and integrated with full TSCG pipeline:

1. **Complete TSCG ontology modeling:**
   - M0_Theremin.jsonld with ASFID/REVOI scores
   - Identification of M2 GenericConcepts (e.g., Transducer, Modulator, Attractor)
   - Full sidebar with Description, Scores, M2 Concepts, User's Guide tabs

2. **Enhanced audio features:**
   - Proper reverb implementation with impulse response
   - Filter controls (lowpass, highpass)
   - Vibrato and portamento effects
   - Recording/playback functionality

3. **Advanced visualization:**
   - Electromagnetic field visualization (particle effects)
   - Spectral analyzer display
   - Historical theremin performances overlay

4. **Educational content:**
   - Interactive tutorial mode
   - Famous theremin pieces playback
   - Physics of capacitance explanation

## Validation Checklist

- [x] BabylonJS 3D scene renders correctly
- [x] Two interactive cursors respond to mouse dragging
- [x] Web Audio API generates sound
- [x] Pitch control works (200-1200 Hz range)
- [x] Volume control works (0-80% range)
- [x] Waveform selector changes timbre
- [x] Standard TSCG UI layout implemented
- [x] Camera controls functional
- [x] Reset button restores defaults
- [x] Note name display accurate (frequency → note conversion)
- [x] Cross-browser compatibility (Chrome, Firefox, Edge)
- [x] Electromagnetic field visualization (particles + volumetric meshes)
- [x] Dynamic field intensity animation during cursor interaction
- [x] EM Fields toggle control
- [ ] Reverb effect (placeholder only)

## License & Attribution

Created by: Echopraxium with the collaboration of Claude AI  
Framework: TSCG (Transdisciplinary System Construction Game)  
Repository: https://github.com/Echopraxium/tscg

---

**Next Steps:** If this prototype validates the approach, proceed with full TSCG instance modeling using `tscg-instance-pipeline` skill to create M0_Theremin.jsonld and integrate into the TSCG framework.
