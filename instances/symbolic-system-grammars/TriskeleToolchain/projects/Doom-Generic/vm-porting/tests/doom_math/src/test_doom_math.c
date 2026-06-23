/*
 * test_doom_math.c — v0.3.10 DoomGeneric math modules
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Tests real DoomGeneric code: m_fixed.c + m_random.c
 *
 * Exit bitmask (7 tests) — expected_exit = 0x7F = 127
 *
 *  bit 0  FixedMul: 1.0 * 2.0 = 2.0
 *  bit 1  FixedMul: 0.5 * 0.5 = 0.25
 *  bit 2  FixedDiv: 4.0 / 2.0 = 2.0
 *  bit 3  FixedDiv: overflow → INT_MAX
 *  bit 4  M_Random: deterministic sequence starts at rndtable[1]=8
 *  bit 5  M_ClearRandom: reset returns to rndtable[1]=8
 *  bit 6  P_Random: independent from M_Random
 */
#include <stdlib.h>
#include <limits.h>
#include "m_fixed.h"
#include "m_random.h"

int main(void)
{
    int result = 0;

    /* Test 1 (bit 0): FixedMul(1.0, 2.0) = 2.0
     * 1.0 = FRACUNIT = 65536, 2.0 = 131072
     * 65536 * 131072 >> 16 = 131072 */
    {
        fixed_t a = FRACUNIT;       /* 1.0 */
        fixed_t b = FRACUNIT * 2;   /* 2.0 */
        fixed_t r = FixedMul(a, b);
        if (r == FRACUNIT * 2)
            result |= 1;
    }

    /* Test 2 (bit 1): FixedMul(0.5, 0.5) = 0.25
     * 0.5 = 32768 → 32768*32768>>16 = 16384 = 0.25*FRACUNIT */
    {
        fixed_t half = FRACUNIT / 2;
        fixed_t r = FixedMul(half, half);
        if (r == FRACUNIT / 4)
            result |= 2;
    }

    /* Test 3 (bit 2): FixedDiv(4.0, 2.0) = 2.0 */
    {
        fixed_t r = FixedDiv(FRACUNIT * 4, FRACUNIT * 2);
        if (r == FRACUNIT * 2)
            result |= 4;
    }

    /* Test 4 (bit 3): FixedDiv overflow → INT_MAX
     * abs(a)>>14 >= abs(b) when a=INT_MAX, b=1 */
    {
        fixed_t r = FixedDiv(INT_MAX, 1);
        if (r == INT_MAX)
            result |= 8;
    }

    /* Test 5 (bit 4): M_Random — first call returns rndtable[1] = 8 */
    {
        M_ClearRandom();
        int r = M_Random();
        if (r == 8)
            result |= 16;
    }

    /* Test 6 (bit 5): M_ClearRandom resets sequence */
    {
        M_Random(); /* advance */
        M_Random();
        M_ClearRandom();
        int r = M_Random();
        if (r == 8) /* back to rndtable[1] */
            result |= 32;
    }

    /* Test 7 (bit 6): P_Random is independent from M_Random */
    {
        M_ClearRandom();
        int m1 = M_Random(); /* rndtable[1] = 8  */
        int p1 = P_Random(); /* rndtable[1] = 8  (own index) */
        int m2 = M_Random(); /* rndtable[2] = 109 */
        int p2 = P_Random(); /* rndtable[2] = 109 */
        if (m1 == 8 && p1 == 8 && m2 == 109 && p2 == 109)
            result |= 64;
    }

    return result;
}
