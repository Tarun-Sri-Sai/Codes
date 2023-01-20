import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class EmptyLineRemover {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("../Text-Files/Input.txt"));
        BufferedWriter bw = new BufferedWriter(new FileWriter("../Text-Files/Output.txt"));
        String line = br.readLine();
        int count = 0;
        final int LIM = (int) 1e5;
        while (line != null) {
            if (count++ > LIM) {
                break;
            }
            // System.err.println("Last line read: " + line); // debug
            if (!line.isEmpty()) {
                bw.write(line + "\n");
                // System.err.println("Printed this line: " + line); // debug
            }
            line = br.readLine();
        }
        br.close();
        bw.close();
    }
}