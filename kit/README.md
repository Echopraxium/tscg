# TSCG Kit — guided workshops

**Author:** Echopraxium with the collaboration of Claude AI

The Kit is the entry door to TSCG for curious newcomers. Each workshop is a single,
self-contained HTML page: open it in a browser, no install, no account, no AI needed.
You build a small simulation piece by piece, guided by an optional tutorial, and
discover a systemic idea by watching it move.

Start from the home page [`index.html`](index.html): it is a **map of scenarios**. The Thermostat
of a studio flat (F1) is the pivot; every other scenario starts from it through an
*articulation* that carries something over and changes one thing. *Lateral* articulations stay
at the same scale (Larsen, Drinking bird, Sunflower); *vertical* ones change scale (zoom out
to the house, zoom in to the inside of the thermostat; both still to build). The design is in
the document "TSCG Kit — Articulation des scénarios".

| # | Workshop | What you build | What you discover | New generic pieces |
|---|---|---|---|---|
| 1 | [`thermostat/`](thermostat/index.html) | a studio flat (F1) heated by a radiator with a wall thermostat | a loop that corrects (negative feedback), attractor, homeostasis | Storage, Sink, Source, Threshold |
| 2 | [`larsen/`](larsen/index.html) | a room with a voice, an amplifier and a loudspeaker | a loop that reinforces (positive feedback), a threshold born from the wiring | Amplification, Transducer |
| 3 | [`tournesol/`](tournesol/index.html) | a young sunflower, a lamp, the sun and an internal clock | a loop that tracks a moving target, anticipation, domain of validity | Gradient, Clock |
| 4 | [`oiseau/`](oiseau/index.html) | a drinking bird: head, evaporation, tilt, return, felt, glass of water | a loop with no resting place: a relaxation oscillator; the energy comes from outside (dry air) | none: the Thermostat's pieces (a Sink opened by a command, a Threshold that tips above) |

Online: `https://echopraxium.github.io/tscg/kit/`

## One interface for every workshop

```
┌──────────────────────────────┬─────────────────────────┐
│ tutorial banner              │ Maquette  (2D, no number)│
├──────────────────────────────┤                         │
│ [ Panneau | Synoptique ]     │                         │
│  Panneau : instruments       ├─────────────────────────┤
│  Synoptique : pieces + wires │ Courbes                 │
└──────────────────────────────┴─────────────────────────┘
```

- **Synoptique** — the logic: generic pieces wired by typed ports (orange = flux,
  blue = information). The graph is the single source of truth.
- **Panneau** — the instruments: gauges, sliders, toggles, lamps on a grid. Every
  instrument keeps one side fixed (lamp 2×2, toggle 3×2, gauge and slider 2×n), so
  the panel packs like Tetris. Instruments only read or write the graph.
- **Maquette** (scale model) — the system itself. You can act on it directly (open the
  window, move the microphone). Instruments that physically hang in the room (a wall
  thermostat, a thermometer) are drawn there as real objects; the Panel stays the remote
  instrument, and the Maquette still shows what it does not (radiator heat, cold draught).

The compartments are resizable with the splitters (double-click resets; the layout is
remembered per browser). The ▼ ▲ arrows change the speed and show how much simulated time
one real second covers (e.g. “12 s = 1 h”). While time runs, chevrons travel along every
wire in the direction of the flow (they reverse when a flux goes negative, and stop when
nothing flows). Every block has an icon, shown left of its name in the palette and in the
top-left corner of the block in the Synoptic; hovering a block in the palette opens a small
information compartment at the bottom of the palette (it keeps the last hovered
or selected block). The theme is dark by default (☀ / ☾ switches, remembered per browser),
and the house button, top left, goes back to the list of workshops.

The Map/Territory distinction is **never stated**: the Panneau shows only what its
instruments measure, the Maquette shows the rest, and the player rediscovers the gap by
playing. Nothing asks about it. Whether it is noticed is observed during think-aloud
tests — that is the proof of concept. "Sous le capot" reveals the generic names
(Storage, Sink, Source, Threshold) and, at the end, that the gap has a name, for those
who go further into the onion. Learning by doing first; the theory, later, names what
was already understood.

## Code layout

| Path | Role |
|---|---|
| `lib/i18n.js` | language (English default, French), theme (dark default, light), shared interface strings |
| `lib/icons.js` | line icons for blocks (`icon:` in a skin, generic kind as fallback) |
| `lib/sim.js` | generic kinds (storage, sink, source, threshold, amplify, transducer, gradient, clock), Model (graph + fixed-step simulation + bindings). Skin options: optional ports (a Sink with a `cmd` input exists only if its skin names it), `above` (a Threshold that switches on above its band), `on` (a Source on by default) |
| `lib/synoptic.js` | SVG node editor (palette + info panel, icons, animated flow chevrons) |
| `lib/panel.js` | grid of instruments |
| `lib/chart.js` | curves, configured per workshop (`W.chart`: axes, series, strips) |
| `lib/tutorial.js` | step runner (steps are data) |
| `lib/app.js` | shared shell: layout, clock, free mode, export |
| `lib/tscg-kit.css` | shared styles, light and dark |
| `<workshop>/workshop.js` | clock (time unit), skins, instruments, chart, steps, final card, Maquette drawing |
| `<workshop>/index.src.html` | source page (works directly, classic scripts) |
| `<workshop>/index.html` | **generated** single file |
| `tools/bundle.js` | inlines CSS and scripts: `node kit/tools/bundle.js kit/thermostat/index.src.html` |

The GitHub Pages build (`cli_tools/compendium/build_compendium.py`) copies `kit/` and
re-bundles every workshop, so the published page always matches the sources.

**Formats are still provisional (v0).** Four workshops now share the libraries; the
workshop definition and the export (`state.graph`, `state.panel`, `predictions`) can be
frozen once the first user tests have been folded in.

## Map of scenarios

Each `workshop.js` sets `factory.meta` next to its factory: name, one-line description, the
idea, an icon, and for every scenario but the pivot an `articulation`
(`from`, `dir`: `lateral` | `up` | `down`, `carried`, `change`, all EN/FR). The home page loads
the four `workshop.js` files (no library needed besides `lib/icons.js`) and draws the map from
these declarations; scenarios still to build are declared in the home page (`PLANNED`).

## Several blocks of the same type

Blocks of a type are numbered when there is more than one ("Room 2", `n.num`, stable).
A panel instrument aims at one block (`{node: id}` in its binding, `Model.target(bind)`); when
several blocks share a type, the panel toolbar offers one button per block. Curves and scale
models still follow the first block of a type.

## Testing with users

Ask testers to think aloud while they play, without helping them, then to click
**"Exporter ma session"** and send the JSON file (steps reached, wiring attempts,
rejected connections, panel actions, bets). Note what they say spontaneously
about the Maquette and the Panneau.

Status: **prototype 0.8.0** — four workshops, each with a guided tutorial and a free mode. UI in English and French. Desktop first; usable but cramped on a phone.

## Languages

English by default, French with the **FR / EN** button (top right of every page, and on the
home page). The choice is remembered by the browser and passed in the URL (`?lang=fr`).
Switching keeps the graph, the panel, the clock and the tutorial progress.

- Shared interface strings: `lib/i18n.js` (`K.t(key)`).
- Workshop texts: each `workshop.js` is a factory `L => ({ ... })` where every text is
  written `L("English", "Français")`; the shell rebuilds the texts on a switch.
- Scale-model drawings use `K.L(en, fr)` at draw time.
