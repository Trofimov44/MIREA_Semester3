import java.util.Scanner;
import java.util.TooManyListenersException;

public class Car {
    String model;
    String license;
    String color;
    int year;

    public Car(String model, String license, String color, int year){
        this.model = model;
        this.license = license;
        this.color = color;
        this.year = year;
    }
    public Car(){
        this.model = "Car";
        this.license = "license";
        this.color = "color";
        this.year = 0;
    }
    public Car(String model, String color){
        this.model = model;
        this.color = color;
    }

    public void To_string(){
        System.out.println(this.model + " " + this.license + " " + this.color + " " + this.year);
    }

    public void getName(int year){
        this.year = year;
    }

    public static void main(String[] args){
        Car model1 = new Car("Lada", "Gg", "red", 12);
        Car model2 = new Car();
        Car model3 = new Car("Moskvich", "green");

        model1.To_string();

        model3.getName(2);
        model3.To_string();

    }
}
