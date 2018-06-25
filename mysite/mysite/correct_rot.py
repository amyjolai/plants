#!/usr/bin/env python3
# -*- coding: utf-8 -*-q
"""
Created on Tue May  1 20:18:25 2018
q
@author: oem
"""

import matplotlib.pyplot as plt
import numpy as np
#import scipy.optimize as opt
import random as rd
#import time 
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


#### CREATING SOME COORDS
cos = np.cos
sin = np.sin

cutoffs = [2,20]
h = rd.randint(0,10)
w = rd.randint(0,10)
d = rd.randint(0,10)
O = (rd.randint(-100,100),rd.randint(-100,100), rd.randint(-100,100))

#Define points for the shape (Not needed for the main code only to demonstrate)
xs = (O[0],O[0],w+O[0],w+O[0],O[0])
ys = (O[1],O[1]+h,O[1],O[1]+h,O[1])
zs = (O[2],O[2]+d,O[2],O[2]+d,O[2])
Xs,Ys,Zs = [],[],[]
for i in range(30):
    for j in range(len(xs)):
        Xs.append(xs[j]+(i*w*rd.normalvariate(5,2)*(-1**rd.randint(0,10))))
        Ys.append(ys[j]+(i*h*rd.normalvariate(5,2)*(-1**rd.randint(0,10))))
        Zs.append(zs[j]+(i*d*rd.normalvariate(5,2)*(-1**rd.randint(0,10))))
        
coords = np.array(list(zip(np.array(Xs),np.array(Ys),np.array(Zs))))

###############################################################################


# Creates a 2D rotation matrix to rotate points (it may be more efficient to let VMD do this)
def rot_mat_2D(angle,unit='d'):
    angle *= -1
    if unit == 'd':
        angle *= np.pi/180.
    return np.matrix([[cos(angle),-sin(angle)],
                      [sin(angle),cos(angle)]])

def rot_mat_3D(angle, dim, unit='d'):
    angle *= -1
    if unit == 'd':
        angle *= np.pi/180.
    if dim =='x':
        return np.matrix([
                [1, 0,          0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle)]])
    if dim =='y':
        return np.matrix([
                [cos(angle), 0,  sin(angle)],
                [0, 1, 0],
                [-sin(angle), 0, cos(angle)]])
    if dim =='z':
        return np.matrix([
                [cos(angle), -sin(angle), 0],
                [sin(angle), cos(angle),  0],
                [0,          0,           1]])

# Finds the angle required to put the long axis of the shape along a single axis
def find_angle(coords, lens, inds):
    i,j = inds
    if lens[i] > lens[j]:
        fit = np.polyfit(coords[:,i], coords[:,j],1)
        angle = np.arctan(fit[0])
    else:
        fit = np.polyfit(coords[:,j], coords[:,i],1)
        angle = np.pi/2. - np.arctan(fit[0])
    return angle

# Finds the dimensions of the system, including the angles of rotation
def find_sys_dims(coords, angle_dim='x'):
    dims = {
    'max':[np.max(coords[:,i]) for i in range(len(coords[0]))],
    'min':[np.min(coords[:,i]) for i in range(len(coords[0]))],
            }    
    dims['lens'] = [dims['max'][i]-dims['min'][i] for i in range(len(dims['max']))]
    dims['center'] = [dims['min'][i]+dims['lens'][i]/2 for i in range(len(dims['max']))]
    return dims

sys_dims = find_sys_dims(coords)
for i in range(len(coords[1])):
    coords[:,i] -= sys_dims['center'][i]

#Xangle = find_angle(coords, sys_dims['lens'], (1,2))
#rot_mat = rot_mat_3D(Xangle, 'x','rad')
#new_coords = np.zeros(np.shape(coords))
#for i in range(len(coords)):
#    new_coords[i] = np.dot(rot_mat,coords[i])

#Yangle = find_angle(coords, sys_dims['lens'], (0,2))
#rot_mat = rot_mat_3D(Yangle, 'y','rad')
#new_coords = np.zeros(np.shape(coords))
#for i in range(len(coords)):
#    new_coords[i] = np.dot(rot_mat,coords[i])

#Zangle = find_angle(coords, sys_dims['lens'],(0,1)) #Finds Z angle
#rot_mat = rot_mat_3D(Zangle, 'z','rad')
#new_coords = np.zeros(np.shape(coords))
#for i in range(len(coords)):
#    new_coords[i] = np.dot(rot_mat,coords[i])



ax.scatter(coords[:,0], coords[:,1], coords[:,2])
ax.scatter(new_coords[:,0], new_coords[:,1], new_coords[:,2])

max_len = np.max(sys_dims['max'])
#plt.xlim(-max_len/2, max_len/2)
#plt.ylim(-max_len/2, max_len/2)
ax.set_xlabel('X',fontsize=18)
ax.set_ylabel('Y',fontsize=18)
ax.set_zlabel('Z',fontsize=18)

#print("Angle = %4.1f"%((Zangle*180)/np.pi))


#How to get angle of arbitrary shape, efficiently?

# Find min and max of x and y
# From those find width and height
# From those find the center (minX+(width/2), minY + (height/2))
# Find aprox angle of rotation by using the a least squares regression as a hueristic.
# Translate all points by center to origin (not necessary but will make things easier atm)
# Rotate point by the aprx_angle
#   If this isn't good enough (I don't think this will be necessary):
#       Draw a horizontal box to fit around the points.
#       Adjust the rotation of this box to optimise angle.

# There will be D-1 degrees of freedom to fix, where D is the number of dimensions.

