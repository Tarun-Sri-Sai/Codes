#ifndef DYN_STR_H
#define DYN_STR_H

typedef struct String_struct
{
    char *val;
    int length, capacity;
} String;

String *init(char *val);
String *new_string();
void string_append(String *source, char *appendix);
void string_extend(String *source, String *extension);
void delete_string(String **source_ptr);
void string_debug_print(String *source);
void string_push_back(String *source, char appendix);
void string_pop_back(String **source_ptr);
const char *string_value_of(String *source);
int string_length(String *source);
void string_nappend(String *source, char *appendix, int max_size);
void string_nextend(String *source, String *extension, int max_size);
static int min(int a, int b);

#endif