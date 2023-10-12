#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
bool is_number(string nums);

int main(int argc, string argv[])
{
    string key = argv[1];
    if (!key || argc > 2 || is_number(key) == false)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    else
    {

        int num = atoi(key);
        if (num >= 26)
        {
            num = num % 26;
        }

        string plaintext = get_string("plaintext: ");
        for (int i = 0, n = strlen(plaintext); i < n; i++)
        {
            if (islower(plaintext[i]) || isupper(plaintext[i]))
            {
                if (plaintext[i] + num > 'Z' && plaintext[i] <= 'Z')
                {
                    int digit = plaintext[i] + num - 'Z' - 1;
                    plaintext[i] = 'A' + digit;
                }
                else if (plaintext[i] + num > 'z')
                {

                    int digit = plaintext[i] + num - 'z' - 1;
                    plaintext[i] = 'a' + digit;
                }
                else
                {
                    plaintext[i] = plaintext[i] + num;
                }
            }
        }
        printf("ciphertext: %s\n", plaintext);
        return 0;
    }
}
bool is_number(string nums)
{
    for (int i = 0, n = strlen(nums); i < n; i++)
    {
        if (nums[i] < '0' || nums[i] > '9')
        {
            return false;
        }
    }
    return true;
}