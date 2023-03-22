#include <stdio.h>
#include "C:/Users/tarun/Documents/Codes/Libraries/c/linked_list/linked_list.h"

int main()
{
    linked_list *list = new_list();
    print_list(list);

    push_front(list, 2);
    print_list(list);

    push_back(list, 1);
    print_list(list);

    pop_front(list);
    print_list(list);

    pop_back(list);
    print_list(list);

    return EXIT_SUCCESS;
}