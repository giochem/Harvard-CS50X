#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

const int BITS_IN_BYTE = 8;

void print_bulb(int bit);

int main(void)
{
    // TODO
    string message = get_string("Mesage: ");

    for (int i = 0, n = strlen(message); i < n; i++)
    {
        int digit = (int) message[i];
        // dawn col
        for (int j = BITS_IN_BYTE; j >= 1; j--)
        {
            int pow_to_2 = (int) pow(2, j - 1);
            
            if (digit - pow_to_2 >= 0)
            {
                print_bulb(1);
                digit -= pow_to_2;
            }
            else
            {
                print_bulb(0);
            }
        }
        printf("\n");
    }
}

void print_bulb(int bit)
{
    if (bit == 0)
    {
        // Dark emoji
        printf("\U000026AB");
    }
    else if (bit == 1)
    {
        // Light emoji
        printf("\U0001F7E1");
    }
}
