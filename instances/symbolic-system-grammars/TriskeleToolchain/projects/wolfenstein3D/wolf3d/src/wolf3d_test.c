/* projects/wolf3d/src/wolf3d_test.c
   Author: Echopraxium with the collaboration of Claude AI
   Test harness — exit bitmask (15 = all 4 passed). */
#include "wolf3d.h"

int main(void) {
    int result = 0;

    /* Test 1: ScaleDiv(10,2) == 5 */
    if (ScaleDiv(10, 2) == 5)
        result |= 1;

    /* Test 2: IsSolid(0,0) == 0 */
    if (IsSolid(0, 0) == 0)
        result |= 2;

    /* Test 3: MoveActor — fixed-point 16.16 */
    {
        actor_t a;
        a.x     = 10 << 16;   /* 655360 */
        a.y     = 20 << 16;   /* 1310720 */
        a.angle = 0;
        MoveActor(&a, 5, 3);
        if (((int)(a.x >> 16) == 15) && ((int)(a.y >> 16) == 23))
            result |= 4;
    }

    /* Test 4: SumTiles(0,0,8,8) == 0 */
    if (SumTiles(0, 0, 8, 8) == 0)
        result |= 8;

    return result;
}
