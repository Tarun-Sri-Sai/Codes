
//  TreeNode Visualizer
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class TreeVisualizer {
    private TreeNode root;
    private final int MAX_HEIGHT = 15;
    private int[] startSpacing = null, middleSpacing = null;

    public TreeVisualizer(TreeNode root) {
        this.root = root;
        startSpacing = new int[MAX_HEIGHT];
        startSpacing[0] = 0;
        for (int i = 1; i < 10; ++i) {
            startSpacing[i] = startSpacing[i - 1] * 2 + 2;
        }
        middleSpacing = new int[MAX_HEIGHT];
        middleSpacing[0] = 1;
        for (int i = 1; i < 10; ++i) {
            middleSpacing[i] = middleSpacing[i - 1] + (1 << (i + 1));
        }
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        List<List<TreeNode>> levelList = getLevelOrder();
        int maxDepth = levelList.size() - 1;
        for (int i = 0; i <= maxDepth; ++i) {
            List<TreeNode> nodeList = levelList.get(i);
            int currentHeight = maxDepth - i;
            result.append(new String(new char[startSpacing[currentHeight]]).replace("\0", " "));
            String middleSpace = new String(new char[middleSpacing[currentHeight]]).replace("\0", " ");
            for (int size = nodeList.size(), j = 0; j < size; ++j) {
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

    private List<List<TreeNode>> getLevelOrder() {
        List<List<TreeNode>> result = new ArrayList<>();
        result.add(new ArrayList<>(Arrays.asList(root)));
        int currentDepth = 0;
        while (currentDepth < result.size()) {
            List<TreeNode> currentList = result.get(currentDepth++);
            List<TreeNode> nextList = new ArrayList<>();
            for (TreeNode currentNode : currentList) {
                if (currentNode.left != null) {
                    nextList.add(currentNode.left);
                }
                if (currentNode.right != null) {
                    nextList.add(currentNode.right);
                }
            }
            if (nextList.size() > 0) {
                result.add(nextList);
            }
        }
        return result;
    }
}