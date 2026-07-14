# WASM Porting Progress — Z-Machine → Doom-Generic

**Living document.** Updated in the same patch that implements each step.
Not a changelog (no rolling limit) — describes the *current state*.
Frozen decision history lives in [`adr/`](adr/).

Last updated: 2026-07-02

---

## Milestone ladder

| ID | Milestone | State |
|----|-----------|-------|
| M0 | Pipeline toolchain intact — zero regression | ✅ done |
| M1 | stdout WASM — `printf`/`puts` → output sink → DOM (patch 1, v0.3.12) | ✅ done & validated |
| M2 | Worker + SAB — worker starts, `.tvmx` runs to completion, `[Exit: 0]` received (step 2, v0.3.14) | ✅ done (2026-07-02) |
| M2b | Stdout flush before `halted` — `printf` output visible without `fgets` | 🔧 next (flush fix) |
| M2c | Interactive stdin — `fgets` blocks on SAB, `<input>` row appears, line delivered | ⬜ blocked on `tsk-cc` alloca fix |
| M3 | Z-Machine v3 interpreter — loads story file, runs `print` opcodes | ⬜ |
| M4 | Z-Machine v3 — `read` opcode (interactive input) | ⬜ |
| M5 | Z-Machine v3 — `czech.z3` or equivalent conformance suite passes | ⬜ |
| M6 | A complete free Z-Machine game playable in the browser | ⬜ |
| M7 | Doom-Generic — framebuffer over SAB → `<canvas>` | ⬜ later |

### Notes on M2c
`fgets` requires a stack-allocated `char buf[256]` which clang `-O0` compiles
to `alloca [256 x i8]` + `store`/`load` via pointer. `tsk-cc` does not yet
resolve these addresses correctly (`Memory fault: addr=0x0`). Fix is in
`tsk-cc` codegen (same family as the `Z_ClearZone` spill issue).
The WASM infrastructure (worker, SAB, hub) is fully operational — M2c is a
`tsk-cc` issue, not a WASM issue.

---

## Host I/O boundary

| Direction | Native | WASM | Status |
|-----------|--------|------|--------|
| Output (`printf`/`puts`/`O_LOG`) | `std::io::stdout` / `Cpu::host` | `SabHost::out_buf` → `postMessage{type:"output"}` | ✅ done |
| Input (`fgets`/`getchar`) | `std::io::stdin` (blocks) | `Atomics.wait` on SAB (blocks) | ⬜ wired, blocked on M2c |

---

## SAB layout (versioned)

Region implemented: **stdin v1** — see ADR-WASM-002.

```
[0..4)      Int32   version = 1
[4..8)      Int32   flag    — 0=VM waiting · 1=line ready · 2=EOF
[8..12)     Int32   len     — UTF-8 byte length
[12..4108)  bytes   data    — input line (UTF-8), N=4096
```

Reserved (not yet implemented): telemetry region, debug-control region.

---

## Known issues / workarounds

**Output lost before `halted`:** `SabHost::out_buf` is not flushed after
`cpu.run()` returns because `sab_host` was moved into `cpu.host`. Fix: add a
dedicated `flush` message from `worker_entry` using the `HostIo::flush` path,
or keep `SabHost` outside the `Box` (M2b).

**`stdin` symbol undefined:** C programs referencing `stdin` as a `FILE*`
global get NULL — `tsk-libc` does not define `stdin` as a symbol. Workaround:
pass `(void*)0` as stream to `fgets`.

**`alloca` addressing (M2c blocker):** `clang -O0` generates `alloca` +
pointer arithmetic for local arrays. `tsk-cc` codegen does not resolve these
correctly. Same root cause as the `Z_ClearZone` spill issue.

---

## Confinement invariant (must always hold)

> Removing `triskele-vm-wasm` leaves `triskele-vm` compiling and passing
> the full native regression suite, unchanged.

---

## Serving requirement

Use `server.py` (not `python -m http.server`) — sends COOP/COEP headers
required for `SharedArrayBuffer`.

---

## Z-Machine target (minimal perimeter, M3→M6)

- **Version:** v3. Smallest opcode set; culturally emblematic (Zork class).
- **Implement:** Z-code decode (2OP/1OP/0OP/VAR), object table, dictionary,
  ZSCII 5-bit text + abbreviations, routine call stack (in VM linear memory),
  `print` → output sink, `read` → SAB stdin, PRNG.
- **Stub:** save/restore (Quetzal), sound, advanced screen model.
- **Avoid:** `setjmp`/`longjmp`.
- **Story file:** embed as C byte array (`xxd -i`) — no filesystem needed.
- **Copyright:** use a free story file (not Infocom Zork — still copyrighted).
- **Conformance:** `czech.z3` or equivalent for M5.

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
