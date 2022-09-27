import os
from math import cos,sin,sqrt,pow,atan2,acos,pi

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
            #pose.append(float(postion[2]))
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
        self.is_look_forward_point= False
        mag = float("inf")
        for i in self.path :
            path_point = i
            rel_x= i[0] - vehicle_position.x
            rel_y= i[1] - vehicle_position.y
            dot_x = rel_x*cos(self.vehicle_yaw) + rel_y*sin(self.vehicle_yaw)
            dot_y = rel_x*sin(self.vehicle_yaw) - rel_y*cos(self.vehicle_yaw)
            dis=sqrt(pow(dot_x,2)+pow(dot_y,2))
            mag = dis
            if dot_x >0 :
                if dis>= self.lfd:
                    self.lfd = self.current_vel*0.25
                    if self.lfd < self.min_lfd : 
                        self.lfd=self.min_lfd
                    elif self.lfd> self.max_lfd :
                        self.lfd=self.max_lfd
                    self.forward_point=path_point
                    self.is_look_forward_point=True
                    break
        
        if dot_y > 0:
            alpha=acos(dot_x/mag)
        else:
            alpha=-1*acos(dot_x/mag)
        
        
        print('alpha :',alpha)
        if self.is_look_forward_point :
            self.steering=atan2((2*self.vehicle_length*sin(alpha)),self.lfd)
            return self.steering #deg
        else : 
            print("There is no waypoint at front")
            return 1
        


def findLocalPath(ref_path,position_x,position_y,Avoid_Radius,obj_pos_x,obj_pos_y):
    out_path=[]
    current_x=position_x
    current_y=position_y
    current_waypoint=0
    threshold = []
    t_idx_min = 0
    t_idx_max = 0

    for i in range(len(ref_path)) :
        dx = ref_path[i][0] - obj_pos_x
        dy = ref_path[i][1] - obj_pos_y
        dis = sqrt(dx*dx + dy*dy)
        if dis < Avoid_Radius+3:
            threshold.append(i)
            t_idx_min = min(threshold)
            t_idx_max = max(threshold)

    for i in range(t_idx_min,t_idx_max+300):
        pose = []
        dist = sqrt(pow((ref_path[i][0]-obj_pos_x),2)+pow((ref_path[i][1]-obj_pos_y),2)) 
        if i < t_idx_max and dist <= Avoid_Radius+3:
            newpoint_x = ref_path[i][0] - obj_pos_x
            newpoint_y = ref_path[i][1] - obj_pos_y
            L = sqrt(pow(newpoint_x,2)+pow(newpoint_y,2))
            slid_ang = atan2(newpoint_y,newpoint_x)
            newpoint_x = (Avoid_Radius-L+3)*cos(slid_ang) + newpoint_x
            newpoint_y = (Avoid_Radius-L+3)*sin(slid_ang) + newpoint_y
            
            #print(sqrt(pow((newpoint_x-ref_path[i][0]),2)+pow((newpoint_y-ref_path[i][1]),2)))
            #print("//////",Avoid_Radius)
            newpoint_x = newpoint_x + ref_path[i][0]
            newpoint_y = newpoint_y + ref_path[i][1]
            #print("ox : {}, x : {}, oy : {}, y : {}".format(ref_path[i][0],newpoint_x,ref_path[i][1],newpoint_y))
            pose.append(newpoint_x)
            pose.append(newpoint_y)
            out_path.append(pose)      
        else:
            pose.append(ref_path[i][0])
            pose.append(ref_path[i][1])              
            out_path.append(pose)
    #if current_waypoint+50 > len(ref_path) :
    #    last_local_waypoint= len(ref_path)
    #else :
    #    last_local_waypoint=current_waypoint+50

    #for i in range(current_waypoint,t_idx+1):
    #    pose=[]
    #    pose.append(ref_path[i][0])
    #    pose.append(ref_path[i][1])
    #    out_path.append(pose)

    return out_path,current_waypoint
      