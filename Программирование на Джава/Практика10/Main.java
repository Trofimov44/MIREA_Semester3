import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println("Введите 5 строк, разделяя их с Enter");
        MyStack<String> stringsArr = new MyStack<String>();
        for (int i = 0; i < 5; i++) stringsArr.push(input.nextLine());

        ArrayList<String> resultStrings = new ArrayList<String>();
        while (!stringsArr.isEmpty()) {
            resultStrings.add(stringsArr.pop());
        }
        System.out.println(resultStrings.toString());

        ArrayList<String> clone = (ArrayList<String>) resultStrings.clone();

        System.out.println(clone.toString());
    }
}
