/* doom_fixed_test.c — Test harness for FixedMul / FixedDiv
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Exit code = bitmask of passing tests (127 = all 7 passed).
 *
 * IMPORTANT — imm19 constraint:
 *   TriskeleVM Type I format: 19-bit signed immediate → [-262144, 262143].
 *   All literal constants (operands AND comparisons) must fit imm19 to avoid
 *   D_SHL which has a known flag-read bug (v0.3.4).
 *   Fixed-point 16.16: safe literal range is [-4.0, ~3.99] = [-262144, 262143].
 *   INT_MAX / INT_MIN are out of range → overflow tests use sign checks instead.
 *
 * Test matrix:
 *   Bit 0  (  1): FixedMul( 1.0,  2.0) ==  2.0
 *   Bit 1  (  2): FixedMul(-1.0,  3.0) == -3.0
 *   Bit 2  (  4): FixedMul( 0,    1.0) ==  0
 *   Bit 3  (  8): FixedDiv( 2.0,  1.0) ==  2.0
 *   Bit 4  ( 16): FixedDiv(-2.0,  1.0) == -2.0
 *   Bit 5  ( 32): FixedDiv overflow, same sign    → result > 0  (== INT_MAX)
 *   Bit 6  ( 64): FixedDiv overflow, opp. sign    → result < 0  (== INT_MIN)
 */

#include "doom_fixed.h"

int main(void)
{
    int result = 0;

    /* ── FixedMul tests ─────────────────────────────────────── */

    /* Test 1 (bit 0): 1.0 * 2.0 == 2.0
     * 65536, 131072, 131072 — all fit imm19 */
    {
        fixed_t a = 65536;   /* 1.0 */
        fixed_t b = 131072;  /* 2.0 */
        fixed_t r = FixedMul(a, b);
        if (r == 131072)
            result |= 1;
    }

    /* Test 2 (bit 1): -1.0 * 3.0 == -3.0
     * -65536, 196608, -196608 — all fit imm19 */
    {
        fixed_t a = -65536;  /* -1.0 */
        fixed_t b = 196608;  /*  3.0 */
        fixed_t r = FixedMul(a, b);
        if (r == -196608)    /* -3.0 */
            result |= 2;
    }

    /* Test 3 (bit 2): 0 * 1.0 == 0
     * 0, 65536, 0 — all fit imm19 */
    {
        fixed_t a = 0;
        fixed_t b = 65536;   /* 1.0 */
        fixed_t r = FixedMul(a, b);
        if (r == 0)
            result |= 4;
    }

    /* ── FixedDiv tests ─────────────────────────────────────── */

    /* Test 4 (bit 3): 2.0 / 1.0 == 2.0
     * 131072, 65536, 131072 — all fit imm19 */
    {
        fixed_t a = 131072;  /* 2.0 */
        fixed_t b = 65536;   /* 1.0 */
        fixed_t r = FixedDiv(a, b);
        if (r == 131072)
            result |= 8;
    }

    /* Test 5 (bit 4): -2.0 / 1.0 == -2.0
     * -131072, 65536, -131072 — all fit imm19 */
    {
        fixed_t a = -131072; /* -2.0 */
        fixed_t b =  65536;  /*  1.0 */
        fixed_t r = FixedDiv(a, b);
        if (r == -131072)
            result |= 16;
    }

    /* Test 6 (bit 5): overflow, same sign → INT_MAX (positive)
     * a=196608 (3.0), b=1 → FIXED_ABS(196608)>>14 = 11 >= 1 → overflow
     * a^b = 196609 > 0 → INT_MAX
     * Test: result > 0  (avoids loading INT_MAX literal — out of imm19) */
    {
        fixed_t a = 196608;  /* 3.0 — triggers overflow guard */
        fixed_t b = 1;
        fixed_t r = FixedDiv(a, b);
        if (r > 0)
            result |= 32;
    }

    /* Test 7 (bit 6): overflow, opposite sign → INT_MIN (negative)
     * a=196608 (3.0), b=-1 → overflow
     * a^b < 0 → INT_MIN
     * Test: result < 0  (avoids loading INT_MIN literal — out of imm19) */
    {
        fixed_t a =  196608; /* 3.0 — triggers overflow guard */
        fixed_t b = -1;
        fixed_t r = FixedDiv(a, b);
        if (r < 0)
            result |= 64;
    }

    return result; /* 127 = all 7 tests passed */
}
