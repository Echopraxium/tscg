// triskele-common/src/isa.rs — auto-suppressed Rust naming warnings
// The ISA uses TSCG notation (St_, It_, Ss_, Im_) which is mandatory by design.
#![allow(non_camel_case_types)]
// triskele-common/src/isa.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// ISA derived from the 16 monoidal primitives of TSCG M3 Structural Grammar.
// Encoding: opcode_byte = [4-bit category | 4-bit instruction_index]
//
// Notation convention (MANDATORY — never S_ or I_):
//   St_  Structure       (Territory/Gt)
//   It_  Information     (Territory/Gt)
//   Ss_  Symbol          (Stereopsis/Gs)
//   Im_  Interoperability (Map/Gm)

// ─────────────────────────────────────────────────────────────────────────────
// OpcodeCategory — 4 high bits of opcode byte
// ─────────────────────────────────────────────────────────────────────────────

/// 16 M3-grounded opcode categories.
/// Each answers a transdisciplinary M3 question about its primitive's identity.
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OpcodeCategory {
    // Gt — Territory Grammar (monoïde ×)
    A   = 0x0,  // Attractor        "Where do data converge?"    Stack + Heap
    St  = 0x1,  // Structure        "How organized?"             Types/structs/NOP
    F   = 0x2,  // Flow             "How does execution flow?"   JMP/CALL/RET/IF/coroutines
    It  = 0x3,  // Information      "What is the info state?"    Flags/events/IRQ
    D   = 0x4,  // Dynamics         "What modifies data?"        MOV/LOAD/STORE/ADD/AND

    // Gm — Map Grammar (monoïde +)
    R   = 0x5,  // Representability "Encodable in another form?" I2F/F2FIX/SIGN
    E   = 0x6,  // Evolvability     "Generates novelty?"         Modules/hooks/adaptive GC
    V   = 0x7,  // Verifiability    "Verifiable/falsifiable?"    CMP/ASSERT/RANGE
    O   = 0x8,  // Observability    "Measurable internally?"     DUMP/TRACE/BREAK
    Im  = 0x9,  // Interoperability "Interfaceable?"             FFI/SYSCALL/SDL2

    // Gs — Stereopsis Grammar (monoïde |)
    T   = 0xA,  // Temporality      "When?"                      TICK/FRAME_SYN/TIMER
    Pos = 0xB,  // Positive Pole    "Onset/activation?"          _^_NEW/_^_SPAWN/_^_ARENA_B
    Neg = 0xC,  // Negative Pole    "Terminus/dissolution?"      _$_DEL/_$_KILL/_$_ARENA_E
    K   = 0xD,  // Knowledge        "What is known?"             TYPEOF/IS_A/SCHEMA
    Ss  = 0xE,  // Symbol           "What is the sign?"          INTERN/LOOKUP/PI/NULL_T
    L   = 0xF,  // Localizability   "Converging toward?"         LEA/DEREF/FAR_CALL
}

impl OpcodeCategory {
    /// Parse the high nibble of an opcode byte.
    pub fn from_byte(b: u8) -> Option<Self> {
        match b >> 4 {
            0x0 => Some(Self::A),
            0x1 => Some(Self::St),
            0x2 => Some(Self::F),
            0x3 => Some(Self::It),
            0x4 => Some(Self::D),
            0x5 => Some(Self::R),
            0x6 => Some(Self::E),
            0x7 => Some(Self::V),
            0x8 => Some(Self::O),
            0x9 => Some(Self::Im),
            0xA => Some(Self::T),
            0xB => Some(Self::Pos),
            0xC => Some(Self::Neg),
            0xD => Some(Self::K),
            0xE => Some(Self::Ss),
            0xF => Some(Self::L),
            _   => None,
        }
    }

    /// Canonical prefix string for tsk-dis display.
    pub fn prefix(&self) -> &'static str {
        match self {
            Self::A   => "A_",
            Self::St  => "St_",
            Self::F   => "F_",
            Self::It  => "It_",
            Self::D   => "D_",
            Self::R   => "R_",
            Self::E   => "E_",
            Self::V   => "V_",
            Self::O   => "O_",
            Self::Im  => "Im_",
            Self::T   => "T_",
            Self::Pos => "_^_",
            Self::Neg => "_$_",
            Self::K   => "K_",
            Self::Ss  => "Ss_",
            Self::L   => "L_",
        }
    }

    /// M3 monoid group.
    pub fn monoid(&self) -> &'static str {
        match self {
            Self::A | Self::St | Self::F | Self::It | Self::D => "Gt",
            Self::R | Self::E  | Self::V  | Self::O  | Self::Im => "Gm",
            Self::T | Self::Pos | Self::Neg | Self::K | Self::Ss | Self::L => "Gs",
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Opcode — full byte (all 256 opcodes)
// ─────────────────────────────────────────────────────────────────────────────

/// Full 256-opcode ISA derived from TriskeleVM_ISA_Reference_v020.md
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Opcode {
    // ── A_ Attractor (0x0_) ── Stack + Heap ──────────────────────────────────
    A_Push      = 0x00,  // push reg → SP
    A_Pop       = 0x01,  // pop SP → reg
    A_PushI     = 0x02,  // push imm32 → SP
    A_Peek      = 0x03,  // read top without popping
    A_Swap      = 0x04,  // swap top 2 stack entries
    A_Dup       = 0x05,  // duplicate top
    A_Depth     = 0x06,  // stack depth → reg
    A_StackF    = 0x07,  // create activation frame
    A_Enter     = 0x08,  // procedure prologue (auto)
    A_Leave     = 0x09,  // procedure epilogue (auto)
    A_Alloc     = 0x0A,  // allocate N bytes → ptr
    A_AllocZ    = 0x0B,  // allocate N bytes zeroed → ptr
    A_Realloc   = 0x0C,  // resize block
    A_Free      = 0x0D,  // free block
    A_HeapSz    = 0x0E,  // available heap size → reg
    A_GcRun     = 0x0F,  // force GC cycle

    // ── St_ Structure (0x1_) ── Types/structs/NOP ────────────────────────────
    St_Nop      = 0x10,  // no operation — structure preserved
    St_DefStruct= 0x11,  // define struct type (fields+offsets)
    St_DefArray = 0x12,  // define array type (element+size)
    St_DefUnion = 0x13,  // define union type
    St_DefEnum  = 0x14,  // define enum type
    St_DefAlias = 0x15,  // define type alias
    St_FieldOff = 0x16,  // field offset in struct → reg
    St_ElemOff  = 0x17,  // array element offset → reg
    St_Sizeof   = 0x18,  // type size in bytes → reg
    St_Alignof  = 0x19,  // required alignment → reg
    St_Stride   = 0x1A,  // array iteration stride → reg
    D_Mul       = 0x1B,  // reg = reg * reg  (integer multiply)
    D_Div       = 0x1C,  // reg = reg / reg  (signed integer divide)
    D_Rem       = 0x1D,  // reg = reg % reg  (signed integer remainder)
    St_Layout   = 0x1E,  // full type layout → buffer
    St_CastLay  = 0x1F,  // reinterpret_cast (reinterpret bytes)

    // ── F_ Flow (0x2_) ── Execution flow + coroutines ────────────────────────
    F_Jmp       = 0x20,  // unconditional jump (offset 24b)
    F_JmpR      = 0x21,  // relative jump (offset 16b signed)
    F_Call      = 0x22,  // call function (saves LR)
    F_Ret       = 0x23,  // return (restores LR)
    F_RetN      = 0x24,  // return + pop N args
    F_Jz        = 0x25,  // jump if zero (flags)
    F_Jnz       = 0x26,  // jump if not zero
    F_Jl        = 0x27,  // jump if less (signed)
    F_Jle       = 0x28,  // jump if less or equal
    F_Jg        = 0x29,  // jump if greater (signed)
    F_Jge       = 0x2A,  // jump if greater or equal
    F_Loop      = 0x2B,  // dec CX, jump if CX≠0
    F_Switch    = 0x2C,  // table jump (reg, table_addr, N)
    F_Trap      = 0x2D,  // exception/trap (8b code)
    F_Halt      = 0x2E,  // stop VM execution
    F_Yield     = 0x2F,  // yield current coroutine (cooperative)

    // ── It_ Information (0x3_) ── État informationnel + bitwise arithmetic ────
    It_DefFlag  = 0x30,  // define named flag
    It_DefState = 0x31,  // define named state (FSM)
    It_DefEvent = 0x32,  // define event type
    It_DefIrq   = 0x33,  // define interrupt
    // 0x34-0x37 repurposed as bitwise arithmetic (fits D_ semantics of "modifying")
    D_And       = 0x34,  // reg = reg & reg  (bitwise AND)
    D_Or        = 0x35,  // reg = reg | reg  (bitwise OR)
    D_Xor       = 0x36,  // reg = reg ^ reg  (bitwise XOR)
    D_Not       = 0x37,  // reg = ~reg       (bitwise NOT)
    It_GetFlag  = 0x38,  // read flag → reg  (was It_SetFlag — shifted up)
    It_ClrFlag  = 0x39,  // clear flag
    It_TogFlag  = 0x3A,  // toggle flag
    It_SetState = 0x3B,  // transition to new state
    It_Emit     = 0x3C,  // emit event
    It_Subscribe= 0x3D,  // subscribe to event
    // 0x3E-0x3F: shift operations
    D_Shl       = 0x3E,  // reg = reg << imm (shift left,  imm in flags[4:0])
    D_Shr       = 0x3F,  // reg = reg >> imm (shift right, imm in flags[4:0])

    // ── D_ Dynamics (0x4_) ── All modifications ───────────────────────────────
    D_Mov       = 0x40,  // reg = reg
    D_MovI      = 0x41,  // reg = imm32
    D_MovI64    = 0x42,  // reg = imm64
    D_Xchg      = 0x43,  // swap reg, reg
    D_Load8     = 0x44,  // reg = mem8[reg+offset]
    D_Load16    = 0x45,  // reg = mem16[reg+offset]
    D_Load32    = 0x46,  // reg = mem32[reg+offset]
    D_Load64    = 0x47,  // reg = mem64[reg+offset]
    D_Store8    = 0x48,  // mem8[reg+offset] = reg
    D_Store16   = 0x49,  // mem16[reg+offset] = reg
    D_Store32   = 0x4A,  // mem32[reg+offset] = reg
    D_Store64   = 0x4B,  // mem64[reg+offset] = reg
    D_Memcpy    = 0x4C,  // memcpy(dst, src, n)
    D_Memset    = 0x4D,  // memset(dst, val, n)
    D_Add       = 0x4E,  // reg = reg + reg
    D_Sub       = 0x4F,  // reg = reg - reg

    // ── R_ Representability (0x5_) ── Type conversions ───────────────────────
    R_I2F       = 0x50,  // int32 → float32
    R_F2I       = 0x51,  // float32 → int32 (truncated)
    R_I2F64     = 0x52,  // int64 → float64
    R_F2I64     = 0x53,  // float64 → int64
    R_F32_64    = 0x54,  // float32 → float64
    R_F64_32    = 0x55,  // float64 → float32
    R_Sign8     = 0x56,  // sign-extend byte → int32
    R_Sign16    = 0x57,  // sign-extend word → int32
    R_Zero8     = 0x58,  // zero-extend byte → int32
    R_Zero16    = 0x59,  // zero-extend word → int32
    R_Trunc     = 0x5A,  // truncate float → int (toward zero)
    R_Round     = 0x5B,  // round float → int
    R_Fix2F     = 0x5C,  // fixed 16.16 → float32
    R_F2Fix     = 0x5D,  // float32 → fixed 16.16
    R_FixMul    = 0x5E,  // D_FIXMUL: fixed 16.16 multiply (a*b)>>16  ← Wolf3D raycaster
    R_FixDiv    = 0x5F,  // D_FIXDIV: fixed 16.16 divide  (a<<16)/b

    // ── E_ Evolvability (0x6_) ── Self-transformation + adaptive GC ──────────
    E_LoadMod   = 0x60,  // load .tvl module at runtime
    E_Unload    = 0x61,  // unload module
    E_Bind      = 0x62,  // bind external symbol → local address
    E_Caps      = 0x63,  // query available VM capabilities
    E_Feature   = 0x64,  // enable runtime feature
    E_Fallback  = 0x65,  // define alternative behavior
    E_Patch     = 0x66,  // modify instruction in memory
    E_Hook      = 0x67,  // install hook on VM event
    E_Unhook    = 0x68,  // remove hook
    E_Version   = 0x69,  // detect VM version → adapt strategy
    E_Sandbox   = 0x6A,  // enter restricted mode
    E_Snapshot  = 0x6B,  // capture VM state → buffer (rollback)
    E_Restore   = 0x6C,  // restore VM state from snapshot
    E_GcCfg     = 0x6D,  // reconfigure GC strategy
    E_GcTune    = 0x6E,  // fine-tune GC parameters
    E_MemPool   = 0x6F,  // create dedicated memory pool

    // ── V_ Verifiability (0x7_) ── Comparisons + assertions ──────────────────
    V_Cmp       = 0x70,  // compare reg, reg → flags
    V_CmpI      = 0x71,  // compare reg, imm32 → flags
    V_Test      = 0x72,  // AND → flags (without storing)
    V_Eq        = 0x73,  // reg = (reg == reg) ? 1 : 0
    V_Neq       = 0x74,  // reg = (reg != reg) ? 1 : 0
    V_Lt        = 0x75,  // reg = (reg <  reg) ? 1 : 0
    V_Lte       = 0x76,  // reg = (reg <= reg) ? 1 : 0
    V_Gt        = 0x77,  // reg = (reg >  reg) ? 1 : 0
    V_Gte       = 0x78,  // reg = (reg >= reg) ? 1 : 0
    V_Assert    = 0x79,  // assert reg≠0 else trap
    V_Check     = 0x7A,  // check memory bounds
    V_TypeEq    = 0x7B,  // verify type tag == expected
    V_Range     = 0x7C,  // reg in [min, max] ? 1 : 0
    V_Null      = 0x7D,  // reg == NULL ? 1 : 0
    V_Overflow  = 0x7E,  // detect overflow from last op
    V_Parity    = 0x7F,  // parity of reg → flag

    // ── O_ Observability (0x8_) ── Debug + introspection ─────────────────────
    O_DumpReg   = 0x80,  // display all registers
    O_DumpStk   = 0x81,  // display N stack entries
    O_DumpMem   = 0x82,  // dump memory [addr, n]
    O_TraceOn   = 0x83,  // enable instruction trace
    O_TraceOff  = 0x84,  // disable instruction trace
    O_Break     = 0x85,  // breakpoint (DAP — VS Code)
    O_Watch     = 0x86,  // watchpoint on memory address
    O_Log       = 0x87,  // log char (reg lo byte) to stdout
    O_LogS      = 0x88,  // log null-terminated string (ptr in reg) to stdout
    O_PerfRd    = 0x89,  // read perf counter → reg
    O_StackTr   = 0x8A,  // symbolic stack trace
    O_CovMark   = 0x8B,  // mark code coverage point
    O_InspHeap  = 0x8C,  // inspect heap state
    O_TimeRd    = 0x8D,  // read VM timestamp (cycles)
    O_Annotate  = 0x8E,  // TSCG semantic annotation (.tscg)
    O_NopD      = 0x8F,  // debug NOP (→ O_Break in debug mode)

    // ── Im_ Interoperability (0x9_) ── FFI/SYSCALL/SDL2 ──────────────────────
    Im_Syscall  = 0x90,  // host system call (16b id)
    Im_FfiCall  = 0x91,  // native C call (ptr, sig_id)
    Im_FbBlit   = 0x92,  // blit framebuffer → host screen  ← Wolf3D
    Im_FbClear  = 0x93,  // clear host framebuffer
    Im_InputRd  = 0x94,  // read host keyboard/mouse state
    Im_Audio    = 0x95,  // send audio buffer to host
    Im_FileRd   = 0x96,  // read file (fd, buf, n)
    Im_FileWr   = 0x97,  // write file
    Im_FileOp   = 0x98,  // open/close/seek file
    Im_RegisterCb=0x99,  // register VM←C callback          ← SDL2 events
    Im_KeyQuery = 0x9A,  // query single key state: Im_KEY_QUERY Rdst, scancode_imm → Rdst=0|1
    Im_CbInvoke = 0x9B,  // invoke callback from VM
    Im_MemMap   = 0x9C,  // map host memory → VM space
    Im_Shared   = 0x9D,  // shared memory between VMs
    Im_TimeHost = 0x9E,  // read host clock (ms)
    Im_Exit     = 0x9F,  // exit VM cleanly (8b code)

    // ── T_ Temporality (0xA_) ── Timing + synchronization ────────────────────
    T_Tick      = 0xA0,  // read VM internal tick counter
    T_Wait      = 0xA1,  // wait N ticks
    T_Sleep     = 0xA2,  // sleep N milliseconds (host)
    T_Yield     = 0xA3,  // yield CPU (cooperative)
    T_TimerSet  = 0xA4,  // arm timer (id, delay, callback_addr)
    T_TimerClr  = 0xA5,  // cancel timer
    T_FrameSyn  = 0xA6,  // synchronize to target frame rate  ← Wolf3D 35fps
    T_Delta     = 0xA7,  // compute delta since last T_Tick
    T_Timeout   = 0xA8,  // test if timer expired
    T_Pause     = 0xA9,  // suspend VM execution
    T_Resume    = 0xAA,  // resume VM execution
    T_Sched     = 0xAB,  // schedule task at instant T
    T_AtomicB   = 0xAC,  // begin atomic section
    T_AtomicE   = 0xAD,  // end atomic section
    T_Barrier   = 0xAE,  // multi-VM synchronization barrier
    T_Watchdog  = 0xAF,  // reset watchdog (avoid timeout)

    // ── _^_ Positive Pole (0xB_) ── Onset / Activation ───────────────────────
    Pos_NewObj  = 0xB0,  // create object (type_id, size) → ptr
    Pos_NewStr  = 0xB1,  // create string (len + data) → ptr
    Pos_NewArr  = 0xB2,  // create typed array [N × size] → ptr
    Pos_Clone   = 0xB3,  // deep copy object → new object
    Pos_Spawn   = 0xB4,  // create new coroutine/fiber
    Pos_OpenCh  = 0xB5,  // open inter-fiber communication channel
    Pos_PushFr  = 0xB6,  // push new activation frame
    Pos_NewCtx  = 0xB7,  // create new execution context
    Pos_Intern  = 0xB8,  // intern string into global pool
    Pos_Pin     = 0xB9,  // pin object (prevent GC)
    Pos_RefInc  = 0xBA,  // increment reference counter
    Pos_Lock    = 0xBB,  // acquire mutex
    Pos_OpenSc  = 0xBC,  // open RAII scope
    Pos_AllocP  = 0xBD,  // allocate in dedicated pool → ptr
    Pos_ArenaB  = 0xBE,  // begin memory arena (Z_Malloc style)
    Pos_Activate= 0xBF,  // activate dormant entity

    // ── _$_ Negative Pole (0xC_) ── Terminus / Dissolution ───────────────────
    Neg_DelObj  = 0xC0,  // destroy object (call destructor)
    Neg_DelStr  = 0xC1,  // free string
    Neg_FreeArr = 0xC2,  // free array
    Neg_Kill    = 0xC3,  // terminate coroutine/fiber
    Neg_CloseCh = 0xC4,  // close communication channel
    Neg_PopFr   = 0xC5,  // pop activation frame
    Neg_DelCtx  = 0xC6,  // destroy execution context
    Neg_Unpin   = 0xC7,  // unpin object (return to GC)
    Neg_RefDec  = 0xC8,  // decrement reference counter
    Neg_Unlock  = 0xC9,  // release mutex
    Neg_CloseSc = 0xCA,  // close RAII scope
    Neg_FreeP   = 0xCB,  // free in dedicated pool
    Neg_ArenaE  = 0xCC,  // end memory arena (bulk release)
    Neg_Deact   = 0xCD,  // deactivate entity (dormancy)
    Neg_Purge   = 0xCE,  // flush pool/cache
    Neg_Abort   = 0xCF,  // immediate abort without cleanup

    // ── K_ Knowledge (0xD_) ── Reflection / Runtime type info ────────────────
    K_Typeof    = 0xD0,  // type tag of value → reg
    K_Sizeof    = 0xD1,  // size in bytes of type → reg
    K_Alignof   = 0xD2,  // required alignment → reg
    K_Fields    = 0xD3,  // number of object fields → reg
    K_FieldGet  = 0xD4,  // read field by index
    K_FieldSet  = 0xD5,  // write field by index
    K_IsA       = 0xD6,  // inheritance/interface test → bool
    K_Cast      = 0xD7,  // checked cast (trap if invalid)
    K_SymLook   = 0xD8,  // resolve symbol name → address
    K_SymName   = 0xD9,  // address → symbol name (debug)
    K_AnnGet    = 0xDA,  // read TSCG annotation on symbol
    K_AnnSet    = 0xDB,  // write TSCG annotation on symbol
    K_Schema    = 0xDC,  // return type schema (JSON-LD ptr)
    K_Validate  = 0xDD,  // validate object vs schema
    K_Version   = 0xDE,  // type/module version
    K_Describe  = 0xDF,  // textual type description (debug)

    // ── Ss_ Symbol (0xE_) ── Signs / Identifiers ──────────────────────────────
    Ss_Intern   = 0xE0,  // intern identifier into pool
    Ss_Lookup   = 0xE1,  // identifier → associated It value
    Ss_Hash     = 0xE2,  // hash identifier → fast key
    Ss_CmpId    = 0xE3,  // compare two identifiers
    Ss_Mangle   = 0xE4,  // name mangling (namespaces)
    Ss_Demangle = 0xE5,  // mangled name → readable name
    Ss_NullT    = 0xE6,  // '\0'  string terminator
    Ss_StrDlm   = 0xE7,  // '"'   string delimiter
    Ss_NsSep    = 0xE8,  // ':'   namespace separator
    Ss_Escape   = 0xE9,  // '\\' escape character
    Ss_Pi       = 0xEA,  // π = 3.14159265358979...
    Ss_ECst     = 0xEB,  // e = 2.71828182845904...
    Ss_Sqrt2    = 0xEC,  // √2 = 1.41421356237309...
    Ss_Inf      = 0xED,  // +∞ IEEE 754
    Ss_Nan      = 0xEE,  // NaN IEEE 754
    Ss_AddrCode = 0xEF,  // address of .code section start

    // ── L_ Localizability (0xF_) ── Addressing / Pointers ────────────────────
    L_Lea       = 0xF0,  // load effective address (base+offset)
    L_Addr      = 0xF1,  // address of local variable → reg
    L_Offset    = 0xF2,  // compute field offset in struct
    L_Idx       = 0xF3,  // array element address (base,idx,stride)
    L_Deref     = 0xF4,  // dereference pointer → value
    L_DerefW    = 0xF5,  // dereference + write
    L_Null      = 0xF6,  // reg = NULL (null pointer)
    L_IsNull    = 0xF7,  // test nullity → bool
    L_BoundChk  = 0xF8,  // verify ptr in valid region
    L_Align     = 0xF9,  // align address to N bytes
    L_Page      = 0xFA,  // memory page of address
    L_Glob      = 0xFB,  // address of global variable (16b id)
    L_Tls       = 0xFC,  // address of thread-local variable
    L_Relocate  = 0xFD,  // apply relocation (linker support)
    L_FarCall   = 0xFE,  // call 64-bit address (> ±8MB)   NOTE: L_, NOT F_
    L_FarJmp    = 0xFF,  // jump 64-bit address (> ±8MB)
}

impl Opcode {
    /// Parse opcode from raw byte.
    pub fn from_byte(b: u8) -> Option<Self> {
        // SAFETY: all 256 u8 values are defined in the repr(u8) enum
        Some(unsafe { std::mem::transmute(b) })
    }

    /// Opcode category (high nibble).
    pub fn category(self) -> OpcodeCategory {
        OpcodeCategory::from_byte(self as u8).unwrap()
    }

    /// Mnemonic name for tsk-dis display.
    pub fn mnemonic(self) -> &'static str {
        match self {
            // A_
            Self::A_Push      => "A_PUSH",
            Self::A_Pop       => "A_POP",
            Self::A_PushI     => "A_PUSH_I",
            Self::A_Peek      => "A_PEEK",
            Self::A_Swap      => "A_SWAP",
            Self::A_Dup       => "A_DUP",
            Self::A_Depth     => "A_DEPTH",
            Self::A_StackF    => "A_STACK_F",
            Self::A_Enter     => "A_ENTER",
            Self::A_Leave     => "A_LEAVE",
            Self::A_Alloc     => "A_ALLOC",
            Self::A_AllocZ    => "A_ALLOC_Z",
            Self::A_Realloc   => "A_REALLOC",
            Self::A_Free      => "A_FREE",
            Self::A_HeapSz    => "A_HEAP_SZ",
            Self::A_GcRun     => "A_GC_RUN",
            // St_
            Self::St_Nop      => "St_NOP",
            Self::St_DefStruct=> "St_DEF_STRUCT",
            Self::St_DefArray => "St_DEF_ARRAY",
            Self::St_DefUnion => "St_DEF_UNION",
            Self::St_DefEnum  => "St_DEF_ENUM",
            Self::St_DefAlias => "St_DEF_ALIAS",
            Self::St_FieldOff => "St_FIELD_OFF",
            Self::St_ElemOff  => "St_ELEM_OFF",
            Self::St_Sizeof   => "St_SIZEOF",
            Self::St_Alignof  => "St_ALIGNOF",
            Self::St_Stride   => "St_STRIDE",
            Self::D_Mul       => "D_MUL",
            Self::D_Div       => "D_DIV",
            Self::D_Rem       => "D_REM",
            Self::St_Layout   => "St_LAYOUT",
            Self::St_CastLay  => "St_CAST_LAY",
            // F_
            Self::F_Jmp       => "F_JMP",
            Self::F_JmpR      => "F_JMP_R",
            Self::F_Call      => "F_CALL",
            Self::F_Ret       => "F_RET",
            Self::F_RetN      => "F_RET_N",
            Self::F_Jz        => "F_JZ",
            Self::F_Jnz       => "F_JNZ",
            Self::F_Jl        => "F_JL",
            Self::F_Jle       => "F_JLE",
            Self::F_Jg        => "F_JG",
            Self::F_Jge       => "F_JGE",
            Self::F_Loop      => "F_LOOP",
            Self::F_Switch    => "F_SWITCH",
            Self::F_Trap      => "F_TRAP",
            Self::F_Halt      => "F_HALT",
            Self::F_Yield     => "F_YIELD",
            // It_
            Self::It_DefFlag  => "It_DEF_FLAG",
            Self::It_DefState => "It_DEF_STATE",
            Self::It_DefEvent => "It_DEF_EVENT",
            Self::It_DefIrq   => "It_DEF_IRQ",
            Self::D_And       => "D_AND",
            Self::D_Or        => "D_OR",
            Self::D_Xor       => "D_XOR",
            Self::D_Not       => "D_NOT",
            Self::It_GetFlag  => "It_GET_FLAG",
            Self::It_ClrFlag  => "It_CLR_FLAG",
            Self::It_TogFlag  => "It_TOG_FLAG",
            Self::It_SetState => "It_SET_STATE",
            Self::It_Emit     => "It_EMIT",
            Self::It_Subscribe=> "It_SUBSCRIBE",
            Self::D_Shl       => "D_SHL",
            Self::D_Shr       => "D_SHR",
            // D_
            Self::D_Mov       => "D_MOV",
            Self::D_MovI      => "D_MOV_I",
            Self::D_MovI64    => "D_MOV_I64",
            Self::D_Xchg      => "D_XCHG",
            Self::D_Load8     => "D_LOAD8",
            Self::D_Load16    => "D_LOAD16",
            Self::D_Load32    => "D_LOAD32",
            Self::D_Load64    => "D_LOAD64",
            Self::D_Store8    => "D_STORE8",
            Self::D_Store16   => "D_STORE16",
            Self::D_Store32   => "D_STORE32",
            Self::D_Store64   => "D_STORE64",
            Self::D_Memcpy    => "D_MEMCPY",
            Self::D_Memset    => "D_MEMSET",
            Self::D_Add       => "D_ADD",
            Self::D_Sub       => "D_SUB",
            // R_
            Self::R_I2F       => "R_I2F",
            Self::R_F2I       => "R_F2I",
            Self::R_I2F64     => "R_I2F64",
            Self::R_F2I64     => "R_F2I64",
            Self::R_F32_64    => "R_F32_64",
            Self::R_F64_32    => "R_F64_32",
            Self::R_Sign8     => "R_SIGN8",
            Self::R_Sign16    => "R_SIGN16",
            Self::R_Zero8     => "R_ZERO8",
            Self::R_Zero16    => "R_ZERO16",
            Self::R_Trunc     => "R_TRUNC",
            Self::R_Round     => "R_ROUND",
            Self::R_Fix2F     => "R_FIX2F",
            Self::R_F2Fix     => "R_F2FIX",
            Self::R_FixMul    => "R_FIXMUL",
            Self::R_FixDiv    => "R_FIXDIV",
            // E_
            Self::E_LoadMod   => "E_LOAD_MOD",
            Self::E_Unload    => "E_UNLOAD",
            Self::E_Bind      => "E_BIND",
            Self::E_Caps      => "E_CAPS",
            Self::E_Feature   => "E_FEATURE",
            Self::E_Fallback  => "E_FALLBACK",
            Self::E_Patch     => "E_PATCH",
            Self::E_Hook      => "E_HOOK",
            Self::E_Unhook    => "E_UNHOOK",
            Self::E_Version   => "E_VERSION",
            Self::E_Sandbox   => "E_SANDBOX",
            Self::E_Snapshot  => "E_SNAPSHOT",
            Self::E_Restore   => "E_RESTORE",
            Self::E_GcCfg     => "E_GC_CFG",
            Self::E_GcTune    => "E_GC_TUNE",
            Self::E_MemPool   => "E_MEM_POOL",
            // V_
            Self::V_Cmp       => "V_CMP",
            Self::V_CmpI      => "V_CMP_I",
            Self::V_Test      => "V_TEST",
            Self::V_Eq        => "V_EQ",
            Self::V_Neq       => "V_NEQ",
            Self::V_Lt        => "V_LT",
            Self::V_Lte       => "V_LTE",
            Self::V_Gt        => "V_GT",
            Self::V_Gte       => "V_GTE",
            Self::V_Assert    => "V_ASSERT",
            Self::V_Check     => "V_CHECK",
            Self::V_TypeEq    => "V_TYPE_EQ",
            Self::V_Range     => "V_RANGE",
            Self::V_Null      => "V_NULL",
            Self::V_Overflow  => "V_OVERFLOW",
            Self::V_Parity    => "V_PARITY",
            // O_
            Self::O_DumpReg   => "O_DUMP_REG",
            Self::O_DumpStk   => "O_DUMP_STK",
            Self::O_DumpMem   => "O_DUMP_MEM",
            Self::O_TraceOn   => "O_TRACE_ON",
            Self::O_TraceOff  => "O_TRACE_OFF",
            Self::O_Break     => "O_BREAK",
            Self::O_Watch     => "O_WATCH",
            Self::O_Log       => "O_LOG",
            Self::O_LogS      => "O_LOG_S",
            Self::O_PerfRd    => "O_PERF_RD",
            Self::O_StackTr   => "O_STACK_TR",
            Self::O_CovMark   => "O_COV_MARK",
            Self::O_InspHeap  => "O_INSP_HEAP",
            Self::O_TimeRd    => "O_TIME_RD",
            Self::O_Annotate  => "O_ANNOTATE",
            Self::O_NopD      => "O_NOP_D",
            // Im_
            Self::Im_Syscall  => "Im_SYSCALL",
            Self::Im_FfiCall  => "Im_FFI_CALL",
            Self::Im_FbBlit   => "Im_FB_BLIT",
            Self::Im_FbClear  => "Im_FB_CLEAR",
            Self::Im_InputRd  => "Im_INPUT_RD",
            Self::Im_Audio    => "Im_AUDIO",
            Self::Im_FileRd   => "Im_FILE_RD",
            Self::Im_FileWr   => "Im_FILE_WR",
            Self::Im_FileOp   => "Im_FILE_OP",
            Self::Im_RegisterCb=>"Im_REGISTER_CB",
            Self::Im_KeyQuery => "Im_KEY_QUERY",
            Self::Im_CbInvoke => "Im_CALL_R",  // doubles as indirect call via register
            Self::Im_MemMap   => "Im_MEM_MAP",
            Self::Im_Shared   => "Im_SHARED",
            Self::Im_TimeHost => "Im_TIME_HOST",
            Self::Im_Exit     => "Im_EXIT",
            // T_
            Self::T_Tick      => "T_TICK",
            Self::T_Wait      => "T_WAIT",
            Self::T_Sleep     => "T_SLEEP",
            Self::T_Yield     => "T_YIELD",
            Self::T_TimerSet  => "T_TIMER_SET",
            Self::T_TimerClr  => "T_TIMER_CLR",
            Self::T_FrameSyn  => "T_FRAME_SYN",
            Self::T_Delta     => "T_DELTA",
            Self::T_Timeout   => "T_TIMEOUT",
            Self::T_Pause     => "T_PAUSE",
            Self::T_Resume    => "T_RESUME",
            Self::T_Sched     => "T_SCHED",
            Self::T_AtomicB   => "T_ATOMIC_B",
            Self::T_AtomicE   => "T_ATOMIC_E",
            Self::T_Barrier   => "T_BARRIER",
            Self::T_Watchdog  => "T_WATCHDOG",
            // _^_
            Self::Pos_NewObj  => "_^_NEW_OBJ",
            Self::Pos_NewStr  => "_^_NEW_STR",
            Self::Pos_NewArr  => "_^_NEW_ARR",
            Self::Pos_Clone   => "_^_CLONE",
            Self::Pos_Spawn   => "_^_SPAWN",
            Self::Pos_OpenCh  => "_^_OPEN_CH",
            Self::Pos_PushFr  => "_^_PUSH_FR",
            Self::Pos_NewCtx  => "_^_NEW_CTX",
            Self::Pos_Intern  => "_^_INTERN",
            Self::Pos_Pin     => "_^_PIN",
            Self::Pos_RefInc  => "_^_REF_INC",
            Self::Pos_Lock    => "_^_LOCK",
            Self::Pos_OpenSc  => "_^_OPEN_SC",
            Self::Pos_AllocP  => "_^_ALLOC_P",
            Self::Pos_ArenaB  => "_^_ARENA_B",
            Self::Pos_Activate=> "_^_ACTIVATE",
            // _$_
            Self::Neg_DelObj  => "_$_DEL_OBJ",
            Self::Neg_DelStr  => "_$_DEL_STR",
            Self::Neg_FreeArr => "_$_FREE_ARR",
            Self::Neg_Kill    => "_$_KILL",
            Self::Neg_CloseCh => "_$_CLOSE_CH",
            Self::Neg_PopFr   => "_$_POP_FR",
            Self::Neg_DelCtx  => "_$_DEL_CTX",
            Self::Neg_Unpin   => "_$_UNPIN",
            Self::Neg_RefDec  => "_$_REF_DEC",
            Self::Neg_Unlock  => "_$_UNLOCK",
            Self::Neg_CloseSc => "_$_CLOSE_SC",
            Self::Neg_FreeP   => "_$_FREE_P",
            Self::Neg_ArenaE  => "_$_ARENA_E",
            Self::Neg_Deact   => "_$_DEACT",
            Self::Neg_Purge   => "_$_PURGE",
            Self::Neg_Abort   => "_$_ABORT",
            // K_
            Self::K_Typeof    => "K_TYPEOF",
            Self::K_Sizeof    => "K_SIZEOF",
            Self::K_Alignof   => "K_ALIGNOF",
            Self::K_Fields    => "K_FIELDS",
            Self::K_FieldGet  => "K_FIELD_GET",
            Self::K_FieldSet  => "K_FIELD_SET",
            Self::K_IsA       => "K_IS_A",
            Self::K_Cast      => "K_CAST",
            Self::K_SymLook   => "K_SYM_LOOK",
            Self::K_SymName   => "K_SYM_NAME",
            Self::K_AnnGet    => "K_ANN_GET",
            Self::K_AnnSet    => "K_ANN_SET",
            Self::K_Schema    => "K_SCHEMA",
            Self::K_Validate  => "K_VALIDATE",
            Self::K_Version   => "K_VERSION",
            Self::K_Describe  => "K_DESCRIBE",
            // Ss_
            Self::Ss_Intern   => "Ss_INTERN",
            Self::Ss_Lookup   => "Ss_LOOKUP",
            Self::Ss_Hash     => "Ss_HASH",
            Self::Ss_CmpId    => "Ss_CMP_ID",
            Self::Ss_Mangle   => "Ss_MANGLE",
            Self::Ss_Demangle => "Ss_DEMANGLE",
            Self::Ss_NullT    => "Ss_NULL_T",
            Self::Ss_StrDlm   => "Ss_STR_DLM",
            Self::Ss_NsSep    => "Ss_NS_SEP",
            Self::Ss_Escape   => "Ss_ESCAPE",
            Self::Ss_Pi       => "Ss_PI",
            Self::Ss_ECst     => "Ss_E_CST",
            Self::Ss_Sqrt2    => "Ss_SQRT2",
            Self::Ss_Inf      => "Ss_INF",
            Self::Ss_Nan      => "Ss_NAN",
            Self::Ss_AddrCode => "Ss_ADDR_CODE",
            // L_
            Self::L_Lea       => "L_LEA",
            Self::L_Addr      => "L_ADDR",
            Self::L_Offset    => "L_OFFSET",
            Self::L_Idx       => "L_IDX",
            Self::L_Deref     => "L_DEREF",
            Self::L_DerefW    => "L_DEREF_W",
            Self::L_Null      => "L_NULL",
            Self::L_IsNull    => "L_IS_NULL",
            Self::L_BoundChk  => "L_BOUND_CHK",
            Self::L_Align     => "L_ALIGN",
            Self::L_Page      => "L_PAGE",
            Self::L_Glob      => "L_GLOB",
            Self::L_Tls       => "L_TLS",
            Self::L_Relocate  => "L_RELOCATE",
            Self::L_FarCall   => "L_FAR_CALL",
            Self::L_FarJmp    => "L_FAR_JMP",
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Base16 Triskele display helpers (for tsk-dis)
// ─────────────────────────────────────────────────────────────────────────────

static PRIMITIVE_NAMES: [&str; 16] = [
    "A", "St", "F", "It", "D", "R", "E", "V",
    "O", "Im", "T", "_^", "_$", "K", "Ss", "L",
];

/// Format a u64 as Base16 Triskele sequence.
/// e.g. 0x1A3F → "St·T·It·L"
pub fn format_base16(value: u64, nibbles: usize) -> String {
    (0..nibbles)
        .rev()
        .map(|i| PRIMITIVE_NAMES[((value >> (i * 4)) & 0xF) as usize])
        .collect::<Vec<_>>()
        .join("·")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_opcode_roundtrip() {
        // All 256 byte values must parse successfully
        for b in 0u8..=255 {
            let op = Opcode::from_byte(b).expect("all bytes must be valid opcodes");
            assert_eq!(op as u8, b, "opcode byte roundtrip failed for 0x{:02X}", b);
        }
    }

    #[test]
    fn test_category_from_byte() {
        assert_eq!(OpcodeCategory::from_byte(0x00), Some(OpcodeCategory::A));
        assert_eq!(OpcodeCategory::from_byte(0x41), Some(OpcodeCategory::D));
        assert_eq!(OpcodeCategory::from_byte(0xFE), Some(OpcodeCategory::L));
    }

    #[test]
    fn test_wolf3d_critical_opcodes() {
        assert_eq!(Opcode::Im_FbBlit   as u8, 0x92);
        assert_eq!(Opcode::T_FrameSyn  as u8, 0xA6);
        assert_eq!(Opcode::Im_RegisterCb as u8, 0x99);
        assert_eq!(Opcode::Pos_ArenaB  as u8, 0xBE);
        assert_eq!(Opcode::Neg_ArenaE  as u8, 0xCC);
        assert_eq!(Opcode::L_FarCall   as u8, 0xFE);
    }

    #[test]
    fn test_notation_convention() {
        // St_ and It_ must NOT be S_ or I_
        assert!(Opcode::St_Nop.mnemonic().starts_with("St_"));
        assert!(Opcode::It_GetFlag.mnemonic().starts_with("It_"));
        assert!(Opcode::Ss_Pi.mnemonic().starts_with("Ss_"));
        assert!(Opcode::Im_FbBlit.mnemonic().starts_with("Im_"));
        // L_FAR_CALL is L_, NOT F_
        assert!(Opcode::L_FarCall.mnemonic().starts_with("L_"));
    }

    #[test]
    fn test_pole_symmetry() {
        // 14 _^_/_$_ pairs — verified against ISA Reference v0.2.0
        // Symmetry: each Pos opcode has exactly one Neg counterpart (in order).
        // Both categories cover bytes 0xB0–0xBF (_^_) and 0xC0–0xCF (_$_).
        let pos_opcodes: &[Opcode] = &[
            Opcode::Pos_NewObj, Opcode::Pos_NewStr, Opcode::Pos_NewArr,
            Opcode::Pos_Spawn,  Opcode::Pos_OpenCh, Opcode::Pos_PushFr,
            Opcode::Pos_NewCtx, Opcode::Pos_Pin,    Opcode::Pos_RefInc,
            Opcode::Pos_Lock,   Opcode::Pos_OpenSc, Opcode::Pos_AllocP,
            Opcode::Pos_ArenaB, Opcode::Pos_Activate,
        ];
        let neg_opcodes: &[Opcode] = &[
            Opcode::Neg_DelObj,  Opcode::Neg_DelStr,  Opcode::Neg_FreeArr,
            Opcode::Neg_Kill,    Opcode::Neg_CloseCh, Opcode::Neg_PopFr,
            Opcode::Neg_DelCtx,  Opcode::Neg_Unpin,   Opcode::Neg_RefDec,
            Opcode::Neg_Unlock,  Opcode::Neg_CloseSc, Opcode::Neg_FreeP,
            Opcode::Neg_ArenaE,  Opcode::Neg_Deact,
        ];
        assert_eq!(pos_opcodes.len(), 14, "must have 14 _^_ opcodes");
        assert_eq!(neg_opcodes.len(), 14, "must have 14 _$_ opcodes");

        for (pos, neg) in pos_opcodes.iter().zip(neg_opcodes.iter()) {
            // All _^_ opcodes are in 0xB0..0xBF range
            assert!((*pos as u8) >= 0xB0 && (*pos as u8) <= 0xBF,
                "_^_ opcode out of range: {:?} = 0x{:02X}", pos, *pos as u8);
            // All _$_ opcodes are in 0xC0..0xCF range
            assert!((*neg as u8) >= 0xC0 && (*neg as u8) <= 0xCF,
                "_$_ opcode out of range: {:?} = 0x{:02X}", neg, *neg as u8);
        }

        // Critical pairs from spec — explicit verification
        assert_eq!(Opcode::Pos_ArenaB as u8, 0xBE);  // _^_ARENA_B
        assert_eq!(Opcode::Neg_ArenaE as u8, 0xCC);  // _$_ARENA_E
    }

    #[test]
    fn test_base16_format() {
        assert_eq!(format_base16(0x0000, 4), "A·A·A·A");
        assert_eq!(format_base16(0x12FF, 4), "St·F·L·L");
    }
}
