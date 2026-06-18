// triskele-vm/src/cpu/decode.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// 32-bit fixed-width instruction decoder.
// Four types — from TriskeleVM_Format_TVM.md §8:
//
//   Type R  [31-24: opcode] [23-19: dst] [18-14: src1] [13-09: src2] [8-0: flags]
//   Type I  [31-24: opcode] [23-19: dst] [18-0: imm19 signed]
//   Type J  [31-24: opcode] [23-0: offset24 signed — PC-relative ±8MB]
//   Type X  Type I with L_GLOB — next 8 bytes in pool = 64-bit constant

use triskele_common::isa::Opcode;
use triskele_common::error::VmError;
use triskele_common::{decode_imm19, decode_offset24};

/// Decoded instruction (typed union).
#[derive(Debug, Clone, Copy)]
pub enum Instruction {
    /// Register-to-register operation.
    R {
        opcode: Opcode,
        dst:    u8,
        src1:   u8,
        src2:   u8,
        flags:  u16,
    },
    /// Immediate operation (19-bit signed immediate).
    I {
        opcode: Opcode,
        dst:    u8,
        imm:    i32,   // sign-extended from 19 bits
    },
    /// Jump / branch (24-bit signed PC-relative offset in bytes).
    J {
        opcode: Opcode,
        offset: i32,   // sign-extended from 24 bits
    },
}

impl Instruction {
    pub fn opcode(&self) -> Opcode {
        match self {
            Self::R { opcode, .. } => *opcode,
            Self::I { opcode, .. } => *opcode,
            Self::J { opcode, .. } => *opcode,
        }
    }
}

/// Decode a 32-bit little-endian word into an Instruction.
///
/// Instruction type is determined by the opcode:
/// - Type J opcodes (F_JMP, F_JZ, F_JNZ, F_JL, F_JLE, F_JG, F_JGE, F_LOOP, F_CALL)
///   use the 24-bit offset layout.
/// - Type I opcodes (D_MOV_I, D_MOV_I64, A_PUSH_I, V_CMP_I, …) use the 19-bit imm layout.
/// - Everything else is Type R.
pub fn decode(word: u32) -> Result<Instruction, VmError> {
    let opcode_byte = (word >> 24) as u8;
    let opcode = Opcode::from_byte(opcode_byte)
        .ok_or(VmError::InvalidOpcode(opcode_byte))?;

    if is_jump_opcode(opcode) {
        let offset = decode_offset24(word);
        return Ok(Instruction::J { opcode, offset });
    }

    if is_immediate_opcode(opcode) {
        let dst = ((word >> 19) & 0x1F) as u8;
        let imm = decode_imm19(word);
        return Ok(Instruction::I { opcode, dst, imm });
    }

    // Default: Type R
    let dst  = ((word >> 19) & 0x1F) as u8;
    let src1 = ((word >> 14) & 0x1F) as u8;
    let src2 = ((word >>  9) & 0x1F) as u8;
    let flags = (word & 0x01FF) as u16;
    Ok(Instruction::R { opcode, dst, src1, src2, flags })
}

/// Deprecated — use triskele_common::decode_offset24 on the full word instead.
/// Kept for backward compatibility with tsk-asm / tsk-dis call sites.
#[inline]
pub fn sign_extend_24(v: i32) -> i32 {
    if v & 0x0080_0000 != 0 { v | !0x00FF_FFFFi32 } else { v }
}

/// Deprecated — use triskele_common::decode_imm19 on the full word instead.
/// Kept for backward compatibility with tsk-asm / tsk-dis call sites.
#[inline]
pub fn sign_extend_19(v: i32) -> i32 {
    if v & 0x0004_0000 != 0 { v | !0x0007_FFFFi32 } else { v }
}

/// True if this opcode uses the Type J (24-bit offset) format.
pub fn is_jump_opcode(op: Opcode) -> bool {
    matches!(op,
        Opcode::F_Jmp  | Opcode::F_Jz  | Opcode::F_Jnz |
        Opcode::F_Jl   | Opcode::F_Jle | Opcode::F_Jg  |
        Opcode::F_Jge  | Opcode::F_Loop| Opcode::F_Call |
        Opcode::F_JmpR
    )
}

/// True if this opcode uses the Type I (19-bit immediate) format.
pub fn is_immediate_opcode(op: Opcode) -> bool {
    matches!(op,
        Opcode::D_MovI    | Opcode::D_MovI64  |
        Opcode::A_PushI   |
        Opcode::V_CmpI    |
        Opcode::Im_Syscall |              // id encoded in imm19
        Opcode::L_Glob    | Opcode::F_Trap    |
        Opcode::F_RetN    | Opcode::F_Switch
    )
}

/// Encode a Type R instruction (for tsk-asm / tests).
/// Deprecated — use triskele_common::encode_r.
/// Kept for tsk-asm / tsk-dis call sites (Opcode wrapper).
pub fn encode_r(opcode: Opcode, dst: u8, src1: u8, src2: u8, flags: u16) -> u32 {
    triskele_common::encode_r(opcode as u8, dst, src1, src2, flags)
}
/// Deprecated — use triskele_common::encode_i.
pub fn encode_i(opcode: Opcode, dst: u8, imm: i32) -> u32 {
    triskele_common::encode_i(opcode as u8, dst, imm)
}
/// Deprecated — use triskele_common::encode_j.
pub fn encode_j(opcode: Opcode, offset: i32) -> u32 {
    triskele_common::encode_j(opcode as u8, offset)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_decode_type_r() {
        let word = encode_r(Opcode::D_Add, 1, 2, 3, 0);
        let instr = decode(word).unwrap();
        match instr {
            Instruction::R { opcode, dst, src1, src2, .. } => {
                assert_eq!(opcode, Opcode::D_Add);
                assert_eq!(dst, 1);
                assert_eq!(src1, 2);
                assert_eq!(src2, 3);
            }
            _ => panic!("expected Type R"),
        }
    }

    #[test]
    fn test_decode_type_i() {
        let word = encode_i(Opcode::D_MovI, 5, 72);  // D_MOV_I R5, 72 ('H')
        let instr = decode(word).unwrap();
        match instr {
            Instruction::I { opcode, dst, imm } => {
                assert_eq!(opcode, Opcode::D_MovI);
                assert_eq!(dst, 5);
                assert_eq!(imm, 72);
            }
            _ => panic!("expected Type I"),
        }
    }

    #[test]
    fn test_decode_type_j() {
        let word = encode_j(Opcode::F_Jmp, -8);
        let instr = decode(word).unwrap();
        match instr {
            Instruction::J { opcode, offset } => {
                assert_eq!(opcode, Opcode::F_Jmp);
                assert_eq!(offset, -8);
            }
            _ => panic!("expected Type J"),
        }
    }

    #[test]
    fn test_sign_extend_24_negative() {
        let v = sign_extend_24(0x00FF_FFFF);  // all bits set = -1
        assert_eq!(v, -1);
    }

    #[test]
    fn test_sign_extend_19_negative() {
        let v = sign_extend_19(0x0007_FFFF);  // all bits set = -1
        assert_eq!(v, -1);
    }

    // ── triskele_common::decode_* integration ────────────────────────────────

    #[test]
    fn test_decode_imm19_negative5() {
        // D_MOV_I R24, -5 — exact word from test_select trace
        let word: u32 = 0x41C7_FFFB;
        assert_eq!(decode_imm19(word), -5);
    }

    #[test]
    fn test_decode_offset24_forward() {
        // F_JNZ +8 — exact word from test_select trace
        let word: u32 = 0x2600_0008;
        assert_eq!(decode_offset24(word), 8);
    }

    #[test]
    fn test_decode_imm19_minus32() {
        // D_MOV_I R24, -32 — frame slot 0
        let word: u32 = 0x41C7_FFE0;
        assert_eq!(decode_imm19(word), -32);
    }
}
