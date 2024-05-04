#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

size_t len = 0;

void randomise(int arr[])
{
    if (len == 0)
    {
        return;
    }
    int i = rand() % len, j = rand() % len;
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

void show(int arr[])
{
    if (len == 0)
    {
        return;
    }
    for (size_t i = 0; i < len; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

bool sorted(int arr[])
{
    for (size_t i = 0; i < len - 1; i++)
    {
        if (arr[i] > arr[i + 1])
        {
            return false;
        }
    }
    return true;
}

void bogo_sort(int arr[])
{
    if (len == 0)
    {
        return;
    }
    int count = 0;
    while (!sorted(arr))
    {
        randomise(arr);
        count++;
        if (count > 1000)
        {
            printf("Yeah no not happening brother :(\n");
            return;
        }
    }
    printf("Shit this somehow sorted it after %d tries :O\n", count);
}

int main(void)
{
    int arr[10];
    scanf("%zu", &len);
    if (len > 0 && len < 11)
    {
        for (size_t i = 0; i < len; i++)
        {
            scanf("%d", &arr[i]);
        }
        bogo_sort(arr);
        show(arr);
    }
    return 0;
}