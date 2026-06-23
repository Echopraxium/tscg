/*
 * w_file.c — TriskeleVM-compatible WAD file dispatch
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.1.0 (VM port — no data relocations)
 *
 * The original w_file.c uses a static wad_file_class_t *wad_file_classes[]
 * initialised with &stdc_wad_file.  That is a data-segment relocation that
 * tsk-link cannot resolve, leaving the pointer at 0.
 *
 * This version calls W_StdC_* directly, avoiding all data relocations.
 */

#include <stdio.h>
#include "config.h"
#include "doomtype.h"
#include "m_argv.h"
#include "w_file.h"

/* Declared in w_file_stdc.c */
extern wad_file_class_t stdc_wad_file;
extern void W_StdC_EnsureInit(void);
extern wad_file_t *W_StdC_OpenFile(char *path);
extern void        W_StdC_CloseFile(wad_file_t *wad);
extern size_t      W_StdC_Read(wad_file_t *wad, unsigned int offset,
                               void *buffer, size_t buffer_len);

wad_file_t *W_OpenFile(char *path)
{
    /* Always initialise the vtable before any use. */
    W_StdC_EnsureInit();

    /* -mmap not supported in TriskeleVM: always use stdc backend. */
    return W_StdC_OpenFile(path);
}

void W_CloseFile(wad_file_t *wad)
{
    W_StdC_CloseFile(wad);
}

size_t W_Read(wad_file_t *wad, unsigned int offset,
              void *buffer, size_t buffer_len)
{
    return W_StdC_Read(wad, offset, buffer, buffer_len);
}
