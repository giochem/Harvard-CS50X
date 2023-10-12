#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("cannot opened for reading %s\n", argv[1]);
        return 1;
    }
    FILE *out = NULL;
    BYTE buff[512];

    int count = 0;

    char name[8] = {0};
    while (fread(buff, sizeof(BYTE) * 512, 1, file) == 1)
    {
        if (buff[0] == 0xFF && buff[1] == 0xD8 && buff[2] == 0xFF && (buff[3] & 0xF0) == 0xE0)
        {
            if (out != NULL)
            {
                fclose(out);
            }
            sprintf(name, "%03d.jpg", count++);
            out = fopen(name, "w");
        }
        if (out != NULL)
        {
            fwrite(buff, sizeof(BYTE) * 512, 1, out);
        }
    }
    if (out != NULL)
    {
        fclose(out);
    }
    fclose(file);
}