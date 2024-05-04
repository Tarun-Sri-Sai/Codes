import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;

public class ClearMultipleSpaces {
    public static void main(String[] args) throws IOException {
        BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in));

        System.out.println("Current directory\t: " + System.getProperty("user.dir"));
        System.out.print("Input file path\t\t: ");
        String inputFile = stdIn.readLine().trim();

        System.out.print("Output file path\t: ");
        String outputFile = stdIn.readLine().trim();
        BufferedReader fileIn = new BufferedReader(new FileReader(inputFile));
        BufferedWriter fileOut = new BufferedWriter(new FileWriter(outputFile));
        String line = fileIn.readLine();

        while (line != null) {
            if (line.length() == 0) {
                line = fileIn.readLine();
                continue;
            }
            line = line.trim();
            if (line.length() == 0) {
                line = fileIn.readLine();
                continue;
            }
            line = line.replaceAll("[\n\t ]+", " ");
            fileOut.write(line);
            line = fileIn.readLine();
            if (line == null) {
                fileOut.write("\n");
                break;
            }
            fileOut.write(" ");
        }
        fileIn.close();
        fileOut.close();
    }
}