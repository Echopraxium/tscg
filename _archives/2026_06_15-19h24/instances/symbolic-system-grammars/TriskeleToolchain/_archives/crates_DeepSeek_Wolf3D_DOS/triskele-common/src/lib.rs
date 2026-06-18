// triskele-common/src/lib.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Shared types for the TriskeleToolchain.
// ISA is derived from the 16 monoidal primitives of TSCG M3 Structural Grammar.

pub mod isa;
pub mod registers;
pub mod tvm;
pub mod error;
pub mod fixed;

pub use isa::{Opcode, OpcodeCategory};
pub use registers::{Flags, RegisterFile};
pub use tvm::{Section, SectionType, TvmFile};
pub use error::VmError;
pub use fixed::{fixed_div, fixed_mul, fixed_to_float, float_to_fixed, Fixed, FIXED_ONE, FIXED_PI};
