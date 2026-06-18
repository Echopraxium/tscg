# TriskeleVM: 64-bit Architecture Upgrade Analysis
> Structural Architecture Review & Roadmap for Transitioning to 64-bit Registers

## 1. Executive Summary

TriskeleVM is a virtual machine (VM) designed with an explicit transdisciplinary grounding in the **TSCG M3 Structural Grammar**. This theoretical foundation mandates a rigid, monoidal approach to code structure, utilizing strict dualities between initialization and finalization states. 

The current specification employs an elegant **32-bit fixed-width RISC-like instruction encoding** coupled with 32 general-purpose virtual registers. To expand capabilities for complex compilation targets—such as real-world retro rendering engines (e.g., Wolf3D)—and natively interface with modern 64-bit execution environments, migrating the virtual machine's register file and internal computational data paths to **64-bit** provides a massive advantage.

This document serves as a comprehensive design spec and technical overview of why this migration is valuable, how it maps to the underlying M3 grammar, and how it impacts the existing compiler (`tsk-cc`), assembler (`tsk-asm`), linker (`tsk-link`), and virtual CPU runtime environments.

---

## 2. Core Architecture & Structural Harmony

### 2.1 Encodings and Structural Balance
The 32-bit instruction word of TriskeleVM is segmented cleanly into fixed-width fields, ensuring high decoding efficiency within a software-emulated inner loop:

* **Type R (Register):** `[ Opcode (8b) | Dst (5b) | Src1 (5b) | Src2 (5b) | Flags/Imm (9b) ]`
* **Type I (Immediate):** `[ Opcode (8b) | Dst (5b) | Immediate (19b) ]`
* **Type J (Jump):** `[ Opcode (8b) | PC-Relative Offset (24b) ]`

The allocation of 32 physical registers optimizes code generation for text-based LLVM IR inputs, minimizing register spill into the stack frame. The hardware convention reserves high registers for crucial environment pointers:
* `R28` -> Frame Pointer (`FP`)
* `R29` -> Stack Pointer (`SP`)
* `R30` -> Link Register (`LR`)
* `R31` -> Program Counter (`PC`)

### 2.2 The TSCG M3 Monoidal Philosophy
The instruction set architecture (ISA) is bound strictly to 16 categorical divisions representing foundational answers to structural identity questions. Most notably, the architecture achieves mathematical equilibrium via symmetric structural monoids:

* **Positive Monoid (`_^_` Active - `0xB0..0xBF`):** Primitives dedicated to structure creation, activation, allocation, and locking (e.g., `Pos_NewObj`, `Pos_ArenaB`, `Pos_Lock`).
* **Negative Monoid (`_$_` Reactive - `0xC0..0xCF`):** Primitives dedicated to structure destruction, deactivation, liberation, and unlocking (e.g., `Neg_DelObj`, `Neg_ArenaE`, `Neg_Unlock`).

This architectural symmetry drastically simplifies static verification. Bytecode validation passes can mathematically guarantee memory safety and resource deadlock prevention by checking matching monoidal states within basic blocks.

---

## 3. The 64-bit Transition Paradigm

Moving to a 64-bit computational layer while preserving the highly compact **32-bit fixed instruction width** mirrors the architectural philosophy of commercial industry standards like RISC-V (`RV64I`) and ARM64 (`AArch64`).

### 3.1 Architectural Trade-offs

1. **Native Host Alignment:** In a 64-bit host environment (such as native x86_64 or ARM64 systems compiling Rust), pointers (`usize`) occupy 8 bytes. By widening the internal VM data paths, memory references within the virtual space map 1:1 to host pointers without needing artificial runtime sandboxing shifts or narrowing arithmetic.
2. **Elimination of Multi-Precision Operations:** Heavy integer math required for matrix projections or multi-precision fixed-point scaling (frequent in retro-engineering tasks like Raycasting) can be executed natively in a single CPU cycle rather than splitting operations across register pairs.
3. **The Immediate Constraint Solution:** Because instruction widths remain 32-bit, the 19-bit signed immediate boundary remains active. Constants exceeding the range $[-262144, 262143]$ must be resolved via either:
   * **Shift & Or sequences:** Rebuilding the target value in a register using a pipeline of bitwise left shifts and logical OR operations.
   * **Constant Pools (.rodata):** Storing absolute values and absolute addresses in a dedicated read-only data block, retrieving them natively via PC-relative effective address loading (`L_LEA`) and quadword dereferencing (`L_DEREF_Q`).

---

## 4. Pipeline Component Impact Analysis

### 4.1 Compiler Backend (`tsk-cc`)
* **SSA Value Binding:** Simplifies structural lowering from text-based LLVM IR. The type mappings `IrType::Ptr` and `IrType::I64` transition from complex split allocations to single 64-bit physical registers.
* **Register Coalescing:** The instruction selector must avoid unnecessary temporary data moving (`D_MOV_R`). Introducing a register coalescing pass during SSA destruction eliminates redundancy.

### 4.2 Assembler & Linker (`tsk-asm` / `tsk-link`)
* **Relocation Dynamics:** The internal representation of labels inside the object file (`.tobj`) symbol table transitions to a full 64-bit unsigned address integer (`u64`). 
* **Linker Patching:** Placeholders targeted by `F_CALL` or `F_JMP` must support wide displacement calculations depending on the final section offsets inside the linked executable binary (`.tvmx`).

### 4.3 Standard Library Generator (`tsk-libc-gen`)
* **Syscall Lowering:** Standard C library stubs (e.g., `@memset`, `@memcpy`) now process arguments through 64-bit register widths. Double indirection overhead is avoided by mapping critical functions directly into efficient native system callbacks.

---

## 5. Implementation Blueprints (Refactored Components)

### 5.1 Refactored ISA Definition (`isa.rs`)
```rust
// uuid: 8f4b23c1-7a9d-4e56-b9cf-1d823fa46e28
// triskele-common/src/isa.rs
#![allow(non_camel_case_types)]

// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.4.0

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OpcodeCategory {
    A   = 0x0,  // Attractor
    St  = 0x1,  // Structure
    F   = 0x2,  // Flow
    D   = 0x3,  // Data
    V   = 0x4,  // Vector
    L   = 0x5,  // Link (Memory)
    O   = 0x6,  // Output
    It  = 0x7,  // Information
    Ss  = 0x8,  // Symbol
    Im  = 0x9,  // Interoperability
    K   = 0xA,  // Knowledge
    Pos = 0xB,  // Positive _^_ Monoid
    Neg = 0xC,  // Negative _$_ Monoid
    T   = 0xD,  // Time
} // enum OpcodeCategory

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Opcode {
    A_NOP        = 0x00,
    St_STRUCT    = 0x10,
    F_JMP        = 0x20,
    F_JZ         = 0x21,
    F_JNZ        = 0x22,
    F_CALL       = 0x23,
    F_RET        = 0x24,
    F_HALT       = 0x25,
    D_MOV_R      = 0x30,  // Move register to register (64-bit wide)
    D_MOV_I      = 0x31,  // Move sign-extended 19-bit immediate
    V_ADD        = 0x40,  // 64-bit integer addition
    V_SUB        = 0x41,  // 64-bit integer subtraction
    V_MUL        = 0x42,  // 64-bit integer multiplication
    V_SDIV       = 0x43,  // Signed 64-bit integer division
    V_CMP_I      = 0x44,  // Compare register with immediate
    V_CMP_R      = 0x45,  // Compare register with register
    V_SHL        = 0x46,  // 64-bit logical shift left
    V_SHR        = 0x47,  // 64-bit logical shift right
    V_AND        = 0x48,  // 64-bit bitwise AND
    V_OR         = 0x49,  // 64-bit bitwise OR
    L_LEA        = 0x50,  // Load Effective Address
    L_DEREF_B    = 0x51,  // Load 8-bit byte (zero-extended to 64-bit)
    L_DEREF_W    = 0x52,  // Load 32-bit word (sign-extended to 64-bit)
    L_DEREF_Q    = 0x53,  // Load 64-bit quadword natively
    L_STORE_B    = 0x54,  // Store 8-bit byte
    L_STORE_W    = 0x55,  // Store 32-bit word
    L_STORE_Q    = 0x56,  // Store 64-bit quadword
    O_LOG        = 0x60,
    It_CTX_B     = 0x70,
    Ss_PI        = 0x80,
    Ss_NULL_T    = 0x81,
    Im_Syscall   = 0x90,
    Im_RegisterCb= 0x91,
    Im_KeyQuery  = 0x92,
    Im_Exit      = 0x93,
    K_TYPEOF     = 0xA0,
    K_IS_A       = 0xA1,
    Pos_NewObj   = 0xB0,
    Pos_NewStr   = 0xB1,
    Pos_AllocArr = 0xB2,
    Pos_Spawn    = 0xB3,
    Pos_OpenCh   = 0xB4,
    Pos_PushFr   = 0xB5,
    Pos_NewCtx   = 0xB6,
    Pos_Pin      = 0xB7,
    Pos_RefInc   = 0xB8,
    Pos_Lock     = 0xB9,
    Pos_OpenSc   = 0xBA,
    Pos_AllocP   = 0xBB,
    Pos_ArenaB   = 0xBC,
    Pos_Activate = 0xBD,
    Neg_DelObj   = 0xC0,
    Neg_DelStr   = 0xC1,
    Neg_FreeArr  = 0xC2,
    Neg_Kill     = 0xC3,
    Neg_CloseCh  = 0xC4,
    Neg_PopFr    = 0xC5,
    Neg_DelCtx   = 0xC6,
    Neg_Unpin    = 0xC7,
    Neg_RefDec   = 0xC8,
    Neg_Unlock   = 0xC9,
    Neg_CloseSc  = 0xCA,
    Neg_FreeP    = 0xCB,
    Neg_ArenaE   = 0xCC,
    Neg_Deact    = 0xCD,
    T_Tick       = 0xD0,
    T_Sleep      = 0xD1,
    T_FrameSyn   = 0xD2,
} // enum Opcode

impl Opcode {
    pub fn from_u8(value: u8) -> Option<Self> {
        match value {
            0x00 => Some(Opcode::A_NOP),
            0x10 => Some(Opcode::St_STRUCT),
            0x20 => Some(Opcode::F_JMP),
            0x21 => Some(Opcode::F_JZ),
            0x22 => Some(Opcode::F_JNZ),
            0x23 => Some(Opcode::F_CALL),
            0x24 => Some(Opcode::F_RET),
            0x25 => Some(Opcode::F_HALT),
            0x30 => Some(Opcode::D_MOV_R),
            0x31 => Some(Opcode::D_MOV_I),
            0x40 => Some(Opcode::V_ADD),
            0x41 => Some(Opcode::V_SUB),
            0x42 => Some(Opcode::V_MUL),
            0x43 => Some(Opcode::V_SDIV),
            0x44 => Some(Opcode::V_CMP_I),
            0x45 => Some(Opcode::V_CMP_R),
            0x46 => Some(Opcode::V_SHL),
            0x47 => Some(Opcode::V_SHR),
            0x48 => Some(Opcode::V_AND),
            0x49 => Some(Opcode::V_OR),
            0x50 => Some(Opcode::L_LEA),
            0x51 => Some(Opcode::L_DEREF_B),
            0x52 => Some(Opcode::L_DEREF_W),
            0x53 => Some(Opcode::L_DEREF_Q),
            0x54 => Some(Opcode::L_STORE_B),
            0x55 => Some(Opcode::L_STORE_W),
            0x56 => Some(Opcode::L_STORE_Q),
            0x60 => Some(Opcode::O_LOG),
            0x70 => Some(Opcode::It_CTX_B),
            0x80 => Some(Opcode::Ss_PI),
            0x81 => Some(Opcode::Ss_NULL_T),
            0x90 => Some(Opcode::Im_Syscall),
            0x91 => Some(Opcode::Im_RegisterCb),
            0x92 => Some(Opcode::Im_KeyQuery),
            0x93 => Some(Opcode::Im_Exit),
            0xA0 => Some(Opcode::K_TYPEOF),
            0xA1 => Some(Opcode::K_IS_A),
            0xB0 => Some(Opcode::Pos_NewObj),
            0xB1 => Some(Opcode::Pos_NewStr),
            0xB2 => Some(Opcode::Pos_AllocArr),
            0xB3 => Some(Opcode::Pos_Spawn),
            0xB4 => Some(Opcode::Pos_OpenCh),
            0xB5 => Some(Opcode::Pos_PushFr),
            0xB6 => Some(Opcode::Pos_NewCtx),
            0xB7 => Some(Opcode::Pos_Pin),
            0xB8 => Some(Opcode::Pos_RefInc),
            0xB9 => Some(Opcode::Pos_Lock),
            0xBA => Some(Opcode::Pos_OpenSc),
            0xBB => Some(Opcode::Pos_AllocP),
            0xBC => Some(Opcode::Pos_ArenaB),
            0xBD => Some(Opcode::Pos_Activate),
            0xC0 => Some(Opcode::Neg_DelObj),
            0xC1 => Some(Opcode::Neg_DelStr),
            0xC2 => Some(Opcode::Neg_FreeArr),
            0xC3 => Some(Opcode::Neg_Kill),
            0xC4 => Some(Opcode::Neg_CloseCh),
            0xC5 => Some(Opcode::Neg_PopFr),
            0xC6 => Some(Opcode::Neg_DelCtx),
            0xC7 => Some(Opcode::Neg_Unpin),
            0xC8 => Some(Opcode::Neg_RefDec),
            0xC9 => Some(Opcode::Neg_Unlock),
            0xCA => Some(Opcode::Neg_CloseSc),
            0xCB => Some(Opcode::Neg_FreeP),
            0xCC => Some(Opcode::Neg_ArenaE),
            0xCD => Some(Opcode::Neg_Deact),
            0xD0 => Some(Opcode::T_Tick),
            0xD1 => Some(Opcode::T_Sleep),
            0xD2 => Some(Opcode::T_FrameSyn),
            _ => None,
        } // match
    } // fn from_u8
} // impl Opcode
5.2 Core Virtual Machine Execution Update (cpu.rs)
Rust
// uuid: c90a14b3-d82e-4b21-97b4-3a551de9162f
// triskele-vm/src/cpu/mod.rs

pub struct Cpu {
    /// 32 General Purpose Registers widened to 64-bit values.
    /// Standard allocations: R28=FP, R29=SP, R30=LR, R31=PC
    pub regs: [u64; 32],
    pub halted: bool,
} // struct Cpu

impl Cpu {
    pub fn new() -> Self {
        Self {
            regs: [0; 32],
            halted: false,
        } // Self
    } // fn new

    pub fn execute_instruction(&mut self, instruction: u32, memory: &mut [u8]) {
        let opcode_byte = (instruction >> 24) as u8;
        let dst  = ((instruction >> 19) & 0x1F) as usize;
        let src1 = ((instruction >> 14) & 0x1F) as usize;
        let src2 = ((instruction >> 9)  & 0x1F) as usize;
        
        let imm19 = (instruction & 0x7FFFF) as i32;
        let sign_extended_imm = (((imm19 << 13) >> 13) as i64) as u64;

        let opcode = match crate::isa::Opcode::from_u8(opcode_byte) {
            Some(op) => op,
            None => {
                self.halted = true;
                return;
            } // None
        }; // match

        match opcode {
            Opcode::D_MOV_I => {
                self.regs[dst] = sign_extended_imm;
            } // D_MOV_I

            Opcode::V_ADD => {
                self.regs[dst] = self.regs[src1].wrapping_add(self.regs[src2]);
            } // V_ADD

            Opcode::L_DEREF_W => {
                let addr = self.regs[src1] as usize;
                let b0 = memory[addr] as u32;
                let b1 = memory[addr + 1] as u32;
                let b2 = memory[addr + 2] as u32;
                let b3 = memory[addr + 3] as u32;
                let val_u32 = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24);
                self.regs[dst] = (val_u32 as i32 as i64) as u64;
            } // L_DEREF_W

            Opcode::L_DEREF_Q => {
                let addr = self.regs[src1] as usize;
                let mut bytes = [0u8; 8];
                bytes.copy_from_slice(&memory[addr..addr + 8]);
                self.regs[dst] = u64::from_le_bytes(bytes);
            } // L_DEREF_Q

            Opcode::L_STORE_Q => {
                let addr = self.regs[dst] as usize;
                let bytes = self.regs[src1].to_le_bytes();
                memory[addr..addr + 8].copy_from_slice(&bytes);
            } // L_STORE_Q

            _ => { /* Additional opcodes lowered to 64-bit internal targets */ }
        } // match
    } // fn execute_instruction
} // impl Cpu
5.3 Code Generation Immediate Expansion Strategy (codegen.rs)
Rust
// uuid: e21d3f54-b4a1-432d-88b9-85fc74e2cf6a
// tsk-cc/src/codegen.rs

impl FuncGen {
    /// Lowers absolute 64-bit immediate values into 32-bit instruction segments.
    /// Uses low-overhead immediate loads when matching the imm19 boundary,
    /// or cascades sequentially across scratch channels if required.
    fn emit_load_const64(&mut self, dst_reg: u8, value: i64) {
        if value >= -262144 && value <= 262143 {
            self.emit_i(Opcode::D_MOV_I, dst_reg, value as i32);
        } else {
            let mut current = value;
            let mut shifts = 0;
            
            let low_part = (current & 0x7FFFF) as i32;
            self.emit_i(Opcode::D_MOV_I, dst_reg, low_part);
            
            current >>= 19;
            shifts += 19;
            
            while current != 0 && current != -1 {
                let chunk = (current & 0x7FFFF) as i32;
                if chunk != 0 {
                    self.emit_i(Opcode::D_MOV_I, REG_SCRATCH as u8, chunk);
                    self.emit_r(Opcode::V_SHL, REG_SCRATCH as u8, REG_SCRATCH as u8, 0, shifts);
                    self.emit_r(Opcode::V_OR, dst_reg, dst_reg, REG_SCRATCH as u8, 0);
                } // if
                current >>= 19;
                shifts += 19;
            } // while
        } // else
    } // fn emit_load_const64
} // impl FuncGen

6. Strategic Architecture Recommendations
To maximize execution throughput and avoid code bloat on wide immediate sequences, the following design guidelines are recommended for further development cycles with Claude AI:

Leverage a Constant Pool (.rodata Priority): Update the tsk-cc chunk layout pipeline to place arbitrary large numerical constants and global label offsets into .rodata during code collection. Emitting an efficient combined sequence of L_LEA + L_DEREF_Q reduces instruction parsing pressure.

Exhaust Category Capacity with Structural Escape Opcodes: With the strict limitation of 16 indices per opcode category enforced by the M3 byte layout ([4-bit category | 4-bit index]), use index 0xF as an explicit Escape Indicator. When detected, the decoder checks internal instruction flags to dynamically expand the instruction space, avoiding category starvation.

Pipelined SIMD (Vector Category Optimization): The structural group V_ possesses a strong geometry-focused footprint. Dedicating future implementation loops toward defining explicit 4-element single-instruction multiple-data operations (SIMD lanes) will drastically accelerate spatial rendering computations.