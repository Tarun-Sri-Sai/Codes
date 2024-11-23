#include <vector>
#include <iostream>
#include <time.h>

#include "../include/sorter.h"

#define UNDERLINE_OPEN "\033[4m"
#define UNDERLINE_CLOSE "\033[0m"

void swap(std::vector<int> &arr, int i, int j)
{
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

int partition(std::vector<int> &arr, int low, int high, int rand_index)
{
    int i = low;
    swap(arr, high, rand_index);
    for (int j = low; j < high; j++)
        if (arr[j] <= arr[high])
            swap(arr, i++, j);
    swap(arr, i, high);
    return i;
}

void print_marked_arr(const std::vector<int> &arr, int underline, int open, int close)
{
    int i_max = arr.size() - 1;
    std::cout << '[';
    for (int i = 0;; i++)
    {
        if (i == open)
            std::cout << '(';
        if (i == underline)
            std::cout << UNDERLINE_OPEN << arr[i] << UNDERLINE_CLOSE;
        else
            std::cout << arr[i];
        if (i == close)
            std::cout << ')';
        if (i == i_max)
        {
            std::cout << "]\n";
            return;
        }
        std::cout << ", ";
    }
}

void print_arr(const std::vector<int> &arr)
{
    int i_max = arr.size() - 1;
    std::cout << '[';
    for (int i = 0;; i++)
    {
        std::cout << arr[i];
        if (i == i_max)
        {
            std::cout << "]\n";
            return;
        }
        std::cout << ", ";
    }
}

void quick_sort(std::vector<int> &arr, int low, int high, bool print_iters)
{
    if (low >= high)
        return;
    int rand_index = low + rand() % (high - low + 1);
    int pivot = partition(arr, low, high, rand_index);
    if (print_iters)
        print_marked_arr(arr, pivot, low, high);
    else
        print_arr(arr);
    quick_sort(arr, low, pivot - 1, print_iters);
    quick_sort(arr, pivot + 1, high, print_iters);
}

void sort(std::vector<int> &arr, bool print_iters)
{
    srand(time(NULL));
    quick_sort(arr, 0, arr.size() - 1, print_iters);
}