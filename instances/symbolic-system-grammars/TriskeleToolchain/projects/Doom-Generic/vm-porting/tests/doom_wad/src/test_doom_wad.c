/*
 * test_doom_wad.c — Test harness for DoomGeneric WAD loader
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * Compiles real DoomGeneric: w_wad.c + w_file.c + w_file_stdc.c + z_zone.c
 * from Doom-Generic/src/.
 *
 * Strategy: write a minimal valid IWAD file to a temp path, load it with
 * W_AddFile, then exercise the full W_ API.
 *
 * WAD layout (little-endian, as Doom expects):
 *   Offset  0: "IWAD"            (4 bytes, identification)
 *   Offset  4: numlumps = 2      (int32)
 *   Offset  8: infotableofs = 28 (int32) — directory starts after 2 lumps data
 *   Offset 12: lump PLAYPAL data = { 0x01, 0x02, 0x03, 0x04 }  (4 bytes, pos=12)
 *   Offset 16: lump ENDOOM  data = { 0xAA, 0xBB }              (2 bytes, pos=16)
 *   Offset 18: padding to align directory at 28                 (10 bytes)
 *   Offset 28: filelump[0]: filepos=12, size=4, name="PLAYPAL\0"
 *   Offset 44: filelump[1]: filepos=16, size=2, name="ENDOOM\0\0"
 *   Total: 60 bytes
 *
 * Exit bitmask (8 tests) — expected_exit = 0xFF = 255
 *
 *  bit 0  W_AddFile returns non-NULL wad_file_t
 *  bit 1  numlumps == 2 after W_AddFile
 *  bit 2  W_CheckNumForName("PLAYPAL") == 0
 *  bit 3  W_GetNumForName("PLAYPAL") == 0
 *  bit 4  W_LumpLength(0) == 4
 *  bit 5  W_ReadLump(0): first byte == 0x01
 *  bit 6  W_GenerateHashTable + W_CheckNumForName("ENDOOM") == 1
 *  bit 7  W_CacheLumpNum(0, PU_STATIC) returns non-NULL
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Stubs must be included BEFORE Doom headers to define I_Error etc. */
#include "doom_wad_stubs.h"

/* Doom headers from ../../src/ (via include_dirs in pipeline.toml) */
#include "z_zone.h"
#include "w_wad.h"

/* ── Minimal WAD builder ─────────────────────────────────────────────────── */

/* WAD is written as raw bytes — no struct alignment worries. */
static void write_le32(unsigned char *buf, int offset, int val)
{
    unsigned char *p = buf + offset;
    p[0] = (unsigned char)( val        & 0xFF);
    p[1] = (unsigned char)((val >>  8) & 0xFF);
    p[2] = (unsigned char)((val >> 16) & 0xFF);
    p[3] = (unsigned char)((val >> 24) & 0xFF);
}

static int build_test_wad(const char *path)
{
    unsigned char wad[60];
    FILE *f;

    memset(wad, 0, sizeof(wad));

    /* Header */
    wad[0] = 'I'; wad[1] = 'W'; wad[2] = 'A'; wad[3] = 'D';
    write_le32(wad,  4, 2);   /* numlumps */
    write_le32(wad,  8, 28);  /* infotableofs */

    /* Lump 0 data: PLAYPAL — 4 bytes at offset 12 */
    wad[12] = 0x01; wad[13] = 0x02; wad[14] = 0x03; wad[15] = 0x04;

    /* Lump 1 data: ENDOOM — 2 bytes at offset 16 */
    wad[16] = 0xAA; wad[17] = 0xBB;

    /* Padding 18..27 already zero */

    /* Directory entry 0: filepos=12, size=4, name="PLAYPAL\0" */
    write_le32(wad, 28, 12);
    write_le32(wad, 32, 4);
    wad[36]='P'; wad[37]='L'; wad[38]='A'; wad[39]='Y';
    wad[40]='P'; wad[41]='A'; wad[42]='L'; wad[43]=0;

    /* Directory entry 1: filepos=16, size=2, name="ENDOOM\0\0" */
    write_le32(wad, 44, 16);
    write_le32(wad, 48, 2);
    wad[52]='E'; wad[53]='N'; wad[54]='D'; wad[55]='O';
    wad[56]='O'; wad[57]='M'; wad[58]=0;  wad[59]=0;

    f = fopen(path, "wb");
    if (!f) return 0;
    fwrite(wad, 1, sizeof(wad), f);
    fclose(f);
    return 1;
}

/* ── main ────────────────────────────────────────────────────────────────── */

int main(void)
{
    const char *wad_path = "test_minimal.wad";
    wad_file_t *wf;
    int result = 0;

    /* Init zone memory (z_zone.c requires Z_Init before any Z_Malloc) */
    Z_Init();

    /* Build minimal WAD file on disk */
    if (!build_test_wad(wad_path))
        return 0;  /* can't create temp file — all tests fail */

    /* ── Test 1 (bit 0): W_AddFile returns non-NULL ──────────────────────── */
    wf = W_AddFile(wad_path);
    if (wf != 0)
        result |= (1 << 0);

    /* ── Test 2 (bit 1): numlumps == 2 ──────────────────────────────────── */
    if (numlumps == 2)
        result |= (1 << 1);

    /* ── Test 3 (bit 2): W_CheckNumForName("PLAYPAL") == 0 ──────────────── */
    {
        int idx = W_CheckNumForName("PLAYPAL");
        if (idx == 0)
            result |= (1 << 2);
    }

    /* ── Test 4 (bit 3): W_GetNumForName("PLAYPAL") == 0 ────────────────── */
    {
        int idx = W_GetNumForName("PLAYPAL");
        if (idx == 0)
            result |= (1 << 3);
    }

    /* ── Test 5 (bit 4): W_LumpLength(0) == 4 ───────────────────────────── */
    {
        int len = W_LumpLength(0);
        if (len == 4)
            result |= (1 << 4);
    }

    /* ── Test 6 (bit 5): W_ReadLump(0) — first byte == 0x01 ─────────────── */
    {
        unsigned char buf[4];
        buf[0] = 0;
        W_ReadLump(0, buf);
        if (buf[0] == 0x01)
            result |= (1 << 5);
    }

    /* ── Test 7 (bit 6): W_GenerateHashTable + W_CheckNumForName("ENDOOM") == 1 */
    {
        int idx;
        W_GenerateHashTable();
        idx = W_CheckNumForName("ENDOOM");
        if (idx == 1)
            result |= (1 << 6);
    }

    /* ── Test 8 (bit 7): W_CacheLumpNum(0, PU_STATIC) returns non-NULL ──── */
    {
        void *p = W_CacheLumpNum(0, PU_STATIC);
        if (p != 0)
            result |= (1 << 7);
    }

    return result;
}
