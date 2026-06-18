// tsk-asm/src/encoder.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Instruction encoders — mirrors triskele-vm/src/cpu/decode.rs
// Kept local to tsk-asm to avoid adding a dependency on triskele-vm.

use triskele_common::isa::Opcode;

/// Encode a Type R instruction.
pub fn encode_r(opcode: Opcode, dst: u8, src1: u8, src2: u8, flags: u16) -> u32 {
    ((opcode as u32) << 24)
        | ((dst  as u32) << 19)
        | ((src1 as u32) << 14)
        | ((src2 as u32) <<  9)
        | (flags as u32 & 0x1FF)
}

/// Encode a Type I instruction (19-bit signed immediate).
pub fn encode_i(opcode: Opcode, dst: u8, imm: i32) -> u32 {
    ((opcode as u32) << 24)
        | ((dst as u32) << 19)
        | (imm as u32 & 0x0007_FFFF)
}

/// Encode a Type J instruction (24-bit signed PC-relative offset).
pub fn encode_j(opcode: Opcode, offset: i32) -> u32 {
    ((opcode as u32) << 24)
        | (offset as u32 & 0x00FF_FFFF)
}

/// True if this opcode uses the Type J (24-bit offset) layout.
pub fn is_jump_mnemonic(op: Opcode) -> bool {
    matches!(op,
        Opcode::F_Jmp  | Opcode::F_JmpR | Opcode::F_Call |
        Opcode::F_Jz   | Opcode::F_Jnz  | Opcode::F_Jl   |
        Opcode::F_Jle  | Opcode::F_Jg   | Opcode::F_Jge  |
        Opcode::F_Loop
    )
}

/// True if this opcode uses the Type I (19-bit immediate) layout.
pub fn is_immediate_mnemonic(op: Opcode) -> bool {
    matches!(op,
        Opcode::D_MovI    | Opcode::D_MovI64  |
        Opcode::A_PushI   | Opcode::V_CmpI    |
        Opcode::F_Trap    | Opcode::F_RetN
    )
}
