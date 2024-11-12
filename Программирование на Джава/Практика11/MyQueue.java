import java.util.ArrayList;

public class MyQueue<E> {
    private ArrayList<E> list = new ArrayList<>();
    private java.util.Date whenBuilt;
    // Возвращает размер стека
    public int getSize() {
        return list.size();
    }

    // Возвращает верхний элемент стека без удаления
    public E peek() {
        if (isEmpty()) {
            throw new IllegalStateException("Стек пуст");
        }
        return list.get(0);
    }

    // Добавляет элемент на верх стека
    public void push(E o) {
        list.add(o);
    }

    // Удаляет и возвращает верхний элемент стека
    public E pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Стек пуст");
        }
        E o = list.get(0);
        list.remove(0);
        return o;
    }

    // Проверяет, пуст ли стек
    public boolean isEmpty() {
        return list.isEmpty();
    }

 public Object clone() throws CloneNotSupportedException {
    // Сделать поверхностную копию
    MyQueue MyStackClone = (MyQueue)super.clone();
    // Сделать глубокую копию whenBuilt
    MyStackClone.whenBuilt = (java.util.Date)(whenBuilt.clone());
    return MyStackClone;
}

    @Override
    public String toString() {
        return "стек: " + list.toString();
    }
}
