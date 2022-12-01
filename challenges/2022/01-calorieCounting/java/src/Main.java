import java.io.FileNotFoundException;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        Challenge c = new Challenge("input.txt");
        System.out.println(c.partOne());
        System.out.println(c.partTwo());
    }
}