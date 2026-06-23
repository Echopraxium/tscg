/*
 * m_fixed.c — Fixed-point arithmetic implementation
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Derived from DoomGeneric m_fixed.c
 * Copyright(C) 1993-1996 Id Software, Inc.
 * Copyright(C) 2005-2014 Simon Howard
 *
 * Fixed-point 16.16 — identical logic to original Doom source,
 * made standalone (no doomtype.h / i_system.h dependencies).
 */

#include "doom_fixed.h"

/* Fixed-point multiply: (a * b) >> FRACBITS */
fixed_t FixedMul(fixed_t a, fixed_t b)
{
    return ((long long)a * (long long)b) >> FRACBITS;
}

/*
 * FixedDiv, C version.
 *
 * Overflow guard: if |a| >> 14 >= |b|, result would overflow
 * a 32-bit fixed_t — return INT_MIN or INT_MAX based on sign.
 */
fixed_t FixedDiv(fixed_t a, fixed_t b)
{
    if ((FIXED_ABS(a) >> 14) >= FIXED_ABS(b))
    {
        return (a ^ b) < 0 ? INT_MIN : INT_MAX;
    }
    else
    {
        long long result;
        result = ((long long)a << 16) / b;
        return (fixed_t)result;
    }
}
