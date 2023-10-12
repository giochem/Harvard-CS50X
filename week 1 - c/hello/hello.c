#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get name of user
    string name = get_string("What's your name? ");
    // print
    printf("hello, %s\n", name);
}