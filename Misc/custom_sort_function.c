//  Implementation of Library sort function in C
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#define MAX_SIZE 100

void quick_sort(int *arr, int low, int high);
int partition(int *arr, int low, int high);
void swap(int *n1, int *n2);
void sort(int *start, int *end);
int check(int *start, int *end);
int bounded_rand(int lb, int ub);

int main()
{
    int n, i, arr[MAX_SIZE];
    srand(time(NULL));
    n = bounded_rand(1, 10);
    for (i = 0; i < n; i++)
    {
        arr[i] = bounded_rand(0, 100);
    }
    sort(arr, arr + n);
    if (check(arr, arr + n))
        printf("Sorted: [");
    else
        printf("Not Sorted: [");
    for (int i = 0; i < n; i++)
    {
        printf("%d%s", arr[i], (i == n - 1 ? "]\n" : ", "));
    }
    return 0;
}

int check(int *start, int *end)
{
    int *arr = start, n = end - start;
    for (int i = 0; i < n - 1; i++)
        if (arr[i] > arr[i + 1])
            return 0;
    return 1;
}

void sort(int *start, int *end)
{
    quick_sort(start, 0, (end - start) - 1);
}

int bounded_rand(int lb, int ub) {
    return lb + rand() % (ub - lb + 1);
}

void quick_sort(int *arr, int low, int high) {
    if (low >= high) {
        return;
    }
    int middle = partition(arr, low, high);
    quick_sort(arr, low, middle - 1);
    quick_sort(arr, middle + 1, high);
}

int partition(int *arr, int low, int high) {
    int i = low - 1, j;
    for (j = low; j < high; ++j) {
        if (arr[j] < arr[high]) {
            swap(&arr[++i], &arr[j]);
        }
    }
    swap(&arr[++i], &arr[high]);
    return i;
}

void swap(int *n1, int *n2) {
    int temp = *n1;
    *n1 = *n2;
    *n2 = temp;
}

int bounded_rand(int lb, int ub) {
    return lb + rand() % (ub - lb + 1);
}