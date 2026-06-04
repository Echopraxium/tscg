# TriskeleToolchain — Rust Workspace File Tree
# Author: Echopraxium with the collaboration of Claude AI
# Version: 0.2.0 — 2026-05-31
# Status: triskele-common ✓ complet | triskele-vm ✓ core | tsk-asm/dis/link/build ⬜ stubs
#
# cargo test : 32 tests — 32 OK — 0 échec
# Milestone  : test_hello_world_milestone ✓

triskele-toolchain/
│
├── Cargo.toml                          ← workspace manifest (resolver="2", edition 2021)
├── Cargo.lock
│
└── crates/
    │
    ├── triskele-common/                ← [✓] types partagés ISA + formats
    │   ├── Cargo.toml
    │   └── src/
    │       ├── lib.rs                  ← pub use de tous les modules
    │       ├── isa.rs                  ← OpcodeCategory (16) + Opcode (256) + format_base16()
    │       │                             #![allow(non_camel_case_types)] — notation TSCG obligatoire
    │       │                             tests: opcode_roundtrip, wolf3d_critical_opcodes,
    │       │                                    notation_convention, pole_symmetry
    │       ├── registers.rs            ← RegisterFile (32×64b) + Flags
    │       │                             REG_FP=28 SP=29 LR=30 PC=31
    │       │                             update_flags_add/sub/cmp()
    │       ├── tvm.rs                  ← TvmFile, Section, SectionType (14 types)
    │       │                             TvmBuilder (in-memory .tvx builder pour tests)
    │       │                             load_from_file() / load_from_reader()
    │       ├── error.rs                ← VmError (PartialEq + thiserror)
    │       │                             From<io::Error> manuel (préserve PartialEq)
    │       └── fixed.rs                ← Fixed = i32, virgule fixe 16.16
    │                                     fixed_mul / fixed_div / float_to_fixed / fixed_to_float
    │                                     FIXED_ONE / FIXED_PI / FIXED_2PI
    │
    ├── triskele-vm/                    ← [✓] interpréteur registres 32-bit
    │   ├── Cargo.toml                  ← bin "tskvm"
    │   └── src/
    │       ├── lib.rs                  ← pub mod cpu, memory, ffi, io
    │       ├── main.rs                 ← CLI tskvm --debug --trace <program.tvx>
    │       │
    │       ├── cpu/
    │       │   ├── decode.rs           ← decode(u32) → Instruction (R/I/J)
    │       │   │                         encode_r/i/j() pour tests et tsk-asm
    │       │   │                         is_jump_opcode() / is_immediate_opcode()
    │       │   │                         sign_extend_24() / sign_extend_19()
    │       │   └── mod.rs              ← Cpu struct + boucle principale run()
    │       │                             exec_r() — A_ St_ D_ V_ R_ O_ T_ Ss_ L_ _^_ _$_ Im_
    │       │                             exec_i() — D_MovI A_PushI V_CmpI D_Load/Store F_Trap
    │       │                             exec_j() — F_Jmp/Jz/Jnz/Jl/Jg/Jge/Jle F_Loop F_Call
    │       │                             tests: hello_world_milestone ✓ d_add ✓ f_halt ✓
    │       │
    │       ├── memory/
    │       │   ├── mod.rs              ← Memory (Vec<u8> linéaire, base 64b)
    │       │   │                         read/write u8/u16/u32/u64 + bytes
    │       │   │                         memcpy() / memset() / load_section()
    │       │   │                         NULL_PAGE_END=0x1000 STACK_TOP=0x70000000
    │       │   │                         HEAP_BASE=0x80000000
    │       │   ├── stack.rs            ← Stack (LIFO, croît vers le bas)
    │       │   │                         push/pop/peek/swap/dup/depth
    │       │   │                         enter_frame() / leave_frame() (A_ENTER/A_LEAVE)
    │       │   ├── heap.rs             ← Heap (bump + free list, Phase 1 manuel)
    │       │   │                         alloc/alloc_zeroed/free/realloc
    │       │   └── arena.rs            ← ArenaAllocator (Z_Malloc style)
    │       │                             arena_begin() ← _^_ARENA_B (0xBE)
    │       │                             arena_alloc() — sous-allocation dans arène active
    │       │                             arena_end()   ← _$_ARENA_E (0xCC)
    │       │
    │       ├── ffi/
    │       │   └── mod.rs              ← [⬜ stub] FfiDispatch — Im_FB_BLIT/Im_REGISTER_CB
    │       │                             (Phase 1 Wolf3D : SDL2 bindings)
    │       └── io/
    │           └── mod.rs              ← [⬜ stub] IoDispatch — Im_FILE_RD/WR/OP
    │
    ├── tsk-asm/                        ← [⬜ stub] assembleur .tsk → .tvx
    │   ├── Cargo.toml
    │   └── src/main.rs
    │
    ├── tsk-dis/                        ← [⬜ stub] désassembleur .tvx → listing annoté
    │   ├── Cargo.toml
    │   └── src/main.rs
    │
    ├── tsk-link/                       ← [⬜ stub] linker .tobj + .tva → .tvx
    │   ├── Cargo.toml
    │   └── src/main.rs
    │
    └── tsk-build/                      ← [⬜ stub] orchestrateur .tyml
        ├── Cargo.toml
        └── src/main.rs

# ─────────────────────────────────────────────────────────────────────────────
# État des opcodes implémentés dans exec_r/exec_i/exec_j (cpu/mod.rs)
# ─────────────────────────────────────────────────────────────────────────────
#
# A_   ✓  Push Pop Peek Swap Dup Depth Enter Leave Alloc AllocZ Free HeapSz
# St_  ✓  Nop
# F_   ✓  Jmp JmpR Call Ret Jz Jnz Jl Jle Jg Jge Loop (via exec_j)
#         Trap (exec_i) | F_Halt → TODO (actuellement passe dans _ =>)
# It_  ⬜  (stubs silencieux)
# D_   ✓  Mov MovI MovI64 Xchg Load8/16/32/64 Store8/32/64 Memcpy Memset Add Sub
# R_   ✓  I2F F2I Sign8 Sign16 Zero8 Zero16 Fix2F F2Fix
# E_   ⬜  (stubs silencieux)
# V_   ✓  Cmp CmpI Eq Neq Lt Lte Gt Gte Assert Null
# O_   ✓  DumpReg Log TraceOn TraceOff TimeRd Break
# Im_  ✓  Exit | FbBlit/RegisterCb → TODO (FFI SDL2, Phase 1)
# T_   ✓  Tick
# _^_  ✓  ArenaB | Lock (no-op Phase 1)
# _$_  ✓  ArenaE | Unlock (no-op Phase 1)
# K_   ⬜  (stubs silencieux)
# Ss_  ✓  Pi
# L_   ✓  Lea Deref DerefW Null IsNull FarCall FarJmp
#
# ─────────────────────────────────────────────────────────────────────────────
# Prochaines priorités
# ─────────────────────────────────────────────────────────────────────────────
#
# 1. F_Halt → wirer comme Halted(0) dans exec_r
# 2. F_Ret  → restaurer PC ← LR
# 3. tsk-asm — parser .tsk → .tvx (milestone : wolf3d_hello.tsk exécutable)
# 4. ffi/sdl2.rs — Im_FbBlit + Im_RegisterCb + T_FrameSyn (Phase 1 Wolf3D)
