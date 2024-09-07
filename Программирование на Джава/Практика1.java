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
        roubles = Math.ceil(roubles);

        double digit = yuan % 10;

        if (yuan == 1){
            System.out.println("У вас 1 китайский Юань, " + "это " + roubles + " руб:");
        }else if (digit > 1 && digit < 5 && yuan > 19 || yuan < 5) {
             System.out.println("У вас "+ yuan + " китайских Юаня - " + "это " + roubles + " руб:");
        }else {
            System.out.println("У вас "+ yuan + " китайских Юаней - " + "это " + roubles + " руб:");
        }
    }
}
