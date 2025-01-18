#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include "../include/dynstr.h"

#define STRING_EQUAL 0

int main()
{
    const int TOTAL = 10;
    int count = 0;

    String *str1 = new_string();
    assert(strcmp(string_value_of(str1), "") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"\" after new_string() was called once\n", ++count, TOTAL);

    delete_string(&str1);
    assert(str1 == NULL);
    printf("[%d/%d] str1 is NULL after delete_string() was called once\n", ++count, TOTAL);

    str1 = init("Hello");
    assert(strcmp(string_value_of(str1), "Hello") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello\" after init() was called once\n", ++count, TOTAL);

    string_nappend(str1, " ", 1);
    assert(strcmp(string_value_of(str1), "Hello ") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello \" after string_nappend() was called once\n", ++count, TOTAL);

    string_append(str1, "World!");
    assert(strcmp(string_value_of(str1), "Hello World!") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello World!\" after string_append() was called once\n", ++count, TOTAL);

    String *str2 = init("I'm Tarun!");

    string_nextend(str1, str2, 3);
    assert(strcmp(string_value_of(str1), "Hello World!I'm") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello World!I'm\" after string_nextend() was called once\n", ++count, TOTAL);

    string_pop_back(&str1);
    string_pop_back(&str1);
    string_pop_back(&str1);
    assert(strcmp(string_value_of(str1), "Hello World!") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello World!\" after string_pop_back() was called thrice\n", ++count, TOTAL);

    string_push_back(str1, ' ');
    assert(strcmp(string_value_of(str1), "Hello World! ") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello World! \" after string_push_back() was called once\n", ++count, TOTAL);

    string_extend(str1, str2);
    assert(strcmp(string_value_of(str1), "Hello World! I'm Tarun!") == STRING_EQUAL);
    printf("[%d/%d] str1 has \"Hello World! I'm Tarun!\" after string_extend() was called once\n", ++count, TOTAL);

    size_t len = string_length(str1);
    assert(strlen("Hello World! I'm Tarun!") == len);
    printf("[%d/%d] str1 is %llu characters long after string_length() was called once\n", ++count, TOTAL, len);

    printf("[%d/%d] All expressions asserted successfully\n", count, TOTAL);
    return EXIT_SUCCESS;
}