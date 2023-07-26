#include <bits/stdc++.h>
using namespace std;

/**
 * Assume number=7
 * 
 * Bit representations from 1 to 6 will be:
 * 
 *              1 -> 0 0 0 1
 *              2 -> 0 0 1 0
 *              3 -> 0 0 1 1
 *              4 -> 0 1 0 0
 *              5 -> 0 1 0 1
 *              6 -> 0 1 1 0
 * 
 * We see that, after every 2 ^ i iterations, where i is 0-based bit position,
 * the bit flips. And only half of the bits in some n complete cycles count.
 * 
 * So, we count the number of total cycles in the numbers 1 to number-1, and
 * if the count is odd, it means that there is one incomplete cycle in the list.
 * Conveniently, the number of 1's at the end of this incomplete cycle are equal
 * to the length of the incomplete cycle.
*/
int count_total_set_bits(int number)
{
    // 1 to (< 1)(exclusive) is not a valid range
    if (number <= 1)
    {
        return 0;
    }

    // Stores the number of set bits for each bit position
    int total_set_bits = 0;
    for (int i = 0; i < 32; i++)
    {
        // The iterations taken to flip a bit
        int cycle = (int)(1LL << i);

        // The number of cycles in the current number(exclusive)
        int cycle_count = number / cycle;

        // If cycle count is odd, that means there are 1's in the ending that should be added
        if (cycle_count % 2 != 0)
        {  
            // Remaining numbers after cycle_count cycles, which are all 1
            total_set_bits += (number % cycle);
        }

        // Only exclusive half of these cycles contribute to the number of 1's
        total_set_bits += (((cycle_count / 2) * cycle));
    }
    return total_set_bits;
}

int main()
{
    int n;
    cin >> n;

    // The function calculates total set bits from 1 to n(exclusive), so input is incremented by 1
    cout << count_total_set_bits(n + 1) << '\n';
    return 0;
}