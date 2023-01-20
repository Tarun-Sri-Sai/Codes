import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class RabinKarp {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        for (int T = Integer.parseInt(br.readLine()); T > 0; T--) {
            String[] I = br.readLine().split(" ");
            String B = I[0], A = I[1];
            bw.write(solve(A, A.length(), B, B.length()) + "\n");
        }
        bw.flush();
    }

    static int solve(String A, int N, String B, int M) {
        long p = 31, q = 57, mod = (long) 1e9 + 7;
        long hA1 = 0, hB1 = 0, p1 = p, p2 = p;
        long hA2 = 0, hB2 = 0, q1 = q, q2 = q;
        int count = 0;
        for (int i = 0; i < M; i++) {
            hA1 = (hA1 + (A.charAt(i) * p1) % mod) % mod;
            hB1 = (hB1 + (B.charAt(i) * p1) % mod) % mod;
            hA2 = (hA2 + (A.charAt(i) * q1) % mod) % mod;
            hB2 = (hB2 + (B.charAt(i) * q1) % mod) % mod;
            p1 = (p1 * p) % mod;
            q1 = (q1 * q) % mod;
        }

        if (hA1 == hB1 && hA2 == hB2) {
            count++;
        }

        for (int i = M; i < N; i++) {
            hA1 = (hA1 - (A.charAt(i - M) * p2) % mod + (A.charAt(i) * p1) % mod + mod) % mod;
            hA2 = (hA2 - (A.charAt(i - M) * q2) % mod + (A.charAt(i) * q1) % mod + mod) % mod;
            hB1 = (hB1 * p) % mod;
            hB2 = (hB2 * q) % mod;
            p1 = (p1 * p) % mod;
            p2 = (p2 * p) % mod;
            q1 = (q1 * q) % mod;
            q2 = (q2 * q) % mod;
            if (hA1 == hB1 && hA2 == hB2) {
                count++;
            }
        }
        return count;
    }
}