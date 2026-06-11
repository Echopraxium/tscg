#include "vm_dos.h"

int main() {
    // Test son
    sound(440);   // La VM doit interpréter le syscall 0x80
    delay(500);
    nosound();

    // while (!kbhit()) delay(100);   // ← commentez cette ligne

    int ch = getch();
    printf("Touche pressée: %d\n", ch);

    return 0;
}