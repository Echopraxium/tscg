# TSCG Kit — guided workshops

**Author:** Echopraxium with the collaboration of Claude AI

The Kit is the entry door to TSCG for curious newcomers. Each workshop is a single,
self-contained HTML page: open it in a browser, no install, no account, no AI needed.
You build a small simulation piece by piece, guided by an optional tutorial, and
discover a systemic idea by watching it move.

Start from the home page [`index.html`](index.html) and play the workshops in order: each one
adds one idea and reuses pieces from the previous one.

| # | Workshop | What you build | What you discover | New generic pieces |
|---|---|---|---|---|
| 1 | [`thermostat/`](thermostat/index.html) | a room heated by a radiator with a bimetal thermostat | a loop that corrects (negative feedback), attractor, homeostasis | Storage, Sink, Source, Threshold |
| 2 | [`larsen/`](larsen/index.html) | a room with a voice, an amplifier and a loudspeaker | a loop that reinforces (positive feedback), a threshold born from the wiring | Amplification, Transducer |
| 3 | [`tournesol/`](tournesol/index.html) | a young sunflower, a lamp, the sun and an internal clock | a loop that tracks a moving target, anticipation, domain of validity | Gradient, Clock |

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
- **Maquette** — the system itself, drawn without any number. You can act on it
  directly (open the window).

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
| `lib/sim.js` | generic kinds (storage, sink, source, threshold, amplify, transducer, gradient, clock), Model (graph + fixed-step simulation + bindings) |
| `lib/synoptic.js` | SVG node editor |
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

**Formats are still provisional (v0).** Three workshops now share the libraries; the
workshop definition and the export (`state.graph`, `state.panel`, `predictions`) can be
frozen once the first user tests have been folded in.

## Testing with users

Ask testers to think aloud while they play, without helping them, then to click
**"Exporter ma session"** and send the JSON file (steps reached, wiring attempts,
rejected connections, panel actions, bets). Note what they say spontaneously
about the Maquette and the Panneau.

Status: **prototype 0.3.0** — three workshops, each with a guided tutorial and a free mode. UI in French for the
first testers. Desktop first; usable but cramped on a phone.
