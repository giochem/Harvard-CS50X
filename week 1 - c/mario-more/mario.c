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
        for (int j = 1; j <= height * 2 + 2; j++)
        {
            // after end # of row
            if (j > i + height + 2)
            {
                break;
            }
            // draw col
            if ((j <= height && i > height - j) || (j >= height + 3 && j <= i + height + 2))
            {
                printf("#");
            }
            else
            {
                // space
                printf(" ");
            }
        }
        printf("\n");
    }
}