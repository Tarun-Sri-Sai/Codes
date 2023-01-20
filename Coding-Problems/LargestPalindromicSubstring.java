import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class LargestPalindromicSubstring {
    static long mod = (long) 1e9 + 7;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        for (int T = Integer.parseInt(br.readLine()); T > 0; T--) {
            int N = Integer.parseInt(br.readLine());
            String S = br.readLine();
            bw.write(largePalSub(S, N) + "\n");
        }
        bw.flush();
    }

    static int largePalSub(String S, int N) {
        int p = 31;
        long[] pow = new long[N + 1];
        long[] fHash = new long[N], bHash = new long[N];
        findPreReq(S, N, p, pow, fHash, bHash);

        int ans = 0;

        int oddMax = 0;
        for (int i = 0; i < N; i++) {
            int p1 = i - oddMax, p2 = i + oddMax;
            if (valid(S, N, p1, p2, pow, fHash, bHash)) {
                while (p1 >= 0 && p2 < N && S.charAt(p1) == S.charAt(p2)) {
                    ans = Math.max(ans, p2 - p1 + 1);
                    p1--;
                    p2++;
                    oddMax++;
                }
            }
        }

        int evenMax = 0;
        for (int i = 0; i < N; i++) {
            int p1 = i - evenMax, p2 = i + evenMax + 1;
            if (valid(S, N, p1, p2, pow, fHash, bHash)) {
                while (p1 >= 0 && p2 < N && S.charAt(p1) == S.charAt(p2)) {
                    ans = Math.max(ans, p2 - p1 + 1);
                    p1--;
                    p2++;
                    evenMax++;
                }
            }
        }
        return ans;
    }

    static void findPreReq(String S, int N, int p, long[] pow, long[] fHash, long[] bHash) {
        for (int i = 0; i < N; i++) {
            pow[i + 1] = (long) Math.pow(p, i + 1) % mod;
        }

        fHash[0] = (S.charAt(0) * p) % mod;
        for (int i = 1; i < N; i++) {
            fHash[i] = ((S.charAt(i) * pow[i + 1]) % mod + fHash[i - 1]) % mod;
        }

        bHash[N - 1] = (S.charAt(N - 1) * p) % mod;
        for (int i = N - 2; i >= 0; i--) {
            bHash[i] = ((S.charAt(i) * pow[N - i]) % mod + bHash[i + 1]) % mod;
        }
    }

    static boolean valid(String S, int N, int p1, int p2, long[] pow, long[] fHash, long[] bHash) {
        if (p1 < 0 || p1 >= N || p2 < 0 || p2 >= N) {
            return false;
        }

        int i = p1, j = p2, k = N - p2 - 1, l = N - p1 - 1;
        long fH = fHash[j], bH = bHash[l];
        if (i > 0) {
            fH = (fH - fHash[i - 1] + mod) % mod;
        }
        if (k < N - 1) {
            bH = (bH - bHash[k + 1] + mod) % mod;
        }
        int diff = k - i;
        if (diff < 0) {
            bH = (bH * pow[Math.abs(diff)]) % mod;
        } else {
            fH = (fH * pow[diff]) % mod;
        }
        return (fH == bH);
    }
}