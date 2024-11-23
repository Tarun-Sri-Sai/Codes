#ifndef _LIST_NODE_H_
#define _LIST_NODE_H_

typedef struct list_node_struct 
{
    int val;
    struct list_node_struct *next, *prev;
} list_node;

list_node *new_node(int val);
void node_debug_print(list_node *node);
void delete_node(list_node **node_ptr);

#endif