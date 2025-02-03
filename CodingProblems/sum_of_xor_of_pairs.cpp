#include <bits/stdc++.h>
#define ll long long

using namespace std;

bool checkBit(int ele, int pos)
{
    return (((ele >> pos) & 1) == 1);
}

ll sumOfXor(int A[], int N)
{
    ll sum = 0;
    for (int i = 0; i < 31; i++)
    {
        ll c0 = 0, c1 = 0;
        for (int j = 0; j < N; j++)
        {
            if (checkBit(A[j], i))
            {
                c1++;
            }
            else
            {
                c0++;
            }
        }
        sum += (c1 * c0 * (1L << i));
    }
    return (sum * 2);
}

int main()
{
    int T;
    cin >> T;
    while (T-- > 0)
    {
        int N;
        cin >> N;
        int A[N];
        for (int i = 0; i < N; i++)
        {
            cin >> A[i];
        }
        cout << sumOfXor(A, N) << '\n';
    }
    return 0;
}
