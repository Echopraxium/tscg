# TriskeleToolchain — Patch v0.3.24
# Author: Echopraxium with the collaboration of Claude AI

## Scope
TODO-1 (Trampoline mechanism technical debt) — **Option B**, per Handover
v0.3.22 §2: remove the out-of-line trampoline mechanism entirely for
named (`Value::Global`) call targets, by emitting a far-call sequence
directly at the call site instead. Builds on top of patch v0.3.23
(Option A), which must be applied first.

Discovered and fixed along the way: **two independent pre-existing
latent bugs** in tsk-link's large-address (5-instruction) D_MovI patch
path — neither related to Option A or B themselves, but both would
have silently broken Option B's far-call placeholder, which is the
first code path to actually exercise an out-of-imm19-range address
load into REG_SCRATCH (R24).

## Files changed
- `crates/tsk-cc/src/codegen.rs`
- `crates/tsk-link/src/main.rs`

## What changed

### 1. New `emit_far_call_placeholder` in tsk-cc (the Option B mechanism)
`Instr::Call { func: Value::Global(fname), .. }` no longer calls
`emit_call_placeholder` (24-bit-relative `F_Call`, which `tsk-link`
might redirect to an out-of-line trampoline). It now emits, directly
at the call site:

```
D_MovI REG_SCRATCH, 0      ; placeholder, patched by tsk-link
St_Nop                     ; reserved (4×) — large-address patch room
St_Nop
St_Nop
St_Nop
L_FarCall REG_SCRATCH      ; the actual call: sets LR, jumps
```

This is the exact pattern `tsk-cc` already used for register-indirect
calls (`Value::Reg`), and `L_FarCall` is an opcode that already existed
in the ISA and VM (`triskele-common::isa::Opcode::L_FarCall`,
`triskele-vm`'s CPU loop) specifically annotated for "call 64-bit
address (> ±8MB)" — it had simply never been wired up for named calls
before. `tsk-link`'s existing `Opcode::D_MovI` relocation branch
(already used for large global-*data*-address loads) patches the
placeholder in place: 1 instruction if the resolved address fits
imm19, or the same 5-instruction sequence otherwise. No code changed
in how relocations are exported from `tsk-cc` — `call_fixups` already
carried `(offset, symbol_name)` pairs generically; `tsk-link` was
already dispatching behavior purely by reading the opcode byte present
at the patched offset, so emitting `D_MovI` instead of `F_Call` there
needed no change to the export path.

The full 20-byte slot is always reserved, since `tsk-cc` cannot know
the link-time address yet; when the short form suffices, only the
first instruction is patched and the 4 `St_Nop` placeholders stay
harmless no-ops.

`emit_call_placeholder` itself is left in place (now unused, flagged
`dead_code` by the compiler) rather than deleted, in case a future
need for the old `F_Call`-based path resurfaces — but nothing in the
current codebase calls it anymore.

### 2. Phase 0b (tsk-link) no longer over-reserves trampoline space
Previously, Phase 0b counted *every* relocation resolving to a
`≥0xE000_0000` address as needing a trampoline slot, regardless of
which opcode was actually present at the relocation site. With Option
B's `D_MovI`-based far calls, that's no longer true — a `D_MovI`
relocation never produces a trampoline, no matter how far the address
is. Counting it anyway just over-reserves space that Phase 3 never
uses (harmless via the data_base padding fallback, but exactly the
kind of phantom bookkeeping this patch removes, not just keeps safely
padded around).

**Fix**: Phase 0b now reads the actual opcode byte at each relocation's
local code offset (from the already-loaded `obj.code`) and only counts
the relocation if that opcode is `F_Call`. This is fully backward
compatible: a `.tobj` compiled by a pre-Option-B `tsk-cc` still emits
real `F_Call` placeholders for named calls, and gets exactly the same
reservation behavior as before (verified — see Validation). A `.tobj`
compiled by the current `tsk-cc` has none for named calls, so the loop
naturally counts zero for them, and the old trampoline machinery
(Phase 2's `Opcode::F_Call` branch, Phase 3's trampoline emission) is
simply never exercised for those relocations — without having been
deleted, so old object files keep working.

### 3. BUGFIX (pre-existing, unrelated to Option A/B): dst==R24 self-corruption
The 5-instruction large-address `D_MovI` patch sequence hardcoded `R24`
as its *internal* scratch register (for the shift amount and lo16
staging), regardless of which register the address was actually being
loaded into (`dst`). When `dst == R24` itself, the sequence overwrote
its own hi16 value before shifting/OR-ing it, silently producing a
wrong address instead of failing loudly.

No existing caller ever triggered this: `load_value`'s `Value::Global`
case always allocates a normal destination register via the register
allocator, never `REG_SCRATCH` itself. Option B's far-call placeholder
is the first caller to load its target directly into `REG_SCRATCH`
(R24) before `L_FarCall` — exactly the case this bug would have hit,
and was caught by deliberately testing that exact scenario before
building Option B on top of it (see Handover-style "verify before
building further" approach).

**Fix**: pick an internal scratch register that is never equal to
`dst` (`25` if `dst == 24`, else `24`).

### 4. BUGFIX (pre-existing, unrelated to Option A/B): wrong opcode constants for D_Shl/D_Or
While validating fix #3 end-to-end (not just via the synthetic unit
test, but through a real compile→link→run pipeline), the VM faulted
with a garbage memory address (`0xFFFFFFFFDEADBEEF`) instead of calling
`printf` correctly. Tracing the executed instructions revealed the
5-instruction patch sequence was emitting `D_Memcpy` and `D_Load32`
opcodes instead of the intended `D_Shl` and `D_Or` — because the
hardcoded constants `0x4C` and `0x46` are `D_Memcpy` and `D_Load32` in
the actual ISA (`triskele_common::isa::Opcode`), not `D_Shl` (`0x3E`)
and `D_Or` (`0x35`).

This path had apparently never been exercised end-to-end before:
every address resolved by the existing 12-project regression suite
fit within imm19, so the 1-instruction patch path was always taken
instead, and the 5-instruction path's wrong constants went unnoticed.
Option B's far-call placeholder is the first caller to resolve an
address (a libc stub, `≥ 0xE000_0000`) that forces this path on a real
end-to-end run rather than just a unit test asserting on the resolved
*address value* (which fix #3's original unit test did — it never
actually decoded and simulated the patched instructions, so it didn't
catch this).

**Fix**: corrected the two constants to their real ISA values (`0x3E`,
`0x35`).

### 5. New/updated tests in tsk-link
- `test_large_address_patch_dst_r24_does_not_self_corrupt` — builds a
  two-object scenario forcing the 5-instruction patch path with
  `dst == R24`, decodes and *simulates* the patched instruction
  sequence (not just asserting on the resolved address), and checks
  R24 ends up holding the real target address. This test initially
  used the same wrong opcode constants as bug #4 in its own simulator
  and had to be corrected in lockstep — now documents the real ISA
  values inline to prevent the two from drifting apart again.
- `test_object_defined_libc_name_skips_phase0_stub`,
  `test_object_defined_libc_name_produces_no_trampoline`,
  `test_libc_name_without_object_definition_still_uses_trampoline` —
  carried over from patch v0.3.23 (Option A), unchanged, still passing.

## Validation performed (Linux sandbox, Rust 1.75 + clang 18)

**Note on debug vs release builds**: `triskele-vm`'s memory
initialization (`Segment::new`, zeroing ~2GB of stack+heap+aux space
via an unoptimized `.cycle().take().collect()` iterator chain) is
extremely slow in `cargo build` (debug) — slow enough to look like an
infinite hang under a 30s timeout. This is unrelated to Option A or B;
it's a pre-existing characteristic of the debug build of
`triskele-vm`. All VM execution in this validation pass uses `cargo
build --release`. Worth a look in a future session (e.g. replacing
the iterator chain with `vec![0u8; size]` + a single poison-pattern
fixup pass, or `Vec::from_iter` with a sized hint) but out of scope
here.

- `cargo test --release -p tsk-link -p tsk-cc -p triskele-common` —
  **66/66 pass** (40 + 14 + 12).
- Compile→link→run, release binaries, 7 distinct C programs:
  - `return 31;` (no calls) — exit 31.
  - `printf` × 3, no `tsk-libc.tvml` linked — far call via
    `D_MovI`(5-instr)+`L_FarCall`, zero trampolines, zero warnings,
    exit 42, correct `printf` output.
  - Same, **with** `tsk-libc.tvml` linked — Option A eliminates the
    stub pre-population, short 1-instruction `D_MovI` patch path taken
    (resolved address fits imm19), exit 42, correct output.
  - `strcpy`/`strlen`/`strcmp` (3 distinct libc symbols), no
    `tsk-libc.tvml` — 3 separate large-address `D_MovI` patches, zero
    trampolines, exit 100, correct output.
  - Same, **with** `tsk-libc.tvml` — Option A + B combined, exit 100,
    correct output.
  - Two calls to a 4-argument local function (`add4`) — stresses
    `REG_SCRATCH`..`REG_SCRATCH+3` argument staging immediately
    followed by `REG_SCRATCH`'s reuse for the far-call placeholder —
    exit 77, correct output.
  - Four nested/chained calls (`inc(square(inc(square(3))))`) —
    stresses R24's live range across consecutive calls — exit 101,
    correct output.
  - **Retro-compatibility**: re-linked the original (pre-Option-B)
    `.tobj` containing real `F_Call` placeholders, both with and
    without `tsk-libc.tvml`. Without it, the old trampoline mechanism
    fires exactly as before (`pre-scan: 3`, `n_trampolines=3`, zero
    mismatch) and the program still runs correctly (exit 42) — Phase
    0b's opcode-aware fix does not regress the legacy F_Call path.
- Did **not** have access to the `projects/Doom-Generic/` test corpus
  in this session, so `run_all_tests.py` was not run here. **Please
  run it on the Windows checkout** (as was done for patch v0.3.23) to
  confirm all 12 projects stay green and `pipeline_report.txt` still
  shows zero `duplicate symbol` / zero trampoline-mismatch warnings —
  and, ideally, check whether `doom_wad.tvmx`'s size decreases further
  now that far calls no longer reserve any (even harmlessly padded)
  trampoline space at all.

## Not in scope for this patch
- Deleting `emit_call_placeholder` and the `F_Call`-trampoline
  machinery in `tsk-link` entirely — left in place for backward
  compatibility with already-compiled `.tobj` files; revisit once
  confident no such files remain in use.
- `triskele-vm`'s slow debug-build memory initialization (noted above)
  — unrelated to trampolines, but discovered while validating this
  patch; worth its own small fix in a future session.
- Option C (trampoline deduplication) — N/A now that Option B removes
  the trampoline mechanism for the cases that mattered.
