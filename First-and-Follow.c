#include <stdio.h>
#include <string.h>
#include <ctype.h>

int n, y;
char a[100][100], f[100];

void follow(char c);
void first(char c);

int main()
{
    int nt, i, j, x;
    char t[100];

    printf("Enter no. of terminals: ");
    scanf("%d", &nt);
    printf("Enter the terminals:\n");
    scanf("%s", t);
    printf("Enter no. of productions: ");
    scanf("%d", &n);
    printf("Enter the productions:\n");
    for (i = 0; i < n; i++)
        scanf("%s", a[i]);
    printf("\nYour productions:\n");
    for (i = 0; i < n; i++)
        printf("%s\n", a[i]);
    for (i = 0; i < nt; i++)
        printf("\t%c", t[i]);
    printf("\n");
    for (i = 0; i < n; i++)
    {
        if (islower(a[i][2]) && a[i][2] != 'e')
        {
            x = 0;
            printf("%c\t", a[i][0]);
            while (a[i][2] != t[x++])
                printf("\t");
            printf("%c=%s\n", a[i][0], a[i] + 2);
        }
        if (isupper(a[i][2]))
        {
            y = 0;
            first(a[i][2]);
            for (j = 0; j < y; j++)
            {
                if (f[j] == 'e')
                {
                    for (x = 0; x < y; x++)
                        f[y] = '\0';
                    y = 0;
                    follow(a[i][0]);
                }
            }
            printf("%c\t", a[i][0]);
            for (j = 0; j < y; j++)
            {
                x = 0;
                while (f[j] != t[x++])
                    printf("\t");
                printf("%c=%s\t", a[i][0], a[i] + 2);
            }
            continue;
        }
        if (a[i][2] == 'e')
        {
            y = 0;
            follow(a[i][0]);
            printf("%c\t", a[i][0]);
            for (j = 0; j < y; j++)
            {
                x = 0;
                while (f[j] != t[x++])
                    printf("\t");
                printf("%c=e", a[i][0]);
            }
            printf("\n");
            continue;
        }
    }
    return 0;
}

void follow(char c)
{
    int i, j;
    if (a[0][0] == c)
        f[y++] = '$';
    for (i = 0; i < n; i++)
    {
        for (j = 0; j < strlen(a[i]); j++)
        {
            if (a[i][j] == c)
            {
                if (a[i][j + 1] != '\0')
                    first(a[i][j + 1]);
                if (a[i][j + 1] == '\0' && c != a[i][0])
                    follow(a[i][0]);
            }
        }
    }
}

void first(char c)
{
    int i;
    if (!isupper(c))
        f[y++] = c;
    for (i = 0; i < n; i++)
    {
        if (a[i][0] == c)
        {
            if (a[i][2] == 'e')
                follow(a[i][0]);
            else if (islower(a[i][2]))
                f[y++] = a[i][2];
            else
                first(a[i][2]);
        }
    }
}