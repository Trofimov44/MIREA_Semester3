package app;
import vehicles.Car;
import vehicles.ElectricCar;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.println();
        Car car2 = new Car("ownerNamecar2", 2, "engineType");
        ElectricCar car3 = new ElectricCar("ownerName3", 3, 2000);

        System.out.println(car2.getOwnerName());
        System.out.println(car2.getInsuranceNumber());
        System.out.println(car2.getEngineType());
        System.out.println(" ");
        System.out.println(car3.getOwnerName());
        System.out.println(car3.getInsuranceNumber());
        System.out.println(car3.getEngineType());
        System.out.println(car3.getBatteryCapacity());
    }
}
