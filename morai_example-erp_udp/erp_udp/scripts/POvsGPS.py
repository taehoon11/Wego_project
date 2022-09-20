import csv
from re import L
import math as m

p = open("position.csv","r",encoding="utf-8")

rdr = csv.reader(p)
pos_x = []
pos_y = []
for line in rdr:
    a = line[0].split()
    pos_x.append(float(a[0]))
    pos_y.append(float(a[1]))

p.close()

g = open("gps.csv","r",encoding="utf-8")

rdr = csv.reader(g)
lat = []
long = []
for line in rdr:
    a = line[0].split()
    lat.append(float(a[0]))
    long.append(float(a[1]))

g.close()

print("x_s : {} x_e : {}".format(pos_x[0],pos_x[-1]))
print("y_s : {} y_e : {}".format(pos_y[0],pos_y[-1]))
print("lat_s : {} lat_e : {}".format(lat[0],lat[-1]))
print("long_s : {} long_e : {}".format(long[0],long[-1]))

t1 = (pos_x[0]-pos_x[-1])**2
t2 = (pos_y[0]-pos_y[-1])**2
l = (t1+t2)**0.5

xf = abs(pos_x[0]-pos_x[-1])
angle = m.acos(xf/l)
deg = (angle*180)/m.pi
print(deg)

