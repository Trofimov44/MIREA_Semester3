package vehicles;

public abstract class Vehicle {
    private String model;
    private int license;
    private String color;
    private int year;
    private String ownerName;
    private int insuranceNumber;
    protected String engineType;

    public Vehicle(String model,int license,String color,int year,String ownerName, int insuranceNumber, String engineType){
        this.model = model;
        this.license = license;
        this.color = color;
        this.year = year;
        this.ownerName = ownerName;
        this.insuranceNumber = insuranceNumber;
        this.engineType = engineType;
    }

    public String toString(){
        return "{"+model+" "+license+" "+color+" "+year+" "+ownerName+" "+insuranceNumber+" "+engineType+"}";
    }

    public String vehicleType(){
        return " ";
    }

    public String getModel(){
        return model;
    }
    public int getLicense(){
        return license;
    }
    public String getColor(){
        return color;
    }
    public int getYear(){
        return year;
    }
    public String getOwnerName(){
        return ownerName;
    }
    public int getInsuranceNumber(){
        return insuranceNumber;
    }
    public String getEngineType(){
        return engineType;
    }

    public void setModel(String model){
        this.model = model;
    }
    public void setLicense(int license){
        this.license = license;
    }
    public void setColor(String color){
        this.color = color;
    }
    public void setYear(int year){
        this.year = year;
    }
    public void setOwnerName(String ownerName){
        this.ownerName = ownerName;
    }
    public void setInsuranceNumber(int insuranceNumber){
        this.insuranceNumber = insuranceNumber;
    }
    public void setEngineType(String engineType){
        this.engineType = engineType;
    }
}
