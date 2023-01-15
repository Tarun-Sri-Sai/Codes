#pragma once

#include <stdio.h>
#include <String.h>
#include <stdlib.h>

#define MAX_STRING 0xFFFF

/**
 * @brief   Dynamic String Object.
 * @details String grows and shrinks based on requirement. Allocation and 
 *          deallocation of the object are explicit. Contains three items:
 *          val, length & capacity. Capacity of String object changes with
 *          change in length. If only library's functions are used for
 *          access and modification, String objects are memory-safe.
 */
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

/**
 * @brief   String object initializer.
 * @details Creates a new String object and appends the char-string val to 
 *          the object's val item.
 *
 * @param   val A char-string to initialize the String object with.
 * @return  A pointer to String object.
 */
String *init(char *val)
{
    String *retval = create();
    append(&retval, val);
    return retval;
}

/**
 * @brief   String object constructor.
 * @details Creates a new String object.
 *
 * @return   A pointer to String object.
 */
String *create()
{
    String *retval = (String *)malloc(sizeof(String *));
    retval->capacity = 2;
    retval->length = 0;
    retval->val = (char *)calloc(retval->capacity + 1, sizeof(char));
    retval->val[retval->length] = '\0';
    return retval;
}

/**
 * @brief   Appends a char-string to String object.
 * @details Appends char-string of type 'char *' to the object pointed by 
 *          source's val item. Does nothing if object pointed by source is
 *          (String *)0.
 *
 * @param   source      A pointer to pointer to String.
 * @param   appendix    char-string to append.
 * @return  void
 */
void append(String **source, char *appendix)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    int i, length = strnlen_s(appendix, MAX_STRING);
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

/**
 * @brief   Appends one String object to another.
 * @details Appends String object source to String object extension. The 
 *          object pointed by extension remains unchanged. Does nothing if
 *          any one of source or extension point to (String *)0.
 *
 * @param   source      A pointer to pointer to String.
 * @param   extension   A pointer to pointer to String.
 * @return  void
 */
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

/**
 * @brief   String object Destructor.
 * @details Appends String object source to String object extension. The 
 *          object pointed by extension remains unchanged. Does nothing if
 *          any one of source or extension point to (String *)0.
 *
 * @param   source  A pointer to pointer to String.
 * @return  void
 */
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

/**
 * @brief   Debugger print a String object.
 * @details Prints the items in object pointed by source. Does nothing if 
 *          source is pointing to (String *)0).
 * 
 * @param   source  A pointer to pointer to String.
 * @return  void
 */
void debug_print(String **source)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    printf("Length: %d\nCapacity: %d\nString: %s\n", (*source)->length, (*source)->capacity, (*source)->val);
}

/**
 * @brief   Adds a character at the end of String object.
 * @details Prints the items in object pointed by source. Does nothing if 
 *          source is pointing to (String *)0).
 * 
 * @param   source      A pointer to pointer to String.
 * @param   appendix    A character to append.
 * @return  void
 */
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

/**
 * @brief   Deletes character at the end of String object.
 * @details Removes last character from object pointed by source. Discards 
 *          old object and creates a new object if only one character is
 *          left in the val item of source. Does nothing if the object
 *          pointed by source is (String *)0.
 * 
 * @param   source  A pointer to pointer to String.
 * @return  void
 */
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

/**
 * @brief   Returns char pointer of String object.
 * @details Returns val item of object pointed by source. Returns (char *)0 
 *          if source is pointing to (String *)0.
 * 
 * @param   source  A pointer to pointer to String.
 * @return  A const char-string version of String object.
 */
const char *to_string(String **source)
{
    if ((*source) == ((String *)0))
    {
        return ((char *)0);
    }
    return (*source)->val;
}

/**
 * @brief   Returns length of String object.
 * @details Returns length item of String object.
 *
 * @param   source  A pointer to pointer to String.
 * @return  Length of type int.
 */
int length(String **source)
{
    if ((*source) == ((String *)0))
    {
        return 0;
    }
    return (*source)->length;
}

/**
 * @brief   Length limited version of append().
 * @details Appends char-string of type 'char *' to the object pointed by 
 *          source's val item. Does nothing if object pointed by source is
 *          (String *)0.
 *
 * @param   source      A pointer to pointer to String.
 * @param   appendix    A char-string to append.
 * @param   max_size    Max allowed length to append.
 * @return  void
 */
void nappend(String **source, char *appendix, int max_size)
{
    if ((*source) == ((String *)0))
    {
        return;
    }
    int i, length = min(strnlen_s(appendix, MAX_STRING), max_size);
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

/**
 * @brief   Length limited version of extend()
 * @details Appends String object source to String object extension. The 
 *          object pointed by extension remains unchanged. Does nothing if
 *          any one of source or extension point to (String *)0.
 *
 * @param   source      A pointer to pointer to String.
 * @param   appendix    A pointer to pointer to String.
 * @param   max_size    Max allowed length to append.
 * @return  void
 */
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

/**
 * @brief   Returns minimum of a and b.
 *
 * @param   a   Integer of type int
 * @param   b   Integer of type int
 * @return  Integer of type int
 */
int min(int a, int b)
{
    return a < b ? a : b;
}
