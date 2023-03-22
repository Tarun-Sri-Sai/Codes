#include <stdio.h>
#include <stdlib.h>
#include "linked_list.h"

#define DEREF 0

void list_push_back(linked_list *list, int val)
{
    if (list == NULL)
    {
        return;
    }
    list_node *tail = list->tail;
    list_node *prev = tail->prev;
    list_node *added_node = new_node(val);

    added_node->prev = prev;
    added_node->next = tail;
    tail->prev = added_node;
    prev->next = added_node;
}

void list_push_front(linked_list *list, int val)
{
    if (list == NULL)
    {
        return;
    }
    list_node *head = list->head;
    list_node *next = head->next;
    list_node *added_node = new_node(val);

    added_node->next = next;
    added_node->prev = head;
    head->next = added_node;
    next->prev = added_node;
}

void list_pop_back(linked_list *list)
{
    if (list == NULL)
    {
        return;
    }
    list_node *head = list->head;
    list_node *tail = list->tail;

    if (head->next == tail)
    {
        return;
    }
    list_node *deleted_node = tail->prev;
    list_node *prev = deleted_node->prev;

    prev->next = tail;
    tail->prev = prev;
    delete_node(&deleted_node);
}

void list_pop_front(linked_list *list)
{
    if (list == NULL)
    {
        return;
    }
    list_node *head = list->head;
    list_node *tail = list->tail;

    if (head->next == tail)
    {
        return;
    }
    list_node *deleted_node = head->next;
    list_node *next = deleted_node->next;

    head->next = next;
    next->prev = head;
    delete_node(&deleted_node);
}

void delete_list(linked_list **list_ptr)
{
    list_node *node = list_ptr[DEREF]->head, *next;

    for (next = node->next; next != NULL; node = next)
    {
        next = node->next;
        delete_node(&node);
    }
    delete_node(&(list_ptr[DEREF]->tail));
    list_ptr[DEREF] = NULL;
}

linked_list *new_list()
{
    linked_list *list = (linked_list *)malloc(sizeof(linked_list));

    list->head = new_node(0);
    list->tail = new_node(0);
    list->head->next = list->tail;
    list->tail->prev = list->head;
    return list;
}

void print_list(linked_list *list)
{
    if (list == NULL)
    {
        return;
    }
    list_node *head = list->head, *ptr, *tail = list->tail;

    printf("[");
    for (ptr = head->next; ptr != tail; ptr = ptr->next)
    {
        printf("%d%s", ptr->val, (ptr->next != tail ? " -> " : ""));
    }
    printf("]\n");
}