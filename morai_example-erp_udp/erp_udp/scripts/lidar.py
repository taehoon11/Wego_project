import socket
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
from lib.lidar_util import UDP_LIDAR_Parser
import os,json

path = os.path.dirname( os.path.abspath( __file__ ) )

print(path)

with open(os.path.join(path,("params.json")),'r') as fp :
    params = json.load(fp)

params=params["params"]
user_ip = params["user_ip"]
lidar_port = params["lidar_dst_port"]


params_lidar = {
    "Range" : 90, #min & max range of lidar azimuths
    "CHANNEL" : 16, #verticla channel of a lidar
    "localIP": user_ip,
    "localPort": lidar_port,
    "Block_SIZE": int(1206)
}



def main():

    udp_lidar = UDP_LIDAR_Parser(ip=params_lidar["localIP"], port=params_lidar["localPort"], params_lidar=params_lidar)

    while True :

        if udp_lidar.is_lidar ==True:            
            x=udp_lidar.x
            y=udp_lidar.y
            z=udp_lidar.z
            distance = udp_lidar.Distance
            intensity=udp_lidar.Intensity
            Target_list = [] 

            #xyz1 = np.concatenate([
            #    x.reshape([-1, 1]),
            #    y.reshape([-1, 1]),
            #    z.reshape([-1, 1])
            #], axis=1).T.astype(np.float32)
            print(distance[1400][8])  #distance(deg*10, channel_deg_idx)
        
            # for i in range(3600):
                # Target_list.append(xyz1.T[14+16*i])

            #output_file_lidar = 'lidar_dis.csv'
            #with open(output_file_lidar, 'a', newline='\r\n', encoding='UTF-8') as csvfile:
            #   # for line in lidar:
            #    csvfile.write((distance) + '\n')
#
            #break
           # print(Target_list)
            
            
           # print(xyz1.T[14],[0])




    
if __name__ == '__main__':

    main()
