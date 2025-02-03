#ifndef _LINKED_LIST_H_
#define _LINKED_LIST_H_

#include "list_node.h"

typedef struct linked_list_struct
{
    list_node *head;
    list_node *tail;
} linked_list;

linked_list *new_list();
void list_push_back(linked_list *list, int val);
void list_push_front(linked_list *list, int val);
void list_pop_back(linked_list *list);
void list_pop_front(linked_list *list);
void delete_list(linked_list **list_ptr);
char *list_debug_print(linked_list *list);
void trim_string(char **string_ptr);

#endif