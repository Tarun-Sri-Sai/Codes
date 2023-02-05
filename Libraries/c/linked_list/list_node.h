#ifndef _LIST_NODE_H_
#define _LIST_NODE_H_

typedef struct list_node_struct 
{
    int val;
    struct list_node_struct *next, *prev;
} list_node;

list_node *get_new_node();
void print_node(list_node *node);
void free_node(list_node **node);

#endif