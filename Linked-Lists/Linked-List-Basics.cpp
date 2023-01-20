#include <bits/stdc++.h>
using namespace std;

class Node
{
public:
    int data;
    Node *next;

    Node(int data)
    {
        this->data = data;
        next = NULL;
    }
};

class LinkedList
{
    Node *head;
    int count;

public:
    LinkedList()
    {
        head = NULL;
        count = 0;
    }

    void push(int data)
    {
        Node *temp = new Node(data);
        count++;
        if (head == NULL)
        {
            head = temp;
            return;
        }
        Node *curr = head;
        while (curr->next != NULL)
        {
            curr = curr->next;
        }
        curr->next = temp;
    }

    void print()
    {
        Node *temp = head;
        int iter = 0;
        if (head != NULL)
        {
            while (temp != NULL)
            {
                iter++;
                cout << temp->data;
                if (iter != count)
                {
                    cout << " -> ";
                }
                temp = temp->next;
            }
            cout << endl;
        }
    }

    void reverse()
    {
        Node *curr = head;
        Node *prev = NULL, *next = NULL;
        while (curr != NULL)
        {
            next = curr->next;
            curr->next = prev;
            prev = curr;
            curr = next;
        }
        head = prev;
    }
};

int main(void)
{
    LinkedList l1;
    int n;
    cin >> n;
    int arr[n];
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
    }
    for (int i = 0; i < n; i++)
    {
        l1.push(arr[i]);
    }
    cout << "\n"
         << "Before reverse: ";
    l1.print();
    l1.reverse();
    cout << "After reverse: ";
    l1.print();
    return 0;
}