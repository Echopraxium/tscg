# Architecture Decision Records — `triskele-vm-wasm`

Decisions specific to the WASM host. ADRs are **immutable** once accepted: a change of
direction is recorded by a **new** ADR that supersedes the old one, not by editing it.
The living state of the porting effort is tracked separately in
[`../PORTING_PROGRESS.md`](../PORTING_PROGRESS.md).

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-WASM-001](ADR-WASM-001-execution-model-worker-atomics.md) | Execution model: Web Worker + Atomics | Accepted |
| [ADR-WASM-002](ADR-WASM-002-worker-main-communication-channels.md) | Worker ↔ main communication: two channels | Accepted |
| [ADR-WASM-003](ADR-WASM-003-multi-worker-topology.md) | Multi-worker topology | Accepted |

## Convention

Each ADR ends with **Annexe A — Rejected alternatives (+ wake conditions)**. The letter
denotes order; the name carries the meaning. Other annexes (B, C…) may hold protocol
diagrams or memory layouts when needed.

A *wake condition* is the explicit signal under which a rejected option should be
reconsidered — turning a dead verdict into a dormant, reactivatable choice.

## Rejected-alternatives digest

A cross-ADR view, so a discarded option can be found without opening every file. The
source ADR's annexe holds the full reasoning.

| Rejected alternative | Source | Wake condition (reconsider if…) |
|----------------------|--------|----------------------------------|
| Async + `Closure` (main-thread, `wasm-bindgen-futures`) | 001 · A.1 | COOP/COEP cannot be served in the target environment |
| Raw callbacks (no async) | 001 · A.2 | none foreseen (dominated by 001·A.1) |
| WASI (`wasm32-wasip1`), non-browser runtime | 001 · A.3 | the in-browser requirement is dropped |
| Single channel — everything over the SAB | 002 · A.1 | a measured `postMessage` throughput bottleneck on one stream |
| Single channel — everything over `postMessage` | 002 · A.2 | the whole execution model leaves Worker+Atomics |
| Direct worker-to-worker (`MessageChannel`) | 002 · A.3 / 003 · A.3 | a measured high-volume worker-pair path where hub latency hurts |
| Three workers from the start, each on its own SAB | 003 · A.1 | a worker needs heavy computation that would block the UI |
| No separate workers ever | 003 · A.2 | (default until 003·A.1 fires) |

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
