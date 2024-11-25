//Вариант 5

// Абстрактный класс с методом createOrder(), который реализуют подклассы.
abstract class DeliveryService {
    public abstract Order createOrder();

    public void deliver() {
        Order order = createOrder();
        System.out.println("Доставка: " + order.getDescription());
    }
}

// Класс для заказов.
abstract class Order {
    public abstract String getDescription();
}

// Класс для доставки пиццы
class PizzaOrder extends Order {
    public String getDescription() {
        return "Пицца";
    }
}

// Класс для доставки продуктов
class GroceryOrder extends Order {
    public String getDescription() {
        return "Продукты";
    }
}

// Конкретный сервис доставки пиццы
class PizzaDelivery extends DeliveryService {
    public Order createOrder() {
        return new PizzaOrder();
    }
}

// Конкретный сервис доставки продуктов
class GroceryDelivery extends DeliveryService {
    public Order createOrder() {
        return new GroceryOrder();
    }
}

// Тестирование
public class Main {
    public static void main(String[] args) {
        // Сервис доставки пиццы
        DeliveryService pizzaDelivery = new PizzaDelivery();
        pizzaDelivery.deliver();

        // Сервис доставки продуктов
        DeliveryService groceryDelivery = new GroceryDelivery();
        groceryDelivery.deliver();
    }
}
