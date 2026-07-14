int printf(const char *fmt, ...);
char *fgets(char *buf, int size, void *stream);

static char buf[256];

int main() {
    printf("Ton nom ? ");
    fgets(buf, 256, (void*)0);
    printf("Bonjour, %s", buf);
    return 0;
}