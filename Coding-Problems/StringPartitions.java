import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class StringPartitions {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        String[] inp = br.readLine().split(" ");
        String s = br.readLine();
        if (hasPartitions(s, inp, 0)) {
            bw.write("YES\n");
        } else {
            bw.write("NO\n");
        }
        bw.flush();
    }

    private static boolean hasPartitions(String s, String[] inp, int idx) {
        if (idx == s.length()) {
            return true;
        }
        for (int i = idx; i < s.length(); i++) {
            if (isInArray(s.substring(idx, i + 1), inp) && hasPartitions(s, inp, i + 1)) {
                return true;
            }
        }
        return false;
    }

    private static boolean isInArray(String s, String[] inp) {
        for (String ele : inp) {
            if (ele.equals(s)) {
                return true;
            }
        }
        return false;
    }
}