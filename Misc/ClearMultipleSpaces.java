import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class ClearMultipleSpaces {
    public static void main(String[] args) throws IOException {
        String inputFile = "Text Files/InputTest.txt";
        String outputFile = "Text Files/Output.txt";
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