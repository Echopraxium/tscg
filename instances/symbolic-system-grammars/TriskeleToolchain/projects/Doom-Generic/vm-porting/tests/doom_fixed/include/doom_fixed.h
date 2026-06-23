/*
 * doom_fixed.h — Fixed-point 16.16 types and constants
 * Standalone wrapper (no DoomGeneric dependencies)
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Derived from DoomGeneric m_fixed.h
 * Copyright(C) 1993-1996 Id Software, Inc.
 * Copyright(C) 2005-2014 Simon Howard
 */

#ifndef __DOOM_FIXED__
#define __DOOM_FIXED__

/* Fixed-point 16.16 */
#define FRACBITS   16
#define FRACUNIT   (1 << FRACBITS)

typedef int fixed_t;

/* Portable INT_MIN / INT_MAX (C89 compliant) */
#ifndef INT_MAX
#define INT_MAX  2147483647
#endif
#ifndef INT_MIN
#define INT_MIN  (-2147483647 - 1)
#endif

/* Portable abs for int (avoids dependency on stdlib.h abs) */
#define FIXED_ABS(x)  ((x) < 0 ? -(x) : (x))

fixed_t FixedMul(fixed_t a, fixed_t b);
fixed_t FixedDiv(fixed_t a, fixed_t b);

#endif /* __DOOM_FIXED__ */
