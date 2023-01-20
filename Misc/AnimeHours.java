
//  Program to find watchtime from episodes
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class AnimeHours {
    public static void main(String[] args) throws IOException {
        final String inputPath = "../Text-Files/Input.txt", outputPath = "../Text-Files/Output.txt";
        BufferedReader br = new BufferedReader(new FileReader(inputPath));
        BufferedWriter bw = new BufferedWriter(new FileWriter(outputPath));
        String line = null;
        float sum = 0;
        boolean print = false;
        while ((line = br.readLine()) != null) {
            if (line.contains("Coming up:")) {
                print = true;
            }
            String[] words = line.split(" ");
            if (line.contains("Total watchtime:")) {
                continue;
            }
            if (!line.contains("hrs")) {
                for (int i = 0; i < words.length; ++i) {
                    if (words[i].matches("\\d+") && i == words.length - 1) {
                        StringBuilder sb = new StringBuilder("(");
                        float val = Float.parseFloat(words[i]) / 3F;
                        sum += val;
                        sb.append(String.format("%.2f", val));
                        sb.append(" hrs)");
                        words[i] = sb.toString();
                    }
                }
                if (!print) {
                    bw.write(line + "\n");
                    continue;
                }
                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < words.length; ++i) {
                    sb.append(words[i]);
                    sb.append(" ");
                }
                bw.write(sb.toString() + "\n");
            } else {
                sum += Float.parseFloat(words[words.length - 2].substring(1));
                bw.write(line + "\n");
            }
        }
        bw.write(String.format("Total watchtime: %.2f hrs", sum));
        System.err.println("Finished writing to " + outputPath);
        br.close();
        bw.close();
    }
}