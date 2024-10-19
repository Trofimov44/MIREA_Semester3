import java.io.ObjectInputStream;
import java.sql.SQLOutput;
import java.util.Scanner;
public class TestCircleRectangle {
    public static void main(String[] args) throws IllegalAccessException {
        Circle circle = new Circle(1);
        Circle circle1 = new Circle(3);

        Rectangle rectangle = new Rectangle(2, 4);
        Rectangle rectangle1 = new Rectangle(3, 4);

        System.out.println(Rectangle.max(rectangle1, rectangle));//Такое себе, но пойдёт
        System.out.printf(Circle.max(circle, circle1) + "\n");
        System.out.println(GeometricObject.compareTo(circle, rectangle));
        Scanner input = new Scanner(System.in);
        double side1;
        double side2;
        double side3;
        String color = "color";
        boolean isFilled;
        int x = 1;

        System.out.println("Введите сторону 1: ");
        side1 = input.nextDouble();
        System.out.println("Введите сторону 2: ");
        side2 = input.nextDouble();
        System.out.println("Введите сторону 3: ");
        side3 = input.nextDouble();
        Triangle Triangle1 = new Triangle(side1, side2, side3);


        System.out.println("Введите цвет: ");
        input.nextLine();
        color = input.nextLine();
        Triangle1.setColor(color);
        System.out.println("Залит ли объект? (1-да, 0-нет): ");
        Scanner input2 = new Scanner(System.in);
        x = input2.nextInt();
        if (x == 1){
            Triangle1.setFilled(true);
        } else{ Triangle1.setFilled(false); }

        System.out.printf(Triangle1.toString() + "\n");
        System.out.printf("Цвет: " + Triangle1.getColor() + "\n");
        System.out.println("Заливка: " + Triangle1.isFilled());
        System.out.printf("Периметр: " + Triangle1.getPerimeter() + "\n");
        System.out.println("Площадь: " + Triangle1.getArea() + "\n");

        GeometricObject[] GeomOdj = new GeometricObject[5];
        GeomOdj[0] = new Circle(4);
        GeomOdj[1] = new GeometricObject();
        GeomOdj[2] = new Rectangle(3, 7);
        GeomOdj[3] = new Triangle(3, 4, 5);
        GeomOdj[4] = new Square(4);

        GeomOdj[0].howToColor();
        GeomOdj[1].howToColor();
        GeomOdj[2].howToColor();
        GeomOdj[3].howToColor();
        GeomOdj[4].howToColor();
        System.out.println(" ");

        System.out.println(GeomOdj[0].getArea());
        System.out.println(GeomOdj[1].getArea());
        System.out.println(GeomOdj[2].getArea());
        System.out.println(GeomOdj[3].getArea());
        System.out.println(GeomOdj[4].getArea());
    }
}
