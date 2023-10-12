#include <cs50.h>
#include <stdio.h>
#include <string.h>

bool luhn_algorithm(char arr[]);

int main(void)
{
    long nums;
    do
    {
        nums = get_long("Number: ");
    }
    while (nums < 0);

    char str[256];
    sprintf(str, "%ld", nums);

    int length = strlen(str);

    if (length == 15 && str[0] == '3' && (str[1] == '4' || str[1] == '7'))
    {
        if (luhn_algorithm(str))
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if (length == 16 && str[0] == '5' && (str[1] == '1' || str[1] == '2' || str[1] == '3' || str[1] == '4' || str[1] == '5'))
    {
        if (luhn_algorithm(str))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else if ((length == 13 || length == 16) && str[0] == '4')
    {
        if (luhn_algorithm(str))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
bool luhn_algorithm(char str[])
{
    int sum_second_to_last = 0;
    for (int i = strlen(str) - 2; i >= 0; i -= 2)
    {
        int digit = str[i] - '0';
        if (digit <= 4)
        {
            sum_second_to_last += digit * 2;
        }
        else
        {
            sum_second_to_last += (digit - 5) * 2 + 1;
        }
    }

    int sum_one_to_last = 0;
    for (int i = strlen(str) - 1; i >= 0; i -= 2)
    {
        int digit = str[i] - '0';
        sum_one_to_last += digit;
    }

    int sum_all = sum_one_to_last + sum_second_to_last;

    if (sum_all % 10 == 0)
    {
        return true;
    }
    return false;
}