/*
* Given an array of bricks of length 'm' ar, where ar[i]
* contains the length of brick type 'i'  and a minimum
* gap 'k' between two brick types, print all the possibilities
* of inserting bricks into a string of length 'n' as given in 
* sample output.
*
* Sample Input:
* 16 3 2
* 3 2 4
*
* Sample Output:
* 000__11__2222___
* 000___11__2222__
* 000____11__2222_
* 000_____11__2222
* {..truncated}
*/

import java.io.*;
import java.util.*;

public class PrintingBricks {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        String[] inp = br.readLine().split(" ");
        int n = Integer.parseInt(inp[0]), m = Integer.parseInt(inp[1]), k = Integer.parseInt(inp[2]);
        int bricks[] = new int[m];
        inp = br.readLine().split(" ");
        for (int i = 0; i < m; i++) {
            bricks[i] = Integer.parseInt(inp[i]);
        }
        char[] ar = new char[n];
        Arrays.fill(ar, '_');
        List<String> result = generate(ar, n, bricks, m, k, 0, 0);
        for (String str : result) {
            bw.write(str + "\n");
        }
        bw.flush();
    }

    private static List<String> generate(char[] a, int n, int[] b, int m, int k, int a_idx, int b_idx) {
        List<String> result = new ArrayList<String>();
        if (b_idx == m) {
            String res = "";
            for (char ch : a) {
                res += ch;
            }
            result.add(res);
            return result;
        }
        String s = Integer.toString(b_idx);
        for (int i = a_idx; i < n; i++) {
            if (i + b[b_idx] - 1 < n) {
                int j;
                for (j = i; j < i + b[b_idx]; j++) {
                    a[j] = s.charAt(0);
                }
                for (int l = j; l < n; l++) {
                    a[l] = '_';
                }
                result.addAll(generate(a, n, b, m, k, j + k, b_idx + 1));
                a[i] = '_';
            }
        }
        return result;
    }
}