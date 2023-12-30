//  Knapsack 01
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define MAX_SIZE 0x100

typedef struct
{
    int id;
    int profit;
    int weight;
} Item;

int max(int a, int b)
{
    return a > b ? a : b;
}

int find_value(int dp[][MAX_SIZE], Item *item, int capacity)
{
    if (capacity - item->weight < 0)
    {
        return dp[item->id - 1][capacity];
    }
    int not_choose = dp[item->id - 1][capacity];
    int choose = dp[item->id - 1][capacity - item->weight] + item->profit;
    return max(not_choose, choose);
}

int knapsack(Item *items[], int n, int capacity)
{
    int profit = 0;
    int dp[MAX_SIZE][MAX_SIZE];
    int j;
    for (j = 0; j <= capacity; j++)
    {
        dp[0][j] = 0;
    }
    int i;
    for (i = 0; i < n; i++)
    {
        Item *item = items[i];
        for (j = 0; j <= capacity; j++)
        {
            dp[item->id][j] = find_value(dp, item, j);
        }
    }
    return dp[items[i - 1]->id][capacity];
}

void print(Item *items[], int n)
{
    int i;
    for (i = 0; i < n; i++)
    {
        printf("\tID: %d\tProfit: %d\tWeight: %d\n", items[i]->id, items[i]->profit, items[i]->weight);
    }
}

int main()
{
    srand(time(NULL));
    int n = 3 + rand() % 3;
    printf("Size: %d\n", n);
    Item *items[MAX_SIZE];
    int i;
    printf("Items:\n");
    for (i = 0; i < n; i++)
    {
        items[i] = (Item *)malloc(sizeof(Item *));
        items[i]->id = i + 1;
        items[i]->profit = 1 + rand() % 10;
        items[i]->weight = 1 + rand() % 10;
    }
    print(items, n);
    int capacity = 10 + rand() % (10 * (n - 2));
    printf("Capacity: %d\n", capacity);
    int profit = knapsack(items, n, capacity);
    printf("Profit: %d\n", profit);
    return 0;
}