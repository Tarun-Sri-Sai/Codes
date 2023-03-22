#ifndef DYN_STR_H
#define DYN_STR_H

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_STRING 0xFFFF
#define DEREF 0
#define STR_NULL_PTR ((String *) 0)

typedef struct String_tag
{
    char *val;
    int length, capacity;
} String;

String *init(char *val);
String *create();
void append(String **source_ptr, char *appendix);
void extend(String **source_ptr, String **extension_ptr);
void discard(String **source_ptr);
void debug_print(String **source_ptr);
void push_back(String **source_ptr, char appendix);
void pop_back(String **source_ptr);
const char *to_string(String **source_ptr);
int length(String **source_ptr);
void nappend(String **source_ptr, char *appendix, int max_size);
void nextend(String **source_ptr, String **extension_ptr, int max_size);
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

void append(String **source_ptr, char *appendix)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    int i, length = strnlen(appendix, MAX_STRING);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity > 0.75)
        {
            source_ptr[DEREF]->capacity *= 2;
            source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
        }
        source_ptr[DEREF]->val[source_ptr[DEREF]->length++] = t;
    }
    source_ptr[DEREF]->val[source_ptr[DEREF]->length] = '\0';
}

void extend(String **source_ptr, String **extension_ptr)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR) || extension_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    int i, length = extension_ptr[DEREF]->length;
    for (i = 0; i < length; ++i)
    {
        char t = extension_ptr[DEREF]->val[i];
        if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity > 0.75)
        {
            source_ptr[DEREF]->capacity *= 2;
            source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
        }
        source_ptr[DEREF]->val[source_ptr[DEREF]->length++] = t;
    }
    source_ptr[DEREF]->val[source_ptr[DEREF]->length] = '\0';
}

void discard(String **source_ptr)
{
    if (*source_ptr == (STR_NULL_PTR))
    {
        return;
    }
    free(source_ptr[DEREF]->val);
    free(source_ptr[DEREF]);
    *source_ptr = (STR_NULL_PTR);
}

void debug_print(String **source_ptr)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    printf("Length: %d\nCapacity: %d\nString: %s\n", source_ptr[DEREF]->length, source_ptr[DEREF]->capacity, source_ptr[DEREF]->val);
}

void push_back(String **source_ptr, char appendix)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    if (appendix == '\0')
    {
        return;
    }
    if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity > 0.75)
    {
        source_ptr[DEREF]->capacity *= 2;
        source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
    }
    source_ptr[DEREF]->val[source_ptr[DEREF]->length++] = appendix;
    source_ptr[DEREF]->val[source_ptr[DEREF]->length] = '\0';
}

void pop_back(String **source_ptr)
{
    if (*source_ptr == (STR_NULL_PTR))
    {
        return;
    }
    if (source_ptr[DEREF]->length == 0)
    {
        String *temp = *source_ptr;
        *source_ptr = create();
        discard(&temp);
        return;
    }
    source_ptr[DEREF]->val[--source_ptr[DEREF]->length] = '\0';
    if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity < 0.25 && source_ptr[DEREF]->capacity > 2)
    {
        source_ptr[DEREF]->capacity /= 2;
        source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
    }
}

const char *to_string(String **source_ptr)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return ((char *)0);
    }
    return source_ptr[DEREF]->val;
}

int length(String **source_ptr)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return 0;
    }
    return source_ptr[DEREF]->length;
}

void nappend(String **source_ptr, char *appendix, int max_size)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    int i, length = min(strnlen(appendix, MAX_STRING), max_size);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity > 0.75)
        {
            source_ptr[DEREF]->capacity *= 2;
            source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
        }
        source_ptr[DEREF]->val[source_ptr[DEREF]->length++] = t;
    }
    source_ptr[DEREF]->val[source_ptr[DEREF]->length] = '\0';
}

void nextend(String **source_ptr, String **extension_ptr, int max_size)
{
    if (source_ptr[DEREF] == (STR_NULL_PTR) || extension_ptr[DEREF] == (STR_NULL_PTR))
    {
        return;
    }
    int i, length = min(extension_ptr[DEREF]->length, max_size);
    for (i = 0; i < length; ++i)
    {
        char t = extension_ptr[DEREF]->val[i];
        if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity > 0.75)
        {
            source_ptr[DEREF]->capacity *= 2;
            source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
        }
        source_ptr[DEREF]->val[source_ptr[DEREF]->length++] = t;
    }
    source_ptr[DEREF]->val[source_ptr[DEREF]->length] = '\0';
}

int min(int a, int b)
{
    return a < b ? a : b;
}
#endif