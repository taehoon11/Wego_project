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
"""
print("_______________")
print(path_folder_name)
print("_______________")
print(path_file_name)
print("_______________")
print(status_port)
"""

# /

class position :

    def __init__(self):
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')
        self.gps_parser=UDP_GPS_Parser(user_ip, gps_port,'GPRMC')
        #print(self.status)
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
        #self.timer=threading.Timer(0.10,self.main_loop)
        #self.timer.start()
        while True :
            status_data=self.status.get_data()
            #print(status_data)
            position_x=status_data[0]
            position_y=status_data[1]
            #wwwwwwwwwwwwwwwwwposition_z=status_data[2]
            #print("position x :{}, position_y : {}".format(position_x,position_y))
            position = "{} {}".format(position_x, position_y)
            #print(position)
            #--------------------------------------------------#
            if self.gps_parser.parsed_data!=None :
                latitude= self.gps_parser.parsed_data[0]
                longitude= self.gps_parser.parsed_data[1]
                print('Lat : {0} , Long : {1}'.format(latitude,longitude))
            gps = "{} {}".format(latitude, longitude)

            time.sleep(0.1)

            output_file_pose = 'position.csv'
            with open(output_file_pose, 'a', newline='\r\n', encoding='UTF-8') as csvfile:
               # for line in position:
                csvfile.write(str(position) + '\n')
                 #   break

            output_file_gps = 'gps.csv'
            with open(output_file_gps, 'a', newline='\r\n', encoding='UTF-8') as csvfile:
                #for line in gps:
                csvfile.write(str(gps) + '\n')
                    #break

if __name__ == "__main__":

    pose=position()
    while True :
        pass
 
