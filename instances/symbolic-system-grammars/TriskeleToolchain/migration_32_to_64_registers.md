# TriskeleVM — Migration 32→64 Registers (v0.2 → v0.3)
**Author:** Echopraxium with the collaboration of Claude AI  
**Date:** 2026-06-03  
**Status:** Complete — 79 tests passing

---

## 1. Motivation

With `-O0` (unoptimized) LLVM IR, functions like `@SumTiles` require 38 simultaneous SSA
registers (34 SSA values + 4 parameters). The v0.2 ISA only provided 24 allocatable registers
(R0-R23), causing register spill → codegen failure → F_Trap stub → silent wrong results.

**Root cause:** 32-register ISA (5-bit fields) → 24 allocatable registers → insufficient for
complex -O0 functions.

**Solution:** 64-register ISA (6-bit fields) → 56 allocatable registers (R0-R55) → covers all
observed -O0 patterns.

---

## 2. ISA Encoding Changes

### 2.1 Instruction Format

```
v0.2 Type R: opcode(8) | dst(5) | src1(5) | src2(5) | flags(9)
v0.3 Type R: opcode(8) | dst(6) | src1(6) | src2(6) | flags(6)

v0.2 Type I: opcode(8) | dst(5) | imm19(19) signed
v0.3 Type I: opcode(8) | dst(6) | imm18(18) signed

Type J: opcode(8) | offset24(24) signed  [UNCHANGED]
```

### 2.2 Immediate Range

| Field  | v0.2       | v0.3       | Impact                         |
|--------|------------|------------|--------------------------------|
| imm    | 19-bit     | 18-bit     | Range: +-262143 -> +-131071    |
| flags  | 9-bit      | 6-bit      | Shift amounts 0-63 (was 0-511) |

---

## 3. Register File Layout

### v0.2 (32 registers)
```
R0-R7   : args/return (caller-saved)
R8-R23  : local variables (16 allocatable)
R24     : codegen scratch 1
R25     : codegen scratch 2
R26-R27 : reserved
R28=FP, R29=SP, R30=LR, R31=PC
```

### v0.3 (64 registers)
```
R0-R7   : args/return (caller-saved)
R8-R55  : local variables (48 allocatable)
R56     : codegen scratch 1 (REG_SCRATCH)
R57     : codegen scratch 2 (REG_SCRATCH2)
R58-R59 : reserved
R60=FP, R61=SP, R62=LR, R63=PC
```

---

## 4. Files Modified

| File                                    | Key changes                                          |
|-----------------------------------------|------------------------------------------------------|
| `triskele-common/src/registers.rs`      | NUM_REGS 32->64, REG_FP/SP/LR/PC 28/29/30/31->60/61/62/63 |
| `triskele-vm/src/cpu/decode.rs`         | 5-bit->6-bit fields, imm 19->18 bits                 |
| `tsk-asm/src/encoder.rs`                | Same as decode.rs (local copy)                       |
| `tsk-cc/src/codegen.rs`                 | MAX_VREGS 24->56, REG_SCRATCH 24->56, REG_SP 29->61  |
| `tsk-link/src/main.rs`                  | D_MovI extraction 5->6 bits, imm mask 19->18 bits    |
| `tsk-asm/src/assembler.rs`              | LeaRodata fixup, shift mask 0x1F->0x3F               |
| `tsk-cc/src/main.rs`                    | dump_bytecode display only                           |

---

## 5. Calling Convention Changes

**New in v0.3:**
- Local variables allocated from **R8** (not R2) to keep R0-R7 as caller-saved
- After each `F_CALL`, R0-R7 are **invalidated** in `ra.map` (codegen)
- Alloca addresses use **conservative mode** — never evicted from register file

**Unchanged:**
- R0 = return value
- R0-R7 = arguments (left-to-right)
- A_Enter saves LR + FP; A_Leave restores

---

## 6. Binary Compatibility

**Breaking change:** All `.tobj` / `.tvmx` files compiled with v0.2 are **incompatible**
with v0.3. The instruction encoding differs:

```
v0.2: D_MOV_I R24, 42  encodes as  0x41C0002A
v0.3: D_MOV_I R56, 42  encodes as  0x41E0002A
```

Always recompile from `.ll` source when upgrading toolchain version.
The `version` field in the `.tobj` / `.tvmx` header can be used for detection.

---

## 7. Future Migration Checklist (128 or 256 registers)

### 7.1 128 registers (7-bit fields)

- Type R: `8+7+7+7 = 29 bits` → only 3 bits for flags
- Type I: imm shrinks to **17 bits** (+-65535)
- Shift amounts 0-127 need 7 bits but only 3 flag bits → **borderline**
- Recommendation: switch to 64-bit instruction words at this point

### 7.2 256 registers (8-bit fields)

- Type R alone needs `8+8+8+8 = 32 bits` — no room for opcode
- **Not feasible** with 32-bit fixed-width instructions
- Required: 64-bit instruction words, or register windows (SPARC-style)

### 7.3 Files to update for any future register migration

```
[ ] triskele-common/src/registers.rs  — NUM_REGS, REG_* constants
[ ] triskele-vm/src/cpu/decode.rs     — field extraction shifts and masks
[ ] tsk-asm/src/encoder.rs            — mirrors decode.rs (kept local)
[ ] tsk-cc/src/codegen.rs             — MAX_VREGS, REG_SCRATCH, REG_SP, enc_r, enc_i
[ ] tsk-link/src/main.rs              — D_MovI dst extraction, imm mask
[ ] tsk-asm/src/assembler.rs          — LeaRodata fixup shifts, shift amount mask
[ ] tsk-cc/src/main.rs                — dump_bytecode display (field extraction)
[ ] All .tobj / .tvmx files           — must be recompiled (binary incompatible)
[ ] TriskeleVM_ISA_Reference.md       — update encoding tables
[ ] SKILL.md (tscg-rust-vm)           — update register layout section
```

---

## 8. Test Coverage

```
triskele-common : 18 tests  (registers, ISA, fixed-point)
triskele-vm     : 55 tests  (decode 36, cpu/memory 19)
tsk-asm         : 22 tests  (encoder 3, assembler 19)
tsk-cc          :  3 tests
tsk-link        :  3 tests
─────────────────────────────
Total           : 79 tests, 0 failures
```

Key new tests for 64-register correctness:
- `test_r_all_64_dst_values` — all R0-R63 in dst field
- `test_r_all_64_src1_values` — all R0-R63 in src1 field  
- `test_r_all_64_src2_values` — all R0-R63 in src2 field
- `test_r_no_field_bleed` — fields don't bleed into each other
- `test_encode_decode_r_high_regs` — R55, R60, R61 (FP, SP)
- `test_sign_extend_18_*` — 18-bit sign extension correctness

---

*TriskeleToolchain Migration Guide v0.3.0*  
*Echopraxium with the collaboration of Claude AI — 2026-06-03*
