#include <cs50.h>
#include <stdio.h>
#include <string.h>

string cover_supper(string key);
bool is_alphabetic(string key);
bool each_letter_once(string str);

int main(int argc, string argv[])
{
    string key = argv[1];
    if (!key || argc > 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    else if (strlen(key) != 26 || !is_alphabetic(key))
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else if (!each_letter_once(key))
    {
        printf("Each letter must exactly once\n");
        return 1;
    }
    else
    {
        key = cover_supper(key);
        string text = get_string("plaintext: ");
        for (int i = 0, n = strlen(text); i < n; i++)
        {
            if ('A' <= text[i] && text[i] <= 'Z')
            {
                int index = text[i] - 'A';
                text[i] = key[index];
            }
            else if (('a' <= text[i] && text[i] <= 'z'))
            {
                int index = text[i] - 'a';
                text[i] = key[index] + 32;
            }
        }
        printf("ciphertext: %s\n", text);
        return 0;
    }
}
bool is_alphabetic(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (!('a' <= key[i] && key[i] <= 'z') && !('A' <= key[i] && key[i] <= 'Z'))
        {
            return false;
        }
    }
    return true;
}
bool each_letter_once(string str)
{
    string key = cover_supper(str);

    int characters[26];
    for (int i = 0; i < 26; i++)
    {
        characters[i] = 0;
    }

    for (int i = 0, n = strlen(key); i < n; i++)
    {
        int index = key[i] - 'A';
        if (characters[index] == 1)
        {
            return false;
        }
        else
        {
            characters[index] = 1;
        }
    }
    return true;
}
string cover_supper(string key)
{
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if ('a' <= key[i] && key[i] <= 'z')
        {
            key[i] -= 32;
        }
    }
    return key;
}