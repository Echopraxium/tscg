/*
 * w_file_stdc.c — TriskeleVM-compatible WAD file I/O
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.1.0 (VM port — lazy vtable init, no data relocations)
 *
 * The original w_file_stdc.c initialises wad_file_class_t stdc_wad_file
 * with function pointers at global scope.  tsk-link has no data-relocation
 * support, so those pointers stay zero and any indirect call crashes.
 *
 * This version initialises the vtable lazily at first open call.
 * Functions are NOT declared static so clang -O0 emits them all.
 */

#include <stdio.h>
#include "m_misc.h"
#include "w_file.h"
#include "z_zone.h"

typedef struct
{
    wad_file_t wad;
    FILE *fstream;
} stdc_wad_file_t;

/* vtable — zero-initialised; filled by W_StdC_EnsureInit() */
wad_file_class_t stdc_wad_file;

static int stdc_init_done = 0;

/* Forward declarations (non-static so clang always emits them) */
wad_file_t *W_StdC_OpenFile(char *path);
void        W_StdC_CloseFile(wad_file_t *wad);
size_t      W_StdC_Read(wad_file_t *wad, unsigned int offset,
                        void *buffer, size_t buffer_len);

void W_StdC_EnsureInit(void)
{
    if (stdc_init_done) return;
    stdc_wad_file.OpenFile  = W_StdC_OpenFile;
    stdc_wad_file.CloseFile = W_StdC_CloseFile;
    stdc_wad_file.Read      = W_StdC_Read;
    stdc_init_done = 1;
}

wad_file_t *W_StdC_OpenFile(char *path)
{
    stdc_wad_file_t *result;
    FILE *fstream;

    W_StdC_EnsureInit();

    fstream = fopen(path, "rb");
    if (fstream == NULL)
        return NULL;

    result = Z_Malloc(sizeof(stdc_wad_file_t), PU_STATIC, 0);
    result->wad.file_class = &stdc_wad_file;
    result->wad.mapped     = NULL;
    result->wad.length     = M_FileLength(fstream);
    result->fstream        = fstream;

    return &result->wad;
}

void W_StdC_CloseFile(wad_file_t *wad)
{
    stdc_wad_file_t *stdc_wad = (stdc_wad_file_t *)wad;
    fclose(stdc_wad->fstream);
    Z_Free(stdc_wad);
}

size_t W_StdC_Read(wad_file_t *wad, unsigned int offset,
                   void *buffer, size_t buffer_len)
{
    stdc_wad_file_t *stdc_wad = (stdc_wad_file_t *)wad;
    fseek(stdc_wad->fstream, offset, SEEK_SET);
    return fread(buffer, 1, buffer_len, stdc_wad->fstream);
}
