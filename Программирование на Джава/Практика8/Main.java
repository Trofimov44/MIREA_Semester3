import java.util.Scanner;
public class Main {
    public static void main(String[] args) {//main для задания 1 и 3
        Scanner input = new Scanner(System.in);
        int x = -1;
        String[] months = {"январь", "февраль", "март", "апрель", "май",
            "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"};
        int[] dom = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        System.out.println("Введите номер месяца: ");
        try {
            int year;
           x = input.nextInt() - 1;
           if (x == 1){
               System.out.println("Введите какой год: ");
               year = input.nextInt();
               System.out.println("Месяц: " + months[x] + "," + "Кол-во дней: " +(year % 4 == 0? dom[x] + 1: dom[x]));
           } else if (x < 0 || x > months.length) {
               throw new ArrayIndexOutOfBoundsException("Недопустимое число");
           }
           else {
                System.out.println("Месяц: " + months[x] + " " + "Кол-во дней: " + dom[x]);
           }
        }
        catch (Exception e){
            System.out.println("Недопустимое число");
        }
    }
}
