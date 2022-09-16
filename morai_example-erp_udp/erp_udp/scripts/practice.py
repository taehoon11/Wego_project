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

## define variables
change_rad_deg = 180/pi   # change radian scale to degree scale
threshold = 5            # avoid threshold between car and object
first_head = 0            # memory variable for first(return) heading angle
ctn = 0                   # only for take first heading angle
return_rate = 1           # return steering angle 
avoid_rate = 1            # avoid steer angle
threshold_deg = 130       # when car avoids object it will maintane steer until degree become threshold deg
threshold_head = 5        # after the event, car's heading will return to first heading

with open(os.path.join(path,("params.json")),'r') as fp :
    params = json.load(fp)

params=params["params"]

user_ip = params["user_ip"]
host_ip = params["host_ip"]



class go_straight2 :

    def __init__(self):
        self.status=udp_parser(user_ip, params["vehicle_status_dst_port"],'erp_status')
        self.obj=udp_parser(user_ip, params["object_info_dst_port"],'erp_obj')
        self.ctrl_cmd=udp_sender(host_ip,params["ctrl_cmd_host_port"],'erp_ctrl_cmd')
        #self.traffic=udp_parser(user_ip, params["get_traffic_dst_port"],'get_traffic')
  
        self._is_status=False
        while not self._is_status :
            if not self.status.get_data() :
                print('No Status Data Cannot run main_loop')
                time.sleep(1)
            else :
                self._is_status=True


        self.main_loop()


    
    def main_loop(self):
        global ctn 
        global first_head
        self.timer=threading.Timer(0.001,self.main_loop)
        self.timer.start()
        
        status_data=self.status.get_data()
        obj_data=self.obj.get_data()
        obj_data= obj_data[0]
        
        obj_pos_x = obj_data[2]
        obj_pos_y = obj_data[3]
        position_x=status_data[12]
        position_y=status_data[13]
        heading=status_data[17]# degree

        if ctn == 0:
            first_head = heading

        x = position_x - obj_pos_x
        y = position_y - obj_pos_y

        
        rad = atan2(y,x)
        deg = rad*change_rad_deg-heading

        if deg > 180:         # make degree beloing in -180 to 180
            deg = deg - 360
        elif deg < -180:
            deg = 360 + deg

        deg_m = abs(deg)
        

        
        len_ob2car = sqrt(pow((obj_pos_x - position_x),2) + pow((obj_pos_y - position_y),2))
        ctrl_mode = 2
        Gear = 4
        cmd_type = 1
        send_velocity = 0 #cmd_type이 2일때 원하는 속도를 넣어준다.
        acceleration = 0 #cmd_type이 3일때 원하는 가속도를 넣어준다.
        accel=0.6
        brake=0
        steering_angle=0
      
        
        #print(deg)    
              
        
        if len_ob2car < threshold and deg_m > threshold_deg:
            if deg > 0 :
                steering_angle= -1*avoid_rate
                
            else:
                steering_angle= avoid_rate
                
        
        if steering_angle == 0:
            if heading > first_head + threshold_head or heading < first_head - threshold_head:
                    steering_angle = return_rate*abs(heading-60)/(heading-60)
        
        
        ctn = ctn +1
        #print(heading)
        self.ctrl_cmd.send_data([ctrl_mode,Gear,cmd_type,send_velocity,acceleration,accel,brake,steering_angle])


if __name__ == "__main__":


    kicty=go_straight2()
    while True :
        pass