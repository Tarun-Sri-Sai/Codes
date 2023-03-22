#include "linked_list.h"
#include <stdio.h>
#include <stdlib.h>

#define DEREF 0

void push_back(linked_list *list, int val)
{
    if (list == NULL) {
        return;
    }
    list_node *tail = list->tail;
    list_node *prev = tail->prev;
    list_node *new_node = get_new_node(val);

    new_node->prev = prev;
    new_node->next = tail;
    tail->prev = new_node;
    prev->next = new_node;
}

void push_front(linked_list *list, int val)
{
    if (list == NULL) {
        return;
    }
    list_node *head = list->head;
    list_node *next = head->next;
    list_node *new_node = get_new_node(val);

    new_node->next = next;
    new_node->prev = head;
    head->next = new_node;
    next->prev = new_node;
}

void pop_back(linked_list *list)
{
    if (list == NULL) {
        return;
    }
    list_node *head = list->head;
    list_node *tail = list->tail;

    if (head->next == tail) {
        return;
    }
    list_node *deleted_node = tail->prev;
    list_node *prev = deleted_node->prev;

    prev->next = tail;
    tail->prev = prev;
    free_node(&deleted_node);
}

void pop_front(linked_list *list)
{
    if (list == NULL) {
        return;
    }
    list_node *head = list->head;
    list_node *tail = list->tail;

    if (head->next == tail) {
        return;
    }
    list_node *deleted_node = head->next;
    list_node *next = deleted_node->next;

    head->next = next;
    next->prev = head;
    free_node(&deleted_node);
}

void delete_list(linked_list **list_ptr)
{
    list_node *node = list_ptr[DEREF]->head, *next;

    for (next = node->next; next != NULL; node = next) {
        next = node->next;
        free_node(&node);
    }
    free_node(&(list_ptr[DEREF]->tail));
    list_ptr[DEREF] = NULL;
}

linked_list *get_new_list()
{
    linked_list *list = (linked_list *)malloc(sizeof(linked_list));

    list->head = get_new_node(0);
    list->tail = get_new_node(0);
    list->head->next = list->tail;
    list->tail->prev = list->head;
    return list;
}

void print_list(linked_list *list) {
    if (list == NULL) {
        return;
    }
    list_node *head = list->head, *ptr, *tail = list->tail;

    printf_s("[");
    for (ptr = head->next; ptr != tail; ptr = ptr->next) {
        printf_s("%d%s", ptr->val, (ptr->next != tail ? " -> " : ""));
    }
    printf_s("]\n");
}