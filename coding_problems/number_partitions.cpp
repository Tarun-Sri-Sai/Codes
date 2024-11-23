#include <bits/stdc++.h>

using namespace std;

int numPart(int N, int K)
{
    if (N == 0)
    {
        return 1;
    }
    if (N < 0)
    {
        return 0;
    }
    if (K == 0)
    {
        return 0;
    }
    return numPart(N - K, K) + numPart(N, K - 1);
}

int main(void)
{
    int T;
    cin >> T;
    while (T-- > 0)
    {
        int N, K;
        cin >> N >> K;
        cout << numPart(N, K) << '\n';
    }
    return 0;
}