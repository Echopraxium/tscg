// triskele-common/src/error.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0

#[derive(Debug, PartialEq, thiserror::Error)]
pub enum VmError {
    #[error("Invalid opcode: 0x{0:02X}")]
    InvalidOpcode(u8),

    #[error("Invalid register index: {0}")]
    InvalidRegister(usize),

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

    #[error("Relocation overflow at 0x{addr:08X}: {dist:.1}MB exceeds ±8MB (use L_FAR_CALL)")]
    RelocationOverflow { addr: u64, dist: f64 },

    #[error("F_TRAP: exception code {0}")]
    Trap(u8),

    #[error("V_ASSERT failed at PC=0x{0:016X}")]
    AssertFailed(u64),

    #[error("Invalid .tobj/.tvmx file: {0}")]
    InvalidTvxFile(String),

    #[error("Section not found: {0}")]
    SectionNotFound(String),

    #[error("Arena error: {0}")]
    ArenaError(String),

    #[error("I/O error: {0}")]
    IoError(String),

    #[error("VM halted with exit code {0}")]
    Halted(i32),

    #[error("Division by zero")]
    DivisionByZero,
}

impl From<std::io::Error> for VmError {
    fn from(e: std::io::Error) -> Self {
        VmError::IoError(e.to_string())
    }
}
