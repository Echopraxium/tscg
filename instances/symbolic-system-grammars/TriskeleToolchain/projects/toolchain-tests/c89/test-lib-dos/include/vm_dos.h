#ifndef VM_DOS_H
#define VM_DOS_H

void sound(unsigned frequency);
void nosound(void);
void delay(unsigned milliseconds);
int kbhit(void);
int getch(void);
void intr(int intno, void *regs);
void set_video_mode(int mode);

// printf est déjà dans tsk-libc
int printf(const char *fmt, ...);

#endif