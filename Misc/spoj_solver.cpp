#include <iostream>
#define ld long double

ld sp_points(int n)
{
    if (n == 0)
    {
        return 2;
    }
    return (ld)80 / (ld)(40 + n);
}

void solve()
{
    std::cout << "How many problems did you solve? ";
    int cs;
    std::cin >> cs;
    ld sum = 0;
    std::cout << "\nProblem No.\tSubmissions\n";
    for (int t = 0; t < cs; t++)
    {
        std::cout << t + 1 << "\t\t";
        int n;
        std::cin >> n;
        sum += sp_points(n);
    }
    std::cout << "\nSP points:\t" << sum << std::endl;
}

int main()
{
    solve();
    return 0;
}