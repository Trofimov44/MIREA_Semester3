//Задача1 и Задача2
import java.util.Scanner;

public class test1 {
    public static void main(String[] args){
        int yuan;
        double roubles;
        final float ROUBLES_PER_YUAN = 11.91f;

        Scanner scanner = new Scanner(System.in);
        System.out.println("Введите Кол-во Юаней: ");
        yuan = scanner.nextInt();
        roubles = ROUBLES_PER_YUAN * yuan;

        if (yuan == 1){
            System.out.println("У вас 1 китайский Юань " + "это " + roubles + " рублей:");
        }else if (yuan == 2 || yuan == 3 || yuan == 4 ){
             System.out.println("У вас "+ yuan + " китайских Юаня " + "это " + roubles + " рублей:");
        }else {
            System.out.println("У вас "+ yuan + " китайских Юаней " + "это " + roubles + " рублей:");
        }
    }
}
