import static java.lang.Math.sqrt;

public class Triangle extends GeometricObject implements Colorable{
    private double side1;
    private double side2;
    private double side3;

    public Triangle(){
        this.side1 = 1.0;
        this.side2 = 1.0;
        this.side3 = 1.0;
        setFilled(false);
    }
    public Triangle(double side1, double side2, double side3) throws IllegalAccessException {
        if (side1 + side2 <= side3 || side1 + side3 <= side2 || side2 + side3 <= side1) {
            throw new IllegalAccessException("Третья сторона не может быть больше суммы двух других");
        }
        this.side1 = side1;
        this.side2 = side2;
        this.side3 = side3;
        setFilled(false);
    }

    public double getSide1(){
        return side1;
    }
    public double getSide2(){
        return side2;
    }
    public double getSide3(){
        return side3;
    }
    public double getArea(){
        double s = (side1 + side2 + side3)/2;
        return sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }

    public double getPerimeter(){
        return side1 + side2 + side3;
    }

    public String toString() {
        return "Треугольник: сторона1 = " + side1 + " сторона2 = " + side2 + " сторона3 = " + side3;
    }

    public void SetSide1(double side1){
        this.side1 = side1;
    }
    public void SetSide2(double side2){
        this.side2 = side2;
    }
    public void SetSide3(double side3){
        this.side3 = side3;
    }

    public void howToColor() {
        System.out.println("Раскрасьте все три стороны.");
    }
}
