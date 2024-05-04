//  Clear terminal with print
#include <stdio.h>
#include <Windows.h>
#define MAX_COUNT (int)1e6
#define NO_OF_INITIAL_ROWS 4
#define NO_OF_INITIAL_COLS 100
#define NO_OF_ROWS 20
#define NO_OF_COLS 12

int main(void)
{
    int count = 0, i, j;
    printf("\x1b[d");
    for (i = 0; i < NO_OF_INITIAL_ROWS; i++)
    {
        for (j = 0; j < NO_OF_INITIAL_COLS; j++)
        {
            printf(" ");
        }
    }
    while (count++ < MAX_COUNT)
    {
        printf("\x1b[d"); //  Used to send cursor to start of terminal
        for (i = 0; i < NO_OF_ROWS; i++)
        {
            for (j = 0; j < NO_OF_COLS; j++)
            {
                if (count % 2 == 0)
                {
                    printf("....");
                }
                else
                {
                    printf("    ");
                }
                Sleep(1);
            }
            printf("\n");
        }
    }
    return 0;
}