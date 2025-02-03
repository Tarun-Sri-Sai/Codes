#include "wrap_text_file.h"

int wrap_text_file(FILE *input, int max_line_size, FILE *output)
{
    if (max_line_size < 0x40)
    {
        max_line_size = 0x40;
    }
    int word_count = 0;
    char last_word[max_line_size];
    int length = 0;
    while (fscanf(input, "%s", last_word) == 1)
    {
        ++word_count;
        int curr_len = strnlen_s(last_word, MAX_STRING);
        if (length + (curr_len + 1) > max_line_size)
        {
            fprintf(output, "\n");
            length = (curr_len + 1);
            fprintf(output, "%s ", last_word);
        }
        else
        {
            length += (curr_len + 1);
            fprintf(output, "%s ", last_word);
        }
    }
    fprintf(output, "\n");
    return word_count;
}
