# ADR-WASM-003 — Multi-worker topology

**Status:** Accepted (2026-06-30)
**Scope:** `triskele-vm-wasm` only.
**Related:** ADR-WASM-001, ADR-WASM-002.

## Context

Beyond running the guest, useful capabilities were considered: monitoring (detect guest
resource leaks — `malloc` without `free`, `fopen` without `fclose` — and open streams)
and debugging (trace, observation, step/breakpoints). The question was whether these
deserve their own worker threads.

A worker is not an inherently expensive thing **when it communicates by `postMessage`**
(no SAB, no `Atomics`, no COOP/COEP). It only becomes expensive when it needs a shared
memory protocol. Monitoring and observation are *views* on VM state, not units of
execution — they need read access to emitted events, not a thread of their own per se.

## Decision

- **Now (patch 2):** a single worker — the **VM worker**. Plus the main thread as hub
  (ADR-WASM-002) and the stdin SAB.
- **Planned (later patches), via `postMessage`, not implemented yet:**
  - a **Monitoring worker** consuming telemetry events (live allocations, open `FILE*`,
    heap bytes, instruction count) emitted by the VM and aggregating/leak-detecting;
  - a **Debug worker** for trace/observation, and — only if a *blocking* breakpoint is
    wanted — a small SAB control region read by the VM at safe points.

**Admission rule (mirrors the TSCG anti-proliferation discipline):** a dedicated worker
is justified only when it performs **heavy computation** that would block the UI if run
on the main thread (e.g. continuous statistical aggregation over millions of events).
For reading counters and rendering a panel, the main thread suffices and **no extra
worker is built**. Build the worker when a compute need demands it, not before.

## Consequences

- The VM emits telemetry events into the void (`postMessage` to the hub); it knows
  nothing about monitoring or debug. Total producer/consumer decoupling.
- Capabilities stack as additive layers, each a new `postMessage` `type` plus
  (for monitoring/debug) a new region *reserved* in the SAB layout's versioning — never
  a refactor of the VM worker or the stdin path.
- Monitoring detects **guest** leaks (heap/handles tracked in `LibcState`), not JS
  leaks. The real work is exposing those counters as events, which is cheap and additive.

---

## Annexe A — Rejected alternatives (+ wake conditions)

**A.1 — Three workers from the start (VM + Monitoring + Debug), each on its own SAB.**
*Rejected because:* multiple SAB protocols and synchronization points are exactly the
recurring infrastructure debt that Worker+Atomics was chosen to avoid; and monitoring/
debug are views, not execution units, so a thread each conflates "observe" with
"execute".
*Wake condition:* build a given worker **if and when** it needs heavy computation that
would otherwise block the UI (the admission rule above).

**A.2 — No separate workers ever; monitoring/debug folded into the main thread only.**
*Rejected because:* it would cap what monitoring can do — a future heavy analytics
consumer would freeze the UI. The decision keeps the *option* of a worker open (via the
`postMessage` event stream) without building it prematurely.
*Wake condition:* this is effectively the default state until A.1's wake condition
fires; no separate trigger.

**A.3 — Workers communicate peer-to-peer instead of through the hub.**
*Rejected:* see ADR-WASM-002 / A.3 (same reasoning — topology knowledge should not
scatter across workers).
*Wake condition:* see ADR-WASM-002 / A.3.

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
