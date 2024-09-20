package vehicles;

public class Car {
    private String ownerName;
    private int insuranceNumber;
    protected String engineType;

    public Car(String ownerName, int insuranceNumber, String engineType){
        this.ownerName = ownerName;
        this.insuranceNumber = insuranceNumber;
        this.engineType = engineType;
    }

    public String getOwnerName(){
        return ownerName;
    }
    public int getInsuranceNumber(){
        return insuranceNumber;
    }
    public void setOwnerName(String ownerName){
        this.ownerName = ownerName;
    }
    public void setInsuranceNumber(int insuranceNumber){
        this.insuranceNumber = insuranceNumber;
    }

    public String getEngineType(){
        return engineType;
    }
}
