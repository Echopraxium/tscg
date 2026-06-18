/* projects/test_patterns/src/test_patterns.c
   Author: Echopraxium with the collaboration of Claude AI
   Tests LLVM IR patterns needed for Wolf3D / DoomGeneric:
   - switch statement
   - function pointers
   - 2D arrays
   - pointer arithmetic
   Exit bitmask: 15 = all 4 passed */

/* ── Test 1: switch statement ─────────────────────────────────────────── */
int classify(int n) {
    switch (n) {
        case 0:  return 10;
        case 1:  return 20;
        case 2:  return 30;
        default: return 99;
    }
}

/* ── Test 2: function pointers ───────────────────────────────────────── */
int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int apply(int (*fn)(int, int), int a, int b) {
    return fn(a, b);
}

/* ── Test 3: 2D array ────────────────────────────────────────────────── */
static int grid[4][4];

void fill_grid(void) {
    int i, j;
    for (i = 0; i < 4; i++)
        for (j = 0; j < 4; j++)
            grid[i][j] = i * 4 + j;
}

int sum_grid(void) {
    int i, j, s = 0;
    for (i = 0; i < 4; i++)
        for (j = 0; j < 4; j++)
            s += grid[i][j];
    return s;
}

/* ── Test 4: pointer arithmetic ──────────────────────────────────────── */
int sum_array(int *arr, int n) {
    int i, s = 0;
    for (i = 0; i < n; i++)
        s += arr[i];
    return s;
}

/* ── main ─────────────────────────────────────────────────────────────── */
int main(void) {
    int result = 0;
    int data[5];
    int i;

    /* Test 1: switch */
    if (classify(0) == 10 && classify(1) == 20 &&
        classify(2) == 30 && classify(99) == 99)
        result |= 1;

    /* Test 2: function pointers */
    if (apply(add, 3, 4) == 7 && apply(mul, 3, 4) == 12)
        result |= 2;

    /* Test 3: 2D array — sum 0..15 = 120 */
    fill_grid();
    if (sum_grid() == 120)
        result |= 4;

    /* Test 4: pointer arithmetic */
    for (i = 0; i < 5; i++) data[i] = i + 1;
    if (sum_array(data, 5) == 15)
        result |= 8;

    return result;
}
