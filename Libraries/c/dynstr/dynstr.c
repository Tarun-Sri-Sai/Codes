#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "dynstr.h"

#define MAX_STRING 0xFFFF
#define DEREF 0

String *init(char *val)
{
    String *retval = new_string();
    append(retval, val);
    return retval;
}

String *new_string()
{
    String *retval = (String *) malloc(sizeof (String *));
    retval->capacity = 2;
    retval->length = 0;
    retval->val = (char *) calloc(retval->capacity + 1, sizeof (char));
    retval->val[retval->length] = '\0';
    return retval;
}

void append(String *source, char *appendix)
{
    if (source == NULL)
    {
        return;
    }
    int i, length = strnlen(appendix, MAX_STRING);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float) source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *) realloc(source->val, (source->capacity + 1) * sizeof (char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

void extend(String *source, String *extension)
{
    if (source == NULL || extension == NULL)
    {
        return;
    }
    int i, length = extension->length;
    for (i = 0; i < length; ++i)
    {
        char t = extension->val[i];
        if ((float) source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *) realloc(source->val, (source->capacity + 1) * sizeof (char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

void delete_string(String **source_ptr)
{
    if (source_ptr[DEREF] == NULL)
    {
        return;
    }
    free(source_ptr[DEREF]->val);
    free(source_ptr[DEREF]);
    source_ptr[DEREF] = NULL;
}

void debug_print(String *source)
{
    if (source == NULL)
    {
        return;
    }
    printf("Length: %d\nCapacity: %d\nString: %s\n", source->length, source->capacity, source->val);
}

void push_back(String *source, char appendix)
{
    if (source == NULL)
    {
        return;
    }
    if (appendix == '\0')
    {
        return;
    }
    if ((float) source->length / source->capacity > 0.75)
    {
        source->capacity *= 2;
        source->val = (char *) realloc(source->val, (source->capacity + 1) * sizeof (char));
    }
    source->val[source->length++] = appendix;
    source->val[source->length] = '\0';
}

void pop_back(String **source_ptr)
{
    if (source_ptr[DEREF] == NULL)
    {
        return;
    }
    if (source_ptr[DEREF]->length == 0)
    {
        String *temp = source_ptr[DEREF];
        source_ptr[DEREF] = new_string();
        delete_string(&temp);
        return;
    }
    source_ptr[DEREF]->val[--source_ptr[DEREF]->length] = '\0';
    if ((float) source_ptr[DEREF]->length / source_ptr[DEREF]->capacity < 0.25 && source_ptr[DEREF]->capacity > 2)
    {
        source_ptr[DEREF]->capacity /= 2;
        source_ptr[DEREF]->val = (char *) realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof (char));
    }
}

const char *to_string(String *source)
{
    if (source == NULL)
    {
        return NULL;
    }
    return source->val;
}

int length(String *source)
{
    if (source == NULL)
    {
        return 0;
    }
    return source->length;
}

void nappend(String *source, char *appendix, int max_size)
{
    if (source == NULL)
    {
        return;
    }
    int i, length = min(strnlen(appendix, MAX_STRING), max_size);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float) source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *) realloc(source->val, (source->capacity + 1) * sizeof (char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

void nextend(String *source, String *extension, int max_size)
{
    if (source == NULL || extension == NULL)
    {
        return;
    }
    int i, length = min(extension->length, max_size);
    for (i = 0; i < length; ++i)
    {
        char t = extension->val[i];
        if ((float) source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof (char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

int min(int a, int b)
{
    return a < b ? a : b;
}