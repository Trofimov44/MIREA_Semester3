package vehicles;

public class ElectricCar extends Vehicle implements ElectricVehicle {
    private int batteryCapacity;

    public ElectricCar(String model,int license,String color,int year,String ownerName, int insuranceNumber,int batteryCapacity) {
        super(model,license,color,year,ownerName,insuranceNumber,null);
        this.engineType = "electric";
        this.batteryCapacity = batteryCapacity;
    }

    public String vehicleType(){
        return "Electric Car";
    }

    public int getBatteryCapacity() {
        return batteryCapacity;
    }
    public void setBatteryCapacity(int batteryCapacity){
        this.batteryCapacity = batteryCapacity;
    }

    public String toString(){
        return "{model = "+getModel()+"; license = "+getLicense()+"; color = "+getColor()+"; year = "+getYear()+
                "; ownerName = "+getOwnerName()+ "; insuranceNumber = "+getInsuranceNumber()+
                "; engineType = "+engineType+ "; batteryCapacity = "+batteryCapacity+"}";
    }
}
