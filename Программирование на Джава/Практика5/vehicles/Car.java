package vehicles;

public class Car extends Vehicle{

    public Car(String model,int license,String color,int year,String ownerName, int insuranceNumber){
        super(model,license,color,year,ownerName,insuranceNumber,null);
        this.engineType = "Combustion";
    }

    public String vehicleType(){
        return "Car";
    }
}
