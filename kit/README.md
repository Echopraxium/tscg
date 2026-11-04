# TSCG Kit — guided workshops

**Author:** Echopraxium with the collaboration of Claude AI

The Kit is the entry door to TSCG for curious newcomers. Each workshop is a single,
self-contained HTML page: open it in a browser, no install, no account, no AI needed.
You build a small simulation piece by piece in a node editor, guided by an optional
tutorial, and discover a systemic idea by watching it move.

| Workshop | What you build | What you discover |
|---|---|---|
| [`thermostat/`](thermostat/index.html) | a room heated by a radiator with a bimetal thermostat | negative feedback, attractor, overshoot, hysteresis trade-off |

Online: `https://echopraxium.github.io/tscg/kit/thermostat/` (copied into the site by
`cli_tools/compendium/build_compendium.py`).

## Design rules

- **Build before you read.** Each tutorial step unlocks one piece and is validated by
  the simulation itself, not by a "next" button.
- **System words first.** Pieces are named after the system (Room, Wall, Heater,
  Bimetal). Their generic TSCG names (Storage, Sink, Source, Threshold) appear only
  with the "under the hood" toggle. No scores, no monoidal notation.
- **Repairable and extensible.** Tutorial steps are data (`STEPS` in the page); the
  piece library (`PIECES`) is shared by all workshops.

## Testing with users

The **"Exporter ma session"** button downloads a JSON log (steps reached, wiring
attempts, rejected connections, prediction, timings). Ask testers to think aloud while
they play, and to send that file afterwards.

Status: **prototype 0.1.0** — tutorial steps 1–4 and a free mode. UI in French for the
first testers.
