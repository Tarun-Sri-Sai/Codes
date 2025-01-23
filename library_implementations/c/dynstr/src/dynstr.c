#include "../include/dynstr.h"

String *init(char *val)
{
    String *retval = new_string();
    string_append(retval, val);
    return retval;
}

String *new_string()
{
    String *retval = (String *)malloc(sizeof(String));
    retval->capacity = 2;
    retval->length = 0;
    retval->val = (char *)calloc(retval->capacity + 1, sizeof(char));
    retval->val[retval->length] = '\0';
    return retval;
}

void string_append(String *source, char *appendix)
{
    if (source == NULL)
    {
        return;
    }
    int i, length = strnlen(appendix, MAX_STRING);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof(char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

void string_extend(String *source, String *extension)
{
    if (source == NULL || extension == NULL)
    {
        return;
    }
    int i, length = extension->length;
    for (i = 0; i < length; ++i)
    {
        char t = extension->val[i];
        if ((float)source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof(char));
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

char *string_debug_print(String *source)
{
    if (source == NULL)
    {
        return "";
    }
    char *debug_string = (char *)calloc(MAX_STRING, sizeof(char));

    sprintf_s(debug_string, MAX_STRING, "Length: %d\nCapacity: %d\nString: %s\n", source->length, source->capacity, source->val);
    trim_string(&debug_string);
    return debug_string;
}

void string_push_back(String *source, char appendix)
{
    if (source == NULL)
    {
        return;
    }
    if (appendix == '\0')
    {
        return;
    }
    if ((float)source->length / source->capacity > 0.75)
    {
        source->capacity *= 2;
        source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof(char));
    }
    source->val[source->length++] = appendix;
    source->val[source->length] = '\0';
}

void string_pop_back(String **source_ptr)
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
    if ((float)source_ptr[DEREF]->length / source_ptr[DEREF]->capacity < 0.25 && source_ptr[DEREF]->capacity > 2)
    {
        source_ptr[DEREF]->capacity /= 2;
        source_ptr[DEREF]->val = (char *)realloc(source_ptr[DEREF]->val, (source_ptr[DEREF]->capacity + 1) * sizeof(char));
    }
}

const char *string_value_of(String *source)
{
    if (source == NULL)
    {
        return NULL;
    }
    int length = string_length(source);
    char *result = (char *)calloc(length, sizeof(char));

    memcpy_s(result, length, source->val, length);
    return result;
}

int string_length(String *source)
{
    if (source == NULL)
    {
        return 0;
    }
    return source->length;
}

void string_nappend(String *source, char *appendix, int max_size)
{
    if (source == NULL)
    {
        return;
    }
    int i, length = min(strnlen(appendix, MAX_STRING), max_size);
    for (i = 0; i < length; ++i)
    {
        char t = appendix[i];
        if ((float)source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof(char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

void string_nextend(String *source, String *extension, int max_size)
{
    if (source == NULL || extension == NULL)
    {
        return;
    }
    int i, length = min(extension->length, max_size);
    for (i = 0; i < length; ++i)
    {
        char t = extension->val[i];
        if ((float)source->length / source->capacity > 0.75)
        {
            source->capacity *= 2;
            source->val = (char *)realloc(source->val, (source->capacity + 1) * sizeof(char));
        }
        source->val[source->length++] = t;
    }
    source->val[source->length] = '\0';
}

int min(int a, int b)
{
    return a < b ? a : b;
}

void trim_string(char **string_ptr)
{
    size_t length = strnlen_s(string_ptr[DEREF], MAX_STRING);

    string_ptr[DEREF] = (char *)realloc(string_ptr[DEREF], length * sizeof(char));
}
