import java.util.ArrayList;

public class Circle {
    public double radius;

    public Circle(double radius){
        this.radius = radius;
    }

    public Circle(){
        this.radius = 0;
    }

    public double getRadius(){
        return radius;
    }

    public double compareTo(Circle o){
        return radius - o.radius;
    }

}
