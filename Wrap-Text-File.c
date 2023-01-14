#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define buffer_t unsigned short int
#define count_t unsigned long int

count_t wrap_text_file(FILE *input, buffer_t MAX_LINE_SIZE);

int main()
{
    FILE *input = fopen("Text-Files/Input.txt", "r");
    if (!input)
    {
        return 0;
    }
    count_t word_count = wrap_text_file(input, 0);
    printf("\nThere are %d words\n", word_count);

    fclose(input);
    return 0;
}

count_t wrap_text_file(FILE *input, buffer_t MAX_LINE_SIZE)
{
    if (MAX_LINE_SIZE < 0x5F)
    {
        MAX_LINE_SIZE = 0x5F;
    }
    count_t word_count = 0;
    char *last_word[MAX_LINE_SIZE];
    buffer_t length = 0;
    while (fscanf(input, "%s", last_word) == 1)
    {
        ++word_count;
        buffer_t curr_len = strlen(last_word);
        if (length + (curr_len + 1) > MAX_LINE_SIZE)
        {
            printf("\n");
            length = (curr_len + 1);
            printf("%s ", last_word);
        }
        else
        {
            length += (curr_len + 1);
            printf("%s ", last_word);
        }
    }
    printf("\n");
    return word_count;
}