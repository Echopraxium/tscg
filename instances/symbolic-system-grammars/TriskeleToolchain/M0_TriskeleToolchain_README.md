# M0_TriskeleToolchain — README

**Author**: Echopraxium with the collaboration of Claude AI  
**Version**: 0.1.0  
**Date**: 2026-05-30  
**TSCG Layer**: M0 (Instance)  
**Ontology type**: `m3:SymbolicSystemGrammar`  
**File**: `instances/symbolic-system-grammars/TriskeleToolchain/M0_TriskeleToolchain.jsonld`

---

## 1. What is TriskeleToolchain?

TriskeleToolchain is a **Symbolic System Grammar** grounded in the TSCG M3
Structural Grammar. It defines a complete computation toolchain whose
foundational alphabet — the **Base16 Triskele encoding** — is derived
directly from the 16 monoidal primitives of the three TSCG grammars:

```
Gt (Territory / ASFID) × 5  →  A  S  F  It  D      hex 0x0–0x4
Gm (Map      / REVOI)  × 5  →  R  E  V  O   Im     hex 0x5–0x9
Gs (Stereopsis/ TKSL)  × 6  →  T  _^ _$ K   Ss  L  hex 0xA–0xF
─────────────────────────────────────────────────────────────────
Total: 16 primitives = 1 nibble = Base16
```

The 5+5+6 asymmetry of Gs is not arbitrary — it reflects the natural
extension required to resolve 17 formula collisions among M2 GenericConcepts
(concepts sharing identical structural formulas despite different semantics).
The Base16 completeness is a *consequence* of M2 expressivity requirements.

### Analogy: JVM / Java

```
TriskeleVM        ≈  JVM     (grounded in M3 Structural Grammar)
TriskeleL         ≈  Java    (grounded in M2 GenericConcepts — Phase 4)
TriskeleToolchain ≈  JDK     (complete development toolchain)
```

---

## 2. Toolchain Components

```
TriskeleToolchain
├── TriskeleVM          Register-based VM (Rust) — M3 layer
│   └── ISA Base16: 16 categories × 16 instructions = 256 opcodes
├── tsk-asm             Assembler (.tsk → .tobj)
├── tsk-dis             Disassembler (.tvx/.tobj → annotated listing)
├── tsk-link            Linker (.tobj + .tva + .tvl → .tvx/.tvl/.tva)
├── tsk-cc              C compiler (.c → .tobj) — Phase 2
├── tsk-dbg             Debugger (DAP server for VS Code) — Phase 2
├── tsk-lsp             Language Server (LSP for TriskeleL) — Phase 3
├── tsk-build           Build orchestrator (.tyml build files)
├── VS Code plugin      Syntax, DAP, LSP, M3 hex grid webview — Phase 2
└── TriskeleL           High-level language (M2 semantics) — Phase 4
```

---

## 3. File Extensions

```
Source
  .tsk      Triskele assembly source
  .tskl     TriskeleL source (Phase 4)
  .tyml     Triskele build file (YAML)
  .tldf     Triskele linker definition file (YAML)

Intermediate
  .tobj     Object file (unlinked)

Final binaries
  .tvx      Executable
  .tvl      Shared library
  .tva      Static archive

Debug / analysis
  .tdbg     Debug symbols
  .tmap     Link map
  .tsk.dis  Disassembly listing
  .tsk.lst  Assembler listing
```

---

## 4. ISA Overview — 256 Opcodes

Each opcode byte encodes: `[4-bit M3 category | 4-bit instruction index]`

```
0x0_  A   Attractor      Control flow: JMP, CALL, RET, LOOP, SWITCH...
0x1_  S   Structure      Memory: PUSH, POP, LOAD, STORE, MEMCPY, MEMSET...
0x2_  F   Flow           Arithmetic: ADD, SUB, MUL, DIV, FIXMUL, FIXDIV...
0x3_  It  Information    Bitwise: AND, OR, XOR, SHL, SHR, ROL, POPCT...
0x4_  D   Dynamics       Registers: MOV, XCHG, SAVE_CTX, REST_CTX...
0x5_  R   Represent.     Conversion: I2F, F2I, SIGN, ZERO, FIX2F...
0x6_  E   Evolvability   Extensions: LOAD_MOD, BIND, HOOK, GC_CFG...
0x7_  V   Verifiability  Comparison: CMP, EQ, LT, GT, ASSERT, RANGE...
0x8_  O   Observability  Debug: DUMP, TRACE, BREAK, WATCH, PERF...
0x9_  Im  Interop.       FFI/Syscalls: SYSCALL, FFI_CALL, FB_BLIT, REGISTER_CB...
0xA_  T   Time           Timing: TICK, WAIT, FRAME_SYN, TIMER, ATOMIC...
0xB_  _^  Pos. Pole      Allocation: ALLOC, NEW, SPAWN, OPEN_CH, LOCK...
0xC_  _$  Neg. Pole      Deallocation: FREE, KILL, CLOSE_CH, UNLOCK...
0xD_  K   Knowledge      Reflection: TYPEOF, SIZEOF, IS_A, ANN_GET, SCHEMA...
0xE_  Ss  Symbol         Strings: NEW, LEN, CAT, CMP, HASH, INTERN...
0xF_  L   Localizability Addressing: LEA, ADDR, IDX, DEREF, BOUND_CHK...
```

---

## 5. VM Architecture

```
Paradigm       Register-based (inspired by LuaVM + CLR)
Registers      32 × 64-bit (R0–R27 general, R28=FP, R29=SP, R30=LR, R31=PC)
Instructions   32-bit fixed-width (3 formats: R / I / J)
Memory         64-bit linear address space
Calling conv.  C-compatible (R0–R7 args, R0 return, cdecl ABI)
GC Phase 1     Manual (P_ALLOC / N_FREE) — Wolf3D PoC
GC Phase 2     Reference counting + cycle detector — TriskeleL
Concurrency    Cooperative coroutines (D_SAVE_CTX / D_REST_CTX)
FFI            Im_FFI_CALL + Im_REGISTER_CB (SDL2 / libc)
Implementation Rust
```

---

## 6. .tvm / .tvx Binary Format

```
[0x00]  Magic "TSKV"
[0x04]  Version       (Base16 Triskele)
[0x08]  Flags         (Base16 Triskele)
[0x0C]  Section count
[0x40]  Section table (N × 32 bytes, Base16 Triskele)
        .code    — bytecode           (M3 tag: F / Flow)
        .rodata  — constants          (M3 tag: It / Information)
        .data    — initialized data   (M3 tag: S / Structure)
        .bss     — uninitialized      (size only)
        .symtab  — symbol table       (M3 tag: Ss / Symbol)
        .strtab  — string table
        .reltab  — relocations        (M3 tag: L / Localizability)
        .tscg    — TSCG annotations   (M3 tag: K / Knowledge)  ← unique
        .import  — FFI declarations   (M3 tag: Im / Interop)
        .debug   — debug info         (M3 tag: O / Observability)
        .raw     — binary assets      (raw — always last)
```

The `.tscg` section is unique to TriskeleVM — it maps code address ranges
to M2 GenericConcept IRIs, enabling semantic hover in the VS Code plugin
and TSCG-aware analysis by TscgPocletMiner.

---

## 7. ASFID / REVOI Scores

```
Dimension        Score   Rationale
─────────────────────────────────────────────────────────────────
A  Attractor     0.90    Entry point + game loop convergence
                         (A_ opcode category = 16 control flow ops)
S  Structure     0.95    Rigorous .tvm format, register file,
                         section table, calling convention
F  Flow          0.88    Arithmetic + fixed-point (Wolf3D raycaster)
                         F_ category critical for 35fps performance
It Information   0.92    Base16 encoding (log₂16 = 4 bits/symbol),
                         .tscg semantic annotation section
D  Dynamics      0.85    Register state, coroutines, context save/restore

R  Represent.    0.88    Type conversions (R_), fixed-point ↔ float
E  Evolvability  0.90    Plugin system (E_), JIT-ready ISA,
                         VS Code extension architecture
V  Verifiability 0.82    ISA formally specified but Wolf3D not yet
                         executed — pending empirical validation
O  Observability 0.85    tsk-dis (4 modes), tsk-dbg (DAP), O_ opcodes,
                         .tscg annotations, link map
Im Interop.      0.87    SDL2 FFI design complete (Im_FFI_CALL,
                         Im_REGISTER_CB) — not yet validated

δ₁ (epistemic gap) = |ASFID_mean − REVOI_mean| / √2
                   = |0.900 − 0.864| / √2
                   = 0.0255

SpectralClass: Coherent
```

---

## 8. M2 GenericConcepts Mobilized (18 total)

```
GenericConcept      Role in TriskeleToolchain
────────────────────────────────────────────────────────────────
m2:Process          Bytecode execution — sequential instruction processing
m2:Structure        .tvm format — hierarchical section organization
m2:Layer            Toolchain layers — asm/link/compile/VM/language
m2:Component        Toolchain components — tsk-asm, tsk-dis, tsk-link...
m2:Channel          FFI channel — Im_FFI_CALL / Im_REGISTER_CB ↔ SDL2
m2:Code             Base16 Triskele encoding — symbolic binary representation
m2:Signature        Calling convention — function ABI (args R0–R7, return R0)
m2:Symbol           .symtab entries — name → address with TSCG M2 tags
m2:Language         TriskeleL — high-level language (M2 grounded, Phase 4)
m2:Agent            TriskeleVM runtime — autonomous execution agent
m2:Pattern          ISA encoding — [category nibble | instruction nibble]
m2:Node             Register file — 32 register slots in execution graph
m2:Topology         .tvm section topology — linear ordered layout
m2:Constraint       Calling convention — register save rules, stack alignment
m2:Homeostasis      T_FRAME_SYN — maintains stable 35fps render rate
m2:Interoperability Im_ opcode category — FFI, syscalls, SDL2 bindings
m2:ValueSpace       Base16 Triskele — encoding space for all constants
m2:Coherence        δ₁ — alignment between ISA design (map) and execution
```

---

## 9. TSCG Validation as SymbolicSystemGrammar

TriskeleToolchain satisfies the 4 SSG criteria:

```
① Finite primitives
   16 M3 primitives (A S F It D R E V O Im T _^ _$ K Ss L)
   → VALIDATED

② Combination rules
   3 explicit rule sets:
   - ISA encoding [category nibble | instruction nibble]
   - .tvm binary format (header + sections + relocations)
   - Calling convention (R0–R7 args, R28 FP, R30 LR)
   → VALIDATED

③ Multiple legitimate interpretations
   Same Base16 alphabet generates:
   - TriskeleVM bytecode  (M3 layer)
   - TriskeleL semantics  (M2 layer — Phase 4)
   - .tvm metadata        (M0 layer)
   → VALIDATED

④ Symbolic arbitration
   Opcode semantics motivated by M3 primitive identity:
   0x2_ = F/Flow → all arithmetic opcodes
   0x9_ = Im/Interop → all FFI/syscall opcodes
   → VALIDATED
```

**Distinction from Brainfuck**: unlike arbitrary instruction sets,
each TriskeleVM opcode category is semantically motivated by its M3
primitive. The ISA is *deduced* from the Structural Grammar, not invented.

---

## 10. Proof-of-Concept Target

```
Phase 1 — Wolfenstein 3D
  → C compiler (tsk-cc) generates TriskeleVM bytecode
  → SDL2 via Im_FFI_CALL + Im_REGISTER_CB
  → 35fps via T_FRAME_SYN
  → Critical opcodes: F_FIXMUL, S_MEMCPY, Im_FB_BLIT, A_LOOP

Phase 2 — Doom
  → Same ISA — no additions required
  → WAD format via Im_FILE_RD
  → BSP traversal via A_CALL recursive + A_LOOP
  → Zone memory manager Z_Malloc → P_ALLOC / N_FREE
```

---

## 11. Related Files

```
Specification documents (this release):
  M0_TriskeleToolchain.jsonld           this ontology
  M0_TriskeleToolchain_README.md        this file
  TriskeleVM_Format_TVM.md              .tvm / .tvx binary format
  TriskeleASM_Specification.md          tsk-asm assembler
  TriskeleDisASM_Specification.md       tsk-dis disassembler
  TriskeleLinker_Specification.md       tsk-link linker

Repository path:
  instances/symbolic-system-grammars/TriskeleToolchain/
```

---

## 12. Changelog

```
v0.1.0  2026-05-30
  Initial release. Full TriskeleToolchain specification:
  Base16 alphabet (16 M3 primitives), ISA (256 opcodes / 16 categories),
  .tvm/.tvx binary format, register file (32 × 64-bit), calling convention,
  tsk-asm / tsk-dis / tsk-link specifications, TSCG annotation sections,
  ASFID/REVOI analysis, 18 M2 GenericConcepts.
  PoC target: Wolfenstein 3D → Doom.
```

---

*TriskeleToolchain — M0 README v0.1.0*  
*Echopraxium with the collaboration of Claude AI — 2026-05-30*
