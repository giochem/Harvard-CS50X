#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    // check value
    while (height < 1 || height > 8);
    for (int i = 1; i <= height; i++)
    {
        // draw row
        for (int j = 1; j <= height; j++)
        {
            // draw col
            if (i > height - j)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}