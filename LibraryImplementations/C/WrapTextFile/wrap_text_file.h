#ifndef WRAP_TEXT_FILE_H
#define WRAP_TEXT_FILE_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_STRING 0xFFFF

int wrap_text_file(FILE *input, int max_line_size, FILE *output);

#endif
