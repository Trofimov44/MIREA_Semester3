package bikeproject;

public interface MountainParts {
    public final String TERRAIN = "off_road";
    public String getSuspension();
    public void setSuspension(String newValue);
    public String getType();
    public void setType(String newValue);
}
