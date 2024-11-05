import java.util.ArrayList;
import java.util.Objects;
import java.util.Scanner;
import java.util.StringJoiner;
import java.lang.Comparable;

public class Main{

    public static double SearchMaxCircleDoubleArr(Circle[][] arr) {
        Circle max = new Circle();
        for (Circle[] i : arr ){
            for (Circle j : i){
                if (max.compareTo(j) < 0){
                        max = j;
                }
            }
        }
        return max.getRadius();
    }

    public static double SearchMaxCircle(ArrayList<Circle> arr){
        Circle max = new Circle();
        for (Circle s : arr){
            if (max.compareTo(s) < 0){
                max = s;
            }
        }
        return max.getRadius();
    }

    public static ArrayList<String> ArrWithoutDuplicates(ArrayList<String> arr){
        ArrayList<String> arr1 = new ArrayList<String>();
        for (String s : arr) {
            if (arr1.contains(s)) {
                continue;
            } else {
                arr1.add(s);
            }
        }
        return arr1;
    }

    public static int ArrSearch(String value, ArrayList<String> arr){
        int x = -1;
        for (int i = 0; i < arr.size(); i++) {
            if (Objects.equals(arr.get(i), value)) {
                x = i;
            }
        }
        return x;
    }

    public static void main(String[] args) {
        //Задание1.1
        ArrayList<String> arr = new ArrayList<String>();
        arr.add("ha");
        arr.add("ho");
        arr.add("ho");
        arr.add("ho");
        arr.add("hi");
        arr.add("lala");
        System.out.println(ArrWithoutDuplicates(arr));

        //Задание1.2
        ArrayList<String> arrry = new ArrayList<String>();
        arrry.add("ha");
        arrry.add("ho");
        arrry.add("hi");
        arrry.add("he");
        System.out.println(ArrSearch("hi", arrry));

        //Задание1.3
        ArrayList<Circle> arr1 = new ArrayList<Circle>();
        arr1.add(new Circle(12));
        arr1.add(new Circle(14));
        arr1.add(new Circle(18));

        System.out.println(SearchMaxCircle(arr1));

        //Задание1.4
        Circle[][] array = new Circle[2][2];
        array[0][0] = new Circle(3);
		array[0][1] = new Circle(5);
		array[1][0] = new Circle(1);
		array[1][1] = new Circle(2);

        System.out.println(SearchMaxCircleDoubleArr(array));

        //Задание2
        Scanner input = new Scanner(System.in);
        System.out.println("Введите 5 строк, разделяя их с Enter");
        Stack2<String> stringsArr = new Stack2<String>();
        for (int i = 0; i < 5; i++) stringsArr.push(input.nextLine());

        ArrayList<String> resultStrings = new ArrayList<String>();
        while (!stringsArr.isEmpty()) {
            resultStrings.add(stringsArr.pop());
        }
        System.out.println(resultStrings.toString());
    }
}
