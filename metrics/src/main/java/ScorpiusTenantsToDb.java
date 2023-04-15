import org.json.simple.*;
import org.json.simple.parser.*;

import java.io.File;
import java.io.FileReader;
import java.sql.*;
import java.util.Calendar;

public class ScorpiusTenantsToDb {

    private static final String ZONE_CALVIN  = "in-chennai-2";
    private static final String ZONE_HYD = "in-hyderabad-1";
    private static final String FILENAME_CALVIN = "/Users/abhishek.bkumar/Desktop/PROJECTS/paas-adoption-dashboard/metrics/src/main/resources/scorpius-calvin.txt";
    private static final String FILENAME_HYD = "/Users/abhishek.bkumar/Desktop/PROJECTS/paas-adoption-dashboard/metrics/src/main/resources/scorpius-hyd.txt";
    private static final String DATABASE_URL = "jdbc:mysql://localhost:3306/";
    private static final String DATABASE_NAME = "pass-adoption-dashboard";
    private static final String DATABASE_USER = "root";
    private static final String DATABASE_PWD = "root";
    private static final String STATE = "active";
    private static final String UPDATE_DATE = "2023-04-15";

    public static void main (String args[]){
        File directory = new File("./");
        JSONParser parser = new JSONParser();
        try{
            //Database connection
            Class.forName("com.mysql.jdbc.Driver");
            Connection con=DriverManager.getConnection(DATABASE_URL+DATABASE_NAME,DATABASE_USER,DATABASE_PWD);

            //Open JSON file
            Object obj = parser.parse(new FileReader(FILENAME_CALVIN));
            JSONObject jsonObject = (JSONObject)obj;

            //Create statement
            Statement stmt= (Statement)con.createStatement();
            String insertQuery = " insert into scorpius_tenants (tenant, appId, state, zone, update_date)"
                    + " values (?, ?, ?, ?, ?)";

            //Getting the date
            Calendar calendar = Calendar.getInstance();
            long timeMillis = calendar.getTimeInMillis();

            //Fetch and insert in the db
            for (Object o : jsonObject.keySet()) {
                String tenant = o.toString();
                JSONArray obj2 = (JSONArray)jsonObject.get(o);
                JSONObject jsonObject2 = (JSONObject)obj2.get(0);
                String appId = (String) jsonObject2.get("appId");

                //Insert in the database
                PreparedStatement preparedStmt = con.prepareStatement(insertQuery);
                preparedStmt.setString (1, tenant);
                preparedStmt.setString (2, appId);
                preparedStmt.setString   (3, STATE);
                preparedStmt.setString(4, ZONE_HYD);
                preparedStmt.setDate    (5, new Date(timeMillis));

                System.out.println(preparedStmt.toString());
                preparedStmt.execute();
            }
            //ResultSet rs=stmt.executeQuery("select * from yak_tenants");
            //while(rs.next())
                //System.out.println(rs.getInt(1)+"  "+rs.getString(2)+"  "+rs.getString(3));
            con.close();
        }   catch (Exception e) {
            System.err.println("Got an exception!");
            // printStackTrace method
            // prints line numbers + call stack
            e.printStackTrace();
            // Prints what exception has been thrown
            System.out.println(e);
        }

    }
}
