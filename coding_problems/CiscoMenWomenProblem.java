
//  Men-Women Problem
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class CiscoMenWomenProblem {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        String S = br.readLine();
        int n = S.length(), maxlen = 0, wc = 0, mc = 0;
        for (int i = 0; i < n; i++) {
            char curr = S.charAt(i);
            if (curr == 'M')
                mc++;
            else
                wc++;
            if (i == n - 1 || curr != S.charAt(i + 1)) {
                maxlen = Math.max(maxlen, 2 * (int) Math.min(mc, wc));
                if (curr == 'M')
                    wc = 0;
                else
                    mc = 0;
            }
        }
        bw.write(maxlen + "\n");
        bw.flush();
    }
}