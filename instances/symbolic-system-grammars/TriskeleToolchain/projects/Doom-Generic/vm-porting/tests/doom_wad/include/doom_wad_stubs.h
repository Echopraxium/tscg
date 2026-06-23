/*
 * doom_wad_stubs.h — Stubs for DoomGeneric w_wad.c / w_file.c dependencies
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.2
 *
 * Stubs for all external symbols not provided by tsk-libc:
 *   I_Error, I_ZoneBase, I_BeginRead, I_EndRead,
 *   M_FileLength, M_StringCopy, M_ExtractFileBase,
 *   D_GameMissionString, D_SuggestGameName,
 *   I_VideoWaitVBL
 *
 * NOTE: myargc/myargv are defined in m_argv.c (compiled in src/).
 */

#ifndef __DOOM_WAD_STUBS__
#define __DOOM_WAD_STUBS__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>
#include "doomtype.h"
#include "d_mode.h"

/* Zone memory size given to Doom: 4 MB */
#define ZONE_SIZE (1 * 1024 * 1024)  // 1MB: VM heap = 4MB total, leave 3MB for calloc/malloc

/* ── I_Error ─────────────────────────────────────────────────────────────── */

void I_Error(const char *error, ...)
{
    char buf[256];
    va_list ap;
    va_start(ap, error);
    vsnprintf(buf, sizeof(buf), error, ap);
    va_end(ap);
    /* Use printf to avoid @stderr external global (not resolved in TriskeleVM) */
    printf("I_Error: %s\n", buf);
    exit(1);
}

/* ── I_ZoneBase ──────────────────────────────────────────────────────────── */
/*
 * Returns a pointer to a freshly malloc'd block of ZONE_SIZE bytes.
 * Z_Init uses this block as the entire zone memory arena.
 * *size is set to the actual size returned.
 */
byte *I_ZoneBase(int *size)
{
    byte *zone = (byte *)malloc(ZONE_SIZE);
    if (!zone)
    {
        printf("I_ZoneBase: malloc failed\n");
        exit(1);
    }
    *size = ZONE_SIZE;
    return zone;
}

/* ── I_BeginRead / I_EndRead ─────────────────────────────────────────────── */
/* Called around WAD lump reads — no-op in our headless VM context. */

void I_BeginRead(void) {}
void I_EndRead(void)   {}

/* ── M_FileLength ────────────────────────────────────────────────────────── */

long M_FileLength(FILE *handle)
{
    long pos, len;
    pos = ftell(handle);
    fseek(handle, 0, SEEK_END);
    len = ftell(handle);
    fseek(handle, pos, SEEK_SET);
    return len;
}

/* ── M_StringCopy ────────────────────────────────────────────────────────── */

int M_StringCopy(char *dest, const char *src, size_t dest_size)
{
    if (dest_size < 1) return 0;
    strncpy(dest, src, dest_size - 1);
    dest[dest_size - 1] = '\0';
    return 1;
}

/* ── M_ExtractFileBase ───────────────────────────────────────────────────── */
/*
 * Extracts the base filename (without extension) from a full path.
 * dest must be at least 9 bytes (8 chars + NUL), uppercase, Doom-style.
 * Used by W_AddFile to name single-lump .wad files.
 */
void M_ExtractFileBase(char *path, char *dest)
{
    char *src;
    char *p;
    int   i;

    /* Find last separator */
    src = path;
    for (p = path; *p; p++)
        if (*p == '/' || *p == '\\') src = p + 1;

    /* Copy up to 8 chars, stop at '.' */
    for (i = 0; i < 8 && src[i] && src[i] != '.'; i++)
        dest[i] = (char)toupper((unsigned char)src[i]);

    /* Pad with NULs */
    for (; i < 8; i++)
        dest[i] = 0;
}

/* ── D_GameMissionString ─────────────────────────────────────────────────── */
/* Returns a human-readable string for a GameMission_t value. */

char *D_GameMissionString(GameMission_t mission)
{
    switch (mission)
    {
        case doom:        return "doom";
        case doom2:       return "doom2";
        case pack_tnt:    return "tnt";
        case pack_plut:   return "plutonia";
        case pack_chex:   return "chex";
        case pack_hacx:   return "hacx";
        default:          return "unknown";
    }
}

/* ── D_SuggestGameName ───────────────────────────────────────────────────── */

char *D_SuggestGameName(GameMission_t mission, GameMode_t mode)
{
    (void)mode;
    return D_GameMissionString(mission);
}

/* ── I_VideoWaitVBL ──────────────────────────────────────────────────────── */

void I_VideoWaitVBL(int count) { (void)count; }

#endif /* __DOOM_WAD_STUBS__ */
