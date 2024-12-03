class Order {
    private State currentState;

    public void setState(State state) {
        currentState = state;
    }

    public void processOrder() {
        if (currentState != null) {
            currentState.handle();
        } else {
            System.out.println("Состояние не задано.");
        }
    }
}
