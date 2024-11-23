#include <iostream>
#include <utility>
#include <vector>
#include <algorithm>

int find(float arr[], int n, float ele)
{
    int low = 0;
    int high = n - 1;
    while (low <= high)
    {
        int mid = low + (high - low) / 2;
        if (arr[mid] == ele)
        {
            return mid;
        }
        if (arr[mid] < ele)
        {
            low = mid + 1;
        }
        else
        {
            high = mid - 1;
        }
    }
    return 0;
}

int main()
{
    int n;
    std::cout << "No. of entries: ";
    std::cin >> n;
    std::cout << "Enter entries:\n";
    float arr[n];
    for (int i = 0; i < n; i++)
    {
        std::cout << i + 1 << "\t";
        std::cin >> arr[i];
    }
    float copyarr[n];
    std::copy(arr, arr + n, copyarr);
    std::sort(arr, arr + n);
    std::cout << std::endl;
    std::cout << "S.No.\t\t"
              << "Data\t\t"
              << "Rank" << std::endl;
    for (int i = 0; i < 40; i++)
    {
        std::cout << "-";
    }
    std::cout << "-\n";
    for (int i = 0; i < n; i++)
    {
        float ele = copyarr[i];
        std::cout << i + 1 << "\t\t" << ele << "\t\t" << n - find(arr, n, ele) << std::endl;
    }
    return 0;
}