import sqlite3
import mariadb
from mariadb import Error
import datetime
from read_from_emu import ReadEmuValues

read_emu_val=ReadEmuValues()

present_time = datetime.datetime.now()
print(present_time)
#--------------------------------------------
## trying to connect to SQLITE db
try:
    sql_connection=sqlite3.connect('sensehatdata.db')
    sql_cur=sql_connection.cursor()
    sql_cur.execute('''CREATE TABLE IF NOT EXISTS sensorhatdata
            (temperature real, pressure real, humidity real, datetime text,uploaded boolean)''')
    
except:
    
  print("An exception occurred")
  
#--------------------------------------------------
# Trying connect to Mariadb
  
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
maria_cur.execute('''CREATE TABLE IF NOT EXISTS sensorhatmrdata
            (temperature real, pressure real, humidity real, datetime text,uploaded boolean)''')
#--------------------------------------------------


# This fuction adds sensor db to sqlite 
def add_values_into_sqlite_db():
    sql_command='''INSERT INTO sensorhatdata(temperature, pressure, humidity, datetime,uploaded) VALUES (?,?,?,?,?); '''
    sql_values = (read_emu_val.get_temperature(),read_emu_val.get_pressure(),read_emu_val.get_humidity(),present_time,False)
    sql_cur.execute(sql_command,sql_values)
    sql_connection.commit()
    
    
def display_sensorhat_sqlite_table():
    with sql_connection:
        sql_cur.execute("SELECT * FROM sensorhatdata")
        print(sql_cur.fetchall())
        
add_values_into_sqlite_db()
display_sensorhat_sqlite_table()

# This fuction adds sensor db to mariadb
def add_values_into_mariadb():
    try:
        maria_cur.execute("INSERT INTO sensorhatmrdata (temperature, pressure,humidity,datetime,uploaded) VALUES (?,?,?,?,?)", (read_emu_val.get_temperature(),read_emu_val.get_pressure(),read_emu_val.get_humidity(),present_time,False))
        maria_conn.commit()
    except Error as e:
        print(f"Error inserting data: {e}")


    maria_conn.close()
    
add_values_into_mariadb()




