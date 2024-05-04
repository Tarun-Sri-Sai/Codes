#include <stdio.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include "../../c/dynstr/dynstr.h"

#define STRING_EQUAL 0

int main()
{
    const int TOTAL = 10;
    int count = 0;

    String *str1 = new_string();
    assert(strcmp(to_string(str1), "") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"\"\t\t\t\tafter new_string()\t\twas called once\n", ++count, TOTAL);

    delete_string(&str1);
    assert(str1 == NULL);
    printf("[%d/%d]\tstr1 is NULL\t\t\t\tafter delete_string()\t\twas called once\n", ++count, TOTAL);

    str1 = init("Hello");
    assert(strcmp(to_string(str1), "Hello") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello\"\t\t\tafter init()\t\t\twas called once\n", ++count, TOTAL);

    nappend(str1, " ", 1);
    assert(strcmp(to_string(str1), "Hello ") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello \"\t\t\tafter nappend()\t\t\twas called once\n", ++count, TOTAL);

    append(str1, "World!");
    assert(strcmp(to_string(str1), "Hello World!") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello World!\"\t\t\tafter append()\t\t\twas called once\n", ++count, TOTAL);

    String *str2 = init("I'm Tarun!");

    nextend(str1, str2, 3);
    assert(strcmp(to_string(str1), "Hello World!I'm") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello World!I'm\"\t\tafter nextend()\t\t\twas called once\n", ++count, TOTAL);

    pop_back(&str1);
    pop_back(&str1);
    pop_back(&str1);
    assert(strcmp(to_string(str1), "Hello World!") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello World!\"\t\t\tafter pop_back()\t\twas called thrice\n", ++count, TOTAL);

    push_back(str1, ' ');
    assert(strcmp(to_string(str1), "Hello World! ") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello World! \"\t\tafter push_back()\t\twas called once\n", ++count, TOTAL);

    extend(str1, str2);
    assert(strcmp(to_string(str1), "Hello World! I'm Tarun!") == STRING_EQUAL);
    printf("[%d/%d]\tstr1 has \"Hello World! I'm Tarun!\"\tafter extend()\t\t\twas called once\n", ++count, TOTAL);

    size_t len = length(str1);
    assert(strlen("Hello World! I'm Tarun!") == len);
    printf("[%d/%d]\tstr1 is %llu characters long\t\tafter length()\t\t\twas called once\n", ++count, TOTAL, len);

    printf("[%d/%d]\tAll expressions asserted successfully\n", count, TOTAL);
    return EXIT_SUCCESS;
}