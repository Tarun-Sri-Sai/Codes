
//  Tree Visualizer
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class TreeVisualizer {
    static Scanner sc;
    static BufferedWriter bw;

    public static void main(String[] args) throws IOException {
        sc = new Scanner(System.in);
        bw = new BufferedWriter(new OutputStreamWriter(System.out));
        Random random = new Random(System.currentTimeMillis());
        HashSet<Integer> hs = new HashSet<>();
        final int SIZE = 6;
        while (hs.size() < SIZE) {
            hs.add(random.nextInt(1000));
        }
        Tree root = null;
        for (int ele : hs) {
            root = Tree.insertInto(root, ele);
        }
        bw.write(Tree.toString(root) + "\n\n");
        root = Tree.getBalanced(root);
        bw.write(Tree.toString(root) + "\n");
        sc.close();
        bw.flush();
    }
}

class Tree {
    int data;
    Tree left, right;
    private static final int MAX_HEIGHT = 15;
    private static int[] startSpacing = null, middleSpacing = null;

    Tree(int data) {
        this.data = data;
        left = right = null;
    }

    private static void init() {
        startSpacing = new int[MAX_HEIGHT];
        startSpacing[0] = 0;
        for (int i = 1; i < 10; i++) {
            startSpacing[i] = startSpacing[i - 1] * 2 + 2;
        }
        middleSpacing = new int[MAX_HEIGHT];
        middleSpacing[0] = 1;
        for (int i = 1; i < 10; i++) {
            middleSpacing[i] = middleSpacing[i - 1] + (1 << (i + 1));
        }
    }

    static Tree insertInto(Tree root, int data) {
        if (root == null) {
            return new Tree(data);
        }
        if (data < root.data) {
            root.left = insertInto(root.left, data);
        }
        if (data > root.data) {
            root.right = insertInto(root.right, data);
        }
        return root;
    }

    static String toString(Tree root) {
        StringBuilder result = new StringBuilder();
        if (startSpacing == null || middleSpacing == null) {
            init();
        }
        List<List<Tree>> levelList = getLevelOrder(root);
        int maxDepth = levelList.size() - 1;
        for (int i = 0; i <= maxDepth; i++) {
            List<Tree> nodeList = levelList.get(i);
            int currentHeight = maxDepth - i;
            result.append(new String(new char[startSpacing[currentHeight]]).replace("\0", " "));
            String middleSpace = new String(new char[middleSpacing[currentHeight]]).replace("\0", " ");
            for (int size = nodeList.size(), j = 0; j < size; j++) {
                String dataString = nodeList.get(j) == null ? "   " : String.format("%3d", nodeList.get(j).data);
                result.append(dataString);
                if (j < size - 1) {
                    result.append(middleSpace);
                }
            }
            result.append(new String(new char[currentHeight]).replace("\0", "\n"));
        }
        return result.toString();
    }

    private static List<List<Tree>> getLevelOrder(Tree root) {
        List<List<Tree>> result = new ArrayList<>();
        result.add(new ArrayList<>(Arrays.asList(root)));
        int currentDepth = 0;
        while (currentDepth < result.size()) {
            List<Tree> currentList = result.get(currentDepth++);
            List<Tree> nextList = new ArrayList<>();
            for (Tree currentNode : currentList) {
                nextList.add(currentNode != null ? currentNode.left : null);
                nextList.add(currentNode != null ? currentNode.right : null);
            }
            if (notAllNull(nextList))
                result.add(nextList);
        }
        return result;
    }

    private static boolean notAllNull(List<Tree> list) {
        for (Tree ele : list) {
            if (ele != null) {
                return true;
            }
        }
        return false;
    }

    static Tree getBalanced(Tree root) {
        List<Tree> nodes = new ArrayList<>();
        storeBSTNodes(root, nodes);
        int size = nodes.size();
        return recursiveBalance(nodes, 0, size - 1);
    }

    private static Tree recursiveBalance(List<Tree> nodes, int start, int end) {
        if (start > end) {
            return null;
        }
        int mid = start + (end - start) / 2;
        Tree node = nodes.get(mid);
        node.left = recursiveBalance(nodes, start, mid - 1);
        node.right = recursiveBalance(nodes, mid + 1, end);
        return node;
    }

    private static void storeBSTNodes(Tree root, List<Tree> nodes) {
        if (root == null) {
            return;
        }
        storeBSTNodes(root.left, nodes);
        nodes.add(root);
        storeBSTNodes(root.right, nodes);
    }
}