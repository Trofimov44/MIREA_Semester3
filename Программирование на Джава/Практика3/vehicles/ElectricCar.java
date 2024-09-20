package vehicles;

public class ElectricCar extends Car {
    private int batteryCapacity;

    public ElectricCar(String ownerName, int insuranceNumber, int batteryCapacity) {
        super(ownerName, insuranceNumber, null);
        this.engineType = "Electric";
        this.batteryCapacity = batteryCapacity;
    }
}
