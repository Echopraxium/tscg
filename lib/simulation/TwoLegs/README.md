# lib/simulation/TwoLegs — one page per poclet (frozen)

**Author:** Echopraxium with the collaboration of Claude AI
**Status:** FROZEN, to converge to [`ThreeLegs`](../ThreeLegs/README.md). No shared
code lives here: this generation has none. Each simulation is one self-contained page
in its poclet folder; what is shared is a set of conventions, the UX controls of
`ontology/InstanceSimulations/M0_InstanceSimulation_UXControls.jsonld` (skill
`tscg-create-instance-simulation`). Physics is hard-coded in each page.

## Inventory (2026-11-14, `instances/poclets/*/static/*.html`)

| Library | Poclets |
|---|---|
| BabylonJS | MtgColorWheel, NuclearReactorsTypology, Ptoe (+ `_Previous`, `__test`), QRCodeToPocketCity, TrophicPyramid, World2DProjection |
| p5 | ExposureTriangle, FireTriangle, FourStrokeEngine, KindlebergerMinsky, NakamotoConsensus, PhaseTransition, Vco |
| vanilla JS | ColorSynthesis, CounterPoint (WebAudioFont), Transistor |
| Kit (ThreeLegs) | Thermostat — already migrated |

Scope of this inventory: poclets only (other instance families and `_static/`
prototypes not counted).

Not every TwoLegs page needs the physics engine: a page whose subject is out of the
engine's scope (`kit/ENGINE_SCOPE.md`, tier C or D: a typology, a projection, a colour
wheel) can converge to ThreeLegs for its Synoptic and its Panel / scale-model layout,
and say explicitly that it simulates no law.
