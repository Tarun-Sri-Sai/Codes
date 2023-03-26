
//  Program to find watchtime from episodes
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;

public class AnimeHours {
    private static BufferedReader stdIn;
    public static void main(String[] args) throws IOException {
        stdIn = new BufferedReader(new InputStreamReader(System.in));
        final String inputPath = stdIn.readLine(), outputPath = stdIn.readLine();
        BufferedReader fileIn = new BufferedReader(new FileReader(inputPath));
        BufferedWriter fileOut = new BufferedWriter(new FileWriter(outputPath));
        String line = null;
        float sum = 0;
        boolean switchToHours = false;

        while ((line = fileIn.readLine()) != null) {
            line = line.trim();
            if (line.contains("Finished:")) {
                switchToHours = true;
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
                        System.err.println("Added value: " + val + " for " + line);
                        sb.append(String.format("%.2f", val));
                        sb.append(" hrs)");
                        words[i] = sb.toString();
                    }
                }
                if (!switchToHours) {
                    fileOut.write(line + "\n");
                    continue;
                }
                StringBuilder sb = new StringBuilder();

                for (int i = 0; i < words.length; ++i) {
                    sb.append(words[i] + (i < words.length - 1 ? " " : ""));
                }
                fileOut.write(sb.toString() + "\n");
            } else {
                float val = Float.parseFloat(words[words.length - 2].substring(1));
                
                sum += val;
                System.err.println("Added value: " + val + " for " + line);
                fileOut.write(line + "\n");
            }
        }
        fileOut.write(String.format("Total watchtime: %.2f hrs", sum));
        System.err.println("Finished writing to " + outputPath);
        fileIn.close();
        fileOut.close();
    }
}