// triskele-common/src/fixed.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Fixed-point 16.16 arithmetic — D_FIXMUL critical path for Wolf3D raycaster.
// R_ opcodes (R_FIX2F, R_F2FIX) bridge between Fixed and float32.

/// Fixed-point 16.16 type.
pub type Fixed = i32;

pub const FIXED_ONE:  Fixed = 0x0001_0000;   // 1.0
pub const FIXED_PI:   Fixed = 0x0003_243F;   // π  (used by Ss_PI)
pub const FIXED_2PI:  Fixed = 0x0006_487E;   // 2π
pub const FIXED_HALF: Fixed = 0x0000_8000;   // 0.5

/// D_FIXMUL — multiply two Fixed 16.16 values.
/// Performance-critical for Wolf3D raycaster inner loop.
#[inline(always)]
pub fn fixed_mul(a: Fixed, b: Fixed) -> Fixed {
    ((a as i64 * b as i64) >> 16) as Fixed
}

/// D_FIXDIV — divide two Fixed 16.16 values.
#[inline(always)]
pub fn fixed_div(a: Fixed, b: Fixed) -> Fixed {
    (((a as i64) << 16) / b as i64) as Fixed
}

/// D_MULDIV — multiply then divide without intermediate overflow.
#[inline(always)]
pub fn fixed_muldiv(a: Fixed, b: Fixed, c: Fixed) -> Fixed {
    ((a as i64 * b as i64) / c as i64) as Fixed
}

/// R_F2FIX — float32 to fixed 16.16.
#[inline(always)]
pub fn float_to_fixed(f: f32) -> Fixed {
    (f * 65536.0) as Fixed
}

/// R_FIX2F — fixed 16.16 to float32.
#[inline(always)]
pub fn fixed_to_float(x: Fixed) -> f32 {
    x as f32 / 65536.0
}

/// Integer part of fixed 16.16.
#[inline(always)]
pub fn fixed_int(x: Fixed) -> i32 {
    x >> 16
}

/// Fractional part of fixed 16.16 (0..FIXED_ONE).
#[inline(always)]
pub fn fixed_frac(x: Fixed) -> Fixed {
    x & 0x0000_FFFF
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fixed_mul_identity() {
        assert_eq!(fixed_mul(FIXED_ONE, FIXED_ONE), FIXED_ONE);
    }

    #[test]
    fn test_fixed_mul_half() {
        let result = fixed_mul(FIXED_ONE, FIXED_HALF);
        assert_eq!(result, FIXED_HALF);
    }

    #[test]
    fn test_float_roundtrip() {
        let f = 3.14_f32;
        let fx = float_to_fixed(f);
        let back = fixed_to_float(fx);
        assert!((back - f).abs() < 0.001, "roundtrip error: {} vs {}", f, back);
    }

    #[test]
    fn test_pi_constant() {
        let pi_f = fixed_to_float(FIXED_PI);
        assert!((pi_f - std::f32::consts::PI).abs() < 0.001);
    }
}
