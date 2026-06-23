/*
 * doom_alloc.c — Zone Memory Allocator (standalone)
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Derived from DoomGeneric z_zone.c
 * Copyright(C) 1993-1996 Id Software, Inc.
 * Copyright(C) 2005-2014 Simon Howard
 *
 * Differences from original z_zone.c:
 *   - No I_Error / I_ZoneBase / printf dependencies
 *   - Z_Init takes a caller-supplied buffer (heap, heap_size)
 *   - Error conditions return/set error codes instead of calling I_Error
 *   - C89 compliant (no // comments, no stdint.h)
 */

#include "doom_alloc.h"

memzone_t* mainzone = 0;

/* ── Z_ClearZone ──────────────────────────────────────────────────────── */

void Z_ClearZone(memzone_t* zone)
{
    memblock_t* block;

    /* Set the entire zone to one free block */
    block = (memblock_t*)((byte*)zone + sizeof(memzone_t));

    zone->blocklist.next = block;
    zone->blocklist.prev = block;
    zone->blocklist.user = (void**)zone;
    zone->blocklist.tag  = PU_STATIC;
    zone->rover          = block;

    block->prev = &zone->blocklist;
    block->next = &zone->blocklist;
    block->tag  = PU_FREE;
    block->size = zone->size - sizeof(memzone_t);
}

/* ── Z_Init ───────────────────────────────────────────────────────────── */
/*
 * Initialise the zone allocator over a caller-supplied heap buffer.
 * heap      : pointer to a static byte array
 * heap_size : total size of that array in bytes
 */
void Z_Init(byte* heap, int heap_size)
{
    mainzone       = (memzone_t*)heap;
    mainzone->size = heap_size;
    Z_ClearZone(mainzone);
}

/* ── Z_Free ───────────────────────────────────────────────────────────── */

void Z_Free(void* ptr)
{
    memblock_t* block;
    memblock_t* other;

    block = (memblock_t*)((byte*)ptr - sizeof(memblock_t));

    /* Validate ZONEID — silently ignore on mismatch (no I_Error) */
    if (block->id != ZONEID)
        return;

    /* Clear owner's pointer if present */
    if (block->tag != PU_FREE && block->user != 0)
        *block->user = 0;

    /* Mark as free */
    block->tag  = PU_FREE;
    block->user = 0;
    block->id   = 0;

    /* Merge with previous free block */
    other = block->prev;
    if (other->tag == PU_FREE)
    {
        other->size += block->size;
        other->next  = block->next;
        other->next->prev = other;

        if (block == mainzone->rover)
            mainzone->rover = other;

        block = other;
    }

    /* Merge with next free block */
    other = block->next;
    if (other->tag == PU_FREE)
    {
        block->size += other->size;
        block->next  = other->next;
        block->next->prev = block;

        if (other == mainzone->rover)
            mainzone->rover = block;
    }
}

/* ── Z_Malloc ─────────────────────────────────────────────────────────── */
/*
 * Returns NULL on allocation failure (replaces I_Error).
 */
void* Z_Malloc(int size, int tag, void** user)
{
    int         extra;
    memblock_t* start;
    memblock_t* rover;
    memblock_t* newblock;
    memblock_t* base;
    void*       result;

    /* Align size to MEM_ALIGN */
    size = (size + MEM_ALIGN - 1) & ~(MEM_ALIGN - 1);

    /* Account for block header */
    size += sizeof(memblock_t);

    /* Start scan from rover (back up over free block before it) */
    base = mainzone->rover;
    if (base->prev->tag == PU_FREE)
        base = base->prev;

    rover = base;
    start = base->prev;

    do
    {
        if (rover == start)
        {
            /* Scanned all the way around — allocation failure */
            return 0;
        }

        if (rover->tag != PU_FREE)
        {
            if (rover->tag < PU_PURGELEVEL)
            {
                /* Cannot purge — skip base past this block */
                base = rover = rover->next;
            }
            else
            {
                /* Purgeable — free it, then continue scan */
                base = base->prev;
                Z_Free((byte*)rover + sizeof(memblock_t));
                base  = base->next;
                rover = base->next;
            }
        }
        else
        {
            rover = rover->next;
        }
    }
    while (base->tag != PU_FREE || base->size < size);

    /* Found a block big enough */
    extra = base->size - size;

    if (extra > MINFRAGMENT)
    {
        /* Split: leave a free fragment after the allocated block */
        newblock       = (memblock_t*)((byte*)base + size);
        newblock->size = extra;
        newblock->tag  = PU_FREE;
        newblock->user = 0;
        newblock->prev = base;
        newblock->next = base->next;
        newblock->next->prev = newblock;

        base->next = newblock;
        base->size = size;
    }

    /* Purgeable blocks require an owner */
    if (user == 0 && tag >= PU_PURGELEVEL)
        return 0;

    base->user = user;
    base->tag  = tag;

    result = (void*)((byte*)base + sizeof(memblock_t));

    if (base->user)
        *base->user = result;

    /* Advance rover for next allocation */
    mainzone->rover = base->next;

    base->id = ZONEID;

    return result;
}

/* ── Z_FreeMemory ─────────────────────────────────────────────────────── */

int Z_FreeMemory(void)
{
    memblock_t* block;
    int         free_bytes;

    free_bytes = 0;

    block = mainzone->blocklist.next;
    while (block != &mainzone->blocklist)
    {
        if (block->tag == PU_FREE || block->tag >= PU_PURGELEVEL)
            free_bytes += block->size;
        block = block->next;
    }

    return free_bytes;
}
