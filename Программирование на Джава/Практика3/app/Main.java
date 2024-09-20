package app;
import vehicles.Car;
import vehicles.ElectricCar;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        Car car2 = new Car("ownerNamecar2", 2, "engineType");
        ElectricCar car3 = new ElectricCar("ownerName", 3, 2000);

        System.out.println(car2.getOwnerName());
        System.out.println(car2.getInsuranceNumber());

        car3.setOwnerName("ownerNamecar3");
        System.out.println(car3.getOwnerName());
        System.out.println(car3.getInsuranceNumber());
        
        System.out.println(car3.getEngineType());

    }
}
