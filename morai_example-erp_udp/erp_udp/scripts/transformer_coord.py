from pyproj import Transformer
from lib.morai_udp_parser import udp_parser
from lib.gps_util import UDP_GPS_Parser
import time
import threading
from math import cos,sin,sqrt,pow,atan2,pi
import os,json
import sys
import numpy as np


path = os.path.dirname( os.path.abspath( __file__ ) )

with open(os.path.join(path,("params.json")),'r') as fp :
    params = json.load(fp)

params=params["params"]
user_ip = params["user_ip"]
status_port = params["vehicle_status_dst_port"]
gps_port = params["gps_dst_port"]

ctn = 0
class position :

    def __init__(self):
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')
        self.gps_parser=UDP_GPS_Parser(user_ip, gps_port,'GPRMC')
        self._is_status=False
        print(not self._is_status)
        
        while not self._is_status :
            if not self.status.get_data() :
                print('No Status Data Cannot run main_loop')
                time.sleep(1)
            else :
                self._is_status=True
                
        self.main_loop()



    
    def main_loop(self):
        global ctn
   
        while True :
                status_data=self.status.get_data()
                latitude= self.gps_parser.parsed_data[0]
                longitude= self.gps_parser.parsed_data[1]
                posx = status_data[12]
                posy = status_data[13]
                heading = status_data[17]

                

                transformer = Transformer.from_crs("epsg:4326", "epsg:5186")
                y,x = transformer.transform(latitude,longitude)
                head = atan2(ny,nx)*180/pi
                print(head -heading)


                


if __name__ == "__main__":

    pose=position()
    while True :
        pass

first_pos_x = 13.661380767822266
first_pos_y = 1100.2760009765625
first_lat = 37.23923666666667
first_lon = 126.77316

second_pos_x = 143.71762084960938 
second_pos_y = 1429.3104248046875
second_lat =  37.24222833333333 
second_lon = 126.77453833333333
 
transformer = Transformer.from_crs("epsg:4326", "epsg:5186")
h1,v1 = transformer.transform(first_lat,first_lon)



s_ox = h1 - first_pos_x 
s_oy = v1 - first_pos_y

transformer2 = Transformer.from_crs("epsg:5186","epsg:4326")
h2,v2 = transformer2.transform(s_ox,s_oy)
print(h2,v2)


transformer3 = Transformer.from_crs("epsg:4326", "epsg:5186")
h3,v3 = transformer3.transform(second_lat,second_lon)

s_ox2 = h3 - second_pos_x
s_oy2 = v3 - second_pos_y

transformer4 = Transformer.from_crs("epsg:5186","epsg:4326")
h4,v4 = transformer4.transform(s_ox2,s_oy2)
print(h4,v4)
print(sqrt(pow((first_pos_x - second_pos_x),2) + pow((first_pos_y - second_pos_y),2)))
print(sqrt(pow((s_ox - s_ox2),2) + pow((s_oy - s_oy2),2)))







#b = atan2(v,h)*180/pi
#
#gap = s - b
#
#
#
## Rotation calib transfer GPS to Simulation coordinate x = hcos(gap) - vsin(gap) /// y = hsin(gap) + vcos(gap)
#newx = h1*cos(gap*pi/180) - v1*sin(gap*pi/180)
#newy = h1*sin(gap*pi/180) + v1*cos(gap*pi/180)
#x_gap = newx - first_pos_x
#y_gap = newy - first_pos_y
#
##print("Gx = {}, Gy = {}".format(newx,newy))
##print("simulx = {}, ximuly = {}".format(first_pos_x,first_pos_y))
## Translation Calib GPS to Simulation 
#
##final check
#
#newx2 = h2*cos(gap*pi/180) - v2*sin(gap*pi/180)
#newy2= h2*sin(gap*pi/180) + v2*cos(gap*pi/180)
#
#newx2 = newx2 -x_gap
#newy2 = newy2 - y_gap
##print(newx2,newy2)
##print(second_pos_x,second_pos_y)
#
#
## Check Short Case
#
#lat3 = 37.241006666666664 
#long3 =126.77431666666668
#x3 =120.94163513183594
#y3 =1294.2222900390625
#
#transformer3 = Transformer.from_crs("epsg:4326", "epsg:5186")
#h3,v3 = transformer3.transform(lat3,long3)
#newx3 = h3*cos(gap*pi/180) - v3*sin(gap*pi/180)
#newy3 = h3*sin(gap*pi/180) + v3*cos(gap*pi/180)
#newx3= newx3 -x_gap
#newy3 = newy3 - y_gap
#print(newx3,newy3)
#print(x3,y3)