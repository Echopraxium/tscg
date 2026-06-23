/*
 * z_zone_stubs.h — Stubs for DoomGeneric z_zone.c dependencies
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.1.0
 *
 * Replaces i_system.h / doomtype.h dependencies for standalone compilation
 * of the original DoomGeneric z_zone.c on TriskeleVM (C89 / clang -O0).
 *
 * Provides:
 *   byte typedef (unsigned char)
 *   boolean typedef (int, TRUE/FALSE)
 *   I_Error  — prints fmt string to stderr then loops forever (VM halts)
 *   I_ZoneBase — returns a static 2MB heap buffer
 *
 * NOTE: I_Error is intentionally NOT variadic (no va_list / vfprintf)
 * because tsk-cc does not yet support va_list LLVM IR patterns.
 * The format string is printed as-is — sufficient for Z_CheckHeap error msgs.
 */

#ifndef __Z_ZONE_STUBS__
#define __Z_ZONE_STUBS__

#include <stdio.h>

/* ── C89 basic types ────────────────────────────────────────────────────── */

typedef unsigned char byte;
typedef int           boolean;

#define TRUE  1
#define FALSE 0

/* ── Heap for I_ZoneBase ────────────────────────────────────────────────── */

/* 2 MB static zone — matches doom_alloc test expectations */
#define DOOM_ZONE_SIZE  (2 * 1024 * 1024)

static byte doom_zone_heap[DOOM_ZONE_SIZE];

/* ── I_ZoneBase ─────────────────────────────────────────────────────────── */
/*
 * Called once by Z_Init to obtain the heap region.
 * Sets *size to the number of usable bytes.
 */
static byte* I_ZoneBase(int* size)
{
    *size = DOOM_ZONE_SIZE;
    return doom_zone_heap;
}

/* ── I_Error ────────────────────────────────────────────────────────────── */
/*
 * Fatal error — print message string to stderr, then loop forever.
 * z_zone.c calls I_Error on heap corruption.
 *
 * NOT variadic: tsk-cc does not support va_list/vfprintf LLVM IR patterns.
 * The format string (with %s, %d etc.) is printed verbatim — acceptable
 * for Z_CheckHeap / Z_Malloc error paths which use simple string literals.
 */
static void I_Error(const char* error, ...)
{
    fprintf(stderr, "I_Error: ");
    fprintf(stderr, "%s\n", error);
    fflush(stderr);
    /* Infinite loop — VM interpreter will halt on next cycle boundary */
    while (1) { }
}

#endif /* __Z_ZONE_STUBS__ */
