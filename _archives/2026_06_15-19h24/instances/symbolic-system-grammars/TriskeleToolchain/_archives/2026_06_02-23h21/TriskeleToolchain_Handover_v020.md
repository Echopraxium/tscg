# TriskeleToolchain — Handover Document

**Author**: Echopraxium with the collaboration of Claude AI  
**Date**: 2026-05-31  
**Version**: 0.2.0  
**Purpose**: Resume document for the next conversation — Rust VM implementation

---

## 1. Project Context

**TriskeleToolchain** is a `m3:SymbolicSystemGrammar` instance grounded in
the TSCG M3 Structural Grammar. It defines a complete computation toolchain
whose ISA is derived directly from the 16 monoidal primitives of the three
TSCG grammars.

**Repository**: `https://github.com/Echopraxium/tscg`  
**Local path**: `E:\_00_Michel\_00_Lab\_00_GitHub\tscg\`  
**Instance path**: `instances/symbolic-system-grammars/TriskeleToolchain/`

---

## 2. What Was Accomplished in This Session

### 2.1 Full ISA specification (v0.2.0)

The ISA was completely designed and semantically validated through a rigorous
**stress test** — each of the 16 opcode categories was derived from the
intrinsic M3 semantics of its monoidal primitive, not from conventional
computing terminology.

Major revisions from the stress test:

| Category | Before | After (v0.2.0) | Key insight |
|----------|--------|----------------|-------------|
| `F_`  | arithmetic | **execution flow** (JMP/CALL/RET/IF/coroutines) | "Flow" is transdisciplinary — execution flow IS a flow |
| `A_`  | control flow | **Stack + Heap** (2 memory attractors) | Stack and Heap are gravitational wells in memory space |
| `St_` | LOAD/STORE | **types/structs/NOP** | NOP = pure structure preservation; LOAD/STORE → D_ |
| `It_` | bitwise ops | **informational state + events + IRQ** | flags/events are encoded information state |
| `D_`  | MOV/XCHG | **all modifications** (MOV/LOAD/STORE/ADD/AND...) | D = "what modifies" — arithmetic and bitwise both modify |
| `E_`  | VM extensions | **self-transformation + adaptive GC** | E = generates structural novelty at runtime |
| `L_FAR_CALL` | was F_ | **is L_** | Target localization (64-bit) dominates over flow |

### 2.2 Mandatory notation convention

```
St_   Structure      (Territory/Gt)   — NEVER S_
It_   Information    (Territory/Gt)   — NEVER I_
Ss_   Symbol         (Stereopsis/Gs)  — NEVER S_
Im_   Interoperability (Map/Gm)       — NEVER I_
```

### 2.3 Key semantic distinctions established

```
Ss_ vs It_     sign (identifier "main") vs value (0x1000)
               Ss_Lookup resolves: Ss → It

St_ vs K_      static structure (compile-time) vs
               reflective knowledge (runtime)

D_ vs It_      raw modification (D_STORE32) vs
               named state change (It_SET_FLAG GAME_OVER)

F_ vs L_       near flow ±8MB (F_CALL) vs
               far localization 64-bit (L_FAR_CALL)

A_ vs _^_      memory attractor (A_ALLOC → Heap) vs
               onset/activation (_^_NEW_OBJ → typed object)
```

### 2.4 Pole symmetry formalized

14 exact _^_/_$_ pairs — no orphan opcodes:
```
_^_NEW_OBJ ↔ _$_DEL_OBJ      _^_SPAWN   ↔ _$_KILL
_^_NEW_STR ↔ _$_DEL_STR      _^_OPEN_CH ↔ _$_CLOSE_CH
_^_NEW_ARR ↔ _$_FREE_ARR     _^_PUSH_FR ↔ _$_POP_FR
_^_PIN     ↔ _$_UNPIN        _^_NEW_CTX ↔ _$_DEL_CTX
_^_REF_INC ↔ _$_REF_DEC      _^_LOCK    ↔ _$_UNLOCK
_^_OPEN_SC ↔ _$_CLOSE_SC     _^_ALLOC_P ↔ _$_FREE_P
_^_ARENA_B ↔ _$_ARENA_E      _^_ACTIVATE↔ _$_DEACT
```

### 2.5 Toolchain specifications produced

| File | Description | Status |
|------|-------------|--------|
| `M0_TriskeleToolchain.jsonld` | TSCG ontology instance | v0.2.0 ✓ |
| `M0_TriskeleToolchain_README.md` | Design process + results | v0.2.0 ✓ |
| `TriskeleVM_ISA_Reference_v020.md` | Full ISA — 256 opcodes | v0.2.0 ✓ |
| `TriskeleVM_Format_TVM.md` | .tvm/.tvx binary format | v0.1.0 ✓ |
| `TriskeleASM_Specification.md` | tsk-asm assembler | v0.1.0 ✓ |
| `TriskeleDisASM_Specification.md` | tsk-dis disassembler | v0.1.0 ✓ |
| `TriskeleLinker_Specification.md` | tsk-link linker | v0.1.0 ✓ |
| `rust-vm-SKILL.md` | Rust implementation skill (EN) | v0.2.0 ✓ |

### 2.6 Cargo workspace initiated

```
triskele-toolchain/
  Cargo.toml                    ← workspace manifest (created)
  crates/
    triskele-common/
      Cargo.toml                ← created
      src/lib.rs                ← created (modules declared)
    triskele-vm/
      src/{cpu,memory,ffi,io}/  ← directories created
    tsk-asm/src/                ← directory created
    tsk-dis/src/                ← directory created
    tsk-link/src/               ← directory created
    tsk-build/src/              ← directory created
```

---

## 3. Architecture Summary

### 3.1 ISA — 16 categories × 16 opcodes = 256 total

```
Monoïde  Hex   Category  M3 question               VM semantics
─────────────────────────────────────────────────────────────────────
Gt  ×    0x0_  A_        Where do data converge?    Stack + Heap
         0x1_  St_       How organized?             Types/structs/NOP
         0x2_  F_        How does execution flow?   JMP/CALL/RET/IF/coroutines
         0x3_  It_       Informational state?        Flags/events/IRQ/values
         0x4_  D_        What modifies?             MOV/LOAD/STORE/ADD/AND

Gm  +    0x5_  R_        Encodable otherwise?       I2F/F2FIX/SIGN
         0x6_  E_        Generates novelty?         Modules/hooks/adaptive GC
         0x7_  V_        Verifiable/falsifiable?    CMP/ASSERT/RANGE
         0x8_  O_        Internally measurable?     DUMP/TRACE/BREAK
         0x9_  Im_       Interfaceable?             FFI/SYSCALL/SDL2

Gs  |    0xA_  T_        When?                      TICK/FRAME_SYN/TIMER
         0xB_  _^_       Onset/activation?          NEW/SPAWN/ARENA_B
         0xC_  _$_       Terminus/dissolution?       DEL/KILL/ARENA_E
         0xD_  K_        What is known?             TYPEOF/IS_A/SCHEMA
         0xE_  Ss_       What is the sign?          INTERN/LOOKUP/PI/NULL_T
         0xF_  L_        Converging to?             LEA/DEREF/FAR_CALL
```

### 3.2 VM Architecture

```
Paradigm       : Register-based (LuaVM simplicity + CLR C-interop)
Registers      : 32 × 64-bit (R0–R31)
                 R0–R7: args/return | R8–R15: temporaries (caller-saved)
                 R16–R23: locals (callee-saved)
                 R28=FP | R29=SP | R30=LR | R31=PC
Instruction    : 32-bit fixed (Type R / I / J / X)
Memory         : 64-bit linear address space
Calling conv.  : C-compatible (R0–R7 args, R0 return, cdecl ABI)
GC Phase 1     : Manual (A_ALLOC / A_FREE) — Wolf3D PoC
GC Phase 2     : Reference counting + cycle detector — TriskeleL
Concurrency    : Cooperative coroutines (F_YIELD, D_SAVE/REST_CTX)
FFI            : Im_FFI_CALL + Im_REGISTER_CB (SDL2 / libc)
Implementation : Rust (Cargo workspace)
```

### 3.3 Memory map

```
0x00000000   NULL page (unmapped — null ptr protection)
0x00001000   .code section (entry point)
0x...        .rodata, .data, .bss (follows code)
0x70000000   Stack top (grows downward, 1MB)
0x80000000   Heap base (grows upward, 4MB)
0xF0000000   VM internal (FFI dispatch tables)
```

### 3.4 PoC targets

```
Phase 1: Wolfenstein 3D (1992, open source)
  Critical opcodes: Im_FB_BLIT (0x92), T_FRAME_SYN (0xA6),
                    D_FixMul, D_Memcpy, D_Memset, F_Loop,
                    Im_REGISTER_CB, L_FAR_CALL

Phase 2: Doom (1993, open source)
  Same ISA — no additions needed
  Additional: Im_FILE_RD (WAD), _^_ARENA_B/_$_ARENA_E (Z_Malloc),
              F_CALL recursive (BSP), F_LOOP (visplanes)
```

---

## 4. Next Steps — Implementation Priority

### 4.1 Immediate priority — triskele-common

```
File: crates/triskele-common/src/isa.rs
  □ OpcodeCategory enum (16 variants, repr(u8))
  □ Opcode enum (256 variants, repr(u8))
  □ from_byte() implementations
  □ name() / category() helpers

File: crates/triskele-common/src/registers.rs
  □ RegisterFile struct (32 × u64)
  □ Flags struct (zero/negative/overflow/carry)
  □ new(stack_top) constructor
  □ get/set/sp/fp/lr/pc/set_pc/inc_pc helpers
  □ update_flags()

File: crates/triskele-common/src/tvm.rs
  □ TvmFile struct (sections, entry point)
  □ load_from_file() — reads .tvx binary
  □ Section enum (.code/.rodata/.data/.bss/.symtab/.tscg/.raw)

File: crates/triskele-common/src/error.rs
  □ VmError enum (all error variants)
  □ thiserror derives
```

### 4.2 Second priority — triskele-vm core

```
File: crates/triskele-vm/src/memory/mod.rs
  □ Memory struct (linear Vec<u8>, 64-bit addressed)
  □ read_u8/u16/u32/u64()
  □ write_u8/u16/u32/u64()
  □ memcpy() / memset()
  □ load_section() — copy .tvm section into memory

File: crates/triskele-vm/src/memory/stack.rs
  □ Stack struct (base, top, current SP)
  □ push() / pop() / peek()
  □ enter_frame() — saves LR + FP, sets new FP
  □ leave_frame() — restores FP + LR

File: crates/triskele-vm/src/memory/heap.rs
  □ Heap struct (base, size, free list)
  □ alloc(size) → u64 (VM address)
  □ alloc_zeroed(size) → u64
  □ free(ptr)
  □ realloc(ptr, new_size) → u64

File: crates/triskele-vm/src/cpu/decode.rs
  □ Instruction enum (R / I / J / X variants)
  □ decode(u32) → Result<Instruction, DecodeError>
  □ sign_extend_24() / sign_extend_19()
  □ is_immediate_opcode() helper

File: crates/triskele-vm/src/cpu/mod.rs
  □ Cpu struct (regs, memory, stack, heap, ffi)
  □ new(tvm, debug) constructor
  □ run() → Result<i32> — main interpreter loop
  □ execute_r/i/j/x() dispatch methods
```

### 4.3 Third priority — FFI SDL2

```
File: crates/triskele-vm/src/ffi/sdl2.rs
  □ FfiDispatch struct
  □ init_sdl2(title, width, height) → Result
  □ sdl2_fb_blit(fb_ptr, w, h, memory) — Im_FB_BLIT
  □ sdl2_poll_events() — Im_INPUT_RD
  □ register_callback(event_id, vm_addr) — Im_REGISTER_CB
  □ frame_sync(target_fps) — T_FRAME_SYN
  □ load_module(path) — E_LOAD_MOD (libloading)
```

### 4.4 Validation milestone

```
Goal: "Hello World" in Triskele assembly runs on the VM

wolf3d_hello.tsk:
  .module  hello
  .type    executable
  .entry   main

  .section .code
  main:
    D_MOV_I  R0, 72         ; 'H'
    O_Log    R0             ; print
    F_Halt
```

---

## 5. Rust Skill Location

The Rust implementation skill is available at:
```
/mnt/skills/user/rust-vm/SKILL.md    (to be installed from rust-vm-SKILL.md)
```

**Read the skill before writing any code** — it contains:
- Complete OpcodeCategory and Opcode enums (copy-paste ready)
- RegisterFile implementation
- Instruction decoder (Types R/I/J)
- VM main loop pattern
- Key opcode implementations (all 16 categories)
- FFI SDL2 patterns (Im_FB_BLIT, Im_REGISTER_CB, T_FRAME_SYN)
- Arena allocator (_^_ARENA_B / _$_ARENA_E)
- Fixed-point 16.16 arithmetic (D_FixMul — Wolf3D raycaster)
- Base16 Triskele display (tsk-dis colorization)
- Common error types

---

## 6. Key Files to Consult

```
Specifications (in this zip / project knowledge):
  TriskeleVM_ISA_Reference_v020.md    ← PRIMARY REFERENCE for opcodes
  TriskeleVM_Format_TVM.md            ← .tvm/.tvx binary format
  TriskeleASM_Specification.md        ← tsk-asm syntax + directives
  TriskeleDisASM_Specification.md     ← tsk-dis output formats
  TriskeleLinker_Specification.md     ← tsk-link linking process
  M0_TriskeleToolchain.jsonld         ← TSCG ontology (scores, concepts)
  M0_TriskeleToolchain_README.md      ← design process + rationale

Project knowledge (in Claude project):
  M3_GenesisGrammar.jsonld            ← M3 primitives reference
  M2_GenericConcepts.jsonld           ← GenericConcepts (18 mobilized)
  M3_EagleEye.jsonld                  ← ASFID definitions
  M3_SphinxEye.jsonld                 ← REVOI definitions
```

---

## 7. Conventions — Quick Reference

```
Language       : Rust (Cargo workspace)
Edition        : 2021
Error handling : anyhow::Result<()> for propagation
                 thiserror for VmError types
Unsafe         : explicit blocks only (FFI, libloading)
Notation       : St_ It_ Ss_ Im_ MANDATORY — never S_ I_
NOP            : St_Nop (0x10) — structure preserved, nothing changes
FAR_CALL       : L_FarCall (0xFE) — NOT F_ (localization dominant)
Fixed-point    : 16.16, FIXED_ONE = 0x00010000, π = 0x0003243F
Framebuffer    : 320×200 RGBA (Wolf3D), blit via Im_FbBlit (0x92)
FPS target     : 35 (Wolf3D), synchronized via T_FrameSyn (0xA6)
SDL2 events    : registered via Im_RegisterCb (0x99)
Z_Malloc       : _^_ARENA_B (0xBE) / _$_ARENA_E (0xCC) — Doom Phase 2
```

---

## 8. TO_DO Items Added This Session

```
[NEW] Skill Rust for TriskeleToolchain
      → /mnt/skills/user/rust-vm/SKILL.md (DONE — delivered as rust-vm-SKILL.md)

[NEW] README TriskeleToolchain
      → M0_TriskeleToolchain_README.md v0.2.0 (DONE)
```

---

## 9. What This Session Demonstrated for TSCG

The ISA stress test produced several arguments relevant to the Zenodo v4.0 article:

1. **16 primitives suffice** — 256 opcodes cover a complete game-capable VM
2. **Transdisciplinarity is operational** — F_ = execution flow = same abstract structure as blood flow, financial flow
3. **_^_/_$_ symmetry is complete** — 14 pairs, no orphan opcodes
4. **K, Ss, L cross-validation** — same 3 Gs primitives that resolve 17 M2 formula collisions also complete the Base16 ISA
5. **Anti-Brainfuck argument formalized** — each category is *deducible* from M3 semantics, not invented

---

*TriskeleToolchain — Handover Document v0.2.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-31*
