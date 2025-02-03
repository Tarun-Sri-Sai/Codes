#include <stdio.h>
#include <stdlib.h>
#include "../include/linked_list.h"

int main()
{
    linked_list *list = new_list();
    printf("%s\n", list_debug_print(list));

    list_push_front(list, 2);
    printf("%s\n", list_debug_print(list));

    list_push_back(list, 1);
    printf("%s\n", list_debug_print(list));

    list_pop_front(list);
    printf("%s\n", list_debug_print(list));

    list_pop_back(list);
    printf("%s\n", list_debug_print(list));

    return EXIT_SUCCESS;
}