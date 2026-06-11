// triskele-common/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Shared types for the TriskeleToolchain.
// ISA is derived from the 16 monoidal primitives of TSCG M3 Structural Grammar.

pub mod isa;
pub mod instr;
pub mod registers;
pub mod tvm;
pub mod error;
pub mod fixed;
pub mod libc_symbols;

pub use isa::{Opcode, OpcodeCategory};
pub use instr::{
    encode_r, encode_i, encode_j,
    decode_opcode, decode_dst, decode_s1, decode_s2, decode_flags,
    decode_imm19, decode_offset24,
    fits_imm19, fits_offset24, split_const32,
    IMM19_MAX, IMM19_MIN, OFF24_MAX, OFF24_MIN,
};
pub use registers::{Flags, RegisterFile};
pub use tvm::{Section, SectionType, TvmFile};
pub use error::VmError;
pub use fixed::{fixed_div, fixed_mul, fixed_to_float, float_to_fixed, Fixed, FIXED_ONE, FIXED_PI};
