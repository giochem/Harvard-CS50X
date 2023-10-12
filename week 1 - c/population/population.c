#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int startsize;
    do
    {
        startsize = get_int("Start size: ");
    }
    while (startsize < 9);
    // TODO: Prompt for end size
    int endsize;
    do
    {
        endsize = get_int("End size: ");
    }
    while (endsize < startsize);
    // TODO: Calculate number of years until we reach threshold
    int num = 0;
    while (startsize < endsize)
    {
        startsize = startsize + startsize / 3 - startsize / 4;
        num = num + 1;
    }
    // TODO: Print number of years
    printf("Years: %i\n", num);
}
