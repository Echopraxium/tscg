---
name: tscg-triskelevm-debug
description: >
  Debugging and diagnostic skill for TriskeleToolchain (tsk-cc, tsk-link,
  triskele-vm) when a pipeline run fails or produces incorrect output.
  Use this skill whenever Michel uploads a pipeline_report.txt, a .tvmx
  binary, a .ll file, or describes a VM crash, wrong test result, or linker
  error. Also use when discussing multi-platform targets (Windows, Linux,
  WASM) or codegen correctness issues. NOT for new feature implementation
  (use tscg-rust-vm skill) and NOT for TSCG ontology work.
---

# TriskeleToolchain Debug Skill

Systematic pipeline for diagnosing and fixing bugs in tsk-cc, tsk-link,
and triskele-vm across Windows / Linux / WASM targets.

---

## 0. Context — Read First Every Session

**Workspace** (Windows):
```
E:\_00_Michel\_00_Lab\_00_GitHub\tscg\instances\symbolic-system-grammars\TriskeleToolchain\
```

**Active patch output**: `/mnt/user-data/outputs/TriskeleToolchain_patch_vXXXX_FINAL.zip`

**Three-platform strategy**:
| Target   | Toolchain           | Status       |
|----------|---------------------|--------------|
| Windows  | clang/MSVC + Rust   | Active       |
| Linux    | clang + Rust        | Planned      |
| WASM     | Emscripten + wasm32 | Planned      |

**Critical invariant**: `triskele-common/src/libc_symbols.rs` is the
linker's single source of truth. Any mismatch with `triskele-vm/src/libc/mod.rs`
dispatch IDs → silent zero-address symbol → crash.

**Author convention**: all generated files credit
`"Echopraxium with the collaboration of Claude AI"`.

---

## 1. Diagnostic Checklist — Before Writing Any Code

Run through this before touching any source file:

```
□ 1. Identify the PHASE of failure (codegen / link / VM runtime)
□ 2. Check the exit code: crash (Memory fault) vs logic error (wrong bitmask)
□ 3. Check for regressions: are the 10+ previously passing projects still ✅?
□ 4. Identify the specific instruction / opcode at the crash PC
□ 5. Decode the last 10 TRACE lines (instructions before crash)
□ 6. Identify the function (sym addr ≤ crash PC < next sym addr)
□ 7. Confirm the fix doesn't break existing unit tests
□ 8. Validate on the full suite before shipping the patch
```

---

## 2. Pipeline Architecture

```
.c sources
  │
  ▼  clang -O0 -emit-llvm
.ll (LLVM IR — Windows SSA form)
  │
  ▼  tsk-cc  (Rust: crates/tsk-cc/)
.tobj (TriskeleObject: code + data + relocations + symbols)
  │
  ▼  tsk-link  (Rust: crates/tsk-link/)
.tvmx (TriskeleVM executable: flat binary, TSKV header)
  │
  ▼  triskele-vm  (Rust: crates/triskele-vm/)
exit_code (VM bitmask of test results)
```

**Key pipeline scripts**:
- `run_pipeline.py <project>` — single project
- `run_all_tests.py` — all 12 projects (10 stable + doom_argv + doom_wad)
- `_01_update_toolchain.bat` — cargo build --release
- `_02_run_pipeline.bat` — run all

---

## 3. Failure Phase Identification

### Phase A — CODEGEN FAILED
```
[tsk-cc] error: ...
STEP FAILED: tsk-cc
```
→ The .ll → .tobj compilation failed. Look for:
- Unsupported LLVM IR instruction (new intrinsic, aggregate type)
- Register allocator panic (too many live values)
- Unimplemented opcode in codegen.rs

### Phase B — LINK FAILED  
```
[tsk-link] error: undefined symbol @xxx
STEP FAILED: tsk-link
```
→ Symbol not in `libc_symbols.rs` or missing from a .tobj.
Check `libc_symbols.rs` ↔ `libc/mod.rs` ID alignment.

### Phase C — VM CRASH (Memory fault)
```
[tskvm] error: Memory fault: addr=0x..., size=...
VM Exit Code: N
```
→ Runtime crash. Use the TRACE analysis procedure (Section 4).

### Phase D — WRONG RESULT (Logic error)
```
VM Exit Code: 1   (only Test 1 bit set, instead of 0xFF)
✅ Test 1: ...
❌ Test 2: numlumps == 2
```
→ No crash, but tests fail. Usually a data corruption bug
that doesn't immediately fault. Use syscall sequence analysis (Section 5).

---

## 4. TRACE Analysis Procedure (VM Crash)

### 4.1 Extract crash context
```python
# Key grep patterns for pipeline_report.txt
grep -E "Memory fault|exit code"   report.txt
grep -B12 "Memory fault" report.txt | grep "TRACE" | tail -10
grep "code sym @" report.txt | sort
```

### 4.2 Identify the crashing function
```python
# Crash at PC=0x44FC, sym table shows:
# @W_AddFile → 0x3BE4,  @ExtendLumpInfo → 0x4500
# 0x3BE4 ≤ 0x44FC < 0x4500  →  crash is in W_AddFile
```

### 4.3 Decode the instruction word
```python
def decode(w):
    op  = (w >> 24) & 0xFF
    dst = (w >> 19) & 0x1F
    s1  = (w >> 14) & 0x1F
    s2  = (w >> 9)  & 0x1F
    fl  = w & 0x1FF
    fl_s = fl - 512 if fl >= 256 else fl
    return op, dst, s1, s2, fl, fl_s
```

### 4.4 Common crash patterns

| Crash addr        | Likely cause                          |
|-------------------|---------------------------------------|
| `0x0`             | NULL ptr dereference (spill bug)      |
| `0x8`–`0x50`      | NULL struct member access             |
| `0x800000XX`      | Executing heap data (corrupted LR)    |
| `size=0x80000000` | Negative length cast to unsigned      |
| `addr=valid+N`    | Wrong struct offset / GEP error       |

### 4.5 Spill bug signatures
```
D_STORE8 [R14+0], R14   ← ptr == val (alias bug)
D_LOAD64 R18, [FP-80]   ← wrong slot (store/reload mismatch)
D_STORE64 [R25+0], R18  ← R25 = FP + (-136) (correct 3-instr path)
```

---

## 5. Syscall Sequence Analysis (Logic Errors)

When there's no crash but tests fail, map the Im_SYSCALL trace to
function names using libc_symbols IDs:

```python
# libc stub address → name
def stub_name(pc):
    id = (pc - 0xE0000000) // 8
    return LIBC_SYMBOLS.get(id, f"id={id}")
```

**Key sequences to recognize**:
```
fopen → fseek × 3 + ftell × 2  =  M_FileLength in W_StdC_OpenFile
fopen → fread × 1               =  W_Read header only (numlumps=0 bug)
fopen → fread × 2               =  W_Read header + directory (correct)
fwrite × 1 → ...                =  build_test_wad wrote the WAD
calloc → ...                    =  ExtendLumpInfo allocated lumpinfo[]
```

**If `calloc` is absent** from the trace: `ExtendLumpInfo` was never called,
meaning `header.numlumps = 0` in the WAD file → `write_le32` bug.

---

## 6. tvmx Binary Analysis

When Michel uploads a `.tvmx`, inspect it with Python directly:

```python
import struct

data = open('doom_wad.tvmx', 'rb').read()
vm_base   = 0x1000
file_base = 0xA0  # standard header size

# Get code size from header
code_size = struct.unpack_from('<I', data, 80)[0]
print(f"Code: 0x1000 → 0x{0x1000+code_size:X}  ({code_size} bytes)")

# Find function address from symbol table
def find_sym(data, name):
    target = name.encode() + b'\x00'
    pos = data.find(target)
    if pos < 0: return None
    return struct.unpack_from('<I', data, pos + len(target))[0]

write_le32_vm = find_sym(data, 'write_le32')

# Disassemble N instructions from a VM address
def disasm(data, vm_addr, n=20):
    fo = (vm_addr - vm_base) + file_base
    for i in range(n):
        w = struct.unpack_from('<I', data, fo + i*4)[0]
        op = (w >> 24) & 0xFF
        # ... decode and print

# Verify trampolines don't overflow into data
data_start = 0x1000 + code_size
tramp_slots = count_libc_relocs(data)
tramp_end = data_start - tramp_slots * 24  # trampolines before data
```

### tvmx header layout
```
offset  0: magic  = 'TSKV'
offset  4: version
offset  8: n_sections
offset 72: code file_offset  (default 0xA0)
offset 80: code size in file
offset 104: data file_offset
offset 112: data size
```

---

## 7. Known Bug Catalogue (v0.3.10 session)

Reference for regression detection:

| ID | Component | Bug | Fix |
|----|-----------|-----|-----|
| B1 | tsk-cc codegen | `emit_spill_store` 1-instr path: negative offset sign-extended wrong via `flags as i16` | Use 3-instruction path for all negative offsets |
| B2 | tsk-cc codegen | `caller_save_slots` read from `spill_map` (mutable between store and reload) | Save `(name, reg, slot)` Vec at store time, use same Vec for reload |
| B3 | tsk-cc codegen | Call result R0 overwritten by caller-save reload | `D_Mov REG_SCRATCH, R0` before reloads when any slot has `reg==0` |
| B4 | tsk-cc codegen | `D_STORE8 [Rn], Rn` (ptr == val alias) | After loading ptr and val, if `rv == rp`: copy val to `REG_SCRATCH+2` |
| B5 | tsk-link | Pre-scan counted 6 FAR calls (opcode check) but 44 trampolines needed | Reserve slot for every reloc toward libc addr, no opcode check |
| B6 | tsk-cc parser | `external dso_local global` emitted 4 bytes in .tobj → two `@numlumps` | New `GlobalInit::External` variant: skip data emission entirely |
| B7 | tsk-cc codegen | `D_Shr`/`D_Shl` used `s2` register but ISA uses `flags[4:0]` for imm | VM already handles `s2 != 0` → use register (codegen was correct); verify actual flags in tvmx |

---

## 8. Codegen Unit Tests (crates/tsk-cc/src/codegen.rs)

Run with:
```cmd
cargo test -p tsk-cc -- test_spill test_caller test_store
```

| Test name | Catches |
|-----------|---------|
| `test_spill_store_reload_same_slot` | B1, B2 — store/reload offset mismatch |
| `test_caller_save_r0_preserved_before_reload` | B3 — R0 clobbered by reload |
| `test_store_no_ptr_val_alias` | B4 — D_STORE8 [Rn], Rn |
| `test_trampolines_do_not_overlap_data_*` | B5 — trampoline overflow |
| `test_trampoline_reservation_counts_all_libc_relocs` | B5 — pre-scan undercount |

**Always run all unit tests before shipping a patch.**

---

## 9. Register Conventions

```
R0–R7    : function arguments / return value (R0)
R8–R23   : temporaries (caller-saved)
R24      : REG_SCRATCH   (codegen scratch — save call result here)
R25      : REG_SCRATCH+1 (spill address computation)
R26      : REG_SCRATCH+2 (Store alias break)
R28 (FP) : frame pointer — NEVER use as scratch
R29 (SP) : stack pointer
R30 (LR) : link register — set by F_CALL, read by F_RET
R31 (PC) : program counter
```

**Spill slot formula** (3-instruction path for negative offsets):
```
offset_from_fp = -(frame_size + slot + 8)
D_MOV_I R25, offset_from_fp
D_ADD   R25, FP, R25
D_STORE64/D_LOAD64 [R25+0], reg
```
Single-instruction path only valid for `0 ≤ offset ≤ 255`.

---

## 10. Trampoline Architecture

**Why trampolines exist**: `F_CALL` encodes a 24-bit signed offset in bytes
(±8 MB range). Libc stubs are at `0xE0000000` (~3.7 GB from code) — beyond range.

**Trampoline structure** (5 instructions = 20 bytes, reserved as 24):
```asm
D_MOV_I  R24, hi13(target)   ; load high bits
D_SHL    R24, R24, R25       ; shift left 19 (via R25)
D_OR     R24, R24, lo19(target)
Im_CALL_R R24                ; indirect 64-bit call
```

**Placement**: trampolines are placed between the end of function code
and the data section. `data_base = code_base + code_size + trampoline_reservation`.

**Pre-scan rule** (B5 fix): reserve one slot per libc relocation,
**without** checking the instruction opcode at `local_off` — the opcode
check was unreliable when spill stores preceded the `F_CALL`.

**Future improvement**: replace `F_CALL` + trampoline with direct
`split_const32(target) + Im_CALL_R` for libc calls in codegen — eliminates
pre-scan entirely. See TODO in tsk-link/src/main.rs.

---

## 11. External Global Handling (GlobalInit::External)

In LLVM IR, `@numlumps = external dso_local global i32` is a **declaration**,
not a definition. tsk-cc must NOT emit data bytes for it.

**Rule**: if the parser sees `external` keyword before `global|constant`,
set `GlobalInit::External`. In `generate_module`, `continue` without emitting
any data or registering a symbol.

**If this is broken**: the linker sees two symbols with the same name
(one from the defining .tobj, one from the using .tobj) at different addresses.
Writes go to one address, reads come from the other → always zero.

**Symptom**: `data sym @numlumps → 0x7BB0` and `data sym @numlumps → 0x7F38`
in the same link report.

---

## 12. Multi-Platform Strategy

### 12.1 Windows (current)
- clang via MSVC toolchain, `_O0` only
- `.ll` SSA may differ from Linux (MSVC ABI vs SysV ABI, different register assignments)
- `run_pipeline.py` + `_01_update_toolchain.bat`
- Tests: `run_all_tests.py` (12 projects)

### 12.2 Linux (planned)
- clang `-O0 -emit-llvm -target x86_64-unknown-linux-gnu`
- SSA numbers will differ but bugs should be reproducible locally
- **Advantage**: Claude can compile tsk-cc and run tests directly in the sandbox
- Rust: install via `rustup` (apt version may be too old for workspace.dependencies)
- Local validation loop: `cargo test -p tsk-cc && cargo test -p tsk-link`

### 12.3 WASM (planned)
- Emscripten: `emcc -O0 -emit-llvm` → .ll → tsk-cc → .tobj
- Or: LLVM IR wasm32 target → needs tsk-cc wasm32 codegen backend
- TriskeleVM itself as WASM: `cargo build --target wasm32-unknown-unknown`
- Libc stubs: map to JS/WASM imports instead of Im_SYSCALL dispatch
- Key challenge: file I/O (fopen/fread/fwrite) → needs VFS layer

### 12.4 Platform-Agnostic Debug
Regardless of platform, these invariants hold:
- `libc_symbols.rs` IDs must match `libc/mod.rs` dispatch
- `external` globals → no data emission
- Trampoline reservation ≥ actual trampolines emitted
- `emit_spill_store` and `emit_spill_reload` use the same slot Vec

---

## 13. Patch Delivery Convention

**All fixes are delivered as `.zip` files**, never as Python scripts that
modify sources directly (regression from v0.3.10 session).

**Standard zip name**: `TriskeleToolchain_patch_vXXXX_FINAL.zip`

**Files typically included**:
```
crates/tsk-cc/src/codegen.rs
crates/tsk-cc/src/ir.rs
crates/tsk-cc/src/parser.rs
crates/tsk-link/src/main.rs
crates/triskele-vm/src/cpu/mod.rs
crates/triskele-vm/src/libc/mod.rs
crates/triskele-common/src/libc_symbols.rs
projects/Doom-Generic/vm-porting/tests/doom_wad/src/*.c
projects/Doom-Generic/vm-porting/tests/doom_wad/include/*.h
```

**After applying the zip**: always run
```cmd
python run_all_tests.py --clean
```
and confirm all 10 stable projects are still ✅ before continuing with
doom_argv and doom_wad.

---

## 14. Handover Document

At end of each debug session, produce
`TriskeleToolchain_Handover_vXXXX.md` with:
- Validation baseline (exit codes for all 12 projects)
- Bugs fixed this session (cause + fix)
- Pending bugs (symptoms + hypothesis)
- Next priorities

---

*TriskeleToolchain Debug Skill v0.1.0*
*Echopraxium with the collaboration of Claude AI — 2026-06-14*
