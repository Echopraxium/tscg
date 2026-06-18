/* projects/wolf3d/include/wolf3d.h
   Author: Echopraxium with the collaboration of Claude AI
   Common types and declarations for Wolf3D sample.
   Must match wolf3d_sample.c exactly. */

#ifndef WOLF3D_H
#define WOLF3D_H

typedef unsigned char  byte;
typedef unsigned short word;
typedef unsigned long  longword;

#define MAPSIZE 64

/* actor_t: x,y are fixed-point 16.16 (long), angle is integer */
typedef struct {
    long x, y;   /* fixed 16.16 */
    int  angle;
} actor_t;

int  ScaleDiv(int num, int denom);
int  IsSolid(int x, int y);
void MoveActor(actor_t *actor, int dx, int dy);
int  SumTiles(int x0, int y0, int w, int h);

#endif /* WOLF3D_H */
