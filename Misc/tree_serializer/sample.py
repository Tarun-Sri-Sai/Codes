from json import dump


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add(self, child):
        self.children.append(child)

    def remove(self, value):
        for i, child in enumerate(self.children):
            if child.get() != value:
                continue
            self.children.pop(i)

    def all(self):
        return self.children

    def child(self, value):
        for child in self.children:
            if child.value != value:
                continue
            return child
        return None

    def get(self):
        return self.value


def to_dict(root):
    if not root:
        return None
    root_dict = {}
    root_dict['value'] = root.get()
    root_dict['children'] = [to_dict(child) for child in root.all()]
    return root_dict


def build():
    tree = TreeNode(0)

    tree.add(TreeNode(1))
    tree.add(TreeNode(2))
    tree.add(TreeNode(3))

    tree.child(1).add(TreeNode(4))

    tree.child(2).add(TreeNode(5))
    tree.child(2).add(TreeNode(6))

    tree.child(2).child(5).add(TreeNode(7))
    tree.child(2).child(5).add(TreeNode(8))

    with open('tree.json', 'w') as f:
        dump(to_dict(tree), f, indent=4)
