/*
 * doom_argv_stubs.h — Stubs for DoomGeneric m_argv.c dependencies
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * m_argv.c includes: doomtype.h, i_system.h, m_misc.h, m_argv.h
 * All these headers are satisfied by ../../src/ (include_dirs in pipeline.toml).
 *
 * The only runtime stub needed is I_Error — called only inside
 * #if ORIGCODE (LoadResponseFile), which is NOT compiled by default.
 * We provide it anyway so the symbol is available for the linker.
 *
 * M_FileLength is declared in m_misc.h and used only in LoadResponseFile
 * (#if ORIGCODE). We stub it here to avoid an undefined symbol at link time
 * in case ORIGCODE is ever enabled.
 */

#ifndef __DOOM_ARGV_STUBS__
#define __DOOM_ARGV_STUBS__

#include <stdio.h>
#include <stdlib.h>

/*
 * I_Error — variadic fatal error (used in #if ORIGCODE blocks only).
 * Prints format string as-is (no va_list), then exits.
 */
static void I_Error(const char *error, ...)
{
    fprintf(stderr, "I_Error: %s\n", error);
    fflush(stderr);
    exit(1);
}

/*
 * M_FileLength — returns the byte length of an open FILE*.
 * Used only in LoadResponseFile (#if ORIGCODE).
 */
static long M_FileLength(FILE *handle)
{
    long pos, len;
    pos = ftell(handle);
    fseek(handle, 0, SEEK_END);
    len = ftell(handle);
    fseek(handle, pos, SEEK_SET);
    return len;
}

#endif /* __DOOM_ARGV_STUBS__ */
