from sense_emu import SenseHat
import socket

sense=SenseHat()

# my student number is 3723049


class ReadEmuValues:
    
    def __init__(self):
    
        self.my_temperature=37.0
        self.my_pressure=23.0
        self.my_hum_ref_level=99.0
    
        self.emu_temp=sense.temp
        self.emu_pressure=sense.pressure
        self.emu_humidity=sense.humidity
    
    def get_temperature(self):
        return self.emu_temp
    
    def get_pressure(self):
        return self.emu_pressure
    
    
    def get_humidity(self):
        return self.emu_humidity
    
    
    def display_curr_vs_exp(self,current,expected,sensor_name):
        recom=""
        if current<expected:
            recom=" Increase "
            
        elif current>expected:
            recom=" Decrease "
            
        else:
            recom=" The values are equal"
        
        return f"sensor name: {sensor_name}, current: {current} expected: {expected}, Recommendation:{recom}"
        
    
        
    def call_display(self):
    
        print(self.display_curr_vs_exp(self.emu_temp,self.my_temperature,"Temperature"))
        print(self.display_curr_vs_exp(self.emu_pressure,self.my_pressure,"Pressure"))
        print(self.display_curr_vs_exp(self.emu_humidity,self.my_hum_ref_level,"Humidity"))

def main():
     emu_object=ReadEmuValues()
     emu_object.call_display()

     
#main()
    
        
        
    

        
    
    
    
    
