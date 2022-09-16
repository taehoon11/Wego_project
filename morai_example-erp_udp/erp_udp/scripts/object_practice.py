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
            obj_data=self.obj.get_data()
            if obj_data == []:
                obj_data = float("inf")
                print(obj_data)

            else:
                obj_data= obj_data[0]

                print(obj_data)           
             #print("obj_pos_x : {} // obj_pos_y : {}".format(obj_data[2],obj_data[3]))
            


      

if __name__ == "__main__":


    kicty=obj()
    while True :
        pass