// triskele-common/src/instr.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.4
//
// Single source of truth for TriskeleVM 32-bit instruction encoding/decoding.
//
// Instruction formats (all 32-bit fixed-width):
//
//   Type R  [31-24: opcode(8)] [23-19: dst(5)] [18-14: s1(5)] [13-9: s2(5)] [8-0: flags(9)]
//   Type I  [31-24: opcode(8)] [23-19: dst(5)] [18-0: imm19(19, signed)]
//   Type J  [31-24: opcode(8)] [23-0: offset24(24, signed, byte offset)]
//
// Rules:
//   - imm19  range: -262144 .. 262143  (±256 KB)
//   - offset24 range: -8388608 .. 8388607  (±8 MB)
//   - All offsets are in BYTES, relative to the instruction address.
//   - tsk-cc and triskele-vm MUST use these functions — no inline bit-twiddling.

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

pub const IMM19_MAX:  i32 =  262143;   //  (1 << 18) - 1
pub const IMM19_MIN:  i32 = -262144;   // -(1 << 18)
pub const OFF24_MAX:  i32 =  8388607;  //  (1 << 23) - 1
pub const OFF24_MIN:  i32 = -8388608;  // -(1 << 23)

pub const MASK_IMM19:  u32 = 0x0007_FFFF;
pub const MASK_OFF24:  u32 = 0x00FF_FFFF;
pub const MASK_DST:    u32 = 0x00F8_0000;  // bits 23-19
pub const MASK_S1:     u32 = 0x0007_C000;  // bits 18-14
pub const MASK_S2:     u32 = 0x0000_3E00;  // bits 13-9
pub const MASK_FLAGS:  u32 = 0x0000_01FF;  // bits 8-0
pub const MASK_OPCODE: u32 = 0xFF00_0000;  // bits 31-24

// ─────────────────────────────────────────────────────────────────────────────
// Encoding
// ─────────────────────────────────────────────────────────────────────────────

/// Encode a Type R instruction.
/// `dst`, `s1`, `s2` are 5-bit register indices (0-31).
/// `flags` is a 9-bit auxiliary field (shift amount, condition code, etc.).
#[inline(always)]
pub fn encode_r(op: u8, dst: u8, s1: u8, s2: u8, flags: u16) -> u32 {
    ((op    as u32) << 24)
    | ((dst as u32) << 19)
    | ((s1  as u32) << 14)
    | ((s2  as u32) <<  9)
    | (flags as u32 & 0x1FF)
}

/// Encode a Type I instruction.
/// `imm` is sign-extended from 19 bits; values outside IMM19_MIN..IMM19_MAX
/// are silently truncated — callers must use `needs_multi_instr` to detect this.
#[inline(always)]
pub fn encode_i(op: u8, dst: u8, imm: i32) -> u32 {
    ((op    as u32) << 24)
    | ((dst as u32) << 19)
    | (imm  as u32 & MASK_IMM19)
}

/// Encode a Type J instruction.
/// `offset` is a signed byte offset relative to the instruction address.
/// Values outside OFF24_MIN..OFF24_MAX are silently truncated.
#[inline(always)]
pub fn encode_j(op: u8, offset: i32) -> u32 {
    ((op as u32) << 24) | (offset as u32 & MASK_OFF24)
}

// ─────────────────────────────────────────────────────────────────────────────
// Decoding
// ─────────────────────────────────────────────────────────────────────────────

/// Extract opcode byte (bits 31-24).
#[inline(always)]
pub fn decode_opcode(word: u32) -> u8 {
    (word >> 24) as u8
}

/// Extract dst field (bits 23-19) as register index.
#[inline(always)]
pub fn decode_dst(word: u32) -> usize {
    ((word >> 19) & 0x1F) as usize
}

/// Extract s1 field (bits 18-14) as register index.
#[inline(always)]
pub fn decode_s1(word: u32) -> usize {
    ((word >> 14) & 0x1F) as usize
}

/// Extract s2 field (bits 13-9) as register index.
#[inline(always)]
pub fn decode_s2(word: u32) -> usize {
    ((word >> 9) & 0x1F) as usize
}

/// Extract flags field (bits 8-0).
#[inline(always)]
pub fn decode_flags(word: u32) -> u16 {
    (word & 0x1FF) as u16
}

/// Extract and sign-extend imm19 (bits 18-0) → i32.
/// Bit 18 is the sign bit.
#[inline(always)]
pub fn decode_imm19(word: u32) -> i32 {
    let raw = (word & MASK_IMM19) as i32;
    // Sign-extend: if bit 18 is set, fill upper bits with 1s
    if raw & 0x0004_0000 != 0 {
        raw | !0x0007_FFFFi32   // = raw | 0xFFF8_0000
    } else {
        raw
    }
}

/// Extract and sign-extend offset24 (bits 23-0) → i32.
/// Bit 23 is the sign bit.
#[inline(always)]
pub fn decode_offset24(word: u32) -> i32 {
    let raw = (word & MASK_OFF24) as i32;
    // Sign-extend: if bit 23 is set, fill upper bits with 1s
    if raw & 0x0080_0000 != 0 {
        raw | !0x00FF_FFFFi32   // = raw | 0xFF00_0000
    } else {
        raw
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Range checks
// ─────────────────────────────────────────────────────────────────────────────

/// Returns true if `val` fits in a signed 19-bit immediate (Type I).
/// If false, a multi-instruction sequence is required (MovI hi; Shl 16; Or lo).
#[inline(always)]
pub fn fits_imm19(val: i64) -> bool {
    val >= IMM19_MIN as i64 && val <= IMM19_MAX as i64
}

/// Returns true if `offset` fits in a signed 24-bit branch offset (Type J).
/// If false, an indirect jump via register is required.
#[inline(always)]
pub fn fits_offset24(offset: i64) -> bool {
    offset >= OFF24_MIN as i64 && offset <= OFF24_MAX as i64
}

// ─────────────────────────────────────────────────────────────────────────────
// Multi-instruction constant loading (tsk-cc helper)
// ─────────────────────────────────────────────────────────────────────────────

/// Decompose a 32-bit constant into (hi16, lo16) for multi-instruction loading:
///   D_MovI  scratch, hi16
///   D_Shl   scratch, scratch, shift_reg   (shift_reg must hold 16)
///   D_Or    scratch, scratch, lo16        (only if lo16 != 0)
///
/// Returns (hi, lo) both as i32, sign-extended to fit imm19.
pub fn split_const32(val: i32) -> (i32, i32) {
    let hi = ((val >> 16) & 0xFFFF) as i32;
    let lo = (val & 0xFFFF) as i32;
    (hi, lo)
}

// ─────────────────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;

    // ── encode/decode roundtrip ──────────────────────────────────────────────

    #[test]
    fn roundtrip_r_basic() {
        // D_ADD R5, R3, R4  (opcode=0x4E, dst=5, s1=3, s2=4, flags=0)
        let w = encode_r(0x4E, 5, 3, 4, 0);
        assert_eq!(decode_opcode(w), 0x4E, "opcode");
        assert_eq!(decode_dst(w),    5,    "dst");
        assert_eq!(decode_s1(w),     3,    "s1");
        assert_eq!(decode_s2(w),     4,    "s2");
        assert_eq!(decode_flags(w),  0,    "flags");
    }

    #[test]
    fn roundtrip_r_all_regs() {
        // Max register indices: R31, R31, R31
        let w = encode_r(0x70, 31, 31, 31, 0x1FF);
        assert_eq!(decode_dst(w),   31,    "dst=R31");
        assert_eq!(decode_s1(w),    31,    "s1=R31");
        assert_eq!(decode_s2(w),    31,    "s2=R31");
        assert_eq!(decode_flags(w), 0x1FF, "flags=0x1FF");
    }

    #[test]
    fn roundtrip_r_fp_sp() {
        // D_ADD R24, FP(R28), R24  — used in alloca address computation
        let w = encode_r(0x4E, 24, 28, 24, 0);
        assert_eq!(decode_dst(w), 24, "dst=R24");
        assert_eq!(decode_s1(w),  28, "s1=FP=R28");
        assert_eq!(decode_s2(w),  24, "s2=R24");
    }

    #[test]
    fn roundtrip_i_zero() {
        let w = encode_i(0x41, 0, 0);
        assert_eq!(decode_imm19(w), 0, "imm=0");
        assert_eq!(decode_dst(w),   0, "dst=R0");
    }

    #[test]
    fn roundtrip_i_positive() {
        // D_MOV_I R0, 10
        let w = encode_i(0x41, 0, 10);
        assert_eq!(decode_imm19(w), 10);
    }

    #[test]
    fn roundtrip_i_negative_small() {
        // D_MOV_I R24, -5  — the failing case for clamp(-5,0,10)
        let w = encode_i(0x41, 24, -5);
        assert_eq!(decode_imm19(w), -5, "imm=-5 must survive encode/decode");
    }

    #[test]
    fn roundtrip_i_negative_fp_offset() {
        // D_MOV_I R24, -32  — frame slot 0 in clamp
        let w = encode_i(0x41, 24, -32);
        assert_eq!(decode_imm19(w), -32);
    }

    #[test]
    fn roundtrip_i_negative_fp_offset_24() {
        // D_MOV_I R24, -24  — frame slot 1
        let w = encode_i(0x41, 24, -24);
        assert_eq!(decode_imm19(w), -24);
    }

    #[test]
    fn roundtrip_i_negative_fp_offset_16() {
        // D_MOV_I R24, -16  — frame slot 2
        let w = encode_i(0x41, 24, -16);
        assert_eq!(decode_imm19(w), -16);
    }

    #[test]
    fn roundtrip_i_boundary_max() {
        let w = encode_i(0x41, 0, IMM19_MAX);
        assert_eq!(decode_imm19(w), IMM19_MAX);
    }

    #[test]
    fn roundtrip_i_boundary_min() {
        let w = encode_i(0x41, 0, IMM19_MIN);
        assert_eq!(decode_imm19(w), IMM19_MIN);
    }

    #[test]
    fn roundtrip_j_positive() {
        // F_JMP +8  — forward branch
        let w = encode_j(0x20, 8);
        assert_eq!(decode_offset24(w), 8);
    }

    #[test]
    fn roundtrip_j_negative() {
        // F_JMP -16  — backward branch (loop)
        let w = encode_j(0x20, -16);
        assert_eq!(decode_offset24(w), -16);
    }

    #[test]
    fn roundtrip_j_boundary_max() {
        let w = encode_j(0x20, OFF24_MAX);
        assert_eq!(decode_offset24(w), OFF24_MAX);
    }

    #[test]
    fn roundtrip_j_boundary_min() {
        let w = encode_j(0x20, OFF24_MIN);
        assert_eq!(decode_offset24(w), OFF24_MIN);
    }

    // ── fits_* range checks ──────────────────────────────────────────────────

    #[test]
    fn fits_imm19_boundaries() {
        assert!( fits_imm19(0));
        assert!( fits_imm19(-5));
        assert!( fits_imm19(IMM19_MAX as i64));
        assert!( fits_imm19(IMM19_MIN as i64));
        assert!(!fits_imm19(IMM19_MAX as i64 + 1));
        assert!(!fits_imm19(IMM19_MIN as i64 - 1));
        // Large constant that requires multi-instruction: 655360 = 10 << 16
        assert!(!fits_imm19(655360));
    }

    #[test]
    fn fits_offset24_boundaries() {
        assert!( fits_offset24(0));
        assert!( fits_offset24(-8));
        assert!( fits_offset24(OFF24_MAX as i64));
        assert!( fits_offset24(OFF24_MIN as i64));
        assert!(!fits_offset24(OFF24_MAX as i64 + 1));
        assert!(!fits_offset24(OFF24_MIN as i64 - 1));
    }

    // ── split_const32 ────────────────────────────────────────────────────────

    #[test]
    fn split_const32_large() {
        // 655360 = 0x000A_0000 = hi=10, lo=0
        let (hi, lo) = split_const32(655360);
        assert_eq!(hi, 10);
        assert_eq!(lo, 0);
        assert_eq!((hi << 16) | lo, 655360);
    }

    #[test]
    fn split_const32_with_lo() {
        // 0x000A_0005 → hi=10, lo=5
        let (hi, lo) = split_const32(0x000A_0005);
        assert_eq!(hi, 10);
        assert_eq!(lo, 5);
    }

    // ── cross-check with known trace words ───────────────────────────────────

    #[test]
    fn decode_trace_d_mov_i_minus5() {
        // From test_select trace: PC=0x1484  word=0x41C7FFFB  "D_MOV_I R24, -5"
        let w: u32 = 0x41C7FFFB;
        assert_eq!(decode_opcode(w), 0x41, "opcode=D_MovI");
        assert_eq!(decode_dst(w),    24,   "dst=R24");
        assert_eq!(decode_imm19(w),  -5,   "imm=-5");
    }

    #[test]
    fn decode_trace_d_mov_i_minus32() {
        // From trace: word=0x41C7FFE0  "D_MOV_I R24, -32"
        let w: u32 = 0x41C7FFE0;
        assert_eq!(decode_opcode(w), 0x41);
        assert_eq!(decode_dst(w),    24);
        assert_eq!(decode_imm19(w),  -32);
    }

    #[test]
    fn decode_trace_d_add_fp() {
        // From trace: word=0x4EC73000  "D_ADD R24, FP(R28), R24"
        let w: u32 = 0x4EC73000;
        assert_eq!(decode_opcode(w), 0x4E, "opcode=D_Add");
        assert_eq!(decode_dst(w),    24,   "dst=R24");
        assert_eq!(decode_s1(w),     28,   "s1=R28=FP");
        assert_eq!(decode_s2(w),     24,   "s2=R24");
    }

    #[test]
    fn decode_trace_d_store32() {
        // From trace: word=0x4AC08000  "D_STORE32 R24, R2"
        let w: u32 = 0x4AC08000;
        assert_eq!(decode_opcode(w), 0x4A, "opcode=D_Store32");
        assert_eq!(decode_dst(w),    24,   "addr_reg=R24");
        assert_eq!(decode_s1(w),     2,    "val_reg=R2");
    }

    #[test]
    fn decode_trace_d_load32() {
        // From trace: word=0x461E0000  "D_LOAD32 R3, [R24]"
        let w: u32 = 0x461E0000;
        assert_eq!(decode_opcode(w), 0x46, "opcode=D_Load32");
        assert_eq!(decode_dst(w),    3,    "dst=R3");
        assert_eq!(decode_s1(w),     24,   "addr=R24");
    }

    #[test]
    fn decode_trace_v_lt() {
        // From trace: word=0x7528C800  "V_LT R5, R3, R4"
        let w: u32 = 0x7528C800;
        assert_eq!(decode_opcode(w), 0x75, "opcode=V_Lt");
        assert_eq!(decode_dst(w),    5,    "dst=R5");
        assert_eq!(decode_s1(w),     3,    "s1=R3");
        assert_eq!(decode_s2(w),     4,    "s2=R4");
    }

    #[test]
    fn decode_trace_v_cmp_i() {
        // From trace: word=0x71280000  "V_CMP_I R5, 0"
        let w: u32 = 0x71280000;
        assert_eq!(decode_opcode(w), 0x71, "opcode=V_CmpI");
        assert_eq!(decode_dst(w),    5,    "dst=R5");
        assert_eq!(decode_imm19(w),  0,    "imm=0");
    }

    #[test]
    fn decode_trace_f_jnz() {
        // From trace: word=0x26000008  "F_JNZ +8"
        let w: u32 = 0x26000008;
        assert_eq!(decode_opcode(w),   0x26, "opcode=F_Jnz");
        assert_eq!(decode_offset24(w), 8,    "offset=+8");
    }
}
