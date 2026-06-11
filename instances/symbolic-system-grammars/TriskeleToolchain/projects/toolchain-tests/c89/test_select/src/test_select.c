/* test_select.c — C89
 * Validates: select (ternary), memset, memcpy
 * Author: Echopraxium with the collaboration of Claude AI
 */

/* ── select patterns ───────────────────────────────────────── */

int clamp(int val, int lo, int hi) {
    int r = val < lo ? lo : val;
    return r > hi ? hi : r;
}

int abs_fixed(int x) {
    return x < 0 ? -x : x;
}

int max2(int a, int b) {
    return a > b ? a : b;
}

int min2(int a, int b) {
    return a < b ? a : b;
}

/* ── memset / memcpy patterns ──────────────────────────────── */

void my_memset(char *dst, int val, int len) {
    int i;
    for (i = 0; i < len; i++) dst[i] = (char)val;
}

void my_memcpy(char *dst, const char *src, int len) {
    int i;
    for (i = 0; i < len; i++) dst[i] = src[i];
}

/* ── main — exit code = number of passing tests ────────────── */

int main(void) {
    char buf1[8];
    char buf2[8];
    int pass = 0;

    /* Test 1: clamp low */
    if (clamp(-5, 0, 10) == 0)  pass++;

    /* Test 2: clamp high */
    if (clamp(15, 0, 10) == 10) pass++;

    /* Test 3: clamp in range */
    if (clamp(5, 0, 10) == 5)   pass++;

    /* Test 4: abs negative */
    if (abs_fixed(-7) == 7)     pass++;

    /* Test 5: abs positive */
    if (abs_fixed(3) == 3)      pass++;

    /* Test 6: max */
    if (max2(4, 9) == 9)        pass++;

    /* Test 7: min */
    if (min2(4, 9) == 4)        pass++;

    /* Test 8: memset then read */
    my_memset(buf1, 0xAB, 8);
    if ((unsigned char)buf1[3] == 0xAB) pass++;

    /* Test 9: memcpy then read */
    my_memset(buf1, 0x55, 8);
    my_memcpy(buf2, buf1, 8);
    if ((unsigned char)buf2[5] == 0x55) pass++;

    return pass;  /* exit 9 = all tests pass */
}
