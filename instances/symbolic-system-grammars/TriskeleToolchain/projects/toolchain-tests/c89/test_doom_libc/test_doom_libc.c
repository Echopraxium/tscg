/*
 * test_doom_libc.c — v0.3.10 DoomGeneric libc coverage
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Exit bitmask (9 tests) — expected_exit = 0x1FF = 511
 *
 *  bit 0  atoi basic
 *  bit 1  toupper / tolower
 *  bit 2  isspace / isdigit / isalpha
 *  bit 3  strcasecmp
 *  bit 4  strncasecmp
 *  bit 5  strstr
 *  bit 6  strdup
 *  bit 7  strlcpy
 *  bit 8  snprintf
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* strlcpy/strlcat are not in C89 standard but used by Doom */
extern size_t strlcpy(char* dst, const char* src, size_t size);
extern size_t strlcat(char* dst, const char* src, size_t size);

int main(void)
{
    int result = 0;
    char buf[64];

    /* Test 1 (bit 0): atoi */
    if (atoi("42") == 42 && atoi("-7") == -7 && atoi("  10") == 10)
        result |= 1;

    /* Test 2 (bit 1): toupper / tolower */
    if (toupper('a') == 'A' && tolower('Z') == 'z' && toupper('3') == '3')
        result |= 2;

    /* Test 3 (bit 2): isspace / isdigit / isalpha */
    if (isspace(' ') && isspace('\t') && !isspace('x') &&
        isdigit('5') && !isdigit('x') &&
        isalpha('a') && !isalpha('3'))
        result |= 4;

    /* Test 4 (bit 3): strcasecmp */
    if (strcasecmp("DOOM", "doom") == 0 &&
        strcasecmp("ABC", "ABD") < 0 &&
        strcasecmp("ABD", "ABC") > 0)
        result |= 8;

    /* Test 5 (bit 4): strncasecmp */
    if (strncasecmp("WOLF3D", "wolf3d", 6) == 0 &&
        strncasecmp("WOLF", "wolf3d", 4) == 0)
        result |= 16;

    /* Test 6 (bit 5): strstr */
    if (strstr("doomgeneric", "generic") != 0 &&
        strstr("hello", "xyz") == 0)
        result |= 32;

    /* Test 7 (bit 6): strdup */
    {
        char* p = strdup("TriskeleVM");
        if (p != 0 && strcmp(p, "TriskeleVM") == 0)
            result |= 64;
        /* no free — bump allocator */
    }

    /* Test 8 (bit 7): strlcpy */
    {
        buf[0] = '\0';
        size_t r = strlcpy(buf, "Doom", sizeof(buf));
        if (r == 4 && strcmp(buf, "Doom") == 0)
            result |= 128;
    }

    /* Test 9 (bit 8): snprintf */
    {
        buf[0] = '\0';
        int n = snprintf(buf, sizeof(buf), "v%d.%d", 0, 3);
        if (n == 4 && buf[0]=='v' && buf[1]=='0' && buf[2]=='.' && buf[3]=='3')
            result |= 256;
    }

    return result;
}
