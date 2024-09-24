package app;
import vehicles.Car;
import vehicles.ElectricCar;
import vehicles.Vehicle;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        Car car2 = new Car("model", 22, "red", 2, "a", 32, "eT");
        ElectricCar car3 = new ElectricCar("model2", 44, "blue", 1, "b", 122,2000);

        System.out.println(car2.getOwnerName());
        System.out.println(car2.getInsuranceNumber());
        System.out.println(car3.getOwnerName());
        System.out.println(car3.getInsuranceNumber());

        System.out.println(car3.getEngineType());

        System.out.println(car2.vehicleType());
        System.out.println(car3.toString());

    }
}
