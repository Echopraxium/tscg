/*
 * doom_zzone_test.c — Test harness for DoomGeneric z_zone.c (real implementation)
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * Tests the original z_zone.c with stubs for I_Error / I_ZoneBase.
 * Uses the same 8-bit exit bitmask convention as doom_alloc (exit = bits 7..0).
 *
 * Exit codes (cumulative bit OR):
 *   Bit 0 (1)   — Z_Malloc returns non-NULL
 *   Bit 1 (2)   — Z_Free does not corrupt heap (Z_CheckHeap passes)
 *   Bit 2 (4)   — double indirection: *user pointer is updated by Z_Malloc
 *   Bit 3 (8)   — Z_Malloc splits blocks (p2 > p1, different addresses)
 *   Bit 4 (16)  — Z_FreeTags frees level-tagged blocks
 *   Bit 5 (32)  — Z_FreeMemory increases after Z_Free
 *   Bit 6 (64)  — Z_CheckHeap passes after multiple alloc/free cycles
 *   Bit 7 (128) — Z_Malloc reuses freed blocks (alloc-after-free)
 *
 * All 8 bits set → exit(255)
 */

#include "z_zone.h"
#include <stdlib.h>

int main(void)
{
    void* p1;
    void* p2;
    void* p3;
    void* p4;
    void* user_ptr;
    void** user = &user_ptr;
    int free_before;
    int free_after;
    int result = 0;

    /* ── Init ─────────────────────────────────────────────────────────── */
    Z_Init();

    /* ── Test 1 (bit 0): Z_Malloc returns non-NULL ────────────────────── */
    p1 = Z_Malloc(256, PU_STATIC, 0);
    if (p1 != 0)
        result |= (1 << 0);

    /* ── Test 2 (bit 1): Z_Free + Z_CheckHeap passes ─────────────────── */
    p2 = Z_Malloc(256, PU_STATIC, 0);
    Z_Free(p1);
    /* Z_CheckHeap calls I_Error on corruption — if we reach here, heap OK */
    Z_CheckHeap();
    result |= (1 << 1);

    /* ── Test 3 (bit 2): double indirection — *user updated ──────────── */
    user_ptr = 0;
    p3 = Z_Malloc(128, PU_STATIC, user);
    if (user_ptr == p3)
        result |= (1 << 2);

    /* ── Test 4 (bit 3): two allocations have different addresses ─────── */
    p4 = Z_Malloc(128, PU_LEVEL, 0);
    if (p4 != p3 && p4 != 0)
        result |= (1 << 3);

    /* ── Test 5 (bit 4): Z_FreeTags releases PU_LEVEL blocks ─────────── */
    free_before = Z_FreeMemory();
    Z_FreeTags(PU_LEVEL, PU_CACHE);
    free_after = Z_FreeMemory();
    if (free_after > free_before)
        result |= (1 << 4);

    /* ── Test 6 (bit 5): Z_FreeMemory increases after Z_Free ─────────── */
    free_before = Z_FreeMemory();
    Z_Free(p3);
    free_after = Z_FreeMemory();
    if (free_after > free_before)
        result |= (1 << 5);

    /* ── Test 7 (bit 6): Z_CheckHeap passes after alloc/free cycles ──── */
    {
        int i;
        void* ptrs[8];
        for (i = 0; i < 8; i++)
            ptrs[i] = Z_Malloc(64, PU_STATIC, 0);
        for (i = 0; i < 4; i++)
            Z_Free(ptrs[i]);
        Z_CheckHeap();
        result |= (1 << 6);
        for (i = 4; i < 8; i++)
            Z_Free(ptrs[i]);
    }

    /* ── Test 8 (bit 7): alloc-after-free reuses freed region ─────────── */
    {
        void* a = Z_Malloc(512, PU_STATIC, 0);
        void* b;
        Z_Free(a);
        b = Z_Malloc(512, PU_STATIC, 0);
        /* rover should return the same region (or nearby) */
        if (b != 0) {
            /* use char* subtraction to avoid void*->int cast warning */
            long diff = (long)((char*)b - (char*)a);
            if (diff < 0) diff = -diff;
            if (diff < 1024)   /* within 1KB = same freed block */
                result |= (1 << 7);
        }
        if (b) Z_Free(b);
    }

    Z_CheckHeap();
    return result;
}
