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

temp_lat = 0
temp_long = 0
with open(os.path.join(path,("params.json")),'r') as fp :
    params = json.load(fp)

params=params["params"]
user_ip = params["user_ip"]
status_port = params["vehicle_status_dst_port"]
gps_port = params["gps_dst_port"]
gps_port2 = params["gps_dst_port2"]

class position :

    def __init__(self):
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')
        self.gps_parser=UDP_GPS_Parser(user_ip, gps_port,'GPRMC')
        self.gps_parser2=UDP_GPS_Parser(user_ip, gps_port2,'GPRMC')
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
        global temp_lat
        global temp_long

        while True :
                status_data=self.status.get_data()
                latitude= self.gps_parser.parsed_data[0]
                longitude= self.gps_parser.parsed_data[1]
                latitude2= self.gps_parser2.parsed_data[0]
                longitude2= self.gps_parser2.parsed_data[1]
                heading = status_data[17]

                transformer = Transformer.from_crs("epsg:4326", "epsg:5186")
                transformer2 = Transformer.from_crs("epsg:4326", "epsg:5186")
                y,x = transformer.transform(latitude,longitude)
                y2,x2 = transformer2.transform(latitude2,longitude2)
                nx = x2-x
                ny = y2-y
                head = atan2(ny,nx)*180/pi
                print(head -heading)
                    

                
                #y,x = transformer.transform(latitude,longitude)  # y(+) = East, X(+) = North
                #print(x,y)


                

                #print(x,y)
                #transformer2 = Transformer.from_crs("epsg:5186","epsg:4326")
                #lat,lon =  transformer2.transform(y,x)
                #print(latitude,longitude)
                #print("Gx = {}, x = {}".format(x-x_gap,pos_x))
                #print('Gy = {}, y = {}'.format(y-y_gap,pos_y))
                #a = atan2(y,x)
                #nx = L*cos(a)
                #ny = L*sin(a)
                #print("x = {}, y = {}".format(nx,ny))
                #nx = x*cos(70.731) - y*cos(19.126)
                #ny = x*sin(70.731) - y*sin(19.126)
                #nnx = pos_x - x
                #nny = pos_y - y
                #a = atan2(nny,nnx)
                #print(a*180/pi)

if __name__ == "__main__":

    pose=position()
    while True :
        pass

       