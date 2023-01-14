#pragma once

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/**
 * @brief   
 * @brief   Dynamic String Library
 * @details String grows and shrinks based on requirement.
 *          Allocation and deallocation of the object are explicit.
 *          Uses pointer to structs of type 'string *' that contain
 *          three items: val, length & capacity. capacity of 'string *'
 *          object changes with change in length.
 *          If only library's functions are used for access and
 *          modification, 'string *' objects are memory-safe.
 */
typedef struct string_tag
{
    char *val;
    unsigned long length, capacity;
} string;

string *init(char *val);
string *create();
void append(string **source, char *appendix);
void extend(string **source, string **extension);
void discard(string **source);
void debug_print(string **source);
void push_back(string **source, char appendix);
void pop_back(string **source);
const char *to_string(string **source);
unsigned long length(string **source);
void nappend(string **source, char *appendix, unsigned long max_size);
void nextend(string **source, string **extension, unsigned long max_size);
unsigned long min(unsigned long a, unsigned long b);

/**
 * @brief   String object initializer
 * @details Creates a new object of type 'string *' and appends
 *          the char string val to the object's val item.
 *
 * @param   val char * 
 * @return  string *
 */
string *init(char *val)
{
    string *retval = create();
    append(&retval, val);
    return retval;
}

/**
 * @brief   String object constructor
 * @details Creates a new object of type 'string *'.
 *
 * @return  string *
 */
string *create()
{
    string *retval = (string *)malloc(sizeof(string *));
    retval->capacity = 2;
    retval->length = 0;
    retval->val = (char *)calloc(retval->capacity + 1, sizeof(char));
    retval->val[retval->length] = '\0';
    return retval;
}

/**
 * @brief   
 * @details Appends char string of type 'char *' to the object pointed by
 *          source's val item.
 *          Does nothing if object pointed by source is (string *)0.
 *
 * @param   source      string ** 
 * @param   appendix    char * 
 * @return  void
 */
void append(string **source, char *appendix)
{
    if ((*source) == ((string *)0))
    {
        return;
    }
    unsigned long i, length = strlen(appendix);
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
 * @brief   Appends one string object to another
 * @details object pointed by the val item of object pointed by extension
 *          to the val item of object pointed by source. The object pointed by
 *          extension remains unchanged.
 *          Does nothing if any one of source or extension point to
 *          (string *)0.
 *
 * @param   source      string **
 * @param   extension   string **
 * @return  void
 */
void extend(string **source, string **extension)
{
    if ((*source) == ((string *)0) || (*extension) == ((string *)0))
    {
        return;
    }
    unsigned long i;
    for (i = 0; i < (*extension)->length; ++i)
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
 * @brief   String object Destructor
 * @details Frees the memory of object pointed by source as well as its
 *          val item. Sets the object to (string *)0.
 *          Does nothing if the object pointed by source is
 *          (string *)0.
 *
 * @param   source  string **
 * @return  void
 */
void discard(string **source)
{
    if (*source == ((string *)0))
    {
        return;
    }
    free((*source)->val);
    free(*source);
    *source = ((string *)0);
}

/**
 * @brief   Debugger Print a String object
 * @details Prints the items in object pointed by source.
 *          Does nothing if source is pointing to (string *)0).
 *
 * @param   source  string ** 
 * @return  void
 */
void debug_print(string **source)
{
    if ((*source) == ((string *)0))
    {
        return;
    }
    printf("Length: %d\nCapacity: %d\nString: %s\n", (*source)->length, (*source)->capacity, (*source)->val);
}

/**
 * @brief   Adds a character to String object
 * @details Appends the character appendix to the val item of the object
 *          pointed  by source.
 *          Does nothing if source is pointing to (string *)0).
 *
 * @param   source      string **
 * @param   appendix    char
 * @return  void
 */
void push_back(string **source, char appendix)
{
    if ((*source) == ((string *)0))
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
 * @brief   Delete character at end
 * @details Removes last character from object pointed by source.
 *          Discards old object and creates a new object if only one
 *          character is left in the val item of source.
 *          Does nothing if the object pointed by source is
 *          (string *)0.
 *
 * @param   source  string **
 * @return  void
 */
void pop_back(string **source)
{
    if (*source == ((string *)0))
    {
        return;
    }
    if ((*source)->length == 0)
    {
        string *temp = *source;
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
 * @brief   Return char pointer of String object
 * @details Returns val item of object pointed by source.
 *          Returns (char *)0 if source is pointing to (string *)0.
 *
 * @param   source  string **
 * @return  const char *
 */
const char *to_string(string **source)
{
    if ((*source) == ((string *)0))
    {
        return ((char *)0);
    }
    return (*source)->val;
}

/**
 * @brief   Returns length of String object
 * @details length item of object pointed by source. Returns 0 if
 *          source is pointing to (string *)0.
 *
 * @param   source  string **
 * @return  unsigned long
 */
unsigned long length(string **source)
{
    if ((*source) == ((string *)0))
    {
        return 0;
    }
    return (*source)->length;
}

/**
 * @brief   Limited length version of append()
 * @details Appends atmost max_size characters from char string of type
 *          'char *' to the val item of object pointed by source.
 *          Does nothing if source is pointing to (string *)0.
 *
 * @param   source      string **
 * @param   appendix      char *
 * @param   max_size      unsigned long
 * @return  void
 */
void nappend(string **source, char *appendix, unsigned long max_size)
{
    if ((*source) == ((string *)0))
    {
        return;
    }
    unsigned long i, length = min(strlen(appendix), max_size);
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
 * @brief   Limited length version of extend()
 * @details Appends the val item of object pointed by extension to the val
 *          item of object pointed by source. The object extension remains
 *          unchanged.
 *          Does nothing if any one of source or extension is pointing to
 *          (string *)0.
 *
 * @param   source      string **
 * @param   extension   string **
 * @param   max_size    unsigned long
 * @return  void
 */
void nextend(string **source, string **extension, unsigned long max_size)
{
    if ((*source) == ((string *)0) || (*extension) == ((string *)0))
    {
        return;
    }
    unsigned long i;
    for (i = 0; i < min((*extension)->length, max_size); ++i)
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
 * @param   a   unsigned long
 * @param   b   unsigned long
 * @return  unsigned long
 */
unsigned long min(unsigned long a, unsigned long b)
{
    return a < b ? a : b;
}
