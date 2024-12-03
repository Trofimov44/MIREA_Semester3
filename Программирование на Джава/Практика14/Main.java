public class Main {
    public static void main(String[] args) {
        Order order = new Order();

        State newState = new NewState();
        State processingState = new ProcessingState();
        State shippedState = new ShippedState();
        State deliveredState = new DeliveredState();

        // Переходы между состояниями
        order.setState(newState);
        order.processOrder();

        order.setState(processingState);
        order.processOrder();

        order.setState(shippedState);
        order.processOrder();

        order.setState(deliveredState);
        order.processOrder();
    }
}
