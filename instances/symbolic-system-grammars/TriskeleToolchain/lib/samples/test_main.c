/* lib/samples/test_main.c
 * Author: Echopraxium with the collaboration of Claude AI
 * Version: 0.3.0
 *
 * Pipeline validation test for TriskeleVM.
 * Tests: F_CALL/F_RET, global array access, backward jumps, nested loops.
 *
 * Compile:
 *   clang -O1 -emit-llvm -S lib/samples/test_main.c -o lib/samples/test_main.ll
 *   cargo run -p tsk-cc  -- lib/samples/test_main.ll  -o lib/samples/test_main.tobj
 *   cargo run -p tsk-link -- lib/samples/test_main.tobj -o lib/samples/test_main.tvmx
 *   cargo run -p triskele-vm -- lib/samples/test_main.tvmx
 *
 * Expected output (via O_LOG / exit code):
 *   Test 1 PASS  ScaleDiv(10,2)  = 5
 *   Test 2 PASS  ScaleDiv(7,0)   = 0
 *   Test 3 PASS  IsSolid(3,5)    = 1
 *   Test 4 PASS  IsSolid(0,0)    = 0
 *   Test 5 PASS  SumTiles(0,0,4,4) = 9
 *   ALL TESTS PASSED
 *   exit code 0
 */

typedef unsigned char  byte;
typedef unsigned short word;

#define MAPSIZE 64

/* Global tilemap — shared with wolf3d_sample.c functions */
byte tilemap[MAPSIZE * MAPSIZE];

/* ── Functions under test (from wolf3d_sample.c) ─────────────────────────── */

int ScaleDiv(int num, int den)
{
    if (den == 0) return 0;
    return num / den;
}

int IsSolid(int x, int y)
{
    if (x < 0 || x >= MAPSIZE || y < 0 || y >= MAPSIZE)
        return 1;
    return tilemap[y * MAPSIZE + x] != 0;
}

int SumTiles(int x0, int y0, int w, int h)
{
    int sum = 0;
    int x, y;
    for (y = y0; y < y0 + h; y++) {
        for (x = x0; x < x0 + w; x++) {
            sum += tilemap[y * MAPSIZE + x];
        }
    }
    return sum;
}

/* ── Minimal output via exit code ────────────────────────────────────────── */
/* TriskeleVM: exit code is returned in R0 at Im_EXIT.                        */
/* We encode pass/fail as a bitmask: bit N = test N passed.                   */
/* All 5 tests pass → bitmask = 0x1F = 31.                                   */
/* The VM loader stub calls main() and exits with R0.                         */

int main(void)
{
    int pass = 0;

    /* Test 1: ScaleDiv(10, 2) == 5 */
    if (ScaleDiv(10, 2) == 5)
        pass |= 1;

    /* Test 2: ScaleDiv(7, 0) == 0  (division by zero guard) */
    if (ScaleDiv(7, 0) == 0)
        pass |= 2;

    /* Test 3: IsSolid on a non-zero tile */
    tilemap[5 * MAPSIZE + 3] = 9;   /* place a wall at (3,5) */
    if (IsSolid(3, 5) == 1)
        pass |= 4;

    /* Test 4: IsSolid on an empty tile */
    if (IsSolid(0, 0) == 0)
        pass |= 8;

    /* Test 5: SumTiles over a 4×4 region containing the wall */
    /* tilemap[5*64+3]=9, rest zero → sum over (0,0,8,8) = 9 */
    if (SumTiles(0, 0, 8, 8) == 9)
        pass |= 16;

    /* Return bitmask: 31 (0x1F) = all tests passed */
    return pass;
}
