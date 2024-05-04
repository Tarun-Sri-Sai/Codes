#include <stdio.h>
#include <stdlib.h>
#include <unordered_set>
#include <fstream>
#include <time.h>
#define ll long long
#define MAX_SIZE 100
using std::ofstream;
using std::unordered_set;

unordered_set<ll> addresses_with_free;
int insert_count_with_free = 0;
unordered_set<ll> addresses_without_free;
int address_count_without_free = 0;

int test_cases()
{
    ofstream fout("Text Files/Input.txt");
    srand(time(NULL));
    int t = MAX_SIZE;
    fout << t << '\n';
    while (t-- > 0)
    {
        int n = MAX_SIZE;
        int s = rand() % 1001;
        fout << n << ' ' << s << '\n';
        for (int i = 0; i < n; i++)
        {
            fout << rand() % 1001 << ' ';
        }
        fout << '\n';
    }
    fout.close();
    return 0;
}

bool subset_sum_with_free(int *arr, int n, int s)
{
    bool **dp = (bool **)calloc(n + 1, sizeof(bool *));
    ll temp = (ll)dp;
    addresses_with_free.insert(temp);
    insert_count_with_free++;
    int i;
    for (i = 0; i < n + 1; i++)
    {
        dp[i] = (bool *)calloc(s + 1, sizeof(bool));
        ll temp1 = (ll)dp[i];
        addresses_with_free.insert(temp1);
        insert_count_with_free++;
    }
    for (i = 0; i < n + 1; i++)
    {
        dp[i][0] = true;
    }
    for (i = 1; i < s + 1; i++)
    {
        dp[0][i] = false;
    }
    int j;
    for (i = 1; i < n + 1; i++)
    {
        for (j = 1; j < s + 1; j++)
        {
            if (j < arr[i - 1])
            {
                dp[i][j] = dp[i - 1][j];
                continue;
            }
            dp[i][j] = dp[i - 1][j] || dp[i - 1][j - arr[i - 1]];
        }
    }
    bool result = dp[n][s];
    for (i = 0; i < n + 1; i++)
    {
        free(dp[i]);
    }
    free(dp);
    return result;
}

bool subset_sum_without_free(int *arr, int n, int s)
{
    bool **dp = (bool **)calloc(n + 1, sizeof(bool *));
    ll temp = (ll)dp;
    addresses_without_free.insert(temp);
    address_count_without_free++;
    int i;
    for (i = 0; i < n + 1; i++)
    {
        dp[i] = (bool *)calloc(s + 1, sizeof(bool));
        ll temp1 = (ll)dp[i];
        addresses_without_free.insert(temp1);
        address_count_without_free++;
    }
    for (i = 0; i < n + 1; i++)
    {
        dp[i][0] = true;
    }
    for (i = 1; i < s + 1; i++)
    {
        dp[0][i] = false;
    }
    int j;
    for (i = 1; i < n + 1; i++)
    {
        for (j = 1; j < s + 1; j++)
        {
            if (j < arr[i - 1])
            {
                dp[i][j] = dp[i - 1][j];
                continue;
            }
            dp[i][j] = dp[i - 1][j] || dp[i - 1][j - arr[i - 1]];
        }
    }
    bool result = dp[n][s];
    return result;
}

int with_free()
{
    FILE *fin;
    fin = fopen("Text Files/Input.txt", "r");
    int t;
    fscanf(fin, "%d", &t);
    while (t-- > 0)
    {
        int n, s;
        fscanf(fin, "%d %d", &n, &s);
        int *arr = (int *)calloc(n, sizeof(int));
        ll temp = (ll)arr;
        addresses_with_free.insert(temp);
        insert_count_with_free++;
        int i;
        for (i = 0; i < n; i++)
        {
            fscanf(fin, "%d", &arr[i]);
        }
        bool result = subset_sum_with_free(arr, n, s);
        // printf("%s\n", (result ? "YES" : "NO") );
        free(arr);
    }
    fclose(fin);
    printf("With free(): %d allocations, %zu addresses\n", insert_count_with_free, addresses_with_free.size());
    return 0;
}

int without_free()
{
    FILE *fin;
    fin = fopen("Text Files/Input.txt", "r");
    int t;
    fscanf(fin, "%d", &t);
    while (t-- > 0)
    {
        int n, s;
        fscanf(fin, "%d %d", &n, &s);
        int *arr = (int *)calloc(n, sizeof(int));
        ll temp = (ll)arr;
        addresses_without_free.insert(temp);
        address_count_without_free++;
        int i;
        for (i = 0; i < n; i++)
        {
            fscanf(fin, "%d", &arr[i]);
        }
        bool result = subset_sum_without_free(arr, n, s);
        // printf("%s\n", (result ? "YES" : "NO") );
    }
    fclose(fin);
    printf("Without free(): %d allocations, %zu addresses\n", address_count_without_free, addresses_without_free.size());
    return 0;
}

int main()
{
    int result = test_cases();
    result += with_free();
    result += without_free();
    return result;
}