/*
 * In-Session:
 * Given an array 'arr', print the
 * number of pairs in arr, such that 
 * arr[i] > arr[j] as well as i < j
 * 
 * Sample Input:
 * 13
 * 8, 12, 20, 27, 4, 13, 6, -3, 16, 24, 5, 9, 2
 * Output:
 * 46
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class SmallerElements {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        int n = Integer.parseInt(br.readLine());
        String[] inp = br.readLine().split(" ");
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(inp[i]);
        }
        int result = MS(arr, 0, n - 1);
        bw.write(result + "\n");
        bw.flush();
    }

    private static int MS(int[] arr, int low, int high) {
        if (low >= high) {
            return 0;
        }
        int count = 0;
        int mid = low + (high - low) / 2;
        count += MS(arr, low, mid);
        count += MS(arr, mid + 1, high);
        count += merge(arr, low, mid, high);
        return count;
    }

    private static int merge(int[] arr, int low, int mid, int high) {
        int p1 = low;
        int p2 = mid + 1;
        int count = 0;
        while (p1 <= mid) {
            while (p2 <= high) {
                if (arr[p1] <= arr[p2]) {
                    break;
                }
                p2++;
            }
            p1++;
            if (p2 == mid + 1) {
                continue;
            }
            count += p2 - (mid + 1);
            p2--;
        }
        int[] temp = new int[high - low + 1];
        int k = 0;
        p1 = low;
        p2 = mid + 1;
        while (p1 <= mid && p2 <= high) {
            if (arr[p1] <= arr[p2]) {
                temp[k++] = arr[p1++];
            } else {
                temp[k++] = arr[p2++];
            }
        }
        while (p1 <= mid) {
            temp[k++] = arr[p1++];
        }
        while (p2 <= high) {
            temp[k++] = arr[p2++];
        }
        for (int i = low; i <= high; i++) {
            arr[i] = temp[i - low];
        }
        return count;
    }
}