import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Challenge {
    private ArrayList<Integer> parsedInput;

    public Challenge(String filename) throws FileNotFoundException {
        parsedInput = new ArrayList<>();

        File inputFile = new File(filename);
        Scanner reader = new Scanner(inputFile);

        int acc = 0;
        while (reader.hasNextLine()) {
            String thisLine = reader.nextLine();

            if ("".equals(thisLine)) {
                if (acc != 0) {
                    parsedInput.add(acc);
                    acc = 0;
                }
            } else {
                acc += Integer.parseInt(thisLine);
            }
        }

        reader.close();
    }

    public int partOne() {
        int largest = 0;
        for (Integer x : parsedInput) {
            if (x > largest) {
                largest = x;
            }
        }
        return largest;
    }

    public int partTwo() {
        ArrayList<Integer> clonedInput = (ArrayList<Integer>) parsedInput.clone();
        clonedInput.sort(Integer::compareTo);
        int acc = 0;
        for (int i = clonedInput.size()-1; i >= clonedInput.size() - 3; i -= 1) {
            acc += clonedInput.get(i);
        }
        return acc;
    }

}