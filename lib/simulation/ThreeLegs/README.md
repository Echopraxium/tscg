# lib/simulation/ThreeLegs — the Kit generation (active)

**Author:** Echopraxium with the collaboration of Claude AI

| Folder | Content | Depends on |
|---|---|---|
| [`engine/`](engine/sim.js) | the simulation engine: generic kinds, their laws as data (`K.LAWS`), the solver's rules (`K.ENGINE`), the Model (graph + fixed-step simulation + bindings) | nothing |
| [`synoptics/`](synoptics/synoptic.js) | the Synoptic: an SVG node editor over a Model | the Kit's `i18n.js` and `icons.js` (`K.t`, `K.L`, `K.iconSvg`); **not** the engine's laws, which the host passes as the `law` option |

Users: the Kit workshops (`kit/<id>/index.src.html`) and the poclet pages built from them
(`instances/poclets/<Name>/static/src/index.src.html`), which load these files with classic
`<script>` tags; `kit/tools/bundle.js` inlines them into the published single-file pages.

What the engine can and cannot simulate: [`kit/ENGINE_SCOPE.md`](../../../kit/ENGINE_SCOPE.md).
The rule "no physics outside `K.LAWS`" is checked by `node kit/tools/check_laws.js`.

The three generations of TSCG simulations: [`../README.md`](../README.md).
