#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>
#include <stdint.h>
#include <assert.h>

#define byte uint8_t
#define MAX_STRING 0xFFFF
#define BYTE_SIZE 8

#define min(a, b) (a < b ? a : b)
#define abs_diff(x, y) (x > y ? x - y : y - x)
#define hyphens(x) (28 + x * 3)

byte *corrupt_string(byte *string, int length, int bits, int chance);
void print_string(byte *string, int length);
byte *copy_string(byte *string, int length);
char *make_string(char ch, int repetition);
void debug_corruption(byte *target, byte *source, int length);
bool is_corrupt(byte *target, byte *source, int length);
int get_prob(int probability);

int main(int argc, char **argv)
{
    byte *input, *corrupted;
    int input_length;

    if (argc != 4)
    {
        printf("Usage\t\t: %s\t\"<data string>\"\t<bits to corrupt>\t<corrupt chance>\n", argv[0]);
        printf("Example command\t: %s\t%s\t\t%d\t\t\t%d\n", argv[0], "Example", 4, 50);
        return EXIT_FAILURE;
    }

    srand(time(NULL));

    input = (byte *)argv[1];
    input_length = strnlen((char *)input, MAX_STRING);

    corrupted = corrupt_string(copy_string(input, input_length),
                               input_length, atoi(argv[2]), atoi(argv[3]));

    debug_corruption(corrupted, input, input_length);

    printf("\n%s\nChecksum result\t\t: ", make_string('-', hyphens(input_length)));
    if (is_corrupt(input, corrupted, input_length))
        printf("String is corrupted\n");
    else
        printf("String is not corrupted\n");
    return EXIT_SUCCESS;
}

byte *corrupt_string(byte *string, int length, int bits, int chance)
{
    int i;

    for (i = 0; i < bits; i++)
    {
        int index = rand() % length;
        int bit_pos = rand() % BYTE_SIZE;

        if (get_prob(chance) == 0)
        {
            continue;
        }

        string[index] ^= ((byte)1 << bit_pos);
    }
    return string;
}

void print_string(byte *string, int length)
{
    int i, i_max = min(length + 1, MAX_STRING) - 1;

    for (i = 0;; i++)
    {
        if (string[i] == 0)
            printf("..");
        else
            printf("%02X", string[i]);

        if (i == i_max)
            return;
        printf(" ");
    }
}

byte *copy_string(byte *string, int length)
{
    byte *result = (byte *)calloc(length + 1, sizeof(byte));

    memcpy_s(result, length + 1, string, length + 1);
    return result;
}

char *make_string(char ch, int repetition)
{
    char *result;

    if (repetition <= 0)
    {
        return "";
    }
    result = (char *)calloc(repetition + 1, sizeof (char));
    memset(result, ch, repetition * sizeof (char));

    result[repetition] = 0;
    return result;
}

void debug_corruption(byte *target, byte *source, int length)
{
    int i;
    byte *diff_string;
    
    printf("Before corruption\t: ");
    print_string(source, length);

    printf("\n\nAfter corruption\t: ");
    print_string(target, length);

    diff_string = (byte *)calloc(length, sizeof(byte));
    for (i = 0; i < length; i++)
    {
        byte diff = (byte)abs_diff(source[i], target[i]);
        
        diff_string[i] = diff;
    }

    printf("\n%s\nCorrupted parts\t\t: ", make_string('-', hyphens(length)));
    print_string(diff_string, length);
    printf("\n");
}

bool is_corrupt(byte *target, byte *source, int length)
{
    byte check_sum1 = (byte)0, check_sum2;
    int i;

    for (i = 0; i < length; i++)
    {
        check_sum1 += source[i];
    }
    check_sum1 = -check_sum1;

    check_sum2 = check_sum1;
    for (i = 0; i < length; i++)
    {
        check_sum2 += target[i];
    }

    return (check_sum2 != 0);
}

int get_prob(int probability)
{
    if (!(0 <= probability && probability <= 100)) {
        return 0;
    }
    return ((rand() % 100) < probability ? 1 : 0);
}