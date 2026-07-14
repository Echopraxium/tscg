# ADR-WASM-002 — Worker ↔ main communication: two channels

**Status:** Accepted (2026-06-30)
**Scope:** `triskele-vm-wasm` only.
**Related:** ADR-WASM-001 (execution model), ADR-WASM-003 (topology).

## Context

The VM worker must exchange data with the main thread for several distinct purposes:
blocking stdin (must freeze the VM until input arrives), and — later — non-blocking
telemetry (leaks, open `FILE*`, counters) and debug control. These have opposite
requirements: stdin must **block**; telemetry/observation must be **non-intrusive**.

## Decision

Use **two channels**, each for what it is good at:

1. **`SharedArrayBuffer` + `Atomics`** — shared memory, synchronous, **blocking**.
   Used **only** where blocking the VM is the feature: **stdin** (and, if ever needed,
   a blocking breakpoint). Heavy (requires COOP/COEP); justified solely by the block.

2. **`postMessage`** — message passing, asynchronous, **non-blocking**, lightweight,
   no special headers. The **default** channel for everything that does not block the
   VM: telemetry events, observation, non-blocking debug.

**Rule:** `postMessage` by default; `Atomics`/SAB only for the two things that must
**block the VM** (stdin now; blocking breakpoint later, if adopted).

The **main thread acts as a hub**: workers never talk to each other directly; all
messages route through the main thread, which carries no business logic — it only
routes by `message.type`. This decouples the VM (which emits events into the void) from
any consumer (which subscribes), so consumers can be added, removed, or crash without
the VM noticing.

## SAB layout — stdin region (v1)

```
[0..4)      Int32   version = 1
[4..8)      Int32   flag    — 0 = VM waiting · 1 = line ready · 2 = EOF
[8..12)     Int32   len     — UTF-8 byte length of the line
[12..12+N)  bytes   data    — input line (UTF-8), N = 4096
```

Total = 12 + 4096 = 4108 bytes.

Protocol:

- **worker VM:** `Atomics.wait(flag, 0)` → read `len` + `data` → set `flag = 0`.
  `flag == 2` (EOF) is translated by `fgets` into a C `NULL` return.
- **main thread:** write `data` + `len` → `Atomics.store(flag, 1)` → `Atomics.notify(flag)`.
  On end-of-input (user closes input): `Atomics.store(flag, 2)` → `Atomics.notify`.

The leading `version` word lets the layout evolve (e.g. when the telemetry/debug
regions are added in later patches) without a silent breaking change.

## Consequences

- The hub is designed as an extensible router from day one (a `switch` on
  `message.type`), but in patch 2 it routes a single message kind (I/O). Adding
  telemetry/debug routing later is a new `case`, not a refactor.
- Telemetry and non-blocking debug will ride `postMessage` — no extra SAB, no extra
  COOP/COEP cost, which is why additional workers are cheap (see ADR-WASM-003).

---

## Annexe A — Rejected alternatives (+ wake conditions)

**A.1 — Single channel: everything over the SAB.**
Route stdin, telemetry and debug all through regions of one `SharedArrayBuffer`.
*Rejected because:* it forces the VM to know the layout of the telemetry/debug regions
(coupling), and pays the synchronous/`Atomics` cost for data that does not need to
block. `postMessage` decouples producer from consumer and is free of COOP/COEP for the
non-blocking traffic.
*Wake condition:* reconsider for a specific stream **if** `postMessage` serialization
throughput becomes a measured bottleneck (very high-frequency telemetry) — then that
stream, and only that one, could move to a dedicated SAB ring buffer.

**A.2 — Single channel: everything over `postMessage`.**
Drop the SAB entirely; implement stdin by yielding and resuming via `postMessage`.
*Rejected because:* `postMessage` is asynchronous and cannot block the VM, so this
collapses back into the async/suspend model rejected in ADR-WASM-001 (A.1 there).
*Wake condition:* tied to ADR-WASM-001 — only relevant if the whole execution model
moves off Worker+Atomics.

**A.3 — Direct worker-to-worker channels (`MessageChannel`) bypassing the main thread.**
Let the VM worker talk straight to a monitoring/debug worker.
*Rejected because:* it removes the central routing point, scattering topology knowledge
across workers and complicating lifecycle (who owns whom). The hub keeps the VM ignorant
of consumers.
*Wake condition:* reconsider **if** a measured need arises for a high-volume
worker-to-worker path where main-thread routing adds meaningful latency — then a direct
`MessageChannel` for that specific pair, while keeping the hub for control.

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
