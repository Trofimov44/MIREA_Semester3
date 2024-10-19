public class Square extends GeometricObject implements Colorable{
    public double side = 0;

    public Square(){
    }
    public Square(double side){
        this.side = side;
    }

    public void howToColor() {
        System.out.println("Раскрасьте все четыре стороны.");
    }

    public void SetSide(double side){
        this.side = side;
    }
    public double GetSide(){
        return side;
    }

    public double getArea() {
        return side * side;
    }
}
