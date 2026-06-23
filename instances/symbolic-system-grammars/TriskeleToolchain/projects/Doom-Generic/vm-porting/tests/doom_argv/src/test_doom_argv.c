/*
 * test_doom_argv.c — Test harness for DoomGeneric m_argv.c
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 1.0.0
 *
 * Compiles real DoomGeneric m_argv.c from Doom-Generic/src/.
 * Uses the same 8-bit exit bitmask convention as other doom_* tests.
 *
 * Exit bitmask (6 tests) — expected_exit = 0x3F = 63
 *
 *  bit 0  M_CheckParm finds existing param "-warp"
 *  bit 1  M_CheckParm returns 0 for missing param "-nosound"
 *  bit 2  M_CheckParmWithArgs: param at last position doesn't count (num_args=1)
 *  bit 3  M_ParmExists returns true for "-warp"
 *  bit 4  M_ParmExists returns false for "-nosound"
 *  bit 5  M_GetExecutableName strips "C:\\games\\" prefix
 */

#include <stdlib.h>
#include <string.h>
#include "doom_argv_stubs.h"
#include "m_argv.h"

/* Fake argv for tests:
 *   argv[0] = platform-specific path (Windows: C:\games\doom.exe, Unix: /games/doom.exe)
 *   argv[1] = "-warp"
 *   argv[2] = "1"
 *   argv[3] = "-skill"
 *   argv[4] = "3"
 *   (no "-nosound")
 */
#if defined(_WIN32) || defined(__DJGPP__)
static char arg0[] = "C:\\games\\doom.exe";
#else
static char arg0[] = "/games/doom.exe";
#endif
static char arg1[] = "-warp";
static char arg2[] = "1";
static char arg3[] = "-skill";
static char arg4[] = "3";

static char *test_argv[] = { arg0, arg1, arg2, arg3, arg4 };
static int   test_argc   = 5;

int main(void)
{
    int result = 0;

    /* Install fake argv/argc into m_argv.c globals */
    myargv = test_argv;
    myargc = test_argc;

    /* Test 1 (bit 0): M_CheckParm finds "-warp" at index 1 */
    {
        int idx = M_CheckParm("-warp");
        if (idx == 1)
            result |= (1 << 0);
    }

    /* Test 2 (bit 1): M_CheckParm returns 0 for "-nosound" (absent) */
    {
        int idx = M_CheckParm("-nosound");
        if (idx == 0)
            result |= (1 << 1);
    }

    /* Test 3 (bit 2): M_CheckParmWithArgs("-skill", 1)
     * "-skill" is at index 3, myargc=5 → myargc - num_args = 4
     * Loop condition: i < 4, so i=3 is valid → returns 3 */
    {
        int idx = M_CheckParmWithArgs("-skill", 1);
        if (idx == 3)
            result |= (1 << 2);
    }

    /* Test 4 (bit 3): M_ParmExists returns true for "-warp" */
    {
        if (M_ParmExists("-warp"))
            result |= (1 << 3);
    }

    /* Test 5 (bit 4): M_ParmExists returns false for "-nosound" */
    {
        if (!M_ParmExists("-nosound"))
            result |= (1 << 4);
    }

    /* Test 6 (bit 5): M_GetExecutableName strips path prefix
     * Windows: argv[0] = "C:\games\doom.exe" → DIR_SEPARATOR = '\\'
     * Unix:    argv[0] = "/games/doom.exe"  → DIR_SEPARATOR = '/'
     * strrchr finds last DIR_SEPARATOR → +1 returns "doom.exe" */
    {
        char *name = M_GetExecutableName();
        if (name != 0 && strcmp(name, "doom.exe") == 0)
            result |= (1 << 5);
    }

    return result;
}
