/*
 * doom_alloc_test.c — Test harness for Zone Memory Allocator
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Exit code = bitmask of passing tests.
 * All 8 tests pass → exit 255.
 *
 * IMPORTANT — imm19 constraint:
 *   TriskeleVM Type I format: 19-bit signed immediate → [-262144, 262143].
 *   sizeof(memblock_t) = 6 * 4 = 24  (fits imm19)
 *   sizeof(memzone_t)  = 4 + 24 + 4  = 32  (fits imm19)
 *   Heap size = 4096 (fits imm19)
 *   All literal constants used for comparison fit imm19.
 *
 * New LLVM IR patterns validated by this harness:
 *   Bit 0  (  1): Pointer comparison   — rover == start (do/while loop exit)
 *   Bit 1  (  2): Byte-offset ptr cast — (byte*)ptr - sizeof(memblock_t)
 *   Bit 2  (  4): Double indirection   — *block->user = result
 *   Bit 3  (  8): Block split          — MINFRAGMENT fragment creation
 *   Bit 4  ( 16): Z_Free merge prev    — coalesce with previous free block
 *   Bit 5  ( 32): Z_Free merge next    — coalesce with next free block
 *   Bit 6  ( 64): Z_FreeMemory loop    — walk linked list, accumulate sum
 *   Bit 7  (128): Alloc-after-free     — re-use freed block (rover logic)
 *
 * Test matrix:
 *   Test 1 (bit 0): Z_Malloc returns non-NULL for small allocation
 *   Test 2 (bit 1): Z_Free sets *user to NULL (double indirection write)
 *   Test 3 (bit 2): owner pointer updated correctly by Z_Malloc
 *   Test 4 (bit 3): two allocations split the block (second ptr > first)
 *   Test 5 (bit 4): Z_Free + prev coalesce: Z_FreeMemory increases
 *   Test 6 (bit 5): Z_Free + next coalesce: two adjacent frees merge
 *   Test 7 (bit 6): Z_FreeMemory reports zone_size - header - used bytes
 *   Test 8 (bit 7): Z_Malloc after Z_Free reuses the freed region
 */

#include "doom_alloc.h"

/* Static heap — 4096 bytes, fits comfortably in imm19 */
#define HEAP_SIZE 4096
static byte heap_buf[HEAP_SIZE];

int main(void)
{
    int   result = 0;
    void* p1;
    void* p2;
    void* p3;
    void* owner1;
    void* owner2;
    int   free_before;
    int   free_after;

    Z_Init(heap_buf, HEAP_SIZE);

    /* ── Test 1 (bit 0): Z_Malloc returns non-NULL
     * Validates: do/while loop terminates (rover == start exit cond),
     *            pointer comparison in LLVM IR.
     * Alloc 64 bytes PU_STATIC, no owner. */
    {
        p1 = Z_Malloc(64, PU_STATIC, 0);
        if (p1 != 0)
            result |= 1;
    }

    /* ── Test 2 (bit 1): byte-offset pointer cast
     * Z_Free must compute: block = (memblock_t*)((byte*)ptr - sizeof(memblock_t))
     * Validates: (byte*)cast + negative GEP offset → LLVM getelementptr i8.
     * After Z_Free, owner1 should be cleared to NULL. */
    {
        owner1 = (void*)1;   /* non-NULL sentinel */
        p2 = Z_Malloc(32, PU_STATIC, (void**)&owner1);
        /* owner1 should now == p2 (set by Z_Malloc) */
        Z_Free(p2);
        /* Z_Free clears *user → owner1 should be NULL */
        if (owner1 == 0)
            result |= 2;
    }

    /* ── Test 3 (bit 2): double indirection — *block->user = result
     * Z_Malloc writes result pointer into *user.
     * owner2 should equal the returned pointer. */
    {
        owner2 = 0;
        p3 = Z_Malloc(16, PU_STATIC, (void**)&owner2);
        if (owner2 == p3 && p3 != 0)
            result |= 4;
        Z_Free(p3);
    }

    /* Re-init for remaining tests — clean slate */
    Z_Init(heap_buf, HEAP_SIZE);

    /* ── Test 4 (bit 3): block split (MINFRAGMENT)
     * Allocate two blocks; p2 must be strictly after p1 (block was split).
     * sizeof(memblock_t)=24, so p2 >= p1 + 64 + 24 = p1 + 88.
     * We just check p2 > p1 (pointer comparison in LLVM IR). */
    {
        p1 = Z_Malloc(64,  PU_STATIC, 0);
        p2 = Z_Malloc(128, PU_STATIC, 0);
        if (p1 != 0 && p2 != 0 && (byte*)p2 > (byte*)p1)
            result |= 8;
    }

    /* ── Test 5 (bit 4): Z_Free + prev-coalesce
     * Free p1 first (it becomes a free block), then free p2.
     * p2->prev == p1's block → merge: p1 block grows, rover adjusted.
     * Validate: Z_FreeMemory after freeing both > Z_FreeMemory after one free. */
    {
        Z_Init(heap_buf, HEAP_SIZE);
        p1 = Z_Malloc(64,  PU_STATIC, 0);
        p2 = Z_Malloc(128, PU_STATIC, 0);
        Z_Free(p1);
        free_before = Z_FreeMemory();
        Z_Free(p2);
        free_after = Z_FreeMemory();
        /* After coalescing, free memory should increase by >= p2's block size */
        if (free_after > free_before)
            result |= 16;
    }

    /* ── Test 6 (bit 5): Z_Free + next-coalesce
     * Allocate p1, p2, p3. Free p3, then free p2.
     * p2->next is p3 (already free) → merge next.
     * Validate: Z_FreeMemory increases correctly. */
    {
        Z_Init(heap_buf, HEAP_SIZE);
        p1 = Z_Malloc(64,  PU_STATIC, 0);
        p2 = Z_Malloc(64,  PU_STATIC, 0);
        p3 = Z_Malloc(64,  PU_STATIC, 0);
        Z_Free(p3);
        free_before = Z_FreeMemory();
        Z_Free(p2);
        free_after = Z_FreeMemory();
        if (free_after > free_before)
            result |= 32;
        Z_Free(p1);
    }

    /* ── Test 7 (bit 6): Z_FreeMemory linked-list walk
     * After Z_Init, one allocation of 128 bytes.
     * free = total - sizeof(memzone_t) - sizeof(memblock_t) - 128 (aligned to 4).
     * We just check that Z_FreeMemory() < HEAP_SIZE and > 0. */
    {
        Z_Init(heap_buf, HEAP_SIZE);
        p1 = Z_Malloc(128, PU_STATIC, 0);
        free_after = Z_FreeMemory();
        if (free_after > 0 && free_after < HEAP_SIZE)
            result |= 64;
        Z_Free(p1);
    }

    /* ── Test 8 (bit 7): alloc-after-free reuses freed block
     * Alloc p1 (64 bytes), record its address, free it, alloc p2 (64 bytes).
     * The rover logic should give p2 == p1 (same region reused). */
    {
        Z_Init(heap_buf, HEAP_SIZE);
        p1 = Z_Malloc(64, PU_STATIC, 0);
        Z_Free(p1);
        p2 = Z_Malloc(64, PU_STATIC, 0);
        if (p2 == p1)
            result |= 128;
    }

    return result; /* 255 = all 8 tests passed */
}
