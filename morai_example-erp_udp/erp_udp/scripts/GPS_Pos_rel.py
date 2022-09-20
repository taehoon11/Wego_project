from asyncio import start_server
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
start_s = [0,0,0]
start_e = [0,0,0]
Er = 6371009
d2r = pi/180

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
        global start_s
        global start_e
        global Er
        global d2r

        while True :
            status_data=self.status.get_data()
            position_x=status_data[12]
            position_y=status_data[13]
            position_z =status_data[14]
            latitude= self.gps_parser.parsed_data[0]
            longitude= self.gps_parser.parsed_data[1]      
            position = "{} {}".format(position_x, position_y)
            if ctn == 0:
                start_s.append(position_x)
                start_s.append(position_y)
                start_s.append(position_z)
                start_e.append(Er*cos(d2r*latitude)*cos(d2r*longitude))
                start_e.append(Er*cos(d2r*latitude)*sin(d2r*longitude))
                start_e.append(Er*sin(d2r*latitude))
                ctn = ctn + 1
            else:
                z = Er*sin(d2r*latitude)
                x = Er*cos(d2r*latitude)*cos(d2r*longitude)
                y = Er*cos(d2r*latitude)*sin(d2r*longitude)
                z_tot = abs(start_e[-1] - z)
                z_s = abs(position_z - start_s[-1])
                print(latitude,longitude)



if __name__ == "__main__":

    pose=position()
    while True :
        pass

