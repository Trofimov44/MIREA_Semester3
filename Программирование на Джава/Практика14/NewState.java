class NewState implements State {
    public void handle() {
        System.out.println("Заказ создан. Ожидание обработки.");
    }
}

class ProcessingState implements State {
    public void handle() {
        System.out.println("Заказ обрабатывается.");
    }
}

class ShippedState implements State {
    public void handle() {
        System.out.println("Заказ отправлен.");
    }
}

class DeliveredState implements State {
    public void handle() {
        System.out.println("Заказ доставлен.");
    }
}
