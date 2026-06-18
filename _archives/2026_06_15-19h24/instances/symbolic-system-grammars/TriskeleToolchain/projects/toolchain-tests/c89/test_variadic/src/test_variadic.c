/*
 * test_variadic.c v2.0 — Test complet variadics
 * Author: Echopraxium with the collaboration of Claude AI
 *
 * Exit bitmask (8 tests) — expected_exit = 255
 */
#include <stdio.h>
#include <stdarg.h>

static int my_format(char* buf, const char* fmt, ...)
{
    va_list ap;
    int n;
    va_start(ap, fmt);
    n = vsprintf(buf, fmt, ap);
    va_end(ap);
    return n;
}

static void my_error_str(char* buf, const char* fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vsprintf(buf, fmt, ap);
    va_end(ap);
}

int main(void)
{
    int result = 0;
    char buf[64];
    int n;

    /* Test 1 (bit 0): printf("%d\n", 42) */
    n = printf("%d\n", 42);
    if (n >= 2) result |= 1;

    /* Test 2 (bit 1): sprintf %d */
    buf[0] = 0;
    sprintf(buf, "%d", 99);
    if (buf[0]=='9' && buf[1]=='9' && buf[2]=='\0') result |= 2;

    /* Test 3 (bit 2): sprintf %s */
    buf[0] = 0;
    sprintf(buf, "%s", "hello");
    if (buf[0]=='h' && buf[1]=='e' && buf[2]=='l' && buf[3]=='l' && buf[4]=='o') result |= 4;

    /* Test 4 (bit 3): sprintf 3 args */
    buf[0] = 0;
    sprintf(buf, "%d+%d=%d", 1, 2, 3);
    if (buf[0]=='1' && buf[2]=='2' && buf[4]=='3') result |= 8;

    /* Test 5 (bit 4): my_format %d */
    buf[0] = 0;
    my_format(buf, "val=%d", 7);
    if (buf[0]=='v' && buf[1]=='a' && buf[2]=='l' && buf[3]=='=' && buf[4]=='7') result |= 16;

    /* Test 6 (bit 5): my_format %s:%d */
    buf[0] = 0;
    my_format(buf, "%s:%d", "x", 5);
    if (buf[0]=='x' && buf[1]==':' && buf[2]=='5') result |= 32;

    /* Test 7 (bit 6): printf no-args */
    n = printf("ok\n");
    if (n >= 2) result |= 64;

    /* Test 8 (bit 7): my_error_str %d */
    buf[0] = 0;
    my_error_str(buf, "err=%d", 42);
    if (buf[0]=='e' && buf[1]=='r' && buf[2]=='r' && buf[3]=='=' && buf[4]=='4' && buf[5]=='2') result |= 128;

    return result;
}
