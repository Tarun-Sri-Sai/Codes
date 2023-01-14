#include <iostream>
using namespace std;

class Node
{
public:
    int val;
    Node *next;

    Node(int val)
    {
        this->val = val;
        this->next = nullptr;
    }

    ~Node()
    {
        delete (this);
    }

    Node *reverse()
    {
        if (this == nullptr || this->next == nullptr)
            return this;
        Node *rest = this->next->reverse();
        this->next->next = this;
        this->next = nullptr;
        return rest;
    }

    Node *findMiddle(bool lower)
    {
        Node *slow = this, *fast = this, *prev = nullptr;
        while (fast != nullptr && fast->next != nullptr)
        {
            prev = slow;
            slow = slow->next;
            fast = fast->next->next;
        }
        if (lower || fast == nullptr)
            return prev;
        return slow;
    }

    static Node *merge(Node *head1, Node *head2)
    {
        if (head1 == nullptr)
            return head2;
        if (head2 == nullptr)
            return head1;
        if (head1->val < head2->val)
        {
            head1->next = merge(head1->next, head2);
            return head1;
        }
        head2->next = merge(head1, head2->next);
        return head2;
    }

    Node *sort()
    {
        if (this == nullptr || this->next == nullptr)
            return this;
        Node *middle = this->findMiddle(true);
        Node *middleNext = middle->next;
        middle->next = nullptr;
        return merge(this->sort(), middleNext->sort());
    }
};

int main()
{
    int n, k;
    cin >> n >> k;
    Node *head = new Node(k), *curr = head;
    for (int i = 0; i < n - 1; i++)
    {
        cin >> k;
        Node *temp = new Node(k);
        curr->next = temp;
        curr = curr->next;
    }
    for (curr = head; curr != nullptr; curr = curr->next)
        cerr << curr->val << ' ';
    cerr << '\n';
    head = head->sort();
    head = head->reverse();
    curr = head;
    for (curr = head; curr != nullptr; curr = curr->next)
        cout << curr->val << ' ';
    cout << '\n';
    return 0;
}