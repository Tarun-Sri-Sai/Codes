#include <stdio.h>
#include <stdlib.h>
#include "list_node.h"

list_node *get_new_node(int val)
{
    list_node *node = (list_node *)malloc(sizeof(list_node));
    node->val = val;
    node->prev = NULL;
    node->next = NULL;
    return node;
}

void free_node(list_node **node) {
    free(*node);
    (*node) = NULL;
}

void print_node(list_node *node) {
    printf_s("{%d, prev = %d, next = %d}", node->val, node->prev->val, node->next->val);
}