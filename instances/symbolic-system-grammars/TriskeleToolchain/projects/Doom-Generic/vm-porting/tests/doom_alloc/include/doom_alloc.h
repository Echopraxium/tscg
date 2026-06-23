/*
 * doom_alloc.h — Zone Memory Allocator types and constants
 * Standalone wrapper (no DoomGeneric dependencies)
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Derived from DoomGeneric z_zone.h / z_zone.c
 * Copyright(C) 1993-1996 Id Software, Inc.
 * Copyright(C) 2005-2014 Simon Howard
 */

#ifndef __DOOM_ALLOC__
#define __DOOM_ALLOC__

/* byte type (C89 compliant — no stdint.h) */
typedef unsigned char byte;

/*
 * Memory tags — control block lifecycle.
 * PU_FREE      : block is free (available for reuse)
 * PU_STATIC    : never freed automatically
 * PU_PURGELEVEL: blocks >= this tag can be auto-purged by Z_Malloc
 */
#define PU_FREE       0
#define PU_STATIC     1
#define PU_PURGELEVEL 100

/* Zone magic identifier — detects corruption */
#define ZONEID   0x1d4a11

/* Minimum fragment size — don't split blocks smaller than this */
#define MINFRAGMENT  64

/* Alignment: align to pointer size (4 bytes on 32-bit) */
#define MEM_ALIGN    4

/*
 * memblock_t — doubly-linked list node for each allocation.
 * The block header immediately precedes the user data.
 * Layout: [memblock_t header][user data ...]
 */
typedef struct memblock_s
{
    int               size;   /* total block size including this header */
    void**            user;   /* pointer to owner's pointer (or NULL)   */
    int               tag;    /* PU_FREE if free, else lifecycle tag     */
    int               id;     /* ZONEID when allocated, 0 when free      */
    struct memblock_s* next;
    struct memblock_s* prev;
} memblock_t;

/*
 * memzone_t — zone header, sits at the start of the heap region.
 * blocklist is a sentinel node (tag=PU_STATIC, never allocated).
 */
typedef struct
{
    int         size;       /* total zone size including this header */
    memblock_t  blocklist;  /* sentinel: .next/.prev wrap the ring   */
    memblock_t* rover;      /* next-fit scan pointer                 */
} memzone_t;

/* Global zone pointer */
extern memzone_t* mainzone;

/* Public API */
void  Z_Init     (byte* heap, int heap_size);
void  Z_ClearZone(memzone_t* zone);
void* Z_Malloc   (int size, int tag, void** user);
void  Z_Free     (void* ptr);
int   Z_FreeMemory(void);

#endif /* __DOOM_ALLOC__ */
