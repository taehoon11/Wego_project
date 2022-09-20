#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
from lib.morai_udp_parser import udp_parser,udp_sender
from lib.utils import pathReader,findLocalPath,purePursuit,Point
from math import cos,sin,sqrt,pow,atan2,pi
import time
import threading
import os,json


path = os.path.dirname( os.path.abspath( __file__ ) )

with open(os.path.join(path,("params.json")),'r') as fp :
    params = json.load(fp)

params=params["params"]

user_ip = params["user_ip"]
host_ip = params["host_ip"]

change_rad_deg = 180/pi

class obj :

    def __init__(self):
        self.obj=udp_parser(user_ip, params["object_info_dst_port"],'erp_obj')
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')

        self._is_status=False
        while not self._is_status :
            if not self.status.get_data() :
                print('No Status Data Cannot run main_loop')
                time.sleep(1)
            else :
                self._is_status=True


        self.main_loop()

    
    
    def main_loop(self):
        while True:
            status_data=self.status.get_data()
            obj_data=self.obj.get_data()
            position_x=status_data[12]
            position_y=status_data[13]
            position_z=status_data[14]
            heading=status_data[17]     # degree
            velocity=status_data[18]
            #obj_data=self.obj.get_data()
            #obj_data= obj_data[0]
            #obj_pos_x = obj_data[2]
            #obj_pos_y = obj_data[3]
 #
            #
#
            #x = position_x - obj_pos_x
            #y = position_y - obj_pos_y
#
        #
            #rad = atan2(y,x)
            #deg = rad*change_rad_deg
            print(position_z)

if __name__ == "__main__":


    kicty=obj()
    while True :
        pass


