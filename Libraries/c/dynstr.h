#ifndef DYN_STR_H
#define DYN_STR_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_STRING 0xFFFF

typedef struct String_tag
{
    char *val;
    int length, capacity;
} String;

String *init(char *val);
String *create();
void append(String **source, char *appendix);
void extend(String **source, String **extension);
void discard(String **source);
void debug_print(String **source);
void push_back(String **source, char appendix);
void pop_back(String **source);
const char *to_string(String **source);
int length(String **source);
void nappend(String **source, char *appendix, int max_size);
void nextend(String **source, String **extension, int max_size);
int min(int a, int b);

String *init(char *val)
{
    String *retval = create();
    append(&retval, val);
    return retval;
}

String *create()
{
    String *retval = (String *)malloc(sizeof(String *));
    retval->capacity = 2;
    retval->length = 0;
    retval->val = (char *)calloc(retval->capacity + 1, sizeof(char));
    retval->val[retval->length] = '\0';
    return retval;
}

void append(String **source, char *appendix)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    int i, length = strnlen(appendix, MAX_STRING);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)(*source)->length / (*source)->capacity > 0.75)
        {
            (*source)->capacity *= 2;
            (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
        }
        (*source)->val[(*source)->length++] = t;
    }
    (*source)->val[(*source)->length] = '\0';
}

void extend(String **source, String **extension)
{
    if ((*source) == ((String *)0) || (*extension) == ((String *)0))
    {
        return;
    }
    int i, length = (*extension)->length;
    for (i = 0; i < length; ++i)
    {
        char t = (*extension)->val[i];
        if ((float)(*source)->length / (*source)->capacity > 0.75)
        {
            (*source)->capacity *= 2;
            (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
        }
        (*source)->val[(*source)->length++] = t;
    }
    (*source)->val[(*source)->length] = '\0';
}

void discard(String **source)
{
    if (*source == ((String *)0))
    {
        return;
    }
    free((*source)->val);
    free(*source);
    *source = ((String *)0);
}

void debug_print(String **source)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    printf("Length: %d\nCapacity: %d\nString: %s\n", (*source)->length, (*source)->capacity, (*source)->val);
}

void push_back(String **source, char appendix)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    if (appendix == '\0')
    {
        return;
    }
    if ((float)(*source)->length / (*source)->capacity > 0.75)
    {
        (*source)->capacity *= 2;
        (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
    }
    (*source)->val[(*source)->length++] = appendix;
    (*source)->val[(*source)->length] = '\0';
}

void pop_back(String **source)
{
    if (*source == ((String *)0))
    {
        return;
    }
    if ((*source)->length == 0)
    {
        String *temp = *source;
        *source = create();
        discard(&temp);
        return;
    }
    (*source)->val[--(*source)->length] = '\0';
    if ((float)(*source)->length / (*source)->capacity < 0.25 && (*source)->capacity > 2)
    {
        (*source)->capacity /= 2;
        (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
    }
}

const char *to_string(String **source)
{
    if ((*source) == ((String *)0))
    {
        return ((char *)0);
    }
    return (*source)->val;
}

int length(String **source)
{
    if ((*source) == ((String *)0))
    {
        return 0;
    }
    return (*source)->length;
}

void nappend(String **source, char *appendix, int max_size)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    int i, length = min(strnlen(appendix, MAX_STRING), max_size);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)(*source)->length / (*source)->capacity > 0.75)
        {
            (*source)->capacity *= 2;
            (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
        }
        (*source)->val[(*source)->length++] = t;
    }
    (*source)->val[(*source)->length] = '\0';
}

void nextend(String **source, String **extension, int max_size)
{
    if ((*source) == ((String *)0) || (*extension) == ((String *)0))
    {
        return;
    }
    int i, length = min((*extension)->length, max_size);
    for (i = 0; i < length; ++i)
    {
        char t = (*extension)->val[i];
        if ((float)(*source)->length / (*source)->capacity > 0.75)
        {
            (*source)->capacity *= 2;
            (*source)->val = (char *)realloc((*source)->val, ((*source)->capacity + 1) * sizeof(char));
        }
        (*source)->val[(*source)->length++] = t;
    }
    (*source)->val[(*source)->length] = '\0';
}

int min(int a, int b)
{
    return a < b ? a : b;
}
#endif