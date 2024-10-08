import datetime
from time import sleep
import paho.mqtt.publish as publish
import mariadb

username = "IhULMgkdOA45LDArJBkUNBg"
mqtt_client_ID = "IhULMgkdOA45LDArJBkUNBg"
password = "0akCIxE6DLR51FTDwRtn8eM1"
mqtt_host = "mqtt3.thingspeak.com"
topic1="channels/2122169/publish/fields/field1"
topic2="channels/2122169/publish/fields/field2"
topic3="channels/2122169/publish/fields/field3"
mqtt_port=1883

# Trying connect to Emulated sensor Mariadb  
try:
    maria_conn = mariadb.connect(
    user="abednigo",
    password="mariapass",
    host="localhost",
    port=3306,
    database="phonesensemdb"
    )
except Error as e:
    print(f"Error connecting to MariaDB: {e}")

maria_cur = maria_conn.cursor()

def connect_and_publish_gps():
    maria_cur.execute("SELECT * FROM phone_gps_coordinates_table WHERE uploaded=False")
  
    for row in maria_cur:
        
        payload1 = str(row[0])
        publish.single(topic1, payload1,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        payload2 = str(row[1])
        publish.single(topic2, payload2,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        print("data uploaded!!")
        
    maria_conn.commit()
    

def connect_and_publish_sound():
    maria_cur.execute("SELECT * FROM microphone_table WHERE uploaded=False")
    for row in maria_cur:
        
        payload3 = str(row[0])
        publish.single(topic3, payload3,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        print("data uploaded!!")
        
    maria_conn.commit()
        
        
def change_all_upload_state():
    maria_cur.execute("UPDATE phone_gps_coordinates_table SET uploaded = True")
    maria_conn.commit()
    
    maria_cur.execute("UPDATE microphone_table SET uploaded = True")
    maria_conn.commit()
    print("All the data is uploaded !!")
    
    
connect_and_publish_gps()
connect_and_publish_sound()
change_all_upload_state()
    