#ifndef DYN_STR_H
#define DYN_STR_H

typedef struct String_struct
{
    char *val;
    int length, capacity;
} String;

String *init(char *val);
String *new_string();
void append(String *source, char *appendix);
void extend(String *source, String *extension);
void delete_string(String **source_ptr);
void debug_print(String *source);
void push_back(String *source, char appendix);
void pop_back(String **source_ptr);
const char *to_string(String *source);
int length(String *source);
void nappend(String *source, char *appendix, int max_size);
void nextend(String *source, String *extension, int max_size);
int min(int a, int b);

#endif