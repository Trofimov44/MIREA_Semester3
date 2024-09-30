package vehicles;

public class Car extends Vehicle{

    public Car(String model,int license,String color,int year,String ownerName, int insuranceNumber, String engineType){
        super(model,license,color,year,ownerName,insuranceNumber,engineType);
    }

    public String vehicleType(){
        return "Car";
    }
}
