import datetime
from time import sleep
import paho.mqtt.publish as publish
import sqlite3

#Connecting to broker
mqtt_client_ID= "IhgLHRk7AjYZCxc7BQ0SDhg"
username = "IhgLHRk7AjYZCxc7BQ0SDhg"
password = "wler5AtI7WPbxetlTFxttIDe"
topic="channels/2099062/publish"
mqtt_host = "mqtt3.thingspeak.com"


# Trying connect to Emulated sensor sqlite db
try:
    sql_connection=sqlite3.connect('sensehatdata.db')
except:
    print("An exception occurred")
    
sql_cur=sql_connection.cursor()

def connect_and_publish():
    t_transport = "websockets"
    t_port = 80
    sql_cur.execute("SELECT * FROM sensorhatdata WHERE uploaded=False")
    
    for row in sql_cur:
        payload = "field1="+str(row[0]) + "&field2=" + str(row[1])+"&field3=" + str(row[2])
        try:
            publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':username,'password':password})
            print("Data has been posted!!")
        except Exception as e:
            print(f"Error uploading to Thinkspeak: {e}")
    
    sql_connection.commit()
    
def change_all_upload_state():
    sql_cur.execute("UPDATE sensorhatdata SET uploaded = True")
    sql_connection.commit()
    print("All the data is uploaded !!")
        
    
#Running the connect and publish function
connect_and_publish()
change_all_upload_state()