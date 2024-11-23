
//  Recursive Backtracking
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class CabinetPartitioning {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        String[] inp = br.readLine().split(" ");
        int n = Integer.parseInt(inp[0]), k = Integer.parseInt(inp[1]), sum = 0;
        inp = br.readLine().split(" ");
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(inp[i]);
            sum += arr[i];
        }
        List<Integer> result = new ArrayList<>();
        findAllTimes(result, arr, n, k, 0, new ArrayList<>());
        int min = sum;
        for (int ele : result) {
            min = Math.min(min, ele);
        }
        bw.write(min + "\n");
        bw.flush();
    }

    private static void findAllTimes(List<Integer> result, int[] arr, int n, int k, int idx, List<Integer> temp) {
        if (temp.size() <= k && idx == n) {
            int max = temp.get(0);
            for (int ele : temp) {
                max = Math.max(max, ele);
            }
            result.add(max);
            temp.clear();
            return;
        }
        for (int i = idx; i < n; i++) {
            int sum = 0;
            for (int j = idx; j <= i; j++) {
                sum += arr[j];
            }
            temp.add(sum);
            findAllTimes(result, arr, n, k, i + 1, new ArrayList<>(temp));
            temp.remove(temp.size() - 1);
        }
    }
}