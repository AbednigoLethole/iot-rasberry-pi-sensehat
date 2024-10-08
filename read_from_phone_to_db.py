import sqlite3
import mariadb
import time
import dash
from dash.dependencies import Output, Input
from dash import dcc, html, dcc
from datetime import datetime
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request

#------------------------------------------------------
#connecting to SQLite DB
try:
    sql_connection=sqlite3.connect('phonesensors.db')
    sql_cur=sql_connection.cursor()
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS phone_gps_coordinates_table(latitude REAL,longitude REAL,datetime TEXT)''')
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS microphone_table(sound_decibels REAL,datetime TEXT)''')
    
except:
    
  print("An exception occurred")

#---------------------------------------------------------
#connecting to Maria DB
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
maria_cur.execute('''CREATE TABLE IF NOT EXISTS phone_gps_coordinates_table
            (latitude real,longitude real,datetime text,uploaded boolean)''')

maria_cur.execute('''CREATE TABLE IF NOT EXISTS microphone_table
            (sound_decibels real,datetime text,uploaded boolean)''')
#------------------------------------------------------

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([])
@server.route("/data", methods=["POST"])

def data():
    
    sql_connection=sqlite3.connect("phonesensors.db") #change to name of your database
    sql_cur=sql_connection.cursor()
    
    # Reading gps coordinates android 
    if str(request.method) == "POST":
        data = json.loads(request.data)
        for d in data['payload']:
        #gps data
            if (d.get("name", None) == "location"):
                ts = datetime.fromtimestamp(d["time"] / 1000000000)
                latitude=d["values"]["latitude"]
                longitude=d["values"]["longitude"]
                
                print("lat: ",latitude,", longi: ",longitude,", time: ",ts)
                #inserting data into sqlite3
                sql_cur.execute("INSERT INTO phone_gps_coordinates_table(latitude, longitude,datetime) VALUES(?,?,?)",(latitude,longitude,ts))
                sql_connection.commit()
                #inserting data into mariadb
                maria_cur.execute("INSERT INTO phone_gps_coordinates_table(latitude, longitude,datetime,uploaded) VALUES(?,?,?,?)",(latitude,longitude,ts,False))
                maria_conn.commit()
                
    #---------------------------------------------------------------     
    # Reading sound decibels from android
    
    if str(request.method) == "POST":
        data = json.loads(request.data)
        for d in data['payload']:
        #microphone data   
            if (d.get("name", None) == "microphone"):
                ts = datetime.fromtimestamp(d["time"] / 1000000000)
                levels=d["values"]["dBFS"] #microphone decibels
                sound_decibels=levels
                print("sound decibel: ",sound_decibels)
                #inserting data into sqlite3
                
                sql_cur.execute("INSERT INTO microphone_table(sound_decibels,datetime) VALUES(?,?)",[sound_decibels,ts])
                sql_connection.commit()
                
                # inserting data into mariadb
                maria_cur.execute("INSERT INTO microphone_table(sound_decibels,datetime,uploaded) VALUES(?,?,?)",[sound_decibels,ts,False])
                maria_conn.commit()
                
        
                
    return "success"


if __name__ == "__main__":
    app.run_server(port=8000, host="192.168.142.215")

