#include <iostream>

int main()
{
    long long number = 0;
    for (int i = 0; i < (int)1e8; i++)
    {
        number += i;
    }
    std::cout << number << '\r';
}