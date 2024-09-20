package app;
import vehicles.Car;
import vehicles.ElectricCar;
import java.util.Scanner;


public class Main {
    public static void main(String[] args) {
        Car car2 = new Car("Бебебе", 32, "PAS");
        Scanner input = new Scanner(System.in);
        System.out.println(car2.getOwnerName());

        ElectricCar car3 = new ElectricCar("Ляляля", 3, 2000);
        System.out.println(car3.getInsuranceNumber());

        car3.setOwnerName("аспро");
        System.out.println(car3.getOwnerName());

    }
}
