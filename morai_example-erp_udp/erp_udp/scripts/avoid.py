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

class go_straight :

    def __init__(self):
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')
        self.obj=udp_parser(user_ip, params["object_info_dst_port"],'erp_obj')
        self.ctrl_cmd=udp_sender(host_ip,params["ctrl_cmd_host_port"],'erp_ctrl_cmd')
        
        self._is_status=False
        while not self._is_status :
            if not self.status.get_data() :
                print('No Status Data Cannot run main_loop')
                time.sleep(1)
            else :
                self._is_status=True


        self.main_loop()
    
    def main_loop(self):
        self.timer=threading.Timer(0.001,self.main_loop)
        self.timer.start()
        
        status_data=self.status.get_data()
        obj_data=self.obj.get_data()
        obj_data= obj_data[0]
        threshold = 5
        
        obj_pos_x = obj_data[2]
        obj_pos_y = obj_data[3]
        position_x=status_data[12]
        position_y=status_data[13]

        
        len_ob2car = sqrt(pow((obj_pos_x - position_x),2) + pow((obj_pos_y - position_y),2))
        ctrl_mode = 2
        Gear = 4
        cmd_type = 1
        send_velocity = 0 
        acceleration = 0 
        accel=1
        brake=0
        steering_angle=0
      
        
        
        if len_ob2car < threshold:
            Gear = 1
            print("Object derect, Change Parking mode")


        self.ctrl_cmd.send_data([ctrl_mode,Gear,cmd_type,send_velocity,acceleration,accel,brake,steering_angle])


if __name__ == "__main__":


    kicty=go_straight()
    while True :
        pass