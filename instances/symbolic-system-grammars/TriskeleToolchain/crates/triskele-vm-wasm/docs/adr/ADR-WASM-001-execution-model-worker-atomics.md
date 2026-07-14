# ADR-WASM-001 — WASM execution model: Web Worker + Atomics

**Status:** Accepted (2026-06-30)
**Scope:** `triskele-vm-wasm` only. Does not affect `triskele-vm` (core) or the native host.

## Context

The browser host must run guest programs (compiled C → `.tvmx`) that perform
**blocking** standard input — e.g. `fgets`/`getchar`, as the Z-Machine does, and
later Doom's frame loop. The browser's main thread cannot block: freezing it would
hang the page. The native host has no such constraint (`std::io::stdin()` blocks the
process thread).

The core invariant must hold: the `.tvmx` is byte-identical across native, WASM and
Linux backends; all platform specificity is absorbed by the host, never by the guest.

## Decision

Run the VM inside a **dedicated Web Worker**. On a worker thread, blocking is allowed.
Blocking input is implemented with **`Atomics.wait` on a `SharedArrayBuffer` (SAB)**:

- `fgets`/`getchar` block the worker thread via `Atomics.wait` until the main thread
  writes a line into the SAB and calls `Atomics.notify`.
- This is a **real block**, exactly like `std::io::stdin().read_line()` on native.

Consequences:

- `triskele-vm::Cpu::run()` stays `Result<i32, VmError>` — **no `RunStatus::Suspended`,
  no PC rewind, no opcode re-execution**. The core does not learn that WASM exists.
- The blocking read is reached through a host-input abstraction (see ADR-WASM-002 /
  the `HostIo` boundary). The SAB-specific code (`js_sys::Atomics`, typed-array views)
  lives **inside `triskele-vm-wasm`**, never in the core.
- The page must be served with **COOP/COEP** headers
  (`Cross-Origin-Opener-Policy: same-origin`,
  `Cross-Origin-Embedder-Policy: require-corp`), because `SharedArrayBuffer` is gated
  behind cross-origin isolation. `python -m http.server` does **not** send these; a
  small dev server is provided.

## Confinement invariant (the test that keeps this honest)

> Removing the `triskele-vm-wasm` crate must leave `triskele-vm` compiling and passing
> the full native regression suite, unchanged.

As long as this holds, the WASM specificity is purely additive and this ADR is upheld.
A failure of this test is the signal that the decision has been violated.

## Consequences for the roadmap (Z-Machine → Doom)

The SAB + worker infrastructure is **not throwaway**: Doom-WASM will reuse the same
SAB mechanism for the framebuffer (worker writes pixels → main thread blits to
`<canvas>`). Building it now for the Z-Machine is the first brick of Doom, not a detour.

---

## Annexe A — Rejected alternatives (+ wake conditions)

**A.1 — Async + `Closure` (`wasm-bindgen-futures`).**
The VM stays on the main thread; `fgets` yields via an `async` function that `.await`s
a `Promise` resolved by a DOM event listener (`Closure`).
*Rejected because:* it does not eliminate the fragile callback, it merely hides it — a
mismanaged `Closure` lifetime silently freezes or leaks input on every turn (recurring
debt). It also forces `run() -> Result<RunStatus>` with `Suspended` + PC rewind in the
core, and makes the WASM execution model **diverge** from the native blocking model.
*Wake condition:* reconsider **if** COOP/COEP cannot be served in the target
environment (e.g. static hosting with no control over HTTP headers), making the SAB
setup cost exceed the async debt.

**A.2 — Raw callbacks (no async).**
`fgets` registers a JS callback; control returns to the event loop; the callback
re-enters the VM.
*Rejected because:* the control flow fragments into nested callbacks, state scatters
into captures, and adding `NeedFrame` (Doom) later becomes unmanageable. Strictly worse
than A.1 on readability for the same fundamental limitation.
*Wake condition:* none foreseen — A.1 dominates it whenever the main-thread model is
chosen at all.

**A.3 — WASI (`wasm32-wasip1`) with a non-browser runtime.**
WASI provides a real blocking `stdin`; `fgets` works unchanged, zero closures, zero
async, zero suspend.
*Rejected because:* it runs under Wasmtime/Node, **not in a web page**, which is the
stated target.
*Wake condition:* reconsider **if** the in-browser requirement is dropped (e.g. a
CLI/desktop WASM distribution becomes a goal), in which case WASI is the cleanest path
and needs no worker/SAB at all.

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
