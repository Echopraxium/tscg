/* Extrait représentatif de Wolf3D C89 */
typedef unsigned char  byte;
typedef unsigned short word;
typedef unsigned long  longword;

#define MAPSIZE 64

byte tilemap[MAPSIZE * MAPSIZE];

typedef struct {
    long x, y;       /* fixed 16.16 */
    int  angle;
} actor_t;

/* Extrait de wl_draw.c — calcul de hauteur de mur */
int ScaleDiv(int num, int den)
{
    if (den == 0) return 0;
    return num / den;
}

/* Extrait de wl_game.c — test de mur */
int IsSolid(int x, int y)
{
    if (x < 0 || x >= MAPSIZE || y < 0 || y >= MAPSIZE)
        return 1;
    return tilemap[y * MAPSIZE + x] != 0;
}

/* Extrait de wl_act1.c — déplacement actor */
void MoveActor(actor_t *actor, int dx, int dy)
{
    int nx = (int)(actor->x >> 16) + dx;
    int ny = (int)(actor->y >> 16) + dy;
    if (!IsSolid(nx, (int)(actor->y >> 16)))
        actor->x += (long)dx << 16;
    if (!IsSolid((int)(actor->x >> 16), ny))
        actor->y += (long)dy << 16;
}

/* Accumulateur simple — test D_Add / boucle */
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
