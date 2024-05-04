package java_packages.collections;

import java.util.Iterator;
import java.util.Stack;

public class TreeMap<K, V> implements Map<K, V>, Iterable<Pair<K, V>> {
    private TreeNode<Pair<K, V>> root;
    private int size = 0;

    public TreeMap() {
        root = null;
    }

    public void putIfAbsent(K key, V value) {
        if (!containsKey(key)) {
            put(key, value);
        }
    }

    public V getOrDefault(K key, V defaultValue) {
        if (!containsKey(key)) {
            return defaultValue;
        }
        V result = get(key);
        return result;
    }

    public V get(K key) {
        Pair<K, V> result = getPair(root, key);
        if (result == null) {
            return null;
        }
        return result.value;
    }

    private Pair<K, V> getPair(TreeNode<Pair<K, V>> root, K key) {
        if (root == null) {
            return null;
        }
        int keyCode = key.hashCode(), rootKeyCode = root.data.hashCode();
        if (keyCode < rootKeyCode) {
            Pair<K, V> result = getPair(root.left, key);
            return result;
        }
        if (keyCode > rootKeyCode) {
            Pair<K, V> result = getPair(root.right, key);
            return result;
        }
        return root.data;
    }

    public void put(K key, V value) {
        insert(new Pair<K, V>(key, value));
    }

    public void remove(K key) {
        root = delete(root, key);
    }

    private TreeNode<Pair<K, V>> delete(
            TreeNode<Pair<K, V>> root,
            K key) {
        if (root == null) { // empty tree
            return root;
        }
        int keyCode = key.hashCode(), rootKeyCode = root.data.hashCode();
        if (keyCode < rootKeyCode) { // target on left side of tree
            root.left = delete(root.left, key);
        } else if (keyCode > rootKeyCode) { // target on right side of tree
            root.right = delete(root.right, key);
        } else if (root.left == null || root.right == null) { // root is target, but less than two children
            size--;
            root = root.left != null ? root.left : root.right;
        } else { // root is target, but two children
            size--;
            root.data = getMax(root.left);
            root.left = delete(root.left, root.data.key);
        }
        if (root == null) {
            return root;
        }
        root.height = 1 + Math.max(
                height(root.left),
                height(root.right)); // update height for balanceFactor purpose
        int rootBalanceFactor = getBalanceFactor(root);
        if (rootBalanceFactor > 1) { // if left subtree is unbalanced
            int leftBalanceFactor = getBalanceFactor(root.left);
            if (leftBalanceFactor < 0) {
                root.left = leftRotate(root.left);
            }
            root = rightRotate(root);
            return root;
        }
        if (rootBalanceFactor < -1) { // if right subtree is unbalanced
            int rightBalanceFactor = getBalanceFactor(root.right);
            if (rightBalanceFactor > 0) {
                root.right = rightRotate(root.right);
            }
            root = leftRotate(root);
            return root;
        }
        return root;
    }

    private Pair<K, V> getMax(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return null;
        }
        if (root.right == null) {
            return root.data;
        }
        Pair<K, V> result = getMax(root.right);
        return result;
    }

    public boolean containsKey(K key) {
        boolean result = search(root, key);
        return result;
    }

    private boolean search(TreeNode<Pair<K, V>> root, K key) {
        if (root == null) {
            return false;
        }
        int keyCode = key.hashCode(), rootKeyCode = root.data.hashCode();
        if (keyCode < rootKeyCode) {
            boolean result = search(root.left, key);
            return result;
        }
        if (keyCode > rootKeyCode) {
            boolean result = search(root.right, key);
            return result;
        }
        return true;
    }

    public void insert(Pair<K, V> data) {
        root = insert(root, data);
    }

    private TreeNode<Pair<K, V>> insert(
            TreeNode<Pair<K, V>> root,
            Pair<K, V> data) {
        if (root == null) { // create new node at target location
            size++;
            return new TreeNode<Pair<K, V>>(data);
        }
        if (data.compare(root.data) < 0) { // target in left subtree
            root.left = insert(root.left, data);
        } else if (data.compare(root.data) > 0) { // target in right subtree
            root.right = insert(root.right, data);
        } else { // target exists, put new pair in that place
            root = new TreeNode<Pair<K, V>>(data);
            return root;
        }
        root.height = 1 + Math.max(
                height(root.left),
                height(root.right)); // update height for balanceFactor purpose
        int rootBalanceFactor = getBalanceFactor(root);
        if (rootBalanceFactor > 1) { // if left subtree is unbalanced
            if (data.compare(root.left.data) > 0) { // LR case
                root.left = leftRotate(root.left);
            }
            root = rightRotate(root); // right rotation necessary in both cases
            return root;
        }
        if (rootBalanceFactor < -1) { // if right subtree is unbalanced
            if (data.compare(root.right.data) < 0) { // RL case
                root.right = rightRotate(root.right);
            }
            root = leftRotate(root); // left rotation necessary in both cases
            return root;
        }
        return root;
    }

    private int getBalanceFactor(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return 0;
        }
        int result = height(root.left) - height(root.right);
        return result;
    }

    private int height(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return -1;
        }
        return root.height;
    }

    private TreeNode<Pair<K, V>> leftRotate(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return root;
        }
        if (root.right == null) {
            return root;
        }
        TreeNode<Pair<K, V>> rightChild = root.right;
        root.right = rightChild.left;
        rightChild.left = root;
        root.height = 1 + Math.max(
                height(root.left),
                height(root.right));
        rightChild.height = 1 + Math.max(
                height(rightChild.left),
                height(rightChild.right));
        return rightChild;
    }

    private TreeNode<Pair<K, V>> rightRotate(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return root;
        }
        if (root.left == null) {
            return root;
        }
        TreeNode<Pair<K, V>> leftChild = root.left;
        root.left = leftChild.right;
        leftChild.right = root;
        root.height = Math.max(height(root.left), height(root.right)) + 1;
        leftChild.height = 1 + Math.max(
                height(leftChild.left),
                height(leftChild.right));
        return leftChild;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        sb.append(preorder(root));
        sb.append("]");
        String result = sb.toString();
        return result;
    }

    private String preorder(TreeNode<Pair<K, V>> root) {
        if (root == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        sb.append(root.data);
        String leftResult = preorder(root.left);
        String rightResult = preorder(root.right);
        boolean leftEmpty = leftResult.equals("");
        boolean rightEmpty = rightResult.equals("");
        if (leftEmpty && rightEmpty) {
            String result = sb.toString();
            return result;
        }
        if (!leftEmpty) {
            sb.append(", ");
            sb.append(leftResult);
        }
        if (!rightEmpty) {
            sb.append(", ");
            sb.append(preorder(root.right));
        }
        String result = sb.toString();
        return result;
    }

    public Iterator<Pair<K, V>> iterator() {
        return new TreeMapIterator<K, V>(this.root);
    }

    public int size() {
        return size;
    }

    public void clear() {
        root = null;
    }
}

class TreeMapIterator<K, V> implements Iterator<Pair<K, V>> {
    Stack<TreeNode<Pair<K, V>>> nodeStack;
    TreeNode<Pair<K, V>> current;

    public TreeMapIterator(TreeNode<Pair<K, V>> root) {
        nodeStack = new Stack<>();
        current = root;
    }

    @Override
    public boolean hasNext() {
        return !nodeStack.isEmpty() || current != null;
    }

    @Override
    public Pair<K, V> next() {
        Pair<K, V> result = null;
        if (hasNext()) {
            while (current != null) {
                nodeStack.push(current);
                current = current.left;
            }
            current = nodeStack.pop();
            result = current.data;
            current = current.right;
        }
        return result;
    }
}

class TreeNode<T> {
    public T data;
    int height;
    public TreeNode<T> left, right;

    public TreeNode(T data) {
        this.data = data;
        height = 0;
        left = right = null;
    }
}