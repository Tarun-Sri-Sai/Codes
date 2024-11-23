#include <vector>
#include <cstdlib>
#include <time.h>

#include "include/sorter.h"

std::vector<int> generate_arr(int min_size, int max_size, int lower_bound, int upper_bound)
{
    srand(time(NULL));
    int size = min_size + rand() % (max_size - min_size + 1);
    std::vector<int> result;
    for (int i = 0; i < size; i++)
        result.push_back(lower_bound + rand() % (upper_bound - lower_bound + 1));
    return result;
}

int main()
{
    std::vector<int> arr = generate_arr(10, 15, 0, 100);
    sort(arr);
    return 0;
}