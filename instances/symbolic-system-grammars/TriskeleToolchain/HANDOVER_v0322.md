# TriskeleToolchain — Handover v0.3.22
# Author: Echopraxium with the collaboration of Claude AI

This handover covers three subjects requested for documentation:
1. Milestone-based progress tracking for the DOOM Generic port (replacing
   percentage estimates with verifiable checkpoints)
2. Trampoline mechanism technical debt — root-cause analysis and fix options
3. Multi-platform VM architecture (Windows / Linux / WASM) — current
   coupling inventory and a proposed separation strategy

A project-level TODO (5 initiatives, priority-ordered) is at the end of
this document.

---

## Executive Summary — What Was Accomplished This Session

- **Milestone ladder (M0–M8) established** to replace percentage-based
  progress estimates, which were judged misleading given that bug
  density doesn't track lines-of-code. M0 and M1 confirmed complete (5
  DOOM modules validated, 8 regression projects passing with zero
  regressions). M2 (libc parity) scoped and ready to start. See
  section 1.
- **Trampoline mechanism's real root cause found** — not the
  "estimation/deduplication" explanation in the previous (v0.3.20)
  handover, but a genuine dual-source-of-truth bug: `LIBC_SYMBOLS`
  (Phase 0 fixed stub addresses) and `tsk-libc.tvml` (real code, linked
  as an ordinary object) silently collide on shared function names
  (`printf`, `strlen`, `strncmp`, `strncpy` confirmed on doom_wad), with
  the second silently overwriting the first. Diagnosed and quantified
  exactly (43 pre-scan count vs 29 actual, 14-symbol discrepancy fully
  attributed). Three fix options ranked; none implemented yet — this is
  analysis only, see section 2.
- **Multi-platform architecture audited from a clean baseline** — zero
  platform-conditional code exists anywhere in the workspace today.
  Full inventory of SDL2/file-I/O/timing/CLI coupling completed. A
  trait-based `DisplayBackend` separation proposed
  (`triskele-display` + `triskele-vm-sdl2` + future
  `triskele-vm-wasm`), explicitly flagged as an unvalidated proposal
  (no WASM build attempted). See section 3.
- **New tool built and validated:** `tsk-static-profiler`, a static
  M3-category histogram tool for compiled `.tobj`/`.tvmx` binaries,
  correctly added as a workspace member reusing
  `triskele_common::{TvmFile, SectionType, OpcodeCategory}` rather than
  duplicating ISA knowledge. Run against 6 real compiled-C object files
  (6597 instructions total): found `D_` dominates at 83.9%, most other
  M3 categories never appear, and no useful per-function
  differentiation exists in compiled C. This negative result directly
  motivated the high-level-language discussion below (TODO-4).
- **Conceptual groundwork laid for a high-level declarative language**
  (working name "Triskele") with M2 GenericConcepts / M1 extensions as
  primitive types, motivated by the `tsk-static-profiler` finding above
  — C has no notion of these concepts, so no compiler targeting it will
  ever produce a meaningful M3-category profile. Discussion only; no
  design work started. See TODO-4.

---

## 1. Milestone-Based Progress Tracking

### Why not a percentage?

Lines-of-code coverage does not correlate with remaining effort. `z_zone.c`
(488 lines, memory allocator) took multiple sessions and surfaced four
fundamental toolchain bugs (B15 alloca offsets, B16 spill offsets, B17
struct-field sizing, B20 register-allocation liveness). The rendering and
game-logic subsystems are still untouched — `r_*.c` + `p_*.c` alone total
~21,000 lines, with recursive BSP traversal, heavy fixed-point arithmetic,
and access patterns very different from anything validated so far. A
percentage computed today would imply a false sense of linear progress.
Below is a milestone ladder instead: each step is a binary, testable
fact — passed or not — so progress can be tracked honestly as the next
milestones are attempted.

### Milestone ladder

**M0 — Toolchain pipeline proven end-to-end ✅ DONE**
Compile C → LLVM IR → Triskele bytecode → link → execute, with correct
results on non-trivial logic (memory allocator, binary file parsing).
Evidence: doom_zzone, doom_wad both exit 255/255.

**M1 — Core support modules validated ✅ DONE (5 of ~90 source files)**

| Module | Test project | Result |
|---|---|---|
| z_zone.c (memory allocator) | doom_zzone | 255/255 ✅ |
| m_fixed.c (fixed-point math) | doom_fixed | 127/127 ✅ |
| m_fixed.c + m_random.c | doom_math | 127/127 ✅ |
| m_argv.c (CLI arg parsing) | doom_argv | 63/63 ✅ |
| w_wad.c + w_file.c + w_file_stdc.c (WAD loader) | doom_wad | 255/255 ✅ |

Additional toolchain-level regression coverage (not DOOM modules per se,
but exercising the same compiler/linker/VM): test_main (31/31), wolf3d
(15/15), test_patterns (15/15), test_select (9/9) — all passing, confirmed
with zero regressions from the B24 linker fix and the Fopen/Fread fixes
applied this session.

**M2 — libc parity (NEXT — small effort, high leverage, already scoped)**
`tsk-libc-gen` currently exposes **23 functions**. `triskele-vm`'s
`LibcSyscall` dispatch enum already defines **59 variants** — the VM-side
implementation is far ahead of what the linker can actually wire up via
trampolines, because `tsk-libc-gen`'s `LIBC_FUNCTIONS` table was never
kept in sync. **Confirmed broken today:**
- `test_variadic`: got exit 79, expected 255 — missing `vsprintf` trampoline.
- `test_doom_libc`: memory fault (`addr=0x0`) — missing `strdup`,
  `strcasecmp`, `snprintf`, and others.

This is a closed, well-defined task: enumerate the gap between the 23
exposed and the 59 implemented, add the missing entries to
`tsk-libc-gen/src/main.rs`'s `LIBC_FUNCTIONS` table. Should also be done
in coordination with the trampoline-debt fix in section 2, since both
touch the same libc-resolution code path.

**M3 — Rendering pipeline compiles (not yet attempted)**
`tsk-cc` successfully compiling `r_main.c`, `r_bsp.c`, `r_segs.c`,
`r_draw.c`, `r_plane.c`, `r_things.c`, `r_data.c` (the BSP/raycasting
renderer, ~7,500 lines combined) without crashing the compiler or
producing obviously wrong codegen. This is the first real test of
`tsk-cc` against recursive data structures, function-pointer tables, and
heavier struct/array nesting than anything compiled so far. Expect new
codegen bugs here — this is where B15/B16/B17/B20-class issues are most
likely to recur.

**M4 — Single static frame renders via SDL2**
A minimal harness that loads a WAD, runs just enough of `r_*` to render
one frame of a known level to the SDL2 framebuffer, and the pixels are
inspectable (e.g. dumped to a PNG and diffed against reference DOOM
output, or eyeballed). Proves the renderer's math and the
`Im_FbBlit`/`Im_FbClear` SDL2 path work together. Does **not** yet require
game loop, input, or sound.

**M5 — Game loop + input live**
`d_loop.c`, `g_game.c`, `i_input.c` wired up: the player can move and turn
in a level using keyboard input, with frames updating in real time.
Performance is not a requirement at this stage — even single-digit FPS
through the interpreted VM would validate correctness.

**M6 — Enemies, combat, game state**
`p_enemy.c`, `p_map.c`, `p_inter.c`, `p_mobj.c` and friends (mobile object
logic, collision, combat) — the bulk of remaining gameplay code.

**M7 — Sound (optional / deferred)**
`i_sdlsound.c`, `i_sdlmusic.c`, `s_sound.c` — explicitly out of scope for
"playable" in the usual sense; can be deferred indefinitely without
blocking a playable build.

**M8 — "Operational" — playable session start to finish**
Load IWAD, navigate menu, play a level to completion, die/win condition
recognized. This is the actual target implied by "version opérationnelle".

### Current position
M0 and M1 complete. M2 identified and scoped but not started. M3 onward
unattempted — no evidence yet on whether `tsk-cc` handles the renderer's
code patterns. Given the bug density observed in M1 (4 fundamental
toolchain bugs surfaced by ~1,600 lines of relatively simple support
code), M3 should be expected to surface comparable or higher bug density
per line, since BSP traversal and span/column rasterization are
structurally more demanding (recursive calls, pointer-heavy lookup
tables, tight inner loops sensitive to register-allocation correctness).
No reliable ETA can be derived from M1's pace alone; M3's first compile
attempt will be the next real data point.

---

## 2. Trampoline Mechanism — Technical Debt Analysis

### Background
TriskeleVM's `F_Call` instruction encodes a 24-bit relative offset
(±8MB range). Calls to libc functions, which live in a fixed segment at
`LIBC_BASE = 0xE000_0000`, are always far outside this range from
program code (which starts near `0x1000`). `tsk-link` handles this by
emitting a small **trampoline** per far call site: 6 instructions (24
bytes) that load the absolute 32-bit target address into a scratch
register and perform an indirect call (`Im_CbInvoke`).

### The B24 bug, revisited — root cause is deeper than first documented
The v0.3.20 handover described B24 as "trampoline reservation mismatch"
and fixed it by padding `final_code` to the pre-computed `data_base`
whenever the actual trampoline count came up short. That fix is correct
and necessary, but the handover's explanation of *why* the count
diverged was incomplete — it speculated about deduplication, which does
**not** actually exist in the code (`far_trampolines.push(...)` runs
unconditionally for every far call site; there is no dedup by target
symbol despite a misleading comment claiming otherwise). The real
mechanism, confirmed by instrumenting both the pre-scan and Phase 3 on
`doom_wad`:

**There are two competing sources of truth for libc function addresses:**
1. `LIBC_SYMBOLS` (Phase 0, in `triskele-common::libc_symbols`) —
   statically assigns every libc function a fixed stub address at
   `LIBC_BASE + offset` (e.g. `printf → 0xE0000200`).
2. `tsk-libc.tvml` (generated by `tsk-libc-gen`, linked as an ordinary
   `.tobj`-equivalent input alongside the program's own object files) —
   contains **real code** (`Im_Syscall(id) + F_Ret`, 8 bytes each) for
   the subset of functions it implements, at addresses determined by
   normal code layout (close to the rest of the program, e.g. `~0x77C4`).

When Phase 1 (symbol layout) processes `tsk-libc.tvml`'s own symbol
table, it **silently overwrites** the Phase-0 stub address for any name
both tables define — logged only as `WARNING: duplicate symbol @printf`,
with no further consequence. The pre-scan (Phase 0b) runs *before* this
overwrite and still sees the original `0xE0000000+` stub address, so it
reserves a trampoline slot for every such call. Phase 3 resolves the
*same* call against the *new*, in-range address and never emits a
trampoline for it.

**Confirmed on doom_wad** (43 libc-targeting relocations counted by
pre-scan, 29 actual trampolines emitted by Phase 3, 14 = 336 bytes of
divergence):

| Symbol | Pre-scan count | Phase 3 actual | Cause |
|---|---|---|---|
| printf | 9 | 0 | redefined in tsk-libc.tvml at ~0x77C4 |
| strlen | 1 | 0 | redefined in tsk-libc.tvml at ~0x7734 |
| strncmp | 2 | 0 | redefined in tsk-libc.tvml at ~0x7754 |
| strncpy | 2 | 0 | redefined in tsk-libc.tvml at ~0x7744 |
| (16 other libc fns) | 29 | 29 | not redefined — genuinely far, correctly counted |

All 43 pre-scan-counted relocations were confirmed to be genuine
`Opcode::F_Call` instructions (verified by decoding the opcode byte at
each `.reltab` offset) — the divergence is entirely explained by the
symbol-shadowing mechanism above, not by any reloc-type confusion.

### Cost of the current mechanism
- **No deduplication**: every far call site gets its own 24-byte
  trampoline, even when ten call sites target the same function.
  Confirmed on doom_wad: 29 trampolines × 24 bytes = 696 bytes of pure
  overhead code, for what is a fairly small test program. This scales
  linearly with call-site count, not with distinct-function count.
- **Indirect-call overhead at runtime**: each far call costs 6
  instructions (load hi16, load shift amount, shift, load lo16, or,
  indirect call) versus 1 instruction for an in-range direct `F_Call`.
- **Two-pass layout fragility**: `data_base` is computed once in Phase
  0b based on the pre-scan estimate, then never recomputed — only
  padded to match if Phase 3's actual code length comes up short (the
  v0.3.20 fix). If a future change caused Phase 3 to need *more*
  trampoline space than reserved (the symmetric failure mode), the
  current code fails loudly with an `anyhow!` error rather than
  corrupting addresses — but this still means the architecture has a
  built-in fragility that the right fix (below) would eliminate
  entirely rather than just guard against.

### Fix options, in increasing order of invasiveness

**Option A — Clarify the libc-resolution architecture (do this first)**
Decide explicitly: either `tsk-libc.tvml` is the sole source of truth
for every function it implements (in which case `LIBC_SYMBOLS` Phase 0
should only pre-populate the functions `tsk-libc.tvml` does *not*
implement), or the reverse. Currently both tables overlap for an
unspecified subset of names with no documented rule, and the resolution
priority (`tsk-libc.tvml`'s real address wins silently) is implicit
linker behavior rather than a stated design. This is a low-risk,
mostly-bookkeeping fix: once the overlap is eliminated, the pre-scan's
estimate becomes exact, and the `WARNING: duplicate symbol` log line for
libc names should never fire again (if it does, that's now a genuine bug
signal worth promoting to a hard error).

**Option B — Implement `L_FarCall` / `Im_FarCall Rx` (already on the
roadmap as a deferred TODO)**
Replace the trampoline mechanism with a direct indirect call at the call
site itself: `D_MovI` the full target address into a scratch register
(5 instructions, same pattern `tsk-cc` already uses for large-constant
loads), followed by `Im_CbInvoke`. This is structurally simpler than
the trampoline approach — the linker would resolve each far `F_Call`
in place rather than allocating a separate trampoline region, which
**removes the entire two-pass data_base estimation problem**, since
there is no longer a variable-sized trampoline section to size in
advance. Note: `tsk-cc`'s codegen already has the `Im_CbInvoke` pattern
implemented for register-indirect calls (`Value::Reg` branch in
`codegen.rs`, used for function-pointer calls) — `Value::Global` (named
calls) currently always takes the `emit_call_placeholder` /  plain
`F_Call` path instead. Option B would mean `tsk-link` rewrites far
`F_Call`s into this same in-place pattern instead of redirecting to an
out-of-line trampoline.

**Option C — Add real deduplication to the existing trampoline scheme**
Key `far_trampolines` by target symbol name instead of pushing
unconditionally per call site. Reduces code size for programs with many
call sites to few distinct far functions, but does **not** address the
root cause (the dual-source-of-truth symbol shadowing) — the pre-scan
estimate would still need a dedup-aware count (number of *distinct* far
symbols, not number of far relocations) to stay accurate, which is a
non-trivial change to the pre-scan logic on its own.

**Recommendation:** A first (cheap, clarifies a real architectural
ambiguity), then B (already roadmapped, and structurally removes the
two-pass estimation problem rather than refining it). C is worth
revisiting only if B is deferred long-term and code-size becomes a
concern independent of the correctness issue.

---

## 3. Multi-Platform VM Architecture (Windows / Linux / WASM)

### Current state: zero platform-conditional code
A full audit of every crate (`grep -r "cfg(target_os\|cfg(windows\|cfg(unix\|cfg(target_arch"`)
found no platform-specific code anywhere in the workspace today — every
`#[cfg(...)]` attribute present is `#[cfg(test)]`. This is good news: the
analysis below starts from a clean baseline rather than having to unwind
existing platform-specific branches.

### Inventory of platform-coupled surface

**SDL2 — the largest coupling point, but already well-isolated**
All SDL2 usage lives in a single file, `triskele-vm/src/ffi/sdl2.rs`
(276 lines), exposing one public type, `Sdl2Context`, with a clean
method-based API (`init`, `fb_blit`, `fb_clear`, `poll_events`,
`register_callback`, `frame_sync`, `key_query`). However, the type
itself — not a trait — is referenced directly by concrete name in three
other places:
- `triskele-vm/src/cpu/mod.rs`: `Cpu.sdl: Option<Sdl2Context>` field,
  plus six call sites inside opcode handlers (`Im_FbBlit`, `Im_FbClear`,
  `Im_InputRd`, `Im_RegisterCb`, `Im_KeyQuery`, `T_FrameSyn`).
- `triskele-vm/src/wolf3d/mod.rs`: owns an `Sdl2Context` directly, calls
  `poll_events`, `frame_sync`, `canvas()` (the last one breaks
  encapsulation by reaching into the raw `sdl2::render::Canvas` type).
- `triskele-vm/src/wolf3d/raycaster.rs`: takes `&Sdl2Context` by
  concrete type in `process_input`, plus reads `scancode` constants
  from the `sdl2` module directly.

SDL2 itself supports Windows and Linux natively (it's a C library with
established bindings on both), so the *crate dependency* is not the
blocker for those two targets — the coupling above only becomes a
problem for WASM, where SDL2 has no meaningful target (the closest
equivalent, Emscripten's SDL2 port, requires a completely different
build toolchain than `wasm32-unknown-unknown`/`wasm32-wasi`, and would
mean compiling the *Rust VM itself* through Emscripten — a much heavier
commitment than abstracting the display backend).

**File I/O — std::fs, portable for Windows/Linux, not for WASM**
`triskele-vm/src/libc/mod.rs` uses `std::fs::File` (via
`std::io::{Read, Write, Seek, SeekFrom}`) for the VM's `fopen`/`fread`/
etc. syscalls. `std::fs` works identically on Windows and Linux (that's
exactly what Rust's standard library abstracts away) — no action needed
for those two targets. It does **not** exist at all for
`wasm32-unknown-unknown`; `wasm32-wasi` has a restricted virtual
filesystem that would need explicit setup (preopened directories) even
if targeted.

**Timing — std::thread::sleep, confined to the SDL2 module**
Used once, inside `Sdl2Context::frame_sync`. Already confined to the
file that would be replaced/abstracted for WASM anyway (`wasm32-unknown
-unknown` has no threads or blocking sleep; a WASM target would need to
yield to the browser's frame callback instead, a fundamentally different
control-flow shape, not just a different sleep implementation).

**CLI argument parsing — clap, confined to the native binary**
`triskele-vm/src/main.rs` uses `clap::Parser`; `triskele-vm/src/lib.rs`
does not depend on `clap` at all. This split is already exactly the
shape needed: `lib.rs`'s `build_cpu()` factory function takes plain
parameters (`Memory`, `entry_pc`, `debug: bool`, `trace: bool`,
`sdl_dim: Option<&str>`, `title: &str`) with no CLI-parsing dependency,
so a WASM entry point could call into the same `lib.rs` surface with
arguments sourced from JS bindings instead of `clap`, without touching
`main.rs` at all.

### What this means for the proposed three-target architecture

**Windows and Linux: already largely solved by Rust's std + SDL2's own
portability.** No preprocessor-equivalent (`#[cfg(...)]`) splitting is
needed between these two today, and none should be needed going
forward for the file-I/O and timing surfaces — `std::fs` and
`std::thread::sleep` are correct on both as-is. SDL2's own native
bindings handle window/input/rendering identically on both platforms
already (this is precisely what SDL2 is for). The only Windows/Linux-
specific concern worth flagging for later is build tooling — SDL2's
*development* dependencies (headers, `.lib`/`.so` linking) differ by
platform, but that's a build-script/CI concern, not a source-code
`#[cfg(...)]` concern.

**WASM is the real fork in the road**, and needs a genuine
trait-based abstraction, not preprocessor conditionals, because the
*shape* of the replacement is different per backend, not just the
implementation:
- Display/input: needs a `DisplayBackend` trait (or similar) with
  methods mirroring `Sdl2Context`'s current public API
  (`fb_blit`/`fb_clear`/`poll_events`/`register_callback`/`key_query`),
  implemented once by `Sdl2Context` (native) and once by a WASM backend
  that talks to a `<canvas>` via `wasm-bindgen`/`web-sys`
  (`ImageData`/`putImageData` for blit, `requestAnimationFrame` driving
  the frame loop instead of `poll_events`+`frame_sync`'s blocking
  sleep, DOM keyboard event listeners instead of SDL2's event pump).
- File I/O: the VM's libc `fopen`/`fread`/etc. would need a small
  storage-abstraction trait as well, since "load a WAD file" means
  something different on each target (native filesystem path vs. an
  in-memory buffer fetched by the browser beforehand and handed to the
  WASM module, since arbitrary filesystem access isn't available to web
  pages at all).
- Timing: frame pacing driven by the host environment's own callback
  (`requestAnimationFrame`) rather than the VM sleeping itself — this is
  an inversion of control, not a swappable implementation detail, and
  is the main reason this can't be resolved with `#[cfg(...)]` alone.

**Recommended crate-boundary split** (none of this exists yet — proposed
structure):
- `triskele-vm` (the interpreter core: CPU, memory, libc dispatch)
  should have **zero** display/timing dependencies at all — it already
  almost achieves this via the `lib.rs`/`main.rs` split, except for the
  `Cpu.sdl: Option<Sdl2Context>` field and the opcode handlers that
  reach into it directly.
- A new `triskele-display` trait crate defining the backend-agnostic
  interface (`DisplayBackend` or similar), with no SDL2 or wasm-bindgen
  dependency itself — just the trait and any shared types (keycodes,
  framebuffer dimensions).
- `triskele-vm-sdl2` (or keep `ffi::sdl2` where it is, but behind the
  new trait) — the existing 276-line module, adapted to implement the
  trait instead of being referenced by concrete type from `cpu/mod.rs`.
- `triskele-vm-wasm` (new) — implements the same trait via
  `wasm-bindgen`/`web-sys`, and provides the WASM-callable entry point
  that uses `lib.rs`'s `build_cpu()` (bypassing `clap`/`main.rs`
  entirely, as noted above).
- `Cpu` itself changes from `sdl: Option<Sdl2Context>` to something like
  `display: Option<Box<dyn DisplayBackend>>`, and the six opcode-handler
  call sites in `cpu/mod.rs` go through the trait instead of the
  concrete type.

This keeps `triskele-vm`'s core (CPU, memory, libc) identical across all
three targets — the only crate that changes per target is the thin
display/input adapter, which is exactly the surface that's already
isolated in `ffi/sdl2.rs` today. No `#[cfg(target_arch = "wasm32")]`
branches should be needed *inside* `triskele-vm` itself if this split is
done; the conditional compilation happens at the **workspace/Cargo.toml
level** (which adapter crate gets built and linked for a given target),
not scattered through the interpreter's logic.

### What's explicitly out of scope for this analysis
This is an architectural inventory and proposal, not an implementation
plan with effort estimates — no WASM build has been attempted yet, so
claims about `wasm-bindgen` API specifics or build-pipeline details
(e.g. whether `wasm32-unknown-unknown` or `wasm32-wasi` is the right
target, how `tsk-link`'s output would be loaded into a WASM linear
memory) are deferred until a first concrete WASM spike is attempted.
The trait boundary proposed above is designed to make that future spike
additive (write the new adapter crate) rather than requiring surgery on
`triskele-vm`'s core — but that claim itself should be re-validated once
the WASM spike is actually underway, not assumed correct in advance.

---

## TODO — Project-Level Action List

This section tracks five concrete initiatives requested for upcoming
sessions, in priority order. Each has a status and the minimum next
step — not a full implementation plan, since several of these are
analysis-stage and should stay that way until validated.

### TODO-1 — Trampoline technical debt (PRIORITY for next session)
**Status:** Root cause fully diagnosed (section 2 above). Fix options
A/B/C identified and ranked. **Nothing implemented yet.**
**Next step:** Implement Option A first — decide and document which of
`LIBC_SYMBOLS` (Phase 0) or `tsk-libc.tvml` is the sole source of truth
per function name, eliminate the overlap, confirm the
`WARNING: duplicate symbol` line stops firing for libc names on a
re-link of doom_wad and the other 7 validated regression projects, then
re-run the full regression suite (test_main, wolf3d, test_patterns,
test_select, doom_fixed, doom_alloc, doom_zzone, doom_wad — all
currently passing) to confirm zero regressions. Option B (`L_FarCall`
for named calls, removing the trampoline mechanism entirely) should
follow once A is stable, since A makes the pre-scan's estimate exact
again — a necessary precondition for trusting B's removal of that
estimate altogether without re-introducing a different blind spot.

### TODO-2 — Milestone identification (M0–M8 ladder)
**Status:** Done — see section 1 above (`M0`/`M1` complete, `M2` scoped,
`M3`–`M8` defined as testable checkpoints, no ETA claimed).
**Next step:** none required to "finish" this — it's a living
reference, not a one-time deliverable. Revisit and extend the ladder
once `M2` (libc parity) is attempted, since that's small enough to
likely close in one session and unblock `M3` immediately after.

### TODO-3 — Multi-backend architecture (Windows / Linux / WASM)
**Status:** Analysis complete (section 3 above): zero existing
platform-conditional code, SDL2 usage already isolated to one 276-line
file but referenced by concrete type (not a trait) from `cpu/mod.rs` and
the `wolf3d` module, `lib.rs`/`main.rs` already split in a way that
keeps `clap` out of the reusable core. Proposed crate boundary
(`triskele-display` trait + `triskele-vm-sdl2` + future
`triskele-vm-wasm`) is a proposal, not validated by any actual WASM
build attempt.
**Why this matters beyond portability:** introducing the
`DisplayBackend` trait and moving `Cpu.sdl: Option<Sdl2Context>` to
`Cpu.display: Option<Box<dyn DisplayBackend>>` forces every call site
that currently assumes SDL2-specific behavior to become explicit about
what it actually needs from a display backend. This kind of refactor
— making implicit assumptions explicit — routinely surfaces latent bugs
that a same-platform-only codebase never exercises (e.g. code that
silently relies on SDL2's specific event-pump timing, or an
uninitialized-field assumption that only holds because `Sdl2Context`
happens to zero-initialize something WASM wouldn't). It would also make
the codebase more modular independent of whether WASM is ever actually
shipped — splitting the VM core from its display adapter is good
hygiene regardless of target count.
**Next step:** start with the trait extraction and the
`triskele-vm-sdl2` adapter (no new behavior, pure refactor — `Cpu` goes
from a concrete `Sdl2Context` field to `Box<dyn DisplayBackend>`, native
build keeps working identically), confirmed by the full regression
suite passing unchanged. Only attempt a `triskele-vm-wasm` spike after
that refactor is stable — building the second backend is what actually
validates whether the trait is well-designed, but doing it before the
first refactor lands would conflate two sources of risk at once.

### TODO-4 — High-level declarative language ("Triskele" — working name)
**Status:** Early conceptual discussion only. No design started.
**Direction agreed so far:** a declarative language grounded in lambda
calculus (in the spirit of Haskell/F#'s expression-oriented, strongly
typed style) whose primitive types are not generic programming types
(int, string, struct) but the M2 GenericConcepts themselves
(`Homeostasis`, `FeedbackLoop`, `Cascade`, etc.), with M1 domain
extensions (Biology, Electronics, ...) acting as typed libraries built
on those primitives. The motivating insight: compiling C through
`tsk-cc` will never produce a meaningful M3-category profile, because C
has no notion of these concepts to begin with — confirmed empirically
in TODO-5 below (83.9% of all compiled-C instructions fall into a
single category, `D_`, across every test function profiled, with most
of the other 15 categories never emitted at all by `tsk-cc`). A
language designed around M2/M1 from the start would let the compiler
emit category-specific opcodes intentionally (e.g. a `feedback { ... }`
construct compiling toward the `Pos_`/`Neg_`/`It_`/`A_` opcodes a
feedback loop's structural formula implies), the way Java's design
anticipated the JVM's bytecode rather than C being retrofitted onto it.
**Open question, not yet resolved:** should the language be
*generative* (a program describes a TSCG system's formal structure, and
the compiler derives bytecode whose category profile matches that
structure by construction), or a general-purpose language that merely
borrows M2/M1 vocabulary as typed sugar over conventional control flow?
These have very different design and effort implications and should be
decided before any grammar/type-system work starts.
**Next step:** sketch — informally, not as a deliverable yet — what a
minimal program for a simple M2 concept (e.g. `Homeostasis` or
`FeedbackLoop`, both of which already have explicit structural-grammar
formulas in `M2_GenericConcepts.jsonld`) would look like syntactically,
to test whether the M2 formula (`A × S × F` for Homeostasis,
`(D×F)×(I×A×S)×(A×S×F)` for FeedbackLoop) translates into something a
type system could plausibly check, before committing to either branch
of the open question above.

### TODO-5 — Static profiling of high-level-language code (not C)
**Status:** Tooling built and validated (`tsk-static-profiler`, a new
workspace crate reusing `triskele_common::{TvmFile, SectionType,
OpcodeCategory}` rather than duplicating ISA knowledge — see its
`README.md` for the explicit scope of what it does and does not claim).
**Empirically confirmed on compiled C** (6 real `.tobj` files from the
doom_wad regression test, 6597 instructions total): `D_` alone accounts
for 83.9% of all instructions; `A_`, `St_`, `F_`, `It_`, `R_`, `V_`
together account for the remaining ~16%; most other categories
(`E_`, `O_`, `Im_`, `T_`, `Pos_`, `Neg_`, `K_`, `Ss_`) never appeared at
all in this sample. No useful per-function differentiation was observed
even between structurally different functions (a hash function and a
memory allocator both showed `D_`-dominated profiles in the 75–97%
range) — **this result is the direct motivation for TODO-4**, and is
the reason this TODO is now reframed as "profile the future high-level
language's output, not C's."
**Why this is expected to behave differently once TODO-4 exists:** if
the high-level language's compiler is designed to emit
concept-specific opcodes for M2/M1 constructs (per TODO-4's premise),
then `tsk-static-profiler` — already built and already reusing the
correct shared types — becomes immediately useful without any changes
to the profiler itself: feed it the new language's compiled output
instead of C's, and the same per-function histogram should show real
differentiation (e.g. a `Cascade`-typed function showing a `Process`/
`Pos_`/`Neg_`-heavy profile distinct from a `Coupling`-typed function's
`Relational`-family profile) if and only if the language design in
TODO-4 actually achieves the category-specific codegen it aims for.
**Next step:** none until TODO-4 produces any compilable output —
`tsk-static-profiler` is ready and waiting; nothing to build here in
isolation until there's higher-level code to point it at. The tool
itself is a good acceptance test for TODO-4 in fact: if a `Homeostasis`
program's compiled output still profiles indistinguishably from a
`Cascade` program's, that's a signal the language's codegen isn't yet
honoring its own type primitives, however correct the language's
surface syntax might look.

### Priority ordering and rationale
1. **Trampolines (TODO-1)** — concrete, scoped, fixes a real defect in
   working code; should not be deferred further since it could silently
   reappear with different counts on future projects.
2. **Multi-backend (TODO-3)** — independent of TODO-1/2, but valuable to
   start soon for the "latent bug surfacing" effect noted above; the
   trait-extraction step is low-risk (pure refactor, regression-suite
   verifiable) and worth doing even if WASM itself is deprioritized
   later.
3. **Milestones (TODO-2)** — already a living document, revisited
   opportunistically rather than worked on as a discrete task.
4. **High-level language (TODO-4)** — the highest-value, highest-risk,
   longest-horizon item. Worth continuing to think through
   conceptually in parallel with TODO-1/3, but shouldn't block them —
   TriskeleToolchain's existing C pipeline keeps being useful for DOOM
   regardless of how TODO-4 evolves.
5. **Static profiling of high-level code (TODO-5)** — blocked on TODO-4
   producing any output; the tool side is done and waiting.

---

## Session Closing Summary — What Was Actually Delivered

This session was analysis- and documentation-focused, per explicit
request — no toolchain code was modified. Concrete deliverables:

**Documents/analysis produced:**
- Milestone ladder M0–M8 (section 1), replacing percentage-based
  progress tracking, with M0/M1 confirmed done and M2 scoped.
- Trampoline root-cause analysis (section 2): the actual mechanism
  (dual source-of-truth symbol collision) is identified and quantified
  exactly on a real example (doom_wad: 43 vs 29, 14-symbol gap fully
  attributed to 4 specific function names). This corrects and replaces
  the incomplete "estimation mismatch" explanation from the v0.3.20
  handover. Three ranked fix options (A/B/C) — none implemented.
- Multi-platform architecture audit (section 3): complete coupling
  inventory (SDL2, file I/O, timing, CLI args) from a verified
  zero-platform-conditional-code baseline, with a proposed (not yet
  built) trait-based crate separation for Windows/Linux/WASM.

**Code produced:**
- `tsk-static-profiler` (new workspace crate, `crates/tsk-static-profiler/`):
  static M3-category histogram tool for `.tobj`/`.tvmx` files. Properly
  integrated as a workspace member depending on `triskele-common`
  (reuses `TvmFile`, `SectionType`, `OpcodeCategory` — no ISA knowledge
  duplicated, aside from one small, explicitly-commented re-implementation
  of `.symtab` parsing since `tsk-link`'s version is private to that
  binary crate). Includes a README explicitly scoping what the tool
  does and does not claim, written in direct response to an earlier,
  unverified external proposal that overstated what category histograms
  can detect (see README for specifics). Validated against 6 real
  compiled object files from the doom_wad regression test.

**Key empirical finding, with downstream consequences:**
Compiled C code is M3-category-flat (`D_` at 83.9%, most categories
absent entirely, no per-function differentiation). This isn't a flaw in
the tool or the ISA — it's expected, since C has no constructs that map
to M2/M1 concepts. It is the direct evidence motivating TODO-4 (a
high-level language designed around M2/M1 primitives from the start)
and reframes TODO-5 from "profile C" (shown to be uninformative) to
"profile whatever TODO-4 eventually produces" (where a meaningful
profile is actually expected if the language design succeeds).

**Explicitly not done this session** (by design, given the
analysis-only framing): no code changes to `tsk-link`, `triskele-vm`,
or `tsk-cc`; no WASM build attempted; no grammar or type system for the
high-level language started — all of the above remain open for future
sessions per the TODO list.


