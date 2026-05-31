---
name: tscg-rust-vm
description: >
  Skill for implementing TriskeleVM and the TriskeleToolchain in Rust.
  Use this skill whenever Michel asks to implement, extend, or debug any
  component of the TriskeleToolchain in Rust: the VM interpreter loop,
  ISA opcode execution, memory management (stack/heap/arenas), FFI bindings
  to SDL2/libc, Im_REGISTER_CB callbacks (C→Rust), the tsk-asm assembler,
  tsk-dis disassembler, tsk-link linker, or tsk-build orchestrator.
  Also use when creating Cargo.toml files, workspace structures, or when
  discussing Rust patterns specific to TriskeleVM (unsafe FFI, libloading,
  arena allocators, register-based interpreter dispatch).
  Do NOT use for BabylonJS simulations, Python scripts, or JSON-LD ontology
  work — those have their own skills.
---

# Rust VM Skill — TriskeleToolchain

Implementation guide for TriskeleVM and the TriskeleToolchain in Rust.

---

## 0. Read First — ISA Reference

**MANDATORY**: Before writing any opcode-related code, consult:
```
instances/symbolic-system-grammars/TriskeleToolchain/TriskeleVM_ISA_Reference_v020.md
```

Key conventions to internalize:
- **Indexed notation**: `St_` `It_` `Ss_` `Im_` — NEVER `S_` `I_`
- **16 categories**: `A_` `St_` `F_` `It_` `D_` `R_` `E_` `V_` `O_` `Im_` `T_` `_^_` `_$_` `K_` `Ss_` `L_`
- **Encoding**: `opcode_byte = [4-bit category | 4-bit instruction_index]`
- **Instruction format**: 32-bit fixed (Type R / Type I / Type J / Type X)
- **Register file**: 32 × 64-bit (R0–R31, aliases FP=R28, SP=R29, LR=R30, PC=R31)

---

## 1. Workspace Structure

```
triskele-toolchain/          ← Cargo workspace root
  Cargo.toml                 ← workspace manifest
  crates/
    triskele-common/         ← shared types, ISA, .tvm format
    triskele-vm/             ← VM interpreter (main crate)
      src/
        main.rs              ← CLI entry point
        lib.rs               ← public API
        cpu/
          mod.rs             ← CPU state, main run loop
          decode.rs          ← 32-bit instruction decoder
          execute.rs         ← opcode dispatch (per category)
          registers.rs       ← register file (32 × 64-bit)
        memory/
          mod.rs             ← linear address space
          stack.rs           ← A_PUSH/A_POP/A_ENTER/A_LEAVE
          heap.rs            ← A_ALLOC/A_FREE
          arena.rs           ← _^_ARENA_B/_$_ARENA_E (Z_Malloc)
          gc.rs              ← E_GC_RUN/E_GC_CFG
        ffi/
          mod.rs             ← FFI dispatch table
          sdl2.rs            ← Im_FB_BLIT/Im_INPUT_RD/Im_REGISTER_CB
          loader.rs          ← E_LOAD_MOD (libloading)
        io/
          mod.rs             ← Im_FILE_RD/WR/OP
          framebuffer.rs     ← Wolf3D framebuffer management
    tsk-asm/                 ← assembler
    tsk-dis/                 ← disassembler
    tsk-link/                ← linker
    tsk-build/               ← build orchestrator
```

---

## 2. Cargo.toml Patterns

### 2.1 Workspace root

```toml
[workspace]
name    = "triskele-toolchain"
version = "0.2.0"
edition = "2021"
members = [
    "crates/triskele-common",
    "crates/triskele-vm",
    "crates/tsk-asm",
    "crates/tsk-dis",
    "crates/tsk-link",
    "crates/tsk-build",
]

[workspace.dependencies]
serde      = { version = "1", features = ["derive"] }
serde_yaml = "0.9"
clap       = { version = "4", features = ["derive"] }
anyhow     = "1"
thiserror  = "1"
colored    = "2"
rustyline  = "14"
memmap2    = "0.9"
fnv        = "1"
log        = "0.4"
env_logger = "0.11"
sdl2       = { version = "0.36", features = ["unsafe_textures"] }
libloading = "0.8"
triskele-common = { path = "crates/triskele-common" }

[profile.release]
opt-level     = 3
lto           = true
codegen-units = 1
panic         = "abort"   # Wolf3D: smaller binary
```

### 2.2 Individual crate

```toml
[package]
name    = "triskele-vm"
version.workspace = true
edition.workspace = true
authors.workspace = true

[dependencies]
triskele-common = { workspace = true }
sdl2            = { workspace = true }
libloading      = { workspace = true }
anyhow          = { workspace = true }
clap            = { workspace = true }
log             = { workspace = true }
env_logger      = { workspace = true }
```

---

## 3. ISA Encoding in Rust

### 3.1 Category enum (4 high bits of opcode)

```rust
// triskele-common/src/isa.rs

/// M3-grounded opcode categories — 4 high bits of opcode byte
/// Notation: St_ It_ Ss_ Im_ mandatory (never S_ I_)
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpcodeCategory {
    // Gt — Territory (monoïde ×)
    A   = 0x0,   // Attractor    — Stack + Heap (2 memory attractors)
    St  = 0x1,   // Structure    — Types/structs/NOP (static layout)
    F   = 0x2,   // Flow         — Execution flow (JMP/CALL/RET/IF/coroutines)
    It  = 0x3,   // Information  — Informational state (flags/events/IRQ)
    D   = 0x4,   // Dynamics     — All modifications (MOV/LOAD/STORE/ADD/AND)

    // Gm — Map (monoïde +)
    R   = 0x5,   // Representability — Type conversions (I2F/F2FIX)
    E   = 0x6,   // Evolvability  — Self-transformation + adaptive GC
    V   = 0x7,   // Verifiability — Comparisons/assertions (CMP/ASSERT)
    O   = 0x8,   // Observability — Debug/introspection (DUMP/TRACE)
    Im  = 0x9,   // Interoperability — FFI/syscalls/SDL2

    // Gs — Stereopsis (monoïde |)
    T   = 0xA,   // Temporality  — Timing/sync (TICK/FRAME_SYN)
    Pos = 0xB,   // PositivePole — Creation/onset (_^_NEW/_^_SPAWN)
    Neg = 0xC,   // NegativePole — Destruction/terminus (_$_DEL/_$_KILL)
    K   = 0xD,   // Knowledge    — Reflection (TYPEOF/IS_A/SCHEMA)
    Ss  = 0xE,   // Symbol       — Signs/identifiers (INTERN/LOOKUP/PI)
    L   = 0xF,   // Localizability — Addressing (LEA/DEREF/FAR_CALL)
}

impl OpcodeCategory {
    pub fn from_byte(b: u8) -> Option<Self> {
        match b >> 4 {
            0x0 => Some(Self::A),  0x1 => Some(Self::St),
            0x2 => Some(Self::F),  0x3 => Some(Self::It),
            0x4 => Some(Self::D),  0x5 => Some(Self::R),
            0x6 => Some(Self::E),  0x7 => Some(Self::V),
            0x8 => Some(Self::O),  0x9 => Some(Self::Im),
            0xA => Some(Self::T),  0xB => Some(Self::Pos),
            0xC => Some(Self::Neg),0xD => Some(Self::K),
            0xE => Some(Self::Ss), 0xF => Some(Self::L),
            _ => None,
        }
    }

    /// Base16 Triskele name (for tsk-dis display)
    pub fn name(&self) -> &'static str {
        match self {
            Self::A => "A_", Self::St => "St_", Self::F => "F_",
            Self::It => "It_", Self::D => "D_", Self::R => "R_",
            Self::E => "E_", Self::V => "V_", Self::O => "O_",
            Self::Im => "Im_", Self::T => "T_", Self::Pos => "_^_",
            Self::Neg => "_$_", Self::K => "K_", Self::Ss => "Ss_",
            Self::L => "L_",
        }
    }
}
```

### 3.2 Opcode enum (full byte — all 256 opcodes)

```rust
/// Full opcodes — [category 4b | index 4b]
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Opcode {
    // A_ — Attractor (Stack + Heap)
    A_Push    = 0x00, A_Pop     = 0x01, A_PushI   = 0x02,
    A_Peek    = 0x03, A_Swap    = 0x04, A_Dup     = 0x05,
    A_Depth   = 0x06, A_StackF  = 0x07, A_Enter   = 0x08,
    A_Leave   = 0x09, A_Alloc   = 0x0A, A_AllocZ  = 0x0B,
    A_Realloc = 0x0C, A_Free    = 0x0D, A_HeapSz  = 0x0E,
    A_GcRun   = 0x0F,

    // St_ — Structure (types/structs/NOP)
    St_Nop      = 0x10, St_DefStruct = 0x11, St_DefArray  = 0x12,
    St_DefUnion = 0x13, St_DefEnum   = 0x14, St_DefAlias  = 0x15,
    St_FieldOff = 0x16, St_ElemOff   = 0x17, St_Sizeof    = 0x18,
    St_Alignof  = 0x19, St_Stride    = 0x1A, St_Pack      = 0x1B,
    St_Unpack   = 0x1C, St_Endian    = 0x1D, St_Layout    = 0x1E,
    St_CastLay  = 0x1F,

    // F_ — Flow (execution flow + coroutines)
    F_Jmp    = 0x20, F_JmpR   = 0x21, F_Call   = 0x22,
    F_Ret    = 0x23, F_RetN   = 0x24, F_Jz     = 0x25,
    F_Jnz    = 0x26, F_Jl     = 0x27, F_Jle    = 0x28,
    F_Jg     = 0x29, F_Jge    = 0x2A, F_Loop   = 0x2B,
    F_Switch = 0x2C, F_Trap   = 0x2D, F_Halt   = 0x2E,
    F_Yield  = 0x2F,

    // It_ — Information (state + events + IRQ)
    It_DefFlag   = 0x30, It_DefState  = 0x31, It_DefEvent = 0x32,
    It_DefIrq    = 0x33, It_GetFlag   = 0x34, It_TestFlag = 0x35,
    It_GetState  = 0x36, It_Pending   = 0x37, It_SetFlag  = 0x38,
    It_ClrFlag   = 0x39, It_TogFlag   = 0x3A, It_SetState = 0x3B,
    It_Emit      = 0x3C, It_Subscribe = 0x3D, It_Unsub    = 0x3E,
    It_IrqOn     = 0x3F,

    // D_ — Dynamics (all modifications: MOV/LOAD/STORE/arithmetic/bitwise)
    D_Mov    = 0x40, D_MovI   = 0x41, D_MovI64 = 0x42,
    D_Xchg   = 0x43, D_Load8  = 0x44, D_Load16 = 0x45,
    D_Load32 = 0x46, D_Load64 = 0x47, D_Store8 = 0x48,
    D_Store16= 0x49, D_Store32= 0x4A, D_Store64= 0x4B,
    D_Memcpy = 0x4C, D_Memset = 0x4D, D_Add    = 0x4E,
    D_Sub    = 0x4F,
    // Extended: D_Mul D_Div D_Mod D_And D_Or D_Xor D_Shl D_Shr
    // D_FixMul D_FixDiv D_MulDiv D_Neg D_Abs D_Inc D_Dec

    // R_ — Representability (type conversions)
    R_I2F    = 0x50, R_F2I    = 0x51, R_I2F64  = 0x52,
    R_F2I64  = 0x53, R_F3264  = 0x54, R_F6432  = 0x55,
    R_Sign8  = 0x56, R_Sign16 = 0x57, R_Zero8  = 0x58,
    R_Zero16 = 0x59, R_Trunc  = 0x5A, R_Round  = 0x5B,
    R_Fix2F  = 0x5C, R_F2Fix  = 0x5D, R_Pack   = 0x5E,
    R_Unpack = 0x5F,

    // E_ — Evolvability (self-transformation + adaptive GC)
    E_LoadMod  = 0x60, E_Unload   = 0x61, E_Bind     = 0x62,
    E_Caps     = 0x63, E_Feature  = 0x64, E_Fallback = 0x65,
    E_Patch    = 0x66, E_Hook     = 0x67, E_Unhook   = 0x68,
    E_Version  = 0x69, E_Sandbox  = 0x6A, E_Snapshot = 0x6B,
    E_Restore  = 0x6C, E_GcCfg    = 0x6D, E_GcTune   = 0x6E,
    E_MemPool  = 0x6F,

    // V_ — Verifiability (comparisons/assertions)
    V_Cmp    = 0x70, V_CmpI   = 0x71, V_Test   = 0x72,
    V_Eq     = 0x73, V_Neq    = 0x74, V_Lt     = 0x75,
    V_Lte    = 0x76, V_Gt     = 0x77, V_Gte    = 0x78,
    V_Assert = 0x79, V_Check  = 0x7A, V_TypeEq = 0x7B,
    V_Range  = 0x7C, V_Null   = 0x7D, V_Ovflow = 0x7E,
    V_Parity = 0x7F,

    // O_ — Observability (debug/introspection/profiling)
    O_DumpReg  = 0x80, O_DumpStk  = 0x81, O_DumpMem  = 0x82,
    O_TraceOn  = 0x83, O_TraceOff = 0x84, O_Break    = 0x85,
    O_Watch    = 0x86, O_Log      = 0x87, O_PerfRst  = 0x88,
    O_PerfRd   = 0x89, O_StackTr  = 0x8A, O_CovMark  = 0x8B,
    O_InspHeap = 0x8C, O_TimeRd   = 0x8D, O_Annotate = 0x8E,
    O_NopD     = 0x8F,

    // Im_ — Interoperability (FFI/syscalls/SDL2)
    Im_Syscall    = 0x90, Im_FfiCall   = 0x91, Im_FbBlit    = 0x92,
    Im_FbClear    = 0x93, Im_InputRd   = 0x94, Im_Audio     = 0x95,
    Im_FileRd     = 0x96, Im_FileWr    = 0x97, Im_FileOp    = 0x98,
    Im_RegisterCb = 0x99, Im_UnregCb   = 0x9A, Im_CbInvoke  = 0x9B,
    Im_MemMap     = 0x9C, Im_Shared    = 0x9D, Im_TimeHost  = 0x9E,
    Im_Exit       = 0x9F,

    // T_ — Temporality (timing/synchronization)
    T_Tick     = 0xA0, T_Wait     = 0xA1, T_Sleep    = 0xA2,
    T_Yield    = 0xA3, T_TimerSet = 0xA4, T_TimerClr = 0xA5,
    T_FrameSyn = 0xA6, T_Delta    = 0xA7, T_Timeout  = 0xA8,
    T_Pause    = 0xA9, T_Resume   = 0xAA, T_Sched    = 0xAB,
    T_AtomicB  = 0xAC, T_AtomicE  = 0xAD, T_Barrier  = 0xAE,
    T_Watchdog = 0xAF,

    // _^_ — PositivePole (creation/onset)
    Pos_NewObj   = 0xB0, Pos_NewStr   = 0xB1, Pos_NewArr   = 0xB2,
    Pos_Clone    = 0xB3, Pos_Spawn    = 0xB4, Pos_OpenCh   = 0xB5,
    Pos_PushFr   = 0xB6, Pos_NewCtx   = 0xB7, Pos_Intern   = 0xB8,
    Pos_Pin      = 0xB9, Pos_RefInc   = 0xBA, Pos_Lock     = 0xBB,
    Pos_OpenSc   = 0xBC, Pos_AllocP   = 0xBD, Pos_ArenaB   = 0xBE,
    Pos_Activate = 0xBF,

    // _$_ — NegativePole (destruction/terminus)
    Neg_DelObj   = 0xC0, Neg_DelStr   = 0xC1, Neg_FreeArr  = 0xC2,
    Neg_Kill     = 0xC3, Neg_CloseCh  = 0xC4, Neg_PopFr    = 0xC5,
    Neg_DelCtx   = 0xC6, Neg_Unpin    = 0xC7, Neg_RefDec   = 0xC8,
    Neg_Unlock   = 0xC9, Neg_CloseSc  = 0xCA, Neg_FreeP    = 0xCB,
    Neg_ArenaE   = 0xCC, Neg_Deact    = 0xCD, Neg_Purge    = 0xCE,
    Neg_Abort    = 0xCF,

    // K_ — Knowledge (reflection/metadata)
    K_Typeof   = 0xD0, K_Sizeof   = 0xD1, K_Alignof  = 0xD2,
    K_Fields   = 0xD3, K_FieldGet = 0xD4, K_FieldSet = 0xD5,
    K_IsA      = 0xD6, K_Cast     = 0xD7, K_SymLook  = 0xD8,
    K_SymName  = 0xD9, K_AnnGet   = 0xDA, K_AnnSet   = 0xDB,
    K_Schema   = 0xDC, K_Validate = 0xDD, K_Version  = 0xDE,
    K_Describe = 0xDF,

    // Ss_ — Symbol (signs/identifiers/predefined constants)
    // Ss_ = the SIGN (identifier "main", '\0', PI)
    // It_ = the VALUE signified (0x1000, 0x00, 3.14)
    // Ss_Lookup resolves Ss → It
    Ss_Intern   = 0xE0, Ss_Lookup   = 0xE1, Ss_Hash     = 0xE2,
    Ss_CmpId    = 0xE3, Ss_Mangle   = 0xE4, Ss_Demangle = 0xE5,
    Ss_NullT    = 0xE6, Ss_StrDlm   = 0xE7, Ss_NsSep    = 0xE8,
    Ss_Escape   = 0xE9, Ss_Pi       = 0xEA, Ss_ECst     = 0xEB,
    Ss_Sqrt2    = 0xEC, Ss_Inf      = 0xED, Ss_Nan      = 0xEE,
    Ss_AddrCode = 0xEF,

    // L_ — Localizability (addressing/pointers)
    // L_FarCall is L_ (not F_): target localization dominates over flow
    L_Lea      = 0xF0, L_Addr     = 0xF1, L_Offset   = 0xF2,
    L_Idx      = 0xF3, L_Deref    = 0xF4, L_DerefW   = 0xF5,
    L_Null     = 0xF6, L_IsNull   = 0xF7, L_BoundChk = 0xF8,
    L_Align    = 0xF9, L_Page     = 0xFA, L_Glob     = 0xFB,
    L_Tls      = 0xFC, L_Relocate = 0xFD, L_FarCall  = 0xFE,
    L_FarJmp   = 0xFF,
}

impl Opcode {
    pub fn from_byte(b: u8) -> Option<Self> {
        Some(unsafe { std::mem::transmute(b) })
    }
    pub fn category(&self) -> OpcodeCategory {
        OpcodeCategory::from_byte(*self as u8).unwrap()
    }
}
```

---

## 4. Register File

```rust
// triskele-vm/src/cpu/registers.rs

pub const REG_COUNT: usize = 32;
pub const REG_FP: usize = 28;   // Frame Pointer
pub const REG_SP: usize = 29;   // Stack Pointer
pub const REG_LR: usize = 30;   // Link Register (return address)
pub const REG_PC: usize = 31;   // Program Counter

#[derive(Debug, Clone)]
pub struct RegisterFile {
    regs:  [u64; REG_COUNT],
    pub flags: Flags,
}

#[derive(Debug, Clone, Default)]
pub struct Flags {
    pub zero:     bool,   // ZF — result == 0
    pub negative: bool,   // NF — result < 0 (signed)
    pub overflow: bool,   // OF — arithmetic overflow
    pub carry:    bool,   // CF — unsigned overflow
}

impl RegisterFile {
    pub fn new(stack_top: u64) -> Self {
        let mut regs = [0u64; REG_COUNT];
        regs[REG_SP] = stack_top;
        regs[REG_FP] = stack_top;
        regs[REG_PC] = 0x0000_1000;  // .code base address
        Self { regs, flags: Flags::default() }
    }

    #[inline] pub fn get(&self, r: usize) -> u64       { self.regs[r] }
    #[inline] pub fn set(&mut self, r: usize, v: u64)  { self.regs[r] = v; }
    #[inline] pub fn sp(&self)  -> u64 { self.regs[REG_SP] }
    #[inline] pub fn fp(&self)  -> u64 { self.regs[REG_FP] }
    #[inline] pub fn lr(&self)  -> u64 { self.regs[REG_LR] }
    #[inline] pub fn pc(&self)  -> u64 { self.regs[REG_PC] }
    #[inline] pub fn set_pc(&mut self, v: u64) { self.regs[REG_PC] = v; }
    #[inline] pub fn inc_pc(&mut self, n: u64) { self.regs[REG_PC] += n; }

    pub fn update_flags(&mut self, result: u64, signed: bool) {
        self.flags.zero     = result == 0;
        self.flags.negative = signed && (result as i64) < 0;
    }
}
```

---

## 5. Instruction Decoder

```rust
// triskele-vm/src/cpu/decode.rs

#[derive(Debug, Clone, Copy)]
pub enum Instruction {
    /// Type R: [opcode 8b | dst 5b | src1 5b | src2 5b | flags 9b]
    R { op: Opcode, dst: u8, src1: u8, src2: u8, flags: u16 },
    /// Type I: [opcode 8b | dst 5b | imm19 signed]
    I { op: Opcode, dst: u8, imm: i32 },
    /// Type J: [opcode 8b | offset24 signed] (±8MB PC-relative)
    J { op: Opcode, offset: i32 },
    /// Type X: pool reference (L_Glob + constant pool)
    X { op: Opcode, dst: u8, pool_idx: u32 },
}

impl Instruction {
    pub fn decode(word: u32) -> Result<Self, DecodeError> {
        let op_byte = (word >> 24) as u8;
        let op = Opcode::from_byte(op_byte)
            .ok_or(DecodeError::InvalidOpcode(op_byte))?;

        match op.category() {
            OpcodeCategory::F => {
                // Flow opcodes: Type J (PC-relative jumps/calls)
                let offset = sign_extend_24((word & 0x00FF_FFFF) as i32);
                Ok(Instruction::J { op, offset })
            }
            _ if is_immediate_opcode(op) => {
                let dst = ((word >> 19) & 0x1F) as u8;
                let imm = sign_extend_19((word & 0x0007_FFFF) as i32);
                Ok(Instruction::I { op, dst, imm })
            }
            _ => {
                let dst   = ((word >> 19) & 0x1F) as u8;
                let src1  = ((word >> 14) & 0x1F) as u8;
                let src2  = ((word >>  9) & 0x1F) as u8;
                let flags = (word & 0x01FF) as u16;
                Ok(Instruction::R { op, dst, src1, src2, flags })
            }
        }
    }
}

fn sign_extend_24(v: i32) -> i32 {
    if v & 0x0080_0000 != 0 { v | !0x00FF_FFFF } else { v }
}
fn sign_extend_19(v: i32) -> i32 {
    if v & 0x0004_0000 != 0 { v | !0x0007_FFFF } else { v }
}

#[derive(Debug, thiserror::Error)]
pub enum DecodeError {
    #[error("Invalid opcode: 0x{0:02X}")]
    InvalidOpcode(u8),
}
```

---

## 6. VM Main Loop

```rust
// triskele-vm/src/cpu/mod.rs

pub struct Cpu {
    pub regs:   RegisterFile,
    pub memory: Memory,
    pub stack:  Stack,
    pub heap:   Heap,
    pub ffi:    FfiDispatch,
    running:    bool,
    debug:      bool,
}

impl Cpu {
    pub fn run(&mut self) -> anyhow::Result<i32> {
        while self.running {
            let word  = self.memory.read_u32(self.regs.pc())?;
            self.regs.inc_pc(4);
            let instr = Instruction::decode(word)?;
            match instr {
                Instruction::R { op, dst, src1, src2, flags } =>
                    self.execute_r(op, dst, src1, src2, flags)?,
                Instruction::I { op, dst, imm } =>
                    self.execute_i(op, dst, imm)?,
                Instruction::J { op, offset } =>
                    self.execute_j(op, offset)?,
                Instruction::X { op, dst, pool_idx } =>
                    self.execute_x(op, dst, pool_idx)?,
            }
        }
        Ok(self.regs.get(0) as i32)  // R0 = exit code
    }
}
```

---

## 7. Key Opcode Implementations

### 7.1 Flow control (F_ category — Type J)

```rust
pub fn execute_j(&mut self, op: Opcode, offset: i32) -> anyhow::Result<()> {
    let pc = self.regs.pc();
    let target = (pc as i64 + offset as i64) as u64;
    match op {
        Opcode::F_Jmp  => { self.regs.set_pc(target); }
        Opcode::F_Call => { self.regs.set(REG_LR, pc); self.regs.set_pc(target); }
        Opcode::F_Ret  => { self.regs.set_pc(self.regs.lr()); }
        Opcode::F_Jz   => { if  self.regs.flags.zero     { self.regs.set_pc(target); } }
        Opcode::F_Jnz  => { if !self.regs.flags.zero     { self.regs.set_pc(target); } }
        Opcode::F_Jl   => { if  self.regs.flags.negative { self.regs.set_pc(target); } }
        Opcode::F_Jge  => { if !self.regs.flags.negative { self.regs.set_pc(target); } }
        Opcode::F_Loop => {
            let cx = self.regs.get(0).wrapping_sub(1);
            self.regs.set(0, cx);
            if cx != 0 { self.regs.set_pc(target); }
        }
        Opcode::F_Halt  => { self.running = false; }
        Opcode::F_Yield => { self.yield_coroutine()?; }
        _ => {}
    }
    Ok(())
}
```

### 7.2 Dynamics (D_ category — all modifications)

```rust
// D_ covers: MOV, LOAD, STORE, arithmetic (ADD/SUB/MUL), bitwise (AND/OR/XOR/SHL)
// Key distinction: D_ = raw modification without named state semantics
//                  It_ = named state change (It_SET_FLAG GAME_OVER)

Opcode::D_Mov    => { self.regs.set(dst, self.regs.get(src1)); }
Opcode::D_Add    => {
    let r = self.regs.get(src1).wrapping_add(self.regs.get(src2));
    self.regs.set(dst, r);
    self.regs.update_flags(r, false);
}
Opcode::D_Load32 => {
    let addr = self.regs.get(src1) + self.regs.get(src2);
    let v    = self.memory.read_u32(addr)? as u64;
    self.regs.set(dst, v);
}
Opcode::D_Store32 => {
    let addr = self.regs.get(dst) + self.regs.get(src2);
    self.memory.write_u32(addr, self.regs.get(src1) as u32)?;
}
Opcode::D_Memcpy => {
    // Wolf3D critical — framebuffer copy
    self.memory.memcpy(self.regs.get(dst), self.regs.get(src1), self.regs.get(src2) as usize)?;
}
Opcode::D_Memset => {
    // Wolf3D critical — screen clear
    self.memory.memset(self.regs.get(dst), self.regs.get(src1) as u8, self.regs.get(src2) as usize)?;
}
```

### 7.3 Attractor — Stack + Heap (A_ category)

```rust
// Two memory attractors: Stack (LIFO) + Heap (dynamic)
Opcode::A_Push   => self.stack.push(self.regs.get(dst))?,
Opcode::A_Pop    => { let v = self.stack.pop()?; self.regs.set(dst, v); }
Opcode::A_Enter  => self.stack.enter_frame(&mut self.regs)?,
Opcode::A_Leave  => self.stack.leave_frame(&mut self.regs)?,
Opcode::A_Alloc  => {
    let ptr = self.heap.alloc(self.regs.get(src1) as usize)?;
    self.regs.set(dst, ptr);
}
Opcode::A_Free   => self.heap.free(self.regs.get(src1))?,
```

### 7.4 Localizability — FAR_CALL is L_ not F_

```rust
// L_FarCall: target localization (64-bit) is the dominant concern
// F_Call: execution flow is dominant (24-bit offset sufficient)
Opcode::L_FarCall => {
    let target = self.regs.get(src1);  // full 64-bit address
    self.regs.set(REG_LR, self.regs.pc());
    self.regs.set_pc(target);
}
Opcode::L_FarJmp => {
    self.regs.set_pc(self.regs.get(src1));
}
Opcode::L_Lea => {
    self.regs.set(dst, self.regs.get(src1).wrapping_add(self.regs.get(src2)));
}
Opcode::L_Deref => {
    let v = self.memory.read_u64(self.regs.get(src1))?;
    self.regs.set(dst, v);
}
Opcode::L_BoundChk => {
    let ptr = self.regs.get(src1);
    if ptr < self.regs.get(src2) || ptr >= flags as u64 {
        return Err(anyhow::anyhow!("L_BOUND_CHK failed: 0x{:X}", ptr));
    }
}
```

### 7.5 Symbol — Ss_ (sign) vs It_ (value)

```rust
// Ss_ = the SIGN (identifier name, predefined constant name)
// It_ = the VALUE signified (raw encoded value)
// Ss_Lookup resolves: Ss (sign) → It (value)

Opcode::Ss_Intern => {
    let ptr = self.regs.get(src1);
    let len = self.regs.get(src2) as usize;
    let id  = self.symbol_pool.intern(ptr, len, &self.memory)?;
    self.regs.set(dst, id);
}
Opcode::Ss_Lookup => {
    // Ss → It: resolve sign to value
    let id  = self.regs.get(src1);
    let val = self.symbol_pool.lookup(id)?;
    self.regs.set(dst, val);
}
Opcode::Ss_Pi => {
    // π as fixed 16.16 (Wolf3D raycaster: 0x0003243F)
    // Ss_Pi is the SIGN "PI" — value is It (fixed-point encoding)
    self.regs.set(dst, 0x0003_243F);
}
```

---

## 8. FFI — Im_REGISTER_CB (C → Rust callback)

```rust
// triskele-vm/src/ffi/sdl2.rs
// Critical pattern: unsafe extern "C" fn for C ABI compatibility

pub struct FfiDispatch {
    sdl_context: sdl2::Sdl,
    canvas:      sdl2::render::Canvas<sdl2::video::Window>,
    callbacks:   std::collections::HashMap<u32, u64>,  // event_id → vm_func_addr
    frame_timer: std::time::Instant,
}

impl FfiDispatch {
    /// Im_FB_BLIT — blit framebuffer to SDL2 screen (Wolf3D critical)
    pub fn sdl2_fb_blit(&mut self, fb_ptr: u64, w: u32, h: u32, memory: &Memory)
        -> anyhow::Result<()>
    {
        let data = memory.read_bytes(fb_ptr, (w * h * 4) as usize)?;
        let tc   = self.canvas.texture_creator();
        let mut tex = tc.create_texture_streaming(
            sdl2::pixels::PixelFormatEnum::RGBA32, w, h)?;
        tex.with_lock(None, |buf, _| buf.copy_from_slice(&data))?;
        self.canvas.copy(&tex, None, None)?;
        self.canvas.present();
        Ok(())
    }

    /// Im_REGISTER_CB — register VM function as SDL2 event callback
    pub fn register_callback(&mut self, event_id: u32, vm_func_addr: u64) {
        self.callbacks.insert(event_id, vm_func_addr);
    }

    /// Poll SDL2 events and dispatch to registered VM callbacks
    pub fn poll_events(&mut self, cpu: &mut Cpu) -> anyhow::Result<()> {
        let mut pump = self.sdl_context.event_pump()?;
        for event in pump.poll_iter() {
            let event_id = sdl_event_to_id(&event);
            if let Some(&vm_addr) = self.callbacks.get(&event_id) {
                cpu.invoke_vm_callback(vm_addr, &event)?;
            }
        }
        Ok(())
    }

    /// T_FRAME_SYN — synchronize to target FPS (Wolf3D: 35fps)
    pub fn frame_sync(&mut self, target_fps: u32) -> anyhow::Result<()> {
        let frame_dur = std::time::Duration::from_micros(1_000_000 / target_fps as u64);
        let elapsed   = self.frame_timer.elapsed();
        if elapsed < frame_dur { std::thread::sleep(frame_dur - elapsed); }
        self.frame_timer = std::time::Instant::now();
        Ok(())
    }

    /// E_LOAD_MOD — dynamic library loading (libloading)
    pub fn load_module(&mut self, path: &str) -> anyhow::Result<()> {
        unsafe {
            let lib = libloading::Library::new(path)?;
            self.loaded_libs.push(lib);
        }
        Ok(())
    }
}
```

---

## 9. Arena Allocator — _^_ARENA_B / _$_ARENA_E

```rust
// triskele-vm/src/memory/arena.rs
// Z_Malloc style — critical for Doom Phase 2

pub struct ArenaAllocator {
    arenas:    Vec<Arena>,
    next_base: u64,
}

struct Arena {
    id:     u64,
    base:   u64,
    size:   usize,
    offset: usize,
    active: bool,
}

impl ArenaAllocator {
    /// _^_ARENA_B — begin arena
    pub fn arena_begin(&mut self, size: usize) -> anyhow::Result<u64> {
        let id   = self.arenas.len() as u64;
        let base = self.next_base;
        self.arenas.push(Arena { id, base, size, offset: 0, active: true });
        self.next_base += size as u64;
        Ok(id)
    }

    /// Allocate within an active arena
    pub fn arena_alloc(&mut self, arena_id: u64, size: usize) -> anyhow::Result<u64> {
        let arena = self.arenas.get_mut(arena_id as usize)
            .ok_or_else(|| anyhow::anyhow!("Invalid arena: {}", arena_id))?;
        if !arena.active { return Err(anyhow::anyhow!("Arena {} is closed", arena_id)); }
        if arena.offset + size > arena.size { return Err(anyhow::anyhow!("Arena {} full", arena_id)); }
        let ptr = arena.base + arena.offset as u64;
        arena.offset += (size + 7) & !7;  // 8-byte alignment
        Ok(ptr)
    }

    /// _$_ARENA_E — end arena, release entire block in one shot
    pub fn arena_end(&mut self, arena_id: u64) -> anyhow::Result<()> {
        let arena = self.arenas.get_mut(arena_id as usize)
            .ok_or_else(|| anyhow::anyhow!("Invalid arena: {}", arena_id))?;
        arena.active = false;
        arena.offset = 0;
        Ok(())
    }
}
```

---

## 10. Fixed-Point 16.16 (Wolf3D raycaster)

```rust
// triskele-common/src/fixed.rs
// D_FixMul — performance-critical for Wolf3D

pub type Fixed = i32;

pub const FIXED_ONE:  Fixed = 0x0001_0000;   // 1.0
pub const FIXED_PI:   Fixed = 0x0003_243F;   // π  (Ss_Pi value)
pub const FIXED_2PI:  Fixed = 0x0006_487E;   // 2π

#[inline(always)]
pub fn fixed_mul(a: Fixed, b: Fixed) -> Fixed {
    ((a as i64 * b as i64) >> 16) as Fixed
}

#[inline(always)]
pub fn fixed_div(a: Fixed, b: Fixed) -> Fixed {
    (((a as i64) << 16) / b as i64) as Fixed
}

#[inline(always)]
pub fn fixed_muldiv(a: Fixed, b: Fixed, c: Fixed) -> Fixed {
    ((a as i64 * b as i64) / c as i64) as Fixed
}

/// R_F2Fix — float32 to fixed 16.16
#[inline(always)]
pub fn float_to_fixed(f: f32) -> Fixed { (f * 65536.0) as Fixed }

/// R_Fix2F — fixed 16.16 to float32
#[inline(always)]
pub fn fixed_to_float(x: Fixed) -> f32 { x as f32 / 65536.0 }
```

---

## 11. Base16 Triskele Display (tsk-dis)

```rust
// tsk-dis/src/base16.rs

/// Display u64 as Base16 Triskele sequence
/// e.g. 0x1A3F → "St·T·It·L"
pub fn format_base16(value: u64, nibbles: usize) -> String {
    let names = ["A","St","F","It","D","R","E","V","O","Im","T","_^","_$","K","Ss","L"];
    (0..nibbles).rev()
        .map(|i| names[((value >> (i * 4)) & 0xF) as usize])
        .collect::<Vec<_>>()
        .join("·")
}

/// ANSI colorize by M3 category
pub fn colorize_category(cat: OpcodeCategory, text: &str) -> String {
    let color = match cat {
        OpcodeCategory::A   => "\x1b[36m",      // cyan
        OpcodeCategory::St  => "\x1b[34m",      // blue
        OpcodeCategory::F   => "\x1b[32m",      // green
        OpcodeCategory::It  => "\x1b[33m",      // yellow
        OpcodeCategory::D   => "\x1b[35m",      // magenta
        OpcodeCategory::R   => "\x1b[37m",      // white
        OpcodeCategory::E   => "\x1b[97m",      // bright white
        OpcodeCategory::V   => "\x1b[96m",      // bright cyan
        OpcodeCategory::O   => "\x1b[94m",      // bright blue
        OpcodeCategory::Im  => "\x1b[92m",      // bright green
        OpcodeCategory::T   => "\x1b[93m",      // bright yellow
        OpcodeCategory::Pos => "\x1b[95m",      // bright magenta
        OpcodeCategory::Neg => "\x1b[31m",      // red
        OpcodeCategory::K   => "\x1b[91m",      // bright red
        OpcodeCategory::Ss  => "\x1b[38;5;208m",// orange
        OpcodeCategory::L   => "\x1b[38;5;135m",// purple
    };
    format!("{}{}\x1b[0m", color, text)
}
```

---

## 12. Common Error Types

```rust
// triskele-common/src/error.rs

#[derive(Debug, thiserror::Error)]
pub enum VmError {
    #[error("Invalid opcode: 0x{0:02X}")]
    InvalidOpcode(u8),
    #[error("Memory fault: addr=0x{addr:016X}, size={size}")]
    MemoryFault { addr: u64, size: usize },
    #[error("Stack overflow: SP=0x{0:016X}")]
    StackOverflow(u64),
    #[error("Stack underflow")]
    StackUnderflow,
    #[error("Heap out of memory: requested {0} bytes")]
    OutOfMemory(usize),
    #[error("FFI error: {0}")]
    FfiError(String),
    #[error("Undefined symbol: {0}")]
    UndefinedSymbol(String),
    #[error("Relocation overflow at 0x{addr:08X}: {dist:.1}MB > ±8MB")]
    RelocationOverflow { addr: u64, dist: f64 },
    #[error("F_TRAP: exception code {0}")]
    Trap(u8),
    #[error("V_ASSERT failed at PC=0x{0:08X}")]
    AssertFailed(u64),
}
```

---

## 13. Implementation Checklist

Before writing any opcode or module:

```
□ Read TriskeleVM_ISA_Reference_v020.md
□ Check category prefix (St_ It_ Ss_ Im_ — never S_ I_)
□ Check _^_/_$_ symmetry if implementing creation/destruction
□ Start with St_Nop (debug interpreter loop first)
□ Use anyhow::Result<()> for error propagation
□ Mark unsafe explicitly (SDL2 FFI, libloading)
□ Wolf3D critical: D_Memcpy/Memset, Im_FbBlit, T_FrameSyn, D_FixMul
□ Doom Phase 2: Pos_ArenaB / Neg_ArenaE (Z_Malloc style)
□ Ss_ vs It_: sign (identifier) vs value (encoded data)
□ F_Call vs L_FarCall: ±8MB offset vs 64-bit address
```

---

*TriskeleToolchain — Rust VM Skill v0.2.0*
*Echopraxium with the collaboration of Claude AI — 2026-05-31*
