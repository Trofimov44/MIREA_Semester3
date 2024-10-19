public class Rectangle extends GeometricObject implements Colorable{
    private double width;
    private double height;

    /** Создает по умолчанию заданный прямоугольник */
    public Rectangle() {
    }

    /** Создает прямоугольник с указанной шириной и высотой */
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    /** Создает прямоугольник с указанной шириной, высотой, цветом и заливкой */
    public Rectangle(double width, double height, String color, boolean filled) {
        this.width = width;
        this.height = height;
        setColor(color);
        setFilled(filled);
    }

    /** Возвращает ширину */
    public double getWidth() {
        return width;
    }

    /** Присваивает новую ширину */
    public void setWidth(double width) {
        this.width = width;
    }

    /** Возвращает высоту */
    public double getHeight() {
        return height;
    }

    /** Присваивает новую высоту */
    public void setHeight(double height) {
        this.height = height;
    }

    /** Возвращает площадь */
    public double getArea() {
        return width * height;
    }

    /** Возвращает периметр */
    public double getPerimeter() {
        return 2 * (width + height);
    }

    public static String max(Rectangle o1, Rectangle o2){
        if (o1.getArea() > o2.getArea()){
            return "Большим объектом является " + o1.getArea();
        }
        else{
            return "Большим объектом является " + o2.getArea();
        }
    }
        public void howToColor() {
        System.out.println("Раскрасьте все четыре стороны.");
    }
}
