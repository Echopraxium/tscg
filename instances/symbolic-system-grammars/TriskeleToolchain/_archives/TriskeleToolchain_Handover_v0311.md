# TriskeleToolchain — Handover v0.3.11

**Date**: 2026-06-14  
**Author**: Echopraxium with the collaboration of Claude AI  
**Session focus**: codegen correctness (spill, caller-save, Store alias),
linker trampoline reservation, external global handling, doom_wad WAD loading

---

## 1. Validation Baseline

### 1.1 Stable projects (DÉCUPLE VALIDATION — confirmed ✅ throughout session)

| Project | Exit expected | Status |
|---------|--------------|--------|
| test_main | 31 (0x1F) | ✅ |
| test_patterns | 15 (0x0F) | ✅ |
| test_select | 9 (0x09) | ✅ |
| test_variadic | ? | ✅ |
| test_doom_libc | ? | ✅ |
| wolf3d | 15 (0x0F) | ✅ |
| doom_fixed | 127 (0x7F) | ✅ |
| doom_alloc | 255 (0xFF) | ✅ |
| doom_zzone | 255 (0xFF) | ✅ |
| doom_math | ? | ✅ |

All 10 stable projects verified passing after every codegen patch.

### 1.2 New projects (in progress)

| Project | Exit expected | Current status |
|---------|--------------|---------------|
| doom_argv | 63 (0x3F) | Unknown — not tested in final session |
| doom_wad | 255 (0xFF) | ❌ Exit 1 (only Test 1 passes) |

### 1.3 doom_wad test breakdown

```
✅ Test 1 (bit 0): W_AddFile returns non-NULL wad_file_t
❌ Test 2 (bit 1): numlumps == 2 after W_AddFile
❌ Test 3 (bit 2): W_CheckNumForName finds PLAYPAL lump
❌ Test 4–8: all depend on numlumps > 0
```

---

## 2. Bugs Fixed This Session

### B1 — emit_spill_store negative offset sign-extension (cpu/mod.rs)
**Symptom**: spill stores with negative FP offsets wrapped to large positive values;
spill reloads read from wrong stack locations → corrupted values.  
**Cause**: `_flags as i16` sign-extension was applied to 9-bit flags field; for
values ≥ 256 (all negative offsets), this gave a positive result.  
**Fix** (`cpu/mod.rs`): all 7 `wrapping_add(_flags as u64)` →
`wrapping_add((_flags as i16) as i64 as u64)`.  
Also fixed `emit_spill_store`/`emit_spill_reload` in `codegen.rs` to use
the 3-instruction path for **all negative offsets**:
```
D_MOV_I R25, offset_from_fp
D_ADD   R25, FP, R25
D_STORE64/D_LOAD64 [R25+0], reg
```
Single-instruction path is only used for `0 ≤ offset ≤ 255`.

### B2 — caller-save store/reload slot mismatch (codegen.rs)
**Symptom**: after a F_CALL, a spilled live value was reloaded from the wrong
stack slot (FP-80 instead of FP-136), yielding 0 → crash.  
**Cause**: the reload loop re-read `spill_map.get(name)` to find the slot, but
between the caller-save STORE and RELOAD, intermediate `load_reg_or_imm` calls
had mutated `spill_map[name]` (via `reload → spill_map.remove` then
`get_or_alloc → spill_map.insert` with a new slot).  
**Fix** (`codegen.rs`): save `(name, reg, slot)` in a local `caller_save_slots:
Vec<(String, usize, i32)>` at store time; reload loop uses this Vec, not
`spill_map`.

### B3 — call result R0 clobbered by caller-save reload (codegen.rs)
**Symptom**: after `calloc()` returns `newlumpinfo` in R0, the caller-save
reload of `newnumlumps` (which had been in R0 before the call) overwrote R0
with the old argument value → `lumpinfo = 1` (an argument count, not a heap
pointer) → `lump_p = 0x1 + 0` → `D_STORE64 [0x1]` crash.  
**Fix** (`codegen.rs`): before the caller-save reload loop, if any
`caller_save_slots` entry has `reg == 0`, emit `D_Mov REG_SCRATCH, R0` to
save the call result. After the reloads, copy from `REG_SCRATCH` instead of
`R0` into the destination register.

### B4 — D_STORE8 [Rn], Rn alias (codegen.rs)
**Symptom**: `D_STORE8 [R14+0], R14` — ptr and val in the same physical register;
when R14=0 → crash at address 0.  
**Cause**: `get_or_alloc` for the GEP result (ptr) recycled the register that
was occupied by the truncated byte value (val) after `val` was spilled. The spill
reload then put `val` back into the same register that `ptr` already occupied.  
**Fix** (`codegen.rs`): in the Store handler, after loading ptr (`rp`) and val
(`rv`), if `rv == rp`, copy `rv` into `REG_SCRATCH+2` (R26) before emitting
the store instruction.

### B5 — trampoline reservation undercount (tsk-link/src/main.rs)
**Symptom**: `F_CALL` instructions pointing beyond code segment (e.g. 0x12260 
while code ends at 0x7864); 44 trampolines generated but only 6 reserved slots
→ trampolines spilled into data section → PC jumped into heap → executed data.  
**Cause**: the pre-scan Phase 0b checked `(word >> 24) == F_Call` at
`obj.code[local_off]`. With 3-instruction spill sequences emitted before each
`F_CALL`, `local_off` sometimes pointed to a `D_MOV_I` (spill store) word
instead of the `F_CALL` opcode → relocation not counted → undercount.  
**Fix** (`tsk-link/src/main.rs`): removed the opcode check entirely. Reserve
one trampoline slot for **every relocation** targeting a libc stub address
(`>= 0xE0000000`), regardless of the instruction word at `local_off`.

### B6 — external global emitted as definition (tsk-cc parser.rs + ir.rs + codegen.rs)
**Symptom**: two `data sym @numlumps` entries at different addresses (e.g.
`0x7BB0` and `0x7F38`); W_AddFile wrote to `0x7BB0`, test read from `0x7F38`
→ always zero.  
**Cause**: `@numlumps = external dso_local global i32` in `test_doom_wad.ll`
is a declaration, not a definition. tsk-cc's parser consumed `external` as a
linkage keyword (like `private`/`internal`) without marking the global as extern
→ `GlobalInit::ZeroInit` → 4 zero bytes emitted in `test_doom_wad.tobj`.  
**Fix**:
- `ir.rs`: new `GlobalInit::External` variant
- `parser.rs`: `external` keyword detected → `is_external_linkage = true` →
  `GlobalInit::External` (no initializer parsed)
- `codegen.rs`: `GlobalInit::External` → `continue` (no data emitted, no
  symbol registered in the object file)

---

## 3. Unit Tests Added (crates/tsk-cc/src/codegen.rs)

Run with: `cargo test -p tsk-cc -- test_spill test_caller test_store_no`

| Test | Catches |
|------|---------|
| `test_spill_store_reload_same_slot` | B1, B2 — store and reload must compute identical FP offsets for the same slot; works with both 1-instruction and 3-instruction paths |
| `test_caller_save_r0_preserved_before_reload` | B3 — if a caller-save reload targets R0, a `D_Mov REG_SCRATCH, R0` must appear first |
| `test_store_no_ptr_val_alias` | B4 — under register pressure, `D_STOREx [Rn], Rn` must never be emitted |

**All 3 tests pass** as of v0.3.11.

---

## 4. Pending Bug — doom_wad: F_CALL targets outside code segment

### 4.1 Symptom
14 F_CALL instructions in W_AddFile point to addresses well beyond code end
(0x7864). Examples: `0x3C7C → 0x12260`, `0x3CD4 → 0x121B8`, `0xFFFFA76C`.

This means W_AddFile is jumping to garbage when calling libc functions
(strcasecmp, strncmp, strlen, Z_Malloc, etc.), which explains why numlumps=0:
W_Read fails silently → header.numlumps = 0 → ExtendLumpInfo not called.

### 4.2 Evidence
From pipeline_report.txt (last run):
```
[tsk-link] DEBUG Phase3: final_code.len()=25668 code_offset=25668 n_trampolines=44
data sym @numlumps → 0x00007B9C   ← single entry ✓ (B6 fix worked)
data sym @lumpinfo → 0x00007C04
code sym @W_AddFile → 0x00003BE4
code sym @ExtendLumpInfo → 0x00004508
```

Code section: `0x1000 → 0x7864` (0x6864 = 26724 bytes = 25668 code + 1056 trampolines).  
Trampolines: `0x7424 → 0x7854`.  
Yet F_CALL in W_AddFile targets `0x12260` — ~45 KB beyond trampolines.

### 4.3 Root cause hypothesis
The trampoline ADDRESS computation in tsk-link Phase 3 is correct (44 × 24 =
1056 bytes, placed at `code_offset + 0x1000 = 0x7424`). But the **F_CALL
delta** encoding that references those trampolines is wrong for obj[0] (`w_wad.c`).

The delta for `F_CALL at 0x3C7C → trampoline`:
- Correct trampoline address ≈ 0x7424 + k×24 (some small k for strcasecmp)
- Computed target = 0x12260 → delta encodes wrong absolute address

**Likely cause**: `obj_base` for `w_wad.tobj` (obj[0]) is calculated too small
in Phase 1, making `instr_vm = obj_base + abs_code_off` too small, making
`delta = trampoline_addr - instr_vm` too large → F_CALL encodes wrong offset.

**Alternatively**: the trampoline lookup table in Phase 3 stores the trampoline
address before `data_base` is finalized, and a recalculation with the correct
`code_base` shifts all trampoline addresses — but not the F_CALL relocations
that were already patched.

### 4.4 Next diagnostic step
Add this debug log to Phase 3 of tsk-link, just after emitting each trampoline:
```rust
eprintln!("[tsk-link] TRAMP: sym=@{} tramp_vm=0x{:X}",
    sym_name, 0x1000u64 + code_cursor as u64);
```
And log the F_CALL patching:
```rust
eprintln!("[tsk-link] PATCH_CALL: instr_vm=0x{:X} tramp_vm=0x{:X} delta={}",
    instr_vm, tramp_addr, delta);
```
This will reveal whether `tramp_vm` is correct and `instr_vm` is wrong, or
vice versa.

### 4.5 Fix to attempt
The B5 fix (reserve by reloc count, not opcode) is **confirmed applied** 
(n_trampolines=44 ✓). The remaining issue is a **Phase 3 patching error**:
the F_CALL instruction at `instr_vm` is being patched with a wrong delta.

Verify in `tsk-link/src/main.rs` Phase 3:
1. Is `obj_code_bases[obj_idx]` correct for w_wad.tobj (obj[0])?
2. Is `abs_code_off` correctly taken from `obj.relocs`?
3. Is `instr_vm = obj_code_bases[obj_idx] + abs_code_off` using the right base?

w_wad.c calls: `strcasecmp`, `strlen`, `strncmp`, `Z_Malloc`, `W_Read`,
`W_OpenFile`, `ExtendLumpInfo`, `W_LumpNameHash`, `W_GenerateHashTable`,
`strncpy`.

---

## 5. Files Modified in v0.3.11 Patch

**Patch zip**: `TriskeleToolchain_patch_v0311_FINAL.zip`

| File | Changes |
|------|---------|
| `crates/triskele-vm/src/cpu/mod.rs` | B1: sign-extend fix for spill flags |
| `crates/triskele-vm/src/libc/mod.rs` | calloc dispatch; fopen/fclose/fread/fwrite/fseek/ftell/feof/fflush added; heap_ceil fix |
| `crates/triskele-common/src/libc_symbols.rs` | _stricmp, _strnicmp, fopen-fflush, strerror, sscanf, calloc IDs |
| `crates/tsk-cc/src/codegen.rs` | B1 (3-instr spill path), B2 (caller_save_slots Vec), B3 (R0 save to REG_SCRATCH), B4 (Store alias break), B6 (GlobalInit::External skip), 3 new unit tests |
| `crates/tsk-cc/src/ir.rs` | B6: GlobalInit::External variant |
| `crates/tsk-cc/src/parser.rs` | B6: detect `external` keyword |
| `crates/tsk-link/src/main.rs` | B5: pre-scan counts all libc relocs (no opcode check); FCALL reloc diagnostic log retained |
| `projects/Doom-Generic/vm-porting/tests/doom_wad/src/test_doom_wad.c` | B6: uses `extern` from w_wad.h |

---

## 6. New Infrastructure This Session

### 6.1 Debug Skill
`tscg-triskele-debug/SKILL.md` — systematic debug methodology:
- Phase identification (codegen / link / VM crash / logic error)
- TRACE analysis procedure with crash pattern catalogue
- tvmx binary inspection snippets (Python)
- Known bug catalogue with symptoms and fixes
- Multi-platform strategy (Windows, Linux, WASM)
- Unit test coverage table

To install: copy to `.claude/skills/user/tscg-triskele-debug/SKILL.md`.

### 6.2 Projects directory reorganized (v0.3.10)
```
projects/
  toolchain-tests/c89/      ← test_main, test_patterns, test_select...
  toolchain-tests/asm/      ← assembly tests
  wolfenstein3D/wolf3d/     ← Wolf3D port
  Doom-Generic/vm-porting/tests/
    doom_fixed/             ← m_fixed.c
    doom_alloc/             ← zone allocator
    doom_zzone/             ← z_zone.c
    doom_math/              ← m_fixed.c + m_random.c
    doom_argv/              ← m_argv.c
    doom_wad/               ← w_wad.c + w_file.c + test_doom_wad.c
  references/
```

### 6.3 run_all_tests.py
Now covers 12 projects. Run with `--clean` to rebuild all.

---

## 7. Key Architecture Reminders

### Trampoline layout
```
code:      [0x1000 ... 0x1000+code_offset-1]    ← function code
trampolines:[0x1000+code_offset ... +n*24]        ← libc far calls
data:      [data_base ...]                        ← globals, strings
heap:      [0x80000000 ...]                       ← malloc/calloc (bump)
stack:     [0x70000000 downward]
libc stubs:[0xE0000000 ...]                       ← Im_SYSCALL dispatch
```

### Spill slot formula
```
offset_from_fp = -(frame_size + slot + 8)
```
- Negative → always 3-instruction path (D_MOV_I + D_ADD + D_STORE64/LOAD64)
- 0..255 → optional single-instruction path

### REG_SCRATCH assignments
```
R24 = REG_SCRATCH       ← save call result (R0) before caller-save reloads
R25 = REG_SCRATCH+1     ← spill address computation
R26 = REG_SCRATCH+2     ← Store alias break (when ptr==val)
```

### GlobalInit variants
```rust
GlobalInit::ZeroInit      → emit zeros (C: int x = 0;)
GlobalInit::Integer(n)    → emit n as LE bytes
GlobalInit::Bytes(b)      → emit raw bytes (string literals)
GlobalInit::External      → emit NOTHING (C: extern int x;)
GlobalInit::Undef         → emit zeros (LLVM undef)
```

---

## 8. Next Priorities

1. **[CRITICAL] Fix tsk-link Phase 3 F_CALL patching** for w_wad.tobj:
   - Add trampoline address + F_CALL patching diagnostic logs
   - Identify why `instr_vm` or `tramp_addr` is wrong for obj[0]
   - Likely: `obj_code_bases[0]` too small by ~X bytes

2. **Validate doom_wad tests 2–8** once F_CALL patching is fixed:
   - Expected: W_AddFile reads header (numlumps=2), calls ExtendLumpInfo,
     fills lumpinfo[], sets numlumps=2
   - All 8 tests should then pass

3. **doom_argv** — run and validate (6 tests, exit=63 expected)

4. **Handover checkpoint** — once doom_wad and doom_argv both ✅:
   - Bump Cargo.toml to 0.3.11
   - Produce final handover

5. **Linux platform** — compile toolchain on Linux, run same tests locally
   to enable faster debug cycles (Claude can compile + run in sandbox)

6. **Future: eliminate trampolines** — replace `F_CALL + trampoline` with
   `split_const32(target) + Im_CALL_R` for all libc calls in codegen.
   Eliminates the pre-scan problem entirely.

---

*TriskeleToolchain Handover v0.3.11*  
*Echopraxium with the collaboration of Claude AI — 2026-06-14*
