package app;
import vehicles.Car;
import vehicles.ElectricCar;

import java.util.Scanner;

public class TestCar {
    public static void main(String[] args) {

        Car car1 = new Car("Lada", 22, "red", 2, "Tim", 32);
        ElectricCar car2 = new ElectricCar("Mockvich", 44, "blue", 1, "B", 122,2000);

        car1.setYear(4);
        car2.setOwnerName("Vlad");

        car2.setInsuranceNumber(2233);

        System.out.println("BatteryCapacity = " + car2.getBatteryCapacity());

        System.out.println(car1.toString());
        System.out.println(car2.toString());
    }
}

