#ifndef _LINKED_LIST_H_
#define _LINKED_LIST_H_

#include "list_node.h"
#include <stdlib.h>

typedef struct linked_list_struct {
    list_node *head;
    list_node *tail;
} linked_list;

linked_list *new_list();
void push_back(linked_list *list, int val);
void push_front(linked_list *list, int val);
void pop_back(linked_list *list);
void pop_front(linked_list *list);
void delete_list(linked_list **list_ptr);
void print_list(linked_list *list);

#endif