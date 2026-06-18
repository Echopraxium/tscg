# TriskeleToolchain — Handover v0.3.20 — doom_wad VALIDATED 8/8 (255/0xFF)

Author: Echopraxium with the collaboration of Claude AI

## Summary

`doom_wad` now passes all 8 tests (exit code 255/0xFF) after fixing three
distinct bugs discovered via native Linux testing (much faster iteration
than the Windows zip/upload cycle).

## Bugs fixed this session

### B24 — tsk-link: trampoline reservation mismatch corrupts data symbols
**File:** `crates/tsk-link/src/main.rs`

`data_base` was computed in two passes:
1. Phase 0b (pre-scan): estimates `n_far_calls` and reserves
   `trampoline_reservation = n_far_calls * 24 bytes` based on `global_syms`
   — which at this point does not yet contain all symbols.
2. Phase 3 (generation): emits the *actual* trampolines, deduplicated by
   target symbol, which can be fewer than the pre-scan estimate.

`self.data_base` was fixed from step 1 and used for **all data-symbol
address calculations**, but the actual data was written starting at
`actual_data_base` (`code_base + final_code.len()`) — which could differ
by tens to hundreds of bytes when the dedup count diverged from the
pre-scan estimate. The code only logged a `WARNING` and did nothing to
correct it, silently corrupting every string/global address in any object
linked after the divergence point.

**Fix:** the mismatch check (and a zero-fill padding step) now runs
**unconditionally** (moved outside the `if !far_trampolines.is_empty()`
block) so it also catches the case where reservation was non-zero but zero
trampolines were actually emitted. If `actual_data_base < self.data_base`
(reservation too large), `final_code` is padded with zero bytes up to
`self.data_base` — preserving every symbol address already computed. If
`actual_data_base > self.data_base` (reservation too small — should not
happen given the conservative pre-scan, but would silently corrupt
addresses in the other direction), linking now fails with an explicit
`anyhow!` error instead of continuing.

Confirmed via `RUST_LOG=warn`:
```
trampoline reservation mismatch: expected data_base=0x7BD4
but code+trampolines end at 0x7A84 (diff=-336)
```
336 bytes = 14 trampoline slots reserved but never emitted (deduplication).

**Impact:** this is a fundamental linker bug, present for any multi-object
link where the libc-relocation pre-scan count diverges from the actual
deduplicated trampoline count. It was likely already affecting other
multi-file projects silently whenever the counts happened to differ.
**Recommend re-running the full regression suite** (test_main, wolf3d,
test_patterns, test_select, doom_fixed, doom_alloc, doom_zzone) to confirm
no other project was relying on the old (broken) behavior.

### Fopen — unbounded path-read loop (defensive fix, not the root cause but enabled diagnosis)
**File:** `crates/triskele-vm/src/libc/mod.rs`

The path-reading loop in `Fopen` had no upper bound:
```rust
loop {
    let b = mem.read_u8(path_ptr + i)?;
    if b == 0 { break; }
    path_bytes.push(b);
    i += 1;
}
```
When `path_ptr` pointed at a region with no null terminator (as a direct
symptom of B24), this grew `path_bytes` unboundedly, exhausting available
memory and triggering an OOM kill (exit 137) with no diagnostic trace.

**Fix:** added a 4096-byte bound; on overflow, `fopen` now returns NULL
(R0=0) instead of looping forever. This is a defensive fix only — the
underlying corruption was B24 — but it should remain in place since a
real fopen() should never receive a path longer than typical filesystem
limits, and silently looping forever on any future corruption is worse
than failing fast.

### Fread — partial-read loop (latent correctness bug, not triggered by doom_wad but found during investigation)
**File:** `crates/triskele-vm/src/libc/mod.rs`

`Read::read()` is not guaranteed to fill the buffer in one call even when
more data is available. The original code treated a single `Ok(n)` as
"fully read," matching libc `fread`'s *typical* behavior but not its
*guaranteed* behavior. Fixed by looping until the buffer is full, EOF, or
an error occurs — matching real `fread` semantics. (In this session's
traces `n_read` always equalled `total` in one call, so this was not the
cause of the ENDOOM corruption, but it's a correctness fix worth keeping.)

### test_doom_wad.c — off-by-2 in synthetic WAD directory entry 1
**File:** `Doom-Generic/vm-porting/tests/doom_wad/src/test_doom_wad.c`

This was the actual root cause of the Test 7 failure (W_GenerateHashTable
+ hash lookup), **not** a toolchain bug at all:

```c
/* Directory entry 1: filepos=16, size=2, name="ENDOOM\0\0" */
write_le32(wad, 44, 16);     // filepos at offset 44..47
write_le32(wad, 48, 2);      // size   at offset 48..51
wad[50]='E'; wad[51]='N';    // BUG: overwrites size's high 2 bytes!
wad[52]='D'; wad[53]='O';
wad[54]='O'; wad[55]='M'; wad[56]=0; wad[57]=0;
```

`name` should start at `filelump_offset + 8 = 44+8 = 52`, not `50`. The
two stray writes at `wad[50]`/`wad[51]` corrupted `size` from `2` to
`0x4E450002` (1313144834) and the name field, when later read at its
*correct* offset 52, started 2 bytes into what should have been "EN" —
yielding `"DOOM\0\0\0\0"` instead of `"ENDOOM\0\0"`.

This explained the apparent "hash bucket mismatch": `W_GenerateHashTable`
was hashing the string `"DOOM"` (read from the corrupted lump name) while
`W_CheckNumForName`'s lookup hashed the literal `"ENDOOM"` — two different
strings producing two different (and both internally consistent) hash
buckets. The D_Rem unsigned-modulo fix from a previous session was
already correct; there was no remaining VM/codegen bug in the hash path.

**Fix:**
```c
wad[52]='E'; wad[53]='N'; wad[54]='D'; wad[55]='O';
wad[56]='O'; wad[57]='M'; wad[58]=0;  wad[59]=0;
```
(also requires `unsigned char wad[60]` to stay exactly large enough —
verified: name now spans indices 52..59, buffer size 60, exact fit.)

## Files in this patch
- `triskele-vm/src/cpu/mod.rs` — D_Rem already-correct unsigned fix retained;
  all debug eprintln tracing added during investigation removed.
- `triskele-vm/src/libc/mod.rs` — Fopen bound fix + Fread read-loop fix retained;
  debug tracing removed.
- `tsk-link/src/main.rs` — B24 fix (padding/error instead of silent corruption);
  two previously-unconditional debug eprintln calls converted to log::debug!
  (available via RUST_LOG=debug, no longer pollute default output).
- `test_doom_wad/src/test_doom_wad.c` — off-by-2 fix for directory entry 1.

## Validation
Full pipeline run natively on Linux (rustc 1.75, clang 18):
```
clang -O0 -emit-llvm -S ...   (all 6 sources)
tsk-cc ... .ll -o ... .tobj    (all 6 sources)
tsk-libc-gen -o tsk-libc.tvml
tsk-link <6 tobj> tsk-libc.tvml --entry main -o doom_wad.tvmx
tskvm doom_wad.tvmx
→ EXIT CODE: 255 (0xFF) — 8/8 tests pass, zero debug noise
```

## Next steps
1. Port these 4 file changes to the Windows workspace.
2. Run `_01_update_toolchain.bat` then
   `_02_run_pipeline.bat Doom-Generic/vm-porting/tests/doom_wad --clean`
   to confirm 255/0xFF on Windows too.
3. **Re-run full regression suite** (test_main=31, wolf3d=15,
   test_patterns=15, test_select=9, doom_fixed=127, doom_alloc=255,
   doom_zzone=255) to confirm B24's linker fix introduces no regressions —
   this bug could theoretically have been silently relied upon (unlikely,
   but worth the few minutes to check) by another project.
4. Continue toward `z_zone.c` DoomGeneric complet / tsk-libc malloc avec
   free-list per existing roadmap.
