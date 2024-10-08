import datetime
from time import sleep
import paho.mqtt.publish as publish
import mariadb

mqtt_client_ID= "KAIkAwwoBjUAEwQZAyYHDhU"
username = "KAIkAwwoBjUAEwQZAyYHDhU"
password = "xg5W8yzLJy6+3Za2KAOqSKBi"
mqtt_host = "mqtt3.thingspeak.com"
topic1="channels/2113815/publish/fields/field1"
topic2="channels/2113815/publish/fields/field2"
topic3="channels/2113815/publish/fields/field3"
mqtt_port=1883

# Trying connect to Emulated sensor Mariadb  
try:
    maria_conn = mariadb.connect(
    user="abednigo",
    password="mariapass",
    host="localhost",
    port=3306,
    database="sensehatmariadb"
    )
except Error as e:
    print(f"Error connecting to MariaDB: {e}")

maria_cur = maria_conn.cursor()

def connect_and_publish():
    maria_cur.execute("SELECT * FROM sensorhatmrdata WHERE uploaded=False")
  
    for row in maria_cur:
        
        payload1 = str(row[0])
        publish.single(topic1, payload1,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        payload2 = str(row[1])
        publish.single(topic2, payload2,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        payload3 = str(row[2])
        publish.single(topic3, payload3,hostname=mqtt_host,port=mqtt_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
        timestmp=row[3]
        print("uploaded!!")
        
    maria_conn.commit()  
        
        
def change_all_upload_state():
    maria_cur.execute("UPDATE sensorhatmrdata SET uploaded = True")
    maria_conn.commit()
    print("All the data is uploaded !!")
    
    
connect_and_publish()
change_all_upload_state()
    

    
    
