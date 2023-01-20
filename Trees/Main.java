import java.io.*;
import java.util.*;

public class Main {
    private static Scanner sc;
    private static BufferedWriter bw;

    public static void main(String[] args) throws IOException {
        sc = new Scanner(System.in);
        bw = new BufferedWriter(new OutputStreamWriter(System.out) );
        AVLTree avlTree = new AVLTree();
        Random random = new Random(System.currentTimeMillis());
        for (int i = 0; i < 10; ++i) {
            avlTree.insert(random.nextInt(100, 1000));
        }
        TreeVisualizer tv = new TreeVisualizer(avlTree.getRoot());
        System.out.println(tv);
        sc.close();
        bw.flush();
    }
}