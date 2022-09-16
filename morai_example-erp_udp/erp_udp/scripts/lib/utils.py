import os
from math import cos,sin,sqrt,pow,atan2,pi

class Point() :
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class pathReader :

    def __init__(self):
       self.file_path=os.path.dirname( os.path.abspath( __file__ ) )
       self.file_path = os.path.normpath(os.path.join(self.file_path, '../..'))
 


    def read(self,file_name):
        out_path=[]
        full_file_name=self.file_path+"/path/"+file_name
        openFile = open(full_file_name, 'r')

        line=openFile.readlines()

        for i in line :
            pose=[]
            postion=i.split()
            pose.append(float(postion[0]))
            pose.append(float(postion[1]))
            pose.append(float(postion[2]))
            out_path.append(pose)
            
        openFile.close()
        return out_path




class purePursuit :
    def __init__(self):
        self.forward_point=Point()
        self.current_postion=Point()
        self.is_look_forward_point=False
        self.vehicle_length=2
        self.lfd=5
        self.min_lfd=5
        self.max_lfd=30
        self.steering=0
        
    def getPath(self,path):
        self.path=path 
 
    
    
    def getEgoStatus(self,position_x,position_y,position_z,velocity,heading):

        self.current_vel=velocity  #kph
        self.vehicle_yaw=heading/180*pi   # rad
        self.current_postion.x=position_x
        self.current_postion.y=position_y
        self.current_postion.z=position_z




    def steering_angle(self):
        vehicle_position=self.current_postion
        rotated_point=Point()
        self.is_look_forward_point= False


        for i in self.path :
            path_point=i
            dx= i[0] - vehicle_position.x
            dy= i[1] - vehicle_position.y
            rotated_point.x=cos(self.vehicle_yaw)*dx + sin(self.vehicle_yaw)*dy 
            # rotated_x axis = normal (head_dir)
            rotated_point.y=sin(self.vehicle_yaw)*dx - cos(self.vehicle_yaw)*dy
            # rotated_y axis = tangential
            if rotated_point.x>0 :
                dis=sqrt(pow(rotated_point.x,2)+pow(rotated_point.y,2))
                if dis>= self.lfd :
                    self.lfd=self.current_vel*0.3
                    if self.lfd < self.min_lfd : 
                        self.lfd=self.min_lfd
                    elif self.lfd > self.max_lfd :
                        self.lfd=self.max_lfd
                    self.forward_point=path_point
                    self.is_look_forward_point=True
                    break
        
        theta=atan2(rotated_point.y,rotated_point.x)

        if self.is_look_forward_point :
            self.steering=atan2((2*self.vehicle_length*sin(theta)),self.lfd)
            return self.steering #deg
        else : 
            print("There is no waypoint at front")
            return 1
        


def findLocalPath(ref_path,position_x,position_y):
    out_path=[]
    current_x=position_x
    current_y=position_y
    current_waypoint=0
    min_dis=float('inf')

    for i in range(len(ref_path)) :
        dx=current_x - ref_path[i][0]
        dy=current_y - ref_path[i][1]
        dis=sqrt(dx*dx + dy*dy)
        if dis < min_dis :
            min_dis=dis
            current_waypoint=i

    if current_waypoint+50 > len(ref_path) :
        last_local_waypoint= len(ref_path)
    else :
        last_local_waypoint=current_waypoint+50

    for i in range(current_waypoint,last_local_waypoint) :
        pose=[]
        pose.append(ref_path[i][0])
        pose.append(ref_path[i][1])
        out_path.append(pose)

    return out_path,current_waypoint
      
def my_pure_pursuit(position_x,position_y,local_path,heading,velocity):

    for i in local_path:
        head = heading*pi/180
        car_len = 2
        ld = 5
        min_d = 5
        max_d = 30
        find_wp = False
        new_coord_x = i[0] - position_x
        new_coord_y = i[1] - position_y
        new_coord_x = (new_coord_x)*cos(head) + (new_coord_y)*sin(head)
        new_coord_y = (new_coord_x)*sin(head) - (new_coord_y)*cos(head)
        if new_coord_x > 0:
            dist = sqrt(pow(new_coord_x,2)+pow(new_coord_y,2))
            if dist >= ld:
                ld = velocity*0.3
                if ld < min_d:
                    ld = min_d
                elif ld > max_d:
                    ld = max_d
                find_wp = True
                break

    alpha = atan2(new_coord_y,new_coord_x)

    if find_wp:
        steer = atan2(2*car_len*sin(alpha),ld)
        return steer
    else: 
        print("Can't find any Waypoint")
        print("I'll ready for find")
        return 1


    
