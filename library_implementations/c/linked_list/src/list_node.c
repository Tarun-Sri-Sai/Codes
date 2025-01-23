#include <stdio.h>
#include <stdlib.h>
#include "../include/list_node.h"

#define DEREF 0

list_node *new_node(int val)
{
    list_node *node = (list_node *)malloc(sizeof(list_node));
    node->val = val;
    node->prev = NULL;
    node->next = NULL;
    return node;
}

void delete_node(list_node **node_ptr)
{
    free(node_ptr[DEREF]);
    node_ptr[DEREF] = NULL;
}

void node_debug_print(list_node *node)
{
    printf("{%d, prev = %d, next = %d}", node->val, node->prev->val, node->next->val);
}