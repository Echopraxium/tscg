# TriskeleVM — Patch 1/2: stdout reroute (printf → output sink)

**Version:** 0.3.11 → 0.3.12
**Goal:** make `printf` / `puts` / `fprintf` / `vfprintf` reach the VM output sink
(`Cpu::output`) instead of the host's `stderr` via `eprint!`. This fixes the WASM
"Hello World" that printed `Exit: 0` with no text, and is the prerequisite for the
Z-Machine (whose text output goes through C `printf`/`puts`).

**Scope:** output rerouting ONLY. `run()` signature, `error.rs`, `main.rs`,
`lib.rs` (WASM) and the HTML are deliberately untouched — the input/suspend
machinery (`fgets`, `RunStatus`, `Suspended`) is patch 2.

## Files changed (2)

### `crates/triskele-vm/src/libc/mod.rs`
1. `dispatch()` signature gains a trailing param `sink: &mut dyn Write`.
2. The 4 `eprint!` sites (Printf, Fprintf, Vfprintf, Puts) now write to `sink`:
   `let _ = sink.write_all(...); let _ = sink.flush();`
3. The 39 unit-test call sites pass a throwaway `&mut std::io::sink()`
   (tests assert the returned char count, not the output channel — unaffected).

### `crates/triskele-vm/src/cpu/mod.rs`
The 2 `crate::libc::dispatch(...)` call sites (Type R defensive path, Type I path)
pass `&mut *self.output` as the new `sink` argument.

## Why this is safe (manual review — not compile-verified in sandbox)

- **Borrows:** `dispatch(&mut self.mem, &mut self.regs, &mut self.libc_state, &mut *self.output)`
  borrows four *disjoint* fields of `self` — allowed by the borrow checker.
- **Types:** `&mut *self.output` is `&mut (dyn Write + Send)`, which coerces to the
  param type `&mut dyn Write` (dropping the `Send` auto-trait is a valid coercion).
  `&mut std::io::sink()` (`Sink: Write`) coerces likewise.
- **`use std::io::Write;`** is already in scope in `libc/mod.rs`.
- **Channel change:** native `printf` now goes to **stdout** (via `Cpu::new`'s default
  `Box::new(std::io::stdout())`) instead of stderr. The integration suites in
  `run_all_tests.py` assert **exit codes only** (`capture_output=False`), so this does
  not affect their pass/fail. `fprintf(stderr, …)` also now routes to the sink — a known
  simplification (the impl already ignored the `FILE*` arg); acceptable for the
  Z-Machine target and the current tests.
- **WASM:** `dispatch`'s `sink` and `self.output` both exist in the WASM build
  (`run_tvmx` sets `cpu.output = ArcWriter`), so `printf` now lands in the captured
  buffer returned to JS.

## Validation steps (your side)

1. `cargo build` (native) and `cargo build --target wasm32-unknown-unknown -p triskele-vm-wasm`.
2. `python run_all_tests.py --clean` — expect the **same 7 exit codes** (zero regression).
3. `cargo test -p triskele-vm` — the `printf`/`puts`/`sprintf` unit tests should still
   pass (they check char counts).
4. **The real check:** rebuild the WASM Hello World that uses `printf` and run it in the
   browser — `#output` should now show the text (e.g. `Exit: 0` followed by `Hi`),
   not `Exit: 0` alone. If it does, the reroute is validated end-to-end and confirms the
   diagnosis.

If anything fails to compile, send me the `rustc` error and I will adjust — I could not
run `cargo` in this sandbox (no Rust toolchain, and the install domains are not on the
network allow-list).

## Next (patch 2/2)

`fgets`/`getchar` syscall reading `state.pending_input` (no further `dispatch`
signature change), `RunStatus { Halted, Suspended }`, `run() -> Result<RunStatus>` with
PC rewind on suspend, `main.rs` + `lib.rs` (WASM) match arms, and the HTML input field +
JS `resume`.

---

*Authorship: Echopraxium with the collaboration of Claude AI.*
